# FounderBench v0.3 Experiment Runbook

## Material Passport

| Field | Value |
| --- | --- |
| artifact_type | experiment_runbook |
| data_access_level | no_raw_secret_values |
| verification_status | planned_not_executed |
| scope | operator instructions for producing missing v0.3 hosted/local model evidence |

Runnable experiment runbook for clearing the missing hosted/local baseline evidence gate.

## Summary

| Metric | Value |
| --- | --- |
| providers | 5 |
| phases | 6 |
| required_single_run_evidence_files | 8 |
| minimum_repeats_for_stochastic_claims | 3 |

## Provider Environment

| Provider | Policy | Priority | API Key Env | Model Env | Base URL Env | Default Model |
| --- | --- | --- | --- | --- | --- | --- |
| DeepSeek | deepseek | required | DEEPSEEK_API_KEY | DEEPSEEK_MODEL |  | deepseek-chat |
| DeepSeek self-consistency | deepseek_sc | recommended | DEEPSEEK_API_KEY | DEEPSEEK_MODEL |  | deepseek-chat |
| Anthropic Claude | anthropic | required | ANTHROPIC_API_KEY | ANTHROPIC_MODEL |  | claude-sonnet-4-5 |
| Google Gemini | gemini | required | GEMINI_API_KEY | GEMINI_MODEL |  | gemini-2.5-flash |
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
python -m moneybench.provider_readiness --json-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.md
```

Expected outputs:
- `outputs/acceleratorbench-provider-readiness-v0.3.json`
- `outputs/acceleratorbench-provider-readiness-v0.3.md`

### single_required_runs

Entry condition: Preflight passes for the provider being executed.

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3.json --report outputs/acceleratorbench-deepseek-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3.json --report outputs/acceleratorbench-anthropic-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3.json --report outputs/acceleratorbench-gemini-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3.json --report outputs/acceleratorbench-local-open-model-v0.3-submission-report.md
```

Expected outputs:
- `outputs/acceleratorbench-deepseek-v0.3.json`
- `outputs/acceleratorbench-deepseek-v0.3-submission-report.md`
- `outputs/acceleratorbench-anthropic-v0.3.json`
- `outputs/acceleratorbench-anthropic-v0.3-submission-report.md`
- `outputs/acceleratorbench-gemini-v0.3.json`
- `outputs/acceleratorbench-gemini-v0.3-submission-report.md`
- `outputs/acceleratorbench-local-open-model-v0.3.json`
- `outputs/acceleratorbench-local-open-model-v0.3-submission-report.md`

### audit_traces

Entry condition: At least the corresponding single run has completed or is intentionally being repeated with audit enabled.

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3-audit.json --report outputs/acceleratorbench-deepseek-v0.3-audit-submission-report.md
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3-audit.json --report outputs/acceleratorbench-anthropic-v0.3-audit-submission-report.md
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3-audit.json --report outputs/acceleratorbench-gemini-v0.3-audit-submission-report.md
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3-audit.json --report outputs/acceleratorbench-local-open-model-v0.3-audit-submission-report.md
```

Expected outputs:
- `outputs/acceleratorbench-deepseek-v0.3-audit.json`
- `outputs/acceleratorbench-deepseek-v0.3-audit-submission-report.md`
- `outputs/acceleratorbench-anthropic-v0.3-audit.json`
- `outputs/acceleratorbench-anthropic-v0.3-audit-submission-report.md`
- `outputs/acceleratorbench-gemini-v0.3-audit.json`
- `outputs/acceleratorbench-gemini-v0.3-audit-submission-report.md`
- `outputs/acceleratorbench-local-open-model-v0.3-audit.json`
- `outputs/acceleratorbench-local-open-model-v0.3-audit-submission-report.md`

### repeat_bundles

Entry condition: Single-run execution is stable enough to justify repeated API spend.

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-seed2.json --resume --seed 2
python -m moneybench.submission_bundle --input outputs/acceleratorbench-deepseek-v0.3-seed0.json --input outputs/acceleratorbench-deepseek-v0.3-seed1.json --input outputs/acceleratorbench-deepseek-v0.3-seed2.json --output outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed2.json --resume --seed 2
python -m moneybench.submission_bundle --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed0.json --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed1.json --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed2.json --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats-submission-report.md
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-seed2.json --resume --seed 2
python -m moneybench.submission_bundle --input outputs/acceleratorbench-anthropic-v0.3-seed0.json --input outputs/acceleratorbench-anthropic-v0.3-seed1.json --input outputs/acceleratorbench-anthropic-v0.3-seed2.json --output outputs/acceleratorbench-anthropic-v0.3-repeats.json --report outputs/acceleratorbench-anthropic-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3-repeats.json --report outputs/acceleratorbench-anthropic-v0.3-repeats-submission-report.md
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-seed2.json --resume --seed 2
python -m moneybench.submission_bundle --input outputs/acceleratorbench-gemini-v0.3-seed0.json --input outputs/acceleratorbench-gemini-v0.3-seed1.json --input outputs/acceleratorbench-gemini-v0.3-seed2.json --output outputs/acceleratorbench-gemini-v0.3-repeats.json --report outputs/acceleratorbench-gemini-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3-repeats.json --report outputs/acceleratorbench-gemini-v0.3-repeats-submission-report.md
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-seed2.json --resume --seed 2
python -m moneybench.submission_bundle --input outputs/acceleratorbench-local-open-model-v0.3-seed0.json --input outputs/acceleratorbench-local-open-model-v0.3-seed1.json --input outputs/acceleratorbench-local-open-model-v0.3-seed2.json --output outputs/acceleratorbench-local-open-model-v0.3-repeats.json --report outputs/acceleratorbench-local-open-model-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3-repeats.json --report outputs/acceleratorbench-local-open-model-v0.3-repeats-submission-report.md
```

