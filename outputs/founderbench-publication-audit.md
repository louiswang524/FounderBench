# FounderBench Publication Audit

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
| hosted_llm_baselines | open_blocker | missing | 0 | Needs fresh DeepSeek/Claude/Gemini current release runs with audit logs and submission validation. |
| local_open_source_baseline | open_blocker | missing | 0 | Needs local OpenAI-compatible inference server/model run or uploaded raw result. |
| executed_private_holdout | open_blocker | missing | 0 | Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in current release. |
| final_license_metadata | open_blocker | incomplete | 6 | CITATION.cff and LICENSE-TODO.md contain owner-facing placeholders. |

## Complete Evidence Items

### completed_artifact

Completed benchmark code, task suite, runner, and release bundle.

- `work/founderbench/founderbench/env.py` (17665 bytes)
- `work/founderbench/founderbench/market_catalog.py` (8477 bytes)
- `work/founderbench/founderbench/tasks.py` (34135 bytes)
- `work/founderbench/founderbench/task_runner.py` (9544 bytes)
- `outputs/founderbench-simulator-invariant-audit.md` (1905 bytes)
- `outputs/founderbench-simulator-invariant-audit.json` (8236 bytes)
- `outputs/founderbench-action-semantics.md` (8403 bytes)
- `outputs/founderbench-action-semantics.json` (8747 bytes)
- `outputs/founderbench-market-catalog.md` (5295 bytes)
- `outputs/founderbench-market-catalog.json` (8028 bytes)
- `outputs/founderbench-task-manifest.json` (33747 bytes)
- `outputs/founderbench-task-coverage.md` (3566 bytes)
- `outputs/founderbench-task-coverage.json` (48725 bytes)
- `outputs/founderbench-task-feasibility-audit.md` (12196 bytes)
- `outputs/founderbench-task-feasibility-audit.json` (28826 bytes)
- `outputs/founderbench-task-revision-ledger.md` (8781 bytes)
- `outputs/founderbench-task-revision-ledger.json` (16203 bytes)
- `outputs/founderbench-task-provenance.md` (3767 bytes)
- `outputs/founderbench-task-provenance.json` (33755 bytes)
- `outputs/founderbench-task-cards.md` (38555 bytes)
- `outputs/founderbench-task-cards.json` (66561 bytes)
- `release/founderbench/SHA256SUMS.json` (40996 bytes)

### metrics_protocol

Defined primary, secondary, diagnostic, family-specific, and uncertainty metrics.

- `outputs/founderbench-metrics-and-evaluation.md` (7627 bytes)
- `outputs/founderbench-metric-sensitivity.md` (3113 bytes)
- `outputs/founderbench-metric-sensitivity.json` (5830 bytes)
- `outputs/founderbench-statistical-protocol.md` (3516 bytes)
- `outputs/founderbench-statistical-protocol.json` (3591 bytes)
- `outputs/founderbench-power-analysis.md` (3049 bytes)
- `outputs/founderbench-power-analysis.json` (3782 bytes)
- `outputs/founderbench-score-rubric.md` (7092 bytes)
- `outputs/founderbench-score-rubric.json` (12206 bytes)
- `outputs/founderbench-scoring-consistency-audit.md` (3807 bytes)
- `outputs/founderbench-scoring-consistency-audit.json` (6412 bytes)
- `outputs/founderbench-baseline-analysis.md` (4380 bytes)
- `outputs/founderbench-paper-tables.md` (5429 bytes)
- `outputs/founderbench-paper-tables.json` (13476 bytes)
- `outputs/founderbench-model-result-cards.md` (4209 bytes)
- `outputs/founderbench-model-result-cards.json` (12073 bytes)
- `outputs/founderbench-paper-figure-data.md` (1628 bytes)
- `outputs/founderbench-paper-figure-data.json` (15206 bytes)
- `outputs/founderbench-random-repeats.md` (795 bytes)

### heuristic_baselines

Representative non-LLM baseline leaderboard and raw results on all 50 current tasks.

