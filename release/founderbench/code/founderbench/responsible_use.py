from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


def build_statement() -> dict[str, Any]:
    intended_uses = [
        "Evaluate structured decision-making behavior of startup-operator agents in a synthetic, controlled simulator.",
        "Compare models or agent policies only through validated task-level submissions and clearly labeled public/repeated/private result tiers.",
        "Study failure modes such as malformed actions, over-budget decisions, brittle planning, poor runway management, and prompt sensitivity.",
        "Support benchmark-methodology research on agent evaluation, not deployment claims about autonomous companies.",
    ]
    unsupported_uses = [
        "Do not use FounderBench scores as evidence that a model can run a real company or predict real startup success.",
        "Do not use the benchmark as business, investment, hiring, lending, legal, tax, or financial advice.",
        "Do not report public-test performance as hidden, private, contamination-free, or robust to task-template gaming.",
        "Do not rank provider submissions that are missing, manually repaired outside the parser contract, or missing required diagnostics.",
        "Do not use generated agent rationales as executable business recommendations; only structured simulator actions are evaluated.",
    ]
    data_and_privacy = [
        {
            "topic": "Synthetic tasks",
            "statement": "current task definitions are synthetic and do not contain real company records, private founder data, customer data, or human-subject measurements.",
        },
        {
            "topic": "Provider submissions",
            "statement": "Hosted/local model submissions may contain provider responses, latency, token usage, and cost metadata; public audit traces must be redacted before release.",
        },
        {
            "topic": "Human calibration",
            "statement": "The included calibration packet is non-executed. Any future expert or founder study should collect consent, avoid confidential company data, and report aggregate findings.",
        },
        {
            "topic": "Private holdout",
            "statement": "Private task definitions should remain evaluator-controlled; public reports should expose aggregate scores and diagnostics only.",
        },
    ]
    submission_disclosures = [
        "model/provider name, version, and access date when applicable",
        "prompt/protocol version and prompt hashes",
        "decoding settings, self-consistency/reflection policy, and run_seed identities",
        "adapter/parser version and whether any output was manually repaired",
        "provider-error categories, invalid-action counts, timeout handling, and omitted-task status",
        "token usage, latency, estimated cost, and redaction status of any released audit traces",
        "whether the submitted model or prompt was trained, tuned, or optimized on released public tasks",
    ]
    residual_risks = [
        {
            "risk": "Benchmark gaming",
            "mitigation": "Keep public/private tiers separate, execute private holdout externally, and require disclosure of public-task tuning.",
            "status": "partially_mitigated_private_execution_missing",
        },
        {
            "risk": "Overclaiming economic competence",
            "mitigation": "Use claim-evidence, validity, and responsible-use language to restrict claims to controlled simulator decisions.",
            "status": "mitigated_for_current_claims",
        },
        {
            "risk": "Provider privacy or secret leakage",
            "mitigation": "Use environment variables, redacted audit logs, secret scans, and provider-run reports that omit raw keys.",
            "status": "mitigated_by_process",
        },
        {
            "risk": "Human calibration confidentiality",
            "mitigation": "Use synthetic tasks, consent language, and aggregate reporting if expert/founder calibration is executed.",
            "status": "planned_not_executed",
        },
        {
            "risk": "Cost and environmental burden",
            "mitigation": "Report token/cost accounting, support resumable runs, and separate repeated-run ablations from required single-run baselines.",
            "status": "mitigated_not_closed_until_provider_runs",
        },
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Responsible-use, ethics, and disclosure statement for FounderBench.",
        "intended_uses": intended_uses,
        "unsupported_uses": unsupported_uses,
        "data_and_privacy": data_and_privacy,
        "required_submission_disclosures": submission_disclosures,
        "residual_risks": residual_risks,
        "summary": {
            "intended_uses": len(intended_uses),
            "unsupported_uses": len(unsupported_uses),
            "data_privacy_topics": len(data_and_privacy),
            "required_submission_disclosures": len(submission_disclosures),
            "residual_risks": len(residual_risks),
            "contains_real_company_data": False,
            "contains_human_subject_data": False,
            "permits_real_world_startup_success_claims": False,
        },
    }


def validate_statement(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    summary = payload.get("summary", {})
    if summary.get("contains_real_company_data") is not False:
        problems.append("Statement must disclose no real company data.")
    if summary.get("contains_human_subject_data") is not False:
        problems.append("Statement must disclose no included human-subject data.")
    if summary.get("permits_real_world_startup_success_claims") is not False:
        problems.append("Statement must block real-world startup success claims.")
    if summary.get("unsupported_uses", 0) < 5:
        problems.append("Expected at least five unsupported-use guardrails.")
    if summary.get("required_submission_disclosures", 0) < 6:
        problems.append("Expected detailed provider submission disclosure requirements.")
    text = json.dumps(payload, sort_keys=True).lower()
    for required in ["not use FounderBench scores", "real company", "human-subject", "private holdout", "manually repaired", "token usage"]:
        required = required.lower()
        if required not in text:
            problems.append(f"Responsible-use statement must mention {required}.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# FounderBench Responsible Use Statement",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Intended Uses",
        "",
        *[f"- {item}" for item in payload["intended_uses"]],
        "",
        "## Unsupported Uses",
        "",
        *[f"- {item}" for item in payload["unsupported_uses"]],
        "",
        "## Data and Privacy",
        "",
        markdown_table(["Topic", "Statement"], [[row["topic"], row["statement"]] for row in payload["data_and_privacy"]]),
        "",
        "## Required Submission Disclosures",
        "",
        *[f"- {item}" for item in payload["required_submission_disclosures"]],
        "",
        "## Residual Risks",
        "",
        markdown_table(["Risk", "Mitigation", "Status"], [[row["risk"], row["mitigation"], row["status"]] for row in payload["residual_risks"]]),
        "",
        "## Validation",
        "",
    ]
    problems = validate_statement(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The statement keeps intended use, unsupported use, privacy, disclosure, and residual-risk boundaries explicit.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_statement(json_output: Path, markdown_output: Path) -> None:
    payload = build_statement()
    problems = validate_statement(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench responsible-use statement.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_statement(Path(args.json_output), Path(args.markdown_output))


if __name__ == "__main__":
    main()
