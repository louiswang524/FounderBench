# FounderBench Citation Context Audit

This generated audit checks local consistency between the paper draft, BibTeX entries, and reference provenance. It is deliberately conservative and still requires external citation-context verification before final submission.

External status: `local_context_verified_external_spotcheck_required`

## Summary

| Metric | Value |
| --- | --- |
| references | 14 |
| paper_reference_lines | 26 |
| contexts_checked | 14 |
| contiguous_numbering | True |
| rows_with_context | 14 |
| rows_matching_bibtex_order | 14 |
| context_term_matches | 14 |
| reference_title_hint_matches | 14 |

## Citation Checks

| No. | Key | Claim Type | Contexts | Context Terms | Title Hint | Source |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | yao2023react | agent reasoning/action framing | 1 | yes | yes | https://arxiv.org/bibtex/2210.03629 |
| 2 | schick2023toolformer | tool-use training | 1 | yes | yes | https://arxiv.org/bibtex/2302.04761 |
| 3 | wang2023voyager | long-horizon embodied agent | 1 | yes | yes | https://arxiv.org/bibtex/2305.16291 |
| 4 | liu2025agentbench | general agent benchmark | 2 | yes | yes | https://openreview.net/forum?id=zAdUB0aCTQ |
| 5 | mialon2023gaia | general assistant benchmark | 4 | yes | yes | https://arxiv.org/bibtex/2311.12983 |
| 6 | jimenez2024swebench | software engineering benchmark | 5 | yes | yes | https://arxiv.org/bibtex/2310.06770 |
| 7 | zhou2024webarena | web-agent environment benchmark | 6 | yes | yes | https://arxiv.org/bibtex/2307.13854 |
| 8 | yao2024taubench | tool-agent-user interaction benchmark | 2 | yes | yes | https://arxiv.org/bibtex/2406.12045 |
| 9 | xu2025theagentcompany | workplace/company agent benchmark | 2 | yes | yes | https://arxiv.org/bibtex/2412.14161 |
| 10 | drouin2024workarena | enterprise web-agent benchmark | 1 | yes | yes | https://servicenow.github.io/WorkArena/ |
| 11 | liu2026econwebarena | economic web-agent benchmark | 1 | yes | yes | https://arxiv.org/bibtex/2506.08136 |
| 12 | han2026enterprisearena | long-horizon enterprise allocation benchmark | 1 | yes | yes | https://arxiv.org/bibtex/2603.23638 |
| 13 | gebru2021datasheets | dataset and benchmark documentation | 2 | yes | yes | https://dl.acm.org/doi/10.1145/3458723 |
| 14 | liang2023holistic | transparent multi-metric model evaluation | 2 | yes | yes | https://openreview.net/forum?id=iO4LZibEqW |

## Limitations

- This audit checks local consistency between the paper draft, BibTeX entries, and recorded provenance.
- It does not prove that every cited paper supports every sentence in the surrounding paragraph.
- A final submission should still run external citation-context verification against primary paper pages or PDFs.

## Validation

Status: PASS

The local citation-context audit is internally consistent with the current paper draft and reference artifacts.
