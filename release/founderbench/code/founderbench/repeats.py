from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import bootstrap_mean_ci, markdown_table
from .submission import validate_run
from .task_runner import run_suite


def run_repeated(policy: str, seeds: list[int]) -> dict[str, Any]:
    runs = []
    for seed in seeds:
        run = run_suite(policy, seed=seed)
        run["policy"] = policy
        run["run_seed"] = seed
        runs.append(run)
    return {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "experiment": "repeated_run_seed_sweep",
        "policy": policy,
        "seeds": seeds,
        "runs": runs,
    }


def validate_repeated(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != "0.3.0":
        problems.append("Repeated-run payload version must be 0.3.0.")
    runs = payload.get("runs")
    if not isinstance(runs, list) or not runs:
        problems.append("Repeated-run payload must contain a non-empty runs array.")
        return problems
    seeds = [run.get("run_seed") for run in runs]
    if len(seeds) != len(set(seeds)):
        problems.append("Repeated-run payload contains duplicate run_seed values.")
    for run in runs:
        problems.extend(validate_run(run))
    return problems


def summary_rows(payload: dict[str, Any]) -> list[list[Any]]:
    rows = []
    for run in payload["runs"]:
        rows.append(
            [
                run.get("run_seed"),
                run["tasks"],
                run["solved"],
                f"{run['solve_rate']:.2f}",
                f"{run['average_task_score']:.2f}",
                run["diagnostics"].get("invalid_actions", 0),
                run["diagnostics"].get("over_budget_decisions", 0),
            ]
        )
    return rows


def interval_rows(payload: dict[str, Any]) -> list[list[Any]]:
    scores = [float(run["average_task_score"]) for run in payload["runs"]]
    solve_rates = [float(run["solve_rate"]) for run in payload["runs"]]
    score_low, score_high = bootstrap_mean_ci(scores, iterations=2000, seed=20260715)
    solve_low, solve_high = bootstrap_mean_ci(solve_rates, iterations=2000, seed=20260716)
    return [
        ["average_task_score", f"{mean(scores):.2f}", f"[{score_low:.2f}, {score_high:.2f}]", len(scores)],
        ["solve_rate", f"{mean(solve_rates):.2f}", f"[{solve_low:.2f}, {solve_high:.2f}]", len(solve_rates)],
    ]


def write_report(payload: dict[str, Any], output: Path) -> None:
    problems = validate_repeated(payload)
    lines = [
        "# FounderBench Repeated-Run Report",
        "",
        f"Policy: `{payload.get('policy')}`",
        f"Seeds: `{payload.get('seeds')}`",
        "",
        "## Validation",
        "",
    ]
    if problems:
        lines.extend(["Status: FAIL", "", *[f"- {problem}" for problem in problems]])
    else:
        lines.append("Status: PASS")
    lines.extend(
        [
            "",
            "## Per-Run Results",
            "",
            markdown_table(["Seed", "Tasks", "Solved", "Solve Rate", "Avg Score", "Invalid Actions", "Over-Budget"], summary_rows(payload)),
            "",
            "## Across-Run Intervals",
            "",
            "Intervals summarize variation across repeated runs. For hosted LLMs, this should be reported in addition to task-mix bootstrap intervals.",
            "",
            markdown_table(["Metric", "Mean", "95% CI", "Runs"], interval_rows(payload)),
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run repeated FounderBench evaluations over policy seeds.")
    parser.add_argument("--policy", default="random")
    parser.add_argument("--seeds", default="0,1,2,3,4", help="Comma-separated integer seeds.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()

    seeds = [int(item.strip()) for item in args.seeds.split(",") if item.strip()]
    payload = run_repeated(args.policy, seeds)
    problems = validate_repeated(payload)
    Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_output).write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_report(payload, Path(args.markdown_output))
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
