from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .human_calibration import build_protocol
from .human_calibration_schema import MIN_REVIEWS, sampled_task_ids


VERSION = "0.3.0"


def build_packet() -> dict[str, Any]:
    protocol = build_protocol()
    required_task_ids = sampled_task_ids()
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Recruitment and operator packet for executing expert/human-founder calibration without treating planned work as evidence.",
        "status": "recruitment_packet_not_executed",
        "minimum_participant_plan": {
            "startup_operators": 6,
            "accelerator_or_investor_mentors": 3,
            "agent_evaluation_researchers": 3,
            "minimum_total": 12,
            "rationale": "Separate startup-judgment validity from benchmark-interface validity while keeping the first calibration wave feasible.",
        },
        "required_task_sample": {
            "strategy": protocol["task_sampling"]["strategy"],
            "minimum_reviews_per_participant": MIN_REVIEWS,
            "required_task_ids": required_task_ids,
            "coverage_rule": protocol["task_sampling"]["coverage_rule"],
        },
        "materials": [
            {
                "path": "outputs/founderbench-human-calibration-protocol.md",
                "use": "Study purpose, participant groups, instrument, analysis plan, privacy notes, and claim guardrails.",
            },
            {
                "path": "outputs/founderbench-human-calibration-schema.json",
                "use": "Machine-readable response contract for validating completed reviews.",
            },
            {
                "path": "outputs/founderbench-human-calibration-template.json",
                "use": "Blank participant response template; do not treat blanks or synthetic examples as data.",
            },
            {
                "path": "outputs/founderbench-task-cards.md",
                "use": "Scenario cards for the required sampled tasks and optional extra review tasks.",
            },
            {
                "path": "outputs/founderbench-action-semantics.md",
                "use": "Action vocabulary reference so participants can rank structured actions consistently.",
            },
            {
                "path": "outputs/founderbench-score-rubric.md",
                "use": "Score-component reference for judging whether incentives match operator judgment.",
            },
            {
                "path": "outputs/founderbench-task-feasibility-audit.md",
                "use": "Task-level ledger for prioritizing external calibration on unsolved or ambiguous tasks.",
            },
            {
                "path": "outputs/founderbench-human-calibration-analysis.md",
                "use": "Generated analysis report; currently should state no executed submissions unless real responses are supplied.",
            },
        ],
        "collection_workflow": [
            "Confirm ethics/IRB requirements, compensation, recruitment source, and conflict-disclosure policy before contacting participants.",
            "Give each participant the task cards, action semantics, score rubric, and blank JSON response template.",
            "Ask participants to complete all required sampled tasks and optionally mark any scenario they skip because of confidentiality overlap.",
            "Validate each returned JSON response with `moneybench.human_calibration_schema.validate_submission` before analysis.",
            "Run `python -m moneybench.human_calibration_analysis --input <submission.json> --json-output <analysis.json> --markdown-output <analysis.md>` after real submissions are collected.",
            "Update the claim-evidence report, validity report, paper draft, and task revisions only after executed calibration has passed validation.",
        ],
        "review_questions": [
            "Is the startup situation plausible under the stated cash, market, and time constraints?",
            "Do the available actions cover the main reasonable operator moves?",
            "Does the scoring reward decisions you would consider sound for this scenario?",
            "Which task should be revised first, and why?",
            "What is the most likely way a model could exploit the task without making a sensible business decision?",
            "Which top three structured actions or action sequences would you recommend?",
        ],
        "expected_post_collection_outputs": [
            "validated participant JSON submissions stored outside the public release unless consent permits release",
            "regenerated human calibration analysis JSON and Markdown",
            "task revision ledger for accepted calibration issues",
            "paper wording update that reports participant counts, recruitment sources, conflicts, and limitations",
        ],
        "claim_guardrails": [
            "This packet is not executed human calibration evidence.",
            "Do not claim human agreement, construct validity, or expert validation until real participant submissions are collected and analyzed.",
            "Do not use synthetic, blank, or internally generated responses as human evidence.",
            "Even executed calibration can support task-realism and score-alignment discussion only; it cannot prove real-world startup success prediction.",
        ],
        "ethics_guardrails": [
            "Do not collect confidential company, customer, financial, or investment information.",
            "Record recruitment source, compensation, conflicts of interest, and any institutional ethics/IRB determination.",
            "Allow participants to skip scenarios that overlap with nonpublic work.",
            "Publish only aggregate ratings and anonymized themes unless explicit participant consent covers broader release.",
        ],
    }


