from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

from .action_ablation import write_report as write_action_ablation_report
from .action_semantics import write_catalog as write_action_semantics
from .ablation import write_report as write_ablation_report
from .analysis import write_report
from .baseline_execution_plan import write_plan as write_baseline_execution_plan
from .benchmark_datasheet import write_datasheet as write_benchmark_datasheet
from .bundle_integrity import write_report as write_bundle_integrity_report
from .citation_audit import write_audit as write_citation_audit
from .claim_evidence import write_report as write_claim_evidence_report
from .completion_audit import write_audit as write_completion_audit
from .contamination_leakage_audit import write_audit as write_contamination_leakage_audit
from .cost_accounting import write_protocol as write_cost_accounting_protocol
from .difficulty_calibration import write_report as write_difficulty_calibration_report
from .determinism_audit import write_audit as write_determinism_audit
from .environment_report import write_report as write_environment_report
from .experiment_runbook import write_runbook as write_experiment_runbook
from .export_tasks import task_manifest
from .experiment_matrix import write_matrix as write_experiment_matrix
from .failure_mode_audit import write_audit as write_failure_mode_audit
from .holdout import evaluator_protocol, write_evaluator_protocol_markdown
from .holdout_smoke import write_report as write_holdout_smoke_report
from .human_calibration import write_protocol as write_human_calibration_protocol
from .human_calibration_analysis import write_analysis as write_human_calibration_analysis
from .human_calibration_packet import write_packet as write_human_calibration_packet
from .human_calibration_schema import write_schema as write_human_calibration_schema
from .leaderboard import summarize
from .leaderboard_policy import write_policy as write_leaderboard_policy
from .leaderboard_stability import write_audit as write_leaderboard_stability_audit
from .license_readiness import write_report as write_license_readiness_report
from .local_model import write_protocol as write_local_model_protocol
from .market_catalog import write_catalog as write_market_catalog
from .metric_sensitivity import write_report as write_metric_sensitivity_report
from .model_comparison import write_report as write_model_comparison_report
from .model_result_cards import write_cards as write_model_result_cards
from .paper_figures import write_figure_data as write_paper_figure_data
from .paper_claim_lint import write_audit as write_paper_claim_lint
from .paper_evidence_map import write_map as write_paper_evidence_map
from .paper_tables import write_tables as write_paper_tables
from .paired_statistics import write_report as write_paired_statistics_report
from .power_analysis import write_analysis as write_power_analysis
from .prompt_protocol import write_protocol as write_prompt_protocol
from .provider_comparability_audit import write_audit as write_provider_comparability_audit
from .provider_contract_audit import write_audit as write_provider_contract_audit
from .provider_readiness import write_readiness as write_provider_readiness
from .provider_run_status import write_status as write_provider_run_status
from .qualitative import build_trace_examples, write_markdown as write_trace_markdown
from .references import write_reference_artifacts
from .repeats import run_repeated, write_report as write_repeated_report
from .publication_audit import write_audit as write_publication_audit
from .release_metadata import write_checklist as write_release_metadata_checklist
from .reproducibility_manifest import write_manifest as write_reproducibility_manifest
from .result_integrity_audit import write_audit as write_result_integrity_audit
from .responsible_use import write_statement as write_responsible_use_statement
from .reviewer_index import write_index as write_reviewer_index
from .reviewer_risk_audit import write_audit as write_reviewer_risk_audit
from .reviewer_smoke import write_report as write_reviewer_smoke_report
from .score_rubric import write_rubric as write_score_rubric
from .scoring_consistency_audit import write_audit as write_scoring_consistency_audit
from .simulator_invariant_audit import write_audit as write_simulator_invariant_audit
from .statistical_protocol import write_protocol as write_statistical_protocol
from .submission import write_submission_report
from .submission_action_plan import write_plan as write_submission_action_plan
from .submission_bundle import write_protocol as write_submission_bundle_protocol
from .submission_gate import write_gate as write_submission_gate
from .submission_manifest import write_manifest as write_submission_manifest
from .submission_schema import write_schema as write_submission_schema
from .task_cards import write_cards as write_task_cards
from .task_coverage import write_coverage as write_task_coverage
from .task_feasibility_audit import write_audit as write_task_feasibility_audit
from .task_provenance import write_provenance as write_task_provenance
from .task_revision_ledger import write_ledger as write_task_revision_ledger
from .task_runner import run_suite
from .validity_report import write_report as write_validity_report


