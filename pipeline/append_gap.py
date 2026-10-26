"""Append a later scrape to the existing corpus without touching what is already there.

The base corpus (data/) keeps every row it has, unchanged. From a completed later scrape
(a fresh --data-dir, e.g. data.gap-2026-10-25/), this adds only review IDs the base does not
have, dated after the base's newest review on that platform through the later run time.
Nothing is resampled: the merged corpus is every base row plus every new row, sorted the
way merge.py sorts, so the window grows and no cap applies.

New IDs dated at or before the base's newest review on their platform ("late-arriving":
the store published them after the base scrape) are left out by default, because adding
them would change counts for days the base already reported. --include-late adds them.

--platforms limits the append to some platforms. A platform not appended keeps its base
coverage, and run.json records that, with --not-extended-note saying why. The site labels
each platform's date range from this.

Writes to the base directory:
- raw_reviews.csv: base rows + new rows, (timestamp, review_id) order.
- daily_true_counts.csv: recomputed per platform/UTC day from the merged corpus. The base run
  was never capped, so its daily counts equal its corpus counts; this is checked first.
- run.json: run time of the later scrape, the base window start, per-platform coverage, and
  a `composition` list naming both runs.
- volume_report.md: an append section on top, the base run's report kept below it.

Annotation is a separate step: run pipeline.annotate on the new raw CSV. Its cache is keyed
by normalized text, so base rows hit the cache and only new texts are sent.

    .venv/bin/python -m pipeline.append_gap --gap-dir data.gap-2026-10-25 --platforms android --dry-run
"""
import argparse
from collections import Counter
import csv
from datetime import timedelta
from pathlib import Path

from . import config
from .annotate import load_raw
from .common import ScrapeError, atomic_text, cli, dt, read_json, validate_row, write_json
from .merge import load_sources, table

PLATFORMS = ("android", "ios")
SOURCE = {"android": "play", "ios": "appstore"}


def read_daily(path):
    with Path(path).open(encoding="utf-8", newline="") as handle:
        return {(r["platform"], r["date_utc"]): int(r["count"]) for r in csv.DictReader(handle)}


def plan(base_rows, base_manifest, gap_rows, gap_run_time, platforms=PLATFORMS, include_late=False):
    if any(part.get("run_time_utc") == gap_run_time for part in base_manifest.get("composition", [])):
        raise ScrapeError("This later run is already appended to the base corpus; nothing to do")
    if dt(gap_run_time) <= dt(base_manifest["run_time_utc"]):
        raise ScrapeError("Later run time must be after the base run time")
    base_ids = {r["review_id"] for r in base_rows}
    window_start = base_manifest.get("window_start_utc") or (
        dt(base_manifest["run_time_utc"]) - timedelta(days=base_manifest["settings"]["window_days"])
    ).isoformat().replace("+00:00", "Z")
    newest = {p: max((r["timestamp"] for r in base_rows if r["platform"] == p), default=window_start) for p in PLATFORMS}
    added, late, seen = [], [], set()
    for row in gap_rows:
        validate_row(row)
        if row["platform"] not in platforms or row["review_id"] in base_ids or row["review_id"] in seen or not row["review_text"].strip():
            continue
        if not dt(window_start) <= dt(row["timestamp"]) <= dt(gap_run_time):
            continue
        seen.add(row["review_id"])
        if dt(row["timestamp"]) <= dt(newest[row["platform"]]):
            late.append(row)
            if not include_late:
                continue
        added.append(row)
    merged = sorted([*base_rows, *added], key=lambda r: (r["timestamp"], r["review_id"]))
    return {"window_start": window_start, "base_newest": newest, "added": added, "late": late,
            "late_included": include_late, "merged": merged}


def summary_rows(rows):
    out = []
    for platform in PLATFORMS:
        group = sorted(r["date_utc"] for r in rows if r["platform"] == platform)
        out.append((platform, len(group), group[0] if group else "", group[-1] if group else ""))
    return out


def report(base_manifest, gap_run_time, gap_meta, result, base_report, platforms, note):
    added, late = result["added"], result["late"]
    added_ids = {r["review_id"] for r in added}
    streams = [(s.get("lang") or s.get("locale"), s.get("rows_fetched", ""), s.get("in_window_rows", ""), s.get("stop_reason", ""))
               for meta in gap_meta.values() for s in meta["streams"]]
    skipped = [p for p in PLATFORMS if p not in platforms]
    return "\n\n".join([
        "# Review volume report (merged corpus)",
        f"Corpus window: {result['window_start']} through {gap_run_time}, inclusive, for "
        + ", ".join(platforms) + (f"; {', '.join(skipped)} keeps the base run's coverage (through {base_manifest['run_time_utc']})" if skipped else "")
        + ". Uncapped: every review kept, nothing sampled.",
        f"Built by appending a later scrape (run time {gap_run_time}) to the base corpus (run time {base_manifest['run_time_utc']}) "
        "with pipeline/append_gap.py. Base rows and their annotations are unchanged. Only review IDs absent from the base, "
        "dated after the base's newest review on their platform, were added.",
        *([f"Not extended: {', '.join(skipped)}. {note}"] if skipped and note else []),
        "## Merged corpus",
        table(("Platform", "Reviews", "First day", "Last day"), summary_rows(result["merged"])),
        "## Kept from the base run",
        table(("Platform", "Reviews", "First day", "Last day"), summary_rows([r for r in result["merged"] if r["review_id"] not in added_ids])),
        "Newest base review per platform: " + ", ".join(f"{p} {t}" for p, t in result["base_newest"].items()) + ".",
        "## Added from the later run",
        table(("Platform", "Reviews", "First day", "Last day"), summary_rows(added)),
        f"{len(late)} further new IDs are dated at or before the base's newest review on their platform (published by the "
        f"store after the base scrape). They were {'added' if result['late_included'] else 'left out, so counts for days the base already reported do not change'}.",
        "Later-run feed coverage per stream (rows fetched, in-window rows for the later run's own 90-day pull, stop reason):",
        table(("Stream", "Fetched", "In window", "Stop"), streams),
        "`daily_true_counts.csv` is recomputed from the merged corpus. Days up to the base run reflect the base scrape; "
        "later days reflect the later scrape for the appended platforms only.",
        "---",
        "# Base run report (unchanged, as generated at the base run)",
        base_report.split("\n", 1)[1] if base_report.startswith("# ") else base_report,
    ]).rstrip() + "\n"


