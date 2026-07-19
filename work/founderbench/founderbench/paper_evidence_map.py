from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .claim_evidence import build_report as build_claim_report
from .paper_tables import build_tables
from .submission_gate import build_gate


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


SECTION_MAP: list[dict[str, Any]] = [
    {
        "section": "Abstract and Introduction",
        "paper_claim": "FounderBench evaluates structured startup-like operating decisions in a controlled simulator, not real-world company success.",
        "evidence_paths": [
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-datasheet.md",
            "outputs/founderbench-responsible-use.md",
            "work/founderbench/SPEC.md",
            "outputs/founderbench-claim-evidence.md",
        ],
        "allowed_claim_ids": ["controlled_startup_operator_benchmark", "real_world_startup_prediction"],
        "status_rule": "claim_guarded",
    },
    {
        "section": "Benchmark Design",
        "paper_claim": "The current release artifact contains 50 fixed public tasks across 10 families, 13 structured actions, and a fixed simulated market catalog.",
        "evidence_paths": [
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-task-coverage.md",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-action-semantics.md",
            "outputs/founderbench-market-catalog.md",
        ],
        "allowed_claim_ids": ["expanded_50_task_suite", "structured_action_space"],
        "status_rule": "all_present",
    },
    {
        "section": "Metrics",
        "paper_claim": "Scores are bounded 0-100 task outcomes with solve threshold, diagnostics, sensitivity checks, and paired comparison protocol.",
        "evidence_paths": [
            "outputs/founderbench-metrics-and-evaluation.md",
            "outputs/founderbench-score-rubric.md",
            "outputs/founderbench-scoring-consistency-audit.md",
            "outputs/founderbench-metric-sensitivity.md",
            "outputs/founderbench-statistical-protocol.md",
            "outputs/founderbench-paired-statistics.md",
            "outputs/founderbench-power-analysis.md",
        ],
        "allowed_claim_ids": ["bounded_normalized_metrics"],
        "status_rule": "all_present",
    },
    {
        "section": "Baselines",
        "paper_claim": "The paper currently reports deterministic random, conservative, heuristic, and task-aware heuristic baselines on all 50 tasks.",
        "evidence_paths": [
            "outputs/founderbench-baseline-raw.json",
            "outputs/founderbench-baseline-leaderboard.json",
            "outputs/founderbench-leaderboard-policy.md",
            "outputs/founderbench-leaderboard-stability.md",
            "outputs/founderbench-baseline-analysis.md",
            "outputs/founderbench-result-integrity-audit.md",
            "outputs/founderbench-paper-tables.md",
            "outputs/founderbench-model-result-cards.md",
        ],
        "allowed_claim_ids": ["deterministic_baseline_spread"],
        "status_rule": "deterministic_tables_only",
    },
    {
        "section": "Ablations and Difficulty Calibration",
        "paper_claim": "Capability-ladder, action-space, task-difficulty, and qualitative trace artifacts support deterministic calibration claims.",
        "evidence_paths": [
            "outputs/founderbench-ablation-report.md",
            "outputs/founderbench-action-ablation.md",
            "outputs/founderbench-difficulty-calibration.md",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-qualitative-traces.md",
        ],
        "allowed_claim_ids": ["capability_ladder_ablation"],
        "status_rule": "all_present",
    },
    {
        "section": "Hosted and Local LLM Results",
        "paper_claim": "Hosted/local provider comparison is planned but not yet supported by current evidence.",
        "evidence_paths": [
            "outputs/founderbench-experiment-matrix.md",
            "outputs/founderbench-experiment-runbook.md",
            "outputs/founderbench-provider-run-status.md",
            "outputs/founderbench-provider-comparability-audit.md",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-leaderboard-policy.md",
            "outputs/founderbench-model-result-cards.md",
            "outputs/founderbench-submission-manifest.md",
        ],
        "allowed_claim_ids": ["hosted_llm_comparison"],
        "status_rule": "intentionally_excluded",
    },
    {
        "section": "Reproducibility and Auditability",
        "paper_claim": "The package includes reproduction commands, source/output hashes, environment report, reviewer smoke test, deterministic replay audit, and release-bundle integrity report.",
        "evidence_paths": [
            "outputs/founderbench-reproduction-guide.md",
            "outputs/founderbench-reproducibility-manifest.md",
            "outputs/founderbench-result-integrity-audit.md",
            "outputs/founderbench-environment-report.md",
            "outputs/founderbench-reviewer-smoke.md",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-determinism-audit.md",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-contamination-leakage-audit.md",
            "release/founderbench/BUNDLE-INTEGRITY.md",
        ],
        "allowed_claim_ids": [],
        "status_rule": "all_present",
    },
    {
        "section": "Limitations",
        "paper_claim": "Limitations are documented for synthetic simulator validity, missing hosted LLM evidence, missing human calibration, missing private holdout execution, and release metadata.",
        "evidence_paths": [
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-datasheet.md",
            "outputs/founderbench-responsible-use.md",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-human-calibration-analysis.md",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-completion-audit.md",
            "outputs/founderbench-submission-gate.md",
        ],
        "allowed_claim_ids": ["private_holdout_available", "real_world_startup_prediction"],
        "status_rule": "claim_guarded",
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


def _claim_by_id() -> dict[str, dict[str, Any]]:
    return {row["id"]: row for row in build_claim_report()["claims"]}


def _status_for(section: dict[str, Any], evidence: list[dict[str, Any]], claims: dict[str, dict[str, Any]]) -> tuple[str, str]:
    if not all(row["exists"] for row in evidence):
        return "incomplete", "One or more evidence paths are missing."
    if section["status_rule"] == "deterministic_tables_only":
        tables = build_tables()
        if tables["summary"]["deterministic_runs"] >= 4:
            if tables["summary"]["valid_provider_runs"] == 0:
                return "supported", "Deterministic baseline evidence is present; provider rows are correctly excluded."
            return "supported", "Deterministic baseline evidence is present; validated provider rows are tracked separately with diagnostics."
        return "incomplete", "Paper tables do not contain the expected deterministic evidence state."
    if section["status_rule"] == "intentionally_excluded":
        claim = claims["hosted_llm_comparison"]
        if claim["status"] == "unsupported_currently":
            return "excluded_until_evidence", claim["permitted_wording"]
        return "supported", "Hosted/local LLM claim is now supported."
    if section["status_rule"] == "claim_guarded":
        guarded = [claims[claim_id] for claim_id in section["allowed_claim_ids"] if claim_id in claims]
        unsupported = [row for row in guarded if row["status"] == "unsupported_currently"]
        if unsupported:
            return "qualified", "; ".join(row["permitted_wording"] for row in unsupported)
        return "supported", "Claim-evidence guardrails permit current wording."
    return "supported", "All section evidence paths are present."


def build_map() -> dict[str, Any]:
    claims = _claim_by_id()
    sections = []
    for section in SECTION_MAP:
        evidence = [file_entry(path) for path in section["evidence_paths"]]
        status, rationale = _status_for(section, evidence, claims)
        sections.append(
            {
                "section": section["section"],
                "paper_claim": section["paper_claim"],
                "status": status,
                "rationale": rationale,
                "evidence": evidence,
                "claim_ids": section["allowed_claim_ids"],
            }
        )
    gate = build_gate()
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Section-by-section evidence map for the current paper draft.",
        "submission_gate": gate["final_status"],
        "sections": sections,
        "summary": {
            "sections": len(sections),
            "supported": sum(1 for row in sections if row["status"] == "supported"),
            "qualified": sum(1 for row in sections if row["status"] == "qualified"),
            "excluded_until_evidence": sum(1 for row in sections if row["status"] == "excluded_until_evidence"),
            "incomplete": sum(1 for row in sections if row["status"] == "incomplete"),
        },
    }


def validate_map(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["sections"] < 8:
        problems.append("Paper evidence map should cover the major draft sections.")
    if payload["summary"]["incomplete"]:
        problems.append("Paper evidence map has incomplete sections.")
    if payload["submission_gate"] != "ready" and payload["summary"]["excluded_until_evidence"] <= 0:
        problems.append("A not-ready paper should explicitly exclude unsupported LLM/private evidence claims.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [row["section"], row["status"], row["paper_claim"], row["rationale"]]
        for row in payload["sections"]
    ]
    lines = [
        "# FounderBench Paper Evidence Map",
        "",
        "This generated map links paper-draft sections to the artifacts that support them. It keeps planned hosted/local LLM comparisons separate from currently supported deterministic evidence.",
        "",
        f"Submission gate: `{payload['submission_gate']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Section Crosswalk",
        "",
        markdown_table(["Paper Section", "Status", "Claim", "Rationale"], rows),
        "",
        "## Evidence Detail",
        "",
    ]
    for row in payload["sections"]:
        lines.extend([f"### {row['section']}", "", f"Status: `{row['status']}`", "", row["paper_claim"], "", "Evidence:"])
        lines.extend(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}" for item in row["evidence"])
        if row["claim_ids"]:
            lines.append("")
            lines.append("Claim-evidence ids:")
            lines.extend(f"- `{claim_id}`" for claim_id in row["claim_ids"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_map(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The paper evidence map is internally consistent with current artifacts and claim guardrails.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_map(json_output: Path, markdown_output: Path) -> None:
    payload = build_map()
    problems = validate_map(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper section evidence map.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_map(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
