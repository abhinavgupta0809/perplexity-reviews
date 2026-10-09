# Phase 01 report: scaffold and scrape

Completed the `docs/handover/01-scrape.md` phase only. No commit, push, deployment,
annotation, or LLM call was made. Existing AGENTS.md and the phase handover were
read and left unchanged.

## Result and Done when

- [x] Offline pytest: **36 passed**. An autouse fixture rejects socket connections in every test.
- [x] `data/raw_reviews.csv`: **14,102 rows**, comprising **13,015 Android** and
  **1,087 iOS** reviews, with the exact 11 specified columns, zero duplicate IDs,
  every timestamp in the inclusive UTC window, and fewer than 20,000 rows.
- [x] Generated `data/volume_report.md` and `data/daily_true_counts.csv` exist.
- [x] This `docs/handover/01-report.md` records actual command output, the App Store
  limit observed, and empty/overlapping locales.

Run time: **2026-10-09T05:42:43Z**. Window starts **2026-07-11T05:42:43Z** and ends
at that run time. Both scrapers share `data/run.json`. There are 14,102 unique,
nonempty reviews before and after the cap; this live run did not require sampling.
The cap path was exercised offline, including more than 20,000 rows.

## Built

- Python 3.11 local `.venv`, fully pinned `requirements.txt`, `.gitignore`,
  `.env.example` (no secrets required), and README with run/resume instructions.
- `pipeline/config.py` with the exact 18 Play pairs and 15 iOS storefronts from
  the handover, IDs, window, cap, seed, delays, timeouts, and retry settings.
- `pipeline/scrape_play.py`: newest-first `google-play-scraper` pagination,
  continuation checkpoints, per-pair contributions, review-ID dedupe, and
  full-page window-edge stopping. A narrow adapter prevents the pinned library
  from suppressing fetch failures and masquerading as normal exhaustion.
- `pipeline/scrape_appstore.py`: requests-based RSS pagination, app-entry skipping,
  per-storefront checkpoints, and page-boundary confirmation. A page-specific
  HTTP 400/404 beyond page one counts as a feed boundary only when the preceding
  page still succeeds. Blocks, exhausted retries, and schema errors exit nonzero.
- `pipeline/common.py`: validation, UTC normalization, sanitized error messages,
  bounded exponential retries, and atomic publication/checkpoints.
- `pipeline/merge.py`: exact CSV schema, empty-body filtering, stable dedupe,
  inclusive timestamp window, deterministic uniform sampling within proportional
  platform/day quotas, pre-cap daily counts, and all requested volume statistics.
- Synthetic scrubbed fixtures and offline parser, privacy, dedupe, window,
  sampling, retry, pagination, resume, atomic-write, and merge tests.

Reviewer names, avatars, profile links, and developer reply text are excluded
before persistence. Only the 11 allowlisted review fields are stored in rows;
checkpoints additionally store sanitized counters and continuation metadata.
Review bodies and titles remain verbatim as instructed, including Unicode and
whitespace. Countries identify the first retrieval locale, not reviewer residence.
No paid calls or credentials are used.

Interim outputs are published only when every configured stream completes. A
zero-row source fails without publishing an apparent complete output. Successful
pages remain resumable after a failure or interruption. Data and checkpoints are
gitignored but remain present locally for Claude's review.

## App Store page limit and coverage

**Observed US limit: 10 pages, 50 reviews per page (500 total). Page 11 returned
HTTP 400; refetching page 10 succeeded.** The earliest US review retrieved is
2026-07-29T00:13:32Z. This does not cover the full 90-day US window,
which begins July 11. No extra archive/source was substituted for the requested
feed. Daily true counts mean pre-cap counts of the retrieved corpus, not the
complete universe of App Store reviews.

All other storefronts stopped on a full page older than the window, so their
maximum feed page limits were not probed. The page totals below include that
successfully served boundary page; they do not count the rejected US page 11.

| Storefront | Pages served | In-window reviews | Stop |
| --- | --- | --- | --- |
| us | 10 | 500 | page_limit_http_400 |
| gb | 2 | 45 | window_edge |
| in | 3 | 82 | window_edge |
| ca | 3 | 54 | window_edge |
| au | 2 | 30 | window_edge |
| de | 3 | 92 | window_edge |
| fr | 3 | 81 | window_edge |
| es | 2 | 42 | window_edge |
| br | 2 | 34 | window_edge |
| mx | 2 | 24 | window_edge |
| jp | 3 | 54 | window_edge |
| kr | 2 | 27 | window_edge |
| id | 2 | 9 | window_edge |
| sg | 2 | 4 | window_edge |
| ae | 2 | 9 | window_edge |

