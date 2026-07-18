# FounderBench Statistical Comparison Protocol

Pre-specified statistical comparison protocol for deterministic and hosted/local LLM submissions.

## Primary Endpoint

| Field | Value |
| --- | --- |
| metric | average_task_score |
| unit | fixed task episode |
| definition | Mean bounded 0-100 task score over the 50-task suite. |
| rationale | Normalizes heterogeneous startup situations while preserving task-specific business objectives. |

## Secondary Endpoints

| Metric | Definition | Use |
| --- | --- | --- |
| solve_rate | Fraction of tasks with task_score >= 70. | Interpretable success-rate companion to average score. |
| public_dev_vs_public_test | Report average score and solve rate separately for FND-001..FND-030 and FND-031..FND-050. | Detect split imbalance and possible overfitting to development tasks. |
| family_breakdown | Report solved/5 and average score for each of the 10 task families. | Identify capability profile rather than only aggregate score. |
| diagnostics | Provider errors, invalid actions, over-budget decisions, latency, token use, and estimated cost. | Distinguish business-decision failure from interface or API failure. |

## Single-Run Comparisons

| Item | Rule |
| --- | --- |
| paired_unit | task id |
| score_gap | model_a_score_i - model_b_score_i |
| interval | Nonparametric bootstrap 95% CI over paired task gaps. |
| hypothesis_test | Two-sided random sign-flip permutation test over paired task gaps. |
| effect_size | Cohen dz over paired task gaps. |
| win_loss_tie | Count tasks where model_a score is greater than, less than, or equal to model_b. |

## Repeated-Sampling Comparisons

| Item | Rule |
| --- | --- |
| when_required | Required for stochastic decoding studies, self-consistency ablations, reflection/multi-agent variants, or when reporting sampling variance. |
| minimum_repeats_recommended | 3 |
| preferred_repeats | 5 |
| aggregation | Report per-run average score and solve rate, then bootstrap across submitted runs for repeated-sampling intervals. |
| paired_repeated_option | When multiple models use identical repeat indices, compare matched repeat means with paired intervals. |

## Multiple Comparisons

| Item | Rule |
| --- | --- |
| default_family | All pairwise model comparisons reported in the main leaderboard. |
| adjustment | Holm-Bonferroni adjustment over primary endpoint p-values. |
| reporting | Report both raw and adjusted p-values; do not hide non-significant comparisons. |

## Required Reporting Fields

- model/provider snapshot
- prompt_version
- policy/agent method
- temperature and decoding settings
- task count and missing task ids if any
- average_task_score and solve_rate
- public_dev and public_test summaries
- family breakdown
- diagnostics and provider_error_categories
- token/cost assumptions
- redacted audit traces for representative success/failure cases

## Claim Rules

- Do not claim one model is better unless the comparison covers all 50 tasks or the claim is explicitly scoped.
- Do not compare raw money, final cash, or revenue as primary outcomes across tasks; use them as diagnostics.
- Treat provider errors, invalid JSON, and invalid actions as benchmark outcomes, not discarded trials.
- For hidden-holdout claims, report only evaluator-approved aggregate fields.

## Validation

Status: PASS

The protocol fixes the primary endpoint, paired unit, uncertainty estimates, repeated-run reporting, and claim guardrails before hosted/local model comparisons are added.
