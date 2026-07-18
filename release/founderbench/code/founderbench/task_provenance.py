from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import FAMILIES, family_name, markdown_table, split_name, task_number
from .task_coverage import FAMILY_CAPABILITIES, FAMILY_EXPECTED_ACTIONS
from .tasks import TASKS


VERSION = "0.3.0"


TEMPLATE_METADATA: dict[str, dict[str, Any]] = {
    "Market selection": {
        "task_range": "FND-001..FND-005",
        "construction": "hand-authored viable-market target sets over no_setup initial states",
        "seed_rule": "literal seed list [11, 41, 43, 47, 53]",
        "setup_source": "no_setup",
        "score_source": "make_market_selection_score",
        "primary_variation": ["good market set", "simulator seed"],
    },
    "First revenue": {
        "task_range": "FND-006..FND-010",
        "construction": "template loop over no_setup initial states with customer/revenue/cash targets",
        "seed_rule": "literal seed list [7, 59, 61, 67, 71]",
        "setup_source": "no_setup",
        "score_source": "make_first_revenue_score",
        "primary_variation": ["target_customers", "target_revenue", "target_cash", "simulator seed"],
    },
    "Retention improvement": {
        "task_range": "FND-011..FND-015",
        "construction": "five hand-authored existing-offer startup states",
        "seed_rule": "19 + task_number",
        "setup_source": "setup_existing_offer",
        "score_source": "make_retention_score",
        "primary_variation": ["market", "cash", "reputation", "capacity", "quality", "customers"],
    },
    "Churn shock recovery": {
        "task_range": "FND-016..FND-020",
        "construction": "five overloaded existing-offer states with support/retention pressure",
        "seed_rule": "23 + task_number",
        "setup_source": "setup_churn_shock",
        "score_source": "make_churn_shock_score",
        "primary_variation": ["market", "cash", "reputation", "capacity", "customer pressure"],
    },
    "Demo Day traction": {
        "task_range": "FND-021..FND-025",
        "construction": "five demo-day growth states with existing traction",
        "seed_rule": "31 + task_number",
        "setup_source": "setup_demo_day",
        "score_source": "make_demo_day_score",
        "primary_variation": ["market", "cash", "existing customers", "growth target", "revenue target"],
    },
    "Pricing": {
        "task_range": "FND-026..FND-030",
        "construction": "five existing-offer states with intentionally weak starting prices",
        "seed_rule": "37 + task_number",
        "setup_source": "setup_existing_offer",
        "score_source": "make_pricing_score",
        "primary_variation": ["market", "starting price", "acceptable price band", "revenue target"],
    },
    "Runway preservation": {
        "task_range": "FND-031..FND-035",
        "construction": "five low-cash existing-offer states requiring tradeoff-aware operations",
        "seed_rule": "41 + task_number",
        "setup_source": "setup_existing_offer",
        "score_source": "make_runway_score",
        "primary_variation": ["market", "cash pressure", "customer floor", "cash target"],
    },
    "Pivot decision": {
        "task_range": "FND-036..FND-040",
        "construction": "five stalled-offer states with target market sets",
        "seed_rule": "43 + task_number",
        "setup_source": "setup_existing_offer with current market pre-researched",
        "score_source": "make_pivot_score",
        "primary_variation": ["stalled market", "target markets", "cash", "starting customers"],
    },
    "Fundraising": {
        "task_range": "FND-041..FND-045",
        "construction": "five traction states where credible fundraising depends on operations",
        "seed_rule": "47 + task_number",
        "setup_source": "setup_demo_day",
        "score_source": "make_fundraising_score",
        "primary_variation": ["market", "cash target", "revenue target", "reputation target"],
    },
    "Channel expansion": {
        "task_range": "FND-046..FND-050",
        "construction": "five under-distributed working-offer states",
        "seed_rule": "53 + task_number",
        "setup_source": "setup_existing_offer",
        "score_source": "make_channel_score",
        "primary_variation": ["market", "awareness", "customer target", "revenue target"],
    },
}


