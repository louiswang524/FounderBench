# FounderBench v0.3 Submission Manifest

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
| task_suite | 50 fixed public v0.3.0 startup tasks across 10 families. |
| simulator | Deterministic seeded startup simulator with 13 structured business actions and an 8-market catalog. |
| metrics | Bounded 0-100 task score, solve rate, diagnostics, sensitivity analysis, paired statistics, and pre-specified comparison protocol. |
| baselines | Random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks with ablations. |
| reproducibility | Reviewer smoke test, reproducibility manifest, determinism audit, release checksum manifest, and bundle integrity report. |

## Core Review Files

| Path | Present | Bytes |
| --- | --- | --- |
| outputs/acceleratorbench-benchmark-card.md | yes | 6684 |
| outputs/acceleratorbench-task-manifest-v0.3.json | yes | 33738 |
| outputs/acceleratorbench-task-coverage-v0.3.md | yes | 3571 |
| outputs/acceleratorbench-metrics-and-evaluation.md | yes | 7358 |
| outputs/acceleratorbench-baseline-analysis-v0.3.md | yes | 4385 |
| outputs/acceleratorbench-model-comparison-v0.3.md | yes | 4618 |
| outputs/acceleratorbench-paper-tables-v0.3.md | yes | 4587 |
| outputs/acceleratorbench-validity-report-v0.3.md | yes | 5998 |
| outputs/acceleratorbench-claim-evidence-v0.3.md | yes | 5856 |
| outputs/acceleratorbench-submission-gate-v0.3.md | yes | 1553 |
| outputs/acceleratorbench-completion-audit-v0.3.md | yes | 8627 |
| outputs/acceleratorbench-reviewer-index-v0.3.md | yes | 21562 |
| release/acceleratorbench-v0.3.0/SHA256SUMS.json | yes | 42106 |
| release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md | yes | 673 |

## Supported Claims

| Claim | Permitted Wording | Evidence |
| --- | --- | --- |
| controlled_startup_operator_benchmark | FounderBench evaluates structured startup-like operating decisions in a controlled simulator. | `work/moneybench/moneybench/env.py`, `work/moneybench/SPEC.md`, `outputs/acceleratorbench-benchmark-card.md` |
| expanded_50_task_suite | v0.3.0 contains 50 fixed public tasks across 10 balanced task families. | `outputs/acceleratorbench-task-manifest-v0.3.json`, `outputs/acceleratorbench-task-coverage-v0.3.md` |
| structured_action_space | The simulator executes only structured actions; rationale is retained for auditability but not scored directly. | `work/moneybench/moneybench/schema.py`, `work/moneybench/moneybench/task_runner.py`, `outputs/acceleratorbench-task-coverage-v0.3.md` |
| bounded_normalized_metrics | Each task returns a bounded 0-100 score; tasks are solved at score >= 70. | `outputs/acceleratorbench-metrics-and-evaluation.md`, `outputs/acceleratorbench-score-rubric-v0.3.md`, `work/moneybench/moneybench/tasks.py` |
| deterministic_baseline_spread | Deterministic baselines show a wide spread from random to task-aware heuristic on the public v0.3 suite. | `outputs/acceleratorbench-baseline-leaderboard-v0.3.json`, `outputs/acceleratorbench-baseline-analysis-v0.3.md`, `outputs/acceleratorbench-paper-tables-v0.3.md` |
| capability_ladder_ablation | The deterministic policy ladder is a calibration ablation, not a model architecture ablation. | `outputs/acceleratorbench-ablation-report-v0.3.md`, `outputs/acceleratorbench-paper-tables-v0.3.md` |

## Excluded Or Not Yet Supported Claims

| Claim | Current Wording | Blocked Wording | Missing Evidence |
| --- | --- | --- | --- |
| hosted_llm_comparison | Provider adapters and experiment protocols are included; hosted v0.3 LLM results remain to be run. | DeepSeek, Claude, and Gemini have been fully compared on v0.3.0. | `outputs/acceleratorbench-deepseek-v0.3.json`, `outputs/acceleratorbench-anthropic-v0.3.json`, `outputs/acceleratorbench-gemini-v0.3.json` |
| private_holdout_available | v0.3.0 includes a private-holdout blueprint and evaluator protocol, not executed hidden results. | The reported v0.3 leaderboard is hidden or private. | `outputs/acceleratorbench-private-holdout-results-v0.3.json` |
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
| required_experiments | 6 required experiment groups are missing. | `outputs/acceleratorbench-experiment-matrix-v0.3.md` |
| provider_run_readiness | Only 0/5 provider configurations are ready. | `outputs/acceleratorbench-provider-readiness-v0.3.md` |
| claim_evidence_alignment | 3 stronger claims remain unsupported by current evidence. | `outputs/acceleratorbench-claim-evidence-v0.3.md` |
| license_and_citation | License/citation metadata is not public-release ready. | `outputs/acceleratorbench-license-readiness-v0.3.md`, `work/moneybench/CITATION.cff`, `work/moneybench/LICENSE-TODO.md` |

## Validation

Status: PASS

The submission manifest is internally consistent with the current gate, completion audit, and claim-evidence report.
