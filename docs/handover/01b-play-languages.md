# Handover 01b: Play is keyed by language, not country

Read `AGENTS.md` first. Small follow-up to phase 01 after Claude's review. Phase 01 passed; this
fixes one modeling error it exposed and widens coverage. No LLM calls, no site work.

## Why

Your own volume report shows it: `en-IN` and `en-GB` returned the same 5,852 review ids as `en-US`,
and `es-ES` the same 1,913 as `es-MX`. Google Play serves reviews by **language**. The country in
the pair does nothing. Two consequences:

1. The `country` column is wrong for every Android row. `us` there means "written in English",
   `mx` means Spanish, `ae` means Arabic. That column will ship in a public CSV, so it has to go.
2. We only collected the 15 languages that happened to be in the pair list, and spent three full
   streams (about 12,600 fetched rows) re-downloading duplicates.

## Changes

### Config

Replace `PLAY_PAIRS` with `PLAY_LANGS`, a tuple of language codes, and one constant
`PLAY_COUNTRY = "us"` passed to the library on every call. Languages, in this order:

```
en, es, pt, fr, ar, id, ru, de, ko, it, th, vi, tr, ja, hi,
nl, pl, sv, da, nb, fi, cs, el, hu, ro, uk, bg, hr, sk, sr,
iw, fa, ur, bn, ta, te, mr, ms, fil, zh-TW, zh-CN, ca
```

If Play rejects a code or returns the same ids as another code, don't guess a replacement. Keep the
stream in the report with its real result and say so.

### Schema

New column order for `data/raw_reviews.csv`:

```
review_id, platform, country, store_lang, timestamp, date_utc, rating, title,
review_text, app_version, thumbs_up, has_dev_reply
```

- `store_lang`: for Android, the Play language code of the first stream that returned the review.
  Empty for iOS.
- `country`: iOS storefront as before. **Empty for Android.**
- Update `validate_row` to enforce exactly that (Android: empty country, non-empty store_lang;
  iOS: two-letter country, empty store_lang).

### Volume report

- "By country and platform" becomes two tables: iOS by storefront, Android by `store_lang`.
- Play contributions table is per language.
- Add one line under "Date ranges": hours between run time and the newest review per platform.
  (Claude measured about 24 hours on Android against a live fetch. Play publishes with a lag, so the
  final day is always partial. Just report the number.)

### Gitignore

`data/` is ignored wholesale, but the final CSVs get committed later. Ignore only
`data/interim/`, `data/run_logs/`, and `data.run1/`.

### Tests

Update fixtures and tests for the new column and validation rules. Add one test that an Android row
with a non-empty country fails validation, and one that two languages returning the same review id
keep the first language. `pytest` passes offline.

## Run it

`ensure_run` refuses a changed config against an existing data dir, which is correct. Move the
current `data/` to `data.run1/` (keep it, don't delete), then run both scrapers and the merge fresh.
Free, no keys.

## Done when

- [ ] `pytest` passes offline
- [ ] `data/raw_reviews.csv` has the 12 columns above; every Android row has empty `country` and a
      `store_lang`; every iOS row the reverse; zero duplicate ids; at most 20,000 rows
- [ ] Volume report regenerated with the per-language table and the lag line
- [ ] `docs/handover/01b-report.md`: rows per language, any code that was rejected or duplicated
      another, whether the 20k cap triggered, and real command output

## Leave alone

These came up in review and are accepted as they are:

- Patching `google_play_scraper` private functions to surface swallowed errors. Fragile across
  versions, but the version is pinned and the failure path is tested.
- US iOS history starting Jul 29 because the feed stops at 10 pages. Source limit. Claude handles it
  in the charts.
- Stopping on the first page that is entirely older than the window.

Don't commit. Don't start annotation.
