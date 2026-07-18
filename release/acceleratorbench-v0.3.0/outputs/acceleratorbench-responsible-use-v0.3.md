# FounderBench v0.3 Responsible Use Statement

Responsible-use, ethics, and disclosure statement for FounderBench v0.3.0.

## Summary

| Metric | Value |
| --- | --- |
| intended_uses | 4 |
| unsupported_uses | 5 |
| data_privacy_topics | 4 |
| required_submission_disclosures | 7 |
| residual_risks | 5 |
| contains_real_company_data | False |
| contains_human_subject_data | False |
| permits_real_world_startup_success_claims | False |

## Intended Uses

- Evaluate structured decision-making behavior of startup-operator agents in a synthetic, controlled simulator.
- Compare models or agent policies only through validated task-level submissions and clearly labeled public/repeated/private result tiers.
- Study failure modes such as malformed actions, over-budget decisions, brittle planning, poor runway management, and prompt sensitivity.
- Support benchmark-methodology research on agent evaluation, not deployment claims about autonomous companies.

## Unsupported Uses

- Do not use FounderBench scores as evidence that a model can run a real company or predict real startup success.
- Do not use the benchmark as business, investment, hiring, lending, legal, tax, or financial advice.
- Do not report public-test performance as hidden, private, contamination-free, or robust to task-template gaming.
- Do not rank provider submissions that are missing, manually repaired outside the parser contract, or missing required diagnostics.
- Do not use generated agent rationales as executable business recommendations; only structured simulator actions are evaluated.

## Data and Privacy

| Topic | Statement |
| --- | --- |
| Synthetic tasks | v0.3.0 task definitions are synthetic and do not contain real company records, private founder data, customer data, or human-subject measurements. |
| Provider submissions | Hosted/local model submissions may contain provider responses, latency, token usage, and cost metadata; public audit traces must be redacted before release. |
| Human calibration | The included calibration packet is non-executed. Any future expert or founder study should collect consent, avoid confidential company data, and report aggregate findings. |
| Private holdout | Private task definitions should remain evaluator-controlled; public reports should expose aggregate scores and diagnostics only. |

## Required Submission Disclosures

- model/provider name, version, and access date when applicable
- prompt/protocol version and prompt hashes
- decoding settings, self-consistency/reflection policy, and run_seed identities
- adapter/parser version and whether any output was manually repaired
- provider-error categories, invalid-action counts, timeout handling, and omitted-task status
- token usage, latency, estimated cost, and redaction status of any released audit traces
- whether the submitted model or prompt was trained, tuned, or optimized on released public tasks

## Residual Risks

| Risk | Mitigation | Status |
| --- | --- | --- |
| Benchmark gaming | Keep public/private tiers separate, execute private holdout externally, and require disclosure of public-task tuning. | partially_mitigated_private_execution_missing |
| Overclaiming economic competence | Use claim-evidence, validity, and responsible-use language to restrict claims to controlled simulator decisions. | mitigated_for_current_claims |
| Provider privacy or secret leakage | Use environment variables, redacted audit logs, secret scans, and provider-run reports that omit raw keys. | mitigated_by_process |
| Human calibration confidentiality | Use synthetic tasks, consent language, and aggregate reporting if expert/founder calibration is executed. | planned_not_executed |
| Cost and environmental burden | Report token/cost accounting, support resumable runs, and separate repeated-run ablations from required single-run baselines. | mitigated_not_closed_until_provider_runs |

## Validation

Status: PASS

The statement keeps intended use, unsupported use, privacy, disclosure, and residual-risk boundaries explicit.
