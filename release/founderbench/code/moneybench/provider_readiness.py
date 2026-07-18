from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


PROVIDERS: list[dict[str, Any]] = [
    {
        "policy": "openai",
        "provider": "OpenAI GPT",
        "api_key_env": "OPENAI_API_KEY",
        "model_env": "OPENAI_MODEL",
        "base_url_env": "OPENAI_BASE_URL",
        "default_base_url": "https://api.openai.com/v1",
        "default_model": "gpt-4.1-mini",
        "output": "outputs/founderbench-openai.json",
        "audit_output": "outputs/founderbench-openai-audit.json",
    },
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
        "policy": "kimi",
        "provider": "Moonshot Kimi",
        "api_key_env": "KIMI_API_KEY",
        "api_key_aliases": ["MOONSHOT_API_KEY"],
        "model_env": "KIMI_MODEL",
        "model_aliases": ["MOONSHOT_MODEL"],
        "base_url_env": "KIMI_BASE_URL",
        "base_url_aliases": ["MOONSHOT_BASE_URL"],
        "default_base_url": "https://api.moonshot.ai/v1",
        "default_model": "kimi-latest",
        "output": "outputs/founderbench-kimi.json",
        "audit_output": "outputs/founderbench-kimi-audit.json",
    },
    {
        "policy": "qwen",
        "provider": "Alibaba Qwen",
        "api_key_env": "QWEN_API_KEY",
        "api_key_aliases": ["DASHSCOPE_API_KEY"],
        "model_env": "QWEN_MODEL",
        "model_aliases": ["DASHSCOPE_MODEL"],
        "base_url_env": "QWEN_BASE_URL",
        "base_url_aliases": ["DASHSCOPE_BASE_URL"],
        "default_base_url": "https://dashscope.aliyuncs.com/compatible-mode/v1",
        "default_model": "qwen-plus",
        "output": "outputs/founderbench-qwen.json",
        "audit_output": "outputs/founderbench-qwen-audit.json",
    },
    {
        "policy": "mistral",
        "provider": "Mistral",
        "api_key_env": "MISTRAL_API_KEY",
        "model_env": "MISTRAL_MODEL",
        "base_url_env": "MISTRAL_BASE_URL",
        "default_base_url": "https://api.mistral.ai/v1",
        "default_model": "mistral-large-latest",
        "output": "outputs/founderbench-mistral.json",
        "audit_output": "outputs/founderbench-mistral-audit.json",
    },
    {
        "policy": "glm",
        "provider": "Z.ai GLM",
        "api_key_env": "GLM_API_KEY",
        "api_key_aliases": ["ZAI_API_KEY"],
        "model_env": "GLM_MODEL",
        "model_aliases": ["ZAI_MODEL"],
        "base_url_env": "GLM_BASE_URL",
        "base_url_aliases": ["ZAI_BASE_URL"],
        "default_base_url": "https://open.bigmodel.cn/api/paas/v4",
        "default_model": "glm-4-plus",
        "output": "outputs/founderbench-glm.json",
        "audit_output": "outputs/founderbench-glm-audit.json",
    },
    {
        "policy": "xai",
        "provider": "xAI Grok",
        "api_key_env": "XAI_API_KEY",
        "model_env": "XAI_MODEL",
        "base_url_env": "XAI_BASE_URL",
        "default_base_url": "https://api.x.ai/v1",
        "default_model": "grok-3-mini",
        "output": "outputs/founderbench-xai.json",
        "audit_output": "outputs/founderbench-xai-audit.json",
    },
    {
        "policy": "llama",
        "provider": "Llama/Open-weight endpoint",
        "api_key_env": "LLAMA_API_KEY",
        "model_env": "LLAMA_MODEL",
        "base_url_env": "LLAMA_BASE_URL",
        "default_model": "meta-llama/Llama-3.1-70B-Instruct",
        "output": "outputs/founderbench-llama.json",
        "audit_output": "outputs/founderbench-llama-audit.json",
        "api_key_optional": True,
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


def _any_env_set(names: list[str]) -> bool:
    return any(_is_set(name) for name in names)


def _configured_or_default(provider: dict[str, Any], key: str, aliases_key: str, default_key: str) -> str:
    names = [provider[key], *provider.get(aliases_key, [])]
    for name in names:
        value = os.environ.get(name)
        if value:
            return value
    return provider.get(default_key, "")


def readiness_matrix() -> dict[str, Any]:
    rows = []
    for provider in PROVIDERS:
        api_key_names = [provider["api_key_env"], *provider.get("api_key_aliases", [])]
        api_key_ready = provider.get("api_key_optional", False) or _any_env_set(api_key_names)
        base_url_ready = True
        if provider.get("base_url_env"):
            base_url_names = [provider["base_url_env"], *provider.get("base_url_aliases", [])]
            base_url_ready = _any_env_set(base_url_names) or bool(provider.get("default_base_url"))
        model = _configured_or_default(provider, "model_env", "model_aliases", "default_model")
        ready = api_key_ready and base_url_ready
        env_status = {
            provider["api_key_env"]: "set" if _is_set(provider["api_key_env"]) else ("optional" if provider.get("api_key_optional") else "missing"),
            provider["model_env"]: "set" if _is_set(provider["model_env"]) else f"default:{provider['default_model']}",
        }
        for alias in provider.get("api_key_aliases", []):
            env_status[alias] = "set" if _is_set(alias) else "alias"
        for alias in provider.get("model_aliases", []):
            env_status[alias] = "set" if _is_set(alias) else "alias"
        if provider.get("base_url_env"):
            env_status[provider["base_url_env"]] = "set" if _is_set(provider["base_url_env"]) else f"default:{provider.get('default_base_url', '')}"
            for alias in provider.get("base_url_aliases", []):
                env_status[alias] = "set" if _is_set(alias) else "alias"
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
