from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .env import MoneyBenchEnv
from .schema import Action
from .task_runner import run_suite


VERSION = "0.3.0"


SCENARIOS: list[dict[str, Any]] = [
    {
        "id": "hold_position",
        "seed": 101,
        "actions": [[Action("do_nothing")], [Action("do_nothing")], [Action("do_nothing")]],
    },
    {
        "id": "build_and_support",
        "seed": 102,
        "actions": [
            [Action("research_market", market_id="saas_churn", budget=120)],
            [Action("build_offer", market_id="saas_churn", budget=2200, price=220)],
            [Action("run_campaign", offer_id="offer_1", budget=900, message_quality=0.8), Action("support_customers", budget=350)],
            [Action("improve_offer", offer_id="offer_1", budget=800)],
        ],
    },
    {
        "id": "unknown_targets_are_risky",
        "seed": 103,
        "actions": [
            [Action("research_market", market_id="missing_market", budget=300)],
            [Action("run_campaign", offer_id="missing_offer", budget=700)],
            [Action("pivot_market", offer_id="missing_offer", market_id="missing_market", budget=700)],
        ],
    },
    {
        "id": "overbudget_bankruptcy_path",
        "seed": 104,
        "actions": [[Action("build_offer", market_id="legal_summary", budget=25000, price=380)]],
    },
    {
        "id": "runway_cost_cut_path",
        "seed": 105,
        "actions": [
            [Action("build_offer", market_id="data_cleanup", budget=1800, price=190)],
            [Action("cut_cost", budget=400)],
            [Action("support_customers", budget=250)],
        ],
    },
]


def _check_env_invariants(env: MoneyBenchEnv, previous_week: int | None) -> list[str]:
    problems: list[str] = []
    state = env.state
    if previous_week is not None and not state.bankrupt and state.week != previous_week + 1:
        problems.append(f"week should advance by 1 from {previous_week}, found {state.week}.")
    if not math.isfinite(state.cash):
        problems.append("cash must stay finite.")
    if not 0.0 <= state.reputation <= 1.0:
        problems.append(f"reputation out of bounds: {state.reputation}.")
    if state.agent_capacity < 0:
        problems.append(f"agent_capacity must be nonnegative, found {state.agent_capacity}.")
    if state.total_risk_penalty < 0:
        problems.append(f"total_risk_penalty must be nonnegative, found {state.total_risk_penalty}.")
    if state.cumulative_revenue < 0:
        problems.append(f"cumulative_revenue must be nonnegative, found {state.cumulative_revenue}.")
    if state.cumulative_api_cost < 0:
        problems.append(f"cumulative_api_cost must be nonnegative, found {state.cumulative_api_cost}.")
    if state.total_funding_raised < 0:
        problems.append(f"total_funding_raised must be nonnegative, found {state.total_funding_raised}.")
    if len(state.memory) > 40:
        problems.append(f"memory length must be <= 40, found {len(state.memory)}.")
    for offer in state.offers:
        if offer.customers < 0:
            problems.append(f"{offer.offer_id} customers must be nonnegative, found {offer.customers}.")
        if offer.age < 0:
            problems.append(f"{offer.offer_id} age must be nonnegative, found {offer.age}.")
        if not 0.0 <= offer.quality <= 1.0:
            problems.append(f"{offer.offer_id} quality out of bounds: {offer.quality}.")
        if not 0.0 <= offer.awareness <= 1.0:
            problems.append(f"{offer.offer_id} awareness out of bounds: {offer.awareness}.")
        if offer.price <= 0 or not math.isfinite(offer.price):
            problems.append(f"{offer.offer_id} price must be positive and finite, found {offer.price}.")
    return problems


def _run_scenario(spec: dict[str, Any]) -> dict[str, Any]:
    env = MoneyBenchEnv(seed=spec["seed"], weeks=len(spec["actions"]) + 2)
    env.reset()
    problems: list[str] = []
    step_rows: list[dict[str, Any]] = []
    previous_week: int | None = None
    for step_index, actions in enumerate(spec["actions"], start=1):
        if env.done():
            break
        before_week = env.state.week
        result = env.step(actions)
        previous_week = before_week
        problems.extend(f"step {step_index}: {problem}" for problem in _check_env_invariants(env, previous_week))
        if result.risk_penalty < 0:
            problems.append(f"step {step_index}: step risk_penalty must be nonnegative.")
        if not math.isfinite(result.profit):
            problems.append(f"step {step_index}: profit must be finite.")
        step_rows.append(
            {
                "step": step_index,
                "actions": [action.type for action in actions],
                "cash": round(env.state.cash, 2),
                "reputation": round(env.state.reputation, 3),
                "offers": len(env.state.offers),
                "customers": sum(offer.customers for offer in env.state.offers),
                "risk_penalty": result.risk_penalty,
                "bankrupt": env.state.bankrupt,
            }
        )
    return {
        "id": spec["id"],
        "seed": spec["seed"],
        "steps_executed": len(step_rows),
        "passed": not problems,
        "problems": problems,
        "final_summary": env.summary(),
        "steps": step_rows,
    }


