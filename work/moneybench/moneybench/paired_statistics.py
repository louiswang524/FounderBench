from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from statistics import mean, pstdev
from typing import Any

from .analysis import bootstrap_mean_ci, markdown_table, task_number


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"
PERMUTATION_SAMPLES = 20000
PERMUTATION_SEED = 20260715


def load_runs(path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def scores_by_policy(runs: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    return {
        run["policy"]: {
            result["task_id"]: float(result["score"]["score"])
            for result in run["results"]
        }
        for run in runs
    }


def solves_by_policy(runs: list[dict[str, Any]]) -> dict[str, dict[str, bool]]:
    return {
        run["policy"]: {
            result["task_id"]: bool(result["score"]["passed"])
            for result in run["results"]
        }
        for run in runs
    }


def permutation_p_value(diffs: list[float], *, samples: int = PERMUTATION_SAMPLES, seed: int = PERMUTATION_SEED) -> float:
    observed = abs(mean(diffs))
    if observed == 0:
        return 1.0
    rng = random.Random(seed)
    extreme = 0
    for _ in range(samples):
        flipped = [diff if rng.random() < 0.5 else -diff for diff in diffs]
        if abs(mean(flipped)) >= observed:
            extreme += 1
    return round((extreme + 1) / (samples + 1), 6)


def holm_bonferroni(p_values: list[float]) -> list[float]:
    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    adjusted = [0.0] * len(p_values)
    running = 0.0
    comparisons = len(p_values)
    for rank, (index, p_value) in enumerate(indexed):
        candidate = min(1.0, (comparisons - rank) * p_value)
        running = max(running, candidate)
        adjusted[index] = round(running, 6)
    return adjusted


def cohen_dz(diffs: list[float]) -> float:
    sd = pstdev(diffs)
    if sd == 0:
        return 0.0
    return round(mean(diffs) / sd, 4)


def comparison_rows(runs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    score_map = scores_by_policy(runs)
    solve_map = solves_by_policy(runs)
    ordered = sorted(runs, key=lambda run: run["average_task_score"], reverse=True)
    top_policy = ordered[0]["policy"]
    rows = []
    for run in ordered[1:]:
        policy = run["policy"]
        tasks = sorted(set(score_map[top_policy]) & set(score_map[policy]), key=task_number)
        diffs = [score_map[top_policy][task_id] - score_map[policy][task_id] for task_id in tasks]
        solve_diffs = [
            (1 if solve_map[top_policy][task_id] else 0) - (1 if solve_map[policy][task_id] else 0)
            for task_id in tasks
        ]
        ci_low, ci_high = bootstrap_mean_ci(diffs, seed=PERMUTATION_SEED + len(policy))
        rows.append(
            {
                "comparison": f"{top_policy} - {policy}",
                "top_policy": top_policy,
                "baseline_policy": policy,
                "tasks": len(tasks),
                "mean_score_gap": round(mean(diffs), 2),
                "score_gap_bootstrap_ci": [round(ci_low, 2), round(ci_high, 2)],
                "paired_permutation_p": permutation_p_value(diffs, seed=PERMUTATION_SEED + len(policy) * 17),
                "cohen_dz": cohen_dz(diffs),
                "task_wins": sum(1 for diff in diffs if diff > 0),
                "task_losses": sum(1 for diff in diffs if diff < 0),
                "task_ties": sum(1 for diff in diffs if diff == 0),
                "solve_gap": round(mean(solve_diffs), 4),
                "solve_wins": sum(1 for diff in solve_diffs if diff > 0),
                "solve_losses": sum(1 for diff in solve_diffs if diff < 0),
            }
        )
    return rows


def build_report(raw_path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> dict[str, Any]:
    runs = load_runs(raw_path)
    rows = comparison_rows(runs)
    adjusted_p_values = holm_bonferroni([row["paired_permutation_p"] for row in rows])
    for row, adjusted_p_value in zip(rows, adjusted_p_values):
        row["holm_adjusted_p"] = adjusted_p_value
        row["significant_after_holm_0_05"] = adjusted_p_value < 0.05
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Paired statistical comparison of deterministic baselines over matched task episodes.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "method": {
            "paired_unit": "task episode",
            "score_gap": "top_policy_score_i - baseline_policy_score_i on the same task id",
            "bootstrap_ci": "nonparametric bootstrap over paired task gaps",
            "permutation_test": "two-sided random sign-flip test over paired task gaps",
            "permutation_samples": PERMUTATION_SAMPLES,
            "multiple_comparison_adjustment": "Holm-Bonferroni over reported paired permutation p-values for the primary endpoint.",
            "effect_size": "Cohen dz = mean paired gap / population standard deviation of paired gaps",
        },
        "summary": {
            "comparisons": len(rows),
            "significant_at_0_05": sum(1 for row in rows if row["paired_permutation_p"] < 0.05),
            "significant_after_holm_0_05": sum(1 for row in rows if row["significant_after_holm_0_05"]),
            "all_score_gap_cis_positive": all(row["score_gap_bootstrap_ci"][0] > 0 for row in rows),
            "max_p_value": max((row["paired_permutation_p"] for row in rows), default=math.nan),
            "max_holm_adjusted_p": max((row["holm_adjusted_p"] for row in rows), default=math.nan),
        },
        "comparisons": rows,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["comparisons"] < 3:
        problems.append("Expected at least three pairwise comparisons.")
    for row in payload["comparisons"]:
        if row["tasks"] != 50:
            problems.append(f"{row['comparison']} compares {row['tasks']} tasks, expected 50.")
        if not 0 <= row["paired_permutation_p"] <= 1:
            problems.append(f"{row['comparison']} has invalid p-value.")
        if not 0 <= row["holm_adjusted_p"] <= 1:
            problems.append(f"{row['comparison']} has invalid Holm-adjusted p-value.")
        if row["holm_adjusted_p"] < row["paired_permutation_p"]:
            problems.append(f"{row['comparison']} has adjusted p-value below raw p-value.")
        if row["significant_after_holm_0_05"] != (row["holm_adjusted_p"] < 0.05):
            problems.append(f"{row['comparison']} has inconsistent Holm significance flag.")
        if row["task_wins"] + row["task_losses"] + row["task_ties"] != row["tasks"]:
            problems.append(f"{row['comparison']} win/loss/tie counts do not sum to task count.")
        low, high = row["score_gap_bootstrap_ci"]
        if low > high:
            problems.append(f"{row['comparison']} CI lower bound exceeds upper bound.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["comparison"],
            row["tasks"],
            row["mean_score_gap"],
            f"[{row['score_gap_bootstrap_ci'][0]}, {row['score_gap_bootstrap_ci'][1]}]",
            row["paired_permutation_p"],
            row["holm_adjusted_p"],
            row["significant_after_holm_0_05"],
            row["cohen_dz"],
            f"{row['task_wins']}/{row['task_losses']}/{row['task_ties']}",
            row["solve_gap"],
            f"{row['solve_wins']}/{row['solve_losses']}",
        ]
        for row in payload["comparisons"]
    ]
    method = payload["method"]
    lines = [
        "# FounderBench v0.3 Paired Statistics",
        "",
        payload["purpose"],
        "",
        "## Method",
        "",
        markdown_table(["Item", "Value"], [[key, value] for key, value in method.items()]),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Pairwise Comparisons",
        "",
        markdown_table(
            [
                "Comparison",
                "Tasks",
                "Mean Gap",
                "Bootstrap 95% CI",
                "Raw permutation p",
                "Holm adjusted p",
                "Holm sig.",
                "Cohen dz",
                "Score W/L/T",
                "Solve Gap",
                "Solve W/L",
            ],
            rows,
        ),
        "",
        "## Interpretation",
        "",
        "- The paired unit is the fixed task episode, so each comparison controls for task identity.",
        "- Permutation p-values test whether the observed signed task gaps are larger than expected under random sign flips.",
        "- Raw and Holm-Bonferroni adjusted p-values are both reported; adjusted p-values govern family-level leaderboard claims.",
        "- Effect sizes are descriptive calibration evidence for deterministic baselines; hosted LLM comparisons should report the same rows once runs are available.",
        "",
        "## Validation",
        "",
    ]
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All comparisons cover the full 50-task public suite and have internally consistent paired statistics.")
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
    parser = argparse.ArgumentParser(description="Generate paired statistical comparison report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
