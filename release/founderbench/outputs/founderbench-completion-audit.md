# FounderBench Goal Completion Audit

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
- Completion standard: A fixed current task manifest contains more than 25 tasks and task coverage/provenance artifacts explain families, splits, curation, and cards.
- Status: `complete`
- Rationale: Task manifest reports 50 tasks.

Evidence:
- `outputs/founderbench-task-manifest.json`: present
- `outputs/founderbench-task-coverage.md`: present
- `outputs/founderbench-task-provenance.md`: present
- `outputs/founderbench-task-cards.md`: present

### simulator_and_action_space

- Goal clause: strengthen the controlled simulator and action space
- Completion standard: Simulator, market catalog, action semantics, and action ablation artifacts exist and document/exercise structured startup actions.
- Status: `complete`
- Rationale: Action semantics catalog documents 13 structured actions.

Evidence:
- `work/moneybench/moneybench/env.py`: present
- `work/moneybench/moneybench/schema.py`: present
- `outputs/founderbench-action-semantics.md`: present
- `outputs/founderbench-market-catalog.md`: present
- `outputs/founderbench-action-ablation.md`: present

### normalized_business_metrics

- Goal clause: define rigorous normalized business metrics
- Completion standard: Primary bounded score, diagnostics, score rubric, sensitivity analysis, and statistical protocol are generated and internally validated.
- Status: `complete`
- Rationale: Metric, rubric, sensitivity, and statistical-protocol artifacts are present.

Evidence:
- `outputs/founderbench-metrics-and-evaluation.md`: present
- `outputs/founderbench-score-rubric.md`: present
- `outputs/founderbench-metric-sensitivity.md`: present
- `outputs/founderbench-statistical-protocol.md`: present
- `outputs/founderbench-paired-statistics.md`: present

### heuristic_baselines_and_ablations

- Goal clause: run representative heuristic baselines with ablations
- Completion standard: Deterministic non-LLM baselines cover all 50 tasks and ablation/statistical/difficulty artifacts exist.
- Status: `complete`
- Rationale: Four deterministic baselines each report 50 tasks.

Evidence:
- `outputs/founderbench-baseline-raw.json`: present
- `outputs/founderbench-baseline-leaderboard.json`: present
- `outputs/founderbench-baseline-analysis.md`: present
- `outputs/founderbench-ablation-report.md`: present
- `outputs/founderbench-action-ablation.md`: present
- `outputs/founderbench-difficulty-calibration.md`: present

### representative_llm_baselines

- Goal clause: run representative LLM baselines
- Completion standard: Required DeepSeek, Anthropic, Gemini, and local/open-source current release outputs exist and pass submission validation.
- Status: `missing`
- Rationale: 6 required experiment groups are missing and 0/5 providers are ready.

Evidence:
- `outputs/founderbench-deepseek.json`: missing
- `outputs/founderbench-deepseek-submission-report.md`: missing
- `outputs/founderbench-anthropic.json`: missing
- `outputs/founderbench-anthropic-submission-report.md`: missing
- `outputs/founderbench-gemini.json`: missing
- `outputs/founderbench-gemini-submission-report.md`: missing
- `outputs/founderbench-local-open-model.json`: missing
- `outputs/founderbench-local-open-model-submission-report.md`: missing
- `outputs/founderbench-provider-run-status.md`: present
- `outputs/founderbench-experiment-runbook.md`: present

Missing evidence:
- `outputs/founderbench-deepseek.json`
- `outputs/founderbench-deepseek-submission-report.md`
- `outputs/founderbench-anthropic.json`
- `outputs/founderbench-anthropic-submission-report.md`
- `outputs/founderbench-gemini.json`
- `outputs/founderbench-gemini-submission-report.md`
- `outputs/founderbench-local-open-model.json`
- `outputs/founderbench-local-open-model-submission-report.md`

### documentation_and_accessibility

- Goal clause: document reproducibility and limitations
- Completion standard: README, spec, reproduction guide, reviewer index, environment/determinism manifests, validity report, and submission schemas are present.
- Status: `complete`
- Rationale: Documentation, reproduction, audit, and schema artifacts are present.

Evidence:
- `work/moneybench/README.md`: present
- `work/moneybench/SPEC.md`: present
- `outputs/founderbench-reproduction-guide.md`: present
- `outputs/founderbench-reviewer-index.md`: present
- `outputs/founderbench-reproducibility-manifest.md`: present
- `outputs/founderbench-environment-report.md`: present
- `outputs/founderbench-determinism-audit.md`: present
- `outputs/founderbench-validity-report.md`: present
- `outputs/founderbench-model-submission-schema.md`: present

### benchmark_card_and_paper_artifacts

- Goal clause: prepare the benchmark card plus paper-ready experimental evidence
- Completion standard: Benchmark card, paper draft, paper tables/figure data, references, claim-evidence report, submission gate, and release bundle exist.
- Status: `partial`
- Rationale: Paper artifacts are present, but 3 stronger claims remain unsupported.

Evidence:
- `outputs/founderbench-benchmark-card.md`: present
- `outputs/founderbench-paper-draft.md`: present
- `outputs/founderbench-paper-tables.md`: present
- `outputs/founderbench-paper-figure-data.md`: present
- `outputs/founderbench-references.bib`: present
- `outputs/founderbench-claim-evidence.md`: present
- `outputs/founderbench-submission-gate.md`: present
- `release/founderbench/SHA256SUMS.json`: present
- `release/founderbench/BUNDLE-INTEGRITY.md`: present

### public_release_metadata

- Goal clause: publishable benchmark paper artifact
- Completion standard: Final public LICENSE and CITATION metadata are selected by the project owner.
- Status: `incomplete`
- Rationale: License/citation metadata is not public-release ready.

Evidence:
- `work/moneybench/LICENSE`: missing
- `work/moneybench/CITATION.cff`: present
- `outputs/founderbench-license-readiness.md`: present
- `outputs/founderbench-release-metadata-checklist.md`: present

Missing evidence:
- `work/moneybench/LICENSE`

## Validation

Status: PASS

The completion audit is internally consistent with the current goal and submission gate.
