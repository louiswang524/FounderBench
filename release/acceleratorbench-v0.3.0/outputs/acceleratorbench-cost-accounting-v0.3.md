# FounderBench v0.3 Cost Accounting Protocol

Provider token and cost-accounting protocol for hosted/local model runs.

## Price Environment Variables

| Variable | Status |
| --- | --- |
| MODEL_INPUT_COST_PER_MILLION | missing |
| MODEL_OUTPUT_COST_PER_MILLION | missing |

## Usage Fields

- `provider_prompt_tokens`
- `provider_completion_tokens`
- `provider_total_tokens`
- `estimated_provider_cost_usd`

## Extraction Rules

- OpenAI/DeepSeek-style usage fields are read from prompt_tokens, completion_tokens, and total_tokens.
- Alternative usage aliases input_tokens/output_tokens and Gemini promptTokenCount/candidatesTokenCount/totalTokenCount are normalized into the same fields.
- If a provider omits usage metadata, token counts remain zero and the paper must report usage as unavailable for that run.
- Estimated provider cost is computed only from recorded token counts and evaluator-configured per-million-token prices.
- The benchmark never stores provider API keys or billing account data in generated artifacts.

## Cost Formula

| Field | Value |
| --- | --- |
| estimated_provider_cost_usd | prompt_tokens * MODEL_INPUT_COST_PER_MILLION / 1_000_000 + completion_tokens * MODEL_OUTPUT_COST_PER_MILLION / 1_000_000 |
| rounding | six decimal places |
| currency | USD when configured prices are USD-denominated |

## Reporting Requirements

- Report token counts and estimated cost for every hosted/local run when provider usage metadata is available.
- Report the exact per-million-token input/output price assumptions used for each model run, but not secret API keys.
- Treat cost as a diagnostic efficiency metric, not as part of the primary task score.
- Do not compare provider cost rows unless price assumptions and usage availability are both documented.
- If prices are unset, report estimated cost as zero and mark cost comparison as unavailable.

## Worked Examples

| Prompt Tokens | Completion Tokens | Input $/M | Output $/M | Estimated Cost |
| --- | --- | --- | --- | --- |
| 100000 | 25000 | 0.1 | 0.4 | 0.02 |
| 1000000 | 250000 | 1.0 | 3.0 | 1.75 |

## Summary

| Metric | Value |
| --- | --- |
| price_env_vars | 2 |
| usage_fields | 4 |
| env_prices_configured | False |
| env_prices_positive | False |

## Validation

Status: PASS

The protocol is internally consistent and contains no provider secret values.
