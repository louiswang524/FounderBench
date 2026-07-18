from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .task_coverage import build_coverage


VERSION = "0.3.0"


def build_audit() -> dict[str, Any]:
    coverage = build_coverage()
    split_counts = coverage["split_counts"]
    leakage_surfaces = [
        {
            "id": "released_public_task_definitions",
            "surface": "Public task definitions, task cards, coverage reports, seeds, allowed actions, and scoring metadata are included in the repository and supplementary package.",
            "status": "known_visible",
            "mitigation": "Treat public_dev and public_test as visible public splits; require disclosure for tuned agents and use a private evaluator-hosted holdout for hidden-suite claims.",
        },
        {
            "id": "prompt_contains_current_task_context",
            "surface": "Provider prompts include the current task id, task description, observation, allowed actions, and response schema.",
            "status": "intended_task_context",
            "mitigation": "Freeze prompt hashes and action schema so providers receive comparable task context without hidden evaluator metadata.",
        },
        {
            "id": "audit_traces_can_contain_prompts_or_responses",
            "surface": "Provider audit logs may contain prompts, redacted raw responses, parser failures, token usage, and latency metadata.",
            "status": "redaction_and_review_required",
            "mitigation": "Redact secrets and review traces before release; never publish private-holdout prompts or raw private task definitions during an active cycle.",
        },
        {
            "id": "older_provider_like_outputs",
            "surface": "Older exploratory provider-like files may exist in local workspaces and can have mismatched prompts, task counts, or benchmark versions.",
            "status": "excluded_until_validated",
            "mitigation": "Use provider-run-status, model-result-card, and submission-validation artifacts to exclude invalid or stale provider rows from paper claims.",
        },
        {
            "id": "task_aware_heuristic_family_knowledge",
            "surface": "The task-aware heuristic encodes task-family knowledge and can overfit the released public suite.",
            "status": "calibration_ceiling_not_agent_baseline",
            "mitigation": "Report it as a calibration ceiling and ablation target, not as evidence that LLM agents can operate startups.",
        },
    ]
    claim_guardrails = [
        "Do not call public_test hidden, unseen, secret, private, or contamination-free.",
        "Do not claim the benchmark is free from pretraining or post-release contamination; public tasks are intentionally visible.",
        "Do not treat the aggregate-only private holdout smoke report as an official hidden leaderboard.",
        "Require model submitters to disclose prompt tuning, agent tuning, or training on public tasks.",
        "Use only evaluator-hosted private tasks for hidden-suite claims, and report aggregate private fields without private task definitions during an active cycle.",
    ]
    split_controls = [
        {
            "split": "public_dev",
            "tasks": split_counts.get("public_dev", 0),
            "visibility": "released",
            "allowed_use": "prompt development, adapter debugging, task calibration, and ablation design",
            "hidden": False,
            "claim_rule": "Development evidence only; not an unseen generalization estimate.",
        },
        {
            "split": "public_test",
            "tasks": split_counts.get("public_test", 0),
            "visibility": "released",
            "allowed_use": "reported open evaluation with overfitting and contamination caveats",
            "hidden": False,
            "claim_rule": "Public benchmark score; not a private holdout or contamination-free score.",
        },
        {
            "split": "private_holdout",
            "tasks": 20,
            "visibility": "evaluator_controlled_protocol_only",
            "allowed_use": "future evaluator-hosted hidden evaluation",
            "hidden": True,
            "claim_rule": "Hidden-suite claims require official evaluator aggregate results; current release has no official private leaderboard.",
        },
    ]
    required_reviewer_checks = [
        "Confirm submitted model cards disclose whether public tasks were used for prompt, agent, or training development.",
        "Verify public reports do not describe public_test as hidden or contamination-free.",
        "Run the evaluator-hosted private holdout before accepting hidden-suite or anti-gaming claims.",
        "Compare public and private score deltas when official private results become available.",
        "Check prompt/protocol hashes and exclude runs whose prompts or task counts do not match current release.",
        "Review released audit traces for secret leakage and keep active private traces aggregate-only.",
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Contamination and leakage audit for public benchmark release, provider submissions, and private-holdout claim discipline.",
        "status": "public_suite_visible_private_holdout_not_executed",
        "summary": {
            "public_tasks": split_counts.get("public_dev", 0) + split_counts.get("public_test", 0),
            "public_dev": split_counts.get("public_dev", 0),
            "public_test": split_counts.get("public_test", 0),
            "private_holdout_protocol_exists": True,
            "official_private_leaderboard": False,
            "contamination_free_claim_supported": False,
            "leakage_surfaces": len(leakage_surfaces),
            "claim_guardrails": len(claim_guardrails),
            "required_reviewer_checks": len(required_reviewer_checks),
        },
        "split_controls": split_controls,
        "leakage_surfaces": leakage_surfaces,
        "claim_guardrails": claim_guardrails,
        "required_reviewer_checks": required_reviewer_checks,
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "public_suite_visible_private_holdout_not_executed":
        problems.append("status must keep public visibility and missing private holdout explicit.")
    summary = payload.get("summary", {})
    if summary.get("public_tasks") != 50:
        problems.append("public_tasks must be 50.")
    if summary.get("public_dev") != 30 or summary.get("public_test") != 20:
        problems.append("public_dev/public_test counts must be 30/20.")
    if summary.get("official_private_leaderboard") is not False:
        problems.append("official_private_leaderboard must remain false for current release.")
    if summary.get("contamination_free_claim_supported") is not False:
        problems.append("contamination_free_claim_supported must remain false for public tasks.")
    public_test = next((row for row in payload.get("split_controls", []) if row.get("split") == "public_test"), {})
    if public_test.get("hidden") is not False:
        problems.append("public_test must not be marked hidden.")
    guardrail_text = " ".join(payload.get("claim_guardrails", []))
    for required in ["Do not call public_test hidden", "Do not claim", "contamination"]:
        if required not in guardrail_text:
            problems.append(f"claim guardrails must include: {required}")
    if len(payload.get("leakage_surfaces", [])) < 5:
        problems.append("Expected at least five leakage surfaces.")
    if len(payload.get("required_reviewer_checks", [])) < 5:
        problems.append("Expected at least five reviewer checks.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    split_rows = [
        [row["split"], row["tasks"], row["visibility"], "yes" if row["hidden"] else "no", row["claim_rule"]]
        for row in payload["split_controls"]
    ]
    surface_rows = [
        [row["id"], row["status"], row["surface"], row["mitigation"]]
        for row in payload["leakage_surfaces"]
    ]
    lines = [
        "# FounderBench Contamination and Leakage Audit",
        "",
        "This generated audit keeps public-split visibility, trace leakage surfaces, and private-holdout claim limits explicit. It does not certify the public suite as contamination-free.",
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Split Controls",
        "",
        markdown_table(["Split", "Tasks", "Visibility", "Hidden", "Claim Rule"], split_rows),
        "",
        "## Leakage Surfaces",
        "",
        markdown_table(["ID", "Status", "Surface", "Mitigation"], surface_rows),
        "",
        "## Claim Guardrails",
        "",
        *[f"- {item}" for item in payload["claim_guardrails"]],
        "",
        "## Required Reviewer Checks",
        "",
        *[f"- {item}" for item in payload["required_reviewer_checks"]],
        "",
        "## Validation",
        "",
    ]
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The audit preserves the distinction between visible public results and future evaluator-hosted private-holdout claims.")
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
    parser = argparse.ArgumentParser(description="Generate FounderBench contamination/leakage audit artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
