# FounderBench Submission Gate

This generated report combines the publication audit, experiment matrix, provider readiness, claim-evidence report, and license-readiness report into a single go/no-go view.

## Decision

Final status: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| final_status | not_ready |
| gates_passed | 3 |
| gates_failed | 2 |
| required_experiments_missing | 3 |
| providers_ready | 4/11 |
| unsupported_claims | 2 |
| license_release_ready | True |

## Gates

| Gate | Status | Evidence | Blocker |
| --- | --- | --- | --- |
| artifact_and_documentation | pass | `outputs/founderbench-publication-audit.md`, `release/founderbench/SHA256SUMS.json` |  |
| required_experiments | fail | `outputs/founderbench-experiment-matrix.md` | 3 required experiment groups are missing. |
| provider_run_readiness | pass | `outputs/founderbench-provider-readiness.md` |  |
| claim_evidence_alignment | fail | `outputs/founderbench-claim-evidence.md` | 2 stronger claims remain unsupported by current evidence. |
| license_and_citation | pass | `outputs/founderbench-license-readiness.md`, `work/founderbench/CITATION.cff`, `work/founderbench/LICENSE` |  |

## Validation

Status: PASS

The gate report is internally consistent. A `not_ready` final status is expected until required external evidence and owner metadata are complete.
