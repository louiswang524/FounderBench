from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .provider_readiness import PROVIDERS


VERSION = "0.3.0"
PRIMARY_TASK_COUNT = 50
MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS = 3


RUNS: list[dict[str, Any]] = [
    {
        "id": "openai_single",
        "policy": "openai",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-openai.json",
        "audit_output": "outputs/founderbench-openai-audit.json",
        "purpose": "Primary OpenAI/GPT hosted baseline, matching the frontier-provider style used by YC-Bench-like comparisons.",
    },
    {
        "id": "deepseek_single",
        "policy": "deepseek",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-deepseek.json",
        "audit_output": "outputs/founderbench-deepseek-audit.json",
        "purpose": "Primary DeepSeek hosted baseline.",
    },
    {
        "id": "deepseek_sc_k3",
        "policy": "deepseek_sc",
        "model_family": "hosted",
        "priority": "recommended",
        "repeat_index": 1,
        "output": "outputs/founderbench-deepseek-sc-k3.json",
        "audit_output": "outputs/founderbench-deepseek-sc-k3-audit.json",
        "purpose": "Self-consistency k=3 ablation for DeepSeek.",
    },
    {
        "id": "anthropic_single",
        "policy": "anthropic",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-anthropic.json",
        "audit_output": "outputs/founderbench-anthropic-audit.json",
        "purpose": "Primary Claude/Anthropic hosted baseline.",
    },
    {
        "id": "gemini_single",
        "policy": "gemini",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-gemini.json",
        "audit_output": "outputs/founderbench-gemini-audit.json",
        "purpose": "Primary Gemini hosted baseline.",
    },
    {
        "id": "kimi_single",
        "policy": "kimi",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-kimi.json",
        "audit_output": "outputs/founderbench-kimi-audit.json",
        "purpose": "Primary Moonshot Kimi hosted/open-weight-family baseline.",
    },
    {
        "id": "qwen_single",
        "policy": "qwen",
        "model_family": "hosted",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-qwen.json",
        "audit_output": "outputs/founderbench-qwen-audit.json",
        "purpose": "Primary Alibaba Qwen hosted/open-weight-family baseline.",
    },
    {
        "id": "mistral_single",
        "policy": "mistral",
        "model_family": "hosted",
        "priority": "recommended",
        "repeat_index": 1,
        "output": "outputs/founderbench-mistral.json",
        "audit_output": "outputs/founderbench-mistral-audit.json",
        "purpose": "Mistral hosted baseline for broader non-US provider coverage.",
    },
    {
        "id": "glm_single",
        "policy": "glm",
        "model_family": "hosted",
        "priority": "recommended",
        "repeat_index": 1,
        "output": "outputs/founderbench-glm.json",
        "audit_output": "outputs/founderbench-glm-audit.json",
        "purpose": "Z.ai GLM hosted baseline for additional China-developed model coverage.",
    },
    {
        "id": "xai_single",
        "policy": "xai",
        "model_family": "hosted",
        "priority": "recommended",
        "repeat_index": 1,
        "output": "outputs/founderbench-xai.json",
        "audit_output": "outputs/founderbench-xai-audit.json",
        "purpose": "xAI/Grok hosted baseline for another frontier closed-model family.",
    },
    {
        "id": "llama_endpoint_single",
        "policy": "llama",
        "model_family": "local_open_source",
        "priority": "recommended",
        "repeat_index": 1,
        "output": "outputs/founderbench-llama.json",
        "audit_output": "outputs/founderbench-llama-audit.json",
        "purpose": "Llama/open-weight endpoint baseline, runnable through any OpenAI-compatible serving provider.",
    },
    {
        "id": "local_open_model_single",
        "policy": "llm",
        "model_family": "local_open_source",
        "priority": "required",
        "repeat_index": 1,
        "output": "outputs/founderbench-local-open-model.json",
        "audit_output": "outputs/founderbench-local-open-model-audit.json",
        "purpose": "Primary local/open-source baseline through an OpenAI-compatible server.",
    },
]


def _provider_by_policy() -> dict[str, dict[str, Any]]:
    return {provider["policy"]: provider for provider in PROVIDERS}


def _submission_report_path(output: str) -> str:
    return output.replace(".json", "-submission-report.md")


def _run_command(policy: str, output: str, *, audit: bool = False, seed: int = 0) -> str:
    suffix = " --audit" if audit else ""
    return f"python -m moneybench.resumable_runner --policy {policy} --output {output} --resume --seed {seed}{suffix}"


