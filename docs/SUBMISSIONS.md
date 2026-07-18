# Model Submissions

FounderBench submissions are JSON files produced by `founderbench.resumable_runner` or by an external agent that follows the same schema.

## Required Contract

A valid public submission must include:

- benchmark name `FounderBench`
- version `0.3.0`
- one run covering all 50 public tasks, `FND-001` through `FND-050`
- task-level score objects
- split summaries for `public_dev` and `public_test`
- aggregate diagnostics, including invalid actions and provider error categories
- model/provider metadata and run seed

Validate before reporting:

```bash
python -m founderbench.submission --input outputs/provider-run.json --report outputs/provider-run-report.md
```

## Hosted Provider Run

```bash
export DEEPSEEK_API_KEY="..."
python -m founderbench.resumable_runner \
  --policy deepseek \
  --output outputs/founderbench-deepseek.json \
  --resume \
  --audit
```

Audit mode records prompt hashes, redacted responses, token usage when available, estimated cost, latency, and parser/provider error categories. Inspect audit logs before sharing.

## Repeated Runs

Run separate seeds, then bundle them:

```bash
python -m founderbench.resumable_runner --policy deepseek --output outputs/deepseek-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy deepseek --output outputs/deepseek-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy deepseek --output outputs/deepseek-seed2.json --resume --seed 2

python -m founderbench.submission_bundle \
  --input outputs/deepseek-seed0.json \
  --input outputs/deepseek-seed1.json \
  --input outputs/deepseek-seed2.json \
  --output outputs/deepseek-repeats.json \
  --report outputs/deepseek-repeats-report.md
```

## Local/Open-Source Model

Serve the model behind an OpenAI-compatible chat-completions endpoint:

```bash
export OPENAI_COMPAT_BASE_URL="http://localhost:8000/v1"
export OPENAI_COMPAT_MODEL="Qwen/Qwen2.5-7B-Instruct"
python -m founderbench.local_model health --output outputs/local-health.json
python -m founderbench.resumable_runner --policy llm --output outputs/local-open-model.json --resume --audit
```

Named OpenAI-compatible hosted policies are also available for broader model-family coverage:

```bash
export KIMI_API_KEY="..."
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi.json --resume --audit

export QWEN_API_KEY="..."
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen.json --resume --audit
```

FounderBench also defines `openai`, `mistral`, `glm`, `xai`, and `llama` policies. Each uses provider-specific `*_API_KEY`, `*_MODEL`, and when needed `*_BASE_URL` variables; see `.env.example` and `outputs/founderbench-provider-readiness.md`.

