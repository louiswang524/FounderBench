# FounderBench: Evaluating LLM Agents on Sequential Startup Decisions

## Abstract

Existing agent benchmarks emphasize tool use, web navigation, and software editing, but rarely isolate repeated operating decisions under scarce resources and delayed consequences. We introduce **FounderBench**, a controlled benchmark for startup-like sequential decision making. Given a simulated company state and noisy market information, an agent must choose from 13 structured business actions over a fixed horizon; a deterministic simulator updates cash, demand, quality, and risk, and task-specific code maps final outcomes to a 0–100 score. Free-form rationale is logged for audit but never scored. The suite contains 50 synthetic public tasks balanced across 10 operating families. **Headline gap:** a task-aware calibration policy averages 80.90 (37/50 solved), while the best hosted single run reaches only 67.69 (32/50); no human-founder baseline is reported. Rankings reverse between average score and solved count, and family profiles expose distinct operating failures. We release tasks, simulator and scoring code, adapters, validated task-level results, and generation scripts. All hosted rows are single runs on visible public tasks. There is no human-founder calibration and no official private leaderboard. Scores do not establish real-world startup competence.

## 1. Introduction

Agent evaluation has moved from short answers toward interactive settings where a model must observe state, choose actions, and accept consequences. Recent long-horizon suites further stress sustained CLI execution (Terminal-Bench, LHTB), policy-rich enterprise workflows (χ-Bench), and even multi-year startup coherence (YC-Bench). These benchmarks are valuable, yet a complementary operating regime remains underexplored: short, family-labeled startup decisions under scarce resources and delayed consequences, scored by inspectable outcome functions rather than open-ended tool traces or year-end cash alone.

That gap matters because persuasive text is easy to confuse with competence. Consider a Demo Day episode: an agent may write a confident fundraising narrative while never researching markets, under-improving offer quality, and exhausting cash on poorly timed campaigns; the simulator records a weak state and the family scorer returns a low outcome even though the prose looked founder-ready. Startup-like decisions couple research, acquisition, retention, pricing, pivots, and fundraising under a single budget. Evaluating them requires an environment where actions change state and outcomes—not rhetoric—determine score.

FounderBench is designed for that setting. Each episode provides a structured company observation and a fixed action vocabulary. The agent returns a JSON action list; a deterministic simulator applies costs and transitions; task-specific scoring code returns a 0–100 outcome score. The design follows a simple principle used by strong execution benchmarks: make success checkable without grading free-form prose.

Relative to prior agent suites, FounderBench deliberately trades open-world breadth for inspectable operating tradeoffs. Tasks are synthetic and fully public; transitions and scores can be replayed; calibration policies establish a capability ladder before hosted models are interpreted. Empirically, the ladder is wide: task-aware calibration reaches 80.90 average score (37/50 solved), while the best hosted single run reaches 67.69 (32/50), with the largest hosted deficits on pivot and Demo Day families. The resulting test asks whether an agent can turn noisy observations into sequenced business actions under binding constraints.

Our contributions are:

1. **Benchmark.** A 50-task suite spanning 10 startup operating families, with fixed seeds, 13 structured actions, and visible task definitions.
2. **Outcome protocol.** A deterministic simulator and task-specific scorers that evaluate final state rather than rationales, keeping provider outputs comparable.
3. **Empirical baselines.** Validated single-run results for eleven hosted configurations and four calibration policies, with family diagnostics and provider-error reporting.
4. **Auditable release.** Task-level evidence, adapters, validation, task-mix analyses, datasheet-style documentation, and generators that regenerate every reported table and figure.

FounderBench is a controlled synthetic test of sequential decisions. It is not evidence that a model can run a real company: there is no human-founder calibration and no official private leaderboard, and the present hosted numbers are single runs on visible public tasks.

## 2. Related Work

