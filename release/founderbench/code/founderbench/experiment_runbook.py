from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .baseline_execution_plan import MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS, build_plan as build_execution_plan
from .provider_readiness import PROVIDERS


VERSION = "0.3.0"


def _provider_rows() -> list[dict[str, Any]]:
    rows = []
    for provider in PROVIDERS:
        rows.append(
            {
                "provider": provider["provider"],
                "policy": provider["policy"],
                "priority": "required" if provider["policy"] in {"deepseek", "anthropic", "gemini", "llm"} else "recommended",
                "api_key_env": provider["api_key_env"],
                "model_env": provider["model_env"],
                "base_url_env": provider.get("base_url_env", ""),
                "default_model": provider["default_model"],
            }
        )
    return rows


def _phase_rows(plan: dict[str, Any]) -> list[dict[str, Any]]:
    required_runs = [row for row in plan["runs"] if row["priority"] == "required"]
    optional_runs = [row for row in plan["runs"] if row["priority"] == "recommended"]
    return [
        {
            "id": "preflight",
            "owner": "evaluator",
            "purpose": "Confirm provider configuration, clean output target names, and record the exact model ids.",
            "entry_condition": "Provider keys and model choices are available in environment variables; no secrets are written to files.",
            "exit_condition": "Provider readiness report is regenerated and reviewed.",
            "commands": [
                "python -m founderbench.provider_readiness --json-output ..\\..\\outputs\\founderbench-provider-readiness.json --markdown-output ..\\..\\outputs\\founderbench-provider-readiness.md"
            ],
            "outputs": [
                "outputs/founderbench-provider-readiness.json",
                "outputs/founderbench-provider-readiness.md",
            ],
        },
        {
            "id": "single_required_runs",
            "owner": "evaluator",
            "purpose": "Run each required hosted/local model once on the complete 50-task suite.",
            "entry_condition": "Preflight passes for the provider being executed.",
            "exit_condition": "Every required single-run output exists and passes submission validation.",
            "commands": [command for row in required_runs for command in [row["run_command"], row["validation_command"]]],
            "outputs": [path for row in required_runs for path in [row["output"], row["submission_report"]]],
        },
        {
            "id": "audit_traces",
            "owner": "evaluator",
            "purpose": "Collect redacted audit traces for hosted/local runs so qualitative failures can be inspected.",
            "entry_condition": "At least the corresponding single run has completed or is intentionally being repeated with audit enabled.",
            "exit_condition": "Audit outputs and their submission reports exist for required runs.",
            "commands": [command for row in required_runs for command in [row["audit_command"], row["audit_validation_command"]]],
            "outputs": [path for row in required_runs for path in [row["audit_output"], row["audit_submission_report"]]],
        },
        {
            "id": "repeat_bundles",
            "owner": "evaluator",
            "purpose": f"Run {MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS} seeds per provider before stochastic confidence claims.",
            "entry_condition": "Single-run execution is stable enough to justify repeated API spend.",
            "exit_condition": "Repeated seed files are combined into validated repeat bundles.",
            "commands": [
                command
                for row in plan["runs"]
                for command in [
                    *[
                        row["run_command"].replace(row["output"], seed_output).replace("--seed 0", f"--seed {seed}")
                        for seed, seed_output in enumerate(row["repeat_outputs"])
                    ],
                    row["repeat_bundle_command"],
                    row["repeat_validation_command"],
                ]
            ],
            "outputs": [
                path
                for row in plan["runs"]
                for path in [*row["repeat_outputs"], row["repeat_bundle_output"], row["repeat_bundle_report"]]
            ],
        },
        {
            "id": "optional_provider_runs",
            "owner": "evaluator",
            "purpose": "Run optional additional provider and open-weight baselines after the required comparison set is underway.",
            "entry_condition": "Required runs are scheduled or complete and optional provider credentials are available.",
            "exit_condition": "Optional provider outputs exist and are clearly separated from required comparison evidence.",
            "commands": [command for row in optional_runs for command in [row["run_command"], row["validation_command"]]],
            "outputs": [path for row in optional_runs for path in [row["output"], row["submission_report"]]],
        },
        {
            "id": "postprocess_and_claim_gate",
            "owner": "paper_author",
            "purpose": "Regenerate paper tables, model comparison, provider status, claim evidence, and submission gate after runs are present.",
            "entry_condition": "Required run outputs and validation reports exist.",
            "exit_condition": "Submission gate no longer reports missing required experiment evidence; claim wording is updated only where evidence supports it.",
            "commands": [
                "python -m founderbench.release regenerate",
                "python -m founderbench.release validate",
                "python -m founderbench.release bundle",
            ],
            "outputs": [
                "outputs/founderbench-model-comparison.md",
                "outputs/founderbench-paper-tables.md",
                "outputs/founderbench-provider-run-status.md",
                "outputs/founderbench-claim-evidence.md",
                "outputs/founderbench-submission-gate.md",
                "release/founderbench",
            ],
        },
    ]


