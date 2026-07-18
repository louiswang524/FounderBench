# FounderBench v0.3 Task Feasibility and Discrimination Audit

Task-level feasibility and discrimination audit for paper review. It summarizes which public tasks are solved by at least one deterministic baseline, which remain unsolved by deterministic baselines, and which tasks are likely to differentiate future hosted/local LLM providers.

Calibration scope: `deterministic_rule_baselines_only`

Claim guardrail:

Tasks unsolved by deterministic baselines are not impossible claims; they require hosted/local LLM, human/expert, or reference-solution calibration before stronger feasibility claims.

## Summary

| Metric | Value |
| --- | --- |
| tasks | 50 |
| families | 10 |
| baseline_solved_tasks | 39 |
| needs_external_calibration | 11 |
| saturated_by_deterministic_baselines | 2 |
| high_discrimination_tasks | 26 |
| mean_score_spread | 51.47 |

## Difficulty Bands

| Band | Tasks |
| --- | --- |
| easy | 10 |
| hard | 19 |
| medium | 8 |
| saturated | 2 |
| unsolved_by_baselines | 11 |

## Family Feasibility

| Family | Tasks | Baseline Solved | Needs External Calibration | High Discrimination | Expected Actions |
| --- | --- | --- | --- | --- | --- |
| Market selection | 5 | 3 | 2 | 3 | build_offer, research_market |
| First revenue | 5 | 3 | 2 | 3 | build_offer, change_price, run_campaign |
| Retention improvement | 5 | 5 | 0 | 5 | improve_offer, support_customers |
| Churn shock recovery | 5 | 5 | 0 | 4 | hire_agent, improve_offer, support_customers |
| Demo Day traction | 5 | 4 | 1 | 4 | improve_offer, raise_funding, run_campaign |
| Pricing | 5 | 5 | 0 | 2 | change_price, interview_customers, run_campaign |
| Runway preservation | 5 | 5 | 0 | 1 | cut_cost, do_nothing, support_customers |
| Pivot decision | 5 | 2 | 3 | 2 | interview_customers, pivot_market, research_market |
| Fundraising | 5 | 5 | 0 | 1 | raise_funding, run_campaign, support_customers |
| Channel expansion | 5 | 2 | 3 | 1 | hire_agent, partner_channel, run_campaign |

## Tasks Needing External Calibration

| Task | Family | Split | Best Policy | Best Score | Spread | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| FND-004 | Market selection | public_dev | conservative | 41.19 | 12.11 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-005 | Market selection | public_dev | conservative | 41.19 | 22.15 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-007 | First revenue | public_dev | task_heuristic | 63.98 | 38.9 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-010 | First revenue | public_dev | task_heuristic | 46.46 | 21.8 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-025 | Demo Day traction | public_dev | task_heuristic | 69.7 | 39.22 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-036 | Pivot decision | public_test | task_heuristic | 55.92 | 49.08 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-037 | Pivot decision | public_test | task_heuristic | 49.18 | 49.18 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-039 | Pivot decision | public_test | task_heuristic | 49.12 | 18.17 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-046 | Channel expansion | public_test | heuristic | 38.86 | 16.72 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-047 | Channel expansion | public_test | task_heuristic | 45.1 | 29.6 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |
| FND-050 | Channel expansion | public_test | heuristic | 43.39 | 26.7 | Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines. |

## High-Discrimination Tasks

| Task | Family | Band | Best Policy | Best Score | Spread |
| --- | --- | --- | --- | --- | --- |
| FND-011 | Retention improvement | hard | task_heuristic | 100.0 | 90.07 |
| FND-012 | Retention improvement | hard | task_heuristic | 90.0 | 90.0 |
| FND-013 | Retention improvement | medium | task_heuristic | 93.33 | 89.76 |
| FND-015 | Retention improvement | medium | task_heuristic | 100.0 | 85.0 |
| FND-021 | Demo Day traction | easy | task_heuristic | 93.42 | 81.88 |
| FND-006 | First revenue | easy | task_heuristic | 88.75 | 81.52 |
| FND-024 | Demo Day traction | medium | task_heuristic | 92.19 | 79.48 |
| FND-020 | Churn shock recovery | hard | task_heuristic | 92.0 | 78.32 |
| FND-023 | Demo Day traction | easy | task_heuristic | 96.67 | 78.09 |
| FND-038 | Pivot decision | hard | task_heuristic | 83.82 | 76.52 |
| FND-040 | Pivot decision | hard | task_heuristic | 89.35 | 75.99 |
| FND-014 | Retention improvement | hard | task_heuristic | 95.59 | 71.89 |
| FND-028 | Pricing | easy | heuristic | 94.33 | 68.82 |
| FND-048 | Channel expansion | hard | task_heuristic | 80.66 | 68.42 |
| FND-017 | Churn shock recovery | hard | task_heuristic | 92.0 | 68.15 |
| FND-002 | Market selection | hard | heuristic | 94.08 | 65.75 |
| FND-022 | Demo Day traction | hard | task_heuristic | 92.14 | 64.31 |
| FND-009 | First revenue | hard | heuristic | 84.07 | 59.65 |
| FND-003 | Market selection | medium | conservative | 96.19 | 59.52 |
| FND-044 | Fundraising | hard | task_heuristic | 100.0 | 59.08 |

## Full Task Ledger

