# Site design spec, v2

Written by Claude. v2 replaces the v1 look after Abhinav's review of the first build: "every text
is white, every chart is blue", too few chart forms, and volume and rating should share one chart.
Structure, tabs, data rules, and behavior from v1 stand unless this file changes them.

Reference for behavior: https://duolingo-reviews.vercel.app/.

## As built (Oct 9, 2026)

Claude built v2 directly. Where the build differs from the sections below, the build is right:

- **Stat band, not tiles.** The six headline figures sit on one surface with dividers and a colored
  dot beside the label, not six cards with top rules.
- **Briefing beside the waterfall.** The five callouts are a list next to the lead chart, each with
  its count as a figure and a colored dot. No side rules.
- **No kicker labels** above headings, and no Unicode glyphs as icons. Icons are inline SVG.
- **Categories split by first label**, so each stacked bar sums to the category total.
- **Languages donut uses a one-hue violet ramp** (`--seq-1` to `--seq-6`), because reusing the
  meaning colors there would make green read as "praise".
- **The matrix uses a log x-axis** and short names (`short` on each improvement in
  `analysis/insights.json`) so sixteen bubbles can be labeled without collisions.
- **Two donuts stack their legend under the chart** in the three-column mood row.
- Mismatch by label is a meter table beside "Label mix by platform".

Changes after Abhinav's second review (Oct 9, 2026). These override the token tables below:

- **Light is the default theme** (`data-theme="light"` on `<html>`), and it is cream: page
  `#f5efe3`, surface `#fdf9f1`, raised `#fffdf8`, border `#e6dccb`, warm text grays.
- **Teal is the accent and the heading color**, at Abhinav's request, as a nod to Perplexity:
  `--brand` and `--accent` are `#1a6f7a` light and `#4fb8c6` dark. Violet stays as the sentiment
  series only. The footer still says independent and unofficial; no logo or wordmark is used.
- **Volume bars are teal** (`--volume` `#20808d` light, `#3aa6b5` dark), drawn translucent behind
  the lines, replacing the gray that read as dead on the dark theme.
- **Byline under the title:** "Built by Abhinav Gupta, MS Product Management at CMU", with
  LinkedIn and GitHub links.

## What was wrong with v1

- **One color doing every job.** Twelve charts in the same blue. Color carried no meaning, so
  nothing on the page said "good" or "bad" until you read the numbers.
- **One text weight.** Titles, values, subtitles, axis ticks, and metadata all near-white. No
  reading order.
- **One chart form.** Horizontal bars, repeated. Composition, change, and priority all drawn the
  same way.
- **One card, tiled.** A uniform two-column grid with no lead story.

## Direction

An analyst's briefing, not an admin panel. Dark and calm, with color spent only where it means
something. A reader should be able to squint at any chart and tell praise from complaint.

Three rules carry the whole redesign:

1. **Color means sentiment.** Green is praise, red is complaint, blue is a request, gold is stars.
   The same everywhere: charts, chips, cards, review badges.
2. **Four levels of text.** Only headings and figures get the brightest ink.
3. **The form follows the question.** Composition gets a donut or a stack. Change over time gets
   the combo chart. Priority gets a matrix. "Where did the reviews go" gets a waterfall.

## Principles (unchanged)

1. **Nothing typed.** Every number comes from `site/data/*.json`.
2. **Show the denominator.** Any subset figure shows its n.
3. **Signals, not verdicts.** The evidence note stays on Opportunities.
4. **Own identity.** No Perplexity logo, wordmark, or brand colors. Footer says independent and
   unofficial.

## Stack

Static, no build step, no framework. Chart.js 4.4.1 from cdnjs. Fonts from Google Fonts: IBM Plex
Sans (400, 500, 600) and IBM Plex Mono (500), `display=swap`, with the system stack as fallback.
Nothing else external.

## Tokens

