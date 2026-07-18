from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .task_feasibility_audit import build_audit as build_task_feasibility_audit


VERSION = "0.3.0"


def build_ledger() -> dict[str, Any]:
    feasibility = build_task_feasibility_audit()
    rows: list[dict[str, Any]] = []
    for row in feasibility["task_rows"]:
        if row["feasibility_status"] != "needs_external_calibration":
            continue
        rows.append(
            {
                "issue_id": f"REV-{row['task_id']}",
                "task_id": row["task_id"],
                "family": row["family"],
                "split": row["split"],
                "source": "task_feasibility_audit",
                "status": "pending_external_calibration",
                "severity": "major",
                "evidence": {
                    "difficulty_band": row["difficulty_band"],
                    "solved_by_deterministic_baselines": row["solved_by"],
                    "best_policy": row["best_policy"],
                    "best_score": row["best_score"],
                    "score_spread": row["score_spread"],
                },
                "revision_question": "Is this task genuinely difficult for startup reasoning, underspecified, or mis-scored?",
                "required_next_evidence": [
                    "hosted/local LLM trajectory on the task",
                    "expert/human-founder calibration review",
                    "reference action sequence or rubric inspection",
                ],
                "allowed_resolution": [
                    "keep_without_change_after_external_calibration",
                    "revise_task_text_or_constraints",
                    "revise_score_rubric",
                    "move_to_harder_or_diagnostic_subset",
                    "retire_or_replace_in_next_version",
                ],
                "claim_guardrail": "Do not claim this task is feasible, impossible, or validated until at least one required evidence source is recorded.",
            }
        )
    source_queue = [
        {
            "source": "human_calibration_analysis",
            "current_status": "not_executed",
            "expected_input": "flagged_tasks and recommended_revisions from executed expert/human-founder submissions",
            "ledger_action": "Create or update task-level rows with participant-count and conflict-disclosure metadata.",
        },
        {
            "source": "hosted_llm_audit_traces",
            "current_status": "missing",
            "expected_input": "validated redacted provider traces for representative successes and failures",
            "ledger_action": "Separate strategic failures from parser/provider failures before revising tasks.",
        },
        {
            "source": "private_holdout_evaluator",
            "current_status": "smoke_only_not_official",
            "expected_input": "evaluator-host aggregate and trace-safe issue reports",
            "ledger_action": "Record hidden-suite gaming or robustness issues without exposing private task definitions.",
        },
        {
            "source": "reviewer_feedback",
            "current_status": "not_collected",
            "expected_input": "paper-reviewer or external-auditor comments mapped to task ids or rubric sections",
            "ledger_action": "Track decision, owner, and evidence before changing public tasks or claims.",
        },
    ]
    status_counts = Counter(row["status"] for row in rows)
    family_counts = Counter(row["family"] for row in rows)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Task and rubric revision ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable benchmark changes.",
        "status": "open_revision_ledger_no_executed_human_rows",
        "scope": "v0.3.0 public task suite and scoring rubric",
        "claim_guardrails": [
            "This ledger is a change-control artifact, not evidence that human calibration has been executed.",
            "Rows derived from deterministic feasibility audits mark tasks for external calibration; they do not prove task defects.",
            "Do not modify official task definitions for a paper result after model runs unless the version is incremented and affected claims are regenerated.",
            "Resolved rows must cite concrete evidence and record whether scores, task text, or paper wording changed.",
        ],
        "summary": {
            "open_revision_rows": len(rows),
            "status_counts": dict(sorted(status_counts.items())),
            "families_with_open_rows": len(family_counts),
            "open_rows_by_family": dict(sorted(family_counts.items())),
            "executed_human_revision_rows": 0,
        },
        "source_queue": source_queue,
        "revision_rows": rows,
    }


def validate_ledger(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload.get("status") != "open_revision_ledger_no_executed_human_rows":
        problems.append("Ledger status must not imply executed human revisions.")
    rows = payload.get("revision_rows", [])
    if not rows:
        problems.append("Expected open revision rows from tasks needing external calibration.")
    if payload.get("summary", {}).get("executed_human_revision_rows") != 0:
        problems.append("Default v0.3 ledger must not include executed human revision rows.")
    if len(payload.get("source_queue", [])) < 4:
        problems.append("Expected queued sources for human calibration, provider traces, holdout, and reviewer feedback.")
    for row in rows:
        if row.get("status") != "pending_external_calibration":
            problems.append(f"{row.get('issue_id')} has unexpected status {row.get('status')}.")
        if not row.get("required_next_evidence"):
            problems.append(f"{row.get('issue_id')} must list required next evidence.")
        if not row.get("claim_guardrail"):
            problems.append(f"{row.get('issue_id')} must include a claim guardrail.")
    if not any("not evidence" in guardrail for guardrail in payload.get("claim_guardrails", [])):
        problems.append("Ledger claim guardrails must state it is not executed evidence.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    source_rows = [
        [row["source"], row["current_status"], row["expected_input"], row["ledger_action"]]
        for row in payload["source_queue"]
    ]
    revision_rows = [
        [
            row["issue_id"],
            row["task_id"],
            row["family"],
            row["split"],
            row["status"],
            row["evidence"]["best_policy"],
            row["evidence"]["best_score"],
            row["evidence"]["score_spread"],
            row["revision_question"],
        ]
        for row in payload["revision_rows"]
    ]
    lines = [
        "# FounderBench v0.3 Task Revision Ledger",
        "",
        payload["purpose"],
        "",
        f"Status: `{payload['status']}`",
        "",
        f"Scope: `{payload['scope']}`",
        "",
        "## Claim Guardrails",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["claim_guardrails"])
    lines.extend(
        [
            "",
            "## Summary",
            "",
            markdown_table(["Metric", "Value"], summary_rows),
            "",
            "## Queued Evidence Sources",
            "",
            markdown_table(["Source", "Current Status", "Expected Input", "Ledger Action"], source_rows),
            "",
            "## Open Revision Rows",
            "",
        ]
    )
    if revision_rows:
        lines.append(markdown_table(["Issue", "Task", "Family", "Split", "Status", "Best Policy", "Best Score", "Spread", "Revision Question"], revision_rows))
    else:
        lines.append("No open revision rows are currently recorded.")
    lines.extend(["", "## Required Resolution Evidence", ""])
    for row in payload["revision_rows"]:
        evidence = "; ".join(row["required_next_evidence"])
        allowed = "; ".join(row["allowed_resolution"])
        lines.append(f"- `{row['issue_id']}`: required evidence: {evidence}. Allowed resolutions: {allowed}.")
    lines.extend(["", "## Validation", ""])
    problems = validate_ledger(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The ledger records open calibration-driven revision questions without claiming executed human or provider evidence.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_ledger(json_output: Path, markdown_output: Path) -> None:
    payload = build_ledger()
    problems = validate_ledger(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench task revision ledger.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_ledger(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
