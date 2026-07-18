from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import FAMILIES, family_name, markdown_table, split_name
from .schema import ActionType
from .tasks import TASKS


VERSION = "0.3.0"
ALL_ACTIONS = set(ActionType.__args__)  # type: ignore[attr-defined]


FAMILY_CAPABILITIES: dict[str, list[str]] = {
    "Market selection": ["market research", "opportunity selection", "early commitment under uncertainty"],
    "First revenue": ["offer building", "campaign execution", "cash-efficient customer acquisition"],
    "Retention improvement": ["product quality improvement", "support", "churn prevention"],
    "Churn shock recovery": ["triage after customer loss", "support scaling", "reputation recovery"],
    "Demo Day traction": ["traction building", "growth pacing", "credible fundraising preparation"],
    "Pricing": ["price correction", "willingness-to-pay inference", "revenue/customer tradeoff"],
    "Runway preservation": ["cost control", "survival under limited cash", "tradeoff-aware operations"],
    "Pivot decision": ["recognizing stalled markets", "customer discovery", "market switching"],
    "Fundraising": ["capital raising", "traction signaling", "reputation and risk management"],
    "Channel expansion": ["partnerships", "scaling working offers", "channel-risk control"],
}


FAMILY_EXPECTED_ACTIONS: dict[str, set[str]] = {
    "Market selection": {"research_market", "build_offer"},
    "First revenue": {"build_offer", "run_campaign", "change_price"},
    "Retention improvement": {"improve_offer", "support_customers"},
    "Churn shock recovery": {"support_customers", "hire_agent", "improve_offer"},
    "Demo Day traction": {"run_campaign", "improve_offer", "raise_funding"},
    "Pricing": {"change_price", "interview_customers", "run_campaign"},
    "Runway preservation": {"cut_cost", "support_customers", "do_nothing"},
    "Pivot decision": {"interview_customers", "pivot_market", "research_market"},
    "Fundraising": {"raise_funding", "run_campaign", "support_customers"},
    "Channel expansion": {"partner_channel", "run_campaign", "hire_agent"},
}


def _counter_rows(counter: Counter[str]) -> list[list[Any]]:
    return [[key, counter[key]] for key in sorted(counter)]


def _task_entry(task) -> dict[str, Any]:
    fam = family_name(task.task_id)
    return {
        "task_id": task.task_id,
        "name": task.name,
        "family": fam,
        "split": split_name(task.task_id),
        "seed": task.seed,
        "weeks": task.weeks,
        "pass_threshold": task.pass_threshold,
        "allowed_actions": sorted(task.allowed_actions),
        "expected_actions": sorted(FAMILY_EXPECTED_ACTIONS[fam]),
        "capabilities": FAMILY_CAPABILITIES[fam],
    }


def build_coverage() -> dict[str, Any]:
    tasks = [_task_entry(task) for task in TASKS]
    family_counts = Counter(task["family"] for task in tasks)
    split_counts = Counter(task["split"] for task in tasks)
    weeks = [int(task["weeks"]) for task in tasks]
    thresholds = [float(task["pass_threshold"]) for task in tasks]
    allowed_action_counts = Counter(action for task in tasks for action in task["allowed_actions"])
    expected_action_counts = Counter(action for task in tasks for action in task["expected_actions"])
    missing_actions = sorted(ALL_ACTIONS - set(allowed_action_counts))
    family_rows = []
    for _, fam in FAMILIES:
        fam_tasks = [task for task in tasks if task["family"] == fam]
        family_rows.append(
            {
                "family": fam,
                "task_count": len(fam_tasks),
                "splits": dict(Counter(task["split"] for task in fam_tasks)),
                "task_ids": [task["task_id"] for task in fam_tasks],
                "expected_actions": sorted(FAMILY_EXPECTED_ACTIONS[fam]),
                "capabilities": FAMILY_CAPABILITIES[fam],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "task_count": len(tasks),
        "summary": {
            "families": len(family_counts),
            "tasks_per_family_min": min(family_counts.values()),
            "tasks_per_family_max": max(family_counts.values()),
            "public_dev_tasks": split_counts.get("public_dev", 0),
            "public_test_tasks": split_counts.get("public_test", 0),
            "action_types_available": len(allowed_action_counts),
            "expected_action_types": len(expected_action_counts),
            "missing_allowed_actions": missing_actions,
            "weeks_min": min(weeks),
            "weeks_max": max(weeks),
            "weeks_mean": round(mean(weeks), 2),
            "pass_threshold_min": min(thresholds),
            "pass_threshold_max": max(thresholds),
        },
        "family_counts": dict(family_counts),
        "split_counts": dict(split_counts),
        "allowed_action_counts": dict(sorted(allowed_action_counts.items())),
        "expected_action_counts": dict(sorted(expected_action_counts.items())),
        "families": family_rows,
        "tasks": tasks,
    }


def validate_coverage(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["task_count"] != 50:
        problems.append(f"Expected 50 tasks, found {payload['task_count']}.")
    if payload["summary"]["families"] != 10:
        problems.append(f"Expected 10 families, found {payload['summary']['families']}.")
    if payload["summary"]["tasks_per_family_min"] != 5 or payload["summary"]["tasks_per_family_max"] != 5:
        problems.append("Expected exactly five tasks per family.")
    if payload["summary"]["public_dev_tasks"] != 30:
        problems.append(f"Expected 30 public_dev tasks, found {payload['summary']['public_dev_tasks']}.")
    if payload["summary"]["public_test_tasks"] != 20:
        problems.append(f"Expected 20 public_test tasks, found {payload['summary']['public_test_tasks']}.")
    if payload["summary"]["missing_allowed_actions"]:
        problems.append(f"Some action types are unavailable: {payload['summary']['missing_allowed_actions']}.")
    for family in payload["families"]:
        if len(family["expected_actions"]) < 2:
            problems.append(f"{family['family']} has too few expected actions.")
        if len(family["capabilities"]) < 2:
            problems.append(f"{family['family']} has too few capability labels.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    family_rows = [
        [
            row["family"],
            row["task_count"],
            ", ".join(row["task_ids"]),
            ", ".join(row["expected_actions"]),
            ", ".join(row["capabilities"]),
        ]
        for row in payload["families"]
    ]
    action_rows = [
        [action, payload["allowed_action_counts"].get(action, 0), payload["expected_action_counts"].get(action, 0)]
        for action in sorted(ALL_ACTIONS)
    ]
    lines = [
        "# FounderBench Task Coverage Report",
        "",
        "This generated report summarizes the fixed public task suite used by the benchmark. It complements the task manifest by explaining family balance, split balance, action coverage, and intended capability coverage.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Split Balance",
        "",
        markdown_table(["Split", "Tasks"], _counter_rows(Counter(payload["split_counts"]))),
        "",
        "## Family Coverage",
        "",
        markdown_table(["Family", "Tasks", "Task IDs", "Expected Actions", "Capabilities"], family_rows),
        "",
        "## Action Coverage",
        "",
        "`Allowed In Tasks` counts how many tasks permit each action. `Expected By Family` counts how many task instances belong to families where the action is strategically relevant.",
        "",
        markdown_table(["Action", "Allowed In Tasks", "Expected By Family"], action_rows),
        "",
        "## Validation",
        "",
    ]
    problems = validate_coverage(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The public task suite has 50 tasks, 10 balanced families, 30 public development tasks, 20 public test tasks, and all 13 structured action types are available.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_coverage(json_output: Path, markdown_output: Path) -> None:
    payload = build_coverage()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate task-suite coverage report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_coverage(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
