"""Generate publication figures and their machine-readable source data."""

from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

from founderbench.analysis import FAMILIES, family_name
from founderbench.paper_tables import PAPER_MODEL_IDS, PROVIDER_RUNS, paper_labeled_runs, provider_status


ROOT = Path(__file__).resolve().parents[2]
PAPER = Path(__file__).resolve().parent
FIGURES = PAPER / "figures"


def validated_models() -> list[dict]:
    runs: list[dict] = []
    for spec in PROVIDER_RUNS:
        if spec["id"] not in PAPER_MODEL_IDS:
            continue
        status = provider_status(spec)
        if status["status"] == "valid":
            runs.extend(paper_labeled_runs(status, status["evidence_path"]))
    return sorted(runs, key=lambda run: run["average_task_score"], reverse=True)


def save(figure: plt.Figure, name: str) -> None:
    figure.savefig(FIGURES / f"{name}.pdf", bbox_inches="tight")
    figure.savefig(FIGURES / f"{name}.png", dpi=220, bbox_inches="tight")
    plt.close(figure)


def benchmark_loop() -> None:
    labels = [
        ("Task card", 0.12, 0.73),
        ("Structured\nobservation", 0.38, 0.73),
        ("LLM policy", 0.64, 0.73),
        ("One of 13\nactions", 0.64, 0.25),
        ("Deterministic\nsimulator", 0.38, 0.25),
        ("Outcome score\nand diagnostics", 0.12, 0.25),
    ]
    fig, ax = plt.subplots(figsize=(7.1, 3.0))
    ax.set_xlim(0, 0.8)
    ax.set_ylim(0, 1)
    ax.axis("off")
    for label, x, y in labels:
        ax.text(
            x,
            y,
            label,
            ha="center",
            va="center",
            fontsize=9,
            bbox={"boxstyle": "round,pad=0.35", "fc": "#edf4fb", "ec": "#35618d"},
        )
    points = [(0.19, 0.73, 0.30, 0.73), (0.46, 0.73, 0.56, 0.73), (0.64, 0.62, 0.64, 0.37)]
    points += [(0.57, 0.25, 0.47, 0.25), (0.30, 0.25, 0.20, 0.25)]
    for x1, y1, x2, y2 in points:
        ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops={"arrowstyle": "->", "lw": 1.4})
    ax.annotate(
        "next step",
        xy=(0.38, 0.62),
        xytext=(0.38, 0.37),
        ha="center",
        fontsize=8,
        arrowprops={"arrowstyle": "->", "lw": 1.4, "connectionstyle": "arc3,rad=-0.45"},
    )
    ax.text(0.74, 0.5, "up to 10\nsteps", ha="center", va="center", fontsize=8, color="#555555")
    save(fig, "benchmark-loop")


def leaderboard(runs: list[dict]) -> None:
    rows = []
    for run in runs:
        error_decisions = run.get("diagnostics", {}).get("provider_errors", 0)
        affected = sum(1 for result in run["results"] if result.get("diagnostics", {}).get("provider_errors", 0))
        rows.append(
            {
                "model": run["policy"],
                "average_score": run["average_task_score"],
                "solved": run["solved"],
                "provider_errors": error_decisions,
                "affected_tasks": affected,
                "err_per_task": round(error_decisions / 50, 3),
                "affected_frac": round(affected / 50, 3),
            }
        )
    with (FIGURES / "leaderboard-data.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)

    labels = [row["model"] for row in reversed(rows)]
    scores = [row["average_score"] for row in reversed(rows)]
    solved = [row["solved"] for row in reversed(rows)]
    affected = [row["affected_tasks"] for row in reversed(rows)]
    err_per_task = [row["err_per_task"] for row in reversed(rows)]
    fig, ax = plt.subplots(figsize=(7.1, 4.3))
    bars = ax.barh(labels, scores, color="#4c78a8")
    ax.set_xlabel("Average task score (0–100)")
    ax.set_xlim(0, 100)
    ax.grid(axis="x", alpha=0.25)
    for bar, score, count, aff, ept in zip(bars, scores, solved, affected, err_per_task):
        marker = f"{score:.1f}  ({count}/50)"
        if aff:
            marker += f"  †{aff}/50 aff ({ept:.2f} err/task)"
        ax.text(score + 1, bar.get_y() + bar.get_height() / 2, marker, va="center", fontsize=7)
    ax.text(
        0.995,
        -0.16,
        "† tasks with ≥1 provider/parser error; err/task = error decisions / 50",
        transform=ax.transAxes,
        ha="right",
        fontsize=6.5,
    )
    save(fig, "model-leaderboard")


def heatmap(runs: list[dict]) -> None:
    family_labels = [family for _, family in FAMILIES]
    matrix = []
    std_matrix = []
    records = []
    for run in runs:
        row = []
        std_row = []
        for family in family_labels:
            scores = [
                float(result["score"]["score"])
                for result in run["results"]
                if family_name(result["task_id"]) == family
            ]
            value = float(np.mean(scores))
            spread = float(np.std(scores, ddof=0))
            row.append(value)
            std_row.append(spread)
            records.append(
                {
                    "model": run["policy"],
                    "family": family,
                    "average_score": round(value, 4),
                    "std": round(spread, 4),
                    "n": len(scores),
                }
            )
        matrix.append(row)
        std_matrix.append(std_row)
    (FIGURES / "family-heatmap-data.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(7.1, 4.6))
    image = ax.imshow(np.asarray(matrix), cmap="viridis", vmin=0, vmax=100, aspect="auto")
    ax.set_yticks(range(len(runs)), [run["policy"] for run in runs], fontsize=7.5)
    ax.set_xticks(
        range(len(family_labels)),
        ["Market", "Revenue", "Retention", "Churn", "Demo", "Pricing", "Runway", "Pivot", "Fundraise", "Channel"],
        rotation=45,
        ha="right",
        fontsize=7,
    )
    for row_index, (row, std_row) in enumerate(zip(matrix, std_matrix)):
        for column_index, (value, spread) in enumerate(zip(row, std_row)):
            color = "white" if value < 45 else "black"
            ax.text(
                column_index,
                row_index,
                f"{value:.0f}\n±{spread:.0f}",
                ha="center",
                va="center",
                fontsize=5.5,
                color=color,
                linespacing=1.05,
            )
    colorbar = fig.colorbar(image, ax=ax, fraction=0.025, pad=0.02)
    colorbar.set_label("Average task score (n=5; ± std)")
    save(fig, "family-heatmap")


def main() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    runs = validated_models()
    if len(runs) != len(PAPER_MODEL_IDS):
        raise RuntimeError(f"Expected {len(PAPER_MODEL_IDS)} validated hosted models, found {len(runs)}.")
    benchmark_loop()
    leaderboard(runs)
    heatmap(runs)
    print(f"Generated figures for {len(runs)} validated models in {FIGURES}")


if __name__ == "__main__":
    main()
