from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import markdown_table
from .difficulty_calibration import build_report as build_difficulty_report
from .task_coverage import build_coverage


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"
MIN_HIGH_DISCRIMINATION_SPREAD = 50.0


def _recommendation(row: dict[str, Any]) -> str:
    if row["difficulty_band"] == "saturated":
        return "Candidate for harder v0.4 variant; keep for public sanity checks."
    if row["difficulty_band"] == "unsolved_by_baselines":
        return "Needs hosted/local LLM, human/expert, or reference-solution calibration before claiming feasibility beyond deterministic baselines."
    if row["score_spread"] >= MIN_HIGH_DISCRIMINATION_SPREAD:
        return "Strong provider-comparison candidate because deterministic baselines separate clearly."
    if row["difficulty_band"] == "hard":
        return "Useful hard task; inspect LLM traces for whether failures are strategic or formatting related."
    return "Keep as calibration coverage for family/split balance."


def build_audit() -> dict[str, Any]:
    difficulty = build_difficulty_report()
    coverage = build_coverage()
    rows = []
    for row in difficulty["task_rows"]:
        feasibility = "baseline_solved" if row["solved_by"] > 0 else "needs_external_calibration"
        if row["difficulty_band"] == "saturated":
            feasibility = "saturated_by_deterministic_baselines"
        rows.append(
            {
                "task_id": row["task_id"],
                "family": row["family"],
                "split": row["split"],
                "difficulty_band": row["difficulty_band"],
                "feasibility_status": feasibility,
                "solved_by": row["solved_by"],
                "policies": row["policies"],
                "best_policy": row["best_policy"],
                "best_score": round(float(row["max_score"]), 2),
                "score_spread": round(float(row["score_spread"]), 2),
                "high_discrimination": float(row["score_spread"]) >= MIN_HIGH_DISCRIMINATION_SPREAD,
                "recommendation": _recommendation(row),
            }
        )
    family_rows = []
    for family in coverage["families"]:
        task_ids = set(family["task_ids"])
        family_task_rows = [row for row in rows if row["task_id"] in task_ids]
        family_rows.append(
            {
                "family": family["family"],
                "tasks": len(family_task_rows),
                "baseline_solved_tasks": sum(1 for row in family_task_rows if row["solved_by"] > 0),
                "needs_external_calibration": sum(1 for row in family_task_rows if row["feasibility_status"] == "needs_external_calibration"),
                "high_discrimination": sum(1 for row in family_task_rows if row["high_discrimination"]),
                "expected_actions": family["expected_actions"],
            }
        )
    status_counts = Counter(row["feasibility_status"] for row in rows)
    band_counts = Counter(row["difficulty_band"] for row in rows)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Task-level feasibility and discrimination audit for paper review. It summarizes which public tasks are solved by at least one deterministic baseline, which remain unsolved by deterministic baselines, and which tasks are likely to differentiate future hosted/local LLM providers.",
        "calibration_scope": "deterministic_rule_baselines_only",
        "claim_guardrail": "Tasks unsolved by deterministic baselines are not impossible claims; they require hosted/local LLM, human/expert, or reference-solution calibration before stronger feasibility claims.",
        "summary": {
            "tasks": len(rows),
            "families": len(family_rows),
            "baseline_solved_tasks": sum(1 for row in rows if row["solved_by"] > 0),
            "needs_external_calibration": status_counts.get("needs_external_calibration", 0),
            "saturated_by_deterministic_baselines": status_counts.get("saturated_by_deterministic_baselines", 0),
            "high_discrimination_tasks": sum(1 for row in rows if row["high_discrimination"]),
            "mean_score_spread": round(mean(row["score_spread"] for row in rows), 2),
            "difficulty_bands": dict(sorted(band_counts.items())),
        },
        "family_summary": family_rows,
        "task_rows": rows,
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["tasks"] != 50:
        problems.append(f"Expected 50 tasks, found {payload['summary']['tasks']}.")
    if payload["summary"]["families"] != 10:
        problems.append("Expected 10 task families.")
    if payload["summary"]["baseline_solved_tasks"] <= 0:
        problems.append("At least one task should be solved by deterministic baselines.")
    if payload["summary"]["needs_external_calibration"] <= 0:
        problems.append("Audit should retain tasks needing external calibration rather than claiming all tasks are calibrated.")
    if payload["summary"]["saturated_by_deterministic_baselines"] >= payload["summary"]["tasks"]:
        problems.append("All tasks are saturated by deterministic baselines.")
    if payload["summary"]["high_discrimination_tasks"] <= 0:
        problems.append("Expected at least one high-discrimination task.")
    for row in payload["task_rows"]:
        if not 0 <= row["best_score"] <= 100:
            problems.append(f"{row['task_id']} best_score out of range.")
        if row["feasibility_status"] == "needs_external_calibration" and row["solved_by"] != 0:
            problems.append(f"{row['task_id']} external calibration status conflicts with solved_by.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items() if key != "difficulty_bands"]
    band_rows = [[key, value] for key, value in payload["summary"]["difficulty_bands"].items()]
    family_rows = [
        [
            row["family"],
            row["tasks"],
            row["baseline_solved_tasks"],
            row["needs_external_calibration"],
            row["high_discrimination"],
            ", ".join(row["expected_actions"]),
        ]
        for row in payload["family_summary"]
    ]
    task_rows = [
        [
            row["task_id"],
            row["family"],
            row["split"],
            row["difficulty_band"],
            row["feasibility_status"],
            f"{row['solved_by']}/{row['policies']}",
            row["best_policy"],
            row["best_score"],
            row["score_spread"],
        ]
        for row in payload["task_rows"]
    ]
    external_rows = [
        [
            row["task_id"],
            row["family"],
            row["split"],
            row["best_policy"],
            row["best_score"],
            row["score_spread"],
            row["recommendation"],
        ]
        for row in payload["task_rows"]
        if row["feasibility_status"] == "needs_external_calibration"
    ]
    high_disc_rows = [
        [
            row["task_id"],
            row["family"],
            row["difficulty_band"],
            row["best_policy"],
            row["best_score"],
            row["score_spread"],
        ]
        for row in sorted(payload["task_rows"], key=lambda item: item["score_spread"], reverse=True)
        if row["high_discrimination"]
    ][:20]
    lines = [
        "# FounderBench Task Feasibility and Discrimination Audit",
        "",
        payload["purpose"],
        "",
        f"Calibration scope: `{payload['calibration_scope']}`",
        "",
        "Claim guardrail:",
        "",
        payload["claim_guardrail"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Difficulty Bands",
        "",
        markdown_table(["Band", "Tasks"], band_rows),
        "",
        "## Family Feasibility",
        "",
        markdown_table(["Family", "Tasks", "Baseline Solved", "Needs External Calibration", "High Discrimination", "Expected Actions"], family_rows),
        "",
        "## Tasks Needing External Calibration",
        "",
    ]
    if external_rows:
        lines.append(markdown_table(["Task", "Family", "Split", "Best Policy", "Best Score", "Spread", "Recommendation"], external_rows))
    else:
        lines.append("No tasks currently require external calibration under this audit.")
    lines.extend(
        [
            "",
            "## High-Discrimination Tasks",
            "",
            markdown_table(["Task", "Family", "Band", "Best Policy", "Best Score", "Spread"], high_disc_rows),
            "",
            "## Full Task Ledger",
            "",
            markdown_table(["Task", "Family", "Split", "Band", "Feasibility", "Solved By", "Best Policy", "Best Score", "Spread"], task_rows),
            "",
            "## Validation",
            "",
        ]
    )
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The feasibility audit covers all 50 tasks, preserves external-calibration needs, and identifies high-discrimination tasks for future model comparisons.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_audit(json_output: Path, markdown_output: Path) -> None:
    payload = build_audit()
    problems = validate_audit(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench task feasibility audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
