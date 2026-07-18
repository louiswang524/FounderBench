from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, get_args

from .analysis import markdown_table
from .schema import ActionType


VERSION = "0.3.0"


ACTION_SEMANTICS: dict[str, dict[str, Any]] = {
    "research_market": {
        "required_fields": ["market_id"],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "max(80, budget or 120)",
        "primary_effects": ["Marks the target market as researched.", "Reveals less noisy future market signals."],
        "risk_triggers": ["Unknown market adds 220 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Reduce market uncertainty before building, pivoting, or interviewing.",
    },
    "build_offer": {
        "required_fields": ["market_id"],
        "optional_fields": ["budget", "price"],
        "minimum_or_default_cost": "budget; underfunded if budget < 700 + build_complexity * 1300",
        "primary_effects": ["Creates a new offer.", "Quality increases with budget and agent capacity.", "Default price is 82% of willingness to pay."],
        "risk_triggers": ["Unknown market adds 260 risk.", "Underfunding adds 180 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Create the product/offer that can later acquire customers and revenue.",
    },
    "run_campaign": {
        "required_fields": ["offer_id"],
        "optional_fields": ["budget", "message_quality"],
        "minimum_or_default_cost": "budget",
        "primary_effects": ["Increases offer awareness based on spend and message quality."],
        "risk_triggers": ["Unknown offer adds 260 risk.", "message_quality < 0.35 adds 360 risk and lowers reputation.", "Budget above 1600 adds spam risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Acquire customers for a built offer.",
    },
    "improve_offer": {
        "required_fields": ["offer_id"],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "budget",
        "primary_effects": ["Improves offer quality based on spend and agent capacity."],
        "risk_triggers": ["Unknown offer adds 240 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Increase retention, conversion, reputation resilience, and product quality.",
    },
    "hire_agent": {
        "required_fields": [],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "max(900, budget or 1200)",
        "primary_effects": ["Increases agent capacity by 0.18 plus up to 0.25 based on spend."],
        "risk_triggers": ["Budget above 65% of cash adds 450 risk."],
        "typical_use": "Add operational capacity when support load or growth strains the company.",
    },
    "support_customers": {
        "required_fields": [],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "budget",
        "primary_effects": ["Improves reputation based on support spend."],
        "risk_triggers": ["Budget above 65% of cash adds 450 risk."],
        "typical_use": "Protect reputation, reduce churn pressure, and stabilize overloaded operations.",
    },
    "change_price": {
        "required_fields": ["offer_id", "price"],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "max(40, budget)",
        "primary_effects": ["Changes offer price."],
        "risk_triggers": ["Unknown offer adds 220 risk.", "Missing/nonpositive price adds 220 risk.", "Price > 135% of willingness to pay adds 160 risk and lowers reputation.", "Price < 45% of willingness to pay adds 80 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Correct weak pricing and balance revenue against demand.",
    },
    "interview_customers": {
        "required_fields": [],
        "optional_fields": ["market_id", "offer_id", "budget"],
        "minimum_or_default_cost": "max(100, budget)",
        "primary_effects": ["Researches target market when provided.", "Improves reputation.", "Can improve offer quality and awareness."],
        "risk_triggers": ["No valid market or offer target adds 120 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Gather customer discovery before pricing, pivoting, or improving a product.",
    },
    "cut_cost": {
        "required_fields": [],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "negative cost/savings: -(min(900, 180 + customers * 18 + budget * 0.25))",
        "primary_effects": ["Increases cash through operating savings.", "Slightly reduces agent capacity."],
        "risk_triggers": ["If customer load exceeds reduced capacity, adds 180 risk and lowers reputation.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Preserve runway under cash pressure.",
    },
    "pivot_market": {
        "required_fields": ["offer_id", "market_id"],
        "optional_fields": ["budget"],
        "minimum_or_default_cost": "max(650, budget)",
        "primary_effects": ["Moves an offer to a new market.", "Loses about half existing customers.", "Reduces quality and awareness.", "Researches the target market."],
        "risk_triggers": ["Missing offer or market adds 280 risk.", "Adds 140 + 20 per lost customer risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Recover from a stalled market when discovery indicates a better target.",
    },
    "raise_funding": {
        "required_fields": [],
        "optional_fields": ["budget", "price"],
        "minimum_or_default_cost": "250 direct cost; funding ask is max(budget, price or 5000)",
        "primary_effects": ["Adds raised capital to cash.", "Raised amount depends on reputation, traction, and cash position."],
        "risk_triggers": ["Unmet funding ask adds 3% of ask-minus-raised as risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Increase runway when credible traction and reputation support fundraising.",
    },
    "partner_channel": {
        "required_fields": ["offer_id"],
        "optional_fields": ["budget", "message_quality"],
        "minimum_or_default_cost": "budget",
        "primary_effects": ["Increases offer awareness through partnerships.", "Slightly improves reputation based on message quality."],
        "risk_triggers": ["Unknown offer adds 240 risk.", "Budget below 500 adds 80 risk.", "Budget above 65% of cash adds 450 risk."],
        "typical_use": "Scale acquisition for a working offer through a partner channel.",
    },
    "do_nothing": {
        "required_fields": [],
        "optional_fields": [],
        "minimum_or_default_cost": "0",
        "primary_effects": ["No direct action effect; weekly settlement still occurs."],
        "risk_triggers": [],
        "typical_use": "Hold position when no useful action remains or after provider failure fallback.",
    },
}


GLOBAL_RULES = [
    "Each non-do_nothing action increments the simulator-side API cost proxy by 0.35.",
    "Any action with budget above 65% of current cash adds 450 risk.",
    "If more than 5 actions are submitted in a week, extra actions are truncated and coordination risk is added.",
    "After actions execute, weekly settlement updates revenue, support costs, customer acquisition, churn, reputation, cash, and market momentum.",
    "If cash falls below zero, the company is marked bankrupt and receives an additional bankruptcy risk event.",
]


def build_catalog() -> dict[str, Any]:
    actions = list(get_args(ActionType))
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Human-readable semantics for the 13 structured business actions executed by the simulator.",
        "summary": {
            "actions": len(actions),
            "actions_with_required_fields": sum(1 for action in actions if ACTION_SEMANTICS[action]["required_fields"]),
            "actions_with_risk_triggers": sum(1 for action in actions if ACTION_SEMANTICS[action]["risk_triggers"]),
        },
        "global_rules": GLOBAL_RULES,
        "actions": [{"type": action, **ACTION_SEMANTICS[action]} for action in actions],
    }


def validate_catalog(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    expected = set(get_args(ActionType))
    actual = {row["type"] for row in payload.get("actions", [])}
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if actual != expected:
        problems.append(f"Action coverage mismatch: missing={sorted(expected - actual)} extra={sorted(actual - expected)}")
    if payload["summary"]["actions"] != len(expected):
        problems.append(f"Expected {len(expected)} actions, found {payload['summary']['actions']}.")
    if len(payload.get("global_rules", [])) < 4:
        problems.append("Expected at least four global simulator rules.")
    for row in payload.get("actions", []):
        for field in ["required_fields", "optional_fields", "minimum_or_default_cost", "primary_effects", "risk_triggers", "typical_use"]:
            if field not in row:
                problems.append(f"{row.get('type', '<unknown>')} missing {field}.")
        if not row.get("primary_effects"):
            problems.append(f"{row.get('type', '<unknown>')} has no primary effects.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    overview_rows = [
        [
            row["type"],
            ", ".join(row["required_fields"]) or "none",
            ", ".join(row["optional_fields"]) or "none",
            row["minimum_or_default_cost"],
            len(row["risk_triggers"]),
        ]
        for row in payload["actions"]
    ]
    lines = [
        "# FounderBench v0.3 Action Semantics",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Global Simulator Rules",
        "",
    ]
    lines.extend(f"- {rule}" for rule in payload["global_rules"])
    lines.extend(
        [
            "",
            "## Action Overview",
            "",
            markdown_table(["Action", "Required Fields", "Optional Fields", "Cost Rule", "Risk Trigger Count"], overview_rows),
            "",
            "## Action Cards",
            "",
        ]
    )
    for row in payload["actions"]:
        lines.extend(
            [
                f"### `{row['type']}`",
                "",
                markdown_table(
                    ["Field", "Value"],
                    [
                        ["required_fields", ", ".join(row["required_fields"]) or "none"],
                        ["optional_fields", ", ".join(row["optional_fields"]) or "none"],
                        ["minimum_or_default_cost", row["minimum_or_default_cost"]],
                        ["primary_effects", "; ".join(row["primary_effects"])],
                        ["risk_triggers", "; ".join(row["risk_triggers"]) or "none"],
                        ["typical_use", row["typical_use"]],
                    ],
                ),
                "",
            ]
        )
    lines.extend(["## Validation", ""])
    problems = validate_catalog(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All 13 structured actions are documented with fields, cost rules, effects, risks, and typical use cases.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_catalog(json_output: Path, markdown_output: Path) -> None:
    payload = build_catalog()
    problems = validate_catalog(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate action semantics catalog.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_catalog(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
