from __future__ import annotations

import time
from dataclasses import asdict

from .env import MoneyBenchEnv
from .llm_policy import (
    AnthropicTaskPolicy,
    DeepSeekSelfConsistencyTaskPolicy,
    DeepSeekTaskPolicy,
    GeminiTaskPolicy,
    GLMTaskPolicy,
    KimiTaskPolicy,
    LlamaTaskPolicy,
    MistralTaskPolicy,
    OpenAICompatibleTaskPolicy,
    OpenAIHostedTaskPolicy,
    QwenTaskPolicy,
    XAITaskPolicy,
)
from .policies import Policy, get_policy
from .provider_adapter import classify_provider_exception
from .schema import Action, StepResult
from .tasks import TASKS, StartupTask, get_task, validate_actions


def run_task(task: StartupTask, policy: Policy, trace: bool = False, audit: bool = False) -> dict:
    env = MoneyBenchEnv(seed=task.seed, weeks=task.weeks)
    observation = env.reset()
    task.setup(env)
    observation = env.observe()
    results: list[StepResult] = []
    events = []
    invalid_action_count = 0
    over_budget_action_count = 0
    provider_error_count = 0
    total_action_count = 0
    total_decision_latency_s = 0.0
    total_prompt_tokens = 0
    total_completion_tokens = 0
    total_provider_tokens = 0
    estimated_provider_cost_usd = 0.0
    provider_error_categories: dict[str, int] = {}

    while not env.done():
        action_error = None
        started = time.perf_counter()
        try:
            if hasattr(policy, "act_task"):
                if policy.__class__.__name__ in {
                    "OpenAICompatibleTaskPolicy",
                    "DeepSeekTaskPolicy",
                    "DeepSeekSelfConsistencyTaskPolicy",
                    "AnthropicTaskPolicy",
                    "GeminiTaskPolicy",
                    "OpenAIHostedTaskPolicy",
                    "KimiTaskPolicy",
                    "QwenTaskPolicy",
                    "MistralTaskPolicy",
                    "LlamaTaskPolicy",
                    "GLMTaskPolicy",
                    "XAITaskPolicy",
                }:
                    actions = policy.act_task(task, observation)  # type: ignore[attr-defined]
                else:
                    actions = policy.act_task(task.task_id, observation)  # type: ignore[attr-defined]
            else:
                actions = policy.act(observation)
        except Exception as exc:
            action_error = f"{type(exc).__name__}: {exc}"
            provider_error_count += 1
            category = classify_provider_exception(exc)
            provider_error_categories[category] = provider_error_categories.get(category, 0) + 1
            actions = [Action("do_nothing", metadata={"error": action_error})]
        total_decision_latency_s += time.perf_counter() - started
        provider_calls = policy.consume_provider_calls() if hasattr(policy, "consume_provider_calls") else []  # type: ignore[attr-defined]
        for call in provider_calls:
            usage = call.get("usage", {})
            total_prompt_tokens += int(usage.get("prompt_tokens", 0))
            total_completion_tokens += int(usage.get("completion_tokens", 0))
            total_provider_tokens += int(usage.get("total_tokens", 0))
            estimated_provider_cost_usd += float(call.get("estimated_cost_usd", 0.0) or 0.0)
        invalid_action_count += sum(1 for action in actions if action.type not in task.allowed_actions)
        over_budget_action_count += int(sum(max(0.0, action.budget) for action in actions) > observation.cash)
        total_action_count += len(actions)
        actions = validate_actions(task, actions)
        result = env.step(actions)
        if action_error:
            result.notes.append(f"Policy error: {action_error}")
        results.append(result)
        if trace:
            events.append(
                {
                    "week": observation.week,
                    "observation": asdict(observation),
                    "actions": [asdict(action) for action in actions],
                    "result": asdict(result),
                    **({"provider_calls": provider_calls} if audit else {}),
                }
            )
        observation = env.observe()

    score = task.score(env, results)
    weeks_run = len(results)
    return {
        "task_id": task.task_id,
        "name": task.name,
        "description": task.description,
        "score": asdict(score),
        "summary": env.summary(),
        "diagnostics": {
            "weeks_run": weeks_run,
            "total_actions": total_action_count,
            "avg_actions_per_week": round(total_action_count / weeks_run, 3) if weeks_run else 0.0,
            "invalid_actions": invalid_action_count,
            "over_budget_decisions": over_budget_action_count,
            "provider_errors": provider_error_count,
            "provider_error_categories": provider_error_categories,
            "decision_latency_s": round(total_decision_latency_s, 4),
            "simulated_api_cost": round(env.state.cumulative_api_cost, 2),
            "provider_prompt_tokens": total_prompt_tokens,
            "provider_completion_tokens": total_completion_tokens,
            "provider_total_tokens": total_provider_tokens,
            "estimated_provider_cost_usd": round(estimated_provider_cost_usd, 6),
        },
        "events": events,
    }


