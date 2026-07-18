# FounderBench Power and Resolution Analysis

Power and resolution analysis for the fixed public task suite before hosted/local LLM results are added.

## Method

| Item | Value |
| --- | --- |
| paired_gap_variance_source | All pairwise deterministic-baseline task-score gaps on the 50 public current tasks. |
| alpha | 0.05 |
| target_power | 0.8 |
| approximation | Normal paired-mean approximation: MDE = (1.96 + 0.84) * sd(paired gaps) / sqrt(n). |
| paired_gap_sd | 34.1838 |

## Summary

| Metric | Value |
| --- | --- |
| public_tasks | 50 |
| policies_used_for_variance | 4 |
| paired_gap_observations | 300 |
| minimum_detectable_score_gap_50_tasks | 13.54 |
| observed_comparisons_above_50_task_mde | 3 |
| claim | The public suite has coarse resolution for small model differences; repeated runs and private-holdout expansion should be reported for close hosted-model comparisons. |

## Minimum Detectable Score Gap

| Task Episodes | Minimum Detectable Score Gap | Interpretation |
| --- | --- | --- |
| 20 | 21.4 | Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance. |
| 30 | 17.48 | Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance. |
| 50 | 13.54 | Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance. |
| 75 | 11.05 | Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance. |
| 100 | 9.57 | Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance. |

## Observed Deterministic Gaps

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Cohen dz | Above 50-Task MDE |
| --- | --- | --- | --- | --- | --- |
| task_heuristic - heuristic | 50 | 19.9 | [13.8, 26.19] | 0.8848 | True |
| task_heuristic - conservative | 50 | 26.87 | [21.67, 32.45] | 1.3433 | True |
| task_heuristic - random | 50 | 47.61 | [40.24, 54.64] | 1.892 | True |

## Solve-Rate Resolution

| Item | Value |
| --- | --- |
| task_episodes | 50 |
| minimum_detectable_solve_rate_gap | 0.198 |
| assumption | Conservative normal approximation with Bernoulli variance p(1-p)=0.25; paired binary tests may need less or more evidence depending on discordance. |

## Claim Guardrails

- Do not interpret non-significant close hosted-model gaps as model equivalence without a pre-specified equivalence margin.
- Do not claim the 50-task public suite can reliably detect small score gaps near the MDE boundary.
- Use repeated-run bundles for stochastic policies and report run-level intervals separately from task-level paired intervals.
- Use the private-holdout protocol for final leaderboard credibility rather than increasing public-task tuning pressure.

## Validation

Status: PASS

The analysis quantifies public-suite resolution and keeps close-model comparison limits explicit.
