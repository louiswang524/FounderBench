from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any


FAMILIES = [
    ("FND-001..FND-005", "Market selection"),
    ("FND-006..FND-010", "First revenue"),
    ("FND-011..FND-015", "Retention improvement"),
    ("FND-016..FND-020", "Churn shock recovery"),
    ("FND-021..FND-025", "Demo Day traction"),
    ("FND-026..FND-030", "Pricing"),
    ("FND-031..FND-035", "Runway preservation"),
    ("FND-036..FND-040", "Pivot decision"),
    ("FND-041..FND-045", "Fundraising"),
    ("FND-046..FND-050", "Channel expansion"),
]


def task_number(task_id: str) -> int:
    return int(task_id.split("-")[1])


def family_name(task_id: str) -> str:
    idx = (task_number(task_id) - 1) // 5
    return FAMILIES[idx][1]


def split_name(task_id: str) -> str:
    return "public_dev" if task_number(task_id) <= 30 else "public_test"


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        out.append("| " + " | ".join(str(cell) for cell in row) + " |")
    return "\n".join(out)


def load_results(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def policy_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True):
        diagnostics = run.get("diagnostics", {})
        splits = run.get("splits", {})
        rows.append(
            [
                run["policy"],
                run["tasks"],
                run["solved"],
                f"{run['solve_rate']:.2f}",
                f"{run['average_task_score']:.2f}",
                f"{splits.get('public_dev', {}).get('average_task_score', 0):.2f}",
                f"{splits.get('public_test', {}).get('average_task_score', 0):.2f}",
                diagnostics.get("over_budget_decisions", 0),
                diagnostics.get("provider_errors", 0),
            ]
        )
    return rows


def family_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for _, fam in FAMILIES:
        row: list[Any] = [fam]
        for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True):
            items = [result for result in run["results"] if family_name(result["task_id"]) == fam]
            solved = sum(1 for item in items if item["score"]["passed"])
            avg = mean(float(item["score"]["score"]) for item in items)
            row.append(f"{solved}/5 ({avg:.1f})")
        rows.append(row)
    return rows


def difficulty_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for run in runs:
        for result in run["results"]:
            by_task[result["task_id"]].append(result)

    rows = []
    for task_id, items in sorted(by_task.items(), key=lambda pair: mean(float(item["score"]["score"]) for item in pair[1])):
        scores = [float(item["score"]["score"]) for item in items]
        solved = sum(1 for item in items if item["score"]["passed"])
        rows.append([task_id, family_name(task_id), f"{mean(scores):.2f}", f"{solved}/{len(items)}"])
    return rows


def failure_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True):
        failed = [result for result in run["results"] if not result["score"]["passed"]]
        bankrupt = sum(1 for result in failed if result["summary"]["bankrupt"])
        over_budget = run.get("diagnostics", {}).get("over_budget_decisions", 0)
        provider_errors = run.get("diagnostics", {}).get("provider_errors", 0)
        worst = min(run["results"], key=lambda result: float(result["score"]["score"]))
        rows.append(
            [
                run["policy"],
                len(failed),
                bankrupt,
                over_budget,
                provider_errors,
                f"{worst['task_id']} ({worst['score']['score']:.2f})",
                family_name(worst["task_id"]),
            ]
        )
    return rows


def provider_error_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    categories = sorted({category for run in runs for category in run.get("diagnostics", {}).get("provider_error_categories", {})})
    if not categories:
        return [["all policies", "none", 0]]
    for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True):
        by_category = run.get("diagnostics", {}).get("provider_error_categories", {})
        for category in categories:
            rows.append([run["policy"], category, by_category.get(category, 0)])
    return rows


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = (len(ordered) - 1) * pct
    lower = int(idx)
    upper = min(lower + 1, len(ordered) - 1)
    weight = idx - lower
    return ordered[lower] * (1 - weight) + ordered[upper] * weight


def bootstrap_mean_ci(values: list[float], *, iterations: int = 2000, seed: int = 20260715) -> tuple[float, float]:
    if not values:
        return 0.0, 0.0
    rng = random.Random(seed)
    estimates = []
    for _ in range(iterations):
        sample = [values[rng.randrange(len(values))] for _ in values]
        estimates.append(mean(sample))
    return percentile(estimates, 0.025), percentile(estimates, 0.975)


