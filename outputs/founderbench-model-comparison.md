# FounderBench Model Comparison Report

Unified model-comparison report that includes deterministic baselines and automatically incorporates hosted/local provider runs only after submission validation passes.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_runs | 4 |
| valid_provider_runs | 11 |
| valid_provider_policies | 7 |
| valid_provider_models | 11 |
| valid_repeated_provider_bundles | 0 |
| provider_candidates | 15 |
| provider_missing_or_invalid | 4 |
| all_valid_runs | 15 |
| paired_comparisons | 14 |
| provider_paired_comparisons | 11 |
| hosted_llm_claims_ready | True |
| open_source_claim_ready | False |

## Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| Gemini 3.5 Flash | 50 | 32 | 0.64 | 67.69 | 73.05 | 59.64 | 0 | 59 |
| Grok 4.5 | 50 | 33 | 0.66 | 66.53 | 73.16 | 56.57 | 0 | 0 |
| GPT-5.6 Sol | 50 | 32 | 0.64 | 66.39 | 71.70 | 58.42 | 0 | 0 |
| Kimi K3 | 50 | 28 | 0.56 | 65.63 | 70.12 | 58.90 | 0 | 70 |
| Claude Sonnet 5 | 50 | 25 | 0.50 | 63.90 | 60.76 | 68.61 | 0 | 0 |
| DeepSeek V4 Reasoner | 50 | 27 | 0.54 | 62.43 | 65.38 | 58.02 | 0 | 3 |
| Claude Sonnet 4.5 | 50 | 24 | 0.48 | 61.09 | 62.09 | 59.58 | 0 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| DeepSeek Chat | 50 | 23 | 0.46 | 56.59 | 54.51 | 59.70 | 0 | 0 |
| GLM 4.5 Air | 50 | 23 | 0.46 | 54.78 | 53.83 | 56.20 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| Gemini 2.5 Flash | 50 | 13 | 0.26 | 52.69 | 53.99 | 50.75 | 0 | 340 |
| Grok 4.3 | 50 | 16 | 0.32 | 52.59 | 48.03 | 59.43 | 0 | 3 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Confidence Intervals

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| Gemini 3.5 Flash | 67.69 | [59.20, 75.25] | 0.64 | [0.50, 0.76] |
| Grok 4.5 | 66.53 | [57.81, 74.62] | 0.66 | [0.52, 0.78] |
| GPT-5.6 Sol | 66.39 | [57.46, 74.89] | 0.64 | [0.50, 0.76] |
| Kimi K3 | 65.63 | [57.89, 72.67] | 0.56 | [0.42, 0.70] |
| Claude Sonnet 5 | 63.90 | [56.34, 71.41] | 0.50 | [0.36, 0.64] |
| DeepSeek V4 Reasoner | 62.43 | [53.97, 70.48] | 0.54 | [0.40, 0.68] |
| Claude Sonnet 4.5 | 61.09 | [52.24, 69.79] | 0.48 | [0.34, 0.62] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| DeepSeek Chat | 56.59 | [47.39, 65.78] | 0.46 | [0.32, 0.60] |
| GLM 4.5 Air | 54.78 | [46.01, 63.53] | 0.46 | [0.32, 0.60] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| Gemini 2.5 Flash | 52.69 | [46.10, 59.68] | 0.26 | [0.14, 0.40] |
| Grok 4.3 | 52.59 | [45.16, 60.21] | 0.32 | [0.20, 0.46] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Paired Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Permutation p | Cohen dz | Score W/L/T |
| --- | --- | --- | --- | --- | --- | --- |
| task_heuristic - Gemini 3.5 Flash | 50 | 13.22 | [6.07, 20.93] | 0.0008 | 0.4806 | 36/9/5 |
| task_heuristic - Grok 4.5 | 50 | 14.38 | [8.53, 20.75] | 5e-05 | 0.6426 | 34/9/7 |
| task_heuristic - GPT-5.6 Sol | 50 | 14.52 | [6.93, 22.44] | 0.00055 | 0.5234 | 34/10/6 |
| task_heuristic - Kimi K3 | 50 | 15.27 | [8.6, 22.12] | 0.00015 | 0.6305 | 37/9/4 |
| task_heuristic - Claude Sonnet 5 | 50 | 17.0 | [10.56, 24.23] | 5e-05 | 0.7093 | 38/9/3 |
| task_heuristic - DeepSeek V4 Reasoner | 50 | 18.47 | [11.85, 25.49] | 5e-05 | 0.7208 | 41/7/2 |
| task_heuristic - Claude Sonnet 4.5 | 50 | 19.82 | [12.59, 27.79] | 5e-05 | 0.7105 | 38/11/1 |
| task_heuristic - heuristic | 50 | 19.9 | [13.8, 26.19] | 5e-05 | 0.8848 | 42/8/0 |
| task_heuristic - DeepSeek Chat | 50 | 24.32 | [15.98, 32.44] | 5e-05 | 0.8294 | 42/7/1 |
| task_heuristic - GLM 4.5 Air | 50 | 26.12 | [19.7, 32.83] | 5e-05 | 1.086 | 45/4/1 |
| task_heuristic - conservative | 50 | 26.87 | [21.67, 32.45] | 5e-05 | 1.3433 | 43/7/0 |
| task_heuristic - Gemini 2.5 Flash | 50 | 28.21 | [20.81, 35.1] | 5e-05 | 1.0672 | 43/5/2 |
| task_heuristic - Grok 4.3 | 50 | 28.32 | [21.32, 35.05] | 5e-05 | 1.1003 | 49/1/0 |
| task_heuristic - random | 50 | 47.61 | [40.24, 54.64] | 5e-05 | 1.892 | 49/1/0 |

