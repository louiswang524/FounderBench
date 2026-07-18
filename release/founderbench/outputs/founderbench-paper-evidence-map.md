# FounderBench Paper Evidence Map

This generated map links paper-draft sections to the artifacts that support them. It keeps planned hosted/local LLM comparisons separate from currently supported deterministic evidence.

Submission gate: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| sections | 8 |
| supported | 5 |
| qualified | 2 |
| excluded_until_evidence | 1 |
| incomplete | 0 |

## Section Crosswalk

| Paper Section | Status | Claim | Rationale |
| --- | --- | --- | --- |
| Abstract and Introduction | qualified | FounderBench evaluates structured startup-like operating decisions in a controlled simulator, not real-world company success. | FounderBench is a synthetic controlled environment for studying startup-relevant decisions. |
| Benchmark Design | supported | The current release artifact contains 50 fixed public tasks across 10 families, 13 structured actions, and a fixed simulated market catalog. | All section evidence paths are present. |
| Metrics | supported | Scores are bounded 0-100 task outcomes with solve threshold, diagnostics, sensitivity checks, and paired comparison protocol. | All section evidence paths are present. |
| Baselines | supported | The paper currently reports deterministic random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks. | Deterministic baseline evidence is present; provider rows are correctly excluded. |
| Ablations and Difficulty Calibration | supported | Capability-ladder, action-space, task-difficulty, and qualitative trace artifacts support deterministic calibration claims. | All section evidence paths are present. |
| Hosted and Local LLM Results | excluded_until_evidence | Hosted/local provider comparison is planned but not yet supported by current evidence. | Provider adapters and experiment protocols are included; hosted current release LLM results remain to be run. |
| Reproducibility and Auditability | supported | The package includes reproduction commands, source/output hashes, environment report, reviewer smoke test, deterministic replay audit, and release-bundle integrity report. | All section evidence paths are present. |
| Limitations | qualified | Limitations are documented for synthetic simulator validity, missing hosted LLM evidence, missing human calibration, missing private holdout execution, and release metadata. | The benchmark includes a private-holdout blueprint and evaluator protocol, not executed hidden results.; FounderBench is a synthetic controlled environment for studying startup-relevant decisions. |

## Evidence Detail

### Abstract and Introduction

Status: `qualified`

FounderBench evaluates structured startup-like operating decisions in a controlled simulator, not real-world company success.

Evidence:
- `outputs/founderbench-benchmark-card.md`: present
- `outputs/founderbench-datasheet.md`: present
- `outputs/founderbench-responsible-use.md`: present
- `work/founderbench/SPEC.md`: present
- `outputs/founderbench-claim-evidence.md`: present

Claim-evidence ids:
- `controlled_startup_operator_benchmark`
- `real_world_startup_prediction`

### Benchmark Design

Status: `supported`

The current release artifact contains 50 fixed public tasks across 10 families, 13 structured actions, and a fixed simulated market catalog.

Evidence:
- `outputs/founderbench-task-manifest.json`: present
- `outputs/founderbench-task-coverage.md`: present
- `outputs/founderbench-simulator-invariant-audit.md`: present
- `outputs/founderbench-contamination-leakage-audit.md`: present
- `outputs/founderbench-action-semantics.md`: present
- `outputs/founderbench-market-catalog.md`: present

Claim-evidence ids:
- `expanded_50_task_suite`
- `structured_action_space`

### Metrics

Status: `supported`

Scores are bounded 0-100 task outcomes with solve threshold, diagnostics, sensitivity checks, and paired comparison protocol.

Evidence:
- `outputs/founderbench-metrics-and-evaluation.md`: present
- `outputs/founderbench-score-rubric.md`: present
- `outputs/founderbench-scoring-consistency-audit.md`: present
- `outputs/founderbench-metric-sensitivity.md`: present
- `outputs/founderbench-statistical-protocol.md`: present
- `outputs/founderbench-paired-statistics.md`: present
- `outputs/founderbench-power-analysis.md`: present

Claim-evidence ids:
- `bounded_normalized_metrics`

### Baselines

Status: `supported`

The paper currently reports deterministic random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks.

Evidence:
- `outputs/founderbench-baseline-raw.json`: present
- `outputs/founderbench-baseline-leaderboard.json`: present
- `outputs/founderbench-leaderboard-policy.md`: present
- `outputs/founderbench-leaderboard-stability.md`: present
- `outputs/founderbench-baseline-analysis.md`: present
- `outputs/founderbench-result-integrity-audit.md`: present
- `outputs/founderbench-paper-tables.md`: present
- `outputs/founderbench-model-result-cards.md`: present

Claim-evidence ids:
- `deterministic_baseline_spread`

### Ablations and Difficulty Calibration

Status: `supported`

Capability-ladder, action-space, task-difficulty, and qualitative trace artifacts support deterministic calibration claims.

Evidence:
- `outputs/founderbench-ablation-report.md`: present
- `outputs/founderbench-action-ablation.md`: present
- `outputs/founderbench-difficulty-calibration.md`: present
- `outputs/founderbench-task-revision-ledger.md`: present
- `outputs/founderbench-qualitative-traces.md`: present

Claim-evidence ids:
- `capability_ladder_ablation`

### Hosted and Local LLM Results

Status: `excluded_until_evidence`

Hosted/local provider comparison is planned but not yet supported by current evidence.

Evidence:
- `outputs/founderbench-experiment-matrix.md`: present
- `outputs/founderbench-experiment-runbook.md`: present
- `outputs/founderbench-provider-run-status.md`: present
- `outputs/founderbench-provider-comparability-audit.md`: present
- `outputs/founderbench-provider-contract-audit.md`: present
- `outputs/founderbench-leaderboard-policy.md`: present
- `outputs/founderbench-model-result-cards.md`: present
- `outputs/founderbench-submission-manifest.md`: present

Claim-evidence ids:
- `hosted_llm_comparison`

### Reproducibility and Auditability

Status: `supported`

The package includes reproduction commands, source/output hashes, environment report, reviewer smoke test, deterministic replay audit, and release-bundle integrity report.

Evidence:
- `outputs/founderbench-reproduction-guide.md`: present
- `outputs/founderbench-reproducibility-manifest.md`: present
- `outputs/founderbench-result-integrity-audit.md`: present
- `outputs/founderbench-environment-report.md`: present
- `outputs/founderbench-reviewer-smoke.md`: present
- `outputs/founderbench-simulator-invariant-audit.md`: present
- `outputs/founderbench-determinism-audit.md`: present
- `outputs/founderbench-provider-contract-audit.md`: present
- `outputs/founderbench-contamination-leakage-audit.md`: present
- `release/founderbench/BUNDLE-INTEGRITY.md`: present

### Limitations

Status: `qualified`

Limitations are documented for synthetic simulator validity, missing hosted LLM evidence, missing human calibration, missing private holdout execution, and release metadata.

Evidence:
- `outputs/founderbench-validity-report.md`: present
- `outputs/founderbench-datasheet.md`: present
- `outputs/founderbench-responsible-use.md`: present
- `outputs/founderbench-contamination-leakage-audit.md`: present
- `outputs/founderbench-human-calibration-analysis.md`: present
- `outputs/founderbench-task-revision-ledger.md`: present
- `outputs/founderbench-completion-audit.md`: present
- `outputs/founderbench-submission-gate.md`: present

Claim-evidence ids:
- `private_holdout_available`
- `real_world_startup_prediction`

## Validation

Status: PASS

The paper evidence map is internally consistent with current artifacts and claim guardrails.
