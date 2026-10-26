# Review volume report (merged corpus)

Corpus window: 2026-07-11T06:03:20Z through 2026-10-25T23:59:59Z, inclusive, for android; ios keeps the base run's coverage (through 2026-10-09T06:03:20Z). Uncapped: every review kept, nothing sampled.

Built by appending a later scrape (run time 2026-10-25T23:59:59Z) to the base corpus (run time 2026-10-09T06:03:20Z) with pipeline/append_gap.py. Base rows and their annotations are unchanged. Only review IDs absent from the base, dated after the base's newest review on their platform, were added.

Not extended: ios. Not extended because Apple's App Store review feed returned almost nothing on 2026-10-26: across eight attempts from about 06:37 to 07:53 UTC, 11 to 15 of the 15 storefronts returned an empty first page each time, and the US feed never reached back to the previous run's newest iPhone review (2026-10-07T16:30:17Z).

## Merged corpus

| Platform | Reviews | First day | Last day |
| --- | --- | --- | --- |
| android | 16167 | 2026-07-11 | 2026-10-25 |
| ios | 1087 | 2026-07-11 | 2026-10-07 |

## Kept from the base run

| Platform | Reviews | First day | Last day |
| --- | --- | --- | --- |
| android | 13704 | 2026-07-11 | 2026-10-08 |
| ios | 1087 | 2026-07-11 | 2026-10-07 |

Newest base review per platform: android 2026-10-08T06:01:23Z, ios 2026-10-07T16:30:17Z.

## Added from the later run

| Platform | Reviews | First day | Last day |
| --- | --- | --- | --- |
| android | 2463 | 2026-10-08 | 2026-10-25 |
| ios | 0 |  |  |

99 further new IDs are dated at or before the base's newest review on their platform (published by the store after the base scrape). They were left out, so counts for days the base already reported do not change.

