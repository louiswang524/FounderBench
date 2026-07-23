# FounderBench

**Evaluating LLM Agents on Sequential Startup Decisions**

[![CI](https://github.com/louiswang524/FounderBench/actions/workflows/ci.yml/badge.svg)](https://github.com/louiswang524/FounderBench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

FounderBench is a **controlled benchmark** for testing whether LLM agents can make **repeated, consequential startup-like decisions** under scarce resources and delayed feedback.

Each episode gives the agent a structured company observation and a fixed action vocabulary. The agent returns JSON actions; a **deterministic simulator** updates cash, customers, quality, reputation, and risk; a **task-specific scorer** maps the final state to a **0–100 outcome**. Free-form rationale is logged for audit but **never scored**.

> **Research question:** Can an LLM agent turn noisy observations into sequenced business actions that improve simulated startup outcomes under limited funding and operational constraints?

This is a synthetic test bed—not evidence that a model can run a real company.

## Headline results (public suite, single hosted runs)

| Policy / model | Mean score | Solved (≥70) |
|---|---:|---:|
| Task-aware heuristic (calibration ceiling) | **80.90** | **37/50** |
| Best hosted single run (Gemini 3.5 Flash) | **67.69** | 32/50 |
| Generic heuristic | 61.01 | — |
| Random | 33.30 | 4/50 |

Average-score and solved-count rankings can disagree. Family profiles show different failure modes (e.g., pivots / Demo Day vs retention). There is **no human-founder baseline** in the current release. Hosted rows are **one run per configuration** on **visible public tasks**.

Paper draft / KDD materials live under [`paper/kdd2027/`](paper/kdd2027/) and [`outputs/founderbench-paper-draft.md`](outputs/founderbench-paper-draft.md).

## Why FounderBench?

| Nearby benchmarks | Typical focus | FounderBench difference |
|---|---|---|
| SWE-bench / Terminal-Bench | Code / CLI execution | Business operating decisions |
| WebArena / WorkArena | Browser / enterprise UI | Structured JSON actions + family scorers |
| YC-Bench / CEO-Bench | Long-horizon cash games | Short family-labeled episodes (≤10 weeks) + 0–100 outcome rubrics |

Design desiderata: **executable outcomes**, **family diagnosis**, **shared interface**, **replayability**, and **contamination awareness** (frozen private holdout fingerprints; private task text not published).

## What's included

- **50** public tasks (`FND-001` … `FND-050`), **5** per family across **10** families  
- **13** structured business actions  
- Deterministic seeded simulator + fixed 8-market catalog  
- Public splits: `public_dev` (FND-001–030) and `public_test` (FND-031–050) — both **visible**  
- Deterministic baselines: `random`, `conservative`, `heuristic`, `task_heuristic`  
- Hosted-provider adapters (OpenAI, DeepSeek, Anthropic, Gemini, Kimi, Qwen, Mistral, GLM, xAI, Llama, OpenAI-compatible local endpoints)  
- Submission validator, audit mode, datasheet, benchmark card, analysis generators  
- Private-holdout **blueprint + public fingerprints** (evaluator secret stays private)

## Repository layout

```text
.
├── work/founderbench/     # Python package + tests + SPEC
│   ├── founderbench/      # Simulator, tasks, adapters, validators
│   └── tests/
├── outputs/               # Generated artifacts (manifests, leaderboards, reports)
├── release/               # Supplementary release bundle + checksums
├── paper/kdd2027/         # ACM manuscript, figures, tables
├── docs/                  # Quickstart, submissions, release notes
├── pyproject.toml         # Editable install
├── CITATION.cff
└── LICENSE                # MIT
```

## Install

```bash
git clone https://github.com/louiswang524/FounderBench.git
cd FounderBench
python3 -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\Activate.ps1
python -m pip install -e .
```

Validate:

```bash
python -m unittest discover -s work/founderbench/tests -v
python -m founderbench.release validate
```

More detail: [`docs/QUICKSTART.md`](docs/QUICKSTART.md).

## Quick start: deterministic baselines (no API keys)

Single task with a trace:

```bash
python -m founderbench.task_cli --policy task_heuristic --task FND-001 --trace
```

All 50 tasks with the generic heuristic:

```bash
python -m founderbench.task_cli --policy heuristic
```

Regenerate core artifacts:

```bash
python -m founderbench.release regenerate
python -m founderbench.release validate
python -m founderbench.release bundle
```

### Calibration policies

| Policy ID | Meaning |
|---|---|
| `random` | Sample legal actions |
| `conservative` | Prefer research/support, low spend |
| `heuristic` | Generic research → build → improve/support (no family ID) |
| `task_heuristic` | Family-conditioned playbook (uses task ID → family). **Calibration ceiling**, not a human founder |

Hosted LLM prompts do **not** receive an explicit family label unless the task card leaks cues. Treat `task_heuristic` as a synthetic reference point.

## Run a hosted LLM

Copy [`.env.example`](.env.example), set provider keys (never commit `.env`), then:

```bash
export DEEPSEEK_API_KEY="..."
python -m founderbench.resumable_runner \
  --policy deepseek \
  --output outputs/founderbench-deepseek.json \
  --resume \
  --audit

python -m founderbench.submission \
  --input outputs/founderbench-deepseek.json \
  --report outputs/founderbench-deepseek-submission-report.md
```

Common `--policy` values: `openai`, `deepseek`, `anthropic`, `gemini`, `kimi`, `qwen`, `mistral`, `glm`, `xai`, `llama`, `llm` (OpenAI-compatible local).

Local / open-weight OpenAI-compatible servers:

```bash
export FOUNDERBENCH_COMPAT_BASE_URL="http://localhost:8000/v1"
export FOUNDERBENCH_COMPAT_MODEL="Qwen/Qwen2.5-7B-Instruct"
python -m founderbench.local_model health --output outputs/local-health.json
python -m founderbench.resumable_runner --policy llm --output outputs/local-open-model.json --resume --audit
```

See [`docs/SUBMISSIONS.md`](docs/SUBMISSIONS.md).

## Task families

| IDs | Family |
|---|---|
| FND-001–005 | Market selection |
| FND-006–010 | First revenue |
| FND-011–015 | Retention improvement |
| FND-016–020 | Churn shock recovery |
| FND-021–025 | Demo Day traction |
| FND-026–030 | Pricing |
| FND-031–035 | Runway preservation |
| FND-036–040 | Pivot decision |
| FND-041–045 | Fundraising |
| FND-046–050 | Channel expansion |

## Action space

Agents may only execute structured actions:

`research_market`, `build_offer`, `run_campaign`, `improve_offer`, `hire_agent`, `support_customers`, `change_price`, `interview_customers`, `cut_cost`, `pivot_market`, `raise_funding`, `partner_channel`, `do_nothing`

Natural-language claims do not change simulator state.

## Scoring

- Primary metric: **unweighted mean** of 50 task scores in \([0, 100]\)  
- A task is **solved** if score ≥ **70** (fixed operating threshold; average remains primary)  
- Provider/parser errors remain in official scores; diagnostics report error load separately  

Rubrics and protocol docs:

- [Task manifest](outputs/founderbench-task-manifest.json)  
- [Score rubric](outputs/founderbench-score-rubric.md) (if present) / metrics doc  
- [Benchmark card](outputs/founderbench-benchmark-card.md)  
- [Datasheet](outputs/founderbench-datasheet.md)  
- [Prompt protocol](outputs/founderbench-prompt-protocol.md)  
- [Metrics and evaluation](outputs/founderbench-metrics-and-evaluation.md)

## Private holdout

A **20-task private holdout** (2 per family) is frozen with public fingerprint commitments. Private task definitions and the evaluator secret are **not** in this repository. Hosted private-holdout leaderboards are not part of the current paper release.

Do not invent or publish private task contents.

## Responsible use

- Scores measure performance on a **synthetic** simulator.  
- Do **not** claim real-world company operation, investment advice, or founder equivalence.  
- `public_test` is a **reporting split**, not a hidden exam.  
- Prefer reporting mean, median/IQR, solved count, family profiles, and error diagnostics together.

## Citation

If you use FounderBench, please cite:

```bibtex
@software{wang2026founderbench,
  author       = {Wang, Yufeng},
  title        = {FounderBench: Evaluating LLM Agents on Sequential Startup Decisions},
  year         = {2026},
  version      = {0.3.0},
  url          = {https://github.com/louiswang524/FounderBench},
  license      = {MIT}
}
```

Also see [`CITATION.cff`](CITATION.cff). Paper draft: [`outputs/founderbench-paper-draft.md`](outputs/founderbench-paper-draft.md).

## License

MIT — see [`LICENSE`](LICENSE).

## Contributing / issues

Issues and PRs are welcome at [github.com/louiswang524/FounderBench](https://github.com/louiswang524/FounderBench). For release process notes, see [`docs/RELEASE.md`](docs/RELEASE.md).
