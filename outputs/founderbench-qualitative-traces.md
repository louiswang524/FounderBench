# FounderBench Qualitative Trace Examples

These examples are regenerated from deterministic task seeds with `trace=True`. They are intended for paper-facing qualitative analysis and debugging, not as additional leaderboard data.

| Example | Policy | Task | Family | Score | Passed | Opening Actions |
| --- | --- | --- | --- | --- | --- | --- |
| task_heuristic_representative_success | task_heuristic | FND-011 | Retention improvement | 100.00 | True | week 1: improve_offer, support_customers; week 2: improve_offer, support_customers; week 3: improve_offer, support_customers |
| task_heuristic_representative_failure | task_heuristic | FND-002 | Market selection | 37.77 | False | week 1: research_market; week 2: research_market; week 3: research_market |
| heuristic_pivot_failure | heuristic | FND-040 | Pivot decision | 19.51 | False | week 1: research_market; week 2: research_market; week 3: research_market |
| random_representative_failure | random | FND-012 | Retention improvement | 46.22 | False | week 1: change_price; week 2: support_customers; week 3: change_price |

## Interpretation Notes

- Success traces show how structured actions accumulate into revenue, customer, reputation, and runway outcomes.
- Failure traces show that unsupported timing, weak family inference, or blind spending can fail even when all actions are syntactically valid.
- Hosted LLM runs should include analogous redacted audit traces with provider-call records for at least one success and one failure.

## task_heuristic_representative_success

Policy: `task_heuristic`
Task: `FND-011` (Retention improvement)
Score: `100.00`; passed: `True`
Reason selected: Highest-scoring solved task for the strongest deterministic baseline.

| Week | Cash | Reputation | Offers | Actions | Revenue | Cost | Customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8000.0 | 0.72 | 1 | improve_offer, support_customers | 775.0 | 1319.8 | None |
| 2 | 7455.2 | 0.748 | 1 | improve_offer, support_customers | 775.0 | 1319.8 | None |
| 3 | 6910.4 | 0.777 | 1 | improve_offer, support_customers | 775.0 | 1319.8 | None |
| 4 | 6365.6 | 0.805 | 1 | support_customers | 775.0 | 519.8 | None |
| 5 | 6620.8 | 0.833 | 1 | support_customers | 930.0 | 523.76 | None |
| 6 | 7027.04 | 0.861 | 1 | support_customers | 930.0 | 343.76 | None |
| 7 | 7613.28 | 0.884 | 1 | support_customers | 930.0 | 343.76 | None |
| 8 | 8199.52 | 0.907 | 1 | support_customers | 1085.0 | 347.72 | None |

## task_heuristic_representative_failure

Policy: `task_heuristic`
Task: `FND-002` (Market selection)
Score: `37.77`; passed: `False`
Reason selected: Lowest-scoring failed task for the strongest deterministic baseline.

| Week | Cash | Reputation | Offers | Actions | Revenue | Cost | Customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 10000.0 | 0.55 | 0 | research_market | 0.0 | 150.0 | None |
| 2 | 9850.0 | 0.55 | 0 | research_market | 0.0 | 150.0 | None |
| 3 | 9700.0 | 0.55 | 0 | research_market | 0.0 | 150.0 | None |
| 4 | 9550.0 | 0.55 | 0 | build_offer | 0.0 | 1900.0 | None |
| 5 | 7650.0 | 0.55 | 1 | research_market | 0.0 | 160.0 | None |
| 6 | 7490.0 | 0.55 | 1 | research_market | 0.0 | 160.0 | None |
| 7 | 7330.0 | 0.55 | 1 | research_market | 0.0 | 160.0 | None |
| 8 | 7170.0 | 0.55 | 1 | research_market | 0.0 | 160.0 | None |

## heuristic_pivot_failure

Policy: `heuristic`
Task: `FND-040` (Pivot decision)
Score: `19.51`; passed: `False`
Reason selected: Generic heuristic failure in a family where task conditioning creates a large gain.

| Week | Cash | Reputation | Offers | Actions | Revenue | Cost | Customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8800.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 2 | 8640.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 3 | 8480.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 4 | 8320.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 5 | 8160.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 6 | 8000.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 7 | 7840.0 | 0.64 | 1 | research_market | 0.0 | 160.0 | None |
| 8 | 7680.0 | 0.64 | 1 | improve_offer, run_campaign, support_customers | 0.0 | 1612.8 | None |

## random_representative_failure

Policy: `random`
Task: `FND-012` (Retention improvement)
Score: `46.22`; passed: `False`
Reason selected: Lowest-scoring random-policy failure, illustrating why blind action sampling is insufficient.

| Week | Cash | Reputation | Offers | Actions | Revenue | Cost | Customers |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 9000.0 | 0.68 | 1 | change_price | 440.0 | 64.48 | None |
| 2 | 9375.52 | 0.664 | 1 | support_customers | 440.0 | 601.48 | None |
| 3 | 9214.04 | 0.694 | 1 | change_price | 1336.0 | 64.48 | None |
| 4 | 10485.56 | 0.694 | 1 | hire_agent | 1336.0 | 1521.48 | None |
| 5 | 10300.08 | 0.694 | 1 | improve_offer | 1336.0 | 801.48 | None |
| 6 | 10834.6 | 0.694 | 1 | run_campaign | 1336.0 | 1200.48 | None |
| 7 | 10970.12 | 0.694 | 1 | cut_cost | 1336.0 | -317.77 | None |
| 8 | 12623.89 | 0.694 | 1 | do_nothing | 1336.0 | 24.48 | None |
