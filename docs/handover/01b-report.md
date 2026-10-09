# Phase 01b report: Google Play language streams

Executed only `docs/handover/01b-play-languages.md`, after reading `AGENTS.md`.
Stopped after this phase. No annotation, LLM call, site work, commit, push, or
deployment was performed. Existing handovers, phase-01 report, and AGENTS.md were
left unchanged.

## Done when

- [x] Offline pytest passes: **47 passed**; every test denies socket connections.
- [x] `data/raw_reviews.csv` has the exact **12 columns**; all Android rows have
  empty `country` and a nonempty `store_lang`; all iOS rows have a two-letter
  storefront `country` and empty `store_lang`; no duplicate IDs; at most 20,000 rows.
- [x] Regenerated volume report includes separate iOS storefront and Android
  store-language tables, per-language Play contributions, and the lag line under
  Date ranges.
- [x] This report includes all language results, rejection/duplication findings,
  cap status, actual commands/output, limitations, and backup verification.

## Result

Run time UTC: **2026-10-09T06:03:20Z**. Inclusive window: **2026-07-11T06:03:20Z** through that run time.
Retrieved **14,791** unique, nonempty reviews before the cap and exported
**14,791** after it: **13,704 Android** and **1,087 iOS**.
The **20,000-row cap did not trigger**.
Android coverage increased by **689 reviews** over
the preserved phase-01 corpus. The schema change is applied to the fresh run only;
the original data remains available unchanged under `data.run1/`.

`data/raw_reviews.csv` columns, in order:

```text
review_id, platform, country, store_lang, timestamp, date_utc, rating, title, review_text, app_version, thumbs_up, has_dev_reply
```

Hours between run time and newest review (before cap): android: 24.03 hours; ios: 37.55 hours.

## Changes made

- Replaced `PLAY_PAIRS` with the exact 42-code `PLAY_LANGS` tuple in handover
  order. Every library call uses the fixed `PLAY_COUNTRY = "us"`, including
  continuation tokens. There is one checkpoint/stream per language.
- Added `store_lang` to the parsers, interim records, CSV schema, fixtures, and
  validation. Android country must be empty and its store language nonempty;
  iOS country must be two lowercase ASCII letters and store language empty.
  Review-ID dedupe preserves the language of the first stream that returned it.
- Added language contribution metadata for overlapping IDs and identical
  in-window ID sets. Each requested code is retained literally; no replacements
  are inferred or substituted.
- Updated merge metadata checks, report breakdowns, and the newest-review lag
  computation (using the pre-cap corpus).
- Changed data ignore rules to `data/interim/`, `data/run_logs/`, and `data.run1/`.
  Final CSVs, generated volume report, and run manifest are visible to Git.
- Updated README and added normalized fixtures plus tests for the exact code
  order/schema, platform validation, first-language dedupe, overlap reporting,
  fixed-country calls, and configuration-change refusal.

The accepted private-function adapter, pinned dependencies, iOS page-limit
behavior, and first-fully-old-page stop rule were preserved. iOS scraper changes
only add the empty `store_lang` field. Existing retry, privacy, resume, cap,
atomic-write, and offline failure-path tests still pass.

## Rows per Play language

Fetched rows include old pages served to establish the window edge. In-window
rows exclude empty bodies and reviews outside the inclusive timestamp window.
Unique added is the language's contribution after cross-stream ID dedupe; Final
CSV rows also reflect any cap sampling.

