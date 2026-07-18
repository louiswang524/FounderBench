from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .claim_evidence import build_report as build_claim_report
from .experiment_matrix import build_matrix
from .provider_readiness import readiness_matrix
from .submission_gate import build_gate


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


REQUIREMENTS: list[dict[str, Any]] = [
    {
        "id": "scaled_task_suite",
        "goal_clause": "scale the startup-agent task suite beyond the current 25 tasks",
        "completion_standard": "A fixed current task manifest contains more than 25 tasks and task coverage/provenance artifacts explain families, splits, curation, and cards.",
        "evidence_paths": [
            "outputs/founderbench-task-manifest.json",
            "outputs/founderbench-task-coverage.md",
            "outputs/founderbench-task-provenance.md",
            "outputs/founderbench-task-cards.md",
        ],
        "evidence_test": "task_count_gt_25",
    },
    {
        "id": "simulator_and_action_space",
        "goal_clause": "strengthen the controlled simulator and action space",
        "completion_standard": "Simulator, market catalog, action semantics, and action ablation artifacts exist and document/exercise structured startup actions.",
        "evidence_paths": [
            "work/moneybench/moneybench/env.py",
            "work/moneybench/moneybench/schema.py",
            "outputs/founderbench-action-semantics.md",
            "outputs/founderbench-market-catalog.md",
            "outputs/founderbench-action-ablation.md",
        ],
        "evidence_test": "action_count_ge_13",
    },
    {
        "id": "normalized_business_metrics",
        "goal_clause": "define rigorous normalized business metrics",
        "completion_standard": "Primary bounded score, diagnostics, score rubric, sensitivity analysis, and statistical protocol are generated and internally validated.",
        "evidence_paths": [
            "outputs/founderbench-metrics-and-evaluation.md",
            "outputs/founderbench-score-rubric.md",
            "outputs/founderbench-metric-sensitivity.md",
            "outputs/founderbench-statistical-protocol.md",
            "outputs/founderbench-paired-statistics.md",
        ],
        "evidence_test": "metrics_present",
    },
    {
        "id": "heuristic_baselines_and_ablations",
        "goal_clause": "run representative heuristic baselines with ablations",
        "completion_standard": "Deterministic non-LLM baselines cover all 50 tasks and ablation/statistical/difficulty artifacts exist.",
        "evidence_paths": [
            "outputs/founderbench-baseline-raw.json",
            "outputs/founderbench-baseline-leaderboard.json",
            "outputs/founderbench-baseline-analysis.md",
            "outputs/founderbench-ablation-report.md",
            "outputs/founderbench-action-ablation.md",
            "outputs/founderbench-difficulty-calibration.md",
        ],
        "evidence_test": "heuristic_runs_complete",
    },
    {
        "id": "representative_llm_baselines",
        "goal_clause": "run representative LLM baselines",
        "completion_standard": "Required DeepSeek, Anthropic, Gemini, and local/open-source current release outputs exist and pass submission validation.",
        "evidence_paths": [
            "outputs/founderbench-deepseek.json",
            "outputs/founderbench-deepseek-submission-report.md",
            "outputs/founderbench-anthropic.json",
            "outputs/founderbench-anthropic-submission-report.md",
            "outputs/founderbench-gemini.json",
            "outputs/founderbench-gemini-submission-report.md",
            "outputs/founderbench-local-open-model.json",
            "outputs/founderbench-local-open-model-submission-report.md",
            "outputs/founderbench-provider-run-status.md",
            "outputs/founderbench-experiment-runbook.md",
        ],
        "evidence_test": "llm_required_runs_valid",
    },
    {
        "id": "documentation_and_accessibility",
        "goal_clause": "document reproducibility and limitations",
        "completion_standard": "README, spec, reproduction guide, reviewer index, environment/determinism manifests, validity report, and submission schemas are present.",
        "evidence_paths": [
            "work/moneybench/README.md",
            "work/moneybench/SPEC.md",
            "outputs/founderbench-reproduction-guide.md",
            "outputs/founderbench-reviewer-index.md",
            "outputs/founderbench-reproducibility-manifest.md",
            "outputs/founderbench-environment-report.md",
            "outputs/founderbench-determinism-audit.md",
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-model-submission-schema.md",
        ],
        "evidence_test": "all_paths_present",
    },
    {
        "id": "benchmark_card_and_paper_artifacts",
        "goal_clause": "prepare the benchmark card plus paper-ready experimental evidence",
        "completion_standard": "Benchmark card, paper draft, paper tables/figure data, references, claim-evidence report, submission gate, and release bundle exist.",
        "evidence_paths": [
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-paper-draft.md",
            "outputs/founderbench-paper-tables.md",
            "outputs/founderbench-paper-figure-data.md",
            "outputs/founderbench-references.bib",
            "outputs/founderbench-claim-evidence.md",
            "outputs/founderbench-submission-gate.md",
            "release/founderbench/SHA256SUMS.json",
            "release/founderbench/BUNDLE-INTEGRITY.md",
        ],
        "evidence_test": "paper_artifacts_present_but_claims_gate",
    },
    {
        "id": "public_release_metadata",
        "goal_clause": "publishable benchmark paper artifact",
        "completion_standard": "Final public LICENSE and CITATION metadata are selected by the project owner.",
        "evidence_paths": [
            "work/moneybench/LICENSE",
            "work/moneybench/CITATION.cff",
            "outputs/founderbench-license-readiness.md",
            "outputs/founderbench-release-metadata-checklist.md",
        ],
        "evidence_test": "license_ready",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def file_evidence(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    entry: dict[str, Any] = {"path": rel_path, "exists": path.exists()}
    if path.exists():
        entry["bytes"] = path.stat().st_size
        entry["sha256"] = sha256(path)
    return entry


def _load_json(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _all_present(evidence: list[dict[str, Any]]) -> bool:
    return all(row["exists"] for row in evidence)


def _status_for_test(test: str, evidence: list[dict[str, Any]]) -> tuple[str, str]:
    if test == "task_count_gt_25":
        manifest = _load_json("outputs/founderbench-task-manifest.json")
        count = int(manifest.get("task_count") or 0)
        if count > 25 and _all_present(evidence):
            return "complete", f"Task manifest reports {count} tasks."
        return "incomplete", f"Task manifest reports {count} tasks; expected more than 25 with complete documentation."

    if test == "action_count_ge_13":
        catalog = _load_json("outputs/founderbench-action-semantics.json")
        actions = catalog.get("actions", [])
        if len(actions) >= 13 and _all_present(evidence):
            return "complete", f"Action semantics catalog documents {len(actions)} structured actions."
        return "incomplete", f"Action semantics catalog documents {len(actions)} actions; expected at least 13 and complete simulator evidence."

    if test == "metrics_present":
        return ("complete", "Metric, rubric, sensitivity, and statistical-protocol artifacts are present.") if _all_present(evidence) else ("incomplete", "Some metric/protocol artifacts are missing.")

    if test == "heuristic_runs_complete":
        raw = _load_json("outputs/founderbench-baseline-raw.json")
        policies = {row.get("policy"): row.get("tasks") for row in raw if isinstance(row, dict)}
        expected = {"random", "conservative", "heuristic", "task_heuristic"}
        if expected <= set(policies) and all(policies[name] == 50 for name in expected) and _all_present(evidence):
            return "complete", "Four deterministic baselines each report 50 tasks."
        return "incomplete", f"Deterministic baseline coverage is incomplete: {policies}."

    if test == "llm_required_runs_valid":
        matrix = build_matrix()
        provider_readiness = readiness_matrix()
        missing = matrix["summary"]["required_missing"]
        ready = provider_readiness["ready_count"]
        if missing == 0 and ready >= 3 and _all_present(evidence):
            return "complete", "Required hosted/local LLM evidence is present and provider readiness threshold is met."
        return "missing", f"{missing} required experiment groups are missing and {ready}/{provider_readiness['provider_count']} providers are ready."

    if test == "all_paths_present":
        return ("complete", "Documentation, reproduction, audit, and schema artifacts are present.") if _all_present(evidence) else ("incomplete", "Some documentation/reproducibility artifacts are missing.")

    if test == "paper_artifacts_present_but_claims_gate":
        claims = build_claim_report()
        if _all_present(evidence) and claims["summary"]["unsupported_currently"] == 0:
            return "complete", "Paper artifacts are present and all claims are supported."
        if _all_present(evidence):
            return "partial", f"Paper artifacts are present, but {claims['summary']['unsupported_currently']} stronger claims remain unsupported."
        return "incomplete", "Some paper-facing artifacts are missing."

    if test == "license_ready":
        gate = build_gate()
        license_gate = next(row for row in gate["gates"] if row["id"] == "license_and_citation")
        if license_gate["status"] == "pass" and _all_present(evidence):
            return "complete", "License and citation metadata are public-release ready."
        return "incomplete", license_gate["blocker"]

    return ("complete", "All listed evidence paths are present.") if _all_present(evidence) else ("incomplete", "Some evidence paths are missing.")


def build_audit() -> dict[str, Any]:
    items = []
    for requirement in REQUIREMENTS:
        evidence = [file_evidence(path) for path in requirement["evidence_paths"]]
        missing_paths = [row["path"] for row in evidence if not row["exists"]]
        status, rationale = _status_for_test(requirement["evidence_test"], evidence)
        if missing_paths and status == "complete":
            status = "incomplete"
            rationale = "Some evidence paths are missing."
        items.append(
            {
                "id": requirement["id"],
                "goal_clause": requirement["goal_clause"],
                "completion_standard": requirement["completion_standard"],
                "status": status,
                "rationale": rationale,
                "evidence": evidence,
                "missing_paths": missing_paths,
            }
        )
    status_counts = {status: sum(1 for item in items if item["status"] == status) for status in ["complete", "partial", "incomplete", "missing"]}
    complete = status_counts["complete"] == len(items)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Goal-level completion audit for the active publishable-benchmark objective.",
        "completion_claim": "complete" if complete else "not_complete",
        "summary": {
            "requirements": len(items),
            **status_counts,
            "submission_gate": build_gate()["final_status"],
        },
        "items": items,
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["requirements"] != len(REQUIREMENTS):
        problems.append("Completion audit requirement count does not match the configured goal requirements.")
    if payload["completion_claim"] == "complete" and payload["summary"]["complete"] != payload["summary"]["requirements"]:
        problems.append("Completion claim cannot be complete while any requirement is not complete.")
    if payload["summary"]["submission_gate"] != "ready" and payload["completion_claim"] == "complete":
        problems.append("Completion claim cannot be complete while the submission gate is not ready.")
    ids = {item["id"] for item in payload["items"]}
    for required in {"scaled_task_suite", "representative_llm_baselines", "public_release_metadata"}:
        if required not in ids:
            problems.append(f"Missing goal requirement {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            item["id"],
            item["status"],
            item["goal_clause"],
            item["rationale"],
        ]
        for item in payload["items"]
    ]
    lines = [
        "# FounderBench Goal Completion Audit",
        "",
        "This generated audit maps the active benchmark-development goal to current evidence. It is intentionally stricter than a file-presence checklist: incomplete external model evidence and owner metadata keep the goal open.",
        "",
        f"Completion claim: `{payload['completion_claim']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Requirement Status",
        "",
        markdown_table(["Requirement", "Status", "Goal Clause", "Rationale"], rows),
        "",
        "## Evidence Details",
        "",
    ]
    for item in payload["items"]:
        lines.extend(
            [
                f"### {item['id']}",
                "",
                f"- Goal clause: {item['goal_clause']}",
                f"- Completion standard: {item['completion_standard']}",
                f"- Status: `{item['status']}`",
                f"- Rationale: {item['rationale']}",
                "",
                "Evidence:",
            ]
        )
        lines.extend(
            f"- `{row['path']}`: {'present' if row['exists'] else 'missing'}"
            for row in item["evidence"]
        )
        if item["missing_paths"]:
            lines.append("")
            lines.append("Missing evidence:")
            lines.extend(f"- `{path}`" for path in item["missing_paths"])
        lines.append("")
    lines.extend(["## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The completion audit is internally consistent with the current goal and submission gate.")
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
    parser = argparse.ArgumentParser(description="Generate goal-level FounderBench completion audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
