# FounderBench Provider Comparability Audit

Provider-run comparability audit for planned and completed hosted/local model baselines.

Status: `protocol_comparability_ready_runs_missing`

## Scope

| Field | Value |
| --- | --- |
| task_count | 50 |
| prompt_version | founderbench-task-agent |
| prompt_template_sha256 | 21cfb19c6ce46b4f74d6d92dc994fca10237b86e166e5b886b5220bb4da15e8b |
| protocol_sha256 | 67b5335c955d256ed530cb39928eef1c583a78604cbcfa906c97d1f05ea2cae5 |
| max_actions_per_week | 4 |
| minimum_repeats_for_stochastic_claims | 3 |
| cost_usage_fields | ['provider_prompt_tokens', 'provider_completion_tokens', 'provider_total_tokens', 'estimated_provider_cost_usd'] |

## Comparability Checks

- Every planned provider/local run targets the same 50 current task ids.
- Every provider uses the canonical structured-action prompt contract and parser.
- Every planned run has a submission validation command and repeat-bundle command.
- Cost comparison remains unavailable unless usage metadata and evaluator price assumptions are both recorded.
- Provider rows remain excluded from model-performance claims until raw outputs and validation reports exist.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 11 |
| main_claim_comparable_required_runs | 7 |
| valid_run_outputs | 0 |
| required_missing_or_invalid | 7 |
| claim_status_counts | {'eligible_after_valid_submission': 7, 'excluded_or_ablation_until_separately_reported': 4} |
| ready_for_hosted_llm_comparison | False |

## Run Rows

| ID | Policy | Family | Priority | Current Status | Tasks | Temp | Role | Main Comparable | Claim Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_single | openai | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| deepseek_single | deepseek | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| anthropic_single | anthropic | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| gemini_single | gemini | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| kimi_single | kimi | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| qwen_single | qwen | hosted | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |
| mistral_single | mistral | hosted | recommended | missing | 50 | 0.2 | primary_or_local_baseline | False | excluded_or_ablation_until_separately_reported |
| glm_single | glm | hosted | recommended | missing | 50 | 0.2 | primary_or_local_baseline | False | excluded_or_ablation_until_separately_reported |
| xai_single | xai | hosted | recommended | missing | 50 | 0.2 | primary_or_local_baseline | False | excluded_or_ablation_until_separately_reported |
| llama_endpoint_single | llama | local_open_source | recommended | missing | 50 | 0.2 | primary_or_local_baseline | False | excluded_or_ablation_until_separately_reported |
| local_open_model_single | llm | local_open_source | required | missing | 50 | 0.2 | primary_or_local_baseline | True | eligible_after_valid_submission |

## Claim Guardrails

- This audit establishes protocol comparability, not completed hosted/local model evidence.
- Single-run provider results are preliminary unless the statistical protocol and repeated-run policy allow stronger wording.
- Missing or invalid provider outputs remain excluded from model-performance claims.

## Validation

Status: PASS

The planned provider/local run protocol is comparable, while missing outputs remain excluded from model-performance claims.
