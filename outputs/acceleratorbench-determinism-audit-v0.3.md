# FounderBench v0.3 Determinism Audit

Replay audit showing included deterministic baselines reproduce stable task outcomes from fixed seeds.

## Scope

| Field | Value |
| --- | --- |
| policies | ['random', 'conservative', 'heuristic', 'task_heuristic'] |
| seed | 0 |
| runs_per_policy | 2 |
| excluded_fields | ['decision_latency_s'] |
| exclusion_rationale | Wall-clock decision latency is environment-dependent and excluded from stable-result hashing. |

## Replay Results

| Policy | Seed | Tasks | Stable Hash Match | Score Match | Solved Match | First Hash | Second Hash |
| --- | --- | --- | --- | --- | --- | --- | --- |
| random | 0 | 50 | True | True | True | c0fe61bb322e | c0fe61bb322e |
| conservative | 0 | 50 | True | True | True | 764bf94c852b | 764bf94c852b |
| heuristic | 0 | 50 | True | True | True | 39bb7136c475 | 39bb7136c475 |
| task_heuristic | 0 | 50 | True | True | True | b7d006ee63f8 | b7d006ee63f8 |

## Summary

| Metric | Value |
| --- | --- |
| policies | 4 |
| stable_matches | 4 |
| score_matches | 4 |
| solved_matches | 4 |
| all_stable | True |

## Validation

Status: PASS

All included deterministic baselines reproduced stable outcomes from fixed seeds. Wall-clock latency fields were excluded from stable-result hashes.
