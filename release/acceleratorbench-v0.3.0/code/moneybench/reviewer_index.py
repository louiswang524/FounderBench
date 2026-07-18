from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


ARTIFACTS: list[dict[str, Any]] = [
    {
        "path": "work/moneybench/README.md",
        "role": "Start here for installation, task families, action space, and run commands.",
        "category": "orientation",
    },
    {
        "path": "work/moneybench/SPEC.md",
        "role": "Formal simulator and benchmark specification.",
        "category": "orientation",
    },
    {
        "path": "outputs/acceleratorbench-action-semantics-v0.3.md",
        "role": "Human-readable semantics for every structured action: required fields, costs, effects, risk triggers, and typical use cases.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-market-catalog-v0.3.md",
        "role": "Fixed simulated market catalog documenting all 8 market ids, demand/competition/WTP/support parameters, observation rules, and settlement rules.",
        "category": "data",
    },
    {
        "path": "outputs/acceleratorbench-benchmark-card.md",
        "role": "Dataset-style benchmark card with intended use, limitations, and scope.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-datasheet-v0.3.md",
        "role": "Datasheet-style disclosure covering motivation, composition, curation, intended use, distribution, maintenance, and unsupported claims.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-responsible-use-v0.3.md",
        "role": "Responsible-use, ethics, privacy, unsupported-use, and provider-submission disclosure statement.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-task-manifest-v0.3.json",
        "role": "Fixed public 50-task suite, task families, splits, budgets, and scenario metadata.",
        "category": "data",
    },
    {
        "path": "outputs/acceleratorbench-task-coverage-v0.3.md",
        "role": "Task-suite balance, split, action, and capability coverage report.",
        "category": "data",
    },
    {
        "path": "outputs/acceleratorbench-task-provenance-v0.3.md",
        "role": "Task curation and provenance record documenting templates, seed rules, setup sources, score sources, and synthetic-data status.",
        "category": "data",
    },
    {
        "path": "outputs/acceleratorbench-task-cards-v0.3.md",
        "role": "Human-readable cards for all 50 tasks, including initial state, scoring metrics, expected actions, family, split, and horizon.",
        "category": "data",
    },
    {
        "path": "outputs/acceleratorbench-metrics-and-evaluation.md",
        "role": "Primary score, solve criteria, diagnostic metrics, penalties, and comparison protocol.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-score-rubric-v0.3.md",
        "role": "Family-level score components, penalty rules, bounds, and pass-threshold validation.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-scoring-consistency-audit-v0.3.md",
        "role": "Score-object consistency audit over all deterministic raw task results, including bounds, pass threshold, metrics payloads, family coverage, and split coverage.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-metric-sensitivity-v0.3.md",
        "role": "Sensitivity analysis comparing official bounded task score against normalized business, solve-rate, survival, revenue, cash, and risk diagnostics.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-baseline-leaderboard-v0.3.json",
        "role": "Machine-readable leaderboard for included non-LLM baselines.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-leaderboard-policy-v0.3.md",
        "role": "Leaderboard/reporting policy defining public, repeated-run, and future private-holdout tiers plus acceptance and rejection rules.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-leaderboard-stability-v0.3.md",
        "role": "Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-baseline-raw-v0.3.json",
        "role": "Task-level raw baseline results for random, conservative, heuristic, and task-aware heuristic policies.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-baseline-analysis-v0.3.md",
        "role": "Bootstrap intervals, split summaries, family scores, and policy comparisons.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-result-integrity-audit-v0.3.md",
        "role": "Raw-to-report integrity audit proving deterministic baseline rows in leaderboard, paper tables, and model comparison match raw task outputs.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-paper-tables-v0.3.md",
        "role": "Paper-ready result tables generated from raw v0.3.0 runs and validated provider availability.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-paper-figure-data-v0.3.md",
        "role": "Paper figure datasets for leaderboard bars, family heatmaps, action-ablation drops, difficulty bands, and metric-sensitivity rankings.",
        "category": "paper",
    },
    {
        "path": "outputs/acceleratorbench-paper-evidence-map-v0.3.md",
        "role": "Section-by-section paper evidence crosswalk linking draft claims to supporting artifacts and excluded claims.",
        "category": "paper",
    },
    {
        "path": "outputs/acceleratorbench-model-comparison-v0.3.md",
        "role": "Unified leaderboard/comparison report that automatically incorporates validated hosted/local provider runs and keeps missing provider evidence explicit.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-model-result-cards-v0.3.md",
        "role": "Reviewer-facing result cards summarizing deterministic baselines and planned provider submissions with validation, diagnostics, cost fields, and claim eligibility.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-ablation-report-v0.3.md",
        "role": "Capability-ladder ablation from random to task-aware heuristic behavior.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-action-ablation-v0.3.md",
        "role": "Action-space ablation showing how disabling discovery, growth, quality/support, pricing, runway/funding, and pivot actions changes task-aware baseline outcomes.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-paired-statistics-v0.3.md",
        "role": "Paired score gaps, bootstrap intervals, raw and Holm-adjusted permutation p-values, effect sizes, and win/loss/tie counts over matched tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-power-analysis-v0.3.md",
        "role": "Power and resolution analysis estimating minimum detectable score gaps for the public suite and warning against overclaiming close model differences.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-statistical-protocol-v0.3.md",
        "role": "Pre-specified primary endpoint, paired comparison test, repeated-sampling, multiple-comparison, and claim rules for model comparisons.",
        "category": "metrics",
    },
    {
        "path": "outputs/acceleratorbench-difficulty-calibration-v0.3.md",
        "role": "Task difficulty bands, baseline solve-count calibration, family/split balance, and high-discrimination tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-task-feasibility-audit-v0.3.md",
        "role": "Task-level feasibility and discrimination ledger identifying baseline-solved, saturated, high-discrimination, and external-calibration-needed tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
        "role": "Change-control ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable task or rubric revisions.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-experiment-matrix-v0.3.md",
        "role": "Paper-facing ledger of completed and missing baselines, ablations, uncertainty checks, audit traces, and holdout evidence.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-random-repeats-v0.3.md",
        "role": "Repeated-seed calibration intervals for the stochastic random baseline.",
        "category": "uncertainty",
    },
    {
        "path": "outputs/acceleratorbench-qualitative-traces-v0.3.md",
        "role": "Representative deterministic success and failure traces for paper analysis.",
        "category": "qualitative",
    },
    {
        "path": "outputs/acceleratorbench-reproduction-guide.md",
        "role": "End-to-end instructions for regenerating artifacts and validating submissions.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-reviewer-smoke-v0.3.md",
        "role": "Fast reviewer smoke report checking task loading, one deterministic task execution, and included baseline submission validation.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-environment-report-v0.3.md",
        "role": "Runtime and dependency report with Python version, import classification, import checks, and provider/local-model dependency notes.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
        "role": "Deterministic simulator stress audit checking state bounds, score bounds, and core environment invariants without claiming real-world validity.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-reproducibility-manifest-v0.3.md",
        "role": "Source/output hashes, environment metadata, and reproduction commands for the current workspace.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-determinism-audit-v0.3.md",
        "role": "Replay audit showing deterministic baselines reproduce stable task outcomes from fixed seeds.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/acceleratorbench-validity-report-v0.3.md",
        "role": "Threats-to-validity matrix with mitigations, evidence paths, and remaining work.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
        "role": "Expert/human-founder calibration protocol for checking task realism, action coverage, score alignment, difficulty, and gaming risks.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-human-calibration-schema-v0.3.md",
        "role": "Machine-readable calibration response schema and validation contract for expert/human-founder reviews.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-human-calibration-template-v0.3.json",
        "role": "Blank JSON template for collecting expert/human-founder calibration responses over required sampled tasks.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-human-calibration-analysis-v0.3.md",
        "role": "Analyzer output for expert/human-founder calibration responses; currently records that no executed calibration submissions are included.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-human-calibration-packet-v0.3.md",
        "role": "Recruitment and operator packet for executing expert/human-founder calibration while preserving not-executed claim guardrails.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-claim-evidence-v0.3.md",
        "role": "Claim-evidence guardrail for supported, qualified, and unsupported paper wording.",
        "category": "documentation",
    },
    {
        "path": "outputs/acceleratorbench-model-submission-template.md",
        "role": "Template for future model providers reporting a run.",
        "category": "submission",
    },
    {
        "path": "outputs/acceleratorbench-model-submission-schema-v0.3.md",
        "role": "Machine-readable submission schema companion documenting accepted run payloads, required diagnostics, and authoritative validation command.",
        "category": "submission",
    },
    {
        "path": "outputs/acceleratorbench-submission-bundle-protocol-v0.3.md",
        "role": "Protocol and CLI helper for combining repeated provider/model seed runs into one validated submission bundle.",
        "category": "submission",
    },
    {
        "path": "outputs/acceleratorbench-submission-validation-v0.3.md",
        "role": "Validation report for the included complete baseline run.",
        "category": "submission",
    },
    {
        "path": "outputs/acceleratorbench-provider-readiness-v0.3.md",
        "role": "Environment readiness matrix and exact commands for hosted/local provider runs.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-cost-accounting-v0.3.md",
        "role": "Provider token and cost-accounting protocol with usage normalization, price environment variables, formula, and reporting guardrails.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-baseline-execution-plan-v0.3.md",
        "role": "Paper-grade hosted/local baseline execution plan with fairness controls, repeats, audit policy, commands, and acceptance criteria.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-experiment-runbook-v0.3.md",
        "role": "Operator runbook for executing missing hosted/local model baselines, audits, repeat bundles, and post-run claim-gate updates.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-provider-run-status-v0.3.md",
        "role": "Generated status report for planned v0.3 provider/local runs, validation reports, audit outputs, and excluded older provider-like files.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-provider-comparability-audit-v0.3.md",
        "role": "Protocol comparability audit checking shared task count, prompt/action contract, validation commands, repeat policy, cost fields, and self-consistency ablation treatment.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
        "role": "Provider-output contract audit checking parser error taxonomy and simulator diagnostics without claiming hosted/local LLM result evidence.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
        "role": "Public-split contamination/leakage audit that keeps public_test visibility, trace leakage risks, and private-holdout claim guardrails explicit.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/acceleratorbench-prompt-protocol-v0.3.md",
        "role": "Canonical LLM prompt contract, provider message wrappers, action vocabulary, and prompt/protocol hashes.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-license-readiness-v0.3.md",
        "role": "License and citation metadata readiness checks plus owner decisions required before public release.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-release-metadata-checklist-v0.3.md",
        "role": "Owner-facing release metadata checklist with license option matrix, CITATION template, and finalization steps.",
        "category": "publication_readiness",
    },
    {
        "path": "work/moneybench/LICENSE.template",
        "role": "Non-final owner-facing template for creating the required public LICENSE file.",
        "category": "publication_readiness",
    },
    {
        "path": "work/moneybench/CITATION.cff.template",
        "role": "Non-final owner-facing CITATION.cff template with placeholders for authors, repository URL, and selected license.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-submission-gate-v0.3.md",
        "role": "Top-level go/no-go submission gate combining publication, experiment, provider, claim, and license readiness.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-submission-manifest-v0.3.md",
        "role": "Compact reviewer-facing manifest of included evidence, supported claims, excluded claims, reproduction commands, and remaining gate blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-completion-audit-v0.3.md",
        "role": "Goal-level completion audit mapping the active publishable-benchmark objective to current evidence and unresolved blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-reviewer-risk-audit-v0.3.md",
        "role": "Pre-submission reviewer-risk audit listing likely reviewer objections, current evidence, open risks, and required responses.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-failure-mode-audit-v0.3.md",
        "role": "AI research failure-mode audit covering code bugs, citation hallucination, result hallucination, shortcut reliance, bug-as-insight, methodology fabrication, and frame-lock.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-paper-claim-lint-v0.3.md",
        "role": "Text-level paper and benchmark-card lint checking required limitation disclosures and selected unsupported positive claim wording.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-submission-action-plan-v0.3.md",
        "role": "Concrete action plan mapping each failing submission gate to owners, commands, expected outputs, and claim impact.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.md",
        "role": "Protocol for running local open-source models through an OpenAI-compatible endpoint.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md",
        "role": "Evaluator-host protocol for secret-seeded hidden task execution, aggregate reporting, and anti-gaming controls.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/acceleratorbench-private-holdout-smoke-v0.3.md",
        "role": "Aggregate-only smoke report proving the private-holdout evaluator harness runs without exposing hidden task definitions; not an official private leaderboard.",
        "category": "anti_gaming",
    },
    {
        "path": "work/moneybench/moneybench/private_holdout_evaluator.py",
        "role": "Executable private-holdout evaluator harness that generates secret-selected private episodes in memory and emits aggregate-only reports by default.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/acceleratorbench-publication-audit-v0.3.md",
        "role": "Submission-readiness matrix mapping benchmark requirements to concrete evidence and blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/acceleratorbench-paper-draft-v0.1.md",
        "role": "Paper-facing draft with motivation, benchmark design, experiments, and limitations.",
        "category": "paper",
    },
    {
        "path": "outputs/acceleratorbench-references.bib",
        "role": "BibTeX references used by the paper draft and related-work notes.",
        "category": "paper",
    },
    {
        "path": "outputs/acceleratorbench-citation-audit-v0.3.md",
        "role": "Local citation-context audit verifying paper citation numbering, BibTeX/provenance coverage, and intended citation use.",
        "category": "paper",
    },
    {
        "path": "release/acceleratorbench-v0.3.0/SHA256SUMS.json",
        "role": "Release-bundle checksum manifest for integrity verification.",
        "category": "release",
    },
    {
        "path": "release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md",
        "role": "Release-bundle integrity report verifying bundled files against SHA256SUMS.json.",
        "category": "release",
    },
]


