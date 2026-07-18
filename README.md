# FounderBench

FounderBench is a controlled benchmark for evaluating whether LLM agents can operate startup-like companies under bounded resources. Each model is placed into fixed startup scenarios, receives simulator observations, chooses structured business actions, and is scored on bounded 0-100 task outcomes such as revenue, customers, runway, reputation, risk, and survival.

The benchmark asks:

```text
Can an LLM agent make repeated business decisions that improve startup outcomes under limited funding,
noisy market signals, operational constraints, and explicit risk penalties?
```

## What Is Included

- 50 fixed public startup tasks: `FND-001` through `FND-050`
- 10 task families across market selection, revenue, retention, churn recovery, pricing, runway, pivoting, fundraising, and channel expansion
- 13 structured business actions
- deterministic seeded simulator
- public development and public test splits
- deterministic baseline policies
- hosted-provider adapters for DeepSeek, Anthropic, Gemini, and OpenAI-compatible local/open-source endpoints
- submission validator, repeated-run bundler, audit reports, benchmark card, datasheet, and paper draft
- private-holdout blueprint and evaluator protocol

The Python package is still named `moneybench` internally for compatibility, but the benchmark and public task IDs are FounderBench.

## Repository Layout

```text
.
├── work/moneybench/          # Source package, tests, benchmark spec
│   ├── moneybench/           # Simulator, tasks, provider adapters, validators
│   └── tests/                # Unit and artifact validation tests
├── outputs/                  # Generated v0.3.0 benchmark artifacts
├── release/                  # Supplementary release bundle with checksums
├── docs/                     # GitHub-facing usage guides
├── .env.example              # Provider environment variable template
└── pyproject.toml            # Editable install metadata
```

## Quick Start

```bash
git clone https://github.com/louiswang524/FounderBench.git
cd <repo>
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .
python -m unittest discover -s work/moneybench/tests -v
python -m moneybench.release validate
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m unittest discover -s work\moneybench\tests -v
python -m moneybench.release validate
```

## Run a Built-In Baseline

Run one public task:

```bash
python -m moneybench.task_cli --policy task_heuristic --task FND-001 --trace
```

Run all 50 tasks for a deterministic baseline:

```bash
python -m moneybench.task_cli --policy heuristic
```

Regenerate all core artifacts:

```bash
python -m moneybench.release regenerate
python -m moneybench.release validate
python -m moneybench.release bundle
```

## Run an LLM Provider

Set the relevant API key as an environment variable. Do not put keys in code or committed files.

```bash
export DEEPSEEK_API_KEY="..."
python -m moneybench.resumable_runner \
  --policy deepseek \
  --output outputs/acceleratorbench-deepseek-v0.3.json \
  --resume \
  --audit
python -m moneybench.submission \
  --input outputs/acceleratorbench-deepseek-v0.3.json \
  --report outputs/acceleratorbench-deepseek-v0.3-submission-report.md
```

Supported provider policies:

- `deepseek`
- `deepseek_sc` for DeepSeek self-consistency with `SC_K=3` by default
- `anthropic`
- `gemini`
- `llm` for OpenAI-compatible local/open-source endpoints

For local/open-source models:

```bash
export OPENAI_COMPAT_BASE_URL="http://localhost:8000/v1"
export OPENAI_COMPAT_MODEL="Qwen/Qwen2.5-7B-Instruct"
python -m moneybench.local_model health --output outputs/local-health.json
python -m moneybench.resumable_runner --policy llm --output outputs/local-open-model.json --resume --audit
```

## Submission Format

A valid model submission must cover all 50 public task IDs, include task-level scores and diagnostics, and pass:

```bash
python -m moneybench.submission --input outputs/provider-run.json --report outputs/provider-run-report.md
```

See [docs/SUBMISSIONS.md](docs/SUBMISSIONS.md) and [outputs/acceleratorbench-model-submission-schema-v0.3.md](outputs/acceleratorbench-model-submission-schema-v0.3.md).

## Important Artifacts

- Task manifest: [outputs/acceleratorbench-task-manifest-v0.3.json](outputs/acceleratorbench-task-manifest-v0.3.json)
- Benchmark card: [outputs/acceleratorbench-benchmark-card.md](outputs/acceleratorbench-benchmark-card.md)
- Metrics and evaluation: [outputs/acceleratorbench-metrics-and-evaluation.md](outputs/acceleratorbench-metrics-and-evaluation.md)
- Prompt protocol: [outputs/acceleratorbench-prompt-protocol-v0.3.md](outputs/acceleratorbench-prompt-protocol-v0.3.md)
- Model submission schema: [outputs/acceleratorbench-model-submission-schema-v0.3.md](outputs/acceleratorbench-model-submission-schema-v0.3.md)
- Paper draft: [outputs/acceleratorbench-paper-draft-v0.1.md](outputs/acceleratorbench-paper-draft-v0.1.md)
- Reviewer index: [outputs/acceleratorbench-reviewer-index-v0.3.md](outputs/acceleratorbench-reviewer-index-v0.3.md)

## Reporting Guardrails

FounderBench is a synthetic controlled simulator. Do not claim that a score proves a model can run a real company, predict startup success, or make real investment decisions. Public-test tasks are visible and released; only evaluator-controlled private holdout runs should be described as hidden or private.

## License And Citation

A final open-source license has not been selected yet. Before publishing the GitHub repository publicly, choose a license and replace the placeholder citation metadata in [work/moneybench/CITATION.cff](work/moneybench/CITATION.cff).