No locale returned zero in-window reviews. Google Play **en-IN, en-GB, and es-ES
added zero new IDs** because their reviews overlapped earlier configured pairs:
en-US contributed the English IDs, and es-MX contributed the Spanish IDs. Their
streams were still fully paginated and are separately reported in the generated
volume report. All other Play pairs and all App Store storefronts added reviews.

## Validation and actual command output

Commands ran from `/Users/abhinav/Desktop/Projects/perplexity-reviews` unless
otherwise noted. Exit codes below are observed, not inferred.

Setup:

```text
$ python3.11 --version
Python 3.11.6
$ python3.11 -m venv .venv
[exit 0; no output]
$ .venv/bin/python -m pip install -r requirements.txt
Successfully installed Pygments-2.21.0 certifi-2026.7.22 charset-normalizer-3.5.2 google-play-scraper-1.2.7 idna-3.20 iniconfig-2.3.1 packaging-26.3 pluggy-1.6.0 pytest-8.4.2 requests-2.32.5 urllib3-2.8.0
[exit 0; installation output excerpt]
```

The implementation was first built and tested under
`/private/tmp/perplexity-reviews-phase01`, then copied into this repository after
filesystem approval. The initial sandboxed PyPI index query failed DNS resolution;
the approved network query succeeded and reported `google-play-scraper (1.2.7)`.
The sandbox initially prevented pytest's optional cache write in this repository;
that run still passed all 36 tests, with one cache warning. The final offline run
disabled the optional cache provider:

```text
$ .venv/bin/python -m pytest -q -p no:cacheprovider
....................................                                     [100%]
36 passed in 1.68s
[exit 0]
```

Tests block socket connections and use saved fixtures/mocked responses. Sampling
checks cover exact cap size, order-independent determinism, unique IDs, and each
platform/day quota differing from its ideal share by less than one row. The
90-day boundary itself is retained, while a review one microsecond older is
excluded. Output/fixture keys are checked against the forbidden identity fields.

The live commands below were executed sequentially by the temporary logging
wrapper `/private/tmp/perplexity-reviews-phase01/run_phase01.py`. Full unedited
source and merge logs are also saved under `data/run_logs/`.