COMMANDS = [
    {
        "purpose": "Run tests",
        "command": "python -m unittest discover -s tests -v",
        "cwd": "work/moneybench",
    },
    {
        "purpose": "Regenerate generated artifacts",
        "command": "python -m moneybench.release regenerate",
        "cwd": "work/moneybench",
    },
    {
        "purpose": "Validate generated artifacts and tests",
        "command": "python -m moneybench.release validate",
        "cwd": "work/moneybench",
    },
    {
        "purpose": "Build supplementary bundle",
        "command": "python -m moneybench.release bundle",
        "cwd": "work/moneybench",
    },
    {
        "purpose": "Validate a model submission",
        "command": "python -m moneybench.submission --input ..\\..\\outputs\\provider-run.json --report ..\\..\\outputs\\provider-run-submission-report.md",
        "cwd": "work/moneybench",
    },
    {
        "purpose": "Combine repeated model runs",
        "command": "python -m moneybench.submission_bundle --input ..\\..\\outputs\\provider-seed0.json --input ..\\..\\outputs\\provider-seed1.json --output ..\\..\\outputs\\provider-repeats.json --report ..\\..\\outputs\\provider-repeats-submission-report.md",
        "cwd": "work/moneybench",
    },
]


OPEN_BLOCKERS = [
    "Run full hosted LLM baselines on all 50 v0.3.0 tasks.",
    "Run at least one local/open-source model baseline through the OpenAI-compatible protocol.",
    "Collect representative redacted hosted-LLM audit traces.",
    "Execute the private holdout protocol on an evaluator-controlled host.",
    "Finalize public license and citation metadata.",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def artifact_entry(spec: dict[str, Any]) -> dict[str, Any]:
    path = ROOT / spec["path"]
    entry = dict(spec)
    entry["exists"] = path.exists()
    if path.exists():
        entry["bytes"] = path.stat().st_size
        entry["sha256"] = sha256(path)
    return entry


def build_index() -> dict[str, Any]:
    artifacts = [artifact_entry(spec) for spec in ARTIFACTS]
    missing = [entry["path"] for entry in artifacts if not entry["exists"]]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Reviewer-facing map of the supplementary material, generated from current workspace files.",
        "start_here": [
            "work/moneybench/README.md",
            "outputs/acceleratorbench-benchmark-card.md",
            "outputs/acceleratorbench-datasheet-v0.3.md",
            "outputs/acceleratorbench-responsible-use-v0.3.md",
            "outputs/acceleratorbench-task-coverage-v0.3.md",
            "outputs/acceleratorbench-task-provenance-v0.3.md",
            "outputs/acceleratorbench-market-catalog-v0.3.md",
            "outputs/acceleratorbench-metrics-and-evaluation.md",
            "outputs/acceleratorbench-score-rubric-v0.3.md",
            "outputs/acceleratorbench-scoring-consistency-audit-v0.3.md",
            "outputs/acceleratorbench-leaderboard-policy-v0.3.md",
            "outputs/acceleratorbench-leaderboard-stability-v0.3.md",
            "outputs/acceleratorbench-power-analysis-v0.3.md",
            "outputs/acceleratorbench-task-feasibility-audit-v0.3.md",
            "outputs/acceleratorbench-task-revision-ledger-v0.3.md",
            "outputs/acceleratorbench-reviewer-smoke-v0.3.md",
            "outputs/acceleratorbench-environment-report-v0.3.md",
            "outputs/acceleratorbench-simulator-invariant-audit-v0.3.md",
            "outputs/acceleratorbench-reproducibility-manifest-v0.3.md",
            "outputs/acceleratorbench-determinism-audit-v0.3.md",
            "outputs/acceleratorbench-validity-report-v0.3.md",
            "outputs/acceleratorbench-human-calibration-protocol-v0.3.md",
            "outputs/acceleratorbench-human-calibration-schema-v0.3.md",
            "outputs/acceleratorbench-human-calibration-analysis-v0.3.md",
            "outputs/acceleratorbench-human-calibration-packet-v0.3.md",
            "outputs/acceleratorbench-claim-evidence-v0.3.md",
            "outputs/acceleratorbench-license-readiness-v0.3.md",
            "outputs/acceleratorbench-release-metadata-checklist-v0.3.md",
            "outputs/acceleratorbench-submission-gate-v0.3.md",
            "outputs/acceleratorbench-submission-manifest-v0.3.md",
            "outputs/acceleratorbench-reviewer-risk-audit-v0.3.md",
            "outputs/acceleratorbench-failure-mode-audit-v0.3.md",
            "outputs/acceleratorbench-submission-action-plan-v0.3.md",
            "outputs/acceleratorbench-experiment-matrix-v0.3.md",
            "outputs/acceleratorbench-cost-accounting-v0.3.md",
            "outputs/acceleratorbench-baseline-execution-plan-v0.3.md",
            "outputs/acceleratorbench-provider-run-status-v0.3.md",
            "outputs/acceleratorbench-provider-comparability-audit-v0.3.md",
            "outputs/acceleratorbench-provider-contract-audit-v0.3.md",
            "outputs/acceleratorbench-contamination-leakage-audit-v0.3.md",
            "outputs/acceleratorbench-result-integrity-audit-v0.3.md",
            "outputs/acceleratorbench-paper-tables-v0.3.md",
            "outputs/acceleratorbench-model-result-cards-v0.3.md",
            "outputs/acceleratorbench-citation-audit-v0.3.md",
            "outputs/acceleratorbench-private-holdout-smoke-v0.3.md",
            "outputs/acceleratorbench-publication-audit-v0.3.md",
        ],
        "commands": COMMANDS,
        "artifacts": artifacts,
        "summary": {
            "artifact_count": len(artifacts),
            "present": sum(1 for entry in artifacts if entry["exists"]),
            "missing": len(missing),
            "missing_paths": missing,
            "open_blockers": len(OPEN_BLOCKERS),
        },
        "open_blockers": OPEN_BLOCKERS,
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    artifact_rows = [
        [
            entry["category"],
            entry["path"],
            "yes" if entry["exists"] else "missing",
            entry.get("bytes", ""),
            entry["role"],
        ]
        for entry in payload["artifacts"]
    ]
    command_rows = [[row["purpose"], row["cwd"], f"`{row['command']}`"] for row in payload["commands"]]
    lines = [
        "# FounderBench v0.3 Reviewer Index",
        "",
        "This generated index is the suggested starting point for reviewing the supplementary package. It maps each major artifact to its review purpose and records file presence plus checksums in the JSON companion.",
        "",
        "## Start Here",
        "",
    ]
    lines.extend(f"- `{path}`" for path in payload["start_here"])
    lines.extend(
        [
            "",
            "## Reproduction Commands",
            "",
            markdown_table(["Purpose", "Working Directory", "Command"], command_rows),
            "",
            "## Artifact Map",
            "",
            markdown_table(["Category", "Path", "Present", "Bytes", "Review Purpose"], artifact_rows),
            "",
            "## Current Open Blockers",
            "",
        ]
    )
    lines.extend(f"- {blocker}" for blocker in payload["open_blockers"])
    lines.extend(
        [
            "",
            "## Integrity",
            "",
            "Use `release/acceleratorbench-v0.3.0/SHA256SUMS.json` for bundled artifact verification. The bundle also includes `release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md`, generated after the checksum manifest to verify the bundled files. The JSON version of this reviewer index includes per-file SHA-256 values for the source workspace artifacts listed above.",
            "",
        ]
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_index(json_output: Path, markdown_output: Path) -> None:
    payload = build_index()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reviewer-facing supplementary package index.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_index(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
