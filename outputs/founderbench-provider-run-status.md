# FounderBench Provider Run Status

Provider-run status report for current release paper evidence, generated from planned hosted/local baseline paths and submission validation.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 11 |
| valid_runs | 3 |
| invalid_runs | 1 |
| missing_runs | 7 |
| required_runs | 7 |
| required_valid | 3 |
| required_missing_or_invalid | 4 |
| audit_outputs_present | 0 |
| repeat_bundles_present | 0 |
| repeat_outputs_present | 0 |
| excluded_provider_like_files | 33 |
| ready_for_llm_claims | False |

## Planned current release Runs

| ID | Policy | Priority | Status | Runs | Tasks | Evidence | Repeat Seeds | Report | Audit | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| openai_single | openai | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-openai.json or outputs/founderbench-openai-repeats.json |
| deepseek_single | deepseek | required | valid | 1 | 50 | single_run | 0 | True | False |  |
| anthropic_single | anthropic | required | valid | 1 | 50 | single_run | 0 | True | False |  |
| gemini_single | gemini | required | valid | 1 | 50 | single_run | 0 | True | False |  |
| kimi_single | kimi | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-kimi.json or outputs/founderbench-kimi-repeats.json |
| qwen_single | qwen | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-qwen.json or outputs/founderbench-qwen-repeats.json |
| mistral_single | mistral | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-mistral.json or outputs/founderbench-mistral-repeats.json |
| glm_single | glm | recommended | invalid | 0 | 0 |  | 0 | False | False | outputs/founderbench-glm.json: Missing validation report outputs/founderbench-glm-submission-report.md |
| xai_single | xai | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-xai.json or outputs/founderbench-xai-repeats.json |
| llama_endpoint_single | llama | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-llama.json or outputs/founderbench-llama-repeats.json |
| local_open_model_single | llm | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/founderbench-local-open-model.json or outputs/founderbench-local-open-model-repeats.json |

## Excluded Provider-Like Files

| Path | Bytes | Reason Excluded |
| --- | --- | --- |
| outputs/founderbench-anthropic-results.json | 5068 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-anthropic-sonnet-4.5-full.log | 82937 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-anthropic-sonnet-4.5-smoke.json | 2302 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-anthropic-sonnet-4.5-smoke.log | 2337 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-acc006-trace.json | 48767 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-sc-k3-v0.2-report.md | 1563 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-sc-k3-v0.2.json | 24944 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-chat-v0.2-runlog.md | 879 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-full.log | 165932 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-results.json | 5069 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-run.log | 4682 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v0.2-check.md | 2174 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v0.2-results.json | 24936 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-pro-v0.2-resumable.json | 24966 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-pro-v0.2-runlog.md | 1172 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-reasoner-full.log | 83297 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-reasoner-smoke.json | 2320 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-reasoner-smoke.log | 2355 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-reasoner-submission-report.md | 1032 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-deepseek-v4-reasoner.json | 81629 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-3.5-flash-full.log | 83051 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-3.5-flash-smoke.json | 2378 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-3.5-flash-smoke.log | 2413 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-3.5-flash-submission-report.md | 1025 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-3.5-flash.json | 82315 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-acc001-trace.json | 42196 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-audit-smoke.json | 53818 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-audit-smoke.log | 107704 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-fixed-smoke.json | 62075 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-fixed-smoke.log | 124222 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-full.log | 168054 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-results.json | 5038 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/founderbench-gemini-run.log | 4818 | Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |

## Validation

Status: PASS

The status report is internally consistent. Missing planned runs are expected until hosted/local model evidence is generated and validated.