def run(args):
    base_rows = load_raw(args.base_dir / "raw_reviews.csv")
    base_manifest = read_json(args.base_dir / "run.json")
    gap_manifest = read_json(args.gap_dir / "run.json")
    gap_run_time = gap_manifest["run_time_utc"]
    platforms = tuple(p for p in PLATFORMS if p in args.platforms)
    gap_rows, gap_meta = load_sources(args.gap_dir, gap_run_time, tuple(SOURCE[p] for p in platforms))
    base_daily = read_daily(args.base_dir / "daily_true_counts.csv")
    if base_daily != Counter((r["platform"], r["date_utc"]) for r in base_rows):
        raise ScrapeError("Base daily true counts differ from base corpus counts (was it capped?); refusing to recompute")
    result = plan(base_rows, base_manifest, gap_rows, gap_run_time, platforms, args.include_late)
    for name, rows in (("Base", base_rows), ("Added", result["added"]), ("New IDs dated inside base coverage (late)", result["late"]), ("Merged", result["merged"])):
        print(f"{name}: " + "; ".join(f"{p} {n} ({a} to {b})" for p, n, a, b in summary_rows(rows)))
    if args.dry_run:
        print("Dry run: no files written")
        return result
    if not result["added"]:
        raise ScrapeError("Later run adds zero new reviews; nothing written")
    if dt(gap_run_time) - dt(result["window_start"]) > timedelta(days=config.WINDOW_DAYS) or len(result["merged"]) > config.MAX_ROWS:
        raise ScrapeError("Merged corpus exceeds config WINDOW_DAYS or MAX_ROWS; raise them so the config describes the corpus")
    base_coverage = base_manifest.get("platform_coverage") or {p: {"through_run_utc": base_manifest["run_time_utc"]} for p in PLATFORMS}
    coverage = {p: ({"through_run_utc": gap_run_time} if p in platforms else
                    base_coverage[p] | ({"not_extended": {"run_time_utc": gap_run_time, "note": args.not_extended_note,
                                                         "summary": args.not_extended_summary, "checked_on": args.not_extended_checked_on}}
                                        if args.not_extended_note else {}))
                for p in PLATFORMS}
    manifest = {
        "run_time_utc": gap_run_time,
        "window_start_utc": result["window_start"],
        "platform_coverage": coverage,
        "settings": gap_manifest["settings"] | {"window_days": config.WINDOW_DAYS, "max_rows": config.MAX_ROWS},
        "composition": [
            *base_manifest.get("composition", [{"run_time_utc": base_manifest["run_time_utc"], "settings": base_manifest["settings"], "rows": len(base_rows), "role": "base"}]),
            {"run_time_utc": gap_run_time, "settings": gap_manifest["settings"], "rows": len(result["added"]), "platforms": list(platforms),
             "late_ids_included": args.include_late, "role": "appended (new IDs only)"},
        ],
    }
    base_report = (args.base_dir / "volume_report.md").read_text(encoding="utf-8")
    with atomic_text(args.base_dir / "volume_report.md") as handle:
        handle.write(report(base_manifest, gap_run_time, gap_meta, result, base_report, platforms, args.not_extended_note))
    with atomic_text(args.base_dir / "daily_true_counts.csv") as handle:
        writer = csv.writer(handle)
        writer.writerow(("platform", "date_utc", "count"))
        writer.writerows((p, d, n) for (p, d), n in sorted(Counter((r["platform"], r["date_utc"]) for r in result["merged"]).items()))
    with atomic_text(args.base_dir / "raw_reviews.csv") as handle:
        writer = csv.DictWriter(handle, fieldnames=config.COLUMNS)
        writer.writeheader()
        writer.writerows(result["merged"])
    write_json(args.base_dir / "run.json", manifest)
    print(f"Wrote {len(result['merged'])} rows ({len(result['added'])} added) to {args.base_dir / 'raw_reviews.csv'}; "
          "daily_true_counts.csv, run.json, volume_report.md updated. Next: pipeline.annotate --dry-run")
    return result


def arguments(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--base-dir", type=Path, default=config.DATA_DIR)
    parser.add_argument("--gap-dir", type=Path, required=True)
    parser.add_argument("--platforms", nargs="+", choices=PLATFORMS, default=list(PLATFORMS))
    parser.add_argument("--include-late", action="store_true")
    parser.add_argument("--not-extended-note", default="", help="Why a platform was not appended (volume report, run.json)")
    parser.add_argument("--not-extended-summary", default="", help="Short reason the site shows, e.g. \"Apple's review feed returned almost nothing\"")
    parser.add_argument("--not-extended-checked-on", default="", help="UTC date the skipped platform was tried, YYYY-MM-DD")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(argv)


def main():
    run(arguments())


if __name__ == "__main__":
    cli(main)
