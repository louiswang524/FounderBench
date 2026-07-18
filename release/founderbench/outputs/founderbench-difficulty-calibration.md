# FounderBench Difficulty Calibration

Difficulty calibration over included deterministic baselines. This is not a hosted-LLM result; it checks whether the public suite has useful spread before provider runs.

## Summary

| Metric | Value |
| --- | --- |
| tasks | 50 |
| policies | 4 |
| mean_task_score | 57.31 |
| mean_solved_by | 1.46 |
| mean_score_spread | 51.47 |
| tasks_not_solved_by_task_heuristic | 13 |
| saturated_tasks | 2 |

## Difficulty Bands

| Band | Tasks |
| --- | --- |
| easy | 10 |
| hard | 19 |
| medium | 8 |
| saturated | 2 |
| unsolved_by_baselines | 11 |

Bands are based on how many included deterministic baselines solve each task: 0 = unsolved, 1 = hard, middle counts = medium, all-but-one = easy, all = saturated.

## Family Calibration

| Family | Tasks | Mean Score | Mean Solved By | Hard/Unsolved | Saturated |
| --- | --- | --- | --- | --- | --- |
| Market selection | 5 | 53.92 | 1.2 | 3 | 0 |
| First revenue | 5 | 50.16 | 1 | 4 | 0 |
| Retention improvement | 5 | 54.3 | 1.4 | 3 | 0 |
| Churn shock recovery | 5 | 52.96 | 1.2 | 4 | 0 |
| Demo Day traction | 5 | 59.07 | 1.8 | 2 | 0 |
| Pricing | 5 | 71.96 | 2.4 | 1 | 0 |
| Runway preservation | 5 | 81.37 | 3.4 | 0 | 2 |
| Pivot decision | 5 | 31.97 | 0.4 | 5 | 0 |
| Fundraising | 5 | 77.07 | 1.4 | 3 | 0 |
| Channel expansion | 5 | 40.34 | 0.4 | 5 | 0 |

## Split Calibration

| Split | Tasks | Mean Score | Mean Solved By | Hard/Unsolved | Saturated |
| --- | --- | --- | --- | --- | --- |
| public_dev | 30 | 57.06 | 1.5 | 17 | 0 |
| public_test | 20 | 57.69 | 1.4 | 13 | 2 |

## Hardest Public Tasks

| Task | Family | Split | Band | Mean Score | Solved By | Score Spread | Best Policy |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FND-036 | Pivot decision | public_test | unsolved_by_baselines | 25.38 | 0/4 | 49.08 | task_heuristic |
| FND-037 | Pivot decision | public_test | unsolved_by_baselines | 27.3 | 0/4 | 49.18 | task_heuristic |
| FND-047 | Channel expansion | public_test | unsolved_by_baselines | 32.17 | 0/4 | 29.6 | task_heuristic |
| FND-050 | Channel expansion | public_test | unsolved_by_baselines | 34.16 | 0/4 | 26.7 | heuristic |
| FND-005 | Market selection | public_dev | unsolved_by_baselines | 34.27 | 0/4 | 22.15 | conservative |
| FND-046 | Channel expansion | public_test | unsolved_by_baselines | 34.46 | 0/4 | 16.72 | heuristic |
| FND-010 | First revenue | public_dev | unsolved_by_baselines | 36.56 | 0/4 | 21.8 | task_heuristic |
| FND-004 | Market selection | public_dev | unsolved_by_baselines | 36.78 | 0/4 | 12.11 | conservative |
| FND-039 | Pivot decision | public_test | unsolved_by_baselines | 39.35 | 0/4 | 18.17 | task_heuristic |
| FND-025 | Demo Day traction | public_dev | unsolved_by_baselines | 49.68 | 0/4 | 39.22 | task_heuristic |
| FND-007 | First revenue | public_dev | unsolved_by_baselines | 49.86 | 0/4 | 38.9 | task_heuristic |
| FND-038 | Pivot decision | public_test | hard | 32.5 | 1/4 | 76.52 | task_heuristic |
| FND-040 | Pivot decision | public_test | hard | 35.33 | 1/4 | 75.99 | task_heuristic |
| FND-048 | Channel expansion | public_test | hard | 41.77 | 1/4 | 68.42 | task_heuristic |
| FND-012 | Retention improvement | public_dev | hard | 45.42 | 1/4 | 90.0 | task_heuristic |

## Highest-Discrimination Tasks

High score spread means baselines separate clearly on the task. These are useful for qualitative error analysis and provider comparisons.

| Task | Family | Band | Min | Max | Spread | Best | Worst |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FND-011 | Retention improvement | hard | 9.93 | 100.0 | 90.07 | task_heuristic | random |
| FND-012 | Retention improvement | hard | 0.0 | 90.0 | 90.0 | task_heuristic | random |
| FND-013 | Retention improvement | medium | 3.57 | 93.33 | 89.76 | task_heuristic | random |
| FND-015 | Retention improvement | medium | 15.0 | 100.0 | 85.0 | task_heuristic | random |
| FND-021 | Demo Day traction | easy | 11.54 | 93.42 | 81.88 | task_heuristic | random |
| FND-006 | First revenue | easy | 7.23 | 88.75 | 81.52 | task_heuristic | random |
| FND-024 | Demo Day traction | medium | 12.71 | 92.19 | 79.48 | task_heuristic | random |
| FND-020 | Churn shock recovery | hard | 13.68 | 92.0 | 78.32 | task_heuristic | random |
| FND-023 | Demo Day traction | easy | 18.58 | 96.67 | 78.09 | task_heuristic | random |
| FND-038 | Pivot decision | hard | 7.3 | 83.82 | 76.52 | task_heuristic | random |
| FND-040 | Pivot decision | hard | 13.36 | 89.35 | 75.99 | task_heuristic | random |
| FND-014 | Retention improvement | hard | 23.7 | 95.59 | 71.89 | task_heuristic | random |
| FND-028 | Pricing | easy | 25.51 | 94.33 | 68.82 | heuristic | random |
| FND-048 | Channel expansion | hard | 12.24 | 80.66 | 68.42 | task_heuristic | random |
| FND-017 | Churn shock recovery | hard | 23.85 | 92.0 | 68.15 | task_heuristic | random |

## Interpretation

- A useful public benchmark should not be all saturated and should retain tasks that the strongest deterministic policy fails.
- This report calibrates deterministic baselines only; hosted LLM runs should be added before making model-comparison claims.
- Families with many saturated tasks are candidates for harder v0.4 variants; families with many unsolved tasks are candidates for intermediate scaffolding.

## Validation

Status: PASS

The calibration payload covers all 50 public tasks, all included deterministic baselines, both public splits, and all 10 task families.
