from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .references import REFERENCE_ENTRIES


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


EXPECTED_CONTEXTS: list[dict[str, Any]] = [
    {
        "number": 1,
        "key": "yao2023react",
        "expected_terms": ["ReAct", "reasoning", "action"],
        "claim_type": "agent reasoning/action framing",
    },
    {
        "number": 2,
        "key": "schick2023toolformer",
        "expected_terms": ["Toolformer", "external APIs"],
        "claim_type": "tool-use training",
    },
    {
        "number": 3,
        "key": "wang2023voyager",
        "expected_terms": ["Voyager", "Minecraft"],
        "claim_type": "long-horizon embodied agent",
    },
    {
        "number": 4,
        "key": "liu2025agentbench",
        "expected_terms": ["AgentBench", "interactive environments"],
        "claim_type": "general agent benchmark",
    },
    {
        "number": 5,
        "key": "mialon2023gaia",
        "expected_terms": ["GAIA", "general assistants"],
        "claim_type": "general assistant benchmark",
    },
    {
        "number": 6,
        "key": "jimenez2024swebench",
        "expected_terms": ["SWE-bench", "GitHub issues"],
        "claim_type": "software engineering benchmark",
    },
    {
        "number": 7,
        "key": "zhou2024webarena",
        "expected_terms": ["WebArena", "web environments"],
        "claim_type": "web-agent environment benchmark",
    },
    {
        "number": 8,
        "key": "yao2024taubench",
        "expected_terms": ["tau-bench", "tool", "user"],
        "claim_type": "tool-agent-user interaction benchmark",
    },
    {
        "number": 9,
        "key": "xu2025theagentcompany",
        "expected_terms": ["TheAgentCompany", "software-company"],
        "claim_type": "workplace/company agent benchmark",
    },
    {
        "number": 10,
        "key": "drouin2024workarena",
        "expected_terms": ["WorkArena", "enterprise web-agent"],
        "claim_type": "enterprise web-agent benchmark",
    },
    {
        "number": 11,
        "key": "liu2026econwebarena",
        "expected_terms": ["EconWebArena", "economic"],
        "claim_type": "economic web-agent benchmark",
    },
    {
        "number": 12,
        "key": "han2026enterprisearena",
        "expected_terms": ["EnterpriseArena", "CFO"],
        "claim_type": "long-horizon enterprise allocation benchmark",
    },
]


def _field(text: str, name: str) -> str:
    match = re.search(rf"{name}=\{{(.+?)\}}", text, flags=re.DOTALL)
    return re.sub(r"\s+", " ", match.group(1)).strip() if match else ""


def _reference_lines(paper: str) -> dict[int, str]:
    lines: dict[int, str] = {}
    for line in paper.splitlines():
        match = re.match(r"\[(\d+)\]\s+(.+)", line.strip())
        if match:
            lines[int(match.group(1))] = match.group(2)
    return lines


def _contexts(paper: str) -> dict[int, list[str]]:
    body = paper.split("## References", 1)[0]
    paragraphs = [paragraph.strip() for paragraph in re.split(r"\n\s*\n", body) if paragraph.strip()]
    contexts: dict[int, list[str]] = {}
    for paragraph in paragraphs:
        for number in re.findall(r"\[(\d+)\]", paragraph):
            contexts.setdefault(int(number), []).append(paragraph)
    return contexts


def _contains_terms(text: str, terms: list[str]) -> bool:
    lowered = text.casefold()
    return all(term.casefold() in lowered for term in terms)


