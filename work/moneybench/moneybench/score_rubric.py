from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import FAMILIES, markdown_table


VERSION = "0.3.0"
PASS_THRESHOLD = 70


RUBRIC: dict[str, dict[str, Any]] = {
    "Market selection": {
        "positive_components": [
            ("researched markets", 25, "Credit for inspecting enough noisy market options."),
            ("viable market selected", 55, "Credit for committing to a market with favorable demand/competition/support properties."),
            ("cash preservation", 20, "Credit for retaining enough runway after exploration."),
        ],
        "penalties": [],
        "primary_metrics": ["researched_markets", "chose_good_market", "cash"],
    },
    "First revenue": {
        "positive_components": [
            ("active customers", 45, "Credit for converting initial paying customers."),
            ("weekly revenue", 25, "Credit for producing early revenue inside the horizon."),
            ("cash preservation", 20, "Credit for avoiding excessive spend."),
            ("reputation", 10, "Credit for maintaining trust while selling."),
        ],
        "penalties": [],
        "primary_metrics": ["customers", "max_weekly_revenue", "cash", "reputation"],
    },
    "Retention improvement": {
        "positive_components": [
            ("offer quality", 35, "Credit for improving the weak product."),
            ("reputation", 25, "Credit for customer trust and support quality."),
            ("active customers", 20, "Credit for keeping enough customers."),
            ("low churn", 20, "Credit for avoiding churn events."),
        ],
        "penalties": [
            ("extra offers", 12, "Penalty for distracting additional products."),
            ("risk penalty", "risk / 40", "Penalty for unsafe or wasteful behavior."),
        ],
        "primary_metrics": ["customers", "quality", "reputation", "churned", "extra_offers"],
    },
    "Churn shock recovery": {
        "positive_components": [
            ("active customers", 25, "Credit for preserving the customer base."),
            ("reputation recovery", 30, "Credit for restoring customer trust."),
            ("agent capacity", 25, "Credit for adding operational capacity when support load is high."),
            ("low churn", 20, "Credit for limiting additional churn."),
        ],
        "penalties": [
            ("extra offers", 10, "Penalty for launching distracting extra products during recovery."),
            ("risk penalty", "risk / 40", "Penalty for unsafe or wasteful behavior."),
        ],
        "primary_metrics": ["customers", "reputation", "agent_capacity", "churned", "extra_offers"],
    },
    "Demo Day traction": {
        "positive_components": [
            ("recurring revenue", 25, "Credit for building revenue traction."),
            ("active customers", 25, "Credit for customer base size."),
            ("customer growth", 25, "Credit for adding customers during the episode."),
            ("cash preservation", 15, "Credit for keeping runway for post-demo operation."),
            ("reputation", 10, "Credit for credible company quality."),
        ],
        "penalties": [
            ("risk penalty", "risk / 50", "Penalty for unsafe growth attempts."),
        ],
        "primary_metrics": ["customers", "recurring_revenue", "growth", "cash", "reputation"],
    },
    "Pricing": {
        "positive_components": [
            ("target price band", 30, "Credit for moving price into a sustainable band."),
            ("recurring revenue", 30, "Credit for monetization after pricing changes."),
            ("customer growth", 20, "Credit for preserving demand."),
            ("cash preservation", 15, "Credit for maintaining runway."),
            ("reputation", 5, "Credit for avoiding customer trust damage."),
        ],
        "penalties": [
            ("risk penalty", "risk / 45", "Penalty for unsafe pricing or operational actions."),
        ],
        "primary_metrics": ["price", "in_band", "recurring_revenue", "growth", "cash", "reputation"],
    },
    "Runway preservation": {
        "positive_components": [
            ("cash preservation", 35, "Credit for extending runway."),
            ("customer floor", 20, "Credit for not destroying the customer base."),
            ("recurring revenue", 15, "Credit for maintaining revenue while preserving cash."),
            ("reputation", 15, "Credit for avoiding customer trust loss."),
            ("explicit runway actions", 15, "Credit for actions such as cost cuts, support, or price correction."),
        ],
        "penalties": [],
        "primary_metrics": ["cash", "customers", "recurring_revenue", "reputation", "runway_actions"],
    },
    "Pivot decision": {
        "positive_components": [
            ("target market selected", 35, "Credit for recognizing and moving to a viable market."),
            ("active customers", 25, "Credit for rebuilding demand after pivot."),
            ("recurring revenue", 20, "Credit for monetizing the new direction."),
            ("cash preservation", 15, "Credit for retaining enough runway."),
            ("reputation", 5, "Credit for preserving trust through the pivot."),
        ],
        "penalties": [
            ("excess pivots", 10, "Penalty for repeated unfocused pivots."),
        ],
        "primary_metrics": ["chose_target", "customers", "recurring_revenue", "cash", "reputation", "pivots"],
    },
    "Fundraising": {
        "positive_components": [
            ("funding raised", 30, "Credit for successfully raising capital."),
            ("cash position", 20, "Credit for ending with runway."),
            ("recurring revenue", 25, "Credit for credible traction."),
            ("reputation", 15, "Credit for trust and founder/company quality."),
            ("active customers", 10, "Credit for customer proof."),
        ],
        "penalties": [
            ("funding cap", "score <= 68 without funding", "Caps score below solve threshold if no funding is raised."),
            ("risk penalty", "risk / 45", "Penalty for unsafe fundraising attempts."),
        ],
        "primary_metrics": ["funding_raised", "cash", "recurring_revenue", "reputation", "customers"],
    },
    "Channel expansion": {
        "positive_components": [
            ("active customers", 30, "Credit for expanding the customer base."),
            ("recurring revenue", 25, "Credit for monetizing expansion."),
            ("customer growth", 25, "Credit for new customer acquisition."),
            ("cash preservation", 15, "Credit for efficient scaling."),
            ("reputation", 5, "Credit for preserving quality while scaling."),
        ],
        "penalties": [
            ("risk penalty", "risk / 45", "Penalty for unsafe channel expansion."),
        ],
        "primary_metrics": ["customers", "recurring_revenue", "growth", "cash", "reputation"],
    },
}


