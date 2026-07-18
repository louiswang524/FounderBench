from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .completion_audit import build_audit as build_completion_audit
from .experiment_matrix import build_matrix
from .submission_gate import build_gate


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


RISK_SPECS: list[dict[str, Any]] = [
    {
        "id": "missing_llm_baselines",
        "reviewer_lens": "methodology",
        "severity": "critical",
        "status_rule": "llm_evidence_missing",
        "likely_objection": "The benchmark is intended to evaluate LLM startup agents, but the current artifact only contains deterministic rule baselines.",
        "evidence_paths": [
            "outputs/acceleratorbench-experiment-matrix-v0.3.md",
            "outputs/acceleratorbench-provider-run-status-v0.3.md",
            "outputs/acceleratorbench-experiment-runbook-v0.3.md",
            "outputs/acceleratorbench-model-comparison-v0.3.md",
        ],
        "required_response": "Run and validate the required hosted/local LLM baselines, then update paper tables, claim gates, and model-comparison artifacts before making model-performance claims.",
    },
    {
        "id": "synthetic_validity",
        "reviewer_lens": "domain",
        "severity": "major",
        "status_rule": "mitigated_not_closed",
        "likely_objection": "A synthetic startup simulator may not measure real startup skill or real company outcomes.",
        "evidence_paths": [
            "outputs/acceleratorbench-validity-report-v0.3.md",
            "outputs/acceleratorbench-task-provenance-v0.3.md",
            "outputs/acceleratorbench-benchmark-card.md",
            "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
        ],
        "required_response": "Frame the benchmark as a controlled decision benchmark, avoid real-world success claims, and collect expert/human-founder calibration evidence.",
    },
    {
        "id": "overclaiming_real_world_success",
        "reviewer_lens": "editorial",
        "severity": "critical",
        "status_rule": "claim_guardrail",
        "likely_objection": "The paper could overstate that high simulator profit predicts real startup profitability or durable company success.",
        "evidence_paths": [
            "outputs/acceleratorbench-claim-evidence-v0.3.md",
            "outputs/acceleratorbench-paper-evidence-map-v0.3.md",
            "outputs/acceleratorbench-submission-manifest-v0.3.md",
        ],
        "required_response": "Keep the supported wording narrow: FounderBench evaluates controlled startup-like operating decisions, not real-world startup prediction.",
    },
    {
        "id": "hidden_holdout_not_executed",
        "reviewer_lens": "anti_gaming",
        "severity": "major",
        "status_rule": "open_external",
        "likely_objection": "Public tasks and deterministic scoring can invite benchmark gaming without an executed private holdout.",
        "evidence_paths": [
            "outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md",
            "outputs/acceleratorbench-private-holdout-smoke-v0.3.md",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
            "work/moneybench/moneybench/private_holdout_evaluator.py",
            "outputs/acceleratorbench-submission-gate-v0.3.md",
        ],
        "required_response": "Have an evaluator run secret-seeded private tasks and report aggregate-only holdout results for submitted models.",
    },
    {
        "id": "heuristic_overfitting_or_hand_coding",
        "reviewer_lens": "methodology",
        "severity": "major",
        "status_rule": "partially_mitigated",
        "likely_objection": "Strong task-aware heuristics may encode benchmark-specific rules, making them look better than naive LLM calls.",
        "evidence_paths": [
            "outputs/acceleratorbench-ablation-report-v0.3.md",
            "outputs/acceleratorbench-action-ablation-v0.3.md",
            "outputs/acceleratorbench-difficulty-calibration-v0.3.md",
            "outputs/acceleratorbench-task-provenance-v0.3.md",
        ],
        "required_response": "Report task-aware heuristic results as calibration ceilings, not agent baselines, and compare against validated LLM runs plus hidden holdout results.",
    },
    {
        "id": "license_metadata_missing",
        "reviewer_lens": "reproducibility",
        "severity": "administrative_major",
        "status_rule": "owner_action_required",
        "likely_objection": "The package is not publicly reusable until final LICENSE and citation metadata are chosen.",
        "evidence_paths": [
            "outputs/acceleratorbench-license-readiness-v0.3.md",
            "outputs/acceleratorbench-release-metadata-checklist-v0.3.md",
            "outputs/acceleratorbench-submission-gate-v0.3.md",
        ],
        "required_response": "The project owner must select and commit final license and citation metadata before public release or supplementary submission.",
    },
    {
        "id": "provider_cost_reproducibility",
        "reviewer_lens": "reproducibility",
        "severity": "major",
        "status_rule": "planned_not_executed",
        "likely_objection": "Hosted API results may be hard to reproduce without exact usage, retries, prices, and provider-error accounting.",
        "evidence_paths": [
            "outputs/acceleratorbench-cost-accounting-v0.3.md",
            "outputs/acceleratorbench-provider-readiness-v0.3.md",
            "outputs/acceleratorbench-prompt-protocol-v0.3.md",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
            "outputs/acceleratorbench-provider-run-status-v0.3.md",
        ],
        "required_response": "Record token usage, provider error categories, retry policy, model identifiers, and normalized costs for each validated provider run.",
    },
    {
        "id": "human_calibration_missing",
        "reviewer_lens": "domain",
        "severity": "major",
        "status_rule": "human_calibration_missing",
        "likely_objection": "The benchmark has no included human-founder or expert calibration results showing task realism, score alignment, or gaming risks.",
        "evidence_paths": [
            "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
            "outputs/acceleratorbench-human-calibration-schema-v0.3.md",
            "outputs/acceleratorbench-human-calibration-analysis-v0.3.md",
            "outputs/acceleratorbench-human-calibration-packet-v0.3.md",
            "outputs/acceleratorbench-validity-report-v0.3.md",
        ],
        "required_response": "Collect calibration submissions, run the analyzer, and report inter-rater concerns and task revisions before strong validity claims.",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_entry(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    entry: dict[str, Any] = {"path": rel_path, "exists": path.exists()}
    if path.exists():
        entry["bytes"] = path.stat().st_size
        entry["sha256"] = sha256(path)
    return entry


def _status_for_rule(rule: str) -> tuple[str, str]:
    gate = build_gate()
    completion = build_completion_audit()
    matrix = build_matrix()
    failed_gates = {row["id"] for row in gate["gates"] if row["status"] != "pass"}
    completion_items = {row["id"]: row for row in completion["items"]}

    if rule == "llm_evidence_missing":
        missing = matrix["summary"]["required_missing"]
        if missing:
            return "open_external", f"{missing} required experiment groups are still missing."
        return "resolved", "Required experiment groups are complete."
    if rule == "claim_guardrail":
        return "mitigated_by_claim_guardrail", "Claim-evidence and paper-evidence artifacts explicitly exclude real-world success prediction."
    if rule == "open_external":
        return "open_external", "The private-holdout protocol and smoke report exist, but no evaluator-hosted official aggregate result is included."
    if rule == "owner_action_required":
        if "license_and_citation" in failed_gates:
            return "owner_action_required", "The submission gate still blocks on final license and citation metadata."
        return "resolved", "License and citation gate is passing."
    if rule == "human_calibration_missing":
        item = completion_items.get("documentation_and_accessibility", {})
        if (ROOT / "outputs" / "acceleratorbench-human-calibration-analysis-v0.3.md").exists():
            return "open_external", "Calibration protocol and analyzer exist, but the analysis records no included submissions."
        return "open_external", item.get("rationale", "No included human calibration analysis is available.")
    if rule == "planned_not_executed":
        return "planned_not_executed", "Cost and provider protocols exist; actual hosted/local runs must fill usage and cost fields."
    if rule == "partially_mitigated":
        return "partially_mitigated", "Ablations and task provenance expose heuristic behavior, but LLM and holdout evidence are still needed."
    if rule == "mitigated_not_closed":
        return "mitigated_not_closed", "Threats and task provenance are documented, but external calibration remains missing."
    return "open", "No status rule matched."


def build_audit() -> dict[str, Any]:
    risks = []
    for spec in RISK_SPECS:
        status, rationale = _status_for_rule(spec["status_rule"])
        evidence = [file_entry(path) for path in spec["evidence_paths"]]
        risks.append(
            {
                "id": spec["id"],
                "reviewer_lens": spec["reviewer_lens"],
                "severity": spec["severity"],
                "status": status,
                "status_rationale": rationale,
                "likely_objection": spec["likely_objection"],
                "required_response": spec["required_response"],
                "evidence": evidence,
            }
        )
    severity_counts = {severity: sum(1 for row in risks if row["severity"] == severity) for severity in sorted({row["severity"] for row in risks})}
    status_counts = {status: sum(1 for row in risks if row["status"] == status) for status in sorted({row["status"] for row in risks})}
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Pre-submission reviewer-risk audit. This is not peer review; it is a deterministic stress test of likely reviewer objections against current evidence.",
        "submission_gate": build_gate()["final_status"],
        "risks": risks,
        "summary": {
            "risks": len(risks),
            "critical": sum(1 for row in risks if row["severity"] == "critical"),
            "open_or_external": sum(1 for row in risks if row["status"] in {"open_external", "owner_action_required", "planned_not_executed"}),
            "severity_counts": severity_counts,
            "status_counts": status_counts,
        },
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["risks"] < 8:
        problems.append("Reviewer-risk audit should cover at least 8 likely objections.")
    if payload["summary"]["critical"] <= 0:
        problems.append("Reviewer-risk audit should include at least one critical risk.")
    ids = {row["id"] for row in payload["risks"]}
    for required in {"missing_llm_baselines", "overclaiming_real_world_success"}:
        if required not in ids:
            problems.append(f"Missing required reviewer risk: {required}.")
    if payload["submission_gate"] != "ready" and payload["summary"]["open_or_external"] <= 0:
        problems.append("A not-ready submission should retain at least one open/external reviewer risk.")
    for risk in payload["risks"]:
        if not risk.get("likely_objection"):
            problems.append(f"Risk {risk.get('id')} lacks a likely objection.")
        if not risk.get("required_response"):
            problems.append(f"Risk {risk.get('id')} lacks a required response.")
        if not risk.get("evidence"):
            problems.append(f"Risk {risk.get('id')} lacks evidence paths.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items() if not isinstance(value, dict)]
    severity_rows = [[key, value] for key, value in payload["summary"]["severity_counts"].items()]
    status_rows = [[key, value] for key, value in payload["summary"]["status_counts"].items()]
    risk_rows = [
        [
            risk["id"],
            risk["reviewer_lens"],
            risk["severity"],
            risk["status"],
            risk["likely_objection"],
            risk["required_response"],
        ]
        for risk in payload["risks"]
    ]
    lines = [
        "# FounderBench v0.3 Reviewer-Risk Audit",
        "",
        "This generated artifact is a pre-submission stress test of likely reviewer concerns. It is not a claim that peer review has occurred.",
        "",
        f"Submission gate: `{payload['submission_gate']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Severity Counts",
        "",
        markdown_table(["Severity", "Count"], severity_rows),
        "",
        "## Status Counts",
        "",
        markdown_table(["Status", "Count"], status_rows),
        "",
        "## Risk Table",
        "",
        markdown_table(["Risk", "Lens", "Severity", "Status", "Likely Objection", "Required Response"], risk_rows),
        "",
        "## Evidence Details",
        "",
    ]
    for risk in payload["risks"]:
        lines.extend(
            [
                f"### {risk['id']}",
                "",
                f"- Reviewer lens: {risk['reviewer_lens']}",
                f"- Severity: `{risk['severity']}`",
                f"- Status: `{risk['status']}`",
                f"- Status rationale: {risk['status_rationale']}",
                f"- Likely objection: {risk['likely_objection']}",
                f"- Required response: {risk['required_response']}",
                "",
                "Evidence:",
            ]
        )
        lines.extend(f"- `{row['path']}`: {'present' if row['exists'] else 'missing'}" for row in risk["evidence"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The reviewer-risk audit is internally consistent with the current submission gate and evidence state.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench reviewer-risk audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
