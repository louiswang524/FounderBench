from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .submission import validate_submission
from .task_runner import run_task
from .tasks import TASKS, get_task


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def _check_output(path: Path) -> dict[str, Any]:
    return {
        "path": str(path.relative_to(ROOT)),
        "exists": path.exists(),
        "bytes": path.stat().st_size if path.exists() else 0,
    }


def build_report() -> dict[str, Any]:
    manifest_path = OUTPUTS / "founderbench-task-manifest.json"
    baseline_raw_path = OUTPUTS / "founderbench-baseline-raw.json"
    smoke_result = run_task(get_task("FND-001"), "task_heuristic")
    validation_problems = validate_submission(baseline_raw_path) if baseline_raw_path.exists() else ["Missing baseline raw output."]
    checks = [
        {
            "id": "python_runtime",
            "status": "pass",
            "detail": f"Python {sys.version.split()[0]}",
        },
        {
            "id": "task_suite_size",
            "status": "pass" if len(TASKS) == 50 else "fail",
            "detail": f"{len(TASKS)} tasks loaded.",
        },
        {
            "id": "manifest_present",
            "status": "pass" if manifest_path.exists() else "fail",
            "detail": str(_check_output(manifest_path)),
        },
        {
            "id": "single_task_execution",
            "status": "pass" if smoke_result["task_id"] == "FND-001" and "score" in smoke_result else "fail",
            "detail": f"FND-001 task_heuristic score={smoke_result.get('score', {}).get('score')}",
        },
        {
            "id": "baseline_submission_validation",
            "status": "pass" if not validation_problems else "fail",
            "detail": "Included baseline raw output passes submission validation." if not validation_problems else "; ".join(validation_problems[:3]),
        },
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Reviewer smoke report for quickly checking that the benchmark artifact loads, executes one deterministic task, and validates included baseline outputs.",
        "status": "pass" if all(row["status"] == "pass" for row in checks) else "fail",
        "checks": checks,
        "quick_commands": [
            "python -m moneybench.reviewer_smoke --json-output ..\\..\\outputs\\founderbench-reviewer-smoke.json --markdown-output ..\\..\\outputs\\founderbench-reviewer-smoke.md",
            "python -m moneybench.task_cli --policy task_heuristic --task FND-001",
            "python -m moneybench.submission --input ..\\..\\outputs\\founderbench-baseline-raw.json --report ..\\..\\outputs\\founderbench-submission-validation.md",
        ],
        "full_validation_commands": [
            "python -m unittest discover -s tests -v",
            "python -m moneybench.release validate",
            "python -m moneybench.release bundle",
        ],
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if len(payload.get("checks", [])) < 5:
        problems.append("Expected at least five smoke checks.")
    if payload.get("status") == "pass" and any(row["status"] != "pass" for row in payload["checks"]):
        problems.append("Smoke report cannot pass while an individual check fails.")
    if "release validate" not in " ".join(payload.get("full_validation_commands", [])):
        problems.append("Smoke report must point reviewers to full release validation.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [[row["id"], row["status"], row["detail"]] for row in payload["checks"]]
    lines = [
        "# FounderBench Reviewer Smoke Report",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Checks",
        "",
        markdown_table(["ID", "Status", "Detail"], rows),
        "",
        "## Quick Commands",
        "",
        "```powershell",
        *payload["quick_commands"],
        "```",
        "",
        "## Full Validation",
        "",
        "```powershell",
        *payload["full_validation_commands"],
        "```",
        "",
        "## Validation",
        "",
    ]
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The smoke report is internally consistent.")
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
    parser = argparse.ArgumentParser(description="Generate reviewer smoke report for FounderBench.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
