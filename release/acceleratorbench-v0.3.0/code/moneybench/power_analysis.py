from __future__ import annotations

import argparse
import json
from math import sqrt
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from .analysis import markdown_table
from .paired_statistics import build_report as build_paired_report, scores_by_policy


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"
Z_TWO_SIDED_005 = 1.96
Z_POWER_080 = 0.84


def minimum_detectable_gap(sd: float, n: int) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    return round((Z_TWO_SIDED_005 + Z_POWER_080) * sd / sqrt(n), 2)


def _all_pairwise_diffs(score_map: dict[str, dict[str, float]]) -> list[float]:
    policies = sorted(score_map)
    diffs: list[float] = []
    for index, left in enumerate(policies):
        for right in policies[index + 1 :]:
            shared = sorted(set(score_map[left]) & set(score_map[right]))
            diffs.extend(score_map[left][task_id] - score_map[right][task_id] for task_id in shared)
    return diffs


def build_analysis(raw_path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> dict[str, Any]:
    paired = build_paired_report(raw_path)
    runs = json.loads(raw_path.read_text(encoding="utf-8"))
    score_map = scores_by_policy(runs)
    all_diffs = _all_pairwise_diffs(score_map)
    paired_gap_sd = pstdev(all_diffs)
    task_counts = [20, 30, 50, 75, 100]
    mde_rows = [
        {
            "task_episodes": count,
            "minimum_detectable_score_gap": minimum_detectable_gap(paired_gap_sd, count),
            "interpretation": "Approximate 80% power for a paired two-sided 0.05 test under the deterministic-baseline observed paired-gap variance.",
        }
        for count in task_counts
    ]
    observed_rows = [
        {
            "comparison": row["comparison"],
            "tasks": row["tasks"],
            "mean_score_gap": row["mean_score_gap"],
            "score_gap_bootstrap_ci": row["score_gap_bootstrap_ci"],
            "cohen_dz": row["cohen_dz"],
            "above_50_task_mde": abs(float(row["mean_score_gap"])) >= mde_rows[2]["minimum_detectable_score_gap"],
        }
        for row in paired["comparisons"]
    ]
    conservative_solve_mde = {
        "task_episodes": 50,
        "minimum_detectable_solve_rate_gap": round((Z_TWO_SIDED_005 + Z_POWER_080) * sqrt(0.25 / 50), 3),
        "assumption": "Conservative normal approximation with Bernoulli variance p(1-p)=0.25; paired binary tests may need less or more evidence depending on discordance.",
    }
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Power and resolution analysis for the fixed public task suite before hosted/local LLM results are added.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "method": {
            "paired_gap_variance_source": "All pairwise deterministic-baseline task-score gaps on the 50 public v0.3.0 tasks.",
            "alpha": 0.05,
            "target_power": 0.80,
            "approximation": "Normal paired-mean approximation: MDE = (1.96 + 0.84) * sd(paired gaps) / sqrt(n).",
            "paired_gap_sd": round(paired_gap_sd, 4),
        },
        "summary": {
            "public_tasks": 50,
            "policies_used_for_variance": len(score_map),
            "paired_gap_observations": len(all_diffs),
            "minimum_detectable_score_gap_50_tasks": mde_rows[2]["minimum_detectable_score_gap"],
            "observed_comparisons_above_50_task_mde": sum(1 for row in observed_rows if row["above_50_task_mde"]),
            "claim": "The public suite has coarse resolution for small model differences; repeated runs and private-holdout expansion should be reported for close hosted-model comparisons.",
        },
        "mde_by_task_count": mde_rows,
        "observed_deterministic_gaps": observed_rows,
        "solve_rate_resolution": conservative_solve_mde,
        "claim_guardrails": [
            "Do not interpret non-significant close hosted-model gaps as model equivalence without a pre-specified equivalence margin.",
            "Do not claim the 50-task public suite can reliably detect small score gaps near the MDE boundary.",
            "Use repeated-run bundles for stochastic policies and report run-level intervals separately from task-level paired intervals.",
            "Use the private-holdout protocol for final leaderboard credibility rather than increasing public-task tuning pressure.",
        ],
    }


def validate_analysis(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["public_tasks"] != 50:
        problems.append("Power analysis must be anchored to the 50-task public suite.")
    if payload["summary"]["minimum_detectable_score_gap_50_tasks"] <= 0:
        problems.append("Minimum detectable score gap must be positive.")
    if payload["summary"]["paired_gap_observations"] < 100:
        problems.append("Expected pairwise deterministic gap observations across multiple policies.")
    if len(payload["mde_by_task_count"]) < 5:
        problems.append("Expected MDE rows for multiple task-suite sizes.")
    if not any(row["task_episodes"] == 50 for row in payload["mde_by_task_count"]):
        problems.append("Expected an MDE row for 50 task episodes.")
    if len(payload["observed_deterministic_gaps"]) < 3:
        problems.append("Expected at least three observed deterministic comparisons.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["minimum_detectable_score_gap", "repeated-run", "private-holdout", "50-task"]:
        if required not in text:
            problems.append(f"Power analysis must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    method_rows = [[key, value] for key, value in payload["method"].items()]
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    mde_rows = [
        [row["task_episodes"], row["minimum_detectable_score_gap"], row["interpretation"]]
        for row in payload["mde_by_task_count"]
    ]
    observed_rows = [
        [
            row["comparison"],
            row["tasks"],
            row["mean_score_gap"],
            f"[{row['score_gap_bootstrap_ci'][0]}, {row['score_gap_bootstrap_ci'][1]}]",
            row["cohen_dz"],
            row["above_50_task_mde"],
        ]
        for row in payload["observed_deterministic_gaps"]
    ]
    solve = payload["solve_rate_resolution"]
    lines = [
        "# FounderBench v0.3 Power and Resolution Analysis",
        "",
        payload["purpose"],
        "",
        "## Method",
        "",
        markdown_table(["Item", "Value"], method_rows),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Minimum Detectable Score Gap",
        "",
        markdown_table(["Task Episodes", "Minimum Detectable Score Gap", "Interpretation"], mde_rows),
        "",
        "## Observed Deterministic Gaps",
        "",
        markdown_table(["Comparison", "Tasks", "Mean Gap", "Bootstrap 95% CI", "Cohen dz", "Above 50-Task MDE"], observed_rows),
        "",
        "## Solve-Rate Resolution",
        "",
        markdown_table(["Item", "Value"], [[key, value] for key, value in solve.items()]),
        "",
        "## Claim Guardrails",
        "",
        *[f"- {item}" for item in payload["claim_guardrails"]],
        "",
        "## Validation",
        "",
    ]
    problems = validate_analysis(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The analysis quantifies public-suite resolution and keeps close-model comparison limits explicit.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_analysis(json_output: Path, markdown_output: Path) -> None:
    payload = build_analysis()
    problems = validate_analysis(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench power/resolution analysis.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_analysis(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
