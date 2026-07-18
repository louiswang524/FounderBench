# FounderBench Model Comparison Report

Unified model-comparison report that includes deterministic baselines and automatically incorporates hosted/local provider runs only after submission validation passes.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_runs | 4 |
| valid_provider_runs | 0 |
| valid_provider_policies | 0 |
| valid_repeated_provider_bundles | 0 |
| provider_candidates | 12 |
| provider_missing_or_invalid | 12 |
| all_valid_runs | 4 |
| paired_comparisons | 3 |
| provider_paired_comparisons | 0 |
| hosted_llm_claims_ready | False |
| open_source_claim_ready | False |

## Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Confidence Intervals

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Paired Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Permutation p | Cohen dz | Score W/L/T |
| --- | --- | --- | --- | --- | --- | --- |
| task_heuristic - heuristic | 50 | 19.9 | [13.8, 26.19] | 5e-05 | 0.8848 | 42/8/0 |
| task_heuristic - conservative | 50 | 26.87 | [21.67, 32.45] | 5e-05 | 1.3433 | 43/7/0 |
| task_heuristic - random | 50 | 47.61 | [40.24, 54.64] | 5e-05 | 1.892 | 49/1/0 |

## Provider Paired Comparisons

No provider paired comparisons are available yet because no hosted/local provider run currently passes validation.

## Family Breakdown

Each cell reports `solved/5 (average score)`.

| Family | task_heuristic | heuristic | conservative | random |
| --- | --- | --- | --- | --- |
| Market selection | 2/5 (59.8) | 2/5 (61.1) | 2/5 (63.2) | 0/5 (31.6) |
| First revenue | 2/5 (69.2) | 2/5 (65.7) | 1/5 (45.3) | 0/5 (20.4) |
| Retention improvement | 5/5 (95.8) | 2/5 (63.5) | 0/5 (47.5) | 0/5 (10.4) |
| Churn shock recovery | 5/5 (91.2) | 1/5 (48.1) | 0/5 (38.3) | 0/5 (34.3) |
| Demo Day traction | 4/5 (88.8) | 3/5 (67.0) | 2/5 (60.3) | 0/5 (20.2) |
| Pricing | 5/5 (85.6) | 4/5 (85.2) | 3/5 (77.3) | 0/5 (39.7) |
| Runway preservation | 5/5 (95.6) | 5/5 (82.5) | 5/5 (79.1) | 2/5 (68.3) |
| Pivot decision | 2/5 (65.5) | 0/5 (26.8) | 0/5 (23.9) | 0/5 (11.7) |
| Fundraising | 5/5 (99.6) | 0/5 (68.0) | 0/5 (68.0) | 2/5 (72.6) |
| Channel expansion | 2/5 (58.0) | 0/5 (42.1) | 0/5 (37.6) | 0/5 (23.7) |

## Provider Evidence Ledger

| ID | Policy | Family | Status | Runs | Evidence | Avg Score | Solve Rate | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_hosted_baseline | openai | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-openai.json or outputs/founderbench-openai-repeats.json |
| deepseek_hosted_baseline | deepseek | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-deepseek.json or outputs/founderbench-deepseek-repeats.json |
| deepseek_self_consistency_k3 | deepseek_sc | hosted_llm_ablation | missing | 0 |  |  |  | Missing outputs/founderbench-deepseek-sc-k3.json or outputs/founderbench-deepseek-sc-k3-repeats.json |
| anthropic_hosted_baseline | anthropic | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-anthropic.json or outputs/founderbench-anthropic-repeats.json |
| gemini_hosted_baseline | gemini | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-gemini.json or outputs/founderbench-gemini-repeats.json |
| kimi_hosted_baseline | kimi | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-kimi.json or outputs/founderbench-kimi-repeats.json |
| qwen_hosted_baseline | qwen | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_hosted_baseline | mistral | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_hosted_baseline | glm | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-glm.json or outputs/founderbench-glm-repeats.json |
| xai_hosted_baseline | xai | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-xai.json or outputs/founderbench-xai-repeats.json |
| llama_open_weight_baseline | llama | open_weight | missing | 0 |  |  |  | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_source_baseline | llm | open_source | missing | 0 |  |  |  | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

## Claim Rules

- Provider rows are included only after raw run validation passes.
- Hosted LLM comparison claims require at least three valid hosted provider baselines.
- Open-source comparison claims require at least one valid local/OpenAI-compatible run.
- Missing or invalid provider runs are reported in the ledger and excluded from leaderboard claims.

## Validation

Status: PASS

The report is internally consistent. Provider comparison sections remain empty until validated provider runs exist.
