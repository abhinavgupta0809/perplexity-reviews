# Phase 03 report: site data and local dashboard

Date: 2026-10-09. Phase 03 is complete. The dashboard is implemented in vanilla HTML/CSS/JS, all 176 offline tests pass, all 35 current-corpus matcher counts match the handover, and every tab loaded in an isolated headless Chrome browser with zero captured page console/runtime errors. No annotation/model API calls, commits, pushes, deployments, or next-phase work were performed. The local QA server and isolated Chrome process were stopped after verification.

## What was built

- `pipeline/build_site_data.py`: offline input validation, exact AND matcher semantics, per-scope matches and token expansion, complete Monday/UTC weeks, all required aggregates, gold agreement parsing, compact reviews, and exact CSV copies. All payloads are prepared and validated before writes; JSON files publish atomically. Unknown match keys/enums/regexes/tokens and zero-all-scope matches fail clearly.
- `tests/test_site_data.py`: hand-worked six-review fixture derived from a saved identity-free fixture; field-by-field/combined matching, failure cases, tokens, scope separation, null means, both week boundaries, daily true-count provenance, multi-category counts, topic ordering/top-ten limit, language grouping, version order/cutoff, gold parsing, deterministic builds, exact copies, and the full expected-count table. The real-corpus test skips with an explicit message only if its CSV is absent.
- `site/index.html`, `styles.css`, `app.js`, `charts.js`: Overview, Deep Dive, Opportunities, Reviews; shared review card; lazy in-memory reviews; global platform scope; hash navigation; all charts and table views; theme changes; responsive sidebar/drawer; keyboard focus management; paging/filtering/sorting; CSV links; loading, error, and empty states.
- `site/data/summary.json`, `insights.json`, `reviews.json`, `site/raw_reviews.csv`, and `site/annotated_reviews.csv`: generated from the protected inputs.
- `site/README.md`: the requested local serve command. No framework, build step, new production dependency, external font/image, or hosting configuration was added. The only external site resource is cdnjs Chart.js 4.4.1.

No reviewer name, avatar, profile link, or secret field is included in the compact review columns. Original review bodies/titles/translations remain the sanitized source content.

## Matcher comparison

The following expected values are the handover's literal regression expectations, not production hard-coded aggregates. The real build reproduced all of them:

| Insight ID | Expected | Actual | Result |
| --- | ---: | ---: | --- |
| c_money | 1,059 | 1,059 | PASS |
| c_accuracy | 444 | 444 | PASS |
| c_regression | 235 | 235 | PASS |
| c_lowsignal | 5,115 | 5,115 | PASS |
| c_ios | 424 | 424 | PASS |
| i_credits | 202 | 202 | PASS |
| i_free_images | 161 | 161 | PASS |
| i_free_questions | 507 | 507 | PASS |
| i_wrong | 444 | 444 | PASS |
| i_ignores | 73 | 73 | PASS |
| i_cancel | 120 | 120 | PASS |
| i_promos | 57 | 57 | PASS |
| i_bugs | 228 | 228 | PASS |
| i_style | 177 | 177 | PASS |
| i_voice | 117 | 117 | PASS |
| i_history | 84 | 84 | PASS |
| i_support | 71 | 71 | PASS |
| i_computer | 68 | 68 | PASS |
| i_models | 69 | 69 | PASS |
| i_login | 60 | 60 | PASS |
| i_preinstalled | 63 | 63 | PASS |
| f_free_uploads | 89 | 89 | PASS |
| f_pricing | 50 | 50 | PASS |
| f_search | 22 | 22 | PASS |
| f_ui | 21 | 21 | PASS |
| f_voice | 19 | 19 | PASS |
| f_threads | 19 | 19 | PASS |
| f_computer | 13 | 13 | PASS |
| f_models | 12 | 12 | PASS |
| s_research | 556 | 556 | PASS |
| s_sources | 550 | 550 | PASS |
| s_study | 308 | 308 | PASS |
| s_accuracy | 730 | 730 | PASS |
| s_speed | 464 | 464 | PASS |
| s_models | 44 | 44 | PASS |

## Output sizes

Gzip sizes use Python `gzip.compress(payload, mtime=0)` and are estimates of transfer compression, not additional generated gzip assets. The requested reviews payload is arrays-of-columns, with lists for labels/categories/competitors, numeric ratings/helpfulness, and boolean flags.

