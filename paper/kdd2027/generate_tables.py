"""Generate compact LaTeX tables from validated FounderBench evidence."""

from __future__ import annotations

from pathlib import Path
from statistics import mean, median, quantiles

from founderbench.paper_tables import (
    OUTPUTS,
    PAPER_MODEL_IDS,
    PROVIDER_RUNS,
    load_runs,
    paper_labeled_runs,
    provider_status,
)


PAPER = Path(__file__).resolve().parent


def tex(text: str) -> str:
    return text.replace("&", r"\&").replace("_", r"\_")


def task_scores(run: dict) -> list[float]:
    return [float(result["score"]["score"]) for result in run["results"]]


def iqr(scores: list[float]) -> float:
    if len(scores) < 2:
        return 0.0
    q1, _, q3 = quantiles(scores, n=4, method="inclusive")
    return q3 - q1


def validated_models() -> list[dict]:
    runs: list[dict] = []
    for spec in PROVIDER_RUNS:
        if spec["id"] not in PAPER_MODEL_IDS:
            continue
        status = provider_status(spec)
        if status["status"] == "valid":
            runs.extend(paper_labeled_runs(status, status["evidence_path"]))
    return sorted(runs, key=lambda run: run["average_task_score"], reverse=True)


def render_models(runs: list[dict]) -> str:
    rows = []
    for run in runs:
        scores = task_scores(run)
        errors = run.get("diagnostics", {}).get("provider_errors", 0)
        affected = sum(1 for result in run["results"] if result.get("diagnostics", {}).get("provider_errors", 0))
        public_test = run.get("splits", {}).get("public_test", {}).get("average_task_score", 0)
        rows.append(
            f"{tex(run['policy'])} & {run['average_task_score']:.2f} & "
            f"{median(scores):.1f} & {iqr(scores):.1f} & "
            f"{run['solved']}/50 & {public_test:.2f} & {errors}/{affected} \\\\"
        )
    return "\n".join(
        [
            r"\begin{table}[t]",
            r"\caption{Validated hosted-model results. Each row is one run over the same 50 public tasks. "
            r"Median/IQR are across tasks. ``Pub.\ test'' is the FND-031--050 reporting split "
            r"(also public/visible, not a hidden holdout). Err/aff counts provider-parser error "
            r"decisions and the number of tasks with at least one such decision.}",
            r"\label{tab:models}",
            r"\centering\scriptsize",
            r"\begin{tabular}{lrrrrrr}",
            r"\toprule",
            r"Model & Mean & Med. & IQR & Solved & Pub.\ test & Err/aff \\",
            r"\midrule",
            *rows,
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ]
    )


def render_baselines() -> str:
    runs = sorted(load_runs(OUTPUTS / "founderbench-baseline-raw.json"), key=lambda run: run["average_task_score"], reverse=True)
    rows = [
        f"{tex(run['policy'])} & {run['average_task_score']:.2f} & {run['solved']}/50 \\\\"
        for run in runs
    ]
    return "\n".join(
        [
            r"\begin{table}[t]",
            r"\caption{Deterministic calibration policies on the complete suite. "
            r"The task-aware policy conditions on family identity; see Sec.~\ref{sec:calibration}.}",
            r"\label{tab:baselines}",
            r"\centering\small",
            r"\begin{tabular}{lrr}",
            r"\toprule",
            r"Policy & Score & Solved \\",
            r"\midrule",
            *rows,
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table}",
        ]
    )


def render_errors(runs: list[dict]) -> str:
    rows = []
    for run in runs:
        errored = [result for result in run["results"] if result.get("diagnostics", {}).get("provider_errors", 0)]
        clean = [result for result in run["results"] if not result.get("diagnostics", {}).get("provider_errors", 0)]
        error_decisions = int(run.get("diagnostics", {}).get("provider_errors", 0))
        # Normalize: error decisions per task and fraction of tasks affected.
        per_task = error_decisions / 50
        aff_frac = len(errored) / 50
        categories = run.get("diagnostics", {}).get("provider_error_categories", {}) or {}
        top_cat = "--"
        if categories:
            key = max(categories, key=categories.get)
            top_cat = f"{tex(str(key))} ({categories[key]})"
        affected_mean = (
            f"{mean(float(result['score']['score']) for result in errored):.2f}" if errored else "--"
        )
        clean_mean = f"{mean(float(result['score']['score']) for result in clean):.2f}" if clean else "--"
        rows.append(
            f"{tex(run['policy'])} & {error_decisions} & {per_task:.2f} & {len(errored)} "
            f"({100*aff_frac:.0f}\\%) & {affected_mean} & {clean_mean} & {top_cat} \\\\"
        )
    return "\n".join(
        [
            r"\begin{table*}[t]",
            r"\caption{Provider-error sensitivity with normalized rates. "
            r"Err/task is error decisions divided by 50 tasks; Aff.\ tasks is the count "
            r"(and fraction) of tasks with $\geq$1 error decision. Means stratify observed "
            r"tasks and are not counterfactual corrected scores.}",
            r"\label{tab:errors}",
            r"\centering\scriptsize",
            r"\begin{tabular}{lrrrrrl}",
            r"\toprule",
            r"Model & Errs & Err/task & Aff.\ tasks & Aff.\ mean & Clean mean & Dominant category \\",
            r"\midrule",
            *rows,
            r"\bottomrule",
            r"\end{tabular}",
            r"\end{table*}",
        ]
    )


def main() -> None:
    runs = validated_models()
    if len(runs) != len(PAPER_MODEL_IDS):
        raise RuntimeError(f"Expected {len(PAPER_MODEL_IDS)} validated hosted models, found {len(runs)}.")
    (PAPER / "table-models.tex").write_text(render_models(runs) + "\n", encoding="utf-8")
    (PAPER / "table-baselines.tex").write_text(render_baselines() + "\n", encoding="utf-8")
    (PAPER / "table-errors.tex").write_text(render_errors(runs) + "\n", encoding="utf-8")
    print(f"Generated LaTeX tables for {len(runs)} validated models.")


if __name__ == "__main__":
    main()
