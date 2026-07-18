# FounderBench v0.3 Paired Statistics

Paired statistical comparison of deterministic baselines over matched task episodes.

## Method

| Item | Value |
| --- | --- |
| paired_unit | task episode |
| score_gap | top_policy_score_i - baseline_policy_score_i on the same task id |
| bootstrap_ci | nonparametric bootstrap over paired task gaps |
| permutation_test | two-sided random sign-flip test over paired task gaps |
| permutation_samples | 20000 |
| multiple_comparison_adjustment | Holm-Bonferroni over reported paired permutation p-values for the primary endpoint. |
| effect_size | Cohen dz = mean paired gap / population standard deviation of paired gaps |

## Summary

| Metric | Value |
| --- | --- |
| comparisons | 3 |
| significant_at_0_05 | 3 |
| significant_after_holm_0_05 | 3 |
| all_score_gap_cis_positive | True |
| max_p_value | 5e-05 |
| max_holm_adjusted_p | 0.00015 |

## Pairwise Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Raw permutation p | Holm adjusted p | Holm sig. | Cohen dz | Score W/L/T | Solve Gap | Solve W/L |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic - heuristic | 50 | 19.9 | [13.8, 26.19] | 5e-05 | 0.00015 | True | 0.8848 | 42/8/0 | 0.36 | 20/2 |
| task_heuristic - conservative | 50 | 26.87 | [21.67, 32.45] | 5e-05 | 0.00015 | True | 1.3433 | 43/7/0 | 0.48 | 24/0 |
| task_heuristic - random | 50 | 47.61 | [40.24, 54.64] | 5e-05 | 0.00015 | True | 1.892 | 49/1/0 | 0.66 | 33/0 |

## Interpretation

- The paired unit is the fixed task episode, so each comparison controls for task identity.
- Permutation p-values test whether the observed signed task gaps are larger than expected under random sign flips.
- Raw and Holm-Bonferroni adjusted p-values are both reported; adjusted p-values govern family-level leaderboard claims.
- Effect sizes are descriptive calibration evidence for deterministic baselines; hosted LLM comparisons should report the same rows once runs are available.

## Validation

Status: PASS

All comparisons cover the full 50-task public suite and have internally consistent paired statistics.
