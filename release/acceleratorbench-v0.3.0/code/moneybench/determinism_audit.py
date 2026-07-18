from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .task_runner import run_suite


VERSION = "0.3.0"
POLICIES = ["random", "conservative", "heuristic", "task_heuristic"]
EXCLUDED_FIELDS = {"decision_latency_s"}


def _strip_unstable(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _strip_unstable(item) for key, item in sorted(value.items()) if key not in EXCLUDED_FIELDS}
    if isinstance(value, list):
        return [_strip_unstable(item) for item in value]
    return value


def stable_payload(run: dict[str, Any]) -> dict[str, Any]:
    payload = copy.deepcopy(run)
    return _strip_unstable(payload)


def stable_hash(run: dict[str, Any]) -> str:
    encoded = json.dumps(stable_payload(run), sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_audit() -> dict[str, Any]:
    rows = []
    for policy in POLICIES:
        first = run_suite(policy, seed=0)
        second = run_suite(policy, seed=0)
        first_hash = stable_hash(first)
        second_hash = stable_hash(second)
        rows.append(
            {
                "policy": policy,
                "seed": 0,
                "tasks": first["tasks"],
                "first_hash": first_hash,
                "second_hash": second_hash,
                "stable_match": first_hash == second_hash,
                "score_match": first["average_task_score"] == second["average_task_score"],
                "solved_match": first["solved"] == second["solved"],
                "excluded_fields": sorted(EXCLUDED_FIELDS),
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Replay audit showing included deterministic baselines reproduce stable task outcomes from fixed seeds.",
        "scope": {
            "policies": POLICIES,
            "seed": 0,
            "runs_per_policy": 2,
            "excluded_fields": sorted(EXCLUDED_FIELDS),
            "exclusion_rationale": "Wall-clock decision latency is environment-dependent and excluded from stable-result hashing.",
        },
        "rows": rows,
        "summary": {
            "policies": len(rows),
            "stable_matches": sum(1 for row in rows if row["stable_match"]),
            "score_matches": sum(1 for row in rows if row["score_match"]),
            "solved_matches": sum(1 for row in rows if row["solved_match"]),
            "all_stable": all(row["stable_match"] for row in rows),
        },
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    rows = payload.get("rows", [])
    if len(rows) != len(POLICIES):
        problems.append(f"Expected {len(POLICIES)} policy rows, found {len(rows)}.")
    for row in rows:
        if row.get("policy") not in POLICIES:
            problems.append(f"Unexpected policy {row.get('policy')}.")
        if row.get("tasks") != 50:
            problems.append(f"{row.get('policy')}: expected 50 tasks.")
        if not row.get("stable_match"):
            problems.append(f"{row.get('policy')}: stable replay hash mismatch.")
        if not row.get("score_match"):
            problems.append(f"{row.get('policy')}: score mismatch.")
        if not row.get("solved_match"):
            problems.append(f"{row.get('policy')}: solved-count mismatch.")
    if not payload.get("summary", {}).get("all_stable"):
        problems.append("Summary all_stable must be true for this audit.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["policy"],
            row["seed"],
            row["tasks"],
            row["stable_match"],
            row["score_match"],
            row["solved_match"],
            row["first_hash"][:12],
            row["second_hash"][:12],
        ]
        for row in payload["rows"]
    ]
    lines = [
        "# FounderBench v0.3 Determinism Audit",
        "",
        payload["purpose"],
        "",
        "## Scope",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["scope"].items()]),
        "",
        "## Replay Results",
        "",
        markdown_table(["Policy", "Seed", "Tasks", "Stable Hash Match", "Score Match", "Solved Match", "First Hash", "Second Hash"], rows),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
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
        lines.append("All included deterministic baselines reproduced stable outcomes from fixed seeds. Wall-clock latency fields were excluded from stable-result hashes.")
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
    parser = argparse.ArgumentParser(description="Generate deterministic replay audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
