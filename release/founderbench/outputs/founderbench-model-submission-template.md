# FounderBench Model Submission Template

Use this template when reporting a model run on FounderBench.

The machine-readable companion schema is `outputs/founderbench-model-submission-schema.json`; the human-readable schema summary is `outputs/founderbench-model-submission-schema.md`.

## Model Card

```yaml
benchmark: FounderBench
benchmark_version: 0.3.0
submission_date: YYYY-MM-DD
provider: provider-name
model: model-name
model_version_or_snapshot: exact-version-if-available
endpoint_type: hosted | local-openai-compatible | other
agent_method: single-call | provider-adapter | other
temperature: 0.2
max_output_tokens: 900
prompt_version: current release-default
tasks: 50
split_policy: public_dev + public_test
```

## Required Result Summary

```json
{
  "policy": "provider/model-name",
  "benchmark_version": "0.3.0",
  "tasks": 50,
  "solved": 0,
  "solve_rate": 0.0,
  "average_task_score": 0.0,
  "public_dev_score": 0.0,
  "public_test_score": 0.0,
  "shutdown_rate": 0.0,
  "average_final_cash": 0.0,
  "average_risk_penalty": 0.0,
  "invalid_actions": 0,
  "over_budget_decisions": 0,
  "provider_errors": 0,
  "provider_error_categories": {},
  "avg_actions_per_task": 0.0,
  "simulated_api_cost": 0.0,
  "provider_total_tokens": 0,
  "estimated_provider_cost_usd": 0.0,
  "decision_latency_s": 0.0
}
```

## Required Artifacts

- Leaderboard JSON.
- Raw result JSON with task-level scores and diagnostics.
- Redacted audit trace for at least one representative failure and one representative success.
- Provider error-category counts, including malformed JSON/schema failures.
- Prompt/method description.
- Model/provider version information.
- Cost assumptions used for `estimated_provider_cost_usd`.

## Recommended Command

```powershell
python -m founderbench.resumable_runner --policy deepseek --output outputs/provider-run.json --resume
```

For local/open-source OpenAI-compatible servers:

```powershell
$env:FOUNDERBENCH_COMPAT_BASE_URL="http://localhost:8000/v1"
$env:FOUNDERBENCH_COMPAT_MODEL="Qwen/Qwen2.5-7B-Instruct"
python -m founderbench.local_model health --output outputs/local-health.json
python -m founderbench.resumable_runner --policy llm --output outputs/local-open-model-run.json --resume --audit
```

The runner uses `${FOUNDERBENCH_COMPAT_BASE_URL}/chat/completions`; the health command uses `${FOUNDERBENCH_COMPAT_BASE_URL}/models`.

For redacted provider-call records:

```powershell
python -m founderbench.resumable_runner --policy deepseek --output outputs/provider-run-audit.json --resume --audit
```

Set provider price assumptions through:

```powershell
$env:MODEL_INPUT_COST_PER_MILLION="0.00"
$env:MODEL_OUTPUT_COST_PER_MILLION="0.00"
```

## Submission Validation

Before reporting a model result, validate the raw run JSON:

```powershell
python -m founderbench.submission --input outputs/provider-run.json --report outputs/provider-run-submission-report.md
```

The validator checks that the run covers all 50 current tasks, includes both public splits, preserves task-level scores, reports required diagnostics, and keeps provider-error category counts consistent with total provider errors. For repeated-sampling studies, submit a JSON list of run objects or `{ "runs": [...] }`; the generated report will include repeated-run confidence intervals.

## Statistical Comparison Protocol

Model comparisons should follow `outputs/founderbench-statistical-protocol.md`: use `average_task_score` as the primary endpoint, compare single runs with paired task-level gaps, report bootstrap intervals and random sign-flip permutation tests, use Holm-Bonferroni adjustment for main leaderboard pairwise comparisons, and keep raw money/revenue/cash as diagnostics rather than primary cross-task outcomes.

## Redaction Requirement

Submitted logs must not contain API keys or credentials. FounderBench audit mode redacts common key patterns, but submitters must still inspect logs before release.

## Reporting Notes

- Do not discard failed tasks.
- Report provider errors as benchmark outcomes.
- Report invalid JSON/action failures instead of manually repairing them outside the adapter.
- If a local model is used, report hardware, inference server, quantization, and decoding settings.
