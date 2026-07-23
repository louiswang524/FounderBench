# FounderBench KDD 2027 paper package

This directory contains the ACM manuscript, supplementary appendix, generated tables, publication figures, and the scripts that connect them to validated task-level evidence.

Figure regeneration requires Python, Matplotlib, and NumPy. PDF compilation requires the ACM `acmart` class and a standard BibTeX toolchain.

## Regenerate evidence and figures

Run from the repository root:

```powershell
python paper/kdd2027/analyze_results.py
python -m founderbench.paper_tables --json-output outputs/founderbench-paper-tables.json --markdown-output outputs/founderbench-paper-tables.md
python -m founderbench.model_comparison --json-output outputs/founderbench-model-comparison.json --markdown-output outputs/founderbench-model-comparison.md
python paper/kdd2027/generate_tables.py
python paper/kdd2027/generate_figures.py
```

`analyze_results.py` accepts only provider rows that pass the FounderBench submission validator. It records each evidence path and SHA-256 digest in `outputs/founderbench-paper-model-registry.json`.

## Compile

With `latexmk` and Perl:

```powershell
cd paper/kdd2027
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

MiKTeX can also compile without `latexmk`:

```powershell
pdflatex -interaction=nonstopmode -halt-on-error main.tex
bibtex main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Interpretation boundaries

- Hosted model rows are single runs over 50 visible public tasks.
- Bootstrap intervals estimate task-mix sensitivity, not model-sampling uncertainty.
- Provider and parser errors remain in official scores and are reported as diagnostics.
- FounderBench is synthetic and does not establish real-world startup competence.
