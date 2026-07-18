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
PACKAGE_ROOT = ROOT / "work" / "founderbench"
VERSION = "0.3.0"


CORE_SOURCE_PATHS = [
    "work/founderbench/founderbench/action_ablation.py",
    "work/founderbench/founderbench/action_semantics.py",
    "work/founderbench/founderbench/baseline_execution_plan.py",
    "work/founderbench/founderbench/benchmark_datasheet.py",
    "work/founderbench/founderbench/bundle_integrity.py",
    "work/founderbench/founderbench/citation_audit.py",
    "work/founderbench/founderbench/completion_audit.py",
    "work/founderbench/founderbench/contamination_leakage_audit.py",
    "work/founderbench/founderbench/cost_accounting.py",
    "work/founderbench/founderbench/determinism_audit.py",
    "work/founderbench/founderbench/environment_report.py",
    "work/founderbench/founderbench/env.py",
    "work/founderbench/founderbench/experiment_runbook.py",
    "work/founderbench/founderbench/failure_mode_audit.py",
    "work/founderbench/founderbench/holdout_smoke.py",
    "work/founderbench/founderbench/human_calibration.py",
    "work/founderbench/founderbench/human_calibration_analysis.py",
    "work/founderbench/founderbench/human_calibration_packet.py",
    "work/founderbench/founderbench/human_calibration_schema.py",
    "work/founderbench/founderbench/leaderboard_policy.py",
    "work/founderbench/founderbench/leaderboard_stability.py",
    "work/founderbench/founderbench/market_catalog.py",
    "work/founderbench/founderbench/tasks.py",
    "work/founderbench/founderbench/task_cards.py",
    "work/founderbench/founderbench/task_feasibility_audit.py",
    "work/founderbench/founderbench/task_runner.py",
    "work/founderbench/founderbench/task_provenance.py",
    "work/founderbench/founderbench/task_revision_ledger.py",
    "work/founderbench/founderbench/policies.py",
    "work/founderbench/founderbench/difficulty_calibration.py",
    "work/founderbench/founderbench/llm_policy.py",
    "work/founderbench/founderbench/metric_sensitivity.py",
    "work/founderbench/founderbench/model_comparison.py",
    "work/founderbench/founderbench/model_result_cards.py",
    "work/founderbench/founderbench/paper_claim_lint.py",
    "work/founderbench/founderbench/paper_evidence_map.py",
    "work/founderbench/founderbench/paper_figures.py",
    "work/founderbench/founderbench/paired_statistics.py",
    "work/founderbench/founderbench/power_analysis.py",
    "work/founderbench/founderbench/prompt_protocol.py",
    "work/founderbench/founderbench/private_holdout_evaluator.py",
    "work/founderbench/founderbench/provider_comparability_audit.py",
    "work/founderbench/founderbench/provider_contract_audit.py",
    "work/founderbench/founderbench/provider_run_status.py",
    "work/founderbench/founderbench/release_metadata.py",
    "work/founderbench/founderbench/responsible_use.py",
    "work/founderbench/founderbench/result_integrity_audit.py",
    "work/founderbench/founderbench/reviewer_risk_audit.py",
    "work/founderbench/founderbench/reviewer_smoke.py",
    "work/founderbench/founderbench/simulator_invariant_audit.py",
    "work/founderbench/founderbench/scoring_consistency_audit.py",
    "work/founderbench/founderbench/statistical_protocol.py",
    "work/founderbench/founderbench/submission.py",
    "work/founderbench/founderbench/submission_action_plan.py",
    "work/founderbench/founderbench/submission_bundle.py",
    "work/founderbench/founderbench/submission_manifest.py",
    "work/founderbench/founderbench/submission_schema.py",
    "work/founderbench/founderbench/release.py",
    "work/founderbench/founderbench/resumable_runner.py",
    "work/founderbench/tests/test_founderbench.py",
    "work/founderbench/README.md",
    "work/founderbench/SPEC.md",
    "work/founderbench/CITATION.cff",
    "work/founderbench/CITATION.cff.template",
    "work/founderbench/LICENSE-TODO.md",
    "work/founderbench/LICENSE.template",
]


