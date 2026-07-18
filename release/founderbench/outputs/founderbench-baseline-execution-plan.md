# FounderBench Baseline Execution Plan

Execution plan for paper-grade hosted and local/open-source LLM baseline runs.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 12 |
| required_runs | 7 |
| recommended_runs | 5 |
| hosted_runs | 10 |
| local_open_source_runs | 2 |
| minimum_repeats_for_stochastic_claims | 3 |

## Scope

| Field | Value |
| --- | --- |
| task_count | 50 |
| splits | ['public_dev', 'public_test'] |
| primary_endpoint | average_task_score |
| secondary_endpoints | ['solved', 'solve_rate', 'shutdown_rate', 'invalid_actions', 'over_budget_decisions', 'provider_errors', 'decision_latency_s', 'simulated_api_cost'] |
| planned_model_roster | ['OpenAI/GPT', 'Anthropic/Claude', 'Google/Gemini', 'DeepSeek', 'Moonshot/Kimi', 'Alibaba/Qwen', 'Mistral', 'Z.ai/GLM', 'xAI/Grok', 'Llama/open-weight', 'local OpenAI-compatible'] |

## Fairness Controls

- Use the canonical prompt protocol and structured action schema for every provider.
- Run every required model on the same 50 current task ids.
- Separate required frontier/commercial coverage from recommended broader ecosystem coverage so missing optional APIs do not block core reproducibility.
- Validate every output with moneybench.submission before including it in leaderboard claims.
- Do not drop failed tasks, malformed outputs, provider errors, bankruptcies, or over-budget decisions.
- Report provider model ids, prompt/protocol hashes, latency, token usage when available, and estimated cost.
- Use the pre-specified paired task-level statistical protocol for model comparisons.

## Repetition Policy

- `single_run_claims`: Allowed only as preliminary baseline rows when clearly labeled single-run.
- `stochastic_claims`: Require at least 3 repeats or an explicit limitation statement; record each repeat with a distinct resumable-runner --seed value.
- `bundle_protocol`: Combine repeated seed outputs with moneybench.submission_bundle and report the generated submission report before stochastic confidence claims.
- `self_consistency`: DeepSeek self-consistency uses k=3 as a separate ablation, not a replacement for the naive baseline.

## Audit Policy

- `required_audit_traces`: Collect redacted audit runs for at least one hosted provider before qualitative LLM failure analysis.
- `redaction`: Audit artifacts must retain prompt hashes and diagnostics while removing raw secret values.
- `sharing`: Inspect audit files manually before public release because model responses may contain accidental sensitive text.

## Acceptance Criteria

- Each required run produces a JSON output with exactly 50 task results.
- Each required run passes moneybench.submission validation.
- Provider-error categories are reported even when zero.
- At least three provider configurations are ready before the submission gate can pass provider readiness.
- Claim-evidence report remains conservative until all LLM comparison evidence exists.

## Planned Runs

| ID | Policy | Family | Priority | Tasks | Output | Submission Report | Repeat Bundle |
| --- | --- | --- | --- | --- | --- | --- | --- |
| openai_single | openai | hosted | required | 50 | outputs/founderbench-openai.json | outputs/founderbench-openai-submission-report.md | outputs/founderbench-openai-repeats.json |
| deepseek_single | deepseek | hosted | required | 50 | outputs/founderbench-deepseek.json | outputs/founderbench-deepseek-submission-report.md | outputs/founderbench-deepseek-repeats.json |
| deepseek_sc_k3 | deepseek_sc | hosted | recommended | 50 | outputs/founderbench-deepseek-sc-k3.json | outputs/founderbench-deepseek-sc-k3-submission-report.md | outputs/founderbench-deepseek-sc-k3-repeats.json |
| anthropic_single | anthropic | hosted | required | 50 | outputs/founderbench-anthropic.json | outputs/founderbench-anthropic-submission-report.md | outputs/founderbench-anthropic-repeats.json |
| gemini_single | gemini | hosted | required | 50 | outputs/founderbench-gemini.json | outputs/founderbench-gemini-submission-report.md | outputs/founderbench-gemini-repeats.json |
| kimi_single | kimi | hosted | required | 50 | outputs/founderbench-kimi.json | outputs/founderbench-kimi-submission-report.md | outputs/founderbench-kimi-repeats.json |
| qwen_single | qwen | hosted | required | 50 | outputs/founderbench-qwen.json | outputs/founderbench-qwen-submission-report.md | outputs/founderbench-qwen-repeats.json |
| mistral_single | mistral | hosted | recommended | 50 | outputs/founderbench-mistral.json | outputs/founderbench-mistral-submission-report.md | outputs/founderbench-mistral-repeats.json |
| glm_single | glm | hosted | recommended | 50 | outputs/founderbench-glm.json | outputs/founderbench-glm-submission-report.md | outputs/founderbench-glm-repeats.json |
| xai_single | xai | hosted | recommended | 50 | outputs/founderbench-xai.json | outputs/founderbench-xai-submission-report.md | outputs/founderbench-xai-repeats.json |
| llama_endpoint_single | llama | local_open_source | recommended | 50 | outputs/founderbench-llama.json | outputs/founderbench-llama-submission-report.md | outputs/founderbench-llama-repeats.json |
| local_open_model_single | llm | local_open_source | required | 50 | outputs/founderbench-local-open-model.json | outputs/founderbench-local-open-model-submission-report.md | outputs/founderbench-local-open-model-repeats.json |