```text
$ .venv/bin/python -u -m pipeline.scrape_play
Run time UTC: 2026-10-09T05:42:43Z
Play en-US: page 1, fetched 200, retained 200, continue
Play en-US: page 2, fetched 200, retained 400, continue
Play en-US: page 3, fetched 200, retained 600, continue
Play en-US: page 4, fetched 200, retained 800, continue
Play en-US: page 5, fetched 200, retained 1000, continue
Play en-US: page 6, fetched 200, retained 1200, continue
Play en-US: page 7, fetched 200, retained 1400, continue
Play en-US: page 8, fetched 200, retained 1600, continue
Play en-US: page 9, fetched 200, retained 1800, continue
Play en-US: page 10, fetched 200, retained 2000, continue
Play en-US: page 11, fetched 200, retained 2200, continue
Play en-US: page 12, fetched 200, retained 2400, continue
Play en-US: page 13, fetched 200, retained 2600, continue
Play en-US: page 14, fetched 200, retained 2800, continue
Play en-US: page 15, fetched 200, retained 2999, continue
Play en-US: page 16, fetched 200, retained 3199, continue
Play en-US: page 17, fetched 200, retained 3399, continue
Play en-US: page 18, fetched 200, retained 3599, continue
Play en-US: page 19, fetched 200, retained 3799, continue
Play en-US: page 20, fetched 200, retained 3999, continue
Play en-US: page 21, fetched 200, retained 4199, continue
Play en-US: page 22, fetched 200, retained 4399, continue
Play en-US: page 23, fetched 200, retained 4599, continue
Play en-US: page 24, fetched 200, retained 4799, continue
Play en-US: page 25, fetched 200, retained 4999, continue
Play en-US: page 26, fetched 200, retained 5199, continue
Play en-US: page 27, fetched 200, retained 5399, continue
Play en-US: page 28, fetched 200, retained 5599, continue
Play en-US: page 29, fetched 200, retained 5799, continue
Play en-US: page 30, fetched 200, retained 5852, continue
Play en-US: page 31, fetched 200, retained 5852, window_edge
Play en-US: 5852 unique in-window rows, 5852 newly added
Play en-IN: page 1, fetched 200, retained 200, continue
Play en-IN: page 2, fetched 200, retained 400, continue
Play en-IN: page 3, fetched 200, retained 600, continue
Play en-IN: page 4, fetched 200, retained 800, continue
Play en-IN: page 5, fetched 200, retained 1000, continue
Play en-IN: page 6, fetched 200, retained 1200, continue
Play en-IN: page 7, fetched 200, retained 1400, continue
Play en-IN: page 8, fetched 200, retained 1600, continue
Play en-IN: page 9, fetched 200, retained 1800, continue
Play en-IN: page 10, fetched 200, retained 2000, continue
Play en-IN: page 11, fetched 200, retained 2200, continue
Play en-IN: page 12, fetched 200, retained 2400, continue
Play en-IN: page 13, fetched 200, retained 2600, continue
Play en-IN: page 14, fetched 200, retained 2800, continue
Play en-IN: page 15, fetched 200, retained 2999, continue
Play en-IN: page 16, fetched 200, retained 3199, continue
Play en-IN: page 17, fetched 200, retained 3399, continue
Play en-IN: page 18, fetched 200, retained 3599, continue
Play en-IN: page 19, fetched 200, retained 3799, continue
Play en-IN: page 20, fetched 200, retained 3999, continue
Play en-IN: page 21, fetched 200, retained 4199, continue
Play en-IN: page 22, fetched 200, retained 4399, continue
Play en-IN: page 23, fetched 200, retained 4599, continue
Play en-IN: page 24, fetched 200, retained 4799, continue
Play en-IN: page 25, fetched 200, retained 4999, continue
Play en-IN: page 26, fetched 200, retained 5199, continue
Play en-IN: page 27, fetched 200, retained 5399, continue
Play en-IN: page 28, fetched 200, retained 5599, continue
Play en-IN: page 29, fetched 200, retained 5799, continue
Play en-IN: page 30, fetched 200, retained 5852, continue
Play en-IN: page 31, fetched 200, retained 5852, window_edge
Play en-IN: 5852 unique in-window rows, 0 newly added
Play en-GB: page 1, fetched 200, retained 200, continue
Play en-GB: page 2, fetched 200, retained 400, continue
Play en-GB: page 3, fetched 200, retained 600, continue
Play en-GB: page 4, fetched 200, retained 800, continue
Play en-GB: page 5, fetched 200, retained 1000, continue
Play en-GB: page 6, fetched 200, retained 1200, continue
Play en-GB: page 7, fetched 200, retained 1400, continue
Play en-GB: page 8, fetched 200, retained 1600, continue
Play en-GB: page 9, fetched 200, retained 1800, continue
Play en-GB: page 10, fetched 200, retained 2000, continue
Play en-GB: page 11, fetched 200, retained 2200, continue
Play en-GB: page 12, fetched 200, retained 2400, continue
Play en-GB: page 13, fetched 200, retained 2600, continue
Play en-GB: page 14, fetched 200, retained 2800, continue
Play en-GB: page 15, fetched 200, retained 2999, continue
Play en-GB: page 16, fetched 200, retained 3199, continue
Play en-GB: page 17, fetched 200, retained 3399, continue
Play en-GB: page 18, fetched 200, retained 3599, continue
Play en-GB: page 19, fetched 200, retained 3799, continue
Play en-GB: page 20, fetched 200, retained 3999, continue
Play en-GB: page 21, fetched 200, retained 4199, continue
Play en-GB: page 22, fetched 200, retained 4399, continue
Play en-GB: page 23, fetched 200, retained 4599, continue
Play en-GB: page 24, fetched 200, retained 4799, continue
Play en-GB: page 25, fetched 200, retained 4999, continue
Play en-GB: page 26, fetched 200, retained 5199, continue
Play en-GB: page 27, fetched 200, retained 5399, continue
Play en-GB: page 28, fetched 200, retained 5599, continue
Play en-GB: page 29, fetched 200, retained 5799, continue
Play en-GB: page 30, fetched 200, retained 5852, continue
Play en-GB: page 31, fetched 200, retained 5852, window_edge
Play en-GB: 5852 unique in-window rows, 0 newly added
Play hi-IN: page 1, fetched 200, retained 13, continue
Play hi-IN: page 2, fetched 200, retained 13, window_edge
Play hi-IN: 13 unique in-window rows, 13 newly added
Play es-MX: page 1, fetched 200, retained 200, continue
Play es-MX: page 2, fetched 200, retained 400, continue
Play es-MX: page 3, fetched 200, retained 600, continue
Play es-MX: page 4, fetched 200, retained 800, continue
Play es-MX: page 5, fetched 200, retained 1000, continue
Play es-MX: page 6, fetched 200, retained 1200, continue
Play es-MX: page 7, fetched 200, retained 1400, continue
Play es-MX: page 8, fetched 200, retained 1600, continue
Play es-MX: page 9, fetched 200, retained 1800, continue
Play es-MX: page 10, fetched 200, retained 1913, continue
Play es-MX: page 11, fetched 200, retained 1913, window_edge
Play es-MX: 1913 unique in-window rows, 1913 newly added
Play es-ES: page 1, fetched 200, retained 200, continue
Play es-ES: page 2, fetched 200, retained 400, continue
Play es-ES: page 3, fetched 200, retained 600, continue
Play es-ES: page 4, fetched 200, retained 800, continue
Play es-ES: page 5, fetched 200, retained 1000, continue
Play es-ES: page 6, fetched 200, retained 1200, continue
Play es-ES: page 7, fetched 200, retained 1400, continue
Play es-ES: page 8, fetched 200, retained 1600, continue
Play es-ES: page 9, fetched 200, retained 1800, continue
Play es-ES: page 10, fetched 200, retained 1913, continue
Play es-ES: page 11, fetched 200, retained 1913, window_edge
Play es-ES: 1913 unique in-window rows, 0 newly added
Play pt-BR: page 1, fetched 200, retained 200, continue
Play pt-BR: page 2, fetched 200, retained 400, continue
Play pt-BR: page 3, fetched 200, retained 600, continue
Play pt-BR: page 4, fetched 200, retained 800, continue
Play pt-BR: page 5, fetched 200, retained 1000, continue
Play pt-BR: page 6, fetched 200, retained 1200, continue
Play pt-BR: page 7, fetched 200, retained 1217, continue
Play pt-BR: page 8, fetched 200, retained 1217, window_edge
Play pt-BR: 1217 unique in-window rows, 1217 newly added
Play de-DE: page 1, fetched 200, retained 181, continue
Play de-DE: page 2, fetched 200, retained 181, window_edge
Play de-DE: 181 unique in-window rows, 181 newly added
Play fr-FR: page 1, fetched 200, retained 200, continue
Play fr-FR: page 2, fetched 200, retained 400, continue
Play fr-FR: page 3, fetched 200, retained 600, continue
Play fr-FR: page 4, fetched 200, retained 800, continue
Play fr-FR: page 5, fetched 200, retained 1000, continue
Play fr-FR: page 6, fetched 200, retained 1200, continue
Play fr-FR: page 7, fetched 200, retained 1400, continue
Play fr-FR: page 8, fetched 200, retained 1600, continue
Play fr-FR: page 9, fetched 200, retained 1678, continue
Play fr-FR: page 10, fetched 200, retained 1678, window_edge
Play fr-FR: 1678 unique in-window rows, 1678 newly added
Play ja-JP: page 1, fetched 200, retained 74, continue
Play ja-JP: page 2, fetched 200, retained 74, window_edge
Play ja-JP: 74 unique in-window rows, 74 newly added
Play ko-KR: page 1, fetched 200, retained 165, continue
Play ko-KR: page 2, fetched 200, retained 165, window_edge
Play ko-KR: 165 unique in-window rows, 165 newly added
Play id-ID: page 1, fetched 200, retained 200, continue
Play id-ID: page 2, fetched 200, retained 400, continue
Play id-ID: page 3, fetched 200, retained 560, continue
Play id-ID: page 4, fetched 200, retained 560, window_edge
Play id-ID: 560 unique in-window rows, 560 newly added
Play ar-AE: page 1, fetched 200, retained 200, continue
Play ar-AE: page 2, fetched 200, retained 400, continue
Play ar-AE: page 3, fetched 200, retained 600, continue
Play ar-AE: page 4, fetched 200, retained 683, continue
Play ar-AE: page 5, fetched 200, retained 683, window_edge
Play ar-AE: 683 unique in-window rows, 683 newly added
Play tr-TR: page 1, fetched 200, retained 101, continue
Play tr-TR: page 2, fetched 200, retained 101, window_edge
Play tr-TR: 101 unique in-window rows, 101 newly added
Play it-IT: page 1, fetched 200, retained 115, continue
Play it-IT: page 2, fetched 200, retained 115, window_edge
Play it-IT: 115 unique in-window rows, 115 newly added
Play ru-RU: page 1, fetched 200, retained 200, continue
Play ru-RU: page 2, fetched 200, retained 251, continue
Play ru-RU: page 3, fetched 200, retained 251, window_edge
Play ru-RU: 251 unique in-window rows, 251 newly added
Play vi-VN: page 1, fetched 200, retained 103, continue
Play vi-VN: page 2, fetched 200, retained 103, window_edge
Play vi-VN: 103 unique in-window rows, 103 newly added
Play th-TH: page 1, fetched 200, retained 109, continue
Play th-TH: page 2, fetched 200, retained 109, window_edge
Play th-TH: 109 unique in-window rows, 109 newly added
play: wrote 13015 unique reviews to /Users/abhinav/Desktop/Projects/perplexity-reviews/data/interim/play.jsonl
Exit code: 0
```