## Provider Paired Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Permutation p | Cohen dz |
| --- | --- | --- | --- | --- | --- |
| task_heuristic - Gemini 3.5 Flash | 50 | 13.22 | [6.07, 20.93] | 0.0008 | 0.4806 |
| task_heuristic - Grok 4.5 | 50 | 14.38 | [8.53, 20.75] | 5e-05 | 0.6426 |
| task_heuristic - GPT-5.6 Sol | 50 | 14.52 | [6.93, 22.44] | 0.00055 | 0.5234 |
| task_heuristic - Kimi K3 | 50 | 15.27 | [8.6, 22.12] | 0.00015 | 0.6305 |
| task_heuristic - Claude Sonnet 5 | 50 | 17.0 | [10.56, 24.23] | 5e-05 | 0.7093 |
| task_heuristic - DeepSeek V4 Reasoner | 50 | 18.47 | [11.85, 25.49] | 5e-05 | 0.7208 |
| task_heuristic - Claude Sonnet 4.5 | 50 | 19.82 | [12.59, 27.79] | 5e-05 | 0.7105 |
| task_heuristic - DeepSeek Chat | 50 | 24.32 | [15.98, 32.44] | 5e-05 | 0.8294 |
| task_heuristic - GLM 4.5 Air | 50 | 26.12 | [19.7, 32.83] | 5e-05 | 1.086 |
| task_heuristic - Gemini 2.5 Flash | 50 | 28.21 | [20.81, 35.1] | 5e-05 | 1.0672 |
| task_heuristic - Grok 4.3 | 50 | 28.32 | [21.32, 35.05] | 5e-05 | 1.1003 |

## Family Breakdown

Each cell reports `solved/5 (average score)`.

| Family | task_heuristic | Gemini 3.5 Flash | Grok 4.5 | GPT-5.6 Sol | Kimi K3 | Claude Sonnet 5 | DeepSeek V4 Reasoner | Claude Sonnet 4.5 | heuristic | DeepSeek Chat | GLM 4.5 Air | conservative | Gemini 2.5 Flash | Grok 4.3 | random |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Market selection | 2/5 (59.8) | 3/5 (58.9) | 2/5 (46.3) | 3/5 (59.4) | 3/5 (59.3) | 1/5 (36.3) | 3/5 (59.0) | 2/5 (47.4) | 2/5 (61.1) | 3/5 (57.4) | 0/5 (25.1) | 2/5 (63.2) | 2/5 (47.3) | 2/5 (57.1) | 0/5 (31.6) |
| First revenue | 2/5 (69.2) | 3/5 (54.8) | 3/5 (60.0) | 2/5 (53.6) | 0/5 (34.8) | 2/5 (68.9) | 2/5 (50.7) | 1/5 (29.6) | 2/5 (65.7) | 0/5 (10.7) | 0/5 (10.0) | 1/5 (45.3) | 1/5 (61.1) | 0/5 (22.1) | 0/5 (20.4) |
| Retention improvement | 5/5 (95.8) | 5/5 (95.7) | 5/5 (96.7) | 5/5 (96.2) | 5/5 (95.5) | 5/5 (94.3) | 5/5 (91.6) | 5/5 (94.7) | 2/5 (63.5) | 5/5 (93.5) | 5/5 (90.2) | 0/5 (47.5) | 3/5 (70.8) | 0/5 (41.1) | 0/5 (10.4) |
| Churn shock recovery | 5/5 (91.2) | 5/5 (91.6) | 5/5 (94.4) | 5/5 (95.2) | 5/5 (93.8) | 0/5 (53.5) | 4/5 (79.0) | 2/5 (67.3) | 1/5 (48.1) | 1/5 (39.3) | 4/5 (74.6) | 0/5 (38.3) | 0/5 (37.4) | 0/5 (54.0) | 0/5 (34.3) |
| Demo Day traction | 4/5 (88.8) | 0/5 (61.3) | 3/5 (67.5) | 1/5 (51.6) | 2/5 (63.9) | 1/5 (35.6) | 1/5 (41.0) | 1/5 (68.0) | 3/5 (67.0) | 1/5 (57.0) | 1/5 (51.6) | 2/5 (60.3) | 2/5 (58.4) | 1/5 (47.1) | 0/5 (20.2) |
| Pricing | 5/5 (85.6) | 4/5 (76.1) | 4/5 (74.1) | 4/5 (74.2) | 4/5 (73.4) | 3/5 (75.9) | 2/5 (71.0) | 1/5 (65.7) | 4/5 (85.2) | 2/5 (69.2) | 4/5 (71.4) | 3/5 (77.3) | 0/5 (48.9) | 2/5 (66.8) | 0/5 (39.7) |
| Runway preservation | 5/5 (95.6) | 5/5 (84.0) | 4/5 (81.4) | 5/5 (87.2) | 5/5 (84.3) | 5/5 (87.5) | 5/5 (90.6) | 5/5 (90.8) | 5/5 (82.5) | 5/5 (91.1) | 4/5 (87.5) | 5/5 (79.1) | 5/5 (77.9) | 5/5 (94.4) | 2/5 (68.3) |
| Pivot decision | 2/5 (65.5) | 0/5 (17.9) | 0/5 (13.7) | 0/5 (5.3) | 0/5 (31.5) | 1/5 (47.1) | 0/5 (17.8) | 0/5 (12.8) | 0/5 (26.8) | 0/5 (12.6) | 0/5 (10.8) | 0/5 (23.9) | 0/5 (21.8) | 0/5 (18.9) | 0/5 (11.7) |
| Fundraising | 5/5 (99.6) | 5/5 (83.6) | 5/5 (86.5) | 5/5 (83.4) | 4/5 (84.5) | 5/5 (83.2) | 5/5 (83.8) | 5/5 (83.6) | 0/5 (68.0) | 5/5 (86.3) | 5/5 (84.0) | 0/5 (68.0) | 0/5 (68.0) | 5/5 (83.5) | 2/5 (72.6) |
| Channel expansion | 2/5 (58.0) | 2/5 (53.0) | 2/5 (44.7) | 2/5 (57.8) | 0/5 (35.3) | 2/5 (56.7) | 0/5 (40.0) | 2/5 (51.1) | 0/5 (42.1) | 1/5 (48.8) | 0/5 (42.5) | 0/5 (37.6) | 0/5 (35.3) | 1/5 (41.0) | 0/5 (23.7) |

