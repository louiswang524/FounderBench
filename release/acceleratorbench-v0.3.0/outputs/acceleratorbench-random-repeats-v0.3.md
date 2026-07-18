# FounderBench v0.3 Repeated-Run Report

Policy: `random`
Seeds: `[0, 1, 2, 3, 4]`

## Validation

Status: PASS

## Per-Run Results

| Seed | Tasks | Solved | Solve Rate | Avg Score | Invalid Actions | Over-Budget |
| --- | --- | --- | --- | --- | --- | --- |
| 0 | 50 | 4 | 0.08 | 33.30 | 0 | 15 |
| 1 | 50 | 8 | 0.16 | 37.16 | 0 | 11 |
| 2 | 50 | 4 | 0.08 | 32.28 | 0 | 10 |
| 3 | 50 | 5 | 0.10 | 34.31 | 0 | 12 |
| 4 | 50 | 6 | 0.12 | 36.53 | 0 | 16 |

## Across-Run Intervals

Intervals summarize variation across repeated runs. For hosted LLMs, this should be reported in addition to task-mix bootstrap intervals.

| Metric | Mean | 95% CI | Runs |
| --- | --- | --- | --- |
| average_task_score | 34.72 | [33.09, 36.34] | 5 |
| solve_rate | 0.11 | [0.08, 0.14] | 5 |
