from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[3]
VERSION = "0.3.0"


EXPERIMENTS: list[dict[str, Any]] = [
    {
        "id": "deterministic_rule_baselines",
        "section": "core_baselines",
        "priority": "required",
        "status_if_present": "complete",
        "description": "Run random, conservative, heuristic, and task-aware heuristic policies on all 50 public current release tasks.",
        "evidence_paths": [
            "outputs/founderbench-baseline-raw.json",
            "outputs/founderbench-baseline-leaderboard.json",
            "outputs/founderbench-baseline-analysis.md",
        ],
        "commands": ["python -m founderbench.release regenerate"],
        "paper_use": "Shows the simulator works, is nontrivial, and separates policies with different business-decision capabilities.",
    },
    {
        "id": "capability_ladder_ablation",
        "section": "ablations",
        "priority": "required",
        "status_if_present": "complete",
        "description": "Compare random -> conservative -> heuristic -> task-aware heuristic to isolate decision capabilities.",
        "evidence_paths": ["outputs/founderbench-ablation-report.md"],
        "commands": ["python -m founderbench.ablation --raw ..\\..\\outputs\\founderbench-baseline-raw.json --output ..\\..\\outputs\\founderbench-ablation-report.md"],
        "paper_use": "Explains which capabilities move the benchmark score and where task-family conditioning matters.",
    },
    {
        "id": "action_space_ablation",
        "section": "ablations",
        "priority": "required",
        "status_if_present": "complete",
        "description": "Disable major action groups in the task-aware heuristic and measure score drops over all 50 tasks.",
        "evidence_paths": [
            "outputs/founderbench-action-ablation.md",
            "outputs/founderbench-action-ablation.json",
        ],
        "commands": ["python -m founderbench.action_ablation --json-output ..\\..\\outputs\\founderbench-action-ablation.json --markdown-output ..\\..\\outputs\\founderbench-action-ablation.md"],
        "paper_use": "Shows that the expanded action space affects outcomes rather than serving as unused interface decoration.",
    },
    {
        "id": "random_repeated_seed_calibration",
        "section": "uncertainty",
        "priority": "required",
        "status_if_present": "complete",
        "description": "Repeat stochastic random-policy runs over multiple seeds and report across-run intervals.",
        "evidence_paths": [
            "outputs/founderbench-random-repeats.json",
            "outputs/founderbench-random-repeats.md",
        ],
        "commands": ["python -m founderbench.repeats --policy random --seeds 0,1,2,3,4 --json-output ..\\..\\outputs\\founderbench-random-repeats.json --markdown-output ..\\..\\outputs\\founderbench-random-repeats.md"],
        "paper_use": "Provides a sanity check for stochastic variance and interval reporting.",
    },
    {
        "id": "qualitative_trace_analysis",
        "section": "qualitative",
        "priority": "required",
        "status_if_present": "complete",
        "description": "Select representative deterministic success and failure traces for explaining benchmark behavior.",
        "evidence_paths": [
            "outputs/founderbench-qualitative-traces.json",
            "outputs/founderbench-qualitative-traces.md",
        ],
        "commands": ["python -m founderbench.qualitative --raw ..\\..\\outputs\\founderbench-baseline-raw.json --json-output ..\\..\\outputs\\founderbench-qualitative-traces.json --markdown-output ..\\..\\outputs\\founderbench-qualitative-traces.md"],
        "paper_use": "Supports failure analysis and shows that scores come from executable simulator trajectories.",
    },
    {
        "id": "deepseek_hosted_baseline",
        "section": "hosted_llm_baselines",
        "priority": "required",
        "description": "Run DeepSeek on the complete 50-task current release suite with submission validation.",
        "evidence_paths": [
            "outputs/founderbench-deepseek.json",
            "outputs/founderbench-deepseek-submission-report.md",
        ],
        "commands": [
            "python -m founderbench.resumable_runner --policy deepseek --output ..\\..\\outputs\\founderbench-deepseek.json --resume",
            "python -m founderbench.submission --input ..\\..\\outputs\\founderbench-deepseek.json --report ..\\..\\outputs\\founderbench-deepseek-submission-report.md",
        ],
        "paper_use": "Provides a representative hosted LLM baseline.",
    },
    {
        "id": "deepseek_self_consistency_k3",
        "section": "hosted_llm_ablations",
        "priority": "recommended",
        "description": "Run DeepSeek self-consistency with k=3 on the complete 50-task current release suite.",
        "evidence_paths": [
            "outputs/founderbench-deepseek-sc-k3.json",
            "outputs/founderbench-deepseek-sc-k3-submission-report.md",
        ],
        "commands": [
            "python -m founderbench.resumable_runner --policy deepseek_sc --output ..\\..\\outputs\\founderbench-deepseek-sc-k3.json --resume",
            "python -m founderbench.submission --input ..\\..\\outputs\\founderbench-deepseek-sc-k3.json --report ..\\..\\outputs\\founderbench-deepseek-sc-k3-submission-report.md",
        ],
        "paper_use": "Tests whether sampling-based self-consistency improves business decision quality.",
    },
    {
        "id": "anthropic_hosted_baseline",
        "section": "hosted_llm_baselines",
        "priority": "required",
        "description": "Run Claude/Anthropic on the complete 50-task current release suite with submission validation.",
        "evidence_paths": [
            "outputs/founderbench-anthropic.json",
            "outputs/founderbench-anthropic-submission-report.md",
        ],
        "commands": [
            "python -m founderbench.resumable_runner --policy anthropic --output ..\\..\\outputs\\founderbench-anthropic.json --resume",
            "python -m founderbench.submission --input ..\\..\\outputs\\founderbench-anthropic.json --report ..\\..\\outputs\\founderbench-anthropic-submission-report.md",
        ],
        "paper_use": "Adds a second hosted LLM family for model differentiation.",
    },
    {
        "id": "gemini_hosted_baseline",
        "section": "hosted_llm_baselines",
        "priority": "required",
        "description": "Run Gemini on the complete 50-task current release suite with submission validation.",
        "evidence_paths": [
            "outputs/founderbench-gemini.json",
            "outputs/founderbench-gemini-submission-report.md",
        ],
        "commands": [
            "python -m founderbench.resumable_runner --policy gemini --output ..\\..\\outputs\\founderbench-gemini.json --resume",
            "python -m founderbench.submission --input ..\\..\\outputs\\founderbench-gemini.json --report ..\\..\\outputs\\founderbench-gemini-submission-report.md",
        ],
        "paper_use": "Adds a third hosted LLM family for model differentiation.",
    },
    {
        "id": "local_open_source_baseline",
        "section": "open_source_baselines",
        "priority": "required",
        "description": "Run at least one local/open-source model via the OpenAI-compatible protocol and validate the submission.",
        "evidence_paths": [
            "outputs/founderbench-local-open-model.json",
            "outputs/founderbench-local-open-model-submission-report.md",
        ],
        "commands": [
            "python -m founderbench.local_model health --output ..\\..\\outputs\\local-health.json",
            "python -m founderbench.resumable_runner --policy llm --output ..\\..\\outputs\\founderbench-local-open-model.json --resume --audit",
            "python -m founderbench.submission --input ..\\..\\outputs\\founderbench-local-open-model.json --report ..\\..\\outputs\\founderbench-local-open-model-submission-report.md",
        ],
        "paper_use": "Makes the comparison accessible beyond closed hosted APIs.",
    },
    {
        "id": "hosted_llm_audit_traces",
        "section": "auditability",
        "priority": "required",
        "description": "Collect redacted audit traces for representative hosted LLM runs.",
        "evidence_paths": [
            "outputs/founderbench-deepseek-audit.json",
            "outputs/founderbench-anthropic-audit.json",
            "outputs/founderbench-gemini-audit.json",
        ],
        "commands": ["python -m founderbench.resumable_runner --policy <provider> --output ..\\..\\outputs\\<provider>-audit.json --resume --audit"],
        "paper_use": "Allows qualitative analysis of provider failures without exposing secrets.",
        "completion_rule": "any",
    },
    {
        "id": "private_holdout_execution",
        "section": "anti_gaming",
        "priority": "required_for_final_submission",
        "description": "Execute the private holdout protocol on an evaluator-controlled host and report aggregate fields only.",
        "evidence_paths": ["outputs/founderbench-private-holdout-results.json"],
        "commands": ["Follow outputs/founderbench-private-holdout-evaluator-protocol.md on evaluator host."],
        "paper_use": "Prevents optimization against visible public tasks and supports leaderboard credibility.",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def evidence_entry(rel_path: str) -> dict[str, Any]:
    path = ROOT / rel_path
    if not path.exists():
        return {"path": rel_path, "exists": False}
    return {
        "path": rel_path,
        "exists": True,
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
    }


def experiment_status(experiment: dict[str, Any], evidence: list[dict[str, Any]]) -> str:
    present = [entry for entry in evidence if entry["exists"]]
    if experiment.get("completion_rule") == "any":
        return "complete" if present else "missing"
    if len(present) == len(evidence):
        return experiment.get("status_if_present", "complete")
    if present:
        return "partial"
    return "missing"


def build_matrix() -> dict[str, Any]:
    experiments = []
    for spec in EXPERIMENTS:
        evidence = [evidence_entry(path) for path in spec["evidence_paths"]]
        row = dict(spec)
        row["evidence"] = evidence
        row["status"] = experiment_status(spec, evidence)
        row["missing_paths"] = [entry["path"] for entry in evidence if not entry["exists"]]
        experiments.append(row)
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Paper-facing experiment matrix for required baselines, ablations, uncertainty checks, audit traces, and holdout evidence.",
        "summary": {
            "experiments": len(experiments),
            "complete": sum(1 for row in experiments if row["status"] == "complete"),
            "partial": sum(1 for row in experiments if row["status"] == "partial"),
            "missing": sum(1 for row in experiments if row["status"] == "missing"),
            "required_missing": sum(1 for row in experiments if row["priority"].startswith("required") and row["status"] != "complete"),
        },
        "experiments": experiments,
    }


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    out = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    out.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(out)


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    rows = [
        [
            row["id"],
            row["section"],
            row["priority"],
            row["status"],
            len([entry for entry in row["evidence"] if entry["exists"]]),
            row["paper_use"],
        ]
        for row in payload["experiments"]
    ]
    lines = [
        "# FounderBench Experiment Matrix",
        "",
        "This generated matrix states which experiments are needed for a publishable benchmark paper and which evidence files currently prove them. Older v0.2 provider outputs are intentionally excluded from this matrix.",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], [[key, value] for key, value in payload["summary"].items()]),
        "",
        "## Experiment Ledger",
        "",
        markdown_table(["ID", "Section", "Priority", "Status", "Evidence Files", "Paper Use"], rows),
        "",
        "## Missing Required Evidence",
        "",
    ]
    missing = [row for row in payload["experiments"] if row["priority"].startswith("required") and row["status"] != "complete"]
    if missing:
        for row in missing:
            lines.extend([f"### {row['id']}", "", row["description"], ""])
            lines.extend(f"- Missing `{path}`" for path in row["missing_paths"])
            lines.extend(["", "Commands:"])
            lines.extend(f"- `{command}`" for command in row["commands"])
            lines.append("")
    else:
        lines.append("All required experiments are complete.")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_matrix(json_output: Path, markdown_output: Path) -> None:
    payload = build_matrix()
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate paper-facing experiment matrix.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_matrix(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