**Interactive, terminal, and sequential agents.** ReAct and Toolformer established reasoning–action loops; Voyager studied open-ended long-horizon play. AgentBench and GAIA broaden interactive evaluation, while SWE-bench, WebArena, and τ-bench emphasize executable correctness. Terminal-Bench and LHTB push CLI long-horizon work. Agentick unifies sequential decision-making across RL/LLM/hybrid agents. FounderBench specializes to startup operating decisions with structured actions.

**Workplace, enterprise, and startup simulations.** TheAgentCompany, WorkArena, EconWebArena, EnterpriseArena, and χ-Bench cover workplace/economic/healthcare settings. CoffeeBench is a multi-agent economic sandbox (net income over 90 days). AgentHire-Bench targets managerial hiring/delegation; BrandEval targets crisis communication under trust/reputation risk. Closest agentic startup operators are YC-Bench (He et al.; year-long CLI, final funds) and CEO-Bench (500-day CEO sim, ending cash). Benhenda’s YC Bench is *predictive* (forecast YC batch outperformance), not agentic. FounderBench uses short family-labeled episodes, structured JSON actions, and task-specific 0–100 scorers.

| Benchmark | Domain | Horizon | Interface | Oracle | Human? | Hidden? |
|---|---|---|---|---|---|---|
| YC-Bench (He et al.) | startup ops | ~1 year | CLI | final funds | no | no† |
| CEO-Bench | startup CEO | 500 days | tools/code | ending cash | no | no† |
| CoffeeBench | multi-agent economy | 90 days | tools | net income | no | no† |
| WebArena | web tasks | multi-step | browser | functional checks | yes | partial |
| SWE-bench | GitHub issues | patch | code | unit tests | no | no |
| FounderBench | startup families | ≤10 weeks/ep. | structured JSON | family 0–100 state | no | frozen‡ |

†As reported in the cited papers' primary public evaluations. ‡Private holdout is frozen; this paper reports hosted scores only on the visible public suite.

**Documentation and evaluation practice.** Datasheets and HELM motivate transparent documentation and multi-metric reporting.

**Executable judging versus LLM judges.** Outcome-only scoring is a deliberate alternative to rubric or LLM-as-a-judge pipelines. RULERS shows that even structured rubrics need locked criteria and evidence anchoring; FounderBench sidesteps that fragility by never grading free-form text. Complementary work (e.g., One Token to Fool LLM-as-a-Judge) shows LLM judges can be manipulated by short adversarial strings, reinforcing why persuasive rationales are logged for audit but excluded from scores. Hybrid designs—proxy state checks, partial human review, or stochastic market noise—can trade determinism for realism; v0.3 prioritizes full re-executable determinism.

## 3. Benchmark Design

### 3.1 Benchmark desiderata

Before detailing mechanics, five desiderata guided FounderBench:

1. **Executable outcomes.** Success must be checkable from simulator state, not prose quality.
2. **Family diagnosis.** The suite should expose which operating failure modes matter, not only a single scalar.
3. **Shared interface.** Providers face identical observations and action schemas.
4. **Replayability.** Fixed seeds and deterministic transitions make policies and audited traces re-executable.
5. **Contamination awareness.** A frozen private holdout exists even if hosted private scores are deferred.

### 3.2 Task formulation

An episode is a tuple \((x_0, H, \mathcal{A}, f)\), where \(x_0\) is the initial company state, \(H \leq 10\) is the horizon in simulated weeks, \(\mathcal{A}\) is the allowed action set, and \(f\) maps final state to a clamped score in \([0,100]\). At week \(t\), the policy observes cash, reputation, capacity, offers, market information, and recent memory, then returns a rationale plus one or more structured actions. Only actions are executed. The simulator validates inputs, applies costs and transitions, advances markets, and returns the next observation. Malformed responses and provider exceptions are recorded and handled by documented fallbacks, so interface reliability remains part of end-to-end score.

### 3.3 Tasks and families

The suite contains 50 public tasks, five in each of ten families: market selection, first revenue, retention, churn recovery, Demo Day traction, pricing, runway preservation, pivot, fundraising, and channel expansion. FND-001–030 are labeled `public_dev` and FND-031–050 `public_test`; both splits are released and visible, so the labels support analysis rather than unseen generalization claims.

