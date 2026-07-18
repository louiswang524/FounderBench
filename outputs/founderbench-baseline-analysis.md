# FounderBench Baseline Analysis

## Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Family Breakdown

Each cell reports `solved/5 (average score)`.

| Family | task_heuristic | heuristic | conservative | random |
| --- | --- | --- | --- | --- |
| Market selection | 2/5 (59.8) | 2/5 (61.1) | 2/5 (63.2) | 0/5 (31.6) |
| First revenue | 2/5 (69.2) | 2/5 (65.7) | 1/5 (45.3) | 0/5 (20.4) |
| Retention improvement | 5/5 (95.8) | 2/5 (63.5) | 0/5 (47.5) | 0/5 (10.4) |
| Churn shock recovery | 5/5 (91.2) | 1/5 (48.1) | 0/5 (38.3) | 0/5 (34.3) |
| Demo Day traction | 4/5 (88.8) | 3/5 (67.0) | 2/5 (60.3) | 0/5 (20.2) |
| Pricing | 5/5 (85.6) | 4/5 (85.2) | 3/5 (77.3) | 0/5 (39.7) |
| Runway preservation | 5/5 (95.6) | 5/5 (82.5) | 5/5 (79.1) | 2/5 (68.3) |
| Pivot decision | 2/5 (65.5) | 0/5 (26.8) | 0/5 (23.9) | 0/5 (11.7) |
| Fundraising | 5/5 (99.6) | 0/5 (68.0) | 0/5 (68.0) | 2/5 (72.6) |
| Channel expansion | 2/5 (58.0) | 0/5 (42.1) | 0/5 (37.6) | 0/5 (23.7) |

## Hardest Tasks

Tasks are sorted by mean score across all reported baselines.

| Task | Family | Mean Score | Solved By |
| --- | --- | --- | --- |
| FND-036 | Pivot decision | 25.38 | 0/4 |
| FND-037 | Pivot decision | 27.30 | 0/4 |
| FND-047 | Channel expansion | 32.17 | 0/4 |
| FND-038 | Pivot decision | 32.50 | 1/4 |
| FND-050 | Channel expansion | 34.16 | 0/4 |
| FND-005 | Market selection | 34.27 | 0/4 |
| FND-046 | Channel expansion | 34.46 | 0/4 |
| FND-040 | Pivot decision | 35.33 | 1/4 |
| FND-010 | First revenue | 36.56 | 0/4 |
| FND-004 | Market selection | 36.78 | 0/4 |
| FND-039 | Pivot decision | 39.35 | 0/4 |
| FND-048 | Channel expansion | 41.77 | 1/4 |

## Failure Diagnostics

| Policy | Failed Tasks | Bankrupt Failures | Over-Budget Decisions | Provider Errors | Worst Task | Worst Family |
| --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 13 | 0 | 5 | 0 | FND-002 (37.77) | Market selection |
| heuristic | 31 | 0 | 0 | 0 | FND-040 (19.51) | Pivot decision |
| conservative | 37 | 0 | 0 | 0 | FND-040 (19.10) | Pivot decision |
| random | 46 | 1 | 15 | 0 | FND-012 (0.00) | Retention improvement |

## Provider Error Taxonomy

Rule baselines should have no provider errors. Hosted LLM runs use this table to distinguish malformed JSON, schema errors, timeouts, and provider exceptions.

| Policy | Category | Count |
| --- | --- | --- |
| all policies | none | 0 |

## Bootstrap Uncertainty

Intervals are nonparametric 95% bootstrap intervals over the fixed 50 task episodes. They estimate sensitivity to the task mix, not provider sampling variance.

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Pairwise Score Gaps

Gaps compare the strongest baseline against each other baseline on matched tasks.

| Comparison | Mean Gap | Gap 95% CI | Tasks |
| --- | --- | --- | --- |
| task_heuristic - heuristic | 19.90 | [13.80, 26.19] | 50 |
| task_heuristic - conservative | 26.87 | [21.67, 32.45] | 50 |
| task_heuristic - random | 47.61 | [40.24, 54.64] | 50 |

## Interpretation Notes

- The task-aware heuristic remains the strongest non-LLM baseline, but it still fails 13/50 tasks.
- The random baseline solves only 4/50 tasks after recalibration, suggesting the environment is not solved by blind action sampling.
- Pivot and channel-expansion tasks remain the hardest families for rule-based policies.
- Runway preservation is still relatively easy for conservative policies and should receive more difficult variants in the next release.
- Provider-error and invalid-action fields are zero for rule baselines; these fields become important for hosted LLM runs.
