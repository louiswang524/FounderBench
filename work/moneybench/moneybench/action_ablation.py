from __future__ import annotations

import argparse
import json
from statistics import mean
from pathlib import Path
from typing import Any

from .analysis import bootstrap_mean_ci, family_name, markdown_table, task_number
from .policies import Policy, TaskHeuristicPolicy
from .schema import Action, Observation
from .submission import validate_run
from .task_runner import run_task
from .tasks import TASKS


VERSION = "0.3.0"


ABLATIONS: list[dict[str, Any]] = [
    {
        "id": "full_task_heuristic",
        "blocked_actions": [],
        "hypothesis": "Reference policy with the full expanded action space.",
    },
    {
        "id": "no_discovery",
        "blocked_actions": ["research_market", "interview_customers"],
        "hypothesis": "Tests dependence on market/customer information gathering.",
    },
    {
        "id": "no_growth",
        "blocked_actions": ["run_campaign", "partner_channel"],
        "hypothesis": "Tests dependence on acquisition and distribution expansion.",
    },
    {
        "id": "no_quality_support_capacity",
        "blocked_actions": ["improve_offer", "support_customers", "hire_agent"],
        "hypothesis": "Tests dependence on retention, quality, support, and capacity actions.",
    },
    {
        "id": "no_pricing",
        "blocked_actions": ["change_price"],
        "hypothesis": "Tests dependence on explicit price correction.",
    },
    {
        "id": "no_runway_funding",
        "blocked_actions": ["cut_cost", "raise_funding"],
        "hypothesis": "Tests dependence on cash preservation and fundraising actions.",
    },
    {
        "id": "no_pivot",
        "blocked_actions": ["pivot_market"],
        "hypothesis": "Tests dependence on explicit market switching.",
    },
]


class ActionFilterPolicy(Policy):
    def __init__(self, blocked_actions: set[str]):
        self.base = TaskHeuristicPolicy()
        self.blocked_actions = blocked_actions

    def act(self, observation: Observation) -> list[Action]:
        return self._filter(self.base.act(observation))

    def act_task(self, task_id: str, observation: Observation) -> list[Action]:
        return self._filter(self.base.act_task(task_id, observation))

    def _filter(self, actions: list[Action]) -> list[Action]:
        kept = [action for action in actions if action.type not in self.blocked_actions]
        return kept or [Action("do_nothing")]


def run_filtered_suite(ablation: dict[str, Any]) -> dict[str, Any]:
    policy = ActionFilterPolicy(set(ablation["blocked_actions"]))
    results = [run_task(task, policy) for task in TASKS]
    solved = sum(1 for result in results if result["score"]["passed"])
    average = sum(float(result["score"]["score"]) for result in results) / len(results)
    diagnostics = {
        "invalid_actions": sum(int(result["diagnostics"]["invalid_actions"]) for result in results),
        "over_budget_decisions": sum(int(result["diagnostics"]["over_budget_decisions"]) for result in results),
        "provider_errors": sum(int(result["diagnostics"]["provider_errors"]) for result in results),
        "provider_error_categories": {},
        "total_actions": sum(int(result["diagnostics"]["total_actions"]) for result in results),
        "decision_latency_s": round(sum(float(result["diagnostics"]["decision_latency_s"]) for result in results), 4),
        "simulated_api_cost": round(sum(float(result["diagnostics"]["simulated_api_cost"]) for result in results), 2),
        "provider_prompt_tokens": 0,
        "provider_completion_tokens": 0,
        "provider_total_tokens": 0,
        "estimated_provider_cost_usd": 0.0,
    }
    split_summary = {}
    for split_name, predicate in {
        "public_dev": lambda task_id: int(task_id.split("-")[1]) <= 30,
        "public_test": lambda task_id: 30 < int(task_id.split("-")[1]) <= 50,
    }.items():
        split_results = [result for result in results if predicate(result["task_id"])]
        split_solved = sum(1 for result in split_results if result["score"]["passed"])
        split_summary[split_name] = {
            "tasks": len(split_results),
            "solved": split_solved,
            "solve_rate": round(split_solved / len(split_results), 3),
            "average_task_score": round(sum(float(result["score"]["score"]) for result in split_results) / len(split_results), 2),
        }
    return {
        "policy": f"action_ablation/{ablation['id']}",
        "benchmark_version": VERSION,
        "ablation_id": ablation["id"],
        "blocked_actions": ablation["blocked_actions"],
        "hypothesis": ablation["hypothesis"],
        "tasks": len(results),
        "solved": solved,
        "solve_rate": round(solved / len(results), 3),
        "average_task_score": round(average, 2),
        "diagnostics": diagnostics,
        "splits": split_summary,
        "results": results,
    }