| Task | Family | Split | Band | Feasibility | Solved By | Best Policy | Best Score | Spread |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FND-001 | Market selection | public_dev | easy | baseline_solved | 3/4 | conservative | 96.19 | 51.19 |
| FND-002 | Market selection | public_dev | hard | baseline_solved | 1/4 | heuristic | 94.08 | 65.75 |
| FND-003 | Market selection | public_dev | medium | baseline_solved | 2/4 | conservative | 96.19 | 59.52 |
| FND-004 | Market selection | public_dev | unsolved_by_baselines | needs_external_calibration | 0/4 | conservative | 41.19 | 12.11 |
| FND-005 | Market selection | public_dev | unsolved_by_baselines | needs_external_calibration | 0/4 | conservative | 41.19 | 22.15 |
| FND-006 | First revenue | public_dev | easy | baseline_solved | 3/4 | task_heuristic | 88.75 | 81.52 |
| FND-007 | First revenue | public_dev | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 63.98 | 38.9 |
| FND-008 | First revenue | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 77.5 | 57.04 |
| FND-009 | First revenue | public_dev | hard | baseline_solved | 1/4 | heuristic | 84.07 | 59.65 |
| FND-010 | First revenue | public_dev | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 46.46 | 21.8 |
| FND-011 | Retention improvement | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 100.0 | 90.07 |
| FND-012 | Retention improvement | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 90.0 | 90.0 |
| FND-013 | Retention improvement | public_dev | medium | baseline_solved | 2/4 | task_heuristic | 93.33 | 89.76 |
| FND-014 | Retention improvement | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 95.59 | 71.89 |
| FND-015 | Retention improvement | public_dev | medium | baseline_solved | 2/4 | task_heuristic | 100.0 | 85.0 |
| FND-016 | Churn shock recovery | public_dev | medium | baseline_solved | 2/4 | task_heuristic | 86.72 | 45.72 |
| FND-017 | Churn shock recovery | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 92.0 | 68.15 |
| FND-018 | Churn shock recovery | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 92.0 | 54.51 |
| FND-019 | Churn shock recovery | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 93.19 | 51.82 |
| FND-020 | Churn shock recovery | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 92.0 | 78.32 |
| FND-021 | Demo Day traction | public_dev | easy | baseline_solved | 3/4 | task_heuristic | 93.42 | 81.88 |
| FND-022 | Demo Day traction | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 92.14 | 64.31 |
| FND-023 | Demo Day traction | public_dev | easy | baseline_solved | 3/4 | task_heuristic | 96.67 | 78.09 |
| FND-024 | Demo Day traction | public_dev | medium | baseline_solved | 2/4 | task_heuristic | 92.19 | 79.48 |
| FND-025 | Demo Day traction | public_dev | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 69.7 | 39.22 |
| FND-026 | Pricing | public_dev | easy | baseline_solved | 3/4 | task_heuristic | 99.44 | 40.52 |
| FND-027 | Pricing | public_dev | hard | baseline_solved | 1/4 | task_heuristic | 79.13 | 51.89 |
| FND-028 | Pricing | public_dev | easy | baseline_solved | 3/4 | heuristic | 94.33 | 68.82 |
| FND-029 | Pricing | public_dev | medium | baseline_solved | 2/4 | task_heuristic | 87.29 | 48.18 |
| FND-030 | Pricing | public_dev | easy | baseline_solved | 3/4 | task_heuristic | 86.44 | 38.78 |
| FND-031 | Runway preservation | public_test | saturated | saturated_by_deterministic_baselines | 4/4 | task_heuristic | 95.96 | 16.3 |
| FND-032 | Runway preservation | public_test | saturated | saturated_by_deterministic_baselines | 4/4 | task_heuristic | 98.97 | 17.18 |
| FND-033 | Runway preservation | public_test | easy | baseline_solved | 3/4 | task_heuristic | 92.53 | 26.53 |
| FND-034 | Runway preservation | public_test | easy | baseline_solved | 3/4 | task_heuristic | 93.79 | 30.23 |
| FND-035 | Runway preservation | public_test | easy | baseline_solved | 3/4 | task_heuristic | 96.65 | 54.55 |
| FND-036 | Pivot decision | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 55.92 | 49.08 |
| FND-037 | Pivot decision | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 49.18 | 49.18 |
| FND-038 | Pivot decision | public_test | hard | baseline_solved | 1/4 | task_heuristic | 83.82 | 76.52 |
| FND-039 | Pivot decision | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 49.12 | 18.17 |
| FND-040 | Pivot decision | public_test | hard | baseline_solved | 1/4 | task_heuristic | 89.35 | 75.99 |
| FND-041 | Fundraising | public_test | hard | baseline_solved | 1/4 | task_heuristic | 100.0 | 32.0 |
| FND-042 | Fundraising | public_test | medium | baseline_solved | 2/4 | task_heuristic | 100.0 | 32.0 |
| FND-043 | Fundraising | public_test | hard | baseline_solved | 1/4 | task_heuristic | 100.0 | 45.1 |
| FND-044 | Fundraising | public_test | hard | baseline_solved | 1/4 | task_heuristic | 100.0 | 59.08 |
| FND-045 | Fundraising | public_test | medium | baseline_solved | 2/4 | random | 100.0 | 32.0 |
| FND-046 | Channel expansion | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | heuristic | 38.86 | 16.72 |
| FND-047 | Channel expansion | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | task_heuristic | 45.1 | 29.6 |
| FND-048 | Channel expansion | public_test | hard | baseline_solved | 1/4 | task_heuristic | 80.66 | 68.42 |
| FND-049 | Channel expansion | public_test | hard | baseline_solved | 1/4 | task_heuristic | 83.02 | 32.29 |
| FND-050 | Channel expansion | public_test | unsolved_by_baselines | needs_external_calibration | 0/4 | heuristic | 43.39 | 26.7 |

## Validation

Status: PASS

The feasibility audit covers all 50 tasks, preserves external-calibration needs, and identifies high-discrimination tasks for future model comparisons.
