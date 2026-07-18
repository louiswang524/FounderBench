# FounderBench v0.3 Validity and Limitations Report

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

- `work/moneybench/moneybench/env.py`: present
- `outputs/acceleratorbench-score-rubric-v0.3.md`: present
- `outputs/acceleratorbench-market-catalog-v0.3.md`: present
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`: present
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md`: present
- `outputs/acceleratorbench-benchmark-card.md`: present

### template_generated_tasks

The 50 public tasks are generated from 10 templates rather than curated from real startup histories.

- `outputs/acceleratorbench-task-manifest-v0.3.json`: present
- `outputs/acceleratorbench-task-coverage-v0.3.md`: present

### visible_public_test

The public test split is visible, so agents or prompts can overfit to released tasks.

- `outputs/acceleratorbench-private-holdout-blueprint-v0.3.json`: present
- `outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md`: present
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`: present

### missing_llm_baselines

The current v0.3 paper evidence includes deterministic baselines but lacks complete hosted/local LLM baselines.

- `outputs/acceleratorbench-provider-readiness-v0.3.md`: present
- `outputs/acceleratorbench-experiment-matrix-v0.3.md`: present
- `outputs/acceleratorbench-model-submission-template.md`: present

### prompt_and_sampling_sensitivity

Hosted LLM scores may depend on prompt wording, decoding settings, and stochastic sampling.

- `outputs/acceleratorbench-random-repeats-v0.3.md`: present
- `outputs/acceleratorbench-reproduction-guide.md`: present
- `work/moneybench/moneybench/repeats.py`: present

### adapter_and_format_failures

A model can fail because of malformed JSON or provider errors rather than poor business decisions.

- `work/moneybench/moneybench/provider_adapter.py`: present
- `work/moneybench/moneybench/submission.py`: present
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md`: present
- `outputs/acceleratorbench-submission-validation-v0.3.md`: present

### heuristic_ceiling_bias

The task-aware heuristic may encode task-family knowledge that ordinary LLM agents do not receive.

- `outputs/acceleratorbench-ablation-report-v0.3.md`: present
- `outputs/acceleratorbench-paper-tables-v0.3.md`: present

### missing_human_founder_baseline

Without a human or expert baseline, it is hard to interpret absolute scores as business judgment quality.

- `outputs/acceleratorbench-benchmark-card.md`: present
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`: present
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md`: present
- `outputs/acceleratorbench-paper-draft-v0.1.md`: present

## Validation

Status: PASS

The report covers construct, external, evaluation, empirical, and reliability threats with mitigations and remaining work.
