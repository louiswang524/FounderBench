# FounderBench

FounderBench is a benchmark for evaluating whether LLM agents can operate startup-like companies under bounded resources. It places each agent in deterministic startup episodes where the agent must choose structured business actions, and the simulator scores the resulting revenue, customers, cash, reputation, risk, and survival.

The benchmark is designed for the research question:

```text
Can an LLM agent make repeated business decisions that improve startup outcomes under limited funding, noisy market signals, operational constraints, and risk penalties?
```

## Current Version

FounderBench includes:

- 50 fixed startup tasks
- 10 task families
- 13 structured business actions
- deterministic seeded simulator
- fixed 8-market simulator catalog
- public development and public test splits
- non-LLM baseline policies
- hosted-provider adapters for OpenAI, DeepSeek, Anthropic, Gemini, Kimi/Moonshot, Qwen/Alibaba, Mistral, GLM/Z.ai, xAI, Llama/open-weight endpoints, and generic OpenAI-compatible local servers
- canonical prompt protocol and prompt/protocol hashes for provider comparability
- resumable provider runner
- redacted audit mode for provider-call provenance
- deterministic replay audit
- expert/human-founder calibration protocol
- leaderboard, manifest, and analysis generators

## Task Families

| Tasks | Family |
|---|---|
| FND-001..FND-005 | Market selection |
| FND-006..FND-010 | First revenue |
| FND-011..FND-015 | Retention improvement |
| FND-016..FND-020 | Churn shock recovery |
| FND-021..FND-025 | Demo Day traction |
| FND-026..FND-030 | Pricing |
| FND-031..FND-035 | Runway preservation |
| FND-036..FND-040 | Pivot decision |
| FND-041..FND-045 | Fundraising |
| FND-046..FND-050 | Channel expansion |

## Action Space

Agents return structured actions only:

- `research_market`
- `build_offer`
- `run_campaign`
- `improve_offer`
- `hire_agent`
- `support_customers`
- `change_price`
- `interview_customers`
- `cut_cost`
- `pivot_market`
- `raise_funding`
- `partner_channel`
- `do_nothing`

Natural-language claims do not directly affect the simulator. This is intentional: the benchmark evaluates executed business decisions rather than persuasive explanations.

## Quick Start

