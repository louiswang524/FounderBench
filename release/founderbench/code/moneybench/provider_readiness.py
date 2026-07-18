from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


PROVIDERS: list[dict[str, Any]] = [
    {
        "policy": "deepseek",
        "provider": "DeepSeek",
        "api_key_env": "DEEPSEEK_API_KEY",
        "model_env": "DEEPSEEK_MODEL",
        "default_model": "deepseek-chat",
        "output": "outputs/founderbench-deepseek.json",
        "audit_output": "outputs/founderbench-deepseek-audit.json",
    },
    {
        "policy": "deepseek_sc",
        "provider": "DeepSeek self-consistency",
        "api_key_env": "DEEPSEEK_API_KEY",
        "model_env": "DEEPSEEK_MODEL",
        "default_model": "deepseek-chat",
        "output": "outputs/founderbench-deepseek-sc-k3.json",
        "audit_output": "outputs/founderbench-deepseek-sc-k3-audit.json",
        "extra_env": {"SC_K": "3", "SC_TEMPERATURE": "0.7"},
    },
    {
        "policy": "anthropic",
        "provider": "Anthropic Claude",
        "api_key_env": "ANTHROPIC_API_KEY",
        "model_env": "ANTHROPIC_MODEL",
        "default_model": "claude-sonnet-4-5",
        "output": "outputs/founderbench-anthropic.json",
        "audit_output": "outputs/founderbench-anthropic-audit.json",
    },
    {
        "policy": "gemini",
        "provider": "Google Gemini",
        "api_key_env": "GEMINI_API_KEY",
        "model_env": "GEMINI_MODEL",
        "default_model": "gemini-2.5-flash",
        "output": "outputs/founderbench-gemini.json",
        "audit_output": "outputs/founderbench-gemini-audit.json",
    },
    {
        "policy": "llm",
        "provider": "Local/OpenAI-compatible",
        "api_key_env": "OPENAI_COMPAT_API_KEY",
        "model_env": "OPENAI_COMPAT_MODEL",
        "base_url_env": "OPENAI_COMPAT_BASE_URL",
        "default_model": "Qwen/Qwen2.5-7B-Instruct",
        "output": "outputs/founderbench-local-open-model.json",
        "audit_output": "outputs/founderbench-local-open-model-audit.json",
        "api_key_optional": True,
    },
]


def _is_set(name: str) -> bool:
    return bool(os.environ.get(name))


def readiness_matrix() -> dict[str, Any]:
    rows = []
    for provider in PROVIDERS:
        api_key_ready = provider.get("api_key_optional", False) or _is_set(provider["api_key_env"])
        base_url_ready = True
        if provider.get("base_url_env"):
            base_url_ready = _is_set(provider["base_url_env"])
        model = os.environ.get(provider["model_env"]) or provider["default_model"]
        ready = api_key_ready and base_url_ready
        env_status = {
            provider["api_key_env"]: "set" if _is_set(provider["api_key_env"]) else ("optional" if provider.get("api_key_optional") else "missing"),
            provider["model_env"]: "set" if _is_set(provider["model_env"]) else f"default:{provider['default_model']}",
        }
        if provider.get("base_url_env"):
            env_status[provider["base_url_env"]] = "set" if _is_set(provider["base_url_env"]) else "missing"
        for key, default in provider.get("extra_env", {}).items():
            env_status[key] = "set" if _is_set(key) else f"default:{default}"
        rows.append(
            {
                "provider": provider["provider"],
                "policy": provider["policy"],
                "model": model,
                "ready_without_secrets_exposed": ready,
                "env_status": env_status,
                "run_command": f"python -m moneybench.resumable_runner --policy {provider['policy']} --output {provider['output']} --resume",
                "audit_command": f"python -m moneybench.resumable_runner --policy {provider['policy']} --output {provider['audit_output']} --resume --audit",
                "validation_command": f"python -m moneybench.submission --input {provider['output']} --report {provider['output'].replace('.json', '-submission-report.md')}",
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "note": "This report records whether required environment variables are configured. It never stores secret values.",
        "providers": rows,
        "ready_count": sum(1 for row in rows if row["ready_without_secrets_exposed"]),
        "provider_count": len(rows),
    }


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    lines = [
        "# FounderBench Provider Readiness Matrix",
        "",
        "This report checks provider-run configuration without printing or storing secret values.",
        "",
        f"Ready providers: {payload['ready_count']}/{payload['provider_count']}",
        "",
        "| Provider | Policy | Model | Ready | Environment Status |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in payload["providers"]:
        env_status = ", ".join(f"{key}={value}" for key, value in row["env_status"].items())
        lines.append(f"| {row['provider']} | `{row['policy']}` | `{row['model']}` | {row['ready_without_secrets_exposed']} | {env_status} |")
    lines.extend(["", "## Commands", ""])
    for row in payload["providers"]:
        lines.extend(
            [
                f"### {row['provider']}",
                "",
                "```powershell",
                row["run_command"],
                row["audit_command"],
                row["validation_command"],
                "```",
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_readiness(json_output: Path, markdown_output: Path) -> None:
    payload = readiness_matrix()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate provider readiness matrix without exposing secrets.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_readiness(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
