# FounderBench v0.3 Paper Evidence Map

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
| Benchmark Design | supported | The v0.3 artifact contains 50 fixed public tasks across 10 families, 13 structured actions, and a fixed simulated market catalog. | All section evidence paths are present. |
| Metrics | supported | Scores are bounded 0-100 task outcomes with solve threshold, diagnostics, sensitivity checks, and paired comparison protocol. | All section evidence paths are present. |
| Baselines | supported | The paper currently reports deterministic random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks. | Deterministic baseline evidence is present; provider rows are correctly excluded. |
| Ablations and Difficulty Calibration | supported | Capability-ladder, action-space, task-difficulty, and qualitative trace artifacts support deterministic calibration claims. | All section evidence paths are present. |
| Hosted and Local LLM Results | excluded_until_evidence | Hosted/local provider comparison is planned but not yet supported by v0.3 evidence. | Provider adapters and experiment protocols are included; hosted v0.3 LLM results remain to be run. |
| Reproducibility and Auditability | supported | The package includes reproduction commands, source/output hashes, environment report, reviewer smoke test, deterministic replay audit, and release-bundle integrity report. | All section evidence paths are present. |
| Limitations | qualified | Limitations are documented for synthetic simulator validity, missing hosted LLM evidence, missing human calibration, missing private holdout execution, and release metadata. | v0.3.0 includes a private-holdout blueprint and evaluator protocol, not executed hidden results.; FounderBench is a synthetic controlled environment for studying startup-relevant decisions. |

## Evidence Detail

### Abstract and Introduction

Status: `qualified`

FounderBench evaluates structured startup-like operating decisions in a controlled simulator, not real-world company success.

Evidence:
- `outputs/acceleratorbench-benchmark-card.md`: present
- `outputs/acceleratorbench-datasheet-v0.3.md`: present
- `outputs/acceleratorbench-responsible-use-v0.3.md`: present
- `work/moneybench/SPEC.md`: present
- `outputs/acceleratorbench-claim-evidence-v0.3.md`: present

Claim-evidence ids:
- `controlled_startup_operator_benchmark`
- `real_world_startup_prediction`

### Benchmark Design

Status: `supported`

The v0.3 artifact contains 50 fixed public tasks across 10 families, 13 structured actions, and a fixed simulated market catalog.

Evidence:
- `outputs/acceleratorbench-task-manifest-v0.3.json`: present
- `outputs/acceleratorbench-task-coverage-v0.3.md`: present
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md`: present
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`: present
- `outputs/acceleratorbench-action-semantics-v0.3.md`: present
- `outputs/acceleratorbench-market-catalog-v0.3.md`: present

Claim-evidence ids:
- `expanded_50_task_suite`
- `structured_action_space`

### Metrics

Status: `supported`

Scores are bounded 0-100 task outcomes with solve threshold, diagnostics, sensitivity checks, and paired comparison protocol.

Evidence:
- `outputs/acceleratorbench-metrics-and-evaluation.md`: present
- `outputs/acceleratorbench-score-rubric-v0.3.md`: present
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.md`: present
- `outputs/acceleratorbench-metric-sensitivity-v0.3.md`: present
- `outputs/acceleratorbench-statistical-protocol-v0.3.md`: present
- `outputs/acceleratorbench-paired-statistics-v0.3.md`: present
- `outputs/acceleratorbench-power-analysis-v0.3.md`: present

Claim-evidence ids:
- `bounded_normalized_metrics`

### Baselines

Status: `supported`

The paper currently reports deterministic random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks.

Evidence:
- `outputs/acceleratorbench-baseline-raw-v0.3.json`: present
- `outputs/acceleratorbench-baseline-leaderboard-v0.3.json`: present
- `outputs/acceleratorbench-leaderboard-policy-v0.3.md`: present
- `outputs/acceleratorbench-leaderboard-stability-v0.3.md`: present
- `outputs/acceleratorbench-baseline-analysis-v0.3.md`: present
- `outputs/acceleratorbench-result-integrity-audit-v0.3.md`: present
- `outputs/acceleratorbench-paper-tables-v0.3.md`: present
- `outputs/acceleratorbench-model-result-cards-v0.3.md`: present

Claim-evidence ids:
- `deterministic_baseline_spread`

### Ablations and Difficulty Calibration

Status: `supported`

Capability-ladder, action-space, task-difficulty, and qualitative trace artifacts support deterministic calibration claims.

Evidence:
- `outputs/acceleratorbench-ablation-report-v0.3.md`: present
- `outputs/acceleratorbench-action-ablation-v0.3.md`: present
- `outputs/acceleratorbench-difficulty-calibration-v0.3.md`: present
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md`: present
- `outputs/acceleratorbench-qualitative-traces-v0.3.md`: present

Claim-evidence ids:
- `capability_ladder_ablation`

### Hosted and Local LLM Results

Status: `excluded_until_evidence`

Hosted/local provider comparison is planned but not yet supported by v0.3 evidence.

Evidence:
- `outputs/acceleratorbench-experiment-matrix-v0.3.md`: present
- `outputs/acceleratorbench-experiment-runbook-v0.3.md`: present
- `outputs/acceleratorbench-provider-run-status-v0.3.md`: present
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.md`: present
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md`: present
- `outputs/acceleratorbench-leaderboard-policy-v0.3.md`: present
- `outputs/acceleratorbench-model-result-cards-v0.3.md`: present
- `outputs/acceleratorbench-submission-manifest-v0.3.md`: present

Claim-evidence ids:
- `hosted_llm_comparison`

### Reproducibility and Auditability

Status: `supported`

The package includes reproduction commands, source/output hashes, environment report, reviewer smoke test, deterministic replay audit, and release-bundle integrity report.

Evidence:
- `outputs/acceleratorbench-reproduction-guide.md`: present
- `outputs/acceleratorbench-reproducibility-manifest-v0.3.md`: present
- `outputs/acceleratorbench-result-integrity-audit-v0.3.md`: present
- `outputs/acceleratorbench-environment-report-v0.3.md`: present
- `outputs/acceleratorbench-reviewer-smoke-v0.3.md`: present
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md`: present
- `outputs/acceleratorbench-determinism-audit-v0.3.md`: present
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md`: present
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`: present
- `release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md`: present

### Limitations

Status: `qualified`

Limitations are documented for synthetic simulator validity, missing hosted LLM evidence, missing human calibration, missing private holdout execution, and release metadata.

Evidence:
- `outputs/acceleratorbench-validity-report-v0.3.md`: present
- `outputs/acceleratorbench-datasheet-v0.3.md`: present
- `outputs/acceleratorbench-responsible-use-v0.3.md`: present
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-analysis-v0.3.md`: present
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md`: present
- `outputs/acceleratorbench-completion-audit-v0.3.md`: present
- `outputs/acceleratorbench-submission-gate-v0.3.md`: present

Claim-evidence ids:
- `private_holdout_available`
- `real_world_startup_prediction`

## Validation

Status: PASS

The paper evidence map is internally consistent with current artifacts and claim guardrails.
