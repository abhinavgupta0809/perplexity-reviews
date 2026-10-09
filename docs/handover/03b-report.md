# Phase 03b report: polish before deploy

Completed `03b-polish.md` on 2026-10-09. All twelve items and both “Also” items are implemented. Offline pytest passes; the rebuilt site passed headless Chrome checks on all four tabs at 1440px and 375px with zero captured page console errors. No API call, commit, or deployment was performed.

## Changes

- `site/app.js`: shared review-card polish, language names with fallback, helpful-count visibility, Most helpful default, topic threshold, Deep Dive hash selection/restoration, and explicit sentiment methodology.
- `site/styles.css`: exclusive desktop/mobile group selectors, consistent hidden-element behavior, a Reviews filter grid, and responsive three-column signal charts.
- `site/charts.js`: a per-chart rating-axis minimum; only the weekly rating/sentiment line uses the raised minimum.
- `pipeline/build_site_data.py`: computed `nonsense_count` in scoped statistics, generated topic/axis settings, and mode 644 on all five generated files before publication.
- `tests/test_site_data.py`: hand-worked Nonsense exclusion/count assertions for all/Android/iOS and generated permission checks alongside the existing deterministic-build/CSV-copy test.
- Root `README.md`: a “Deploy” section identifying the static `site/` folder, no build step, and `cd site && vercel deploy --prod`. That command was not run.
- Rebuilt `site/data/*.json` and both downloadable CSV copies.

## Twelve-item verification

| Item | Implementation and verification |
| --- | --- |
| 1. Exclusive Deep Dive selectors | The sidebar-specific selector overrides shared field styling. Chrome verified list-only at 1440px and 640px, select-only at 375px and 639px. |
| 2. More only for clamped text | Measure rendered scrollHeight/clientHeight after render, translation changes, window resize, and container resize. Chrome checked visibility against actual overflow at both target widths, expanded More to Less, confirmed a three-word review has no More, and resized existing cards to verify changed visibility. A global hidden rule prevents button display styles overriding hidden. |
| 3. No zero helpful count | Shared cards append helpful metadata only above zero. Chrome inspected Reviews cards at both widths for absence of “0 helpful”; cards in all lists share this implementation. |
| 4. Language names | `Intl.DisplayNames` supplies names in chart labels, filter choices, and review tags; `und` is explicitly Undetermined and Other remains Other. Chrome verified English/Undetermined and then reloaded with DisplayNames disabled to verify safe code fallback. |
| 5. Reviews filter alignment | Removed the redundant Platform field. Labels sit above their inputs/selects in one responsive grid; the checkbox keeps its adjacent label. Chrome verified no Platform field, equal 40px control heights, and no horizontal overflow; desktop/mobile screenshots were visually inspected. |
| 6. Most helpful default | Both initial Reviews state and Clear filters use helpful sorting. Chrome verified the default selected sort at both widths; desktop screenshot shows the most helpful reviews first. Existing timestamp/ID tie-breaking remains. |
| 7. Signal chart columns | A dedicated signal-chart grid uses three equal columns at 1100px and above, one below. Chrome checked computed columns at 1099px, 1100px, and 1440px; mobile remains one column. |
| 8. Useful top topics | Only scoped topic counts at least the generated threshold show. Chrome compared Answer Accuracy chips to qualifying source statistics and selected an iOS category with no qualifying topics to verify the whole block disappears. Builder retains its existing top-ten data. |
| 9. Weekly line axis | Only the weekly stars/sentiment model supplies a minimum of 3; subtitle states “y-axis starts at 3.” Chrome inspected the line scale as 3–5 and the mean-star bar scales as their full 1–5 range. |
| 10. Deep Dive hash | Navigation writes platform, mode, and encoded selected group, including the initial selection. Chrome verified category/group selection, the supplied iOS Credits URL, reload restoration, unknown-mode/group fallback, and desktop list/mobile select changes. Hash changes to a different group reset stale detail filters. |
| 11. Sentiment method | Builder computes scoped Nonsense counts: all 367, Android 347, iOS 20. The Average sentiment tile uses the current scope; the footer method line uses the corpus total. Chrome verified both explanations against generated data; offline assertions verify scoped counts and unchanged exclusion arithmetic. |
| 12. Hide off-topic text | Every list uses one review component that inserts only the hidden notice and Show button for Nonsense-labeled reviews. Title, body/translation, and topic are not inserted until Show. Chrome tested real Reviews and Deep Dive cards at both widths, then a synthetic Nonsense row in the drawer, including explicit Show. Both CSV copies remain byte-identical to source; review JSON bytes and analytical counts remain unchanged apart from new descriptive statistics. |

## Commands and real results

### Offline tests and JavaScript syntax

```text
$ PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q
........................................................................ [ 40%]
........................................................................ [ 81%]
................................                                         [100%]
176 passed in 3.45s
```

Tests remain offline through the existing socket-blocking fixture. No dependency was added.

```text
$ node --check site/app.js
exit 0, no output
$ node --check site/charts.js
exit 0, no output
```

The app syntax check was also rerun after the final hash change and exited 0.

### Rebuild