```powershell
cd work\founderbench
python -m unittest discover -s tests -v
python -m founderbench.export_tasks --output ..\..\outputs\founderbench-task-manifest.json
python -m founderbench.task_coverage --json-output ..\..\outputs\founderbench-task-coverage.json --markdown-output ..\..\outputs\founderbench-task-coverage.md
python -m founderbench.task_provenance --json-output ..\..\outputs\founderbench-task-provenance.json --markdown-output ..\..\outputs\founderbench-task-provenance.md
python -m founderbench.task_cards --json-output ..\..\outputs\founderbench-task-cards.json --markdown-output ..\..\outputs\founderbench-task-cards.md
python -m founderbench.action_semantics --json-output ..\..\outputs\founderbench-action-semantics.json --markdown-output ..\..\outputs\founderbench-action-semantics.md
python -m founderbench.market_catalog --json-output ..\..\outputs\founderbench-market-catalog.json --markdown-output ..\..\outputs\founderbench-market-catalog.md
python -m founderbench.responsible_use --json-output ..\..\outputs\founderbench-responsible-use.json --markdown-output ..\..\outputs\founderbench-responsible-use.md
python -m founderbench.leaderboard --output ..\..\outputs\founderbench-baseline-leaderboard.json --raw-output ..\..\outputs\founderbench-baseline-raw.json
python -m founderbench.leaderboard_stability --json-output ..\..\outputs\founderbench-leaderboard-stability.json --markdown-output ..\..\outputs\founderbench-leaderboard-stability.md
python -m founderbench.analysis --raw ..\..\outputs\founderbench-baseline-raw.json --output ..\..\outputs\founderbench-baseline-analysis.md
python -m founderbench.paper_tables --json-output ..\..\outputs\founderbench-paper-tables.json --markdown-output ..\..\outputs\founderbench-paper-tables.md
python -m founderbench.paper_figures --json-output ..\..\outputs\founderbench-paper-figure-data.json --markdown-output ..\..\outputs\founderbench-paper-figure-data.md
python -m founderbench.model_comparison --json-output ..\..\outputs\founderbench-model-comparison.json --markdown-output ..\..\outputs\founderbench-model-comparison.md
python -m founderbench.result_integrity_audit --json-output ..\..\outputs\founderbench-result-integrity-audit.json --markdown-output ..\..\outputs\founderbench-result-integrity-audit.md
python -m founderbench.ablation --raw ..\..\outputs\founderbench-baseline-raw.json --output ..\..\outputs\founderbench-ablation-report.md
python -m founderbench.action_ablation --json-output ..\..\outputs\founderbench-action-ablation.json --markdown-output ..\..\outputs\founderbench-action-ablation.md
python -m founderbench.paired_statistics --json-output ..\..\outputs\founderbench-paired-statistics.json --markdown-output ..\..\outputs\founderbench-paired-statistics.md
python -m founderbench.power_analysis --json-output ..\..\outputs\founderbench-power-analysis.json --markdown-output ..\..\outputs\founderbench-power-analysis.md
python -m founderbench.difficulty_calibration --json-output ..\..\outputs\founderbench-difficulty-calibration.json --markdown-output ..\..\outputs\founderbench-difficulty-calibration.md
python -m founderbench.qualitative --raw ..\..\outputs\founderbench-baseline-raw.json --json-output ..\..\outputs\founderbench-qualitative-traces.json --markdown-output ..\..\outputs\founderbench-qualitative-traces.md
python -m founderbench.repeats --policy random --seeds 0,1,2,3,4 --json-output ..\..\outputs\founderbench-random-repeats.json --markdown-output ..\..\outputs\founderbench-random-repeats.md
python -m founderbench.score_rubric --json-output ..\..\outputs\founderbench-score-rubric.json --markdown-output ..\..\outputs\founderbench-score-rubric.md
python -m founderbench.scoring_consistency_audit --json-output ..\..\outputs\founderbench-scoring-consistency-audit.json --markdown-output ..\..\outputs\founderbench-scoring-consistency-audit.md
python -m founderbench.metric_sensitivity --json-output ..\..\outputs\founderbench-metric-sensitivity.json --markdown-output ..\..\outputs\founderbench-metric-sensitivity.md
python -m founderbench.statistical_protocol --json-output ..\..\outputs\founderbench-statistical-protocol.json --markdown-output ..\..\outputs\founderbench-statistical-protocol.md
python -m founderbench.reviewer_smoke --json-output ..\..\outputs\founderbench-reviewer-smoke.json --markdown-output ..\..\outputs\founderbench-reviewer-smoke.md
python -m founderbench.local_model protocol --output ..\..\outputs\founderbench-local-openai-compatible-protocol.md
python -m founderbench.prompt_protocol --json-output ..\..\outputs\founderbench-prompt-protocol.json --markdown-output ..\..\outputs\founderbench-prompt-protocol.md
python -m founderbench.provider_readiness --json-output ..\..\outputs\founderbench-provider-readiness.json --markdown-output ..\..\outputs\founderbench-provider-readiness.md
python -m founderbench.cost_accounting --json-output ..\..\outputs\founderbench-cost-accounting.json --markdown-output ..\..\outputs\founderbench-cost-accounting.md
python -m founderbench.baseline_execution_plan --json-output ..\..\outputs\founderbench-baseline-execution-plan.json --markdown-output ..\..\outputs\founderbench-baseline-execution-plan.md
python -m founderbench.provider_run_status --json-output ..\..\outputs\founderbench-provider-run-status.json --markdown-output ..\..\outputs\founderbench-provider-run-status.md
python -m founderbench.license_readiness --json-output ..\..\outputs\founderbench-license-readiness.json --markdown-output ..\..\outputs\founderbench-license-readiness.md
python -m founderbench.release_metadata --json-output ..\..\outputs\founderbench-release-metadata-checklist.json --markdown-output ..\..\outputs\founderbench-release-metadata-checklist.md
python -m founderbench.holdout protocol --output ..\..\outputs\founderbench-private-holdout-evaluator-protocol.md
python -m founderbench.human_calibration --json-output ..\..\outputs\founderbench-human-calibration-protocol.json --markdown-output ..\..\outputs\founderbench-human-calibration-protocol.md
python -m founderbench.human_calibration_schema --json-output ..\..\outputs\founderbench-human-calibration-schema.json --markdown-output ..\..\outputs\founderbench-human-calibration-schema.md --template-output ..\..\outputs\founderbench-human-calibration-template.json
python -m founderbench.references --bibtex-output ..\..\outputs\founderbench-references.bib --provenance-output ..\..\outputs\founderbench-reference-provenance.json
python -m founderbench.submission --input ..\..\outputs\founderbench-baseline-raw.json --report ..\..\outputs\founderbench-submission-validation.md
python -m founderbench.submission_schema --json-output ..\..\outputs\founderbench-model-submission-schema.json --markdown-output ..\..\outputs\founderbench-model-submission-schema.md
python -m founderbench.submission_bundle --input ..\..\outputs\founderbench-deepseek-seed0.json --input ..\..\outputs\founderbench-deepseek-seed1.json --input ..\..\outputs\founderbench-deepseek-seed2.json --output ..\..\outputs\founderbench-deepseek-repeats.json --report ..\..\outputs\founderbench-deepseek-repeats-submission-report.md
python -m founderbench.experiment_matrix --json-output ..\..\outputs\founderbench-experiment-matrix.json --markdown-output ..\..\outputs\founderbench-experiment-matrix.md
python -m founderbench.reproducibility_manifest --json-output ..\..\outputs\founderbench-reproducibility-manifest.json --markdown-output ..\..\outputs\founderbench-reproducibility-manifest.md
python -m founderbench.environment_report --json-output ..\..\outputs\founderbench-environment-report.json --markdown-output ..\..\outputs\founderbench-environment-report.md
python -m founderbench.determinism_audit --json-output ..\..\outputs\founderbench-determinism-audit.json --markdown-output ..\..\outputs\founderbench-determinism-audit.md
python -m founderbench.validity_report --json-output ..\..\outputs\founderbench-validity-report.json --markdown-output ..\..\outputs\founderbench-validity-report.md
python -m founderbench.claim_evidence --json-output ..\..\outputs\founderbench-claim-evidence.json --markdown-output ..\..\outputs\founderbench-claim-evidence.md
python -m founderbench.submission_gate --json-output ..\..\outputs\founderbench-submission-gate.json --markdown-output ..\..\outputs\founderbench-submission-gate.md
python -m founderbench.reviewer_index --json-output ..\..\outputs\founderbench-reviewer-index.json --markdown-output ..\..\outputs\founderbench-reviewer-index.md
python -m founderbench.publication_audit --json-output ..\..\outputs\founderbench-publication-audit.json --markdown-output ..\..\outputs\founderbench-publication-audit.md
```