def _validation_command(output: str) -> str:
    return f"python -m moneybench.submission --input {output} --report {_submission_report_path(output)}"


def _repeat_output(output: str) -> str:
    return output.replace(".json", "-repeats.json")


def _seed_output(output: str, seed: int) -> str:
    return output.replace(".json", f"-seed{seed}.json")


def _bundle_command(policy: str, output: str) -> str:
    repeat_output = _repeat_output(output)
    inputs = " ".join(f"--input {_seed_output(output, seed)}" for seed in range(MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS))
    return f"python -m moneybench.submission_bundle {inputs} --output {repeat_output} --report {_submission_report_path(repeat_output)}"


def build_plan() -> dict[str, Any]:
    providers = _provider_by_policy()
    runs = []
    for spec in RUNS:
        provider = providers[spec["policy"]]
        row = dict(spec)
        row["task_count"] = PRIMARY_TASK_COUNT
        row["model_env"] = provider["model_env"]
        row["api_key_env"] = provider["api_key_env"]
        row["base_url_env"] = provider.get("base_url_env", "")
        row["default_model"] = provider["default_model"]
        row["run_command"] = _run_command(spec["policy"], spec["output"], seed=spec["repeat_index"] - 1)
        row["audit_command"] = _run_command(spec["policy"], spec["audit_output"], audit=True, seed=spec["repeat_index"] - 1)
        row["validation_command"] = _validation_command(spec["output"])
        row["audit_validation_command"] = _validation_command(spec["audit_output"])
        row["submission_report"] = _submission_report_path(spec["output"])
        row["audit_submission_report"] = _submission_report_path(spec["audit_output"])
        row["repeat_outputs"] = [_seed_output(spec["output"], seed) for seed in range(MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS)]
        row["repeat_bundle_output"] = _repeat_output(spec["output"])
        row["repeat_bundle_report"] = _submission_report_path(row["repeat_bundle_output"])
        row["repeat_bundle_command"] = _bundle_command(spec["policy"], spec["output"])
        row["repeat_validation_command"] = _validation_command(row["repeat_bundle_output"])
        runs.append(row)

    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Execution plan for paper-grade hosted and local/open-source LLM baseline runs.",
        "scope": {
            "task_count": PRIMARY_TASK_COUNT,
            "splits": ["public_dev", "public_test"],
            "primary_endpoint": "average_task_score",
            "secondary_endpoints": ["solved", "solve_rate", "shutdown_rate", "invalid_actions", "over_budget_decisions", "provider_errors", "decision_latency_s", "simulated_api_cost"],
            "planned_model_roster": ["OpenAI/GPT", "Anthropic/Claude", "Google/Gemini", "DeepSeek", "Moonshot/Kimi", "Alibaba/Qwen", "Mistral", "Z.ai/GLM", "xAI/Grok", "Llama/open-weight", "local OpenAI-compatible"],
        },
        "fairness_controls": [
            "Use the canonical prompt protocol and structured action schema for every provider.",
            "Run every required model on the same 50 current task ids.",
            "Separate required frontier/commercial coverage from recommended broader ecosystem coverage so missing optional APIs do not block core reproducibility.",
            "Validate every output with moneybench.submission before including it in leaderboard claims.",
            "Do not drop failed tasks, malformed outputs, provider errors, bankruptcies, or over-budget decisions.",
            "Report provider model ids, prompt/protocol hashes, latency, token usage when available, and estimated cost.",
            "Use the pre-specified paired task-level statistical protocol for model comparisons.",
        ],
        "repetition_policy": {
            "single_run_claims": "Allowed only as preliminary baseline rows when clearly labeled single-run.",
            "stochastic_claims": f"Require at least {MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS} repeats or an explicit limitation statement; record each repeat with a distinct resumable-runner --seed value.",
            "bundle_protocol": "Combine repeated seed outputs with moneybench.submission_bundle and report the generated submission report before stochastic confidence claims.",
            "self_consistency": "DeepSeek self-consistency uses k=3 as a separate ablation, not a replacement for the naive baseline.",
        },
        "audit_policy": {
            "required_audit_traces": "Collect redacted audit runs for at least one hosted provider before qualitative LLM failure analysis.",
            "redaction": "Audit artifacts must retain prompt hashes and diagnostics while removing raw secret values.",
            "sharing": "Inspect audit files manually before public release because model responses may contain accidental sensitive text.",
        },
        "acceptance_criteria": [
            "Each required run produces a JSON output with exactly 50 task results.",
            "Each required run passes moneybench.submission validation.",
            "Provider-error categories are reported even when zero.",
            "At least three provider configurations are ready before the submission gate can pass provider readiness.",
            "Claim-evidence report remains conservative until all LLM comparison evidence exists.",
        ],
        "runs": runs,
        "summary": {
            "planned_runs": len(runs),
            "required_runs": sum(1 for row in runs if row["priority"] == "required"),
            "recommended_runs": sum(1 for row in runs if row["priority"] == "recommended"),
            "hosted_runs": sum(1 for row in runs if row["model_family"] == "hosted"),
            "local_open_source_runs": sum(1 for row in runs if row["model_family"] == "local_open_source"),
            "minimum_repeats_for_stochastic_claims": MINIMUM_REPEATS_FOR_STOCHASTIC_CLAIMS,
        },
    }