- `outputs/founderbench-baseline-leaderboard.json` (2653 bytes)
- `outputs/founderbench-leaderboard-policy.md` (3389 bytes)
- `outputs/founderbench-leaderboard-policy.json` (4124 bytes)
- `outputs/founderbench-leaderboard-stability.md` (3181 bytes)
- `outputs/founderbench-leaderboard-stability.json` (7593 bytes)
- `outputs/founderbench-baseline-raw.json` (342117 bytes)
- `outputs/founderbench-model-comparison.md` (5442 bytes)
- `outputs/founderbench-model-comparison.json` (14115 bytes)
- `outputs/founderbench-result-integrity-audit.md` (1582 bytes)
- `outputs/founderbench-result-integrity-audit.json` (2081 bytes)
- `outputs/founderbench-model-result-cards.md` (4209 bytes)
- `outputs/founderbench-model-result-cards.json` (12073 bytes)
- `outputs/founderbench-ablation-report.md` (2444 bytes)
- `outputs/founderbench-action-ablation.md` (2372 bytes)
- `outputs/founderbench-action-ablation.json` (643468 bytes)
- `outputs/founderbench-paired-statistics.md` (2169 bytes)
- `outputs/founderbench-paired-statistics.json` (2706 bytes)
- `outputs/founderbench-difficulty-calibration.md` (5566 bytes)
- `outputs/founderbench-difficulty-calibration.json` (37652 bytes)
- `outputs/founderbench-task-feasibility-audit.md` (12196 bytes)
- `outputs/founderbench-task-feasibility-audit.json` (28826 bytes)
- `outputs/founderbench-task-revision-ledger.md` (8781 bytes)
- `outputs/founderbench-task-revision-ledger.json` (16203 bytes)

### provider_adapters

Hosted/local provider adapters and model submission validation tooling.

- `work/founderbench/founderbench/llm_policy.py` (17847 bytes)
- `work/founderbench/founderbench/prompt_protocol.py` (8150 bytes)
- `work/founderbench/founderbench/local_model.py` (6088 bytes)
- `work/founderbench/founderbench/baseline_execution_plan.py` (16257 bytes)
- `work/founderbench/founderbench/experiment_runbook.py` (14085 bytes)
- `work/founderbench/founderbench/provider_readiness.py` (10337 bytes)
- `work/founderbench/founderbench/provider_run_status.py` (11070 bytes)
- `work/founderbench/founderbench/cost_accounting.py` (8483 bytes)
- `work/founderbench/founderbench/submission.py` (8913 bytes)
- `work/founderbench/founderbench/submission_bundle.py` (8809 bytes)
- `work/founderbench/founderbench/submission_schema.py` (9386 bytes)
- `outputs/founderbench-model-submission-template.md` (4362 bytes)
- `outputs/founderbench-leaderboard-policy.md` (3389 bytes)
- `outputs/founderbench-leaderboard-policy.json` (4124 bytes)
- `outputs/founderbench-model-submission-schema.md` (1516 bytes)
- `outputs/founderbench-model-submission-schema.json` (20298 bytes)
- `outputs/founderbench-submission-bundle-protocol.md` (1529 bytes)
- `outputs/founderbench-submission-bundle-protocol.json` (1685 bytes)
- `outputs/founderbench-local-openai-compatible-protocol.md` (1171 bytes)
- `outputs/founderbench-local-openai-compatible-protocol.json` (1575 bytes)
- `outputs/founderbench-prompt-protocol.md` (5202 bytes)
- `outputs/founderbench-prompt-protocol.json` (7130 bytes)
- `outputs/founderbench-provider-readiness.md` (6689 bytes)
- `outputs/founderbench-provider-readiness.json` (9082 bytes)
- `outputs/founderbench-cost-accounting.md` (2408 bytes)
- `outputs/founderbench-cost-accounting.json` (2530 bytes)
- `outputs/founderbench-baseline-execution-plan.md` (17282 bytes)
- `outputs/founderbench-baseline-execution-plan.json` (27938 bytes)
- `outputs/founderbench-experiment-runbook.md` (24358 bytes)
- `outputs/founderbench-experiment-runbook.json` (28926 bytes)
- `outputs/founderbench-provider-run-status.md` (5434 bytes)
- `outputs/founderbench-provider-run-status.json` (16984 bytes)
- `outputs/founderbench-provider-comparability-audit.md` (3847 bytes)
- `outputs/founderbench-provider-comparability-audit.json` (9594 bytes)
- `outputs/founderbench-provider-contract-audit.md` (2167 bytes)
- `outputs/founderbench-provider-contract-audit.json` (3003 bytes)
- `outputs/founderbench-submission-validation.md` (1431 bytes)

