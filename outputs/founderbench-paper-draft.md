# FounderBench: Evaluating LLM Agents as Startup Operators Under Controlled Resources

## Abstract

Large language model agents are increasingly used to plan, call tools, and execute multi-step workflows, but current agent benchmarks under-measure whether such systems can make repeated operating decisions under scarce resources and delayed feedback. We introduce **FounderBench**, a controlled benchmark for evaluating startup-operator agents. Each episode gives an agent a simulated company state, noisy market information, limited cash, a fixed horizon, and a structured business-action interface; the agent must choose actions that produce customers, revenue, retention, runway, reputation, and survival inside the simulator.

FounderBench contains 50 fixed public tasks across 10 startup operating families and 13 structured actions. It includes normalized 0-100 task scoring, public development/test split labels, provider adapters, submission validation, redacted audit logging, and a release bundle with reproducibility checks. We calibrate the benchmark with four deterministic non-LLM baselines. Random action sampling solves 4/50 tasks, a conservative policy solves 13/50, a generic heuristic solves 19/50, and a task-aware heuristic solves 37/50 with an average score of 80.90. Paired task-level statistics, action-space ablations, leaderboard-stability checks, and difficulty analysis show that the suite is not saturated by current rule baselines and that task-family conditioning matters. These results support FounderBench as a benchmark artifact and deterministic calibration suite, but it is not yet a comparison of hosted LLM providers.

## 1. Introduction

LLM agents are moving from isolated text generation toward systems that can operate workflows over time. A one-person company may already delegate market research, sales writing, customer support, analytics, and planning to language-model agents, and future organizations may rely even more heavily on agentic execution. Evaluating such systems requires more than asking whether a model can describe a business strategy; it requires testing whether the model can repeatedly allocate scarce resources under uncertainty and recover from consequences.

Existing agent benchmarks have made substantial progress on interactive evaluation, but they usually target web tasks, software tasks, general assistant questions, or workplace task completion rather than startup operation. AgentBench evaluates language models across multiple interactive environments [4], GAIA evaluates general assistants on questions requiring reasoning and tool use [5], SWE-bench validates software patches for GitHub issues against repository tests [6], WebArena tests web agents in realistic web environments [7], tau-bench measures tool-agent-user interaction reliability [8], and TheAgentCompany simulates digital workers in a small software-company setting [9]. These benchmarks motivate outcome-based agent evaluation, but they do not isolate the startup-operator setting in which market choice, pricing, churn, runway, fundraising, pivots, and channel expansion interact over a simulated business horizon.

FounderBench addresses this gap by formulating startup operation as a controlled, sequential decision benchmark. The agent observes a company state and returns JSON actions from a fixed business interface. The simulator executes only those structured actions; free-form rationale is retained for auditing but does not directly affect score. This design lets models be evaluated on consequences rather than persuasive prose, while keeping task definitions, simulator seeds, metrics, and diagnostics reproducible.

The current paper reports the current release benchmark artifact and deterministic baseline calibration. It is intentionally scoped: the artifact supports claims about task design, scoring, reproducibility, and rule-baseline difficulty, while hosted/local LLM comparisons, human calibration, and private hidden-holdout results remain future evidence requirements. The claim-evidence report and paper-claim linting artifact explicitly mark hosted-LLM comparison claims, private holdout execution claims, and real-world startup-prediction claims as unsupported until the required evidence exists.

Our contributions are:

1. We introduce FounderBench, a 50-task controlled benchmark for startup-operator agents under bounded resources.
2. We define a 13-action structured business interface and simulator that score outcomes rather than free-form business text.
3. We provide normalized task scores, diagnostics, paired statistical protocol, submission validation, provider adapters, and reproducibility artifacts for future model comparisons.
4. We report deterministic baseline calibration, ablations, difficulty analysis, and audit traces showing that the public suite is neither solved by random action sampling nor fully saturated by a task-aware heuristic.
5. We release reviewer-facing guardrails, including a datasheet, responsible-use statement, validity report, claim-evidence report, paper-claim linting, contamination-leakage audit, and release-bundle integrity checks, to keep unsupported claims visible.

## 2. Related Work

FounderBench belongs to the growing family of LLM-agent benchmarks that evaluate interaction with an environment rather than static answer generation. ReAct introduced interleaved reasoning and action for language-model agents [1], Toolformer studied how models can use external APIs [2], and Voyager demonstrated long-horizon agent behavior in Minecraft [3]. FounderBench follows this interaction framing, but focuses on structured business operations and simulated company outcomes.

