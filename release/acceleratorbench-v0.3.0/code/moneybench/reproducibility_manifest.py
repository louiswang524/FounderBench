from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

from .analysis import markdown_table


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = ROOT / "work" / "moneybench"
VERSION = "0.3.0"


CORE_SOURCE_PATHS = [
    "work/moneybench/moneybench/action_ablation.py",
    "work/moneybench/moneybench/action_semantics.py",
    "work/moneybench/moneybench/baseline_execution_plan.py",
    "work/moneybench/moneybench/benchmark_datasheet.py",
    "work/moneybench/moneybench/bundle_integrity.py",
    "work/moneybench/moneybench/citation_audit.py",
    "work/moneybench/moneybench/completion_audit.py",
    "work/moneybench/moneybench/contamination_leakage_audit.py",
    "work/moneybench/moneybench/cost_accounting.py",
    "work/moneybench/moneybench/determinism_audit.py",
    "work/moneybench/moneybench/environment_report.py",
    "work/moneybench/moneybench/env.py",
    "work/moneybench/moneybench/experiment_runbook.py",
    "work/moneybench/moneybench/failure_mode_audit.py",
    "work/moneybench/moneybench/holdout_smoke.py",
    "work/moneybench/moneybench/human_calibration.py",
    "work/moneybench/moneybench/human_calibration_analysis.py",
    "work/moneybench/moneybench/human_calibration_packet.py",
    "work/moneybench/moneybench/human_calibration_schema.py",
    "work/moneybench/moneybench/leaderboard_policy.py",
    "work/moneybench/moneybench/leaderboard_stability.py",
    "work/moneybench/moneybench/market_catalog.py",
    "work/moneybench/moneybench/tasks.py",
    "work/moneybench/moneybench/task_cards.py",
    "work/moneybench/moneybench/task_feasibility_audit.py",
    "work/moneybench/moneybench/task_runner.py",
    "work/moneybench/moneybench/task_provenance.py",
    "work/moneybench/moneybench/task_revision_ledger.py",
    "work/moneybench/moneybench/policies.py",
    "work/moneybench/moneybench/difficulty_calibration.py",
    "work/moneybench/moneybench/llm_policy.py",
    "work/moneybench/moneybench/metric_sensitivity.py",
    "work/moneybench/moneybench/model_comparison.py",
    "work/moneybench/moneybench/model_result_cards.py",
    "work/moneybench/moneybench/paper_claim_lint.py",
    "work/moneybench/moneybench/paper_evidence_map.py",
    "work/moneybench/moneybench/paper_figures.py",
    "work/moneybench/moneybench/paired_statistics.py",
    "work/moneybench/moneybench/power_analysis.py",
    "work/moneybench/moneybench/prompt_protocol.py",
    "work/moneybench/moneybench/private_holdout_evaluator.py",
    "work/moneybench/moneybench/provider_comparability_audit.py",
    "work/moneybench/moneybench/provider_contract_audit.py",
    "work/moneybench/moneybench/provider_run_status.py",
    "work/moneybench/moneybench/release_metadata.py",
    "work/moneybench/moneybench/responsible_use.py",
    "work/moneybench/moneybench/result_integrity_audit.py",
    "work/moneybench/moneybench/reviewer_risk_audit.py",
    "work/moneybench/moneybench/reviewer_smoke.py",
    "work/moneybench/moneybench/simulator_invariant_audit.py",
    "work/moneybench/moneybench/scoring_consistency_audit.py",
    "work/moneybench/moneybench/statistical_protocol.py",
    "work/moneybench/moneybench/submission.py",
    "work/moneybench/moneybench/submission_action_plan.py",
    "work/moneybench/moneybench/submission_bundle.py",
    "work/moneybench/moneybench/submission_manifest.py",
    "work/moneybench/moneybench/submission_schema.py",
    "work/moneybench/moneybench/release.py",
    "work/moneybench/moneybench/resumable_runner.py",
    "work/moneybench/tests/test_moneybench.py",
    "work/moneybench/README.md",
    "work/moneybench/SPEC.md",
    "work/moneybench/CITATION.cff",
    "work/moneybench/CITATION.cff.template",
    "work/moneybench/LICENSE-TODO.md",
    "work/moneybench/LICENSE.template",
]