def _task_scores(run: dict[str, Any]) -> dict[str, float]:
    return {result["task_id"]: float(result["score"]["score"]) for result in run["results"]}


def _family_drops(reference: dict[str, Any], ablated: dict[str, Any]) -> list[dict[str, Any]]:
    ref_scores = _task_scores(reference)
    ablated_scores = _task_scores(ablated)
    rows = []
    for family in sorted({family_name(task_id) for task_id in ref_scores}):
        task_ids = sorted([task_id for task_id in ref_scores if family_name(task_id) == family], key=task_number)
        drops = [ref_scores[task_id] - ablated_scores[task_id] for task_id in task_ids]
        rows.append({"family": family, "mean_score_drop": round(mean(drops), 2), "tasks": len(task_ids)})
    return sorted(rows, key=lambda row: row["mean_score_drop"], reverse=True)


def build_report() -> dict[str, Any]:
    runs = [run_filtered_suite(ablation) for ablation in ABLATIONS]
    reference = runs[0]
    ref_scores = _task_scores(reference)
    rows = []
    for run in runs:
        scores = _task_scores(run)
        drops = [ref_scores[task_id] - scores[task_id] for task_id in sorted(ref_scores, key=task_number)]
        low, high = bootstrap_mean_ci(drops, seed=20260715 + len(run["ablation_id"]))
        rows.append(
            {
                "ablation_id": run["ablation_id"],
                "blocked_actions": run["blocked_actions"],
                "hypothesis": run["hypothesis"],
                "average_task_score": run["average_task_score"],
                "solved": run["solved"],
                "mean_score_drop": round(mean(drops), 2),
                "drop_95_ci": [round(low, 2), round(high, 2)],
                "solved_drop": reference["solved"] - run["solved"],
                "largest_family_drops": _family_drops(reference, run)[:3],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Action-space ablation of the task-aware heuristic over the full 50-task public suite.",
        "reference": "full_task_heuristic",
        "runs": runs,
        "rows": rows,
        "summary": {
            "ablations": len(rows),
            "tasks_per_ablation": 50,
            "reference_score": reference["average_task_score"],
            "reference_solved": reference["solved"],
            "largest_score_drop": max(row["mean_score_drop"] for row in rows),
            "largest_solved_drop": max(row["solved_drop"] for row in rows),
        },
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("summary", {}).get("ablations", 0) < 6:
        problems.append("Expected at least six action-space ablation rows.")
    if payload.get("summary", {}).get("tasks_per_ablation") != 50:
        problems.append("Expected 50 tasks per ablation.")
    for run in payload.get("runs", []):
        problems.extend(validate_run(run))
    if payload.get("rows", [{}])[0].get("ablation_id") != "full_task_heuristic":
        problems.append("First ablation row must be the full task-heuristic reference.")
    if payload.get("summary", {}).get("largest_score_drop", 0) <= 0:
        problems.append("Expected at least one action ablation to reduce average score.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["ablation_id"],
            ", ".join(row["blocked_actions"]) or "none",
            f"{row['average_task_score']:.2f}",
            row["solved"],
            f"{row['mean_score_drop']:+.2f}",
            f"[{row['drop_95_ci'][0]:+.2f}, {row['drop_95_ci'][1]:+.2f}]",
            f"{row['solved_drop']:+d}",
            "; ".join(f"{item['family']} {item['mean_score_drop']:+.2f}" for item in row["largest_family_drops"]),
        ]
        for row in payload["rows"]
    ]
    lines = [
        "# FounderBench v0.3 Action-Space Ablation",
        "",
        payload["purpose"],
        "",
        "The reference is the task-aware heuristic with all actions enabled. Each ablation filters one action group from that same policy, replaces empty action lists with `do_nothing`, and reruns all 50 tasks.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Ablation Results",
        "",
        markdown_table(
            ["Ablation", "Blocked Actions", "Avg Score", "Solved", "Mean Score Drop", "Drop 95% CI", "Solved Drop", "Largest Family Drops"],
            rows,
        ),
        "",
        "## Interpretation",
        "",
        "- Large drops indicate that the expanded action space is not decorative: removing the action group changes benchmark outcomes.",
        "- This ablation is a deterministic simulator calibration, not a substitute for hosted LLM ablations.",
        "- Hosted LLM method ablations should report the same primary metrics plus provider cost and error diagnostics.",
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
        lines.append("All action-space ablation runs cover 50 tasks and pass the submission validator.")
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
    parser = argparse.ArgumentParser(description="Generate action-space ablation report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
