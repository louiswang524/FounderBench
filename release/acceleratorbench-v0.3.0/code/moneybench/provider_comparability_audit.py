from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .baseline_execution_plan import MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS, PRIMARY_TASK_COUNT, build_plan
from .cost_accounting import build_protocol as build_cost_protocol
from .prompt_protocol import build_protocol as build_prompt_protocol
from .provider_run_status import build_status as build_provider_status


VERSION = "0.3.0"


def _wrapper_by_policy(prompt: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["policy"]: row for row in prompt["provider_message_wrappers"]}


def _run_row(run: dict[str, Any], wrapper: dict[str, Any], status: dict[str, Any]) -> dict[str, Any]:
    expected_task_count = run["task_count"] == PRIMARY_TASK_COUNT
    canonical_prompt = bool(wrapper) and run["policy"] == wrapper.get("policy")
    has_validation = "moneybench.submission" in run["validation_command"]
    has_repeats = (
        len(run["repeat_outputs"]) == MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS
        and "moneybench.submission_bundle" in run["repeat_bundle_command"]
    )
    is_sc_ablation = run["policy"] == "deepseek_sc"
    decoding_role = "self_consistency_ablation" if is_sc_ablation else "primary_or_local_baseline"
    comparable_for_main_claim = (
        expected_task_count
        and canonical_prompt
        and has_validation
        and has_repeats
        and not is_sc_ablation
        and run["priority"] == "required"
    )
    return {
        "id": run["id"],
        "policy": run["policy"],
        "model_family": run["model_family"],
        "priority": run["priority"],
        "planned_status": status.get("status", "missing"),
        "task_count": run["task_count"],
        "expected_task_count": expected_task_count,
        "prompt_version": wrapper.get("policy", ""),
        "temperature": wrapper.get("temperature"),
        "self_consistency_k": wrapper.get("self_consistency_k"),
        "decoding_role": decoding_role,
        "canonical_prompt_contract": canonical_prompt,
        "validation_command_present": has_validation,
        "repeat_outputs": len(run["repeat_outputs"]),
        "repeat_bundle_command_present": has_repeats,
        "audit_command_present": "--audit" in run["audit_command"],
        "cost_fields_required": True,
        "comparable_for_main_claim": comparable_for_main_claim,
        "claim_status": "eligible_after_valid_submission" if comparable_for_main_claim else "excluded_or_ablation_until_separately_reported",
    }