Later-run feed coverage per stream (rows fetched, in-window rows for the later run's own 90-day pull, stop reason):

| Stream | Fetched | In window | Stop |
| --- | --- | --- | --- |
| en | 6000 | 5701 | window_edge |
| es | 2200 | 1885 | window_edge |
| pt | 1400 | 1161 | window_edge |
| fr | 2000 | 1717 | window_edge |
| ar | 1000 | 773 | window_edge |
| id | 800 | 566 | window_edge |
| ru | 600 | 268 | window_edge |
| de | 400 | 194 | window_edge |
| ko | 400 | 148 | window_edge |
| it | 400 | 121 | window_edge |
| th | 400 | 106 | window_edge |
| vi | 400 | 106 | window_edge |
| tr | 400 | 122 | window_edge |
| ja | 400 | 66 | window_edge |
| hi | 400 | 15 | window_edge |
| nl | 312 | 25 | window_edge |
| pl | 400 | 69 | window_edge |
| sv | 127 | 11 | no_continuation |
| da | 51 | 1 | no_continuation |
| nb | 54 | 4 | no_continuation |
| fi | 55 | 5 | no_continuation |
| cs | 385 | 21 | window_edge |
| el | 186 | 16 | no_continuation |
| hu | 312 | 15 | window_edge |
| ro | 273 | 32 | window_edge |
| uk | 400 | 8 | window_edge |
| bg | 95 | 8 | no_continuation |
| hr | 150 | 12 | no_continuation |
| sk | 101 | 6 | no_continuation |
| sr | 95 | 12 | no_continuation |
| iw | 236 | 18 | window_edge |
| fa | 600 | 270 | window_edge |
| ur | 15 | 0 | window_edge |
| bn | 59 | 11 | no_continuation |
| ta | 33 | 1 | no_continuation |
| te | 30 | 1 | no_continuation |
| mr | 43 | 2 | no_continuation |
| ms | 77 | 8 | no_continuation |
| fil | 3 | 0 | window_edge |
| zh-TW | 400 | 80 | window_edge |
| zh-CN | 400 | 69 | window_edge |
| ca | 60 | 3 | no_continuation |

`daily_true_counts.csv` is recomputed from the merged corpus. Days up to the base run reflect the base scrape; later days reflect the later scrape for the appended platforms only.

---

# Base run report (unchanged, as generated at the base run)


Run time UTC: 2026-10-09T06:03:20Z

Window: 2026-07-11T06:03:20Z through 2026-10-09T06:03:20Z, inclusive.

Total rows before cap: 14791

Total rows after cap: 14791

Cap: 20000; sampling seed: 42.

Counts before cap are unique, nonempty reviews retrieved from the configured locales. They are not the total universe of store reviews: feeds can stop before the window is covered. Country is populated only for iOS and records the first storefront that returned a review, not reviewer residence. Android country is empty; store_lang records the first Play language stream that returned each review.

## By platform

| Platform | Before cap | After cap |
| --- | --- | --- |
| android | 13704 | 13704 |
| ios | 1087 | 1087 |

## iOS by storefront

| Storefront | Before cap | After cap |
| --- | --- | --- |
| ae | 9 | 9 |
| au | 30 | 30 |
| br | 34 | 34 |
| ca | 54 | 54 |
| de | 92 | 92 |
| es | 42 | 42 |
| fr | 81 | 81 |
| gb | 45 | 45 |
| id | 9 | 9 |
| in | 82 | 82 |
| jp | 54 | 54 |
| kr | 27 | 27 |
| mx | 24 | 24 |
| sg | 4 | 4 |
| us | 500 | 500 |

## Android by store_lang

| Store language | Before cap | After cap |
| --- | --- | --- |
| ar | 683 | 683 |
| bg | 8 | 8 |
| bn | 10 | 10 |
| ca | 2 | 2 |
| cs | 21 | 21 |
| de | 181 | 181 |
| el | 17 | 17 |
| en | 5852 | 5852 |
| es | 1913 | 1913 |
| fa | 261 | 261 |
| fi | 3 | 3 |
| fr | 1678 | 1678 |
| hi | 13 | 13 |
| hr | 11 | 11 |
| hu | 14 | 14 |
| id | 560 | 560 |
| it | 115 | 115 |
| iw | 16 | 16 |
| ja | 74 | 74 |
| ko | 165 | 165 |
| mr | 2 | 2 |
| ms | 12 | 12 |
| nb | 2 | 2 |
| nl | 25 | 25 |
| pl | 68 | 68 |
| pt | 1217 | 1217 |
| ro | 36 | 36 |
| ru | 251 | 251 |
| sk | 8 | 8 |
| sr | 12 | 12 |
| sv | 9 | 9 |
| ta | 1 | 1 |
| te | 1 | 1 |
| th | 109 | 109 |
| tr | 101 | 101 |
| uk | 11 | 11 |
| vi | 103 | 103 |
| zh-CN | 60 | 60 |
| zh-TW | 79 | 79 |

## By UTC week (Monday start)

| Week starting | Before cap | After cap |
| --- | --- | --- |
| 2026-07-06 | 312 | 312 |
| 2026-07-13 | 1107 | 1107 |
| 2026-07-20 | 1117 | 1117 |
| 2026-07-27 | 1111 | 1111 |
| 2026-08-03 | 1065 | 1065 |
| 2026-08-10 | 1124 | 1124 |
| 2026-08-17 | 1151 | 1151 |
| 2026-08-24 | 1129 | 1129 |
| 2026-08-31 | 1256 | 1256 |
| 2026-09-07 | 1303 | 1303 |
| 2026-09-14 | 1262 | 1262 |
| 2026-09-21 | 1325 | 1325 |
| 2026-09-28 | 1037 | 1037 |
| 2026-10-05 | 492 | 492 |

## By star rating per platform

| Platform | Stars | Before cap | After cap |
| --- | --- | --- | --- |
| android | 1 | 1701 | 1701 |
| android | 2 | 316 | 316 |
| android | 3 | 582 | 582 |
| android | 4 | 1403 | 1403 |
| android | 5 | 9702 | 9702 |
| ios | 1 | 298 | 298 |
| ios | 2 | 54 | 54 |
| ios | 3 | 57 | 57 |
| ios | 4 | 50 | 50 |
| ios | 5 | 628 | 628 |

## Review text lengths and shares

Lengths count Unicode characters in the unmodified body. Words use whitespace splitting; this is not language-aware tokenization. P90 uses linear interpolation.

| Dataset | Platform | Rows | Median chars | P90 chars | Under 4 words | Non-ASCII |
| --- | --- | --- | --- | --- | --- | --- |
| Before cap | all | 14791 | 18.0 | 120.0 | 52.84% | 37.56% |
| Before cap | android | 13704 | 16.0 | 98.0 | 55.62% | 36.59% |
| Before cap | ios | 1087 | 85.0 | 374.0 | 17.85% | 49.86% |
| After cap | all | 14791 | 18.0 | 120.0 | 52.84% | 37.56% |
| After cap | android | 13704 | 16.0 | 98.0 | 55.62% | 36.59% |
| After cap | ios | 1087 | 85.0 | 374.0 | 17.85% | 49.86% |

## Date ranges

| Dataset | Platform | Earliest date | Latest date |
| --- | --- | --- | --- |
| Before cap | android | 2026-07-11 | 2026-10-08 |
| Before cap | ios | 2026-07-11 | 2026-10-07 |
| After cap | android | 2026-07-11 | 2026-10-08 |
| After cap | ios | 2026-07-11 | 2026-10-07 |

Hours between run time and newest review (before cap): android: 24.03 hours; ios: 37.55 hours.

## Google Play language contributions (before cap)

| Language | Pages served | Rows fetched | In-window rows | Unique added | Overlapping IDs by first language | Same IDs as | Stop reason |
| --- | --- | --- | --- | --- | --- | --- | --- |
| en | 31 | 6200 | 5852 | 5852 | — | — | window_edge |
| es | 11 | 2200 | 1913 | 1913 | — | — | window_edge |
| pt | 8 | 1600 | 1217 | 1217 | — | — | window_edge |
| fr | 10 | 2000 | 1678 | 1678 | — | — | window_edge |
| ar | 5 | 1000 | 683 | 683 | — | — | window_edge |
| id | 4 | 800 | 560 | 560 | — | — | window_edge |
| ru | 3 | 600 | 251 | 251 | — | — | window_edge |
| de | 2 | 400 | 181 | 181 | — | — | window_edge |
| ko | 2 | 400 | 165 | 165 | — | — | window_edge |
| it | 2 | 400 | 115 | 115 | — | — | window_edge |
| th | 2 | 400 | 109 | 109 | — | — | window_edge |
| vi | 2 | 400 | 103 | 103 | — | — | window_edge |
| tr | 2 | 400 | 101 | 101 | — | — | window_edge |
| ja | 2 | 400 | 74 | 74 | — | — | window_edge |
| hi | 2 | 400 | 13 | 13 | — | — | window_edge |
| nl | 2 | 309 | 25 | 25 | — | — | window_edge |
| pl | 2 | 400 | 68 | 68 | — | — | window_edge |
| sv | 1 | 125 | 9 | 9 | — | — | no_continuation |
| da | 1 | 50 | 0 | 0 | — | — | window_edge |
| nb | 1 | 52 | 2 | 2 | — | — | no_continuation |
| fi | 1 | 53 | 3 | 3 | — | — | no_continuation |
| cs | 2 | 379 | 21 | 21 | — | — | window_edge |
| el | 1 | 183 | 17 | 17 | — | — | no_continuation |
| hu | 2 | 308 | 14 | 14 | — | — | window_edge |
| ro | 2 | 267 | 36 | 36 | — | — | window_edge |
| uk | 2 | 400 | 11 | 11 | — | — | window_edge |
| bg | 1 | 94 | 8 | 8 | — | — | no_continuation |
| hr | 1 | 147 | 11 | 11 | — | — | no_continuation |
| sk | 1 | 100 | 8 | 8 | — | — | no_continuation |
| sr | 1 | 93 | 12 | 12 | — | — | no_continuation |
| iw | 2 | 233 | 16 | 16 | — | — | window_edge |
| fa | 3 | 600 | 261 | 261 | — | — | window_edge |
| ur | 1 | 15 | 0 | 0 | — | — | window_edge |
| bn | 1 | 54 | 10 | 10 | — | — | no_continuation |
| ta | 1 | 33 | 1 | 1 | — | — | no_continuation |
| te | 1 | 30 | 1 | 1 | — | — | no_continuation |
| mr | 1 | 43 | 2 | 2 | — | — | no_continuation |
| ms | 1 | 77 | 12 | 12 | — | — | no_continuation |
| fil | 1 | 3 | 0 | 0 | — | — | window_edge |
| zh-TW | 2 | 400 | 79 | 79 | — | — | window_edge |
| zh-CN | 2 | 400 | 60 | 60 | — | — | window_edge |
| ca | 1 | 59 | 2 | 2 | — | — | no_continuation |

## App Store pages served per storefront (before cap)

| Storefront | Pages served | Rows fetched | In-window rows | Unique added | Stop reason | Rejected page |
| --- | --- | --- | --- | --- | --- | --- |
| us | 10 | 500 | 500 | 500 | page_limit_http_400 | 11 |
| gb | 2 | 100 | 45 | 45 | window_edge | — |
| in | 3 | 150 | 82 | 82 | window_edge | — |
| ca | 3 | 150 | 54 | 54 | window_edge | — |
| au | 2 | 100 | 30 | 30 | window_edge | — |
| de | 3 | 150 | 92 | 92 | window_edge | — |
| fr | 3 | 150 | 81 | 81 | window_edge | — |
| es | 2 | 100 | 42 | 42 | window_edge | — |
| br | 2 | 100 | 34 | 34 | window_edge | — |
| mx | 2 | 100 | 24 | 24 | window_edge | — |
| jp | 3 | 150 | 54 | 54 | window_edge | — |
| kr | 2 | 100 | 27 | 27 | window_edge | — |
| id | 2 | 100 | 9 | 9 | window_edge | — |
| sg | 2 | 100 | 4 | 4 | window_edge | — |
| ae | 2 | 84 | 9 | 9 | window_edge | — |

## Locales with no in-window reviews

play: da, play: ur, play: fil
