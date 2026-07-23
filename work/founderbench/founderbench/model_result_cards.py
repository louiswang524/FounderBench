from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .leaderboard import summarize
from .paper_tables import OUTPUTS, PROVIDER_RUNS, ROOT, load_runs, provider_status
from .submission import validate_run


VERSION = "0.3.0"


def _deterministic_card(run: dict[str, Any]) -> dict[str, Any]:
    summary = summarize(run)
    diagnostics = run.get("diagnostics", {})
    validation_problems = validate_run(run)
    return {
        "card_type": "validated_run",
        "policy": summary["policy"],
        "benchmark_version": run.get("benchmark_version", VERSION),
        "run_seed": run.get("run_seed"),
        "status": "valid" if not validation_problems else "invalid",
        "claim_eligibility": "deterministic_baseline_claims_only",
        "tasks": summary["tasks"],
        "solved": summary["solved"],
        "solve_rate": summary["solve_rate"],
        "average_task_score": summary["average_task_score"],
        "public_dev_score": summary["public_dev_score"],
        "public_test_score": summary["public_test_score"],
        "provider_errors": summary["provider_errors"],
        "invalid_actions": summary["invalid_actions"],
        "over_budget_decisions": summary["over_budget_decisions"],
        "provider_total_tokens": diagnostics.get("provider_total_tokens", 0),
        "estimated_provider_cost_usd": diagnostics.get("estimated_provider_cost_usd", 0.0),
        "provider_error_categories": diagnostics.get("provider_error_categories", {}),
        "validation_problems": validation_problems,
        "paper_use": "May be used for deterministic non-LLM baseline calibration. Do not describe as hosted LLM evidence.",
    }


def _provider_card(status: dict[str, Any]) -> dict[str, Any]:
    card = {
        "card_type": "planned_provider_run",
        "id": status["id"],
        "policy": status["policy"],
        "model": status.get("label", status["policy"]),
        "family": status["family"],
        "status": status["status"],
        "claim_eligibility": "excluded_until_validated",
        "evidence_path": status.get("evidence_path", ""),
        "evidence_kind": status.get("evidence_kind", ""),
        "runs": status.get("runs", 0),
        "submission_report_exists": status.get("submission_report_exists", False),
        "repeat_bundle_report_exists": status.get("repeat_bundle_report_exists", False),
        "validation_problems": status.get("problems", []),
        "paper_use": "Excluded from model-performance claims until raw run or repeat bundle exists and the submission report passes.",
    }
    if status["status"] == "valid":
        card.update(
            {
                "claim_eligibility": "eligible_for_provider_tables",
                "tasks": status.get("tasks"),
                "solved": status.get("solved"),
                "solve_rate": status.get("solve_rate"),
                "average_task_score": status.get("average_task_score"),
                "repeat_summary": status.get("repeat_summary", {}),
                "paper_use": "Eligible for provider-result tables, subject to the statistical protocol and claim-evidence gates.",
            }
        )
    return card


def build_cards(raw_path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> dict[str, Any]:
    deterministic_runs = load_runs(raw_path)
    deterministic_cards = [_deterministic_card(run) for run in deterministic_runs]
    provider_cards = [_provider_card(provider_status(spec)) for spec in PROVIDER_RUNS]
    valid_provider_cards = [card for card in provider_cards if card["status"] == "valid"]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Reviewer-facing result cards for deterministic baselines and provider submissions. Cards summarize validity, task coverage, diagnostics, cost fields, and paper-claim eligibility.",
        "source_files": {
            "deterministic_raw": str(raw_path.relative_to(ROOT)),
            "planned_provider_specs": [row["path"] for row in PROVIDER_RUNS],
        },
        "summary": {
            "deterministic_cards": len(deterministic_cards),
            "provider_candidate_cards": len(provider_cards),
            "valid_provider_cards": len(valid_provider_cards),
            "hosted_llm_claims_ready": len([card for card in valid_provider_cards if card.get("family") == "hosted_llm"]) >= 3,
            "open_source_claim_ready": any(card["policy"] == "llm" and card["status"] == "valid" for card in provider_cards),
        },
        "claim_guardrails": [
            "Deterministic baseline cards are not hosted LLM evidence.",
            "Provider cards marked missing or invalid must be excluded from model-performance claims.",
            "Provider cards become paper-eligible only after the raw submission and validation report both exist and pass.",
            "Cost fields are reportable only when provider usage metadata and price assumptions are available.",
        ],
        "deterministic_cards": deterministic_cards,
        "provider_cards": provider_cards,
    }