On `:root`. Dark values go under both `@media (prefers-color-scheme: dark)` guarded by
`:root:not([data-theme="light"])`, and `:root[data-theme="dark"]`. Dark is the designed-first theme.

### Surfaces and text

| Token | Dark | Light | Use |
|---|---|---|---|
| `--page` | `#0e0f12` | `#f4f3ef` | page |
| `--surface` | `#15171c` | `#fcfcfb` | cards |
| `--raised` | `#1c1f26` | `#ffffff` | drawer, tooltips, active controls |
| `--border` | `#2a2d35` | `#e2e0da` | hairlines, gridlines |
| `--text-1` | `#f4f4f2` | `#0b0b0b` | headings, tile figures, card titles |
| `--text-2` | `#c3c2b7` | `#3d3c39` | body copy, review text |
| `--text-3` | `#8d8c84` | `#6b6a65` | subtitles, metadata, axis ticks, legends, "n=" notes (5.3:1 on cards in both themes) |
| `--text-4` | `#62615c` | `#9b9a94` | disabled controls and decoration only. Never for text a reader needs: it is under 3:1. |
| `--accent` | `#9085e9` | `#4a3aa7` | selection, focus ring, active tab, links |

Review text and body copy are `--text-2`, not `--text-1`. If a block of copy looks white, it's wrong.

### Meaning colors

One hue per meaning. These are the only data colors on the site.

| Token | Meaning | Dark | Light |
|---|---|---|---|
| `--praise` | Specific Praise, positive, 4-5 stars | `#199e70` | `#1baf7a` |
| `--good` | Generic Good | `#c98500` | `#eda100` |
| `--request` | Feature Request, Explore tag | `#3987e5` | `#2a78d6` |
| `--bad` | Generic Bad | `#d55181` | `#e87ba4` |
| `--nonsense` | Nonsense | `#9085e9` | `#4a3aa7` |
| `--complaint` | Specific Complaint, negative, 1-2 stars, Fix tag | `#e66767` | `#e34948` |
| `--stars` | the star-rating series | `#c98500` | `#eda100` |
| `--sentiment` | the LLM-sentiment series | `#9085e9` | `#4a3aa7` |
| `--android` | Android series | `#3987e5` | `#2a78d6` |
| `--ios` | iOS series | `#d95926` | `#eb6834` |
| `--volume` | quiet backdrop bars (3.4:1 on cards) | `#666b79` | `#8a8880` |
| `--neutral` | 3 stars, mixed, "other" | `#55554f` | `#c9c8c2` |

**Label order is fixed:** Specific Praise, Generic Good, Feature Request, Generic Bad, Nonsense,
Specific Complaint. This order passed the dataviz palette validator in both themes; a different
order puts red beside pink or violet beside blue and fails. Use it for every legend, stack, and
donut.

**Five-step rating ramp** (for 1 to 5 stars or sentiment, low to high):
dark `#e66767 · #a8504f · #55554f · #2f7d62 · #199e70`;
light `#e34948 · #f0a39f · #c9c8c2 · #8fd4b7 · #1baf7a`.

Rules:

- Text never takes a data color. A colored dot, bar, or rule beside it carries the meaning.
- Green and red are never the only difference. Every mark that uses them also has a label, a
  value, or a position that says the same thing.
- Three light-theme colors (`--praise`, `--good`, `--bad`) are under 3:1 on the light surface, so
  every chart keeps its value labels and its table view.

## Type

- IBM Plex Sans for everything; IBM Plex Mono for figures: tile numbers, card counts, axis ticks,
  table numbers, the n beside a title. Tabular figures on.
- Scale: page title 32/36 600 · section title 20/26 600 · card title 15/20 600 · body 14/22 400 ·
  meta 12/16 500 · kicker 11/14 600 uppercase, +0.08em tracking, `--text-3`.
- Tile figure 34/38 Mono 500. Opportunity-card count 28/30 Mono 500.

## Layout

