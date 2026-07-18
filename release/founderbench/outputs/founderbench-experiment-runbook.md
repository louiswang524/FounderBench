# FounderBench Experiment Runbook

## Material Passport

| Field | Value |
| --- | --- |
| artifact_type | experiment_runbook |
| data_access_level | no_raw_secret_values |
| verification_status | planned_not_executed |
| scope | operator instructions for producing missing current release hosted/local model evidence |

Runnable experiment runbook for clearing the missing hosted/local baseline evidence gate.

## Summary

| Metric | Value |
| --- | --- |
| providers | 12 |
| phases | 6 |
| required_single_run_evidence_files | 14 |
| minimum_repeats_for_stochastic_claims | 3 |

## Provider Environment

| Provider | Policy | Priority | API Key Env | Model Env | Base URL Env | Default Model |
| --- | --- | --- | --- | --- | --- | --- |
| OpenAI GPT | openai | recommended | OPENAI_API_KEY | OPENAI_MODEL | OPENAI_BASE_URL | gpt-4.1-mini |
| DeepSeek | deepseek | required | DEEPSEEK_API_KEY | DEEPSEEK_MODEL |  | deepseek-chat |
| DeepSeek self-consistency | deepseek_sc | recommended | DEEPSEEK_API_KEY | DEEPSEEK_MODEL |  | deepseek-chat |
| Anthropic Claude | anthropic | required | ANTHROPIC_API_KEY | ANTHROPIC_MODEL |  | claude-sonnet-4-5 |
| Google Gemini | gemini | required | GEMINI_API_KEY | GEMINI_MODEL |  | gemini-2.5-flash |
| Moonshot Kimi | kimi | recommended | KIMI_API_KEY | KIMI_MODEL | KIMI_BASE_URL | kimi-latest |
| Alibaba Qwen | qwen | recommended | QWEN_API_KEY | QWEN_MODEL | QWEN_BASE_URL | qwen-plus |
| Mistral | mistral | recommended | MISTRAL_API_KEY | MISTRAL_MODEL | MISTRAL_BASE_URL | mistral-large-latest |
| Z.ai GLM | glm | recommended | GLM_API_KEY | GLM_MODEL | GLM_BASE_URL | glm-4-plus |
| xAI Grok | xai | recommended | XAI_API_KEY | XAI_MODEL | XAI_BASE_URL | grok-3-mini |
| Llama/Open-weight endpoint | llama | recommended | LLAMA_API_KEY | LLAMA_MODEL | LLAMA_BASE_URL | meta-llama/Llama-3.1-70B-Instruct |
| Local/OpenAI-compatible | llm | required | OPENAI_COMPAT_API_KEY | OPENAI_COMPAT_MODEL | OPENAI_COMPAT_BASE_URL | Qwen/Qwen2.5-7B-Instruct |

## Phase Overview

| Phase | Owner | Purpose | Exit Condition |
| --- | --- | --- | --- |
| preflight | evaluator | Confirm provider configuration, clean output target names, and record the exact model ids. | Provider readiness report is regenerated and reviewed. |
| single_required_runs | evaluator | Run each required hosted/local model once on the complete 50-task suite. | Every required single-run output exists and passes submission validation. |
| audit_traces | evaluator | Collect redacted audit traces for hosted/local runs so qualitative failures can be inspected. | Audit outputs and their submission reports exist for required runs. |
| repeat_bundles | evaluator | Run 3 seeds per provider before stochastic confidence claims. | Repeated seed files are combined into validated repeat bundles. |
| recommended_ablation | evaluator | Run the recommended self-consistency ablation as a separate comparison, not as a replacement for the naive provider baseline. | Recommended ablation output exists and is clearly labeled in model-comparison artifacts. |
| postprocess_and_claim_gate | paper_author | Regenerate paper tables, model comparison, provider status, claim evidence, and submission gate after runs are present. | Submission gate no longer reports missing required experiment evidence; claim wording is updated only where evidence supports it. |

## Phase Commands

### preflight

Entry condition: Provider keys and model choices are available in environment variables; no secrets are written to files.

```powershell
python -m founderbench.provider_readiness --json-output ..\..\outputs\founderbench-provider-readiness.json --markdown-output ..\..\outputs\founderbench-provider-readiness.md
```

Expected outputs:
- `outputs/founderbench-provider-readiness.json`
- `outputs/founderbench-provider-readiness.md`

