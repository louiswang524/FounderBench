# FounderBench Final Provider Results

This table summarizes the validated hosted-provider runs available in this workspace. Runs with provider/parser errors are still included, but the diagnostics must be reported with the score.

| Model | Avg Score | Solved | Provider/Parser Errors | Error Categories | Tokens |
| --- | ---: | ---: | ---: | --- | ---: |
| Gemini 3.5 Flash | 67.69 | 32/50 | 59 | `invalid_json=29`, `provider_rate_limit=30` | 1,356,532 |
| DeepSeek V4 Reasoner | 62.43 | 27/50 | 3 | `invalid_numeric_field=1`, `invalid_json=2` | 1,467,535 |
| DeepSeek Chat | 56.59 | 23/50 | 0 | none | 750,075 |
| GLM 4.5 Air | 54.78 | 23/50 | 0 | none | 698,110 |
| Gemini 2.5 Flash | 52.69 | 13/50 | 340 | `invalid_json=8`, `provider_io_error=332` | 560,539 |

Notes:

- Gemini 2.5 Flash is included as requested, but should be labeled degraded because most of its failures were provider/API or parser errors.
- The official model-comparison artifacts include the planned validated provider rows at `outputs/founderbench-model-comparison.md`.
- Hosted LLM comparison claims are still not fully ready because several required provider/local baselines remain missing.
