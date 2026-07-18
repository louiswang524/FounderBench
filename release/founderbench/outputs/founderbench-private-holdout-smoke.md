# FounderBench Private Holdout Smoke Report

This generated report is a smoke test for the private-holdout evaluator harness. It uses a disclosed public smoke secret and must not be reported as an official hidden-holdout leaderboard.

Status: `smoke_test_only_not_official_holdout`

Policy: `conservative`
Run seed: `0`

## Claim Guardrail

Do not report this smoke result as an official private leaderboard, hidden holdout score, or model-comparison result.

## Summary

| Metric | Value |
| --- | --- |
| private_tasks | 20 |
| private_solved | 6 |
| private_solve_rate | 0.3 |
| private_average_task_score | 53.02 |
| private_invalid_actions | 0 |
| private_over_budget_decisions | 0 |
| private_provider_errors | 0 |
| contains_raw_private_results | False |

## Public Report Fields

- `private_tasks`: 20
- `private_solved`: 6
- `private_solve_rate`: 0.3
- `private_average_task_score`: 53.02
- `private_provider_errors`: 0
- `private_invalid_actions`: 0
- `private_over_budget_decisions`: 0
- `private_estimated_provider_cost_usd`: 0.0
- `fingerprint_manifest_sha256`: 79ccf170547cfb8e1a7c9f181e2a3498fc29c3b76fd1ef1ea941bb2d88fb9047

## Validation

Status: PASS

The private-holdout evaluator harness executed aggregate-only smoke reporting without exposing raw private task results.
