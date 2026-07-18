# FounderBench Task Provenance

Task curation and provenance record for the fixed current release public suite.

## Summary

| Metric | Value |
| --- | --- |
| tasks | 50 |
| templates | 10 |
| public_dev | 30 |
| public_test | 20 |
| real_world_data_used | False |
| human_subject_data_used | False |
| all_templates_have_five_tasks | True |

## Curation Method

| Field | Value |
| --- | --- |
| source | Hand-designed synthetic startup templates encoded in work/founderbench/founderbench/tasks.py. |
| template_count | 10 |
| variants_per_template | 5 |
| public_split_rule | FND-001..FND-030 are public_dev; FND-031..FND-050 are public_test. |
| private_holdout_status | Blueprint/protocol only; private task definitions are not included in current release. |
| real_world_data_used | False |
| human_subject_data_used | False |
| external_private_data_used | False |

## Template Provenance

| Family | Range | Task IDs | Construction | Seed Rule | Setup Source | Score Source |
| --- | --- | --- | --- | --- | --- | --- |
| Market selection | FND-001..FND-005 | FND-001, FND-002, FND-003, FND-004, FND-005 | hand-authored viable-market target sets over no_setup initial states | literal seed list [11, 41, 43, 47, 53] | no_setup | make_market_selection_score |
| First revenue | FND-006..FND-010 | FND-006, FND-007, FND-008, FND-009, FND-010 | template loop over no_setup initial states with customer/revenue/cash targets | literal seed list [7, 59, 61, 67, 71] | no_setup | make_first_revenue_score |
| Retention improvement | FND-011..FND-015 | FND-011, FND-012, FND-013, FND-014, FND-015 | five hand-authored existing-offer startup states | 19 + task_number | setup_existing_offer | make_retention_score |
| Churn shock recovery | FND-016..FND-020 | FND-016, FND-017, FND-018, FND-019, FND-020 | five overloaded existing-offer states with support/retention pressure | 23 + task_number | setup_churn_shock | make_churn_shock_score |
| Demo Day traction | FND-021..FND-025 | FND-021, FND-022, FND-023, FND-024, FND-025 | five demo-day growth states with existing traction | 31 + task_number | setup_demo_day | make_demo_day_score |
| Pricing | FND-026..FND-030 | FND-026, FND-027, FND-028, FND-029, FND-030 | five existing-offer states with intentionally weak starting prices | 37 + task_number | setup_existing_offer | make_pricing_score |
| Runway preservation | FND-031..FND-035 | FND-031, FND-032, FND-033, FND-034, FND-035 | five low-cash existing-offer states requiring tradeoff-aware operations | 41 + task_number | setup_existing_offer | make_runway_score |
| Pivot decision | FND-036..FND-040 | FND-036, FND-037, FND-038, FND-039, FND-040 | five stalled-offer states with target market sets | 43 + task_number | setup_existing_offer with current market pre-researched | make_pivot_score |
| Fundraising | FND-041..FND-045 | FND-041, FND-042, FND-043, FND-044, FND-045 | five traction states where credible fundraising depends on operations | 47 + task_number | setup_demo_day | make_fundraising_score |
| Channel expansion | FND-046..FND-050 | FND-046, FND-047, FND-048, FND-049, FND-050 | five under-distributed working-offer states | 53 + task_number | setup_existing_offer | make_channel_score |

## Notes

- current release is a controlled synthetic benchmark suite, not a dataset mined from real companies.
- The task templates are public in source code; private hidden evaluation is reserved for a future evaluator-hosted cycle.
- This provenance record should be cited alongside the task manifest, task-card catalog, and validity report.

## Validation

Status: PASS

All 50 public tasks trace to 10 documented synthetic templates with explicit split, seed, setup, and scoring provenance.
