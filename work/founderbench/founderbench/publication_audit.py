from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
RELEASE = ROOT / "release" / "founderbench"
VERSION = "0.3.0"


REQUIREMENTS: list[dict[str, Any]] = [
    {
        "id": "completed_artifact",
        "category": "artifact",
        "requirement": "Completed benchmark code, task suite, runner, and release bundle.",
        "required_paths": [
            "work/founderbench/founderbench/env.py",
            "work/founderbench/founderbench/market_catalog.py",
            "work/founderbench/founderbench/tasks.py",
            "work/founderbench/founderbench/task_runner.py",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-simulator-invariant-audit.json",
            "outputs/founderbench-action-semantics.md",
            "outputs/founderbench-action-semantics.json",
            "outputs/founderbench-market-catalog.md",
            "outputs/founderbench-market-catalog.json",
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-task-coverage.md",
            "outputs/founderbench-task-coverage.json",
            "outputs/founderbench-task-feasibility-audit.md",
            "outputs/founderbench-task-feasibility-audit.json",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-task-revision-ledger.json",
            "outputs/founderbench-task-provenance.md",
            "outputs/founderbench-task-provenance.json",
            "outputs/founderbench-task-cards.md",
            "outputs/founderbench-task-cards.json",
            "release/founderbench/SHA256SUMS.json",
        ],
    },
    {
        "id": "metrics_protocol",
        "category": "metrics",
        "requirement": "Defined primary, secondary, diagnostic, family-specific, and uncertainty metrics.",
        "required_paths": [
            "outputs/founderbench-metrics-and-evaluation.md",
            "outputs/founderbench-metric-sensitivity.md",
            "outputs/founderbench-metric-sensitivity.json",
            "outputs/founderbench-statistical-protocol.md",
            "outputs/founderbench-statistical-protocol.json",
            "outputs/founderbench-power-analysis.md",
            "outputs/founderbench-power-analysis.json",
            "outputs/founderbench-score-rubric.md",
            "outputs/founderbench-score-rubric.json",
            "outputs/founderbench-scoring-consistency-audit.md",
            "outputs/founderbench-scoring-consistency-audit.json",
            "outputs/founderbench-baseline-analysis.md",
            "outputs/founderbench-paper-tables.md",
            "outputs/founderbench-paper-tables.json",
            "outputs/founderbench-model-result-cards.md",
            "outputs/founderbench-model-result-cards.json",
            "outputs/founderbench-paper-figure-data.md",
            "outputs/founderbench-paper-figure-data.json",
            "outputs/founderbench-random-repeats.md",
        ],
    },
    {
        "id": "heuristic_baselines",
        "category": "baselines",
        "requirement": "Representative non-LLM baseline leaderboard and raw results on all 50 current tasks.",
        "required_paths": [
            "outputs/founderbench-baseline-leaderboard.json",
            "outputs/founderbench-leaderboard-policy.md",
            "outputs/founderbench-leaderboard-policy.json",
            "outputs/founderbench-leaderboard-stability.md",
            "outputs/founderbench-leaderboard-stability.json",
            "outputs/founderbench-baseline-raw.json",
            "outputs/founderbench-model-comparison.md",
            "outputs/founderbench-model-comparison.json",
            "outputs/founderbench-result-integrity-audit.md",
            "outputs/founderbench-result-integrity-audit.json",
            "outputs/founderbench-model-result-cards.md",
            "outputs/founderbench-model-result-cards.json",
            "outputs/founderbench-ablation-report.md",
            "outputs/founderbench-action-ablation.md",
            "outputs/founderbench-action-ablation.json",
            "outputs/founderbench-paired-statistics.md",
            "outputs/founderbench-paired-statistics.json",
            "outputs/founderbench-difficulty-calibration.md",
            "outputs/founderbench-difficulty-calibration.json",
            "outputs/founderbench-task-feasibility-audit.md",
            "outputs/founderbench-task-feasibility-audit.json",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-task-revision-ledger.json",
        ],
    },
    {
        "id": "provider_adapters",
        "category": "baselines",
        "requirement": "Hosted/local provider adapters and model submission validation tooling.",
        "required_paths": [
            "work/founderbench/founderbench/llm_policy.py",
            "work/founderbench/founderbench/prompt_protocol.py",
            "work/founderbench/founderbench/local_model.py",
            "work/founderbench/founderbench/baseline_execution_plan.py",
            "work/founderbench/founderbench/experiment_runbook.py",
            "work/founderbench/founderbench/provider_readiness.py",
            "work/founderbench/founderbench/provider_run_status.py",
            "work/founderbench/founderbench/cost_accounting.py",
            "work/founderbench/founderbench/submission.py",
            "work/founderbench/founderbench/submission_bundle.py",
            "work/founderbench/founderbench/submission_schema.py",
            "outputs/founderbench-model-submission-template.md",
            "outputs/founderbench-leaderboard-policy.md",
            "outputs/founderbench-leaderboard-policy.json",
            "outputs/founderbench-model-submission-schema.md",
            "outputs/founderbench-model-submission-schema.json",
            "outputs/founderbench-submission-bundle-protocol.md",
            "outputs/founderbench-submission-bundle-protocol.json",
            "outputs/founderbench-local-openai-compatible-protocol.md",
            "outputs/founderbench-local-openai-compatible-protocol.json",
            "outputs/founderbench-prompt-protocol.md",
            "outputs/founderbench-prompt-protocol.json",
            "outputs/founderbench-provider-readiness.md",
            "outputs/founderbench-provider-readiness.json",
            "outputs/founderbench-cost-accounting.md",
            "outputs/founderbench-cost-accounting.json",
            "outputs/founderbench-baseline-execution-plan.md",
            "outputs/founderbench-baseline-execution-plan.json",
            "outputs/founderbench-experiment-runbook.md",
            "outputs/founderbench-experiment-runbook.json",
            "outputs/founderbench-provider-run-status.md",
            "outputs/founderbench-provider-run-status.json",
            "outputs/founderbench-provider-comparability-audit.md",
            "outputs/founderbench-provider-comparability-audit.json",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-provider-contract-audit.json",
            "outputs/founderbench-submission-validation.md",
        ],
    },
    {
        "id": "auditability",
        "category": "reproducibility",
        "requirement": "Trace, parse-failure, redaction, and qualitative analysis support.",
        "required_paths": [
            "work/founderbench/founderbench/provider_adapter.py",
            "work/founderbench/founderbench/qualitative.py",
            "outputs/founderbench-qualitative-traces.md",
            "outputs/founderbench-qualitative-traces.json",
            "outputs/founderbench-environment-report.md",
            "outputs/founderbench-environment-report.json",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-simulator-invariant-audit.json",
            "outputs/founderbench-scoring-consistency-audit.md",
            "outputs/founderbench-scoring-consistency-audit.json",
            "outputs/founderbench-reproducibility-manifest.md",
            "outputs/founderbench-reproducibility-manifest.json",
            "outputs/founderbench-result-integrity-audit.md",
            "outputs/founderbench-result-integrity-audit.json",
            "outputs/founderbench-determinism-audit.md",
            "outputs/founderbench-determinism-audit.json",
            "outputs/founderbench-prompt-protocol.md",
            "outputs/founderbench-prompt-protocol.json",
            "outputs/founderbench-provider-comparability-audit.md",
            "outputs/founderbench-provider-comparability-audit.json",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-provider-contract-audit.json",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-contamination-leakage-audit.json",
        ],
    },
    {
        "id": "private_holdout_protocol",
        "category": "anti_gaming",
        "requirement": "Private holdout blueprint, fingerprint generator, and evaluator protocol.",
        "required_paths": [
            "work/founderbench/founderbench/holdout.py",
            "work/founderbench/founderbench/private_holdout_evaluator.py",
            "outputs/founderbench-private-holdout-blueprint.json",
            "outputs/founderbench-private-holdout-evaluator-protocol.md",
            "outputs/founderbench-private-holdout-evaluator-protocol.json",
            "outputs/founderbench-private-holdout-smoke.md",
            "outputs/founderbench-private-holdout-smoke.json",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-contamination-leakage-audit.json",
        ],
    },
    {
        "id": "documentation",
        "category": "documentation",
        "requirement": "Benchmark card, reproduction guide, specification, paper draft, references, and checklist.",
        "required_paths": [
            "work/founderbench/README.md",
            "work/founderbench/SPEC.md",
            "work/founderbench/CITATION.cff.template",
            "work/founderbench/LICENSE.template",
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-datasheet.md",
            "outputs/founderbench-datasheet.json",
            "outputs/founderbench-reproduction-guide.md",
            "outputs/founderbench-reviewer-smoke.md",
            "outputs/founderbench-reviewer-smoke.json",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-human-calibration-protocol.json",
            "outputs/founderbench-human-calibration-schema.md",
            "outputs/founderbench-human-calibration-schema.json",
            "outputs/founderbench-human-calibration-template.json",
            "outputs/founderbench-human-calibration-analysis.md",
            "outputs/founderbench-human-calibration-analysis.json",
            "outputs/founderbench-human-calibration-packet.md",
            "outputs/founderbench-human-calibration-packet.json",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-task-revision-ledger.json",
            "outputs/founderbench-paper-draft.md",
            "outputs/founderbench-citation-audit.md",
            "outputs/founderbench-citation-audit.json",
            "outputs/founderbench-paper-evidence-map.md",
            "outputs/founderbench-paper-evidence-map.json",
            "outputs/founderbench-references.bib",
            "outputs/founderbench-reference-provenance.json",
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-validity-report.json",
            "outputs/founderbench-responsible-use.md",
            "outputs/founderbench-responsible-use.json",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-simulator-invariant-audit.json",
            "outputs/founderbench-claim-evidence.md",
            "outputs/founderbench-claim-evidence.json",
            "outputs/founderbench-paper-claim-lint.md",
            "outputs/founderbench-paper-claim-lint.json",
            "outputs/founderbench-submission-gate.md",
            "outputs/founderbench-submission-gate.json",
            "outputs/founderbench-submission-manifest.md",
            "outputs/founderbench-submission-manifest.json",
            "outputs/founderbench-completion-audit.md",
            "outputs/founderbench-completion-audit.json",
            "outputs/founderbench-reviewer-risk-audit.md",
            "outputs/founderbench-reviewer-risk-audit.json",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-provider-contract-audit.json",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-contamination-leakage-audit.json",
            "outputs/founderbench-failure-mode-audit.md",
            "outputs/founderbench-failure-mode-audit.json",
            "outputs/founderbench-submission-action-plan.md",
            "outputs/founderbench-submission-action-plan.json",
            "outputs/founderbench-supplementary-package-checklist.md",
            "outputs/founderbench-experiment-matrix.md",
            "outputs/founderbench-experiment-matrix.json",
            "outputs/founderbench-reviewer-index.md",
            "outputs/founderbench-reviewer-index.json",
        ],
    },
    {
        "id": "hosted_llm_baselines",
        "category": "open_blocker",
        "requirement": "Full current release hosted LLM baselines on all 50 tasks.",
        "required_paths": [],
        "status_override": "missing",
        "blocker": "Needs fresh DeepSeek/Claude/Gemini current release runs with audit logs and submission validation.",
    },
    {
        "id": "local_open_source_baseline",
        "category": "open_blocker",
        "requirement": "At least one local/open-source model baseline.",
        "required_paths": [],
        "status_override": "missing",
        "blocker": "Needs local OpenAI-compatible inference server/model run or uploaded raw result.",
    },
    {
        "id": "executed_private_holdout",
        "category": "open_blocker",
        "requirement": "Executed hidden-suite leaderboard on evaluator host.",
        "required_paths": [],
        "status_override": "missing",
        "blocker": "Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in current release.",
    },
    {
        "id": "final_license_metadata",
        "category": "open_blocker",
        "requirement": "Final public license and citation metadata selected by project owner.",
        "required_paths": [
            "work/founderbench/CITATION.cff",
            "work/founderbench/LICENSE",
            "LICENSE",
            "CITATION.cff",
            "outputs/founderbench-license-readiness.md",
            "outputs/founderbench-license-readiness.json",
            "outputs/founderbench-release-metadata-checklist.md",
            "outputs/founderbench-release-metadata-checklist.json",
        ],
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def resolve(path: str) -> Path:
    return ROOT / path


def audit() -> dict[str, Any]:
    items = []
    for requirement in REQUIREMENTS:
        evidence = []
        missing = []
        for rel in requirement.get("required_paths", []):
            path = resolve(rel)
            if path.exists():
                evidence.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
            else:
                missing.append(rel)
        if requirement.get("status_override"):
            status = requirement["status_override"]
        elif missing:
            status = "incomplete"
        else:
            status = "complete"
        items.append(
            {
                "id": requirement["id"],
                "category": requirement["category"],
                "requirement": requirement["requirement"],
                "status": status,
                "evidence": evidence,
                "missing_paths": missing,
                **({"blocker": requirement["blocker"]} if "blocker" in requirement else {}),
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "release_bundle": "release/founderbench",
        "summary": {
            "complete": sum(1 for item in items if item["status"] == "complete"),
            "incomplete": sum(1 for item in items if item["status"] == "incomplete"),
            "missing": sum(1 for item in items if item["status"] == "missing"),
        },
        "items": items,
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = []
    for item in payload["items"]:
        evidence_count = len(item["evidence"])
        blocker = item.get("blocker", "")
        rows.append([item["id"], item["category"], item["status"], evidence_count, blocker])
    lines = [
        "# FounderBench Publication Audit",
        "",
        "This audit maps benchmark/dataset submission expectations to concrete release artifacts. It is generated from the current workspace and intentionally keeps unresolved publication blockers visible.",
        "",
        "## Summary",
        "",
        markdown_table(["Status", "Count"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Requirement Matrix",
        "",
        markdown_table(["ID", "Category", "Status", "Evidence Files", "Blocker"], rows),
        "",
        "## Complete Evidence Items",
        "",
    ]
    for item in payload["items"]:
        if item["status"] != "complete":
            continue
        lines.extend([f"### {item['id']}", "", item["requirement"], ""])
        lines.extend(f"- `{entry['path']}` ({entry['bytes']} bytes)" for entry in item["evidence"])
        lines.append("")
    lines.extend(["## Open Blockers", ""])
    for item in payload["items"]:
        if item["status"] == "complete":
            continue
        lines.extend([f"- `{item['id']}`: {item['requirement']}"])
        if item.get("blocker"):
            lines.append(f"  Blocker: {item['blocker']}")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_audit(json_output: Path, markdown_output: Path) -> None:
    payload = audit()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate publication-readiness evidence audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
