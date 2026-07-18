# FounderBench Related Work Notes

This note records verified sources for positioning FounderBench. It is intentionally concise and source-linked so the paper draft can later be converted to BibTeX or LaTeX citations.

## LLM Agents and Tool Use

| Source | Verified Link | Relevance to FounderBench |
|---|---|---|
| ReAct: Synergizing Reasoning and Acting in Language Models | https://arxiv.org/abs/2210.03629 | Introduces interleaved reasoning/action prompting for LLMs interacting with external environments. FounderBench shares the reason-act framing but evaluates business outcomes rather than QA/webshop trajectories. |
| Toolformer: Language Models Can Teach Themselves to Use Tools | https://arxiv.org/abs/2302.04761 | Studies language models learning when/how to call tools. FounderBench similarly requires structured tool/action use, but through a controlled startup simulator. |
| Voyager: An Open-Ended Embodied Agent with Large Language Models | https://arxiv.org/abs/2305.16291 | Demonstrates long-horizon LLM agency with feedback, skills, and self-verification in Minecraft. FounderBench targets long-horizon business operation rather than embodied exploration. |

## General Agent Benchmarks

| Source | Verified Link | Relevance to FounderBench |
|---|---|---|
| AgentBench: Evaluating LLMs as Agents | https://arxiv.org/abs/2308.03688 | Multi-environment benchmark for evaluating LLMs as agents. FounderBench narrows to startup/economic operations and richer business state. |
| GAIA: a benchmark for General AI Assistants | https://arxiv.org/abs/2311.12983 | Evaluates assistants on real-world questions requiring reasoning, multimodality, web browsing, and tool use. FounderBench differs by using sequential simulated company outcomes instead of short-answer tasks. |
| SWE-bench: Can Language Models Resolve Real-World GitHub Issues? | https://arxiv.org/abs/2310.06770 | Evaluates agents/models on real GitHub issue resolution. It motivates outcome-validated tasks; FounderBench applies outcome validation to business operations. |

## Web, Workplace, and Tool-Interaction Benchmarks

| Source | Verified Link | Relevance to FounderBench |
|---|---|---|
| WebArena: A Realistic Web Environment for Building Autonomous Agents | https://arxiv.org/abs/2307.13854 | Provides realistic, reproducible web environments for agents. FounderBench similarly emphasizes reproducibility, but uses a compact economic simulator rather than browser tasks. |
| tau-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains | https://arxiv.org/abs/2406.12045 | Evaluates tool-using agents in dynamic user/domain-policy interactions and introduces reliability-oriented evaluation. FounderBench shares concern for consistency and policy/action validity. |
| TheAgentCompany: Benchmarking LLM Agents on Consequential Real World Tasks | https://arxiv.org/abs/2412.14161 | Simulates a software company workplace and evaluates digital-worker tasks. FounderBench is closest in spirit but evaluates agents as company operators optimizing startup outcomes rather than workers completing workplace tasks. |
| WorkArena | https://servicenow.github.io/WorkArena/ | Enterprise web-agent benchmark in ServiceNow-style tasks. FounderBench differs by focusing on high-level company strategy and economic consequences. |

## Economic and Business-Oriented Agent Evaluation

| Source | Verified Link | Relevance to FounderBench |
|---|---|---|
| EconWebArena: Benchmarking Autonomous Agents on Economic Tasks in Realistic Web Environments | https://arxiv.org/abs/2506.08136 | Evaluates agents on economic information tasks across real websites. FounderBench evaluates economic operation and company outcomes rather than information retrieval. |
| EnterpriseArena: Can LLM Agents Be CFOs? | https://arxiv.org/abs/2603.23638 | Evaluates long-horizon enterprise resource allocation under uncertainty. FounderBench is complementary: startup-agent operation with market selection, revenue, retention, pivot, and fundraising tasks. |

## Positioning Summary

FounderBench is closest to agent benchmarks that require interaction and outcome validation, but its contribution is a controlled startup-operating environment where the score depends on simulated company state over time. It fills a gap between:

- general agent/task benchmarks such as AgentBench and GAIA,
- realistic web/workplace benchmarks such as WebArena, WorkArena, tau-bench, and TheAgentCompany,
- economic/resource-allocation benchmarks such as EconWebArena and EnterpriseArena.

The distinctive evaluation target is not whether an agent can answer, browse, patch code, or complete workplace tasks, but whether it can repeatedly allocate scarce startup resources to produce durable business value.