def validate_packet(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "recruitment_packet_not_executed":
        problems.append("Packet status must not imply executed human results.")
    participant_plan = payload.get("minimum_participant_plan", {})
    if participant_plan.get("minimum_total", 0) < 10:
        problems.append("Expected a minimum participant plan of at least 10 reviewers.")
    if len([key for key in participant_plan if key not in {"minimum_total", "rationale"}]) < 3:
        problems.append("Expected at least three participant groups.")
    sample = payload.get("required_task_sample", {})
    if sample.get("minimum_reviews_per_participant", 0) < MIN_REVIEWS:
        problems.append(f"Expected at least {MIN_REVIEWS} required task reviews per participant.")
    if set(sample.get("required_task_ids", [])) != set(sampled_task_ids()):
        problems.append("Required task sample must match the calibration schema.")
    material_paths = {item.get("path") for item in payload.get("materials", [])}
    required_materials = {
        "outputs/founderbench-human-calibration-protocol.md",
        "outputs/founderbench-human-calibration-schema.json",
        "outputs/founderbench-human-calibration-template.json",
        "outputs/founderbench-task-cards.md",
    }
    missing_materials = sorted(required_materials - material_paths)
    if missing_materials:
        problems.append(f"Missing required materials: {', '.join(missing_materials)}.")
    workflow_text = " ".join(payload.get("collection_workflow", []))
    if "human_calibration_analysis" not in workflow_text:
        problems.append("Collection workflow must include the analyzer command.")
    if "IRB" not in " ".join(payload.get("ethics_guardrails", [])):
        problems.append("Ethics guardrails must mention institutional ethics/IRB determination.")
    if not any("not executed" in guardrail.lower() for guardrail in payload.get("claim_guardrails", [])):
        problems.append("Claim guardrails must state the packet is not executed evidence.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    participant_plan = payload["minimum_participant_plan"]
    participant_rows = [
        ["startup_operators", participant_plan["startup_operators"]],
        ["accelerator_or_investor_mentors", participant_plan["accelerator_or_investor_mentors"]],
        ["agent_evaluation_researchers", participant_plan["agent_evaluation_researchers"]],
        ["minimum_total", participant_plan["minimum_total"]],
    ]
    material_rows = [[item["path"], item["use"]] for item in payload["materials"]]
    sample = payload["required_task_sample"]
    lines = [
        "# FounderBench Human Calibration Recruitment Packet",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Participant Plan",
        "",
        markdown_table(["Group", "Minimum N"], participant_rows),
        "",
        participant_plan["rationale"],
        "",
        "## Required Task Sample",
        "",
        markdown_table(
            ["Field", "Value"],
            [
                ["strategy", sample["strategy"]],
                ["minimum_reviews_per_participant", sample["minimum_reviews_per_participant"]],
                ["coverage_rule", sample["coverage_rule"]],
                ["required_task_ids", ", ".join(sample["required_task_ids"])],
            ],
        ),
        "",
        "## Materials",
        "",
        markdown_table(["Path", "Use"], material_rows),
        "",
        "## Collection Workflow",
        "",
    ]
    lines.extend(f"{index}. {item}" for index, item in enumerate(payload["collection_workflow"], start=1))
    lines.extend(["", "## Review Questions", ""])
    lines.extend(f"- {item}" for item in payload["review_questions"])
    lines.extend(["", "## Expected Post-Collection Outputs", ""])
    lines.extend(f"- {item}" for item in payload["expected_post_collection_outputs"])
    lines.extend(["", "## Claim Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(["", "## Ethics Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["ethics_guardrails"])
    lines.extend(["", "## Validation", ""])
    problems = validate_packet(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The packet is internally consistent and explicitly marked as not executed human evidence.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_packet(json_output: Path, markdown_output: Path) -> None:
    payload = build_packet()
    problems = validate_packet(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate human calibration recruitment packet.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_packet(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
