# FounderBench AI Research Failure-Mode Audit

This generated audit applies a seven-mode AI research failure checklist to the benchmark artifact. It is an integrity aid, not a substitute for external peer review.

Submission gate: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| modes | 7 |
| clear | 0 |
| mitigated_or_guarded | 5 |
| warnings_or_blockers | 6 |
| stronger_claims_blocked | 4 |

## Mode Checks

| Mode | ID | Status | Gate Effect | Risk | Required Response |
| --- | --- | --- | --- | --- | --- |
| 1 | implementation_bug_passing_self_review | mitigated_not_closed | blocking_warning | Analysis or simulator code has a plausible-looking bug that is accepted into the paper as a valid result. | Keep deterministic replay, bundle integrity, and full test validation in the release loop; add independent hosted-run logs before model-result claims. |
| 2 | hallucinated_citation | local_context_verified_external_spotcheck_required | blocking_warning | A cited reference may not exist, may be miscited, or may be used for a claim it does not support. | Before submission, run an external citation verification pass over all BibTeX entries and citation contexts. |
| 3 | hallucinated_experimental_result | mitigated_for_reported_deterministic_results | blocks_stronger_llm_claims | A result table or model-comparison claim could report a number that no executed run produced. | Only report deterministic baseline numbers generated from raw output; keep hosted/local LLM result claims excluded until validated provider run files exist. |
| 4 | shortcut_reliance | warning_open | blocks_robustness_claims | Agents or task-aware baselines may exploit public task templates or scoring shortcuts rather than robust startup decision ability. | Use private holdout execution and model submissions before interpreting high public-suite scores as robust agent ability. |
| 5 | bug_reframed_as_novel_insight | mitigated_by_claim_guardrail | not_blocking_for_current_claims | Unexpected artifacts from implementation or scoring could be narrated as scientific findings. | Do not frame surprising heuristic/provider behavior as a substantive insight unless raw logs, ablations, and independent reruns support it. |
| 6 | methodology_fabrication | mitigated_by_artifact_labels | blocks_submission_ready_claim | The paper's methods could describe tasks, actions, experiments, or provider runs that were planned but not actually executed. | Keep planned experiments explicitly labeled as planned or missing, and update Methods only after generated artifacts prove execution. |
| 7 | frame_lock | frame_guarded_but_open | blocks_external_validity_claims | The benchmark could stay locked into the early startup-profit framing even if evidence supports only a narrower controlled-decision benchmark. | Use conservative benchmark framing until human/expert calibration and hidden holdout evidence justify broader claims. |

## Evidence Details

### Mode 1: implementation_bug_passing_self_review

- Status: `mitigated_not_closed`
- Gate effect: `blocking_warning`
- Rationale: The deterministic artifact path has tests, smoke checks, determinism audit, and bundle integrity, but independent hosted-run logs remain absent.
- Risk: Analysis or simulator code has a plausible-looking bug that is accepted into the paper as a valid result.
- Required response: Keep deterministic replay, bundle integrity, and full test validation in the release loop; add independent hosted-run logs before model-result claims.

Evidence:
- `work/founderbench/tests/test_founderbench.py`: present
- `outputs/founderbench-determinism-audit.md`: present
- `outputs/founderbench-reviewer-smoke.md`: present
- `release/founderbench/BUNDLE-INTEGRITY.md`: present

### Mode 2: hallucinated_citation

- Status: `local_context_verified_external_spotcheck_required`
- Gate effect: `blocking_warning`
- Rationale: References, provenance, and a local citation-context audit are present; final submission still needs external citation-context spot checks against primary pages or PDFs.
- Risk: A cited reference may not exist, may be miscited, or may be used for a claim it does not support.
- Required response: Before submission, run an external citation verification pass over all BibTeX entries and citation contexts.

Evidence:
- `outputs/founderbench-references.bib`: present
- `outputs/founderbench-reference-provenance.json`: present
- `outputs/founderbench-citation-audit.md`: present
- `outputs/founderbench-paper-draft.md`: present

### Mode 3: hallucinated_experimental_result

- Status: `mitigated_for_reported_deterministic_results`
- Gate effect: `blocks_stronger_llm_claims`
- Rationale: Deterministic results are traceable to raw runs, but 6 required experiment groups remain missing.
- Risk: A result table or model-comparison claim could report a number that no executed run produced.
- Required response: Only report deterministic baseline numbers generated from raw output; keep hosted/local LLM result claims excluded until validated provider run files exist.

Evidence:
- `outputs/founderbench-baseline-raw.json`: present
- `outputs/founderbench-paper-tables.md`: present
- `outputs/founderbench-model-comparison.md`: present
- `outputs/founderbench-claim-evidence.md`: present

### Mode 4: shortcut_reliance

- Status: `warning_open`
- Gate effect: `blocks_robustness_claims`
- Rationale: Public-suite ablations exist, but hidden-holdout execution is still required to rule out public-template shortcuts.
- Risk: Agents or task-aware baselines may exploit public task templates or scoring shortcuts rather than robust startup decision ability.
- Required response: Use private holdout execution and model submissions before interpreting high public-suite scores as robust agent ability.

Evidence:
- `outputs/founderbench-action-ablation.md`: present
- `outputs/founderbench-difficulty-calibration.md`: present
- `outputs/founderbench-private-holdout-evaluator-protocol.md`: present
- `outputs/founderbench-reviewer-risk-audit.md`: present

### Mode 5: bug_reframed_as_novel_insight

- Status: `mitigated_by_claim_guardrail`
- Gate effect: `not_blocking_for_current_claims`
- Rationale: 3 stronger claims are explicitly excluded until evidence exists.
- Risk: Unexpected artifacts from implementation or scoring could be narrated as scientific findings.
- Required response: Do not frame surprising heuristic/provider behavior as a substantive insight unless raw logs, ablations, and independent reruns support it.

Evidence:
- `outputs/founderbench-claim-evidence.md`: present
- `outputs/founderbench-paper-evidence-map.md`: present
- `outputs/founderbench-validity-report.md`: present

### Mode 6: methodology_fabrication

- Status: `mitigated_by_artifact_labels`
- Gate effect: `blocks_submission_ready_claim`
- Rationale: The submission gate is not_ready; planned provider runs remain labeled as missing or planned in generated artifacts.
- Risk: The paper's methods could describe tasks, actions, experiments, or provider runs that were planned but not actually executed.
- Required response: Keep planned experiments explicitly labeled as planned or missing, and update Methods only after generated artifacts prove execution.

Evidence:
- `work/founderbench/SPEC.md`: present
- `outputs/founderbench-task-manifest.json`: present
- `outputs/founderbench-action-semantics.md`: present
- `outputs/founderbench-experiment-matrix.md`: present
- `outputs/founderbench-provider-run-status.md`: present

### Mode 7: frame_lock

- Status: `frame_guarded_but_open`
- Gate effect: `blocks_external_validity_claims`
- Rationale: Validity, calibration, and submission-manifest artifacts keep the benchmark framed as controlled simulation, not real startup prediction.
- Risk: The benchmark could stay locked into the early startup-profit framing even if evidence supports only a narrower controlled-decision benchmark.
- Required response: Use conservative benchmark framing until human/expert calibration and hidden holdout evidence justify broader claims.

Evidence:
- `outputs/founderbench-validity-report.md`: present
- `outputs/founderbench-human-calibration-protocol.md`: present
- `outputs/founderbench-human-calibration-analysis.md`: present
- `outputs/founderbench-submission-manifest.md`: present

## Validation

Status: PASS

The failure-mode audit is internally consistent with the current evidence and submission gate.
