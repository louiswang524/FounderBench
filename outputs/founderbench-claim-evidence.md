# FounderBench Claim-Evidence Report

This generated report maps major paper/benchmark-card claims to current evidence. It is intentionally conservative: claims about hosted LLM comparisons, hidden holdouts, or real-world startup prediction remain unsupported until the required evidence exists.

## Summary

| Metric | Value |
| --- | --- |
| claims | 9 |
| supported | 6 |
| unsupported_currently | 3 |
| evidence_complete | 9 |

## Claim Matrix

| ID | Status | Evidence | Permitted Wording | Avoid Wording |
| --- | --- | --- | --- | --- |
| controlled_startup_operator_benchmark | supported | yes | FounderBench evaluates structured startup-like operating decisions in a controlled simulator. | FounderBench measures real-world startup success. |
| expanded_50_task_suite | supported | yes | The benchmark contains 50 fixed public tasks across 10 balanced task families. | The benchmark contains a hidden or privately evaluated benchmark suite. |
| structured_action_space | supported | yes | The simulator executes only structured actions; rationale is retained for auditability but not scored directly. | Models can earn score through persuasive business prose. |
| bounded_normalized_metrics | supported | yes | Each task returns a bounded 0-100 score; tasks are solved at score >= 70. | The score is a direct dollar value or external business valuation. |
| deterministic_baseline_spread | supported | yes | Deterministic baselines show a wide spread from random to task-aware heuristic on the public current suite. | The benchmark is validated against current frontier LLMs. |
| capability_ladder_ablation | supported | yes | The deterministic policy ladder is a calibration ablation, not a model architecture ablation. | The ablation proves LLM reasoning mechanisms. |
| hosted_llm_comparison | unsupported_currently | yes | Provider adapters and experiment protocols are included; hosted current release LLM results remain to be run. | DeepSeek, Claude, and Gemini have been fully compared on current release. |
| private_holdout_available | unsupported_currently | yes | The benchmark includes a private-holdout blueprint and evaluator protocol, not executed hidden results. | The reported current release leaderboard is hidden or private. |
| real_world_startup_prediction | unsupported_currently | yes | FounderBench is a synthetic controlled environment for studying startup-relevant decisions. | High benchmark score means a model can run a successful real company. |

## Evidence Detail

### controlled_startup_operator_benchmark

FounderBench is a controlled benchmark for evaluating startup-operator agents under bounded resources.

Evidence:
- `work/founderbench/founderbench/env.py`: present
- `work/founderbench/SPEC.md`: present
- `outputs/founderbench-benchmark-card.md`: present

### expanded_50_task_suite

The current release artifact contains 50 fixed public tasks across 10 startup operating families.

Evidence:
- `outputs/founderbench-task-manifest.json`: present
- `outputs/founderbench-task-coverage.md`: present

### structured_action_space

Agents are evaluated through a structured 13-action business interface, and free-form rationale does not directly affect score.

Evidence:
- `work/founderbench/founderbench/schema.py`: present
- `work/founderbench/founderbench/task_runner.py`: present
- `outputs/founderbench-task-coverage.md`: present

### bounded_normalized_metrics

Task scores are bounded from 0 to 100 with a solve threshold of 70 and family-specific scoring rubrics.

Evidence:
- `outputs/founderbench-metrics-and-evaluation.md`: present
- `outputs/founderbench-score-rubric.md`: present
- `work/founderbench/founderbench/tasks.py`: present

### deterministic_baseline_spread

Rule-based baselines show the benchmark is neither solved by random action sampling nor impossible for simple structured policies.

Evidence:
- `outputs/founderbench-baseline-leaderboard.json`: present
- `outputs/founderbench-baseline-analysis.md`: present
- `outputs/founderbench-paper-tables.md`: present

### capability_ladder_ablation

The deterministic policy ladder gives an ablation-style calibration of business-decision capabilities.

Evidence:
- `outputs/founderbench-ablation-report.md`: present
- `outputs/founderbench-paper-tables.md`: present

### hosted_llm_comparison

FounderBench differentiates current hosted LLM providers on current release.

Evidence:
- `outputs/founderbench-provider-readiness.md`: present
- `outputs/founderbench-experiment-matrix.md`: present

Missing evidence before stronger claim:
- `outputs/founderbench-deepseek.json`: missing
- `outputs/founderbench-anthropic.json`: missing
- `outputs/founderbench-gemini.json`: missing

### private_holdout_available

The benchmark includes an executed private hidden holdout leaderboard.

Evidence:
- `outputs/founderbench-private-holdout-blueprint.json`: present
- `outputs/founderbench-private-holdout-evaluator-protocol.md`: present

Missing evidence before stronger claim:
- `outputs/founderbench-private-holdout-results.json`: missing

### real_world_startup_prediction

FounderBench predicts real startup profitability or long-term company success.

Evidence:
- `outputs/founderbench-validity-report.md`: present
- `outputs/founderbench-human-calibration-protocol.md`: present
- `outputs/founderbench-benchmark-card.md`: present

Missing evidence before stronger claim:
- `executed human/expert validation study`: missing
- `real-world outcome correlation study`: missing

## Validation

Status: PASS

All supported claims have current evidence, and unsupported claims name the missing evidence required before stronger wording.