PACKAGE_ROOT = Path(__file__).resolve().parents[1]


def _default_workspace_root() -> Path:
    """Support both this Codex workspace layout and a standalone GitHub clone."""
    if PACKAGE_ROOT.parent.name == "work":
        return PACKAGE_ROOT.parents[1]
    return PACKAGE_ROOT


ROOT = _default_workspace_root()
OUTPUTS = Path(os.environ.get("FOUNDERBENCH_OUTPUTS", ROOT / "outputs"))
RELEASE_ROOT = Path(os.environ.get("FOUNDERBENCH_RELEASE_ROOT", ROOT / "release"))
VERSION = "0.3.0"


REQUIRED_OUTPUTS = [
    "founderbench-task-manifest.json",
    "founderbench-task-coverage.json",
    "founderbench-task-coverage.md",
    "founderbench-task-provenance.json",
    "founderbench-task-provenance.md",
    "founderbench-task-cards.json",
    "founderbench-task-cards.md",
    "founderbench-action-semantics.json",
    "founderbench-action-semantics.md",
    "founderbench-market-catalog.json",
    "founderbench-market-catalog.md",
    "founderbench-baseline-leaderboard.json",
    "founderbench-leaderboard-policy.json",
    "founderbench-leaderboard-policy.md",
    "founderbench-leaderboard-stability.json",
    "founderbench-leaderboard-stability.md",
    "founderbench-baseline-raw.json",
    "founderbench-baseline-analysis.md",
    "founderbench-result-integrity-audit.json",
    "founderbench-result-integrity-audit.md",
    "founderbench-paper-tables.json",
    "founderbench-paper-tables.md",
    "founderbench-paper-figure-data.json",
    "founderbench-paper-figure-data.md",
    "founderbench-model-result-cards.json",
    "founderbench-model-result-cards.md",
    "founderbench-paper-evidence-map.json",
    "founderbench-paper-evidence-map.md",
    "founderbench-paper-claim-lint.json",
    "founderbench-paper-claim-lint.md",
    "founderbench-model-comparison.json",
    "founderbench-model-comparison.md",
    "founderbench-ablation-report.md",
    "founderbench-action-ablation.json",
    "founderbench-action-ablation.md",
    "founderbench-difficulty-calibration.json",
    "founderbench-difficulty-calibration.md",
    "founderbench-task-feasibility-audit.json",
    "founderbench-task-feasibility-audit.md",
    "founderbench-task-revision-ledger.json",
    "founderbench-task-revision-ledger.md",
    "founderbench-qualitative-traces.json",
    "founderbench-qualitative-traces.md",
    "founderbench-random-repeats.json",
    "founderbench-random-repeats.md",
    "founderbench-benchmark-card.md",
    "founderbench-datasheet.json",
    "founderbench-datasheet.md",
    "founderbench-metrics-and-evaluation.md",
    "founderbench-metric-sensitivity.json",
    "founderbench-metric-sensitivity.md",
    "founderbench-paired-statistics.json",
    "founderbench-paired-statistics.md",
    "founderbench-power-analysis.json",
    "founderbench-power-analysis.md",
    "founderbench-statistical-protocol.json",
    "founderbench-statistical-protocol.md",
    "founderbench-score-rubric.json",
    "founderbench-score-rubric.md",
    "founderbench-scoring-consistency-audit.json",
    "founderbench-scoring-consistency-audit.md",
    "founderbench-reproduction-guide.md",
    "founderbench-reviewer-smoke.json",
    "founderbench-reviewer-smoke.md",
    "founderbench-environment-report.json",
    "founderbench-environment-report.md",
    "founderbench-simulator-invariant-audit.json",
    "founderbench-simulator-invariant-audit.md",
    "founderbench-model-submission-template.md",
    "founderbench-model-submission-schema.json",
    "founderbench-model-submission-schema.md",
    "founderbench-submission-bundle-protocol.json",
    "founderbench-submission-bundle-protocol.md",
    "founderbench-local-openai-compatible-protocol.json",
    "founderbench-local-openai-compatible-protocol.md",
    "founderbench-prompt-protocol.json",
    "founderbench-prompt-protocol.md",
    "founderbench-provider-readiness.json",
    "founderbench-provider-readiness.md",
    "founderbench-cost-accounting.json",
    "founderbench-cost-accounting.md",
    "founderbench-baseline-execution-plan.json",
    "founderbench-baseline-execution-plan.md",
    "founderbench-experiment-runbook.json",
    "founderbench-experiment-runbook.md",
    "founderbench-provider-run-status.json",
    "founderbench-provider-run-status.md",
    "founderbench-provider-comparability-audit.json",
    "founderbench-provider-comparability-audit.md",
    "founderbench-provider-contract-audit.json",
    "founderbench-provider-contract-audit.md",
    "founderbench-contamination-leakage-audit.json",
    "founderbench-contamination-leakage-audit.md",
    "founderbench-license-readiness.json",
    "founderbench-license-readiness.md",
    "founderbench-release-metadata-checklist.json",
    "founderbench-release-metadata-checklist.md",
    "founderbench-submission-validation.md",
    "founderbench-private-holdout-blueprint.json",
    "founderbench-private-holdout-evaluator-protocol.json",
    "founderbench-private-holdout-evaluator-protocol.md",
    "founderbench-private-holdout-smoke.json",
    "founderbench-private-holdout-smoke.md",
    "founderbench-human-calibration-protocol.json",
    "founderbench-human-calibration-protocol.md",
    "founderbench-human-calibration-schema.json",
    "founderbench-human-calibration-schema.md",
    "founderbench-human-calibration-template.json",
    "founderbench-human-calibration-analysis.json",
    "founderbench-human-calibration-analysis.md",
    "founderbench-human-calibration-packet.json",
    "founderbench-human-calibration-packet.md",
    "founderbench-paper-draft.md",
    "founderbench-references.bib",
    "founderbench-reference-provenance.json",
    "founderbench-citation-audit.json",
    "founderbench-citation-audit.md",
    "founderbench-reproducibility-manifest.json",
    "founderbench-reproducibility-manifest.md",
    "founderbench-determinism-audit.json",
    "founderbench-determinism-audit.md",
    "founderbench-validity-report.json",
    "founderbench-validity-report.md",
    "founderbench-responsible-use.json",
    "founderbench-responsible-use.md",
    "founderbench-claim-evidence.json",
    "founderbench-claim-evidence.md",
    "founderbench-completion-audit.json",
    "founderbench-completion-audit.md",
    "founderbench-submission-manifest.json",
    "founderbench-submission-manifest.md",
    "founderbench-reviewer-risk-audit.json",
    "founderbench-reviewer-risk-audit.md",
    "founderbench-failure-mode-audit.json",
    "founderbench-failure-mode-audit.md",
    "founderbench-submission-gate.json",
    "founderbench-submission-gate.md",
    "founderbench-submission-action-plan.json",
    "founderbench-submission-action-plan.md",
    "founderbench-related-work-notes.md",
    "founderbench-experiment-matrix.json",
    "founderbench-experiment-matrix.md",
    "founderbench-reviewer-index.json",
    "founderbench-reviewer-index.md",
    "founderbench-publication-audit.json",
    "founderbench-publication-audit.md",
    "founderbench-supplementary-package-checklist.md",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_tests() -> None:
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=PACKAGE_ROOT,
        check=True,
    )


