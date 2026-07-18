# FounderBench Metrics and Evaluation Protocol

## Unit of Evaluation

The unit of evaluation is a fixed task episode.

Each task specifies:

- task id
- task family
- seed
- time horizon
- initial company state
- allowed actions
- pass threshold
- scoring function

## Main Metrics

### Task Score

Each task returns a bounded score:

```text
0 <= task_score <= 100
```

A task is considered solved when:

```text
task_score >= 70
```

### Solve Rate

```text
solve_rate = solved_tasks / total_tasks
```

### Average Task Score

```text
average_task_score = mean(task_score_i)
```

Average task score is the official leaderboard metric because every task maps its own startup situation into the same bounded 0-100 scale. Raw simulator money, final cash, and cumulative revenue are reported as diagnostics rather than primary metrics because tasks have different starting cash, horizons, markets, and objectives.

### Metric Sensitivity

The supplementary metric-sensitivity report compares the official ranking against solve rate, median task score, task-normalized business score, survival, final cash, cumulative revenue, low-risk score, and revenue efficiency. This report is intended to detect whether the leaderboard conclusion depends on one arbitrary metric choice.

### Statistical Comparison Protocol

The supplementary statistical-protocol report pre-specifies how official model comparisons should be made: paired task-level score gaps for single runs, bootstrap intervals over paired gaps, two-sided random sign-flip permutation tests, Cohen dz effect sizes, repeated-run intervals for stochastic submissions, and Holm-Bonferroni adjustment for main leaderboard pairwise comparisons.

### Bootstrap Task-Mix Intervals

For fixed-suite baseline analysis, FounderBench reports nonparametric 95% bootstrap intervals over task episodes for average score and solve rate. These intervals estimate sensitivity to the task mix. They do not measure stochastic model sampling variance; hosted LLM submissions should additionally report repeated-run intervals when feasible.

### Repeated-Run Intervals

For stochastic policies or hosted LLM submissions, FounderBench supports repeated-run reports over multiple seeds or repeated model samples:

```powershell
python -m founderbench.repeats --policy random --seeds 0,1,2,3,4 --json-output outputs/repeats.json --markdown-output outputs/repeats.md
```

The current release package includes a five-seed random-policy calibration. Across seeds 0..4, random averages 34.72 task score with 95% repeated-run interval [33.09, 36.34], and 0.11 solve rate with interval [0.08, 0.14]. Hosted LLM results should report analogous repeated prompt-sample intervals in addition to task-mix intervals.

## Secondary Metrics

### Shutdown Rate

Fraction of tasks where the company goes bankrupt or otherwise shuts down.

### Average Final Cash

Mean final cash across all task episodes.

### Average Risk Penalty

Mean accumulated risk penalty across all task episodes.

Risk penalties represent behavior such as overspending, spam-like acquisition, impossible actions, or operationally unsafe decisions.

### Execution Diagnostics

Official runs also report execution-quality diagnostics:

- `invalid_actions`: structured actions not included in the task's allowed action set before validation
- `over_budget_decisions`: weekly decisions where requested action budgets exceeded observed cash
- `provider_errors`: model/API exceptions converted into `do_nothing` actions
- `provider_error_categories`: taxonomy counts for provider/adapter failures
- `decision_latency_s`: total wall-clock time spent obtaining policy decisions
- `simulated_api_cost`: simulator-side per-action API cost proxy
- `provider_total_tokens`: total provider-reported tokens, when available
- `estimated_provider_cost_usd`: cost estimate from configured input/output token prices
- `avg_actions_per_task`: average number of structured actions selected per task

These diagnostics do not replace the task score, but they make failure modes auditable and help separate business failure from adapter/formatting failure.

Provider error categories include:

- `invalid_json`
- `invalid_response_root`
- `missing_actions`
- `invalid_actions_type`
- `invalid_action_schema`
- `missing_action_type`
- `invalid_numeric_field`
- `no_json_object`
- `provider_timeout`
- `provider_io_error`
- `provider_exception`

### Redacted Audit Trace

When `--audit` is enabled, task events include `provider_calls` records with:

- provider and model
- task id and week
- prompt SHA-256 hash
- redacted raw response text
- provider token usage, if returned by the API
- estimated provider cost
- provider-call latency

Audit logs are intended for debugging and reproducibility. They must be inspected before release because automated redaction is a safety layer, not a guarantee.

## Family-Specific Scoring

### Market Selection

Rewards:

- researching enough markets
- selecting a viable market
- preserving enough cash

### First Revenue

Rewards:

- acquiring paying customers
- generating weekly revenue
- preserving runway
- maintaining reputation

### Retention Improvement

Rewards:

- improving offer quality
- increasing/maintaining reputation
- retaining customers
- avoiding irrelevant extra products

### Churn Shock Recovery

Rewards:

- preserving customer base
- reducing churn
- restoring reputation
- adding operational capacity when needed

### Demo Day Traction

Rewards:

- recurring revenue
- active customers
- customer growth
- remaining cash
- reputation

### Pricing

Rewards:

- moving price into a sustainable target band
- preserving or improving recurring revenue
- growing customers after price changes
- avoiding reputation and risk penalties

### Runway Preservation

Rewards:

- preserving cash
- retaining enough customers
- maintaining reputation
- taking explicit runway actions such as cost cuts, support, or pricing correction

### Pivot Decision

Rewards:

- moving stalled offers into viable target markets
- rebuilding growth after the pivot
- preserving enough cash and reputation
- avoiding repeated unfocused pivots

### Fundraising

Rewards:

- raising actual simulated funding
- having credible revenue and customer traction
- maintaining reputation
- avoiding high-risk fundraising attempts

### Channel Expansion

Rewards:

- customer growth
- recurring revenue
- efficient acquisition through campaigns or partnerships
- preserving cash and reputation

## Leaderboard Report

Official results should include:

```json
{
  "model": "provider/model-name",
  "benchmark_version": "0.3.0",
  "tasks": 50,
  "solved": 19,
  "solve_rate": 0.38,
  "average_task_score": 61.01,
  "shutdown_rate": 0.0,
  "average_final_cash": 18800.23,
  "average_risk_penalty": 0.0,
  "invalid_actions": 0,
  "over_budget_decisions": 0,
  "provider_errors": 0,
  "avg_actions_per_task": 12.28,
  "simulated_api_cost": 214.9,
  "provider_total_tokens": 0,
  "estimated_provider_cost_usd": 0.0,
  "decision_latency_s": 0.0048
}
```

## Reproducibility Rules

Official evaluations should:

1. Use the released task manifest.
2. Use deterministic simulator seeds.
3. Record model name and provider.
4. Record prompt version.
5. Save raw task-level outputs.
6. Exclude API credentials from logs.
7. Report failures as benchmark outcomes, not discarded runs.
