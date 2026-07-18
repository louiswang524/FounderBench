# FounderBench Baseline Execution Plan

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
- Run every required model on the same 50 current task ids.
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
| deepseek_single | deepseek | hosted | required | 50 | outputs/founderbench-deepseek.json | outputs/founderbench-deepseek-submission-report.md | outputs/founderbench-deepseek-repeats.json |
| deepseek_sc_k3 | deepseek_sc | hosted | recommended | 50 | outputs/founderbench-deepseek-sc-k3.json | outputs/founderbench-deepseek-sc-k3-submission-report.md | outputs/founderbench-deepseek-sc-k3-repeats.json |
| anthropic_single | anthropic | hosted | required | 50 | outputs/founderbench-anthropic.json | outputs/founderbench-anthropic-submission-report.md | outputs/founderbench-anthropic-repeats.json |
| gemini_single | gemini | hosted | required | 50 | outputs/founderbench-gemini.json | outputs/founderbench-gemini-submission-report.md | outputs/founderbench-gemini-repeats.json |
| local_open_model_single | llm | local_open_source | required | 50 | outputs/founderbench-local-open-model.json | outputs/founderbench-local-open-model-submission-report.md | outputs/founderbench-local-open-model-repeats.json |

## Commands

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
