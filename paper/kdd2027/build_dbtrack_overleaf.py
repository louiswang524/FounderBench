"""Build a named single-blind Overleaf zip for KDD Datasets & Benchmarks Track."""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
STAGE = ROOT / "outputs" / "overleaf-founderbench-kdd2027-dbtrack"
ZIP_PATH = ROOT / "outputs" / "founderbench-kdd2027-overleaf-dbtrack.zip"
PDF_OUT = ROOT / "outputs" / "founderbench-kdd2027-dbtrack.pdf"

AUTHOR = "Yufeng Wang"
EMAIL = "louiswang524@gmail.com"


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected string in {label}:\n{old[:120]}")
    return text.replace(old, new)


def build_main(text: str) -> str:
    # D&B track: single-blind → names listed; review option for line numbers
    # Keep sigconf,review (no anonymous)
    if r"\documentclass[sigconf,review]{acmart}" not in text and r"\documentclass[sigconf,anonymous,review]{acmart}" not in text:
        raise SystemExit("Unexpected documentclass in main.tex")

    text = text.replace(
        r"\documentclass[sigconf,anonymous,review]{acmart}",
        r"\documentclass[sigconf,review]{acmart}",
    )

    authors = (
        rf"\author{{{AUTHOR}}}"
        "\n"
        r"\affiliation{%"
        "\n"
        r"  \institution{Independent Researcher}"
        "\n"
        r"  \country{United States}}"
        "\n"
        rf"\email{{{EMAIL}}}"
        "\n"
        rf"\renewcommand{{\shortauthors}}{{{AUTHOR}}}"
    )
    # Replace any existing author/affiliation/email/shortauthors block
    text, n = re.subn(
        r"\\author\{.*?\}(?:\s*\\affiliation\{.*?\})?\s*\\email\{.*?\}(?:\s*\\renewcommand\{\\shortauthors\}\{.*?\})?",
        lambda _m: authors,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("Failed to set author block in main.tex")
    # Deduplicate accidental double shortauthors
    text = re.sub(
        r"(\\renewcommand\{\\shortauthors\}\{[^}]+\})\s*\1",
        r"\1",
        text,
    )

    text = replace_required(
        text,
        r"\bibliography{../../outputs/founderbench-references}",
        r"\bibliography{founderbench-references}",
        "main.tex",
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
            "main.tex",
        )
    return text


def build_appendix(text: str) -> str:
    text = re.sub(r"^.*?\\maketitle\s*", "", text, count=1, flags=re.S)
    text = re.sub(r"\s*\\end\{document\}\s*$", "\n", text)
    return text


def main() -> None:
    if STAGE.exists():
        shutil.rmtree(STAGE)
    STAGE.mkdir(parents=True)
    (STAGE / "figures").mkdir()

    main_tex = (SRC / "main.tex").read_text(encoding="utf-8")
    (STAGE / "main.tex").write_text(build_main(main_tex), encoding="utf-8")
    (STAGE / "appendix-content.tex").write_text(
        build_appendix((SRC / "appendix.tex").read_text(encoding="utf-8")),
        encoding="utf-8",
    )

    for name in ["table-baselines.tex", "table-models.tex", "table-errors.tex", "main.bbl"]:
        shutil.copy2(SRC / name, STAGE / name)
    shutil.copy2(ROOT / "outputs" / "founderbench-references.bib", STAGE / "founderbench-references.bib")
    for fig in ["benchmark-loop.pdf", "model-leaderboard.pdf", "family-heatmap.pdf"]:
        shutil.copy2(SRC / "figures" / fig, STAGE / "figures" / fig)

    readme = f"""# FounderBench — KDD Datasets & Benchmarks (single-blind)

Track: **Datasets & Benchmarks** (single-blind; author names listed)
Author: {AUTHOR} <{EMAIL}>
Class: `\\documentclass[sigconf,review]{{acmart}}`

## Compile
1. Main document: `main.tex`
2. Compiler: pdfLaTeX + BibTeX
3. Single PDF: content + references + appendix

## Note
Affiliation is set to "Independent Researcher". Edit `main.tex` if you want a university/company affiliation.
"""
    (STAGE / "README-DBTRACK.md").write_text(readme, encoding="utf-8")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in STAGE.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(STAGE).as_posix())

    print(f"STAGE: {STAGE}")
    print(f"ZIP: {ZIP_PATH}")
    print(f"SIZE: {ZIP_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
