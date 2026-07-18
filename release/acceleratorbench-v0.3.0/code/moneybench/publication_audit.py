from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
RELEASE = ROOT / "release" / "acceleratorbench-v0.3.0"
VERSION = "0.3.0"


REQUIREMENTS: list[dict[str, Any]] = [
    {
        "id": "completed_artifact",
        "category": "artifact",
        "requirement": "Completed benchmark code, task suite, runner, and release bundle.",
        "required_paths": [
            "work/moneybench/moneybench/env.py",
            "work/moneybench/moneybench/market_catalog.py",
            "work/moneybench/moneybench/tasks.py",
            "work/moneybench/moneybench/task_runner.py",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.json",
            "outputs/acceleratorbench-action-semantics-v0.3.md",
            "outputs/acceleratorbench-action-semantics-v0.3.json",
            "outputs/acceleratorbench-market-catalog-v0.3.md",
            "outputs/acceleratorbench-market-catalog-v0.3.json",
            "outputs/acceleratorbench-task-manifest-v0.3.json",
            "outputs/acceleratorbench-task-coverage-v0.3.md",
            "outputs/acceleratorbench-task-coverage-v0.3.json",
            "outputs/acceleratorbench-task-feasibility-audit-v0.3.md",
            "outputs/acceleratorbench-task-feasibility-audit-v0.3.json",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.json",
            "outputs/acceleratorbench-task-provenance-v0.3.md",
            "outputs/acceleratorbench-task-provenance-v0.3.json",
            "outputs/acceleratorbench-task-cards-v0.3.md",
            "outputs/acceleratorbench-task-cards-v0.3.json",
            "release/acceleratorbench-v0.3.0/SHA256SUMS.json",
        ],
    },
    {
        "id": "metrics_protocol",
        "category": "metrics",
        "requirement": "Defined primary, secondary, diagnostic, family-specific, and uncertainty metrics.",
        "required_paths": [
            "outputs/acceleratorbench-metrics-and-evaluation.md",
            "outputs/acceleratorbench-metric-sensitivity-v0.3.md",
            "outputs/acceleratorbench-metric-sensitivity-v0.3.json",
            "outputs/acceleratorbench-statistical-protocol-v0.3.md",
            "outputs/acceleratorbench-statistical-protocol-v0.3.json",
            "outputs/acceleratorbench-power-analysis-v0.3.md",
            "outputs/acceleratorbench-power-analysis-v0.3.json",
            "outputs/acceleratorbench-score-rubric-v0.3.md",
            "outputs/acceleratorbench-score-rubric-v0.3.json",
            "outputs/acceleratorbench-scoring-consistency-audit-v0.3.md",
            "outputs/acceleratorbench-scoring-consistency-audit-v0.3.json",
            "outputs/acceleratorbench-baseline-analysis-v0.3.md",
            "outputs/acceleratorbench-paper-tables-v0.3.md",
            "outputs/acceleratorbench-paper-tables-v0.3.json",
            "outputs/acceleratorbench-model-result-cards-v0.3.md",
            "outputs/acceleratorbench-model-result-cards-v0.3.json",
            "outputs/acceleratorbench-paper-figure-data-v0.3.md",
            "outputs/acceleratorbench-paper-figure-data-v0.3.json",
            "outputs/acceleratorbench-random-repeats-v0.3.md",
        ],
    },
    {
        "id": "heuristic_baselines",
        "category": "baselines",
        "requirement": "Representative non-LLM baseline leaderboard and raw results on all 50 v0.3.0 tasks.",
        "required_paths": [
            "outputs/acceleratorbench-baseline-leaderboard-v0.3.json",
            "outputs/acceleratorbench-leaderboard-policy-v0.3.md",
            "outputs/acceleratorbench-leaderboard-policy-v0.3.json",
            "outputs/acceleratorbench-leaderboard-stability-v0.3.md",
            "outputs/acceleratorbench-leaderboard-stability-v0.3.json",
            "outputs/acceleratorbench-baseline-raw-v0.3.json",
            "outputs/acceleratorbench-model-comparison-v0.3.md",
            "outputs/acceleratorbench-model-comparison-v0.3.json",
            "outputs/acceleratorbench-result-integrity-audit-v0.3.md",
            "outputs/acceleratorbench-result-integrity-audit-v0.3.json",
            "outputs/acceleratorbench-model-result-cards-v0.3.md",
            "outputs/acceleratorbench-model-result-cards-v0.3.json",
            "outputs/acceleratorbench-ablation-report-v0.3.md",
            "outputs/acceleratorbench-action-ablation-v0.3.md",
            "outputs/acceleratorbench-action-ablation-v0.3.json",
            "outputs/acceleratorbench-paired-statistics-v0.3.md",
            "outputs/acceleratorbench-paired-statistics-v0.3.json",
            "outputs/acceleratorbench-difficulty-calibration-v0.3.md",
            "outputs/acceleratorbench-difficulty-calibration-v0.3.json",
            "outputs/acceleratorbench-task-feasibility-audit-v0.3.md",
            "outputs/acceleratorbench-task-feasibility-audit-v0.3.json",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.json",
        ],
    },
    {
        "id": "provider_adapters",
        "category": "baselines",
        "requirement": "Hosted/local provider adapters and model submission validation tooling.",
        "required_paths": [
            "work/moneybench/moneybench/llm_policy.py",
            "work/moneybench/moneybench/prompt_protocol.py",
            "work/moneybench/moneybench/local_model.py",
            "work/moneybench/moneybench/baseline_execution_plan.py",
            "work/moneybench/moneybench/experiment_runbook.py",
            "work/moneybench/moneybench/provider_readiness.py",
            "work/moneybench/moneybench/provider_run_status.py",
            "work/moneybench/moneybench/cost_accounting.py",
            "work/moneybench/moneybench/submission.py",
            "work/moneybench/moneybench/submission_bundle.py",
            "work/moneybench/moneybench/submission_schema.py",
            "outputs/acceleratorbench-model-submission-template.md",
            "outputs/acceleratorbench-leaderboard-policy-v0.3.md",
            "outputs/acceleratorbench-leaderboard-policy-v0.3.json",
            "outputs/acceleratorbench-model-submission-schema-v0.3.md",
            "outputs/acceleratorbench-model-submission-schema-v0.3.json",
            "outputs/acceleratorbench-submission-bundle-protocol-v0.3.md",
            "outputs/acceleratorbench-submission-bundle-protocol-v0.3.json",
            "outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.md",
            "outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.json",
            "outputs/acceleratorbench-prompt-protocol-v0.3.md",
            "outputs/acceleratorbench-prompt-protocol-v0.3.json",
            "outputs/acceleratorbench-provider-readiness-v0.3.md",
            "outputs/acceleratorbench-provider-readiness-v0.3.json",
            "outputs/acceleratorbench-cost-accounting-v0.3.md",
            "outputs/acceleratorbench-cost-accounting-v0.3.json",
            "outputs/acceleratorbench-baseline-execution-plan-v0.3.md",
            "outputs/acceleratorbench-baseline-execution-plan-v0.3.json",
            "outputs/acceleratorbench-experiment-runbook-v0.3.md",
            "outputs/acceleratorbench-experiment-runbook-v0.3.json",
            "outputs/acceleratorbench-provider-run-status-v0.3.md",
            "outputs/acceleratorbench-provider-run-status-v0.3.json",
            "outputs/acceleratorbench-provider-comparability-audit-v0.3.md",
            "outputs/acceleratorbench-provider-comparability-audit-v0.3.json",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.json",
            "outputs/acceleratorbench-submission-validation-v0.3.md",
        ],
    },
    {
        "id": "auditability",
        "category": "reproducibility",
        "requirement": "Trace, parse-failure, redaction, and qualitative analysis support.",
        "required_paths": [
            "work/moneybench/moneybench/provider_adapter.py",
            "work/moneybench/moneybench/qualitative.py",
            "outputs/acceleratorbench-qualitative-traces-v0.3.md",
            "outputs/acceleratorbench-qualitative-traces-v0.3.json",
            "outputs/acceleratorbench-environment-report-v0.3.md",
            "outputs/acceleratorbench-environment-report-v0.3.json",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.json",
            "outputs/acceleratorbench-scoring-consistency-audit-v0.3.md",
            "outputs/acceleratorbench-scoring-consistency-audit-v0.3.json",
            "outputs/acceleratorbench-reproducibility-manifest-v0.3.md",
            "outputs/acceleratorbench-reproducibility-manifest-v0.3.json",
            "outputs/acceleratorbench-result-integrity-audit-v0.3.md",
            "outputs/acceleratorbench-result-integrity-audit-v0.3.json",
            "outputs/acceleratorbench-determinism-audit-v0.3.md",
            "outputs/acceleratorbench-determinism-audit-v0.3.json",
            "outputs/acceleratorbench-prompt-protocol-v0.3.md",
            "outputs/acceleratorbench-prompt-protocol-v0.3.json",
            "outputs/acceleratorbench-provider-comparability-audit-v0.3.md",
            "outputs/acceleratorbench-provider-comparability-audit-v0.3.json",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.json",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.json",
        ],
    },
    {
        "id": "private_holdout_protocol",
        "category": "anti_gaming",
        "requirement": "Private holdout blueprint, fingerprint generator, and evaluator protocol.",
        "required_paths": [
            "work/moneybench/moneybench/holdout.py",
            "work/moneybench/moneybench/private_holdout_evaluator.py",
            "outputs/acceleratorbench-private-holdout-blueprint-v0.3.json",
            "outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md",
            "outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.json",
            "outputs/acceleratorbench-private-holdout-smoke-v0.3.md",
            "outputs/acceleratorbench-private-holdout-smoke-v0.3.json",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.json",
        ],
    },
    {
        "id": "documentation",
        "category": "documentation",
        "requirement": "Benchmark card, reproduction guide, specification, paper draft, references, and checklist.",
        "required_paths": [
            "work/moneybench/README.md",
            "work/moneybench/SPEC.md",
            "work/moneybench/CITATION.cff.template",
            "work/moneybench/LICENSE.template",
            "outputs/acceleratorbench-benchmark-card.md",
            "outputs/acceleratorbench-datasheet-v0.3.md",
            "outputs/acceleratorbench-datasheet-v0.3.json",
            "outputs/acceleratorbench-reproduction-guide.md",
            "outputs/acceleratorbench-reviewer-smoke-v0.3.md",
            "outputs/acceleratorbench-reviewer-smoke-v0.3.json",
            "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
            "outputs/acceleratorbench-human-calibration-protocol-v0.3.json",
            "outputs/acceleratorbench-human-calibration-schema-v0.3.md",
            "outputs/acceleratorbench-human-calibration-schema-v0.3.json",
            "outputs/acceleratorbench-human-calibration-template-v0.3.json",
            "outputs/acceleratorbench-human-calibration-analysis-v0.3.md",
            "outputs/acceleratorbench-human-calibration-analysis-v0.3.json",
            "outputs/acceleratorbench-human-calibration-packet-v0.3.md",
            "outputs/acceleratorbench-human-calibration-packet-v0.3.json",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.json",
            "outputs/acceleratorbench-paper-draft-v0.1.md",
            "outputs/acceleratorbench-citation-audit-v0.3.md",
            "outputs/acceleratorbench-citation-audit-v0.3.json",
            "outputs/acceleratorbench-paper-evidence-map-v0.3.md",
            "outputs/acceleratorbench-paper-evidence-map-v0.3.json",
            "outputs/acceleratorbench-references.bib",
            "outputs/acceleratorbench-reference-provenance-v0.3.json",
            "outputs/acceleratorbench-validity-report-v0.3.md",
            "outputs/acceleratorbench-validity-report-v0.3.json",
            "outputs/acceleratorbench-responsible-use-v0.3.md",
            "outputs/acceleratorbench-responsible-use-v0.3.json",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.json",
            "outputs/acceleratorbench-claim-evidence-v0.3.md",
            "outputs/acceleratorbench-claim-evidence-v0.3.json",
            "outputs/acceleratorbench-paper-claim-lint-v0.3.md",
            "outputs/acceleratorbench-paper-claim-lint-v0.3.json",
            "outputs/acceleratorbench-submission-gate-v0.3.md",
            "outputs/acceleratorbench-submission-gate-v0.3.json",
            "outputs/acceleratorbench-submission-manifest-v0.3.md",
            "outputs/acceleratorbench-submission-manifest-v0.3.json",
            "outputs/acceleratorbench-completion-audit-v0.3.md",
            "outputs/acceleratorbench-completion-audit-v0.3.json",
            "outputs/acceleratorbench-reviewer-risk-audit-v0.3.md",
            "outputs/acceleratorbench-reviewer-risk-audit-v0.3.json",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.json",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.json",
            "outputs/acceleratorbench-failure-mode-audit-v0.3.md",
            "outputs/acceleratorbench-failure-mode-audit-v0.3.json",
            "outputs/acceleratorbench-submission-action-plan-v0.3.md",
            "outputs/acceleratorbench-submission-action-plan-v0.3.json",
            "outputs/acceleratorbench-supplementary-package-checklist.md",
            "outputs/acceleratorbench-experiment-matrix-v0.3.md",
            "outputs/acceleratorbench-experiment-matrix-v0.3.json",
            "outputs/acceleratorbench-reviewer-index-v0.3.md",
            "outputs/acceleratorbench-reviewer-index-v0.3.json",
        ],
    },
    {
        "id": "hosted_llm_baselines",
        "category": "open_blocker",
        "requirement": "Full v0.3.0 hosted LLM baselines on all 50 tasks.",
        "required_paths": [],
        "status_override": "missing",
        "blocker": "Needs fresh DeepSeek/Claude/Gemini v0.3.0 runs with audit logs and submission validation.",
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
        "blocker": "Protocol exists, but private task definitions and hidden leaderboard are intentionally not included in v0.3.0.",
    },
    {
        "id": "final_license_metadata",
        "category": "open_blocker",
        "requirement": "Final public license and citation metadata selected by project owner.",
        "required_paths": [
            "work/moneybench/CITATION.cff",
            "work/moneybench/LICENSE-TODO.md",
            "outputs/acceleratorbench-license-readiness-v0.3.md",
            "outputs/acceleratorbench-license-readiness-v0.3.json",
            "outputs/acceleratorbench-release-metadata-checklist-v0.3.md",
            "outputs/acceleratorbench-release-metadata-checklist-v0.3.json",
        ],
        "status_override": "incomplete",
        "blocker": "CITATION.cff and LICENSE-TODO.md contain owner-facing placeholders.",
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
        "release_bundle": "release/acceleratorbench-v0.3.0",
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
        "# FounderBench v0.3 Publication Audit",
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
