from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .claim_evidence import build_report as build_claim_report
from .completion_audit import build_audit as build_completion_audit
from .experiment_matrix import build_matrix
from .submission_gate import build_gate


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


CORE_REVIEW_PATHS = [
    "outputs/acceleratorbench-benchmark-card.md",
    "outputs/acceleratorbench-task-manifest-v0.3.json",
    "outputs/acceleratorbench-task-coverage-v0.3.md",
    "outputs/acceleratorbench-metrics-and-evaluation.md",
    "outputs/acceleratorbench-baseline-analysis-v0.3.md",
    "outputs/acceleratorbench-model-comparison-v0.3.md",
    "outputs/acceleratorbench-paper-tables-v0.3.md",
    "outputs/acceleratorbench-validity-report-v0.3.md",
    "outputs/acceleratorbench-claim-evidence-v0.3.md",
    "outputs/acceleratorbench-submission-gate-v0.3.md",
    "outputs/acceleratorbench-completion-audit-v0.3.md",
    "outputs/acceleratorbench-reviewer-index-v0.3.md",
    "release/acceleratorbench-v0.3.0/SHA256SUMS.json",
    "release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md",
]


REPRODUCTION_COMMANDS = [
    {"purpose": "Regenerate generated artifacts", "cwd": "work/moneybench", "command": "python -m moneybench.release regenerate"},
    {"purpose": "Validate generated artifacts and tests", "cwd": "work/moneybench", "command": "python -m moneybench.release validate"},
    {"purpose": "Build supplementary release bundle", "cwd": "work/moneybench", "command": "python -m moneybench.release bundle"},
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


def _supported_claim_rows(claims: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": row["id"],
            "status": row["status"],
            "permitted_wording": row["permitted_wording"],
            "evidence_paths": [item["path"] for item in row.get("evidence", []) if item.get("exists")],
        }
        for row in claims["claims"]
        if row["status"] == "supported"
    ]


def _excluded_claim_rows(claims: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": row["id"],
            "status": row["status"],
            "current_wording": row["permitted_wording"],
            "avoid_wording": row["avoid_wording"],
            "missing_evidence": [item["path"] for item in row.get("missing", []) if not item.get("exists")],
        }
        for row in claims["claims"]
        if row["status"] != "supported"
    ]


def build_manifest() -> dict[str, Any]:
    gate = build_gate()
    completion = build_completion_audit()
    claims = build_claim_report()
    matrix = build_matrix()
    core_files = [file_entry(path) for path in CORE_REVIEW_PATHS]
    failed_gates = [row for row in gate["gates"] if row["status"] != "pass"]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Compact submission manifest for reviewers: included evidence, excluded claims, reproduction commands, and readiness status.",
        "readiness": {
            "submission_gate": gate["final_status"],
            "completion_claim": completion["completion_claim"],
            "ready_for_publication": gate["final_status"] == "ready" and completion["completion_claim"] == "complete",
            "failed_gates": [row["id"] for row in failed_gates],
            "required_experiments_missing": matrix["summary"]["required_missing"],
        },
        "included_evidence_summary": {
            "task_suite": "50 fixed public v0.3.0 startup tasks across 10 families.",
            "simulator": "Deterministic seeded startup simulator with 13 structured business actions and an 8-market catalog.",
            "metrics": "Bounded 0-100 task score, solve rate, diagnostics, sensitivity analysis, paired statistics, and pre-specified comparison protocol.",
            "baselines": "Random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks with ablations.",
            "reproducibility": "Reviewer smoke test, reproducibility manifest, determinism audit, release checksum manifest, and bundle integrity report.",
        },
        "core_review_files": core_files,
        "supported_claims": _supported_claim_rows(claims),
        "excluded_or_not_yet_supported_claims": _excluded_claim_rows(claims),
        "reproduction_commands": REPRODUCTION_COMMANDS,
        "remaining_work": [
            {"gate": row["id"], "blocker": row["blocker"], "evidence": row["evidence"]}
            for row in failed_gates
        ],
        "summary": {
            "core_review_files": len(core_files),
            "core_review_files_present": sum(1 for row in core_files if row["exists"]),
            "supported_claims": len(_supported_claim_rows(claims)),
            "excluded_or_not_yet_supported_claims": len(_excluded_claim_rows(claims)),
            "failed_gates": len(failed_gates),
        },
    }