| Code | Pages served | Fetched rows | In-window rows | Unique added | Final CSV rows | Overlap with first language | Same ID set as | Stop reason |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| en | 31 | 6200 | 5852 | 5852 | 5852 | None | None | window_edge |
| es | 11 | 2200 | 1913 | 1913 | 1913 | None | None | window_edge |
| pt | 8 | 1600 | 1217 | 1217 | 1217 | None | None | window_edge |
| fr | 10 | 2000 | 1678 | 1678 | 1678 | None | None | window_edge |
| ar | 5 | 1000 | 683 | 683 | 683 | None | None | window_edge |
| id | 4 | 800 | 560 | 560 | 560 | None | None | window_edge |
| ru | 3 | 600 | 251 | 251 | 251 | None | None | window_edge |
| de | 2 | 400 | 181 | 181 | 181 | None | None | window_edge |
| ko | 2 | 400 | 165 | 165 | 165 | None | None | window_edge |
| it | 2 | 400 | 115 | 115 | 115 | None | None | window_edge |
| th | 2 | 400 | 109 | 109 | 109 | None | None | window_edge |
| vi | 2 | 400 | 103 | 103 | 103 | None | None | window_edge |
| tr | 2 | 400 | 101 | 101 | 101 | None | None | window_edge |
| ja | 2 | 400 | 74 | 74 | 74 | None | None | window_edge |
| hi | 2 | 400 | 13 | 13 | 13 | None | None | window_edge |
| nl | 2 | 309 | 25 | 25 | 25 | None | None | window_edge |
| pl | 2 | 400 | 68 | 68 | 68 | None | None | window_edge |
| sv | 1 | 125 | 9 | 9 | 9 | None | None | no_continuation |
| da | 1 | 50 | 0 | 0 | 0 | None | None | window_edge |
| nb | 1 | 52 | 2 | 2 | 2 | None | None | no_continuation |
| fi | 1 | 53 | 3 | 3 | 3 | None | None | no_continuation |
| cs | 2 | 379 | 21 | 21 | 21 | None | None | window_edge |
| el | 1 | 183 | 17 | 17 | 17 | None | None | no_continuation |
| hu | 2 | 308 | 14 | 14 | 14 | None | None | window_edge |
| ro | 2 | 267 | 36 | 36 | 36 | None | None | window_edge |
| uk | 2 | 400 | 11 | 11 | 11 | None | None | window_edge |
| bg | 1 | 94 | 8 | 8 | 8 | None | None | no_continuation |
| hr | 1 | 147 | 11 | 11 | 11 | None | None | no_continuation |
| sk | 1 | 100 | 8 | 8 | 8 | None | None | no_continuation |
| sr | 1 | 93 | 12 | 12 | 12 | None | None | no_continuation |
| iw | 2 | 233 | 16 | 16 | 16 | None | None | window_edge |
| fa | 3 | 600 | 261 | 261 | 261 | None | None | window_edge |
| ur | 1 | 15 | 0 | 0 | 0 | None | None | window_edge |
| bn | 1 | 54 | 10 | 10 | 10 | None | None | no_continuation |
| ta | 1 | 33 | 1 | 1 | 1 | None | None | no_continuation |
| te | 1 | 30 | 1 | 1 | 1 | None | None | no_continuation |
| mr | 1 | 43 | 2 | 2 | 2 | None | None | no_continuation |
| ms | 1 | 77 | 12 | 12 | 12 | None | None | no_continuation |
| fil | 1 | 3 | 0 | 0 | 0 | None | None | window_edge |
| zh-TW | 2 | 400 | 79 | 79 | 79 | None | None | window_edge |
| zh-CN | 2 | 400 | 60 | 60 | 60 | None | None | window_edge |
| ca | 1 | 59 | 2 | 2 | 2 | None | None | no_continuation |

**Rejected codes: none observed.** Every requested code returned parseable review
items without an HTTP/schema rejection. **Duplicated codes: none observed among
the retained in-window IDs**; all overlap maps and identical-ID-set lists were
empty. No replacement code was guessed.

**No in-window reviews:** `da`, `ur`, and `fil`. They returned 50, 15, and 3
reviews respectively, but each first page was entirely older than the window;
those streams stopped at that accepted window edge. These are observed empty
window results, not claims that the codes were rejected. Their real results
remain in both this report and the generated volume report.

US iOS again served 10 pages (500 reviews), rejected page 11 with HTTP 400, and
successfully served page 10 on the boundary confirmation. Its oldest retrieved
review remains July 29. That accepted source-history limit was not redesigned.
All other iOS streams stopped at the window edge. Pre-cap daily counts describe
the retrieved corpus rather than all reviews published by the stores.

## Actual commands and output

Commands ran from `/Users/abhinav/Desktop/Projects/perplexity-reviews` unless
noted. No paid API or key was used. Code was prepared and tested first under
`/private/tmp/perplexity-reviews-phase01b`, then installed after filesystem approval.

Backup and installation:

```text
$ .venv/bin/python /private/tmp/perplexity-reviews-phase01b/install_phase01b.py
Moved data/ to data.run1/; all 45 files preserved byte-for-byte
Installed pipeline/config.py
Installed pipeline/common.py
Installed pipeline/scrape_play.py
Installed pipeline/scrape_appstore.py
Installed pipeline/merge.py
Installed tests/test_pipeline.py
Installed tests/test_play_languages.py
Installed tests/fixtures/normalized_reviews.json
Installed README.md
Installed .gitignore
Phase-01 CSV SHA256: 007b6cd67f43548dc5cbb5ba92438f0cd33a8c3c34ff7a686384561568bc1353
Fresh data/ will be created by the scrapers
[exit 0]
```

The installer compared SHA256 hashes of every file before and after the move.
It refuses to overwrite an existing `data.run1/`. The final audit independently
checked the preserved phase-01 CSV hash again.

Offline tests after installation:

```text
$ .venv/bin/python -m pytest -q -p no:cacheprovider
...............................................                          [100%]
47 passed in 1.71s
[exit 0]
```

The final staged test run also passed (`47 passed in 1.69s`). Socket access is
disabled in every test. The new duplicate-language test makes `en` and `fil`
return the same fixture IDs and verifies that only the first language survives
export, while the second stream's real overlap is reported. Android rows with a
nonempty country fail validation, and iOS inverse rules are separately tested.

Fresh live run, executed sequentially through the temporary logger
`/private/tmp/perplexity-reviews-phase01b/run_phase01b.py`. Full output is also
preserved in `data/run_logs/`:

```text
$ .venv/bin/python -u -m pipeline.scrape_play
Run time UTC: 2026-10-09T06:03:20Z
Play en: page 1, fetched 200, retained 200, continue
Play en: page 2, fetched 200, retained 400, continue
Play en: page 3, fetched 200, retained 600, continue
Play en: page 4, fetched 200, retained 800, continue
Play en: page 5, fetched 200, retained 1000, continue
Play en: page 6, fetched 200, retained 1200, continue
Play en: page 7, fetched 200, retained 1400, continue
Play en: page 8, fetched 200, retained 1600, continue
Play en: page 9, fetched 200, retained 1800, continue
Play en: page 10, fetched 200, retained 2000, continue
Play en: page 11, fetched 200, retained 2200, continue
Play en: page 12, fetched 200, retained 2400, continue
Play en: page 13, fetched 200, retained 2600, continue
Play en: page 14, fetched 200, retained 2800, continue
Play en: page 15, fetched 200, retained 2999, continue
Play en: page 16, fetched 200, retained 3199, continue
Play en: page 17, fetched 200, retained 3399, continue
Play en: page 18, fetched 200, retained 3599, continue
Play en: page 19, fetched 200, retained 3799, continue
Play en: page 20, fetched 200, retained 3999, continue
Play en: page 21, fetched 200, retained 4199, continue
Play en: page 22, fetched 200, retained 4399, continue
Play en: page 23, fetched 200, retained 4599, continue
Play en: page 24, fetched 200, retained 4799, continue
Play en: page 25, fetched 200, retained 4999, continue
Play en: page 26, fetched 200, retained 5199, continue
Play en: page 27, fetched 200, retained 5399, continue
Play en: page 28, fetched 200, retained 5599, continue
Play en: page 29, fetched 200, retained 5799, continue
Play en: page 30, fetched 200, retained 5852, continue
Play en: page 31, fetched 200, retained 5852, window_edge
Play en: 5852 unique in-window rows, 5852 newly added, overlaps {}, same IDs as []
Play es: page 1, fetched 200, retained 200, continue
Play es: page 2, fetched 200, retained 400, continue
Play es: page 3, fetched 200, retained 600, continue
Play es: page 4, fetched 200, retained 800, continue
Play es: page 5, fetched 200, retained 1000, continue
Play es: page 6, fetched 200, retained 1200, continue
Play es: page 7, fetched 200, retained 1400, continue
Play es: page 8, fetched 200, retained 1600, continue
Play es: page 9, fetched 200, retained 1800, continue
Play es: page 10, fetched 200, retained 1913, continue
Play es: page 11, fetched 200, retained 1913, window_edge
Play es: 1913 unique in-window rows, 1913 newly added, overlaps {}, same IDs as []
Play pt: page 1, fetched 200, retained 200, continue
Play pt: page 2, fetched 200, retained 400, continue
Play pt: page 3, fetched 200, retained 600, continue
Play pt: page 4, fetched 200, retained 800, continue
Play pt: page 5, fetched 200, retained 1000, continue
Play pt: page 6, fetched 200, retained 1200, continue
Play pt: page 7, fetched 200, retained 1217, continue
Play pt: page 8, fetched 200, retained 1217, window_edge
Play pt: 1217 unique in-window rows, 1217 newly added, overlaps {}, same IDs as []
Play fr: page 1, fetched 200, retained 200, continue
Play fr: page 2, fetched 200, retained 400, continue
Play fr: page 3, fetched 200, retained 600, continue
Play fr: page 4, fetched 200, retained 800, continue
Play fr: page 5, fetched 200, retained 1000, continue
Play fr: page 6, fetched 200, retained 1200, continue
Play fr: page 7, fetched 200, retained 1400, continue
Play fr: page 8, fetched 200, retained 1600, continue
Play fr: page 9, fetched 200, retained 1678, continue
Play fr: page 10, fetched 200, retained 1678, window_edge
Play fr: 1678 unique in-window rows, 1678 newly added, overlaps {}, same IDs as []
Play ar: page 1, fetched 200, retained 200, continue
Play ar: page 2, fetched 200, retained 400, continue
Play ar: page 3, fetched 200, retained 600, continue
Play ar: page 4, fetched 200, retained 683, continue
Play ar: page 5, fetched 200, retained 683, window_edge
Play ar: 683 unique in-window rows, 683 newly added, overlaps {}, same IDs as []
Play id: page 1, fetched 200, retained 200, continue
Play id: page 2, fetched 200, retained 400, continue
Play id: page 3, fetched 200, retained 560, continue
Play id: page 4, fetched 200, retained 560, window_edge
Play id: 560 unique in-window rows, 560 newly added, overlaps {}, same IDs as []
Play ru: page 1, fetched 200, retained 200, continue
Play ru: page 2, fetched 200, retained 251, continue
Play ru: page 3, fetched 200, retained 251, window_edge
Play ru: 251 unique in-window rows, 251 newly added, overlaps {}, same IDs as []
Play de: page 1, fetched 200, retained 181, continue
Play de: page 2, fetched 200, retained 181, window_edge
Play de: 181 unique in-window rows, 181 newly added, overlaps {}, same IDs as []
Play ko: page 1, fetched 200, retained 165, continue
Play ko: page 2, fetched 200, retained 165, window_edge
Play ko: 165 unique in-window rows, 165 newly added, overlaps {}, same IDs as []
Play it: page 1, fetched 200, retained 115, continue
Play it: page 2, fetched 200, retained 115, window_edge
Play it: 115 unique in-window rows, 115 newly added, overlaps {}, same IDs as []
Play th: page 1, fetched 200, retained 109, continue
Play th: page 2, fetched 200, retained 109, window_edge
Play th: 109 unique in-window rows, 109 newly added, overlaps {}, same IDs as []
Play vi: page 1, fetched 200, retained 103, continue
Play vi: page 2, fetched 200, retained 103, window_edge
Play vi: 103 unique in-window rows, 103 newly added, overlaps {}, same IDs as []
Play tr: page 1, fetched 200, retained 101, continue
Play tr: page 2, fetched 200, retained 101, window_edge
Play tr: 101 unique in-window rows, 101 newly added, overlaps {}, same IDs as []
Play ja: page 1, fetched 200, retained 74, continue
Play ja: page 2, fetched 200, retained 74, window_edge
Play ja: 74 unique in-window rows, 74 newly added, overlaps {}, same IDs as []
Play hi: page 1, fetched 200, retained 13, continue
Play hi: page 2, fetched 200, retained 13, window_edge
Play hi: 13 unique in-window rows, 13 newly added, overlaps {}, same IDs as []
Play nl: page 1, fetched 200, retained 25, continue
Play nl: page 2, fetched 109, retained 25, window_edge
Play nl: 25 unique in-window rows, 25 newly added, overlaps {}, same IDs as []
Play pl: page 1, fetched 200, retained 68, continue
Play pl: page 2, fetched 200, retained 68, window_edge
Play pl: 68 unique in-window rows, 68 newly added, overlaps {}, same IDs as []
Play sv: page 1, fetched 125, retained 9, no_continuation
Play sv: 9 unique in-window rows, 9 newly added, overlaps {}, same IDs as []
Play da: page 1, fetched 50, retained 0, window_edge
Play da: 0 unique in-window rows, 0 newly added, overlaps {}, same IDs as []
Play nb: page 1, fetched 52, retained 2, no_continuation
Play nb: 2 unique in-window rows, 2 newly added, overlaps {}, same IDs as []
Play fi: page 1, fetched 53, retained 3, no_continuation
Play fi: 3 unique in-window rows, 3 newly added, overlaps {}, same IDs as []
Play cs: page 1, fetched 200, retained 21, continue
Play cs: page 2, fetched 179, retained 21, window_edge
Play cs: 21 unique in-window rows, 21 newly added, overlaps {}, same IDs as []
Play el: page 1, fetched 183, retained 17, no_continuation
Play el: 17 unique in-window rows, 17 newly added, overlaps {}, same IDs as []
Play hu: page 1, fetched 200, retained 14, continue
Play hu: page 2, fetched 108, retained 14, window_edge
Play hu: 14 unique in-window rows, 14 newly added, overlaps {}, same IDs as []
Play ro: page 1, fetched 200, retained 36, continue
Play ro: page 2, fetched 67, retained 36, window_edge
Play ro: 36 unique in-window rows, 36 newly added, overlaps {}, same IDs as []
Play uk: page 1, fetched 200, retained 11, continue
Play uk: page 2, fetched 200, retained 11, window_edge
Play uk: 11 unique in-window rows, 11 newly added, overlaps {}, same IDs as []
Play bg: page 1, fetched 94, retained 8, no_continuation
Play bg: 8 unique in-window rows, 8 newly added, overlaps {}, same IDs as []
Play hr: page 1, fetched 147, retained 11, no_continuation
Play hr: 11 unique in-window rows, 11 newly added, overlaps {}, same IDs as []
Play sk: page 1, fetched 100, retained 8, no_continuation
Play sk: 8 unique in-window rows, 8 newly added, overlaps {}, same IDs as []
Play sr: page 1, fetched 93, retained 12, no_continuation
Play sr: 12 unique in-window rows, 12 newly added, overlaps {}, same IDs as []
Play iw: page 1, fetched 200, retained 16, continue
Play iw: page 2, fetched 33, retained 16, window_edge
Play iw: 16 unique in-window rows, 16 newly added, overlaps {}, same IDs as []
Play fa: page 1, fetched 200, retained 200, continue
Play fa: page 2, fetched 200, retained 261, continue
Play fa: page 3, fetched 200, retained 261, window_edge
Play fa: 261 unique in-window rows, 261 newly added, overlaps {}, same IDs as []
Play ur: page 1, fetched 15, retained 0, window_edge
Play ur: 0 unique in-window rows, 0 newly added, overlaps {}, same IDs as []
Play bn: page 1, fetched 54, retained 10, no_continuation
Play bn: 10 unique in-window rows, 10 newly added, overlaps {}, same IDs as []
Play ta: page 1, fetched 33, retained 1, no_continuation
Play ta: 1 unique in-window rows, 1 newly added, overlaps {}, same IDs as []
Play te: page 1, fetched 30, retained 1, no_continuation
Play te: 1 unique in-window rows, 1 newly added, overlaps {}, same IDs as []
Play mr: page 1, fetched 43, retained 2, no_continuation
Play mr: 2 unique in-window rows, 2 newly added, overlaps {}, same IDs as []
Play ms: page 1, fetched 77, retained 12, no_continuation
Play ms: 12 unique in-window rows, 12 newly added, overlaps {}, same IDs as []
Play fil: page 1, fetched 3, retained 0, window_edge
Play fil: 0 unique in-window rows, 0 newly added, overlaps {}, same IDs as []
Play zh-TW: page 1, fetched 200, retained 79, continue
Play zh-TW: page 2, fetched 200, retained 79, window_edge
Play zh-TW: 79 unique in-window rows, 79 newly added, overlaps {}, same IDs as []
Play zh-CN: page 1, fetched 200, retained 60, continue
Play zh-CN: page 2, fetched 200, retained 60, window_edge
Play zh-CN: 60 unique in-window rows, 60 newly added, overlaps {}, same IDs as []
Play ca: page 1, fetched 59, retained 2, no_continuation
Play ca: 2 unique in-window rows, 2 newly added, overlaps {}, same IDs as []
play: wrote 13704 unique reviews to /Users/abhinav/Desktop/Projects/perplexity-reviews/data/interim/play.jsonl
Exit code: 0
```

