# FounderBench

FounderBench is a benchmark for evaluating whether LLM agents can operate startup-like companies under bounded resources. It places each agent in deterministic startup episodes where the agent must choose structured business actions, and the simulator scores the resulting revenue, customers, cash, reputation, risk, and survival.

The benchmark is designed for the research question:

```text
Can an LLM agent make repeated business decisions that improve startup outcomes under limited funding, noisy market signals, operational constraints, and risk penalties?
```

## Current Version

FounderBench v0.3.0 includes:

- 50 fixed startup tasks
- 10 task families
- 13 structured business actions
- deterministic seeded simulator
- fixed 8-market simulator catalog
- public development and public test splits
- non-LLM baseline policies
- hosted-provider adapters for DeepSeek, Anthropic, Gemini, and OpenAI-compatible local servers
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
cd work\moneybench
python -m unittest discover -s tests -v
python -m moneybench.export_tasks --output ..\..\outputs\acceleratorbench-task-manifest-v0.3.json
python -m moneybench.task_coverage --json-output ..\..\outputs\acceleratorbench-task-coverage-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-task-coverage-v0.3.md
python -m moneybench.task_provenance --json-output ..\..\outputs\acceleratorbench-task-provenance-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-task-provenance-v0.3.md
python -m moneybench.task_cards --json-output ..\..\outputs\acceleratorbench-task-cards-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-task-cards-v0.3.md
python -m moneybench.action_semantics --json-output ..\..\outputs\acceleratorbench-action-semantics-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-action-semantics-v0.3.md
python -m moneybench.market_catalog --json-output ..\..\outputs\acceleratorbench-market-catalog-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-market-catalog-v0.3.md
python -m moneybench.responsible_use --json-output ..\..\outputs\acceleratorbench-responsible-use-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-responsible-use-v0.3.md
python -m moneybench.leaderboard --output ..\..\outputs\acceleratorbench-baseline-leaderboard-v0.3.json --raw-output ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json
python -m moneybench.leaderboard_stability --json-output ..\..\outputs\acceleratorbench-leaderboard-stability-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-leaderboard-stability-v0.3.md
python -m moneybench.analysis --raw ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json --output ..\..\outputs\acceleratorbench-baseline-analysis-v0.3.md
python -m moneybench.paper_tables --json-output ..\..\outputs\acceleratorbench-paper-tables-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-paper-tables-v0.3.md
python -m moneybench.paper_figures --json-output ..\..\outputs\acceleratorbench-paper-figure-data-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-paper-figure-data-v0.3.md
python -m moneybench.model_comparison --json-output ..\..\outputs\acceleratorbench-model-comparison-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-model-comparison-v0.3.md
python -m moneybench.result_integrity_audit --json-output ..\..\outputs\acceleratorbench-result-integrity-audit-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-result-integrity-audit-v0.3.md
python -m moneybench.ablation --raw ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json --output ..\..\outputs\acceleratorbench-ablation-report-v0.3.md
python -m moneybench.action_ablation --json-output ..\..\outputs\acceleratorbench-action-ablation-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-action-ablation-v0.3.md
python -m moneybench.paired_statistics --json-output ..\..\outputs\acceleratorbench-paired-statistics-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-paired-statistics-v0.3.md
python -m moneybench.power_analysis --json-output ..\..\outputs\acceleratorbench-power-analysis-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-power-analysis-v0.3.md
python -m moneybench.difficulty_calibration --json-output ..\..\outputs\acceleratorbench-difficulty-calibration-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-difficulty-calibration-v0.3.md
python -m moneybench.qualitative --raw ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json --json-output ..\..\outputs\acceleratorbench-qualitative-traces-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-qualitative-traces-v0.3.md
python -m moneybench.repeats --policy random --seeds 0,1,2,3,4 --json-output ..\..\outputs\acceleratorbench-random-repeats-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-random-repeats-v0.3.md
python -m moneybench.score_rubric --json-output ..\..\outputs\acceleratorbench-score-rubric-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-score-rubric-v0.3.md
python -m moneybench.scoring_consistency_audit --json-output ..\..\outputs\acceleratorbench-scoring-consistency-audit-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-scoring-consistency-audit-v0.3.md
python -m moneybench.metric_sensitivity --json-output ..\..\outputs\acceleratorbench-metric-sensitivity-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-metric-sensitivity-v0.3.md
python -m moneybench.statistical_protocol --json-output ..\..\outputs\acceleratorbench-statistical-protocol-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-statistical-protocol-v0.3.md
python -m moneybench.reviewer_smoke --json-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.md
python -m moneybench.local_model protocol --output ..\..\outputs\acceleratorbench-local-openai-compatible-protocol-v0.3.md
python -m moneybench.prompt_protocol --json-output ..\..\outputs\acceleratorbench-prompt-protocol-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-prompt-protocol-v0.3.md
python -m moneybench.provider_readiness --json-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-provider-readiness-v0.3.md
python -m moneybench.cost_accounting --json-output ..\..\outputs\acceleratorbench-cost-accounting-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-cost-accounting-v0.3.md
python -m moneybench.baseline_execution_plan --json-output ..\..\outputs\acceleratorbench-baseline-execution-plan-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-baseline-execution-plan-v0.3.md
python -m moneybench.provider_run_status --json-output ..\..\outputs\acceleratorbench-provider-run-status-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-provider-run-status-v0.3.md
python -m moneybench.license_readiness --json-output ..\..\outputs\acceleratorbench-license-readiness-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-license-readiness-v0.3.md
python -m moneybench.release_metadata --json-output ..\..\outputs\acceleratorbench-release-metadata-checklist-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-release-metadata-checklist-v0.3.md
python -m moneybench.holdout protocol --output ..\..\outputs\acceleratorbench-private-holdout-evaluator-protocol-v0.3.md
python -m moneybench.human_calibration --json-output ..\..\outputs\acceleratorbench-human-calibration-protocol-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-human-calibration-protocol-v0.3.md
python -m moneybench.human_calibration_schema --json-output ..\..\outputs\acceleratorbench-human-calibration-schema-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-human-calibration-schema-v0.3.md --template-output ..\..\outputs\acceleratorbench-human-calibration-template-v0.3.json
python -m moneybench.references --bibtex-output ..\..\outputs\acceleratorbench-references.bib --provenance-output ..\..\outputs\acceleratorbench-reference-provenance-v0.3.json
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json --report ..\..\outputs\acceleratorbench-submission-validation-v0.3.md
python -m moneybench.submission_schema --json-output ..\..\outputs\acceleratorbench-model-submission-schema-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-model-submission-schema-v0.3.md
python -m moneybench.submission_bundle --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed0.json --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed1.json --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed2.json --output ..\..\outputs\acceleratorbench-deepseek-v0.3-repeats.json --report ..\..\outputs\acceleratorbench-deepseek-v0.3-repeats-submission-report.md
python -m moneybench.experiment_matrix --json-output ..\..\outputs\acceleratorbench-experiment-matrix-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-experiment-matrix-v0.3.md
python -m moneybench.reproducibility_manifest --json-output ..\..\outputs\acceleratorbench-reproducibility-manifest-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-reproducibility-manifest-v0.3.md
python -m moneybench.environment_report --json-output ..\..\outputs\acceleratorbench-environment-report-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-environment-report-v0.3.md
python -m moneybench.determinism_audit --json-output ..\..\outputs\acceleratorbench-determinism-audit-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-determinism-audit-v0.3.md
python -m moneybench.validity_report --json-output ..\..\outputs\acceleratorbench-validity-report-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-validity-report-v0.3.md
python -m moneybench.claim_evidence --json-output ..\..\outputs\acceleratorbench-claim-evidence-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-claim-evidence-v0.3.md
python -m moneybench.submission_gate --json-output ..\..\outputs\acceleratorbench-submission-gate-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-submission-gate-v0.3.md
python -m moneybench.reviewer_index --json-output ..\..\outputs\acceleratorbench-reviewer-index-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-reviewer-index-v0.3.md
python -m moneybench.publication_audit --json-output ..\..\outputs\acceleratorbench-publication-audit-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-publication-audit-v0.3.md
```

If `python` is not on PATH, use the bundled Codex runtime:

```powershell
& "C:\Users\louis\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe" -m unittest discover -s tests -v
```

## Hosted Provider Runs

Use the resumable runner for long hosted-model runs:

```powershell
$env:DEEPSEEK_API_KEY = "<key>"
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3.json --resume
```

Use audit mode to save redacted provider-call records:

```powershell
$env:MODEL_INPUT_COST_PER_MILLION = "0.00"
$env:MODEL_OUTPUT_COST_PER_MILLION = "0.00"
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3-audit.json --resume --audit
```

Audit logs include prompt hashes, redacted model responses, token usage when provided by the API, estimated provider cost, and latency. Inspect audit logs manually before sharing them.

Provider cost estimates use token usage returned by provider APIs plus evaluator-configured `MODEL_INPUT_COST_PER_MILLION` and `MODEL_OUTPUT_COST_PER_MILLION` assumptions. The accounting protocol is generated at `outputs/acceleratorbench-cost-accounting-v0.3.md`.

The prompt contract used by hosted and local provider policies is documented in `outputs/acceleratorbench-prompt-protocol-v0.3.md`. It fixes the action vocabulary, response schema, weekly action cap, provider message wrappers, self-consistency setting, and SHA-256 hashes needed to compare provider runs.

For a local/open-source baseline, serve the model through an OpenAI-compatible endpoint and use the `llm` policy:

```powershell
$env:OPENAI_COMPAT_BASE_URL = "http://localhost:8000/v1"
$env:OPENAI_COMPAT_MODEL = "Qwen/Qwen2.5-7B-Instruct"
python -m moneybench.local_model health --output ..\..\outputs\local-health.json
python -m moneybench.resumable_runner --policy llm --output ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --resume --audit
```

Validate provider submissions before reporting them:

```powershell
python -m moneybench.submission --input ..\..\outputs\provider-run.json --report ..\..\outputs\provider-run-submission-report.md
```

The resumable runner writes the same aggregate diagnostics, split summaries, and task coverage expected by the submission validator, so completed hosted/local runs should not require manual reshaping.

For repeated-sampling reports, run the same policy into separate output files with different `--seed` values, then submit a JSON object with a top-level `runs` array. The `--seed` value is recorded as `run_seed` and acts as a repeat index for hosted providers:

```powershell
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3-seed0.json --resume --seed 0
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3-seed1.json --resume --seed 1
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3-seed2.json --resume --seed 2
```

Combine the seed files into one validated repeated-run bundle:

```powershell
python -m moneybench.submission_bundle --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed0.json --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed1.json --input ..\..\outputs\acceleratorbench-deepseek-v0.3-seed2.json --output ..\..\outputs\acceleratorbench-deepseek-v0.3-repeats.json --report ..\..\outputs\acceleratorbench-deepseek-v0.3-repeats-submission-report.md
```

The model submission schema is documented in `outputs/acceleratorbench-model-submission-schema-v0.3.md`, and the repeated-run bundle protocol is documented in `outputs/acceleratorbench-submission-bundle-protocol-v0.3.md`. The schema describes accepted payload shapes and required fields; the validator checks all 50 task ids, public split coverage, task-level scores, aggregate diagnostics, and provider-error category accounting. The bundle helper also rejects duplicate policy/`run_seed` identities.

## Private Holdout Evaluator

The private holdout protocol is executable on an evaluator-controlled host. It requires an evaluator-held secret and emits aggregate private report fields by default:

```powershell
$env:FounderBench_HOLDOUT_SECRET = "<private-secret>"
python -m moneybench.holdout fingerprints --output private-holdout-fingerprints.json
python -m moneybench.private_holdout_evaluator --policy deepseek --output private-deepseek-report.json
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
- `deepseek_sc`
- `anthropic`
- `gemini`
- `llm` for OpenAI-compatible endpoints

