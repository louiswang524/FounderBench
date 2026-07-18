from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


CLAIMS: list[dict[str, Any]] = [
    {
        "id": "controlled_startup_operator_benchmark",
        "claim": "FounderBench is a controlled benchmark for evaluating startup-operator agents under bounded resources.",
        "status": "supported",
        "permitted_wording": "FounderBench evaluates structured startup-like operating decisions in a controlled simulator.",
        "avoid_wording": "FounderBench measures real-world startup success.",
        "evidence_paths": [
            "work/moneybench/moneybench/env.py",
            "work/moneybench/SPEC.md",
            "outputs/founderbench-benchmark-card.md",
        ],
    },
    {
        "id": "expanded_50_task_suite",
        "claim": "The current release artifact contains 50 fixed public tasks across 10 startup operating families.",
        "status": "supported",
        "permitted_wording": "The benchmark contains 50 fixed public tasks across 10 balanced task families.",
        "avoid_wording": "The benchmark contains a hidden or privately evaluated benchmark suite.",
        "evidence_paths": [
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-task-coverage.md",
        ],
    },
    {
        "id": "structured_action_space",
        "claim": "Agents are evaluated through a structured 13-action business interface, and free-form rationale does not directly affect score.",
        "status": "supported",
        "permitted_wording": "The simulator executes only structured actions; rationale is retained for auditability but not scored directly.",
        "avoid_wording": "Models can earn score through persuasive business prose.",
        "evidence_paths": [
            "work/moneybench/moneybench/schema.py",
            "work/moneybench/moneybench/task_runner.py",
            "outputs/founderbench-task-coverage.md",
        ],
    },
    {
        "id": "bounded_normalized_metrics",
        "claim": "Task scores are bounded from 0 to 100 with a solve threshold of 70 and family-specific scoring rubrics.",
        "status": "supported",
        "permitted_wording": "Each task returns a bounded 0-100 score; tasks are solved at score >= 70.",
        "avoid_wording": "The score is a direct dollar value or external business valuation.",
        "evidence_paths": [
            "outputs/founderbench-metrics-and-evaluation.md",
            "outputs/founderbench-score-rubric.md",
            "work/moneybench/moneybench/tasks.py",
        ],
    },
    {
        "id": "deterministic_baseline_spread",
        "claim": "Rule-based baselines show the benchmark is neither solved by random action sampling nor impossible for simple structured policies.",
        "status": "supported",
        "permitted_wording": "Deterministic baselines show a wide spread from random to task-aware heuristic on the public current suite.",
        "avoid_wording": "The benchmark is validated against current frontier LLMs.",
        "evidence_paths": [
            "outputs/founderbench-baseline-leaderboard.json",
            "outputs/founderbench-baseline-analysis.md",
            "outputs/founderbench-paper-tables.md",
        ],
    },
    {
        "id": "capability_ladder_ablation",
        "claim": "The deterministic policy ladder gives an ablation-style calibration of business-decision capabilities.",
        "status": "supported",
        "permitted_wording": "The deterministic policy ladder is a calibration ablation, not a model architecture ablation.",
        "avoid_wording": "The ablation proves LLM reasoning mechanisms.",
        "evidence_paths": [
            "outputs/founderbench-ablation-report.md",
            "outputs/founderbench-paper-tables.md",
        ],
    },
    {
        "id": "hosted_llm_comparison",
        "claim": "FounderBench differentiates current hosted LLM providers on current release.",
        "status": "unsupported_currently",
        "permitted_wording": "Provider adapters and experiment protocols are included; hosted current release LLM results remain to be run.",
        "avoid_wording": "DeepSeek, Claude, and Gemini have been fully compared on current release.",
        "evidence_paths": [
            "outputs/founderbench-provider-readiness.md",
            "outputs/founderbench-experiment-matrix.md",
        ],
        "missing_evidence": [
            "outputs/founderbench-deepseek.json",
            "outputs/founderbench-anthropic.json",
            "outputs/founderbench-gemini.json",
        ],
    },
    {
        "id": "private_holdout_available",
        "claim": "The benchmark includes an executed private hidden holdout leaderboard.",
        "status": "unsupported_currently",
        "permitted_wording": "The benchmark includes a private-holdout blueprint and evaluator protocol, not executed hidden results.",
        "avoid_wording": "The reported current release leaderboard is hidden or private.",
        "evidence_paths": [
            "outputs/founderbench-private-holdout-blueprint.json",
            "outputs/founderbench-private-holdout-evaluator-protocol.md",
        ],
        "missing_evidence": ["outputs/founderbench-private-holdout-results.json"],
    },
    {
        "id": "real_world_startup_prediction",
        "claim": "FounderBench predicts real startup profitability or long-term company success.",
        "status": "unsupported_currently",
        "permitted_wording": "FounderBench is a synthetic controlled environment for studying startup-relevant decisions.",
        "avoid_wording": "High benchmark score means a model can run a successful real company.",
        "evidence_paths": [
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-benchmark-card.md",
        ],
        "missing_evidence": ["executed human/expert validation study", "real-world outcome correlation study"],
    },
]


