from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from .analysis import family_name, markdown_table
from .task_runner import make_policy, run_task
from .tasks import get_task


def load_results(path: Path) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _find_run(runs: list[dict[str, Any]], policy: str) -> dict[str, Any]:
    for run in runs:
        if run.get("policy") == policy:
            return run
    raise ValueError(f"Missing policy run: {policy}")


def select_examples(runs: list[dict[str, Any]]) -> list[dict[str, str]]:
    task_heuristic = _find_run(runs, "task_heuristic")
    heuristic = _find_run(runs, "heuristic")
    random_run = _find_run(runs, "random")

    strongest_passes = [result for result in task_heuristic["results"] if result["score"]["passed"]]
    strongest_fails = [result for result in task_heuristic["results"] if not result["score"]["passed"]]
    heuristic_pivot_fails = [
        result
        for result in heuristic["results"]
        if family_name(result["task_id"]) == "Pivot decision" and not result["score"]["passed"]
    ]
    random_failures = [result for result in random_run["results"] if not result["score"]["passed"]]

    examples = [
        {
            "label": "task_heuristic_representative_success",
            "policy": "task_heuristic",
            "task_id": max(strongest_passes, key=lambda item: float(item["score"]["score"]))["task_id"],
            "reason": "Highest-scoring solved task for the strongest deterministic baseline.",
        },
        {
            "label": "task_heuristic_representative_failure",
            "policy": "task_heuristic",
            "task_id": min(strongest_fails, key=lambda item: float(item["score"]["score"]))["task_id"],
            "reason": "Lowest-scoring failed task for the strongest deterministic baseline.",
        },
        {
            "label": "heuristic_pivot_failure",
            "policy": "heuristic",
            "task_id": min(heuristic_pivot_fails, key=lambda item: float(item["score"]["score"]))["task_id"],
            "reason": "Generic heuristic failure in a family where task conditioning creates a large gain.",
        },
        {
            "label": "random_representative_failure",
            "policy": "random",
            "task_id": min(random_failures, key=lambda item: float(item["score"]["score"]))["task_id"],
            "reason": "Lowest-scoring random-policy failure, illustrating why blind action sampling is insufficient.",
        },
    ]
    return examples


def _compact_event(event: dict[str, Any]) -> dict[str, Any]:
    observation = event["observation"]
    result = event["result"]
    return {
        "week": event["week"],
        "cash": round(float(observation["cash"]), 2),
        "reputation": round(float(observation["reputation"]), 3),
        "offers": len(observation.get("offers", [])),
        "actions": [
            {
                key: value
                for key, value in action.items()
                if key in {"type", "market_id", "offer_id", "budget", "price", "message_quality"} and value not in {None, 0, 0.0}
            }
            for action in event["actions"]
        ],
        "revenue": round(float(result.get("revenue", 0.0)), 2),
        "cost": round(float(result.get("cost", 0.0)), 2),
        "customers": result.get("customers"),
        "notes": result.get("notes", [])[:3],
    }


def build_trace_examples(raw_path: Path) -> dict[str, Any]:
    runs = load_results(raw_path)
    examples = []
    for selection in select_examples(runs):
        policy = make_policy(selection["policy"])
        task = get_task(selection["task_id"])
        result = run_task(task, policy, trace=True, audit=False)
        examples.append(
            {
                **selection,
                "task_name": result["name"],
                "task_family": family_name(result["task_id"]),
                "description": result["description"],
                "score": result["score"],
                "summary": result["summary"],
                "diagnostics": result["diagnostics"],
                "events": [_compact_event(event) for event in result["events"]],
            }
        )
    return {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "source_raw": str(raw_path),
        "examples": examples,
    }


def _first_actions(events: list[dict[str, Any]], count: int = 3) -> str:
    snippets = []
    for event in events[:count]:
        action_types = ", ".join(action["type"] for action in event["actions"])
        snippets.append(f"week {event['week']}: {action_types}")
    return "; ".join(snippets)


def write_markdown(examples: dict[str, Any], output: Path) -> None:
    rows = []
    for example in examples["examples"]:
        rows.append(
            [
                example["label"],
                example["policy"],
                example["task_id"],
                example["task_family"],
                f"{float(example['score']['score']):.2f}",
                example["score"]["passed"],
                _first_actions(example["events"]),
            ]
        )
    lines = [
        "# FounderBench Qualitative Trace Examples",
        "",
        "These examples are regenerated from deterministic task seeds with `trace=True`. They are intended for paper-facing qualitative analysis and debugging, not as additional leaderboard data.",
        "",
        markdown_table(["Example", "Policy", "Task", "Family", "Score", "Passed", "Opening Actions"], rows),
        "",
        "## Interpretation Notes",
        "",
        "- Success traces show how structured actions accumulate into revenue, customer, reputation, and runway outcomes.",
        "- Failure traces show that unsupported timing, weak family inference, or blind spending can fail even when all actions are syntactically valid.",
        "- Hosted LLM runs should include analogous redacted audit traces with provider-call records for at least one success and one failure.",
        "",
    ]
    for example in examples["examples"]:
        lines.extend(
            [
                f"## {example['label']}",
                "",
                f"Policy: `{example['policy']}`",
                f"Task: `{example['task_id']}` ({example['task_family']})",
                f"Score: `{float(example['score']['score']):.2f}`; passed: `{example['score']['passed']}`",
                f"Reason selected: {example['reason']}",
                "",
                markdown_table(
                    ["Week", "Cash", "Reputation", "Offers", "Actions", "Revenue", "Cost", "Customers"],
                    [
                        [
                            event["week"],
                            event["cash"],
                            event["reputation"],
                            event["offers"],
                            ", ".join(action["type"] for action in event["actions"]),
                            event["revenue"],
                            event["cost"],
                            event["customers"],
                        ]
                        for event in example["events"][:8]
                    ],
                ),
                "",
            ]
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate reproducible qualitative trace examples.")
    parser.add_argument("--raw", required=True, help="Raw benchmark result JSON used for example selection.")
    parser.add_argument("--json-output", required=True, help="Trace example JSON output.")
    parser.add_argument("--markdown-output", required=True, help="Trace example Markdown output.")
    args = parser.parse_args()
    examples = build_trace_examples(Path(args.raw))
    Path(args.json_output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_output).write_text(json.dumps(examples, indent=2), encoding="utf-8")
    write_markdown(examples, Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
