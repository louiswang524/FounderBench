# FounderBench v0.3 Paper Claim Lint

Paper and benchmark-card claim lint for unsupported hosted-LLM, hidden-holdout, and real-world startup-success wording.

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
| paper_draft | pass | outputs/acceleratorbench-paper-draft-v0.1.md | 0 | 0 |
| benchmark_card | pass | outputs/acceleratorbench-benchmark-card.md | 0 | 0 |

## Required Disclosures

### paper_draft

| Phrase | Present |
| --- | --- |
| not yet a comparison of hosted LLM providers | True |
| does not include private task definitions or hidden-suite scores | True |
| real-world startup-prediction claims as unsupported | True |

### benchmark_card

| Phrase | Present |
| --- | --- |
| hosted LLM submissions still need repeated-sampling reports | True |
| full publishable-artifact goal as `not_complete` | True |
| required hosted/local LLM evidence | True |

## Claim Guardrail

This lint is a conservative text check. Passing it does not prove the paper is publication-ready; it only checks that key current-draft overclaiming guardrails are present and selected unsupported positive claims are absent.

## Validation

Status: PASS

The current paper draft and benchmark card include required limitation disclosures and avoid the scanned unsupported positive claims.