CORE_OUTPUT_PATHS = [
    "outputs/founderbench-task-manifest.json",
    "outputs/founderbench-task-coverage.md",
    "outputs/founderbench-task-provenance.md",
    "outputs/founderbench-task-provenance.json",
    "outputs/founderbench-task-cards.md",
    "outputs/founderbench-task-cards.json",
    "outputs/founderbench-action-semantics.md",
    "outputs/founderbench-action-semantics.json",
    "outputs/founderbench-datasheet.md",
    "outputs/founderbench-datasheet.json",
    "outputs/founderbench-market-catalog.md",
    "outputs/founderbench-market-catalog.json",
    "outputs/founderbench-score-rubric.md",
    "outputs/founderbench-scoring-consistency-audit.md",
    "outputs/founderbench-scoring-consistency-audit.json",
    "outputs/founderbench-metric-sensitivity.md",
    "outputs/founderbench-metric-sensitivity.json",
    "outputs/founderbench-baseline-raw.json",
    "outputs/founderbench-baseline-leaderboard.json",
    "outputs/founderbench-leaderboard-policy.md",
    "outputs/founderbench-leaderboard-policy.json",
    "outputs/founderbench-leaderboard-stability.md",
    "outputs/founderbench-leaderboard-stability.json",
    "outputs/founderbench-baseline-analysis.md",
    "outputs/founderbench-result-integrity-audit.md",
    "outputs/founderbench-result-integrity-audit.json",
    "outputs/founderbench-paper-tables.md",
    "outputs/founderbench-paper-figure-data.md",
    "outputs/founderbench-paper-figure-data.json",
    "outputs/founderbench-paper-evidence-map.md",
    "outputs/founderbench-paper-evidence-map.json",
    "outputs/founderbench-paper-claim-lint.md",
    "outputs/founderbench-paper-claim-lint.json",
    "outputs/founderbench-citation-audit.md",
    "outputs/founderbench-citation-audit.json",
    "outputs/founderbench-model-comparison.md",
    "outputs/founderbench-model-comparison.json",
    "outputs/founderbench-model-result-cards.md",
    "outputs/founderbench-model-result-cards.json",
    "outputs/founderbench-ablation-report.md",
    "outputs/founderbench-action-ablation.md",
    "outputs/founderbench-action-ablation.json",
    "outputs/founderbench-paired-statistics.md",
    "outputs/founderbench-paired-statistics.json",
    "outputs/founderbench-power-analysis.md",
    "outputs/founderbench-power-analysis.json",
    "outputs/founderbench-statistical-protocol.md",
    "outputs/founderbench-statistical-protocol.json",
    "outputs/founderbench-difficulty-calibration.md",
    "outputs/founderbench-difficulty-calibration.json",
    "outputs/founderbench-task-feasibility-audit.md",
    "outputs/founderbench-task-feasibility-audit.json",
    "outputs/founderbench-task-revision-ledger.md",
    "outputs/founderbench-task-revision-ledger.json",
    "outputs/founderbench-determinism-audit.md",
    "outputs/founderbench-determinism-audit.json",
    "outputs/founderbench-environment-report.md",
    "outputs/founderbench-environment-report.json",
    "outputs/founderbench-simulator-invariant-audit.md",
    "outputs/founderbench-simulator-invariant-audit.json",
    "outputs/founderbench-reviewer-smoke.md",
    "outputs/founderbench-reviewer-smoke.json",
    "outputs/founderbench-random-repeats.md",
    "outputs/founderbench-qualitative-traces.md",
    "outputs/founderbench-experiment-matrix.md",
    "outputs/founderbench-human-calibration-protocol.md",
    "outputs/founderbench-human-calibration-protocol.json",
    "outputs/founderbench-human-calibration-schema.md",
    "outputs/founderbench-human-calibration-schema.json",
    "outputs/founderbench-human-calibration-template.json",
    "outputs/founderbench-human-calibration-analysis.md",
    "outputs/founderbench-human-calibration-analysis.json",
    "outputs/founderbench-human-calibration-packet.md",
    "outputs/founderbench-human-calibration-packet.json",
    "outputs/founderbench-private-holdout-smoke.md",
    "outputs/founderbench-private-holdout-smoke.json",
    "outputs/founderbench-model-submission-schema.md",
    "outputs/founderbench-model-submission-schema.json",
    "outputs/founderbench-submission-bundle-protocol.md",
    "outputs/founderbench-submission-bundle-protocol.json",
    "outputs/founderbench-prompt-protocol.md",
    "outputs/founderbench-prompt-protocol.json",
    "outputs/founderbench-release-metadata-checklist.md",
    "outputs/founderbench-release-metadata-checklist.json",
    "outputs/founderbench-cost-accounting.md",
    "outputs/founderbench-cost-accounting.json",
    "outputs/founderbench-submission-action-plan.md",
    "outputs/founderbench-submission-action-plan.json",
    "outputs/founderbench-completion-audit.md",
    "outputs/founderbench-completion-audit.json",
    "outputs/founderbench-submission-manifest.md",
    "outputs/founderbench-submission-manifest.json",
    "outputs/founderbench-reviewer-risk-audit.md",
    "outputs/founderbench-reviewer-risk-audit.json",
    "outputs/founderbench-responsible-use.md",
    "outputs/founderbench-responsible-use.json",
    "outputs/founderbench-failure-mode-audit.md",
    "outputs/founderbench-failure-mode-audit.json",
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
    "outputs/founderbench-contamination-leakage-audit.md",
    "outputs/founderbench-contamination-leakage-audit.json",
]


REPRODUCTION_COMMANDS = [
    {
        "purpose": "Regenerate all generated current release artifacts",
        "cwd": "work/founderbench",
        "command": "python -m founderbench.release regenerate",
    },
    {
        "purpose": "Run tests and validate required outputs",
        "cwd": "work/founderbench",
        "command": "python -m founderbench.release validate",
    },
    {
        "purpose": "Build supplementary release bundle",
        "cwd": "work/founderbench",
        "command": "python -m founderbench.release bundle",
    },
]


SECRET_ENV_NAMES = [
    "DEEPSEEK_API_KEY",
    "ANTHROPIC_API_KEY",
    "GEMINI_API_KEY",
    "FOUNDERBENCH_COMPAT_API_KEY",
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
        "purpose": "Source-workspace reproducibility manifest for the current release supplementary artifact.",
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
        "# FounderBench Reproducibility Manifest",
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
