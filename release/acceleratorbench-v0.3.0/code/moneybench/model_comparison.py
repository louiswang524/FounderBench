from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import ci_rows, family_rows, markdown_table, policy_rows
from .paired_statistics import comparison_rows
from .paper_tables import OUTPUTS, PROVIDER_RUNS, ROOT, load_runs, provider_status


VERSION = "0.3.0"


def build_report(raw_path: Path = OUTPUTS / "acceleratorbench-baseline-raw-v0.3.json") -> dict[str, Any]:
    deterministic_runs = load_runs(raw_path)
    provider_rows = [provider_status(spec) for spec in PROVIDER_RUNS]
    valid_provider_runs: list[dict[str, Any]] = []
    for row in provider_rows:
        if row["status"] == "valid":
            valid_provider_runs.extend(load_runs(ROOT / row["evidence_path"]))
    all_valid_runs = deterministic_runs + valid_provider_runs
    valid_provider_policies = {run["policy"] for run in valid_provider_runs}
    paired_rows = comparison_rows(all_valid_runs) if len(all_valid_runs) >= 2 else []
    provider_paired_rows = [
        row
        for row in paired_rows
        if row["top_policy"] in valid_provider_policies or row["baseline_policy"] in valid_provider_policies
    ]
    valid_hosted_policies = {
        row["policy"]
        for row in provider_rows
        if row["status"] == "valid" and row["family"] == "hosted_llm"
    }
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Unified model-comparison report that includes deterministic baselines and automatically incorporates hosted/local provider runs only after submission validation passes.",
        "source_files": {
            "deterministic_raw": str(raw_path.relative_to(ROOT)),
            "provider_candidates": [row["path"] for row in provider_rows],
        },
        "summary": {
            "deterministic_runs": len(deterministic_runs),
            "valid_provider_runs": len(valid_provider_runs),
            "valid_provider_policies": len(valid_provider_policies),
            "valid_repeated_provider_bundles": sum(1 for row in provider_rows if row.get("evidence_kind") == "repeat_bundle"),
            "provider_candidates": len(provider_rows),
            "provider_missing_or_invalid": sum(1 for row in provider_rows if row["status"] != "valid"),
            "all_valid_runs": len(all_valid_runs),
            "paired_comparisons": len(paired_rows),
            "provider_paired_comparisons": len(provider_paired_rows),
            "hosted_llm_claims_ready": len(valid_hosted_policies) >= 3,
            "open_source_claim_ready": any(row["policy"] == "llm" and row["status"] == "valid" for row in provider_rows),
        },
        "leaderboard_rows": policy_rows(all_valid_runs),
        "confidence_interval_rows": ci_rows(all_valid_runs),
        "family_rows": family_rows(all_valid_runs),
        "paired_comparisons": paired_rows,
        "provider_paired_comparisons": provider_paired_rows,
        "provider_status": provider_rows,
        "claim_rules": [
            "Provider rows are included only after raw run validation passes.",
            "Hosted LLM comparison claims require at least three valid hosted provider baselines.",
            "Open-source comparison claims require at least one valid local/OpenAI-compatible run.",
            "Missing or invalid provider runs are reported in the ledger and excluded from leaderboard claims.",
        ],
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["deterministic_runs"] < 4:
        problems.append("Expected at least four deterministic baseline runs.")
    if payload["summary"]["all_valid_runs"] < payload["summary"]["deterministic_runs"]:
        problems.append("All valid runs cannot be fewer than deterministic runs.")
    if payload["summary"]["valid_provider_runs"] == 0 and payload["summary"]["hosted_llm_claims_ready"]:
        problems.append("Hosted LLM claims cannot be ready without valid provider runs.")
    if len(payload["provider_status"]) != len(PROVIDER_RUNS):
        problems.append("Provider status ledger does not cover all configured provider candidates.")
    for row in payload["paired_comparisons"]:
        if row["tasks"] != 50:
            problems.append(f"{row['comparison']} compares {row['tasks']} tasks, expected 50.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    provider_rows = [
        [
            row["id"],
            row["policy"],
            row["family"],
            row["status"],
            row["runs"],
            row.get("evidence_kind", ""),
            row.get("average_task_score", ""),
            row.get("solve_rate", ""),
            "; ".join(row["problems"][:2]),
        ]
        for row in payload["provider_status"]
    ]
    paired_rows = [
        [
            row["comparison"],
            row["tasks"],
            row["mean_score_gap"],
            f"[{row['score_gap_bootstrap_ci'][0]}, {row['score_gap_bootstrap_ci'][1]}]",
            row["paired_permutation_p"],
            row["cohen_dz"],
            f"{row['task_wins']}/{row['task_losses']}/{row['task_ties']}",
        ]
        for row in payload["paired_comparisons"]
    ]
    provider_paired_rows = [
        [
            row["comparison"],
            row["tasks"],
            row["mean_score_gap"],
            f"[{row['score_gap_bootstrap_ci'][0]}, {row['score_gap_bootstrap_ci'][1]}]",
            row["paired_permutation_p"],
            row["cohen_dz"],
        ]
        for row in payload["provider_paired_comparisons"]
    ]
    lines = [
        "# FounderBench v0.3 Model Comparison Report",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Leaderboard",
        "",
        markdown_table(["Policy", "Tasks", "Solved", "Solve Rate", "Avg Score", "Public Dev", "Public Test", "Over-Budget", "Provider Errors"], payload["leaderboard_rows"]),
        "",
        "## Confidence Intervals",
        "",
        markdown_table(["Policy", "Avg Score", "Score 95% CI", "Solve Rate", "Solve Rate 95% CI"], payload["confidence_interval_rows"]),
        "",
        "## Paired Comparisons",
        "",
        markdown_table(["Comparison", "Tasks", "Mean Gap", "Bootstrap 95% CI", "Permutation p", "Cohen dz", "Score W/L/T"], paired_rows),
        "",
        "## Provider Paired Comparisons",
        "",
    ]
    if provider_paired_rows:
        lines.append(markdown_table(["Comparison", "Tasks", "Mean Gap", "Bootstrap 95% CI", "Permutation p", "Cohen dz"], provider_paired_rows))
    else:
        lines.append("No provider paired comparisons are available yet because no hosted/local provider run currently passes validation.")
    lines.extend(
        [
            "",
            "## Family Breakdown",
            "",
            "Each cell reports `solved/5 (average score)`.",
            "",
            markdown_table(["Family", *[row[0] for row in payload["leaderboard_rows"]]], payload["family_rows"]),
            "",
            "## Provider Evidence Ledger",
            "",
            markdown_table(["ID", "Policy", "Family", "Status", "Runs", "Evidence", "Avg Score", "Solve Rate", "Problems"], provider_rows),
            "",
            "## Claim Rules",
            "",
        ]
    )
    lines.extend(f"- {rule}" for rule in payload["claim_rules"])
    lines.extend(["", "## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The report is internally consistent. Provider comparison sections remain empty until validated provider runs exist.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    problems = validate_report(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate unified model-comparison report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