CORE_OUTPUT_PATHS = [
    "outputs/acceleratorbench-task-manifest-v0.3.json",
    "outputs/acceleratorbench-task-coverage-v0.3.md",
    "outputs/acceleratorbench-task-provenance-v0.3.md",
    "outputs/acceleratorbench-task-provenance-v0.3.json",
    "outputs/acceleratorbench-task-cards-v0.3.md",
    "outputs/acceleratorbench-task-cards-v0.3.json",
    "outputs/acceleratorbench-action-semantics-v0.3.md",
    "outputs/acceleratorbench-action-semantics-v0.3.json",
    "outputs/acceleratorbench-datasheet-v0.3.md",
    "outputs/acceleratorbench-datasheet-v0.3.json",
    "outputs/acceleratorbench-market-catalog-v0.3.md",
    "outputs/acceleratorbench-market-catalog-v0.3.json",
    "outputs/acceleratorbench-score-rubric-v0.3.md",
    "outputs/acceleratorbench-scoring-consistency-audit-v0.3.md",
    "outputs/acceleratorbench-scoring-consistency-audit-v0.3.json",
    "outputs/acceleratorbench-metric-sensitivity-v0.3.md",
    "outputs/acceleratorbench-metric-sensitivity-v0.3.json",
    "outputs/acceleratorbench-baseline-raw-v0.3.json",
    "outputs/acceleratorbench-baseline-leaderboard-v0.3.json",
    "outputs/acceleratorbench-leaderboard-policy-v0.3.md",
    "outputs/acceleratorbench-leaderboard-policy-v0.3.json",
    "outputs/acceleratorbench-leaderboard-stability-v0.3.md",
    "outputs/acceleratorbench-leaderboard-stability-v0.3.json",
    "outputs/acceleratorbench-baseline-analysis-v0.3.md",
    "outputs/acceleratorbench-result-integrity-audit-v0.3.md",
    "outputs/acceleratorbench-result-integrity-audit-v0.3.json",
    "outputs/acceleratorbench-paper-tables-v0.3.md",
    "outputs/acceleratorbench-paper-figure-data-v0.3.md",
    "outputs/acceleratorbench-paper-figure-data-v0.3.json",
    "outputs/acceleratorbench-paper-evidence-map-v0.3.md",
    "outputs/acceleratorbench-paper-evidence-map-v0.3.json",
    "outputs/acceleratorbench-paper-claim-lint-v0.3.md",
    "outputs/acceleratorbench-paper-claim-lint-v0.3.json",
    "outputs/acceleratorbench-citation-audit-v0.3.md",
    "outputs/acceleratorbench-citation-audit-v0.3.json",
    "outputs/acceleratorbench-model-comparison-v0.3.md",
    "outputs/acceleratorbench-model-comparison-v0.3.json",
    "outputs/acceleratorbench-model-result-cards-v0.3.md",
    "outputs/acceleratorbench-model-result-cards-v0.3.json",
    "outputs/acceleratorbench-ablation-report-v0.3.md",
    "outputs/acceleratorbench-action-ablation-v0.3.md",
    "outputs/acceleratorbench-action-ablation-v0.3.json",
    "outputs/acceleratorbench-paired-statistics-v0.3.md",
    "outputs/acceleratorbench-paired-statistics-v0.3.json",
    "outputs/acceleratorbench-power-analysis-v0.3.md",
    "outputs/acceleratorbench-power-analysis-v0.3.json",
    "outputs/acceleratorbench-statistical-protocol-v0.3.md",
    "outputs/acceleratorbench-statistical-protocol-v0.3.json",
    "outputs/acceleratorbench-difficulty-calibration-v0.3.md",
    "outputs/acceleratorbench-difficulty-calibration-v0.3.json",
    "outputs/acceleratorbench-task-feasibility-audit-v0.3.md",
    "outputs/acceleratorbench-task-feasibility-audit-v0.3.json",
    "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
    "outputs/acceleratorbench-task-revision-ledger-v0.3.json",
    "outputs/acceleratorbench-determinism-audit-v0.3.md",
    "outputs/acceleratorbench-determinism-audit-v0.3.json",
    "outputs/acceleratorbench-environment-report-v0.3.md",
    "outputs/acceleratorbench-environment-report-v0.3.json",
    "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
    "outputs/acceleratorbench-simulator-invariant-audit-v0.3.json",
    "outputs/acceleratorbench-reviewer-smoke-v0.3.md",
    "outputs/acceleratorbench-reviewer-smoke-v0.3.json",
    "outputs/acceleratorbench-random-repeats-v0.3.md",
    "outputs/acceleratorbench-qualitative-traces-v0.3.md",
    "outputs/acceleratorbench-experiment-matrix-v0.3.md",
    "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
    "outputs/acceleratorbench-human-calibration-protocol-v0.3.json",
    "outputs/acceleratorbench-human-calibration-schema-v0.3.md",
    "outputs/acceleratorbench-human-calibration-schema-v0.3.json",
    "outputs/acceleratorbench-human-calibration-template-v0.3.json",
    "outputs/acceleratorbench-human-calibration-analysis-v0.3.md",
    "outputs/acceleratorbench-human-calibration-analysis-v0.3.json",
    "outputs/acceleratorbench-human-calibration-packet-v0.3.md",
    "outputs/acceleratorbench-human-calibration-packet-v0.3.json",
    "outputs/acceleratorbench-private-holdout-smoke-v0.3.md",
    "outputs/acceleratorbench-private-holdout-smoke-v0.3.json",
    "outputs/acceleratorbench-model-submission-schema-v0.3.md",
    "outputs/acceleratorbench-model-submission-schema-v0.3.json",
    "outputs/acceleratorbench-submission-bundle-protocol-v0.3.md",
    "outputs/acceleratorbench-submission-bundle-protocol-v0.3.json",
    "outputs/acceleratorbench-prompt-protocol-v0.3.md",
    "outputs/acceleratorbench-prompt-protocol-v0.3.json",
    "outputs/acceleratorbench-release-metadata-checklist-v0.3.md",
    "outputs/acceleratorbench-release-metadata-checklist-v0.3.json",
    "outputs/acceleratorbench-cost-accounting-v0.3.md",
    "outputs/acceleratorbench-cost-accounting-v0.3.json",
    "outputs/acceleratorbench-submission-action-plan-v0.3.md",
    "outputs/acceleratorbench-submission-action-plan-v0.3.json",
    "outputs/acceleratorbench-completion-audit-v0.3.md",
    "outputs/acceleratorbench-completion-audit-v0.3.json",
    "outputs/acceleratorbench-submission-manifest-v0.3.md",
    "outputs/acceleratorbench-submission-manifest-v0.3.json",
    "outputs/acceleratorbench-reviewer-risk-audit-v0.3.md",
    "outputs/acceleratorbench-reviewer-risk-audit-v0.3.json",
    "outputs/acceleratorbench-responsible-use-v0.3.md",
    "outputs/acceleratorbench-responsible-use-v0.3.json",
    "outputs/acceleratorbench-failure-mode-audit-v0.3.md",
    "outputs/acceleratorbench-failure-mode-audit-v0.3.json",
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
    "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
    "outputs/acceleratorbench-contamination-leakage-audit-v0.3.json",
]


