# FounderBench v0.3 Provider Run Status

Provider-run status report for v0.3 paper evidence, generated from planned hosted/local baseline paths and submission validation.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 5 |
| valid_runs | 0 |
| invalid_runs | 0 |
| missing_runs | 5 |
| required_runs | 4 |
| required_valid | 0 |
| required_missing_or_invalid | 4 |
| audit_outputs_present | 0 |
| repeat_bundles_present | 0 |
| repeat_outputs_present | 0 |
| excluded_provider_like_files | 12 |
| ready_for_llm_claims | False |

## Planned v0.3 Runs

| ID | Policy | Priority | Status | Runs | Tasks | Evidence | Repeat Seeds | Report | Audit | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| deepseek_single | deepseek | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/acceleratorbench-deepseek-v0.3.json or outputs/acceleratorbench-deepseek-v0.3-repeats.json |
| deepseek_sc_k3 | deepseek_sc | recommended | missing | 0 | 0 |  | 0 | False | False | Missing outputs/acceleratorbench-deepseek-sc-k3-v0.3.json or outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json |
| anthropic_single | anthropic | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/acceleratorbench-anthropic-v0.3.json or outputs/acceleratorbench-anthropic-v0.3-repeats.json |
| gemini_single | gemini | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/acceleratorbench-gemini-v0.3.json or outputs/acceleratorbench-gemini-v0.3-repeats.json |
| local_open_model_single | llm | required | missing | 0 | 0 |  | 0 | False | False | Missing outputs/acceleratorbench-local-open-model-v0.3.json or outputs/acceleratorbench-local-open-model-v0.3-repeats.json |

## Excluded Provider-Like Files

| Path | Bytes | Reason Excluded |
| --- | --- | --- |
| outputs/acceleratorbench-anthropic-results.json | 5068 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-acc006-trace.json | 48767 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-chat-sc-k3-v0.2-report.md | 1519 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-chat-sc-k3-v0.2.json | 24944 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-chat-v0.2-runlog.md | 849 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-results.json | 5069 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-v0.2-check.md | 2119 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-v0.2-results.json | 24936 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-v4-pro-v0.2-resumable.json | 24966 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-deepseek-v4-pro-v0.2-runlog.md | 1141 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-gemini-acc001-trace.json | 42196 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |
| outputs/acceleratorbench-gemini-results.json | 5038 | Not a planned v0.3 provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims. |

## Validation

Status: PASS

The status report is internally consistent. Missing planned runs are expected until hosted/local model evidence is generated and validated.