def _evidence(path: str) -> dict[str, Any]:
    real_path = ROOT / path
    return {"path": path, "exists": real_path.exists()}


def build_report() -> dict[str, Any]:
    rows = []
    for claim in CLAIMS:
        row = dict(claim)
        row["evidence"] = [_evidence(path) for path in claim["evidence_paths"]]
        row["missing"] = [_evidence(path) for path in claim.get("missing_evidence", [])]
        row["evidence_complete"] = all(item["exists"] for item in row["evidence"])
        row["missing_evidence_present"] = [item for item in row["missing"] if item["exists"]]
        rows.append(row)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Claim-evidence guardrail for paper and benchmark-card wording.",
        "summary": {
            "claims": len(rows),
            "supported": sum(1 for row in rows if row["status"] == "supported"),
            "unsupported_currently": sum(1 for row in rows if row["status"] == "unsupported_currently"),
            "evidence_complete": sum(1 for row in rows if row["evidence_complete"]),
        },
        "claims": rows,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["version"] != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload['version']}.")
    if payload["summary"]["claims"] < 8:
        problems.append("Expected at least eight claim checks.")
    if payload["summary"]["unsupported_currently"] < 2:
        problems.append("Expected unsupported claims for missing LLM/holdout evidence.")
    for row in payload["claims"]:
        if row["status"] == "supported" and not row["evidence_complete"]:
            problems.append(f"Supported claim {row['id']} has missing evidence.")
        if row["status"] == "unsupported_currently" and not row.get("missing"):
            problems.append(f"Unsupported claim {row['id']} should name missing evidence.")
        if not row["permitted_wording"] or not row["avoid_wording"]:
            problems.append(f"Claim {row['id']} lacks wording guidance.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["id"],
            row["status"],
            "yes" if row["evidence_complete"] else "partial",
            row["permitted_wording"],
            row["avoid_wording"],
        ]
        for row in payload["claims"]
    ]
    lines = [
        "# FounderBench Claim-Evidence Report",
        "",
        "This generated report maps major paper/benchmark-card claims to current evidence. It is intentionally conservative: claims about hosted LLM comparisons, hidden holdouts, or real-world startup prediction remain unsupported until the required evidence exists.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Claim Matrix",
        "",
        markdown_table(["ID", "Status", "Evidence", "Permitted Wording", "Avoid Wording"], rows),
        "",
        "## Evidence Detail",
        "",
    ]
    for row in payload["claims"]:
        lines.extend([f"### {row['id']}", "", row["claim"], "", "Evidence:"])
        lines.extend(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}" for item in row["evidence"])
        if row["missing"]:
            lines.extend(["", "Missing evidence before stronger claim:"])
            lines.extend(f"- `{item['path']}`: {'present' if item['exists'] else 'missing'}" for item in row["missing"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All supported claims have current evidence, and unsupported claims name the missing evidence required before stronger wording.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate claim-evidence report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
