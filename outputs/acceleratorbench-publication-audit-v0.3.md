# FounderBench v0.3 Publication Audit

This audit maps benchmark/dataset submission expectations to concrete release artifacts. It is generated from the current workspace and intentionally keeps unresolved publication blockers visible.

## Summary

| Status | Count |
| --- | --- |
| complete | 7 |
| incomplete | 1 |
| missing | 3 |

## Requirement Matrix

| ID | Category | Status | Evidence Files | Blocker |
| --- | --- | --- | --- | --- |
| completed_artifact | artifact | complete | 22 |  |
| metrics_protocol | metrics | complete | 19 |  |
| heuristic_baselines | baselines | complete | 23 |  |
| provider_adapters | baselines | complete | 37 |  |
| auditability | reproducibility | complete | 24 |  |
| private_holdout_protocol | anti_gaming | complete | 9 |  |
| documentation | documentation | complete | 59 |  |
| hosted_llm_baselines | open_blocker | missing | 0 | Needs fresh DeepSeek/Claude/Gemini v0.3.0 runs with audit logs and submission validation. |
| local_open_source_baseline | open_blocker | missing | 0 | Needs local OpenAI-compatible inference server/model run or uploaded raw result. |
| executed_private_holdout | open_blocker | missing | 0 | Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in v0.3.0. |
| final_license_metadata | open_blocker | incomplete | 6 | CITATION.cff and LICENSE-TODO.md contain owner-facing placeholders. |

## Complete Evidence Items

### completed_artifact

Completed benchmark code, task suite, runner, and release bundle.

