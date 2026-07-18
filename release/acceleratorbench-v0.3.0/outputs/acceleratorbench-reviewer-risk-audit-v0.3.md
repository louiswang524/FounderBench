# FounderBench v0.3 Reviewer-Risk Audit

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
- `outputs/acceleratorbench-experiment-matrix-v0.3.md`: present
- `outputs/acceleratorbench-provider-run-status-v0.3.md`: present
- `outputs/acceleratorbench-experiment-runbook-v0.3.md`: present
- `outputs/acceleratorbench-model-comparison-v0.3.md`: present

### synthetic_validity

- Reviewer lens: domain
- Severity: `major`
- Status: `mitigated_not_closed`
- Status rationale: Threats and task provenance are documented, but external calibration remains missing.
- Likely objection: A synthetic startup simulator may not measure real startup skill or real company outcomes.
- Required response: Frame the benchmark as a controlled decision benchmark, avoid real-world success claims, and collect expert/human-founder calibration evidence.

Evidence:
- `outputs/acceleratorbench-validity-report-v0.3.md`: present
- `outputs/acceleratorbench-task-provenance-v0.3.md`: present
- `outputs/acceleratorbench-benchmark-card.md`: present
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`: present

### overclaiming_real_world_success

- Reviewer lens: editorial
- Severity: `critical`
- Status: `mitigated_by_claim_guardrail`
- Status rationale: Claim-evidence and paper-evidence artifacts explicitly exclude real-world success prediction.
- Likely objection: The paper could overstate that high simulator profit predicts real startup profitability or durable company success.
- Required response: Keep the supported wording narrow: FounderBench evaluates controlled startup-like operating decisions, not real-world startup prediction.

Evidence:
- `outputs/acceleratorbench-claim-evidence-v0.3.md`: present
- `outputs/acceleratorbench-paper-evidence-map-v0.3.md`: present
- `outputs/acceleratorbench-submission-manifest-v0.3.md`: present

### hidden_holdout_not_executed

- Reviewer lens: anti_gaming
- Severity: `major`
- Status: `open_external`
- Status rationale: The private-holdout protocol and smoke report exist, but no evaluator-hosted official aggregate result is included.
- Likely objection: Public tasks and deterministic scoring can invite benchmark gaming without an executed private holdout.
- Required response: Have an evaluator run secret-seeded private tasks and report aggregate-only holdout results for submitted models.

Evidence:
- `outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md`: present
- `outputs/acceleratorbench-private-holdout-smoke-v0.3.md`: present
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`: present
- `work/moneybench/moneybench/private_holdout_evaluator.py`: present
- `outputs/acceleratorbench-submission-gate-v0.3.md`: present

### heuristic_overfitting_or_hand_coding

- Reviewer lens: methodology
- Severity: `major`
- Status: `partially_mitigated`
- Status rationale: Ablations and task provenance expose heuristic behavior, but LLM and holdout evidence are still needed.
- Likely objection: Strong task-aware heuristics may encode benchmark-specific rules, making them look better than naive LLM calls.
- Required response: Report task-aware heuristic results as calibration ceilings, not agent baselines, and compare against validated LLM runs plus hidden holdout results.

Evidence:
- `outputs/acceleratorbench-ablation-report-v0.3.md`: present
- `outputs/acceleratorbench-action-ablation-v0.3.md`: present
- `outputs/acceleratorbench-difficulty-calibration-v0.3.md`: present
- `outputs/acceleratorbench-task-provenance-v0.3.md`: present

### license_metadata_missing

- Reviewer lens: reproducibility
- Severity: `administrative_major`
- Status: `owner_action_required`
- Status rationale: The submission gate still blocks on final license and citation metadata.
- Likely objection: The package is not publicly reusable until final LICENSE and citation metadata are chosen.
- Required response: The project owner must select and commit final license and citation metadata before public release or supplementary submission.

Evidence:
- `outputs/acceleratorbench-license-readiness-v0.3.md`: present
- `outputs/acceleratorbench-release-metadata-checklist-v0.3.md`: present
- `outputs/acceleratorbench-submission-gate-v0.3.md`: present

### provider_cost_reproducibility

- Reviewer lens: reproducibility
- Severity: `major`
- Status: `planned_not_executed`
- Status rationale: Cost and provider protocols exist; actual hosted/local runs must fill usage and cost fields.
- Likely objection: Hosted API results may be hard to reproduce without exact usage, retries, prices, and provider-error accounting.
- Required response: Record token usage, provider error categories, retry policy, model identifiers, and normalized costs for each validated provider run.

Evidence:
- `outputs/acceleratorbench-cost-accounting-v0.3.md`: present
- `outputs/acceleratorbench-provider-readiness-v0.3.md`: present
- `outputs/acceleratorbench-prompt-protocol-v0.3.md`: present
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md`: present
- `outputs/acceleratorbench-provider-run-status-v0.3.md`: present

### human_calibration_missing

- Reviewer lens: domain
- Severity: `major`
- Status: `open_external`
- Status rationale: Calibration protocol and analyzer exist, but the analysis records no included submissions.
- Likely objection: The benchmark has no included human-founder or expert calibration results showing task realism, score alignment, or gaming risks.
- Required response: Collect calibration submissions, run the analyzer, and report inter-rater concerns and task revisions before strong validity claims.

Evidence:
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-schema-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-analysis-v0.3.md`: present
- `outputs/acceleratorbench-human-calibration-packet-v0.3.md`: present
- `outputs/acceleratorbench-validity-report-v0.3.md`: present

## Validation

Status: PASS

The reviewer-risk audit is internally consistent with the current submission gate and evidence state.
