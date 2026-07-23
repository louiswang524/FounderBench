"""Build an anonymous double-blind Overleaf zip for KDD Research Track."""

from __future__ import annotations

import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = Path(__file__).resolve().parent
STAGE = ROOT / "outputs" / "overleaf-founderbench-kdd2027-anonymous"
ZIP_PATH = ROOT / "outputs" / "founderbench-kdd2027-overleaf-anonymous.zip"


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"Missing expected string in {label}:\n{old[:120]}")
    return text.replace(old, new)


def build_main(text: str) -> str:
    text = replace_required(
        text,
        r"\documentclass[sigconf,review]{acmart}",
        r"\documentclass[sigconf,anonymous,review]{acmart}",
        "main.tex",
    )
    text = replace_required(
        text,
        r"\settopmatter{printacmref=true}",
        r"\settopmatter{printacmref=false}",
        "main.tex",
    )

    anon_authors = (
        r"\author{Anonymous Author(s)}"
        "\n"
        r"\affiliation{%"
        "\n"
        r"  \institution{Anonymous Institution}"
        "\n"
        r"  \city{Anonymous City}"
        "\n"
        r"  \country{Anonymous Country}}"
        "\n"
        r"\renewcommand{\shortauthors}{Anonymous Author(s)}"
    )
    text, n = re.subn(
        r"\\author\{.*?\}(?:\s*\\affiliation\{.*?\})?\s*\\email\{.*?\}(?:\s*\\renewcommand\{\\shortauthors\}\{.*?\})?",
        lambda _m: anon_authors,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("Failed to anonymize author block in main.tex")
    text = re.sub(
        r"(\\renewcommand\{\\shortauthors\}\{Anonymous Author\(s\)\})\s*\1",
        r"\1",
        text,
    )

    replacements = [
        (
            "We release tasks, simulator and scoring code, adapters, validated task-level results, and generation scripts.",
            "An anonymized artifact with tasks, simulator and scoring code, adapters, validated task-level results, and generation scripts will be released upon acceptance.",
        ),
        (
            r"  \item \textbf{Auditable release.} Task-level evidence, adapters, validation, task-mix analyses, datasheet-style documentation, and generators that regenerate every reported table and figure.",
            r"  \item \textbf{Auditable artifact.} Task-level evidence, adapters, validation, task-mix analyses, datasheet-style documentation, and generators that regenerate every reported table and figure (to be released upon acceptance).",
        ),
        (
            "Exact schemas ship with the artifact.",
            "Exact schemas are included in the supplementary artifact.",
        ),
        (
            "Full action-effect rules are in the appendix and released source.",
            "Full action-effect rules are in the appendix and supplementary source.",
        ),
        (
            "Complete component weights for all ten families are in the released rubric and appendix.",
            "Complete component weights for all ten families are in the supplementary rubric and appendix.",
        ),
        (
            "We prioritize full determinism for v0.3 so every published score is re-executable from the artifact; the cost is reduced ecological validity under market shocks and adversarial conditions that a stochastic or human-in-the-loop layer would capture.",
            "We prioritize full determinism for v0.3 so every published score is re-executable from the supplementary artifact; the cost is reduced ecological validity under market shocks and adversarial conditions that a stochastic or human-in-the-loop layer would capture.",
        ),
        (
            "Released action-space ablations further show",
            "Action-space ablations in the supplementary artifact further show",
        ),
        (
            "The release includes Python source, task definitions, simulator and scoring code, adapters, a resumable runner, raw task-level JSON, submission reports, generated tables and figures, a benchmark card, datasheet, task cards, scoring rubric, prompt protocol, environment report, and checksums.",
            "The supplementary artifact includes Python source, task definitions, simulator and scoring code, adapters, a resumable runner, raw task-level JSON, submission reports, generated tables and figures, a benchmark card, datasheet, task cards, scoring rubric, prompt protocol, environment report, and checksums; a public archival release is planned upon acceptance.",
        ),
        (
            "Accessibility still depends on final public repository and license metadata.",
            "Public accessibility will depend on the post-acceptance repository and license metadata.",
        ),
        (
            "The release also freezes a 20-task private holdout",
            "The benchmark also freezes a 20-task private holdout",
        ),
        (
            "The release ties every reported number to executable evidence.",
            "Every reported number is tied to executable evidence in the supplementary artifact.",
        ),
        (
            r"\bibliography{../../outputs/founderbench-references}",
            r"\bibliography{founderbench-references}",
        ),
    ]
    for old, new in replacements:
        text = replace_required(text, old, new, "main.tex")

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
    replacements = [
        (
            "Complete human-readable cards and executable setup and scoring functions are included in the artifact.",
            "Complete human-readable cards and executable setup and scoring functions are included in the supplementary artifact.",
        ),
        (
            "The exact generated protocol and prompt hashes are released in\n\\texttt{outputs/founderbench-prompt-protocol.md}.",
            "The exact generated protocol and prompt hashes are included in the supplementary file\n\\texttt{founderbench-prompt-protocol.md}.",
        ),
        (
            "All constants and action branches are in the released \\texttt{env.py}.",
            "All constants and action branches are in the supplementary \\texttt{env.py}.",
        ),
        (
            "The complete per-family rubric is in \\texttt{outputs/founderbench-score-rubric.md}.",
            "The complete per-family rubric is in the supplementary \\texttt{founderbench-score-rubric.md}.",
        ),
        (
            "The paper's sensitivity artifact reports",
            "The supplementary sensitivity artifact reports",
        ),
        (
            "\\section{Artifact Map}\nThe paper package contains:",
            "\\section{Artifact Map}\nThe supplementary package contains:",
        ),
    ]
    for old, new in replacements:
        text = replace_required(text, old, new, "appendix.tex")
    return text


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

    readme = """# FounderBench — Anonymous Overleaf package (double-blind)

Prepared for KDD-style **double-blind** review:
`\\documentclass[sigconf,anonymous,review]{acmart}`

## Important track note
- **KDD Research Track**: double-blind → use this package.
- **KDD Datasets & Benchmarks Track**: currently **single-blind** (author names should be listed). Do **not** use this anonymous package for D&B unless the CFP changes.

## Compile
1. Main document: `main.tex`
2. Compiler: pdfLaTeX + BibTeX
3. Produces a **single PDF**: content + references + optional appendix
4. `main.bbl` is included as a BibTeX fallback

## Anonymity checklist applied
- `anonymous,review` class options
- Author names/affiliations suppressed
- No acknowledgments
- No public repository URL
- Release language softened to “upon acceptance” / supplementary artifact
- Appendix merged after references (KDD single-PDF requirement)
"""
    (STAGE / "README-ANONYMOUS.md").write_text(readme, encoding="utf-8")

    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in STAGE.rglob("*"):
            if path.is_file():
                zf.write(path, path.relative_to(STAGE).as_posix())

    print(f"STAGE: {STAGE}")
    print(f"ZIP: {ZIP_PATH}")
    print(f"SIZE: {ZIP_PATH.stat().st_size}")
    for path in sorted(STAGE.rglob("*")):
        if path.is_file():
            print(f"  {path.relative_to(STAGE).as_posix()}")


if __name__ == "__main__":
    main()
