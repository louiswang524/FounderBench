# FounderBench v0.3 Reviewer Index

This generated index is the suggested starting point for reviewing the supplementary package. It maps each major artifact to its review purpose and records file presence plus checksums in the JSON companion.

## Start Here

- `work/moneybench/README.md`
- `outputs/acceleratorbench-benchmark-card.md`
- `outputs/acceleratorbench-datasheet-v0.3.md`
- `outputs/acceleratorbench-responsible-use-v0.3.md`
- `outputs/acceleratorbench-task-coverage-v0.3.md`
- `outputs/acceleratorbench-task-provenance-v0.3.md`
- `outputs/acceleratorbench-market-catalog-v0.3.md`
- `outputs/acceleratorbench-metrics-and-evaluation.md`
- `outputs/acceleratorbench-score-rubric-v0.3.md`
- `outputs/acceleratorbench-scoring-consistency-audit-v0.3.md`
- `outputs/acceleratorbench-leaderboard-policy-v0.3.md`
- `outputs/acceleratorbench-leaderboard-stability-v0.3.md`
- `outputs/acceleratorbench-power-analysis-v0.3.md`
- `outputs/acceleratorbench-task-feasibility-audit-v0.3.md`
- `outputs/acceleratorbench-task-revision-ledger-v0.3.md`
- `outputs/acceleratorbench-reviewer-smoke-v0.3.md`
- `outputs/acceleratorbench-environment-report-v0.3.md`
- `outputs/acceleratorbench-simulator-invariant-audit-v0.3.md`
- `outputs/acceleratorbench-reproducibility-manifest-v0.3.md`
- `outputs/acceleratorbench-determinism-audit-v0.3.md`
- `outputs/acceleratorbench-validity-report-v0.3.md`
- `outputs/acceleratorbench-human-calibration-protocol-v0.3.md`
- `outputs/acceleratorbench-human-calibration-schema-v0.3.md`
- `outputs/acceleratorbench-human-calibration-analysis-v0.3.md`
- `outputs/acceleratorbench-human-calibration-packet-v0.3.md`
- `outputs/acceleratorbench-claim-evidence-v0.3.md`
- `outputs/acceleratorbench-license-readiness-v0.3.md`
- `outputs/acceleratorbench-release-metadata-checklist-v0.3.md`
- `outputs/acceleratorbench-submission-gate-v0.3.md`
- `outputs/acceleratorbench-submission-manifest-v0.3.md`
- `outputs/acceleratorbench-reviewer-risk-audit-v0.3.md`
- `outputs/acceleratorbench-failure-mode-audit-v0.3.md`
- `outputs/acceleratorbench-submission-action-plan-v0.3.md`
- `outputs/acceleratorbench-experiment-matrix-v0.3.md`
- `outputs/acceleratorbench-cost-accounting-v0.3.md`
- `outputs/acceleratorbench-baseline-execution-plan-v0.3.md`
- `outputs/acceleratorbench-provider-run-status-v0.3.md`
- `outputs/acceleratorbench-provider-comparability-audit-v0.3.md`
- `outputs/acceleratorbench-provider-contract-audit-v0.3.md`
- `outputs/acceleratorbench-contamination-leakage-audit-v0.3.md`
- `outputs/acceleratorbench-result-integrity-audit-v0.3.md`
- `outputs/acceleratorbench-paper-tables-v0.3.md`
- `outputs/acceleratorbench-model-result-cards-v0.3.md`
- `outputs/acceleratorbench-citation-audit-v0.3.md`
- `outputs/acceleratorbench-private-holdout-smoke-v0.3.md`
- `outputs/acceleratorbench-publication-audit-v0.3.md`

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
| orientation | work/moneybench/README.md | yes | 21778 | Start here for installation, task families, action space, and run commands. |
| orientation | work/moneybench/SPEC.md | yes | 9226 | Formal simulator and benchmark specification. |
| documentation | outputs/acceleratorbench-action-semantics-v0.3.md | yes | 8408 | Human-readable semantics for every structured action: required fields, costs, effects, risk triggers, and typical use cases. |
| data | outputs/acceleratorbench-market-catalog-v0.3.md | yes | 5291 | Fixed simulated market catalog documenting all 8 market ids, demand/competition/WTP/support parameters, observation rules, and settlement rules. |
| documentation | outputs/acceleratorbench-benchmark-card.md | yes | 6684 | Dataset-style benchmark card with intended use, limitations, and scope. |
| documentation | outputs/acceleratorbench-datasheet-v0.3.md | yes | 5252 | Datasheet-style disclosure covering motivation, composition, curation, intended use, distribution, maintenance, and unsupported claims. |
| documentation | outputs/acceleratorbench-responsible-use-v0.3.md | yes | 4105 | Responsible-use, ethics, privacy, unsupported-use, and provider-submission disclosure statement. |
| data | outputs/acceleratorbench-task-manifest-v0.3.json | yes | 33738 | Fixed public 50-task suite, task families, splits, budgets, and scenario metadata. |
| data | outputs/acceleratorbench-task-coverage-v0.3.md | yes | 3571 | Task-suite balance, split, action, and capability coverage report. |
| data | outputs/acceleratorbench-task-provenance-v0.3.md | yes | 3741 | Task curation and provenance record documenting templates, seed rules, setup sources, score sources, and synthetic-data status. |
| data | outputs/acceleratorbench-task-cards-v0.3.md | yes | 38551 | Human-readable cards for all 50 tasks, including initial state, scoring metrics, expected actions, family, split, and horizon. |
| metrics | outputs/acceleratorbench-metrics-and-evaluation.md | yes | 7358 | Primary score, solve criteria, diagnostic metrics, penalties, and comparison protocol. |
| metrics | outputs/acceleratorbench-score-rubric-v0.3.md | yes | 7097 | Family-level score components, penalty rules, bounds, and pass-threshold validation. |
| metrics | outputs/acceleratorbench-scoring-consistency-audit-v0.3.md | yes | 3812 | Score-object consistency audit over all deterministic raw task results, including bounds, pass threshold, metrics payloads, family coverage, and split coverage. |
| metrics | outputs/acceleratorbench-metric-sensitivity-v0.3.md | yes | 3118 | Sensitivity analysis comparing official bounded task score against normalized business, solve-rate, survival, revenue, cash, and risk diagnostics. |
| baseline_evidence | outputs/acceleratorbench-baseline-leaderboard-v0.3.json | yes | 2653 | Machine-readable leaderboard for included non-LLM baselines. |
| metrics | outputs/acceleratorbench-leaderboard-policy-v0.3.md | yes | 3488 | Leaderboard/reporting policy defining public, repeated-run, and future private-holdout tiers plus acceptance and rejection rules. |
| baseline_evidence | outputs/acceleratorbench-leaderboard-stability-v0.3.md | yes | 3186 | Leaderboard stability audit over deterministic baselines using split checks, leave-one-family-out checks, and bootstrap task-mix resampling. |
| baseline_evidence | outputs/acceleratorbench-baseline-raw-v0.3.json | yes | 342102 | Task-level raw baseline results for random, conservative, heuristic, and task-aware heuristic policies. |
| baseline_evidence | outputs/acceleratorbench-baseline-analysis-v0.3.md | yes | 4385 | Bootstrap intervals, split summaries, family scores, and policy comparisons. |
| reproducibility | outputs/acceleratorbench-result-integrity-audit-v0.3.md | yes | 1623 | Raw-to-report integrity audit proving deterministic baseline rows in leaderboard, paper tables, and model comparison match raw task outputs. |
| baseline_evidence | outputs/acceleratorbench-paper-tables-v0.3.md | yes | 4587 | Paper-ready result tables generated from raw v0.3.0 runs and validated provider availability. |
| paper | outputs/acceleratorbench-paper-figure-data-v0.3.md | yes | 1647 | Paper figure datasets for leaderboard bars, family heatmaps, action-ablation drops, difficulty bands, and metric-sensitivity rankings. |
| paper | outputs/acceleratorbench-paper-evidence-map-v0.3.md | yes | 8562 | Section-by-section paper evidence crosswalk linking draft claims to supporting artifacts and excluded claims. |
| baseline_evidence | outputs/acceleratorbench-model-comparison-v0.3.md | yes | 4618 | Unified leaderboard/comparison report that automatically incorporates validated hosted/local provider runs and keeps missing provider evidence explicit. |
| baseline_evidence | outputs/acceleratorbench-model-result-cards-v0.3.md | yes | 3164 | Reviewer-facing result cards summarizing deterministic baselines and planned provider submissions with validation, diagnostics, cost fields, and claim eligibility. |
| baseline_evidence | outputs/acceleratorbench-ablation-report-v0.3.md | yes | 2449 | Capability-ladder ablation from random to task-aware heuristic behavior. |
| baseline_evidence | outputs/acceleratorbench-action-ablation-v0.3.md | yes | 2377 | Action-space ablation showing how disabling discovery, growth, quality/support, pricing, runway/funding, and pivot actions changes task-aware baseline outcomes. |
| baseline_evidence | outputs/acceleratorbench-paired-statistics-v0.3.md | yes | 2174 | Paired score gaps, bootstrap intervals, raw and Holm-adjusted permutation p-values, effect sizes, and win/loss/tie counts over matched tasks. |
| metrics | outputs/acceleratorbench-power-analysis-v0.3.md | yes | 3053 | Power and resolution analysis estimating minimum detectable score gaps for the public suite and warning against overclaiming close model differences. |
| metrics | outputs/acceleratorbench-statistical-protocol-v0.3.md | yes | 3583 | Pre-specified primary endpoint, paired comparison test, repeated-sampling, multiple-comparison, and claim rules for model comparisons. |
| baseline_evidence | outputs/acceleratorbench-difficulty-calibration-v0.3.md | yes | 5571 | Task difficulty bands, baseline solve-count calibration, family/split balance, and high-discrimination tasks. |
| baseline_evidence | outputs/acceleratorbench-task-feasibility-audit-v0.3.md | yes | 12201 | Task-level feasibility and discrimination ledger identifying baseline-solved, saturated, high-discrimination, and external-calibration-needed tasks. |
| publication_readiness | outputs/acceleratorbench-task-revision-ledger-v0.3.md | yes | 8777 | Change-control ledger for converting calibration, provider-trace, holdout, and reviewer feedback into auditable task or rubric revisions. |
| publication_readiness | outputs/acceleratorbench-experiment-matrix-v0.3.md | yes | 5601 | Paper-facing ledger of completed and missing baselines, ablations, uncertainty checks, audit traces, and holdout evidence. |
| uncertainty | outputs/acceleratorbench-random-repeats-v0.3.md | yes | 800 | Repeated-seed calibration intervals for the stochastic random baseline. |
| qualitative | outputs/acceleratorbench-qualitative-traces-v0.3.md | yes | 5234 | Representative deterministic success and failure traces for paper analysis. |
| reproducibility | outputs/acceleratorbench-reproduction-guide.md | yes | 7272 | End-to-end instructions for regenerating artifacts and validating submissions. |
| reproducibility | outputs/acceleratorbench-reviewer-smoke-v0.3.md | yes | 1365 | Fast reviewer smoke report checking task loading, one deterministic task execution, and included baseline submission validation. |
| reproducibility | outputs/acceleratorbench-environment-report-v0.3.md | yes | 2183 | Runtime and dependency report with Python version, import classification, import checks, and provider/local-model dependency notes. |
| reproducibility | outputs/acceleratorbench-simulator-invariant-audit-v0.3.md | yes | 1910 | Deterministic simulator stress audit checking state bounds, score bounds, and core environment invariants without claiming real-world validity. |
| reproducibility | outputs/acceleratorbench-reproducibility-manifest-v0.3.md | yes | 25528 | Source/output hashes, environment metadata, and reproduction commands for the current workspace. |
| reproducibility | outputs/acceleratorbench-determinism-audit-v0.3.md | yes | 1303 | Replay audit showing deterministic baselines reproduce stable task outcomes from fixed seeds. |
| documentation | outputs/acceleratorbench-validity-report-v0.3.md | yes | 5998 | Threats-to-validity matrix with mitigations, evidence paths, and remaining work. |
| documentation | outputs/acceleratorbench-human-calibration-protocol-v0.3.md | yes | 3808 | Expert/human-founder calibration protocol for checking task realism, action coverage, score alignment, difficulty, and gaming risks. |
| documentation | outputs/acceleratorbench-human-calibration-schema-v0.3.md | yes | 2021 | Machine-readable calibration response schema and validation contract for expert/human-founder reviews. |
| documentation | outputs/acceleratorbench-human-calibration-template-v0.3.json | yes | 6895 | Blank JSON template for collecting expert/human-founder calibration responses over required sampled tasks. |
| documentation | outputs/acceleratorbench-human-calibration-analysis-v0.3.md | yes | 993 | Analyzer output for expert/human-founder calibration responses; currently records that no executed calibration submissions are included. |
| documentation | outputs/acceleratorbench-human-calibration-packet-v0.3.md | yes | 4981 | Recruitment and operator packet for executing expert/human-founder calibration while preserving not-executed claim guardrails. |
| documentation | outputs/acceleratorbench-claim-evidence-v0.3.md | yes | 5856 | Claim-evidence guardrail for supported, qualified, and unsupported paper wording. |
| submission | outputs/acceleratorbench-model-submission-template.md | yes | 4260 | Template for future model providers reporting a run. |
| submission | outputs/acceleratorbench-model-submission-schema-v0.3.md | yes | 1506 | Machine-readable submission schema companion documenting accepted run payloads, required diagnostics, and authoritative validation command. |
| submission | outputs/acceleratorbench-submission-bundle-protocol-v0.3.md | yes | 1584 | Protocol and CLI helper for combining repeated provider/model seed runs into one validated submission bundle. |
| submission | outputs/acceleratorbench-submission-validation-v0.3.md | yes | 1440 | Validation report for the included complete baseline run. |
| provider_runs | outputs/acceleratorbench-provider-readiness-v0.3.md | yes | 3332 | Environment readiness matrix and exact commands for hosted/local provider runs. |
| provider_runs | outputs/acceleratorbench-cost-accounting-v0.3.md | yes | 2413 | Provider token and cost-accounting protocol with usage normalization, price environment variables, formula, and reporting guardrails. |
| provider_runs | outputs/acceleratorbench-baseline-execution-plan-v0.3.md | yes | 10314 | Paper-grade hosted/local baseline execution plan with fairness controls, repeats, audit policy, commands, and acceptance criteria. |
| provider_runs | outputs/acceleratorbench-experiment-runbook-v0.3.md | yes | 15964 | Operator runbook for executing missing hosted/local model baselines, audits, repeat bundles, and post-run claim-gate updates. |
| provider_runs | outputs/acceleratorbench-provider-run-status-v0.3.md | yes | 4463 | Generated status report for planned v0.3 provider/local runs, validation reports, audit outputs, and excluded older provider-like files. |
| provider_runs | outputs/acceleratorbench-provider-comparability-audit-v0.3.md | yes | 3255 | Protocol comparability audit checking shared task count, prompt/action contract, validation commands, repeat policy, cost fields, and self-consistency ablation treatment. |
| provider_runs | outputs/acceleratorbench-provider-contract-audit-v0.3.md | yes | 2170 | Provider-output contract audit checking parser error taxonomy and simulator diagnostics without claiming hosted/local LLM result evidence. |
| anti_gaming | outputs/acceleratorbench-contamination-leakage-audit-v0.3.md | yes | 4302 | Public-split contamination/leakage audit that keeps public_test visibility, trace leakage risks, and private-holdout claim guardrails explicit. |
| provider_runs | outputs/acceleratorbench-prompt-protocol-v0.3.md | yes | 4536 | Canonical LLM prompt contract, provider message wrappers, action vocabulary, and prompt/protocol hashes. |
| publication_readiness | outputs/acceleratorbench-license-readiness-v0.3.md | yes | 2417 | License and citation metadata readiness checks plus owner decisions required before public release. |
| publication_readiness | outputs/acceleratorbench-release-metadata-checklist-v0.3.md | yes | 3574 | Owner-facing release metadata checklist with license option matrix, CITATION template, and finalization steps. |
| publication_readiness | work/moneybench/LICENSE.template | yes | 475 | Non-final owner-facing template for creating the required public LICENSE file. |
| publication_readiness | work/moneybench/CITATION.cff.template | yes | 571 | Non-final owner-facing CITATION.cff template with placeholders for authors, repository URL, and selected license. |
| publication_readiness | outputs/acceleratorbench-submission-gate-v0.3.md | yes | 1553 | Top-level go/no-go submission gate combining publication, experiment, provider, claim, and license readiness. |
| publication_readiness | outputs/acceleratorbench-submission-manifest-v0.3.md | yes | 6050 | Compact reviewer-facing manifest of included evidence, supported claims, excluded claims, reproduction commands, and remaining gate blockers. |
| publication_readiness | outputs/acceleratorbench-completion-audit-v0.3.md | yes | 8627 | Goal-level completion audit mapping the active publishable-benchmark objective to current evidence and unresolved blockers. |
| publication_readiness | outputs/acceleratorbench-reviewer-risk-audit-v0.3.md | yes | 10135 | Pre-submission reviewer-risk audit listing likely reviewer objections, current evidence, open risks, and required responses. |
| publication_readiness | outputs/acceleratorbench-failure-mode-audit-v0.3.md | yes | 8786 | AI research failure-mode audit covering code bugs, citation hallucination, result hallucination, shortcut reliance, bug-as-insight, methodology fabrication, and frame-lock. |
| publication_readiness | outputs/acceleratorbench-paper-claim-lint-v0.3.md | yes | 1548 | Text-level paper and benchmark-card lint checking required limitation disclosures and selected unsupported positive claim wording. |
| publication_readiness | outputs/acceleratorbench-submission-action-plan-v0.3.md | yes | 13345 | Concrete action plan mapping each failing submission gate to owners, commands, expected outputs, and claim impact. |
| provider_runs | outputs/acceleratorbench-local-openai-compatible-protocol-v0.3.md | yes | 1194 | Protocol for running local open-source models through an OpenAI-compatible endpoint. |
| anti_gaming | outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md | yes | 2163 | Evaluator-host protocol for secret-seeded hidden task execution, aggregate reporting, and anti-gaming controls. |
| anti_gaming | outputs/acceleratorbench-private-holdout-smoke-v0.3.md | yes | 1339 | Aggregate-only smoke report proving the private-holdout evaluator harness runs without exposing hidden task definitions; not an official private leaderboard. |
| anti_gaming | work/moneybench/moneybench/private_holdout_evaluator.py | yes | 7766 | Executable private-holdout evaluator harness that generates secret-selected private episodes in memory and emits aggregate-only reports by default. |
| publication_readiness | outputs/acceleratorbench-publication-audit-v0.3.md | yes | 16702 | Submission-readiness matrix mapping benchmark requirements to concrete evidence and blockers. |
| paper | outputs/acceleratorbench-paper-draft-v0.1.md | yes | 27632 | Paper-facing draft with motivation, benchmark design, experiments, and limitations. |
| paper | outputs/acceleratorbench-references.bib | yes | 5246 | BibTeX references used by the paper draft and related-work notes. |
| paper | outputs/acceleratorbench-citation-audit-v0.3.md | yes | 2656 | Local citation-context audit verifying paper citation numbering, BibTeX/provenance coverage, and intended citation use. |
| release | release/acceleratorbench-v0.3.0/SHA256SUMS.json | yes | 42106 | Release-bundle checksum manifest for integrity verification. |
| release | release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md | yes | 673 | Release-bundle integrity report verifying bundled files against SHA256SUMS.json. |

## Current Open Blockers

- Run full hosted LLM baselines on all 50 v0.3.0 tasks.
- Run at least one local/open-source model baseline through the OpenAI-compatible protocol.
- Collect representative redacted hosted-LLM audit traces.
- Execute the private holdout protocol on an evaluator-controlled host.
- Finalize public license and citation metadata.

## Integrity

Use `release/acceleratorbench-v0.3.0/SHA256SUMS.json` for bundled artifact verification. The bundle also includes `release/acceleratorbench-v0.3.0/BUNDLE-INTEGRITY.md`, generated after the checksum manifest to verify the bundled files. The JSON version of this reviewer index includes per-file SHA-256 values for the source workspace artifacts listed above.
