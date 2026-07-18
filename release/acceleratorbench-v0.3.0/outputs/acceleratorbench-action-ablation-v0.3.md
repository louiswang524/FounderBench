# FounderBench v0.3 Action-Space Ablation

Action-space ablation of the task-aware heuristic over the full 50-task public suite.

The reference is the task-aware heuristic with all actions enabled. Each ablation filters one action group from that same policy, replaces empty action lists with `do_nothing`, and reruns all 50 tasks.

## Summary

| Metric | Value |
| --- | --- |
| ablations | 7 |
| tasks_per_ablation | 50 |
| reference_score | 80.9 |
| reference_solved | 37 |
| largest_score_drop | 19.41 |
| largest_solved_drop | 15 |

## Ablation Results

| Ablation | Blocked Actions | Avg Score | Solved | Mean Score Drop | Drop 95% CI | Solved Drop | Largest Family Drops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| full_task_heuristic | none | 80.90 | 37 | +0.00 | [+0.00, +0.00] | +0 | Channel expansion +0.00; Churn shock recovery +0.00; Demo Day traction +0.00 |
| no_discovery | research_market, interview_customers | 77.30 | 35 | +3.61 | [-1.08, +8.60] | +2 | Market selection +22.72; Pricing +9.23; Pivot decision +3.36 |
| no_growth | run_campaign, partner_channel | 69.80 | 29 | +11.10 | [+6.49, +15.93] | +8 | First revenue +40.37; Pivot decision +26.91; Channel expansion +23.27 |
| no_quality_support_capacity | improve_offer, support_customers, hire_agent | 61.49 | 22 | +19.41 | [+13.43, +25.99] | +15 | Retention improvement +62.14; Churn shock recovery +53.83; Pivot decision +25.98 |
| no_pricing | change_price | 75.90 | 30 | +5.01 | [+2.04, +8.45] | +7 | Pricing +29.65; Pivot decision +20.41; Channel expansion +0.00 |
| no_runway_funding | cut_cost, raise_funding | 77.74 | 32 | +3.16 | [+0.64, +5.72] | +5 | Fundraising +31.61; Channel expansion +0.00; Churn shock recovery +0.00 |
| no_pivot | pivot_market | 79.92 | 35 | +0.99 | [-0.46, +2.85] | +2 | Pivot decision +9.88; Channel expansion +0.00; Churn shock recovery +0.00 |

## Interpretation

- Large drops indicate that the expanded action space is not decorative: removing the action group changes benchmark outcomes.
- This ablation is a deterministic simulator calibration, not a substitute for hosted LLM ablations.
- Hosted LLM method ablations should report the same primary metrics plus provider cost and error diagnostics.

## Validation

Status: PASS

All action-space ablation runs cover 50 tasks and pass the submission validator.