| File | Raw bytes | Gzip bytes |
| --- | ---: | ---: |
| summary.json | 99,215 | 21,027 |
| reviews.json | 3,896,796 | 1,247,473 |
| insights.json | 1,037,301 | 369,253 |
| raw_reviews.csv | 2,371,800 | 960,635 |
| annotated_reviews.csv | 3,874,724 | 1,274,104 |

The review payload contains all 14,791 reviews. Its raw size is **3,896,796 bytes**; gzipped size is **1,247,473 bytes**. JSON is fetched once on the first tab/drawer that needs it; only the current page's cards enter the DOM.

## Real commands and output

### Offline tests

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
```

Final exit 0:

```text
........................................................................ [ 40%]
........................................................................ [ 81%]
................................                                         [100%]
176 passed in 3.52s
```

The global autouse fixture disables socket connections, so this pytest run was offline. Development runs also passed with 175 tests before the additional language/version/topic test was added. No pytest failure occurred.

### Data build

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.build_site_data
```

Final exit 0, complete output:

```text
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
summary.json: raw=99215 bytes; gzip=21027 bytes
insights.json: raw=1037301 bytes; gzip=369253 bytes
reviews.json: raw=3896796 bytes; gzip=1247473 bytes
raw_reviews.csv: 2371800 bytes
annotated_reviews.csv: 3874724 bytes
```

### Syntax and data-source checks

```sh
node --check site/app.js
node --check site/charts.js
rg -n '14791|14,791' site/index.html site/app.js site/charts.js
rg -n 'innerHTML|insertAdjacentHTML|yAxisID|xAxisID|eval\(' site/index.html site/app.js site/charts.js
```

Both Node checks exited 0 with no output. Both `rg` searches exited 1 with no output: expected no matches. An additional digit scan was reviewed; remaining digits are HTML heading tag names, UTF-8/viewport syntax, the explicitly required Chart.js version, and the spec's CSS token name `--text-2`. There are no typed analytical values/dates/counts or JavaScript numeric literals. Runtime numerical settings are read from generated `summary.meta.ui`; the mismatch gap is read from the taxonomy.

### Determinism and protected-input verification

A local Python command hashed all three JSON outputs and both CSV copies, called the builder again with unchanged inputs, compared output hashes, compared CSV bytes to originals, and compared all 22 protected input files to the pre-work SHA-256 snapshot. It passed; actual verification output:

```text
Real-data rebuild byte-identical: True (all JSON and both CSV copies)
CSV copies byte-identical to their inputs: True
Protected inputs checked: 22
Protected inputs changed: []
Complete weeks: ['2026-07-13', '2026-07-20', '2026-07-27', '2026-08-03', '2026-08-10', '2026-08-17', '2026-08-24', '2026-08-31', '2026-09-07', '2026-09-14', '2026-09-21', '2026-09-28']
Full-day boundaries: 2026-07-12 2026-10-07
```

The verification Python command exited 0. In its shell cell, the subsequent no-match review-total grep returned the cell's overall exit 1; that was the expected grep result, not a data-build failure. Protected files include AGENTS.md, all preexisting docs/handover documents, DESIGN.md, TAXONOMY.md, annotation_prompt.md, existing analysis files, annotated/raw reviews, daily true counts, and run metadata. None changed.

### Local server and headless browser

The first `python3 -m http.server 8783 --bind 127.0.0.1` attempt failed in the sandbox with `PermissionError: [Errno 1] Operation not permitted`. It also printed `pyenv: cannot rehash: /Users/abhinav/.pyenv/shims isn't writable`. No page was served by that attempt.

The approved local-server command was:

```sh
.venv/bin/python -m http.server 8783 --bind 127.0.0.1 --directory site
```

It served the page and all local CSS/JS/JSON with HTTP 200 on initial loads and 304 on unchanged reloads. Its real closing output was:

```text
Serving HTTP on 127.0.0.1 port 8783 (http://127.0.0.1:8783/) ...
Keyboard interrupt received, exiting.
```

Server termination exited 0. No server was left running.

Chrome was started with an isolated temporary profile:

```sh
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' --headless=new --remote-debugging-port=9783 --user-data-dir=/private/tmp/perplexity-03-chrome --no-first-run --no-default-browser-check --disable-gpu --window-size=1440,1000 about:blank
node /private/tmp/perplexity-03-browser.mjs
```

The first Node attempt in the sandbox failed with `connect EPERM 127.0.0.1:9783`. Approved network access enabled the local Chrome DevTools Protocol connection. The helper used Node's built-in WebSocket and no package installation. Final helper exit 0, actual PASS messages and captured values:

```text
PASS: Reviews JSON is lazy on Overview
PASS: overview: loads, all 12 chart/table toggles work, single axes and tooltip callbacks
PASS: deep-dive: loads, all 0 chart/table toggles work, single axes and tooltip callbacks
PASS: opportunities: loads, all 3 chart/table toggles work, single axes and tooltip callbacks
PASS: reviews: loads, all 0 chart/table toggles work, single axes and tooltip callbacks
PASS: Global platform changes Reviews list
PASS: Global platform changes Deep Dive list
PASS: Drawer traps focus both ways, updates platform, closes on Esc and returns focus
PASS: Deep star filter works and preserves keyboard focus after rerender
PASS: ARIA tabs support arrow-key activation and retain tab focus
PASS: Overview changes counts and hides versions on iOS; label mix retains both platform denominators
PASS: Deep Dive category selection and topic-chip filter work
PASS: Related opportunity jumps to and focuses its card
PASS: Reviews paginate in disjoint pages of 50
PASS: Filter and first-page render below 100ms (max 14.60ms)
PASS: Empty state and clear filters work
PASS: Mouse hover shows a real value/n tooltip
PASS: Theme change recreates charts and uses dark tokens
PASS: overview: no horizontal page overflow at 375px
PASS: deep-dive: no horizontal page overflow at 375px
PASS: opportunities: no horizontal page overflow at 375px
PASS: reviews: no horizontal page overflow at 375px
PASS: Drawer is full width at 375px
PASS: Tab and platform restore from hash on reload
PASS: Reviews JSON fetched once before reload
Console errors: 0
Chart.js version: 4.4.1
Review fetches before reload: 1
Filtering/page-render timings ms: [6.399999998509884, 14.600000001490116, 6.5999999940395355, 1, 2.5]
```

The browser helper subscribes to console error messages, runtime exceptions, and browser log errors. All four tabs had zero such errors. Overview had eleven canvases plus the inline-bar mismatch table in all scope, with twelve working table toggles. iOS had ten canvases because versions are hidden. The mismatch toggle hides its inline bars to show the plain value/n table; its native hover hint includes share, n, and mismatches. Opportunities had three canvases. Every chart toggle was exercised; a real mouse hover also showed its value/n tooltip. Source version was verified as Chart.js 4.4.1.

Native Chrome stderr included Mac CVDisplayLink warnings, allocator warnings, and Chrome background registration/updater messages. These were native-browser diagnostics, distinct from the dashboard's captured page console errors. They did not prevent rendering or screenshots. The owned Chrome session was interrupted after QA and exited 0.

Evidence is retained locally in the gitignored run-logs directory: [browser results](../../data/run_logs/03-browser-results.json), [helper source](../../data/run_logs/03-browser-smoke.mjs), [desktop dark screenshot](../../data/run_logs/03-desktop.png), and [mobile light drawer screenshot](../../data/run_logs/03-mobile.png). The helper is specific to the local ports/profile used above. Both screenshots were visually inspected.

## Nine hard requirements

| Requirement | How verified |
| --- | --- |
| No typed data figures/dates/counts | Review-total grep found no matches; digit scan/code review confirmed figures originate in generated JSON, including footer gold figures and all numerical UI settings; mandatory technical syntax exceptions are listed below. |
| Safe review text insertion | No innerHTML/insertAdjacentHTML/eval matches; shared card uses textContent for body, title, translation, and topic, including original/translation switching. |
| Platform applies everywhere | Browser changed Reviews, Deep Dive, scoped Overview counts/version visibility, Opportunities/current drawer; drawer platform controls update the same global hash and scope. Label mix explicitly keeps both platforms as required. |
| Hash restores tab/platform | Loaded/reloaded `#opportunities?platform=ios` and asserted active tab/toggle; navigation consistently writes both fields. |
| No dual axes | Every active canvas chart was inspected for exactly x/y scales and no secondary axis IDs; weekly volume and averages are separate charts. |
| Every chart table/tooltip | Toggled every chart to its complete value/n table and back; checked tooltip callbacks on every active chart, and verified a real hover tooltip plus the inline mismatch hover hint. |
| Light/dark and chart redraw | Theme button recreated chart instances with CSS tokens; dark desktop and light mobile screenshots inspected; system-theme and explicit-theme CSS guards reviewed. |
| 375px layout | Every tab's document scrollWidth was at most innerWidth; sidebar list hides/select shows; drawer width is 375px with left edge at zero and starts at its top. |
| Keyboard | Native controls and focus-visible styles reviewed; tested tab arrow activation, Deep Dive filter focus retention, drawer forward/backward Tab wrapping, inert background, Esc close, and focus return to the opportunity card. |