Several benchmarks emphasize realistic digital environments. AgentBench provides a broad suite of interactive environments [4], GAIA studies general assistants that must combine reasoning and tool use [5], SWE-bench evaluates whether agents can resolve GitHub issues [6], WebArena creates realistic web environments for web-agent tasks [7], and tau-bench evaluates tool-agent-user interactions under domain policies [8]. FounderBench is complementary because it converts startup operation into a controlled state-changing environment with bounded business outcomes.

Workplace and economic-agent benchmarks are closest to our motivation. TheAgentCompany measures agents in a simulated software-company environment [9], WorkArena evaluates enterprise web-agent tasks [10], EconWebArena evaluates economic web intelligence [11], and EnterpriseArena studies CFO-style long-horizon resource allocation [12]. FounderBench shares their interest in consequential decisions, but uses a compact controlled simulator to make startup operating tradeoffs reproducible and inspectable.

## 3. Benchmark Design

FounderBench evaluates an agent on fixed startup episodes. Each task specifies an initial company state, a set of markets, a horizon, a simulator seed, allowed actions, a pass threshold, and a scoring function. The unit of evaluation is a task episode rather than an unbounded money-maximization game, which makes scores comparable across different startup situations.

At each simulated week, the agent receives cash, reputation, capacity, active offers, known or noisy market signals, and recent simulator memory. The agent responds with JSON containing a rationale and an action list. Invalid actions, unsupported action types, malformed JSON, and over-budget choices are not discarded; they become benchmark outcomes through diagnostics and default simulator behavior.

The simulator includes a fixed market catalog with eight markets. Markets differ in demand, competition, willingness-to-pay, build complexity, support load, and volatility. Research actions reveal more reliable market information, while operating actions change product quality, customers, revenue, reputation, risk, runway, and funding state.

### 3.1 Task Suite

FounderBench contains 50 public tasks across 10 balanced task families.

| Task IDs | Family | Capability Tested |
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

The public release contains two visible splits: `public_dev` for FND-001..FND-030 and `public_test` for FND-031..FND-050. The contamination-leakage audit records that `public_test` is released and must not be described as hidden, unseen, private, or contamination-free. The supplementary package also includes a private-holdout blueprint, fingerprint protocol, evaluator protocol, executable evaluator-host harness, and aggregate-only holdout smoke report. The smoke report verifies the harness with a disclosed public smoke secret and is not an official hidden leaderboard. The benchmark does not include private task definitions or hidden-suite scores.

The task-card catalog gives a human-readable card for every task. The task-provenance report records that tasks are generated from hand-designed synthetic templates rather than real company data or human-subject data. The task-feasibility audit and task-revision ledger mark 11 tasks as needing external calibration because no deterministic baseline solves them.

### 3.2 Action Space

Agents act through 13 structured business actions.

| Action | Purpose |
|---|---|
| `research_market` | Improve market signal quality |
| `build_offer` | Create an offer for a target market |
| `run_campaign` | Increase awareness and customer acquisition |
| `improve_offer` | Improve offer quality |
| `hire_agent` | Increase operating capacity |
| `support_customers` | Improve reputation and reduce support pressure |
| `change_price` | Adjust offer price |
| `interview_customers` | Improve customer understanding and product quality |
| `cut_cost` | Preserve cash with possible tradeoffs |
| `pivot_market` | Move an offer into a new market |
| `raise_funding` | Raise simulated capital from traction |
| `partner_channel` | Expand distribution through partnerships |
| `do_nothing` | Take no action |

This action design is deliberately restrictive. It makes provider outputs comparable and prevents agents from receiving score through unexecuted claims. The action-semantics catalog documents required fields, cost rules, state effects, risk triggers, and typical use cases for every action.

### 3.3 Prompt and Submission Protocol

The prompt-protocol artifact fixes the provider message format, JSON response schema, action vocabulary, prompt hashes, and redaction rules for hosted and local submissions. The submission schema validates complete 50-task runs, required diagnostics, split summaries, token/cost metadata when available, and repeated-run bundles. The unified model-comparison report automatically excludes missing or invalid provider rows until raw submissions pass validation.

## 4. Metrics and Evaluation Protocol