```text
$ .venv/bin/python -u -m pipeline.scrape_appstore
Run time UTC: 2026-10-09T06:03:20Z
App Store us: page 1, fetched 50, retained 50, continue
App Store us: page 2, fetched 50, retained 100, continue
App Store us: page 3, fetched 50, retained 150, continue
App Store us: page 4, fetched 50, retained 200, continue
App Store us: page 5, fetched 50, retained 250, continue
App Store us: page 6, fetched 50, retained 300, continue
App Store us: page 7, fetched 50, retained 350, continue
App Store us: page 8, fetched 50, retained 400, continue
App Store us: page 9, fetched 50, retained 450, continue
App Store us: page 10, fetched 50, retained 500, continue
App Store us: page 11 HTTP 400; preceding page confirmed; 10 pages served
App Store us: 500 unique in-window rows, 500 newly added
App Store gb: page 1, fetched 50, retained 45, continue
App Store gb: page 2, fetched 50, retained 45, window_edge
App Store gb: 45 unique in-window rows, 45 newly added
App Store in: page 1, fetched 50, retained 50, continue
App Store in: page 2, fetched 50, retained 82, continue
App Store in: page 3, fetched 50, retained 82, window_edge
App Store in: 82 unique in-window rows, 82 newly added
App Store ca: page 1, fetched 50, retained 50, continue
App Store ca: page 2, fetched 50, retained 54, continue
App Store ca: page 3, fetched 50, retained 54, window_edge
App Store ca: 54 unique in-window rows, 54 newly added
App Store au: page 1, fetched 50, retained 30, continue
App Store au: page 2, fetched 50, retained 30, window_edge
App Store au: 30 unique in-window rows, 30 newly added
App Store de: page 1, fetched 50, retained 50, continue
App Store de: page 2, fetched 50, retained 92, continue
App Store de: page 3, fetched 50, retained 92, window_edge
App Store de: 92 unique in-window rows, 92 newly added
App Store fr: page 1, fetched 50, retained 50, continue
App Store fr: page 2, fetched 50, retained 81, continue
App Store fr: page 3, fetched 50, retained 81, window_edge
App Store fr: 81 unique in-window rows, 81 newly added
App Store es: page 1, fetched 50, retained 42, continue
App Store es: page 2, fetched 50, retained 42, window_edge
App Store es: 42 unique in-window rows, 42 newly added
App Store br: page 1, fetched 50, retained 34, continue
App Store br: page 2, fetched 50, retained 34, window_edge
App Store br: 34 unique in-window rows, 34 newly added
App Store mx: page 1, fetched 50, retained 24, continue
App Store mx: page 2, fetched 50, retained 24, window_edge
App Store mx: 24 unique in-window rows, 24 newly added
App Store jp: page 1, fetched 50, retained 50, continue
App Store jp: page 2, fetched 50, retained 54, continue
App Store jp: page 3, fetched 50, retained 54, window_edge
App Store jp: 54 unique in-window rows, 54 newly added
App Store kr: page 1, fetched 50, retained 27, continue
App Store kr: page 2, fetched 50, retained 27, window_edge
App Store kr: 27 unique in-window rows, 27 newly added
App Store id: page 1, fetched 50, retained 9, continue
App Store id: page 2, fetched 50, retained 9, window_edge
App Store id: 9 unique in-window rows, 9 newly added
App Store sg: page 1, fetched 50, retained 4, continue
App Store sg: page 2, fetched 50, retained 4, window_edge
App Store sg: 4 unique in-window rows, 4 newly added
App Store ae: page 1, fetched 50, retained 9, continue
App Store ae: page 2, fetched 34, retained 9, window_edge
App Store ae: 9 unique in-window rows, 9 newly added
appstore: wrote 1087 unique reviews to /Users/abhinav/Desktop/Projects/perplexity-reviews/data/interim/appstore.jsonl
Exit code: 0
```