def validate_plan(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["scope"]["task_count"] != PRIMARY_TASK_COUNT:
        problems.append(f"Expected task_count={PRIMARY_TASK_COUNT}.")
    if payload["summary"]["required_runs"] < 4:
        problems.append("Expected at least four required LLM/local baseline runs.")
    if payload["summary"]["hosted_runs"] < 3:
        problems.append("Expected at least three hosted provider runs.")
    if payload["summary"]["local_open_source_runs"] < 1:
        problems.append("Expected at least one local/open-source run.")
    if payload["repetition_policy"]["self_consistency"].lower().find("separate ablation") < 0:
        problems.append("Self-consistency must be treated as a separate ablation.")
    for row in payload["runs"]:
        if row["task_count"] != PRIMARY_TASK_COUNT:
            problems.append(f"{row['id']} does not target all public tasks.")
        if "--resume" not in row["run_command"]:
            problems.append(f"{row['id']} run command must be resumable.")
        if "--seed" not in row["run_command"]:
            problems.append(f"{row['id']} run command must record a repeat seed/index.")
        if "moneybench.submission" not in row["validation_command"]:
            problems.append(f"{row['id']} missing submission validation command.")
        if "moneybench.submission_bundle" not in row["repeat_bundle_command"]:
            problems.append(f"{row['id']} missing repeated-run bundle command.")
        if row["priority"] == "required" and not row["submission_report"]:
            problems.append(f"{row['id']} missing submission report path.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    run_rows = [
        [
            row["id"],
            row["policy"],
            row["model_family"],
            row["priority"],
            row["task_count"],
            row["output"],
            row["submission_report"],
            row["repeat_bundle_output"],
        ]
        for row in payload["runs"]
    ]
    lines = [
        "# FounderBench Baseline Execution Plan",
        "",
        payload["purpose"],
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Scope",
        "",
        markdown_table(["Field", "Value"], [[key, value] for key, value in payload["scope"].items()]),
        "",
        "## Fairness Controls",
        "",
    ]
    lines.extend(f"- {item}" for item in payload["fairness_controls"])
    lines.extend(["", "## Repetition Policy", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in payload["repetition_policy"].items())
    lines.extend(["", "## Audit Policy", ""])
    lines.extend(f"- `{key}`: {value}" for key, value in payload["audit_policy"].items())
    lines.extend(["", "## Acceptance Criteria", ""])
    lines.extend(f"- {item}" for item in payload["acceptance_criteria"])
    lines.extend(
        [
            "",
            "## Planned Runs",
            "",
            markdown_table(["ID", "Policy", "Family", "Priority", "Tasks", "Output", "Submission Report", "Repeat Bundle"], run_rows),
            "",
            "## Commands",
            "",
        ]
    )
    for row in payload["runs"]:
        lines.extend(
            [
                f"### {row['id']}",
                "",
                row["purpose"],
                "",
                "```powershell",
                row["run_command"],
                row["validation_command"],
                row["audit_command"],
                row["audit_validation_command"],
                row["repeat_bundle_command"],
                row["repeat_validation_command"],
                "```",
                "",
            ]
        )
    lines.extend(["## Validation", ""])
    problems = validate_plan(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The execution plan covers the required hosted and local/open-source baseline evidence needed before LLM comparison claims are made.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_plan(json_output: Path, markdown_output: Path) -> None:
    payload = build_plan()
    problems = validate_plan(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate hosted/local baseline execution plan.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_plan(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
