from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from .analysis import markdown_table


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


TARGETS: list[dict[str, Any]] = [
    {
        "id": "paper_draft",
        "path": "outputs/acceleratorbench-paper-draft-v0.1.md",
        "required_disclosures": [
            "not yet a comparison of hosted LLM providers",
            "does not include private task definitions or hidden-suite scores",
            "real-world startup-prediction claims as unsupported",
        ],
    },
    {
        "id": "benchmark_card",
        "path": "outputs/acceleratorbench-benchmark-card.md",
        "required_disclosures": [
            "hosted LLM submissions still need repeated-sampling reports",
            "full publishable-artifact goal as `not_complete`",
            "required hosted/local LLM evidence",
        ],
    },
]


FORBIDDEN_PATTERNS: list[dict[str, str]] = [
    {
        "id": "real_world_prediction_claim",
        "pattern": r"\bFounderBench\s+(?:predicts|measures|validates)\s+real[- ]world\s+startup",
        "why": "The current artifact is a synthetic controlled simulator, not validated real-world startup prediction.",
    },
    {
        "id": "autonomous_company_deployment_claim",
        "pattern": r"\b(?:models?|agents?|LLM agents?)\s+can\s+(?:safely\s+)?run\s+a\s+(?:successful\s+)?real\s+compan",
        "why": "The benchmark must not be framed as evidence for autonomous real-company deployment.",
    },
    {
        "id": "hosted_provider_completed_claim",
        "pattern": r"\b(?:DeepSeek|Claude|Gemini).{0,80}\b(?:fully\s+compared|validated|evaluated)\s+on\s+v0\.3\.0",
        "why": "Hosted provider v0.3.0 runs are not present in the current release.",
    },
    {
        "id": "executed_private_holdout_claim",
        "pattern": r"\b(?:executed|official)\s+(?:private|hidden).{0,40}\b(?:holdout|leaderboard|scores)",
        "why": "v0.3.0 includes a holdout protocol and smoke test, not official hidden-suite results.",
    },
]


NEGATION_CUES = ["not", "no", "without", "unsupported", "avoid", "does not", "do not", "not yet", "marking"]


def _read_target(target: dict[str, Any]) -> str:
    return (ROOT / target["path"]).read_text(encoding="utf-8")


def _line_number(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def _has_nearby_negation(text: str, index: int) -> bool:
    window = text[max(0, index - 120) : index].lower()
    return any(cue in window for cue in NEGATION_CUES)


def scan_target(target: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / target["path"]
    exists = path.exists()
    text = _read_target(target) if exists else ""
    lower_text = text.lower()
    required = [
        {
            "phrase": phrase,
            "present": phrase.lower() in lower_text,
        }
        for phrase in target["required_disclosures"]
    ]
    forbidden_hits = []
    for rule in FORBIDDEN_PATTERNS:
        for match in re.finditer(rule["pattern"], text, flags=re.IGNORECASE | re.DOTALL):
            if _has_nearby_negation(text, match.start()):
                continue
            forbidden_hits.append(
                {
                    "rule_id": rule["id"],
                    "line": _line_number(text, match.start()),
                    "match": " ".join(match.group(0).split()),
                    "why": rule["why"],
                }
            )
    return {
        "id": target["id"],
        "path": target["path"],
        "exists": exists,
        "required_disclosures": required,
        "missing_required_disclosures": [row["phrase"] for row in required if not row["present"]],
        "forbidden_hits": forbidden_hits,
        "status": "pass" if exists and all(row["present"] for row in required) and not forbidden_hits else "fail",
    }


def build_audit() -> dict[str, Any]:
    targets = [scan_target(target) for target in TARGETS]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Paper and benchmark-card claim lint for unsupported hosted-LLM, hidden-holdout, and real-world startup-success wording.",
        "targets": targets,
        "summary": {
            "targets": len(targets),
            "passed": sum(1 for target in targets if target["status"] == "pass"),
            "failed": sum(1 for target in targets if target["status"] == "fail"),
            "forbidden_hits": sum(len(target["forbidden_hits"]) for target in targets),
            "missing_required_disclosures": sum(len(target["missing_required_disclosures"]) for target in targets),
        },
        "claim_guardrail": "This lint is a conservative text check. Passing it does not prove the paper is publication-ready; it only checks that key current-draft overclaiming guardrails are present and selected unsupported positive claims are absent.",
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("summary", {})
    if summary.get("targets") != len(TARGETS):
        problems.append("Unexpected number of lint targets.")
    if summary.get("failed") != 0:
        problems.append("One or more paper-claim lint targets failed.")
    if summary.get("forbidden_hits") != 0:
        problems.append("Unsupported positive claim wording was found.")
    if summary.get("missing_required_disclosures") != 0:
        problems.append("Required limitation disclosures are missing.")
    for target in payload.get("targets", []):
        if target["status"] != "pass":
            problems.append(f"{target['id']} claim lint status is {target['status']}.")
        if not target["exists"]:
            problems.append(f"{target['path']} is missing.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    target_rows = [
        [
            target["id"],
            target["status"],
            target["path"],
            len(target["missing_required_disclosures"]),
            len(target["forbidden_hits"]),
        ]
        for target in payload["targets"]
    ]
    lines = [
        "# FounderBench v0.3 Paper Claim Lint",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Target Status",
        "",
        markdown_table(["Target", "Status", "Path", "Missing Disclosures", "Forbidden Hits"], target_rows),
        "",
        "## Required Disclosures",
        "",
    ]
    for target in payload["targets"]:
        lines.extend([f"### {target['id']}", ""])
        rows = [[row["phrase"], row["present"]] for row in target["required_disclosures"]]
        lines.extend([markdown_table(["Phrase", "Present"], rows), ""])
        if target["forbidden_hits"]:
            lines.extend(["Forbidden wording hits:", ""])
            for hit in target["forbidden_hits"]:
                lines.append(f"- {hit['rule_id']} line {hit['line']}: `{hit['match']}`")
            lines.append("")
    lines.extend(["## Claim Guardrail", "", payload["claim_guardrail"], "", "## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The current paper draft and benchmark card include required limitation disclosures and avoid the scanned unsupported positive claims.")
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
    parser = argparse.ArgumentParser(description="Generate paper and benchmark-card claim lint.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