```text
$ .venv/bin/python -u -m pipeline.merge
Run time UTC: 2026-10-09T06:03:20Z
Rows before cap: 14791; rows after cap: 14791
Rows by platform before cap: {'android': 13704, 'ios': 1087}
Wrote raw_reviews.csv, daily_true_counts.csv, volume_report.md
Exit code: 0
```

Independent data audit:

```text
$ .venv/bin/python /private/tmp/perplexity-reviews-phase01b/verify_phase01b.py
Exact columns: PASS
Android country/store_lang and iOS storefront/store_lang rules: PASS
Unique IDs, inclusive UTC window, nonempty bodies, valid ratings, cap: PASS
Pre-cap daily counts and deterministic proportional sampling: PASS
Verbatim source fields and first-language/storefront attribution: PASS
42 Play streams in handover order and 15 iOS storefronts complete: PASS
Separate platform tables and independently computed lag line: PASS
Phase-01 backup CSV unchanged: PASS
Privacy keys absent: PASS (65 JSON/JSONL files plus CSV columns)
Run time UTC: 2026-10-09T06:03:20Z
Rows before cap: 14791
Rows after cap: 14791
Rows by platform: {'android': 13704, 'ios': 1087}
20k cap triggered: False
Hours between run time and newest review (before cap): android: 24.03 hours; ios: 37.55 hours.
CSV SHA256: 3c74e530d8ae2d598cadba8992b76b627438fed60d353ca5ed9cb2f538ab7030
[exit 0]
```

