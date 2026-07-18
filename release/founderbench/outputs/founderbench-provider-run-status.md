# FounderBench Provider Run Status

Provider-run status report for current release paper evidence, generated from planned hosted/local baseline paths and submission validation.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 12 |
| valid_runs | 0 |
| invalid_runs | 0 |
| missing_runs | 12 |
| required_runs | 7 |
| required_valid | 0 |
| required_missing_or_invalid | 7 |
| audit_outputs_present | 0 |
| repeat_bundles_present | 0 |
| repeat_outputs_present | 0 |
| excluded_provider_like_files | 12 |
| ready_for_llm_claims | False |

## Planned current release Runs

| ID | Policy | Priority | Status | Runs | Tasks | Evidence | Repeat Seeds | Report | Audit | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_single | openai | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-openai.json or outputs/founderbench-openai-repeats.json |
| deepseek_single | deepseek | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-deepseek.json or outputs/founderbench-deepseek-repeats.json |
| deepseek_sc_k3 | deepseek_sc | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-deepseek-sc-k3.json or outputs/founderbench-deepseek-sc-k3-repeats.json |
| anthropic_single | anthropic | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-anthropic.json or outputs/founderbench-anthropic-repeats.json |
| gemini_single | gemini | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-gemini.json or outputs/founderbench-gemini-repeats.json |
| kimi_single | kimi | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-kimi.json or outputs/founderbench-kimi-repeats.json |
| qwen_single | qwen | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_single | mistral | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_single | glm | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-glm.json or outputs/founderbench-glm-repeats.json |
| xai_single | xai | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-xai.json or outputs/founderbench-xai-repeats.json |
| llama_endpoint_single | llama | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_model_single | llm | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

## Excluded Provider-Like Files

| Path | Bytes | Reason Excluded |
| --- | --- | --- |
| outputs/founderbench-anthropic-results.json | 5068 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-acc006-trace.json | 48767 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-sc-k3-v0.2-report.md | 1563 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-sc-k3-v0.2.json | 24944 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-v0.2-runlog.md | 879 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-results.json | 5069 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v0.2-check.md | 2174 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v0.2-results.json | 24936 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-pro-v0.2-resumable.json | 24966 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-pro-v0.2-runlog.md | 1172 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-acc001-trace.json | 42196 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-results.json | 5038 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |

## Validation

Status: PASS

The status report is internally consistent. Missing planned runs are expected until hosted/local model evidence is generated and validated.
