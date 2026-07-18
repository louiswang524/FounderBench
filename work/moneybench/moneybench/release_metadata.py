from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .license_readiness import REQUIRED_DECISIONS


VERSION = "0.3.0"


LICENSE_OPTIONS = [
    {
        "spdx_id": "MIT",
        "fit": "Permissive software/data-adjacent artifact reuse with minimal obligations.",
        "owner_note": "Simple and common; does not include explicit patent grant.",
    },
    {
        "spdx_id": "Apache-2.0",
        "fit": "Permissive reuse with explicit patent license and NOTICE handling.",
        "owner_note": "Often preferred for larger open-source projects and industry use.",
    },
    {
        "spdx_id": "BSD-3-Clause",
        "fit": "Permissive reuse with non-endorsement clause.",
        "owner_note": "Common academic/research software choice.",
    },
    {
        "spdx_id": "CC-BY-4.0",
        "fit": "Dataset/documentation reuse with attribution.",
        "owner_note": "May be appropriate for documentation/data, but not usually ideal as the only software-code license.",
    },
]


def citation_template() -> dict[str, Any]:
    return {
        "cff-version": "1.2.0",
        "title": "FounderBench: Evaluating LLM Agents as Startup Operators Under Controlled Resources",
        "message": "If you use FounderBench, please cite the associated paper or this software artifact.",
        "type": "software",
        "authors": [{"name": "<replace with author name or ORCID-aware author object>"}],
        "version": VERSION,
        "date-released": "2026-07-15",
        "abstract": "FounderBench is a controlled startup-agent benchmark for evaluating LLM agents on repeated business decisions under bounded resources.",
        "repository-code": "https://github.com/<owner>/<repo>",
        "license": "<SPDX license id selected by project owner>",
    }


def build_checklist() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Owner-facing public-release metadata checklist for finalizing license and citation files.",
        "status": "owner_action_required",
        "required_decisions": REQUIRED_DECISIONS,
        "license_options": LICENSE_OPTIONS,
        "citation_template": citation_template(),
        "finalization_steps": [
            "Choose one license identifier and add the corresponding full LICENSE text to work/moneybench/LICENSE.",
            "Use work/moneybench/LICENSE.template only as a guide; it is not a substitute for the final LICENSE file.",
            "Replace placeholder author metadata in work/moneybench/CITATION.cff.",
            "Use work/moneybench/CITATION.cff.template only as a guide; it is not a substitute for finalized citation metadata.",
            "Replace repository-code with the public repository URL.",
            "Set the CITATION.cff license field to the selected SPDX identifier.",
            "Remove or update LICENSE-TODO.md so it no longer states that no public release license has been selected.",
            "Run python -m moneybench.release regenerate and python -m moneybench.release validate.",
        ],
        "guardrails": [
            "This artifact does not select a license or author list for the owner.",
            "Template files are intentionally non-final and must not be treated as release metadata.",
            "Do not publish the package as open source until work/moneybench/LICENSE exists and CITATION.cff placeholders are replaced.",
            "If code and documentation/data use different licenses, state both clearly in README and CITATION metadata.",
        ],
    }


def validate_checklist(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "owner_action_required":
        problems.append("Release metadata checklist must remain owner_action_required until owner decisions are made.")
    if len(payload.get("required_decisions", [])) < 4:
        problems.append("Expected license, author, repository, and citation-license decisions.")
    spdx_ids = {row["spdx_id"] for row in payload.get("license_options", [])}
    for required in {"MIT", "Apache-2.0", "BSD-3-Clause"}:
        if required not in spdx_ids:
            problems.append(f"Missing common license option {required}.")
    citation = payload.get("citation_template", {})
    if "<" not in json.dumps(citation):
        problems.append("Citation template should include placeholders rather than pretending to be final.")
    if not payload.get("finalization_steps"):
        problems.append("Finalization steps are required.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    decision_rows = [
        [
            row["id"],
            row["decision"],
            ", ".join(row["acceptable_examples"]),
            ", ".join(row["target_files"]),
        ]
        for row in payload["required_decisions"]
    ]
    license_rows = [[row["spdx_id"], row["fit"], row["owner_note"]] for row in payload["license_options"]]
    lines = [
        "# FounderBench v0.3 Release Metadata Checklist",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Required Owner Decisions",
        "",
        markdown_table(["ID", "Decision", "Examples", "Target Files"], decision_rows),
        "",
        "## Common License Options",
        "",
        markdown_table(["SPDX ID", "Fit", "Owner Note"], license_rows),
        "",
        "## CITATION.cff Template",
        "",
        "```json",
        json.dumps(payload["citation_template"], indent=2),
        "```",
        "",
        "## Finalization Steps",
        "",
    ]
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(payload["finalization_steps"], start=1))
    lines.extend(["", "## Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["guardrails"])
    lines.extend(["", "## Validation", ""])
    problems = validate_checklist(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The checklist is internally consistent and intentionally leaves owner-controlled metadata unresolved.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_checklist(json_output: Path, markdown_output: Path) -> None:
    payload = build_checklist()
    problems = validate_checklist(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate owner-facing release metadata checklist.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_checklist(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
