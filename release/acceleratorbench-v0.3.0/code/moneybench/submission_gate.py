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
from .publication_audit import audit


VERSION = "0.3.0"


def gate_status(name: str, passed: bool, evidence: list[str], blocker: str = "") -> dict[str, Any]:
    return {
        "id": name,
        "status": "pass" if passed else "fail",
        "evidence": evidence,
        "blocker": blocker,
    }


def build_gate() -> dict[str, Any]:
    publication = audit()
    experiments = build_matrix()
    license_report = build_license_report()
    providers = readiness_matrix()
    claims = build_claim_report()

    publication_ready = publication["summary"]["missing"] == 0 and publication["summary"]["incomplete"] == 0
    required_experiments_ready = experiments["summary"]["required_missing"] == 0
    license_ready = bool(license_report["summary"]["release_ready"])
    providers_ready = providers["ready_count"] >= 3
    claim_ready = claims["summary"]["unsupported_currently"] == 0
    core_ready_ids = {
        "completed_artifact",
        "metrics_protocol",
        "heuristic_baselines",
        "provider_adapters",
        "auditability",
        "private_holdout_protocol",
    }
    completed_core = {
        item["id"]
        for item in publication["items"]
        if item["id"] in core_ready_ids and item["status"] == "complete"
    }
    artifact_ready = core_ready_ids <= completed_core

    gates = [
        gate_status(
            "artifact_and_documentation",
            artifact_ready,
            ["outputs/acceleratorbench-publication-audit-v0.3.md", "release/acceleratorbench-v0.3.0/SHA256SUMS.json"],
            "" if artifact_ready else "Core artifact/documentation evidence is incomplete.",
        ),
        gate_status(
            "required_experiments",
            required_experiments_ready,
            ["outputs/acceleratorbench-experiment-matrix-v0.3.md"],
            "" if required_experiments_ready else f"{experiments['summary']['required_missing']} required experiment groups are missing.",
        ),
        gate_status(
            "provider_run_readiness",
            providers_ready,
            ["outputs/acceleratorbench-provider-readiness-v0.3.md"],
            "" if providers_ready else f"Only {providers['ready_count']}/{providers['provider_count']} provider configurations are ready.",
        ),
        gate_status(
            "claim_evidence_alignment",
            claim_ready,
            ["outputs/acceleratorbench-claim-evidence-v0.3.md"],
            "" if claim_ready else f"{claims['summary']['unsupported_currently']} stronger claims remain unsupported by current evidence.",
        ),
        gate_status(
            "license_and_citation",
            license_ready,
            ["outputs/acceleratorbench-license-readiness-v0.3.md", "work/moneybench/CITATION.cff", "work/moneybench/LICENSE-TODO.md"],
            "" if license_ready else "License/citation metadata is not public-release ready.",
        ),
    ]
    final_ready = all(gate["status"] == "pass" for gate in gates)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Top-level submission gate combining artifact, experiment, provider, claim, and license readiness.",
        "final_status": "ready" if final_ready else "not_ready",
        "summary": {
            "gates": len(gates),
            "pass": sum(1 for gate in gates if gate["status"] == "pass"),
            "fail": sum(1 for gate in gates if gate["status"] == "fail"),
            "publication_audit": publication["summary"],
            "experiment_matrix": experiments["summary"],
            "provider_readiness": {"ready_count": providers["ready_count"], "provider_count": providers["provider_count"]},
            "claim_evidence": claims["summary"],
            "license_readiness": license_report["summary"],
        },
        "gates": gates,
    }


def validate_gate(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["version"] != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload['version']}.")
    if payload["summary"]["gates"] < 5:
        problems.append("Expected at least five submission gates.")
    gate_statuses = [gate["status"] for gate in payload["gates"]]
    if payload["final_status"] == "ready" and any(status != "pass" for status in gate_statuses):
        problems.append("final_status cannot be ready while any gate fails.")
    if payload["final_status"] == "not_ready" and all(status == "pass" for status in gate_statuses):
        problems.append("final_status should be ready when all gates pass.")
    for gate in payload["gates"]:
        if gate["status"] == "fail" and not gate["blocker"]:
            problems.append(f"Failing gate {gate['id']} must include a blocker.")
        if not gate["evidence"]:
            problems.append(f"Gate {gate['id']} has no evidence paths.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    gate_rows = [[gate["id"], gate["status"], ", ".join(f"`{path}`" for path in gate["evidence"]), gate["blocker"]] for gate in payload["gates"]]
    summary_rows = [
        ["final_status", payload["final_status"]],
        ["gates_passed", payload["summary"]["pass"]],
        ["gates_failed", payload["summary"]["fail"]],
        ["required_experiments_missing", payload["summary"]["experiment_matrix"]["required_missing"]],
        ["providers_ready", f"{payload['summary']['provider_readiness']['ready_count']}/{payload['summary']['provider_readiness']['provider_count']}"],
        ["unsupported_claims", payload["summary"]["claim_evidence"]["unsupported_currently"]],
        ["license_release_ready", payload["summary"]["license_readiness"]["release_ready"]],
    ]
    lines = [
        "# FounderBench v0.3 Submission Gate",
        "",
        "This generated report combines the publication audit, experiment matrix, provider readiness, claim-evidence report, and license-readiness report into a single go/no-go view.",
        "",
        "## Decision",
        "",
        f"Final status: `{payload['final_status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Gates",
        "",
        markdown_table(["Gate", "Status", "Evidence", "Blocker"], gate_rows),
        "",
        "## Validation",
        "",
    ]
    problems = validate_gate(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The gate report is internally consistent. A `not_ready` final status is expected until required external evidence and owner metadata are complete.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_gate(json_output: Path, markdown_output: Path) -> None:
    payload = build_gate()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate top-level submission gate report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_gate(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
