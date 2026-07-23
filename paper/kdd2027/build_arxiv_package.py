"""Build an arXiv-ready FounderBench preprint package (source zip + PDF)."""

from __future__ import annotations

import re
import shutil
import subprocess
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
STAGE = ROOT / "outputs" / "arxiv-founderbench"
ZIP_PATH = ROOT / "outputs" / "founderbench-arxiv-source.zip"
PDF_OUT = ROOT / "outputs" / "founderbench-arxiv.pdf"

AUTHOR = "Yufeng Wang"
EMAIL = "louiswang524@gmail.com"
TITLE = "FounderBench: Evaluating LLM Agents on Sequential Startup Decisions"


def replace_required(text: str, old: str, new: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected string:\n{old[:140]}")
    return text.replace(old, new)


def build_main(text: str) -> str:
    # Preprint: no review line numbers, named authors
    text = text.replace(
        r"\documentclass[sigconf,anonymous,review]{acmart}",
        r"\documentclass[sigconf]{acmart}",
    )
    text = text.replace(
        r"\documentclass[sigconf,review]{acmart}",
        r"\documentclass[sigconf]{acmart}",
    )
    text = replace_required(
        text,
        r"\settopmatter{printacmref=true}",
        r"\settopmatter{printacmref=false}",
    )
    text = replace_required(
        text,
        r"\pagestyle{plain}",
        r"\pagestyle{plain}"
        "\n"
        r"% Preprint build for arXiv (not the KDD review PDF).",
    )

    authors = (
        rf"\author{{{AUTHOR}}}"
        "\n"
        r"\affiliation{%"
        "\n"
        r"  \institution{Independent Researcher}"
        "\n"
        r"  \city{San Francisco}"
        "\n"
        r"  \state{CA}"
        "\n"
        r"  \country{United States}}"
        "\n"
        rf"\email{{{EMAIL}}}"
        "\n"
        rf"\renewcommand{{\shortauthors}}{{{AUTHOR}}}"
    )
    text, n = re.subn(
        r"\\author\{.*?\}(?:\s*\\affiliation\{.*?\})?\s*\\email\{.*?\}(?:\s*\\renewcommand\{\\shortauthors\}\{.*?\})?",
        lambda _m: authors,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("Failed to set author block")
    text = re.sub(
        r"(\\renewcommand\{\\shortauthors\}\{[^}]+\})\s*\1",
        r"\1",
        text,
    )

    text = replace_required(
        text,
        r"\bibliography{../../outputs/founderbench-references}",
        r"\bibliography{founderbench-references}",
    )

    # Preprint banner after maketitle
    if "Preprint under review" not in text:
        text = replace_required(
            text,
            r"\maketitle",
            "\n".join(
                [
                    r"\maketitle",
                    r"\begin{center}",
                    r"\textit{Preprint. Concurrently under review at ACM~KDD 2027 Datasets \& Benchmarks Track.}",
                    r"\end{center}",
                    r"\vspace{0.5em}",
                ]
            ),
        )

    if r"\input{appendix-content}" not in text:
        text = replace_required(
            text,
            r"\end{document}",
            "\n".join(
                [
                    r"\clearpage",
                    r"\appendix",
                    r"\section*{Appendix}",
                    r"\input{appendix-content}",
                    "",
                    r"\end{document}",
                    "",
                ]
            ),
        )
    return text


def build_appendix(text: str) -> str:
    text = re.sub(r"^.*?\\maketitle\s*", "", text, count=1, flags=re.S)
    text = re.sub(r"\s*\\end\{document\}\s*$", "\n", text)
    return text


def compile_pdf(cwd: Path) -> None:
    cmds = [
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["bibtex", "main"],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
        ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "main.tex"],
    ]
    for cmd in cmds:
        subprocess.run(cmd, cwd=cwd, check=True)


def main() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    (STAGE / "figures").mkdir()

    (STAGE / "main.tex").write_text(build_main((SRC / "main.tex").read_text(encoding="utf-8")), encoding="utf-8")
    (STAGE / "appendix-content.tex").write_text(
        build_appendix((SRC / "appendix.tex").read_text(encoding="utf-8")),
        encoding="utf-8",
    )
    for name in ["table-baselines.tex", "table-models.tex", "table-errors.tex", "main.bbl"]:
        shutil.copy2(SRC / name, STAGE / name)
    shutil.copy2(ROOT / "outputs" / "founderbench-references.bib", STAGE / "founderbench-references.bib")
    for fig in ["benchmark-loop.pdf", "model-leaderboard.pdf", "family-heatmap.pdf"]:
        shutil.copy2(SRC / "figures" / fig, STAGE / "figures" / fig)

    readme = f"""# FounderBench arXiv package

Title: {TITLE}
Author: {AUTHOR} <{EMAIL}>

## KDD policy (Datasets & Benchmarks)

arXiv preprints are allowed for KDD submissions. Sister KDD tracks explicitly state that work already on arXiv/SSRN may be submitted. D&B is **single-blind**, so a named preprint is fine. Still double-check the live CFP before upload: https://kdd2027.kdd.org/datasets-and-benchmarks-track-call-for-papers/

## What to upload to arXiv

**Recommended:** upload the PDF (`founderbench-arxiv.pdf`) *or* this TeX source zip.

### Suggested arXiv metadata
- **Title:** {TITLE}
- **Authors:** {AUTHOR}
- **Primary category:** cs.AI (or cs.LG)
- **Cross-lists (optional):** cs.CL, cs.MA
- **Comments:** Preprint. Under review at ACM KDD 2027 Datasets & Benchmarks Track. 7 content pages + appendix appendix.
- **License:** Choose an arXiv-compatible license you are comfortable with (e.g., CC BY 4.0 or arXiv perpetual non-exclusive).

### Compile (if uploading source)
```
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
Main file: `main.tex` (appendix included).

## Differences from the KDD review PDF
- No `review` line numbers
- Named author block
- Short preprint banner under the title
- Affiliation city filled (San Francisco) to silence acmart warnings — edit if wrong
"""
    (STAGE / "README-ARXIV.md").write_text(readme, encoding="utf-8")

    compile_pdf(STAGE)
    shutil.copy2(STAGE / "main.pdf", PDF_OUT)

    # Source zip without build debris
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    include = {
        "main.tex",
        "appendix-content.tex",
        "table-baselines.tex",
        "table-models.tex",
        "table-errors.tex",
        "main.bbl",
        "founderbench-references.bib",
        "README-ARXIV.md",
        "figures/benchmark-loop.pdf",
        "figures/model-leaderboard.pdf",
        "figures/family-heatmap.pdf",
    }
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in STAGE.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(STAGE).as_posix()
            if rel in include or rel.startswith("figures/") and rel.endswith(".pdf"):
                if path.suffix.lower() in {".aux", ".log", ".out", ".blg", ".pdf"} and path.name != "main.pdf":
                    if path.suffix.lower() == ".pdf" and path.parent.name == "figures":
                        zf.write(path, rel)
                    continue
                if path.name == "main.pdf":
                    continue
                zf.write(path, rel)
        # also include compiled PDF in a separate convenience copy outside zip? user gets PDF_OUT
        zf.write(STAGE / "main.pdf", "founderbench-arxiv.pdf")

    print(f"STAGE: {STAGE}")
    print(f"PDF: {PDF_OUT} ({PDF_OUT.stat().st_size} bytes)")
    print(f"ZIP: {ZIP_PATH} ({ZIP_PATH.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
