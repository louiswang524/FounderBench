from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .action_ablation import build_report as build_action_ablation_report
from .analysis import markdown_table
from .difficulty_calibration import build_report as build_difficulty_report
from .metric_sensitivity import build_report as build_metric_sensitivity_report
from .paper_tables import build_tables


VERSION = "0.3.0"


def _float(value: Any) -> float:
    return round(float(value), 4)


def build_figure_data() -> dict[str, Any]:
    tables = build_tables()
    action_ablation = build_action_ablation_report()
    difficulty = build_difficulty_report()
    metric_sensitivity = build_metric_sensitivity_report()

    leaderboard = [
        {
            "policy": row[0],
            "tasks": int(row[1]),
            "solved": int(row[2]),
            "solve_rate": _float(row[3]),
            "average_task_score": _float(row[4]),
            "public_dev_score": _float(row[5]),
            "public_test_score": _float(row[6]),
            "over_budget_decisions": int(row[7]),
            "provider_errors": int(row[8]),
        }
        for row in tables["all_valid_policy_rows"]
    ]

    family_heatmap = []
    policies = [row[0] for row in tables["all_valid_policy_rows"]]
    for row in tables["family_rows"]:
        family = row[0]
        for policy, cell in zip(policies, row[1:]):
            solved_part, score_part = str(cell).split(" ", 1)
            family_heatmap.append(
                {
                    "family": family,
                    "policy": policy,
                    "solved": int(solved_part.split("/")[0]),
                    "tasks": int(solved_part.split("/")[1]),
                    "average_score": _float(score_part.strip("()")),
                }
            )

    ablation_drops = [
        {
            "ablation_id": row["ablation_id"],
            "blocked_actions": row["blocked_actions"],
            "mean_score_drop": row["mean_score_drop"],
            "drop_ci_low": row["drop_95_ci"][0],
            "drop_ci_high": row["drop_95_ci"][1],
            "solved_drop": row["solved_drop"],
        }
        for row in action_ablation["rows"]
        if row["ablation_id"] != "full_task_heuristic"
    ]

    difficulty_bands = [
        {
            "band": band,
            "task_count": count,
        }
        for band, count in sorted(difficulty["summary"]["band_counts"].items())
    ]

    metric_rankings = [
        {
            "metric": row["metric"],
            "leader": row["leader"],
            "spearman_with_primary": row["spearman_with_primary"],
            "ranking": row["ranking"],
        }
        for row in metric_sensitivity["metric_rows"]
    ]

    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Paper figure data generated from validated v0.3 result artifacts.",
        "source_artifacts": [
            "outputs/acceleratorbench-paper-tables-v0.3.json",
            "outputs/acceleratorbench-action-ablation-v0.3.json",
            "outputs/acceleratorbench-difficulty-calibration-v0.3.json",
            "outputs/acceleratorbench-metric-sensitivity-v0.3.json",
        ],
        "figures": [
            {
                "id": "leaderboard_bar",
                "caption": "Average task score and solved tasks for deterministic baselines and validated provider submissions.",
                "recommended_encoding": "bar chart with policies on x-axis and average_task_score on y-axis; solved tasks as labels.",
                "data": leaderboard,
            },
            {
                "id": "family_heatmap",
                "caption": "Family-level solved count and average score by policy.",
                "recommended_encoding": "heatmap with task family by policy, colored by average_score and annotated with solved/tasks.",
                "data": family_heatmap,
            },
            {
                "id": "action_ablation_drop",
                "caption": "Mean score drop when disabling major action groups in the task-aware heuristic.",
                "recommended_encoding": "horizontal bar chart with confidence intervals.",
                "data": ablation_drops,
            },
            {
                "id": "difficulty_band_counts",
                "caption": "Number of public tasks by deterministic-baseline difficulty band.",
                "recommended_encoding": "ordered bar chart.",
                "data": difficulty_bands,
            },
            {
                "id": "metric_sensitivity_rankings",
                "caption": "Metric sensitivity rankings compared with the official average task score.",
                "recommended_encoding": "table or slope chart showing ranking changes across metrics.",
                "data": metric_rankings,
            },
        ],
        "summary": {
            "figures": 5,
            "leaderboard_policies": len(leaderboard),
            "family_heatmap_cells": len(family_heatmap),
            "action_ablation_rows": len(ablation_drops),
            "difficulty_bands": len(difficulty_bands),
            "metric_rankings": len(metric_rankings),
        },
    }


def validate_figure_data(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    figures = payload.get("figures", [])
    if len(figures) < 5:
        problems.append("Expected at least five paper figure datasets.")
    ids = {figure.get("id") for figure in figures}
    required = {"leaderboard_bar", "family_heatmap", "action_ablation_drop", "difficulty_band_counts", "metric_sensitivity_rankings"}
    if not required <= ids:
        problems.append(f"Missing figure datasets: {sorted(required - ids)}")
    for figure in figures:
        if not figure.get("data"):
            problems.append(f"Figure {figure.get('id')} has no data.")
        if not figure.get("caption"):
            problems.append(f"Figure {figure.get('id')} missing caption.")
    if payload.get("summary", {}).get("leaderboard_policies", 0) < 4:
        problems.append("Expected at least four leaderboard policies.")
    if payload.get("summary", {}).get("family_heatmap_cells", 0) < 40:
        problems.append("Expected family heatmap cells for all deterministic policies and families.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    figure_rows = [
        [
            figure["id"],
            len(figure["data"]),
            figure["caption"],
            figure["recommended_encoding"],
        ]
        for figure in payload["figures"]
    ]
    lines = [
        "# FounderBench v0.3 Paper Figure Data",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Figure Data Sets",
        "",
        markdown_table(["Figure ID", "Rows", "Caption", "Recommended Encoding"], figure_rows),
        "",
        "## Source Artifacts",
        "",
    ]
    lines.extend(f"- `{path}`" for path in payload["source_artifacts"])
    lines.extend(["", "## Validation", ""])
    problems = validate_figure_data(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All figure datasets are present and trace to generated v0.3 artifacts.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_figure_data(json_output: Path, markdown_output: Path) -> None:
    payload = build_figure_data()
    problems = validate_figure_data(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper figure data artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_figure_data(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
