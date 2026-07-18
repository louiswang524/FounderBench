from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from statistics import mean
from typing import Any

from .analysis import family_name, markdown_table, split_name
from .score_rubric import PASS_THRESHOLD, build_rubric


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


def load_runs(path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_audit(raw_path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> dict[str, Any]:
    runs = load_runs(raw_path)
    rubric = build_rubric()
    rubric_by_family = {row["family"]: row for row in rubric["families"]}
    rows: list[dict[str, Any]] = []
    problems: list[str] = []
    family_policy_counts: dict[str, Counter[str]] = defaultdict(Counter)
    split_policy_counts: dict[str, Counter[str]] = defaultdict(Counter)
    metric_key_counts: Counter[str] = Counter()
    for run in runs:
        policy = run["policy"]
        seen_task_ids: set[str] = set()
        for result in run["results"]:
            task_id = result["task_id"]
            family = family_name(task_id)
            split = split_name(task_id)
            score_obj = result["score"]
            score = float(score_obj["score"])
            passed = bool(score_obj["passed"])
            metrics = score_obj.get("metrics", {})
            expected_passed = score >= PASS_THRESHOLD
            row_problems: list[str] = []
            if task_id in seen_task_ids:
                row_problems.append("duplicate task id within policy run")
            seen_task_ids.add(task_id)
            if not 0 <= score <= 100:
                row_problems.append("score outside [0, 100]")
            if passed != expected_passed:
                row_problems.append(f"passed flag mismatch with threshold {PASS_THRESHOLD}")
            if not isinstance(metrics, dict) or not metrics:
                row_problems.append("missing score metrics payload")
            else:
                for key, value in metrics.items():
                    metric_key_counts[key] += 1
                    if isinstance(value, float) and not (value == value and value not in {float("inf"), float("-inf")}):
                        row_problems.append(f"metric {key} is not finite")
                    if not isinstance(value, (int, float, bool, str)):
                        row_problems.append(f"metric {key} has unsupported type {type(value).__name__}")
            family_policy_counts[family][policy] += 1
            split_policy_counts[split][policy] += 1
            rows.append(
                {
                    "policy": policy,
                    "task_id": task_id,
                    "family": family,
                    "split": split,
                    "score": score,
                    "passed": passed,
                    "expected_passed": expected_passed,
                    "metrics": sorted(metrics),
                    "problems": row_problems,
                }
            )
            problems.extend(f"{policy}/{task_id}: {problem}" for problem in row_problems)
    family_rows = []
    for family, rubric_row in rubric_by_family.items():
        counts = family_policy_counts[family]
        family_rows.append(
            {
                "family": family,
                "positive_weight_total": rubric_row["positive_weight_total"],
                "policy_task_counts": dict(sorted(counts.items())),
                "all_policies_have_5_tasks": all(count == 5 for count in counts.values()) and len(counts) == len(runs),
                "primary_metrics": rubric_row["primary_metrics"],
            }
        )
    split_rows = []
    for split, counts in sorted(split_policy_counts.items()):
        expected = 30 if split == "public_dev" else 20
        split_rows.append(
            {
                "split": split,
                "expected_tasks_per_policy": expected,
                "policy_task_counts": dict(sorted(counts.items())),
                "all_policies_match_expected": all(count == expected for count in counts.values()) and len(counts) == len(runs),
            }
        )
    failed_rows = [row for row in rows if row["problems"]]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Scoring consistency audit over all included deterministic raw task results.",
        "source_file": str(raw_path.relative_to(ROOT)),
        "score_contract": {
            "score_min": 0,
            "score_max": 100,
            "pass_threshold": PASS_THRESHOLD,
            "pass_rule": "passed is true iff score >= pass_threshold",
            "metric_payload_rule": "Each task score must include non-empty numeric, bool, or string categorical metrics.",
        },
        "summary": {
            "runs": len(runs),
            "task_results_checked": len(rows),
            "expected_task_results": len(runs) * 50,
            "score_rows_with_problems": len(failed_rows),
            "families_checked": len(family_rows),
            "splits_checked": len(split_rows),
            "all_family_counts_valid": all(row["all_policies_have_5_tasks"] for row in family_rows),
            "all_split_counts_valid": all(row["all_policies_match_expected"] for row in split_rows),
            "mean_score": round(mean(row["score"] for row in rows), 2),
            "passes": sum(1 for row in rows if row["passed"]),
        },
        "family_rows": family_rows,
        "split_rows": split_rows,
        "metric_key_counts": dict(sorted(metric_key_counts.items())),
        "failed_rows": failed_rows,
        "problems": problems,
        "claim_guardrail": "This audit checks the consistency of generated score objects and rubric coverage; it does not validate that rubric weights are the correct model of real startup success.",
    }


def validate_audit(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("summary", {})
    if summary.get("task_results_checked") != summary.get("expected_task_results"):
        problems.append("Task result count does not match runs * 50.")
    if summary.get("task_results_checked") != 200:
        problems.append("Expected 200 deterministic task result score objects.")
    if summary.get("score_rows_with_problems") != 0:
        problems.append("One or more score rows failed consistency checks.")
    if summary.get("families_checked") != 10:
        problems.append("Expected 10 family coverage checks.")
    if summary.get("splits_checked") != 2:
        problems.append("Expected 2 split coverage checks.")
    if summary.get("all_family_counts_valid") is not True:
        problems.append("Each policy should have 5 tasks per family.")
    if summary.get("all_split_counts_valid") is not True:
        problems.append("Each policy should match expected public_dev/public_test counts.")
    contract = payload.get("score_contract", {})
    if contract.get("pass_threshold") != PASS_THRESHOLD:
        problems.append(f"Pass threshold should be {PASS_THRESHOLD}.")
    if payload.get("problems"):
        problems.append("Problem ledger must be empty for a passing audit.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["passed is true iff", "metric_payload_rule", "real startup success"]:
        if required not in text:
            problems.append(f"Scoring consistency audit must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    family_rows = [
        [
            row["family"],
            row["positive_weight_total"],
            row["all_policies_have_5_tasks"],
            row["policy_task_counts"],
            ", ".join(row["primary_metrics"]),
        ]
        for row in payload["family_rows"]
    ]
    split_rows = [
        [
            row["split"],
            row["expected_tasks_per_policy"],
            row["all_policies_match_expected"],
            row["policy_task_counts"],
        ]
        for row in payload["split_rows"]
    ]
    metric_rows = [[key, value] for key, value in payload["metric_key_counts"].items()]
    lines = [
        "# FounderBench Scoring Consistency Audit",
        "",
        payload["purpose"],
        "",
        "## Score Contract",
        "",
        markdown_table(["Item", "Value"], [[key, value] for key, value in payload["score_contract"].items()]),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Family Coverage",
        "",
        markdown_table(["Family", "Positive Weight Total", "Valid Counts", "Policy Task Counts", "Primary Metrics"], family_rows),
        "",
        "## Split Coverage",
        "",
        markdown_table(["Split", "Expected Tasks Per Policy", "Valid Counts", "Policy Task Counts"], split_rows),
        "",
        "## Metric Key Coverage",
        "",
        markdown_table(["Metric Key", "Occurrences"], metric_rows),
        "",
        "## Failed Rows",
        "",
    ]
    if payload["failed_rows"]:
        lines.append(markdown_table(["Policy", "Task", "Problems"], [[row["policy"], row["task_id"], "; ".join(row["problems"])] for row in payload["failed_rows"]]))
    else:
        lines.append("No failed score rows.")
    lines.extend(["", "## Claim Guardrail", "", payload["claim_guardrail"], "", "## Validation", ""])
    problems = validate_audit(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("All included deterministic score objects satisfy bounds, threshold, metric-payload, family, and split consistency checks.")
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
    parser = argparse.ArgumentParser(description="Generate scoring consistency audit.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_audit(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
