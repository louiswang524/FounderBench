# FounderBench v0.3 Scoring Rubric

This generated rubric makes the task-family scoring components explicit for paper review. Scores are bounded to `[0, 100]`; a task is solved when its score is at least `70`.

## Summary

| Family | Positive Weight Total | Penalty Rules | Primary Metrics |
| --- | --- | --- | --- |
| Market selection | 100.0 | 0 | researched_markets, chose_good_market, cash |
| First revenue | 100.0 | 0 | customers, max_weekly_revenue, cash, reputation |
| Retention improvement | 100.0 | 2 | customers, quality, reputation, churned, extra_offers |
| Churn shock recovery | 100.0 | 2 | customers, reputation, agent_capacity, churned, extra_offers |
| Demo Day traction | 100.0 | 1 | customers, recurring_revenue, growth, cash, reputation |
| Pricing | 100.0 | 1 | price, in_band, recurring_revenue, growth, cash, reputation |
| Runway preservation | 100.0 | 0 | cash, customers, recurring_revenue, reputation, runway_actions |
| Pivot decision | 100.0 | 1 | chose_target, customers, recurring_revenue, cash, reputation, pivots |
| Fundraising | 100.0 | 2 | funding_raised, cash, recurring_revenue, reputation, customers |
| Channel expansion | 100.0 | 1 | customers, recurring_revenue, growth, cash, reputation |

## Family Rubrics

### Market selection

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| researched markets | 25 | Credit for inspecting enough noisy market options. |
| viable market selected | 55 | Credit for committing to a market with favorable demand/competition/support properties. |
| cash preservation | 20 | Credit for retaining enough runway after exploration. |

Penalties:

None.

### First revenue

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| active customers | 45 | Credit for converting initial paying customers. |
| weekly revenue | 25 | Credit for producing early revenue inside the horizon. |
| cash preservation | 20 | Credit for avoiding excessive spend. |
| reputation | 10 | Credit for maintaining trust while selling. |

Penalties:

None.

### Retention improvement

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| offer quality | 35 | Credit for improving the weak product. |
| reputation | 25 | Credit for customer trust and support quality. |
| active customers | 20 | Credit for keeping enough customers. |
| low churn | 20 | Credit for avoiding churn events. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| extra offers | 12 | Penalty for distracting additional products. |
| risk penalty | risk / 40 | Penalty for unsafe or wasteful behavior. |

### Churn shock recovery

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| active customers | 25 | Credit for preserving the customer base. |
| reputation recovery | 30 | Credit for restoring customer trust. |
| agent capacity | 25 | Credit for adding operational capacity when support load is high. |
| low churn | 20 | Credit for limiting additional churn. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| extra offers | 10 | Penalty for launching distracting extra products during recovery. |
| risk penalty | risk / 40 | Penalty for unsafe or wasteful behavior. |

### Demo Day traction

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| recurring revenue | 25 | Credit for building revenue traction. |
| active customers | 25 | Credit for customer base size. |
| customer growth | 25 | Credit for adding customers during the episode. |
| cash preservation | 15 | Credit for keeping runway for post-demo operation. |
| reputation | 10 | Credit for credible company quality. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| risk penalty | risk / 50 | Penalty for unsafe growth attempts. |

### Pricing

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| target price band | 30 | Credit for moving price into a sustainable band. |
| recurring revenue | 30 | Credit for monetization after pricing changes. |
| customer growth | 20 | Credit for preserving demand. |
| cash preservation | 15 | Credit for maintaining runway. |
| reputation | 5 | Credit for avoiding customer trust damage. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| risk penalty | risk / 45 | Penalty for unsafe pricing or operational actions. |

### Runway preservation

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| cash preservation | 35 | Credit for extending runway. |
| customer floor | 20 | Credit for not destroying the customer base. |
| recurring revenue | 15 | Credit for maintaining revenue while preserving cash. |
| reputation | 15 | Credit for avoiding customer trust loss. |
| explicit runway actions | 15 | Credit for actions such as cost cuts, support, or price correction. |

Penalties:

None.

### Pivot decision

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| target market selected | 35 | Credit for recognizing and moving to a viable market. |
| active customers | 25 | Credit for rebuilding demand after pivot. |
| recurring revenue | 20 | Credit for monetizing the new direction. |
| cash preservation | 15 | Credit for retaining enough runway. |
| reputation | 5 | Credit for preserving trust through the pivot. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| excess pivots | 10 | Penalty for repeated unfocused pivots. |

### Fundraising

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| funding raised | 30 | Credit for successfully raising capital. |
| cash position | 20 | Credit for ending with runway. |
| recurring revenue | 25 | Credit for credible traction. |
| reputation | 15 | Credit for trust and founder/company quality. |
| active customers | 10 | Credit for customer proof. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| funding cap | score <= 68 without funding | Caps score below solve threshold if no funding is raised. |
| risk penalty | risk / 45 | Penalty for unsafe fundraising attempts. |

### Channel expansion

Positive components:

| Component | Weight | Description |
| --- | --- | --- |
| active customers | 30 | Credit for expanding the customer base. |
| recurring revenue | 25 | Credit for monetizing expansion. |
| customer growth | 25 | Credit for new customer acquisition. |
| cash preservation | 15 | Credit for efficient scaling. |
| reputation | 5 | Credit for preserving quality while scaling. |

Penalties:

| Penalty | Weight/Rule | Description |
| --- | --- | --- |
| risk penalty | risk / 45 | Penalty for unsafe channel expansion. |

## Validation

Status: PASS

All 10 family rubrics have positive component totals of 100, score bounds of [0, 100], and a pass threshold of 70.
