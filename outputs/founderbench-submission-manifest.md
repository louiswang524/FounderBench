# FounderBench Submission Manifest

This generated manifest is a compact reviewer-facing map of what the current submission includes, what it supports, and what it intentionally does not claim yet.

## Readiness

| Field | Value |
| --- | --- |
| submission_gate | not_ready |
| completion_claim | not_complete |
| ready_for_publication | False |
| failed_gates | ['required_experiments', 'provider_run_readiness', 'claim_evidence_alignment', 'license_and_citation'] |
| required_experiments_missing | 6 |

## Included Evidence Summary

| Area | Included Evidence |
| --- | --- |
| task_suite | 50 fixed public current release startup tasks across 10 families. |
| simulator | Deterministic seeded startup simulator with 13 structured business actions and an 8-market catalog. |
| metrics | Bounded 0-100 task score, solve rate, diagnostics, sensitivity analysis, paired statistics, and pre-specified comparison protocol. |
| baselines | Random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks with ablations. |
| reproducibility | Reviewer smoke test, reproducibility manifest, determinism audit, release checksum manifest, and bundle integrity report. |

## Core Review Files

| Path | Present | Bytes |
| --- | --- | --- |
| outputs/founderbench-benchmark-card.md | yes | 6843 |
| outputs/founderbench-task-manifest.json | yes | 33747 |
| outputs/founderbench-task-coverage.md | yes | 3566 |
| outputs/founderbench-metrics-and-evaluation.md | yes | 7625 |
| outputs/founderbench-baseline-analysis.md | yes | 4380 |
| outputs/founderbench-model-comparison.md | yes | 4523 |
| outputs/founderbench-paper-tables.md | yes | 4510 |
| outputs/founderbench-validity-report.md | yes | 5808 |
| outputs/founderbench-claim-evidence.md | yes | 5750 |
| outputs/founderbench-submission-gate.md | yes | 1492 |
| outputs/founderbench-completion-audit.md | yes | 8166 |
| outputs/founderbench-reviewer-index.md | yes | 20471 |
| release/founderbench/SHA256SUMS.json | yes | 40818 |
| release/founderbench/BUNDLE-INTEGRITY.md | yes | 662 |

## Supported Claims

| Claim | Permitted Wording | Evidence |
| --- | --- | --- |
| controlled_startup_operator_benchmark | FounderBench evaluates structured startup-like operating decisions in a controlled simulator. | `work/moneybench/moneybench/env.py`, `work/moneybench/SPEC.md`, `outputs/founderbench-benchmark-card.md` |
| expanded_50_task_suite | The benchmark contains 50 fixed public tasks across 10 balanced task families. | `outputs/founderbench-task-manifest.json`, `outputs/founderbench-task-coverage.md` |
| structured_action_space | The simulator executes only structured actions; rationale is retained for auditability but not scored directly. | `work/moneybench/moneybench/schema.py`, `work/moneybench/moneybench/task_runner.py`, `outputs/founderbench-task-coverage.md` |
| bounded_normalized_metrics | Each task returns a bounded 0-100 score; tasks are solved at score >= 70. | `outputs/founderbench-metrics-and-evaluation.md`, `outputs/founderbench-score-rubric.md`, `work/moneybench/moneybench/tasks.py` |
| deterministic_baseline_spread | Deterministic baselines show a wide spread from random to task-aware heuristic on the public current suite. | `outputs/founderbench-baseline-leaderboard.json`, `outputs/founderbench-baseline-analysis.md`, `outputs/founderbench-paper-tables.md` |
| capability_ladder_ablation | The deterministic policy ladder is a calibration ablation, not a model architecture ablation. | `outputs/founderbench-ablation-report.md`, `outputs/founderbench-paper-tables.md` |

## Excluded Or Not Yet Supported Claims

| Claim | Current Wording | Blocked Wording | Missing Evidence |
| --- | --- | --- | --- |
| hosted_llm_comparison | Provider adapters and experiment protocols are included; hosted current release LLM results remain to be run. | DeepSeek, Claude, and Gemini have been fully compared on current release. | `outputs/founderbench-deepseek.json`, `outputs/founderbench-anthropic.json`, `outputs/founderbench-gemini.json` |
| private_holdout_available | The benchmark includes a private-holdout blueprint and evaluator protocol, not executed hidden results. | The reported current release leaderboard is hidden or private. | `outputs/founderbench-private-holdout-results.json` |
| real_world_startup_prediction | FounderBench is a synthetic controlled environment for studying startup-relevant decisions. | High benchmark score means a model can run a successful real company. | `executed human/expert validation study`, `real-world outcome correlation study` |

## Reproduction Commands

| Purpose | Working Directory | Command |
| --- | --- | --- |
| Regenerate generated artifacts | work/moneybench | `python -m moneybench.release regenerate` |
| Validate generated artifacts and tests | work/moneybench | `python -m moneybench.release validate` |
| Build supplementary release bundle | work/moneybench | `python -m moneybench.release bundle` |

## Remaining Work

| Gate | Blocker | Evidence |
| --- | --- | --- |
| required_experiments | 6 required experiment groups are missing. | `outputs/founderbench-experiment-matrix.md` |
| provider_run_readiness | Only 0/5 provider configurations are ready. | `outputs/founderbench-provider-readiness.md` |
| claim_evidence_alignment | 3 stronger claims remain unsupported by current evidence. | `outputs/founderbench-claim-evidence.md` |
| license_and_citation | License/citation metadata is not public-release ready. | `outputs/founderbench-license-readiness.md`, `work/moneybench/CITATION.cff`, `work/moneybench/LICENSE-TODO.md` |

## Validation

Status: PASS

The submission manifest is internally consistent with the current gate, completion audit, and claim-evidence report.