def validate_cards(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["deterministic_cards"] < 4:
        problems.append("Expected at least four deterministic baseline cards.")
    if payload["summary"]["provider_candidate_cards"] != len(PROVIDER_RUNS):
        problems.append("Provider cards do not cover all planned provider runs.")
    if payload["summary"]["valid_provider_cards"] == 0 and payload["summary"]["hosted_llm_claims_ready"]:
        problems.append("Hosted LLM claims cannot be ready without valid provider cards.")
    for card in payload["deterministic_cards"]:
        if card["status"] != "valid":
            problems.append(f"{card['policy']} deterministic card is not valid.")
        if card["tasks"] != 50:
            problems.append(f"{card['policy']} card should cover 50 tasks.")
        if card["claim_eligibility"] != "deterministic_baseline_claims_only":
            problems.append(f"{card['policy']} has wrong claim eligibility.")
    for card in payload["provider_cards"]:
        if card["status"] != "valid" and card["claim_eligibility"] != "excluded_until_validated":
            problems.append(f"{card['policy']} invalid/missing provider card must be excluded.")
    if not any("Provider cards marked missing or invalid" in item for item in payload["claim_guardrails"]):
        problems.append("Provider exclusion guardrail is required.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    deterministic_rows = [
        [
            card["policy"],
            card["status"],
            card["tasks"],
            card["solved"],
            f"{card['solve_rate']:.2f}",
            f"{card['average_task_score']:.2f}",
            f"{card['public_dev_score']:.2f}",
            f"{card['public_test_score']:.2f}",
            card["provider_errors"],
            card["invalid_actions"],
            card["over_budget_decisions"],
            card["provider_total_tokens"],
            f"{float(card['estimated_provider_cost_usd']):.4f}",
            card["claim_eligibility"],
        ]
        for card in payload["deterministic_cards"]
    ]
    provider_rows = [
        [
            card["id"],
            card["policy"],
            card["model"],
            card["family"],
            card["status"],
            card["runs"],
            card["evidence_kind"],
            card["submission_report_exists"],
            card["repeat_bundle_report_exists"],
            card["claim_eligibility"],
            "; ".join(card["validation_problems"][:2]),
        ]
        for card in payload["provider_cards"]
    ]
    lines = [
        "# FounderBench Model Result Cards",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Claim Guardrails",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(
        [
            "",
            "## Deterministic Baseline Cards",
            "",
            markdown_table(
                [
                    "Policy",
                    "Status",
                    "Tasks",
                    "Solved",
                    "Solve Rate",
                    "Avg Score",
                    "Public Dev",
                    "Public Test",
                    "Provider Errors",
                    "Invalid Actions",
                    "Over-Budget",
                    "Provider Tokens",
                    "Cost USD",
                    "Claim Eligibility",
                ],
                deterministic_rows,
            ),
            "",
            "## Planned Provider Cards",
            "",
            markdown_table(
                [
                    "ID",
                    "Policy",
                    "Model",
                    "Family",
                    "Status",
                    "Runs",
                    "Evidence",
                    "Report",
                    "Repeat Report",
                    "Claim Eligibility",
                    "Problems",
                ],
                provider_rows,
            ),
            "",
            "## Validation",
            "",
        ]
    )
    problems = validate_cards(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("Result cards are internally consistent. Missing provider cards remain excluded from model-performance claims.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench model result cards.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_cards(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
