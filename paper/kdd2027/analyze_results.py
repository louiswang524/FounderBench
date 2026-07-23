"""Freeze validated model evidence and generate paper-focused diagnostics."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from statistics import mean

from founderbench.analysis import FAMILIES, bootstrap_mean_ci, family_name
from founderbench.paper_tables import (
    PAPER_MODEL_IDS,
    PROVIDER_RUNS,
    ROOT,
    load_runs,
    paper_labeled_runs,
    provider_status,
)


PAPER = Path(__file__).resolve().parent
OUTPUTS = ROOT / "outputs"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collect() -> tuple[list[dict], list[dict]]:
    registry = []
    runs = []
    for spec in PROVIDER_RUNS:
        if spec["id"] not in PAPER_MODEL_IDS:
            continue
        status = provider_status(spec)
        if status["status"] != "valid":
            continue
        path = ROOT / status["evidence_path"]
        labeled = paper_labeled_runs(status, status["evidence_path"])
        if len(labeled) != 1:
            raise RuntimeError(f"Paper registry expects one run per model, found {len(labeled)} for {spec['id']}.")
        run = labeled[0]
        diagnostics = run.get("diagnostics", {})
        audited_model_ids = sorted(
            {
                str(call["model"])
                for result in run.get("results", [])
                for event in result.get("events", [])
                for call in event.get("provider_calls", [])
                if call.get("model")
            }
        )
        registry.append(
            {
                "id": spec["id"],
                "model": spec["label"],
                "model_label_source": "variant-specific paper registry and evidence path",
                "audited_model_identifiers": audited_model_ids,
                "provider_policy": spec["policy"],
                "benchmark_version": run["benchmark_version"],
                "run_seed": run["run_seed"],
                "tasks": run["tasks"],
                "average_task_score": run["average_task_score"],
                "solved": run["solved"],
                "provider_errors": diagnostics.get("provider_errors", 0),
                "provider_error_categories": diagnostics.get("provider_error_categories", {}),
                "provider_prompt_tokens": diagnostics.get("provider_prompt_tokens", 0),
                "provider_completion_tokens": diagnostics.get("provider_completion_tokens", 0),
                "provider_total_tokens": diagnostics.get("provider_total_tokens", 0),
                "estimated_provider_cost_usd": diagnostics.get("estimated_provider_cost_usd", 0.0),
                "evidence_path": status["evidence_path"],
                "submission_report": status["report"],
                "sha256": sha256(path),
                "validation_status": "valid",
                "evidence_kind": status["evidence_kind"],
            }
        )
        runs.append(run)
    return registry, runs


def analyze(registry: list[dict], runs: list[dict]) -> dict:
    models = []
    for run in sorted(runs, key=lambda row: row["average_task_score"], reverse=True):
        scores = [float(result["score"]["score"]) for result in run["results"]]
        score_low, score_high = bootstrap_mean_ci(scores)
        errored = [result for result in run["results"] if result.get("diagnostics", {}).get("provider_errors", 0)]
        clean = [result for result in run["results"] if not result.get("diagnostics", {}).get("provider_errors", 0)]
        families = {}
        for _, family in FAMILIES:
            family_results = [result for result in run["results"] if family_name(result["task_id"]) == family]
            families[family] = {
                "average_task_score": round(mean(float(result["score"]["score"]) for result in family_results), 2),
                "solved": sum(bool(result["score"]["passed"]) for result in family_results),
            }
        models.append(
            {
                "model": run["policy"],
                "average_task_score": run["average_task_score"],
                "solved": run["solved"],
                "solve_rate": run["solve_rate"],
                "task_mix_score_ci_95": [round(score_low, 2), round(score_high, 2)],
                "provider_error_decisions": run.get("diagnostics", {}).get("provider_errors", 0),
                "tasks_with_provider_errors": len(errored),
                "errored_task_mean": round(mean(float(result["score"]["score"]) for result in errored), 2) if errored else None,
                "clean_task_mean": round(mean(float(result["score"]["score"]) for result in clean), 2) if clean else None,
                "families": families,
            }
        )
    rank_reversals = []
    for left in models:
        for right in models:
            if left["average_task_score"] > right["average_task_score"] and left["solved"] < right["solved"]:
                rank_reversals.append(
                    {
                        "higher_average": left["model"],
                        "higher_solved": right["model"],
                        "average_gap": round(left["average_task_score"] - right["average_task_score"], 2),
                        "solved_gap": right["solved"] - left["solved"],
                    }
                )
    calibration_runs = load_runs(OUTPUTS / "founderbench-baseline-raw.json")
    task_aware = next(run for run in calibration_runs if run["policy"] == "task_heuristic")
    family_comparison = []
    for _, family in FAMILIES:
        task_aware_scores = [
            float(result["score"]["score"])
            for result in task_aware["results"]
            if family_name(result["task_id"]) == family
        ]
        hosted_rows = [
            {
                "model": run["policy"],
                "average_task_score": round(
                    mean(
                        float(result["score"]["score"])
                        for result in run["results"]
                        if family_name(result["task_id"]) == family
                    ),
                    2,
                ),
            }
            for run in runs
        ]
        best_hosted = max(hosted_rows, key=lambda row: row["average_task_score"])
        task_aware_mean = round(mean(task_aware_scores), 2)
        family_comparison.append(
            {
                "family": family,
                "task_aware_score": task_aware_mean,
                "best_hosted_model": best_hosted["model"],
                "best_hosted_score": best_hosted["average_task_score"],
                "task_aware_leads_all_hosted": task_aware_mean > best_hosted["average_task_score"],
            }
        )
    return {
        "benchmark": "FounderBench",
        "benchmark_version": "0.3.0",
        "generated_from_validated_single_runs": True,
        "interval_interpretation": "Task-mix uncertainty only; not repeated-run or model-sampling uncertainty.",
        "validated_model_count": len(registry),
        "models": models,
        "solved_average_rank_reversals": rank_reversals,
        "task_aware_family_comparison": family_comparison,
    }


def markdown(registry: list[dict], analysis: dict) -> str:
    lines = [
        "# FounderBench KDD Paper Analysis",
        "",
        f"Validated single-run model rows: **{len(registry)}**.",
        "",
        "Bootstrap intervals below estimate sensitivity to the 50-task mix. They are not repeated-run or model-sampling uncertainty.",
        "",
        "## Frozen model registry",
        "",
        "| Model | Score | Solved | Errors | Evidence | SHA-256 |",
        "|---|---:|---:|---:|---|---|",
    ]
    for row in sorted(registry, key=lambda item: item["average_task_score"], reverse=True):
        lines.append(
            f"| {row['model']} | {row['average_task_score']:.2f} | {row['solved']}/50 | "
            f"{row['provider_errors']} | `{row['evidence_path']}` | `{row['sha256']}` |"
        )
    lines += [
        "",
        "## Provider-error sensitivity",
        "",
        "This is a diagnostic stratification, not a counterfactual corrected leaderboard. Error-free and errored task subsets differ in composition.",
        "",
        "| Model | Error decisions | Affected tasks | Mean on affected tasks | Mean on unaffected tasks |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in analysis["models"]:
        affected = "—" if row["errored_task_mean"] is None else f"{row['errored_task_mean']:.2f}"
        clean = "—" if row["clean_task_mean"] is None else f"{row['clean_task_mean']:.2f}"
        lines.append(
            f"| {row['model']} | {row['provider_error_decisions']} | {row['tasks_with_provider_errors']} | "
            f"{affected} | {clean} |"
        )
    lines += [
        "",
        "## Solved-versus-average rank reversals",
        "",
        "These reversals occur because solved count thresholds each task at 70, while average score preserves distances above and below that threshold.",
        "",
        "| Higher average-score model | Higher solved-count model | Average gap | Solved gap |",
        "|---|---|---:|---:|",
    ]
    for row in analysis["solved_average_rank_reversals"]:
        lines.append(
            f"| {row['higher_average']} | {row['higher_solved']} | {row['average_gap']:.2f} | {row['solved_gap']} |"
        )
    lines += [
        "",
        "## Task-aware family comparison",
        "",
        "| Family | Task-aware score | Best hosted model | Best hosted score | Task-aware leads |",
        "|---|---:|---|---:|---|",
    ]
    for row in analysis["task_aware_family_comparison"]:
        lines.append(
            f"| {row['family']} | {row['task_aware_score']:.2f} | {row['best_hosted_model']} | "
            f"{row['best_hosted_score']:.2f} | {'yes' if row['task_aware_leads_all_hosted'] else 'no'} |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    registry, runs = collect()
    collected_ids = {row["id"] for row in registry}
    if collected_ids != PAPER_MODEL_IDS:
        missing = sorted(PAPER_MODEL_IDS - collected_ids)
        extra = sorted(collected_ids - PAPER_MODEL_IDS)
        raise RuntimeError(f"Paper registry is incomplete or changed; missing={missing}, extra={extra}.")
    analysis = analyze(registry, runs)
    (OUTPUTS / "founderbench-paper-model-registry.json").write_text(json.dumps(registry, indent=2), encoding="utf-8")
    (OUTPUTS / "founderbench-paper-analysis.json").write_text(json.dumps(analysis, indent=2), encoding="utf-8")
    (OUTPUTS / "founderbench-paper-analysis.md").write_text(markdown(registry, analysis), encoding="utf-8")
    print(f"Froze {len(registry)} validated model rows and generated diagnostics.")


if __name__ == "__main__":
    main()
