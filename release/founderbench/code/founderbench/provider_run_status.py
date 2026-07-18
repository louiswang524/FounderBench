from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .baseline_execution_plan import build_plan
from .paper_tables import ROOT, load_runs
from .submission import validate_run


OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def _sha256(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _planned_paths(plan: dict[str, Any]) -> set[str]:
    paths: set[str] = set()
    for row in plan["runs"]:
        paths.add(row["output"])
        paths.add(row["audit_output"])
        paths.add(row["submission_report"])
        paths.add(row["audit_submission_report"])
        paths.add(row["repeat_bundle_output"])
        paths.add(row["repeat_bundle_report"])
        for repeat_output in row["repeat_outputs"]:
            paths.add(repeat_output)
    return paths


def _status_for_run(row: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / row["output"]
    report_path = ROOT / row["submission_report"]
    audit_path = ROOT / row["audit_output"]
    audit_report_path = ROOT / row["audit_submission_report"]
    repeat_bundle_path = ROOT / row["repeat_bundle_output"]
    repeat_bundle_report_path = ROOT / row["repeat_bundle_report"]
    status: dict[str, Any] = {
        "id": row["id"],
        "policy": row["policy"],
        "priority": row["priority"],
        "model_family": row["model_family"],
        "output": row["output"],
        "submission_report": row["submission_report"],
        "audit_output": row["audit_output"],
        "exists": path.exists(),
        "submission_report_exists": report_path.exists(),
        "audit_exists": audit_path.exists(),
        "audit_submission_report_exists": audit_report_path.exists(),
        "repeat_bundle_output": row["repeat_bundle_output"],
        "repeat_bundle_report": row["repeat_bundle_report"],
        "repeat_bundle_exists": repeat_bundle_path.exists(),
        "repeat_bundle_report_exists": repeat_bundle_report_path.exists(),
        "repeat_outputs": row["repeat_outputs"],
        "repeat_outputs_present": sum(1 for output in row["repeat_outputs"] if (ROOT / output).exists()),
        "evidence_kind": "",
        "status": "missing",
        "runs": 0,
        "tasks": 0,
        "problems": [],
    }
    candidates = [
        ("repeat_bundle", repeat_bundle_path, repeat_bundle_report_path, row["repeat_bundle_output"], row["repeat_bundle_report"]),
        ("single_run", path, report_path, row["output"], row["submission_report"]),
    ]
    invalid_problems: list[str] = []
    for kind, candidate_path, candidate_report, candidate_rel, report_rel in candidates:
        if not candidate_path.exists():
            continue
        try:
            runs = load_runs(candidate_path)
        except Exception as exc:  # noqa: BLE001 - report malformed external submissions.
            invalid_problems.append(f"{candidate_rel}: {exc}")
            continue
        problems: list[str] = []
        task_counts = []
        for run in runs:
            task_counts.append(run.get("tasks", 0))
            problems.extend(validate_run(run))
        if not candidate_report.exists():
            problems.append(f"Missing validation report {report_rel}")
        if problems:
            invalid_problems.extend(f"{candidate_rel}: {problem}" for problem in problems)
            continue
        status["bytes"] = candidate_path.stat().st_size
        status["sha256"] = _sha256(candidate_path)
        status["runs"] = len(runs)
        status["tasks"] = max(task_counts) if task_counts else 0
        status["status"] = "valid"
        status["evidence_kind"] = kind
        status["evidence_path"] = candidate_rel
        return status
    status["problems"] = invalid_problems or [f"Missing {row['output']} or {row['repeat_bundle_output']}"]
    status["status"] = "invalid" if invalid_problems else "missing"
    return status


def _legacy_provider_files(planned_paths: set[str]) -> list[dict[str, Any]]:
    if not OUTPUTS.exists():
        return []
    patterns = ("deepseek", "anthropic", "gemini", "local-open-model")
    excluded_names = {
        "founderbench-provider-readiness.json",
        "founderbench-provider-readiness.md",
        "founderbench-baseline-execution-plan.json",
        "founderbench-baseline-execution-plan.md",
        "founderbench-provider-run-status.json",
        "founderbench-provider-run-status.md",
    }
    rows = []
    for path in sorted(OUTPUTS.glob("*")):
        if not path.is_file():
            continue
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        if rel in planned_paths or path.name in excluded_names:
            continue
        lower = path.name.lower()
        if any(pattern in lower for pattern in patterns):
            rows.append(
                {
                    "path": rel,
                    "bytes": path.stat().st_size,
                    "reason_excluded": "Not a planned current release provider evidence path; older, smoke, trace, or differently named provider artifacts are excluded from paper claims.",
                }
            )
    return rows


def build_status() -> dict[str, Any]:
    plan = build_plan()
    planned = [_status_for_run(row) for row in plan["runs"]]
    planned_paths = _planned_paths(plan)
    legacy = _legacy_provider_files(planned_paths)
    required = [row for row in planned if row["priority"] == "required"]
    valid_required = [row for row in required if row["status"] == "valid"]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Provider-run status report for current release paper evidence, generated from planned hosted/local baseline paths and submission validation.",
        "planned_runs": planned,
        "excluded_provider_like_files": legacy,
        "summary": {
            "planned_runs": len(planned),
            "valid_runs": sum(1 for row in planned if row["status"] == "valid"),
            "invalid_runs": sum(1 for row in planned if row["status"] == "invalid"),
            "missing_runs": sum(1 for row in planned if row["status"] == "missing"),
            "required_runs": len(required),
            "required_valid": len(valid_required),
            "required_missing_or_invalid": len(required) - len(valid_required),
            "audit_outputs_present": sum(1 for row in planned if row["audit_exists"]),
            "repeat_bundles_present": sum(1 for row in planned if row["repeat_bundle_exists"]),
            "repeat_outputs_present": sum(row["repeat_outputs_present"] for row in planned),
            "excluded_provider_like_files": len(legacy),
            "ready_for_llm_claims": len(valid_required) == len(required),
        },
    }


def validate_status(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["planned_runs"] < 5:
        problems.append("Expected at least five planned provider/local runs.")
    if payload["summary"]["required_runs"] < 4:
        problems.append("Expected at least four required provider/local runs.")
    if payload["summary"]["ready_for_llm_claims"] and payload["summary"]["required_missing_or_invalid"]:
        problems.append("LLM claims cannot be ready while required runs are missing or invalid.")
    for row in payload["planned_runs"]:
        if row["status"] == "valid" and row["tasks"] != 50:
            problems.append(f"{row['id']} is valid but does not report 50 tasks.")
        if row["status"] != "valid" and not row["problems"]:
            problems.append(f"{row['id']} is {row['status']} but has no problem explanation.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    planned_rows = [
        [
            row["id"],
            row["policy"],
            row["priority"],
            row["status"],
            row["runs"],
            row["tasks"],
            row["evidence_kind"],
            row["repeat_outputs_present"],
            row["submission_report_exists"],
            row["audit_exists"],
            "; ".join(row["problems"][:2]),
        ]
        for row in payload["planned_runs"]
    ]
    excluded_rows = [
        [row["path"], row["bytes"], row["reason_excluded"]]
        for row in payload["excluded_provider_like_files"]
    ]
    lines = [
        "# FounderBench Provider Run Status",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Planned current release Runs",
        "",
        markdown_table(["ID", "Policy", "Priority", "Status", "Runs", "Tasks", "Evidence", "Repeat Seeds", "Report", "Audit", "Problems"], planned_rows),
        "",
        "## Excluded Provider-Like Files",
        "",
    ]
    if excluded_rows:
        lines.append(markdown_table(["Path", "Bytes", "Reason Excluded"], excluded_rows))
    else:
        lines.append("No provider-like files outside the planned current evidence paths were found.")
    lines.extend(["", "## Validation", ""])
    problems = validate_status(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The status report is internally consistent. Missing planned runs are expected until hosted/local model evidence is generated and validated.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_status(json_output: Path, markdown_output: Path) -> None:
    payload = build_status()
    problems = validate_status(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate provider-run status report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_status(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
