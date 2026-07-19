from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table, policy_rows
from .leaderboard import summarize


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _policy_order(rows: list[dict[str, Any]]) -> list[str]:
    return [row["policy"] for row in sorted(rows, key=lambda row: row["average_task_score"], reverse=True)]


def _as_policy_map(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {row["policy"]: row for row in rows}


def _table_policy_map(rows: list[list[Any]]) -> dict[str, list[Any]]:
    return {str(row[0]): row for row in rows}


def _select_rows(rows: list[list[Any]], policies: set[str]) -> list[list[Any]]:
    return [row for row in rows if str(row[0]) in policies]


def _compare_dict_rows(expected: dict[str, Any], actual: dict[str, Any], keys: list[str]) -> list[str]:
    problems: list[str] = []
    for key in keys:
        if expected.get(key) != actual.get(key):
            problems.append(f"{key}: expected {expected.get(key)!r}, found {actual.get(key)!r}")
    return problems


def build_audit(
    raw_path: Path = OUTPUTS / "founderbench-baseline-raw.json",
    leaderboard_path: Path = OUTPUTS / "founderbench-baseline-leaderboard.json",
    paper_tables_path: Path = OUTPUTS / "founderbench-paper-tables.json",
    model_comparison_path: Path = OUTPUTS / "founderbench-model-comparison.json",
) -> dict[str, Any]:
    raw = load_json(raw_path)
    leaderboard = load_json(leaderboard_path)
    paper_tables = load_json(paper_tables_path)
    model_comparison = load_json(model_comparison_path)

    recomputed_rows = sorted([summarize(run) for run in raw], key=lambda row: row["average_task_score"], reverse=True)
    expected_table_rows = policy_rows(raw)
    deterministic_policies = {str(row[0]) for row in expected_table_rows}
    recomputed_by_policy = _as_policy_map(recomputed_rows)
    leaderboard_by_policy = _as_policy_map(leaderboard.get("rows", []))
    paper_table_by_policy = _table_policy_map(paper_tables.get("all_valid_policy_rows", []))
    model_table_by_policy = _table_policy_map(model_comparison.get("leaderboard_rows", []))

    key_fields = [
        "tasks",
        "solved",
        "solve_rate",
        "average_task_score",
        "public_dev_score",
        "public_test_score",
        "invalid_actions",
        "over_budget_decisions",
        "provider_errors",
    ]
    policy_checks = []
    for expected in recomputed_rows:
        policy = expected["policy"]
        actual = leaderboard_by_policy.get(policy)
        problems = [f"missing leaderboard row for {policy}"] if actual is None else _compare_dict_rows(expected, actual, key_fields)
        expected_table = _table_policy_map(expected_table_rows).get(policy)
        paper_row = paper_table_by_policy.get(policy)
        model_row = model_table_by_policy.get(policy)
        if expected_table != paper_row:
            problems.append(f"paper table row mismatch: expected {expected_table!r}, found {paper_row!r}")
        if expected_table != model_row:
            problems.append(f"model-comparison row mismatch: expected {expected_table!r}, found {model_row!r}")
        task_ids = [result["task_id"] for result in next(run for run in raw if run["policy"] == policy)["results"]]
        if len(task_ids) != len(set(task_ids)):
            problems.append("duplicate task ids in raw results")
        if len(task_ids) != expected["tasks"]:
            problems.append(f"raw task count mismatch: expected {expected['tasks']}, found {len(task_ids)}")
        policy_checks.append(
            {
                "policy": policy,
                "status": "pass" if not problems else "fail",
                "raw_tasks": len(task_ids),
                "average_task_score": expected["average_task_score"],
                "leaderboard_score": actual.get("average_task_score") if actual else None,
                "paper_table_score": paper_row[4] if paper_row else None,
                "model_comparison_score": model_row[4] if model_row else None,
                "problems": problems,
            }
        )

    ordering_checks = {
        "leaderboard_order_matches_raw": _policy_order(recomputed_rows) == _policy_order(leaderboard.get("rows", [])),
        "paper_table_order_matches_raw": [row[0] for row in expected_table_rows]
        == [row[0] for row in _select_rows(paper_tables.get("all_valid_policy_rows", []), deterministic_policies)],
        "model_comparison_order_matches_raw": [row[0] for row in expected_table_rows]
        == [row[0] for row in _select_rows(model_comparison.get("leaderboard_rows", []), deterministic_policies)],
    }
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Raw-to-report integrity audit for deterministic baseline results.",
        "source_files": {
            "raw": str(raw_path.relative_to(ROOT)),
            "leaderboard": str(leaderboard_path.relative_to(ROOT)),
            "paper_tables": str(paper_tables_path.relative_to(ROOT)),
            "model_comparison": str(model_comparison_path.relative_to(ROOT)),
        },
        "summary": {
            "raw_runs": len(raw),
            "policies_checked": len(policy_checks),
            "policies_passed": sum(1 for row in policy_checks if row["status"] == "pass"),
            "policies_failed": sum(1 for row in policy_checks if row["status"] == "fail"),
            "all_ordering_checks_passed": all(ordering_checks.values()),
            "all_integrity_checks_passed": all(row["status"] == "pass" for row in policy_checks) and all(ordering_checks.values()),
        },
        "ordering_checks": ordering_checks,
        "policy_checks": policy_checks,
        "claim_guardrail": "Deterministic baseline tables are paper-eligible only while this audit passes; hosted/local provider rows require separate submission validation before inclusion.",
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("summary", {})
    if summary.get("raw_runs") != 4:
        problems.append("Expected four deterministic raw baseline runs.")
    if summary.get("policies_checked") != 4:
        problems.append("Expected four policy integrity checks.")
    if summary.get("policies_failed") != 0:
        problems.append("One or more policy rows failed raw-to-report integrity checks.")
    if summary.get("all_ordering_checks_passed") is not True:
        problems.append("Ordering checks must pass.")
    if summary.get("all_integrity_checks_passed") is not True:
        problems.append("Overall integrity checks must pass.")
    for row in payload.get("policy_checks", []):
        if row["raw_tasks"] != 50:
            problems.append(f"{row['policy']} raw task count must be 50.")
        if row["status"] != "pass":
            problems.append(f"{row['policy']} integrity status is {row['status']}.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["raw-to-report", "leaderboard", "paper_tables", "model_comparison", "submission validation"]:
        if required not in text:
            problems.append(f"Integrity audit must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    policy_rows_md = [
        [
            row["policy"],
            row["status"],
            row["raw_tasks"],
            row["average_task_score"],
            row["leaderboard_score"],
            row["paper_table_score"],
            row["model_comparison_score"],
            "; ".join(row["problems"]),
        ]
        for row in payload["policy_checks"]
    ]
    lines = [
        "# FounderBench Result Integrity Audit",
        "",
        payload["purpose"],
        "",
        "## Source Files",
        "",
        markdown_table(["Role", "Path"], [[key, value] for key, value in payload["source_files"].items()]),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Ordering Checks",
        "",
        markdown_table(["Check", "Passed"], [[key, value] for key, value in payload["ordering_checks"].items()]),
        "",
        "## Policy Checks",
        "",
        markdown_table(["Policy", "Status", "Raw Tasks", "Raw Avg", "Leaderboard Avg", "Paper Table Avg", "Model Comparison Avg", "Problems"], policy_rows_md),
        "",
        "## Claim Guardrail",
        "",
        payload["claim_guardrail"],
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
        lines.append("Raw deterministic baseline results exactly reproduce leaderboard, paper-table, and model-comparison rows.")
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
    parser = argparse.ArgumentParser(description="Generate raw-to-report result integrity audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