## Outputs

Important generated artifacts live under `outputs/`:

- `acceleratorbench-task-manifest-v0.3.json`
- `acceleratorbench-task-coverage-v0.3.json`
- `acceleratorbench-task-coverage-v0.3.md`
- `acceleratorbench-task-provenance-v0.3.json`
- `acceleratorbench-task-provenance-v0.3.md`
- `acceleratorbench-task-cards-v0.3.json`
- `acceleratorbench-task-cards-v0.3.md`
- `acceleratorbench-action-semantics-v0.3.json`
- `acceleratorbench-action-semantics-v0.3.md`
- `acceleratorbench-market-catalog-v0.3.json`
- `acceleratorbench-market-catalog-v0.3.md`
- `acceleratorbench-responsible-use-v0.3.json`
- `acceleratorbench-responsible-use-v0.3.md`
- `acceleratorbench-baseline-leaderboard-v0.3.json`
- `acceleratorbench-leaderboard-stability-v0.3.json`
- `acceleratorbench-leaderboard-stability-v0.3.md`
- `acceleratorbench-baseline-raw-v0.3.json`
- `acceleratorbench-baseline-analysis-v0.3.md`
- `acceleratorbench-paper-tables-v0.3.json`
- `acceleratorbench-paper-tables-v0.3.md`
- `acceleratorbench-paper-figure-data-v0.3.json`
- `acceleratorbench-paper-figure-data-v0.3.md`
- `acceleratorbench-model-comparison-v0.3.json`
- `acceleratorbench-model-comparison-v0.3.md`
- `acceleratorbench-result-integrity-audit-v0.3.json`
- `acceleratorbench-result-integrity-audit-v0.3.md`
- `acceleratorbench-ablation-report-v0.3.md`
- `acceleratorbench-action-ablation-v0.3.json`
- `acceleratorbench-action-ablation-v0.3.md`
- `acceleratorbench-paired-statistics-v0.3.json`
- `acceleratorbench-paired-statistics-v0.3.md`
- `acceleratorbench-power-analysis-v0.3.json`
- `acceleratorbench-power-analysis-v0.3.md`
- `acceleratorbench-difficulty-calibration-v0.3.json`
- `acceleratorbench-difficulty-calibration-v0.3.md`
- `acceleratorbench-qualitative-traces-v0.3.json`
- `acceleratorbench-qualitative-traces-v0.3.md`
- `acceleratorbench-random-repeats-v0.3.json`
- `acceleratorbench-random-repeats-v0.3.md`
- `acceleratorbench-score-rubric-v0.3.json`
- `acceleratorbench-score-rubric-v0.3.md`
- `acceleratorbench-scoring-consistency-audit-v0.3.json`
- `acceleratorbench-scoring-consistency-audit-v0.3.md`
- `acceleratorbench-metric-sensitivity-v0.3.json`
- `acceleratorbench-metric-sensitivity-v0.3.md`
- `acceleratorbench-statistical-protocol-v0.3.json`
- `acceleratorbench-statistical-protocol-v0.3.md`
- `acceleratorbench-local-openai-compatible-protocol-v0.3.json`
- `acceleratorbench-local-openai-compatible-protocol-v0.3.md`
- `acceleratorbench-prompt-protocol-v0.3.json`
- `acceleratorbench-prompt-protocol-v0.3.md`
- `acceleratorbench-provider-readiness-v0.3.json`
- `acceleratorbench-provider-readiness-v0.3.md`
- `acceleratorbench-cost-accounting-v0.3.json`
- `acceleratorbench-cost-accounting-v0.3.md`
- `acceleratorbench-baseline-execution-plan-v0.3.json`
- `acceleratorbench-baseline-execution-plan-v0.3.md`
- `acceleratorbench-provider-run-status-v0.3.json`
- `acceleratorbench-provider-run-status-v0.3.md`
- `acceleratorbench-license-readiness-v0.3.json`
- `acceleratorbench-license-readiness-v0.3.md`
- `acceleratorbench-release-metadata-checklist-v0.3.json`
- `acceleratorbench-release-metadata-checklist-v0.3.md`
- `acceleratorbench-private-holdout-evaluator-protocol-v0.3.json`
- `acceleratorbench-private-holdout-evaluator-protocol-v0.3.md`
- `acceleratorbench-human-calibration-protocol-v0.3.json`
- `acceleratorbench-human-calibration-protocol-v0.3.md`
- `acceleratorbench-human-calibration-schema-v0.3.json`
- `acceleratorbench-human-calibration-schema-v0.3.md`
- `acceleratorbench-human-calibration-template-v0.3.json`
- `acceleratorbench-references.bib`
- `acceleratorbench-reference-provenance-v0.3.json`
- `acceleratorbench-reproducibility-manifest-v0.3.json`
- `acceleratorbench-reproducibility-manifest-v0.3.md`
- `acceleratorbench-environment-report-v0.3.json`
- `acceleratorbench-environment-report-v0.3.md`
- `acceleratorbench-determinism-audit-v0.3.json`
- `acceleratorbench-determinism-audit-v0.3.md`
- `acceleratorbench-validity-report-v0.3.json`
- `acceleratorbench-validity-report-v0.3.md`
- `acceleratorbench-claim-evidence-v0.3.json`
- `acceleratorbench-claim-evidence-v0.3.md`
- `acceleratorbench-submission-gate-v0.3.json`
- `acceleratorbench-submission-gate-v0.3.md`
- `acceleratorbench-experiment-matrix-v0.3.json`
- `acceleratorbench-experiment-matrix-v0.3.md`
- `acceleratorbench-reviewer-index-v0.3.json`
- `acceleratorbench-reviewer-index-v0.3.md`
- `acceleratorbench-publication-audit-v0.3.json`
- `acceleratorbench-publication-audit-v0.3.md`
- `acceleratorbench-benchmark-card.md`
- `acceleratorbench-metrics-and-evaluation.md`
- `acceleratorbench-reproduction-guide.md`
- `acceleratorbench-reviewer-smoke-v0.3.json`
- `acceleratorbench-reviewer-smoke-v0.3.md`
- `acceleratorbench-model-submission-template.md`
- `acceleratorbench-model-submission-schema-v0.3.json`
- `acceleratorbench-model-submission-schema-v0.3.md`
- `acceleratorbench-submission-bundle-protocol-v0.3.json`
- `acceleratorbench-submission-bundle-protocol-v0.3.md`
- `acceleratorbench-submission-validation-v0.3.md`

## Non-Goals

FounderBench is not a real-money trading system, a legal recommendation engine, or a blueprint for deploying unsupervised autonomous companies. It is a controlled evaluation environment for studying startup-relevant agent decision-making.
