# FounderBench Model Submission Schema

Machine-readable schema for raw model run submissions. The authoritative validator remains python -m moneybench.submission, which also checks task-id set equality and diagnostic consistency.

## Accepted Payload Shapes

| Shape |
| --- |
| single run object |
| array of run objects |
| object with runs array |

## Required Run Fields

| Field |
| --- |
| policy |
| benchmark_version |
| tasks |
| solved |
| solve_rate |
| average_task_score |
| results |
| diagnostics |
| splits |

## Required Diagnostics

| Diagnostic |
| --- |
| decision_latency_s |
| estimated_provider_cost_usd |
| invalid_actions |
| over_budget_decisions |
| provider_completion_tokens |
| provider_error_categories |
| provider_errors |
| provider_prompt_tokens |
| provider_total_tokens |
| simulated_api_cost |
| total_actions |

## Task Coverage

- Required task ids: 50
- Required splits: `public_dev`, `public_test`
- Every valid single run must contain exactly 50 task results.

## Authoritative Validation

`python -m moneybench.submission --input outputs/provider-run.json --report outputs/provider-run-submission-report.md`

The JSON schema documents field shape. The Python validator additionally checks exact task-id coverage, split summaries, score typing, diagnostic consistency, and repeated-run payloads.

## Validation

Status: PASS

The schema is internally consistent with the current release submission validator.
