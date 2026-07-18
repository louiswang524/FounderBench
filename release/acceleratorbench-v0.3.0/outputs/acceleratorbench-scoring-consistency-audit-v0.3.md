# FounderBench v0.3 Scoring Consistency Audit

Scoring consistency audit over all included deterministic raw task results.

## Score Contract

| Item | Value |
| --- | --- |
| score_min | 0 |
| score_max | 100 |
| pass_threshold | 70 |
| pass_rule | passed is true iff score >= pass_threshold |
| metric_payload_rule | Each task score must include non-empty numeric, bool, or string categorical metrics. |

## Summary

| Metric | Value |
| --- | --- |
| runs | 4 |
| task_results_checked | 200 |
| expected_task_results | 200 |
| score_rows_with_problems | 0 |
| families_checked | 10 |
| splits_checked | 2 |
| all_family_counts_valid | True |
| all_split_counts_valid | True |
| mean_score | 57.31 |
| passes | 73 |

## Family Coverage

| Family | Positive Weight Total | Valid Counts | Policy Task Counts | Primary Metrics |
| --- | --- | --- | --- | --- |
| Market selection | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | researched_markets, chose_good_market, cash |
| First revenue | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | customers, max_weekly_revenue, cash, reputation |
| Retention improvement | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | customers, quality, reputation, churned, extra_offers |
| Churn shock recovery | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | customers, reputation, agent_capacity, churned, extra_offers |
| Demo Day traction | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | customers, recurring_revenue, growth, cash, reputation |
| Pricing | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | price, in_band, recurring_revenue, growth, cash, reputation |
| Runway preservation | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | cash, customers, recurring_revenue, reputation, runway_actions |
| Pivot decision | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | chose_target, customers, recurring_revenue, cash, reputation, pivots |
| Fundraising | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | funding_raised, cash, recurring_revenue, reputation, customers |
| Channel expansion | 100.0 | True | {'conservative': 5, 'heuristic': 5, 'random': 5, 'task_heuristic': 5} | customers, recurring_revenue, growth, cash, reputation |

## Split Coverage

| Split | Expected Tasks Per Policy | Valid Counts | Policy Task Counts |
| --- | --- | --- | --- |
| public_dev | 30 | True | {'conservative': 30, 'heuristic': 30, 'random': 30, 'task_heuristic': 30} |
| public_test | 20 | True | {'conservative': 20, 'heuristic': 20, 'random': 20, 'task_heuristic': 20} |

## Metric Key Coverage

| Metric Key | Occurrences |
| --- | --- |
| agent_capacity | 20 |
| cash | 160 |
| chose_good_market | 20 |
| chose_target_market | 20 |
| churned | 40 |
| customers | 160 |
| extra_offers | 60 |
| funding_raised | 20 |
| growth | 60 |
| in_target_band | 20 |
| market_id | 20 |
| max_weekly_revenue | 20 |
| price | 20 |
| quality | 20 |
| recurring_revenue | 120 |
| reputation | 140 |
| researched_markets | 20 |
| risk_penalty | 20 |
| runway_actions | 20 |

## Failed Rows

No failed score rows.

## Claim Guardrail

This audit checks the consistency of generated score objects and rubric coverage; it does not validate that rubric weights are the correct model of real startup success.

## Validation

Status: PASS

All included deterministic score objects satisfy bounds, threshold, metric-payload, family, and split consistency checks.
