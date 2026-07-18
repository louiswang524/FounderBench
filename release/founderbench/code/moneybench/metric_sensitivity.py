from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean, median
from typing import Any

from .analysis import markdown_table, task_number


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def load_runs(path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def rank_desc(values: dict[str, float]) -> list[str]:
    return sorted(values, key=lambda key: (-values[key], key))


def rank_positions(values: dict[str, float]) -> dict[str, int]:
    return {policy: idx + 1 for idx, policy in enumerate(rank_desc(values))}


def spearman_rank_correlation(a: dict[str, float], b: dict[str, float]) -> float:
    shared = sorted(set(a) & set(b))
    n = len(shared)
    if n < 2:
        return 1.0
    rank_a = rank_positions({key: a[key] for key in shared})
    rank_b = rank_positions({key: b[key] for key in shared})
    d2 = sum((rank_a[key] - rank_b[key]) ** 2 for key in shared)
    return round(1 - (6 * d2) / (n * (n * n - 1)), 4)


def minmax(value: float, low: float, high: float) -> float:
    if high <= low:
        return 0.5
    return (value - low) / (high - low)


def task_normalized_business_scores(runs: list[dict[str, Any]]) -> dict[str, float]:
    by_task: dict[str, list[tuple[str, float]]] = {}
    for run in runs:
        for result in run["results"]:
            by_task.setdefault(result["task_id"], []).append((run["policy"], float(result["summary"]["score"])))
    per_policy: dict[str, list[float]] = {run["policy"]: [] for run in runs}
    for task_id in sorted(by_task, key=task_number):
        scores = [score for _, score in by_task[task_id]]
        low, high = min(scores), max(scores)
        for policy, score in by_task[task_id]:
            per_policy[policy].append(100 * minmax(score, low, high))
    return {policy: round(mean(values), 2) for policy, values in per_policy.items()}


def build_report(raw_path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> dict[str, Any]:
    runs = load_runs(raw_path)
    policy_results = {
        run["policy"]: {
            "task_scores": [float(result["score"]["score"]) for result in run["results"]],
            "passed": [1.0 if result["score"]["passed"] else 0.0 for result in run["results"]],
            "company_scores": [float(result["summary"]["score"]) for result in run["results"]],
            "cash": [float(result["summary"]["cash"]) for result in run["results"]],
            "revenue": [float(result["summary"]["cumulative_revenue"]) for result in run["results"]],
            "cost": [float(result["summary"]["cumulative_cost"]) for result in run["results"]],
            "risk": [float(result["summary"]["risk_penalty"]) for result in run["results"]],
            "bankrupt": [1.0 if result["summary"]["bankrupt"] else 0.0 for result in run["results"]],
        }
        for run in runs
    }
    normalized_business = task_normalized_business_scores(runs)
    metric_values: dict[str, dict[str, float]] = {
        "average_task_score": {policy: round(mean(values["task_scores"]), 2) for policy, values in policy_results.items()},
        "solve_rate": {policy: round(mean(values["passed"]), 4) for policy, values in policy_results.items()},
        "median_task_score": {policy: round(median(values["task_scores"]), 2) for policy, values in policy_results.items()},
        "task_normalized_business_score": normalized_business,
        "average_final_cash": {policy: round(mean(values["cash"]), 2) for policy, values in policy_results.items()},
        "average_cumulative_revenue": {policy: round(mean(values["revenue"]), 2) for policy, values in policy_results.items()},
        "survival_rate": {policy: round(1 - mean(values["bankrupt"]), 4) for policy, values in policy_results.items()},
        "low_risk_score": {policy: round(100 - min(100, mean(values["risk"]) / 20), 2) for policy, values in policy_results.items()},
        "revenue_efficiency": {
            policy: round(mean(values["revenue"]) / max(1.0, mean(values["cost"])), 4)
            for policy, values in policy_results.items()
        },
    }
    primary = metric_values["average_task_score"]
    metric_rows = []
    for metric, values in metric_values.items():
        ranking = rank_desc(values)
        metric_rows.append(
            {
                "metric": metric,
                "leader": ranking[0],
                "ranking": ranking,
                "spearman_with_primary": spearman_rank_correlation(primary, values),
                "values": values,
            }
        )
    primary_rank = rank_desc(primary)
    rank_changes = []
    for row in metric_rows:
        positions = rank_positions(row["values"])
        primary_positions = rank_positions(primary)
        rank_changes.append(
            {
                "metric": row["metric"],
                "max_rank_shift": max(abs(positions[policy] - primary_positions[policy]) for policy in primary),
                "same_leader_as_primary": row["leader"] == primary_rank[0],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Metric sensitivity analysis for deterministic baselines. The official ranking uses bounded task score; alternatives test whether unbounded money-like simulator signals change the qualitative conclusion.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "policies": primary_rank,
        "primary_metric": "average_task_score",
        "metric_rows": metric_rows,
        "rank_changes": rank_changes,
        "summary": {
            "metrics": len(metric_rows),
            "policies": len(primary),
            "same_leader_metrics": sum(1 for row in rank_changes if row["same_leader_as_primary"]),
            "low_correlation_metrics": sum(1 for row in metric_rows if row["spearman_with_primary"] < 0.5),
            "max_rank_shift": max(row["max_rank_shift"] for row in rank_changes),
        },
        "interpretation": [
            "Average bounded task score remains the official metric because it normalizes heterogeneous startup situations to a common 0-100 scale.",
            "Task-normalized business score is reported as a sensitivity check because raw company score is not comparable across tasks with different starting states and horizons.",
            "Metrics such as cash, revenue, and low risk are diagnostic rather than primary because optimizing one alone can reward degenerate behavior.",
        ],
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("primary_metric") != "average_task_score":
        problems.append("Primary metric must remain average_task_score.")
    if payload["summary"]["policies"] < 4:
        problems.append("Expected at least four baseline policies.")
    if payload["summary"]["metrics"] < 6:
        problems.append("Expected at least six sensitivity metrics.")
    metrics = {row["metric"] for row in payload["metric_rows"]}
    required = {"average_task_score", "solve_rate", "task_normalized_business_score", "survival_rate", "revenue_efficiency"}
    if not required <= metrics:
        problems.append(f"Missing required sensitivity metrics: {sorted(required - metrics)}")
    primary = next(row for row in payload["metric_rows"] if row["metric"] == "average_task_score")
    if primary["spearman_with_primary"] != 1.0:
        problems.append("Primary metric must have rank correlation 1.0 with itself.")
    for row in payload["metric_rows"]:
        if not -1.0 <= row["spearman_with_primary"] <= 1.0:
            problems.append(f"{row['metric']} has invalid Spearman correlation.")
        if set(row["ranking"]) != set(payload["policies"]):
            problems.append(f"{row['metric']} ranking does not cover all policies.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    metric_rows = [
        [
            row["metric"],
            row["leader"],
            row["spearman_with_primary"],
            " > ".join(row["ranking"]),
        ]
        for row in payload["metric_rows"]
    ]
    value_rows = []
    for row in payload["metric_rows"]:
        values = row["values"]
        value_rows.append([row["metric"], *[values[policy] for policy in payload["policies"]]])
    rank_rows = [
        [row["metric"], row["same_leader_as_primary"], row["max_rank_shift"]]
        for row in payload["rank_changes"]
    ]
    lines = [
        "# FounderBench Metric Sensitivity",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Ranking Sensitivity",
        "",
        markdown_table(["Metric", "Leader", "Spearman vs Primary", "Ranking"], metric_rows),
        "",
        "## Metric Values",
        "",
        markdown_table(["Metric", *payload["policies"]], value_rows),
        "",
        "## Rank Changes",
        "",
        markdown_table(["Metric", "Same Leader as Primary", "Max Rank Shift"], rank_rows),
        "",
        "## Interpretation",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["interpretation"])
    lines.extend(["", "## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The report compares the official bounded task score with normalized business, solve-rate, survival, revenue, cash, and risk diagnostics.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    problems = validate_report(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate metric sensitivity report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
