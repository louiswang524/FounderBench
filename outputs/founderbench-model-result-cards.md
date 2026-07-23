# FounderBench Model Result Cards

Reviewer-facing result cards for deterministic baselines and provider submissions. Cards summarize validity, task coverage, diagnostics, cost fields, and paper-claim eligibility.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_cards | 4 |
| provider_candidate_cards | 15 |
| valid_provider_cards | 11 |
| hosted_llm_claims_ready | True |
| open_source_claim_ready | False |

## Claim Guardrails

- Deterministic baseline cards are not hosted LLM evidence.
- Provider cards marked missing or invalid must be excluded from model-performance claims.
- Provider cards become paper-eligible only after the raw submission and validation report both exist and pass.
- Cost fields are reportable only when provider usage metadata and price assumptions are available.

## Deterministic Baseline Cards

| Policy | Status | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Provider Errors | Invalid Actions | Over-Budget | Provider Tokens | Cost USD | Claim Eligibility |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| random | valid | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 0 | 0 | 15 | 0 | 0.0000 | deterministic_baseline_claims_only |
| conservative | valid | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 | 0 | 0 | 0.0000 | deterministic_baseline_claims_only |
| heuristic | valid | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 | 0 | 0 | 0.0000 | deterministic_baseline_claims_only |
| task_heuristic | valid | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 0 | 0 | 5 | 0 | 0.0000 | deterministic_baseline_claims_only |

## Planned Provider Cards

| ID | Policy | Model | Family | Status | Runs | Evidence | Report | Repeat Report | Claim Eligibility | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_hosted_baseline | openai | GPT-5.6 Sol | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| deepseek_hosted_baseline | deepseek | DeepSeek Chat | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| deepseek_v4_reasoner_hosted_baseline | deepseek | DeepSeek V4 Reasoner | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| anthropic_hosted_baseline | anthropic | Claude Sonnet 4.5 | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| anthropic_sonnet_5_hosted_baseline | anthropic | Claude Sonnet 5 | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| gemini_hosted_baseline | gemini | Gemini 2.5 Flash | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| gemini_3_5_flash_hosted_baseline | gemini | Gemini 3.5 Flash | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| kimi_hosted_baseline | kimi | Kimi K3 | hosted_llm | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| qwen_hosted_baseline | qwen | Qwen | hosted_llm | missing | 0 |  | False | False | excluded_until_validated | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_hosted_baseline | mistral | Mistral | hosted_llm_optional | missing | 0 |  | False | False | excluded_until_validated | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_hosted_baseline | glm | GLM 4.5 Air | hosted_llm_optional | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| xai_hosted_baseline | xai | Grok 4.5 | hosted_llm_optional | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| xai_grok_4_3_hosted_baseline | xai | Grok 4.3 | hosted_llm_optional | valid | 1 | single_run | True | False | eligible_for_provider_tables |  |
| llama_open_weight_baseline | llama | Llama/Open-weight | open_weight | missing | 0 |  | False | False | excluded_until_validated | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_source_baseline | llm | Local open-source model | open_source | missing | 0 |  | False | False | excluded_until_validated | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

## Validation

Status: PASS

Result cards are internally consistent. Missing provider cards remain excluded from model-performance claims.
