from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, get_args

from .llm_policy import (
    DEEPSEEK_SYSTEM_PROMPT,
    KEY_PATTERN,
    PROMPT_OBJECTIVE,
    PROMPT_RULES,
    PROMPT_VERSION,
    RESPONSE_SCHEMA,
    SYSTEM_PROMPT,
)
from .provider_readiness import PROVIDERS
from .schema import ActionType
from .tasks import TASKS


VERSION = "0.3.0"


def _sha256_json(payload: dict[str, Any]) -> str:
    text = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def prompt_template() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "prompt_version": PROMPT_VERSION,
        "task": {
            "task_id": "<FND-###>",
            "name": "<task name>",
            "description": "<task objective and startup situation>",
            "weeks_remaining": "<integer>",
            "pass_threshold": 70,
        },
        "objective": PROMPT_OBJECTIVE,
        "allowed_actions": "<sorted subset of action_types allowed by this task>",
        "observation": {
            "week": "<integer>",
            "cash": "<float>",
            "reputation": "<float>",
            "agent_capacity": "<float>",
            "markets": "<list of visible market records>",
            "offers": "<list of active offer records>",
            "memory": "<simulator notes from prior weeks>",
        },
        "response_schema": RESPONSE_SCHEMA,
        "rules": PROMPT_RULES,
    }


def build_protocol() -> dict[str, Any]:
    actions = list(get_args(ActionType))
    template = prompt_template()
    provider_wrappers = []
    for provider in PROVIDERS:
        system_prompt = DEEPSEEK_SYSTEM_PROMPT if provider["policy"] == "deepseek" else SYSTEM_PROMPT
        wrapper = {
            "policy": provider["policy"],
            "provider": provider["provider"],
            "default_model": provider["default_model"],
            "system_prompt_sha256": hashlib.sha256(system_prompt.encode("utf-8")).hexdigest(),
            "user_prompt": "render_task_prompt(task, observation)",
            "temperature": 0.2,
        }
        provider_wrappers.append(wrapper)
    protocol = {
        "benchmark": "FounderBench",
        "version": VERSION,
        "prompt_version": PROMPT_VERSION,
        "task_count": len(TASKS),
        "action_types": actions,
        "max_actions_per_week": 4,
        "response_contract": {
            "format": "JSON object only",
            "required_keys": ["rationale", "actions"],
            "action_fields": ["type", "market_id", "offer_id", "budget", "price", "message_quality"],
            "parser": "founderbench.provider_adapter.parse_provider_response",
        },
        "prompt_template": template,
        "prompt_template_sha256": _sha256_json(template),
        "provider_message_wrappers": provider_wrappers,
        "run_trace_requirements": [
            "Record prompt_sha256 for every provider call.",
            "Record raw_response_redacted, parse/error category, token usage, estimated cost, and latency when available.",
            "Validate each complete suite with python -m founderbench.submission before comparing scores.",
        ],
        "anti_gaming_controls": [
            "Models receive only the current task observation and allowed actions.",
            "The simulator executes structured actions only; natural-language business claims do not affect score.",
            "Public runs report prompt hashes, while hidden-holdout evaluation withholds private task definitions.",
        ],
    }
    protocol["protocol_sha256"] = _sha256_json(protocol)
    return protocol


def validate_protocol(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    actions = payload.get("action_types", [])
    if len(actions) != len(get_args(ActionType)):
        problems.append(f"Expected {len(get_args(ActionType))} action types, found {len(actions)}.")
    if set(actions) != set(get_args(ActionType)):
        problems.append("Action vocabulary does not match schema.ActionType.")
    response = payload.get("response_contract", {})
    if response.get("required_keys") != ["rationale", "actions"]:
        problems.append("Response contract must require rationale and actions.")
    wrappers = payload.get("provider_message_wrappers", [])
    if {row.get("policy") for row in wrappers} != {provider["policy"] for provider in PROVIDERS}:
        problems.append("Provider wrappers do not cover every configured provider policy.")
    if payload.get("max_actions_per_week") != 4:
        problems.append("Prompt protocol must preserve the four-action weekly cap.")
    for key in ["prompt_template_sha256", "protocol_sha256"]:
        value = payload.get(key, "")
        if not isinstance(value, str) or len(value) != 64:
            problems.append(f"{key} is not a SHA-256 hex digest.")
    if KEY_PATTERN.search(str(payload)):
        problems.append("Prompt protocol appears to contain a secret-like API key.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# FounderBench Prompt Protocol",
        "",
        f"Version: {payload['version']}",
        f"Prompt version: `{payload['prompt_version']}`",
        f"Prompt template SHA-256: `{payload['prompt_template_sha256']}`",
        f"Protocol SHA-256: `{payload['protocol_sha256']}`",
        "",
        "## Contract",
        "",
        f"- Task count: {payload['task_count']}",
        f"- Maximum actions per week: {payload['max_actions_per_week']}",
        "- Response format: JSON object only with required keys `rationale` and `actions`.",
        "- Parser: `founderbench.provider_adapter.parse_provider_response`.",
        "",
        "## Action Vocabulary",
        "",
        ", ".join(f"`{action}`" for action in payload["action_types"]),
        "",
        "## Prompt Rules",
        "",
    ]
    lines.extend(f"- {rule}" for rule in payload["prompt_template"]["rules"])
    lines.extend(
        [
            "",
            "## Provider Message Wrappers",
            "",
            "| Provider | Policy | Default Model | Temperature | System Prompt Hash |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in payload["provider_message_wrappers"]:
        lines.append(
            f"| {row['provider']} | `{row['policy']}` | `{row['default_model']}` | "
            f"{row['temperature']} | `{row['system_prompt_sha256']}` |"
        )
    lines.extend(
        [
            "",
            "## Run Trace Requirements",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["run_trace_requirements"])
    lines.extend(
        [
            "",
            "## Anti-Gaming Controls",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["anti_gaming_controls"])
    lines.extend(
        [
            "",
            "## Canonical Prompt Template",
            "",
            "```json",
            json.dumps(payload["prompt_template"], indent=2),
            "```",
            "",
        ]
    )
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
    parser = argparse.ArgumentParser(description="Generate FounderBench prompt protocol artifacts.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_protocol(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
