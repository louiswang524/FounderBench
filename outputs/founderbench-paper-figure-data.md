# FounderBench Paper Figure Data

Paper figure data generated from validated current release result artifacts.

## Summary

| Metric | Value |
| --- | --- |
| figures | 5 |
| leaderboard_policies | 4 |
| family_heatmap_cells | 40 |
| action_ablation_rows | 6 |
| difficulty_bands | 5 |
| metric_rankings | 9 |

## Figure Data Sets

| Figure ID | Rows | Caption | Recommended Encoding |
| --- | --- | --- | --- |
| leaderboard_bar | 4 | Average task score and solved tasks for deterministic baselines and validated provider submissions. | bar chart with policies on x-axis and average_task_score on y-axis; solved tasks as labels. |
| family_heatmap | 40 | Family-level solved count and average score by policy. | heatmap with task family by policy, colored by average_score and annotated with solved/tasks. |
| action_ablation_drop | 6 | Mean score drop when disabling major action groups in the task-aware heuristic. | horizontal bar chart with confidence intervals. |
| difficulty_band_counts | 5 | Number of public tasks by deterministic-baseline difficulty band. | ordered bar chart. |
| metric_sensitivity_rankings | 9 | Metric sensitivity rankings compared with the official average task score. | table or slope chart showing ranking changes across metrics. |

## Source Artifacts

- `outputs/founderbench-paper-tables.json`
- `outputs/founderbench-action-ablation.json`
- `outputs/founderbench-difficulty-calibration.json`
- `outputs/founderbench-metric-sensitivity.json`

## Validation

Status: PASS

All figure datasets are present and trace to generated current release artifacts.
