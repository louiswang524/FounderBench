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
        "path": "work/founderbench/README.md",
        "role": "Start here for installation, task families, action space, and run commands.",
        "category": "orientation",
    },
    {
        "path": "work/founderbench/SPEC.md",
        "role": "Formal simulator and benchmark specification.",
        "category": "orientation",
    },
    {
        "path": "outputs/founderbench-action-semantics.md",
        "role": "Human-readable semantics for every structured action: required fields, costs, effects, risk triggers, and typical use cases.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-market-catalog.md",
        "role": "Fixed simulated market catalog documenting all 8 market ids, demand/competition/WTP/support parameters, observation rules, and settlement rules.",
        "category": "data",
    },
    {
        "path": "outputs/founderbench-benchmark-card.md",
        "role": "Dataset-style benchmark card with intended use, limitations, and scope.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-datasheet.md",
        "role": "Datasheet-style disclosure covering motivation, composition, curation, intended use, distribution, maintenance, and unsupported claims.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-responsible-use.md",
        "role": "Responsible-use, ethics, privacy, unsupported-use, and provider-submission disclosure statement.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-task-manifest.json",
        "role": "Fixed public 50-task suite, task families, splits, budgets, and scenario metadata.",
        "category": "data",
    },
    {
        "path": "outputs/founderbench-task-coverage.md",
        "role": "Task-suite balance, split, action, and capability coverage report.",
        "category": "data",
    },
    {
        "path": "outputs/founderbench-task-provenance.md",
        "role": "Task curation and provenance record documenting templates, seed rules, setup sources, score sources, and synthetic-data status.",
        "category": "data",
    },
    {
        "path": "outputs/founderbench-task-cards.md",
        "role": "Human-readable cards for all 50 tasks, including initial state, scoring metrics, expected actions, family, split, and horizon.",
        "category": "data",
    },
    {
        "path": "outputs/founderbench-metrics-and-evaluation.md",
        "role": "Primary score, solve criteria, diagnostic metrics, penalties, and comparison protocol.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-score-rubric.md",
        "role": "Family-level score components, penalty rules, bounds, and pass-threshold validation.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-scoring-consistency-audit.md",
        "role": "Score-object consistency audit over all deterministic raw task results, including bounds, pass threshold, metrics payloads, family coverage, and split coverage.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-metric-sensitivity.md",
        "role": "Sensitivity analysis comparing official bounded task score against normalized business, solve-rate, survival, revenue, cash, and risk diagnostics.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-baseline-leaderboard.json",
        "role": "Machine-readable leaderboard for included non-LLM baselines.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-leaderboard-policy.md",
        "role": "Leaderboard/reporting policy defining public, repeated-run, and future private-holdout tiers plus acceptance and rejection rules.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-leaderboard-stability.md",
        "role": "Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-baseline-raw.json",
        "role": "Task-level raw baseline results for random, conservative, heuristic, and task-aware heuristic policies.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-baseline-analysis.md",
        "role": "Bootstrap intervals, split summaries, family scores, and policy comparisons.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-result-integrity-audit.md",
        "role": "Raw-to-report integrity audit proving deterministic baseline rows in leaderboard, paper tables, and model comparison match raw task outputs.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-paper-tables.md",
        "role": "Paper-ready result tables generated from raw current release runs and validated provider availability.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-paper-figure-data.md",
        "role": "Paper figure datasets for leaderboard bars, family heatmaps, action-ablation drops, difficulty bands, and metric-sensitivity rankings.",
        "category": "paper",
    },
    {
        "path": "outputs/founderbench-paper-evidence-map.md",
        "role": "Section-by-section paper evidence crosswalk linking draft claims to supporting artifacts and excluded claims.",
        "category": "paper",
    },
    {
        "path": "outputs/founderbench-model-comparison.md",
        "role": "Unified leaderboard/comparison report that automatically incorporates validated hosted/local provider runs and keeps missing provider evidence explicit.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-model-result-cards.md",
        "role": "Reviewer-facing result cards summarizing deterministic baselines and planned provider submissions with validation, diagnostics, cost fields, and claim eligibility.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-ablation-report.md",
        "role": "Capability-ladder ablation from random to task-aware heuristic behavior.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-action-ablation.md",
        "role": "Action-space ablation showing how disabling discovery, growth, quality/support, pricing, runway/funding, and pivot actions changes task-aware baseline outcomes.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-paired-statistics.md",
        "role": "Paired score gaps, bootstrap intervals, raw and Holm-adjusted permutation p-values, effect sizes, and win/loss/tie counts over matched tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-power-analysis.md",
        "role": "Power and resolution analysis estimating minimum detectable score gaps for the public suite and warning against overclaiming close model differences.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-statistical-protocol.md",
        "role": "Pre-specified primary endpoint, paired comparison test, repeated-sampling, multiple-comparison, and claim rules for model comparisons.",
        "category": "metrics",
    },
    {
        "path": "outputs/founderbench-difficulty-calibration.md",
        "role": "Task difficulty bands, baseline solve-count calibration, family/split balance, and high-discrimination tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-task-feasibility-audit.md",
        "role": "Task-level feasibility and discrimination ledger identifying baseline-solved, saturated, high-discrimination, and external-calibration-needed tasks.",
        "category": "baseline_evidence",
    },
    {
        "path": "outputs/founderbench-task-revision-ledger.md",
        "role": "Change-control ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable task or rubric revisions.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-experiment-matrix.md",
        "role": "Paper-facing ledger of completed and missing baselines, ablations, uncertainty checks, audit traces, and holdout evidence.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-random-repeats.md",
        "role": "Repeated-seed calibration intervals for the stochastic random baseline.",
        "category": "uncertainty",
    },
    {
        "path": "outputs/founderbench-qualitative-traces.md",
        "role": "Representative deterministic success and failure traces for paper analysis.",
        "category": "qualitative",
    },
    {
        "path": "outputs/founderbench-reproduction-guide.md",
        "role": "End-to-end instructions for regenerating artifacts and validating submissions.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-reviewer-smoke.md",
        "role": "Fast reviewer smoke report checking task loading, one deterministic task execution, and included baseline submission validation.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-environment-report.md",
        "role": "Runtime and dependency report with Python version, import classification, import checks, and provider/local-model dependency notes.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-simulator-invariant-audit.md",
        "role": "Deterministic simulator stress audit checking state bounds, score bounds, and core environment invariants without claiming real-world validity.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-reproducibility-manifest.md",
        "role": "Source/output hashes, environment metadata, and reproduction commands for the current workspace.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-determinism-audit.md",
        "role": "Replay audit showing deterministic baselines reproduce stable task outcomes from fixed seeds.",
        "category": "reproducibility",
    },
    {
        "path": "outputs/founderbench-validity-report.md",
        "role": "Threats-to-validity matrix with mitigations, evidence paths, and remaining work.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-human-calibration-protocol.md",
        "role": "Expert/human-founder calibration protocol for checking task realism, action coverage, score alignment, difficulty, and gaming risks.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-human-calibration-schema.md",
        "role": "Machine-readable calibration response schema and validation contract for expert/human-founder reviews.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-human-calibration-template.json",
        "role": "Blank JSON template for collecting expert/human-founder calibration responses over required sampled tasks.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-human-calibration-analysis.md",
        "role": "Analyzer output for expert/human-founder calibration responses; currently records that no executed calibration submissions are included.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-human-calibration-packet.md",
        "role": "Recruitment and operator packet for executing expert/human-founder calibration while preserving not-executed claim guardrails.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-claim-evidence.md",
        "role": "Claim-evidence guardrail for supported, qualified, and unsupported paper wording.",
        "category": "documentation",
    },
    {
        "path": "outputs/founderbench-model-submission-template.md",
        "role": "Template for future model providers reporting a run.",
        "category": "submission",
    },
    {
        "path": "outputs/founderbench-model-submission-schema.md",
        "role": "Machine-readable submission schema companion documenting accepted run payloads, required diagnostics, and authoritative validation command.",
        "category": "submission",
    },
    {
        "path": "outputs/founderbench-submission-bundle-protocol.md",
        "role": "Protocol and CLI helper for combining repeated provider/model seed runs into one validated submission bundle.",
        "category": "submission",
    },
    {
        "path": "outputs/founderbench-submission-validation.md",
        "role": "Validation report for the included complete baseline run.",
        "category": "submission",
    },
    {
        "path": "outputs/founderbench-provider-readiness.md",
        "role": "Environment readiness matrix and exact commands for hosted/local provider runs.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-cost-accounting.md",
        "role": "Provider token and cost-accounting protocol with usage normalization, price environment variables, formula, and reporting guardrails.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-baseline-execution-plan.md",
        "role": "Paper-grade hosted/local baseline execution plan with fairness controls, repeats, audit policy, commands, and acceptance criteria.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-experiment-runbook.md",
        "role": "Operator runbook for executing missing hosted/local model baselines, audits, repeat bundles, and post-run claim-gate updates.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-provider-run-status.md",
        "role": "Generated status report for planned current release provider/local runs, validation reports, audit outputs, and excluded older provider-like files.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-provider-comparability-audit.md",
        "role": "Protocol comparability audit checking shared task count, prompt/action contract, validation commands, repeat policy, cost fields, and self-consistency ablation treatment.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-provider-contract-audit.md",
        "role": "Provider-output contract audit checking parser error taxonomy and simulator diagnostics without claiming hosted/local LLM result evidence.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-contamination-leakage-audit.md",
        "role": "Public-split contamination/leakage audit that keeps public_test visibility, trace leakage risks, and private-holdout claim guardrails explicit.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/founderbench-prompt-protocol.md",
        "role": "Canonical LLM prompt contract, provider message wrappers, action vocabulary, and prompt/protocol hashes.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-license-readiness.md",
        "role": "License and citation metadata readiness checks plus owner decisions required before public release.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-release-metadata-checklist.md",
        "role": "Owner-facing release metadata checklist with license option matrix, CITATION template, and finalization steps.",
        "category": "publication_readiness",
    },
    {
        "path": "work/founderbench/LICENSE.template",
        "role": "Non-final owner-facing template for creating the required public LICENSE file.",
        "category": "publication_readiness",
    },
    {
        "path": "work/founderbench/CITATION.cff.template",
        "role": "Non-final owner-facing CITATION.cff template with placeholders for authors, repository URL, and selected license.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-submission-gate.md",
        "role": "Top-level go/no-go submission gate combining publication, experiment, provider, claim, and license readiness.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-submission-manifest.md",
        "role": "Compact reviewer-facing manifest of included evidence, supported claims, excluded claims, reproduction commands, and remaining gate blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-completion-audit.md",
        "role": "Goal-level completion audit mapping the active publishable-benchmark objective to current evidence and unresolved blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-reviewer-risk-audit.md",
        "role": "Pre-submission reviewer-risk audit listing likely reviewer objections, current evidence, open risks, and required responses.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-failure-mode-audit.md",
        "role": "AI research failure-mode audit covering code bugs, citation hallucination, result hallucination, shortcut reliance, bug-as-insight, methodology fabrication, and frame-lock.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-paper-claim-lint.md",
        "role": "Text-level paper and benchmark-card lint checking required limitation disclosures and selected unsupported positive claim wording.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-submission-action-plan.md",
        "role": "Concrete action plan mapping each failing submission gate to owners, commands, expected outputs, and claim impact.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-local-openai-compatible-protocol.md",
        "role": "Protocol for running local open-source models through an OpenAI-compatible endpoint.",
        "category": "provider_runs",
    },
    {
        "path": "outputs/founderbench-private-holdout-evaluator-protocol.md",
        "role": "Evaluator-host protocol for secret-seeded hidden task execution, aggregate reporting, and anti-gaming controls.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/founderbench-private-holdout-smoke.md",
        "role": "Aggregate-only smoke report proving the private-holdout evaluator harness runs without exposing hidden task definitions; not an official private leaderboard.",
        "category": "anti_gaming",
    },
    {
        "path": "work/founderbench/founderbench/private_holdout_evaluator.py",
        "role": "Executable private-holdout evaluator harness that generates secret-selected private episodes in memory and emits aggregate-only reports by default.",
        "category": "anti_gaming",
    },
    {
        "path": "outputs/founderbench-publication-audit.md",
        "role": "Submission-readiness matrix mapping benchmark requirements to concrete evidence and blockers.",
        "category": "publication_readiness",
    },
    {
        "path": "outputs/founderbench-paper-draft.md",
        "role": "Paper-facing draft with motivation, benchmark design, experiments, and limitations.",
        "category": "paper",
    },
    {
        "path": "outputs/founderbench-references.bib",
        "role": "BibTeX references used by the paper draft and related-work notes.",
        "category": "paper",
    },
    {
        "path": "outputs/founderbench-citation-audit.md",
        "role": "Local citation-context audit verifying paper citation numbering, BibTeX/provenance coverage, and intended citation use.",
        "category": "paper",
    },
    {
        "path": "release/founderbench/SHA256SUMS.json",
        "role": "Release-bundle checksum manifest for integrity verification.",
        "category": "release",
    },
    {
        "path": "release/founderbench/BUNDLE-INTEGRITY.md",
        "role": "Release-bundle integrity report verifying bundled files against SHA256SUMS.json.",
        "category": "release",
    },
]