If `python` is not on PATH, use the bundled Codex runtime:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

## Hosted Provider Runs

Use the resumable runner for long hosted-model runs:

```powershell
$env:DEEPSEEK_API_KEY = "<key>"
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek.json --resume
```

Use audit mode to save redacted provider-call records:

```powershell
$env:MODEL_INPUT_COST_PER_MILLION = "0.00"
$env:MODEL_OUTPUT_COST_PER_MILLION = "0.00"
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek-audit.json --resume --audit
```

Audit logs include prompt hashes, redacted model responses, token usage when provided by the API, estimated provider cost, and latency. Inspect audit logs manually before sharing them.

Provider cost estimates use token usage returned by provider APIs plus evaluator-configured `MODEL_INPUT_COST_PER_MILLION` and `MODEL_OUTPUT_COST_PER_MILLION` assumptions. The accounting protocol is generated at `outputs/founderbench-cost-accounting.md`.

The prompt contract used by hosted and local provider policies is documented in `outputs/founderbench-prompt-protocol.md`. It fixes the action vocabulary, response schema, weekly action cap, provider message wrappers, and SHA-256 hashes needed to compare provider runs.

For a local/open-source baseline, serve the model through an OpenAI-compatible endpoint and use the `llm` policy:

```powershell
$env:FOUNDERBENCH_COMPAT_BASE_URL = "http://localhost:8000/v1"
$env:FOUNDERBENCH_COMPAT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
python -m founderbench.local_model health --output ..\..\outputs\local-health.json
python -m founderbench.resumable_runner --policy llm --output ..\..\outputs\founderbench-local-open-model.json --resume --audit
```

