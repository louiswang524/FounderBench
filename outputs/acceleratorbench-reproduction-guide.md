# FounderBench Reproduction Guide

## Files

Core implementation:

- `work/moneybench/moneybench/env.py`
- `work/moneybench/moneybench/tasks.py`
- `work/moneybench/moneybench/task_runner.py`
- `work/moneybench/moneybench/task_cli.py`
- `work/moneybench/moneybench/leaderboard.py`
- `work/moneybench/moneybench/llm_policy.py`

Dataset artifact:

- `outputs/acceleratorbench-task-manifest-v0.3.json`

Baseline outputs:

- `outputs/acceleratorbench-baseline-leaderboard-v0.3.json`
- `outputs/acceleratorbench-baseline-raw-v0.3.json`

## Reviewer Smoke Check

For a fast first-pass artifact check, run:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.reviewer_smoke --json-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.md
```

This loads the 50-task suite, runs one deterministic task, and validates the included baseline raw output with the submission validator.

## Run Unit Tests

```powershell
cd C:\Users\louis\Documents\Codex\2026-07-14\use\work\moneybench
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -p "test_*.py"
```

## Export Task Manifest

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.export_tasks --output ..\..\outputs\acceleratorbench-task-manifest-v0.3.json
```

## Run Baseline Leaderboard

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.leaderboard --output ..\..\outputs\acceleratorbench-baseline-leaderboard-v0.3.json --raw-output ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json
```

## Run One Policy

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy task_heuristic
```

## Run One Task

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy task_heuristic --task FND-001
```

## Run Hosted Providers

DeepSeek:

```powershell
$env:DEEPSEEK_API_KEY = "<key>"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy deepseek
```

Anthropic:

```powershell
$env:ANTHROPIC_API_KEY = "<key>"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy anthropic
```

Gemini:

```powershell
$env:GEMINI_API_KEY = "<key>"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy gemini
```

Provider readiness can be checked without printing or storing secret values:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.provider_readiness --json-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.md
```

The readiness matrix records which environment variables are set or missing and lists the exact resumable/audit/validation commands for each provider.

## Resumable Provider Runs

Long hosted-provider evaluations should use the resumable runner:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3.json --resume
```

## Local/Open-Source Model Baseline

Local models should be served through an OpenAI-compatible `/v1/chat/completions` endpoint such as vLLM, LM Studio, Ollama OpenAI-compatible mode, or another compatible server.

```powershell
$env:OPENAI_COMPAT_BASE_URL = "http://localhost:8000/v1"
$env:OPENAI_COMPAT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.local_model health --output ..\..\outputs\local-health.json
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.resumable_runner --policy llm --output ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --resume --audit
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.submission --input ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --report ..\..\outputs\acceleratorbench-local-open-model-submission-report.md
```

The local/open-source protocol artifacts are:

- `outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.json`
- `outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.md`

## Redacted Audit Mode

Audit mode records redacted provider-call records inside task events. It includes prompt hashes, redacted raw responses, usage tokens when the provider returns them, estimated provider cost from configured prices, and call latency.

```powershell
$env:MODEL_INPUT_COST_PER_MILLION = "0.00"
$env:MODEL_OUTPUT_COST_PER_MILLION = "0.00"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.task_cli --policy deepseek --task FND-001 --audit
```

For resumable audit logs:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3-audit.json --resume --audit
```

Before sharing audit logs, inspect them manually. The benchmark redacts common API-key patterns, but submitters are responsible for ensuring no credentials or private data are released.

## Private Holdout Blueprint

The public blueprint describes the intended hidden evaluation protocol without revealing private task definitions:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.holdout blueprint --output ..\..\outputs\acceleratorbench-private-holdout-blueprint-v0.3.json
```

An evaluator can generate private task fingerprints from a secret:

```powershell
$env:FounderBench_HOLDOUT_SECRET = "<private-secret>"
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.holdout fingerprints --output private-holdout-fingerprints.json
```

Do not publish the private secret or hidden task definitions before the evaluation cycle closes.

The evaluator-facing protocol can be generated as Markdown or JSON:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.holdout protocol --output ..\..\outputs\acceleratorbench-private-holdout-evaluator-protocol-v0.3.md
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m moneybench.holdout protocol --output ..\..\outputs\acceleratorbench-private-holdout-evaluator-protocol-v0.3.json
```

The protocol specifies required evaluator inputs, pre-submission commitments, public report fields, and anti-gaming notes. It is a protocol artifact, not an executed private leaderboard.
