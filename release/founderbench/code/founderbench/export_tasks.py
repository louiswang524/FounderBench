from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .tasks import TASKS


def task_split(task_id: str) -> str:
    task_num = int(task_id.split("-")[1])
    if task_num <= 30:
        return "public_dev"
    if task_num <= 50:
        return "public_test"
    return "private_holdout"


def task_manifest() -> dict:
    return {
        "benchmark": "FounderBench",
        "version": "0.3.0",
        "task_count": len(TASKS),
        "splits": {
            "public_dev": "FND-001..FND-030; intended for prompt/agent development and calibration.",
            "public_test": "FND-031..FND-050; intended for reported open evaluation.",
            "private_holdout": "Reserved for future hidden seeds/templates; not included in current release.",
        },
        "families": {
            "FND-001..FND-005": "Market selection",
            "FND-006..FND-010": "First revenue",
            "FND-011..FND-015": "Retention improvement",
            "FND-016..FND-020": "Churn shock recovery",
            "FND-021..FND-025": "Demo Day traction",
            "FND-026..FND-030": "Pricing",
            "FND-031..FND-035": "Runway preservation",
            "FND-036..FND-040": "Pivot decision",
            "FND-041..FND-045": "Fundraising",
            "FND-046..FND-050": "Channel expansion",
        },
        "tasks": [
            {
                "task_id": task.task_id,
                "name": task.name,
                "description": task.description,
                "seed": task.seed,
                "weeks": task.weeks,
                "pass_threshold": task.pass_threshold,
                "split": task_split(task.task_id),
                "allowed_actions": sorted(task.allowed_actions),
            }
            for task in TASKS
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Export FounderBench task manifest.")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(task_manifest(), indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