`FOUNDERBENCH_COMPAT_BASE_URL` should be the OpenAI-compatible `/v1` root. The benchmark posts model decisions to `${FOUNDERBENCH_COMPAT_BASE_URL}/chat/completions`; `local_model health` checks `${FOUNDERBENCH_COMPAT_BASE_URL}/models`.

Validate provider submissions before reporting them:

```powershell
python -m founderbench.submission --input ..\..\outputs\provider-run.json --report ..\..\outputs\provider-run-submission-report.md
```

The resumable runner writes the same aggregate diagnostics, split summaries, and task coverage expected by the submission validator, so completed hosted/local runs should not require manual reshaping.

For repeated-sampling reports, run the same policy into separate output files with different `--seed` values, then submit a JSON object with a top-level `runs` array. The `--seed` value is recorded as `run_seed` and acts as a repeat index for hosted providers:

```powershell
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek-seed0.json --resume --seed 0
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek-seed1.json --resume --seed 1
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek-seed2.json --resume --seed 2
```

Combine the seed files into one validated repeated-run bundle:

```powershell
python -m founderbench.submission_bundle --input ..\..\outputs\founderbench-deepseek-seed0.json --input ..\..\outputs\founderbench-deepseek-seed1.json --input ..\..\outputs\founderbench-deepseek-seed2.json --output ..\..\outputs\founderbench-deepseek-repeats.json --report ..\..\outputs\founderbench-deepseek-repeats-submission-report.md
```

The model submission schema is documented in `outputs/founderbench-model-submission-schema.md`, and the repeated-run bundle protocol is documented in `outputs/founderbench-submission-bundle-protocol.md`. The schema describes accepted payload shapes and required fields; the validator checks all 50 task ids, public split coverage, task-level scores, aggregate diagnostics, and provider-error category accounting. The bundle helper also rejects duplicate policy/`run_seed` identities.

## Private Holdout Evaluator

The private holdout protocol is executable on an evaluator-controlled host. It requires an evaluator-held secret and emits aggregate private report fields by default:

```powershell
$env:FounderBench_HOLDOUT_SECRET = "<private-secret>"
python -m founderbench.holdout fingerprints --output private-holdout-fingerprints.json
python -m founderbench.private_holdout_evaluator --policy deepseek --output private-deepseek-report.json
```

Do not publish evaluator-held secrets, hidden task definitions, hidden seeds, or raw private traces before the evaluation cycle closes.

## Baselines

Built-in non-LLM policies:

- `random`
- `conservative`
- `heuristic`
- `task_heuristic`

Provider policies:

- `deepseek`
- `anthropic`
- `gemini`
- `openai` for OpenAI/GPT models
- `deepseek` for the DeepSeek hosted baseline
- `anthropic` for Claude
- `gemini` for Gemini
- `kimi` for Moonshot/Kimi OpenAI-compatible endpoints
- `qwen` for Alibaba/Qwen OpenAI-compatible endpoints
- `mistral`, `glm`, `xai`, and `llama` for optional broader provider/open-weight coverage
- `llm` for generic OpenAI-compatible local/open-source endpoints

## Outputs

Important generated artifacts live under `outputs/`:

