# FounderBench Submission Gate

This generated report combines the publication audit, experiment matrix, provider readiness, claim-evidence report, and license-readiness report into a single go/no-go view.

## Decision

Final status: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| final_status | not_ready |
| gates_passed | 1 |
| gates_failed | 4 |
| required_experiments_missing | 6 |
| providers_ready | 0/12 |
| unsupported_claims | 3 |
| license_release_ready | False |

## Gates

| Gate | Status | Evidence | Blocker |
| --- | --- | --- | --- |
| artifact_and_documentation | pass | `outputs/founderbench-publication-audit.md`, `release/founderbench/SHA256SUMS.json` |  |
| required_experiments | fail | `outputs/founderbench-experiment-matrix.md` | 6 required experiment groups are missing. |
| provider_run_readiness | fail | `outputs/founderbench-provider-readiness.md` | Only 0/12 provider configurations are ready. |
| claim_evidence_alignment | fail | `outputs/founderbench-claim-evidence.md` | 3 stronger claims remain unsupported by current evidence. |
| license_and_citation | fail | `outputs/founderbench-license-readiness.md`, `work/founderbench/CITATION.cff`, `work/founderbench/LICENSE-TODO.md` | License/citation metadata is not public-release ready. |

## Validation

Status: PASS

The gate report is internally consistent. A `not_ready` final status is expected until required external evidence and owner metadata are complete.
