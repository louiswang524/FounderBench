# FounderBench Provider Readiness Matrix

This report checks provider-run configuration without printing or storing secret values.

Ready providers: 0/12

| Provider | Policy | Model | Ready | Environment Status |
| --- | --- | --- | --- | --- |
| OpenAI GPT | `openai` | `gpt-4.1-mini` | False | OPENAI_API_KEY=missing, OPENAI_MODEL=default:gpt-4.1-mini, OPENAI_BASE_URL=default:https://api.openai.com/v1 |
| DeepSeek | `deepseek` | `deepseek-chat` | False | DEEPSEEK_API_KEY=missing, DEEPSEEK_MODEL=default:deepseek-chat |
| DeepSeek self-consistency | `deepseek_sc` | `deepseek-chat` | False | DEEPSEEK_API_KEY=missing, DEEPSEEK_MODEL=default:deepseek-chat, SC_K=default:3, SC_TEMPERATURE=default:0.7 |
| Anthropic Claude | `anthropic` | `claude-sonnet-4-5` | False | ANTHROPIC_API_KEY=missing, ANTHROPIC_MODEL=default:claude-sonnet-4-5 |
| Google Gemini | `gemini` | `gemini-2.5-flash` | False | GEMINI_API_KEY=missing, GEMINI_MODEL=default:gemini-2.5-flash |
| Moonshot Kimi | `kimi` | `kimi-latest` | False | KIMI_API_KEY=missing, KIMI_MODEL=default:kimi-latest, MOONSHOT_API_KEY=alias, MOONSHOT_MODEL=alias, KIMI_BASE_URL=default:https://api.moonshot.ai/v1, MOONSHOT_BASE_URL=alias |
| Alibaba Qwen | `qwen` | `qwen-plus` | False | QWEN_API_KEY=missing, QWEN_MODEL=default:qwen-plus, DASHSCOPE_API_KEY=alias, DASHSCOPE_MODEL=alias, QWEN_BASE_URL=default:https://dashscope.aliyuncs.com/compatible-mode/v1, DASHSCOPE_BASE_URL=alias |
| Mistral | `mistral` | `mistral-large-latest` | False | MISTRAL_API_KEY=missing, MISTRAL_MODEL=default:mistral-large-latest, MISTRAL_BASE_URL=default:https://api.mistral.ai/v1 |
| Z.ai GLM | `glm` | `glm-4-plus` | False | GLM_API_KEY=missing, GLM_MODEL=default:glm-4-plus, ZAI_API_KEY=alias, ZAI_MODEL=alias, GLM_BASE_URL=default:https://open.bigmodel.cn/api/paas/v4, ZAI_BASE_URL=alias |
| xAI Grok | `xai` | `grok-3-mini` | False | XAI_API_KEY=missing, XAI_MODEL=default:grok-3-mini, XAI_BASE_URL=default:https://api.x.ai/v1 |
| Llama/Open-weight endpoint | `llama` | `meta-llama/Llama-3.1-70B-Instruct` | False | LLAMA_API_KEY=optional, LLAMA_MODEL=default:meta-llama/Llama-3.1-70B-Instruct, LLAMA_BASE_URL=default: |
| Local/OpenAI-compatible | `llm` | `Qwen/Qwen2.5-7B-Instruct` | False | OPENAI_COMPAT_API_KEY=optional, OPENAI_COMPAT_MODEL=default:Qwen/Qwen2.5-7B-Instruct, OPENAI_COMPAT_BASE_URL=default: |

## Commands

### OpenAI GPT

```powershell
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai.json --resume
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-openai.json --report outputs/founderbench-openai-submission-report.md
```

### DeepSeek

```powershell
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek.json --resume
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-deepseek.json --report outputs/founderbench-deepseek-submission-report.md
```

### DeepSeek self-consistency

```powershell
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3.json --resume
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-deepseek-sc-k3.json --report outputs/founderbench-deepseek-sc-k3-submission-report.md
```

### Anthropic Claude

```powershell
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic.json --resume
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-anthropic.json --report outputs/founderbench-anthropic-submission-report.md
```

### Google Gemini

```powershell
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini.json --resume
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-gemini.json --report outputs/founderbench-gemini-submission-report.md
```

### Moonshot Kimi

```powershell
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi.json --resume
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-kimi.json --report outputs/founderbench-kimi-submission-report.md
```

### Alibaba Qwen

```powershell
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen.json --resume
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-qwen.json --report outputs/founderbench-qwen-submission-report.md
```

### Mistral

```powershell
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral.json --resume
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-mistral.json --report outputs/founderbench-mistral-submission-report.md
```

### Z.ai GLM

```powershell
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm.json --resume
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-glm.json --report outputs/founderbench-glm-submission-report.md
```

### xAI Grok

```powershell
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai.json --resume
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-xai.json --report outputs/founderbench-xai-submission-report.md
```

### Llama/Open-weight endpoint

```powershell
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama.json --resume
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-llama.json --report outputs/founderbench-llama-submission-report.md
```

### Local/OpenAI-compatible

```powershell
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
```
