# FounderBench Datasheet

This generated datasheet provides benchmark/dataset-style disclosure for reviewers. It complements the benchmark card by answering composition, curation, intended-use, distribution, and maintenance questions in a fixed schema.

Status: `documentation_complete_external_evidence_still_missing`

## Artifact Summary

| Field | Value |
| --- | --- |
| public_tasks | 50 |
| task_families | 10 |
| structured_actions | 13 |
| simulated_markets | 8 |
| contains_real_company_data | False |
| contains_human_subject_data | False |
| public_test_hidden | False |
| official_private_leaderboard_included | False |

## Datasheet Questions

### Motivation

**Why was the benchmark created?**

To evaluate whether LLM agents can make repeated startup-like operating decisions under bounded resources, noisy market information, and risk penalties.

**What is the primary evaluation unit?**

A fixed simulated startup episode with initial state, task objective, structured action space, horizon, seed, and bounded 0-100 score.

**What should the benchmark not be used to claim?**

It should not be used to claim real-world startup success prediction, autonomous-company deployability, or hidden-suite leaderboard performance without additional evidence.

### Composition

**What does current release contain?**

50 public tasks across 10 task families, a deterministic simulator, an 8-market catalog, 13 structured actions, non-LLM baselines, provider adapters, validation tooling, and generated reviewer artifacts.

**What are the public splits?**

FND-001..FND-030 are public_dev; FND-031..FND-050 are public_test. Both splits are released and visible.

**Does current release include private task definitions?**

No. It includes a private-holdout blueprint, evaluator protocol, harness, and smoke report, but no official private leaderboard or hidden task definitions.

**Does the artifact contain personal data, real company data, or human-subject data?**

No. current tasks are synthetic and template-generated; no real company records or human-subject source data are included.

### Collection and Curation

**How were tasks created?**

Tasks were generated from 10 hand-designed synthetic templates with 5 public variants each, fixed seeds, setup functions, and task-family scoring functions.

**How are scoring rules documented?**

The score rubric, task cards, task provenance report, task coverage report, metric-sensitivity report, and simulator invariant audit document score components, bounds, and validation checks.

**Can public tasks be revised after model runs?**

Official task definitions should not be changed for a reported result without incrementing the benchmark version and regenerating affected claims.

### Uses

**What uses are intended?**

Research on LLM agents, sequential decision-making, structured action policies, cost-aware model comparison, and startup-operator simulation.

**What uses are out of scope?**

Real-money trading, investment advice, company governance automation, legal/financial due diligence, or claims that a model can safely run a real company without human oversight.

**How should public scores be reported?**

Public scores should name the version, task count, split visibility, prompt/protocol version, model identifier, run seed, diagnostics, and whether results are single-run or repeated.

### Distribution and Access

**What files should be distributed?**

The release bundle, source package, task manifest/cards, generated reports, validation scripts, checksum manifest, and reproduction guide.

**What metadata remains owner-dependent?**

Final public LICENSE and citation metadata are not owner-finalized in the current workspace and remain a publication blocker.

**How are secrets handled?**

Provider keys and private-holdout secrets are environment variables only; generated artifacts record variable names, redacted traces, hashes, and aggregate diagnostics but not secret values.

### Maintenance

**How should future versions be maintained?**

Version task/rubric changes, keep public and private evaluation cycles separate, rotate private holdout secrets after each cycle, and preserve old release bundles for reproducibility.

**How are issues tracked?**

Use the task revision ledger for calibration, provider-trace, holdout, and reviewer issues; do not silently edit reported tasks or rubrics.

**What evidence is still needed for a final paper?**

Validated hosted/local LLM baselines, executed evaluator-host private holdout, executed human/expert calibration, and final owner-selected license/citation metadata.

## Evidence Paths

- `outputs/founderbench-benchmark-card.md`
- `outputs/founderbench-task-provenance.md`
- `outputs/founderbench-task-coverage.md`
- `outputs/founderbench-contamination-leakage-audit.md`
- `outputs/founderbench-simulator-invariant-audit.md`
- `outputs/founderbench-license-readiness.md`
- `outputs/founderbench-completion-audit.md`

## Validation

Status: PASS

The datasheet covers required disclosure sections and keeps unsupported evidence claims explicit.