FounderBench uses normalized task outcomes as the primary evaluation target. The main metrics are `solved`, `solve_rate`, and `average_task_score`, where each task score is clamped to [0, 100] and a task is solved at score >= 70. The score is not a direct dollar value or external valuation; raw money, customers, revenue, reputation, risk, and cash are diagnostics interpreted within each task.

The score-rubric artifact decomposes each family score into positive components and penalties. The scoring-consistency audit checks all deterministic score objects against bounds, the pass threshold, metrics payload requirements, family coverage, and split coverage. The simulator-invariant audit checks state bounds, score bounds, pass flags, bankruptcy behavior, and invalid-action handling.

The metric-sensitivity report compares the official ranking with solve rate, median task score, task-normalized business score, survival, cash, revenue, risk, and revenue efficiency. This is important because raw simulated money is not directly comparable across tasks with different initial cash, horizons, markets, and objectives.

The statistical-protocol report pre-specifies paired task-level comparisons. For deterministic single runs, comparisons use matched task score gaps, bootstrap intervals over task gaps, random sign-flip permutation tests, Cohen dz effect sizes, and Holm-Bonferroni adjustment for main leaderboard pairwise claims. The paired-statistics report applies this protocol to deterministic baselines. The power-analysis report estimates the public-suite resolution and warns that close hosted-model differences require repeated-run intervals or larger private-holdout evaluation before strong ranking claims.

## 5. Baseline Calibration

We evaluate four deterministic non-LLM baselines to calibrate task difficulty and scoring behavior. The `random` policy samples weakly disciplined actions, `conservative` preserves runway and support, `heuristic` applies generic market and operating rules, and `task_heuristic` uses task-family-specific rules. These baselines are not intended as model competitors; they are calibration instruments for checking whether the benchmark is trivial, impossible, or sensitive to structured decision quality.

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Over-Budget |
|---|---:|---:|---:|---:|---:|---:|---:|
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 5 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 15 |

The baseline spread shows that the public suite is not solved by random action sampling, while simple structured policies can solve a nonzero subset of tasks. The strongest rule baseline still fails 13 tasks, leaving room for future hosted/local LLM evaluation and human calibration.

Task-mix bootstrap intervals also show a large separation among policies. The task-aware heuristic obtains 80.90 average score with interval [74.94, 86.42], compared with 61.01 [55.21, 66.94] for the generic heuristic, 54.04 [48.20, 60.14] for the conservative policy, and 33.30 [26.89, 40.60] for random. A separate repeated-run random-policy calibration over seeds 0..4 gives 34.72 average score with repeated-run interval [33.09, 36.34], illustrating the reporting format expected for stochastic submissions.

Paired task-level comparisons show that the task-aware heuristic exceeds the generic heuristic by 19.90 points on average with bootstrap interval [13.80, 26.19]. The average gap over conservative is 26.87 [21.67, 32.45], and the average gap over random is 47.61 [40.24, 54.64]. The paired-statistics report also includes raw and Holm-Bonferroni adjusted permutation p-values, effect sizes, and task win/loss/tie counts.

## 6. Analysis

### 6.1 Capability Ladder

The deterministic policies form a capability ladder. Moving from random to conservative adds runway preservation and cautious support behavior, improving average score by 20.74 points. Moving from conservative to generic heuristic adds market scoring, pricing correction, acquisition, quality improvement, and support logic, improving score by 6.97 points. Moving from generic heuristic to task-aware heuristic adds task-family conditioning, improving score by 19.90 points and adding 18 solved tasks.

The largest task-conditioning gains occur in churn shock recovery, pivot decision, retention improvement, and fundraising. This pattern suggests that the benchmark is not merely rewarding generic growth activity; it rewards recognizing the operating situation and selecting actions that match the task family.

### 6.2 Action-Space Ablation

The action-space ablation disables major action groups in the task-aware heuristic and reruns all 50 tasks. This checks whether the 13-action interface is behaviorally meaningful rather than only syntactic. Large drops identify action groups whose removal materially changes outcomes, while small drops identify areas where current tasks may not sufficiently stress an action type.

### 6.3 Family-Level Difficulty