## Commands

### openai_single

Primary OpenAI/GPT hosted baseline, matching the frontier-provider style used by YC-Bench-like comparisons.

```powershell
python -m moneybench.resumable_runner --policy openai --output outputs/founderbench-openai.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-openai.json --report outputs/founderbench-openai-submission-report.md
python -m moneybench.resumable_runner --policy openai --output outputs/founderbench-openai-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-openai-audit.json --report outputs/founderbench-openai-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-openai-seed0.json --input outputs/founderbench-openai-seed1.json --input outputs/founderbench-openai-seed2.json --output outputs/founderbench-openai-repeats.json --report outputs/founderbench-openai-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-openai-repeats.json --report outputs/founderbench-openai-repeats-submission-report.md
```

### deepseek_single

Primary DeepSeek hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-deepseek.json --report outputs/founderbench-deepseek-submission-report.md
python -m moneybench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-deepseek-audit.json --report outputs/founderbench-deepseek-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-deepseek-seed0.json --input outputs/founderbench-deepseek-seed1.json --input outputs/founderbench-deepseek-seed2.json --output outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
```

### deepseek_sc_k3

Self-consistency k=3 ablation for DeepSeek.

```powershell
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-deepseek-sc-k3.json --report outputs/founderbench-deepseek-sc-k3-submission-report.md
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-deepseek-sc-k3-audit.json --report outputs/founderbench-deepseek-sc-k3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-deepseek-sc-k3-seed0.json --input outputs/founderbench-deepseek-sc-k3-seed1.json --input outputs/founderbench-deepseek-sc-k3-seed2.json --output outputs/founderbench-deepseek-sc-k3-repeats.json --report outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-deepseek-sc-k3-repeats.json --report outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md
```

### anthropic_single

Primary Claude/Anthropic hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-anthropic.json --report outputs/founderbench-anthropic-submission-report.md
python -m moneybench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-anthropic-audit.json --report outputs/founderbench-anthropic-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-anthropic-seed0.json --input outputs/founderbench-anthropic-seed1.json --input outputs/founderbench-anthropic-seed2.json --output outputs/founderbench-anthropic-repeats.json --report outputs/founderbench-anthropic-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-anthropic-repeats.json --report outputs/founderbench-anthropic-repeats-submission-report.md
```

### gemini_single

