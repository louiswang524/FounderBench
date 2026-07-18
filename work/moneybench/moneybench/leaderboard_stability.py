from __future__ import annotations

import argparse
import json
import random
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import FAMILIES, family_name, markdown_table, split_name, task_number
from .metric_sensitivity import rank_desc, spearman_rank_correlation


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"
BOOTSTRAP_ITERATIONS = 1000
BOOTSTRAP_SEED = 20260716


def load_runs(path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def task_scores_by_policy(runs: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    return {
        run["policy"]: {result["task_id"]: float(result["score"]["score"]) for result in run["results"]}
        for run in runs
    }


def aggregate_scores(score_map: dict[str, dict[str, float]], task_ids: list[str]) -> dict[str, float]:
    return {
        policy: round(mean(scores[task_id] for task_id in task_ids), 2)
        for policy, scores in score_map.items()
    }


def build_audit(raw_path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> dict[str, Any]:
    runs = load_runs(raw_path)
    score_map = task_scores_by_policy(runs)
    all_tasks = sorted(next(iter(score_map.values())).keys(), key=task_number)
    primary_scores = aggregate_scores(score_map, all_tasks)
    primary_ranking = rank_desc(primary_scores)
    primary_leader = primary_ranking[0]

    split_rows = []
    for split in ["public_dev", "public_test"]:
        task_ids = [task_id for task_id in all_tasks if split_name(task_id) == split]
        scores = aggregate_scores(score_map, task_ids)
        ranking = rank_desc(scores)
        split_rows.append(
            {
                "split": split,
                "tasks": len(task_ids),
                "leader": ranking[0],
                "ranking": ranking,
                "scores": scores,
                "spearman_with_full": spearman_rank_correlation(primary_scores, scores),
                "same_leader_as_full": ranking[0] == primary_leader,
            }
        )

    family_rows = []
    for _, family in FAMILIES:
        task_ids = [task_id for task_id in all_tasks if family_name(task_id) != family]
        scores = aggregate_scores(score_map, task_ids)
        ranking = rank_desc(scores)
        family_rows.append(
            {
                "held_out_family": family,
                "tasks_used": len(task_ids),
                "leader": ranking[0],
                "ranking": ranking,
                "scores": scores,
                "spearman_with_full": spearman_rank_correlation(primary_scores, scores),
                "same_leader_as_full": ranking[0] == primary_leader,
            }
        )

    rng = random.Random(BOOTSTRAP_SEED)
    leader_counts: Counter[str] = Counter()
    rank_sum: dict[str, int] = {policy: 0 for policy in primary_ranking}
    for _ in range(BOOTSTRAP_ITERATIONS):
        sampled_tasks = [all_tasks[rng.randrange(len(all_tasks))] for _ in all_tasks]
        scores = aggregate_scores(score_map, sampled_tasks)
        ranking = rank_desc(scores)
        leader_counts[ranking[0]] += 1
        for rank, policy in enumerate(ranking, start=1):
            rank_sum[policy] += rank
    bootstrap_rows = [
        {
            "policy": policy,
            "full_rank": primary_ranking.index(policy) + 1,
            "full_score": primary_scores[policy],
            "leader_probability": round(leader_counts[policy] / BOOTSTRAP_ITERATIONS, 4),
            "mean_bootstrap_rank": round(rank_sum[policy] / BOOTSTRAP_ITERATIONS, 3),
        }
        for policy in primary_ranking
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "method": {
            "primary_metric": "average_task_score",
            "task_count": len(all_tasks),
            "split_checks": "Recompute rankings separately on public_dev and public_test.",
            "leave_one_family_out": "Recompute rankings after removing each 5-task family.",
            "bootstrap": f"{BOOTSTRAP_ITERATIONS} resamples of 50 task ids with replacement.",
            "bootstrap_seed": BOOTSTRAP_SEED,
        },
        "summary": {
            "policies": len(primary_ranking),
            "tasks": len(all_tasks),
            "primary_leader": primary_leader,
            "full_ranking": primary_ranking,
            "split_same_leader": sum(1 for row in split_rows if row["same_leader_as_full"]),
            "leave_one_family_same_leader": sum(1 for row in family_rows if row["same_leader_as_full"]),
            "families_checked": len(family_rows),
            "bootstrap_primary_leader_probability": round(leader_counts[primary_leader] / BOOTSTRAP_ITERATIONS, 4),
            "minimum_leave_one_family_spearman": round(min(row["spearman_with_full"] for row in family_rows), 4),
        },
        "primary_scores": primary_scores,
        "split_rows": split_rows,
        "leave_one_family_rows": family_rows,
        "bootstrap_rows": bootstrap_rows,
        "claim_guardrail": "This audit supports deterministic-baseline rank stability only; hosted/local LLM rankings still require validated provider runs and repeated-run uncertainty.",
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("summary", {})
    if summary.get("tasks") != 50:
        problems.append("Expected stability audit over 50 public tasks.")
    if summary.get("policies", 0) < 4:
        problems.append("Expected at least four deterministic policies.")
    if summary.get("families_checked") != 10:
        problems.append("Expected leave-one-family checks for all 10 families.")
    if len(payload.get("split_rows", [])) != 2:
        problems.append("Expected public_dev and public_test split checks.")
    if len(payload.get("bootstrap_rows", [])) != summary.get("policies"):
        problems.append("Expected one bootstrap row per policy.")
    if summary.get("bootstrap_primary_leader_probability", 0) <= 0:
        problems.append("Primary leader should win at least one bootstrap sample.")
    for row in payload.get("leave_one_family_rows", []):
        if row["tasks_used"] != 45:
            problems.append(f"{row['held_out_family']} leave-one-family check should use 45 tasks.")
        if not -1 <= row["spearman_with_full"] <= 1:
            problems.append(f"{row['held_out_family']} has invalid Spearman correlation.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["leave-one-family", "bootstrap", "public_test", "validated provider runs"]:
        if required not in text:
            problems.append(f"Stability audit must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    split_rows = [
        [row["split"], row["tasks"], row["leader"], " > ".join(row["ranking"]), row["spearman_with_full"], row["same_leader_as_full"]]
        for row in payload["split_rows"]
    ]
    family_rows = [
        [row["held_out_family"], row["tasks_used"], row["leader"], " > ".join(row["ranking"]), row["spearman_with_full"], row["same_leader_as_full"]]
        for row in payload["leave_one_family_rows"]
    ]
    bootstrap_rows = [
        [row["policy"], row["full_rank"], row["full_score"], row["leader_probability"], row["mean_bootstrap_rank"]]
        for row in payload["bootstrap_rows"]
    ]
    lines = [
        "# FounderBench v0.3 Leaderboard Stability Audit",
        "",
        payload["purpose"],
        "",
        "## Method",
        "",
        markdown_table(["Item", "Value"], [[key, value] for key, value in payload["method"].items()]),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Split Stability",
        "",
        markdown_table(["Split", "Tasks", "Leader", "Ranking", "Spearman vs Full", "Same Leader"], split_rows),
        "",
        "## Leave-One-Family-Out Stability",
        "",
        markdown_table(["Held-Out Family", "Tasks Used", "Leader", "Ranking", "Spearman vs Full", "Same Leader"], family_rows),
        "",
        "## Bootstrap Task-Mix Stability",
        "",
        markdown_table(["Policy", "Full Rank", "Full Score", "Leader Probability", "Mean Bootstrap Rank"], bootstrap_rows),
        "",
        "## Claim Guardrail",
        "",
        payload["claim_guardrail"],
        "",
        "## Validation",
        "",
    ]
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The deterministic-baseline leaderboard is internally audited for split, family, and task-mix stability.")
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
    parser = argparse.ArgumentParser(description="Generate deterministic leaderboard stability audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
