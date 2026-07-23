# FounderBench Frozen Private Holdout Calibration

Aggregate-only deterministic baselines on the frozen 20-task private holdout.

Status: `frozen_private_calibration_only`

## Claim Guardrail

These are deterministic calibration rows on the frozen private holdout. They are not an official hosted private leaderboard.

Secret commitment (SHA-256 of secret): `8d75465b105f4ace28659ea904b55d47cb75d1668bb1fc48e25769bc10253814`

Fingerprint manifest SHA-256: `ef730c722de6e555b02a46f2aae913eba847fe338aab74b5a7d8b0fefb34d9d9`

## Baselines

| Policy | Private avg score | Solved | Solve rate |
| --- | --- | --- | --- |
| random | 33.33 | 3/20 | 0.15 |
| conservative | 50.53 | 5/20 | 0.25 |
| heuristic | 57.49 | 6/20 | 0.3 |
| task_heuristic | 54.81 | 4/20 | 0.2 |

## Notes

- Private task definitions are generated from the evaluator-held secret and are not published.
- Hosted model private-holdout runs are not included in this freeze.
- Public `public_test` remains visible and is not a hidden split.