### auditability

Trace, parse-failure, redaction, and qualitative analysis support.

- `work/founderbench/founderbench/provider_adapter.py` (4363 bytes)
- `work/founderbench/founderbench/qualitative.py` (8492 bytes)
- `outputs/founderbench-qualitative-traces.md` (5229 bytes)
- `outputs/founderbench-qualitative-traces.json` (27316 bytes)
- `outputs/founderbench-environment-report.md` (2203 bytes)
- `outputs/founderbench-environment-report.json` (18283 bytes)
- `outputs/founderbench-simulator-invariant-audit.md` (1905 bytes)
- `outputs/founderbench-simulator-invariant-audit.json` (8236 bytes)
- `outputs/founderbench-scoring-consistency-audit.md` (3807 bytes)
- `outputs/founderbench-scoring-consistency-audit.json` (6412 bytes)
- `outputs/founderbench-reproducibility-manifest.md` (24840 bytes)
- `outputs/founderbench-reproducibility-manifest.json` (38540 bytes)
- `outputs/founderbench-result-integrity-audit.md` (1582 bytes)
- `outputs/founderbench-result-integrity-audit.json` (2081 bytes)
- `outputs/founderbench-determinism-audit.md` (1298 bytes)
- `outputs/founderbench-determinism-audit.json` (2364 bytes)
- `outputs/founderbench-prompt-protocol.md` (5202 bytes)
- `outputs/founderbench-prompt-protocol.json` (7130 bytes)
- `outputs/founderbench-provider-comparability-audit.md` (3847 bytes)
- `outputs/founderbench-provider-comparability-audit.json` (9594 bytes)
- `outputs/founderbench-provider-contract-audit.md` (2167 bytes)
- `outputs/founderbench-provider-contract-audit.json` (3003 bytes)
- `outputs/founderbench-contamination-leakage-audit.md` (4287 bytes)
- `outputs/founderbench-contamination-leakage-audit.json` (5009 bytes)

### private_holdout_protocol

Private holdout blueprint, fingerprint generator, and evaluator protocol.

- `work/founderbench/founderbench/holdout.py` (10925 bytes)
- `work/founderbench/founderbench/private_holdout_evaluator.py` (7766 bytes)
- `outputs/founderbench-private-holdout-blueprint.json` (1629 bytes)
- `outputs/founderbench-private-holdout-evaluator-protocol.md` (2167 bytes)
- `outputs/founderbench-private-holdout-evaluator-protocol.json` (2180 bytes)
- `outputs/founderbench-private-holdout-smoke.md` (1334 bytes)
- `outputs/founderbench-private-holdout-smoke.json` (1782 bytes)
- `outputs/founderbench-contamination-leakage-audit.md` (4287 bytes)
- `outputs/founderbench-contamination-leakage-audit.json` (5009 bytes)

### documentation

Benchmark card, reproduction guide, specification, paper draft, references, and checklist.