def build_audit(paper_path: Path | None = None) -> dict[str, Any]:
    paper_path = paper_path or (ROOT / "outputs" / "acceleratorbench-paper-draft-v0.1.md")
    paper = paper_path.read_text(encoding="utf-8")
    ref_lines = _reference_lines(paper)
    contexts = _contexts(paper)
    entries_by_key = {entry["key"]: entry for entry in REFERENCE_ENTRIES}
    expected_order = [entry["key"] for entry in REFERENCE_ENTRIES]
    rows = []
    for expected in EXPECTED_CONTEXTS:
        entry = entries_by_key[expected["key"]]
        bibtex = entry["bibtex"]
        number = expected["number"]
        context_text = " ".join(contexts.get(number, []))
        reference_line = ref_lines.get(number, "")
        rows.append(
            {
                "number": number,
                "key": expected["key"],
                "expected_key_at_position": expected_order[number - 1] if number - 1 < len(expected_order) else None,
                "title": _field(bibtex, "title"),
                "url": _field(bibtex, "url"),
                "source": entry["source"],
                "reference_line_present": bool(reference_line),
                "context_count": len(contexts.get(number, [])),
                "context_terms_present": _contains_terms(context_text, expected["expected_terms"]),
                "reference_line_matches_title_hint": bool(reference_line) and _contains_terms(reference_line, [expected["expected_terms"][0]]),
                "claim_type": expected["claim_type"],
                "expected_terms": expected["expected_terms"],
            }
        )
    numbering = sorted(ref_lines)
    contiguous = numbering == list(range(1, len(REFERENCE_ENTRIES) + 1))
    rows_with_context = sum(1 for row in rows if row["context_count"] > 0)
    rows_matching_order = sum(1 for row in rows if row["key"] == row["expected_key_at_position"])
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Local citation-context audit for the paper draft. It verifies numeric citation order, BibTeX/provenance coverage, and whether each citation is used in a context matching its intended benchmark-literature claim. It does not replace external citation-context peer review.",
        "paper_path": str(paper_path.relative_to(ROOT)),
        "external_status": "local_context_verified_external_spotcheck_required",
        "summary": {
            "references": len(REFERENCE_ENTRIES),
            "paper_reference_lines": len(ref_lines),
            "contexts_checked": len(rows),
            "contiguous_numbering": contiguous,
            "rows_with_context": rows_with_context,
            "rows_matching_bibtex_order": rows_matching_order,
            "context_term_matches": sum(1 for row in rows if row["context_terms_present"]),
            "reference_title_hint_matches": sum(1 for row in rows if row["reference_line_matches_title_hint"]),
        },
        "checks": rows,
        "limitations": [
            "This audit checks local consistency between the paper draft, BibTeX entries, and recorded provenance.",
            "It does not prove that every cited paper supports every sentence in the surrounding paragraph.",
            "A final submission should still run external citation-context verification against primary paper pages or PDFs.",
        ],
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    summary = payload["summary"]
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if summary["references"] != len(REFERENCE_ENTRIES):
        problems.append("Citation audit reference count does not match reference entries.")
    if not summary["contiguous_numbering"]:
        problems.append("Paper reference numbering is not contiguous.")
    if summary["rows_with_context"] != summary["contexts_checked"]:
        problems.append("Every checked reference should have at least one in-text citation context.")
    if summary["rows_matching_bibtex_order"] != summary["contexts_checked"]:
        problems.append("Numeric paper references should match BibTeX/provenance order.")
    if summary["context_term_matches"] < summary["contexts_checked"]:
        problems.append("One or more citation contexts lacks expected terms.")
    if summary["reference_title_hint_matches"] < summary["contexts_checked"]:
        problems.append("One or more reference lines does not match the expected title hint.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    check_rows = [
        [
            row["number"],
            row["key"],
            row["claim_type"],
            row["context_count"],
            "yes" if row["context_terms_present"] else "no",
            "yes" if row["reference_line_matches_title_hint"] else "no",
            row["source"],
        ]
        for row in payload["checks"]
    ]
    lines = [
        "# FounderBench v0.3 Citation Context Audit",
        "",
        "This generated audit checks local consistency between the paper draft, BibTeX entries, and reference provenance. It is deliberately conservative and still requires external citation-context verification before final submission.",
        "",
        f"External status: `{payload['external_status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Citation Checks",
        "",
        markdown_table(["No.", "Key", "Claim Type", "Contexts", "Context Terms", "Title Hint", "Source"], check_rows),
        "",
        "## Limitations",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["limitations"])
    lines.extend(["", "## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The local citation-context audit is internally consistent with the current paper draft and reference artifacts.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench citation-context audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
