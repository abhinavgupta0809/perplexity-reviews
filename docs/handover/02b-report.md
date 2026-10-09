# Phase 02b report: completed live annotation

Phase date: 2026-10-09. Python 3.11.6.

Phase 02b is complete following Abhinav's instruction to resume with the replacement workspace-scoped key. Gold annotation and evaluation succeeded; every resumed gold stop check passed; the full corpus completed. The full output has 14,791 rows in the same order as raw_reviews.csv, with every original field preserved and zero annotation_error rows. No additional source-code or test changes were made during the resume. No prompt, taxonomy, gold-set, commit, push, deployment, or next-phase work was performed.

## What changed

- `pipeline/annotation_support.py`: object-root schema with required `results`; missing/invalid roots fail batch validation; enums match case-insensitively and store taxonomy spelling; duplicate detection and all semantic label/category rules remain strict.
- Topic is stripped/lowercased and accepts 1–80 characters with categories; it remains empty without categories. Language is lowercased, accepts two/three letters with an optional two-letter or three-digit region, and stores the base code. English/und translations are cleared; other languages still require nonblank translation. String types remain strict.
- API 4xx other than 429 stop immediately and surface the error type/message. Only those fields are read; key, prompt, request content, review bodies, and titles are redacted if echoed there. No request body or key was logged. Existing bounded 429/5xx/connection retries remain.
- `pipeline/annotate.py`: `--offline-prices` skips the pricing fetch and identifies the dated rates; fresh pricing remains the default. `--max-cost USD` defaults to $5.00, requires a finite positive amount, and stops nonzero when cumulative actual response cost exceeds it. Valid results from the crossing response are cached before stopping; no output CSV is published.
- Added request-count, validation-retry, single-fallback, and non-`end_turn` counters for the required reporting. Dedupe/cache keys, cache lock, estimator, sampling, retry-then-single behavior, and evaluator were left as designed.
- Updated the config pricing comment and affected tests. No dependency changes.

Offline tests cover object root, missing `results`, passing/failing normalization cases, canonical enum storage and unknown/repeated values, sanitized non-retried 4xx, offline pricing, invalid cost limits, spend-stop cache preservation and resume, and reporting counters. Existing socket-blocking fixtures disable networking throughout pytest.

