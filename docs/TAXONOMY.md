# Taxonomy v1

Written by Claude after reading a stratified sample of 300 reviews from the Oct 9, 2026 scrape
(14,791 reviews). Machine-readable copy: `analysis/taxonomy.json`. The prompt the model sees:
`docs/annotation_prompt.md`. If these three disagree, `taxonomy.json` wins for validation and this
file gets fixed.

## Labels: what kind of review is it

One or two per review. The first is the primary label.

| Label | Use when | Categories |
|---|---|---|
| Specific Praise | Positive, and names a feature, a quality, or a use case | 1-2 |
| Specific Complaint | Negative, and names a concrete problem | 1-2 |
| Feature Request | Asks for something to be added, changed, or made free | 1-2 |
| Generic Good | Positive with nothing specific ("great app", "love it") | none |
| Generic Bad | Negative with nothing specific ("worst app", "useless") | none |
| Nonsense | Unintelligible, off-topic, wrong app, abuse with no product content | none |

Rules:

- **Specific outranks generic.** "Good app but too expensive" is `Specific Complaint, Generic Good`,
  in that order.
- **Two specific labels:** order by which takes more of the text. Tie goes to the complaint.
- **Never pair** Generic Good with Specific Praise, Generic Bad with Specific Complaint, or Generic
  Good with Generic Bad. Nonsense always stands alone.
- **Naming a use case counts as specific.** "Great for research" is Specific Praise (Search &
  Sources). "Helps me study for exams" is Specific Praise (Use Cases). "Great app" is Generic Good.
- **A comparison alone is not specific.** "ChatGPT is better" is Generic Bad with a competitor tag.

## Categories: what part of the product

Up to two, most important first. Empty for Generic Good, Generic Bad, and Nonsense.

| Category | Covers |
|---|---|
| Answer Accuracy | Wrong, invented, or contradictory answers; misunderstanding the question; praise for being correct or reliable |
| Search & Sources | Web search quality, citations and links, freshness of information, research depth, Deep Research |
| Answer Style & Filters | Too long or too short, tone, rudeness, personality, bias or editorializing, refusals, content filters |
| Model Choice | Picking a model, being forced onto the default, per-model limits, asking for a model, praise for many models in one app |
| Credits & Paid Limits | The credits system; paying users running out or being asked to buy more |
| Free Limits & Paywall | Free-tier caps on questions, uploads, or photos; upgrade prompts; "it asks me to pay" |
| Pricing & Value | Too expensive, good value, regional or student pricing, free-trial requests |
| Billing & Subscription | Charges, refunds, cancelling, unauthorized charges, promo or partner offers (PayPal, carriers, Samsung), subscription ended early |
| Customer Support | Support not answering or not resolving |
| Computer & Agents | The Computer product, agent tasks, automation, Comet, building or coding tasks handed to an agent |
| Voice & Dictation | Voice mode, speech recognition, interruptions, voice quality |
| Images & Files | Sending or reading images, generating or editing images and video, file uploads and file handling |
| Threads & History | Lost chats, organizing or renaming, Spaces, memory, custom instructions |
| Bugs & Stability | Crashes, freezes, errors, cut-off responses, features that stopped working, install problems |
| Speed | Fast or slow |
| Login & Account | Sign-in, account deletion, phone-number requirement |
| UI / UX | Layout, navigation, redesigns, ease of use, tablet layout |
| Privacy & Permissions | Permissions, data collection, data deletion, the app being preinstalled |
| Use Cases | What they use it for when no feature is named: study, homework, work, daily tasks, medical or legal questions |
| Other | Specific, but fits nothing above (ads, language support, and so on) |

Tie-breakers the sample forced:

- **Credits vs free limits.** Says "credits", or says they pay (Pro, Max, subscription): Credits &
  Paid Limits. Otherwise a limit complaint is Free Limits & Paywall.
- **Limit on a feature.** "Only one photo a day" is Free Limits & Paywall first, Images & Files second.
- **Price vs paywall.** "Too expensive" is Pricing & Value. "It makes me pay to continue" is Free
  Limits & Paywall.
- **Accuracy vs search.** Wrong facts are Answer Accuracy. Bad, missing, or dead sources are Search
  & Sources.
- **Bugs vs speed.** Slow is Speed. Broken is Bugs & Stability.

## Other fields from the model

| Field | Rule |
|---|---|
| `sentiment_rating` | 1-5 from the text alone, ignoring the stars. 1 very negative, 3 neutral or mixed, 5 very positive. Nonsense gets 3. |
| `language` | ISO 639-1 code of the text as written. Romanized Hindi is `hi`. Emoji-only or undeterminable is `und`. |
| `english_translation` | Faithful translation when the language isn't English. Empty otherwise. |
| `topic` | 2-6 lowercase English words naming the specific thing ("credits run out mid task"). Empty for generic and nonsense. Feeds the opportunity clusters. |
| `competitors` | Products named in the text, from the fixed list. Empty when none. |
| `regression_claim` | True when the reviewer says the product got worse than it used to be. |

## Computed in code, never by the model

| Column | Rule |
|---|---|
| `rating_mismatch` | abs(stars - sentiment) >= 2. Same rule the Duolingo reference used. |
| `is_low_signal` | No categories. These rows count in volume and ratings and are excluded from topic work. |
| `is_duplicate_text` | Normalized text appears 3 or more times in the corpus. |
| `is_truncated` | Android text is 500 characters or longer (Play cuts reviews there). |
| `needs_translation` | `language` is not `en` and not `und`. |

There is no spam column. The reference flagged every repeated 1-3 word review as spam; in this corpus
that is 27% of rows and they are ordinary short praise.

## What the sample showed

Read before anything is labeled, so treat these as expectations to test, not findings:

- Money dominates the complaints: the credits system on paid plans, and tight free limits on photo
  and file uploads.
- Accuracy complaints are common and often arrive with "it used to be better".
- Praise clusters on research, study, sources, and speed.
- iOS reviews are longer and angrier than Android ones.