### single_required_runs

Entry condition: Preflight passes for the provider being executed.

```powershell
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-openai.json --report outputs/founderbench-openai-submission-report.md
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-deepseek.json --report outputs/founderbench-deepseek-submission-report.md
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-anthropic.json --report outputs/founderbench-anthropic-submission-report.md
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-gemini.json --report outputs/founderbench-gemini-submission-report.md
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-kimi.json --report outputs/founderbench-kimi-submission-report.md
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-qwen.json --report outputs/founderbench-qwen-submission-report.md
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
```

Expected outputs:
- `outputs/founderbench-openai.json`
- `outputs/founderbench-openai-submission-report.md`
- `outputs/founderbench-deepseek.json`
- `outputs/founderbench-deepseek-submission-report.md`
- `outputs/founderbench-anthropic.json`
- `outputs/founderbench-anthropic-submission-report.md`
- `outputs/founderbench-gemini.json`
- `outputs/founderbench-gemini-submission-report.md`
- `outputs/founderbench-kimi.json`
- `outputs/founderbench-kimi-submission-report.md`
- `outputs/founderbench-qwen.json`
- `outputs/founderbench-qwen-submission-report.md`
- `outputs/founderbench-local-open-model.json`
- `outputs/founderbench-local-open-model-submission-report.md`

### audit_traces

Entry condition: At least the corresponding single run has completed or is intentionally being repeated with audit enabled.

```powershell
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-openai-audit.json --report outputs/founderbench-openai-audit-submission-report.md
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-deepseek-audit.json --report outputs/founderbench-deepseek-audit-submission-report.md
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-anthropic-audit.json --report outputs/founderbench-anthropic-audit-submission-report.md
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-gemini-audit.json --report outputs/founderbench-gemini-audit-submission-report.md
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-kimi-audit.json --report outputs/founderbench-kimi-audit-submission-report.md
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-qwen-audit.json --report outputs/founderbench-qwen-audit-submission-report.md
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-audit.json --resume --seed 0 --audit
python -m founderbench.submission --input outputs/founderbench-local-open-model-audit.json --report outputs/founderbench-local-open-model-audit-submission-report.md
```

Expected outputs:
- `outputs/founderbench-openai-audit.json`
- `outputs/founderbench-openai-audit-submission-report.md`
- `outputs/founderbench-deepseek-audit.json`
- `outputs/founderbench-deepseek-audit-submission-report.md`
- `outputs/founderbench-anthropic-audit.json`
- `outputs/founderbench-anthropic-audit-submission-report.md`
- `outputs/founderbench-gemini-audit.json`
- `outputs/founderbench-gemini-audit-submission-report.md`
- `outputs/founderbench-kimi-audit.json`
- `outputs/founderbench-kimi-audit-submission-report.md`
- `outputs/founderbench-qwen-audit.json`
- `outputs/founderbench-qwen-audit-submission-report.md`
- `outputs/founderbench-local-open-model-audit.json`
- `outputs/founderbench-local-open-model-audit-submission-report.md`

### repeat_bundles

Entry condition: Single-run execution is stable enough to justify repeated API spend.

