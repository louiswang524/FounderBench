from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .claim_evidence import build_report as build_claim_report
from .experiment_matrix import build_matrix
from .submission_gate import build_gate


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


MODES: list[dict[str, Any]] = [
    {
        "id": "implementation_bug_passing_self_review",
        "mode": 1,
        "risk": "Analysis or simulator code has a plausible-looking bug that is accepted into the paper as a valid result.",
        "status_rule": "mitigated_by_tests_not_closed",
        "evidence_paths": [
            "work/founderbench/tests/test_founderbench.py",
            "outputs/founderbench-determinism-audit.md",
            "outputs/founderbench-reviewer-smoke.md",
            "release/founderbench/BUNDLE-INTEGRITY.md",
        ],
        "required_response": "Keep deterministic replay, bundle integrity, and full test validation in the release loop; add independent hosted-run logs before model-result claims.",
    },
    {
        "id": "hallucinated_citation",
        "mode": 2,
        "risk": "A cited reference may not exist, may be miscited, or may be used for a claim it does not support.",
        "status_rule": "citation_provenance_present",
        "evidence_paths": [
            "outputs/founderbench-references.bib",
            "outputs/founderbench-reference-provenance.json",
            "outputs/founderbench-citation-audit.md",
            "outputs/founderbench-paper-draft.md",
        ],
        "required_response": "Before submission, run an external citation verification pass over all BibTeX entries and citation contexts.",
    },
    {
        "id": "hallucinated_experimental_result",
        "mode": 3,
        "risk": "A result table or model-comparison claim could report a number that no executed run produced.",
        "status_rule": "results_traceable_but_llm_missing",
        "evidence_paths": [
            "outputs/founderbench-baseline-raw.json",
            "outputs/founderbench-paper-tables.md",
            "outputs/founderbench-model-comparison.md",
            "outputs/founderbench-claim-evidence.md",
        ],
        "required_response": "Only report deterministic baseline numbers generated from raw output; keep hosted/local LLM result claims excluded until validated provider run files exist.",
    },
    {
        "id": "shortcut_reliance",
        "mode": 4,
        "risk": "Agents or task-aware baselines may exploit public task templates or scoring shortcuts rather than robust startup decision ability.",
        "status_rule": "warning_open",
        "evidence_paths": [
            "outputs/founderbench-action-ablation.md",
            "outputs/founderbench-difficulty-calibration.md",
            "outputs/founderbench-private-holdout-evaluator-protocol.md",
            "outputs/founderbench-reviewer-risk-audit.md",
        ],
        "required_response": "Use private holdout execution and model submissions before interpreting high public-suite scores as robust agent ability.",
    },
    {
        "id": "bug_reframed_as_novel_insight",
        "mode": 5,
        "risk": "Unexpected artifacts from implementation or scoring could be narrated as scientific findings.",
        "status_rule": "claim_guarded",
        "evidence_paths": [
            "outputs/founderbench-claim-evidence.md",
            "outputs/founderbench-paper-evidence-map.md",
            "outputs/founderbench-validity-report.md",
        ],
        "required_response": "Do not frame surprising heuristic/provider behavior as a substantive insight unless raw logs, ablations, and independent reruns support it.",
    },
    {
        "id": "methodology_fabrication",
        "mode": 6,
        "risk": "The paper's methods could describe tasks, actions, experiments, or provider runs that were planned but not actually executed.",
        "status_rule": "methods_tied_to_artifacts",
        "evidence_paths": [
            "work/founderbench/SPEC.md",
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-action-semantics.md",
            "outputs/founderbench-experiment-matrix.md",
            "outputs/founderbench-provider-run-status.md",
        ],
        "required_response": "Keep planned experiments explicitly labeled as planned or missing, and update Methods only after generated artifacts prove execution.",
    },
    {
        "id": "frame_lock",
        "mode": 7,
        "risk": "The benchmark could stay locked into the early startup-profit framing even if evidence supports only a narrower controlled-decision benchmark.",
        "status_rule": "frame_guarded_but_external_validation_missing",
        "evidence_paths": [
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-human-calibration-analysis.md",
            "outputs/founderbench-submission-manifest.md",
        ],
        "required_response": "Use conservative benchmark framing until human/expert calibration and hidden holdout evidence justify broader claims.",
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


def _status_for_rule(rule: str) -> tuple[str, str, str]:
    gate = build_gate()
    matrix = build_matrix()
    claims = build_claim_report()
    unsupported = claims["summary"]["unsupported_currently"]

    if rule == "mitigated_by_tests_not_closed":
        return (
            "mitigated_not_closed",
            "blocking_warning",
            "The deterministic artifact path has tests, smoke checks, determinism audit, and bundle integrity, but independent hosted-run logs remain absent.",
        )
    if rule == "citation_provenance_present":
        return (
            "local_context_verified_external_spotcheck_required",
            "blocking_warning",
            "References, provenance, and a local citation-context audit are present; final submission still needs external citation-context spot checks against primary pages or PDFs.",
        )
    if rule == "results_traceable_but_llm_missing":
        missing = matrix["summary"]["required_missing"]
        if missing:
            return (
                "mitigated_for_reported_deterministic_results",
                "blocks_stronger_llm_claims",
                f"Deterministic results are traceable to raw runs, but {missing} required experiment groups remain missing.",
            )
        return ("clear", "not_blocking", "Required experiment groups are complete and traceable.")
    if rule == "warning_open":
        return (
            "warning_open",
            "blocks_robustness_claims",
            "Public-suite ablations exist, but hidden-holdout execution is still required to rule out public-template shortcuts.",
        )
    if rule == "claim_guarded":
        if unsupported:
            return (
                "mitigated_by_claim_guardrail",
                "not_blocking_for_current_claims",
                f"{unsupported} stronger claims are explicitly excluded until evidence exists.",
            )
        return ("clear", "not_blocking", "Claim-evidence report marks all stronger claims supported.")
    if rule == "methods_tied_to_artifacts":
        status = "not_ready" if gate["final_status"] != "ready" else "ready"
        return (
            "mitigated_by_artifact_labels",
            "blocks_submission_ready_claim" if status != "ready" else "not_blocking",
            f"The submission gate is {status}; planned provider runs remain labeled as missing or planned in generated artifacts.",
        )
    if rule == "frame_guarded_but_external_validation_missing":
        return (
            "frame_guarded_but_open",
            "blocks_external_validity_claims",
            "Validity, calibration, and submission-manifest artifacts keep the benchmark framed as controlled simulation, not real startup prediction.",
        )
    return ("unknown", "blocking_warning", "No status rule matched.")


def build_audit() -> dict[str, Any]:
    checks = []
    for mode in MODES:
        status, gate_effect, rationale = _status_for_rule(mode["status_rule"])
        evidence = [file_entry(path) for path in mode["evidence_paths"]]
        checks.append(
            {
                "mode": mode["mode"],
                "id": mode["id"],
                "risk": mode["risk"],
                "status": status,
                "gate_effect": gate_effect,
                "status_rationale": rationale,
                "evidence": evidence,
                "required_response": mode["required_response"],
            }
        )
    blocking_or_warning = [row for row in checks if row["gate_effect"] != "not_blocking" and row["gate_effect"] != "not_blocking_for_current_claims"]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "AI research failure-mode audit adapted to benchmark artifact integrity. It checks for seven failure classes: code bugs, citation hallucination, result hallucination, shortcut reliance, bug-as-insight, methodology fabrication, and frame-lock.",
        "submission_gate": build_gate()["final_status"],
        "checks": checks,
        "summary": {
            "modes": len(checks),
            "clear": sum(1 for row in checks if row["status"] == "clear"),
            "mitigated_or_guarded": sum(1 for row in checks if row["status"].startswith("mitigated") or row["status"].startswith("frame_guarded")),
            "warnings_or_blockers": len(blocking_or_warning),
            "stronger_claims_blocked": sum(1 for row in checks if row["gate_effect"].startswith("blocks_")),
        },
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["modes"] != 7:
        problems.append("Failure-mode audit must cover exactly seven modes.")
    ids = {row["id"] for row in payload["checks"]}
    for required in {"implementation_bug_passing_self_review", "hallucinated_experimental_result", "methodology_fabrication", "frame_lock"}:
        if required not in ids:
            problems.append(f"Missing failure-mode check: {required}.")
    if payload["submission_gate"] != "ready" and payload["summary"]["warnings_or_blockers"] <= 0:
        problems.append("A not-ready submission should retain warnings or blockers in the failure-mode audit.")
    for row in payload["checks"]:
        if not row.get("evidence"):
            problems.append(f"Mode {row.get('id')} lacks evidence paths.")
        if not row.get("required_response"):
            problems.append(f"Mode {row.get('id')} lacks a required response.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    check_rows = [
        [
            row["mode"],
            row["id"],
            row["status"],
            row["gate_effect"],
            row["risk"],
            row["required_response"],
        ]
        for row in payload["checks"]
    ]
    lines = [
        "# FounderBench AI Research Failure-Mode Audit",
        "",
        "This generated audit applies a seven-mode AI research failure checklist to the benchmark artifact. It is an integrity aid, not a substitute for external peer review.",
        "",
        f"Submission gate: `{payload['submission_gate']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Mode Checks",
        "",
        markdown_table(["Mode", "ID", "Status", "Gate Effect", "Risk", "Required Response"], check_rows),
        "",
        "## Evidence Details",
        "",
    ]
    for row in payload["checks"]:
        lines.extend(
            [
                f"### Mode {row['mode']}: {row['id']}",
                "",
                f"- Status: `{row['status']}`",
                f"- Gate effect: `{row['gate_effect']}`",
                f"- Rationale: {row['status_rationale']}",
                f"- Risk: {row['risk']}",
                f"- Required response: {row['required_response']}",
                "",
                "Evidence:",
            ]
        )
        lines.extend(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}" for item in row["evidence"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The failure-mode audit is internally consistent with the current evidence and submission gate.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench AI research failure-mode audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
