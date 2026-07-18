# FounderBench Specification

## Goal

FounderBench evaluates how well an LLM agent can convert limited capital, noisy market information, and bounded tool access into durable startup outcomes inside a deterministic simulated economy.

The benchmark is motivated by a future where one-person, agent-heavy, or no-person companies rely on LLM agents for substantial business execution. Static benchmarks measure answer quality; FounderBench measures repeated decision quality under business constraints.

## Evaluation Unit

The unit of evaluation is a fixed startup task episode.

Each task defines:

- task id
- task family
- split
- deterministic simulator seed
- time horizon
- initial company state
- allowed action set
- pass threshold
- bounded 0-100 scoring function

## Splits

The benchmark contains public splits only:

- `public_dev`: FND-001..FND-030
- `public_test`: FND-031..FND-050

A future evaluation cycle should execute a true private holdout with hidden seeds and templates. The current supplementary artifacts include a private-holdout blueprint, fingerprint generator, and evaluator protocol. The blueprint commits to a 20-task private suite with two hidden tasks per family. An evaluator can set `FounderBench_HOLDOUT_SECRET` and generate task fingerprints without publishing task definitions.

The task provenance artifact (`outputs/founderbench-task-provenance.md`) documents that current release uses 10 hand-designed synthetic templates with 5 variants each. It records template ranges, seed rules, setup functions, scoring functions, and that no real-world company data or human-subject data is used.

## Task Families

| Tasks | Family | Capability |
|---|---|---|
| FND-001..FND-005 | Market selection | Select a viable opportunity from noisy market signals |
| FND-006..FND-010 | First revenue | Sequence research, building, pricing, and acquisition |
| FND-011..FND-015 | Retention improvement | Improve quality/support for existing customers |
| FND-016..FND-020 | Churn shock recovery | Stabilize reputation, capacity, and customers under pressure |
| FND-021..FND-025 | Demo Day traction | Grow revenue, customers, runway, and credibility |
| FND-026..FND-030 | Pricing | Move toward sustainable price points |
| FND-031..FND-035 | Runway preservation | Preserve cash without destroying the customer base |
| FND-036..FND-040 | Pivot decision | Recover from stalled offers through research and market shifts |
| FND-041..FND-045 | Fundraising | Raise capital from credible traction |
| FND-046..FND-050 | Channel expansion | Scale working offers through campaigns and partnerships |

## Action Space

Agents submit structured actions. The simulator executes only these actions:

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

Invalid actions are converted to `do_nothing` by validation and counted in diagnostics.

The generated action-semantics catalog (`outputs/founderbench-action-semantics.md`) documents each action's required fields, optional fields, cost rule, primary simulator effects, risk triggers, and typical use cases.

The generated market catalog (`outputs/founderbench-market-catalog.md`) documents the fixed 8-market simulator set, including market ids, demand, competition, willingness-to-pay, build complexity, support load, volatility, observation rules, and weekly settlement rules.

## Observation Contract

At each simulated week, the agent receives:

- week
- cash
- reputation
- agent capacity
- noisy or researched market signals
- active offers
- short memory of recent simulator notes

The agent returns JSON with a brief rationale and a list of actions. The rationale is logged for auditability but does not directly affect the simulator.

Unresearched markets expose noisy demand, competition, and willingness-to-pay signals. `research_market` and `interview_customers` can mark markets as researched, after which exact simulator signals are exposed for that market.

## Scoring

Each task returns:

```text
0 <= task_score <= 100
```

A task is solved if:

```text
task_score >= 70
```

The official aggregate metrics are:

- solved tasks
- solve rate
- average task score
- public development score
- public test score
- shutdown rate
- average final cash
- average risk penalty

## Diagnostics

Every run also reports:

- invalid actions
- over-budget decisions
- provider errors
- average actions per task
- decision latency
- simulator-side API cost proxy
- provider prompt/completion/total tokens, when available
- estimated provider cost, when token prices are configured

These diagnostics support paper analysis but do not replace task score.