Tasks are generated from hand-designed synthetic templates with fixed variants and seeds. They contain no real-company or human-subject records. This improves control and redistributability at the cost of ecological validity.

### 3.4 State, markets, and actions

Eight synthetic markets differ in demand, competition, willingness to pay, build complexity, support load, and volatility. Research improves information quality. The 13 actions cover research, offer creation and improvement, campaigns, hiring, support, pricing, interviews, cost cutting, pivots, fundraising, channel partnerships, and no-op. Exact schemas ship with the artifact. Because only structured actions execute, a model cannot score by claiming it researched customers or improved a product; it must select the action and pay its simulated cost.

### 3.5 Design properties

The desiderata above place FounderBench as a domain-specialized, deterministic-outcome suite. A natural alternative is hybrid verification (executable hard constraints plus locked rubrics or limited expert review). We prioritize full determinism for v0.3 so every published score is re-executable; the cost is reduced ecological validity under market shocks and adversarial conditions.

## 4. Evaluation Protocol

### 4.1 Metrics

For task \(i\) with final state \(x_i\),

\[
s_i = \min(100,\max(0,f_i(x_i))).
\]

The primary aggregate is the unweighted mean \(\bar{s}=\frac{1}{50}\sum_{i=1}^{50}s_i\). A task is solved when \(s_i \geq 70\). We chose 70 as a fixed operating threshold—roughly “clearly successful” on the family rubrics—not as an optimized cutpoint: it sits between the generic-heuristic mean (61.01) and the task-aware ceiling (80.90). We do not ablate alternative thresholds here; average score remains primary because it preserves distances below and above any fixed cut. Raw cash and revenue remain diagnostics because tasks differ in initial conditions and objectives.

### 4.2 Models and execution

Hosted APIs use provider-specific adapters under one prompt protocol. Each task starts from its published seed and state. Audit mode records traces; a submission validator checks all 50 IDs, score bounds, split summaries, diagnostics, and policy identity before a row enters the paper registry. Evidence files are frozen by SHA-256.

We evaluate Claude Sonnet 4.5 and 5, DeepSeek Chat and V4 Reasoner, Gemini 2.5 Flash and 3.5 Flash, GLM 4.5 Air, Grok 4.3 and 4.5, GPT-5.6 Sol, and Kimi K3. Labels record the API identifiers used during collection; they do not imply identical inference settings across providers. All hosted results are one run per configuration. We report nonparametric bootstrap intervals over tasks as **task-mix sensitivity**, not sampling variance, and do not use those intervals for significance claims among closely ranked hosted models.

### 4.3 Calibration and diagnostics

Four deterministic policies calibrate the suite: random, conservative, generic heuristic, and task-aware heuristic. They are reference points, not model competitors. The task-aware policy branches on family identity derived from the task ID—a privileged prior that ordinary hosted prompts do not share unless the card text leaks family cues. It is a calibration ceiling, not human performance, and not an unbiased estimate of the “true” model gap. On a frozen private remix (deterministic calibration only; no official private leaderboard), the task-aware mean falls below the generic heuristic (54.81 vs. 57.49), consistent with public-suite overfitting risk. Released action-space ablations show removing quality/support/capacity actions drops the task-aware mean by about 19 points. The runner records invalid actions, over-budget decisions, provider/parser errors, latency, action counts, and token usage when available. Provider errors trigger documented fallbacks and remain in official scores; we report affected-task rates so interface load is visible without treating official scores as pure strategy.

## 5. Results and Analysis

### 5.1 Overall performance

Calibration policies form a clear capability ladder. Random scores 33.30 and solves 4/50; the conservative and generic heuristics reach 54.04 and 61.01; the task-aware policy reaches 80.90 and solves 37/50. The suite is therefore neither trivial nor saturated: structured decision quality and family awareness matter.