Max width 1280px, 24px gutters (16px under 640px), 12-column grid. Cards have 14px radius, a 1px
`--border`, no shadow in dark. Vary card spans by importance; the grid is no longer two equal
columns. Each tab opens with one lead element.

Header, sticky control row (tabs left, platform toggle right), URL hash, and footer are as built.
The active tab and active toggle use `--accent`, not white.

## Chart rules

- Every chart keeps: title, one-line subtitle, hover tooltip with value and n, "View as table".
- Gridlines `--border` at low contrast, horizontal only on vertical charts. Axis ticks `--text-3`
  in Mono.
- Bars: 4px radius on the data end. 2px surface-colored gap between stacked segments and between
  donut segments.
- Legends sit above the plot, left-aligned, with a colored dot and `--text-3` label.
- Time series are weekly, complete weeks only.
- A group with fewer than 30 reviews in scope is drawn at 45% opacity with "n<30".
- Charts read colors from the tokens and redraw on theme change.

## Tab 1: Overview

**Row A, tiles (6).** Same six as built. Each tile gets a 3px top rule in a meaning color: Average
stars `--stars`, Average sentiment `--sentiment`, Substantive `--praise`, Rating mismatch
`--complaint`, the rest `--border`. Figure in `--text-1` Mono, label as a kicker, sub-line in
`--text-3`.

**Row B, lead chart, full width: "Where the signal is"** (waterfall). Floating bars, left to
right: Total reviews · minus Generic Good · minus Generic Bad · minus Nonsense · equals
Substantive · then Substantive split into three bars side by side: Praise, Complaints, Requests.
The removed steps hang down from the running total in their label colors at 55% opacity; Total and
Substantive are `--volume` with a `--text-1` value; the three split bars are full-strength
`--praise`, `--complaint`, `--request`. Thin connector lines between steps. Values come from
primary labels, so the arithmetic closes exactly. Subtitle: "By primary label. Everything in Deep
Dive and Opportunities rests on the substantive reviews."

**Row C, callouts.** The five insight callouts as a strip. Each: its count as a large Mono figure
on the left, title and text on the right, and a 3px left rule: `--complaint` for c_money,
c_accuracy, c_regression; `--accent` for c_lowsignal and c_ios.

**Row D, "Volume and rating by week"** (combo, full width). One chart, as Abhinav asked: weekly
review count as `--volume` bars on the left axis; average stars as a `--stars` line and average
sentiment as a `--sentiment` line on the right axis. This is a two-axis chart, so it carries
guardrails: left axis titled "Reviews" and starting at 0; right axis titled "Average, 1 to 5",
fixed at 1 to 5, ticks tinted to match the lines; lines 2.5px with 4px points; legend lists all
three; tooltip shows all three values for the week.

**Row E, mood (three cards, 4/4/4).**

- **"What kind of review"**: donut, six labels in the fixed order, total in the center in Mono.
  Legend to the right as a list: dot, label, count, percent.
- **"How the text reads"**: donut of sentiment in three groups: positive (4-5) `--praise`,
  neutral (3) `--neutral`, negative (1-2) `--complaint`. Center shows the positive share.
  Subtitle notes Nonsense is left out.
- **"Stars vs sentiment"**: grouped bars at 1 to 5, `--stars` and `--sentiment`.

**Row F, topics (7/5).**

- **"What reviews are about"**: horizontal stacked bars, one per category, sorted by total.
  Segments: praise `--praise`, requests `--request`, complaints `--complaint`, by which specific
  label the review carries (a review with two specific labels counts in each). Total at the bar
  end.
- **"Satisfaction by category"**: diverging bars around 3.0 stars. Categories above 3 extend
  right in `--praise`, below 3 extend left in `--complaint`, sorted high to low, value at the bar
  end, a visible center line labeled "3.0".

**Row G (6/6).**

- **"Label mix by platform"**: two 100% stacked bars, fixed label order, n on each. As built,
  recolored.
