from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import family_name, markdown_table, split_name, task_number


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def load_runs(path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def difficulty_band(solved_by: int, policies: int) -> str:
    if solved_by == 0:
        return "unsolved_by_baselines"
    if solved_by == policies:
        return "saturated"
    if solved_by == 1:
        return "hard"
    if solved_by == policies - 1:
        return "easy"
    return "medium"


def build_report(raw_path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> dict[str, Any]:
    runs = load_runs(raw_path)
    policy_order = [run["policy"] for run in sorted(runs, key=lambda item: item["average_task_score"], reverse=True)]
    by_task: dict[str, list[tuple[str, dict[str, Any]]]] = defaultdict(list)
    for run in runs:
        for result in run["results"]:
            by_task[result["task_id"]].append((run["policy"], result))

    task_rows = []
    for task_id in sorted(by_task, key=task_number):
        entries = by_task[task_id]
        scores_by_policy = {policy: float(result["score"]["score"]) for policy, result in entries}
        passed_by_policy = {policy: bool(result["score"]["passed"]) for policy, result in entries}
        scores = list(scores_by_policy.values())
        solved_by = sum(1 for passed in passed_by_policy.values() if passed)
        task_rows.append(
            {
                "task_id": task_id,
                "family": family_name(task_id),
                "split": split_name(task_id),
                "mean_score": round(mean(scores), 2),
                "min_score": round(min(scores), 2),
                "max_score": round(max(scores), 2),
                "score_spread": round(max(scores) - min(scores), 2),
                "solved_by": solved_by,
                "policies": len(entries),
                "difficulty_band": difficulty_band(solved_by, len(entries)),
                "best_policy": max(scores_by_policy, key=scores_by_policy.get),
                "worst_policy": min(scores_by_policy, key=scores_by_policy.get),
                "passed_by_policy": passed_by_policy,
                "scores_by_policy": scores_by_policy,
            }
        )

    band_counts: dict[str, int] = defaultdict(int)
    split_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    family_rows: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in task_rows:
        band_counts[row["difficulty_band"]] += 1
        split_rows[row["split"]].append(row)
        family_rows[row["family"]].append(row)

    family_summary = []
    for family, rows in sorted(family_rows.items(), key=lambda pair: task_number(pair[1][0]["task_id"])):
        family_summary.append(
            {
                "family": family,
                "tasks": len(rows),
                "mean_score": round(mean(row["mean_score"] for row in rows), 2),
                "mean_solved_by": round(mean(row["solved_by"] for row in rows), 2),
                "hard_or_unsolved": sum(1 for row in rows if row["difficulty_band"] in {"hard", "unsolved_by_baselines"}),
                "saturated": sum(1 for row in rows if row["difficulty_band"] == "saturated"),
            }
        )

    split_summary = []
    for split, rows in sorted(split_rows.items()):
        split_summary.append(
            {
                "split": split,
                "tasks": len(rows),
                "mean_score": round(mean(row["mean_score"] for row in rows), 2),
                "mean_solved_by": round(mean(row["solved_by"] for row in rows), 2),
                "hard_or_unsolved": sum(1 for row in rows if row["difficulty_band"] in {"hard", "unsolved_by_baselines"}),
                "saturated": sum(1 for row in rows if row["difficulty_band"] == "saturated"),
            }
        )

    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Difficulty calibration over included deterministic baselines. This is not a hosted-LLM result; it checks whether the public suite has useful spread before provider runs.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "policies": policy_order,
        "summary": {
            "tasks": len(task_rows),
            "policies": len(policy_order),
            "mean_task_score": round(mean(row["mean_score"] for row in task_rows), 2),
            "mean_solved_by": round(mean(row["solved_by"] for row in task_rows), 2),
            "mean_score_spread": round(mean(row["score_spread"] for row in task_rows), 2),
            "band_counts": dict(sorted(band_counts.items())),
            "tasks_not_solved_by_task_heuristic": sum(1 for row in task_rows if not row["passed_by_policy"].get("task_heuristic", False)),
            "saturated_tasks": band_counts.get("saturated", 0),
        },
        "family_summary": family_summary,
        "split_summary": split_summary,
        "task_rows": task_rows,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["tasks"] != 50:
        problems.append(f"Expected 50 tasks, found {payload['summary']['tasks']}.")
    if payload["summary"]["policies"] < 4:
        problems.append("Difficulty calibration expects at least four deterministic baselines.")
    if payload["summary"]["tasks_not_solved_by_task_heuristic"] <= 0:
        problems.append("Task-aware heuristic solves every task; suite lacks unresolved calibration targets.")
    if payload["summary"]["saturated_tasks"] >= payload["summary"]["tasks"]:
        problems.append("Every task is saturated by baselines; suite is too easy for calibration.")
    if len(payload["family_summary"]) != 10:
        problems.append("Expected 10 family summaries.")
    if {row["split"] for row in payload["split_summary"]} != {"public_dev", "public_test"}:
        problems.append("Expected public_dev and public_test split summaries.")
    for row in payload["task_rows"]:
        if row["score_spread"] < 0:
            problems.append(f"Task {row['task_id']} has negative score spread.")
        if row["difficulty_band"] not in {"unsolved_by_baselines", "hard", "medium", "easy", "saturated"}:
            problems.append(f"Task {row['task_id']} has unknown difficulty band {row['difficulty_band']}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary = payload["summary"]
    family_rows = [
        [row["family"], row["tasks"], row["mean_score"], row["mean_solved_by"], row["hard_or_unsolved"], row["saturated"]]
        for row in payload["family_summary"]
    ]
    split_rows = [
        [row["split"], row["tasks"], row["mean_score"], row["mean_solved_by"], row["hard_or_unsolved"], row["saturated"]]
        for row in payload["split_summary"]
    ]
    hardest_rows = [
        [
            row["task_id"],
            row["family"],
            row["split"],
            row["difficulty_band"],
            row["mean_score"],
            f"{row['solved_by']}/{row['policies']}",
            row["score_spread"],
            row["best_policy"],
        ]
        for row in sorted(payload["task_rows"], key=lambda item: (item["solved_by"], item["mean_score"]))[:15]
    ]
    spread_rows = [
        [
            row["task_id"],
            row["family"],
            row["difficulty_band"],
            row["min_score"],
            row["max_score"],
            row["score_spread"],
            row["best_policy"],
            row["worst_policy"],
        ]
        for row in sorted(payload["task_rows"], key=lambda item: item["score_spread"], reverse=True)[:15]
    ]
    band_rows = [[band, count] for band, count in summary["band_counts"].items()]
    lines = [
        "# FounderBench v0.3 Difficulty Calibration",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(
            ["Metric", "Value"],
            [
                ["tasks", summary["tasks"]],
                ["policies", summary["policies"]],
                ["mean_task_score", summary["mean_task_score"]],
                ["mean_solved_by", summary["mean_solved_by"]],
                ["mean_score_spread", summary["mean_score_spread"]],
                ["tasks_not_solved_by_task_heuristic", summary["tasks_not_solved_by_task_heuristic"]],
                ["saturated_tasks", summary["saturated_tasks"]],
            ],
        ),
        "",
        "## Difficulty Bands",
        "",
        markdown_table(["Band", "Tasks"], band_rows),
        "",
        "Bands are based on how many included deterministic baselines solve each task: 0 = unsolved, 1 = hard, middle counts = medium, all-but-one = easy, all = saturated.",
        "",
        "## Family Calibration",
        "",
        markdown_table(["Family", "Tasks", "Mean Score", "Mean Solved By", "Hard/Unsolved", "Saturated"], family_rows),
        "",
        "## Split Calibration",
        "",
        markdown_table(["Split", "Tasks", "Mean Score", "Mean Solved By", "Hard/Unsolved", "Saturated"], split_rows),
        "",
        "## Hardest Public Tasks",
        "",
        markdown_table(["Task", "Family", "Split", "Band", "Mean Score", "Solved By", "Score Spread", "Best Policy"], hardest_rows),
        "",
        "## Highest-Discrimination Tasks",
        "",
        "High score spread means baselines separate clearly on the task. These are useful for qualitative error analysis and provider comparisons.",
        "",
        markdown_table(["Task", "Family", "Band", "Min", "Max", "Spread", "Best", "Worst"], spread_rows),
        "",
        "## Interpretation",
        "",
        "- A useful public benchmark should not be all saturated and should retain tasks that the strongest deterministic policy fails.",
        "- This report calibrates deterministic baselines only; hosted LLM runs should be added before making model-comparison claims.",
        "- Families with many saturated tasks are candidates for harder v0.4 variants; families with many unsolved tasks are candidates for intermediate scaffolding.",
        "",
    ]
    problems = validate_report(payload)
    lines.extend(["## Validation", ""])
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The calibration payload covers all 50 public tasks, all included deterministic baselines, both public splits, and all 10 task families.")
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
    parser = argparse.ArgumentParser(description="Generate deterministic-baseline difficulty calibration report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
