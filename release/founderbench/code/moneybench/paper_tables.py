from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import ci_rows, difficulty_rows, family_rows, markdown_table, pairwise_rows, policy_rows
from .submission import validate_run


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
VERSION = "0.3.0"


PROVIDER_RUNS = [
    {
        "id": "openai_hosted_baseline",
        "policy": "openai",
        "path": "outputs/founderbench-openai.json",
        "report": "outputs/founderbench-openai-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-openai-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-openai-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "deepseek_hosted_baseline",
        "policy": "deepseek",
        "path": "outputs/founderbench-deepseek.json",
        "report": "outputs/founderbench-deepseek-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-deepseek-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-deepseek-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "deepseek_self_consistency_k3",
        "policy": "deepseek_sc",
        "path": "outputs/founderbench-deepseek-sc-k3.json",
        "report": "outputs/founderbench-deepseek-sc-k3-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-deepseek-sc-k3-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-deepseek-sc-k3-repeats-submission-report.md",
        "family": "hosted_llm_ablation",
    },
    {
        "id": "anthropic_hosted_baseline",
        "policy": "anthropic",
        "path": "outputs/founderbench-anthropic.json",
        "report": "outputs/founderbench-anthropic-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-anthropic-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-anthropic-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "gemini_hosted_baseline",
        "policy": "gemini",
        "path": "outputs/founderbench-gemini.json",
        "report": "outputs/founderbench-gemini-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-gemini-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-gemini-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "kimi_hosted_baseline",
        "policy": "kimi",
        "path": "outputs/founderbench-kimi.json",
        "report": "outputs/founderbench-kimi-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-kimi-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-kimi-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "qwen_hosted_baseline",
        "policy": "qwen",
        "path": "outputs/founderbench-qwen.json",
        "report": "outputs/founderbench-qwen-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-qwen-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-qwen-repeats-submission-report.md",
        "family": "hosted_llm",
    },
    {
        "id": "mistral_hosted_baseline",
        "policy": "mistral",
        "path": "outputs/founderbench-mistral.json",
        "report": "outputs/founderbench-mistral-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-mistral-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-mistral-repeats-submission-report.md",
        "family": "hosted_llm_optional",
    },
    {
        "id": "glm_hosted_baseline",
        "policy": "glm",
        "path": "outputs/founderbench-glm.json",
        "report": "outputs/founderbench-glm-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-glm-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-glm-repeats-submission-report.md",
        "family": "hosted_llm_optional",
    },
    {
        "id": "xai_hosted_baseline",
        "policy": "xai",
        "path": "outputs/founderbench-xai.json",
        "report": "outputs/founderbench-xai-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-xai-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-xai-repeats-submission-report.md",
        "family": "hosted_llm_optional",
    },
    {
        "id": "llama_open_weight_baseline",
        "policy": "llama",
        "path": "outputs/founderbench-llama.json",
        "report": "outputs/founderbench-llama-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-llama-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-llama-repeats-submission-report.md",
        "family": "open_weight",
    },
    {
        "id": "local_open_source_baseline",
        "policy": "llm",
        "path": "outputs/founderbench-local-open-model.json",
        "report": "outputs/founderbench-local-open-model-submission-report.md",
        "repeat_bundle_path": "outputs/founderbench-local-open-model-repeats.json",
        "repeat_bundle_report": "outputs/founderbench-local-open-model-repeats-submission-report.md",
        "family": "open_source",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_runs(path: Path) -> list[dict[str, Any]]:
    payload = load_json(path)
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict) and "results" in payload:
        return [payload]
    if isinstance(payload, dict) and isinstance(payload.get("runs"), list):
        return payload["runs"]
    raise ValueError(f"Unsupported run payload shape in {path}")


def _validate_run_file(path: Path) -> tuple[list[dict[str, Any]], list[str]]:
    runs = load_runs(path)
    problems: list[str] = []
    for run in runs:
        problems.extend(validate_run(run))
    return runs, problems


def provider_status(spec: dict[str, str]) -> dict[str, Any]:
    path = ROOT / spec["path"]
    report_path = ROOT / spec["report"]
    bundle_path = ROOT / spec["repeat_bundle_path"]
    bundle_report_path = ROOT / spec["repeat_bundle_report"]
    row: dict[str, Any] = {
        **spec,
        "status": "missing",
        "exists": path.exists(),
        "submission_report_exists": report_path.exists(),
        "repeat_bundle_exists": bundle_path.exists(),
        "repeat_bundle_report_exists": bundle_report_path.exists(),
        "evidence_path": "",
        "evidence_kind": "",
        "runs": 0,
        "problems": [],
    }

    candidates = [
        ("repeat_bundle", bundle_path, bundle_report_path, spec["repeat_bundle_path"], spec["repeat_bundle_report"]),
        ("single_run", path, report_path, spec["path"], spec["report"]),
    ]
    invalid_problems: list[str] = []
    selected_runs: list[dict[str, Any]] = []
    selected_path: Path | None = None
    selected_kind = ""
    selected_rel = ""
    for kind, candidate_path, candidate_report, candidate_rel, report_rel in candidates:
        if not candidate_path.exists():
            continue
        try:
            runs, problems = _validate_run_file(candidate_path)
        except Exception as exc:  # noqa: BLE001 - report malformed external submissions.
            invalid_problems.append(f"{candidate_rel}: {exc}")
            continue
        if not candidate_report.exists():
            problems.append(f"Missing validation report {report_rel}")
        if problems:
            invalid_problems.extend(f"{candidate_rel}: {problem}" for problem in problems)
            continue
        selected_runs = runs
        selected_path = candidate_path
        selected_kind = kind
        selected_rel = candidate_rel
        break

    if not selected_runs or selected_path is None:
        row["problems"] = invalid_problems or [f"Missing {spec['path']} or {spec['repeat_bundle_path']}"]
        row["status"] = "invalid" if invalid_problems else "missing"
        return row

    runs = selected_runs
    row["bytes"] = selected_path.stat().st_size
    row["sha256"] = sha256(selected_path)
    row["runs"] = len(runs)
    row["status"] = "valid"
    row["evidence_path"] = selected_rel
    row["evidence_kind"] = selected_kind
    best = sorted(runs, key=lambda item: item.get("average_task_score", 0), reverse=True)[0]
    row["average_task_score"] = best.get("average_task_score")
    row["solve_rate"] = best.get("solve_rate")
    row["solved"] = best.get("solved")
    row["tasks"] = best.get("tasks")
    if len(runs) > 1:
        scores = [float(run.get("average_task_score", 0)) for run in runs]
        solve_rates = [float(run.get("solve_rate", 0)) for run in runs]
        row["repeat_summary"] = {
            "mean_average_task_score": round(sum(scores) / len(scores), 4),
            "min_average_task_score": round(min(scores), 4),
            "max_average_task_score": round(max(scores), 4),
            "mean_solve_rate": round(sum(solve_rates) / len(solve_rates), 4),
            "run_seeds": [run.get("run_seed") for run in runs],
        }
    return row


def build_tables(raw_path: Path = OUTPUTS / "founderbench-baseline-raw.json") -> dict[str, Any]:
    deterministic_runs = load_runs(raw_path)
    provider_rows = [provider_status(spec) for spec in PROVIDER_RUNS]
    valid_provider_runs: list[dict[str, Any]] = []
    for row in provider_rows:
        if row["status"] != "valid":
            continue
        valid_provider_runs.extend(load_runs(ROOT / row["evidence_path"]))
    all_valid_runs = deterministic_runs + valid_provider_runs
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Paper-ready tables generated from raw current release runs and validated provider-run availability.",
        "source_files": {
            "deterministic_raw": str(raw_path.relative_to(ROOT)),
        },
        "summary": {
            "deterministic_runs": len(deterministic_runs),
            "valid_provider_runs": len(valid_provider_runs),
            "provider_candidates": len(provider_rows),
            "provider_missing_or_invalid": sum(1 for row in provider_rows if row["status"] != "valid"),
            "valid_provider_policies": len({row["policy"] for row in provider_rows if row["status"] == "valid"}),
            "valid_repeated_provider_bundles": sum(1 for row in provider_rows if row.get("evidence_kind") == "repeat_bundle"),
        },
        "deterministic_policy_rows": policy_rows(deterministic_runs),
        "all_valid_policy_rows": policy_rows(all_valid_runs),
        "confidence_interval_rows": ci_rows(all_valid_runs),
        "pairwise_rows": pairwise_rows(all_valid_runs),
        "family_rows": family_rows(all_valid_runs),
        "hardest_task_rows": difficulty_rows(all_valid_runs)[:12],
        "provider_status": provider_rows,
    }


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    valid_policies = [row[0] for row in payload["all_valid_policy_rows"]]
    provider_rows = [
        [
            row["id"],
            row["policy"],
            row["family"],
            row["status"],
            row["runs"],
            row.get("evidence_kind", ""),
            row.get("average_task_score", ""),
            row.get("solve_rate", ""),
            "; ".join(row["problems"][:2]),
        ]
        for row in payload["provider_status"]
    ]
    lines = [
        "# FounderBench Paper Tables",
        "",
        "These generated tables are intended for the paper results section. They are derived from raw current release run files; hosted/provider rows are included in the main tables only after submission validation passes.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Main Leaderboard",
        "",
        markdown_table(["Policy", "Tasks", "Solved", "Solve Rate", "Avg Score", "Public Dev", "Public Test", "Over-Budget", "Provider Errors"], payload["all_valid_policy_rows"]),
        "",
        "## Confidence Intervals",
        "",
        markdown_table(["Policy", "Avg Score", "Score 95% CI", "Solve Rate", "Solve Rate 95% CI"], payload["confidence_interval_rows"]),
        "",
        "## Pairwise Score Gaps",
        "",
        markdown_table(["Comparison", "Mean Gap", "95% CI", "Shared Tasks"], payload["pairwise_rows"]),
        "",
        "## Family Breakdown",
        "",
        "Each cell reports `solved/5 (average score)`. Valid policies included: " + ", ".join(f"`{policy}`" for policy in valid_policies) + ".",
        "",
        markdown_table(["Family", *valid_policies], payload["family_rows"]),
        "",
        "## Hardest Public Tasks",
        "",
        markdown_table(["Task", "Family", "Mean Score", "Solved By"], payload["hardest_task_rows"]),
        "",
        "## Provider Evidence Status",
        "",
        markdown_table(["ID", "Policy", "Family", "Status", "Runs", "Evidence", "Avg Score", "Solve Rate", "Problems"], provider_rows),
        "",
        "Provider runs marked `missing` or `invalid` are excluded from the main leaderboard and tables. This avoids mixing older or partial provider outputs into the current release paper evidence.",
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_tables(json_output: Path, markdown_output: Path) -> None:
    payload = build_tables()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper-ready result tables.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_tables(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
