from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .submission import EXPECTED_VERSION, REQUIRED_DIAGNOSTICS
from .tasks import TASKS


VERSION = EXPECTED_VERSION
TASK_IDS = [task.task_id for task in TASKS]


def build_schema() -> dict[str, Any]:
    diagnostic_properties = {
        "invalid_actions": {"type": "integer", "minimum": 0},
        "over_budget_decisions": {"type": "integer", "minimum": 0},
        "provider_errors": {"type": "integer", "minimum": 0},
        "provider_error_categories": {"type": "object", "additionalProperties": {"type": "integer", "minimum": 0}},
        "total_actions": {"type": "integer", "minimum": 0},
        "decision_latency_s": {"type": "number", "minimum": 0},
        "simulated_api_cost": {"type": "number", "minimum": 0},
        "provider_prompt_tokens": {"type": "integer", "minimum": 0},
        "provider_completion_tokens": {"type": "integer", "minimum": 0},
        "provider_total_tokens": {"type": "integer", "minimum": 0},
        "estimated_provider_cost_usd": {"type": "number", "minimum": 0},
    }
    task_result_schema = {
        "type": "object",
        "required": ["task_id", "family", "split", "score", "summary", "diagnostics"],
        "additionalProperties": True,
        "properties": {
            "task_id": {"type": "string", "enum": TASK_IDS},
            "family": {"type": "string"},
            "split": {"type": "string", "enum": ["public_dev", "public_test"]},
            "score": {
                "type": "object",
                "required": ["task_id", "name", "score", "passed", "components", "notes"],
                "additionalProperties": True,
                "properties": {
                    "task_id": {"type": "string", "enum": TASK_IDS},
                    "name": {"type": "string"},
                    "score": {"type": "number", "minimum": 0, "maximum": 100},
                    "passed": {"type": "boolean"},
                    "components": {"type": "object"},
                    "notes": {"type": "array", "items": {"type": "string"}},
                },
            },
            "summary": {
                "type": "object",
                "required": ["cash", "reputation", "customers", "recurring_revenue", "risk_penalty", "bankrupt"],
                "additionalProperties": True,
            },
            "diagnostics": {
                "type": "object",
                "required": sorted(REQUIRED_DIAGNOSTICS),
                "additionalProperties": True,
                "properties": diagnostic_properties,
            },
        },
    }
    run_schema = {
        "type": "object",
        "required": [
            "policy",
            "benchmark_version",
            "tasks",
            "solved",
            "solve_rate",
            "average_task_score",
            "results",
            "diagnostics",
            "splits",
        ],
        "additionalProperties": True,
        "properties": {
            "policy": {"type": "string"},
            "benchmark_version": {"const": VERSION},
            "tasks": {"const": 50},
            "solved": {"type": "integer", "minimum": 0, "maximum": 50},
            "solve_rate": {"type": "number", "minimum": 0, "maximum": 1},
            "average_task_score": {"type": "number", "minimum": 0, "maximum": 100},
            "public_dev_score": {"type": "number", "minimum": 0, "maximum": 100},
            "public_test_score": {"type": "number", "minimum": 0, "maximum": 100},
            "shutdown_rate": {"type": "number", "minimum": 0, "maximum": 1},
            "average_final_cash": {"type": "number"},
            "average_risk_penalty": {"type": "number", "minimum": 0},
            "results": {"type": "array", "minItems": 50, "maxItems": 50, "items": task_result_schema},
            "diagnostics": {
                "type": "object",
                "required": sorted(REQUIRED_DIAGNOSTICS),
                "additionalProperties": True,
                "properties": diagnostic_properties,
            },
            "splits": {
                "type": "object",
                "required": ["public_dev", "public_test"],
                "additionalProperties": True,
            },
        },
    }
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://FounderBench.local/schemas/model-submission.schema.json",
        "title": "FounderBench Model Submission",
        "description": "Machine-readable schema for raw model run submissions. The authoritative validator remains python -m moneybench.submission, which also checks task-id set equality and diagnostic consistency.",
        "benchmark": "FounderBench",
        "version": VERSION,
        "accepted_payload_shapes": [
            "single run object",
            "array of run objects",
            "object with runs array",
        ],
        "required_task_ids": TASK_IDS,
        "required_diagnostics": sorted(REQUIRED_DIAGNOSTICS),
        "oneOf": [
            {"$ref": "#/$defs/run"},
            {"type": "array", "items": {"$ref": "#/$defs/run"}},
            {
                "type": "object",
                "required": ["runs"],
                "properties": {"runs": {"type": "array", "items": {"$ref": "#/$defs/run"}}},
            },
        ],
        "$defs": {
            "run": run_schema,
            "task_result": task_result_schema,
        },
        "validator_command": "python -m moneybench.submission --input outputs/provider-run.json --report outputs/provider-run-submission-report.md",
    }


def validate_schema(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if len(payload.get("required_task_ids", [])) != 50:
        problems.append("Expected exactly 50 required task ids.")
    if set(payload.get("required_diagnostics", [])) != REQUIRED_DIAGNOSTICS:
        problems.append("Required diagnostics do not match the submission validator.")
    run_schema = payload.get("$defs", {}).get("run", {})
    if "results" not in run_schema.get("required", []):
        problems.append("Run schema must require task-level results.")
    if payload.get("validator_command") is None:
        problems.append("Schema must name the authoritative validator command.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    required_rows = [[field] for field in payload["$defs"]["run"]["required"]]
    diagnostics_rows = [[field] for field in payload["required_diagnostics"]]
    shape_rows = [[shape] for shape in payload["accepted_payload_shapes"]]
    lines = [
        "# FounderBench Model Submission Schema",
        "",
        payload["description"],
        "",
        "## Accepted Payload Shapes",
        "",
        markdown_table(["Shape"], shape_rows),
        "",
        "## Required Run Fields",
        "",
        markdown_table(["Field"], required_rows),
        "",
        "## Required Diagnostics",
        "",
        markdown_table(["Diagnostic"], diagnostics_rows),
        "",
        "## Task Coverage",
        "",
        f"- Required task ids: {len(payload['required_task_ids'])}",
        "- Required splits: `public_dev`, `public_test`",
        "- Every valid single run must contain exactly 50 task results.",
        "",
        "## Authoritative Validation",
        "",
        f"`{payload['validator_command']}`",
        "",
        "The JSON schema documents field shape. The Python validator additionally checks exact task-id coverage, split summaries, score typing, diagnostic consistency, and repeated-run payloads.",
        "",
        "## Validation",
        "",
    ]
    problems = validate_schema(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The schema is internally consistent with the current release submission validator.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_schema(json_output: Path, markdown_output: Path) -> None:
    payload = build_schema()
    problems = validate_schema(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate model submission JSON schema artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_schema(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
