# FounderBench Reviewer Index

This generated index is the suggested starting point for reviewing the supplementary package. It maps each major artifact to its review purpose and records file presence plus checksums in the JSON companion.

## Start Here

- `work/moneybench/README.md`
- `outputs/founderbench-benchmark-card.md`
- `outputs/founderbench-datasheet.md`
- `outputs/founderbench-responsible-use.md`
- `outputs/founderbench-task-coverage.md`
- `outputs/founderbench-task-provenance.md`
- `outputs/founderbench-market-catalog.md`
- `outputs/founderbench-metrics-and-evaluation.md`
- `outputs/founderbench-score-rubric.md`
- `outputs/founderbench-scoring-consistency-audit.md`
- `outputs/founderbench-leaderboard-policy.md`
- `outputs/founderbench-leaderboard-stability.md`
- `outputs/founderbench-power-analysis.md`
- `outputs/founderbench-task-feasibility-audit.md`
- `outputs/founderbench-task-revision-ledger.md`
- `outputs/founderbench-reviewer-smoke.md`
- `outputs/founderbench-environment-report.md`
- `outputs/founderbench-simulator-invariant-audit.md`
- `outputs/founderbench-reproducibility-manifest.md`
- `outputs/founderbench-determinism-audit.md`
- `outputs/founderbench-validity-report.md`
- `outputs/founderbench-human-calibration-protocol.md`
- `outputs/founderbench-human-calibration-schema.md`
- `outputs/founderbench-human-calibration-analysis.md`
- `outputs/founderbench-human-calibration-packet.md`
- `outputs/founderbench-claim-evidence.md`
- `outputs/founderbench-license-readiness.md`
- `outputs/founderbench-release-metadata-checklist.md`
- `outputs/founderbench-submission-gate.md`
- `outputs/founderbench-submission-manifest.md`
- `outputs/founderbench-reviewer-risk-audit.md`
- `outputs/founderbench-failure-mode-audit.md`
- `outputs/founderbench-submission-action-plan.md`
- `outputs/founderbench-experiment-matrix.md`
- `outputs/founderbench-cost-accounting.md`
- `outputs/founderbench-baseline-execution-plan.md`
- `outputs/founderbench-provider-run-status.md`
- `outputs/founderbench-provider-comparability-audit.md`
- `outputs/founderbench-provider-contract-audit.md`
- `outputs/founderbench-contamination-leakage-audit.md`
- `outputs/founderbench-result-integrity-audit.md`
- `outputs/founderbench-paper-tables.md`
- `outputs/founderbench-model-result-cards.md`
- `outputs/founderbench-citation-audit.md`
- `outputs/founderbench-private-holdout-smoke.md`
- `outputs/founderbench-publication-audit.md`

## Reproduction Commands

| Purpose | Working Directory | Command |
| --- | --- | --- |
| Run tests | work/moneybench | `python -m unittest discover -s tests -v` |
| Regenerate generated artifacts | work/moneybench | `python -m moneybench.release regenerate` |
| Validate generated artifacts and tests | work/moneybench | `python -m moneybench.release validate` |
| Build supplementary bundle | work/moneybench | `python -m moneybench.release bundle` |
| Validate a model submission | work/moneybench | `python -m moneybench.submission --input ..\..\outputs\provider-run.json --report ..\..\outputs\provider-run-submission-report.md` |
| Combine repeated model runs | work/moneybench | `python -m moneybench.submission_bundle --input ..\..\outputs\provider-seed0.json --input ..\..\outputs\provider-seed1.json --output ..\..\outputs\provider-repeats.json --report ..\..\outputs\provider-repeats-submission-report.md` |

## Artifact Map

