# FounderBench v0.3 Leaderboard Stability Audit

Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling.

## Method

| Item | Value |
| --- | --- |
| primary_metric | average_task_score |
| task_count | 50 |
| split_checks | Recompute rankings separately on public_dev and public_test. |
| leave_one_family_out | Recompute rankings after removing each 5-task family. |
| bootstrap | 1000 resamples of 50 task ids with replacement. |
| bootstrap_seed | 20260716 |

## Summary

| Metric | Value |
| --- | --- |
| policies | 4 |
| tasks | 50 |
| primary_leader | task_heuristic |
| full_ranking | ['task_heuristic', 'heuristic', 'conservative', 'random'] |
| split_same_leader | 2 |
| leave_one_family_same_leader | 10 |
| families_checked | 10 |
| bootstrap_primary_leader_probability | 1.0 |
| minimum_leave_one_family_spearman | 1.0 |

## Split Stability

| Split | Tasks | Leader | Ranking | Spearman vs Full | Same Leader |
| --- | --- | --- | --- | --- | --- |
| public_dev | 30 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| public_test | 20 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |

## Leave-One-Family-Out Stability

| Held-Out Family | Tasks Used | Leader | Ranking | Spearman vs Full | Same Leader |
| --- | --- | --- | --- | --- | --- |
| Market selection | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| First revenue | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Retention improvement | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Churn shock recovery | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Demo Day traction | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Pricing | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Runway preservation | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Pivot decision | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Fundraising | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |
| Channel expansion | 45 | task_heuristic | task_heuristic > heuristic > conservative > random | 1.0 | True |

## Bootstrap Task-Mix Stability

| Policy | Full Rank | Full Score | Leader Probability | Mean Bootstrap Rank |
| --- | --- | --- | --- | --- |
| task_heuristic | 1 | 80.9 | 1.0 | 1.0 |
| heuristic | 2 | 61.01 | 0.0 | 2.004 |
| conservative | 3 | 54.04 | 0.0 | 2.996 |
| random | 4 | 33.3 | 0.0 | 4.0 |

## Claim Guardrail

This audit supports deterministic-baseline rank stability only; hosted/local LLM rankings still require validated provider runs and repeated-run uncertainty.

## Validation

Status: PASS

The deterministic-baseline leaderboard is internally audited for split, family, and task-mix stability.
