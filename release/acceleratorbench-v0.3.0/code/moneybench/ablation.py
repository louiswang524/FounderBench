from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import FAMILIES, bootstrap_mean_ci, family_name, markdown_table, task_number


ABLATION_LADDER = [
    ("random", "No strategic prior; samples legal business actions stochastically."),
    ("conservative", "Adds runway preservation and cautious offer/support behavior."),
    ("heuristic", "Adds generic market scoring, pricing correction, acquisition, quality, and support rules."),
    ("task_heuristic", "Adds task-family conditioning, analogous to an agent correctly inferring the operating mode."),
]


def load_results(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _by_policy(runs: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {run["policy"]: run for run in runs}


def _task_scores(run: dict[str, Any]) -> dict[str, float]:
    return {result["task_id"]: float(result["score"]["score"]) for result in run["results"]}


def _solve_count(run: dict[str, Any]) -> int:
    return sum(1 for result in run["results"] if result["score"]["passed"])


def ablation_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    by_policy = _by_policy(runs)
    rows: list[list[Any]] = []
    previous_policy: str | None = None
    for policy, added_capability in ABLATION_LADDER:
        if policy not in by_policy:
            rows.append([policy, added_capability, "missing", "missing", "missing", "missing", "missing"])
            previous_policy = policy
            continue
        run = by_policy[policy]
        score = float(run["average_task_score"])
        solved = _solve_count(run)
        if previous_policy and previous_policy in by_policy:
            prev = by_policy[previous_policy]
            shared = sorted(set(_task_scores(run)) & set(_task_scores(prev)), key=task_number)
            diffs = [_task_scores(run)[task_id] - _task_scores(prev)[task_id] for task_id in shared]
            low, high = bootstrap_mean_ci(diffs, seed=20260715 + len(policy))
            delta = f"{mean(diffs):+.2f}"
            delta_ci = f"[{low:+.2f}, {high:+.2f}]"
            solved_delta = f"{solved - _solve_count(prev):+d}"
        else:
            delta = "n/a"
            delta_ci = "n/a"
            solved_delta = "n/a"
        rows.append([policy, added_capability, f"{score:.2f}", solved, delta, delta_ci, solved_delta])
        previous_policy = policy
    return rows


def family_gain_rows(runs: list[dict[str, Any]], baseline: str = "heuristic", target: str = "task_heuristic") -> list[list[Any]]:
    by_policy = _by_policy(runs)
    if baseline not in by_policy or target not in by_policy:
        return [[baseline, target, "missing policies", "", ""]]
    base_scores = _task_scores(by_policy[baseline])
    target_scores = _task_scores(by_policy[target])
    rows = []
    for _, family in FAMILIES:
        task_ids = sorted([task_id for task_id in target_scores if family_name(task_id) == family], key=task_number)
        diffs = [target_scores[task_id] - base_scores[task_id] for task_id in task_ids]
        base_solved = sum(
            1
            for result in by_policy[baseline]["results"]
            if family_name(result["task_id"]) == family and result["score"]["passed"]
        )
        target_solved = sum(
            1
            for result in by_policy[target]["results"]
            if family_name(result["task_id"]) == family and result["score"]["passed"]
        )
        rows.append([family, f"{mean(diffs):+.2f}", f"{base_solved}/5", f"{target_solved}/5", f"{target_solved - base_solved:+d}"])
    return sorted(rows, key=lambda row: float(row[1]), reverse=True)


def write_report(runs: list[dict[str, Any]], output: Path) -> None:
    lines = [
        "# FounderBench v0.3 Ablation Report",
        "",
        "This report treats the four deterministic non-LLM baselines as a capability ladder. It does not replace hosted LLM ablations, but it provides a reproducible calibration showing which kinds of decision information make the synthetic startup tasks easier.",
        "",
        "## Capability Ladder",
        "",
        markdown_table(
            ["Policy", "Added Capability", "Avg Score", "Solved", "Score Delta", "Delta 95% CI", "Solved Delta"],
            ablation_rows(runs),
        ),
        "",
        "## Task-Conditioning Gain by Family",
        "",
        "This table compares `task_heuristic` against the generic `heuristic` policy. Large gains mean the family rewards correctly identifying the startup operating situation rather than only applying generic growth rules.",
        "",
        markdown_table(["Family", "Avg Score Gain", "Heuristic Solved", "Task-Heuristic Solved", "Solved Gain"], family_gain_rows(runs)),
        "",
        "## Interpretation",
        "",
        "- The ladder separates blind action selection, cash-preserving operations, generic startup operating logic, and explicit task-family conditioning.",
        "- If future LLM baselines only beat `random` or `conservative`, the benchmark is mostly testing basic action validity and runway awareness.",
        "- If future LLM baselines beat `heuristic`, the evidence is stronger that they infer operating context and choose family-appropriate actions.",
        "- If future LLM baselines beat `task_heuristic`, the benchmark provides evidence beyond the current hand-coded task-family prior.",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench ablation report.")
    parser.add_argument("--raw", required=True, help="Raw benchmark result JSON.")
    parser.add_argument("--output", required=True, help="Markdown output path.")
    args = parser.parse_args()
    write_report(load_results(Path(args.raw)), Path(args.output))
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