def build_runbook() -> dict[str, Any]:
    plan = build_execution_plan()
    phases = _phase_rows(plan)
    required_outputs = sorted({path for row in plan["runs"] if row["priority"] == "required" for path in [row["output"], row["submission_report"]]})
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "material_passport": {
            "artifact_type": "experiment_runbook",
            "data_access_level": "no_raw_secret_values",
            "verification_status": "planned_not_executed",
            "scope": "operator instructions for producing missing current release hosted/local model evidence",
        },
        "purpose": "Runnable experiment runbook for clearing the missing hosted/local baseline evidence gate.",
        "provider_environment": _provider_rows(),
        "phases": phases,
        "required_evidence_before_llm_claims": required_outputs,
        "quality_gates": [
            "Never paste API keys into commands, run logs, JSON outputs, Markdown reports, or paper text.",
            "Each included model run must contain exactly 50 task results and pass founderbench.submission validation.",
            "Provider errors, invalid actions, over-budget decisions, bankruptcies, and timeouts remain in the denominator.",
            "Hosted/local model-comparison claims require all required provider/local runs to be valid.",
            "Stochastic confidence claims require validated repeat bundles, not only single-run outputs.",
            "Audit traces must be inspected for accidental sensitive text before release.",
        ],
        "claim_unlock_rules": [
            {
                "claim": "hosted_llm_comparison",
                "unlock_condition": "DeepSeek, Anthropic, Gemini, and local/open-source required runs validate on all 50 tasks.",
                "otherwise": "Keep wording to planned/infrastructure-ready provider comparison.",
            },
            {
                "claim": "private_holdout_leaderboard",
                "unlock_condition": "Evaluator-controlled private holdout aggregate report exists.",
                "otherwise": "Describe only the private holdout protocol, not private holdout results.",
            },
        ],
        "summary": {
            "providers": len(_provider_rows()),
            "phases": len(phases),
            "required_single_run_evidence_files": len(required_outputs),
            "minimum_repeats_for_stochastic_claims": MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS,
        },
    }


def validate_runbook(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["material_passport"]["verification_status"] != "planned_not_executed":
        problems.append("Runbook must not present planned experiments as executed.")
    if payload["summary"]["providers"] < 5:
        problems.append("Runbook should cover hosted providers plus local/open-source execution.")
    if payload["summary"]["phases"] < 5:
        problems.append("Runbook should include preflight, runs, audits, repeats, and postprocessing.")
    if payload["summary"]["required_single_run_evidence_files"] < 8:
        problems.append("Runbook should name required run outputs and submission reports.")
    phase_ids = {phase["id"] for phase in payload["phases"]}
    for required in {"preflight", "single_required_runs", "audit_traces", "repeat_bundles", "postprocess_and_claim_gate"}:
        if required not in phase_ids:
            problems.append(f"Missing runbook phase {required}.")
    if not any("API keys" in gate for gate in payload["quality_gates"]):
        problems.append("Runbook must include a secret-handling quality gate.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    provider_rows = [
        [
            row["provider"],
            row["policy"],
            row["priority"],
            row["api_key_env"],
            row["model_env"],
            row["base_url_env"],
            row["default_model"],
        ]
        for row in payload["provider_environment"]
    ]
    phase_rows = [
        [phase["id"], phase["owner"], phase["purpose"], phase["exit_condition"]]
        for phase in payload["phases"]
    ]
    lines = [
        "# FounderBench Experiment Runbook",
        "",
        "## Material Passport",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["material_passport"].items()]),
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Provider Environment",
        "",
        markdown_table(["Provider", "Policy", "Priority", "API Key Env", "Model Env", "Base URL Env", "Default Model"], provider_rows),
        "",
        "## Phase Overview",
        "",
        markdown_table(["Phase", "Owner", "Purpose", "Exit Condition"], phase_rows),
        "",
        "## Phase Commands",
        "",
    ]
    for phase in payload["phases"]:
        lines.extend(
            [
                f"### {phase['id']}",
                "",
                f"Entry condition: {phase['entry_condition']}",
                "",
                "```powershell",
                *phase["commands"],
                "```",
                "",
                "Expected outputs:",
            ]
        )
        lines.extend(f"- `{path}`" for path in phase["outputs"])
        lines.append("")
    lines.extend(["## Quality Gates", ""])
    lines.extend(f"- {gate}" for gate in payload["quality_gates"])
    lines.extend(["", "## Claim Unlock Rules", ""])
    for rule in payload["claim_unlock_rules"]:
        lines.extend(
            [
                f"### {rule['claim']}",
                "",
                f"- Unlock condition: {rule['unlock_condition']}",
                f"- Otherwise: {rule['otherwise']}",
                "",
            ]
        )
    lines.extend(["## Validation", ""])
    problems = validate_runbook(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The runbook is internally consistent and keeps planned experiments separate from executed evidence.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_runbook(json_output: Path, markdown_output: Path) -> None:
    payload = build_runbook()
    problems = validate_runbook(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the FounderBench hosted/local experiment runbook.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_runbook(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