```powershell
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-openai-seed0.json --input outputs/founderbench-openai-seed1.json --input outputs/founderbench-openai-seed2.json --output outputs/founderbench-openai-repeats.json --report outputs/founderbench-openai-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-openai-repeats.json --report outputs/founderbench-openai-repeats-submission-report.md
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-deepseek-seed0.json --input outputs/founderbench-deepseek-seed1.json --input outputs/founderbench-deepseek-seed2.json --output outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-deepseek-sc-k3-seed0.json --input outputs/founderbench-deepseek-sc-k3-seed1.json --input outputs/founderbench-deepseek-sc-k3-seed2.json --output outputs/founderbench-deepseek-sc-k3-repeats.json --report outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-deepseek-sc-k3-repeats.json --report outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-anthropic-seed0.json --input outputs/founderbench-anthropic-seed1.json --input outputs/founderbench-anthropic-seed2.json --output outputs/founderbench-anthropic-repeats.json --report outputs/founderbench-anthropic-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-anthropic-repeats.json --report outputs/founderbench-anthropic-repeats-submission-report.md
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-gemini-seed0.json --input outputs/founderbench-gemini-seed1.json --input outputs/founderbench-gemini-seed2.json --output outputs/founderbench-gemini-repeats.json --report outputs/founderbench-gemini-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-gemini-repeats.json --report outputs/founderbench-gemini-repeats-submission-report.md
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-kimi-seed0.json --input outputs/founderbench-kimi-seed1.json --input outputs/founderbench-kimi-seed2.json --output outputs/founderbench-kimi-repeats.json --report outputs/founderbench-kimi-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-kimi-repeats.json --report outputs/founderbench-kimi-repeats-submission-report.md
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-qwen-seed0.json --input outputs/founderbench-qwen-seed1.json --input outputs/founderbench-qwen-seed2.json --output outputs/founderbench-qwen-repeats.json --report outputs/founderbench-qwen-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-qwen-repeats.json --report outputs/founderbench-qwen-repeats-submission-report.md
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-mistral-seed0.json --input outputs/founderbench-mistral-seed1.json --input outputs/founderbench-mistral-seed2.json --output outputs/founderbench-mistral-repeats.json --report outputs/founderbench-mistral-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-mistral-repeats.json --report outputs/founderbench-mistral-repeats-submission-report.md
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-glm-seed0.json --input outputs/founderbench-glm-seed1.json --input outputs/founderbench-glm-seed2.json --output outputs/founderbench-glm-repeats.json --report outputs/founderbench-glm-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-glm-repeats.json --report outputs/founderbench-glm-repeats-submission-report.md
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-xai-seed0.json --input outputs/founderbench-xai-seed1.json --input outputs/founderbench-xai-seed2.json --output outputs/founderbench-xai-repeats.json --report outputs/founderbench-xai-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-xai-repeats.json --report outputs/founderbench-xai-repeats-submission-report.md
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-llama-seed0.json --input outputs/founderbench-llama-seed1.json --input outputs/founderbench-llama-seed2.json --output outputs/founderbench-llama-repeats.json --report outputs/founderbench-llama-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-llama-repeats.json --report outputs/founderbench-llama-repeats-submission-report.md
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-seed2.json --resume --seed 2
python -m founderbench.submission_bundle --input outputs/founderbench-local-open-model-seed0.json --input outputs/founderbench-local-open-model-seed1.json --input outputs/founderbench-local-open-model-seed2.json --output outputs/founderbench-local-open-model-repeats.json --report outputs/founderbench-local-open-model-repeats-submission-report.md
python -m founderbench.submission --input outputs/founderbench-local-open-model-repeats.json --report outputs/founderbench-local-open-model-repeats-submission-report.md
```

Expected outputs:
- `outputs/founderbench-openai-seed0.json`
- `outputs/founderbench-openai-seed1.json`
- `outputs/founderbench-openai-seed2.json`
- `outputs/founderbench-openai-repeats.json`
- `outputs/founderbench-openai-repeats-submission-report.md`
- `outputs/founderbench-deepseek-seed0.json`
- `outputs/founderbench-deepseek-seed1.json`
- `outputs/founderbench-deepseek-seed2.json`
- `outputs/founderbench-deepseek-repeats.json`
- `outputs/founderbench-deepseek-repeats-submission-report.md`
- `outputs/founderbench-deepseek-sc-k3-seed0.json`
- `outputs/founderbench-deepseek-sc-k3-seed1.json`
- `outputs/founderbench-deepseek-sc-k3-seed2.json`
- `outputs/founderbench-deepseek-sc-k3-repeats.json`
- `outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md`
- `outputs/founderbench-anthropic-seed0.json`
- `outputs/founderbench-anthropic-seed1.json`
- `outputs/founderbench-anthropic-seed2.json`
- `outputs/founderbench-anthropic-repeats.json`
- `outputs/founderbench-anthropic-repeats-submission-report.md`
- `outputs/founderbench-gemini-seed0.json`
- `outputs/founderbench-gemini-seed1.json`
- `outputs/founderbench-gemini-seed2.json`
- `outputs/founderbench-gemini-repeats.json`
- `outputs/founderbench-gemini-repeats-submission-report.md`
- `outputs/founderbench-kimi-seed0.json`
- `outputs/founderbench-kimi-seed1.json`
- `outputs/founderbench-kimi-seed2.json`
- `outputs/founderbench-kimi-repeats.json`
- `outputs/founderbench-kimi-repeats-submission-report.md`
- `outputs/founderbench-qwen-seed0.json`
- `outputs/founderbench-qwen-seed1.json`
- `outputs/founderbench-qwen-seed2.json`
- `outputs/founderbench-qwen-repeats.json`
- `outputs/founderbench-qwen-repeats-submission-report.md`
- `outputs/founderbench-mistral-seed0.json`
- `outputs/founderbench-mistral-seed1.json`
- `outputs/founderbench-mistral-seed2.json`
- `outputs/founderbench-mistral-repeats.json`
- `outputs/founderbench-mistral-repeats-submission-report.md`
- `outputs/founderbench-glm-seed0.json`
- `outputs/founderbench-glm-seed1.json`
- `outputs/founderbench-glm-seed2.json`
- `outputs/founderbench-glm-repeats.json`
- `outputs/founderbench-glm-repeats-submission-report.md`
- `outputs/founderbench-xai-seed0.json`
- `outputs/founderbench-xai-seed1.json`
- `outputs/founderbench-xai-seed2.json`
- `outputs/founderbench-xai-repeats.json`
- `outputs/founderbench-xai-repeats-submission-report.md`
- `outputs/founderbench-llama-seed0.json`
- `outputs/founderbench-llama-seed1.json`
- `outputs/founderbench-llama-seed2.json`
- `outputs/founderbench-llama-repeats.json`
- `outputs/founderbench-llama-repeats-submission-report.md`
- `outputs/founderbench-local-open-model-seed0.json`
- `outputs/founderbench-local-open-model-seed1.json`
- `outputs/founderbench-local-open-model-seed2.json`
- `outputs/founderbench-local-open-model-repeats.json`
- `outputs/founderbench-local-open-model-repeats-submission-report.md`

