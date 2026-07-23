# FounderBench

**Evaluating LLM Agents on Sequential Startup Decisions**

[![CI](https://github.com/louiswang524/FounderBench/actions/workflows/ci.yml/badge.svg)](https://github.com/louiswang524/FounderBench/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

Code and evaluation harness for **FounderBench**: a controlled benchmark for whether LLM agents can make **repeated, consequential startup-like decisions** under scarce resources and delayed feedback.

Paper (manuscript / arXiv link will go here when posted) · [Analysis artifacts](outputs/) · [Quickstart](docs/QUICKSTART.md) · [Submissions](docs/SUBMISSIONS.md)

Each episode gives the agent a structured company observation and a fixed action vocabulary. The agent returns JSON actions; a **deterministic simulator** updates cash, customers, quality, reputation, and risk; a **task-specific scorer** maps the final state to a **0–100 outcome**. Free-form rationale is logged for audit but **never scored**.

> This is a synthetic test bed—not evidence that a model can run a real company.

## Public results (single hosted runs)

Primary metric: **unweighted mean** of 50 public task scores. A task is **solved** if score ≥ **70**. Hosted rows are **one run per configuration** on **visible** public tasks (`public_dev` + `public_test`). There is **no human-founder baseline** in this release.

### Leaderboard

| Policy / model | Avg score | 95% CI | Solved | Solve rate | Provider errors |
|---|---:|---|---:|---:|---:|
| Task-aware heuristic *(calibration ceiling)* | **80.90** | [74.94, 86.42] | **37/50** | 0.74 | 0 |
| Gemini 3.5 Flash | **67.69** | [59.20, 75.25] | 32/50 | 0.64 | 59 |
| Grok 4.5 | 66.53 | [57.81, 74.62] | **33/50** | 0.66 | 0 |
| GPT-5.6 Sol | 66.39 | [57.46, 74.89] | 32/50 | 0.64 | 0 |
| Kimi K3 | 65.63 | [57.89, 72.67] | 28/50 | 0.56 | 70 |
| Claude Sonnet 5 | 63.90 | [56.34, 71.41] | 25/50 | 0.50 | 0 |
| DeepSeek V4 Reasoner | 62.43 | [53.97, 70.48] | 27/50 | 0.54 | 3 |
| Claude Sonnet 4.5 | 61.09 | [52.24, 69.79] | 24/50 | 0.48 | 0 |
| Generic heuristic | 61.01 | [55.21, 66.94] | 19/50 | 0.38 | 0 |
| DeepSeek Chat | 56.59 | [47.39, 65.78] | 23/50 | 0.46 | 0 |
| GLM 4.5 Air | 54.78 | [46.01, 63.53] | 23/50 | 0.46 | 0 |
| Conservative | 54.04 | [48.20, 60.14] | 13/50 | 0.26 | 0 |
| Gemini 2.5 Flash | 52.69 | [46.10, 59.68] | 13/50 | 0.26 | 340 |
| Grok 4.3 | 52.59 | [45.16, 60.21] | 16/50 | 0.32 | 3 |
| Random | 33.30 | [26.89, 40.60] | 4/50 | 0.08 | 0 |

Bootstrap CIs reflect sensitivity to the 50-task mix, **not** repeated-run variance. Full tables: [`outputs/founderbench-model-comparison.md`](outputs/founderbench-model-comparison.md).

### What the numbers mean

| Finding | Detail |
|---|---|
| Hosted models sit below the calibration ceiling | Best hosted mean **67.69** vs task-aware heuristic **80.90** (paired gap ≈ **13** points, permutation *p* &lt; 0.001). |
| Average vs solved can disagree | Gemini 3.5 Flash leads on **mean**; Grok 4.5 leads on **solved** (33 vs 32). Thresholding at 70 and averaging are different lenses. |
| Hard families for hosted models | **Pivot decision** and often **Demo Day / channel / first revenue** stay weak; **retention / runway / fundraising** are comparatively strong. |
| Task-aware still leads most families | Hosted models only beat the task-aware playbook on a few families (e.g. retention, churn for top models). See family matrix below. |
| Provider errors are part of the official score | Errors are **not** dropped from means; diagnostics split affected vs unaffected tasks in the analysis report. |

### Family snapshot (solved/5 · mean)

Compact view for the calibration ceiling and top hosted cluster:

| Family | Task-aware | Gemini 3.5 Flash | Grok 4.5 | GPT-5.6 Sol |
|---|---|---|---|---|
| Market selection | 2/5 · 59.8 | 3/5 · 58.9 | 2/5 · 46.3 | 3/5 · 59.4 |
| First revenue | 2/5 · 69.2 | 3/5 · 54.8 | 3/5 · 60.0 | 2/5 · 53.6 |
| Retention improvement | 5/5 · 95.8 | 5/5 · 95.7 | 5/5 · 96.7 | 5/5 · 96.2 |
| Churn shock recovery | 5/5 · 91.2 | 5/5 · 91.6 | 5/5 · 94.4 | 5/5 · 95.2 |
| Demo Day traction | 4/5 · 88.8 | 0/5 · 61.3 | 3/5 · 67.5 | 1/5 · 51.6 |
| Pricing | 5/5 · 85.6 | 4/5 · 76.1 | 4/5 · 74.1 | 4/5 · 74.2 |
| Runway preservation | 5/5 · 95.6 | 5/5 · 84.0 | 4/5 · 81.4 | 5/5 · 87.2 |
| Pivot decision | 2/5 · 65.5 | 0/5 · 17.9 | 0/5 · 13.7 | 0/5 · 5.3 |
| Fundraising | 5/5 · 99.6 | 5/5 · 83.6 | 5/5 · 86.5 | 5/5 · 83.4 |
| Channel expansion | 2/5 · 58.0 | 2/5 · 53.0 | 2/5 · 44.7 | 2/5 · 57.8 |

Full family matrix for all policies: [`outputs/founderbench-model-comparison.md`](outputs/founderbench-model-comparison.md#family-breakdown). Deeper write-up: [`outputs/founderbench-paper-analysis.md`](outputs/founderbench-paper-analysis.md).

### Analysis artifacts

| File | Contents |
|---|---|
| [`outputs/founderbench-model-comparison.md`](outputs/founderbench-model-comparison.md) | Leaderboard, CIs, paired tests, family matrix |
| [`outputs/founderbench-paper-analysis.md`](outputs/founderbench-paper-analysis.md) | Frozen registry, error sensitivity, rank reversals |
| [`outputs/founderbench-model-result-cards.md`](outputs/founderbench-model-result-cards.md) | Per-model cards |
| [`outputs/founderbench-claim-evidence.md`](outputs/founderbench-claim-evidence.md) | Claim ↔ evidence map |
| `outputs/founderbench-*-submission-report.md` | Per-run submission validation reports |

## Why FounderBench?

| Nearby benchmarks | Typical focus | FounderBench difference |
|---|---|---|
| SWE-bench / Terminal-Bench | Code / CLI execution | Business operating decisions |
| WebArena / WorkArena | Browser / enterprise UI | Structured JSON actions + family scorers |
| YC-Bench / CEO-Bench | Long-horizon cash games | Short family-labeled episodes (≤10 weeks) + 0–100 outcome rubrics |

Design goals: **executable outcomes**, **family diagnosis**, **shared interface**, **replayability**, and **contamination awareness** (frozen private-holdout fingerprints; private task text not published).

## What's included

- **50** public tasks (`FND-001` … `FND-050`), **5** per family across **10** families
- **13** structured business actions
- Deterministic seeded simulator + fixed 8-market catalog
- Public splits: `public_dev` (FND-001–030) and `public_test` (FND-031–050) — both **visible**
- Deterministic baselines: `random`, `conservative`, `heuristic`, `task_heuristic`
- Hosted-provider adapters (OpenAI, DeepSeek, Anthropic, Gemini, Kimi, Qwen, Mistral, GLM, xAI, Llama, OpenAI-compatible local endpoints)
- Submission validator, audit mode, datasheet, benchmark card
- Private-holdout **blueprint + public fingerprints** (evaluator secret stays private)

## Repository layout

```text
.
├── work/founderbench/     # Python package + tests + SPEC
│   ├── founderbench/      # Simulator, tasks, adapters, validators
│   └── tests/
├── outputs/               # Leaderboards, manifests, run JSONs, analysis
├── release/               # Supplementary release bundle + checksums
├── docs/                  # Quickstart, submissions, release notes
├── pyproject.toml
├── CITATION.cff
└── LICENSE                # MIT
```

Manuscript sources are **not** kept in this repository (same pattern as SWE-bench, WebArena, Terminal-Bench, LiveCodeBench). Cite the paper/arXiv when available; reproduce numbers from `outputs/`.

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

```bash
python -m founderbench.task_cli --policy task_heuristic --task FND-001 --trace
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

Hosted LLM prompts do **not** receive an explicit family label unless the task card leaks cues.

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

`research_market`, `build_offer`, `run_campaign`, `improve_offer`, `hire_agent`, `support_customers`, `change_price`, `interview_customers`, `cut_cost`, `pivot_market`, `raise_funding`, `partner_channel`, `do_nothing`

Natural-language claims do not change simulator state.

## Scoring and protocol docs

- Primary metric: unweighted mean of 50 scores in \([0, 100]\)
- Solved if score ≥ **70** (operating threshold; average remains primary)
- Provider/parser errors remain in official scores

Further docs: [task manifest](outputs/founderbench-task-manifest.json) · [benchmark card](outputs/founderbench-benchmark-card.md) · [datasheet](outputs/founderbench-datasheet.md) · [prompt protocol](outputs/founderbench-prompt-protocol.md) · [metrics](outputs/founderbench-metrics-and-evaluation.md)

## Private holdout

A **20-task private holdout** (2 per family) is frozen with public fingerprint commitments. Private task definitions and the evaluator secret are **not** in this repository. Hosted private-holdout leaderboards are not part of the current public release.

## Responsible use

- Scores measure performance on a **synthetic** simulator.
- Do **not** claim real-world company operation, investment advice, or founder equivalence.
- `public_test` is a **reporting split**, not a hidden exam.
- Prefer reporting mean, CI, solved count, family profiles, and error diagnostics together.

## Citation

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

See also [`CITATION.cff`](CITATION.cff). Update this block with the arXiv / conference citation when the paper is public.

## License

MIT — see [`LICENSE`](LICENSE).

## Contributing

Issues and PRs welcome at [github.com/louiswang524/FounderBench](https://github.com/louiswang524/FounderBench). Release process: [`docs/RELEASE.md`](docs/RELEASE.md).