def regenerate() -> None:
    OUTPUTS.mkdir(parents=True, exist_ok=True)
    (OUTPUTS / "founderbench-task-manifest.json").write_text(
        json.dumps(task_manifest(), indent=2),
        encoding="utf-8",
    )
    write_task_coverage(
        OUTPUTS / "founderbench-task-coverage.json",
        OUTPUTS / "founderbench-task-coverage.md",
    )
    write_task_provenance(
        OUTPUTS / "founderbench-task-provenance.json",
        OUTPUTS / "founderbench-task-provenance.md",
    )
    write_task_cards(
        OUTPUTS / "founderbench-task-cards.json",
        OUTPUTS / "founderbench-task-cards.md",
    )
    write_action_semantics(
        OUTPUTS / "founderbench-action-semantics.json",
        OUTPUTS / "founderbench-action-semantics.md",
    )
    write_market_catalog(
        OUTPUTS / "founderbench-market-catalog.json",
        OUTPUTS / "founderbench-market-catalog.md",
    )
    raw = [run_suite(policy) for policy in ["random", "conservative", "heuristic", "task_heuristic"]]
    leaderboard = {
        "benchmark": "FounderBench",
        "version": VERSION,
        "rows": sorted([summarize(result) for result in raw], key=lambda row: row["average_task_score"], reverse=True),
    }
    (OUTPUTS / "founderbench-baseline-raw.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    (OUTPUTS / "founderbench-baseline-leaderboard.json").write_text(json.dumps(leaderboard, indent=2), encoding="utf-8")
    write_leaderboard_policy(
        OUTPUTS / "founderbench-leaderboard-policy.json",
        OUTPUTS / "founderbench-leaderboard-policy.md",
    )
    write_leaderboard_stability_audit(
        OUTPUTS / "founderbench-leaderboard-stability.json",
        OUTPUTS / "founderbench-leaderboard-stability.md",
    )
    write_report(raw, OUTPUTS / "founderbench-baseline-analysis.md")
    write_paper_tables(
        OUTPUTS / "founderbench-paper-tables.json",
        OUTPUTS / "founderbench-paper-tables.md",
    )
    write_paper_figure_data(
        OUTPUTS / "founderbench-paper-figure-data.json",
        OUTPUTS / "founderbench-paper-figure-data.md",
    )
    write_task_revision_ledger(
        OUTPUTS / "founderbench-task-revision-ledger.json",
        OUTPUTS / "founderbench-task-revision-ledger.md",
    )
    write_model_comparison_report(
        OUTPUTS / "founderbench-model-comparison.json",
        OUTPUTS / "founderbench-model-comparison.md",
    )
    write_result_integrity_audit(
        OUTPUTS / "founderbench-result-integrity-audit.json",
        OUTPUTS / "founderbench-result-integrity-audit.md",
    )
    write_model_result_cards(
        OUTPUTS / "founderbench-model-result-cards.json",
        OUTPUTS / "founderbench-model-result-cards.md",
    )
    write_ablation_report(raw, OUTPUTS / "founderbench-ablation-report.md")
    write_action_ablation_report(
        OUTPUTS / "founderbench-action-ablation.json",
        OUTPUTS / "founderbench-action-ablation.md",
    )
    write_difficulty_calibration_report(
        OUTPUTS / "founderbench-difficulty-calibration.json",
        OUTPUTS / "founderbench-difficulty-calibration.md",
    )
    write_task_feasibility_audit(
        OUTPUTS / "founderbench-task-feasibility-audit.json",
        OUTPUTS / "founderbench-task-feasibility-audit.md",
    )
    qualitative = build_trace_examples(OUTPUTS / "founderbench-baseline-raw.json")
    (OUTPUTS / "founderbench-qualitative-traces.json").write_text(json.dumps(qualitative, indent=2), encoding="utf-8")
    write_trace_markdown(qualitative, OUTPUTS / "founderbench-qualitative-traces.md")
    repeated_random = run_repeated("random", [0, 1, 2, 3, 4])
    (OUTPUTS / "founderbench-random-repeats.json").write_text(json.dumps(repeated_random, indent=2), encoding="utf-8")
    write_repeated_report(repeated_random, OUTPUTS / "founderbench-random-repeats.md")
    write_benchmark_datasheet(
        OUTPUTS / "founderbench-datasheet.json",
        OUTPUTS / "founderbench-datasheet.md",
    )
    write_score_rubric(
        OUTPUTS / "founderbench-score-rubric.json",
        OUTPUTS / "founderbench-score-rubric.md",
    )
    write_scoring_consistency_audit(
        OUTPUTS / "founderbench-scoring-consistency-audit.json",
        OUTPUTS / "founderbench-scoring-consistency-audit.md",
    )
    write_metric_sensitivity_report(
        OUTPUTS / "founderbench-metric-sensitivity.json",
        OUTPUTS / "founderbench-metric-sensitivity.md",
    )
    write_paired_statistics_report(
        OUTPUTS / "founderbench-paired-statistics.json",
        OUTPUTS / "founderbench-paired-statistics.md",
    )
    write_power_analysis(
        OUTPUTS / "founderbench-power-analysis.json",
        OUTPUTS / "founderbench-power-analysis.md",
    )
    write_statistical_protocol(
        OUTPUTS / "founderbench-statistical-protocol.json",
        OUTPUTS / "founderbench-statistical-protocol.md",
    )
    write_reviewer_smoke_report(
        OUTPUTS / "founderbench-reviewer-smoke.json",
        OUTPUTS / "founderbench-reviewer-smoke.md",
    )
    write_reference_artifacts(
        OUTPUTS / "founderbench-references.bib",
        OUTPUTS / "founderbench-reference-provenance.json",
    )
    write_citation_audit(
        OUTPUTS / "founderbench-citation-audit.json",
        OUTPUTS / "founderbench-citation-audit.md",
    )
    write_local_model_protocol(OUTPUTS / "founderbench-local-openai-compatible-protocol.json")
    write_local_model_protocol(OUTPUTS / "founderbench-local-openai-compatible-protocol.md")
    write_prompt_protocol(
        OUTPUTS / "founderbench-prompt-protocol.json",
        OUTPUTS / "founderbench-prompt-protocol.md",
    )
    write_provider_readiness(
        OUTPUTS / "founderbench-provider-readiness.json",
        OUTPUTS / "founderbench-provider-readiness.md",
    )
    write_cost_accounting_protocol(
        OUTPUTS / "founderbench-cost-accounting.json",
        OUTPUTS / "founderbench-cost-accounting.md",
    )
    write_baseline_execution_plan(
        OUTPUTS / "founderbench-baseline-execution-plan.json",
        OUTPUTS / "founderbench-baseline-execution-plan.md",
    )
    write_experiment_runbook(
        OUTPUTS / "founderbench-experiment-runbook.json",
        OUTPUTS / "founderbench-experiment-runbook.md",
    )
    write_provider_run_status(
        OUTPUTS / "founderbench-provider-run-status.json",
        OUTPUTS / "founderbench-provider-run-status.md",
    )
    write_provider_comparability_audit(
        OUTPUTS / "founderbench-provider-comparability-audit.json",
        OUTPUTS / "founderbench-provider-comparability-audit.md",
    )
    write_provider_contract_audit(
        OUTPUTS / "founderbench-provider-contract-audit.json",
        OUTPUTS / "founderbench-provider-contract-audit.md",
    )
    write_contamination_leakage_audit(
        OUTPUTS / "founderbench-contamination-leakage-audit.json",
        OUTPUTS / "founderbench-contamination-leakage-audit.md",
    )
    write_license_readiness_report(
        OUTPUTS / "founderbench-license-readiness.json",
        OUTPUTS / "founderbench-license-readiness.md",
    )
    write_release_metadata_checklist(
        OUTPUTS / "founderbench-release-metadata-checklist.json",
        OUTPUTS / "founderbench-release-metadata-checklist.md",
    )
    (OUTPUTS / "founderbench-private-holdout-evaluator-protocol.json").write_text(
        json.dumps(evaluator_protocol(), indent=2),
        encoding="utf-8",
    )
    write_evaluator_protocol_markdown(OUTPUTS / "founderbench-private-holdout-evaluator-protocol.md")
    write_holdout_smoke_report(
        OUTPUTS / "founderbench-private-holdout-smoke.json",
        OUTPUTS / "founderbench-private-holdout-smoke.md",
    )
    write_human_calibration_protocol(
        OUTPUTS / "founderbench-human-calibration-protocol.json",
        OUTPUTS / "founderbench-human-calibration-protocol.md",
    )
    write_human_calibration_schema(
        OUTPUTS / "founderbench-human-calibration-schema.json",
        OUTPUTS / "founderbench-human-calibration-schema.md",
        OUTPUTS / "founderbench-human-calibration-template.json",
    )
    write_human_calibration_analysis(
        [],
        OUTPUTS / "founderbench-human-calibration-analysis.json",
        OUTPUTS / "founderbench-human-calibration-analysis.md",
    )
    write_human_calibration_packet(
        OUTPUTS / "founderbench-human-calibration-packet.json",
        OUTPUTS / "founderbench-human-calibration-packet.md",
    )
    write_submission_report(
        OUTPUTS / "founderbench-baseline-raw.json",
        OUTPUTS / "founderbench-submission-validation.md",
    )
    write_submission_schema(
        OUTPUTS / "founderbench-model-submission-schema.json",
        OUTPUTS / "founderbench-model-submission-schema.md",
    )
    write_submission_bundle_protocol(
        OUTPUTS / "founderbench-submission-bundle-protocol.json",
        OUTPUTS / "founderbench-submission-bundle-protocol.md",
    )
    write_experiment_matrix(
        OUTPUTS / "founderbench-experiment-matrix.json",
        OUTPUTS / "founderbench-experiment-matrix.md",
    )
    write_environment_report(
        OUTPUTS / "founderbench-environment-report.json",
        OUTPUTS / "founderbench-environment-report.md",
    )
    write_simulator_invariant_audit(
        OUTPUTS / "founderbench-simulator-invariant-audit.json",
        OUTPUTS / "founderbench-simulator-invariant-audit.md",
    )
    write_determinism_audit(
        OUTPUTS / "founderbench-determinism-audit.json",
        OUTPUTS / "founderbench-determinism-audit.md",
    )
    write_validity_report(
        OUTPUTS / "founderbench-validity-report.json",
        OUTPUTS / "founderbench-validity-report.md",
    )
    write_responsible_use_statement(
        OUTPUTS / "founderbench-responsible-use.json",
        OUTPUTS / "founderbench-responsible-use.md",
    )
    write_claim_evidence_report(
        OUTPUTS / "founderbench-claim-evidence.json",
        OUTPUTS / "founderbench-claim-evidence.md",
    )
    write_submission_gate(
        OUTPUTS / "founderbench-submission-gate.json",
        OUTPUTS / "founderbench-submission-gate.md",
    )
    write_completion_audit(
        OUTPUTS / "founderbench-completion-audit.json",
        OUTPUTS / "founderbench-completion-audit.md",
    )
    write_submission_manifest(
        OUTPUTS / "founderbench-submission-manifest.json",
        OUTPUTS / "founderbench-submission-manifest.md",
    )
    write_paper_evidence_map(
        OUTPUTS / "founderbench-paper-evidence-map.json",
        OUTPUTS / "founderbench-paper-evidence-map.md",
    )
    write_paper_claim_lint(
        OUTPUTS / "founderbench-paper-claim-lint.json",
        OUTPUTS / "founderbench-paper-claim-lint.md",
    )
    write_reviewer_risk_audit(
        OUTPUTS / "founderbench-reviewer-risk-audit.json",
        OUTPUTS / "founderbench-reviewer-risk-audit.md",
    )
    write_failure_mode_audit(
        OUTPUTS / "founderbench-failure-mode-audit.json",
        OUTPUTS / "founderbench-failure-mode-audit.md",
    )
    write_reproducibility_manifest(
        OUTPUTS / "founderbench-reproducibility-manifest.json",
        OUTPUTS / "founderbench-reproducibility-manifest.md",
    )
    write_submission_action_plan(
        OUTPUTS / "founderbench-submission-action-plan.json",
        OUTPUTS / "founderbench-submission-action-plan.md",
    )
    write_reviewer_index(
        OUTPUTS / "founderbench-reviewer-index.json",
        OUTPUTS / "founderbench-reviewer-index.md",
    )
    write_publication_audit(
        OUTPUTS / "founderbench-publication-audit.json",
        OUTPUTS / "founderbench-publication-audit.md",
    )


def validate_outputs() -> list[str]:
    problems: list[str] = []
    manifest_path = OUTPUTS / "founderbench-task-manifest.json"
    leaderboard_path = OUTPUTS / "founderbench-baseline-leaderboard.json"
    raw_path = OUTPUTS / "founderbench-baseline-raw.json"

    for name in REQUIRED_OUTPUTS:
        path = OUTPUTS / name
        if not path.exists():
            problems.append(f"Missing required output: {name}")

    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("version") != VERSION:
            problems.append(f"Manifest version mismatch: {manifest.get('version')}")
        if manifest.get("task_count") != 50:
            problems.append(f"Expected 50 tasks, found {manifest.get('task_count')}")
        splits = {task.get("split") for task in manifest.get("tasks", [])}
        if not {"public_dev", "public_test"} <= splits:
            problems.append(f"Manifest split labels incomplete: {sorted(splits)}")

    if leaderboard_path.exists():
        leaderboard = json.loads(leaderboard_path.read_text(encoding="utf-8"))
        if leaderboard.get("version") != VERSION:
            problems.append(f"Leaderboard version mismatch: {leaderboard.get('version')}")
        if len(leaderboard.get("rows", [])) < 4:
            problems.append("Leaderboard has fewer than four baseline rows.")

    if raw_path.exists():
        raw = json.loads(raw_path.read_text(encoding="utf-8"))
        for run in raw:
            if run.get("tasks") != 50:
                problems.append(f"Raw run {run.get('policy')} has {run.get('tasks')} tasks, expected 50.")
            if "diagnostics" not in run:
                problems.append(f"Raw run {run.get('policy')} missing diagnostics.")
            if "splits" not in run:
                problems.append(f"Raw run {run.get('policy')} missing split summary.")

    return problems


def copy_tree(src: Path, dst: Path) -> None:
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(
        src,
        dst,
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".pytest_cache"),
    )