- `work/moneybench/moneybench/env.py` (17663 bytes)
- `work/moneybench/moneybench/market_catalog.py` (8265 bytes)
- `work/moneybench/moneybench/tasks.py` (34061 bytes)
- `work/moneybench/moneybench/task_runner.py` (8645 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md` (1910 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.json` (8236 bytes)
- `outputs/acceleratorbench-action-semantics-v0.3.md` (8408 bytes)
- `outputs/acceleratorbench-action-semantics-v0.3.json` (8747 bytes)
- `outputs/acceleratorbench-market-catalog-v0.3.md` (5291 bytes)
- `outputs/acceleratorbench-market-catalog-v0.3.json` (8019 bytes)
- `outputs/acceleratorbench-task-manifest-v0.3.json` (33738 bytes)
- `outputs/acceleratorbench-task-coverage-v0.3.md` (3571 bytes)
- `outputs/acceleratorbench-task-coverage-v0.3.json` (48725 bytes)
- `outputs/acceleratorbench-task-feasibility-audit-v0.3.md` (12201 bytes)
- `outputs/acceleratorbench-task-feasibility-audit-v0.3.json` (28826 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md` (8777 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.json` (16194 bytes)
- `outputs/acceleratorbench-task-provenance-v0.3.md` (3741 bytes)
- `outputs/acceleratorbench-task-provenance-v0.3.json` (33733 bytes)
- `outputs/acceleratorbench-task-cards-v0.3.md` (38551 bytes)
- `outputs/acceleratorbench-task-cards-v0.3.json` (66552 bytes)
- `release/acceleratorbench-v0.3.0/SHA256SUMS.json` (42106 bytes)

### metrics_protocol

Defined primary, secondary, diagnostic, family-specific, and uncertainty metrics.

- `outputs/acceleratorbench-metrics-and-evaluation.md` (7358 bytes)
- `outputs/acceleratorbench-metric-sensitivity-v0.3.md` (3118 bytes)
- `outputs/acceleratorbench-metric-sensitivity-v0.3.json` (5839 bytes)
- `outputs/acceleratorbench-statistical-protocol-v0.3.md` (3583 bytes)
- `outputs/acceleratorbench-statistical-protocol-v0.3.json` (3653 bytes)
- `outputs/acceleratorbench-power-analysis-v0.3.md` (3053 bytes)
- `outputs/acceleratorbench-power-analysis-v0.3.json` (3790 bytes)
- `outputs/acceleratorbench-score-rubric-v0.3.md` (7097 bytes)
- `outputs/acceleratorbench-score-rubric-v0.3.json` (12206 bytes)
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.md` (3812 bytes)
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.json` (6421 bytes)
- `outputs/acceleratorbench-baseline-analysis-v0.3.md` (4385 bytes)
- `outputs/acceleratorbench-paper-tables-v0.3.md` (4587 bytes)
- `outputs/acceleratorbench-paper-tables-v0.3.json` (9221 bytes)
- `outputs/acceleratorbench-model-result-cards-v0.3.md` (3164 bytes)
- `outputs/acceleratorbench-model-result-cards-v0.3.json` (7987 bytes)
- `outputs/acceleratorbench-paper-figure-data-v0.3.md` (1647 bytes)
- `outputs/acceleratorbench-paper-figure-data-v0.3.json` (15231 bytes)
- `outputs/acceleratorbench-random-repeats-v0.3.md` (800 bytes)

### heuristic_baselines

Representative non-LLM baseline leaderboard and raw results on all 50 v0.3.0 tasks.

- `outputs/acceleratorbench-baseline-leaderboard-v0.3.json` (2653 bytes)
- `outputs/acceleratorbench-leaderboard-policy-v0.3.md` (3488 bytes)
- `outputs/acceleratorbench-leaderboard-policy-v0.3.json` (4223 bytes)
- `outputs/acceleratorbench-leaderboard-stability-v0.3.md` (3186 bytes)
- `outputs/acceleratorbench-leaderboard-stability-v0.3.json` (7602 bytes)
- `outputs/acceleratorbench-baseline-raw-v0.3.json` (342102 bytes)
- `outputs/acceleratorbench-model-comparison-v0.3.md` (4618 bytes)
- `outputs/acceleratorbench-model-comparison-v0.3.json` (9674 bytes)
- `outputs/acceleratorbench-result-integrity-audit-v0.3.md` (1623 bytes)
- `outputs/acceleratorbench-result-integrity-audit-v0.3.json` (2117 bytes)
- `outputs/acceleratorbench-model-result-cards-v0.3.md` (3164 bytes)
- `outputs/acceleratorbench-model-result-cards-v0.3.json` (7987 bytes)
- `outputs/acceleratorbench-ablation-report-v0.3.md` (2449 bytes)
- `outputs/acceleratorbench-action-ablation-v0.3.md` (2377 bytes)
- `outputs/acceleratorbench-action-ablation-v0.3.json` (643744 bytes)
- `outputs/acceleratorbench-paired-statistics-v0.3.md` (2174 bytes)
- `outputs/acceleratorbench-paired-statistics-v0.3.json` (2715 bytes)
- `outputs/acceleratorbench-difficulty-calibration-v0.3.md` (5571 bytes)
- `outputs/acceleratorbench-difficulty-calibration-v0.3.json` (37661 bytes)
- `outputs/acceleratorbench-task-feasibility-audit-v0.3.md` (12201 bytes)
- `outputs/acceleratorbench-task-feasibility-audit-v0.3.json` (28826 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md` (8777 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.json` (16194 bytes)

### provider_adapters

Hosted/local provider adapters and model submission validation tooling.

- `work/moneybench/moneybench/llm_policy.py` (17178 bytes)
- `work/moneybench/moneybench/prompt_protocol.py` (8341 bytes)
- `work/moneybench/moneybench/local_model.py` (5968 bytes)
- `work/moneybench/moneybench/baseline_execution_plan.py` (13721 bytes)
- `work/moneybench/moneybench/experiment_runbook.py` (14237 bytes)
- `work/moneybench/moneybench/provider_readiness.py` (6360 bytes)
- `work/moneybench/moneybench/provider_run_status.py` (10829 bytes)
- `work/moneybench/moneybench/cost_accounting.py` (8282 bytes)
- `work/moneybench/moneybench/submission.py` (8913 bytes)
- `work/moneybench/moneybench/submission_bundle.py` (8649 bytes)
- `work/moneybench/moneybench/submission_schema.py` (9164 bytes)
- `outputs/acceleratorbench-model-submission-template.md` (4260 bytes)
- `outputs/acceleratorbench-leaderboard-policy-v0.3.md` (3488 bytes)
- `outputs/acceleratorbench-leaderboard-policy-v0.3.json` (4223 bytes)
- `outputs/acceleratorbench-model-submission-schema-v0.3.md` (1506 bytes)
- `outputs/acceleratorbench-model-submission-schema-v0.3.json` (20304 bytes)
- `outputs/acceleratorbench-submission-bundle-protocol-v0.3.md` (1584 bytes)
- `outputs/acceleratorbench-submission-bundle-protocol-v0.3.json` (1740 bytes)
- `outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.md` (1194 bytes)
- `outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.json` (1603 bytes)
- `outputs/acceleratorbench-prompt-protocol-v0.3.md` (4536 bytes)
- `outputs/acceleratorbench-prompt-protocol-v0.3.json` (5473 bytes)
- `outputs/acceleratorbench-provider-readiness-v0.3.md` (3332 bytes)
- `outputs/acceleratorbench-provider-readiness-v0.3.json` (4322 bytes)
- `outputs/acceleratorbench-cost-accounting-v0.3.md` (2413 bytes)
- `outputs/acceleratorbench-cost-accounting-v0.3.json` (2530 bytes)
- `outputs/acceleratorbench-baseline-execution-plan-v0.3.md` (10314 bytes)
- `outputs/acceleratorbench-baseline-execution-plan-v0.3.json` (15421 bytes)
- `outputs/acceleratorbench-experiment-runbook-v0.3.md` (15964 bytes)
- `outputs/acceleratorbench-experiment-runbook-v0.3.json` (18521 bytes)
- `outputs/acceleratorbench-provider-run-status-v0.3.md` (4463 bytes)
- `outputs/acceleratorbench-provider-run-status-v0.3.json` (10488 bytes)
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.md` (3255 bytes)
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.json` (5893 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md` (2170 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.json` (3001 bytes)
- `outputs/acceleratorbench-submission-validation-v0.3.md` (1440 bytes)

### auditability

Trace, parse-failure, redaction, and qualitative analysis support.

- `work/moneybench/moneybench/provider_adapter.py` (4359 bytes)
- `work/moneybench/moneybench/qualitative.py` (8296 bytes)
- `outputs/acceleratorbench-qualitative-traces-v0.3.md` (5234 bytes)
- `outputs/acceleratorbench-qualitative-traces-v0.3.json` (27325 bytes)
- `outputs/acceleratorbench-environment-report-v0.3.md` (2183 bytes)
- `outputs/acceleratorbench-environment-report-v0.3.json` (17940 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md` (1910 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.json` (8236 bytes)
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.md` (3812 bytes)
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.json` (6421 bytes)
- `outputs/acceleratorbench-reproducibility-manifest-v0.3.md` (25528 bytes)
- `outputs/acceleratorbench-reproducibility-manifest-v0.3.json` (39201 bytes)
- `outputs/acceleratorbench-result-integrity-audit-v0.3.md` (1623 bytes)
- `outputs/acceleratorbench-result-integrity-audit-v0.3.json` (2117 bytes)
- `outputs/acceleratorbench-determinism-audit-v0.3.md` (1303 bytes)
- `outputs/acceleratorbench-determinism-audit-v0.3.json` (2364 bytes)
- `outputs/acceleratorbench-prompt-protocol-v0.3.md` (4536 bytes)
- `outputs/acceleratorbench-prompt-protocol-v0.3.json` (5473 bytes)
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.md` (3255 bytes)
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.json` (5893 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md` (2170 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.json` (3001 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md` (4302 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.json` (5019 bytes)

### private_holdout_protocol

Private holdout blueprint, fingerprint generator, and evaluator protocol.

- `work/moneybench/moneybench/holdout.py` (10921 bytes)
- `work/moneybench/moneybench/private_holdout_evaluator.py` (7766 bytes)
- `outputs/acceleratorbench-private-holdout-blueprint-v0.3.json` (1629 bytes)
- `outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md` (2163 bytes)
- `outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.json` (2176 bytes)
- `outputs/acceleratorbench-private-holdout-smoke-v0.3.md` (1339 bytes)
- `outputs/acceleratorbench-private-holdout-smoke-v0.3.json` (1782 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md` (4302 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.json` (5019 bytes)

### documentation

Benchmark card, reproduction guide, specification, paper draft, references, and checklist.

- `work/moneybench/README.md` (21778 bytes)
- `work/moneybench/SPEC.md` (9226 bytes)
- `work/moneybench/CITATION.cff.template` (571 bytes)
- `work/moneybench/LICENSE.template` (475 bytes)
- `outputs/acceleratorbench-benchmark-card.md` (6684 bytes)
- `outputs/acceleratorbench-datasheet-v0.3.md` (5252 bytes)
- `outputs/acceleratorbench-datasheet-v0.3.json` (6704 bytes)
- `outputs/acceleratorbench-reproduction-guide.md` (7272 bytes)
- `outputs/acceleratorbench-reviewer-smoke-v0.3.md` (1365 bytes)
- `outputs/acceleratorbench-reviewer-smoke-v0.3.json` (1616 bytes)
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md` (3808 bytes)
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.json` (4335 bytes)
- `outputs/acceleratorbench-human-calibration-schema-v0.3.md` (2021 bytes)
- `outputs/acceleratorbench-human-calibration-schema-v0.3.json` (2118 bytes)
- `outputs/acceleratorbench-human-calibration-template-v0.3.json` (6895 bytes)
- `outputs/acceleratorbench-human-calibration-analysis-v0.3.md` (993 bytes)
- `outputs/acceleratorbench-human-calibration-analysis-v0.3.json` (884 bytes)
- `outputs/acceleratorbench-human-calibration-packet-v0.3.md` (4981 bytes)
- `outputs/acceleratorbench-human-calibration-packet-v0.3.json` (5494 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md` (8777 bytes)
- `outputs/acceleratorbench-task-revision-ledger-v0.3.json` (16194 bytes)
- `outputs/acceleratorbench-paper-draft-v0.1.md` (27632 bytes)
- `outputs/acceleratorbench-citation-audit-v0.3.md` (2656 bytes)
- `outputs/acceleratorbench-citation-audit-v0.3.json` (8491 bytes)
- `outputs/acceleratorbench-paper-evidence-map-v0.3.md` (8562 bytes)
- `outputs/acceleratorbench-paper-evidence-map-v0.3.json` (17538 bytes)
- `outputs/acceleratorbench-references.bib` (5246 bytes)
- `outputs/acceleratorbench-reference-provenance-v0.3.json` (2102 bytes)
- `outputs/acceleratorbench-validity-report-v0.3.md` (5998 bytes)
- `outputs/acceleratorbench-validity-report-v0.3.json` (10521 bytes)
- `outputs/acceleratorbench-responsible-use-v0.3.md` (4105 bytes)
- `outputs/acceleratorbench-responsible-use-v0.3.json` (4514 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md` (1910 bytes)
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.json` (8236 bytes)
- `outputs/acceleratorbench-claim-evidence-v0.3.md` (5856 bytes)
- `outputs/acceleratorbench-claim-evidence-v0.3.json` (10737 bytes)
- `outputs/acceleratorbench-paper-claim-lint-v0.3.md` (1548 bytes)
- `outputs/acceleratorbench-paper-claim-lint-v0.3.json` (1893 bytes)
- `outputs/acceleratorbench-submission-gate-v0.3.md` (1553 bytes)
- `outputs/acceleratorbench-submission-gate-v0.3.json` (2273 bytes)
- `outputs/acceleratorbench-submission-manifest-v0.3.md` (6050 bytes)
- `outputs/acceleratorbench-submission-manifest-v0.3.json` (9719 bytes)
- `outputs/acceleratorbench-completion-audit-v0.3.md` (8627 bytes)
- `outputs/acceleratorbench-completion-audit-v0.3.json` (15764 bytes)
- `outputs/acceleratorbench-reviewer-risk-audit-v0.3.md` (10135 bytes)
- `outputs/acceleratorbench-reviewer-risk-audit-v0.3.json` (13599 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md` (2170 bytes)
- `outputs/acceleratorbench-provider-contract-audit-v0.3.json` (3001 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md` (4302 bytes)
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.json` (5019 bytes)
- `outputs/acceleratorbench-failure-mode-audit-v0.3.md` (8786 bytes)
- `outputs/acceleratorbench-failure-mode-audit-v0.3.json` (11689 bytes)
- `outputs/acceleratorbench-submission-action-plan-v0.3.md` (13345 bytes)
- `outputs/acceleratorbench-submission-action-plan-v0.3.json` (18240 bytes)
- `outputs/acceleratorbench-supplementary-package-checklist.md` (11842 bytes)
- `outputs/acceleratorbench-experiment-matrix-v0.3.md` (5601 bytes)
- `outputs/acceleratorbench-experiment-matrix-v0.3.json` (16096 bytes)
- `outputs/acceleratorbench-reviewer-index-v0.3.md` (21562 bytes)
- `outputs/acceleratorbench-reviewer-index-v0.3.json` (36758 bytes)

## Open Blockers

- `hosted_llm_baselines`: Full v0.3.0 hosted LLM baselines on all 50 tasks.
  Blocker: Needs fresh DeepSeek/Claude/Gemini v0.3.0 runs with audit logs and submission validation.
- `local_open_source_baseline`: At least one local/open-source model baseline.
  Blocker: Needs local OpenAI-compatible inference server/model run or uploaded raw result.
- `executed_private_holdout`: Executed hidden-suite leaderboard on evaluator host.
  Blocker: Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in v0.3.0.
- `final_license_metadata`: Final public license and citation metadata selected by project owner.
  Blocker: CITATION.cff and LICENSE-TODO.md contain owner-facing placeholders.