def build_audit() -> dict[str, Any]:
    plan = build_plan()
    prompt = build_prompt_protocol()
    cost = build_cost_protocol()
    status = build_provider_status()
    wrappers = _wrapper_by_policy(prompt)
    status_by_id = {row["id"]: row for row in status["planned_runs"]}
    run_rows = [_run_row(run, wrappers.get(run["policy"], {}), status_by_id.get(run["id"], {})) for run in plan["runs"]]
    claim_counts = Counter(row["claim_status"] for row in run_rows)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Provider-run comparability audit for planned and completed hosted/local model baselines.",
        "status": "protocol_comparability_ready_runs_missing",
        "scope": {
            "task_count": plan["scope"]["task_count"],
            "prompt_version": prompt["prompt_version"],
            "prompt_template_sha256": prompt["prompt_template_sha256"],
            "protocol_sha256": prompt["protocol_sha256"],
            "max_actions_per_week": prompt["max_actions_per_week"],
            "minimum_repeats_for_stochastic_claims": MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS,
            "cost_usage_fields": cost["usage_fields"],
        },
        "comparability_checks": [
            "Every planned provider/local run targets the same 50 v0.3.0 task ids.",
            "Every provider uses the canonical structured-action prompt contract and parser.",
            "Every planned run has a submission validation command and repeat-bundle command.",
            "DeepSeek self-consistency k=3 is marked as a separate ablation, not a substitute for the naive baseline.",
            "Cost comparison remains unavailable unless usage metadata and evaluator price assumptions are both recorded.",
            "Provider rows remain excluded from model-performance claims until raw outputs and validation reports exist.",
        ],
        "run_rows": run_rows,
        "summary": {
            "planned_runs": len(run_rows),
            "main_claim_comparable_required_runs": sum(1 for row in run_rows if row["comparable_for_main_claim"]),
            "self_consistency_ablations": sum(1 for row in run_rows if row["decoding_role"] == "self_consistency_ablation"),
            "valid_run_outputs": status["summary"]["valid_runs"],
            "required_missing_or_invalid": status["summary"]["required_missing_or_invalid"],
            "claim_status_counts": dict(sorted(claim_counts.items())),
            "ready_for_hosted_llm_comparison": False if status["summary"]["required_missing_or_invalid"] else status["summary"]["ready_for_llm_claims"],
        },
        "claim_guardrails": [
            "This audit establishes protocol comparability, not completed hosted/local model evidence.",
            "Single-run provider results are preliminary unless the statistical protocol and repeated-run policy allow stronger wording.",
            "DeepSeek self-consistency k=3 is an ablation row and must not replace the naive DeepSeek baseline.",
            "Missing or invalid provider outputs remain excluded from model-performance claims.",
        ],
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "protocol_comparability_ready_runs_missing":
        problems.append("Comparability audit status must not imply completed provider evidence.")
    if payload["scope"]["task_count"] != PRIMARY_TASK_COUNT:
        problems.append("Comparability audit must target the full 50-task suite.")
    if payload["scope"]["minimum_repeats_for_stochastic_claims"] != MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS:
        problems.append("Repeat policy does not match baseline execution plan.")
    if payload["summary"]["planned_runs"] < 5:
        problems.append("Expected hosted/local planned runs plus self-consistency ablation.")
    if payload["summary"]["main_claim_comparable_required_runs"] < 4:
        problems.append("Expected at least four required main-claim-comparable planned runs.")
    if payload["summary"]["self_consistency_ablations"] != 1:
        problems.append("Expected exactly one self-consistency ablation row.")
    if payload["summary"]["valid_run_outputs"] == 0 and payload["summary"]["ready_for_hosted_llm_comparison"]:
        problems.append("Hosted LLM comparison cannot be ready without valid provider outputs.")
    for row in payload["run_rows"]:
        if not row["expected_task_count"]:
            problems.append(f"{row['id']} does not target the expected task count.")
        if not row["canonical_prompt_contract"]:
            problems.append(f"{row['id']} lacks canonical prompt contract.")
        if not row["validation_command_present"]:
            problems.append(f"{row['id']} lacks submission validation command.")
        if row["policy"] == "deepseek_sc" and row["claim_status"] != "excluded_or_ablation_until_separately_reported":
            problems.append("DeepSeek self-consistency must remain an ablation claim row.")
    if not any("not completed hosted/local model evidence" in item for item in payload["claim_guardrails"]):
        problems.append("Claim guardrails must distinguish protocol comparability from completed evidence.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    scope_rows = [[key, value] for key, value in payload["scope"].items()]
    run_rows = [
        [
            row["id"],
            row["policy"],
            row["model_family"],
            row["priority"],
            row["planned_status"],
            row["task_count"],
            row["temperature"],
            row["self_consistency_k"],
            row["decoding_role"],
            row["comparable_for_main_claim"],
            row["claim_status"],
        ]
        for row in payload["run_rows"]
    ]
    lines = [
        "# FounderBench v0.3 Provider Comparability Audit",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Scope",
        "",
        markdown_table(["Field", "Value"], scope_rows),
        "",
        "## Comparability Checks",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["comparability_checks"])
    lines.extend(
        [
            "",
            "## Summary",
            "",
            markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
            "",
            "## Run Rows",
            "",
            markdown_table(
                ["ID", "Policy", "Family", "Priority", "Current Status", "Tasks", "Temp", "SC k", "Role", "Main Comparable", "Claim Status"],
                run_rows,
            ),
            "",
            "## Claim Guardrails",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(["", "## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The planned provider/local run protocol is comparable, while missing outputs remain excluded from model-performance claims.")
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
    parser = argparse.ArgumentParser(description="Generate provider comparability audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
