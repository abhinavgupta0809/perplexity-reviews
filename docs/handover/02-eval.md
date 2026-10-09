# Phase 02 gold-set evaluation

Gold rows: 120

Rows with annotation_error: 0

## Agreement

| Metric | Matches | Rows | Value | Target | Status |
| --- | --- | --- | --- | --- | --- |
| Primary label accuracy | 117 | 120 | 97.50% | 85.00% | PASS |
| Label set overlap | 120 | 120 | 100.00% | — | — |
| Primary category agreement | 87 | 92 | 94.57% | 80.00% | PASS |
| Low-signal agreement | 28 | 28 | 100.00% | — | — |
| Sentiment within one point | 120 | 120 | 100.00% | — | — |

Sentiment mean absolute error: 0.2000 over 120 scored rows. Missing/failed sentiment rows: 0. Within-one-point accuracy uses every gold row; missing/failed results count as misses. Failed annotations also count as misses on label/category/low-signal metrics.

## Primary-label confusion matrix

| Gold primary label | Specific Praise | Specific Complaint | Feature Request | Generic Good | Generic Bad | Nonsense | (missing) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Specific Praise | 27 | 1 | 1 | 0 | 0 | 0 | 0 |
| Specific Complaint | 0 | 54 | 0 | 0 | 0 | 0 | 0 |
| Feature Request | 0 | 1 | 8 | 0 | 0 | 0 | 0 |
| Generic Good | 0 | 0 | 0 | 16 | 0 | 0 | 0 |
| Generic Bad | 0 | 0 | 0 | 0 | 9 | 0 | 0 |
| Nonsense | 0 | 0 | 0 | 0 | 0 | 3 | 0 |

## Per-category agreement

Gold count includes each row whose gold category set contains that category. A match requires the model's primary category to equal that category; a two-category gold row can appear in two denominators.

| Category | Gold count | Primary-category matches | Agreement |
| --- | --- | --- | --- |
| Answer Accuracy | 17 | 14 | 82.35% |
| Search &amp; Sources | 16 | 8 | 50.00% |
| Answer Style &amp; Filters | 7 | 4 | 57.14% |
| Model Choice | 3 | 3 | 100.00% |
| Credits &amp; Paid Limits | 6 | 6 | 100.00% |
| Free Limits &amp; Paywall | 19 | 16 | 84.21% |
| Pricing &amp; Value | 6 | 4 | 66.67% |
| Billing &amp; Subscription | 4 | 2 | 50.00% |
| Customer Support | 0 | 0 | n/a |
| Computer &amp; Agents | 2 | 1 | 50.00% |
| Voice &amp; Dictation | 5 | 4 | 80.00% |
| Images &amp; Files | 13 | 5 | 38.46% |
| Threads &amp; History | 3 | 3 | 100.00% |
| Bugs &amp; Stability | 4 | 3 | 75.00% |
| Speed | 5 | 3 | 60.00% |
| Login &amp; Account | 1 | 1 | 100.00% |
| UI / UX | 5 | 4 | 80.00% |
| Privacy &amp; Permissions | 2 | 0 | 0.00% |
| Use Cases | 6 | 6 | 100.00% |
| Other | 0 | 0 | n/a |

## All label/category/low-signal disagreements (7)

Every disagreement on primary label, primary category, or low-signal agreement is included once. Text is sliced to 300 Unicode characters before Markdown escaping; no row limit is applied.

| Review ID | Stars | Review text (first 300 characters) | Gold labels | Gold categories | Model labels | Model categories | Model topic |
| --- | --- | --- | --- | --- | --- | --- | --- |
| ios_14554233799 | 5 | Perplexity is the best especially for research | Specific Praise | Search &amp; Sources | Specific Praise | Use Cases, Search &amp; Sources | good for research |
| play_a9a3cc58-595f-4dae-84be-db1a4ab1fbe1 | 1 | pésima la app no la recomiendo para nada inmediatamente te quieren hacer un cobro qué asquerosidad la verdad por eso en ese mismísimo momento la desinstalé no sé la recomiendo a nadie | Specific Complaint | Free Limits &amp; Paywall | Specific Complaint | Billing &amp; Subscription | pushes charge right away |
| play_d9245ce0-9b37-4a9a-bcb3-eeb2adaa63cb | 1 | wäre schön es auch ohne Kreditkarte nutzen zu können | Feature Request | Billing &amp; Subscription | Feature Request | Free Limits &amp; Paywall | use without credit card |
| play_90601662-8871-47e6-9594-0ea5caf7caa3 | 3 | 일단 정보 찾는데 출처나 자료의 신뢰도가 높다는 장점이 있어요! 그래서 유용하게 쓰고 있는데 어느 순간부터 같은 계정으로 로그인을 해도 마치 다른 계정을 사용하는 것처럼 예전에 했던 기록이 날라가 있어서 당황했어요.. 잠시 다시 예전 기록이 전부 돌아오긴 했지만 다시 예전 기록이 날라간 상황입니다..🥲 이거 해결해주시면 좋을 것 같아요! | Specific Praise \| Specific Complaint | Search &amp; Sources \| Threads &amp; History | Specific Complaint, Specific Praise | Threads &amp; History, Search &amp; Sources | chat history disappears after login |
| play_eb52f19b-faa6-4753-9325-06e474db8c81 | 3 | O app é ótimo, só acharia uma boa e daria cinco estrelas se N tivesse tanto filtro para certas perguntas ou pesquisas, poderiam tirar essa censura um pouco :) | Feature Request \| Generic Good | Answer Style &amp; Filters | Specific Complaint, Generic Good | Answer Style &amp; Filters | too many content filters |
| play_2082ed97-d0cc-4c3f-9872-ae5e238c1ba6 | 5 | Les sources sont excellentes. Accordez un peu plus de crédit pour Prp basique | Specific Praise \| Feature Request | Search &amp; Sources \| Free Limits &amp; Paywall | Feature Request, Specific Praise | Credits &amp; Paid Limits, Search &amp; Sources | more credits for basic pro |
| play_ed0c8841-1c7c-469a-a6a3-f669a7d7ef9a | 5 | I'm grateful to have found perplexity. such a wonderful research tool. wonderful for brainstorming. love the new computer mode. | Specific Praise | Search &amp; Sources \| Computer &amp; Agents | Specific Praise | Use Cases, Computer &amp; Agents | good for research and brainstorming |
