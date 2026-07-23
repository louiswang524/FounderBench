# Benchmark-paper writing review → FounderBench revision notes

Date: 2026-07-20

## Papers studied for writing pattern

| Paper | What to steal for FounderBench |
|---|---|
| **SWE-bench** | Abstract = gap → named suite + scale → task in one sentence → why hard → headline % → release. Intro opens with evaluation saturation, then concrete prior-benchmark failure. Early design figure. Explicit “features/properties” subsection. |
| **WebArena** | Intro lists *concrete limitations of prior environments* (simplified, static, surface-form grading). Formal environment framing. Strong human vs model gap sentence. Functional correctness as the design thesis. |
| **GAIA** | Abstract states a clear *philosophy* (easy for humans, hard for AI; short verifiable answers). Numbers in abstract. Hidden-answer / leaderboard honesty. |
| **Datasheets / HELM** | Documentation and multi-metric reporting as first-class contributions, not appendix fluff. |
| **NeurIPS DB track practice** | Accessibility, documentation, reproducibility, responsible use called out as review axes. |

## Diagnosis of prior FounderBench draft

1. Abstract front-loaded caveats and under-sold the capability gap (task-aware 80.90 vs hosted ≤67.69).
2. Introduction lacked a crisp “prior benchmarks fail because…” paragraph and buried the design principle.
3. Related work was a citation list; strong papers use contrast axes and end each cluster with “we differ by X.”
4. Design section jumped to episode mechanics without a formal task formulation or a “design properties” block (SWE-bench-style).
5. Results delayed the takeaway; SWE-bench/WebArena lead with the gap, then analyze why.
6. Reproducibility was a laundry list; DB reviewers prefer checklist-style axes.

## Revisions applied

- Rewrote abstract to Challenge → Suite → Task → Headline numbers → Release → Short disclosure.
- Rewrote introduction around the rhetoric-vs-outcome gap, early figure pointer, contribution bullets with role labels (Benchmark / Outcome protocol / Empirical baselines / Auditable release).
- Reorganized related work into contrast paragraphs; added YC-Bench, Terminal-Bench, LHTB, and χ-Bench with a positioning table.
- Added formal episode tuple and a **Design properties** subsection.
- Tightened results takeaways (capability ladder; >13-point hosted gap; named rank reversals).
- Compressed reproducibility into review axes; kept limitations honest.
- Synced `outputs/founderbench-paper-draft.md`; restored required claim-lint disclosure phrases.

## Files touched

- `paper/kdd2027/main.tex` (primary manuscript)
- `outputs/founderbench-paper-draft.md` (synced prose)
- This note: `paper/kdd2027/WRITING-REVISION-NOTES.md`