Family-level results show heterogeneous difficulty. Runway preservation is easiest for structured policies: task-aware, heuristic, and conservative policies all solve all five runway tasks. Pivot decision and channel expansion are harder: the task-aware heuristic solves only 2/5 in each family, while generic and conservative policies solve none. Fundraising is solved by the task-aware heuristic, but not by generic or conservative policies, indicating that the required traction/funding sequence is more task-specific than generic operating behavior.

This difficulty spread is useful for a benchmark paper because it shows both calibration and remaining uncertainty. The difficulty-calibration report identifies saturated tasks, high-discrimination tasks, and tasks that still require external calibration. The task-feasibility audit records deterministic-unsolved tasks as open feasibility questions rather than declaring them impossible.

### 6.4 Failure Diagnostics and Qualitative Traces

Failure diagnostics distinguish poor decisions from interface failures. Random produces 15 over-budget decisions and one bankruptcy failure, while deterministic structured policies avoid bankruptcy. The worst heuristic and conservative task is FND-040 in the pivot family, where both policies delay or avoid the needed market shift. Qualitative traces show that the task-aware heuristic can improve retention through repeated quality/support actions, but can still fail market selection when research does not lead to a viable commitment.

The qualitative traces are regenerated from fixed seeds and included as supplementary artifacts. Hosted LLM submissions should provide analogous redacted audit traces that include provider-call records, prompt hashes, redacted responses, token usage when returned, estimated provider cost, and latency.

## 7. Reproducibility and Release Artifacts

FounderBench is packaged as a reproducible benchmark artifact. The release includes source code, task manifest, raw baseline outputs, generated tables, paper figure data, task-card catalog, action-semantics catalog, market catalog, scoring-rubric report, metric-sensitivity report, statistical-protocol report, power-analysis report, paired-statistics report, leaderboard policy, leaderboard-stability audit, result-integrity audit, scoring-consistency audit, simulator-invariant audit, determinism audit, reviewer smoke report, environment report, cost-accounting protocol, prompt-protocol report, provider-contract audit, provider-comparability audit, contamination-leakage audit, citation-context audit, validity report, responsible-use statement, datasheet, claim-evidence report, paper-claim linting, reviewer-risk audit, AI research failure-mode audit, completion audit, submission gate, submission action plan, experiment matrix, reviewer index, non-final license/citation templates, and release-bundle checksum/integrity reports. The AI research failure-mode audit explicitly checks risks such as hallucinated citations and hallucinated experimental results.

The result-integrity audit independently recomputes deterministic leaderboard, paper-table, and model-comparison rows from raw task-level JSON. The determinism audit reruns the four rule baselines with fixed seeds and compares stable-result hashes. The release-bundle integrity report verifies bundled files against the checksum manifest. Together, these artifacts make the deterministic baseline claims traceable to generated outputs rather than manually copied table values.

The provider tooling is present but intentionally claim-gated. Hosted provider runs can be executed with the resumable runner, and the submission validator checks complete task coverage, diagnostics, split summaries, and repeated-run bundle identity. The provider-readiness and provider-run-status artifacts currently mark planned hosted/local current release runs as missing, and the unified model-comparison report excludes them from paper claims until valid raw submissions exist.

## 8. Limitations

FounderBench is a controlled synthetic benchmark, not a real company deployment test. The simulator approximates startup dynamics through hand-designed market, conversion, churn, reputation, risk, cash, and funding rules. The simulator-invariant audit checks software-level behavior, but it does not validate real-world market dynamics.

The public task suite is template-generated rather than curated from real startup histories. This improves control and reproducibility, but limits ecological validity. The task-provenance report documents the synthetic construction process and the absence of real company or human-subject source data.

The current draft reports non-LLM baselines only. It is not yet a comparison of hosted LLM providers. The final model-comparison paper requires full current release runs for hosted and local open-source models, including repeated sampling, audit traces, submission validation, and cost accounting.

There is not yet an official private hidden leaderboard. The release includes a private-holdout blueprint, fingerprint protocol, evaluator protocol, executable harness, and aggregate-only holdout smoke report, but the holdout smoke report is not an official hidden leaderboard. The benchmark does not include private task definitions or hidden-suite scores.

No human-founder or expert calibration study has been executed yet. The supplementary human-calibration protocol, schema/template, recruitment packet, analysis tool, and task-revision ledger define how such evidence should be collected. The generated analysis artifact is currently marked as having no included submissions, so real-world startup-prediction claims as unsupported remains the correct wording.

