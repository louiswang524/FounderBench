from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .tasks import TASKS


VERSION = "0.3.0"
DIFFICULTY_LABELS = ["too_easy", "appropriate", "too_hard", "ambiguous"]
LIKERT_FIELDS = ["scenario_realism", "action_coverage", "score_alignment"]
MIN_REVIEWS = 20


def sampled_task_ids() -> list[str]:
    ids: list[str] = []
    for start in range(1, 51, 5):
        ids.extend([f"FND-{start:03d}", f"FND-{start + 1:03d}"])
    return ids


def build_schema() -> dict[str, Any]:
    task_ids = sampled_task_ids()
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Machine-readable schema and blank template contract for expert/human-founder calibration responses.",
        "status": "schema_only_not_executed",
        "required_task_ids": task_ids,
        "difficulty_labels": DIFFICULTY_LABELS,
        "likert_fields": LIKERT_FIELDS,
        "minimum_reviews": MIN_REVIEWS,
        "submission_shape": {
            "participant_group": "startup_operator | agent_researcher | other",
            "participant_experience_years": "nonnegative number or null",
            "conflict_disclosure": "string",
            "task_reviews": [
                {
                    "task_id": "FND-001",
                    "scenario_realism": "integer 1-5",
                    "action_coverage": "integer 1-5",
                    "score_alignment": "integer 1-5",
                    "difficulty": "too_easy | appropriate | too_hard | ambiguous",
                    "top_actions": ["up to three structured action type strings"],
                    "gaming_risk": "string",
                    "recommended_revision": "string",
                    "flag_for_revision": "boolean",
                }
            ],
        },
        "aggregation_plan": [
            "Validate each participant submission before analysis.",
            "Aggregate mean scenario_realism, action_coverage, and score_alignment by task and family.",
            "Flag tasks with mean score_alignment below 3.5 or at least 30% ambiguous difficulty labels.",
            "Report anonymized gaming-risk themes and recommended revisions separately from the model leaderboard.",
        ],
        "claim_guardrails": [
            "This schema does not constitute executed human calibration evidence.",
            "Executed results may support construct-validity discussion, but not real-world startup prediction claims.",
        ],
    }


def blank_template() -> dict[str, Any]:
    reviews = []
    task_names = {task.task_id: task.name for task in TASKS}
    for task_id in sampled_task_ids():
        reviews.append(
            {
                "task_id": task_id,
                "task_name": task_names.get(task_id, ""),
                "scenario_realism": None,
                "action_coverage": None,
                "score_alignment": None,
                "difficulty": "",
                "top_actions": [],
                "gaming_risk": "",
                "recommended_revision": "",
                "flag_for_revision": False,
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "participant_group": "",
        "participant_experience_years": None,
        "conflict_disclosure": "",
        "task_reviews": reviews,
    }


def validate_submission(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"version must be {VERSION}.")
    reviews = payload.get("task_reviews")
    if not isinstance(reviews, list):
        return [*problems, "task_reviews must be a list."]
    if len(reviews) < MIN_REVIEWS:
        problems.append(f"Expected at least {MIN_REVIEWS} task reviews.")
    seen = set()
    valid_public_ids = {task.task_id for task in TASKS}
    for idx, review in enumerate(reviews):
        if not isinstance(review, dict):
            problems.append(f"task_reviews[{idx}] must be an object.")
            continue
        task_id = review.get("task_id")
        if task_id not in valid_public_ids:
            problems.append(f"task_reviews[{idx}] has unknown task_id {task_id}.")
        if task_id in seen:
            problems.append(f"Duplicate review for {task_id}.")
        seen.add(task_id)
        for field in LIKERT_FIELDS:
            value = review.get(field)
            if not isinstance(value, int) or not 1 <= value <= 5:
                problems.append(f"{task_id}.{field} must be an integer in 1..5.")
        if review.get("difficulty") not in DIFFICULTY_LABELS:
            problems.append(f"{task_id}.difficulty must be one of {DIFFICULTY_LABELS}.")
        top_actions = review.get("top_actions")
        if not isinstance(top_actions, list) or len(top_actions) > 3:
            problems.append(f"{task_id}.top_actions must be a list of at most three actions.")
        if not isinstance(review.get("flag_for_revision"), bool):
            problems.append(f"{task_id}.flag_for_revision must be boolean.")
    required = set(sampled_task_ids())
    missing_required = sorted(required - seen)
    if missing_required:
        problems.append(f"Missing required sampled task reviews: {', '.join(missing_required)}.")
    return problems


def validate_schema(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "schema_only_not_executed":
        problems.append("Schema status must not imply executed calibration results.")
    if len(payload.get("required_task_ids", [])) != MIN_REVIEWS:
        problems.append(f"Expected {MIN_REVIEWS} required sampled task ids.")
    if set(payload.get("difficulty_labels", [])) != set(DIFFICULTY_LABELS):
        problems.append("Difficulty labels are incomplete.")
    if set(payload.get("likert_fields", [])) != set(LIKERT_FIELDS):
        problems.append("Likert fields are incomplete.")
    template = blank_template()
    template_problems = validate_submission(template)
    if not template_problems:
        problems.append("Blank template should not validate as an executed submission.")
    expected_blank_failures = [problem for problem in template_problems if "must be an integer" in problem or "difficulty" in problem]
    if not expected_blank_failures:
        problems.append("Blank template should fail only because ratings are not filled.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# FounderBench v0.3 Human Calibration Schema",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Required Sample",
        "",
        markdown_table(
            ["Metric", "Value"],
            [
                ["minimum_reviews", payload["minimum_reviews"]],
                ["required_task_ids", ", ".join(payload["required_task_ids"])],
                ["difficulty_labels", ", ".join(payload["difficulty_labels"])],
                ["likert_fields", ", ".join(payload["likert_fields"])],
            ],
        ),
        "",
        "## Submission Shape",
        "",
        "```json",
        json.dumps(payload["submission_shape"], indent=2),
        "```",
        "",
        "## Aggregation Plan",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["aggregation_plan"])
    lines.extend(["", "## Claim Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(["", "## Validation", ""])
    problems = validate_schema(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The schema and blank template contract are internally consistent and explicitly not executed human evidence.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_schema(json_output: Path, markdown_output: Path, template_output: Path) -> None:
    payload = build_schema()
    problems = validate_schema(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)
    template_output.parent.mkdir(parents=True, exist_ok=True)
    template_output.write_text(json.dumps(blank_template(), indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate human calibration response schema and blank template.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    parser.add_argument("--template-output", required=True)
    args = parser.parse_args()
    write_schema(Path(args.json_output), Path(args.markdown_output), Path(args.template_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")
    print(f"Wrote {args.template_output}")


if __name__ == "__main__":
    main()
