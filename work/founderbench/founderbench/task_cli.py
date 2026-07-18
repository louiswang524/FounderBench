from __future__ import annotations

import argparse
import json

from .task_runner import run_suite


def main() -> None:
    parser = argparse.ArgumentParser(description="Run FounderBench fixed startup tasks.")
    parser.add_argument(
        "--policy",
        choices=["random", "conservative", "heuristic", "task_heuristic", "llm", "deepseek", "anthropic", "gemini"],
        default="task_heuristic",
    )
    parser.add_argument("--task", action="append", help="Run only a specific task id. Can be repeated.")
    parser.add_argument("--trace", action="store_true")
    parser.add_argument("--audit", action="store_true", help="Include redacted provider call records in trace events.")
    args = parser.parse_args()
    print(json.dumps(run_suite(args.policy, trace=args.trace or args.audit, task_ids=args.task, audit=args.audit), indent=2))


if __name__ == "__main__":
    main()
