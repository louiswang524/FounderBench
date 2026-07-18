# FounderBench Benchmark Card

## Name

FounderBench v0.3.0

## Purpose

FounderBench evaluates whether LLM agents can operate startup-like businesses under bounded resources. The benchmark is motivated by the expected rise of agent-heavy, one-person, and no-person companies where LLM agents perform substantial business execution.

## Core Evaluation Question

Can an LLM agent make repeated business decisions that improve startup outcomes under limited funding, runway, noisy market signals, operational constraints, and risk penalties?

## Artifact Type

Agent benchmark environment with a fixed task suite.

Current release:

- 50 fixed startup tasks
- 10 task families
- deterministic seeded simulator
- fixed 8-market simulator catalog
- structured action interface with 13 business actions
- baseline policies
- hosted provider adapters
- provider token/cost-accounting protocol
- hosted/local baseline execution plan
- hosted/local experiment runbook
- provider-run status report for v0.3 evidence
- repeated-run submission bundle protocol
- leaderboard tooling
- JSON task manifest
- task provenance report
- deterministic replay audit
- reviewer smoke-test report
- runtime environment/dependency report
- release-bundle checksum and integrity report
- expert/human-founder calibration protocol
- expert/human-founder calibration response schema/template
- expert/human-founder calibration analysis status report
- license/citation readiness and release metadata checklist
- submission gate and submission action-plan reports
- goal-level completion audit
- public development and public test split labels
- executable evaluator-host private holdout harness

## Task Families

| Family | Task IDs | What It Tests |
|---|---|---|
| Market selection | FND-001..FND-005 | Researching noisy markets and committing to a viable offer |
| First revenue | FND-006..FND-010 | Sequencing research, product build, pricing, and acquisition |
| Retention improvement | FND-011..FND-015 | Improving quality and support for existing customers |
| Churn shock recovery | FND-016..FND-020 | Stabilizing reputation, capacity, and customers under pressure |
| Demo Day traction | FND-021..FND-025 | Growing revenue, customers, and credibility before evaluation |
| Pricing | FND-026..FND-030 | Finding sustainable price points under customer and revenue constraints |
| Runway preservation | FND-031..FND-035 | Extending cash runway without destroying the active customer base |
| Pivot decision | FND-036..FND-040 | Recovering from stalled offers by researching and shifting markets |
| Fundraising | FND-041..FND-045 | Raising capital from credible traction while preserving operations |
| Channel expansion | FND-046..FND-050 | Scaling working offers through campaigns and partner channels |

## Action Space

Agents return structured actions:

- `research_market`
- `build_offer`
- `run_campaign`
- `improve_offer`
- `hire_agent`
- `support_customers`
- `change_price`
- `interview_customers`
- `cut_cost`
- `pivot_market`
- `raise_funding`
- `partner_channel`
- `do_nothing`

The simulator executes only structured actions. Free-form claims do not directly affect score.

The supplementary action-semantics catalog documents required fields, cost rules, simulator effects, risk triggers, and typical use cases for all 13 actions.

The supplementary market catalog documents the fixed simulated markets, including demand, competition, willingness-to-pay, build complexity, support load, volatility, observation rules, and weekly settlement rules. This makes the market environment inspectable without reverse-engineering simulator code.

## Metrics

Primary metrics:

- `solved`: number of tasks with score >= 70
- `solve_rate`: solved / total tasks
- `average_task_score`: mean bounded score from 0 to 100

Secondary metrics:

- `average_final_cash`
- `shutdown_rate`
- `average_risk_penalty`
- `invalid_actions`
- `over_budget_decisions`
- `provider_errors`
- `decision_latency_s`
- `simulated_api_cost`
- per-task score components, such as customers, cash, churn, reputation, capacity, and recurring revenue

## Baselines

Current v0.3.0 calibration:

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget Decisions |
|---|---:|---:|---:|---:|---:|---:|---:|
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 |

This spread suggests the benchmark is not trivial and not impossible for non-LLM baselines.

## Known Limitations

- The economy is simulated and simplified.
- Task variants are generated from ten templates, not yet curated from real startup histories.
- The task provenance report documents the synthetic template source and confirms that no real company or human-subject data is used.
- Runway and fundraising have been tightened with behavior/outcome gates, but runway remains comparatively easy for conservative strategies and pivot/channel-expansion remain hard.
- Current provider prompts need better budget-discipline guidance.
- Expert/human-founder calibration is specified as a protocol, but no human calibration results are included yet.
- A calibration analyzer is included, but the current generated analysis status is `no_submissions_found` until expert/founder response files are collected.
- Official leaderboard diagnostics include simulated API cost, decision latency, invalid actions, over-budget decisions, and provider errors. Real provider billing cost is not yet estimated from token usage.
- Hidden evaluation seeds are not yet separated from public development seeds.
- Determinism has been audited for included rule baselines, but hosted LLM submissions still need repeated-sampling reports.
- Repeated hosted/local submissions should be combined with the submission-bundle helper so duplicate policy/run-seed identities are rejected before leaderboard claims.
- The generated completion audit currently marks the full publishable-artifact goal as `not_complete` because required hosted/local LLM evidence and final public release metadata are still missing.

## Intended Use

FounderBench is intended for research on:

- LLM agent evaluation
- long-horizon decision-making
- tool/action planning
- business operations simulation
- multi-agent startup teams
- cost-aware model comparison

## Non-Goals

FounderBench is not:

- a real-money trading environment
- a recommendation to deploy autonomous companies without human/legal governance
- a replacement for real startup due diligence
- affiliated with Y Combinator
