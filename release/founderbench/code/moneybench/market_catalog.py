from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import markdown_table
from .env import DEFAULT_MARKETS


VERSION = "0.3.0"


def classify(value: float, low: float, high: float) -> str:
    if value < low:
        return "low"
    if value > high:
        return "high"
    return "medium"


def build_catalog() -> dict[str, Any]:
    rows = []
    for market in DEFAULT_MARKETS:
        rows.append(
            {
                **asdict(market),
                "demand_band": classify(market.base_demand, 0.55, 0.72),
                "competition_band": classify(market.competition, 0.4, 0.62),
                "build_complexity_band": classify(market.build_complexity, 0.35, 0.52),
                "support_load_band": classify(market.support_load, 0.3, 0.45),
                "volatility_band": classify(market.volatility, 0.1, 0.15),
                "opportunity_notes": [
                    "Higher demand helps acquisition.",
                    "Higher competition reduces conversion.",
                    "Higher willingness_to_pay supports higher prices.",
                    "Higher support_load increases weekly support cost and churn pressure.",
                    "Higher build_complexity requires more build_offer budget for quality.",
                ],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Human-readable catalog of the fixed simulated markets used in current release.",
        "summary": {
            "markets": len(rows),
            "mean_base_demand": round(mean(row["base_demand"] for row in rows), 3),
            "mean_competition": round(mean(row["competition"] for row in rows), 3),
            "mean_willingness_to_pay": round(mean(row["willingness_to_pay"] for row in rows), 2),
            "mean_support_load": round(mean(row["support_load"] for row in rows), 3),
        },
        "observation_rules": [
            "Unresearched markets expose noisy demand, competition, and willingness-to-pay signals.",
            "research_market or interview_customers with a market_id marks that market as researched.",
            "Researched markets expose exact current demand, exact competition, and exact willingness-to-pay signals.",
            "Current demand equals base_demand plus seed-dependent market momentum, clamped to [0.05, 1.2].",
            "Market momentum evolves each week using volatility-scaled shocks and decay.",
        ],
        "settlement_rules": [
            "Customer acquisition increases with demand, awareness, quality, price fit, and reputation.",
            "Competition subtracts from conversion.",
            "Churn depends on support load, offer quality, and reputation.",
            "Weekly support cost scales with customers and support load.",
            "Support overload can reduce reputation when support_required exceeds agent_capacity * 30.",
        ],
        "markets": rows,
    }


def validate_catalog(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["markets"] != 8:
        problems.append(f"Expected 8 markets, found {payload['summary']['markets']}.")
    ids = [row["market_id"] for row in payload["markets"]]
    if len(ids) != len(set(ids)):
        problems.append("Market ids must be unique.")
    for row in payload["markets"]:
        for field in ["base_demand", "competition", "willingness_to_pay", "build_complexity", "support_load", "volatility"]:
            if not isinstance(row[field], (int, float)):
                problems.append(f"{row['market_id']} field {field} must be numeric.")
        if not row["need"]:
            problems.append(f"{row['market_id']} missing need description.")
    if len(payload["observation_rules"]) < 4:
        problems.append("Expected at least four observation rules.")
    if len(payload["settlement_rules"]) < 4:
        problems.append("Expected at least four settlement rules.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    market_rows = [
        [
            row["market_id"],
            row["name"],
            row["base_demand"],
            row["competition"],
            row["willingness_to_pay"],
            row["build_complexity"],
            row["support_load"],
            row["volatility"],
        ]
        for row in payload["markets"]
    ]
    band_rows = [
        [
            row["market_id"],
            row["demand_band"],
            row["competition_band"],
            row["build_complexity_band"],
            row["support_load_band"],
            row["volatility_band"],
        ]
        for row in payload["markets"]
    ]
    lines = [
        "# FounderBench Market Catalog",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Observation Rules",
        "",
    ]
    lines.extend(f"- {rule}" for rule in payload["observation_rules"])
    lines.extend(["", "## Settlement Rules", ""])
    lines.extend(f"- {rule}" for rule in payload["settlement_rules"])
    lines.extend(
        [
            "",
            "## Market Parameters",
            "",
            markdown_table(["Market ID", "Name", "Demand", "Competition", "WTP", "Build Complexity", "Support Load", "Volatility"], market_rows),
            "",
            "## Market Bands",
            "",
            markdown_table(["Market ID", "Demand", "Competition", "Build Complexity", "Support Load", "Volatility"], band_rows),
            "",
            "## Market Cards",
            "",
        ]
    )
    for row in payload["markets"]:
        lines.extend(
            [
                f"### `{row['market_id']}`: {row['name']}",
                "",
                markdown_table(
                    ["Field", "Value"],
                    [
                        ["need", row["need"]],
                        ["base_demand", row["base_demand"]],
                        ["competition", row["competition"]],
                        ["willingness_to_pay", row["willingness_to_pay"]],
                        ["build_complexity", row["build_complexity"]],
                        ["support_load", row["support_load"]],
                        ["volatility", row["volatility"]],
                        ["bands", f"demand={row['demand_band']}, competition={row['competition_band']}, support={row['support_load_band']}"],
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
        lines.append("All 8 fixed markets have unique ids, numeric simulator parameters, and documented observation/settlement rules.")
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
    parser = argparse.ArgumentParser(description="Generate market catalog.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_catalog(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
