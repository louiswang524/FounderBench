# FounderBench v0.3 Baseline Execution Plan

Execution plan for paper-grade hosted and local/open-source LLM baseline runs.

## Summary

| Metric | Value |
| --- | --- |
| planned_runs | 5 |
| required_runs | 4 |
| recommended_runs | 1 |
| hosted_runs | 4 |
| local_open_source_runs | 1 |
| minimum_repeats_for_stochastic_claims | 3 |

## Scope

| Field | Value |
| --- | --- |
| task_count | 50 |
| splits | ['public_dev', 'public_test'] |
| primary_endpoint | average_task_score |
| secondary_endpoints | ['solved', 'solve_rate', 'shutdown_rate', 'invalid_actions', 'over_budget_decisions', 'provider_errors', 'decision_latency_s', 'simulated_api_cost'] |

## Fairness Controls

- Use the canonical prompt protocol and structured action schema for every provider.
- Run every required model on the same 50 v0.3.0 task ids.
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
| deepseek_single | deepseek | hosted | required | 50 | outputs/acceleratorbench-deepseek-v0.3.json | outputs/acceleratorbench-deepseek-v0.3-submission-report.md | outputs/acceleratorbench-deepseek-v0.3-repeats.json |
| deepseek_sc_k3 | deepseek_sc | hosted | recommended | 50 | outputs/acceleratorbench-deepseek-sc-k3-v0.3.json | outputs/acceleratorbench-deepseek-sc-k3-v0.3-submission-report.md | outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json |
| anthropic_single | anthropic | hosted | required | 50 | outputs/acceleratorbench-anthropic-v0.3.json | outputs/acceleratorbench-anthropic-v0.3-submission-report.md | outputs/acceleratorbench-anthropic-v0.3-repeats.json |
| gemini_single | gemini | hosted | required | 50 | outputs/acceleratorbench-gemini-v0.3.json | outputs/acceleratorbench-gemini-v0.3-submission-report.md | outputs/acceleratorbench-gemini-v0.3-repeats.json |
| local_open_model_single | llm | local_open_source | required | 50 | outputs/acceleratorbench-local-open-model-v0.3.json | outputs/acceleratorbench-local-open-model-v0.3-submission-report.md | outputs/acceleratorbench-local-open-model-v0.3-repeats.json |

## Commands

### deepseek_single

Primary DeepSeek hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3.json --report outputs/acceleratorbench-deepseek-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3-audit.json --report outputs/acceleratorbench-deepseek-v0.3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/acceleratorbench-deepseek-v0.3-seed0.json --input outputs/acceleratorbench-deepseek-v0.3-seed1.json --input outputs/acceleratorbench-deepseek-v0.3-seed2.json --output outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md
```

### deepseek_sc_k3

Self-consistency k=3 ablation for DeepSeek.

```powershell
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-audit.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed0.json --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed1.json --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-seed2.json --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-repeats-submission-report.md
```

### anthropic_single

Primary Claude/Anthropic hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3.json --report outputs/acceleratorbench-anthropic-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3-audit.json --report outputs/acceleratorbench-anthropic-v0.3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/acceleratorbench-anthropic-v0.3-seed0.json --input outputs/acceleratorbench-anthropic-v0.3-seed1.json --input outputs/acceleratorbench-anthropic-v0.3-seed2.json --output outputs/acceleratorbench-anthropic-v0.3-repeats.json --report outputs/acceleratorbench-anthropic-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3-repeats.json --report outputs/acceleratorbench-anthropic-v0.3-repeats-submission-report.md
```

### gemini_single

Primary Gemini hosted baseline.

```powershell
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3.json --report outputs/acceleratorbench-gemini-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3-audit.json --report outputs/acceleratorbench-gemini-v0.3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/acceleratorbench-gemini-v0.3-seed0.json --input outputs/acceleratorbench-gemini-v0.3-seed1.json --input outputs/acceleratorbench-gemini-v0.3-seed2.json --output outputs/acceleratorbench-gemini-v0.3-repeats.json --report outputs/acceleratorbench-gemini-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3-repeats.json --report outputs/acceleratorbench-gemini-v0.3-repeats-submission-report.md
```

### local_open_model_single

Primary local/open-source baseline through an OpenAI-compatible server.

```powershell
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3.json --resume --seed 0
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3.json --report outputs/acceleratorbench-local-open-model-v0.3-submission-report.md
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-audit.json --resume --seed 0 --audit
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3-audit.json --report outputs/acceleratorbench-local-open-model-v0.3-audit-submission-report.md
python -m moneybench.submission_bundle --input outputs/acceleratorbench-local-open-model-v0.3-seed0.json --input outputs/acceleratorbench-local-open-model-v0.3-seed1.json --input outputs/acceleratorbench-local-open-model-v0.3-seed2.json --output outputs/acceleratorbench-local-open-model-v0.3-repeats.json --report outputs/acceleratorbench-local-open-model-v0.3-repeats-submission-report.md
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3-repeats.json --report outputs/acceleratorbench-local-open-model-v0.3-repeats-submission-report.md
```

## Validation

Status: PASS

The execution plan covers the required hosted and local/open-source baseline evidence needed before LLM comparison claims are made.
