# FounderBench v0.3 Task Coverage Report

This generated report summarizes the fixed public task suite used by the benchmark. It complements the task manifest by explaining family balance, split balance, action coverage, and intended capability coverage.

## Summary

| Metric | Value |
| --- | --- |
| families | 10 |
| tasks_per_family_min | 5 |
| tasks_per_family_max | 5 |
| public_dev_tasks | 30 |
| public_test_tasks | 20 |
| action_types_available | 13 |
| expected_action_types | 13 |
| missing_allowed_actions | [] |
| weeks_min | 7 |
| weeks_max | 14 |
| weeks_mean | 9.5 |
| pass_threshold_min | 70.0 |
| pass_threshold_max | 70.0 |

## Split Balance

| Split | Tasks |
| --- | --- |
| public_dev | 30 |
| public_test | 20 |

## Family Coverage

| Family | Tasks | Task IDs | Expected Actions | Capabilities |
| --- | --- | --- | --- | --- |
| Market selection | 5 | FND-001, FND-002, FND-003, FND-004, FND-005 | build_offer, research_market | market research, opportunity selection, early commitment under uncertainty |
| First revenue | 5 | FND-006, FND-007, FND-008, FND-009, FND-010 | build_offer, change_price, run_campaign | offer building, campaign execution, cash-efficient customer acquisition |
| Retention improvement | 5 | FND-011, FND-012, FND-013, FND-014, FND-015 | improve_offer, support_customers | product quality improvement, support, churn prevention |
| Churn shock recovery | 5 | FND-016, FND-017, FND-018, FND-019, FND-020 | hire_agent, improve_offer, support_customers | triage after customer loss, support scaling, reputation recovery |
| Demo Day traction | 5 | FND-021, FND-022, FND-023, FND-024, FND-025 | improve_offer, raise_funding, run_campaign | traction building, growth pacing, credible fundraising preparation |
| Pricing | 5 | FND-026, FND-027, FND-028, FND-029, FND-030 | change_price, interview_customers, run_campaign | price correction, willingness-to-pay inference, revenue/customer tradeoff |
| Runway preservation | 5 | FND-031, FND-032, FND-033, FND-034, FND-035 | cut_cost, do_nothing, support_customers | cost control, survival under limited cash, tradeoff-aware operations |
| Pivot decision | 5 | FND-036, FND-037, FND-038, FND-039, FND-040 | interview_customers, pivot_market, research_market | recognizing stalled markets, customer discovery, market switching |
| Fundraising | 5 | FND-041, FND-042, FND-043, FND-044, FND-045 | raise_funding, run_campaign, support_customers | capital raising, traction signaling, reputation and risk management |
| Channel expansion | 5 | FND-046, FND-047, FND-048, FND-049, FND-050 | hire_agent, partner_channel, run_campaign | partnerships, scaling working offers, channel-risk control |

## Action Coverage

`Allowed In Tasks` counts how many tasks permit each action. `Expected By Family` counts how many task instances belong to families where the action is strategically relevant.

| Action | Allowed In Tasks | Expected By Family |
| --- | --- | --- |
| build_offer | 50 | 10 |
| change_price | 50 | 10 |
| cut_cost | 50 | 5 |
| do_nothing | 50 | 5 |
| hire_agent | 50 | 10 |
| improve_offer | 50 | 15 |
| interview_customers | 50 | 10 |
| partner_channel | 50 | 5 |
| pivot_market | 50 | 5 |
| raise_funding | 50 | 10 |
| research_market | 50 | 10 |
| run_campaign | 50 | 25 |
| support_customers | 50 | 20 |

## Validation

Status: PASS

The public task suite has 50 tasks, 10 balanced families, 30 public development tasks, 20 public test tasks, and all 13 structured action types are available.