## Provider Evidence Ledger

| ID | Policy | Model | Family | Status | Runs | Evidence | Avg Score | Solve Rate | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_hosted_baseline | openai | GPT-5.6 Sol | hosted_llm | valid | 1 | single_run | 66.39 | 0.64 |  |
| deepseek_hosted_baseline | deepseek | DeepSeek Chat | hosted_llm | valid | 1 | single_run | 56.59 | 0.46 |  |
| deepseek_v4_reasoner_hosted_baseline | deepseek | DeepSeek V4 Reasoner | hosted_llm | valid | 1 | single_run | 62.43 | 0.54 |  |
| anthropic_hosted_baseline | anthropic | Claude Sonnet 4.5 | hosted_llm | valid | 1 | single_run | 61.09 | 0.48 |  |
| anthropic_sonnet_5_hosted_baseline | anthropic | Claude Sonnet 5 | hosted_llm | valid | 1 | single_run | 63.9 | 0.5 |  |
| gemini_hosted_baseline | gemini | Gemini 2.5 Flash | hosted_llm | valid | 1 | single_run | 52.69 | 0.26 |  |
| gemini_3_5_flash_hosted_baseline | gemini | Gemini 3.5 Flash | hosted_llm | valid | 1 | single_run | 67.69 | 0.64 |  |
| kimi_hosted_baseline | kimi | Kimi K3 | hosted_llm | valid | 1 | single_run | 65.63 | 0.56 |  |
| qwen_hosted_baseline | qwen | Qwen | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_hosted_baseline | mistral | Mistral | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_hosted_baseline | glm | GLM 4.5 Air | hosted_llm_optional | valid | 1 | single_run | 54.78 | 0.46 |  |
| xai_hosted_baseline | xai | Grok 4.5 | hosted_llm_optional | valid | 1 | single_run | 66.53 | 0.66 |  |
| xai_grok_4_3_hosted_baseline | xai | Grok 4.3 | hosted_llm_optional | valid | 1 | single_run | 52.59 | 0.32 |  |
| llama_open_weight_baseline | llama | Llama/Open-weight | open_weight | missing | 0 |  |  |  | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_source_baseline | llm | Local open-source model | open_source | missing | 0 |  |  |  | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

## Claim Rules

- Provider rows are included only after raw run validation passes.
- Hosted LLM comparison claims require at least three valid hosted provider baselines.
- Open-source comparison claims require at least one valid local/OpenAI-compatible run.
- Missing or invalid provider runs are reported in the ledger and excluded from leaderboard claims.

## Validation

Status: PASS

The report is internally consistent. Only validated provider evidence is included; missing or invalid candidates remain explicit in the status ledger.
