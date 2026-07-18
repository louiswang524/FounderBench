# FounderBench v0.3 Task Revision Ledger

Task and rubric revision ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable benchmark changes.

Status: `open_revision_ledger_no_executed_human_rows`

Scope: `v0.3.0 public task suite and scoring rubric`

## Claim Guardrails

- This ledger is a change-control artifact, not evidence that human calibration has been executed.
- Rows derived from deterministic feasibility audits mark tasks for external calibration; they do not prove task defects.
- Do not modify official task definitions for a paper result after model runs unless the version is incremented and affected claims are regenerated.
- Resolved rows must cite concrete evidence and record whether scores, task text, or paper wording changed.

## Summary

| Metric | Value |
| --- | --- |
| open_revision_rows | 11 |
| status_counts | {'pending_external_calibration': 11} |
| families_with_open_rows | 5 |
| open_rows_by_family | {'Channel expansion': 3, 'Demo Day traction': 1, 'First revenue': 2, 'Market selection': 2, 'Pivot decision': 3} |
| executed_human_revision_rows | 0 |

## Queued Evidence Sources

| Source | Current Status | Expected Input | Ledger Action |
| --- | --- | --- | --- |
| human_calibration_analysis | not_executed | flagged_tasks and recommended_revisions from executed expert/human-founder submissions | Create or update task-level rows with participant-count and conflict-disclosure metadata. |
| hosted_llm_audit_traces | missing | validated redacted provider traces for representative successes and failures | Separate strategic failures from parser/provider failures before revising tasks. |
| private_holdout_evaluator | smoke_only_not_official | evaluator-host aggregate and trace-safe issue reports | Record hidden-suite gaming or robustness issues without exposing private task definitions. |
| reviewer_feedback | not_collected | paper-reviewer or external-auditor comments mapped to task ids or rubric sections | Track decision, owner, and evidence before changing public tasks or claims. |

## Open Revision Rows

| Issue | Task | Family | Split | Status | Best Policy | Best Score | Spread | Revision Question |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| REV-FND-004 | FND-004 | Market selection | public_dev | pending_external_calibration | conservative | 41.19 | 12.11 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-005 | FND-005 | Market selection | public_dev | pending_external_calibration | conservative | 41.19 | 22.15 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-007 | FND-007 | First revenue | public_dev | pending_external_calibration | task_heuristic | 63.98 | 38.9 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-010 | FND-010 | First revenue | public_dev | pending_external_calibration | task_heuristic | 46.46 | 21.8 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-025 | FND-025 | Demo Day traction | public_dev | pending_external_calibration | task_heuristic | 69.7 | 39.22 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-036 | FND-036 | Pivot decision | public_test | pending_external_calibration | task_heuristic | 55.92 | 49.08 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-037 | FND-037 | Pivot decision | public_test | pending_external_calibration | task_heuristic | 49.18 | 49.18 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-039 | FND-039 | Pivot decision | public_test | pending_external_calibration | task_heuristic | 49.12 | 18.17 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-046 | FND-046 | Channel expansion | public_test | pending_external_calibration | heuristic | 38.86 | 16.72 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-047 | FND-047 | Channel expansion | public_test | pending_external_calibration | task_heuristic | 45.1 | 29.6 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |
| REV-FND-050 | FND-050 | Channel expansion | public_test | pending_external_calibration | heuristic | 43.39 | 26.7 | Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored? |

## Required Resolution Evidence

- `REV-FND-004`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-005`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-007`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-010`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-025`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-036`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-037`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-039`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-046`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-047`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.
- `REV-FND-050`: required evidence: hosted/local LLM trajectory on the task; expert/human-founder calibration review; reference action sequence or rubric inspection. Allowed resolutions: keep_without_change_after_external_calibration; revise_task_text_or_constraints; revise_score_rubric; move_to_harder_or_diagnostic_subset; retire_or_replace_in_next_version.

## Validation

Status: PASS

The ledger records open calibration-driven revision questions without claiming executed human or provider evidence.