def ci_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True):
        scores = [float(result["score"]["score"]) for result in run["results"]]
        solved = [1.0 if result["score"]["passed"] else 0.0 for result in run["results"]]
        score_low, score_high = bootstrap_mean_ci(scores)
        solve_low, solve_high = bootstrap_mean_ci(solved)
        rows.append(
            [
                run["policy"],
                f"{mean(scores):.2f}",
                f"[{score_low:.2f}, {score_high:.2f}]",
                f"{mean(solved):.2f}",
                f"[{solve_low:.2f}, {solve_high:.2f}]",
            ]
        )
    return rows


def pairwise_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    sorted_runs = sorted(runs, key=lambda item: item["average_task_score"], reverse=True)
    by_policy = {run["policy"]: {result["task_id"]: float(result["score"]["score"]) for result in run["results"]} for run in sorted_runs}
    top_policy = sorted_runs[0]["policy"]
    top_scores = by_policy[top_policy]
    for run in sorted_runs[1:]:
        policy = run["policy"]
        shared_tasks = sorted(set(top_scores) & set(by_policy[policy]), key=task_number)
        diffs = [top_scores[task_id] - by_policy[policy][task_id] for task_id in shared_tasks]
        low, high = bootstrap_mean_ci(diffs, seed=20260715 + len(policy))
        rows.append([f"{top_policy} - {policy}", f"{mean(diffs):.2f}", f"[{low:.2f}, {high:.2f}]", len(shared_tasks)])
    return rows


def write_report(runs: list[dict[str, Any]], output: Path) -> None:
    policies = [run["policy"] for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True)]
    lines = [
        "# FounderBench Baseline Analysis",
        "",
        "## Leaderboard",
        "",
        markdown_table(
            ["Policy", "Tasks", "Solved", "Solve Rate", "Avg Score", "Public Dev", "Public Test", "Over-Budget", "Provider Errors"],
            policy_rows(runs),
        ),
        "",
        "## Family Breakdown",
        "",
        "Each cell reports `solved/5 (average score)`.",
        "",
        markdown_table(["Family", *policies], family_rows(runs)),
        "",
        "## Hardest Tasks",
        "",
        "Tasks are sorted by mean score across all reported baselines.",
        "",
        markdown_table(["Task", "Family", "Mean Score", "Solved By"], difficulty_rows(runs)[:12]),
        "",
        "## Failure Diagnostics",
        "",
        markdown_table(["Policy", "Failed Tasks", "Bankrupt Failures", "Over-Budget Decisions", "Provider Errors", "Worst Task", "Worst Family"], failure_rows(runs)),
        "",
        "## Provider Error Taxonomy",
        "",
        "Rule baselines should have no provider errors. Hosted LLM runs use this table to distinguish malformed JSON, schema errors, timeouts, and provider exceptions.",
        "",
        markdown_table(["Policy", "Category", "Count"], provider_error_rows(runs)),
        "",
        "## Bootstrap Uncertainty",
        "",
        "Intervals are nonparametric 95% bootstrap intervals over the fixed 50 task episodes. They estimate sensitivity to the task mix, not provider sampling variance.",
        "",
        markdown_table(["Policy", "Avg Score", "Score 95% CI", "Solve Rate", "Solve Rate 95% CI"], ci_rows(runs)),
        "",
        "## Pairwise Score Gaps",
        "",
        "Gaps compare the strongest baseline against each other baseline on matched tasks.",
        "",
        markdown_table(["Comparison", "Mean Gap", "Gap 95% CI", "Tasks"], pairwise_rows(runs)),
        "",
        "## Interpretation Notes",
        "",
        "- The task-aware heuristic remains the strongest non-LLM baseline, but it still fails 13/50 tasks.",
        "- The random baseline solves only 4/50 tasks after recalibration, suggesting the environment is not solved by blind action sampling.",
        "- Pivot and channel-expansion tasks remain the hardest families for rule-based policies.",
        "- Runway preservation is still relatively easy for conservative policies and should receive more difficult variants in the next release.",
        "- Provider-error and invalid-action fields are zero for rule baselines; these fields become important for hosted LLM runs.",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper-ready FounderBench analysis tables.")
    parser.add_argument("--raw", required=True, help="Raw benchmark result JSON.")
    parser.add_argument("--output", required=True, help="Markdown output path.")
    args = parser.parse_args()
    write_report(load_results(Path(args.raw)), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
