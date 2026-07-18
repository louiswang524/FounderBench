from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


def build_protocol() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Protocol for expert or human-founder calibration of the synthetic startup-agent task suite.",
        "status": "protocol_only_not_executed",
        "research_questions": [
            "Do task incentives match expert startup-operator judgment?",
            "Do score components reward decisions that experts consider sensible under the stated constraints?",
            "Which task families are too easy, too hard, or underspecified for human operators?",
            "How should model scores be interpreted relative to human/expert action rankings?",
        ],
        "participant_groups": [
            {
                "group": "startup operators",
                "target_n": "5-10",
                "eligibility": "Founders, operators, or accelerator mentors with experience evaluating early-stage startup decisions.",
                "role": "Rate scenario realism, action quality, and scoring alignment.",
            },
            {
                "group": "technical agent researchers",
                "target_n": "3-5",
                "eligibility": "Researchers or engineers familiar with LLM agent evaluation and tool-use benchmarks.",
                "role": "Rate benchmark clarity, action interface coverage, and anti-gaming risks.",
            },
        ],
        "task_sampling": {
            "strategy": "stratified_by_family",
            "minimum_tasks": 20,
            "recommended_tasks": 30,
            "coverage_rule": "Sample at least two tasks from each of the 10 task families; include public_dev and public_test tasks.",
            "materials": [
                "task card",
                "market catalog entry",
                "action semantics",
                "score rubric",
                "representative baseline trace when available",
            ],
        },
        "review_instrument": [
            {
                "item": "scenario_realism",
                "scale": "1-5 Likert",
                "prompt": "The startup situation is plausible enough for evaluating business-decision quality.",
            },
            {
                "item": "action_coverage",
                "scale": "1-5 Likert",
                "prompt": "The available structured actions cover the main reasonable moves in this scenario.",
            },
            {
                "item": "score_alignment",
                "scale": "1-5 Likert",
                "prompt": "The scoring rubric rewards decisions I would consider operationally sound.",
            },
            {
                "item": "difficulty",
                "scale": "too_easy / appropriate / too_hard / ambiguous",
                "prompt": "The task difficulty is appropriate for differentiating agents.",
            },
            {
                "item": "best_action_ranking",
                "scale": "ranked list",
                "prompt": "Rank the top three actions or action sequences you would recommend.",
            },
            {
                "item": "gaming_risk",
                "scale": "free text",
                "prompt": "Describe any way a model could exploit the task without making a sensible business decision.",
            },
        ],
        "analysis_plan": [
            "Report mean and distribution of scenario_realism, action_coverage, and score_alignment by task family.",
            "Flag tasks with mean score_alignment below 3.5 or more than 30% ambiguous difficulty labels.",
            "Compute agreement between expert top-action rankings and high-scoring baseline/model trajectories.",
            "Qualitatively summarize gaming risks and convert accepted issues into task or rubric revisions.",
            "Keep expert calibration separate from the official leaderboard until the protocol has been executed.",
        ],
        "reporting_fields": [
            "participant_count_by_group",
            "task_ids_reviewed",
            "family_coverage",
            "mean_scenario_realism",
            "mean_action_coverage",
            "mean_score_alignment",
            "difficulty_distribution",
            "flagged_tasks",
            "recommended_revisions",
            "limitations",
        ],
        "claim_guardrails": [
            "Before execution, describe this only as a proposed calibration protocol.",
            "Do not claim that FounderBench is validated against human startup judgment until results are collected.",
            "Even after execution, treat expert agreement as construct-validity evidence, not proof of real-world startup success prediction.",
        ],
        "ethics_and_privacy": [
            "Do not collect confidential company details or private customer data.",
            "Allow participants to skip scenarios that overlap with nonpublic work.",
            "Report aggregate ratings and anonymized free-text themes.",
            "Record compensation, recruitment source, and conflicts of interest in the final study report.",
        ],
    }


def validate_protocol(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "protocol_only_not_executed":
        problems.append("Protocol status must not imply executed human results.")
    if len(payload.get("participant_groups", [])) < 2:
        problems.append("Expected at least two participant groups.")
    if len(payload.get("review_instrument", [])) < 5:
        problems.append("Expected at least five review instrument items.")
    if payload.get("task_sampling", {}).get("minimum_tasks", 0) < 20:
        problems.append("Expected calibration over at least 20 sampled tasks.")
    if not payload.get("claim_guardrails"):
        problems.append("Claim guardrails are required.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    group_rows = [
        [row["group"], row["target_n"], row["eligibility"], row["role"]]
        for row in payload["participant_groups"]
    ]
    instrument_rows = [
        [row["item"], row["scale"], row["prompt"]]
        for row in payload["review_instrument"]
    ]
    lines = [
        "# FounderBench v0.3 Human Calibration Protocol",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Research Questions",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["research_questions"])
    lines.extend(
        [
            "",
            "## Participant Groups",
            "",
            markdown_table(["Group", "Target N", "Eligibility", "Role"], group_rows),
            "",
            "## Task Sampling",
            "",
            markdown_table(
                ["Field", "Value"],
                [[key, value if not isinstance(value, list) else ", ".join(value)] for key, value in payload["task_sampling"].items()],
            ),
            "",
            "## Review Instrument",
            "",
            markdown_table(["Item", "Scale", "Prompt"], instrument_rows),
            "",
            "## Analysis Plan",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["analysis_plan"])
    lines.extend(["", "## Reporting Fields", ""])
    lines.extend(f"- `{item}`" for item in payload["reporting_fields"])
    lines.extend(["", "## Claim Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(["", "## Ethics and Privacy", ""])
    lines.extend(f"- {item}" for item in payload["ethics_and_privacy"])
    lines.extend(["", "## Validation", ""])
    problems = validate_protocol(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The protocol is internally valid and explicitly marked as not yet executed.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_protocol(json_output: Path, markdown_output: Path) -> None:
    payload = build_protocol()
    problems = validate_protocol(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate human/expert calibration protocol.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_protocol(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
