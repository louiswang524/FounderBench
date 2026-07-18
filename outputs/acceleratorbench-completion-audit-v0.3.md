# FounderBench v0.3 Goal Completion Audit

This generated audit maps the active benchmark-development goal to current evidence. It is intentionally stricter than a file-presence checklist: incomplete external model evidence and owner metadata keep the goal open.

Completion claim: `not_complete`

## Summary

| Metric | Value |
| --- | --- |
| requirements | 8 |
| complete | 5 |
| partial | 1 |
| incomplete | 1 |
| missing | 1 |
| submission_gate | not_ready |

## Requirement Status

| Requirement | Status | Goal Clause | Rationale |
| --- | --- | --- | --- |
| scaled_task_suite | complete | scale the startup-agent task suite beyond the current 25 tasks | Task manifest reports 50 tasks. |
| simulator_and_action_space | complete | strengthen the controlled simulator and action space | Action semantics catalog documents 13 structured actions. |
| normalized_business_metrics | complete | define rigorous normalized business metrics | Metric, rubric, sensitivity, and statistical-protocol artifacts are present. |
| heuristic_baselines_and_ablations | complete | run representative heuristic baselines with ablations | Four deterministic baselines each report 50 tasks. |
| representative_llm_baselines | missing | run representative LLM baselines | 6 required experiment groups are missing and 0/5 providers are ready. |
| documentation_and_accessibility | complete | document reproducibility and limitations | Documentation, reproduction, audit, and schema artifacts are present. |
| benchmark_card_and_paper_artifacts | partial | prepare the benchmark card plus paper-ready experimental evidence | Paper artifacts are present, but 3 stronger claims remain unsupported. |
| public_release_metadata | incomplete | publishable benchmark paper artifact | License/citation metadata is not public-release ready. |

## Evidence Details

### scaled_task_suite

- Goal clause: scale the startup-agent task suite beyond the current 25 tasks
- Completion standard: A fixed v0.3 task manifest contains more than 25 tasks and task coverage/provenance artifacts explain families, splits, curation, and cards.
- Status: `complete`
- Rationale: Task manifest reports 50 tasks.

Evidence:
- `outputs/acceleratorbench-task-manifest-v0.3.json`: present
- `outputs/acceleratorbench-task-coverage-v0.3.md`: present
- `outputs/acceleratorbench-task-provenance-v0.3.md`: present
- `outputs/acceleratorbench-task-cards-v0.3.md`: present

### simulator_and_action_space

- Goal clause: strengthen the controlled simulator and action space
- Completion standard: Simulator, market catalog, action semantics, and action ablation artifacts exist and document/exercise structured startup actions.
- Status: `complete`
- Rationale: Action semantics catalog documents 13 structured actions.

Evidence:
- `work/moneybench/moneybench/env.py`: present
- `work/moneybench/moneybench/schema.py`: present
- `outputs/acceleratorbench-action-semantics-v0.3.md`: present
- `outputs/acceleratorbench-market-catalog-v0.3.md`: present
- `outputs/acceleratorbench-action-ablation-v0.3.md`: present

### normalized_business_metrics

- Goal clause: define rigorous normalized business metrics
- Completion standard: Primary bounded score, diagnostics, score rubric, sensitivity analysis, and statistical protocol are generated and internally validated.
- Status: `complete`
- Rationale: Metric, rubric, sensitivity, and statistical-protocol artifacts are present.

Evidence:
- `outputs/acceleratorbench-metrics-and-evaluation.md`: present
- `outputs/acceleratorbench-score-rubric-v0.3.md`: present
- `outputs/acceleratorbench-metric-sensitivity-v0.3.md`: present
- `outputs/acceleratorbench-statistical-protocol-v0.3.md`: present
- `outputs/acceleratorbench-paired-statistics-v0.3.md`: present

### heuristic_baselines_and_ablations

- Goal clause: run representative heuristic baselines with ablations
- Completion standard: Deterministic non-LLM baselines cover all 50 tasks and ablation/statistical/difficulty artifacts exist.
- Status: `complete`
- Rationale: Four deterministic baselines each report 50 tasks.

Evidence:
- `outputs/acceleratorbench-baseline-raw-v0.3.json`: present
- `outputs/acceleratorbench-baseline-leaderboard-v0.3.json`: present
- `outputs/acceleratorbench-baseline-analysis-v0.3.md`: present
- `outputs/acceleratorbench-ablation-report-v0.3.md`: present
- `outputs/acceleratorbench-action-ablation-v0.3.md`: present
- `outputs/acceleratorbench-difficulty-calibration-v0.3.md`: present

