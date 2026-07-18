# FounderBench v0.3 Claim-Evidence Report

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
| expanded_50_task_suite | supported | yes | v0.3.0 contains 50 fixed public tasks across 10 balanced task families. | v0.3.0 contains a hidden or privately evaluated benchmark suite. |
| structured_action_space | supported | yes | The simulator executes only structured actions; rationale is retained for auditability but not scored directly. | Models can earn score through persuasive business prose. |
| bounded_normalized_metrics | supported | yes | Each task returns a bounded 0-100 score; tasks are solved at score >= 70. | The score is a direct dollar value or external business valuation. |
| deterministic_baseline_spread | supported | yes | Deterministic baselines show a wide spread from random to task-aware heuristic on the public v0.3 suite. | The benchmark is validated against current frontier LLMs. |
| capability_ladder_ablation | supported | yes | The deterministic policy ladder is a calibration ablation, not a model architecture ablation. | The ablation proves LLM reasoning mechanisms. |
| hosted_llm_comparison | unsupported_currently | yes | Provider adapters and experiment protocols are included; hosted v0.3 LLM results remain to be run. | DeepSeek, Claude, and Gemini have been fully compared on v0.3.0. |
| private_holdout_available | unsupported_currently | yes | v0.3.0 includes a private-holdout blueprint and evaluator protocol, not executed hidden results. | The reported v0.3 leaderboard is hidden or private. |
| real_world_startup_prediction | unsupported_currently | yes | FounderBench is a synthetic controlled environment for studying startup-relevant decisions. | High benchmark score means a model can run a successful real company. |

## Evidence Detail

### controlled_startup_operator_benchmark

FounderBench is a controlled benchmark for evaluating startup-operator agents under bounded resources.

Evidence:
- `work/moneybench/moneybench/env.py`: present
- `work/moneybench/SPEC.md`: present
- `outputs/acceleratorbench-benchmark-card.md`: present

### expanded_50_task_suite

The v0.3 artifact contains 50 fixed public tasks across 10 startup operating families.

Evidence:
- `outputs/acceleratorbench-task-manifest-v0.3.json`: present
- `outputs/acceleratorbench-task-coverage-v0.3.md`: present

### structured_action_space

Agents are evaluated through a structured 13-action business interface, and free-form rationale does not directly affect score.

Evidence:
- `work/moneybench/moneybench/schema.py`: present
- `work/moneybench/moneybench/task_runner.py`: present
- `outputs/acceleratorbench-task-coverage-v0.3.md`: present

### bounded_normalized_metrics

Task scores are bounded from 0 to 100 with a solve threshold of 70 and family-specific scoring rubrics.

Evidence:
- `outputs/acceleratorbench-metrics-and-evaluation.md`: present
- `outputs/acceleratorbench-score-rubric-v0.3.md`: present
- `work/moneybench/moneybench/tasks.py`: present

### deterministic_baseline_spread

Rule-based baselines show the benchmark is neither solved by random action sampling nor impossible for simple structured policies.

Evidence:
- `outputs/acceleratorbench-baseline-leaderboard-v0.3.json`: present
- `outputs/acceleratorbench-baseline-analysis-v0.3.md`: present
- `outputs/acceleratorbench-paper-tables-v0.3.md`: present

### capability_ladder_ablation

The deterministic policy ladder gives an ablation-style calibration of business-decision capabilities.

Evidence:
- `outputs/acceleratorbench-ablation-report-v0.3.md`: present
- `outputs/acceleratorbench-paper-tables-v0.3.md`: present

### hosted_llm_comparison

FounderBench differentiates current hosted LLM providers on v0.3.0.

Evidence:
- `outputs/acceleratorbench-provider-readiness-v0.3.md`: present
- `outputs/acceleratorbench-experiment-matrix-v0.3.md`: present

Missing evidence before stronger claim:
- `outputs/acceleratorbench-deepseek-v0.3.json`: missing
- `outputs/acceleratorbench-anthropic-v0.3.json`: missing
- `outputs/acceleratorbench-gemini-v0.3.json`: missing

### private_holdout_available

v0.3.0 includes an executed private hidden holdout leaderboard.

Evidence:
- `outputs/acceleratorbench-private-holdout-blueprint-v0.3.json`: present
- `outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md`: present

Missing evidence before stronger claim:
- `outputs/acceleratorbench-private-holdout-results-v0.3.json`: missing

### real_world_startup_prediction

FounderBench predicts real startup profitability or long-term company success.

Evidence:
- `outputs/acceleratorbench-validity-report-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`: present
- `outputs/acceleratorbench-benchmark-card.md`: present

Missing evidence before stronger claim:
- `executed human/expert validation study`: missing
- `real-world outcome correlation study`: missing

## Validation

Status: PASS

All supported claims have current evidence, and unsupported claims name the missing evidence required before stronger wording.
