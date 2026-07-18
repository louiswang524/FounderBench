from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .provider_adapter import ProviderResponseError, classify_provider_exception, parse_provider_response
from .task_runner import run_task
from .tasks import get_task


VERSION = "0.3.0"


CASES: list[dict[str, Any]] = [
    {
        "id": "valid_minimal_do_nothing",
        "response": '{"rationale": "wait", "actions": [{"type": "do_nothing"}]}',
        "expected": "pass",
    },
    {
        "id": "invalid_json",
        "response": "not json",
        "expected": "invalid_json",
    },
    {
        "id": "invalid_root",
        "response": '["do_nothing"]',
        "expected": "invalid_response_root",
    },
    {
        "id": "missing_actions",
        "response": '{"rationale": "ok"}',
        "expected": "missing_actions",
    },
    {
        "id": "invalid_actions_type",
        "response": '{"actions": "do_nothing"}',
        "expected": "invalid_actions_type",
    },
    {
        "id": "invalid_action_schema",
        "response": '{"actions": ["do_nothing"]}',
        "expected": "invalid_action_schema",
    },
    {
        "id": "missing_action_type",
        "response": '{"actions": [{"budget": 10}]}',
        "expected": "missing_action_type",
    },
    {
        "id": "invalid_numeric_field",
        "response": '{"actions": [{"type": "do_nothing", "budget": "bad"}]}',
        "expected": "invalid_numeric_field",
    },
]


class AlwaysMalformedPolicy:
    def act(self, observation):
        raise ProviderResponseError("missing_actions", "synthetic malformed provider output")


def _case_result(case: dict[str, Any]) -> dict[str, Any]:
    try:
        actions = parse_provider_response(case["response"])
        observed = "pass"
        parsed_actions = len(actions)
    except Exception as exc:  # The contract intentionally audits categorized parser failures.
        observed = classify_provider_exception(exc)
        parsed_actions = 0
    return {
        "id": case["id"],
        "expected": case["expected"],
        "observed": observed,
        "passed": observed == case["expected"],
        "parsed_actions": parsed_actions,
    }


def build_audit() -> dict[str, Any]:
    cases = [_case_result(case) for case in CASES]
    task_result = run_task(get_task("FND-001"), AlwaysMalformedPolicy())
    diagnostics = task_result["diagnostics"]
    simulator_checks = [
        {
            "id": "malformed_provider_output_counted",
            "expected": "provider_errors_positive",
            "observed": diagnostics["provider_errors"],
            "passed": diagnostics["provider_errors"] > 0,
        },
        {
            "id": "error_category_preserved",
            "expected": "missing_actions",
            "observed": diagnostics["provider_error_categories"],
            "passed": diagnostics["provider_error_categories"].get("missing_actions", 0) > 0,
        },
        {
            "id": "malformed_output_fallback_is_diagnostic_counted",
            "expected": "provider_error_for_each_fallback_step",
            "observed": {"invalid_actions": diagnostics["invalid_actions"], "total_actions": diagnostics["total_actions"]},
            "passed": diagnostics["provider_errors"] == diagnostics["total_actions"] and diagnostics["provider_errors"] > 0,
        },
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Provider-output contract audit for hosted/local LLM submissions. This is a dry-run parser and simulator-diagnostic check, not LLM baseline evidence.",
        "status": "contract_validated_no_provider_results_claimed",
        "parser_cases": cases,
        "simulator_checks": simulator_checks,
        "claim_guardrails": [
            "This audit does not unlock hosted/local LLM comparison claims.",
            "Malformed provider outputs remain counted as benchmark outcomes through diagnostics.",
            "Evaluator code must not manually repair invalid model outputs outside the adapter/parser contract; fallback actions must remain diagnostic-counted.",
            "Provider submissions still require complete 50-task JSON outputs and founderbench.submission validation.",
        ],
        "summary": {
            "parser_cases": len(cases),
            "parser_cases_passed": sum(1 for row in cases if row["passed"]),
            "simulator_checks": len(simulator_checks),
            "simulator_checks_passed": sum(1 for row in simulator_checks if row["passed"]),
            "llm_baseline_evidence": False,
        },
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "contract_validated_no_provider_results_claimed":
        problems.append("status must keep this audit separate from provider-result evidence.")
    summary = payload.get("summary", {})
    if summary.get("parser_cases") < 8:
        problems.append("Expected at least eight parser contract cases.")
    if summary.get("parser_cases") != summary.get("parser_cases_passed"):
        problems.append("All parser contract cases must pass.")
    if summary.get("simulator_checks") != summary.get("simulator_checks_passed"):
        problems.append("All simulator diagnostic checks must pass.")
    if summary.get("llm_baseline_evidence") is not False:
        problems.append("llm_baseline_evidence must remain false.")
    guardrail_text = " ".join(payload.get("claim_guardrails", []))
    for required in ["does not unlock", "must not manually repair", "50-task"]:
        if required not in guardrail_text:
            problems.append(f"claim guardrails must include: {required}")
    observed = {row["observed"] for row in payload.get("parser_cases", [])}
    for category in {"invalid_json", "missing_actions", "invalid_numeric_field"}:
        if category not in observed:
            problems.append(f"Parser audit must cover {category}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    parser_rows = [
        [row["id"], row["expected"], row["observed"], "yes" if row["passed"] else "no", row["parsed_actions"]]
        for row in payload["parser_cases"]
    ]
    simulator_rows = [
        [row["id"], row["expected"], json.dumps(row["observed"], sort_keys=True), "yes" if row["passed"] else "no"]
        for row in payload["simulator_checks"]
    ]
    lines = [
        "# FounderBench Provider Contract Audit",
        "",
        "This generated audit checks parser and simulator-diagnostic behavior for provider outputs before hosted/local model runs are accepted. It is not LLM baseline evidence.",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Parser Cases",
        "",
        markdown_table(["Case", "Expected", "Observed", "Passed", "Parsed Actions"], parser_rows),
        "",
        "## Simulator Diagnostic Checks",
        "",
        markdown_table(["Check", "Expected", "Observed", "Passed"], simulator_rows),
        "",
        "## Claim Guardrails",
        "",
        *[f"- {item}" for item in payload["claim_guardrails"]],
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
        lines.append("Provider-output parsing and simulator diagnostics are internally consistent without claiming provider baseline evidence.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench provider contract audit artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
