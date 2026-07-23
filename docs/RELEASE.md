# Release And Publication Checklist

Public repository: https://github.com/louiswang524/FounderBench

## Done for v0.3.0 public polish

1. Root `LICENSE` and `work/founderbench/LICENSE` set to **MIT**.
2. `CITATION.cff` (root + package) filled with author, title, license, and repo URL.
3. `pyproject.toml` license/author/description updated.
4. Top-level `README.md` rewritten for GitHub users.

## Before each public push

1. Run `python -m founderbench.release validate` (from repo root with editable install).
2. Run `python -m founderbench.release bundle` if shipping the supplementary bundle.
3. Confirm `.env` and holdout secrets are not staged (`git status`).
4. Review `outputs/founderbench-submission-gate.md` and `outputs/founderbench-publication-audit.md` after regenerating audits.

## Still out of scope / intentional

- Private holdout task definitions and evaluator secret remain unpublished.
- Hosted private-holdout model leaderboard is not claimed until run on an evaluator host.
- Do not claim real-world company competence from FounderBench scores.