The public release metadata is also not final. The package includes non-final license/citation templates and a release-metadata checklist, but final author, repository, and license decisions are still owner actions.

## 9. Next Experiments

The main empirical next step is to run representative hosted and local LLM baselines on all 50 tasks. The current experiment matrix requires DeepSeek, Claude, Gemini, and at least one local open-source model through the OpenAI-compatible protocol. Each run should use audit mode and pass the submission validator before entering the model-comparison report.

The second next step is external calibration. Expert or founder reviewers should complete the human-calibration packet, rate scenario realism and score alignment, identify gaming risks, and flag task or rubric revisions. Any resulting changes should be recorded in the task-revision ledger and should trigger a benchmark version increment when they affect official task definitions or scoring.

The third next step is private evaluation. The private-holdout blueprint should be instantiated on an evaluation host, hidden task definitions should remain unreleased, and only aggregate scores should be reported through the evaluator protocol. This would allow future leaderboard claims without treating the current public test split as hidden.

## 10. Conclusion

FounderBench reframes LLM-agent evaluation around repeated startup-operation decisions under bounded resources. Its key idea is to replace open-ended business prose with structured actions whose consequences are scored in a controlled simulator. The current release artifact provides a 50-task suite, 13-action interface, normalized scoring, deterministic baseline calibration, ablations, diagnostics, submission validation, and extensive reproducibility and claim-safety artifacts.

The current evidence supports FounderBench as a benchmark artifact and deterministic calibration suite. It does not yet support claims about hosted LLM provider rankings, hidden-holdout performance, human agreement, or real-world company success. Completing those experiments would turn the artifact paper into a full model-comparison benchmark paper.

## References

The supplementary package includes `founderbench-references.bib` and `founderbench-reference-provenance.json` with BibTeX entries and source provenance for these references. It also includes generated review artifacts for task coverage, task provenance, task cards, task-feasibility auditing, task-revision tracking, action semantics, action-space ablations, market catalog, scoring rubrics, scoring consistency, metric sensitivity, statistical protocol, power analysis, model comparison, model result cards, paired statistics, leaderboard stability, result integrity, difficulty calibration, prompt protocol, provider comparability, cost accounting, responsible-use and disclosure boundaries, release metadata, non-final license/citation templates, submission schema, repeated-run submission bundling, hosted/local baseline execution planning, experiment runbook, provider-run status, reviewer smoke testing, release-bundle integrity verification, reproducibility, runtime environment/dependency reporting, determinism audit, citation-context auditing, private-holdout smoke testing, validity threats, human calibration protocol/schema/packet/analysis, claim-evidence alignment, paper-claim linting, reviewer-risk auditing, AI research failure-mode auditing, submission gate/action planning, goal-level completion audit, experiment requirements, paper-ready tables, and paper figure data.

[1] Yao et al. ReAct: Synergizing Reasoning and Acting in Language Models. https://arxiv.org/abs/2210.03629

[2] Schick et al. Toolformer: Language Models Can Teach Themselves to Use Tools. https://arxiv.org/abs/2302.04761

[3] Wang et al. Voyager: An Open-Ended Embodied Agent with Large Language Models. https://arxiv.org/abs/2305.16291

[4] Liu et al. AgentBench: Evaluating LLMs as Agents. https://arxiv.org/abs/2308.03688

[5] Mialon et al. GAIA: a benchmark for General AI Assistants. https://arxiv.org/abs/2311.12983

[6] Jimenez et al. SWE-bench: Can Language Models Resolve Real-World GitHub Issues? https://arxiv.org/abs/2310.06770

[7] Zhou et al. WebArena: A Realistic Web Environment for Building Autonomous Agents. https://arxiv.org/abs/2307.13854

[8] Yao et al. tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains. https://arxiv.org/abs/2406.12045

[9] Xu et al. TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks. https://arxiv.org/abs/2412.14161

[10] Drouin et al. WorkArena: How Capable Are Web Agents at Solving Common Knowledge Work Tasks? https://servicenow.github.io/WorkArena/

[11] EconWebArena: Benchmarking Autonomous Agents on Economic Tasks in Realistic Web Environments. https://arxiv.org/abs/2506.08136

[12] Han et al. EnterpriseArena: Can LLM Agents Be CFOs? Benchmarking Long-Horizon Resource Allocation. https://arxiv.org/abs/2603.23638
