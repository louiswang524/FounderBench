# FounderBench Paper Tables

These generated tables are intended for the paper results section. They are derived from raw current release run files; hosted/provider rows are included in the main tables only after submission validation passes.

## Summary

| Metric | Value |
| --- | --- |
| deterministic_runs | 4 |
| valid_provider_runs | 2 |
| provider_candidates | 11 |
| provider_missing_or_invalid | 9 |
| valid_provider_policies | 2 |
| valid_repeated_provider_bundles | 0 |

## Main Leaderboard

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget | Provider Errors |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 | 0 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 |
| deepseek | 50 | 23 | 0.46 | 56.59 | 54.51 | 59.70 | 0 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 |
| gemini | 50 | 13 | 0.26 | 52.69 | 53.99 | 50.75 | 0 | 340 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 | 0 |

## Confidence Intervals

| Policy | Avg Score | Score 95% CI | Solve Rate | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| task_heuristic | 80.90 | [74.94, 86.42] | 0.74 | [0.62, 0.86] |
| heuristic | 61.01 | [55.21, 66.94] | 0.38 | [0.26, 0.52] |
| deepseek | 56.59 | [47.39, 65.78] | 0.46 | [0.32, 0.60] |
| conservative | 54.04 | [48.20, 60.14] | 0.26 | [0.14, 0.38] |
| gemini | 52.69 | [46.10, 59.68] | 0.26 | [0.14, 0.40] |
| random | 33.30 | [26.89, 40.60] | 0.08 | [0.02, 0.16] |

## Pairwise Score Gaps

| Comparison | Mean Gap | 95% CI | Shared Tasks |
| --- | --- | --- | --- |
| task_heuristic - heuristic | 19.90 | [13.80, 26.19] | 50 |
| task_heuristic - deepseek | 24.32 | [16.35, 32.67] | 50 |
| task_heuristic - conservative | 26.87 | [21.67, 32.45] | 50 |
| task_heuristic - gemini | 28.21 | [20.83, 35.09] | 50 |
| task_heuristic - random | 47.61 | [40.24, 54.64] | 50 |

## Family Breakdown

Each cell reports `solved/5 (average score)`. Valid policies included: `task_heuristic`, `heuristic`, `deepseek`, `conservative`, `gemini`, `random`.

| Family | task_heuristic | heuristic | deepseek | conservative | gemini | random |
| --- | --- | --- | --- | --- | --- | --- |
| Market selection | 2/5 (59.8) | 2/5 (61.1) | 3/5 (57.4) | 2/5 (63.2) | 2/5 (47.3) | 0/5 (31.6) |
| First revenue | 2/5 (69.2) | 2/5 (65.7) | 0/5 (10.7) | 1/5 (45.3) | 1/5 (61.1) | 0/5 (20.4) |
| Retention improvement | 5/5 (95.8) | 2/5 (63.5) | 5/5 (93.5) | 0/5 (47.5) | 3/5 (70.8) | 0/5 (10.4) |
| Churn shock recovery | 5/5 (91.2) | 1/5 (48.1) | 1/5 (39.3) | 0/5 (38.3) | 0/5 (37.4) | 0/5 (34.3) |
| Demo Day traction | 4/5 (88.8) | 3/5 (67.0) | 1/5 (57.0) | 2/5 (60.3) | 2/5 (58.4) | 0/5 (20.2) |
| Pricing | 5/5 (85.6) | 4/5 (85.2) | 2/5 (69.2) | 3/5 (77.3) | 0/5 (48.9) | 0/5 (39.7) |
| Runway preservation | 5/5 (95.6) | 5/5 (82.5) | 5/5 (91.1) | 5/5 (79.1) | 5/5 (77.9) | 2/5 (68.3) |
| Pivot decision | 2/5 (65.5) | 0/5 (26.8) | 0/5 (12.6) | 0/5 (23.9) | 0/5 (21.8) | 0/5 (11.7) |
| Fundraising | 5/5 (99.6) | 0/5 (68.0) | 5/5 (86.3) | 0/5 (68.0) | 0/5 (68.0) | 2/5 (72.6) |
| Channel expansion | 2/5 (58.0) | 0/5 (42.1) | 1/5 (48.8) | 0/5 (37.6) | 0/5 (35.3) | 0/5 (23.7) |

## Hardest Public Tasks

| Task | Family | Mean Score | Solved By |
| --- | --- | --- | --- |
| FND-036 | Pivot decision | 20.11 | 0/6 |
| FND-037 | Pivot decision | 26.07 | 0/6 |
| FND-040 | Pivot decision | 26.74 | 1/6 |
| FND-038 | Pivot decision | 28.64 | 1/6 |
| FND-005 | Market selection | 30.69 | 0/6 |
| FND-050 | Channel expansion | 32.48 | 0/6 |
| FND-039 | Pivot decision | 33.66 | 0/6 |
| FND-047 | Channel expansion | 34.15 | 0/6 |
| FND-046 | Channel expansion | 37.36 | 0/6 |
| FND-010 | First revenue | 37.44 | 0/6 |
| FND-017 | Churn shock recovery | 41.58 | 1/6 |
| FND-048 | Channel expansion | 42.14 | 1/6 |

## Provider Evidence Status

| ID | Policy | Family | Status | Runs | Evidence | Avg Score | Solve Rate | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_hosted_baseline | openai | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-openai.json or outputs/founderbench-openai-repeats.json |
| deepseek_hosted_baseline | deepseek | hosted_llm | valid | 1 | single_run | 56.59 | 0.46 |  |
| anthropic_hosted_baseline | anthropic | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-anthropic.json or outputs/founderbench-anthropic-repeats.json |
| gemini_hosted_baseline | gemini | hosted_llm | valid | 1 | single_run | 52.69 | 0.26 |  |
| kimi_hosted_baseline | kimi | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-kimi.json or outputs/founderbench-kimi-repeats.json |
| qwen_hosted_baseline | qwen | hosted_llm | missing | 0 |  |  |  | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_hosted_baseline | mistral | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_hosted_baseline | glm | hosted_llm_optional | invalid | 0 |  |  |  | outputs/founderbench-glm.json: Missing validation report outputs/founderbench-glm-submission-report.md |
| xai_hosted_baseline | xai | hosted_llm_optional | missing | 0 |  |  |  | Missing outputs/founderbench-xai.json or outputs/founderbench-xai-repeats.json |
| llama_open_weight_baseline | llama | open_weight | missing | 0 |  |  |  | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_source_baseline | llm | open_source | missing | 0 |  |  |  | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

Provider runs marked `missing` or `invalid` are excluded from the main leaderboard and tables. This avoids mixing older or partial provider outputs into the current release paper evidence.
