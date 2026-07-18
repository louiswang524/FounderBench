from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


def build_policy() -> dict[str, Any]:
    tiers = [
        {
            "tier": "public_open",
            "status": "active_for_current release",
            "eligible_inputs": "Validated 50-task public_dev/public_test submissions.",
            "ranking_metric": "average_task_score",
            "secondary_ordering": ["solve_rate", "provider_errors ascending", "invalid_actions ascending", "estimated_provider_cost_usd when available"],
            "claim_scope": "Visible public benchmark score; not hidden, private, or contamination-free.",
        },
        {
            "tier": "public_repeated",
            "status": "supported_when_repeat_bundle_validates",
            "eligible_inputs": "Validated repeated-run bundle with unique policy/run_seed identities.",
            "ranking_metric": "mean average_task_score across submitted runs",
            "secondary_ordering": ["mean solve_rate", "score confidence interval", "diagnostic failure rates"],
            "claim_scope": "Stochastic public-run estimate; still visible public tasks.",
        },
        {
            "tier": "private_holdout",
            "status": "protocol_only_not_executed_current release",
            "eligible_inputs": "Evaluator-hosted aggregate private report generated from secret-held private tasks.",
            "ranking_metric": "private_average_task_score",
            "secondary_ordering": ["private_solve_rate", "private_provider_errors ascending", "private_invalid_actions ascending"],
            "claim_scope": "Hidden-suite score only after official evaluator execution; no such leaderboard is included in current release.",
        },
    ]
    acceptance_rules = [
        "Submission must pass `python -m founderbench.submission` with exactly 50 public task results unless it is an evaluator-host private report.",
        "Run JSON must report benchmark_version 0.3.0, both public splits, required diagnostics, provider-error categories, and run_seed when used for repeated runs.",
        "Provider errors, invalid actions, bankruptcies, over-budget decisions, and timeouts remain in the denominator.",
        "Hosted/local provider rows are excluded until the raw run and submission report both exist and validate.",
        "Model submitters must disclose prompt/agent tuning on public tasks and whether the submitted model was trained or fine-tuned on released tasks.",
    ]
    rejection_rules = [
        "Missing or extra public task ids.",
        "Manual repair of model outputs outside the adapter/parser contract.",
        "Dropped failed tasks or omitted provider-error diagnostics.",
        "Duplicate policy/run_seed identities in a repeated-run bundle.",
        "Unredacted secrets in public audit traces.",
        "Claims that public_test is hidden, private, unseen, or contamination-free.",
    ]
    reporting_fields = [
        "model/provider/name and version",
        "policy id and adapter commit/source state",
        "prompt/protocol version and hashes",
        "task count and split visibility",
        "run_seed or repeated-run bundle summary",
        "average_task_score, solved, solve_rate, and family/split summaries",
        "provider errors, invalid actions, over-budget decisions, timeouts, and parser categories",
        "token usage and estimated provider cost when available",
        "audit trace availability and redaction status",
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Leaderboard and model-reporting policy for public submissions, repeated runs, and future private holdout evaluation.",
        "status": "public_leaderboard_policy_ready_private_leaderboard_not_executed",
        "leaderboard_tiers": tiers,
        "acceptance_rules": acceptance_rules,
        "rejection_rules": rejection_rules,
        "reporting_fields": reporting_fields,
        "claim_guardrails": [
            "Do not merge public and private results into one leaderboard without labeling tiers.",
            "Do not treat task-aware heuristic rows as LLM-agent baselines.",
            "Do not use public leaderboard rows to claim hidden-suite robustness.",
            "Do not rank missing or invalid provider submissions.",
        ],
        "summary": {
            "tiers": len(tiers),
            "public_tier_active": True,
            "private_leaderboard_included": False,
            "acceptance_rules": len(acceptance_rules),
            "rejection_rules": len(rejection_rules),
            "reporting_fields": len(reporting_fields),
        },
    }


def validate_policy(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "public_leaderboard_policy_ready_private_leaderboard_not_executed":
        problems.append("status must keep private leaderboard non-execution explicit.")
    summary = payload.get("summary", {})
    if summary.get("tiers", 0) < 3:
        problems.append("Expected public, repeated, and private leaderboard tiers.")
    if summary.get("public_tier_active") is not True:
        problems.append("Public tier should be active.")
    if summary.get("private_leaderboard_included") is not False:
        problems.append("Private leaderboard must not be included for current release.")
    if summary.get("acceptance_rules", 0) < 5:
        problems.append("Expected at least five acceptance rules.")
    if summary.get("rejection_rules", 0) < 5:
        problems.append("Expected at least five rejection rules.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["average_task_score", "public_test", "private", "run_seed", "manual repair"]:
        if required not in text:
            problems.append(f"Policy must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    tier_rows = [
        [
            row["tier"],
            row["status"],
            row["eligible_inputs"],
            row["ranking_metric"],
            row["claim_scope"],
        ]
        for row in payload["leaderboard_tiers"]
    ]
    lines = [
        "# FounderBench Leaderboard Policy",
        "",
        "This generated policy defines how public model submissions, repeated runs, and future private-holdout reports should be accepted, ranked, reported, or rejected.",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Leaderboard Tiers",
        "",
        markdown_table(["Tier", "Status", "Eligible Inputs", "Ranking Metric", "Claim Scope"], tier_rows),
        "",
        "## Acceptance Rules",
        "",
        *[f"- {item}" for item in payload["acceptance_rules"]],
        "",
        "## Rejection Rules",
        "",
        *[f"- {item}" for item in payload["rejection_rules"]],
        "",
        "## Reporting Fields",
        "",
        *[f"- `{item}`" for item in payload["reporting_fields"]],
        "",
        "## Claim Guardrails",
        "",
        *[f"- {item}" for item in payload["claim_guardrails"]],
        "",
        "## Validation",
        "",
    ]
    problems = validate_policy(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("Leaderboard policy is internally consistent and keeps public and private result tiers separate.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_policy(json_output: Path, markdown_output: Path) -> None:
    payload = build_policy()
    problems = validate_policy(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench leaderboard policy artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_policy(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
