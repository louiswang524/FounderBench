# FounderBench Paper Tables

These generated tables are intended for the paper results section. They are derived from raw current release run files; hosted/provider rows are included in the main tables only after submission validation passes.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_runs | 4 |
| valid_provider_runs | 0 |
| provider_candidates | 5 |
| provider_missing_or_invalid | 5 |
| valid_provider_policies | 0 |
| valid_repeated_provider_bundles | 0 |

## Main Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Confidence Intervals

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Pairwise Score Gaps

| Comparison | Mean Gap | 95% CI | Shared Tasks |
| --- | --- | --- | --- |
| task_heuristic - heuristic | 19.90 | [13.80, 26.19] | 50 |
| task_heuristic - conservative | 26.87 | [21.67, 32.45] | 50 |
| task_heuristic - random | 47.61 | [40.24, 54.64] | 50 |

## Family Breakdown

Each cell reports `solved/5 (average score)`. Valid policies included: `task_heuristic`, `heuristic`, `conservative`, `random`.

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

## Hardest Public Tasks

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

## Provider Evidence Status

| ID | Policy | Family | Status | Runs | Evidence | Avg Score | Solve Rate | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek_hosted_baseline | deepseek | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-deepseek.json or outputs/founderbench-deepseek-repeats.json |
| deepseek_self_consistency_k3 | deepseek_sc | hosted_llm_ablation | missing | 0 |  |  |  | Missing outputs/founderbench-deepseek-sc-k3.json or outputs/founderbench-deepseek-sc-k3-repeats.json |
| anthropic_hosted_baseline | anthropic | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-anthropic.json or outputs/founderbench-anthropic-repeats.json |
| gemini_hosted_baseline | gemini | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-gemini.json or outputs/founderbench-gemini-repeats.json |
| local_open_source_baseline | llm | open_source | missing | 0 |  |  |  | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

Provider runs marked `missing` or `invalid` are excluded from the main leaderboard and tables. This avoids mixing older or partial provider outputs into the current release paper evidence.