The audit validated the CSV fields, platform rules, ID uniqueness, inclusive
window, preserved source text, first-language/storefront attribution, source
completion/order, daily counts, sample reproducibility, privacy keys, split
tables, and independently computed lag line. It confirmed the old CSV was intact.

Completed-run replay with sockets disabled:

```text
$ .venv/bin/python /private/tmp/perplexity-reviews-phase01b/idempotence_phase01b.py
Completed-run replay with network disabled: PASS
All five data outputs byte-for-byte unchanged: PASS
[exit 0; final output excerpt]
```

The replay called both scraper `main()` functions and merge again without socket
access, then compared both source JSONLs, raw CSV, daily counts, and volume report
byte for byte. Full replay output is in `data/run_logs/idempotence.log`.

Ignore-rule and whitespace checks:

```text
$ git check-ignore data/interim/play.jsonl data/run_logs/scrape_play.log data.run1/raw_reviews.csv data/raw_reviews.csv data/daily_true_counts.csv data/volume_report.md data/run.json
data/interim/play.jsonl
data/run_logs/scrape_play.log
data.run1/raw_reviews.csv
[exit 0; final data files were not ignored]
$ git diff --check
[exit 0; no output]
$ git status --short
?? .env.example
?? .gitignore
?? AGENTS.md
?? README.md
?? data/
?? docs/
?? pipeline/
?? requirements.txt
?? tests/
[exit 0; before writing this report]
```

## Not tested, surprises, and open questions

- No live failure occurred in the fresh scraper/merge runs. HTTP blocks,
  retries, malformed schemas, and checkpoint recovery remain covered by offline
  tests; no block or deliberate interruption was induced against the stores.
- No Play code rejection or in-window duplication occurred live, so the
  duplicate-code path was exercised with saved fixtures/mocks. Literal codes
  `nb`, `iw`, `fil`, `zh-TW`, and `zh-CN` were passed unchanged.
- The live corpus stayed below the cap. Larger synthetic inputs still exercise
  deterministic proportional sampling and rounding guarantees in pytest.
- The empty windows for `da`, `ur`, and `fil` are retained as observed. No extra
  language code or alternate source was tried.
- The reported Play lag is a measured difference from the run time to the newest
  retrieved review; it is not an extrapolated count for the partial last day.
- US iOS feed truncation remains an accepted limit for Claude's analysis.
- No changes to handovers or later-phase scope are proposed. Claude reviews 01b next.
