# Review weakness triage (FounderBench)

Date: 2026-07-21 (second pass)

## What we fixed in the manuscript (this pass)

| Weakness | Paper response |
|---|---|
| Synthetic / deterministic miscalibration | Limitations + design-properties: omit market shocks/adversarial feedback; hybrid verification discussed as alternative |
| Task-aware prior / overfitting | Calibration: privileged family branch; private remix reverse (54.81 vs 57.49); action-space ablation ~19pt drop; gap not pure strategy |
| Strategy vs API/parser errors | Explicit conflation language; official scores keep errors; Err/aff + affected-task diagnostics |
| Single runs / contamination | Already disclosed; private holdout frozen without hosted private leaderboard; limitations expanded |
| Missing ablations / solve ≥70 | Justify 70 as fixed operating cut between heuristic means; list missing protocol/threshold/sensitivity ablations |
| Transition / scoring clarity | Prior pass equations retained; appendix threshold + private remix note |
| Heuristic leakage transparency | Family ID from task ID; hosted prompts lack explicit family label; appendix algorithm bullets |
| Related work: RULERS / LLM-as-judge | New paragraph + cites `hong2026rulers`, `zhao2025onetoken`; hybrid eval situating |
| Hybrid proxy verification | Design-properties paragraph balances determinism vs realism |

## What still needs new work (cannot be fixed by prose alone)

| Weakness | Recommended next experiment |
|---|---|
| Single hosted runs / fragile ranking | Re-run top 3–5 models **≥3 seeds**; report mean±std |
| Hidden / private hosted scores | Run hosted models on frozen private holdout on evaluator host (only if authors choose) |
| Interface-only ablation | Retry budget / reparse-only protocol; optional “clean interface” diagnostic column |
| Environment sensitivity | Sweep observation-noise intensity / cost coefficients on deterministic policies first |
| Human / founder calibration | Small expert study on a subset of tasks vs task-aware heuristic |
| Prompt / threshold ablations | Cross prompt protocols; report solved@60/70/80 as sensitivity |

## Suggested author-response tone

Agree that synthetic dynamics, privileged calibration, and single-run hosted scores limit external validity and ranking strength. Point to outcome-only scoring motivated by RULERS / judge-manipulation results; to private-holdout freeze + deterministic reverse ladder as honesty about overfitting; commit to repeated runs and sensitivity ablations as highest-priority experimental upgrades.

## Files touched

- `paper/kdd2027/main.tex`
- `paper/kdd2027/appendix.tex`
- `outputs/founderbench-references.bib`
- `outputs/founderbench-paper-draft.md`
- `paper/kdd2027/REVIEW-WEAKNESS-RESPONSE.md`
