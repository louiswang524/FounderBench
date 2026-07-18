from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


def build_protocol() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Pre-specified statistical comparison protocol for deterministic and hosted/local LLM submissions.",
        "primary_endpoint": {
            "metric": "average_task_score",
            "unit": "fixed task episode",
            "definition": "Mean bounded 0-100 task score over the 50-task suite.",
            "rationale": "Normalizes heterogeneous startup situations while preserving task-specific business objectives.",
        },
        "secondary_endpoints": [
            {
                "metric": "solve_rate",
                "definition": "Fraction of tasks with task_score >= 70.",
                "use": "Interpretable success-rate companion to average score.",
            },
            {
                "metric": "public_dev_vs_public_test",
                "definition": "Report average score and solve rate separately for FND-001..FND-030 and FND-031..FND-050.",
                "use": "Detect split imbalance and possible overfitting to development tasks.",
            },
            {
                "metric": "family_breakdown",
                "definition": "Report solved/5 and average score for each of the 10 task families.",
                "use": "Identify capability profile rather than only aggregate score.",
            },
            {
                "metric": "diagnostics",
                "definition": "Provider errors, invalid actions, over-budget decisions, latency, token use, and estimated cost.",
                "use": "Distinguish business-decision failure from interface or API failure.",
            },
        ],
        "single_run_comparison": {
            "paired_unit": "task id",
            "score_gap": "model_a_score_i - model_b_score_i",
            "interval": "Nonparametric bootstrap 95% CI over paired task gaps.",
            "hypothesis_test": "Two-sided random sign-flip permutation test over paired task gaps.",
            "effect_size": "Cohen dz over paired task gaps.",
            "win_loss_tie": "Count tasks where model_a score is greater than, less than, or equal to model_b.",
        },
        "repeated_sampling_comparison": {
            "when_required": "Required for stochastic decoding studies, self-consistency ablations, reflection/multi-agent variants, or when reporting sampling variance.",
            "minimum_repeats_recommended": 3,
            "preferred_repeats": 5,
            "aggregation": "Report per-run average score and solve rate, then bootstrap across submitted runs for repeated-sampling intervals.",
            "paired_repeated_option": "When multiple models use identical repeat indices, compare matched repeat means with paired intervals.",
        },
        "multiple_comparisons": {
            "default_family": "All pairwise model comparisons reported in the main leaderboard.",
            "adjustment": "Holm-Bonferroni adjustment over primary endpoint p-values.",
            "reporting": "Report both raw and adjusted p-values; do not hide non-significant comparisons.",
        },
        "required_reporting_fields": [
            "model/provider snapshot",
            "prompt_version",
            "policy/agent method",
            "temperature and decoding settings",
            "task count and missing task ids if any",
            "average_task_score and solve_rate",
            "public_dev and public_test summaries",
            "family breakdown",
            "diagnostics and provider_error_categories",
            "token/cost assumptions",
            "redacted audit traces for representative success/failure cases",
        ],
        "claim_rules": [
            "Do not claim one model is better unless the comparison covers all 50 tasks or the claim is explicitly scoped.",
            "Do not compare raw money, final cash, or revenue as primary outcomes across tasks; use them as diagnostics.",
            "Treat provider errors, invalid JSON, and invalid actions as benchmark outcomes, not discarded trials.",
            "For hidden-holdout claims, report only evaluator-approved aggregate fields.",
        ],
    }


def validate_protocol(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["primary_endpoint"]["metric"] != "average_task_score":
        problems.append("Primary endpoint must be average_task_score.")
    if payload["single_run_comparison"]["paired_unit"] != "task id":
        problems.append("Single-run comparisons must be paired by task id.")
    if payload["multiple_comparisons"]["adjustment"] != "Holm-Bonferroni adjustment over primary endpoint p-values.":
        problems.append("Multiple-comparison adjustment must be pre-specified.")
    if payload["repeated_sampling_comparison"]["minimum_repeats_recommended"] < 3:
        problems.append("Repeated-sampling recommendation is too small.")
    required = {"prompt_version", "average_task_score and solve_rate", "diagnostics and provider_error_categories"}
    if not required <= set(payload["required_reporting_fields"]):
        problems.append(f"Missing required reporting fields: {sorted(required - set(payload['required_reporting_fields']))}")
    if len(payload["claim_rules"]) < 4:
        problems.append("Expected at least four claim guardrails.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    secondary_rows = [[row["metric"], row["definition"], row["use"]] for row in payload["secondary_endpoints"]]
    single_rows = [[key, value] for key, value in payload["single_run_comparison"].items()]
    repeated_rows = [[key, value] for key, value in payload["repeated_sampling_comparison"].items()]
    multiple_rows = [[key, value] for key, value in payload["multiple_comparisons"].items()]
    lines = [
        "# FounderBench v0.3 Statistical Comparison Protocol",
        "",
        payload["purpose"],
        "",
        "## Primary Endpoint",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["primary_endpoint"].items()]),
        "",
        "## Secondary Endpoints",
        "",
        markdown_table(["Metric", "Definition", "Use"], secondary_rows),
        "",
        "## Single-Run Comparisons",
        "",
        markdown_table(["Item", "Rule"], single_rows),
        "",
        "## Repeated-Sampling Comparisons",
        "",
        markdown_table(["Item", "Rule"], repeated_rows),
        "",
        "## Multiple Comparisons",
        "",
        markdown_table(["Item", "Rule"], multiple_rows),
        "",
        "## Required Reporting Fields",
        "",
    ]
    lines.extend(f"- {field}" for field in payload["required_reporting_fields"])
    lines.extend(["", "## Claim Rules", ""])
    lines.extend(f"- {rule}" for rule in payload["claim_rules"])
    lines.extend(["", "## Validation", ""])
    problems = validate_protocol(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The protocol fixes the primary endpoint, paired unit, uncertainty estimates, repeated-run reporting, and claim guardrails before hosted/local model comparisons are added.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_protocol(json_output: Path, markdown_output: Path) -> None:
    payload = build_protocol()
    problems = validate_protocol(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate statistical comparison protocol.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_protocol(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
