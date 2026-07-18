from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import family_name, markdown_table
from .human_calibration_schema import LIKERT_FIELDS, VERSION, validate_submission


FLAG_SCORE_THRESHOLD = 3.5
AMBIGUOUS_RATE_THRESHOLD = 0.30


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _empty_report(input_files: list[str]) -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Analyzer for executed expert/human-founder calibration responses.",
        "status": "no_submissions_found",
        "input_files": input_files,
        "participant_count": 0,
        "participant_count_by_group": {},
        "task_ids_reviewed": [],
        "family_coverage": {},
        "summary": {
            "mean_scenario_realism": None,
            "mean_action_coverage": None,
            "mean_score_alignment": None,
            "flagged_tasks": 0,
            "recommended_revisions": 0,
        },
        "task_rows": [],
        "family_rows": [],
        "difficulty_distribution": {},
        "top_action_counts": {},
        "flagged_tasks": [],
        "recommended_revisions": [],
        "claim_guardrails": [
            "No executed expert/human-founder calibration submissions were found.",
            "Do not cite this as human validation evidence until the status is executed.",
        ],
    }


def build_analysis(submissions: list[dict[str, Any]], input_files: list[str] | None = None) -> dict[str, Any]:
    input_files = input_files or []
    valid_submissions = []
    invalid = []
    for idx, submission in enumerate(submissions):
        problems = validate_submission(submission)
        if problems:
            invalid.append({"index": idx, "problems": problems})
        else:
            valid_submissions.append(submission)
    if not valid_submissions:
        report = _empty_report(input_files)
        report["invalid_submissions"] = invalid
        return report

    participant_groups = Counter(str(item.get("participant_group", "unspecified")) for item in valid_submissions)
    task_reviews: dict[str, list[dict[str, Any]]] = defaultdict(list)
    difficulty_counts: Counter[str] = Counter()
    action_counts: Counter[str] = Counter()
    revisions = []
    for participant_idx, submission in enumerate(valid_submissions):
        for review in submission["task_reviews"]:
            task_reviews[review["task_id"]].append(review)
            difficulty_counts[str(review["difficulty"])] += 1
            action_counts.update(str(action) for action in review.get("top_actions", []))
            if review.get("recommended_revision"):
                revisions.append(
                    {
                        "participant_index": participant_idx,
                        "task_id": review["task_id"],
                        "family": family_name(review["task_id"]),
                        "recommended_revision": review["recommended_revision"],
                    }
                )

    task_rows = []
    flagged_tasks = []
    for task_id, reviews in sorted(task_reviews.items()):
        ambiguous = sum(1 for review in reviews if review["difficulty"] == "ambiguous")
        row = {
            "task_id": task_id,
            "family": family_name(task_id),
            "reviews": len(reviews),
            "mean_scenario_realism": round(mean(review["scenario_realism"] for review in reviews), 3),
            "mean_action_coverage": round(mean(review["action_coverage"] for review in reviews), 3),
            "mean_score_alignment": round(mean(review["score_alignment"] for review in reviews), 3),
            "ambiguous_rate": round(ambiguous / len(reviews), 3),
            "revision_flags": sum(1 for review in reviews if review["flag_for_revision"]),
        }
        task_rows.append(row)
        if row["mean_score_alignment"] < FLAG_SCORE_THRESHOLD or row["ambiguous_rate"] >= AMBIGUOUS_RATE_THRESHOLD or row["revision_flags"]:
            flagged_tasks.append(row)

    by_family: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in task_rows:
        by_family[row["family"]].append(row)
    family_rows = [
        {
            "family": family,
            "tasks_reviewed": len(rows),
            "mean_scenario_realism": round(mean(row["mean_scenario_realism"] for row in rows), 3),
            "mean_action_coverage": round(mean(row["mean_action_coverage"] for row in rows), 3),
            "mean_score_alignment": round(mean(row["mean_score_alignment"] for row in rows), 3),
            "flagged_tasks": sum(1 for row in rows if row in flagged_tasks),
        }
        for family, rows in sorted(by_family.items())
    ]

    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Analyzer for executed expert/human-founder calibration responses.",
        "status": "executed",
        "input_files": input_files,
        "participant_count": len(valid_submissions),
        "participant_count_by_group": dict(sorted(participant_groups.items())),
        "invalid_submissions": invalid,
        "task_ids_reviewed": sorted(task_reviews),
        "family_coverage": {family: row["tasks_reviewed"] for family, row in ((row["family"], row) for row in family_rows)},
        "summary": {
            "mean_scenario_realism": round(mean(row["mean_scenario_realism"] for row in task_rows), 3),
            "mean_action_coverage": round(mean(row["mean_action_coverage"] for row in task_rows), 3),
            "mean_score_alignment": round(mean(row["mean_score_alignment"] for row in task_rows), 3),
            "flagged_tasks": len(flagged_tasks),
            "recommended_revisions": len(revisions),
        },
        "task_rows": task_rows,
        "family_rows": family_rows,
        "difficulty_distribution": dict(sorted(difficulty_counts.items())),
        "top_action_counts": dict(action_counts.most_common()),
        "flagged_tasks": flagged_tasks,
        "recommended_revisions": revisions,
        "claim_guardrails": [
            "Executed calibration supports construct-validity discussion only.",
            "Do not claim real-world startup success prediction from expert agreement.",
            "Report participant count, recruitment source, conflicts, and limitations with any paper claim.",
        ],
    }