def validate_manifest(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["core_review_files"] != payload["summary"]["core_review_files_present"]:
        problems.append("All core review files must be present.")
    if payload["readiness"]["submission_gate"] != "ready" and not payload["remaining_work"]:
        problems.append("A not-ready submission manifest must list remaining work.")
    if payload["readiness"]["ready_for_publication"] and payload["remaining_work"]:
        problems.append("A ready publication manifest cannot list remaining work.")
    if payload["summary"]["supported_claims"] <= 0:
        problems.append("Submission manifest should include at least one supported claim.")
    if payload["summary"]["excluded_or_not_yet_supported_claims"] <= 0 and payload["readiness"]["submission_gate"] != "ready":
        problems.append("A not-ready submission manifest should name excluded or unsupported claims.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    readiness_rows = [[key, value] for key, value in payload["readiness"].items()]
    evidence_rows = [[key, value] for key, value in payload["included_evidence_summary"].items()]
    core_rows = [
        [row["path"], "yes" if row["exists"] else "missing", row.get("bytes", "")]
        for row in payload["core_review_files"]
    ]
    supported_rows = [
        [row["id"], row["permitted_wording"], ", ".join(f"`{path}`" for path in row["evidence_paths"][:4])]
        for row in payload["supported_claims"]
    ]
    excluded_rows = [
        [row["id"], row["current_wording"], row["avoid_wording"], ", ".join(f"`{path}`" for path in row["missing_evidence"])]
        for row in payload["excluded_or_not_yet_supported_claims"]
    ]
    command_rows = [[row["purpose"], row["cwd"], f"`{row['command']}`"] for row in payload["reproduction_commands"]]
    remaining_rows = [
        [row["gate"], row["blocker"], ", ".join(f"`{path}`" for path in row["evidence"])]
        for row in payload["remaining_work"]
    ]
    lines = [
        "# FounderBench v0.3 Submission Manifest",
        "",
        "This generated manifest is a compact reviewer-facing map of what the current submission includes, what it supports, and what it intentionally does not claim yet.",
        "",
        "## Readiness",
        "",
        markdown_table(["Field", "Value"], readiness_rows),
        "",
        "## Included Evidence Summary",
        "",
        markdown_table(["Area", "Included Evidence"], evidence_rows),
        "",
        "## Core Review Files",
        "",
        markdown_table(["Path", "Present", "Bytes"], core_rows),
        "",
        "## Supported Claims",
        "",
    ]
    if supported_rows:
        lines.append(markdown_table(["Claim", "Permitted Wording", "Evidence"], supported_rows))
    else:
        lines.append("No supported claims are currently listed.")
    lines.extend(["", "## Excluded Or Not Yet Supported Claims", ""])
    if excluded_rows:
        lines.append(markdown_table(["Claim", "Current Wording", "Blocked Wording", "Missing Evidence"], excluded_rows))
    else:
        lines.append("No excluded claims are currently listed.")
    lines.extend(
        [
            "",
            "## Reproduction Commands",
            "",
            markdown_table(["Purpose", "Working Directory", "Command"], command_rows),
            "",
            "## Remaining Work",
            "",
        ]
    )
    if remaining_rows:
        lines.append(markdown_table(["Gate", "Blocker", "Evidence"], remaining_rows))
    else:
        lines.append("No remaining gate blockers are listed.")
    lines.extend(["", "## Validation", ""])
    problems = validate_manifest(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The submission manifest is internally consistent with the current gate, completion audit, and claim-evidence report.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(json_output: Path, markdown_output: Path) -> None:
    payload = build_manifest()
    problems = validate_manifest(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate compact FounderBench submission manifest.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_manifest(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