### representative_llm_baselines

- Goal clause: run representative LLM baselines
- Completion standard: Required DeepSeek, Anthropic, Gemini, and local/open-source v0.3 outputs exist and pass submission validation.
- Status: `missing`
- Rationale: 6 required experiment groups are missing and 0/5 providers are ready.

Evidence:
- `outputs/acceleratorbench-deepseek-v0.3.json`: missing
- `outputs/acceleratorbench-deepseek-v0.3-submission-report.md`: missing
- `outputs/acceleratorbench-anthropic-v0.3.json`: missing
- `outputs/acceleratorbench-anthropic-v0.3-submission-report.md`: missing
- `outputs/acceleratorbench-gemini-v0.3.json`: missing
- `outputs/acceleratorbench-gemini-v0.3-submission-report.md`: missing
- `outputs/acceleratorbench-local-open-model-v0.3.json`: missing
- `outputs/acceleratorbench-local-open-model-v0.3-submission-report.md`: missing
- `outputs/acceleratorbench-provider-run-status-v0.3.md`: present
- `outputs/acceleratorbench-experiment-runbook-v0.3.md`: present

Missing evidence:
- `outputs/acceleratorbench-deepseek-v0.3.json`
- `outputs/acceleratorbench-deepseek-v0.3-submission-report.md`
- `outputs/acceleratorbench-anthropic-v0.3.json`
- `outputs/acceleratorbench-anthropic-v0.3-submission-report.md`
- `outputs/acceleratorbench-gemini-v0.3.json`
- `outputs/acceleratorbench-gemini-v0.3-submission-report.md`
- `outputs/acceleratorbench-local-open-model-v0.3.json`
- `outputs/acceleratorbench-local-open-model-v0.3-submission-report.md`

### documentation_and_accessibility

- Goal clause: document reproducibility and limitations
- Completion standard: README, spec, reproduction guide, reviewer index, environment/determinism manifests, validity report, and submission schemas are present.
- Status: `complete`
- Rationale: Documentation, reproduction, audit, and schema artifacts are present.

Evidence:
- `work/moneybench/README.md`: present
- `work/moneybench/SPEC.md`: present
- `outputs/acceleratorbench-reproduction-guide.md`: present
- `outputs/acceleratorbench-reviewer-index-v0.3.md`: present
- `outputs/acceleratorbench-reproducibility-manifest-v0.3.md`: present
- `outputs/acceleratorbench-environment-report-v0.3.md`: present
- `outputs/acceleratorbench-determinism-audit-v0.3.md`: present
- `outputs/acceleratorbench-validity-report-v0.3.md`: present
- `outputs/acceleratorbench-model-submission-schema-v0.3.md`: present

### benchmark_card_and_paper_artifacts

- Goal clause: prepare the benchmark card plus paper-ready experimental evidence
- Completion standard: Benchmark card, paper draft, paper tables/figure data, references, claim-evidence report, submission gate, and release bundle exist.
- Status: `partial`
- Rationale: Paper artifacts are present, but 3 stronger claims remain unsupported.

Evidence:
- `outputs/acceleratorbench-benchmark-card.md`: present
- `outputs/acceleratorbench-paper-draft-v0.1.md`: present
- `outputs/acceleratorbench-paper-tables-v0.3.md`: present
- `outputs/acceleratorbench-paper-figure-data-v0.3.md`: present
- `outputs/acceleratorbench-references.bib`: present
- `outputs/acceleratorbench-claim-evidence-v0.3.md`: present
- `outputs/acceleratorbench-submission-gate-v0.3.md`: present
- `release/acceleratorbench-v0.3.0/SHA256SUMS.json`: present
- `release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md`: present

### public_release_metadata

- Goal clause: publishable benchmark paper artifact
- Completion standard: Final public LICENSE and CITATION metadata are selected by the project owner.
- Status: `incomplete`
- Rationale: License/citation metadata is not public-release ready.

Evidence:
- `work/moneybench/LICENSE`: missing
- `work/moneybench/CITATION.cff`: present
- `outputs/acceleratorbench-license-readiness-v0.3.md`: present
- `outputs/acceleratorbench-release-metadata-checklist-v0.3.md`: present

Missing evidence:
- `work/moneybench/LICENSE`

## Validation

Status: PASS

The completion audit is internally consistent with the current goal and submission gate.