def validate_analysis(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") not in {"no_submissions_found", "executed"}:
        problems.append("Status must be no_submissions_found or executed.")
    if payload.get("status") == "executed":
        if payload.get("participant_count", 0) < 1:
            problems.append("Executed analysis must include at least one valid participant submission.")
        if not payload.get("task_rows"):
            problems.append("Executed analysis must include task rows.")
        if not payload.get("family_rows"):
            problems.append("Executed analysis must include family rows.")
        if not set(LIKERT_FIELDS) <= {"scenario_realism", "action_coverage", "score_alignment"}:
            problems.append("Likert field configuration is inconsistent.")
    if not payload.get("claim_guardrails"):
        problems.append("Claim guardrails are required.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    task_rows = [
        [
            row["task_id"],
            row["family"],
            row["reviews"],
            row["mean_scenario_realism"],
            row["mean_action_coverage"],
            row["mean_score_alignment"],
            row["ambiguous_rate"],
            row["revision_flags"],
        ]
        for row in payload["task_rows"]
    ]
    family_rows = [
        [
            row["family"],
            row["tasks_reviewed"],
            row["mean_scenario_realism"],
            row["mean_action_coverage"],
            row["mean_score_alignment"],
            row["flagged_tasks"],
        ]
        for row in payload["family_rows"]
    ]
    lines = [
        "# FounderBench Human Calibration Analysis",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [["participant_count", payload["participant_count"]], *summary_rows]),
        "",
        "## Participant Groups",
        "",
    ]
    if payload["participant_count_by_group"]:
        lines.append(markdown_table(["Group", "Participants"], [[key, value] for key, value in payload["participant_count_by_group"].items()]))
    else:
        lines.append("No valid participant submissions were analyzed.")
    lines.extend(["", "## Family Coverage", ""])
    if family_rows:
        lines.append(markdown_table(["Family", "Tasks", "Realism", "Action Coverage", "Score Alignment", "Flagged Tasks"], family_rows))
    else:
        lines.append("No family coverage is available yet.")
    lines.extend(["", "## Task Rows", ""])
    if task_rows:
        lines.append(markdown_table(["Task", "Family", "Reviews", "Realism", "Action Coverage", "Score Alignment", "Ambiguous Rate", "Revision Flags"], task_rows))
    else:
        lines.append("No task-level calibration rows are available yet.")
    lines.extend(["", "## Flagged Tasks", ""])
    if payload["flagged_tasks"]:
        lines.append(markdown_table(["Task", "Family", "Score Alignment", "Ambiguous Rate", "Revision Flags"], [[row["task_id"], row["family"], row["mean_score_alignment"], row["ambiguous_rate"], row["revision_flags"]] for row in payload["flagged_tasks"]]))
    else:
        lines.append("No tasks are flagged because no executed calibration evidence is available, or all analyzed tasks passed the thresholds.")
    lines.extend(["", "## Claim Guardrails", ""])
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(["", "## Validation", ""])
    problems = validate_analysis(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The analysis payload is internally consistent.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_analysis(input_paths: list[Path], json_output: Path, markdown_output: Path) -> None:
    submissions = [load_json(path) for path in input_paths]
    payload = build_analysis(submissions, [str(path) for path in input_paths])
    problems = validate_analysis(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Analyze executed expert/human-founder calibration responses.")
    parser.add_argument("--input", action="append", default=[], help="Calibration response JSON. May be repeated.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_analysis([Path(path) for path in args.input], Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
