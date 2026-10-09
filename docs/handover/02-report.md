# Phase 02 report: annotate and evaluate

Date: 2026-10-09. Project: `/Users/abhinav/Desktop/Projects/perplexity-reviews`.

Phase 02 is complete under the handover's no-key branch. The annotation and evaluation scripts are implemented, all 111 tests pass offline, and both required dry runs succeeded. No `.env` or usable `ANTHROPIC_API_KEY` was available. The live gold annotation and evaluation were skipped as instructed. No full paid annotation, commit, push, deployment, or next-phase work was performed.

## What was built

- `pipeline/annotate.py`: runtime prompt/taxonomy loading, normalized-text deduplication, first-row star ratings, batched user arrays containing only `i, stars, title, text`, strict result validation, batch retry followed by single-review fallback, append-only validated-result cache, resume, and atomic CSV output.
- `pipeline/annotation_support.py`: API schema generation, file-backed validation, current-price parsing, response token accounting, and a sanitized Anthropic transport.
- `pipeline/evaluate.py`: all nine requested evaluation outputs, exact ID matching, target checks, complete confusion/category tables, and every disagreement on metrics 1, 3, or 4.
- Offline fake-client annotation tests, hand-calculated evaluator tests, and sanitized JSON fixtures.
- Pinned `anthropic==1.12.1`, `python-dotenv==1.2.1`, and required transitive dependencies. Updated `.env.example` with the key name only and README with usage and assumptions.

All four modes are covered: dry run, gold, limited smoke test, and full annotation requiring `--yes`. Batch size defaults to 25 and is configurable. All 12 raw fields are preserved alongside the 14 requested annotation fields. Full/limited output retains every source row in order; gold output contains only gold rows in source order. Duplicate flags use the entire source corpus, including during gold runs.

The cache key is exactly SHA-256 of prompt text + model ID + normalized text key. Valid results are flushed immediately; incomplete terminal cache records can be repaired on resume, while other corruption fails loudly. A cache lock prevents concurrent duplicate spending. Prompt edits or changes to the configured model invalidate cache keys. Failed results are not cached.

Final validation failures retain their rows with annotation fields empty and `annotation_error` populated. Source-derived duplicate/truncation flags still have TRUE/FALSE values; missing sentiment leaves `rating_mismatch` empty. Limits leave unselected, uncached rows explicitly marked with `annotation_error`. Fatal API/transport failures preserve validated cache entries and do not publish a new apparently complete CSV.

No taxonomy label/category literal appears in Python source. The standalone label is identified from the taxonomy as the sole label outside its specific and generic groups; this avoids embedding its name in code.

## Anthropic documentation used

These current primary sources were read before client implementation on 2026-10-09:

