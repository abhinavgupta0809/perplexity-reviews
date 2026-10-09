# Handover 03: site data + site

Read `AGENTS.md` first. Phase 02b passed: 14,791 reviews labeled, 0 errors, 97.5% primary-label and
94.6% primary-category agreement with the gold set. This phase turns the annotated CSV into a static
site. No API calls. No deploy.

## Inputs (read-only, written by Claude)

- `docs/DESIGN.md`: the site spec. Layout, tokens, every chart, every state. Follow it. Where it is
  silent, choose the simpler option and say what you chose in the report.
- `analysis/insights.json`: callouts, improvements, feature requests, strengths, label takeaways,
  category notes. Each item has a `match`; `match_spec` in the same file defines the semantics.
- `analysis/taxonomy.json`, `data/annotated_reviews.csv`, `data/daily_true_counts.csv`,
  `data/run.json`, `docs/handover/02-eval.md` (agreement figures, for the footer).

## Part 1: `pipeline/build_site_data.py`

Reads the inputs, writes everything under `site/data/` plus the two CSV copies. Deterministic:
same inputs, byte-identical outputs. No network.

### Matcher

Implement exactly what `match_spec` says. All fields present must hold.

- `pattern` is a case-insensitive regex searched in
  `" ".join([title, review_text, english_translation, topic]).lower()`.
- `platform` restricts to that platform.
- Reject an unknown match key, an unknown label or category, or an invalid regex with a clear error.
- **Fail the build** if any insight item matches zero reviews in the `all` scope.

For reference, counts Claude got in the `all` scope with this exact logic. Your build must reproduce
them; a difference means the matcher differs:

| id | n | id | n | id | n |
|---|---|---|---|---|---|
| c_money | 1059 | i_bugs | 228 | f_free_uploads | 89 |
| c_accuracy | 444 | i_style | 177 | f_pricing | 50 |
| c_regression | 235 | i_voice | 117 | f_search | 22 |
| c_lowsignal | 5115 | i_history | 84 | f_ui | 21 |
| c_ios | 424 | i_support | 71 | f_voice | 19 |
| i_credits | 202 | i_computer | 68 | f_threads | 19 |
| i_free_images | 161 | i_models | 69 | f_computer | 13 |
| i_free_questions | 507 | i_login | 60 | f_models | 12 |
| i_wrong | 444 | i_preinstalled | 63 | s_research | 556 |
| i_ignores | 73 | s_sources | 550 | s_study | 308 |
| i_cancel | 120 | s_accuracy | 730 | s_speed | 464 |
| i_promos | 57 | s_models | 44 | | |

Put these in a test as the expected values for the current data, and print a comparison in the
report.

### Tokens

Fill `{{count}}`, `{{pct_low_star}}`, `{{avg_rating}}`, `{{ios_count}}`, `{{android_count}}`,
`{{pct_of_substantive}}` in `title`, `text`, and `desc` from the item's own match, per scope.
`pct_low_star` = share of matched reviews with 1 or 2 stars. `pct_of_substantive` = matched reviews
over reviews with at least one category in that scope. Counts as integers with thousands
separators, percentages as whole numbers with `%`, ratings to two decimals. An unknown token fails
the build.

### Outputs

- `site/data/summary.json`: under each of `all`, `android`, `ios`, everything the Overview, the
  Deep Dive headers and sidebars, the Opportunities signal charts, and the footer need. Also
  top-level `meta`: run time, date range, generated-at, gold agreement figures parsed from
  `02-eval.md`, per-platform totals.
- `site/data/insights.json`: every insight item with resolved text per scope, stats per scope
  (count, pct_low_star, avg_rating, android_count, ios_count), and the matched `review_id` list.
- `site/data/reviews.json`: all reviews in a compact form (short keys or arrays-of-columns, your
  choice), with the fields the review card and the filters need. Report its raw and gzipped size.
- `site/raw_reviews.csv`, `site/annotated_reviews.csv`: copies.

Definitions that must hold everywhere:

- **Weeks** start Monday, UTC. A week is complete only if all 7 days fall inside
  `[first full day of the window, last day with reviews minus 1]`. Charts use complete weeks only.
  Chart 1 (volume) uses `daily_true_counts.csv`; the others use the annotated rows.
- **Primary label** = first label. **Category counts** count a review once per category it has.
- **Substantive** = at least one category.
- Means over an empty set are null, never 0. The site shows "n/a".
- Top topics per label and per category: the 10 most frequent non-empty `topic` strings, with counts.

### Tests

Offline, against a small hand-built annotated fixture where every expected number is worked out by
hand in the test: each match field alone and combined; unknown key, bad regex, and zero-match
failures; token filling and the unknown-token failure; week completeness at both edges; scope
separation; null means; determinism (two runs, identical bytes). Plus the expected-count table above
as a test against the real data, skipped with a clear message if the real CSV is absent.

## Part 2: the site

Build `site/` per `docs/DESIGN.md`. Vanilla JS, no framework, no build step, Chart.js 4.4.1 from
cdnjs and nothing else external.

Hard requirements, each of which Claude will check:

1. No number, date, or count appears in `index.html`, `app.js`, or `charts.js` as a literal. Grep
   for the review total to prove it.
2. Review text, titles, translations, and topics are set with `textContent`. No `innerHTML` with
   data in it.
3. The platform toggle changes every tab, including open lists and drawers.
4. Tab and platform are in the URL hash and restore on load.
5. No dual-axis chart anywhere.
6. Every chart has a working "View as table" toggle and a tooltip.
7. Light and dark both work, and charts redraw on theme change.
8. At 375px wide: no horizontal page scroll, sidebar becomes a select, drawer goes full screen.
9. Keyboard: every control reachable, drawer traps and returns focus, Esc closes it.

Add `site/README.md` with the one command to serve locally (`python3 -m http.server` from `site/`).

## Run it

1. `pytest`, offline.
2. `python -m pipeline.build_site_data`. Put the matcher comparison table and the file sizes in
   your report.
3. Serve `site/` locally and load it. If you can drive a headless browser, capture the console for
   errors on each tab and say so. If you can't, say that plainly; Claude will do the browser pass.

## Done when

- [ ] `pytest` passes offline
- [ ] `build_site_data.py` reproduces all 35 expected counts
- [ ] `site/` loads from a local server with no console errors on any tab (or you state you
      couldn't check)
- [ ] The nine hard requirements are met; for each, one line in the report on how you verified it
- [ ] `docs/handover/03-report.md` per `AGENTS.md`, including anything in DESIGN.md you found
      ambiguous or impractical and what you did instead

Don't commit. Don't deploy. Don't edit `insights.json`, `DESIGN.md`, the taxonomy, or the prompt.
