# FounderBench Paper Claim Lint

Markdown and LaTeX paper claim lint for single-run hosted evidence, hidden-holdout boundaries, and real-world startup-success wording.

## Summary

| Metric | Value |
| --- | --- |
| targets | 2 |
| passed | 2 |
| failed | 0 |
| forbidden_hits | 0 |
| missing_required_disclosures | 0 |

## Target Status

| Target | Status | Path | Missing Disclosures | Forbidden Hits |
| --- | --- | --- | --- | --- |
| paper_draft | pass | outputs/founderbench-paper-draft.md | 0 | 0 |
| kdd_latex | pass | paper/kdd2027/main.tex | 0 | 0 |

## Required Disclosures

### paper_draft

| Phrase | Present |
| --- | --- |
| all hosted rows are single runs on visible public tasks | True |
| no human-founder calibration | True |
| no official private leaderboard | True |
| scores do not establish real-world startup competence | True |

### kdd_latex

| Phrase | Present |
| --- | --- |
| all hosted results are one run per configuration | True |
| both sets are released and visible | True |
| no human-founder calibration | True |
| no official hidden leaderboard | True |
| not evidence that a model can run a real company | True |

## Claim Guardrail

This lint is a conservative text check. Passing it does not prove the paper is publication-ready; it only checks that key current-draft overclaiming guardrails are present and selected unsupported positive claims are absent.

## Validation

Status: PASS

The current paper draft and benchmark card include required limitation disclosures and avoid the scanned unsupported positive claims.