```text
$ .venv/bin/python -u -m pipeline.scrape_appstore
Run time UTC: 2026-10-09T05:42:43Z
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
Run time UTC: 2026-10-09T05:42:43Z
Rows before cap: 14102; rows after cap: 14102
Rows by platform before cap: {'android': 13015, 'ios': 1087}
Wrote raw_reviews.csv, daily_true_counts.csv, volume_report.md
Exit code: 0
```

Independent artifact audit:

```text
$ .venv/bin/python /private/tmp/perplexity-reviews-phase01/verify_phase01.py
Exact columns: PASS
Unique IDs, inclusive UTC window, nonempty bodies, valid ratings, cap: PASS
Pre-cap daily counts and deterministic proportional sampling: PASS
Verbatim source fields and first-locale country attribution: PASS
Privacy keys absent: PASS (40 JSON/JSONL files plus CSV columns)
Run time UTC: 2026-10-09T05:42:43Z
Rows before cap: 14102
Rows after cap: 14102
Rows by platform: {'android': 13015, 'ios': 1087}
CSV SHA256: 007b6cd67f43548dc5cbb5ba92438f0cd33a8c3c34ff7a686384561568bc1353
[exit 0]
```

The audit compared every exported field with its sanitized interim source row,
checked country attribution against checkpoint locale order, recomputed daily
counts, and scanned all JSON/JSONL output and fixture keys for identity fields
and developer reply text. Its first attempt failed in the temporary verifier,
with `json.decoder.JSONDecodeError: Unterminated string starting at: line 1 column
181 (char 180)`: `str.splitlines()` also splits on Unicode separators that can
occur inside verbatim review bodies. The verifier was corrected to iterate
physical JSONL lines, matching the merge reader. No pipeline/data correction was
needed; the corrected audit passed. This failure is recorded rather than omitted.

