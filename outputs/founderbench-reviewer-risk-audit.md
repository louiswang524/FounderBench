# FounderBench Reviewer-Risk Audit

This generated artifact is a pre-submission stress test of likely reviewer concerns. It is not a claim that peer review has occurred.

Submission gate: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| risks | 8 |
| critical | 2 |
| open_or_external | 5 |

## Severity Counts

| Severity | Count |
| --- | --- |
| administrative_major | 1 |
| critical | 2 |
| major | 5 |

## Status Counts

| Status | Count |
| --- | --- |
| mitigated_by_claim_guardrail | 1 |
| mitigated_not_closed | 1 |
| open_external | 3 |
| owner_action_required | 1 |
| partially_mitigated | 1 |
| planned_not_executed | 1 |

## Risk Table

| Risk | Lens | Severity | Status | Likely Objection | Required Response |
| --- | --- | --- | --- | --- | --- |
| missing_llm_baselines | methodology | critical | open_external | The benchmark is intended to evaluate LLM startup agents, but the current artifact only contains deterministic rule baselines. | Run and validate the required hosted/local LLM baselines, then update paper tables, claim gates, and model-comparison artifacts before making model-performance claims. |
| synthetic_validity | domain | major | mitigated_not_closed | A synthetic startup simulator may not measure real startup skill or real company outcomes. | Frame the benchmark as a controlled decision benchmark, avoid real-world success claims, and collect expert/human-founder calibration evidence. |
| overclaiming_real_world_success | editorial | critical | mitigated_by_claim_guardrail | The paper could overstate that high simulator profit predicts real startup profitability or durable company success. | Keep the supported wording narrow: FounderBench evaluates controlled startup-like operating decisions, not real-world startup prediction. |
| hidden_holdout_not_executed | anti_gaming | major | open_external | Public tasks and deterministic scoring can invite benchmark gaming without an executed private holdout. | Have an evaluator run secret-seeded private tasks and report aggregate-only holdout results for submitted models. |
| heuristic_overfitting_or_hand_coding | methodology | major | partially_mitigated | Strong task-aware heuristics may encode benchmark-specific rules, making them look better than naive LLM calls. | Report task-aware heuristic results as calibration ceilings, not agent baselines, and compare against validated LLM runs plus hidden holdout results. |
| license_metadata_missing | reproducibility | administrative_major | owner_action_required | The package is not publicly reusable until final LICENSE and citation metadata are chosen. | The project owner must select and commit final license and citation metadata before public release or supplementary submission. |
| provider_cost_reproducibility | reproducibility | major | planned_not_executed | Hosted API results may be hard to reproduce without exact usage, retries, prices, and provider-error accounting. | Record token usage, provider error categories, retry policy, model identifiers, and normalized costs for each validated provider run. |
| human_calibration_missing | domain | major | open_external | The benchmark has no included human-founder or expert calibration results showing task realism, score alignment, or gaming risks. | Collect calibration submissions, run the analyzer, and report inter-rater concerns and task revisions before strong validity claims. |

## Evidence Details

### missing_llm_baselines

- Reviewer lens: methodology
- Severity: `critical`
- Status: `open_external`
- Status rationale: 6 required experiment groups are still missing.
- Likely objection: The benchmark is intended to evaluate LLM startup agents, but the current artifact only contains deterministic rule baselines.
- Required response: Run and validate the required hosted/local LLM baselines, then update paper tables, claim gates, and model-comparison artifacts before making model-performance claims.

Evidence:
- `outputs/founderbench-experiment-matrix.md`: present
- `outputs/founderbench-provider-run-status.md`: present
- `outputs/founderbench-experiment-runbook.md`: present
- `outputs/founderbench-model-comparison.md`: present

### synthetic_validity

- Reviewer lens: domain
- Severity: `major`
- Status: `mitigated_not_closed`
- Status rationale: Threats and task provenance are documented, but external calibration remains missing.
- Likely objection: A synthetic startup simulator may not measure real startup skill or real company outcomes.
- Required response: Frame the benchmark as a controlled decision benchmark, avoid real-world success claims, and collect expert/human-founder calibration evidence.

Evidence:
- `outputs/founderbench-validity-report.md`: present
- `outputs/founderbench-task-provenance.md`: present
- `outputs/founderbench-benchmark-card.md`: present
- `outputs/founderbench-human-calibration-protocol.md`: present

