from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = ROOT / "work" / "founderbench"
VERSION = "0.3.0"


REQUIRED_DECISIONS = [
    {
        "id": "license_choice",
        "decision": "Select a public release license.",
        "why_it_matters": "External users need explicit reuse, modification, and redistribution terms.",
        "acceptable_examples": ["MIT", "Apache-2.0", "BSD-3-Clause"],
        "target_files": ["work/founderbench/LICENSE"],
    },
    {
        "id": "author_metadata",
        "decision": "Replace placeholder author metadata in CITATION.cff.",
        "why_it_matters": "Citation metadata must identify artifact authors before public release.",
        "acceptable_examples": ["Personal author names", "Organization plus maintainers"],
        "target_files": ["work/founderbench/CITATION.cff"],
    },
    {
        "id": "repository_url",
        "decision": "Add public repository URL to CITATION.cff.",
        "why_it_matters": "Reviewers and users need a stable source-code location.",
        "acceptable_examples": ["https://github.com/<owner>/<repo>"],
        "target_files": ["work/founderbench/CITATION.cff"],
    },
    {
        "id": "citation_license_field",
        "decision": "Set the CITATION.cff license field to the selected license identifier.",
        "why_it_matters": "Citation tooling expects machine-readable license metadata.",
        "acceptable_examples": ["MIT", "Apache-2.0", "BSD-3-Clause"],
        "target_files": ["work/founderbench/CITATION.cff"],
    },
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def build_report() -> dict[str, Any]:
    citation_path = PACKAGE_ROOT / "CITATION.cff"
    citation_template_path = PACKAGE_ROOT / "CITATION.cff.template"
    license_todo_path = PACKAGE_ROOT / "LICENSE-TODO.md"
    license_path = PACKAGE_ROOT / "LICENSE"
    license_template_path = PACKAGE_ROOT / "LICENSE.template"
    citation_text = read_text(citation_path)
    license_todo_text = read_text(license_todo_path)
    checks = [
        {
            "id": "citation_file_exists",
            "status": "pass" if citation_path.exists() else "missing",
            "path": "work/founderbench/CITATION.cff",
            "detail": "CITATION.cff is present.",
        },
        {
            "id": "citation_author_placeholder",
            "status": "incomplete" if "TODO: Add author names" in citation_text else "pass",
            "path": "work/founderbench/CITATION.cff",
            "detail": "Author metadata must be finalized.",
        },
        {
            "id": "citation_repository_placeholder",
            "status": "incomplete" if "TODO: Add public repository URL" in citation_text else "pass",
            "path": "work/founderbench/CITATION.cff",
            "detail": "Repository URL must be finalized.",
        },
        {
            "id": "citation_license_placeholder",
            "status": "incomplete" if 'license: "TODO"' in citation_text or "license: TODO" in citation_text else "pass",
            "path": "work/founderbench/CITATION.cff",
            "detail": "License metadata must match the selected release license.",
        },
        {
            "id": "license_file_exists",
            "status": "pass" if license_path.exists() else "missing",
            "path": "work/founderbench/LICENSE",
            "detail": "A final LICENSE file should exist for public release.",
        },
        {
            "id": "license_template_exists",
            "status": "pass" if license_template_path.exists() else "missing",
            "path": "work/founderbench/LICENSE.template",
            "detail": "A non-final license template should help the owner create the final LICENSE file.",
        },
        {
            "id": "citation_template_exists",
            "status": "pass" if citation_template_path.exists() else "missing",
            "path": "work/founderbench/CITATION.cff.template",
            "detail": "A non-final citation template should help the owner replace placeholders safely.",
        },
        {
            "id": "license_todo_present",
            "status": (
                "pass"
                if license_path.exists() and "MIT License" in read_text(license_path) and not license_todo_path.exists()
                else (
                    "incomplete"
                    if "No public release license has been selected" in license_todo_text or not license_path.exists()
                    else "pass"
                )
            ),
            "path": "work/founderbench/LICENSE",
            "detail": (
                "Public MIT LICENSE is present and LICENSE-TODO.md has been removed."
                if license_path.exists() and not license_todo_path.exists()
                else "LICENSE-TODO.md documents the unresolved owner decision."
            ),
        },
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "License and citation metadata readiness report for public benchmark release.",
        "summary": {
            "checks": len(checks),
            "pass": sum(1 for check in checks if check["status"] == "pass"),
            "incomplete": sum(1 for check in checks if check["status"] == "incomplete"),
            "missing": sum(1 for check in checks if check["status"] == "missing"),
            "owner_decisions_required": len(REQUIRED_DECISIONS),
            "release_ready": all(check["status"] == "pass" for check in checks),
        },
        "checks": checks,
        "required_decisions": REQUIRED_DECISIONS,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["version"] != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload['version']}.")
    if payload["summary"]["checks"] < 5:
        problems.append("Expected at least five license/citation checks.")
    if payload["summary"]["owner_decisions_required"] < 3:
        problems.append("Expected owner decisions for license, authors, and repository.")
    if payload["summary"]["release_ready"] and any(check["status"] != "pass" for check in payload["checks"]):
        problems.append("release_ready cannot be true while checks are incomplete.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    check_rows = [[check["id"], check["status"], check["path"], check["detail"]] for check in payload["checks"]]
    decision_rows = [
        [
            decision["id"],
            decision["decision"],
            decision["why_it_matters"],
            ", ".join(decision["target_files"]),
        ]
        for decision in payload["required_decisions"]
    ]
    lines = [
        "# FounderBench License and Citation Readiness",
        "",
        "This generated report tracks the owner-controlled metadata required before public release. It does not choose a license; it names the remaining decisions.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Checks",
        "",
        markdown_table(["ID", "Status", "Path", "Detail"], check_rows),
        "",
        "## Required Owner Decisions",
        "",
        markdown_table(["ID", "Decision", "Why It Matters", "Target Files"], decision_rows),
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
        lines.append("The report is internally valid. Public release readiness remains false until all checks pass.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate license/citation readiness report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