## Design decisions and ambiguities

- **Generated-at vs deterministic builds:** wall-clock generation time would break byte-identical outputs. Generated-at uses `data/run.json`'s run timestamp, with an explicit basis in meta and the footer. No input timestamp was altered.
- **Pain-score denominator:** the spec says share at low stars by category without restricting its denominator. It uses all category reviews; the separate complaints/requests chart uses only rows with either named specific label. Both spell out the denominator. Low-volume muting uses the full category count in the current scope.
- **Nonsense sentiment:** the Nonsense takeaway explicitly says excluded from sentiment reads. The taxonomy's standalone label is excluded from sentiment means/distributions, while its rows still count toward total reviews and store stars. Sentiment denominators are shown. Empty means are null and display n/a.
- **Scope/window edges:** complete weeks share one source window across scopes. The first partial UTC day is excluded; the day before the latest review date is the last full day. Missing platform days within a complete window contribute zero volume; an empty annotated week has null means. No partial week is included.
- **No literal number wording:** interpreted as no literal analytical values/dates/counts. UTF-8, viewport scale, heading tags, CSS token names, and the explicitly required CDN version are technical syntax, not data figures. JavaScript control/format/page/axis settings also come from generated metadata. Removing the mandated library version from the CDN URL would conflict with the stack instruction.
- **Sidebar label groups:** label counts and label detail lists use primary label consistently; category membership counts each review once in each named category. Insight matching remains labels_any over the complete label list, as specified.
- **Defaults and ties:** Reviews starts Newest; Deep Dive/drawer starts Most helpful. Ties use newest UTC timestamp then review ID. Longest uses original body length. Topic ties use lexical order; natural version ordering is used. Filters persist between tabs; changing scope resets paging. Clear filters keeps the global platform scope. Paging past a reduced result set clamps to the last available page.
- **Focus on a disappearing source card:** a scope change can hide a zero-match card. Close returns focus to the corresponding visible rebuilt card; if none exists, it returns to the current tab button. Keeping focus on a removed node is impossible.
- **Narrative preservation:** Claude-owned narrative wording was preserved. In particular, c_lowsignal's match selects substantive reviews (5,115), as the expected table requires, despite its ID/title referring to non-specific reviews. Its displayed match count is not inverted. Zero-count cards hide; under-ten cards are muted and labeled “Few reviews.”

No design/input file was edited to resolve these choices. No blocking input issue was found.

## Failures, corrections, and limits

The first sandbox server and CDP attempts failed as recorded above, then succeeded with approved access. During extended QA, three helper assertions failed: an unscoped review selector included the closed drawer's hidden cards; a reused document invalidated the initial lazy-load assertion; and a programmatic pagination click had not focused its button as keyboard activation does. The helper was corrected to scope active lists, start from a fresh document, and focus before activation. These failures are not claimed as passing runs. Inspection confirmed the star-filter focus itself was correct. The final extended run passed all checks with zero captured page errors.

Visual QA led to wrapping long category labels, preserving focus through DOM refreshes, resetting the drawer to its top, keeping two-decimal rating values, using complete-week denominators in subtitles, and adding the inline mismatch table toggle/value-n hint. These fixes are in the final files and final browser pass.

Performance measurements are for this installed headless Chrome and the current corpus, not a guarantee for every device/query. Safari/Firefox, real touch devices, screen-reader output, OS-theme emulation, deliberate missing/corrupt JSON failures in the browser, actual CSV download UI, and every filter/sort combination were not tested. Their implementations were reviewed; CSV bytes and links were verified locally. Browser states verified include lazy loading, all tabs, chart tables, scopes, paging, empty/reset, category/topics, related-card jumps, keyboard tabs/focus, drawer, and both explicit themes. No new model-quality or business analysis was performed.

## Done when

- [x] Pytest passes offline: 176 tests.
- [x] build_site_data.py reproduces all 35 expected counts.
- [x] Local site loaded with no captured page console errors on every tab.
- [x] Nine requirements implemented and verified as recorded above, with technical-syntax interpretation made explicit.
- [x] This report contains real commands/output, matcher comparison, file sizes, decisions, failures, limits, and verification evidence.

Stopped at phase 03 completion. No commit or deployment.