### recommended_ablation

Entry condition: The matching naive provider baseline exists or is scheduled.

```powershell
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-deepseek-sc-k3.json --report outputs/founderbench-deepseek-sc-k3-submission-report.md
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-mistral.json --report outputs/founderbench-mistral-submission-report.md
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-glm.json --report outputs/founderbench-glm-submission-report.md
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-xai.json --report outputs/founderbench-xai-submission-report.md
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama.json --resume --seed 0
python -m founderbench.submission --input outputs/founderbench-llama.json --report outputs/founderbench-llama-submission-report.md
```

Expected outputs:
- `outputs/founderbench-deepseek-sc-k3.json`
- `outputs/founderbench-deepseek-sc-k3-submission-report.md`
- `outputs/founderbench-mistral.json`
- `outputs/founderbench-mistral-submission-report.md`
- `outputs/founderbench-glm.json`
- `outputs/founderbench-glm-submission-report.md`
- `outputs/founderbench-xai.json`
- `outputs/founderbench-xai-submission-report.md`
- `outputs/founderbench-llama.json`
- `outputs/founderbench-llama-submission-report.md`

### postprocess_and_claim_gate

Entry condition: Required run outputs and validation reports exist.

```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
python -m founderbench.release bundle
```

Expected outputs:
- `outputs/founderbench-model-comparison.md`
- `outputs/founderbench-paper-tables.md`
- `outputs/founderbench-provider-run-status.md`
- `outputs/founderbench-claim-evidence.md`
- `outputs/founderbench-submission-gate.md`
- `release/founderbench`

## Quality Gates

- Never paste API keys into commands, run logs, JSON outputs, Markdown reports, or paper text.
- Each included model run must contain exactly 50 task results and pass founderbench.submission validation.
- Provider errors, invalid actions, over-budget decisions, bankruptcies, and timeouts remain in the denominator.
- Hosted/local model-comparison claims require all required provider/local runs to be valid.
- Stochastic confidence claims require validated repeat bundles, not only single-run outputs.
- Audit traces must be inspected for accidental sensitive text before release.

## Claim Unlock Rules

### hosted_llm_comparison

- Unlock condition: DeepSeek, Anthropic, Gemini, and local/open-source required runs validate on all 50 tasks.
- Otherwise: Keep wording to planned/infrastructure-ready provider comparison.

### self_consistency_improves_metrics

- Unlock condition: Validated DeepSeek naive and DeepSeek self-consistency repeat bundles exist and are compared by the statistical protocol.
- Otherwise: Describe self-consistency as a planned or preliminary ablation only.

### private_holdout_leaderboard

- Unlock condition: Evaluator-controlled private holdout aggregate report exists.
- Otherwise: Describe only the private holdout protocol, not private holdout results.

## Validation

Status: PASS

The runbook is internally consistent and keeps planned experiments separate from executed evidence.
