from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"
PRICE_ENV_VARS = ["MODEL_INPUT_COST_PER_MILLION", "MODEL_OUTPUT_COST_PER_MILLION"]
USAGE_FIELDS = ["provider_prompt_tokens", "provider_completion_tokens", "provider_total_tokens", "estimated_provider_cost_usd"]


def _price_env_status() -> dict[str, str]:
    status = {}
    for name in PRICE_ENV_VARS:
        raw = os.environ.get(name)
        if raw is None:
            status[name] = "missing"
            continue
        try:
            value = float(raw)
        except ValueError:
            status[name] = "invalid_number"
            continue
        status[name] = "set_zero" if value == 0 else "set_positive"
    return status


def estimate_cost(prompt_tokens: int, completion_tokens: int, input_per_million: float, output_per_million: float) -> float:
    return round(
        prompt_tokens * input_per_million / 1_000_000
        + completion_tokens * output_per_million / 1_000_000,
        6,
    )


def build_protocol() -> dict[str, Any]:
    env_status = _price_env_status()
    examples = [
        {
            "prompt_tokens": 100_000,
            "completion_tokens": 25_000,
            "input_cost_per_million": 0.10,
            "output_cost_per_million": 0.40,
            "estimated_cost_usd": estimate_cost(100_000, 25_000, 0.10, 0.40),
        },
        {
            "prompt_tokens": 1_000_000,
            "completion_tokens": 250_000,
            "input_cost_per_million": 1.00,
            "output_cost_per_million": 3.00,
            "estimated_cost_usd": estimate_cost(1_000_000, 250_000, 1.00, 3.00),
        },
    ]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Provider token and cost-accounting protocol for hosted/local model runs.",
        "price_environment_variables": env_status,
        "usage_fields": USAGE_FIELDS,
        "extraction_rules": [
            "OpenAI/DeepSeek-style usage fields are read from prompt_tokens, completion_tokens, and total_tokens.",
            "Alternative usage aliases input_tokens/output_tokens and Gemini promptTokenCount/candidatesTokenCount/totalTokenCount are normalized into the same fields.",
            "If a provider omits usage metadata, token counts remain zero and the paper must report usage as unavailable for that run.",
            "Estimated provider cost is computed only from recorded token counts and evaluator-configured per-million-token prices.",
            "The benchmark never stores provider API keys or billing account data in generated artifacts.",
        ],
        "cost_formula": {
            "estimated_provider_cost_usd": "prompt_tokens * MODEL_INPUT_COST_PER_MILLION / 1_000_000 + completion_tokens * MODEL_OUTPUT_COST_PER_MILLION / 1_000_000",
            "rounding": "six decimal places",
            "currency": "USD when configured prices are USD-denominated",
        },
        "reporting_requirements": [
            "Report token counts and estimated cost for every hosted/local run when provider usage metadata is available.",
            "Report the exact per-million-token input/output price assumptions used for each model run, but not secret API keys.",
            "Treat cost as a diagnostic efficiency metric, not as part of the primary task score.",
            "Do not compare provider cost rows unless price assumptions and usage availability are both documented.",
            "If prices are unset, report estimated cost as zero and mark cost comparison as unavailable.",
        ],
        "examples": examples,
        "summary": {
            "price_env_vars": len(PRICE_ENV_VARS),
            "usage_fields": len(USAGE_FIELDS),
            "env_prices_configured": all(value in {"set_zero", "set_positive"} for value in env_status.values()),
            "env_prices_positive": all(value == "set_positive" for value in env_status.values()),
        },
    }


def validate_protocol(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if set(payload.get("price_environment_variables", {})) != set(PRICE_ENV_VARS):
        problems.append("Price environment-variable status is incomplete.")
    if set(payload.get("usage_fields", [])) != set(USAGE_FIELDS):
        problems.append("Usage fields do not match the submission diagnostics contract.")
    for example in payload.get("examples", []):
        expected = estimate_cost(
            int(example["prompt_tokens"]),
            int(example["completion_tokens"]),
            float(example["input_cost_per_million"]),
            float(example["output_cost_per_million"]),
        )
        if example["estimated_cost_usd"] != expected:
            problems.append("Cost example does not match the documented formula.")
    text = json.dumps(payload)
    if "sk-" in text or "AQ." in text:
        problems.append("Protocol must not contain secret-looking values.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    env_rows = [[key, value] for key, value in payload["price_environment_variables"].items()]
    formula_rows = [[key, value] for key, value in payload["cost_formula"].items()]
    example_rows = [
        [
            row["prompt_tokens"],
            row["completion_tokens"],
            row["input_cost_per_million"],
            row["output_cost_per_million"],
            row["estimated_cost_usd"],
        ]
        for row in payload["examples"]
    ]
    lines = [
        "# FounderBench Cost Accounting Protocol",
        "",
        payload["purpose"],
        "",
        "## Price Environment Variables",
        "",
        markdown_table(["Variable", "Status"], env_rows),
        "",
        "## Usage Fields",
        "",
    ]
    lines.extend(f"- `{field}`" for field in payload["usage_fields"])
    lines.extend(["", "## Extraction Rules", ""])
    lines.extend(f"- {rule}" for rule in payload["extraction_rules"])
    lines.extend(
        [
            "",
            "## Cost Formula",
            "",
            markdown_table(["Field", "Value"], formula_rows),
            "",
            "## Reporting Requirements",
            "",
        ]
    )
    lines.extend(f"- {item}" for item in payload["reporting_requirements"])
    lines.extend(
        [
            "",
            "## Worked Examples",
            "",
            markdown_table(["Prompt Tokens", "Completion Tokens", "Input $/M", "Output $/M", "Estimated Cost"], example_rows),
            "",
            "## Summary",
            "",
            markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
            "",
            "## Validation",
            "",
        ]
    )
    problems = validate_protocol(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The protocol is internally consistent and contains no provider secret values.")
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
    parser = argparse.ArgumentParser(description="Generate provider token/cost-accounting protocol.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_protocol(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
