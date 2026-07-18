# FounderBench Contamination and Leakage Audit

This generated audit keeps public-split visibility, trace leakage surfaces, and private-holdout claim limits explicit. It does not certify the public suite as contamination-free.

Status: `public_suite_visible_private_holdout_not_executed`

## Summary

| Metric | Value |
| --- | --- |
| public_tasks | 50 |
| public_dev | 30 |
| public_test | 20 |
| private_holdout_protocol_exists | True |
| official_private_leaderboard | False |
| contamination_free_claim_supported | False |
| leakage_surfaces | 5 |
| claim_guardrails | 5 |
| required_reviewer_checks | 6 |

## Split Controls

| Split | Tasks | Visibility | Hidden | Claim Rule |
| --- | --- | --- | --- | --- |
| public_dev | 30 | released | no | Development evidence only; not an unseen generalization estimate. |
| public_test | 20 | released | no | Public benchmark score; not a private holdout or contamination-free score. |
| private_holdout | 20 | evaluator_controlled_protocol_only | yes | Hidden-suite claims require official evaluator aggregate results; current release has no official private leaderboard. |

## Leakage Surfaces

| ID | Status | Surface | Mitigation |
| --- | --- | --- | --- |
| released_public_task_definitions | known_visible | Public task definitions, task cards, coverage reports, seeds, allowed actions, and scoring metadata are included in the repository and supplementary package. | Treat public_dev and public_test as visible public splits; require disclosure for tuned agents and use a private evaluator-hosted holdout for hidden-suite claims. |
| prompt_contains_current_task_context | intended_task_context | Provider prompts include the current task id, task description, observation, allowed actions, and response schema. | Freeze prompt hashes and action schema so providers receive comparable task context without hidden evaluator metadata. |
| audit_traces_can_contain_prompts_or_responses | redaction_and_review_required | Provider audit logs may contain prompts, redacted raw responses, parser failures, token usage, and latency metadata. | Redact secrets and review traces before release; never publish private-holdout prompts or raw private task definitions during an active cycle. |
| older_provider_like_outputs | excluded_until_validated | Older exploratory provider-like files may exist in local workspaces and can have mismatched prompts, task counts, or benchmark versions. | Use provider-run-status, model-result-card, and submission-validation artifacts to exclude invalid or stale provider rows from paper claims. |
| task_aware_heuristic_family_knowledge | calibration_ceiling_not_agent_baseline | The task-aware heuristic encodes task-family knowledge and can overfit the released public suite. | Report it as a calibration ceiling and ablation target, not as evidence that LLM agents can operate startups. |

## Claim Guardrails

- Do not call public_test hidden, unseen, secret, private, or contamination-free.
- Do not claim the benchmark is free from pretraining or post-release contamination; public tasks are intentionally visible.
- Do not treat the aggregate-only private holdout smoke report as an official hidden leaderboard.
- Require model submitters to disclose prompt tuning, agent tuning, or training on public tasks.
- Use only evaluator-hosted private tasks for hidden-suite claims, and report aggregate private fields without private task definitions during an active cycle.

## Required Reviewer Checks

- Confirm submitted model cards disclose whether public tasks were used for prompt, agent, or training development.
- Verify public reports do not describe public_test as hidden or contamination-free.
- Run the evaluator-hosted private holdout before accepting hidden-suite or anti-gaming claims.
- Compare public and private score deltas when official private results become available.
- Check prompt/protocol hashes and exclude runs whose prompts or task counts do not match current release.
- Review released audit traces for secret leakage and keep active private traces aggregate-only.

## Validation

Status: PASS

The audit preserves the distinction between visible public results and future evaluator-hosted private-holdout claims.