- [Structured outputs](https://platform.claude.com/docs/en/build-with-claude/structured-outputs): runtime JSON schema through `messages.create(output_config.format)`, with required fields and enum values. Unsupported bounds and cross-field constraints are enforced locally. Enum casing variations are rejected and retried, consistent with the handover's prohibition on repairing labels.
- [Prompt caching](https://platform.claude.com/docs/en/build-with-claude/prompt-caching): explicit `cache_control={"type": "ephemeral"}` on the unchanged system prompt, using the default five-minute lifetime.
- [Rate limits](https://platform.claude.com/docs/en/api/rate-limits): honor 429 `retry-after`; a 429 without that header fails with a spend-cap diagnostic.
- [Haiku 5.5 overview](https://platform.claude.com/docs/en/models/haiku-5-5/overview): `claude-haiku-5-5` is the requested model. Non-default sampling controls are rejected, so `temperature`, `top_p`, and `top_k` are omitted; defaults are the allowed sampling settings.
- [Python SDK](https://platform.claude.com/docs/en/cli-sdks-libraries/sdks/python): use the pinned SDK, typed errors, and `max_retries=0` so the wrapper owns bounded transport retries.
- [Create a Message](https://platform.claude.com/docs/en/api/messages/create): read usage and stop reasons from responses; count tokens from every response, including responses that subsequently fail validation.
- [Pricing](https://platform.claude.com/docs/en/about-claude/pricing): rates below.

Transport retries are separate from the required validation retry sequence. 429/connection/transient HTTP errors get at most three transport attempts. Error logs never print secrets, reviewer objects, or response bodies.

## Prices and cost accounting

Prices read 2026-10-09, USD per million tokens from the [current pricing table](https://platform.claude.com/docs/en/about-claude/pricing):

| Haiku 5.5 prompt length | Input | Output | 5-minute cache write | Cache read |
| --- | ---: | ---: | ---: | ---: |
| Up to 100,000 tokens | $0.10 | $0.50 | $0.125 | $0.01 |
| Over 100,000 tokens | $0.50 | $2.50 | $0.625 | $0.05 |

These dated rates in `config.py` are used only for dry-run estimates. For a paid run, the client fetches a fresh public pricing table before spending, then calculates token-usage cost from actual response input/output/cache-write/cache-read counts. It prints running token totals and the final cost at that tariff. This is published-tariff usage cost, not an account invoice adjusted for discounts; no invoice dollar field is returned by the Messages response.

The dry-run heuristic uses UTF-8 bytes / 3, 180 output tokens per review plus a body-token translation allowance, and one prompt-cache write followed by hits. Retries, cache expiration, additional thinking, and server-injected schema tokens are excluded. Estimates are not actual billed tokens.

**Actual live gold-run usage in this phase:** 0 requests, 0 input tokens, 0 output tokens, 0 cache-write tokens, 0 cache-read tokens, **$0.000000**. The gold run was not performed; these are zero-spend totals, not measurements of a completed annotation.

## Real commands and output

Commands below ran from the project directory with Python 3.11.6. `PYTHONDONTWRITEBYTECODE=1` avoids incidental bytecode writes and `-p no:cacheprovider` avoids pytest cache files.

### Dependency installation

```sh
.venv/bin/python -m pip install -r requirements.txt
```

Exit 0. Actual final installation output:

```text
Successfully installed annotated-types-0.8.0 anthropic-1.12.1 anyio-4.15.1 docstring_parser-0.18.0 h11-0.16.0 httpcore2-2.13.1 httpx2-2.13.1 jiter-0.17.0 pydantic-2.14.0 pydantic_core-2.50.0 python-dotenv-1.2.1 sniffio-1.3.1 truststore-0.10.4 typing-inspection-0.4.4 typing_extensions-4.16.0
```

```sh
.venv/bin/python -m pip check
```

Exit 0, output: `No broken requirements found.` Pip also warned that its normal user cache directory was not writable in the sandbox and disabled that cache; this did not prevent installation/checks.

### Offline tests

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pytest -q -p no:cacheprovider
```

Exit 0:

```text
........................................................................ [ 64%]
.......................................                                  [100%]
111 passed in 2.52s
```

Tests disable socket connections globally. Coverage includes all specified validation failures, deduplication/fan-out, metadata exclusion, first-row ratings, retry/fallback/error rows, cache hits and prompt changes, all dry-run combinations, full-run refusal without `--yes`, derived fields, exact output count/order/raw-field retention, interrupted cache recovery, response-usage cost arithmetic, schema shape, and a fake 429 retry.

The hand-built evaluator case verifies primary label accuracy 1/4, label overlap 2/4, category agreement 1/2, low-signal agreement 1/2, sentiment within one 3/4, and MAE 1.25, plus matrix cells, category denominators, and every required disagreement. Additional tests cover failed rows, perfect predictions, empty denominators, bad joins/inputs, Markdown escaping, 300-character slicing, and an untrimmed 140-row disagreement table.

### Gold dry run

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --gold --dry-run
```

Exit 0:

```text
Model: claude-haiku-5-5
Selected rows: 120; distinct text keys: 120
Keys already cached: 0; distinct keys to send: 120
Requests estimated: 5; batch size: 25
Estimated input tokens: 22018 (uncached=5763, cache_write=3251, cache_read=13004)
Estimated output tokens: 25194
Estimated cost USD: $0.013710; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
Dry run: zero API calls; no files written
```

### Credential check and skipped live commands

A local dotenv-aware presence check printed only booleans:

```text
.env exists: False
ANTHROPIC_API_KEY available: False
```

Therefore these commands **were not run**:

```sh
.venv/bin/python -m pipeline.annotate --gold
.venv/bin/python -m pipeline.evaluate
```

`data/interim/gold_annotations.csv` and `docs/handover/02-eval.md` were not created. Their conditional Done-when requirement does not apply when the key is absent.

### Full-corpus dry run

```sh
PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -m pipeline.annotate --dry-run
```

Exit 0:

```text
Model: claude-haiku-5-5
Selected rows: 14791; distinct text keys: 10837
Keys already cached: 0; distinct keys to send: 10837
Requests estimated: 434; batch size: 25
Estimated input tokens: 1868409 (uncached=457475, cache_write=3251, cache_read=1407683)
Estimated output tokens: 2218565
Estimated cost USD: $1.169513; prices read 2026-10-09
Estimate assumptions: UTF-8 bytes/3; 180 output tokens/review plus body-token allowance; one 5m prompt-cache write, then hits; excludes retries, cache expiry, extra thinking, and server-injected schema tokens.
Dry run: zero API calls; no files written
```

The source is phase 01b's current corpus, so its computed row/distinct counts differ from the first-scrape numbers in the handover. No full paid command was executed.

### Integrity checks

A local verification script checked installed files against the tested staging copies, protected-file SHA-256 values, and Python string literals. Exit 0:

```text
Python 3.11.6
11 protected input files unchanged; installed files match tested staging files
No taxonomy label/category literals in Python source
data/interim/annotations.jsonl exists: False
data/interim/gold_annotations.csv exists: False
data/annotated_reviews.csv exists: False
docs/handover/02-eval.md exists: False
```

Protected checks cover AGENTS.md, raw_reviews.csv, all preexisting docs/handover files, annotation_prompt.md, TAXONOMY.md, taxonomy.json, and gold_set.csv. Raw CSV SHA-256 remains `3c74e530d8ae2d598cadba8992b76b627438fed60d353ca5ed9cb2f538ab7030`. No scraper code or protected input was changed. The report is the only new handover document.

## Failures, surprises, and limits

Development verification in the temporary staging directory passed first with 99 tests, then with 111 after evaluator tests were added. No final test failure occurred. An auxiliary attempt to import `bs4` failed with `ModuleNotFoundError`; no dependency was added because the pricing parser uses Python's standard-library HTML parser. The initial parser needed correction for the public table's separate long-prompt row before installation; the corrected parser was checked against the fetched page and synthetic offline cases. A later browser-tool read of the model overview returned an internal error; fetching that public page with `curl -L --fail` succeeded.

Not tested: live API authentication, model availability for this account, live structured-output acceptance, live cache hit rates, live token/billing totals, real service rate limits, model label quality, and gold agreement targets. Fake-client results establish implementation behavior, not model quality. No evaluation score against the real gold set is claimed.

No input defect or unresolved implementation question was found. Claude's agreement review remains dependent on a future credentialed gold run; the full annotation remains Abhinav's responsibility afterward.

## Done when

- [x] Pytest passes offline.
- [x] Annotation/evaluator scripts and requested modes exist.
- [x] Gold/full dry-run outputs are recorded above.
- [x] Conditional live gold/eval outputs: skipped because no key was available.
- [x] This report records docs, dated prices, actual command results, zero actual spend, and untested work.

Stopped at phase 02.

