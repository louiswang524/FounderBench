# FounderBench Metric Sensitivity

Metric sensitivity analysis for deterministic baselines. The official ranking uses bounded task score; alternatives test whether unbounded money-like simulator signals change the qualitative conclusion.

## Summary

| Metric | Value |
| --- | --- |
| metrics | 9 |
| policies | 4 |
| same_leader_metrics | 5 |
| low_correlation_metrics | 6 |
| max_rank_shift | 3 |

## Ranking Sensitivity

| Metric | Leader | Spearman vs Primary | Ranking |
| --- | --- | --- | --- |
| average_task_score | task_heuristic | 1.0 | task_heuristic > heuristic > conservative > random |
| solve_rate | task_heuristic | 1.0 | task_heuristic > heuristic > conservative > random |
| median_task_score | task_heuristic | 1.0 | task_heuristic > heuristic > conservative > random |
| task_normalized_business_score | task_heuristic | 0.4 | task_heuristic > conservative > random > heuristic |
| average_final_cash | random | -0.4 | random > task_heuristic > conservative > heuristic |
| average_cumulative_revenue | task_heuristic | 0.4 | task_heuristic > random > heuristic > conservative |
| survival_rate | conservative | 0.2 | conservative > heuristic > task_heuristic > random |
| low_risk_score | conservative | 0.2 | conservative > heuristic > task_heuristic > random |
| revenue_efficiency | conservative | 0.2 | conservative > heuristic > task_heuristic > random |

## Metric Values

| Metric | task_heuristic | heuristic | conservative | random |
| --- | --- | --- | --- | --- |
| average_task_score | 80.9 | 61.01 | 54.04 | 33.3 |
| solve_rate | 0.74 | 0.38 | 0.26 | 0.08 |
| median_task_score | 91.0 | 66.77 | 48.09 | 26.38 |
| task_normalized_business_score | 63.09 | 37.02 | 48.48 | 45.13 |
| average_final_cash | 20805.39 | 17571.8 | 20047.67 | 22244.57 |
| average_cumulative_revenue | 15261.62 | 13246.5 | 12946.85 | 13424.06 |
| survival_rate | 1.0 | 1.0 | 1.0 | 0.98 |
| low_risk_score | 96.04 | 100.0 | 100.0 | 69.15 |
| revenue_efficiency | 2.4114 | 2.4555 | 4.9431 | 2.3979 |

## Rank Changes

| Metric | Same Leader as Primary | Max Rank Shift |
| --- | --- | --- |
| average_task_score | True | 0 |
| solve_rate | True | 0 |
| median_task_score | True | 0 |
| task_normalized_business_score | True | 2 |
| average_final_cash | False | 3 |
| average_cumulative_revenue | True | 2 |
| survival_rate | False | 2 |
| low_risk_score | False | 2 |
| revenue_efficiency | False | 2 |

## Interpretation

- Average bounded task score remains the official metric because it normalizes heterogeneous startup situations to a common 0-100 scale.
- Task-normalized business score is reported as a sensitivity check because raw company score is not comparable across tasks with different starting states and horizons.
- Metrics such as cash, revenue, and low risk are diagnostic rather than primary because optimizing one alone can reward degenerate behavior.

## Validation

Status: PASS

The report compares the official bounded task score with normalized business, solve-rate, survival, revenue, cash, and risk diagnostics.
