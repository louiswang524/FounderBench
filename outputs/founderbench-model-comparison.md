# FounderBench Model Comparison Report

Unified model-comparison report that includes deterministic baselines and automatically incorporates hosted/local provider runs only after submission validation passes.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_runs | 4 |
| valid_provider_runs | 3 |
| valid_provider_policies | 3 |
| valid_repeated_provider_bundles | 0 |
| provider_candidates | 11 |
| provider_missing_or_invalid | 8 |
| all_valid_runs | 7 |
| paired_comparisons | 6 |
| provider_paired_comparisons | 3 |
| hosted_llm_claims_ready | True |
| open_source_claim_ready | False |

## Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| anthropic | 50 | 24 | 0.48 | 61.09 | 62.09 | 59.58 | 0 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| deepseek | 50 | 23 | 0.46 | 56.59 | 54.51 | 59.70 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| gemini | 50 | 13 | 0.26 | 52.69 | 53.99 | 50.75 | 0 | 340 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Confidence Intervals

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| anthropic | 61.09 | [52.24, 69.79] | 0.48 | [0.34, 0.62] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| deepseek | 56.59 | [47.39, 65.78] | 0.46 | [0.32, 0.60] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| gemini | 52.69 | [46.10, 59.68] | 0.26 | [0.14, 0.40] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Paired Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Permutation p | Cohen dz | Score W/L/T |
| --- | --- | --- | --- | --- | --- | --- |
| task_heuristic - anthropic | 50 | 19.82 | [12.42, 27.55] | 5e-05 | 0.7105 | 38/11/1 |
| task_heuristic - heuristic | 50 | 19.9 | [13.8, 26.19] | 5e-05 | 0.8848 | 42/8/0 |
| task_heuristic - deepseek | 50 | 24.32 | [16.35, 32.67] | 5e-05 | 0.8294 | 42/7/1 |
| task_heuristic - conservative | 50 | 26.87 | [21.67, 32.45] | 5e-05 | 1.3433 | 43/7/0 |
| task_heuristic - gemini | 50 | 28.21 | [20.83, 35.09] | 5e-05 | 1.0672 | 43/5/2 |
| task_heuristic - random | 50 | 47.61 | [40.24, 54.64] | 5e-05 | 1.892 | 49/1/0 |

## Provider Paired Comparisons

| Comparison | Tasks | Mean Gap | Bootstrap 95% CI | Permutation p | Cohen dz |
| --- | --- | --- | --- | --- | --- |
| task_heuristic - anthropic | 50 | 19.82 | [12.42, 27.55] | 5e-05 | 0.7105 |
| task_heuristic - deepseek | 50 | 24.32 | [16.35, 32.67] | 5e-05 | 0.8294 |
| task_heuristic - gemini | 50 | 28.21 | [20.83, 35.09] | 5e-05 | 1.0672 |

## Family Breakdown

Each cell reports `solved/5 (average score)`.

| Family | task_heuristic | anthropic | heuristic | deepseek | conservative | gemini | random |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Market selection | 2/5 (59.8) | 2/5 (47.4) | 2/5 (61.1) | 3/5 (57.4) | 2/5 (63.2) | 2/5 (47.3) | 0/5 (31.6) |
| First revenue | 2/5 (69.2) | 1/5 (29.6) | 2/5 (65.7) | 0/5 (10.7) | 1/5 (45.3) | 1/5 (61.1) | 0/5 (20.4) |
| Retention improvement | 5/5 (95.8) | 5/5 (94.7) | 2/5 (63.5) | 5/5 (93.5) | 0/5 (47.5) | 3/5 (70.8) | 0/5 (10.4) |
| Churn shock recovery | 5/5 (91.2) | 2/5 (67.3) | 1/5 (48.1) | 1/5 (39.3) | 0/5 (38.3) | 0/5 (37.4) | 0/5 (34.3) |
| Demo Day traction | 4/5 (88.8) | 1/5 (68.0) | 3/5 (67.0) | 1/5 (57.0) | 2/5 (60.3) | 2/5 (58.4) | 0/5 (20.2) |
| Pricing | 5/5 (85.6) | 1/5 (65.7) | 4/5 (85.2) | 2/5 (69.2) | 3/5 (77.3) | 0/5 (48.9) | 0/5 (39.7) |
| Runway preservation | 5/5 (95.6) | 5/5 (90.8) | 5/5 (82.5) | 5/5 (91.1) | 5/5 (79.1) | 5/5 (77.9) | 2/5 (68.3) |
| Pivot decision | 2/5 (65.5) | 0/5 (12.8) | 0/5 (26.8) | 0/5 (12.6) | 0/5 (23.9) | 0/5 (21.8) | 0/5 (11.7) |
| Fundraising | 5/5 (99.6) | 5/5 (83.6) | 0/5 (68.0) | 5/5 (86.3) | 0/5 (68.0) | 0/5 (68.0) | 2/5 (72.6) |
| Channel expansion | 2/5 (58.0) | 2/5 (51.1) | 0/5 (42.1) | 1/5 (48.8) | 0/5 (37.6) | 0/5 (35.3) | 0/5 (23.7) |

## Provider Evidence Ledger

| ID | Policy | Family | Status | Runs | Evidence | Avg Score | Solve Rate | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_hosted_baseline | openai | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-openai.json or outputs/founderbench-openai-repeats.json |
| deepseek_hosted_baseline | deepseek | hosted_llm | valid | 1 | single_run | 56.59 | 0.46 |  |
| anthropic_hosted_baseline | anthropic | hosted_llm | valid | 1 | single_run | 61.09 | 0.48 |  |
| gemini_hosted_baseline | gemini | hosted_llm | valid | 1 | single_run | 52.69 | 0.26 |  |
| kimi_hosted_baseline | kimi | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-kimi.json or outputs/founderbench-kimi-repeats.json |
| qwen_hosted_baseline | qwen | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_hosted_baseline | mistral | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_hosted_baseline | glm | hosted_llm_optional | invalid | 0 |  |  |  | outputs/founderbench-glm.json: Missing validation report outputs/founderbench-glm-submission-report.md |
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
