from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .leaderboard import summarize
from .submission import EXPECTED_VERSION, load_json, validate_run, write_submission_report


def _extract_runs(payload: Any, source: str) -> list[dict[str, Any]]:
    if isinstance(payload, dict) and "results" in payload:
        return [payload]
    if isinstance(payload, dict) and isinstance(payload.get("runs"), list):
        return payload["runs"]
    if isinstance(payload, list):
        return payload
    raise ValueError(f"{source}: expected a run object, a run list, or an object with a runs array.")


def bundle_payload(runs: list[dict[str, Any]], input_files: list[str] | None = None) -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": EXPECTED_VERSION,
        "created_by": "moneybench.submission_bundle",
        "input_files": input_files or [],
        "runs": runs,
    }


def bundle_runs(input_paths: list[Path]) -> dict[str, Any]:
    runs: list[dict[str, Any]] = []
    for path in input_paths:
        runs.extend(_extract_runs(load_json(path), str(path)))
    return bundle_payload(runs, [str(path) for path in input_paths])


def validate_bundle(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("Bundle benchmark must be FounderBench.")
    if payload.get("version") != EXPECTED_VERSION:
        problems.append(f"Bundle version must be {EXPECTED_VERSION}.")
    runs = payload.get("runs")
    if not isinstance(runs, list) or not runs:
        problems.append("Bundle must contain a non-empty runs array.")
        return problems

    seen: set[tuple[str, Any]] = set()
    for index, run in enumerate(runs):
        if not isinstance(run, dict):
            problems.append(f"runs[{index}] must be an object.")
            continue
        problems.extend(validate_run(run))
        key = (str(run.get("policy", "<unknown>")), run.get("run_seed", "missing"))
        if key in seen:
            problems.append(f"Duplicate run identity policy={key[0]} run_seed={key[1]}.")
        seen.add(key)
    return problems


def build_protocol() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": EXPECTED_VERSION,
        "purpose": "Protocol and CLI helper for combining repeated model/provider runs into one validated submission bundle.",
        "summary": "Combines single-run JSON files, existing run arrays, or existing {runs: [...]} payloads into one {runs: [...]} bundle and validates every run before comparison.",
        "accepted_inputs": [
            "single run object with a results array",
            "JSON list of run objects",
            "JSON object with top-level runs array",
        ],
        "validation_checks": [
            "each run passes moneybench.submission.validate_run",
            "bundle has benchmark=FounderBench and version=0.3.0",
            "bundle has at least one run",
            "no duplicate policy/run_seed pairs",
        ],
        "output_shape": {
            "benchmark": "FounderBench",
            "version": EXPECTED_VERSION,
            "created_by": "moneybench.submission_bundle",
            "input_files": ["path/to/run-seed0.json"],
            "runs": ["validated run objects"],
        },
        "example_commands": [
            "python -m moneybench.submission_bundle --input outputs/acceleratorbench-deepseek-v0.3-seed0.json --input outputs/acceleratorbench-deepseek-v0.3-seed1.json --input outputs/acceleratorbench-deepseek-v0.3-seed2.json --output outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md",
            "python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3-repeats.json --report outputs/acceleratorbench-deepseek-v0.3-repeats-submission-report.md",
        ],
        "claim_rule": "Repeated-run claims should cite the bundled submission report. Single-run claims must be labeled preliminary unless the statistical protocol permits otherwise.",
    }


def validate_protocol(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != EXPECTED_VERSION:
        problems.append(f"Expected protocol version {EXPECTED_VERSION}.")
    if "submission_bundle" not in " ".join(payload.get("example_commands", [])):
        problems.append("Protocol must document the submission_bundle command.")
    if "no duplicate policy/run_seed pairs" not in payload.get("validation_checks", []):
        problems.append("Protocol must document duplicate repeat detection.")
    return problems


def write_protocol(json_output: Path, markdown_output: Path) -> None:
    payload = build_protocol()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = [
        "# FounderBench Submission Bundle Protocol",
        "",
        payload["summary"],
        "",
        "## Accepted Inputs",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["accepted_inputs"])
    lines.extend(
        [
            "",
            "## Validation Checks",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["validation_checks"])
    lines.extend(
        [
            "",
            "## Output Shape",
            "",
            "```json",
            json.dumps(payload["output_shape"], indent=2),
            "```",
            "",
            "## Commands",
            "",
        ]
    )
    lines.extend(f"```powershell\n{command}\n```" for command in payload["example_commands"])
    lines.extend(["", "## Claim Rule", "", payload["claim_rule"], ""])
    problems = validate_protocol(payload)
    lines.extend(["## Validation", "", "Status: PASS" if not problems else "Status: FAIL"])
    lines.extend(f"- {problem}" for problem in problems)
    markdown_output.parent.mkdir(parents=True, exist_ok=True)
    markdown_output.write_text("\n".join(lines), encoding="utf-8")


def _bundle_rows(runs: list[dict[str, Any]]) -> list[list[Any]]:
    rows = []
    for run in runs:
        row = summarize(run)
        rows.append(
            [
                row["policy"],
                run.get("run_seed", ""),
                row["tasks"],
                row["solved"],
                f"{row['solve_rate']:.2f}",
                f"{row['average_task_score']:.2f}",
                row["provider_errors"],
                row["invalid_actions"],
            ]
        )
    return rows


def write_bundle(input_paths: list[Path], output: Path, report_output: Path | None = None) -> list[str]:
    payload = bundle_runs(input_paths)
    problems = validate_bundle(payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    if report_output is not None:
        write_submission_report(output, report_output)
        lines = report_output.read_text(encoding="utf-8").splitlines()
        lines.extend(
            [
                "",
                "## Bundle Inputs",
                "",
                markdown_table(["Input File"], [[path] for path in payload["input_files"]]),
                "",
                "## Run Identities",
                "",
                markdown_table(
                    ["Policy", "Run Seed", "Tasks", "Solved", "Solve Rate", "Avg Score", "Provider Errors", "Invalid Actions"],
                    _bundle_rows(payload["runs"]),
                ),
                "",
            ]
        )
        report_output.write_text("\n".join(lines), encoding="utf-8")
    return problems


def main() -> None:
    parser = argparse.ArgumentParser(description="Combine validated FounderBench runs into one repeated-run submission bundle.")
    parser.add_argument("--input", action="append", required=True, help="Input run JSON. May be passed multiple times.")
    parser.add_argument("--output", required=True, help="Combined bundle JSON output.")
    parser.add_argument("--report", help="Optional Markdown validation report output.")
    args = parser.parse_args()

    problems = write_bundle([Path(path) for path in args.input], Path(args.output), Path(args.report) if args.report else None)
    if problems:
        for problem in problems:
            print(f"ERROR: {problem}")
        raise SystemExit(1)
    print("FounderBench submission bundle validation passed.")


if __name__ == "__main__":
    main()
