from __future__ import annotations

import argparse
import json
from pathlib import Path

from .task_runner import run_suite


def summarize(result: dict) -> dict:
    return {
        "policy": result["policy"],
        "tasks": result["tasks"],
        "solved": result["solved"],
        "solve_rate": result["solve_rate"],
        "average_task_score": result["average_task_score"],
        "public_dev_score": result.get("splits", {}).get("public_dev", {}).get("average_task_score"),
        "public_test_score": result.get("splits", {}).get("public_test", {}).get("average_task_score"),
        "shutdown_rate": round(
            sum(1 for item in result["results"] if item["summary"]["bankrupt"]) / result["tasks"],
            3,
        ),
        "average_final_cash": round(
            sum(float(item["summary"]["cash"]) for item in result["results"]) / result["tasks"],
            2,
        ),
        "average_risk_penalty": round(
            sum(float(item["summary"]["risk_penalty"]) for item in result["results"]) / result["tasks"],
            2,
        ),
        "invalid_actions": result["diagnostics"]["invalid_actions"],
        "over_budget_decisions": result["diagnostics"]["over_budget_decisions"],
        "provider_errors": result["diagnostics"]["provider_errors"],
        "provider_error_categories": result["diagnostics"].get("provider_error_categories", {}),
        "avg_actions_per_task": round(result["diagnostics"]["total_actions"] / result["tasks"], 2),
        "simulated_api_cost": result["diagnostics"]["simulated_api_cost"],
        "provider_total_tokens": result["diagnostics"]["provider_total_tokens"],
        "estimated_provider_cost_usd": result["diagnostics"]["estimated_provider_cost_usd"],
        "decision_latency_s": result["diagnostics"]["decision_latency_s"],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FounderBench baselines and emit leaderboard.")
    parser.add_argument("--policy", action="append", default=["random", "conservative", "heuristic", "task_heuristic"])
    parser.add_argument("--output", required=True)
    parser.add_argument("--raw-output")
    args = parser.parse_args()

    raw = [run_suite(policy) for policy in args.policy]
    leaderboard = {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "rows": sorted([summarize(result) for result in raw], key=lambda row: row["average_task_score"], reverse=True),
    }

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(leaderboard, indent=2), encoding="utf-8")
    if args.raw_output:
        Path(args.raw_output).write_text(json.dumps(raw, indent=2), encoding="utf-8")
    print(json.dumps(leaderboard, indent=2))


if __name__ == "__main__":
    main()