The [structured outputs documentation](https://platform.claude.com/docs/en/build-with-claude/structured-outputs) was checked for the raw schema request shape. No prompt, taxonomy, or gold-set changes were made.

## Resumed gold and full accounting

| Measurement | Gold | Full corpus |
| --- | ---: | ---: |
| Actual API requests | 6 | 454 |
| Successful responses | 6 | 454 |
| Uncached input tokens | 8,543 | 598,851 |
| Output tokens | 40,609 | 2,746,505 |
| Cache-write tokens | 4,072 | 0 |
| Cache-read tokens | 20,360 | 1,848,688 |
| Batches needing validation retry | 1 | 24 |
| Reviews falling back to single calls | 0 | 1 |
| Published-tariff usage cost USD | $0.021871 | $1.451624 |
| Non-end_turn stop reasons | None | None |
| Requests ending on HTTP 4xx | 0 | 0 |
| annotation_error rows | 0 | 0 |

Combined displayed usage cost: **$1.473495**. These are token-usage costs at freshly fetched public tariffs, not an account invoice adjusted for discounts. Both live runs used the default price fetch and `--max-cost 5.00`; neither used `--offline-prices` or reached the guard.

The full dry run reused 120 cached gold keys, leaving 10,717 keys for 429 original batches. The 24 validation retries and one single fallback account for the full run's 454 requests. The validated cache now has all 10,837 distinct corpus keys, with no incomplete terminal record. Retry/fallback totals were also checked against the complete logs.

### Gold stop checks and evaluation

- Gold rows: 120; annotation_error rows: 0 (stop threshold: more than 6).
- Resumed gold HTTP 4xx: none.
- Dry estimate: $0.013719; actual reported cost: $0.021871; ratio: 1.5942 (stop threshold: greater than 10).
- Primary label accuracy: 117/120, 97.50%, target passed.
- Label set overlap: 120/120, 100.00%.
- Primary category agreement: 87/92, 94.57%, target passed.
- Low-signal agreement: 28/28, 100.00%.
- Sentiment within one point: 120/120, 100.00%; mean absolute error: 0.2000.
- Seven disagreements are included in the script-generated [02-eval.md](02-eval.md).

No stop condition fired in the resumed run. The earlier key's 400 is recorded separately below; Abhinav explicitly authorized restarting at step 2 after replacing that key.

### Full output counts

Raw rows: **14,791**; annotated rows: **14,791**; annotation_error rows: **0**; blank primary labels: **0**. Counts below use the first label in each output row; they sum to the full row count.

| Primary label | Rows |
| --- | ---: |
| Generic Good | 8,674 |
| Specific Complaint | 2,049 |
| Specific Praise | 2,880 |
| Generic Bad | 635 |
| Feature Request | 186 |
| Nonsense | 367 |

## Real commands and output

Commands ran from the repository directory. This resume starts at handover step 2, as instructed. The prior offline test result remains applicable: source and test hashes were unchanged by this resume. Pytest was not rerun during the resume.

### Offline tests from the implementation turn

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
```

Exit 0, actual output:

```text
........................................................................ [ 44%]
........................................................................ [ 89%]
.................                                                        [100%]
161 passed in 2.66s
```

### Resumed gold dry run

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --gold --dry-run
```

Exit 0:

```text
Model: claude-haiku-5-5
Selected rows: 120; distinct text keys: 120
Keys already cached: 0; distinct keys to send: 120
Requests estimated: 5; batch size: 25
Estimated input tokens: 22308 (uncached=5763, cache_write=3309, cache_read=13236)
Estimated output tokens: 25194
Estimated cost USD: $0.013719; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
Dry run: zero API calls; no files written
```

### Resumed gold live run

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --gold --max-cost 5.00 2>&1 | tee /private/tmp/perplexity-02b-resume-gold.log
```

The initial sandbox attempt exited 1 before any API request:

```text
ERROR: Cannot fetch current pricing; no paid requests started
Model: claude-haiku-5-5
Selected rows: 120; distinct text keys: 120
Keys already cached: 0; distinct keys to send: 120
Requests estimated: 5; batch size: 25
Estimated input tokens: 22308 (uncached=5763, cache_write=3309, cache_read=13236)
Estimated output tokens: 25194
Estimated cost USD: $0.013719; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
```

Reran the same command with approved network access. Exit 0; complete actual output:

```text
Model: claude-haiku-5-5
Selected rows: 120; distinct text keys: 120
Keys already cached: 0; distinct keys to send: 120
Requests estimated: 5; batch size: 25
Estimated input tokens: 22308 (uncached=5763, cache_write=3309, cache_read=13236)
Estimated output tokens: 25194
Estimated cost USD: $0.013719; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
Annotating distinct keys 1-25 of 120
Actual usage so far: input=1245, output=6057, cache_write=4072, cache_read=0, responses=1
Annotating distinct keys 26-50 of 120
Actual usage so far: input=2463, output=12432, cache_write=4072, cache_read=4072, responses=2
Annotating distinct keys 51-75 of 120
Actual usage so far: input=4280, output=19628, cache_write=4072, cache_read=8144, responses=3
Annotating distinct keys 76-100 of 120
Actual usage so far: input=5795, output=26527, cache_write=4072, cache_read=12216, responses=4
Annotating distinct keys 101-120 of 120
Actual usage so far: input=7169, output=33297, cache_write=4072, cache_read=16288, responses=5
Batch validation failed for 1 indices; retrying the batch once
Actual usage so far: input=8543, output=40609, cache_write=4072, cache_read=20360, responses=6
Wrote 120 rows in input order to /Users/abhinav/Desktop/Projects/perplexity-reviews/data/interim/gold_annotations.csv; rows with annotation_error=0
Actual usage: input=8543, output=40609, cache_write=4072, cache_read=20360, responses=6
Actual token-usage cost USD (published tariff; excludes account discounts): $0.021871
Batches needing validation retry: 1; reviews falling back to single calls: 0
Stop reasons other than end_turn: {}
Actual API requests: 6
```

### Evaluation

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.evaluate
```

Exit 0:

```text
Evaluated 120 gold rows; annotation_error=0
Primary label accuracy: 97.50%; target >= 85%
Primary category agreement: 94.57%; target >= 80%
Disagreements: 7; wrote /Users/abhinav/Desktop/Projects/perplexity-reviews/docs/handover/02-eval.md
```

### Full-corpus dry run

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --dry-run
```

Exit 0:

```text
Model: claude-haiku-5-5
Selected rows: 14791; distinct text keys: 10837
Keys already cached: 120; distinct keys to send: 10717
Requests estimated: 429; batch size: 25
Estimated input tokens: 1871263 (uncached=451702, cache_write=3309, cache_read=1416252)
Estimated output tokens: 2193371
Estimated cost USD: $1.156432; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
Dry run: zero API calls; no files written
```

### Full-corpus live run

```sh
set -o pipefail
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --yes --max-cost 5.00 2>&1 | tee /private/tmp/perplexity-02b-resume-full.log
```

The initial sandbox attempt exited 1 before any API request:

```text
ERROR: Cannot fetch current pricing; no paid requests started
Model: claude-haiku-5-5
Selected rows: 14791; distinct text keys: 10837
Keys already cached: 120; distinct keys to send: 10717
Requests estimated: 429; batch size: 25
Estimated input tokens: 1871263 (uncached=451702, cache_write=3309, cache_read=1416252)
Estimated output tokens: 2193371
Estimated cost USD: $1.156432; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
```

Reran the same command with approved network access. Exit 0. Actual final output excerpt:

```text
Annotating distinct keys 10651-10675 of 10717
Actual usage so far: input=596960, output=2737679, cache_write=0, cache_read=1840544, responses=452
Annotating distinct keys 10676-10700 of 10717
Actual usage so far: input=598052, output=2743170, cache_write=0, cache_read=1844616, responses=453
Annotating distinct keys 10701-10717 of 10717
Actual usage so far: input=598851, output=2746505, cache_write=0, cache_read=1848688, responses=454
Wrote 14791 rows in input order to /Users/abhinav/Desktop/Projects/perplexity-reviews/data/annotated_reviews.csv; rows with annotation_error=0
Actual usage: input=598851, output=2746505, cache_write=0, cache_read=1848688, responses=454
Actual token-usage cost USD (published tariff; excludes account discounts): $1.451624
Batches needing validation retry: 24; reviews falling back to single calls: 1
Stop reasons other than end_turn: {}
Actual API requests: 454
```

The complete per-batch output is preserved in [02b-full-run.log](../../data/interim/02b-full-run.log). The complete gold output is also preserved in [02b-gold-run.log](../../data/interim/02b-gold-run.log). Logs contain operational counters, not review text, keys, or reviewer metadata.

### Final verification

A local Python verification command compared row count and review-ID order, checked every original raw field, validated the entire cache with the runtime taxonomy, counted primary labels, reconciled retry/fallback log entries with summaries, and compared SHA-256 values for 27 input/code/test files captured before the resume. It exited 0; actual verification output excerpt:

```text
Raw rows: 14791
Annotated rows: 14791
Full row count matches raw: True
Full review ID order matches raw: True
Every original raw field preserved: True
Full annotation_error rows: 0
Gold rows: 120
Gold annotation_error rows: 0
Validated cache entries: 10837
Raw distinct text keys: 10837
Cache incomplete final record: False
Primary label counts:
Generic Good: 8674
Specific Complaint: 2049
Specific Praise: 2880
Generic Bad: 635
Feature Request: 186
Nonsense: 367
Blank primary label rows: 0
Input/code/test hashes checked: 27
Input/code/test files changed: []
02-eval.md generated: True
```

The hash snapshot excludes this report and the permitted generated 02-eval.md. It includes AGENTS.md, raw_reviews.csv, annotation_prompt.md, TAXONOMY.md, existing analysis files, other preexisting handovers, pipeline Python files, and test Python files. No checked file changed.

The local credential check printed only these booleans:

```text
.env key available: True
Shell key set: False
Shell key absent or matches .env: True
Input/code/test hashes saved: 27
```

The shell had no overriding key, so the replacement key in .env was the one loaded by the scripts.

## Earlier failure and its resolution

Before the key replacement, the first live request exited 1 with this actual error:

```text
ERROR: Anthropic HTTP 400: invalid_request_error: This API key is not scoped to a workspace, so this request must include the anthropic-workspace-id header with the ID of the workspace to use. Add the header, or use an API key that is scoped to a workspace.
```

That attempt made one API request, received no successful Messages response, reported zero tokens and $0.000000 accumulated usage cost, and performed no validation retry or single fallback. The agent stopped then as instructed, without guessing a workspace header. Abhinav replaced the key and explicitly instructed this resume. The resumed accounting table excludes that earlier failed request; including it, phase 02b has 461 API request attempts (1 earlier failure + 6 resumed gold + 454 full).

Pricing fetches failed inside the sandbox both before the original key failure and during this resume. Approved network reruns succeeded. There were no HTTP 4xx, transport retries, or non-end_turn stop reasons during the successful resumed runs. Validation retries are reported above as retries, not concealed as first-attempt success; the single fallback ultimately produced a valid result, since the complete cache and output contain no failed annotation.

The prior implementation turn also ran pip check successfully (`No broken requirements found.`), with a warning that the user cache directory was unwritable. Its git diff check produced no output, but repository files were untracked, so that check did not inspect them. Neither check was repeated during this resume.

## Limits and surprises

The replacement workspace-scoped key resolved the initial authentication/configuration failure without a code change. Actual gold and full costs were above the heuristic dry estimates; dry estimates exclude retries and use approximations for tokens. Both live costs remained below the $5 guards, and the gold actual/dry ratio remained below the handover's stop threshold.

The successful runs exercised real authentication, structured-output acceptance, prompt-cache reads, response usage accounting, validation retries, one single fallback, CSV generation, and gold evaluation. The spend-stop and HTTP error/retry paths remain covered by offline tests; a deliberate live spend-limit breach, live rate-limit/transient-failure test, crash/resume test, or account-invoice reconciliation was not performed. No full-corpus quality review beyond the requested output integrity/count checks was performed; label-quality analysis remains Claude's role. No open implementation issue was found in this resume.

## Done when

- [x] Pytest passes offline: 161 tests in the implementation turn; code/tests unchanged during resume.
- [x] All six changes are implemented with tests.
- [x] Gold CSV and generated docs/handover/02-eval.md exist, produced by the scripts.
- [x] Full annotated CSV exists with the same count/order and original fields as raw_reviews.csv.
- [x] This report includes real command output and separate requests/tokens/cost/retry/fallback/stop/error accounting.

Stopped at phase 02b completion. No next-phase work was started.