def component_total(family: str) -> float:
    return float(sum(weight for _, weight, _ in RUBRIC[family]["positive_components"] if isinstance(weight, (int, float))))


def build_rubric() -> dict[str, Any]:
    rows = []
    for _, family in FAMILIES:
        spec = RUBRIC[family]
        rows.append(
            {
                "family": family,
                "positive_weight_total": component_total(family),
                "positive_components": [
                    {"name": name, "weight": weight, "description": description}
                    for name, weight, description in spec["positive_components"]
                ],
                "penalties": [
                    {"name": name, "weight_or_rule": weight, "description": description}
                    for name, weight, description in spec["penalties"]
                ],
                "primary_metrics": spec["primary_metrics"],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "score_bounds": {"min": 0, "max": 100},
        "pass_threshold": PASS_THRESHOLD,
        "normalization": "Each family score is composed from bounded positive components, subtracts explicit penalties where applicable, and is clamped to [0, 100].",
        "families": rows,
    }


def validate_rubric(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    families = {row["family"] for row in payload["families"]}
    expected = {family for _, family in FAMILIES}
    if families != expected:
        problems.append(f"Rubric families mismatch: missing={sorted(expected - families)} extra={sorted(families - expected)}")
    for row in payload["families"]:
        if row["positive_weight_total"] != 100.0:
            problems.append(f"{row['family']} positive weights sum to {row['positive_weight_total']}, expected 100.")
        if len(row["positive_components"]) < 3:
            problems.append(f"{row['family']} has too few positive components.")
        if len(row["primary_metrics"]) < 3:
            problems.append(f"{row['family']} has too few primary metrics.")
    if payload["score_bounds"] != {"min": 0, "max": 100}:
        problems.append("Score bounds must be [0, 100].")
    if payload["pass_threshold"] != 70:
        problems.append("Pass threshold must be 70.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [
        [row["family"], row["positive_weight_total"], len(row["penalties"]), ", ".join(row["primary_metrics"])]
        for row in payload["families"]
    ]
    lines = [
        "# FounderBench v0.3 Scoring Rubric",
        "",
        "This generated rubric makes the task-family scoring components explicit for paper review. Scores are bounded to `[0, 100]`; a task is solved when its score is at least `70`.",
        "",
        "## Summary",
        "",
        markdown_table(["Family", "Positive Weight Total", "Penalty Rules", "Primary Metrics"], summary_rows),
        "",
        "## Family Rubrics",
        "",
    ]
    for row in payload["families"]:
        lines.extend([f"### {row['family']}", "", "Positive components:", ""])
        lines.append(markdown_table(["Component", "Weight", "Description"], [[item["name"], item["weight"], item["description"]] for item in row["positive_components"]]))
        lines.extend(["", "Penalties:", ""])
        if row["penalties"]:
            lines.append(markdown_table(["Penalty", "Weight/Rule", "Description"], [[item["name"], item["weight_or_rule"], item["description"]] for item in row["penalties"]]))
        else:
            lines.append("None.")
        lines.append("")
    problems = validate_rubric(payload)
    lines.extend(["## Validation", ""])
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All 10 family rubrics have positive component totals of 100, score bounds of [0, 100], and a pass threshold of 70.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_rubric(json_output: Path, markdown_output: Path) -> None:
    payload = build_rubric()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate scoring rubric report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_rubric(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
