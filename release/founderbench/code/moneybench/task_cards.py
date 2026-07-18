from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

from .analysis import FAMILIES, family_name, markdown_table, split_name
from .env import MoneyBenchEnv
from .score_rubric import RUBRIC
from .task_coverage import FAMILY_CAPABILITIES, FAMILY_EXPECTED_ACTIONS
from .tasks import TASKS, StartupTask


VERSION = "0.3.0"


def initial_observation(task: StartupTask) -> dict[str, Any]:
    env = MoneyBenchEnv(seed=task.seed, weeks=task.weeks)
    env.reset()
    task.setup(env)
    return asdict(env.observe())


def build_cards() -> dict[str, Any]:
    cards = []
    for task in TASKS:
        family = family_name(task.task_id)
        observation = initial_observation(task)
        cards.append(
            {
                "task_id": task.task_id,
                "name": task.name,
                "family": family,
                "split": split_name(task.task_id),
                "description": task.description,
                "seed": task.seed,
                "weeks": task.weeks,
                "pass_threshold": task.pass_threshold,
                "allowed_actions": sorted(task.allowed_actions),
                "expected_actions": sorted(FAMILY_EXPECTED_ACTIONS[family]),
                "capabilities": FAMILY_CAPABILITIES[family],
                "scoring_metrics": RUBRIC[family]["primary_metrics"],
                "initial_state": {
                    "cash": observation["cash"],
                    "reputation": observation["reputation"],
                    "agent_capacity": observation["agent_capacity"],
                    "markets_visible": len(observation["markets"]),
                    "offers": len(observation["offers"]),
                    "customers": sum(int(offer.get("customers", 0)) for offer in observation["offers"]),
                    "memory_items": len(observation["memory"]),
                },
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Human-readable task cards for the fixed current release public suite.",
        "summary": {
            "tasks": len(cards),
            "families": len({card["family"] for card in cards}),
            "public_dev": sum(1 for card in cards if card["split"] == "public_dev"),
            "public_test": sum(1 for card in cards if card["split"] == "public_test"),
            "actions": len({action for card in cards for action in card["allowed_actions"]}),
        },
        "families": {span: name for span, name in FAMILIES},
        "cards": cards,
    }


def validate_cards(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["tasks"] != 50:
        problems.append(f"Expected 50 task cards, found {payload['summary']['tasks']}.")
    if payload["summary"]["families"] != 10:
        problems.append(f"Expected 10 families, found {payload['summary']['families']}.")
    if payload["summary"]["public_dev"] != 30:
        problems.append(f"Expected 30 public_dev cards, found {payload['summary']['public_dev']}.")
    if payload["summary"]["public_test"] != 20:
        problems.append(f"Expected 20 public_test cards, found {payload['summary']['public_test']}.")
    for card in payload["cards"]:
        if len(card["allowed_actions"]) < 1:
            problems.append(f"{card['task_id']} has no allowed actions.")
        if len(card["expected_actions"]) < 2:
            problems.append(f"{card['task_id']} has too few expected actions.")
        if len(card["scoring_metrics"]) < 3:
            problems.append(f"{card['task_id']} has too few scoring metrics.")
        if card["initial_state"]["markets_visible"] < 1:
            problems.append(f"{card['task_id']} exposes no markets.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    index_rows = [
        [
            card["task_id"],
            card["name"],
            card["family"],
            card["split"],
            card["weeks"],
            card["initial_state"]["cash"],
            card["initial_state"]["offers"],
            card["initial_state"]["customers"],
        ]
        for card in payload["cards"]
    ]
    lines = [
        "# FounderBench Task Cards",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Task Index",
        "",
        markdown_table(["Task", "Name", "Family", "Split", "Weeks", "Initial Cash", "Initial Offers", "Initial Customers"], index_rows),
        "",
        "## Cards",
        "",
    ]
    for card in payload["cards"]:
        state = card["initial_state"]
        lines.extend(
            [
                f"### {card['task_id']}: {card['name']}",
                "",
                card["description"],
                "",
                markdown_table(
                    ["Field", "Value"],
                    [
                        ["family", card["family"]],
                        ["split", card["split"]],
                        ["seed", card["seed"]],
                        ["weeks", card["weeks"]],
                        ["pass_threshold", card["pass_threshold"]],
                        ["initial_cash", state["cash"]],
                        ["initial_reputation", state["reputation"]],
                        ["initial_agent_capacity", state["agent_capacity"]],
                        ["initial_offers", state["offers"]],
                        ["initial_customers", state["customers"]],
                        ["markets_visible", state["markets_visible"]],
                        ["expected_actions", ", ".join(card["expected_actions"])],
                        ["scoring_metrics", ", ".join(card["scoring_metrics"])],
                        ["capabilities", ", ".join(card["capabilities"])],
                    ],
                ),
                "",
            ]
        )
    lines.extend(["## Validation", ""])
    problems = validate_cards(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All 50 public task cards include family, split, horizon, initial-state summary, expected actions, and scoring metrics.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_cards(json_output: Path, markdown_output: Path) -> None:
    payload = build_cards()
    problems = validate_cards(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate human-readable task cards.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_cards(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
