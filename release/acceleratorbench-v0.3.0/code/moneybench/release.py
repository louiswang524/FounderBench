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
    "acceleratorbench-task-manifest-v0.3.json",
    "acceleratorbench-task-coverage-v0.3.json",
    "acceleratorbench-task-coverage-v0.3.md",
    "acceleratorbench-task-provenance-v0.3.json",
    "acceleratorbench-task-provenance-v0.3.md",
    "acceleratorbench-task-cards-v0.3.json",
    "acceleratorbench-task-cards-v0.3.md",
    "acceleratorbench-action-semantics-v0.3.json",
    "acceleratorbench-action-semantics-v0.3.md",
    "acceleratorbench-market-catalog-v0.3.json",
    "acceleratorbench-market-catalog-v0.3.md",
    "acceleratorbench-baseline-leaderboard-v0.3.json",
    "acceleratorbench-leaderboard-policy-v0.3.json",
    "acceleratorbench-leaderboard-policy-v0.3.md",
    "acceleratorbench-leaderboard-stability-v0.3.json",
    "acceleratorbench-leaderboard-stability-v0.3.md",
    "acceleratorbench-baseline-raw-v0.3.json",
    "acceleratorbench-baseline-analysis-v0.3.md",
    "acceleratorbench-result-integrity-audit-v0.3.json",
    "acceleratorbench-result-integrity-audit-v0.3.md",
    "acceleratorbench-paper-tables-v0.3.json",
    "acceleratorbench-paper-tables-v0.3.md",
    "acceleratorbench-paper-figure-data-v0.3.json",
    "acceleratorbench-paper-figure-data-v0.3.md",
    "acceleratorbench-model-result-cards-v0.3.json",
    "acceleratorbench-model-result-cards-v0.3.md",
    "acceleratorbench-paper-evidence-map-v0.3.json",
    "acceleratorbench-paper-evidence-map-v0.3.md",
    "acceleratorbench-paper-claim-lint-v0.3.json",
    "acceleratorbench-paper-claim-lint-v0.3.md",
    "acceleratorbench-model-comparison-v0.3.json",
    "acceleratorbench-model-comparison-v0.3.md",
    "acceleratorbench-ablation-report-v0.3.md",
    "acceleratorbench-action-ablation-v0.3.json",
    "acceleratorbench-action-ablation-v0.3.md",
    "acceleratorbench-difficulty-calibration-v0.3.json",
    "acceleratorbench-difficulty-calibration-v0.3.md",
    "acceleratorbench-task-feasibility-audit-v0.3.json",
    "acceleratorbench-task-feasibility-audit-v0.3.md",
    "acceleratorbench-task-revision-ledger-v0.3.json",
    "acceleratorbench-task-revision-ledger-v0.3.md",
    "acceleratorbench-qualitative-traces-v0.3.json",
    "acceleratorbench-qualitative-traces-v0.3.md",
    "acceleratorbench-random-repeats-v0.3.json",
    "acceleratorbench-random-repeats-v0.3.md",
    "acceleratorbench-benchmark-card.md",
    "acceleratorbench-datasheet-v0.3.json",
    "acceleratorbench-datasheet-v0.3.md",
    "acceleratorbench-metrics-and-evaluation.md",
    "acceleratorbench-metric-sensitivity-v0.3.json",
    "acceleratorbench-metric-sensitivity-v0.3.md",
    "acceleratorbench-paired-statistics-v0.3.json",
    "acceleratorbench-paired-statistics-v0.3.md",
    "acceleratorbench-power-analysis-v0.3.json",
    "acceleratorbench-power-analysis-v0.3.md",
    "acceleratorbench-statistical-protocol-v0.3.json",
    "acceleratorbench-statistical-protocol-v0.3.md",
    "acceleratorbench-score-rubric-v0.3.json",
    "acceleratorbench-score-rubric-v0.3.md",
    "acceleratorbench-scoring-consistency-audit-v0.3.json",
    "acceleratorbench-scoring-consistency-audit-v0.3.md",
    "acceleratorbench-reproduction-guide.md",
    "acceleratorbench-reviewer-smoke-v0.3.json",
    "acceleratorbench-reviewer-smoke-v0.3.md",
    "acceleratorbench-environment-report-v0.3.json",
    "acceleratorbench-environment-report-v0.3.md",
    "acceleratorbench-simulator-invariant-audit-v0.3.json",
    "acceleratorbench-simulator-invariant-audit-v0.3.md",
    "acceleratorbench-model-submission-template.md",
    "acceleratorbench-model-submission-schema-v0.3.json",
    "acceleratorbench-model-submission-schema-v0.3.md",
    "acceleratorbench-submission-bundle-protocol-v0.3.json",
    "acceleratorbench-submission-bundle-protocol-v0.3.md",
    "acceleratorbench-local-openai-compatible-protocol-v0.3.json",
    "acceleratorbench-local-openai-compatible-protocol-v0.3.md",
    "acceleratorbench-prompt-protocol-v0.3.json",
    "acceleratorbench-prompt-protocol-v0.3.md",
    "acceleratorbench-provider-readiness-v0.3.json",
    "acceleratorbench-provider-readiness-v0.3.md",
    "acceleratorbench-cost-accounting-v0.3.json",
    "acceleratorbench-cost-accounting-v0.3.md",
    "acceleratorbench-baseline-execution-plan-v0.3.json",
    "acceleratorbench-baseline-execution-plan-v0.3.md",
    "acceleratorbench-experiment-runbook-v0.3.json",
    "acceleratorbench-experiment-runbook-v0.3.md",
    "acceleratorbench-provider-run-status-v0.3.json",
    "acceleratorbench-provider-run-status-v0.3.md",
    "acceleratorbench-provider-comparability-audit-v0.3.json",
    "acceleratorbench-provider-comparability-audit-v0.3.md",
    "acceleratorbench-provider-contract-audit-v0.3.json",
    "acceleratorbench-provider-contract-audit-v0.3.md",
    "acceleratorbench-contamination-leakage-audit-v0.3.json",
    "acceleratorbench-contamination-leakage-audit-v0.3.md",
    "acceleratorbench-license-readiness-v0.3.json",
    "acceleratorbench-license-readiness-v0.3.md",
    "acceleratorbench-release-metadata-checklist-v0.3.json",
    "acceleratorbench-release-metadata-checklist-v0.3.md",
    "acceleratorbench-submission-validation-v0.3.md",
    "acceleratorbench-private-holdout-blueprint-v0.3.json",
    "acceleratorbench-private-holdout-evaluator-protocol-v0.3.json",
    "acceleratorbench-private-holdout-evaluator-protocol-v0.3.md",
    "acceleratorbench-private-holdout-smoke-v0.3.json",
    "acceleratorbench-private-holdout-smoke-v0.3.md",
    "acceleratorbench-human-calibration-protocol-v0.3.json",
    "acceleratorbench-human-calibration-protocol-v0.3.md",
    "acceleratorbench-human-calibration-schema-v0.3.json",
    "acceleratorbench-human-calibration-schema-v0.3.md",
    "acceleratorbench-human-calibration-template-v0.3.json",
    "acceleratorbench-human-calibration-analysis-v0.3.json",
    "acceleratorbench-human-calibration-analysis-v0.3.md",
    "acceleratorbench-human-calibration-packet-v0.3.json",
    "acceleratorbench-human-calibration-packet-v0.3.md",
    "acceleratorbench-paper-draft-v0.1.md",
    "acceleratorbench-references.bib",
    "acceleratorbench-reference-provenance-v0.3.json",
    "acceleratorbench-citation-audit-v0.3.json",
    "acceleratorbench-citation-audit-v0.3.md",
    "acceleratorbench-reproducibility-manifest-v0.3.json",
    "acceleratorbench-reproducibility-manifest-v0.3.md",
    "acceleratorbench-determinism-audit-v0.3.json",
    "acceleratorbench-determinism-audit-v0.3.md",
    "acceleratorbench-validity-report-v0.3.json",
    "acceleratorbench-validity-report-v0.3.md",
    "acceleratorbench-responsible-use-v0.3.json",
    "acceleratorbench-responsible-use-v0.3.md",
    "acceleratorbench-claim-evidence-v0.3.json",
    "acceleratorbench-claim-evidence-v0.3.md",
    "acceleratorbench-completion-audit-v0.3.json",
    "acceleratorbench-completion-audit-v0.3.md",
    "acceleratorbench-submission-manifest-v0.3.json",
    "acceleratorbench-submission-manifest-v0.3.md",
    "acceleratorbench-reviewer-risk-audit-v0.3.json",
    "acceleratorbench-reviewer-risk-audit-v0.3.md",
    "acceleratorbench-failure-mode-audit-v0.3.json",
    "acceleratorbench-failure-mode-audit-v0.3.md",
    "acceleratorbench-submission-gate-v0.3.json",
    "acceleratorbench-submission-gate-v0.3.md",
    "acceleratorbench-submission-action-plan-v0.3.json",
    "acceleratorbench-submission-action-plan-v0.3.md",
    "acceleratorbench-related-work-notes.md",
    "acceleratorbench-experiment-matrix-v0.3.json",
    "acceleratorbench-experiment-matrix-v0.3.md",
    "acceleratorbench-reviewer-index-v0.3.json",
    "acceleratorbench-reviewer-index-v0.3.md",
    "acceleratorbench-publication-audit-v0.3.json",
    "acceleratorbench-publication-audit-v0.3.md",
    "acceleratorbench-supplementary-package-checklist.md",
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
    (OUTPUTS / "acceleratorbench-task-manifest-v0.3.json").write_text(
        json.dumps(task_manifest(), indent=2),
        encoding="utf-8",
    )
    write_task_coverage(
        OUTPUTS / "acceleratorbench-task-coverage-v0.3.json",
        OUTPUTS / "acceleratorbench-task-coverage-v0.3.md",
    )
    write_task_provenance(
        OUTPUTS / "acceleratorbench-task-provenance-v0.3.json",
        OUTPUTS / "acceleratorbench-task-provenance-v0.3.md",
    )
    write_task_cards(
        OUTPUTS / "acceleratorbench-task-cards-v0.3.json",
        OUTPUTS / "acceleratorbench-task-cards-v0.3.md",
    )
    write_action_semantics(
        OUTPUTS / "acceleratorbench-action-semantics-v0.3.json",
        OUTPUTS / "acceleratorbench-action-semantics-v0.3.md",
    )
    write_market_catalog(
        OUTPUTS / "acceleratorbench-market-catalog-v0.3.json",
        OUTPUTS / "acceleratorbench-market-catalog-v0.3.md",
    )
    raw = [run_suite(policy) for policy in ["random", "conservative", "heuristic", "task_heuristic"]]
    leaderboard = {
        "benchmark": "FounderBench",
        "version": VERSION,
        "rows": sorted([summarize(result) for result in raw], key=lambda row: row["average_task_score"], reverse=True),
    }
    (OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    (OUTPUTS / "acceleratorbench-baseline-leaderboard-v0.3.json").write_text(json.dumps(leaderboard, indent=2), encoding="utf-8")
    write_leaderboard_policy(
        OUTPUTS / "acceleratorbench-leaderboard-policy-v0.3.json",
        OUTPUTS / "acceleratorbench-leaderboard-policy-v0.3.md",
    )
    write_leaderboard_stability_audit(
        OUTPUTS / "acceleratorbench-leaderboard-stability-v0.3.json",
        OUTPUTS / "acceleratorbench-leaderboard-stability-v0.3.md",
    )
    write_report(raw, OUTPUTS / "acceleratorbench-baseline-analysis-v0.3.md")
    write_paper_tables(
        OUTPUTS / "acceleratorbench-paper-tables-v0.3.json",
        OUTPUTS / "acceleratorbench-paper-tables-v0.3.md",
    )
    write_paper_figure_data(
        OUTPUTS / "acceleratorbench-paper-figure-data-v0.3.json",
        OUTPUTS / "acceleratorbench-paper-figure-data-v0.3.md",
    )
    write_task_revision_ledger(
        OUTPUTS / "acceleratorbench-task-revision-ledger-v0.3.json",
        OUTPUTS / "acceleratorbench-task-revision-ledger-v0.3.md",
    )
    write_model_comparison_report(
        OUTPUTS / "acceleratorbench-model-comparison-v0.3.json",
        OUTPUTS / "acceleratorbench-model-comparison-v0.3.md",
    )
    write_result_integrity_audit(
        OUTPUTS / "acceleratorbench-result-integrity-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-result-integrity-audit-v0.3.md",
    )
    write_model_result_cards(
        OUTPUTS / "acceleratorbench-model-result-cards-v0.3.json",
        OUTPUTS / "acceleratorbench-model-result-cards-v0.3.md",
    )
    write_ablation_report(raw, OUTPUTS / "acceleratorbench-ablation-report-v0.3.md")
    write_action_ablation_report(
        OUTPUTS / "acceleratorbench-action-ablation-v0.3.json",
        OUTPUTS / "acceleratorbench-action-ablation-v0.3.md",
    )
    write_difficulty_calibration_report(
        OUTPUTS / "acceleratorbench-difficulty-calibration-v0.3.json",
        OUTPUTS / "acceleratorbench-difficulty-calibration-v0.3.md",
    )
    write_task_feasibility_audit(
        OUTPUTS / "acceleratorbench-task-feasibility-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-task-feasibility-audit-v0.3.md",
    )
    qualitative = build_trace_examples(OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json")
    (OUTPUTS / "acceleratorbench-qualitative-traces-v0.3.json").write_text(json.dumps(qualitative, indent=2), encoding="utf-8")
    write_trace_markdown(qualitative, OUTPUTS / "acceleratorbench-qualitative-traces-v0.3.md")
    repeated_random = run_repeated("random", [0, 1, 2, 3, 4])
    (OUTPUTS / "acceleratorbench-random-repeats-v0.3.json").write_text(json.dumps(repeated_random, indent=2), encoding="utf-8")
    write_repeated_report(repeated_random, OUTPUTS / "acceleratorbench-random-repeats-v0.3.md")
    write_benchmark_datasheet(
        OUTPUTS / "acceleratorbench-datasheet-v0.3.json",
        OUTPUTS / "acceleratorbench-datasheet-v0.3.md",
    )
    write_score_rubric(
        OUTPUTS / "acceleratorbench-score-rubric-v0.3.json",
        OUTPUTS / "acceleratorbench-score-rubric-v0.3.md",
    )
    write_scoring_consistency_audit(
        OUTPUTS / "acceleratorbench-scoring-consistency-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-scoring-consistency-audit-v0.3.md",
    )
    write_metric_sensitivity_report(
        OUTPUTS / "acceleratorbench-metric-sensitivity-v0.3.json",
        OUTPUTS / "acceleratorbench-metric-sensitivity-v0.3.md",
    )
    write_paired_statistics_report(
        OUTPUTS / "acceleratorbench-paired-statistics-v0.3.json",
        OUTPUTS / "acceleratorbench-paired-statistics-v0.3.md",
    )
    write_power_analysis(
        OUTPUTS / "acceleratorbench-power-analysis-v0.3.json",
        OUTPUTS / "acceleratorbench-power-analysis-v0.3.md",
    )
    write_statistical_protocol(
        OUTPUTS / "acceleratorbench-statistical-protocol-v0.3.json",
        OUTPUTS / "acceleratorbench-statistical-protocol-v0.3.md",
    )
    write_reviewer_smoke_report(
        OUTPUTS / "acceleratorbench-reviewer-smoke-v0.3.json",
        OUTPUTS / "acceleratorbench-reviewer-smoke-v0.3.md",
    )
    write_reference_artifacts(
        OUTPUTS / "acceleratorbench-references.bib",
        OUTPUTS / "acceleratorbench-reference-provenance-v0.3.json",
    )
    write_citation_audit(
        OUTPUTS / "acceleratorbench-citation-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-citation-audit-v0.3.md",
    )
    write_local_model_protocol(OUTPUTS / "acceleratorbench-local-openai-compatible-protocol-v0.3.json")
    write_local_model_protocol(OUTPUTS / "acceleratorbench-local-openai-compatible-protocol-v0.3.md")
    write_prompt_protocol(
        OUTPUTS / "acceleratorbench-prompt-protocol-v0.3.json",
        OUTPUTS / "acceleratorbench-prompt-protocol-v0.3.md",
    )
    write_provider_readiness(
        OUTPUTS / "acceleratorbench-provider-readiness-v0.3.json",
        OUTPUTS / "acceleratorbench-provider-readiness-v0.3.md",
    )
    write_cost_accounting_protocol(
        OUTPUTS / "acceleratorbench-cost-accounting-v0.3.json",
        OUTPUTS / "acceleratorbench-cost-accounting-v0.3.md",
    )
    write_baseline_execution_plan(
        OUTPUTS / "acceleratorbench-baseline-execution-plan-v0.3.json",
        OUTPUTS / "acceleratorbench-baseline-execution-plan-v0.3.md",
    )
    write_experiment_runbook(
        OUTPUTS / "acceleratorbench-experiment-runbook-v0.3.json",
        OUTPUTS / "acceleratorbench-experiment-runbook-v0.3.md",
    )
    write_provider_run_status(
        OUTPUTS / "acceleratorbench-provider-run-status-v0.3.json",
        OUTPUTS / "acceleratorbench-provider-run-status-v0.3.md",
    )
    write_provider_comparability_audit(
        OUTPUTS / "acceleratorbench-provider-comparability-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-provider-comparability-audit-v0.3.md",
    )
    write_provider_contract_audit(
        OUTPUTS / "acceleratorbench-provider-contract-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-provider-contract-audit-v0.3.md",
    )
    write_contamination_leakage_audit(
        OUTPUTS / "acceleratorbench-contamination-leakage-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-contamination-leakage-audit-v0.3.md",
    )
    write_license_readiness_report(
        OUTPUTS / "acceleratorbench-license-readiness-v0.3.json",
        OUTPUTS / "acceleratorbench-license-readiness-v0.3.md",
    )
    write_release_metadata_checklist(
        OUTPUTS / "acceleratorbench-release-metadata-checklist-v0.3.json",
        OUTPUTS / "acceleratorbench-release-metadata-checklist-v0.3.md",
    )
    (OUTPUTS / "acceleratorbench-private-holdout-evaluator-protocol-v0.3.json").write_text(
        json.dumps(evaluator_protocol(), indent=2),
        encoding="utf-8",
    )
    write_evaluator_protocol_markdown(OUTPUTS / "acceleratorbench-private-holdout-evaluator-protocol-v0.3.md")
    write_holdout_smoke_report(
        OUTPUTS / "acceleratorbench-private-holdout-smoke-v0.3.json",
        OUTPUTS / "acceleratorbench-private-holdout-smoke-v0.3.md",
    )
    write_human_calibration_protocol(
        OUTPUTS / "acceleratorbench-human-calibration-protocol-v0.3.json",
        OUTPUTS / "acceleratorbench-human-calibration-protocol-v0.3.md",
    )
    write_human_calibration_schema(
        OUTPUTS / "acceleratorbench-human-calibration-schema-v0.3.json",
        OUTPUTS / "acceleratorbench-human-calibration-schema-v0.3.md",
        OUTPUTS / "acceleratorbench-human-calibration-template-v0.3.json",
    )
    write_human_calibration_analysis(
        [],
        OUTPUTS / "acceleratorbench-human-calibration-analysis-v0.3.json",
        OUTPUTS / "acceleratorbench-human-calibration-analysis-v0.3.md",
    )
    write_human_calibration_packet(
        OUTPUTS / "acceleratorbench-human-calibration-packet-v0.3.json",
        OUTPUTS / "acceleratorbench-human-calibration-packet-v0.3.md",
    )
    write_submission_report(
        OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json",
        OUTPUTS / "acceleratorbench-submission-validation-v0.3.md",
    )
    write_submission_schema(
        OUTPUTS / "acceleratorbench-model-submission-schema-v0.3.json",
        OUTPUTS / "acceleratorbench-model-submission-schema-v0.3.md",
    )
    write_submission_bundle_protocol(
        OUTPUTS / "acceleratorbench-submission-bundle-protocol-v0.3.json",
        OUTPUTS / "acceleratorbench-submission-bundle-protocol-v0.3.md",
    )
    write_experiment_matrix(
        OUTPUTS / "acceleratorbench-experiment-matrix-v0.3.json",
        OUTPUTS / "acceleratorbench-experiment-matrix-v0.3.md",
    )
    write_environment_report(
        OUTPUTS / "acceleratorbench-environment-report-v0.3.json",
        OUTPUTS / "acceleratorbench-environment-report-v0.3.md",
    )
    write_simulator_invariant_audit(
        OUTPUTS / "acceleratorbench-simulator-invariant-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-simulator-invariant-audit-v0.3.md",
    )
    write_determinism_audit(
        OUTPUTS / "acceleratorbench-determinism-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-determinism-audit-v0.3.md",
    )
    write_validity_report(
        OUTPUTS / "acceleratorbench-validity-report-v0.3.json",
        OUTPUTS / "acceleratorbench-validity-report-v0.3.md",
    )
    write_responsible_use_statement(
        OUTPUTS / "acceleratorbench-responsible-use-v0.3.json",
        OUTPUTS / "acceleratorbench-responsible-use-v0.3.md",
    )
    write_claim_evidence_report(
        OUTPUTS / "acceleratorbench-claim-evidence-v0.3.json",
        OUTPUTS / "acceleratorbench-claim-evidence-v0.3.md",
    )
    write_submission_gate(
        OUTPUTS / "acceleratorbench-submission-gate-v0.3.json",
        OUTPUTS / "acceleratorbench-submission-gate-v0.3.md",
    )
    write_completion_audit(
        OUTPUTS / "acceleratorbench-completion-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-completion-audit-v0.3.md",
    )
    write_submission_manifest(
        OUTPUTS / "acceleratorbench-submission-manifest-v0.3.json",
        OUTPUTS / "acceleratorbench-submission-manifest-v0.3.md",
    )
    write_paper_evidence_map(
        OUTPUTS / "acceleratorbench-paper-evidence-map-v0.3.json",
        OUTPUTS / "acceleratorbench-paper-evidence-map-v0.3.md",
    )
    write_paper_claim_lint(
        OUTPUTS / "acceleratorbench-paper-claim-lint-v0.3.json",
        OUTPUTS / "acceleratorbench-paper-claim-lint-v0.3.md",
    )
    write_reviewer_risk_audit(
        OUTPUTS / "acceleratorbench-reviewer-risk-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-reviewer-risk-audit-v0.3.md",
    )
    write_failure_mode_audit(
        OUTPUTS / "acceleratorbench-failure-mode-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-failure-mode-audit-v0.3.md",
    )
    write_reproducibility_manifest(
        OUTPUTS / "acceleratorbench-reproducibility-manifest-v0.3.json",
        OUTPUTS / "acceleratorbench-reproducibility-manifest-v0.3.md",
    )
    write_submission_action_plan(
        OUTPUTS / "acceleratorbench-submission-action-plan-v0.3.json",
        OUTPUTS / "acceleratorbench-submission-action-plan-v0.3.md",
    )
    write_reviewer_index(
        OUTPUTS / "acceleratorbench-reviewer-index-v0.3.json",
        OUTPUTS / "acceleratorbench-reviewer-index-v0.3.md",
    )
    write_publication_audit(
        OUTPUTS / "acceleratorbench-publication-audit-v0.3.json",
        OUTPUTS / "acceleratorbench-publication-audit-v0.3.md",
    )


def validate_outputs() -> list[str]:
    problems: list[str] = []
    manifest_path = OUTPUTS / "acceleratorbench-task-manifest-v0.3.json"
    leaderboard_path = OUTPUTS / "acceleratorbench-baseline-leaderboard-v0.3.json"
    raw_path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json"

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
    bundle = RELEASE_ROOT / f"acceleratorbench-v{VERSION}"
    if bundle.exists():
        shutil.rmtree(bundle)
    (bundle / "code").mkdir(parents=True)
    (bundle / "outputs").mkdir(parents=True)
    (bundle / "paper").mkdir(parents=True)

    copy_tree(PACKAGE_ROOT / "moneybench", bundle / "code" / "moneybench")
    copy_tree(PACKAGE_ROOT / "tests", bundle / "code" / "tests")
    for name in ["README.md", "SPEC.md", "CITATION.cff", "CITATION.cff.template", "LICENSE-TODO.md", "LICENSE.template"]:
        shutil.copy2(PACKAGE_ROOT / name, bundle / "code" / name)

    for name in REQUIRED_OUTPUTS:
        src = OUTPUTS / name
        if src.exists():
            target_dir = bundle / ("paper" if "paper-draft" in name or "related-work" in name else "outputs")
            shutil.copy2(src, target_dir / name)

    readme = [
        "# FounderBench v0.3.0 Supplementary Bundle",
        "",
        "This bundle contains code, fixed task manifest, baseline outputs, analysis tables, and paper-facing documentation.",
        "",
        "Run validation from the original workspace with:",
        "",
        "```powershell",
        "python -m moneybench.release validate",
        "```",
        "",
        "This release does not yet include hosted LLM v0.3.0 baselines or a private hidden holdout.",
        "",
    ]
    (bundle / "README.md").write_text("\n".join(readme), encoding="utf-8")

    write_checksum_manifest(bundle)
    write_bundle_integrity_report(bundle, bundle / "BUNDLE-INTEGRITY.json", bundle / "BUNDLE-INTEGRITY.md")
    write_reviewer_index(
        OUTPUTS / "acceleratorbench-reviewer-index-v0.3.json",
        OUTPUTS / "acceleratorbench-reviewer-index-v0.3.md",
    )
    for name in ["acceleratorbench-reviewer-index-v0.3.json", "acceleratorbench-reviewer-index-v0.3.md"]:
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
        print("Regenerated v0.3 core artifacts.")
        return

    if args.command == "validate":
        run_tests()
        problems = validate_outputs()
        if problems:
            for problem in problems:
                print(f"ERROR: {problem}")
            raise SystemExit(1)
        print("FounderBench v0.3 validation passed.")
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