def _task_score_check() -> dict[str, Any]:
    run = run_suite("conservative")
    scores = [float(result["score"]["score"]) for result in run["results"]]
    pass_flags_match = [
        bool(result["score"]["passed"]) == (float(result["score"]["score"]) >= 70.0)
        for result in run["results"]
    ]
    return {
        "policy": "conservative",
        "tasks": run["tasks"],
        "min_score": min(scores),
        "max_score": max(scores),
        "all_scores_bounded": all(0.0 <= score <= 100.0 for score in scores),
        "pass_flags_match_threshold": all(pass_flags_match),
    }


def build_audit() -> dict[str, Any]:
    scenarios = [_run_scenario(spec) for spec in SCENARIOS]
    task_score_check = _task_score_check()
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Deterministic simulator invariant audit for state bounds, diagnostic sanity, and task score bounds. This is not a substitute for domain validation.",
        "status": "simulator_invariants_validated_for_stress_scenarios",
        "scenarios": scenarios,
        "task_score_check": task_score_check,
        "invariants_checked": [
            "week advances monotonically until bankruptcy/done",
            "cash and profit remain finite",
            "reputation remains in [0, 1]",
            "agent capacity and cumulative revenue/API cost/funding/risk remain nonnegative",
            "offer customers and age remain nonnegative",
            "offer quality and awareness remain in [0, 1]",
            "task scores remain in [0, 100] and pass flags match the 70-point threshold",
        ],
        "claim_guardrail": "This audit checks simulator mechanics and task-score bounds only; it does not validate real-world startup dynamics or unlock hosted/local LLM result claims.",
        "summary": {
            "scenarios": len(scenarios),
            "scenarios_passed": sum(1 for row in scenarios if row["passed"]),
            "scenario_steps": sum(row["steps_executed"] for row in scenarios),
            "task_score_policy": task_score_check["policy"],
            "task_scores_bounded": task_score_check["all_scores_bounded"],
            "pass_flags_match_threshold": task_score_check["pass_flags_match_threshold"],
        },
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "simulator_invariants_validated_for_stress_scenarios":
        problems.append("Unexpected simulator invariant audit status.")
    summary = payload.get("summary", {})
    if summary.get("scenarios", 0) < 5:
        problems.append("Expected at least five stress scenarios.")
    if summary.get("scenarios") != summary.get("scenarios_passed"):
        problems.append("All stress scenarios must pass invariant checks.")
    if summary.get("scenario_steps", 0) < 10:
        problems.append("Expected at least ten executed scenario steps.")
    if summary.get("task_scores_bounded") is not True:
        problems.append("Task score check must keep all scores bounded.")
    if summary.get("pass_flags_match_threshold") is not True:
        problems.append("Task score pass flags must match the threshold.")
    if len(payload.get("invariants_checked", [])) < 6:
        problems.append("Expected at least six invariant descriptions.")
    guardrail = payload.get("claim_guardrail", "")
    if "does not validate real-world startup dynamics" not in guardrail:
        problems.append("Claim guardrail must avoid real-world validation overclaiming.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    scenario_rows = [
        [
            row["id"],
            row["seed"],
            row["steps_executed"],
            "yes" if row["passed"] else "no",
            row["final_summary"]["cash"],
            row["final_summary"]["reputation"],
            row["final_summary"]["bankrupt"],
        ]
        for row in payload["scenarios"]
    ]
    score_check = payload["task_score_check"]
    lines = [
        "# FounderBench v0.3 Simulator Invariant Audit",
        "",
        "This generated audit stress-tests simulator mechanics and task-score bounds. It is a software-validity check, not a claim that the simulator captures real startup dynamics.",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Invariants Checked",
        "",
        *[f"- {item}" for item in payload["invariants_checked"]],
        "",
        "## Stress Scenarios",
        "",
        markdown_table(["Scenario", "Seed", "Steps", "Passed", "Final Cash", "Final Reputation", "Bankrupt"], scenario_rows),
        "",
        "## Task Score Bounds",
        "",
        markdown_table(
            ["Policy", "Tasks", "Min Score", "Max Score", "Scores Bounded", "Pass Flags Match Threshold"],
            [
                [
                    score_check["policy"],
                    score_check["tasks"],
                    score_check["min_score"],
                    score_check["max_score"],
                    score_check["all_scores_bounded"],
                    score_check["pass_flags_match_threshold"],
                ]
            ],
        ),
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
        lines.append("Stress scenarios and task-score bounds satisfy the declared simulator invariants.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench simulator invariant audit artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
