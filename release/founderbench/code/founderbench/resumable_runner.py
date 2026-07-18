from __future__ import annotations

import argparse
import json
from pathlib import Path

from .analysis import split_name
from .task_runner import make_policy, run_task
from .tasks import TASKS, get_task


def summarize(results: list[dict], policy_name: str, seed: int = 0) -> dict:
    solved = sum(1 for result in results if result["score"]["passed"])
    average = sum(float(result["score"]["score"]) for result in results) / len(results) if results else 0.0
    diagnostics = {
        "invalid_actions": sum(int(result.get("diagnostics", {}).get("invalid_actions", 0)) for result in results),
        "over_budget_decisions": sum(int(result.get("diagnostics", {}).get("over_budget_decisions", 0)) for result in results),
        "provider_errors": sum(int(result.get("diagnostics", {}).get("provider_errors", 0)) for result in results),
        "provider_error_categories": {},
        "total_actions": sum(int(result.get("diagnostics", {}).get("total_actions", 0)) for result in results),
        "decision_latency_s": round(sum(float(result.get("diagnostics", {}).get("decision_latency_s", 0.0)) for result in results), 4),
        "simulated_api_cost": round(sum(float(result.get("diagnostics", {}).get("simulated_api_cost", 0.0)) for result in results), 2),
        "provider_prompt_tokens": sum(int(result.get("diagnostics", {}).get("provider_prompt_tokens", 0)) for result in results),
        "provider_completion_tokens": sum(int(result.get("diagnostics", {}).get("provider_completion_tokens", 0)) for result in results),
        "provider_total_tokens": sum(int(result.get("diagnostics", {}).get("provider_total_tokens", 0)) for result in results),
        "estimated_provider_cost_usd": round(sum(float(result.get("diagnostics", {}).get("estimated_provider_cost_usd", 0.0)) for result in results), 6),
    }
    for result in results:
        for category, count in result.get("diagnostics", {}).get("provider_error_categories", {}).items():
            diagnostics["provider_error_categories"][category] = diagnostics["provider_error_categories"].get(category, 0) + int(count)
    splits = {}
    for name in ("public_dev", "public_test"):
        split_results = [result for result in results if split_name(result["task_id"]) == name]
        if split_results:
            split_solved = sum(1 for result in split_results if result["score"]["passed"])
            splits[name] = {
                "tasks": len(split_results),
                "solved": split_solved,
                "solve_rate": round(split_solved / len(split_results), 3),
                "average_task_score": round(sum(float(result["score"]["score"]) for result in split_results) / len(split_results), 2),
            }
    return {
        "benchmark": "FounderBench",
        "benchmark_version": "0.3.0",
        "policy": policy_name,
        "run_seed": seed,
        "tasks": len(results),
        "solved": solved,
        "solve_rate": round(solved / len(results), 3) if results else 0.0,
        "average_task_score": round(average, 2),
        "diagnostics": diagnostics,
        "splits": splits,
        "results": results,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FounderBench tasks and save after every task.")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--task", action="append")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--audit", action="store_true", help="Include redacted provider call records in each task trace.")
    parser.add_argument("--seed", type=int, default=0, help="Repeat/run index recorded in the output and passed to deterministic policies.")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    existing: list[dict] = []
    if args.resume and output.exists():
        existing = json.loads(output.read_text(encoding="utf-8")).get("results", [])
    completed = {result["task_id"] for result in existing}
    tasks = [get_task(task_id) for task_id in args.task] if args.task else TASKS
    policy = make_policy(args.policy, seed=args.seed)

    results = list(existing)
    for task in tasks:
        if task.task_id in completed:
            continue
        result = run_task(task, policy, trace=args.audit, audit=args.audit)
        results.append(result)
        output.write_text(json.dumps(summarize(results, args.policy, seed=args.seed), indent=2), encoding="utf-8")
        print(f"{task.task_id} score={result['score']['score']} passed={result['score']['passed']}")

    print(json.dumps(summarize(results, args.policy, seed=args.seed), indent=2))


if __name__ == "__main__":
    main()
