# FounderBench v0.3 Ablation Report

This report treats the four deterministic non-LLM baselines as a capability ladder. It does not replace hosted LLM ablations, but it provides a reproducible calibration showing which kinds of decision information make the synthetic startup tasks easier.

## Capability Ladder

| Policy | Added Capability | Avg Score | Solved | Score Delta | Delta 95% CI | Solved Delta |
| --- | --- | --- | --- | --- | --- | --- |
| random | No strategic prior; samples legal business actions stochastically. | 33.30 | 4 | n/a | n/a | n/a |
| conservative | Adds runway preservation and cautious offer/support behavior. | 54.04 | 13 | +20.74 | [+14.73, +26.52] | +9 |
| heuristic | Adds generic market scoring, pricing correction, acquisition, quality, and support rules. | 61.01 | 19 | +6.97 | [+2.55, +11.16] | +6 |
| task_heuristic | Adds task-family conditioning, analogous to an agent correctly inferring the operating mode. | 80.90 | 37 | +19.90 | [+13.64, +26.13] | +18 |

## Task-Conditioning Gain by Family

This table compares `task_heuristic` against the generic `heuristic` policy. Large gains mean the family rewards correctly identifying the startup operating situation rather than only applying generic growth rules.

| Family | Avg Score Gain | Heuristic Solved | Task-Heuristic Solved | Solved Gain |
| --- | --- | --- | --- | --- |
| Churn shock recovery | +43.07 | 1/5 | 5/5 | +4 |
| Pivot decision | +38.64 | 0/5 | 2/5 | +2 |
| Retention improvement | +32.26 | 2/5 | 5/5 | +3 |
| Fundraising | +31.61 | 0/5 | 5/5 | +5 |
| Demo Day traction | +21.87 | 3/5 | 4/5 | +1 |
| Channel expansion | +15.83 | 0/5 | 2/5 | +2 |
| Runway preservation | +13.07 | 5/5 | 5/5 | +0 |
| First revenue | +3.55 | 2/5 | 2/5 | +0 |
| Pricing | +0.38 | 4/5 | 5/5 | +1 |
| Market selection | -1.31 | 2/5 | 2/5 | +0 |

## Interpretation

- The ladder separates blind action selection, cash-preserving operations, generic startup operating logic, and explicit task-family conditioning.
- If future LLM baselines only beat `random` or `conservative`, the benchmark is mostly testing basic action validity and runway awareness.
- If future LLM baselines beat `heuristic`, the evidence is stronger that they infer operating context and choose family-appropriate actions.
- If future LLM baselines beat `task_heuristic`, the benchmark provides evidence beyond the current hand-coded task-family prior.
