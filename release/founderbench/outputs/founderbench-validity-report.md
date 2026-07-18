# FounderBench Validity and Limitations Report

This generated report states known threats to validity, current mitigations, artifact evidence, and remaining work. It is intended to keep paper claims appropriately scoped.

## Summary

| Metric | Value |
| --- | --- |
| threats | 8 |
| high_severity | 3 |
| medium_severity | 4 |
| low_severity | 1 |
| evidence_complete | 8 |

## Threat Matrix

| ID | Category | Severity | Evidence | Current Mitigation | Remaining Work |
| --- | --- | --- | --- | --- | --- |
| synthetic_market_dynamics | construct_validity | high | yes | Frame the benchmark as a controlled decision environment, not a real-market proxy; expose simulator code, score rubrics, market catalog, a human-calibration protocol, and a task-revision ledger for calibration issues. | Execute expert review or human-founder calibration to assess whether task incentives match startup judgment. |
| template_generated_tasks | external_validity | medium | yes | Report task-family coverage, split balance, seeds, horizons, and action coverage in generated artifacts. | Curate additional scenarios from public startup postmortems, accelerator cases, or expert-authored variants. |
| visible_public_test | evaluation_validity | high | yes | Label public_dev/public_test honestly and provide private-holdout blueprint plus evaluator protocol. | Instantiate hidden task definitions on an evaluator host and report hidden-suite scores. |
| missing_llm_baselines | empirical_validity | high | yes | Provider adapters, readiness matrix, submission validator, and experiment matrix specify exact missing runs. | Run DeepSeek, Claude, Gemini, self-consistency, and at least one local open-source model on all 50 tasks. |
| prompt_and_sampling_sensitivity | reliability | medium | yes | Support repeated-run reports, raw task outputs, audit mode, and submission validation. | Report repeated prompt-sample intervals for hosted LLM submissions and freeze prompt versions. |
| adapter_and_format_failures | measurement_validity | medium | yes | Count provider errors, parse categories, invalid actions, and over-budget decisions as diagnostics rather than discarding runs. | Include redacted hosted audit traces for representative provider successes and failures. |
| heuristic_ceiling_bias | baseline_validity | medium | yes | Report it as a capability-ladder calibration baseline, not as an agent-realistic baseline. | Compare against prompt-only LLMs, self-consistency, and local open models to contextualize the heuristic ceiling. |
| missing_human_founder_baseline | interpretability | low | yes | Use relative model/baseline comparisons, provide a human-calibration protocol and revision ledger, and avoid claiming real-world startup competence. | Execute the protocol and collect small expert/human-founder pilot results or expert ranking of task actions. |

## Evidence Paths

### synthetic_market_dynamics

The simulator uses hand-designed demand, churn, reputation, risk, and cash dynamics rather than real startup markets.

- `work/founderbench/founderbench/env.py`: present
- `outputs/founderbench-score-rubric.md`: present
- `outputs/founderbench-market-catalog.md`: present
- `outputs/founderbench-simulator-invariant-audit.md`: present
- `outputs/founderbench-human-calibration-protocol.md`: present
- `outputs/founderbench-task-revision-ledger.md`: present
- `outputs/founderbench-benchmark-card.md`: present

### template_generated_tasks

The 50 public tasks are generated from 10 templates rather than curated from real startup histories.

- `outputs/founderbench-task-manifest.json`: present
- `outputs/founderbench-task-coverage.md`: present

### visible_public_test

The public test split is visible, so agents or prompts can overfit to released tasks.

- `outputs/founderbench-private-holdout-blueprint.json`: present
- `outputs/founderbench-private-holdout-evaluator-protocol.md`: present
- `outputs/founderbench-contamination-leakage-audit.md`: present

### missing_llm_baselines

The current current release paper evidence includes deterministic baselines but lacks complete hosted/local LLM baselines.

- `outputs/founderbench-provider-readiness.md`: present
- `outputs/founderbench-experiment-matrix.md`: present
- `outputs/founderbench-model-submission-template.md`: present

### prompt_and_sampling_sensitivity

Hosted LLM scores may depend on prompt wording, decoding settings, and stochastic sampling.

- `outputs/founderbench-random-repeats.md`: present
- `outputs/founderbench-reproduction-guide.md`: present
- `work/founderbench/founderbench/repeats.py`: present

### adapter_and_format_failures

A model can fail because of malformed JSON or provider errors rather than poor business decisions.

- `work/founderbench/founderbench/provider_adapter.py`: present
- `work/founderbench/founderbench/submission.py`: present
- `outputs/founderbench-provider-contract-audit.md`: present
- `outputs/founderbench-submission-validation.md`: present

### heuristic_ceiling_bias

The task-aware heuristic may encode task-family knowledge that ordinary LLM agents do not receive.

- `outputs/founderbench-ablation-report.md`: present
- `outputs/founderbench-paper-tables.md`: present

### missing_human_founder_baseline

Without a human or expert baseline, it is hard to interpret absolute scores as business judgment quality.

- `outputs/founderbench-benchmark-card.md`: present
- `outputs/founderbench-human-calibration-protocol.md`: present
- `outputs/founderbench-task-revision-ledger.md`: present
- `outputs/founderbench-paper-draft.md`: present

## Validation

Status: PASS

The report covers construct, external, evaluation, empirical, and reliability threats with mitigations and remaining work.