```text
$ PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.build_site_data
Built 14791 reviews; 12 complete UTC Monday weeks; scopes: all, android, ios
Matcher c_money: 1059
Matcher c_accuracy: 444
Matcher c_regression: 235
Matcher c_lowsignal: 5115
Matcher c_ios: 424
Matcher i_credits: 202
Matcher i_free_images: 161
Matcher i_free_questions: 507
Matcher i_wrong: 444
Matcher i_ignores: 73
Matcher i_cancel: 120
Matcher i_promos: 57
Matcher i_bugs: 228
Matcher i_style: 177
Matcher i_voice: 117
Matcher i_history: 84
Matcher i_support: 71
Matcher i_computer: 68
Matcher i_models: 69
Matcher i_login: 60
Matcher i_preinstalled: 63
Matcher f_free_uploads: 89
Matcher f_pricing: 50
Matcher f_search: 22
Matcher f_ui: 21
Matcher f_voice: 19
Matcher f_threads: 19
Matcher f_computer: 13
Matcher f_models: 12
Matcher s_research: 556
Matcher s_sources: 550
Matcher s_study: 308
Matcher s_accuracy: 730
Matcher s_speed: 464
Matcher s_models: 44
summary.json: raw=102459 bytes; gzip=21394 bytes
insights.json: raw=1039296 bytes; gzip=369367 bytes
reviews.json: raw=3896796 bytes; gzip=1247473 bytes
raw_reviews.csv: 2371800 bytes
annotated_reviews.csv: 3874724 bytes
```

All 35 expected matcher counts still pass the real-corpus regression test. Gzip sizes are computed with fixed mtime, not additional generated gzip assets.

A second build under private umask 077 compared SHA-256 hashes of all five outputs and asserted their file modes. Its command used `.venv/bin/python -c` to set/restore the umask around `build(arguments([]))` and exited 0:

```text
Rebuild under umask 077: five output files byte-identical and mode 644
```

The separate input-integrity/CSV verification command exited 0:

```text
Protected inputs unchanged: 24
Nonsense counts: {'all': 367, 'android': 347, 'ios': 20}
Generated modes: {'site/data/summary.json': '0o644', 'site/data/reviews.json': '0o644', 'site/data/insights.json': '0o644', 'site/raw_reviews.csv': '0o644', 'site/annotated_reviews.csv': '0o644'}
Both CSV copies byte-identical
```

The protected snapshot covers AGENTS.md, preexisting Markdown under docs, analysis inputs, and top-level data files. No Claude-owned file or source corpus was edited.

### Browser checks

Used the installed Chrome with an isolated temporary profile, the existing local venv HTTP server, and a Node helper using Chrome DevTools Protocol. No browser/test package was installed.

```sh
.venv/bin/python -m http.server 8783 --bind 127.0.0.1 --directory site
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless=new --remote-debugging-port=9783 --user-data-dir=/private/tmp/perplexity-03b-chrome --no-first-run --no-default-browser-check --disable-gpu --window-size=1440,1000 about:blank
node /private/tmp/perplexity-03b-browser.mjs
```

The final helper run exited 0. It starts from about:blank so the final source is loaded fresh. Runtime exceptions, console errors, and browser log errors were captured; all eight tab/viewport combinations recorded zero errors. Chart.js reported 4.4.1. Results and helper source are retained in gitignored run logs:

- [Browser results](../../data/run_logs/03b-browser-results.json)
- [Browser helper](../../data/run_logs/03b-browser-smoke.mjs)
- [Desktop screenshot](../../data/run_logs/03b-desktop.png)
- [Mobile screenshot](../../data/run_logs/03b-mobile.png)

Both screenshots were visually inspected. The drawer test intercepts reviews.json in Chrome memory with one safe synthetic Nonsense row; it never changes a file or reports review bodies. That interception and the DisplayNames override were removed, and the page was reloaded afterward. The owned HTTP server and Chrome sessions were interrupted after verification; both exited 0.

## Failures and limits

The first pytest run failed: 1 failed, 175 passed in 3.65s. The new permission code treated the atomic writer's `handle.name` as a pathname, but its underlying fdopen handle exposes an integer descriptor. Corrected it to `os.fchmod(handle.fileno(), 0o644)` before atomic replacement, then reran the entire suite successfully. JSON temporary files now publish as 644; exact CSV copies receive the same mode before replacement.

The initial sandbox HTTP server failed with `PermissionError: [Errno 1] Operation not permitted`; the initial browser helper failed with localhost `connect EPERM`. Both succeeded after requesting the required sandbox escalation. Native Chrome stderr included allocator, CVDisplayLink, and background-service diagnostics; the page's captured error channels were clean.

Safari, Firefox, real touch devices, screen readers, and deployment were not tested. The existing phase-03 drawer focus-trap/theme/table behavior was not exhaustively rerun; this pass checks the current handover's requested interactions and scoped rendering. The browser width tests are CSS viewports in installed headless Chrome. No API/model-quality work was performed. The root deployment command is documentation only.

No blocking issue or open question remains for this phase. The request to keep Nonsense rows in every number was interpreted as preserving existing analytical counting and the existing sentiment exclusion explicitly required by item 11; masking changes only initial presentation, never corpus/download contents.

## Done when

- [x] Pytest passes offline: 176 tests.
- [x] All twelve items done, each verified above.
- [x] This report records changes, real commands/output, failures, limits, and decisions.

Stopped at phase 03b completion. No commit or deployment.