REPRODUCTION_COMMANDS = [
    {
        "purpose": "Regenerate all generated v0.3 artifacts",
        "cwd": "work/moneybench",
        "command": "python -m moneybench.release regenerate",
    },
    {
        "purpose": "Run tests and validate required outputs",
        "cwd": "work/moneybench",
        "command": "python -m moneybench.release validate",
    },
    {
        "purpose": "Build supplementary release bundle",
        "cwd": "work/moneybench",
        "command": "python -m moneybench.release bundle",
    },
]


SECRET_ENV_NAMES = [
    "DEEPSEEK_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "OPENAI_COMPAT_API_KEY",
]

SECRET_PATTERNS = [
    re.compile(r"sk" r"-ant-api[0-9A-Za-z_-]{8,}", re.IGNORECASE),
    re.compile(r"sk-[0-9a-f]{32,}", re.IGNORECASE),
    re.compile(r"AQ\.[0-9A-Za-z_-]{8,}", re.IGNORECASE),
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


def git_commit() -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        )
    except Exception:
        return None
    commit = result.stdout.strip()
    return commit or None


def build_manifest() -> dict[str, Any]:
    source_files = [file_entry(path) for path in CORE_SOURCE_PATHS]
    output_files = [file_entry(path) for path in CORE_OUTPUT_PATHS]
    secret_env_presence = {name: "set_or_unset_not_recorded" for name in SECRET_ENV_NAMES}
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Source-workspace reproducibility manifest for the v0.3 supplementary artifact.",
        "environment": {
            "python_version": sys.version.split()[0],
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "working_directory": str(PACKAGE_ROOT),
            "git_commit": git_commit(),
            "secret_env_presence": secret_env_presence,
        },
        "commands": REPRODUCTION_COMMANDS,
        "source_files": source_files,
        "output_files": output_files,
        "summary": {
            "source_files": len(source_files),
            "source_files_present": sum(1 for entry in source_files if entry["exists"]),
            "output_files": len(output_files),
            "output_files_present": sum(1 for entry in output_files if entry["exists"]),
            "secret_values_recorded": False,
        },
    }