Expected outputs:
- `outputs/acceleratorbench-deepseek-v0.3-seed0.json`
- `outputs/acceleratorbench-deepseek-v0.3-seed1.json`
- `outputs/acceleratorbench-deepseek-v0.3-seed2.json`
- `outputs/acceleratorbench-deepseek-v0.3-repeats.json`
- `outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed0.json`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed1.json`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed2.json`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats-submission-report.md`
- `outputs/acceleratorbench-anthropic-v0.3-seed0.json`
- `outputs/acceleratorbench-anthropic-v0.3-seed1.json`
- `outputs/acceleratorbench-anthropic-v0.3-seed2.json`
- `outputs/acceleratorbench-anthropic-v0.3-repeats.json`
- `outputs/acceleratorbench-anthropic-v0.3-repeats-submission-report.md`
- `outputs/acceleratorbench-gemini-v0.3-seed0.json`
- `outputs/acceleratorbench-gemini-v0.3-seed1.json`
- `outputs/acceleratorbench-gemini-v0.3-seed2.json`
- `outputs/acceleratorbench-gemini-v0.3-repeats.json`
- `outputs/acceleratorbench-gemini-v0.3-repeats-submission-report.md`
- `outputs/acceleratorbench-local-open-model-v0.3-seed0.json`
- `outputs/acceleratorbench-local-open-model-v0.3-seed1.json`
- `outputs/acceleratorbench-local-open-model-v0.3-seed2.json`
- `outputs/acceleratorbench-local-open-model-v0.3-repeats.json`
- `outputs/acceleratorbench-local-open-model-v0.3-repeats-submission-report.md`

### recommended_ablation

Entry condition: The matching naive provider baseline exists or is scheduled.

```powershell
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-submission-report.md
```

Expected outputs:
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3.json`
- `outputs/acceleratorbench-deepseek-sc-k3-v0.3-submission-report.md`

### postprocess_and_claim_gate

Entry condition: Required run outputs and validation reports exist.

```powershell
python -m moneybench.release regenerate
python -m moneybench.release validate
python -m moneybench.release bundle
```

Expected outputs:
- `outputs/acceleratorbench-model-comparison-v0.3.md`
- `outputs/acceleratorbench-paper-tables-v0.3.md`
- `outputs/acceleratorbench-provider-run-status-v0.3.md`
- `outputs/acceleratorbench-claim-evidence-v0.3.md`
- `outputs/acceleratorbench-submission-gate-v0.3.md`
- `release/acceleratorbench-v0.3.0`

## Quality Gates

- Never paste API keys into commands, run logs, JSON outputs, Markdown reports, or paper text.
- Each included model run must contain exactly 50 task results and pass moneybench.submission validation.
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
