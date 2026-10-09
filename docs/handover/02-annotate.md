# Handover 02: annotate + evaluate

Read `AGENTS.md` first. Phase 01b passed review. This phase builds the labeling script and the
evaluator, and runs them **on the gold set only**. The full run is Abhinav's, after Claude signs off
on agreement.

## Inputs (read-only, written by Claude)

- `docs/annotation_prompt.md`: the system prompt, between the `PROMPT START` / `PROMPT END` markers.
  Load it from the file at run time.
- `analysis/taxonomy.json`: allowed labels, categories, competitors, limits, forbidden label pairs.
  Validation reads this. No label or category string appears in Python source.
- `analysis/gold_set.csv`: 120 reviews Claude labeled by hand. Columns `review_id, platform, rating,
  gold_labels, gold_categories, gold_sentiment`; multiple values are joined with ` | `.
- `docs/TAXONOMY.md`: the human-readable version, for your context.

## Build

```
pipeline/annotate.py     raw_reviews.csv -> data/annotated_reviews.csv
pipeline/evaluate.py     annotations vs gold -> docs/handover/02-eval.md
tests/                   offline tests with a fake client
```

### Model and API

- Anthropic API, model `claude-haiku-5-5`, key from `ANTHROPIC_API_KEY` in `.env`. Add `anthropic`
  (pinned) and a dotenv loader to `requirements.txt`; update `.env.example`.
- **Read the current Anthropic docs before writing the client code.** Don't code the API from memory.
  Use whatever the docs currently recommend for: schema-enforced JSON output, caching the long
  system prompt across requests, and rate-limit handling. Say in your report which doc pages you used.
- Lowest-variance sampling settings the model allows.
- Take the per-token prices from the current pricing page, put them in `config.py` with the date you
  read them, and use them only for the dry-run estimate.

### What gets sent

- Deduplicate first. Key = lowercase, whitespace-collapsed `title + "\n" + review_text`. Label each
  distinct key once and copy the result to every row that shares it. (10,270 distinct texts out of
  14,102 rows in the first scrape, so this cuts spend by about a quarter.) Use the star rating of the
  first row for the key.
- User message: a JSON array of `{"i", "stars", "title", "text"}`, about 25 reviews per request.
  Make batch size a flag.
- Nothing else goes to the API. No ids, dates, countries, or versions.

### What comes back, and validation

Per review: `labels`, `categories`, `sentiment`, `language`, `english_translation`, `topic`,
`competitors`, `regression_claim`, as the prompt defines them. Validate every result against
`taxonomy.json`:

- every `i` present exactly once
- 1-2 labels, 0-2 categories, all from the allowed lists, no repeats
- no forbidden label pair; `Nonsense` alone
- categories empty exactly when no label is in `specific_labels`
- sentiment an integer 1-5; competitors from the allowed list
- `topic` empty when categories are empty

On a validation failure, retry that batch once. If a review still fails, resend it alone once. If it
still fails, write the row with empty annotation fields and `annotation_error` set to the reason.
Never repair a label in code and never drop the row.

### Cache and resume

Append each validated result to `data/interim/annotations.jsonl`, keyed by
`sha256(prompt text + model id + text key)`. A rerun sends only keys missing from the cache. Editing
the prompt or changing the model re-labels everything, which is intended.

### Modes

| Flag | Behavior |
|---|---|
| `--dry-run` | No API calls. Prints distinct keys to send, keys already cached, estimated input and output tokens, and estimated cost. Works with every other flag. |
| `--gold` | Only the reviews in `analysis/gold_set.csv`. Writes `data/interim/gold_annotations.csv`, not the main output. |
| `--limit N` | First N uncached keys, for smoke tests. |
| (none) | Everything. Refuses to start unless `--yes` is also passed, and prints the dry-run estimate first. |

Print running totals of actual input and output tokens from the API responses, and the actual cost
at the end.

### Output: `data/annotated_reviews.csv`

All 12 raw columns unchanged, then:

| Column | Source |
|---|---|
| `labels` | model, joined with `, ` |
| `categories` | model, joined with `, ` |
| `sentiment_rating` | model |
| `language` | model |
| `needs_translation` | code: language is not `en` and not `und` |
| `english_translation` | model |
| `topic` | model |
| `competitors` | model, joined with `, ` |
| `regression_claim` | model, TRUE/FALSE |
| `rating_mismatch` | code: abs(rating - sentiment_rating) >= `mismatch_threshold` |
| `is_low_signal` | code: categories empty |
| `is_duplicate_text` | code: this row's text key occurs 3+ times in the corpus |
| `is_truncated` | code: platform is android and len(review_text) >= 500 |
| `annotation_error` | empty when fine |

Derived booleans are TRUE/FALSE. Where sentiment is missing, `rating_mismatch` is empty, not FALSE.
Row count and order must match `raw_reviews.csv` exactly.

### Evaluator (`evaluate.py`)

Compares `data/interim/gold_annotations.csv` to `analysis/gold_set.csv` and writes
`docs/handover/02-eval.md`. All of it computed, none typed:

1. **Primary label accuracy**: model's first label == gold's first label. Target >= 85%.
2. **Label set overlap**: share of rows where the two label sets share at least one label.
3. **Primary category agreement**: over rows where gold has categories, model's first category is in
   gold's category set. Target >= 80%.
4. **Low-signal agreement**: over rows where gold has no categories, model has none either.
5. **Sentiment**: share within 1 point of gold, and mean absolute error.
6. Confusion matrix of primary labels (gold rows, model columns).
7. Per-category table: gold count, and how often the model's primary category agreed.
8. **Every disagreement on metrics 1, 3, or 4**, as a table: review id, stars, the review text
   (first 300 characters), gold labels and categories, model labels and categories, model topic.
   Claude reads this table to decide whether the prompt or the gold label was wrong, so don't trim it.
9. Count of rows with `annotation_error`.

### Tests

Offline, fake client, no network. Cover: text-key normalization and fan-out to duplicates; each
validation rule above with a failing case; retry then single-review fallback then error row; cache
hit skips the call; prompt change invalidates the cache; `--dry-run` makes zero calls; full run
without `--yes` refuses; derived columns including the empty-mismatch case; output row count and
order equal input; each evaluator metric on a small hand-built case.

## Run it

1. `pytest`, offline.
2. `annotate.py --gold --dry-run`. Put the output in your report.
3. If `ANTHROPIC_API_KEY` is set, run `annotate.py --gold` for real, then `evaluate.py`. This is
   120 short reviews, a few cents. If the key isn't set (there was no `.env` when this was written),
   stop there and say so. Don't ask for the key in chat and never print it.
4. `annotate.py --dry-run` for the full corpus. Put the estimate in your report. **Do not run the
   full annotation.**

## Done when

- [ ] `pytest` passes offline
- [ ] `annotate.py` and `evaluate.py` exist with the modes above
- [ ] Gold dry-run and full dry-run outputs are in the report
- [ ] If a key was available: `data/interim/gold_annotations.csv` and `docs/handover/02-eval.md` exist
- [ ] `docs/handover/02-report.md` per `AGENTS.md`: doc pages used, prices and the date you read
      them, real command output, actual gold-run tokens and cost, what wasn't tested

Don't commit. Don't edit the prompt, taxonomy, or gold set; if one looks wrong, say so in the report.
