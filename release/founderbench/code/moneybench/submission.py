from __future__ import annotations

import argparse
import json
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import bootstrap_mean_ci, markdown_table, split_name
from .leaderboard import summarize
from .tasks import TASKS


EXPECTED_VERSION = "0.3.0"
EXPECTED_TASK_IDS = {task.task_id for task in TASKS}
REQUIRED_DIAGNOSTICS = {
    "invalid_actions",
    "over_budget_decisions",
    "provider_errors",
    "provider_error_categories",
    "total_actions",
    "decision_latency_s",
    "simulated_api_cost",
    "provider_prompt_tokens",
    "provider_completion_tokens",
    "provider_total_tokens",
    "estimated_provider_cost_usd",
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _as_runs(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "results" in payload:
        return [payload]
    if isinstance(payload, dict) and "runs" in payload and isinstance(payload["runs"], list):
        return payload["runs"]
    raise ValueError("Submission must be a run object, a list of run objects, or an object with a runs array.")


def validate_run(run: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    policy = run.get("policy", "<unknown>")

    if run.get("benchmark_version", EXPECTED_VERSION) != EXPECTED_VERSION:
        problems.append(f"{policy}: benchmark_version must be {EXPECTED_VERSION}.")
    if run.get("tasks") != 50:
        problems.append(f"{policy}: expected tasks=50, found {run.get('tasks')}.")
    if not isinstance(run.get("results"), list):
        problems.append(f"{policy}: missing results array.")
        return problems

    result_ids = [item.get("task_id") for item in run["results"]]
    if len(result_ids) != 50:
        problems.append(f"{policy}: expected 50 task results, found {len(result_ids)}.")
    if set(result_ids) != EXPECTED_TASK_IDS:
        missing = sorted(EXPECTED_TASK_IDS - set(result_ids))
        extra = sorted(set(result_ids) - EXPECTED_TASK_IDS)
        if missing:
            problems.append(f"{policy}: missing task ids {missing[:8]}{'...' if len(missing) > 8 else ''}.")
        if extra:
            problems.append(f"{policy}: unexpected task ids {extra[:8]}{'...' if len(extra) > 8 else ''}.")

    for result in run["results"]:
        task_id = result.get("task_id", "<missing>")
        score = result.get("score", {})
        diagnostics = result.get("diagnostics", {})
        if not isinstance(score.get("score"), (int, float)):
            problems.append(f"{policy}/{task_id}: score.score must be numeric.")
        if not isinstance(score.get("passed"), bool):
            problems.append(f"{policy}/{task_id}: score.passed must be boolean.")
        missing_diagnostics = REQUIRED_DIAGNOSTICS - set(diagnostics)
        if missing_diagnostics:
            problems.append(f"{policy}/{task_id}: missing diagnostics {sorted(missing_diagnostics)}.")
        if not isinstance(diagnostics.get("provider_error_categories", {}), dict):
            problems.append(f"{policy}/{task_id}: provider_error_categories must be an object.")

    diagnostics = run.get("diagnostics", {})
    missing_run_diagnostics = REQUIRED_DIAGNOSTICS - set(diagnostics)
    if missing_run_diagnostics:
        problems.append(f"{policy}: missing aggregate diagnostics {sorted(missing_run_diagnostics)}.")
    provider_error_sum = sum(int(v) for v in diagnostics.get("provider_error_categories", {}).values())
    provider_errors = int(diagnostics.get("provider_errors", 0) or 0)
    if provider_error_sum and provider_error_sum != provider_errors:
        problems.append(f"{policy}: provider_error_categories sum {provider_error_sum} != provider_errors {provider_errors}.")

    splits = run.get("splits", {})
    for required_split in ("public_dev", "public_test"):
        if required_split not in splits:
            problems.append(f"{policy}: missing split summary for {required_split}.")

    return problems


def validate_submission(path: Path) -> list[str]:
    runs = _as_runs(load_json(path))
    problems: list[str] = []
    for run in runs:
        problems.extend(validate_run(run))
    return problems


def _score_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for run in sorted(runs, key=lambda item: item.get("average_task_score", 0), reverse=True):
        row = summarize(run)
        rows.append(
            [
                row["policy"],
                row["tasks"],
                row["solved"],
                f"{row['solve_rate']:.2f}",
                f"{row['average_task_score']:.2f}",
                f"{row['public_dev_score']:.2f}",
                f"{row['public_test_score']:.2f}",
                row["provider_errors"],
                row["invalid_actions"],
                row["over_budget_decisions"],
                row["provider_total_tokens"],
                f"{row['estimated_provider_cost_usd']:.4f}",
            ]
        )
    return rows


def _repeat_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    grouped: dict[str, list[dict[str, Any]]] = {}
    for run in runs:
        grouped.setdefault(run.get("policy", "<unknown>"), []).append(run)
    for policy, policy_runs in sorted(grouped.items()):
        if len(policy_runs) < 2:
            rows.append([policy, len(policy_runs), "n/a", "n/a", "n/a"])
            continue
        scores = [float(run["average_task_score"]) for run in policy_runs]
        solved = [float(run["solve_rate"]) for run in policy_runs]
        low, high = bootstrap_mean_ci(scores, iterations=2000, seed=20260715)
        solve_low, solve_high = bootstrap_mean_ci(solved, iterations=2000, seed=20260716)
        rows.append([policy, len(policy_runs), f"{mean(scores):.2f}", f"[{low:.2f}, {high:.2f}]", f"[{solve_low:.2f}, {solve_high:.2f}]"])
    return rows


def write_submission_report(input_path: Path, output_path: Path) -> None:
    runs = _as_runs(load_json(input_path))
    problems: list[str] = []
    for run in runs:
        problems.extend(validate_run(run))

    lines = [
        "# FounderBench Model Submission Report",
        "",
        f"Input: `{input_path}`",
        f"Benchmark version: `{EXPECTED_VERSION}`",
        f"Runs checked: {len(runs)}",
        "",
        "## Validation",
        "",
    ]
    if problems:
        lines.extend(["Status: FAIL", "", "Problems:"])
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.extend(["Status: PASS", "", "The submission contains complete task coverage, split summaries, and required diagnostics."])

    lines.extend(
        [
            "",
            "## Leaderboard Summary",
            "",
            markdown_table(
                [
                    "Policy",
                    "Tasks",
                    "Solved",
                    "Solve Rate",
                    "Avg Score",
                    "Public Dev",
                    "Public Test",
                    "Provider Errors",
                    "Invalid Actions",
                    "Over-Budget",
                    "Provider Tokens",
                    "Cost USD",
                ],
                _score_rows(runs),
            ),
            "",
            "## Repeated-Run Summary",
            "",
            "When multiple runs share a policy name, intervals estimate stochastic variation across submitted runs. Single runs are marked `n/a`.",
            "",
            markdown_table(["Policy", "Runs", "Mean Avg Score", "Score 95% CI", "Solve Rate 95% CI"], _repeat_rows(runs)),
            "",
            "## Split Coverage",
            "",
        ]
    )
    split_counts = {"public_dev": 0, "public_test": 0}
    for run in runs:
        for result in run["results"]:
            split_counts[split_name(result["task_id"])] += 1
    lines.append(markdown_table(["Split", "Task Results"], [[name, count] for name, count in split_counts.items()]))
    lines.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate and summarize FounderBench model submissions.")
    parser.add_argument("--input", required=True, help="Raw run JSON, list of runs, or {runs: [...]} JSON.")
    parser.add_argument("--report", help="Optional Markdown report output.")
    args = parser.parse_args()

    input_path = Path(args.input)
    problems = validate_submission(input_path)
    if args.report:
        write_submission_report(input_path, Path(args.report))
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("FounderBench model submission validation passed.")


if __name__ == "__main__":
    main()