No hosted single run matches the task-aware ceiling. The top of the hosted table is a tight cluster rather than a decisive ranking: Gemini 3.5 Flash has the highest single-run average at 67.69 (task-mix 95% interval [59.20, 75.25]), followed closely by Grok 4.5 at 66.53 ([57.81, 74.62]) and GPT-5.6 Sol at 66.39 ([57.46, 74.89]). These intervals overlap almost completely, so the 1.3-point Gemini–GPT gap is not a significant separation under task-mix resampling. Grok 4.5 solves the most tasks (33/50), while Gemini and GPT both solve 32/50. Several models clear half the suite, so the environment is tractable, but the best hosted average remains more than 13 points below task-aware calibration.

| Model | Average score | Solved | Public test | Error decisions |
|---|---:|---:|---:|---:|
| Gemini 3.5 Flash | 67.69 | 32/50 | 59.64 | 59 |
| Grok 4.5 | 66.53 | 33/50 | 56.57 | 0 |
| GPT-5.6 Sol | 66.39 | 32/50 | 58.42 | 0 |
| Kimi K3 | 65.63 | 28/50 | 58.90 | 70 |
| Claude Sonnet 5 | 63.90 | 25/50 | 68.61 | 0 |
| DeepSeek V4 Reasoner | 62.43 | 27/50 | 58.02 | 3 |
| Claude Sonnet 4.5 | 61.09 | 24/50 | 59.58 | 0 |
| DeepSeek Chat | 56.59 | 23/50 | 59.70 | 0 |
| GLM 4.5 Air | 54.78 | 23/50 | 56.20 | 0 |
| Gemini 2.5 Flash | 52.69 | 13/50 | 50.75 | 340 |
| Grok 4.3 | 52.59 | 16/50 | 59.43 | 3 |

### 5.2 Solved count versus average score

Solved count and average score answer different questions. Once a task crosses 70, solved count discards further gains; average score still rewards raising 70 to 90 and penalizes severe failures. Rank reversals follow: Gemini 3.5 Flash outscores Grok 4.5 on average but solves one fewer task; similar reversals appear for Claude Sonnet 5 versus DeepSeek V4 Reasoner and Gemini 2.5 Flash versus Grok 4.3. We therefore treat average score as primary and solved count as complementary.

### 5.3 Close top models and cross-benchmark rankings

FounderBench rankings need not match public LLM leaderboards that emphasize coding, chat, or general reasoning. Pairwise, Gemini 3.5 Flash and GPT-5.6 Sol win 21 and 19 tasks respectively (10 ties); their advantage is concentrated in different families (e.g., Gemini on Demo Day and pivot, GPT on channel, churn recovery, and runway). Split summaries also disagree with a single “best model” story: Claude Sonnet 5 has the strongest `public_test` average (68.61) despite a mid-table overall mean. Moreover, Gemini’s top average coexists with 59 provider/parser error decisions (invalid JSON and rate limits), so the row is not a clean strategic win. Together with the overlapping task-mix intervals, these facts advise reading the top hosted rows as a near-tie on this suite—not as evidence that Gemini Flash dominates GPT-class models in general.

### 5.4 Family-level behavior and failure taxonomy

Similar overall scores can hide different operating profiles. Some models do relatively well on runway or retention yet struggle on pivots and fundraising, where early actions create later prerequisites. The task-aware policy exceeds the best hosted family mean on eight of ten families; hosted models lead only on retention improvement and churn shock recovery. Family means are diagnostic: each cell averages five synthetic visible tasks and should not be read as general business capability.

Observed failures concentrate in four recurring buckets (descriptive, not mutually exclusive):

1. **Prerequisite gaps.** Pivot and Demo Day show the largest task-aware–hosted gaps (~18 and ~21 points at the best hosted family mean).
2. **Budget and runway mistakes.** Runway and fundraising require timed cost-cutting/fundraising; models often campaign or hire before stabilizing cash.
3. **Family misfit.** Retention/churn are where hosted models can match or exceed the task-aware prior.
4. **Interface load.** Provider/parser failures remain in official scores (e.g., Gemini 2.5 Flash: 340 errors on 44/50 tasks; Gemini 3.5 Flash top average coexists with 59 errors).

