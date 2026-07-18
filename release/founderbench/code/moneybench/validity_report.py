from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


THREATS: list[dict[str, Any]] = [
    {
        "id": "synthetic_market_dynamics",
        "category": "construct_validity",
        "severity": "high",
        "threat": "The simulator uses hand-designed demand, churn, reputation, risk, and cash dynamics rather than real startup markets.",
        "current_mitigation": "Frame the benchmark as a controlled decision environment, not a real-market proxy; expose simulator code, score rubrics, market catalog, a human-calibration protocol, and a task-revision ledger for calibration issues.",
        "evidence_paths": [
            "work/moneybench/moneybench/env.py",
            "outputs/founderbench-score-rubric.md",
            "outputs/founderbench-market-catalog.md",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-benchmark-card.md",
        ],
        "remaining_work": "Execute expert review or human-founder calibration to assess whether task incentives match startup judgment.",
    },
    {
        "id": "template_generated_tasks",
        "category": "external_validity",
        "severity": "medium",
        "threat": "The 50 public tasks are generated from 10 templates rather than curated from real startup histories.",
        "current_mitigation": "Report task-family coverage, split balance, seeds, horizons, and action coverage in generated artifacts.",
        "evidence_paths": [
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-task-coverage.md",
        ],
        "remaining_work": "Curate additional scenarios from public startup postmortems, accelerator cases, or expert-authored variants.",
    },
    {
        "id": "visible_public_test",
        "category": "evaluation_validity",
        "severity": "high",
        "threat": "The public test split is visible, so agents or prompts can overfit to released tasks.",
        "current_mitigation": "Label public_dev/public_test honestly and provide private-holdout blueprint plus evaluator protocol.",
        "evidence_paths": [
            "outputs/founderbench-private-holdout-blueprint.json",
            "outputs/founderbench-private-holdout-evaluator-protocol.md",
            "outputs/founderbench-contamination-leakage-audit.md",
        ],
        "remaining_work": "Instantiate hidden task definitions on an evaluator host and report hidden-suite scores.",
    },
    {
        "id": "missing_llm_baselines",
        "category": "empirical_validity",
        "severity": "high",
        "threat": "The current current release paper evidence includes deterministic baselines but lacks complete hosted/local LLM baselines.",
        "current_mitigation": "Provider adapters, readiness matrix, submission validator, and experiment matrix specify exact missing runs.",
        "evidence_paths": [
            "outputs/founderbench-provider-readiness.md",
            "outputs/founderbench-experiment-matrix.md",
            "outputs/founderbench-model-submission-template.md",
        ],
        "remaining_work": "Run DeepSeek, Claude, Gemini, self-consistency, and at least one local open-source model on all 50 tasks.",
    },
    {
        "id": "prompt_and_sampling_sensitivity",
        "category": "reliability",
        "severity": "medium",
        "threat": "Hosted LLM scores may depend on prompt wording, decoding settings, and stochastic sampling.",
        "current_mitigation": "Support repeated-run reports, raw task outputs, audit mode, and submission validation.",
        "evidence_paths": [
            "outputs/founderbench-random-repeats.md",
            "outputs/founderbench-reproduction-guide.md",
            "work/moneybench/moneybench/repeats.py",
        ],
        "remaining_work": "Report repeated prompt-sample intervals for hosted LLM submissions and freeze prompt versions.",
    },
    {
        "id": "adapter_and_format_failures",
        "category": "measurement_validity",
        "severity": "medium",
        "threat": "A model can fail because of malformed JSON or provider errors rather than poor business decisions.",
        "current_mitigation": "Count provider errors, parse categories, invalid actions, and over-budget decisions as diagnostics rather than discarding runs.",
        "evidence_paths": [
            "work/moneybench/moneybench/provider_adapter.py",
            "work/moneybench/moneybench/submission.py",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-submission-validation.md",
        ],
        "remaining_work": "Include redacted hosted audit traces for representative provider successes and failures.",
    },
    {
        "id": "heuristic_ceiling_bias",
        "category": "baseline_validity",
        "severity": "medium",
        "threat": "The task-aware heuristic may encode task-family knowledge that ordinary LLM agents do not receive.",
        "current_mitigation": "Report it as a capability-ladder calibration baseline, not as an agent-realistic baseline.",
        "evidence_paths": [
            "outputs/founderbench-ablation-report.md",
            "outputs/founderbench-paper-tables.md",
        ],
        "remaining_work": "Compare against prompt-only LLMs, self-consistency, and local open models to contextualize the heuristic ceiling.",
    },
    {
        "id": "missing_human_founder_baseline",
        "category": "interpretability",
        "severity": "low",
        "threat": "Without a human or expert baseline, it is hard to interpret absolute scores as business judgment quality.",
        "current_mitigation": "Use relative model/baseline comparisons, provide a human-calibration protocol and revision ledger, and avoid claiming real-world startup competence.",
        "evidence_paths": [
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-paper-draft.md",
        ],
        "remaining_work": "Execute the protocol and collect small expert/human-founder pilot results or expert ranking of task actions.",
    },
]


def _exists(path: str) -> bool:
    root = Path(__file__).resolve().parents[3]
    return (root / path).exists()


def build_report() -> dict[str, Any]:
    rows = []
    for threat in THREATS:
        row = dict(threat)
        row["evidence"] = [{"path": path, "exists": _exists(path)} for path in threat["evidence_paths"]]
        row["evidence_complete"] = all(item["exists"] for item in row["evidence"])
        rows.append(row)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Threats-to-validity and limitations matrix for benchmark paper review.",
        "summary": {
            "threats": len(rows),
            "high_severity": sum(1 for row in rows if row["severity"] == "high"),
            "medium_severity": sum(1 for row in rows if row["severity"] == "medium"),
            "low_severity": sum(1 for row in rows if row["severity"] == "low"),
            "evidence_complete": sum(1 for row in rows if row["evidence_complete"]),
        },
        "threats": rows,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["version"] != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload['version']}.")
    if payload["summary"]["threats"] < 6:
        problems.append("Expected at least six validity threats.")
    categories = {row["category"] for row in payload["threats"]}
    for required in {"construct_validity", "external_validity", "evaluation_validity", "empirical_validity", "reliability"}:
        if required not in categories:
            problems.append(f"Missing validity category {required}.")
    for row in payload["threats"]:
        if not row["evidence"]:
            problems.append(f"{row['id']} has no evidence paths.")
        if not row["current_mitigation"]:
            problems.append(f"{row['id']} has no mitigation.")
        if not row["remaining_work"]:
            problems.append(f"{row['id']} has no remaining work.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["id"],
            row["category"],
            row["severity"],
            "yes" if row["evidence_complete"] else "partial",
            row["current_mitigation"],
            row["remaining_work"],
        ]
        for row in payload["threats"]
    ]
    lines = [
        "# FounderBench Validity and Limitations Report",
        "",
        "This generated report states known threats to validity, current mitigations, artifact evidence, and remaining work. It is intended to keep paper claims appropriately scoped.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Threat Matrix",
        "",
        markdown_table(["ID", "Category", "Severity", "Evidence", "Current Mitigation", "Remaining Work"], rows),
        "",
        "## Evidence Paths",
        "",
    ]
    for row in payload["threats"]:
        lines.extend([f"### {row['id']}", "", row["threat"], ""])
        lines.extend(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}" for item in row["evidence"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The report covers construct, external, evaluation, empirical, and reliability threats with mitigations and remaining work.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate validity and limitations report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
