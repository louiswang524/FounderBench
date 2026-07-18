from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .private_holdout_evaluator import run_private_holdout, validate_private_report


VERSION = "0.3.0"
SMOKE_SECRET = "founderbench-public-smoke-secret-not-for-evaluation"


def build_report(policy: str = "conservative", seed: int = 0) -> dict[str, Any]:
    private_report = run_private_holdout(policy, SMOKE_SECRET, audit=False, seed=seed)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "status": "smoke_test_only_not_official_holdout",
        "purpose": "Aggregate-only smoke test proving the private-holdout evaluator harness can generate and execute 20 hidden-format tasks without publishing task definitions.",
        "official_claim_guardrail": "Do not report this smoke result as an official private leaderboard, hidden holdout score, or model-comparison result.",
        "policy": policy,
        "run_seed": seed,
        "public_smoke_secret_disclosed": True,
        "secret_values_recorded": False,
        "private_report": private_report,
        "summary": {
            "private_tasks": private_report["private_tasks"],
            "private_solved": private_report["private_solved"],
            "private_solve_rate": private_report["private_solve_rate"],
            "private_average_task_score": private_report["private_average_task_score"],
            "private_invalid_actions": private_report["private_invalid_actions"],
            "private_over_budget_decisions": private_report["private_over_budget_decisions"],
            "private_provider_errors": private_report["private_provider_errors"],
            "contains_raw_private_results": "private_results" in private_report,
        },
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "smoke_test_only_not_official_holdout":
        problems.append("Holdout smoke report must be labeled smoke-only.")
    if "official private leaderboard" not in payload.get("official_claim_guardrail", ""):
        problems.append("Holdout smoke report must block official leaderboard claims.")
    if payload["summary"]["private_tasks"] != 20:
        problems.append("Holdout smoke report must execute 20 private-format tasks.")
    if payload["summary"]["contains_raw_private_results"]:
        problems.append("Holdout smoke report must not include raw private task results.")
    if payload.get("secret_values_recorded") is not False:
        problems.append("Holdout smoke report must not record secret values.")
    problems.extend(validate_private_report(payload.get("private_report", {})))
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    lines = [
        "# FounderBench Private Holdout Smoke Report",
        "",
        "This generated report is a smoke test for the private-holdout evaluator harness. It uses a disclosed public smoke secret and must not be reported as an official hidden-holdout leaderboard.",
        "",
        f"Status: `{payload['status']}`",
        "",
        f"Policy: `{payload['policy']}`",
        f"Run seed: `{payload['run_seed']}`",
        "",
        "## Claim Guardrail",
        "",
        payload["official_claim_guardrail"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Public Report Fields",
        "",
    ]
    public_fields = [
        "private_tasks",
        "private_solved",
        "private_solve_rate",
        "private_average_task_score",
        "private_provider_errors",
        "private_invalid_actions",
        "private_over_budget_decisions",
        "private_estimated_provider_cost_usd",
        "fingerprint_manifest_sha256",
    ]
    lines.extend(f"- `{field}`: {payload['private_report'].get(field)}" for field in public_fields)
    lines.extend(["", "## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The private-holdout evaluator harness executed aggregate-only smoke reporting without exposing raw private task results.")
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
    parser = argparse.ArgumentParser(description="Generate private-holdout evaluator smoke report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