- `founderbench-task-manifest.json`
- `founderbench-task-coverage.json`
- `founderbench-task-coverage.md`
- `founderbench-task-provenance.json`
- `founderbench-task-provenance.md`
- `founderbench-task-cards.json`
- `founderbench-task-cards.md`
- `founderbench-action-semantics.json`
- `founderbench-action-semantics.md`
- `founderbench-market-catalog.json`
- `founderbench-market-catalog.md`
- `founderbench-responsible-use.json`
- `founderbench-responsible-use.md`
- `founderbench-baseline-leaderboard.json`
- `founderbench-leaderboard-stability.json`
- `founderbench-leaderboard-stability.md`
- `founderbench-baseline-raw.json`
- `founderbench-baseline-analysis.md`
- `founderbench-paper-tables.json`
- `founderbench-paper-tables.md`
- `founderbench-paper-figure-data.json`
- `founderbench-paper-figure-data.md`
- `founderbench-model-comparison.json`
- `founderbench-model-comparison.md`
- `founderbench-result-integrity-audit.json`
- `founderbench-result-integrity-audit.md`
- `founderbench-ablation-report.md`
- `founderbench-action-ablation.json`
- `founderbench-action-ablation.md`
- `founderbench-paired-statistics.json`
- `founderbench-paired-statistics.md`
- `founderbench-power-analysis.json`
- `founderbench-power-analysis.md`
- `founderbench-difficulty-calibration.json`
- `founderbench-difficulty-calibration.md`
- `founderbench-qualitative-traces.json`
- `founderbench-qualitative-traces.md`
- `founderbench-random-repeats.json`
- `founderbench-random-repeats.md`
- `founderbench-score-rubric.json`
- `founderbench-score-rubric.md`
- `founderbench-scoring-consistency-audit.json`
- `founderbench-scoring-consistency-audit.md`
- `founderbench-metric-sensitivity.json`
- `founderbench-metric-sensitivity.md`
- `founderbench-statistical-protocol.json`
- `founderbench-statistical-protocol.md`
- `founderbench-local-openai-compatible-protocol.json`
- `founderbench-local-openai-compatible-protocol.md`
- `founderbench-prompt-protocol.json`
- `founderbench-prompt-protocol.md`
- `founderbench-provider-readiness.json`
- `founderbench-provider-readiness.md`
- `founderbench-cost-accounting.json`
- `founderbench-cost-accounting.md`
- `founderbench-baseline-execution-plan.json`
- `founderbench-baseline-execution-plan.md`
- `founderbench-provider-run-status.json`
- `founderbench-provider-run-status.md`
- `founderbench-license-readiness.json`
- `founderbench-license-readiness.md`
- `founderbench-release-metadata-checklist.json`
- `founderbench-release-metadata-checklist.md`
- `founderbench-private-holdout-evaluator-protocol.json`
- `founderbench-private-holdout-evaluator-protocol.md`
- `founderbench-human-calibration-protocol.json`
- `founderbench-human-calibration-protocol.md`
- `founderbench-human-calibration-schema.json`
- `founderbench-human-calibration-schema.md`
- `founderbench-human-calibration-template.json`
- `founderbench-references.bib`
- `founderbench-reference-provenance.json`
- `founderbench-reproducibility-manifest.json`
- `founderbench-reproducibility-manifest.md`
- `founderbench-environment-report.json`
- `founderbench-environment-report.md`
- `founderbench-determinism-audit.json`
- `founderbench-determinism-audit.md`
- `founderbench-validity-report.json`
- `founderbench-validity-report.md`
- `founderbench-claim-evidence.json`
- `founderbench-claim-evidence.md`
- `founderbench-submission-gate.json`
- `founderbench-submission-gate.md`
- `founderbench-experiment-matrix.json`
- `founderbench-experiment-matrix.md`
- `founderbench-reviewer-index.json`
- `founderbench-reviewer-index.md`
- `founderbench-publication-audit.json`
- `founderbench-publication-audit.md`
- `founderbench-benchmark-card.md`
- `founderbench-metrics-and-evaluation.md`
- `founderbench-reproduction-guide.md`
- `founderbench-reviewer-smoke.json`
- `founderbench-reviewer-smoke.md`
- `founderbench-model-submission-template.md`
- `founderbench-model-submission-schema.json`
- `founderbench-model-submission-schema.md`
- `founderbench-submission-bundle-protocol.json`
- `founderbench-submission-bundle-protocol.md`
- `founderbench-submission-validation.md`

## Non-Goals

FounderBench is not a real-money trading system, a legal recommendation engine, or a blueprint for deploying unsupervised autonomous companies. It is a controlled evaluation environment for studying startup-relevant agent decision-making.