def write_checksum_manifest(bundle: Path) -> None:
    post_manifest_files = {"SHA256SUMS.json", "BUNDLE-INTEGRITY.json", "BUNDLE-INTEGRITY.md"}
    files = [
        path
        for path in bundle.rglob("*")
        if path.is_file() and path.relative_to(bundle).as_posix() not in post_manifest_files
    ]
    checksums = []
    for path in sorted(files):
        rel = path.relative_to(bundle).as_posix()
        checksums.append({"path": rel, "sha256": sha256(path), "bytes": path.stat().st_size})
    (bundle / "SHA256SUMS.json").write_text(json.dumps(checksums, indent=2), encoding="utf-8")


def build_bundle() -> Path:
    bundle = RELEASE_ROOT / "founderbench"
    if bundle.exists():
        shutil.rmtree(bundle)
    (bundle / "code").mkdir(parents=True)
    (bundle / "outputs").mkdir(parents=True)
    (bundle / "paper").mkdir(parents=True)

    copy_tree(PACKAGE_ROOT / "founderbench", bundle / "code" / "founderbench")
    copy_tree(PACKAGE_ROOT / "tests", bundle / "code" / "tests")
    for name in ["README.md", "SPEC.md", "CITATION.cff", "CITATION.cff.template", "LICENSE", "LICENSE.template"]:
        src = PACKAGE_ROOT / name
        if src.exists():
            shutil.copy2(src, bundle / "code" / name)

    for name in REQUIRED_OUTPUTS:
        src = OUTPUTS / name
        if src.exists():
            target_dir = bundle / ("paper" if "paper-draft" in name or "related-work" in name else "outputs")
            shutil.copy2(src, target_dir / name)

    readme = [
        "# FounderBench Supplementary Bundle",
        "",
        "This bundle contains code, fixed task manifest, baseline outputs, analysis tables, and paper-facing documentation.",
        "",
        "Run validation from the original workspace with:",
        "",
        "```powershell",
        "python -m founderbench.release validate",
        "```",
        "",
        "This release does not yet include hosted LLM current release baselines or a private hidden holdout.",
        "",
    ]
    (bundle / "README.md").write_text("\n".join(readme), encoding="utf-8")

    write_checksum_manifest(bundle)
    write_bundle_integrity_report(bundle, bundle / "BUNDLE-INTEGRITY.json", bundle / "BUNDLE-INTEGRITY.md")
    write_reviewer_index(
        OUTPUTS / "founderbench-reviewer-index.json",
        OUTPUTS / "founderbench-reviewer-index.md",
    )
    for name in ["founderbench-reviewer-index.json", "founderbench-reviewer-index.md"]:
        shutil.copy2(OUTPUTS / name, bundle / "outputs" / name)
    write_checksum_manifest(bundle)
    write_bundle_integrity_report(bundle, bundle / "BUNDLE-INTEGRITY.json", bundle / "BUNDLE-INTEGRITY.md")
    return bundle


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and package FounderBench release artifacts.")
    parser.add_argument("command", choices=["validate", "regenerate", "bundle"])
    args = parser.parse_args()

    if args.command == "regenerate":
        regenerate()
        print("Regenerated current release core artifacts.")
        return

    if args.command == "validate":
        run_tests()
        problems = validate_outputs()
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}")
            raise SystemExit(1)
        print("FounderBench validation passed.")
        return

    if args.command == "bundle":
        run_tests()
        problems = validate_outputs()
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}")
            raise SystemExit(1)
        bundle = build_bundle()
        print(f"Wrote {bundle}")


if __name__ == "__main__":
    main()
