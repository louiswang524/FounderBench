from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


SECTIONS: list[dict[str, Any]] = [
    {
        "id": "motivation",
        "title": "Motivation",
        "entries": [
            {
                "question": "Why was the benchmark created?",
                "answer": "To evaluate whether LLM agents can make repeated startup-like operating decisions under bounded resources, noisy market information, and risk penalties.",
            },
            {
                "question": "What is the primary evaluation unit?",
                "answer": "A fixed simulated startup episode with initial state, task objective, structured action space, horizon, seed, and bounded 0-100 score.",
            },
            {
                "question": "What should the benchmark not be used to claim?",
                "answer": "It should not be used to claim real-world startup success prediction, autonomous-company deployability, or hidden-suite leaderboard performance without additional evidence.",
            },
        ],
    },
    {
        "id": "composition",
        "title": "Composition",
        "entries": [
            {
                "question": "What does current release contain?",
                "answer": "50 public tasks across 10 task families, a deterministic simulator, an 8-market catalog, 13 structured actions, non-LLM baselines, provider adapters, validation tooling, and generated reviewer artifacts.",
            },
            {
                "question": "What are the public splits?",
                "answer": "FND-001..FND-030 are public_dev; FND-031..FND-050 are public_test. Both splits are released and visible.",
            },
            {
                "question": "Does current release include private task definitions?",
                "answer": "No. It includes a private-holdout blueprint, evaluator protocol, harness, and smoke report, but no official private leaderboard or hidden task definitions.",
            },
            {
                "question": "Does the artifact contain personal data, real company data, or human-subject data?",
                "answer": "No. current tasks are synthetic and template-generated; no real company records or human-subject source data are included.",
            },
        ],
    },
    {
        "id": "collection_and_curation",
        "title": "Collection and Curation",
        "entries": [
            {
                "question": "How were tasks created?",
                "answer": "Tasks were generated from 10 hand-designed synthetic templates with 5 public variants each, fixed seeds, setup functions, and task-family scoring functions.",
            },
            {
                "question": "How are scoring rules documented?",
                "answer": "The score rubric, task cards, task provenance report, task coverage report, metric-sensitivity report, and simulator invariant audit document score components, bounds, and validation checks.",
            },
            {
                "question": "Can public tasks be revised after model runs?",
                "answer": "Official task definitions should not be changed for a reported result without incrementing the benchmark version and regenerating affected claims.",
            },
        ],
    },
    {
        "id": "uses",
        "title": "Uses",
        "entries": [
            {
                "question": "What uses are intended?",
                "answer": "Research on LLM agents, sequential decision-making, structured action policies, cost-aware model comparison, and startup-operator simulation.",
            },
            {
                "question": "What uses are out of scope?",
                "answer": "Real-money trading, investment advice, company governance automation, legal/financial due diligence, or claims that a model can safely run a real company without human oversight.",
            },
            {
                "question": "How should public scores be reported?",
                "answer": "Public scores should name the version, task count, split visibility, prompt/protocol version, model identifier, run seed, diagnostics, and whether results are single-run or repeated.",
            },
        ],
    },
    {
        "id": "distribution_and_access",
        "title": "Distribution and Access",
        "entries": [
            {
                "question": "What files should be distributed?",
                "answer": "The release bundle, source package, task manifest/cards, generated reports, validation scripts, checksum manifest, and reproduction guide.",
            },
            {
                "question": "What metadata remains owner-dependent?",
                "answer": "Final public LICENSE and citation metadata are not owner-finalized in the current workspace and remain a publication blocker.",
            },
            {
                "question": "How are secrets handled?",
                "answer": "Provider keys and private-holdout secrets are environment variables only; generated artifacts record variable names, redacted traces, hashes, and aggregate diagnostics but not secret values.",
            },
        ],
    },
    {
        "id": "maintenance",
        "title": "Maintenance",
        "entries": [
            {
                "question": "How should future versions be maintained?",
                "answer": "Version task/rubric changes, keep public and private evaluation cycles separate, rotate private holdout secrets after each cycle, and preserve old release bundles for reproducibility.",
            },
            {
                "question": "How are issues tracked?",
                "answer": "Use the task revision ledger for calibration, provider-trace, holdout, and reviewer issues; do not silently edit reported tasks or rubrics.",
            },
            {
                "question": "What evidence is still needed for a final paper?",
                "answer": "Validated hosted/local LLM baselines, executed evaluator-host private holdout, executed human/expert calibration, and final owner-selected license/citation metadata.",
            },
        ],
    },
]


def build_datasheet() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Datasheet-style disclosure for benchmark/dataset submission review.",
        "status": "documentation_complete_external_evidence_still_missing",
        "artifact_summary": {
            "public_tasks": 50,
            "task_families": 10,
            "structured_actions": 13,
            "simulated_markets": 8,
            "contains_real_company_data": False,
            "contains_human_subject_data": False,
            "public_test_hidden": False,
            "official_private_leaderboard_included": False,
        },
        "sections": SECTIONS,
        "evidence_paths": [
            "outputs/founderbench-benchmark-card.md",
            "outputs/founderbench-task-provenance.md",
            "outputs/founderbench-task-coverage.md",
            "outputs/founderbench-contamination-leakage-audit.md",
            "outputs/founderbench-simulator-invariant-audit.md",
            "outputs/founderbench-license-readiness.md",
            "outputs/founderbench-completion-audit.md",
        ],
    }


def validate_datasheet(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("artifact_summary", {})
    if summary.get("public_tasks") != 50:
        problems.append("public_tasks must be 50.")
    if summary.get("task_families") != 10:
        problems.append("task_families must be 10.")
    if summary.get("structured_actions") != 13:
        problems.append("structured_actions must be 13.")
    for field in ["contains_real_company_data", "contains_human_subject_data", "public_test_hidden", "official_private_leaderboard_included"]:
        if summary.get(field) is not False:
            problems.append(f"{field} must be false for current release.")
    section_ids = {section["id"] for section in payload.get("sections", [])}
    for required in {"motivation", "composition", "collection_and_curation", "uses", "distribution_and_access", "maintenance"}:
        if required not in section_ids:
            problems.append(f"Missing datasheet section {required}.")
    for section in payload.get("sections", []):
        if len(section.get("entries", [])) < 3:
            problems.append(f"Section {section.get('id')} must have at least three entries.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required_phrase in ["real-world startup success", "public_test", "license", "human-subject"]:
        if required_phrase.lower() not in text:
            problems.append(f"Datasheet must mention {required_phrase}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# FounderBench Datasheet",
        "",
        "This generated datasheet provides benchmark/dataset-style disclosure for reviewers. It complements the benchmark card by answering composition, curation, intended-use, distribution, and maintenance questions in a fixed schema.",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Artifact Summary",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["artifact_summary"].items()]),
        "",
        "## Datasheet Questions",
        "",
    ]
    for section in payload["sections"]:
        lines.extend([f"### {section['title']}", ""])
        for entry in section["entries"]:
            lines.extend([f"**{entry['question']}**", "", entry["answer"], ""])
    lines.extend(["## Evidence Paths", ""])
    lines.extend(f"- `{path}`" for path in payload["evidence_paths"])
    lines.extend(["", "## Validation", ""])
    problems = validate_datasheet(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The datasheet covers required disclosure sections and keeps unsupported evidence claims explicit.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_datasheet(json_output: Path, markdown_output: Path) -> None:
    payload = build_datasheet()
    problems = validate_datasheet(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench datasheet artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_datasheet(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