Model submissions must follow the generated submission schema (`outputs/founderbench-model-submission-schema.md`) and pass `python -m founderbench.submission`. The schema documents accepted payload shapes, required run fields, required diagnostics, required splits, and the 50-task coverage contract.

The deterministic replay audit (`outputs/founderbench-determinism-audit.md`) reruns included deterministic baselines twice with fixed seeds and verifies stable result hashes after excluding wall-clock latency fields.

## Audit Mode

Hosted-provider runs may be executed with `--audit`. Audit mode records provider-call records in task events:

- provider
- model
- task id
- week
- prompt SHA-256 hash
- redacted raw response
- token usage
- estimated provider cost
- latency

Audit logs must be inspected manually before release. Automated redaction is a safety layer, not a complete guarantee.

## Private Holdout Protocol

The proposed private holdout protocol is:

1. Keep public code, public development tasks, and public test tasks fixed.
2. Generate private holdout fingerprints from a secret held only by the evaluator.
3. Accept model submissions through the same structured action interface.
4. Run submitted models against hidden tasks on the evaluator host.
5. Publish aggregate private scores and selected redacted audit failures.
6. Rotate or release the holdout after the benchmark cycle closes.

The public blueprint is generated by:

```powershell
python -m founderbench.holdout blueprint --output outputs/founderbench-private-holdout-blueprint.json
```

Private fingerprints are generated by:

```powershell
$env:FounderBench_HOLDOUT_SECRET = "<private-secret>"
python -m founderbench.holdout fingerprints --output private-holdout-fingerprints.json
```

The evaluator protocol is generated by:

```powershell
python -m founderbench.holdout protocol --output outputs/founderbench-private-holdout-evaluator-protocol.md
```

An evaluator-controlled host can execute the secret-seeded private suite with:

```powershell
$env:FounderBench_HOLDOUT_SECRET = "<private-secret>"
python -m founderbench.private_holdout_evaluator --policy deepseek --output private-deepseek-report.json
```

The default evaluator report is aggregate-only. It records private task count, private solve rate, private average score, diagnostics, and the fingerprint manifest hash, but it does not publish hidden task initial states, selected templates, hidden seeds, or raw traces.

## Anti-Gaming Principles

FounderBench should punish or expose:

- overspending
- spam-like acquisition
- repeated unfocused pivots
- ignoring customer support load
- excessive action spam
- invalid tool calls
- bankrupting the company for short-term metrics
- free-form claims unsupported by simulator actions

## Baselines

Required non-LLM baselines:

- random
- conservative
- heuristic
- task-aware heuristic

Required model baselines for a paper submission:

- core hosted frontier providers covering OpenAI/GPT, Anthropic/Claude, Google/Gemini, DeepSeek, Moonshot/Kimi, and Alibaba/Qwen when API access is available
- at least one local or open-source model through the OpenAI-compatible adapter
- optional broader ecosystem rows for Mistral, GLM/Z.ai, xAI/Grok, and Llama/open-weight endpoints
- provider and local/open-source model baselines using the same canonical prompt contract

Required deterministic calibration ablations:

- policy capability ladder from random to task-aware heuristic
- action-space ablation that disables major action groups and reports score drops

Required interpretability/calibration evidence for a stronger paper submission:

- execute the expert/human-founder calibration protocol
- collect responses with the generated calibration schema/template
- report task realism, action coverage, scoring alignment, difficulty labels, and flagged tasks
- keep expert-calibration evidence separate from the official model leaderboard

## Current Known Limitations

- current tasks are hand-designed/generated from templates rather than curated from real startup histories.
- Public test tasks are visible; the private holdout protocol exists, but no hidden-suite leaderboard has been executed yet.
- Runway tasks remain relatively easy for conservative policies.
- Pivot and channel-expansion tasks are hard for current rule baselines.
- Real provider baselines on all 50 current tasks still need to be rerun.
- The human-calibration protocol exists, but expert/human-founder results have not yet been collected.
- Token-level provider cost depends on API usage metadata and configured price assumptions.
