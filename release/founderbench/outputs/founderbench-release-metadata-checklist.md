# FounderBench Release Metadata Checklist

Owner-facing public-release metadata checklist for finalizing license and citation files.

Status: `owner_action_required`

## Required Owner Decisions

| ID | Decision | Examples | Target Files |
| --- | --- | --- | --- |
| license_choice | Select a public release license. | MIT, Apache-2.0, BSD-3-Clause | work/moneybench/LICENSE |
| author_metadata | Replace placeholder author metadata in CITATION.cff. | Personal author names, Organization plus maintainers | work/moneybench/CITATION.cff |
| repository_url | Add public repository URL to CITATION.cff. | https://github.com/<owner>/<repo> | work/moneybench/CITATION.cff |
| citation_license_field | Set the CITATION.cff license field to the selected license identifier. | MIT, Apache-2.0, BSD-3-Clause | work/moneybench/CITATION.cff |

## Common License Options

| SPDX ID | Fit | Owner Note |
| --- | --- | --- |
| MIT | Permissive software/data-adjacent artifact reuse with minimal obligations. | Simple and common; does not include explicit patent grant. |
| Apache-2.0 | Permissive reuse with explicit patent license and NOTICE handling. | Often preferred for larger open-source projects and industry use. |
| BSD-3-Clause | Permissive reuse with non-endorsement clause. | Common academic/research software choice. |
| CC-BY-4.0 | Dataset/documentation reuse with attribution. | May be appropriate for documentation/data, but not usually ideal as the only software-code license. |

## CITATION.cff Template

```json
{
  "cff-version": "1.2.0",
  "title": "FounderBench: Evaluating LLM Agents as Startup Operators Under Controlled Resources",
  "message": "If you use FounderBench, please cite the associated paper or this software artifact.",
  "type": "software",
  "authors": [
    {
      "name": "<replace with author name or ORCID-aware author object>"
    }
  ],
  "version": "0.3.0",
  "date-released": "2026-07-15",
  "abstract": "FounderBench is a controlled startup-agent benchmark for evaluating LLM agents on repeated business decisions under bounded resources.",
  "repository-code": "https://github.com/<owner>/<repo>",
  "license": "<SPDX license id selected by project owner>"
}
```

## Finalization Steps

1. Choose one license identifier and add the corresponding full LICENSE text to work/moneybench/LICENSE.
2. Use work/moneybench/LICENSE.template only as a guide; it is not a substitute for the final LICENSE file.
3. Replace placeholder author metadata in work/moneybench/CITATION.cff.
4. Use work/moneybench/CITATION.cff.template only as a guide; it is not a substitute for finalized citation metadata.
5. Replace repository-code with the public repository URL.
6. Set the CITATION.cff license field to the selected SPDX identifier.
7. Remove or update LICENSE-TODO.md so it no longer states that no public release license has been selected.
8. Run python -m moneybench.release regenerate and python -m moneybench.release validate.

## Guardrails

- This artifact does not select a license or author list for the owner.
- Template files are intentionally non-final and must not be treated as release metadata.
- Do not publish the package as open source until work/moneybench/LICENSE exists and CITATION.cff placeholders are replaced.
- If code and documentation/data use different licenses, state both clearly in README and CITATION metadata.

## Validation

Status: PASS

The checklist is internally consistent and intentionally leaves owner-controlled metadata unresolved.