def make_policy(policy_name: str, seed: int = 0) -> Policy:
    if policy_name == "llm":
        return OpenAICompatibleTaskPolicy()  # type: ignore[return-value]
    if policy_name == "openai":
        return OpenAIHostedTaskPolicy()  # type: ignore[return-value]
    if policy_name == "deepseek":
        return DeepSeekTaskPolicy()  # type: ignore[return-value]
    if policy_name == "deepseek_sc":
        return DeepSeekSelfConsistencyTaskPolicy()  # type: ignore[return-value]
    if policy_name == "anthropic":
        return AnthropicTaskPolicy()  # type: ignore[return-value]
    if policy_name == "gemini":
        return GeminiTaskPolicy()  # type: ignore[return-value]
    if policy_name == "kimi":
        return KimiTaskPolicy()  # type: ignore[return-value]
    if policy_name == "qwen":
        return QwenTaskPolicy()  # type: ignore[return-value]
    if policy_name == "mistral":
        return MistralTaskPolicy()  # type: ignore[return-value]
    if policy_name == "llama":
        return LlamaTaskPolicy()  # type: ignore[return-value]
    if policy_name == "glm":
        return GLMTaskPolicy()  # type: ignore[return-value]
    if policy_name == "xai":
        return XAITaskPolicy()  # type: ignore[return-value]
    return get_policy(policy_name, seed=seed)


def run_suite(policy_name: str, trace: bool = False, task_ids: list[str] | None = None, audit: bool = False, seed: int = 0) -> dict:
    policy = make_policy(policy_name, seed=seed)
    selected_tasks = [get_task(task_id) for task_id in task_ids] if task_ids else TASKS
    task_results = [run_task(task, policy, trace=trace, audit=audit) for task in selected_tasks]
    solved = sum(1 for result in task_results if result["score"]["passed"])
    average = sum(float(result["score"]["score"]) for result in task_results) / len(task_results)
    diagnostics = {
        "invalid_actions": sum(int(result["diagnostics"]["invalid_actions"]) for result in task_results),
        "over_budget_decisions": sum(int(result["diagnostics"]["over_budget_decisions"]) for result in task_results),
        "provider_errors": sum(int(result["diagnostics"]["provider_errors"]) for result in task_results),
        "provider_error_categories": {},
        "total_actions": sum(int(result["diagnostics"]["total_actions"]) for result in task_results),
        "decision_latency_s": round(sum(float(result["diagnostics"]["decision_latency_s"]) for result in task_results), 4),
        "simulated_api_cost": round(sum(float(result["diagnostics"]["simulated_api_cost"]) for result in task_results), 2),
        "provider_prompt_tokens": sum(int(result["diagnostics"]["provider_prompt_tokens"]) for result in task_results),
        "provider_completion_tokens": sum(int(result["diagnostics"]["provider_completion_tokens"]) for result in task_results),
        "provider_total_tokens": sum(int(result["diagnostics"]["provider_total_tokens"]) for result in task_results),
        "estimated_provider_cost_usd": round(sum(float(result["diagnostics"]["estimated_provider_cost_usd"]) for result in task_results), 6),
    }
    for result in task_results:
        for category, count in result["diagnostics"].get("provider_error_categories", {}).items():
            diagnostics["provider_error_categories"][category] = diagnostics["provider_error_categories"].get(category, 0) + int(count)
    split_summary = {}
    for split_name, predicate in {
        "public_dev": lambda task_id: int(task_id.split("-")[1]) <= 30,
        "public_test": lambda task_id: 30 < int(task_id.split("-")[1]) <= 50,
    }.items():
        split_results = [result for result in task_results if predicate(result["task_id"])]
        if split_results:
            split_solved = sum(1 for result in split_results if result["score"]["passed"])
            split_summary[split_name] = {
                "tasks": len(split_results),
                "solved": split_solved,
                "solve_rate": round(split_solved / len(split_results), 3),
                "average_task_score": round(sum(float(result["score"]["score"]) for result in split_results) / len(split_results), 2),
            }
    return {
        "policy": policy_name,
        "run_seed": seed,
        "tasks": len(task_results),
        "solved": solved,
        "solve_rate": round(solved / len(task_results), 3),
        "average_task_score": round(average, 2),
        "diagnostics": diagnostics,
        "splits": split_summary,
        "results": task_results,
    }