Primary Gemini hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy gemini --output outputs/founderbench-gemini.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-gemini.json --report outputs/founderbench-gemini-submission-report.md
python -m moneybench.resumable_runner --policy gemini --output outputs/founderbench-gemini-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-gemini-audit.json --report outputs/founderbench-gemini-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-gemini-seed0.json --input outputs/founderbench-gemini-seed1.json --input outputs/founderbench-gemini-seed2.json --output outputs/founderbench-gemini-repeats.json --report outputs/founderbench-gemini-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-gemini-repeats.json --report outputs/founderbench-gemini-repeats-submission-report.md
```

### kimi_single

Primary Moonshot Kimi hosted/open-weight-family baseline.

```powershell
python -m moneybench.resumable_runner --policy kimi --output outputs/founderbench-kimi.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-kimi.json --report outputs/founderbench-kimi-submission-report.md
python -m moneybench.resumable_runner --policy kimi --output outputs/founderbench-kimi-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-kimi-audit.json --report outputs/founderbench-kimi-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-kimi-seed0.json --input outputs/founderbench-kimi-seed1.json --input outputs/founderbench-kimi-seed2.json --output outputs/founderbench-kimi-repeats.json --report outputs/founderbench-kimi-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-kimi-repeats.json --report outputs/founderbench-kimi-repeats-submission-report.md
```

### qwen_single

Primary Alibaba Qwen hosted/open-weight-family baseline.

```powershell
python -m moneybench.resumable_runner --policy qwen --output outputs/founderbench-qwen.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-qwen.json --report outputs/founderbench-qwen-submission-report.md
python -m moneybench.resumable_runner --policy qwen --output outputs/founderbench-qwen-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-qwen-audit.json --report outputs/founderbench-qwen-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-qwen-seed0.json --input outputs/founderbench-qwen-seed1.json --input outputs/founderbench-qwen-seed2.json --output outputs/founderbench-qwen-repeats.json --report outputs/founderbench-qwen-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-qwen-repeats.json --report outputs/founderbench-qwen-repeats-submission-report.md
```

### mistral_single

Mistral hosted baseline for broader non-US provider coverage.

```powershell
python -m moneybench.resumable_runner --policy mistral --output outputs/founderbench-mistral.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-mistral.json --report outputs/founderbench-mistral-submission-report.md
python -m moneybench.resumable_runner --policy mistral --output outputs/founderbench-mistral-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-mistral-audit.json --report outputs/founderbench-mistral-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-mistral-seed0.json --input outputs/founderbench-mistral-seed1.json --input outputs/founderbench-mistral-seed2.json --output outputs/founderbench-mistral-repeats.json --report outputs/founderbench-mistral-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-mistral-repeats.json --report outputs/founderbench-mistral-repeats-submission-report.md
```

### glm_single

Z.ai GLM hosted baseline for additional China-developed model coverage.

```powershell
python -m moneybench.resumable_runner --policy glm --output outputs/founderbench-glm.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-glm.json --report outputs/founderbench-glm-submission-report.md
python -m moneybench.resumable_runner --policy glm --output outputs/founderbench-glm-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-glm-audit.json --report outputs/founderbench-glm-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-glm-seed0.json --input outputs/founderbench-glm-seed1.json --input outputs/founderbench-glm-seed2.json --output outputs/founderbench-glm-repeats.json --report outputs/founderbench-glm-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-glm-repeats.json --report outputs/founderbench-glm-repeats-submission-report.md
```

### xai_single

xAI/Grok hosted baseline for another frontier closed-model family.

```powershell
python -m moneybench.resumable_runner --policy xai --output outputs/founderbench-xai.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-xai.json --report outputs/founderbench-xai-submission-report.md
python -m moneybench.resumable_runner --policy xai --output outputs/founderbench-xai-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-xai-audit.json --report outputs/founderbench-xai-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-xai-seed0.json --input outputs/founderbench-xai-seed1.json --input outputs/founderbench-xai-seed2.json --output outputs/founderbench-xai-repeats.json --report outputs/founderbench-xai-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-xai-repeats.json --report outputs/founderbench-xai-repeats-submission-report.md
```

### llama_endpoint_single

Llama/open-weight endpoint baseline, runnable through any OpenAI-compatible serving provider.

```powershell
python -m moneybench.resumable_runner --policy llama --output outputs/founderbench-llama.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-llama.json --report outputs/founderbench-llama-submission-report.md
python -m moneybench.resumable_runner --policy llama --output outputs/founderbench-llama-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-llama-audit.json --report outputs/founderbench-llama-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-llama-seed0.json --input outputs/founderbench-llama-seed1.json --input outputs/founderbench-llama-seed2.json --output outputs/founderbench-llama-repeats.json --report outputs/founderbench-llama-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-llama-repeats.json --report outputs/founderbench-llama-repeats-submission-report.md
```

### local_open_model_single

Primary local/open-source baseline through an OpenAI-compatible server.

```powershell
python -m moneybench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume --seed 0
python -m moneybench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
python -m moneybench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/founderbench-local-open-model-audit.json --report outputs/founderbench-local-open-model-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/founderbench-local-open-model-seed0.json --input outputs/founderbench-local-open-model-seed1.json --input outputs/founderbench-local-open-model-seed2.json --output outputs/founderbench-local-open-model-repeats.json --report outputs/founderbench-local-open-model-repeats-submission-report.md
python -m moneybench.submission --input outputs/founderbench-local-open-model-repeats.json --report outputs/founderbench-local-open-model-repeats-submission-report.md
```

## Validation

Status: PASS

The execution plan covers the required hosted and local/open-source baseline evidence needed before LLM comparison claims are made.