def build_provenance() -> dict[str, Any]:
    task_rows = []
    template_rows = []
    for _, family in FAMILIES:
        tasks = sorted([task for task in TASKS if family_name(task.task_id) == family], key=lambda task: task_number(task.task_id))
        metadata = TEMPLATE_METADATA[family]
        template_rows.append(
            {
                "family": family,
                "task_range": metadata["task_range"],
                "task_ids": [task.task_id for task in tasks],
                "split_counts": {
                    "public_dev": sum(1 for task in tasks if split_name(task.task_id) == "public_dev"),
                    "public_test": sum(1 for task in tasks if split_name(task.task_id) == "public_test"),
                },
                "construction": metadata["construction"],
                "seed_rule": metadata["seed_rule"],
                "setup_source": metadata["setup_source"],
                "score_source": metadata["score_source"],
                "expected_actions": sorted(FAMILY_EXPECTED_ACTIONS[family]),
                "capabilities": FAMILY_CAPABILITIES[family],
                "primary_variation": metadata["primary_variation"],
            }
        )
        for task in tasks:
            task_rows.append(
                {
                    "task_id": task.task_id,
                    "family": family,
                    "split": split_name(task.task_id),
                    "name": task.name,
                    "seed": task.seed,
                    "weeks": task.weeks,
                    "pass_threshold": task.pass_threshold,
                    "template_range": metadata["task_range"],
                    "setup_source": metadata["setup_source"],
                    "score_source": metadata["score_source"],
                    "expected_actions": sorted(FAMILY_EXPECTED_ACTIONS[family]),
                }
            )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Task curation and provenance record for the fixed current release public suite.",
        "curation_method": {
            "source": "Hand-designed synthetic startup templates encoded in work/founderbench/founderbench/tasks.py.",
            "template_count": 10,
            "variants_per_template": 5,
            "public_split_rule": "FND-001..FND-030 are public_dev; FND-031..FND-050 are public_test.",
            "private_holdout_status": "Blueprint/protocol only; private task definitions are not included in current release.",
            "real_world_data_used": False,
            "human_subject_data_used": False,
            "external_private_data_used": False,
        },
        "templates": template_rows,
        "tasks": task_rows,
        "summary": {
            "tasks": len(task_rows),
            "templates": len(template_rows),
            "public_dev": sum(1 for task in task_rows if task["split"] == "public_dev"),
            "public_test": sum(1 for task in task_rows if task["split"] == "public_test"),
            "real_world_data_used": False,
            "human_subject_data_used": False,
            "all_templates_have_five_tasks": all(len(row["task_ids"]) == 5 for row in template_rows),
        },
    }


def validate_provenance(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["tasks"] != 50:
        problems.append(f"Expected 50 tasks, found {payload['summary']['tasks']}.")
    if payload["summary"]["templates"] != 10:
        problems.append(f"Expected 10 templates, found {payload['summary']['templates']}.")
    if payload["summary"]["public_dev"] != 30:
        problems.append(f"Expected 30 public_dev tasks, found {payload['summary']['public_dev']}.")
    if payload["summary"]["public_test"] != 20:
        problems.append(f"Expected 20 public_test tasks, found {payload['summary']['public_test']}.")
    if not payload["summary"]["all_templates_have_five_tasks"]:
        problems.append("Every template should have exactly five public tasks.")
    if payload["curation_method"]["real_world_data_used"] or payload["curation_method"]["human_subject_data_used"]:
        problems.append("current release provenance should not claim real-world or human-subject source data.")
    for row in payload["templates"]:
        if len(row["expected_actions"]) < 2:
            problems.append(f"{row['family']} has too few expected actions.")
        if not row["seed_rule"] or not row["score_source"]:
            problems.append(f"{row['family']} missing seed or score provenance.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    template_rows = [
        [
            row["family"],
            row["task_range"],
            ", ".join(row["task_ids"]),
            row["construction"],
            row["seed_rule"],
            row["setup_source"],
            row["score_source"],
        ]
        for row in payload["templates"]
    ]
    lines = [
        "# FounderBench Task Provenance",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Curation Method",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["curation_method"].items()]),
        "",
        "## Template Provenance",
        "",
        markdown_table(["Family", "Range", "Task IDs", "Construction", "Seed Rule", "Setup Source", "Score Source"], template_rows),
        "",
        "## Notes",
        "",
        "- current release is a controlled synthetic benchmark suite, not a dataset mined from real companies.",
        "- The task templates are public in source code; private hidden evaluation is reserved for a future evaluator-hosted cycle.",
        "- This provenance record should be cited alongside the task manifest, task-card catalog, and validity report.",
        "",
        "## Validation",
        "",
    ]
    problems = validate_provenance(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All 50 public tasks trace to 10 documented synthetic templates with explicit split, seed, setup, and scoring provenance.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_provenance(json_output: Path, markdown_output: Path) -> None:
    payload = build_provenance()
    problems = validate_provenance(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate task-suite provenance artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_provenance(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
