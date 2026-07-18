# FounderBench Simulator Invariant Audit

This generated audit stress-tests simulator mechanics and task-score bounds. It is a software-validity check, not a claim that the simulator captures real startup dynamics.

Status: `simulator_invariants_validated_for_stress_scenarios`

## Summary

| Metric | Value |
| --- | --- |
| scenarios | 5 |
| scenarios_passed | 5 |
| scenario_steps | 14 |
| task_score_policy | conservative |
| task_scores_bounded | True |
| pass_flags_match_threshold | True |

## Invariants Checked

- week advances monotonically until bankruptcy/done
- cash and profit remain finite
- reputation remains in [0, 1]
- agent capacity and cumulative revenue/API cost/funding/risk remain nonnegative
- offer customers and age remain nonnegative
- offer quality and awareness remain in [0, 1]
- task scores remain in [0, 100] and pass flags match the 70-point threshold

## Stress Scenarios

| Scenario | Seed | Steps | Passed | Final Cash | Final Reputation | Bankrupt |
| --- | --- | --- | --- | --- | --- | --- |
| hold_position | 101 | 3 | yes | 10000.0 | 0.55 | False |
| build_and_support | 102 | 4 | yes | 5630.0 | 0.574 | False |
| unknown_targets_are_risky | 103 | 3 | yes | 8300.0 | 0.398 | False |
| overbudget_bankruptcy_path | 104 | 1 | yes | -15000.0 | 0.46 | True |
| runway_cost_cut_path | 105 | 3 | yes | 8230.0 | 0.57 | False |

## Task Score Bounds

| Policy | Tasks | Min Score | Max Score | Scores Bounded | Pass Flags Match Threshold |
| --- | --- | --- | --- | --- | --- |
| conservative | 50 | 19.1 | 96.19 | True | True |

## Claim Guardrail

This audit checks simulator mechanics and task-score bounds only; it does not validate real-world startup dynamics or unlock hosted/local LLM result claims.

## Validation

Status: PASS

Stress scenarios and task-score bounds satisfy the declared simulator invariants.