- **"Stars by Android version"**: a line with points in `--stars`, version order on x, y from 3.5
  to 5 stated in the subtitle, point radius scaled gently by review count. Hidden in iOS scope.

**Row H (4/4/4).**

- **"'It got worse' per week"**: area chart in `--complaint` at 25% fill with a 2px line.
- **"Competitors named"**: horizontal stacked bars per competitor split by the reviewer's stars:
  1-2 `--complaint`, 3 `--neutral`, 4-5 `--praise`. Total at the end.
- **"Languages"**: donut of English vs the next five languages vs Other, using the rating-free
  series order `--android`, `--ios`, `--praise`, `--good`, `--bad`, `--nonsense`, `--neutral`
  (Other is always `--neutral`), with a legend list showing counts.

**Row I.** "Mismatch by label" table as built, inline bars in `--complaint`.

## Tab 2: Deep Dive

As built, with:

- Sidebar dots use the label's color in Labels mode. In Categories mode each row gets a 4px-wide
  mini bar showing its praise-to-complaint split in `--praise` / `--complaint`.
- Detail header gains a **composition bar**: one full-width 10px stacked bar of praise, requests,
  complaints for the group, with the three counts beneath. For a label, the bar shows the star
  split on the five-step ramp instead.
- Stats row figures in Mono; "at low stars" shows a small `--complaint` dot, mean stars a
  `--stars` dot.

## Tab 3: Opportunities

**Lead chart, full width: "Size against pain"** (priority matrix). A bubble chart of the 16
improvement items: x = reviews matched, y = share at 1-2 stars, bubble area = reviews, color =
`--complaint` for Fix and `--request` for Explore. Every bubble is labeled with a short title.
Quadrant lines at the medians, with quiet corner captions: "Big and painful", "Small but severe",
"Big, milder", "Watch". Clicking a bubble scrolls to its card. Under 640px this becomes a ranked
list with two inline bars per item.
Quadrants (2026-10-09): solid lines at the median size and the median pain, each with a boxed label drawn above the bubbles at whichever end of the line is clear. Each quadrant is tinted (strongest for big and painful, none for small and milder) and carries a corner heading in `--brand`, 16px bold: its name and how many areas fall in it, with one line below saying what the position means. Counts are computed from the plotted points. The y range adds a band above the highest and below the lowest bubble so the headings never share space with bubbles; ticks and grid lines show only 0 to 100%. The x range adds room at both ends so edge bubbles are not clipped. Bubble labels avoid the headings.

**Signal row (three cards)** as built, recolored: complaints and requests by category as stacked
`--complaint` / `--request`; pain score in `--complaint`; feature requests by theme in `--request`.

**Cards.**

- Improve cards: a 3px top rule (`--complaint` Fix, `--request` Explore); the count as a large
  Mono figure top right; a **pain meter** under the description, a 6px track filled to the
  low-star share in `--complaint`, with the percent beside it; Android and iOS counts as two small
  dots in `--android` / `--ios` with numbers.
- Feature-request cards: `--request` top rule, count figure, no meter.
- "What to protect" cards: `--praise` top rule, count figure, mean stars with a `--stars` dot.

## Tab 4: Reviews

As built.

## Review card

As built, with:

- Star badge filled by rating: 1-2 `--complaint`, 3 `--neutral`, 4-5 `--praise`, at 18% opacity
  with the number in `--text-1`.
- Label chips carry their color dot; category chips are plain.
- Metadata row in `--text-3` Mono; review text in `--text-2`; iOS title in `--text-1`.

## Motion

Charts draw in once, 400ms ease-out, no bounce. The drawer slides 200ms. Honor
`prefers-reduced-motion` by turning both off.

## States and accessibility

As built. In addition: every text-on-surface pair meets 4.5:1 (`--text-3` is the tightest at
5.3:1 on cards and 4.9:1 on the light page), focus rings are 2px `--accent`, and the donut legends are real
lists so a screen reader gets the numbers.