### overclaiming_real_world_success

- Reviewer lens: editorial
- Severity: `critical`
- Status: `mitigated_by_claim_guardrail`
- Status rationale: Claim-evidence and paper-evidence artifacts explicitly exclude real-world success prediction.
- Likely objection: The paper could overstate that high simulator profit predicts real startup profitability or durable company success.
- Required response: Keep the supported wording narrow: FounderBench evaluates controlled startup-like operating decisions, not real-world startup prediction.

Evidence:
- `outputs/founderbench-claim-evidence.md`: present
- `outputs/founderbench-paper-evidence-map.md`: present
- `outputs/founderbench-submission-manifest.md`: present

### hidden_holdout_not_executed

- Reviewer lens: anti_gaming
- Severity: `major`
- Status: `open_external`
- Status rationale: The private-holdout protocol and smoke report exist, but no evaluator-hosted official aggregate result is included.
- Likely objection: Public tasks and deterministic scoring can invite benchmark gaming without an executed private holdout.
- Required response: Have an evaluator run secret-seeded private tasks and report aggregate-only holdout results for submitted models.

Evidence:
- `outputs/founderbench-private-holdout-evaluator-protocol.md`: present
- `outputs/founderbench-private-holdout-smoke.md`: present
- `outputs/founderbench-contamination-leakage-audit.md`: present
- `work/moneybench/moneybench/private_holdout_evaluator.py`: present
- `outputs/founderbench-submission-gate.md`: present

### heuristic_overfitting_or_hand_coding

- Reviewer lens: methodology
- Severity: `major`
- Status: `partially_mitigated`
- Status rationale: Ablations and task provenance expose heuristic behavior, but LLM and holdout evidence are still needed.
- Likely objection: Strong task-aware heuristics may encode benchmark-specific rules, making them look better than naive LLM calls.
- Required response: Report task-aware heuristic results as calibration ceilings, not agent baselines, and compare against validated LLM runs plus hidden holdout results.

Evidence:
- `outputs/founderbench-ablation-report.md`: present
- `outputs/founderbench-action-ablation.md`: present
- `outputs/founderbench-difficulty-calibration.md`: present
- `outputs/founderbench-task-provenance.md`: present

### license_metadata_missing

- Reviewer lens: reproducibility
- Severity: `administrative_major`
- Status: `owner_action_required`
- Status rationale: The submission gate still blocks on final license and citation metadata.
- Likely objection: The package is not publicly reusable until final LICENSE and citation metadata are chosen.
- Required response: The project owner must select and commit final license and citation metadata before public release or supplementary submission.

Evidence:
- `outputs/founderbench-license-readiness.md`: present
- `outputs/founderbench-release-metadata-checklist.md`: present
- `outputs/founderbench-submission-gate.md`: present

### provider_cost_reproducibility

- Reviewer lens: reproducibility
- Severity: `major`
- Status: `planned_not_executed`
- Status rationale: Cost and provider protocols exist; actual hosted/local runs must fill usage and cost fields.
- Likely objection: Hosted API results may be hard to reproduce without exact usage, retries, prices, and provider-error accounting.
- Required response: Record token usage, provider error categories, retry policy, model identifiers, and normalized costs for each validated provider run.

Evidence:
- `outputs/founderbench-cost-accounting.md`: present
- `outputs/founderbench-provider-readiness.md`: present
- `outputs/founderbench-prompt-protocol.md`: present
- `outputs/founderbench-provider-contract-audit.md`: present
- `outputs/founderbench-provider-run-status.md`: present

### human_calibration_missing

- Reviewer lens: domain
- Severity: `major`
- Status: `open_external`
- Status rationale: Calibration protocol and analyzer exist, but the analysis records no included submissions.
- Likely objection: The benchmark has no included human-founder or expert calibration results showing task realism, score alignment, or gaming risks.
- Required response: Collect calibration submissions, run the analyzer, and report inter-rater concerns and task revisions before strong validity claims.

Evidence:
- `outputs/founderbench-human-calibration-protocol.md`: present
- `outputs/founderbench-human-calibration-schema.md`: present
- `outputs/founderbench-human-calibration-analysis.md`: present
- `outputs/founderbench-human-calibration-packet.md`: present
- `outputs/founderbench-validity-report.md`: present

## Validation

Status: PASS

The reviewer-risk audit is internally consistent with the current submission gate and evidence state.