Actual completed-run replay, with socket connections disabled, called both
scrapers and merge again. Full output is in `data/run_logs/idempotence.log`:

```text
$ .venv/bin/python /private/tmp/perplexity-reviews-phase01/idempotence_phase01.py
Completed-run replay with network disabled: PASS
All five data outputs byte-for-byte unchanged: PASS
[exit 0; final output excerpt]
```

The five files compared were both source JSONLs, `raw_reviews.csv`,
`daily_true_counts.csv`, and `volume_report.md`.

```text
$ git diff --check
[exit 0; no output]
$ git status --short
?? .env.example
?? .gitignore
?? AGENTS.md
?? README.md
?? docs/
?? pipeline/
?? requirements.txt
?? tests/
[exit 0; before writing this report; data and .venv are gitignored]
```

## Not tested and open questions

- No live HTTP block, deliberate interruption, or schema break was induced.
  These failure paths and checkpoint recovery were tested with offline mocks.
- The live corpus did not exceed 20,000 rows; proportional cap sampling was
  validated on larger synthetic inputs rather than activated on this live run.
- Beyond-US App Store maximum page limits were not measured because those feeds
  reached the window edge first, as the handover directs.
- Completeness beyond what the public feeds expose cannot be verified. In
  particular, US iOS reviews from July 11 through July 28 may be missing because
  the feed caps at 500 more recent reviews. This is a source limitation for Claude
  to account for during analysis.
- No annotation, gold-set work, site generation, or subsequent phase was run.
  No handover changes are proposed. Claude reviews this phase next.
