# FounderBench License and Citation Readiness

This generated report tracks the owner-controlled metadata required before public release. It does not choose a license; it names the remaining decisions.

## Summary

| Metric | Value |
| --- | --- |
| checks | 8 |
| pass | 4 |
| incomplete | 3 |
| missing | 1 |
| owner_decisions_required | 4 |
| release_ready | False |

## Checks

| ID | Status | Path | Detail |
| --- | --- | --- | --- |
| citation_file_exists | pass | work/moneybench/CITATION.cff | CITATION.cff is present. |
| citation_author_placeholder | incomplete | work/moneybench/CITATION.cff | Author metadata must be finalized. |
| citation_repository_placeholder | pass | work/moneybench/CITATION.cff | Repository URL must be finalized. |
| citation_license_placeholder | incomplete | work/moneybench/CITATION.cff | License metadata must match the selected release license. |
| license_file_exists | missing | work/moneybench/LICENSE | A final LICENSE file should exist for public release. |
| license_template_exists | pass | work/moneybench/LICENSE.template | A non-final license template should help the owner create the final LICENSE file. |
| citation_template_exists | pass | work/moneybench/CITATION.cff.template | A non-final citation template should help the owner replace placeholders safely. |
| license_todo_present | incomplete | work/moneybench/LICENSE-TODO.md | LICENSE-TODO.md documents the unresolved owner decision. |

## Required Owner Decisions

| ID | Decision | Why It Matters | Target Files |
| --- | --- | --- | --- |
| license_choice | Select a public release license. | External users need explicit reuse, modification, and redistribution terms. | work/moneybench/LICENSE |
| author_metadata | Replace placeholder author metadata in CITATION.cff. | Citation metadata must identify artifact authors before public release. | work/moneybench/CITATION.cff |
| repository_url | Add public repository URL to CITATION.cff. | Reviewers and users need a stable source-code location. | work/moneybench/CITATION.cff |
| citation_license_field | Set the CITATION.cff license field to the selected license identifier. | Citation tooling expects machine-readable license metadata. | work/moneybench/CITATION.cff |

## Validation

Status: PASS

The report is internally valid. Public release readiness remains false until all checks pass.
