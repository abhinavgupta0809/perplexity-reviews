# Handover 03b: polish before deploy

Read `AGENTS.md` first. Phase 03 passed review. Claude reran the tests (176 pass), recounted the
headline numbers from the CSV (they match `summary.json`), and drove the site in headless Chrome:
all four tabs render, the platform toggle and hash work, the drawer traps and returns focus, light
and dark both work, there is no horizontal scroll at 375px, and the console is clean.

What follows is what the browser pass turned up. Small changes, no new features. No API calls, no
deploy, no commit.

`docs/DESIGN.md` is updated where an item below changes the spec. Where they differ, this file wins.

## Fixes

1. **Deep Dive shows two selectors on desktop.** The "Choose a group" select and the sidebar list
   both render at 1440px. Show the list at 640px and wider and the select below that, never both.

2. **"More" appears on every review card,** including three-word reviews. Show it only when the
   text is actually clamped (measure after render, re-check on resize). When expanded, it reads
   "Less".

3. **"0 helpful" on most cards.** Show the helpful count only when it is above zero.

4. **Languages chart shows codes** (`en`, `es`, `und`). Show language names, using
   `Intl.DisplayNames` in the browser with the code as fallback; `und` reads "Undetermined". Same
   for the language filter on the Reviews tab and the language tag on review cards.

5. **Reviews tab filter row is misaligned,** and "Platform: All" renders as loose text. Remove the
   platform item from this row (the global toggle already does that job) and align the remaining
   labels and controls on one grid: label above control, equal heights, wrapping cleanly.

6. **Reviews tab opens on a wall of "nice app".** Default sort becomes Most helpful.

7. **Feature requests chart sits alone in a half-empty row** on Opportunities. Lay the three signal
   charts out as three equal columns at 1100px and wider, one column below that.

8. **Top topics are too fragmented to be useful** (most chips show a count of 2 or 3). Show only
   topics with 5 or more reviews in the current scope, and hide the "Top topics" block entirely when
   none qualify.

9. **The weekly stars and sentiment lines look flat** on a 1 to 5 axis. Set the y-axis to 3.0 to
   5.0 for that one line chart and say so in its subtitle ("y-axis starts at 3"). Bar charts keep
   their full axes.

10. **Deep Dive selection isn't in the URL.** Add the mode and the selected group to the hash
    (`#deep-dive?platform=ios&mode=categories&group=Credits%20%26%20Paid%20Limits`) and restore
    them on load. Unknown values fall back to the first group without an error.

11. **Say how sentiment is computed.** Sentiment averages leave out the 367 Nonsense reviews, which
    is right, but nothing on the page says so. Add it to the Average sentiment tile's subtext and to
    the footer method line. The count comes from the data, not typed.

12. **Keep abusive text off the page.** A few Nonsense-labeled reviews are slurs and abuse with no
    product content. On the site only: in every list, a Nonsense-labeled review shows "Off-topic
    review hidden" with a "Show" button instead of its text. They still count in every number and
    stay in both CSV downloads unchanged.

## Also

- Add a root `README.md` section "Deploy": the site is the `site/` folder, static, no build step;
  `cd site && vercel deploy --prod`. Don't run it.
- `site/data/*.json` were written with owner-only permissions (600). Write generated site files as
  644 so any static host can serve them.

## Tests and checks

Update tests where data shape changes (item 11 needs the Nonsense count in `summary.json` if it
isn't there). `pytest` passes offline. Rebuild site data. Then load each tab in the headless browser
again and confirm: clean console; items 1, 2, 3, 10 behave as described at 1440px and 375px.

## Done when

- [ ] `pytest` passes offline
- [ ] All 12 items done; one line each in the report on how you verified it
- [ ] `docs/handover/03b-report.md` per `AGENTS.md`

Don't commit. Don't deploy. Don't edit `insights.json`, the taxonomy, or the prompt.
