# FounderBench Leaderboard Policy

This generated policy defines how public model submissions, repeated runs, and future private-holdout reports should be accepted, ranked, reported, or rejected.

Status: `public_leaderboard_policy_ready_private_leaderboard_not_executed`

## Summary

| Metric | Value |
| --- | --- |
| tiers | 3 |
| public_tier_active | True |
| private_leaderboard_included | False |
| acceptance_rules | 6 |
| rejection_rules | 6 |
| reporting_fields | 9 |

## Leaderboard Tiers

| Tier | Status | Eligible Inputs | Ranking Metric | Claim Scope |
| --- | --- | --- | --- | --- |
| public_open | active_for_current release | Validated 50-task public_dev/public_test submissions. | average_task_score | Visible public benchmark score; not hidden, private, or contamination-free. |
| public_repeated | supported_when_repeat_bundle_validates | Validated repeated-run bundle with unique policy/run_seed identities. | mean average_task_score across submitted runs | Stochastic public-run estimate; still visible public tasks. |
| private_holdout | protocol_only_not_executed_current release | Evaluator-hosted aggregate private report generated from secret-held private tasks. | private_average_task_score | Hidden-suite score only after official evaluator execution; no such leaderboard is included in current release. |

## Acceptance Rules

- Submission must pass `python -m founderbench.submission` with exactly 50 public task results unless it is an evaluator-host private report.
- Run JSON must report benchmark_version 0.3.0, both public splits, required diagnostics, provider-error categories, and run_seed when used for repeated runs.
- Provider errors, invalid actions, bankruptcies, over-budget decisions, and timeouts remain in the denominator.
- Hosted/local provider rows are excluded until the raw run and submission report both exist and validate.
- Self-consistency or reflection variants must be reported as separate ablations unless pre-registered as the primary policy.
- Model submitters must disclose prompt/agent tuning on public tasks and whether the submitted model was trained or fine-tuned on released tasks.

## Rejection Rules

- Missing or extra public task ids.
- Manual repair of model outputs outside the adapter/parser contract.
- Dropped failed tasks or omitted provider-error diagnostics.
- Duplicate policy/run_seed identities in a repeated-run bundle.
- Unredacted secrets in public audit traces.
- Claims that public_test is hidden, private, unseen, or contamination-free.

## Reporting Fields

- `model/provider/name and version`
- `policy id and adapter commit/source state`
- `prompt/protocol version and hashes`
- `task count and split visibility`
- `run_seed or repeated-run bundle summary`
- `average_task_score, solved, solve_rate, and family/split summaries`
- `provider errors, invalid actions, over-budget decisions, timeouts, and parser categories`
- `token usage and estimated provider cost when available`
- `audit trace availability and redaction status`

## Claim Guardrails

- Do not merge public and private results into one leaderboard without labeling tiers.
- Do not treat task-aware heuristic rows as LLM-agent baselines.
- Do not use public leaderboard rows to claim hidden-suite robustness.
- Do not rank missing or invalid provider submissions.

## Validation

Status: PASS

Leaderboard policy is internally consistent and keeps public and private result tiers separate.
