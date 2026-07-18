# FounderBench Provider Readiness Matrix

This report checks provider-run configuration without printing or storing secret values.

Ready providers: 0/5

| Provider | Policy | Model | Ready | Environment Status |
| --- | --- | --- | --- | --- |
| DeepSeek | `deepseek` | `deepseek-chat` | False | DEEPSEEK_API_KEY=missing, DEEPSEEK_MODEL=default:deepseek-chat |
| DeepSeek self-consistency | `deepseek_sc` | `deepseek-chat` | False | DEEPSEEK_API_KEY=missing, DEEPSEEK_MODEL=default:deepseek-chat, SC_K=default:3, SC_TEMPERATURE=default:0.7 |
| Anthropic Claude | `anthropic` | `claude-sonnet-4-5` | False | ANTHROPIC_API_KEY=missing, ANTHROPIC_MODEL=default:claude-sonnet-4-5 |
| Google Gemini | `gemini` | `gemini-2.5-flash` | False | GEMINI_API_KEY=missing, GEMINI_MODEL=default:gemini-2.5-flash |
| Local/OpenAI-compatible | `llm` | `Qwen/Qwen2.5-7B-Instruct` | False | OPENAI_COMPAT_API_KEY=optional, OPENAI_COMPAT_MODEL=default:Qwen/Qwen2.5-7B-Instruct, OPENAI_COMPAT_BASE_URL=missing |

## Commands

### DeepSeek

```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek.json --resume
python -m moneybench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-audit.json --resume --audit
python -m moneybench.submission --input outputs/founderbench-deepseek.json --report outputs/founderbench-deepseek-submission-report.md
```

### DeepSeek self-consistency

```powershell
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3.json --resume
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-audit.json --resume --audit
python -m moneybench.submission --input outputs/founderbench-deepseek-sc-k3.json --report outputs/founderbench-deepseek-sc-k3-submission-report.md
```

### Anthropic Claude

```powershell
python -m moneybench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic.json --resume
python -m moneybench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-audit.json --resume --audit
python -m moneybench.submission --input outputs/founderbench-anthropic.json --report outputs/founderbench-anthropic-submission-report.md
```

### Google Gemini

```powershell
python -m moneybench.resumable_runner --policy gemini --output outputs/founderbench-gemini.json --resume
python -m moneybench.resumable_runner --policy gemini --output outputs/founderbench-gemini-audit.json --resume --audit
python -m moneybench.submission --input outputs/founderbench-gemini.json --report outputs/founderbench-gemini-submission-report.md
```

### Local/OpenAI-compatible

```powershell
python -m moneybench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume
python -m moneybench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-audit.json --resume --audit
python -m moneybench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
```