def validate_manifest(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload["version"] != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload['version']}.")
    if payload["summary"]["source_files"] != payload["summary"]["source_files_present"]:
        problems.append("Some core source files are missing.")
    if payload["summary"]["output_files"] != payload["summary"]["output_files_present"]:
        problems.append("Some core output files are missing.")
    if payload["summary"]["secret_values_recorded"]:
        problems.append("Manifest must not record secret values.")
    text = json.dumps(payload)
    if any(pattern.search(text) for pattern in SECRET_PATTERNS):
        problems.append("Manifest appears to contain secret-looking material.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    env = payload["environment"]
    source_rows = [[entry["path"], entry["exists"], entry.get("bytes", ""), entry.get("sha256", "")] for entry in payload["source_files"]]
    output_rows = [[entry["path"], entry["exists"], entry.get("bytes", ""), entry.get("sha256", "")] for entry in payload["output_files"]]
    command_rows = [[row["purpose"], row["cwd"], f"`{row['command']}`"] for row in payload["commands"]]
    lines = [
        "# FounderBench v0.3 Reproducibility Manifest",
        "",
        "This generated manifest records the source/output hashes and reproduction commands for the current workspace. It records only secret variable names, never secret values.",
        "",
        "## Environment",
        "",
        markdown_table(
            ["Field", "Value"],
            [
                ["Python", env["python_version"]],
                ["Python executable", env["python_executable"]],
                ["Platform", env["platform"]],
                ["Machine", env["machine"]],
                ["Working directory", env["working_directory"]],
                ["Git commit", env["git_commit"] or "not available"],
                ["Secret values recorded", payload["summary"]["secret_values_recorded"]],
            ],
        ),
        "",
        "## Commands",
        "",
        markdown_table(["Purpose", "Working Directory", "Command"], command_rows),
        "",
        "## Core Source Files",
        "",
        markdown_table(["Path", "Exists", "Bytes", "SHA-256"], source_rows),
        "",
        "## Core Output Files",
        "",
        markdown_table(["Path", "Exists", "Bytes", "SHA-256"], output_rows),
        "",
        "## Validation",
        "",
    ]
    problems = validate_manifest(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All listed core source and output files are present, and no secret values are recorded.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_manifest(json_output: Path, markdown_output: Path) -> None:
    payload = build_manifest()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reproducibility manifest.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_manifest(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
