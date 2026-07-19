from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .claim_evidence import build_report as build_claim_report
from .experiment_matrix import build_matrix
from .license_readiness import build_report as build_license_report
from .provider_readiness import readiness_matrix
from .submission_gate import build_gate


VERSION = "0.3.0"


def _missing_required_experiments(experiments: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        row
        for row in experiments["experiments"]
        if row["priority"].startswith("required") and row["status"] != "complete"
    ]


def _provider_steps(providers: dict[str, Any]) -> list[dict[str, Any]]:
    steps = []
    for row in providers["providers"]:
        if row["ready_without_secrets_exposed"]:
            continue
        missing_env = [key for key, value in row["env_status"].items() if value == "missing"]
        steps.append(
            {
                "id": f"configure_{row['policy']}",
                "gate": "provider_run_readiness",
                "owner": "evaluator",
                "priority": "required" if row["policy"] in {"deepseek", "anthropic", "gemini", "llm"} else "recommended",
                "status": "blocked_on_environment",
                "action": f"Configure provider environment for {row['provider']}.",
                "missing_inputs": missing_env,
                "commands": [row["run_command"], row["audit_command"], row["validation_command"]],
                "expected_outputs": [row["run_command"].split("--output ", 1)[1].split(" --", 1)[0]],
                "claim_impact": "Required before hosted/local LLM comparison claims can be made.",
            }
        )
    return steps


def _experiment_steps(experiments: dict[str, Any]) -> list[dict[str, Any]]:
    steps = []
    for row in _missing_required_experiments(experiments):
        steps.append(
            {
                "id": f"complete_{row['id']}",
                "gate": "required_experiments",
                "owner": "evaluator",
                "priority": row["priority"],
                "status": row["status"],
                "action": row["description"],
                "missing_inputs": row["missing_paths"],
                "commands": row["commands"],
                "expected_outputs": row["evidence_paths"],
                "claim_impact": row["paper_use"],
            }
        )
    return steps


def _claim_steps(claims: dict[str, Any]) -> list[dict[str, Any]]:
    steps = []
    for row in claims["claims"]:
        if row["status"] != "unsupported_currently":
            continue
        missing = [item["path"] for item in row.get("missing", []) if not item["exists"]]
        if not missing:
            continue
        steps.append(
            {
                "id": f"support_claim_{row['id']}",
                "gate": "claim_evidence_alignment",
                "owner": "paper_author",
                "priority": "required_for_stronger_claim",
                "status": "unsupported_currently",
                "action": f"Either collect evidence for `{row['id']}` or keep paper wording conservative.",
                "missing_inputs": missing,
                "commands": [],
                "expected_outputs": missing,
                "claim_impact": f"Permitted wording now: {row['permitted_wording']}",
            }
        )
    return steps


def _license_steps(license_report: dict[str, Any]) -> list[dict[str, Any]]:
    if license_report["summary"]["release_ready"]:
        return []
    return [
        {
            "id": f"finalize_{decision['id']}",
            "gate": "license_and_citation",
            "owner": "project_owner",
            "priority": "required",
            "status": "owner_action_required",
            "action": decision["decision"],
            "missing_inputs": decision["target_files"],
            "commands": ["python -m founderbench.release regenerate", "python -m founderbench.release validate"],
            "expected_outputs": decision["target_files"],
            "claim_impact": decision["why_it_matters"],
        }
        for decision in license_report["required_decisions"]
    ]


def build_plan() -> dict[str, Any]:
    gate = build_gate()
    experiments = build_matrix()
    providers = readiness_matrix()
    claims = build_claim_report()
    license_report = build_license_report()
    steps = [
        *_experiment_steps(experiments),
        *_provider_steps(providers),
        *_claim_steps(claims),
        *_license_steps(license_report),
    ]
    unique_steps = []
    seen = set()
    for step in steps:
        if step["id"] in seen:
            continue
        seen.add(step["id"])
        unique_steps.append(step)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Reviewer-facing action plan for clearing the remaining FounderBench submission gates.",
        "submission_gate_status": gate["final_status"],
        "summary": {
            "steps": len(unique_steps),
            "required_steps": sum(1 for step in unique_steps if step["priority"].startswith("required")),
            "owner_action_steps": sum(1 for step in unique_steps if step["owner"] == "project_owner"),
            "provider_environment_steps": sum(1 for step in unique_steps if step["gate"] == "provider_run_readiness"),
            "claim_alignment_steps": sum(1 for step in unique_steps if step["gate"] == "claim_evidence_alignment"),
            "ready_for_submission": gate["final_status"] == "ready",
        },
        "steps": unique_steps,
        "gate_snapshot": {
            "failed_gates": [row["id"] for row in gate["gates"] if row["status"] != "pass"],
            "gates": gate["gates"],
        },
    }


def validate_plan(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["submission_gate_status"] == "not_ready" and not payload["steps"]:
        problems.append("A not_ready gate must have action-plan steps.")
    if payload["summary"]["ready_for_submission"] and payload["steps"]:
        problems.append("ready_for_submission should not have remaining action-plan steps.")
    for step in payload["steps"]:
        for field in ["id", "gate", "owner", "priority", "status", "action", "claim_impact"]:
            if field not in step:
                problems.append(f"Step is missing {field}.")
        if step["priority"].startswith("required") and not step["expected_outputs"]:
            problems.append(f"Required step {step['id']} must name expected outputs.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            step["id"],
            step["gate"],
            step["owner"],
            step["priority"],
            step["status"],
            step["action"],
        ]
        for step in payload["steps"]
    ]
    lines = [
        "# FounderBench Submission Action Plan",
        "",
        payload["purpose"],
        "",
        f"Submission gate status: `{payload['submission_gate_status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Action Steps",
        "",
    ]
    if rows:
        lines.append(markdown_table(["ID", "Gate", "Owner", "Priority", "Status", "Action"], rows))
    else:
        lines.append("No action steps remain.")
    lines.extend(["", "## Step Details", ""])
    for step in payload["steps"]:
        lines.extend(
            [
                f"### {step['id']}",
                "",
                f"- Gate: `{step['gate']}`",
                f"- Owner: `{step['owner']}`",
                f"- Claim impact: {step['claim_impact']}",
                "- Missing inputs/outputs:",
            ]
        )
        lines.extend(f"  - `{item}`" for item in step["missing_inputs"])
        if step["commands"]:
            lines.extend(["- Commands:", "```powershell", *step["commands"], "```"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_plan(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The action plan is internally consistent with the current submission gate.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_plan(json_output: Path, markdown_output: Path) -> None:
    payload = build_plan()
    problems = validate_plan(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate submission action plan from current gate and evidence state.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_plan(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
