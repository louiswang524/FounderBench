from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "http://localhost:8000/v1"
DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"


def local_config_from_env() -> dict[str, Any]:
    return {
        "endpoint_type": "local-openai-compatible",
        "base_url": (os.environ.get("OPENAI_COMPAT_BASE_URL") or DEFAULT_BASE_URL).rstrip("/"),
        "model": os.environ.get("OPENAI_COMPAT_MODEL") or DEFAULT_MODEL,
        "api_key_configured": bool(os.environ.get("OPENAI_COMPAT_API_KEY") or os.environ.get("OPENAI_API_KEY")),
        "timeout_s": int(os.environ.get("PROVIDER_TIMEOUT_S", "60")),
    }


def validate_local_config(config: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    base_url = str(config.get("base_url", ""))
    model = str(config.get("model", ""))
    if not base_url.startswith(("http://", "https://")):
        problems.append("base_url must start with http:// or https://.")
    if not base_url.rstrip("/").endswith("/v1"):
        problems.append("base_url should point at an OpenAI-compatible /v1 endpoint.")
    if not model:
        problems.append("model is required.")
    return problems


def check_models_endpoint(config: dict[str, Any]) -> dict[str, Any]:
    url = f"{str(config['base_url']).rstrip('/')}/models"
    request = urllib.request.Request(url, headers={"Content-Type": "application/json"}, method="GET")
    try:
        with urllib.request.urlopen(request, timeout=int(config.get("timeout_s", 10))) as response:
            body = json.loads(response.read().decode("utf-8"))
        model_ids = [item.get("id") for item in body.get("data", []) if isinstance(item, dict)]
        return {
            "ok": True,
            "url": url,
            "configured_model": config.get("model"),
            "available_models": model_ids,
            "configured_model_available": config.get("model") in model_ids if model_ids else None,
        }
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError, OSError) as exc:
        return {
            "ok": False,
            "url": url,
            "configured_model": config.get("model"),
            "error_type": type(exc).__name__,
            "error": str(exc),
        }


def protocol(config: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = config or local_config_from_env()
    return {
        "benchmark": "FounderBench",
        "benchmark_version": "0.3.0",
        "purpose": "Run a local/open-source model through an OpenAI-compatible chat-completions server.",
        "recommended_models": [
            "Qwen/Qwen2.5-7B-Instruct",
            "Qwen/Qwen2.5-14B-Instruct",
            "meta-llama/Llama-3.1-8B-Instruct",
            "mistralai/Mistral-7B-Instruct-v0.3",
        ],
        "config": cfg,
        "environment": {
            "OPENAI_COMPAT_BASE_URL": cfg["base_url"],
            "OPENAI_COMPAT_MODEL": cfg["model"],
            "OPENAI_COMPAT_API_KEY": "optional for local servers; do not commit real keys",
        },
        "commands": [
            "python -m moneybench.local_model protocol --output outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.json",
            "python -m moneybench.local_model health --output outputs/local-health.json",
            "python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3.json --resume --audit",
            "python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3.json --report outputs/acceleratorbench-local-open-model-submission-report.md",
        ],
        "reporting_requirements": [
            "model id and exact checkpoint or quantization",
            "inference server and version",
            "hardware",
            "decoding settings",
            "raw run JSON",
            "submission validation report",
            "representative redacted audit traces",
        ],
    }


def write_protocol(output: Path, config: dict[str, Any] | None = None) -> None:
    payload = protocol(config)
    problems = validate_local_config(payload["config"])
    if problems:
        raise ValueError("; ".join(problems))
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.suffix.lower() == ".md":
        lines = [
            "# FounderBench Local/Open-Source Model Protocol",
            "",
            "This protocol runs a local or open-source model through an OpenAI-compatible `/v1/chat/completions` endpoint.",
            "",
            "## Environment",
            "",
            *[f"- `{key}`: `{value}`" for key, value in payload["environment"].items()],
            "",
            "## Commands",
            "",
            *[f"```powershell\n{command}\n```" for command in payload["commands"]],
            "",
            "## Reporting Requirements",
            "",
            *[f"- {item}" for item in payload["reporting_requirements"]],
            "",
        ]
        output.write_text("\n".join(lines), encoding="utf-8")
    else:
        output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Local/open-source OpenAI-compatible model helper.")
    parser.add_argument("command", choices=["protocol", "health"])
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    config = local_config_from_env()
    output = Path(args.output)
    if args.command == "protocol":
        write_protocol(output, config)
        print(f"Wrote {output}")
        return
    result = {"config": config, "config_problems": validate_local_config(config), "health": check_models_endpoint(config)}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
