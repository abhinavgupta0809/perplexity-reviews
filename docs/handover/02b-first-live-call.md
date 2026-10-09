# Handover 02b: make the first live call safe, run gold, then run everything

Read `AGENTS.md` first. Phase 02 passed code review: 111 tests pass, both dry runs reproduce, and
Claude checked your prices against the live pricing page (they match). Nothing here is a redesign.
These are six small changes so the first paid request doesn't fail for an avoidable reason, then the
gold run that phase 02 couldn't do without a key, then the full corpus.

**Abhinav has authorized you to run the full annotation in this phase** (Oct 9, 2026). The estimate
is about $1.17 and a rerun after a prompt change costs about the same, so there is no reason to wait
for a separate approval. This overrides the "never run the full annotation yourself" line in
`AGENTS.md` for this phase and for reruns Claude asks for.

## Changes

### 1. Schema root must be an object

`output_schema` returns a top-level array. Every example on the structured-outputs page uses an
object root, and the page never says an array root is accepted. Don't find out with a 400.

- Root: `{"type": "object", "properties": {"results": <the current array schema>},
  "required": ["results"], "additionalProperties": false}`.
- Parse `payload["results"]`. A response without that key is a validation failure for the batch.
- Claude already changed `docs/annotation_prompt.md` (now v2) to ask for `{"results": [...]}`.

### 2. Show the API's error message on 4xx

`APIClient.create` raises `Anthropic HTTP 400; no response body logged`. The docs say an unsupported
schema feature returns "a 400 error with details", and those details are the only way to fix it.

- For 4xx other than 429, include the API's error `type` and `message` in the raised error.
- Still never log the request body, review text, or the key.

### 3. Don't lose an annotation over formatting

The validator currently fails a whole result for cosmetic reasons, which costs retries and can end
in an `annotation_error` row with every label blank. Labels and categories stay strict. Loosen only
these:

| Field | Now | Change to |
|---|---|---|
| `topic` | must be 2-6 lowercase ASCII words | strip and lowercase it in code; valid if non-empty and at most 80 characters when categories exist; still must be empty when they don't |
| `language` | exactly two letters or `und` | lowercase it; accept `xx`, `xxx`, or either with a region suffix (`zh-tw`); store the part before the hyphen |
| `english_translation` when language is `en` or `und` | must be empty, else fail | set it to empty in code |
| `english_translation` when language is anything else | must be non-empty | keep this rule |

### 4. Enum casing

The structured-outputs page says a returned enum value can differ from the schema only in
capitalization and tells you to compare case-insensitively. For `labels`, `categories`, and
`competitors`: match case-insensitively and store the canonical string from `taxonomy.json`. This is
the one exception to "never repair a label in code". A value that doesn't match in any casing still
fails.

### 5. Price check must not block a run forever

`live_prices()` scrapes the docs page before any paid call and aborts if the table layout changes.
Keep that as the default. Add `--offline-prices`: skip the fetch, use the dated prices in
`config.py`, and print one line saying the reported cost uses prices read on that date.

### 6. Spend guard

Add `--max-cost USD` (default 5.00). After each response, if the running actual cost exceeds it,
stop cleanly: keep the cache, don't write the output CSV, exit non-zero with the amount spent. This
is a backstop against a retry loop or a pricing surprise, not a budget.

### Tests

Update the affected tests and add: `--max-cost` stops mid-run with the cache intact and no output CSV; object-root schema shape; response missing `results`; a 4xx
error surfaces type and message but not the request body; each loosened rule with a passing and a
failing case; case-insensitive enum match stores the canonical value; `--offline-prices` makes no
HTTP request. `pytest` passes offline.

## Run it

1. `pytest`.
2. `annotate.py --gold --dry-run`.
3. If `ANTHROPIC_API_KEY` is set: `annotate.py --gold`, then `evaluate.py`. If the first request
   returns a 4xx, stop, put the error type and message in the report, and don't retry with guesses.
   If there's still no key, stop and say so.
4. Look at the gold run before spending more. Stop here and report, without running the full
   corpus, if any of these is true: more than 6 of the 120 gold rows have `annotation_error`; any
   request ended on a 4xx; actual gold cost was more than ten times the dry-run estimate. These
   mean the pipeline is wrong, and a full run would repeat the fault 100 times over.
5. Otherwise run the full corpus whatever the agreement numbers say: `annotate.py --dry-run`, then
   `annotate.py --yes`. Low agreement is Claude's problem to fix in the prompt, and the full output
   helps diagnose it. Let it finish; if it is interrupted, rerun the same command and it resumes
   from the cache.
6. After the full run, print for the report: row count of `data/annotated_reviews.csv` against
   `raw_reviews.csv`, count of `annotation_error` rows, and counts per primary label.

## Done when

- [ ] `pytest` passes offline
- [ ] The six changes above are in, with tests
- [ ] If a key was available: `data/interim/gold_annotations.csv` and `docs/handover/02-eval.md`
      exist, generated by the scripts
- [ ] Unless a stop condition in step 4 fired: `data/annotated_reviews.csv` exists with the same row
      count and order as `raw_reviews.csv`
- [ ] `docs/handover/02b-report.md`: real command output; for the gold run and the full run
      separately, actual requests, tokens by type, cost, how many batches needed a retry, how many
      reviews fell back to single calls, any `stop_reason` other than `end_turn`, and the count of
      `annotation_error` rows

## Leave alone

Accepted in review as they are: the dedupe and cache design, the cache lock, retry-then-single
fallback, the dry-run estimator, default sampling settings, and the evaluator.

Don't commit. Don't edit the prompt, taxonomy, or gold set.