- `work/founderbench/README.md` (20687 bytes)
- `work/founderbench/SPEC.md` (9647 bytes)
- `work/founderbench/CITATION.cff.template` (582 bytes)
- `work/founderbench/LICENSE.template` (468 bytes)
- `outputs/founderbench-benchmark-card.md` (6843 bytes)
- `outputs/founderbench-datasheet.md` (5208 bytes)
- `outputs/founderbench-datasheet.json` (6665 bytes)
- `outputs/founderbench-reproduction-guide.md` (7323 bytes)
- `outputs/founderbench-reviewer-smoke.md` (1325 bytes)
- `outputs/founderbench-reviewer-smoke.json` (1581 bytes)
- `outputs/founderbench-human-calibration-protocol.md` (3803 bytes)
- `outputs/founderbench-human-calibration-protocol.json` (4335 bytes)
- `outputs/founderbench-human-calibration-schema.md` (2016 bytes)
- `outputs/founderbench-human-calibration-schema.json` (2118 bytes)
- `outputs/founderbench-human-calibration-template.json` (6895 bytes)
- `outputs/founderbench-human-calibration-analysis.md` (988 bytes)
- `outputs/founderbench-human-calibration-analysis.json` (884 bytes)
- `outputs/founderbench-human-calibration-packet.md` (4908 bytes)
- `outputs/founderbench-human-calibration-packet.json` (5426 bytes)
- `outputs/founderbench-task-revision-ledger.md` (8781 bytes)
- `outputs/founderbench-task-revision-ledger.json` (16203 bytes)
- `outputs/founderbench-paper-draft.md` (27853 bytes)
- `outputs/founderbench-citation-audit.md` (2651 bytes)
- `outputs/founderbench-citation-audit.json` (8482 bytes)
- `outputs/founderbench-paper-evidence-map.md` (8114 bytes)
- `outputs/founderbench-paper-evidence-map.json` (17081 bytes)
- `outputs/founderbench-references.bib` (5246 bytes)
- `outputs/founderbench-reference-provenance.json` (2102 bytes)
- `outputs/founderbench-validity-report.md` (5782 bytes)
- `outputs/founderbench-validity-report.json` (10130 bytes)
- `outputs/founderbench-responsible-use.md` (4057 bytes)
- `outputs/founderbench-responsible-use.json` (4471 bytes)
- `outputs/founderbench-simulator-invariant-audit.md` (1905 bytes)
- `outputs/founderbench-simulator-invariant-audit.json` (8236 bytes)
- `outputs/founderbench-claim-evidence.md` (5768 bytes)
- `outputs/founderbench-claim-evidence.json` (10489 bytes)
- `outputs/founderbench-paper-claim-lint.md` (1530 bytes)
- `outputs/founderbench-paper-claim-lint.json` (1880 bytes)
- `outputs/founderbench-submission-gate.md` (1498 bytes)
- `outputs/founderbench-submission-gate.json` (2223 bytes)
- `outputs/founderbench-submission-manifest.md` (5856 bytes)
- `outputs/founderbench-submission-manifest.json` (9530 bytes)
- `outputs/founderbench-completion-audit.md` (8186 bytes)
- `outputs/founderbench-completion-audit.json` (15327 bytes)
- `outputs/founderbench-reviewer-risk-audit.md` (9851 bytes)
- `outputs/founderbench-reviewer-risk-audit.json` (13320 bytes)
- `outputs/founderbench-provider-contract-audit.md` (2167 bytes)
- `outputs/founderbench-provider-contract-audit.json` (3003 bytes)
- `outputs/founderbench-contamination-leakage-audit.md` (4287 bytes)
- `outputs/founderbench-contamination-leakage-audit.json` (5009 bytes)
- `outputs/founderbench-failure-mode-audit.md` (8556 bytes)
- `outputs/founderbench-failure-mode-audit.json` (11463 bytes)
- `outputs/founderbench-submission-action-plan.md` (17359 bytes)
- `outputs/founderbench-submission-action-plan.json` (23008 bytes)
- `outputs/founderbench-supplementary-package-checklist.md` (12204 bytes)
- `outputs/founderbench-experiment-matrix.md` (5249 bytes)
- `outputs/founderbench-experiment-matrix.json` (14076 bytes)
- `outputs/founderbench-reviewer-index.md` (20469 bytes)
- `outputs/founderbench-reviewer-index.json` (35692 bytes)

## Open Blockers

- `hosted_llm_baselines`: Full current release hosted LLM baselines on all 50 tasks.
  Blocker: Needs fresh DeepSeek/Claude/Gemini current release runs with audit logs and submission validation.
- `local_open_source_baseline`: At least one local/open-source model baseline.
  Blocker: Needs local OpenAI-compatible inference server/model run or uploaded raw result.
- `executed_private_holdout`: Executed hidden-suite leaderboard on evaluator host.
  Blocker: Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in current release.
- `final_license_metadata`: Final public license and citation metadata selected by project owner.
  Blocker: CITATION.cff and LICENSE-TODO.md contain owner-facing placeholders.