COMMANDS = [
    {
        "purpose": "Run tests",
        "command": "python -m unittest discover -s tests -v",
        "cwd": "work/founderbench",
    },
    {
        "purpose": "Regenerate generated artifacts",
        "command": "python -m founderbench.release regenerate",
        "cwd": "work/founderbench",
    },
    {
        "purpose": "Validate generated artifacts and tests",
        "command": "python -m founderbench.release validate",
        "cwd": "work/founderbench",
    },
    {
        "purpose": "Build supplementary bundle",
        "command": "python -m founderbench.release bundle",
        "cwd": "work/founderbench",
    },
    {
        "purpose": "Validate a model submission",
        "command": "python -m founderbench.submission --input ..\\..\\outputs\\provider-run.json --report ..\\..\\outputs\\provider-run-submission-report.md",
        "cwd": "work/founderbench",
    },
    {
        "purpose": "Combine repeated model runs",
        "command": "python -m founderbench.submission_bundle --input ..\\..\\outputs\\provider-seed0.json --input ..\\..\\outputs\\provider-seed1.json --output ..\\..\\outputs\\provider-repeats.json --report ..\\..\\outputs\\provider-repeats-submission-report.md",
        "cwd": "work/founderbench",
    },
]


OPEN_BLOCKERS = [
    "Run full hosted LLM baselines on all 50 current tasks.",
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
            "work/founderbench/README.md",
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-datasheet.md",
            "outputs/founderbench-responsible-use.md",
            "outputs/founderbench-task-coverage.md",
            "outputs/founderbench-task-provenance.md",
            "outputs/founderbench-market-catalog.md",
            "outputs/founderbench-metrics-and-evaluation.md",
            "outputs/founderbench-score-rubric.md",
            "outputs/founderbench-scoring-consistency-audit.md",
            "outputs/founderbench-leaderboard-policy.md",
            "outputs/founderbench-leaderboard-stability.md",
            "outputs/founderbench-power-analysis.md",
            "outputs/founderbench-task-feasibility-audit.md",
            "outputs/founderbench-task-revision-ledger.md",
            "outputs/founderbench-reviewer-smoke.md",
            "outputs/founderbench-environment-report.md",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-reproducibility-manifest.md",
            "outputs/founderbench-determinism-audit.md",
            "outputs/founderbench-validity-report.md",
            "outputs/founderbench-human-calibration-protocol.md",
            "outputs/founderbench-human-calibration-schema.md",
            "outputs/founderbench-human-calibration-analysis.md",
            "outputs/founderbench-human-calibration-packet.md",
            "outputs/founderbench-claim-evidence.md",
            "outputs/founderbench-license-readiness.md",
            "outputs/founderbench-release-metadata-checklist.md",
            "outputs/founderbench-submission-gate.md",
            "outputs/founderbench-submission-manifest.md",
            "outputs/founderbench-reviewer-risk-audit.md",
            "outputs/founderbench-failure-mode-audit.md",
            "outputs/founderbench-submission-action-plan.md",
            "outputs/founderbench-experiment-matrix.md",
            "outputs/founderbench-cost-accounting.md",
            "outputs/founderbench-baseline-execution-plan.md",
            "outputs/founderbench-provider-run-status.md",
            "outputs/founderbench-provider-comparability-audit.md",
            "outputs/founderbench-provider-contract-audit.md",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-result-integrity-audit.md",
            "outputs/founderbench-paper-tables.md",
            "outputs/founderbench-model-result-cards.md",
            "outputs/founderbench-citation-audit.md",
            "outputs/founderbench-private-holdout-smoke.md",
            "outputs/founderbench-publication-audit.md",
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
        "# FounderBench Reviewer Index",
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
            "Use `release/founderbench/SHA256SUMS.json` for bundled artifact verification. The bundle also includes `release/founderbench/BUNDLE-INTEGRITY.md`, generated after the checksum manifest to verify the bundled files. The JSON version of this reviewer index includes per-file SHA-256 values for the source workspace artifacts listed above.",
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