| Category | Path | Present | Bytes | Review Purpose |
| --- | --- | --- | --- | --- |
| orientation | work/moneybench/README.md | yes | 20647 | Start here for installation, task families, action space, and run commands. |
| orientation | work/moneybench/SPEC.md | yes | 9629 | Formal simulator and benchmark specification. |
| documentation | outputs/founderbench-action-semantics.md | yes | 8403 | Human-readable semantics for every structured action: required fields, costs, effects, risk triggers, and typical use cases. |
| data | outputs/founderbench-market-catalog.md | yes | 5295 | Fixed simulated market catalog documenting all 8 market ids, demand/competition/WTP/support parameters, observation rules, and settlement rules. |
| documentation | outputs/founderbench-benchmark-card.md | yes | 6843 | Dataset-style benchmark card with intended use, limitations, and scope. |
| documentation | outputs/founderbench-datasheet.md | yes | 5208 | Datasheet-style disclosure covering motivation, composition, curation, intended use, distribution, maintenance, and unsupported claims. |
| documentation | outputs/founderbench-responsible-use.md | yes | 4094 | Responsible-use, ethics, privacy, unsupported-use, and provider-submission disclosure statement. |
| data | outputs/founderbench-task-manifest.json | yes | 33747 | Fixed public 50-task suite, task families, splits, budgets, and scenario metadata. |
| data | outputs/founderbench-task-coverage.md | yes | 3566 | Task-suite balance, split, action, and capability coverage report. |
| data | outputs/founderbench-task-provenance.md | yes | 3763 | Task curation and provenance record documenting templates, seed rules, setup sources, score sources, and synthetic-data status. |
| data | outputs/founderbench-task-cards.md | yes | 38555 | Human-readable cards for all 50 tasks, including initial state, scoring metrics, expected actions, family, split, and horizon. |
| metrics | outputs/founderbench-metrics-and-evaluation.md | yes | 7625 | Primary score, solve criteria, diagnostic metrics, penalties, and comparison protocol. |
| metrics | outputs/founderbench-score-rubric.md | yes | 7092 | Family-level score components, penalty rules, bounds, and pass-threshold validation. |
| metrics | outputs/founderbench-scoring-consistency-audit.md | yes | 3807 | Score-object consistency audit over all deterministic raw task results, including bounds, pass threshold, metrics payloads, family coverage, and split coverage. |
| metrics | outputs/founderbench-metric-sensitivity.md | yes | 3113 | Sensitivity analysis comparing official bounded task score against normalized business, solve-rate, survival, revenue, cash, and risk diagnostics. |
| baseline_evidence | outputs/founderbench-baseline-leaderboard.json | yes | 2653 | Machine-readable leaderboard for included non-LLM baselines. |
| metrics | outputs/founderbench-leaderboard-policy.md | yes | 3514 | Leaderboard/reporting policy defining public, repeated-run, and future private-holdout tiers plus acceptance and rejection rules. |
| baseline_evidence | outputs/founderbench-leaderboard-stability.md | yes | 3181 | Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling. |
| baseline_evidence | outputs/founderbench-baseline-raw.json | yes | 342072 | Task-level raw baseline results for random, conservative, heuristic, and task-aware heuristic policies. |
| baseline_evidence | outputs/founderbench-baseline-analysis.md | yes | 4380 | Bootstrap intervals, split summaries, family scores, and policy comparisons. |
| reproducibility | outputs/founderbench-result-integrity-audit.md | yes | 1582 | Raw-to-report integrity audit proving deterministic baseline rows in leaderboard, paper tables, and model comparison match raw task outputs. |
| baseline_evidence | outputs/founderbench-paper-tables.md | yes | 5625 | Paper-ready result tables generated from raw current release runs and validated provider availability. |
| paper | outputs/founderbench-paper-figure-data.md | yes | 1628 | Paper figure datasets for leaderboard bars, family heatmaps, action-ablation drops, difficulty bands, and metric-sensitivity rankings. |
| paper | outputs/founderbench-paper-evidence-map.md | yes | 8112 | Section-by-section paper evidence crosswalk linking draft claims to supporting artifacts and excluded claims. |
| baseline_evidence | outputs/founderbench-model-comparison.md | yes | 5638 | Unified leaderboard/comparison report that automatically incorporates validated hosted/local provider runs and keeps missing provider evidence explicit. |
| baseline_evidence | outputs/founderbench-model-result-cards.md | yes | 4442 | Reviewer-facing result cards summarizing deterministic baselines and planned provider submissions with validation, diagnostics, cost fields, and claim eligibility. |
| baseline_evidence | outputs/founderbench-ablation-report.md | yes | 2444 | Capability-ladder ablation from random to task-aware heuristic behavior. |
| baseline_evidence | outputs/founderbench-action-ablation.md | yes | 2372 | Action-space ablation showing how disabling discovery, growth, quality/support, pricing, runway/funding, and pivot actions changes task-aware baseline outcomes. |
| baseline_evidence | outputs/founderbench-paired-statistics.md | yes | 2169 | Paired score gaps, bootstrap intervals, raw and Holm-adjusted permutation p-values, effect sizes, and win/loss/tie counts over matched tasks. |
| metrics | outputs/founderbench-power-analysis.md | yes | 3049 | Power and resolution analysis estimating minimum detectable score gaps for the public suite and warning against overclaiming close model differences. |
| metrics | outputs/founderbench-statistical-protocol.md | yes | 3578 | Pre-specified primary endpoint, paired comparison test, repeated-sampling, multiple-comparison, and claim rules for model comparisons. |
| baseline_evidence | outputs/founderbench-difficulty-calibration.md | yes | 5566 | Task difficulty bands, baseline solve-count calibration, family/split balance, and high-discrimination tasks. |
| baseline_evidence | outputs/founderbench-task-feasibility-audit.md | yes | 12196 | Task-level feasibility and discrimination ledger identifying baseline-solved, saturated, high-discrimination, and external-calibration-needed tasks. |
| publication_readiness | outputs/founderbench-task-revision-ledger.md | yes | 8781 | Change-control ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable task or rubric revisions. |
| publication_readiness | outputs/founderbench-experiment-matrix.md | yes | 5398 | Paper-facing ledger of completed and missing baselines, ablations, uncertainty checks, audit traces, and holdout evidence. |
| uncertainty | outputs/founderbench-random-repeats.md | yes | 795 | Repeated-seed calibration intervals for the stochastic random baseline. |
| qualitative | outputs/founderbench-qualitative-traces.md | yes | 5229 | Representative deterministic success and failure traces for paper analysis. |
| reproducibility | outputs/founderbench-reproduction-guide.md | yes | 7259 | End-to-end instructions for regenerating artifacts and validating submissions. |
| reproducibility | outputs/founderbench-reviewer-smoke.md | yes | 1315 | Fast reviewer smoke report checking task loading, one deterministic task execution, and included baseline submission validation. |
| reproducibility | outputs/founderbench-environment-report.md | yes | 2189 | Runtime and dependency report with Python version, import classification, import checks, and provider/local-model dependency notes. |
| reproducibility | outputs/founderbench-simulator-invariant-audit.md | yes | 1905 | Deterministic simulator stress audit checking state bounds, score bounds, and core environment invariants without claiming real-world validity. |
| reproducibility | outputs/founderbench-reproducibility-manifest.md | yes | 24575 | Source/output hashes, environment metadata, and reproduction commands for the current workspace. |
| reproducibility | outputs/founderbench-determinism-audit.md | yes | 1298 | Replay audit showing deterministic baselines reproduce stable task outcomes from fixed seeds. |
| documentation | outputs/founderbench-validity-report.md | yes | 5808 | Threats-to-validity matrix with mitigations, evidence paths, and remaining work. |
| documentation | outputs/founderbench-human-calibration-protocol.md | yes | 3803 | Expert/human-founder calibration protocol for checking task realism, action coverage, score alignment, difficulty, and gaming risks. |
| documentation | outputs/founderbench-human-calibration-schema.md | yes | 2016 | Machine-readable calibration response schema and validation contract for expert/human-founder reviews. |
| documentation | outputs/founderbench-human-calibration-template.json | yes | 6895 | Blank JSON template for collecting expert/human-founder calibration responses over required sampled tasks. |
| documentation | outputs/founderbench-human-calibration-analysis.md | yes | 988 | Analyzer output for expert/human-founder calibration responses; currently records that no executed calibration submissions are included. |
| documentation | outputs/founderbench-human-calibration-packet.md | yes | 4904 | Recruitment and operator packet for executing expert/human-founder calibration while preserving not-executed claim guardrails. |
| documentation | outputs/founderbench-claim-evidence.md | yes | 5750 | Claim-evidence guardrail for supported, qualified, and unsupported paper wording. |
| submission | outputs/founderbench-model-submission-template.md | yes | 4352 | Template for future model providers reporting a run. |
| submission | outputs/founderbench-model-submission-schema.md | yes | 1512 | Machine-readable submission schema companion documenting accepted run payloads, required diagnostics, and authoritative validation command. |
| submission | outputs/founderbench-submission-bundle-protocol.md | yes | 1521 | Protocol and CLI helper for combining repeated provider/model seed runs into one validated submission bundle. |
| submission | outputs/founderbench-submission-validation.md | yes | 1431 | Validation report for the included complete baseline run. |
| provider_runs | outputs/founderbench-provider-readiness.md | yes | 7260 | Environment readiness matrix and exact commands for hosted/local provider runs. |
| provider_runs | outputs/founderbench-cost-accounting.md | yes | 2408 | Provider token and cost-accounting protocol with usage normalization, price environment variables, formula, and reporting guardrails. |
| provider_runs | outputs/founderbench-baseline-execution-plan.md | yes | 18654 | Paper-grade hosted/local baseline execution plan with fairness controls, repeats, audit policy, commands, and acceptance criteria. |
| provider_runs | outputs/founderbench-experiment-runbook.md | yes | 26100 | Operator runbook for executing missing hosted/local model baselines, audits, repeat bundles, and post-run claim-gate updates. |
| provider_runs | outputs/founderbench-provider-run-status.md | yes | 5626 | Generated status report for planned current release provider/local runs, validation reports, audit outputs, and excluded older provider-like files. |
| provider_runs | outputs/founderbench-provider-comparability-audit.md | yes | 4317 | Protocol comparability audit checking shared task count, prompt/action contract, validation commands, repeat policy, cost fields, and self-consistency ablation treatment. |
| provider_runs | outputs/founderbench-provider-contract-audit.md | yes | 2165 | Provider-output contract audit checking parser error taxonomy and simulator diagnostics without claiming hosted/local LLM result evidence. |
| anti_gaming | outputs/founderbench-contamination-leakage-audit.md | yes | 4315 | Public-split contamination/leakage audit that keeps public_test visibility, trace leakage risks, and private-holdout claim guardrails explicit. |
| provider_runs | outputs/founderbench-prompt-protocol.md | yes | 5413 | Canonical LLM prompt contract, provider message wrappers, action vocabulary, and prompt/protocol hashes. |
| publication_readiness | outputs/founderbench-license-readiness.md | yes | 2406 | License and citation metadata readiness checks plus owner decisions required before public release. |
| publication_readiness | outputs/founderbench-release-metadata-checklist.md | yes | 3569 | Owner-facing release metadata checklist with license option matrix, CITATION template, and finalization steps. |
| publication_readiness | work/moneybench/LICENSE.template | yes | 466 | Non-final owner-facing template for creating the required public LICENSE file. |
| publication_readiness | work/moneybench/CITATION.cff.template | yes | 582 | Non-final owner-facing CITATION.cff template with placeholders for authors, repository URL, and selected license. |
| publication_readiness | outputs/founderbench-submission-gate.md | yes | 1494 | Top-level go/no-go submission gate combining publication, experiment, provider, claim, and license readiness. |
| publication_readiness | outputs/founderbench-submission-manifest.md | yes | 5822 | Compact reviewer-facing manifest of included evidence, supported claims, excluded claims, reproduction commands, and remaining gate blockers. |
| publication_readiness | outputs/founderbench-completion-audit.md | yes | 8168 | Goal-level completion audit mapping the active publishable-benchmark objective to current evidence and unresolved blockers. |
| publication_readiness | outputs/founderbench-reviewer-risk-audit.md | yes | 9847 | Pre-submission reviewer-risk audit listing likely reviewer objections, current evidence, open risks, and required responses. |
| publication_readiness | outputs/founderbench-failure-mode-audit.md | yes | 8550 | AI research failure-mode audit covering code bugs, citation hallucination, result hallucination, shortcut reliance, bug-as-insight, methodology fabrication, and frame-lock. |
| publication_readiness | outputs/founderbench-paper-claim-lint.md | yes | 1530 | Text-level paper and benchmark-card lint checking required limitation disclosures and selected unsupported positive claim wording. |
| publication_readiness | outputs/founderbench-submission-action-plan.md | yes | 18068 | Concrete action plan mapping each failing submission gate to owners, commands, expected outputs, and claim impact. |
| provider_runs | outputs/founderbench-local-openai-compatible-protocol.md | yes | 1163 | Protocol for running local open-source models through an OpenAI-compatible endpoint. |
| anti_gaming | outputs/founderbench-private-holdout-evaluator-protocol.md | yes | 2163 | Evaluator-host protocol for secret-seeded hidden task execution, aggregate reporting, and anti-gaming controls. |
| anti_gaming | outputs/founderbench-private-holdout-smoke.md | yes | 1334 | Aggregate-only smoke report proving the private-holdout evaluator harness runs without exposing hidden task definitions; not an official private leaderboard. |
| anti_gaming | work/moneybench/moneybench/private_holdout_evaluator.py | yes | 7766 | Executable private-holdout evaluator harness that generates secret-selected private episodes in memory and emits aggregate-only reports by default. |
| publication_readiness | outputs/founderbench-publication-audit.md | yes | 15247 | Submission-readiness matrix mapping benchmark requirements to concrete evidence and blockers. |
| paper | outputs/founderbench-paper-draft.md | yes | 27853 | Paper-facing draft with motivation, benchmark design, experiments, and limitations. |
| paper | outputs/founderbench-references.bib | yes | 5246 | BibTeX references used by the paper draft and related-work notes. |
| paper | outputs/founderbench-citation-audit.md | yes | 2651 | Local citation-context audit verifying paper citation numbering, BibTeX/provenance coverage, and intended citation use. |
| release | release/founderbench/SHA256SUMS.json | yes | 40824 | Release-bundle checksum manifest for integrity verification. |
| release | release/founderbench/BUNDLE-INTEGRITY.md | yes | 662 | Release-bundle integrity report verifying bundled files against SHA256SUMS.json. |

## Current Open Blockers

- Run full hosted LLM baselines on all 50 current tasks.
- Run at least one local/open-source model baseline through the OpenAI-compatible protocol.
- Collect representative redacted hosted-LLM audit traces.
- Execute the private holdout protocol on an evaluator-controlled host.
- Finalize public license and citation metadata.

## Integrity

Use `release/founderbench/SHA256SUMS.json` for bundled artifact verification. The bundle also includes `release/founderbench/BUNDLE-INTEGRITY.md`, generated after the checksum manifest to verify the bundled files. The JSON version of this reviewer index includes per-file SHA-256 values for the source workspace artifacts listed above.
