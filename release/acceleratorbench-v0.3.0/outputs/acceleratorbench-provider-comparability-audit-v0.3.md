# FounderBench v0.3 Provider Comparability Audit

Provider-run comparability audit for planned and completed hosted/local model baselines.

Status: `protocol_comparability_ready_runs_missing`

## Scope

| Field | Value |
| --- | --- |
| task_count | 50 |
| prompt_version | founderbench-task-agent-v0.3 |
| prompt_template_sha256 | 9b9e911514c279ee76aa7b1fc88c6d014f134482031de30516146d22c9bbc5fd |
| protocol_sha256 | 938e4e2edf216bed42a965deb72c5b09e3083de233bb057159bfa5cbd941e9f4 |
| max_actions_per_week | 4 |
| minimum_repeats_for_stochastic_claims | 3 |
| cost_usage_fields | ['provider_prompt_tokens', 'provider_completion_tokens', 'provider_total_tokens', 'estimated_provider_cost_usd'] |

## Comparability Checks

- Every planned provider/local run targets the same 50 v0.3.0 task ids.
- Every provider uses the canonical structured-action prompt contract and parser.
- Every planned run has a submission validation command and repeat-bundle command.
- DeepSeek self-consistency k=3 is marked as a separate ablation, not a substitute for the naive baseline.
- Cost comparison remains unavailable unless usage metadata and evaluator price assumptions are both recorded.
- Provider rows remain excluded from model-performance claims until raw outputs and validation reports exist.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 5 |
| main_claim_comparable_required_runs | 4 |
| self_consistency_ablations | 1 |
| valid_run_outputs | 0 |
| required_missing_or_invalid | 4 |
| claim_status_counts | {'eligible_after_valid_submission': 4, 'excluded_or_ablation_until_separately_reported': 1} |
| ready_for_hosted_llm_comparison | False |

## Run Rows

| ID | Policy | Family | Priority | Current Status | Tasks | Temp | SC k | Role | Main Comparable | Claim Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek_single | deepseek | hosted | required | missing | 50 | 0.2 | 1 | primary_or_local_baseline | True | eligible_after_valid_submission |
| deepseek_sc_k3 | deepseek_sc | hosted | recommended | missing | 50 | 0.7 | 3 | self_consistency_ablation | False | excluded_or_ablation_until_separately_reported |
| anthropic_single | anthropic | hosted | required | missing | 50 | 0.2 | 1 | primary_or_local_baseline | True | eligible_after_valid_submission |
| gemini_single | gemini | hosted | required | missing | 50 | 0.2 | 1 | primary_or_local_baseline | True | eligible_after_valid_submission |
| local_open_model_single | llm | local_open_source | required | missing | 50 | 0.2 | 1 | primary_or_local_baseline | True | eligible_after_valid_submission |

## Claim Guardrails

- This audit establishes protocol comparability, not completed hosted/local model evidence.
- Single-run provider results are preliminary unless the statistical protocol and repeated-run policy allow stronger wording.
- DeepSeek self-consistency k=3 is an ablation row and must not replace the naive DeepSeek baseline.
- Missing or invalid provider outputs remain excluded from model-performance claims.

## Validation

Status: PASS

The planned provider/local run protocol is comparable, while missing outputs remain excluded from model-performance claims.