### 5.5 Provider-error sensitivity

Official scores retain provider and parser failures because interface reliability is part of end-to-end execution. We also stratify each run into tasks with and without recorded errors. This stratification is descriptive, not counterfactual: the subsets contain different tasks, so mean differences do not estimate an error-free score. Gemini 3.5 Flash's affected-task mean is higher than its unaffected mean, which is exactly why the split cannot be treated as a causal penalty.

## 6. Reproducibility and Responsible Use

The release includes Python source, task definitions, simulator and scoring code, adapters, a resumable runner, raw task-level JSON, submission reports, generated tables and figures, a benchmark card, datasheet, task cards, scoring rubric, prompt protocol, environment report, and checksums. Documentation follows datasheet and holistic-evaluation practice. Deterministic baselines run without commercial credentials; hosted reproduction requires provider keys and may drift with API updates.

For dataset-and-benchmark review, we emphasize accessibility of a self-contained package with key-free baselines; documentation of actions, rubrics, and schemas; impact as a shared test bed for resource allocation and recovery rather than business-plan prose; bounded representativeness of balanced synthetic families; reproducibility via fixed seeds, raw outcomes, hashes, and generators; and responsible use through synthetic data plus explicit bans on investment or deployment claims.

Accessibility still depends on final public repository and license metadata. Any post-result task or rubric change must create a new version rather than silently alter the reported suite.

The release also freezes a 20-task private holdout (two tasks per family), with public fingerprint commitments and an evaluator-held secret. Private task definitions are not published; all hosted results in this paper are on the visible public suite, so there is no official private leaderboard.

## 7. Limitations

**Synthetic validity.** Hand-designed, largely deterministic transitions approximate only a subset of startup dynamics and omit market shocks, adversarial feedback, and many stochastic couplings; passing does not imply real-market judgment.

**Visible public suite and contamination.** All 50 public task definitions are released; `public_test` is a reporting split, not a hidden exam. A frozen private task list exists for contamination-resistant evaluation, but this paper does not report hosted scores on it, so there is no official private leaderboard. Without repeated hosted runs or private hosted scores, sampling variance and contamination risk remain only partially quantified.

**Single hosted runs and missing protocol ablations.** Task-mix intervals do not capture sampling variance, provider drift, or repeated-run reliability. All hosted rows are single runs on visible public tasks. We also lack systematic ablations of prompt protocols, hosted action-schema variants, alternative solve thresholds, and sensitivity sweeps over observation-noise intensity or cost coefficients.

**Provider dependence versus strategy.** Availability, rate limits, aliases, and formatting affect end-to-end scores; because provider/parser errors remain in official means, strategic competence is partially conflated with API/adaptor robustness. Diagnostics expose load but cannot fully disentangle infrastructure and strategy without a retry ablation.

**Calibration priors.** The task-aware heuristic encodes family-specific priors and can overfit the visible suite. There is no human-founder calibration and no official private leaderboard of hosted models yet; scores do not establish real-world startup competence. The 80.90 task-aware score is a synthetic ceiling, not a human reference.

**Representativeness.** Ten balanced families omit legal, accounting, hiring, ethics, security, and many domain-specific decisions.

## 8. Conclusion

FounderBench asks whether agents can turn noisy observations into consequential startup-like actions under bounded resources. Its central design choice is to score deterministic simulated outcomes rather than persuasive prose. Eleven hosted configurations show substantial capability but remain below a task-aware calibration policy, with heterogeneous family behavior and solved-versus-average rank reversals. The release ties every reported number to executable evidence. FounderBench should be read as a controlled synthetic sequential-decision test—not a predictor of company success. Priority upgrades are repeated hosted runs, private hosted evaluation, interface-retry and environment-sensitivity ablations, and expert/founder calibration.

Also see `outputs/founderbench-paper-model-registry.json` for validated hosted evidence digests used by the paper tables.
