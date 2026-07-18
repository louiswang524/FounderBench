from __future__ import annotations

import argparse
import json

from .env import MoneyBenchEnv
from .policies import get_policy


def run(policy_name: str, seed: int, weeks: int, trace: bool = False) -> dict:
    env = MoneyBenchEnv(seed=seed, weeks=weeks)
    policy = get_policy(policy_name, seed=seed)
    observation = env.reset()
    events = []

    while not env.done():
        actions = policy.act(observation)
        result = env.step(actions)
        if trace:
            events.append(
                {
                    "week": observation.week,
                    "cash": observation.cash,
                    "actions": [action.__dict__ for action in actions],
                    "result": result.__dict__,
                }
            )
        observation = env.observe()

    return {
        "policy": policy_name,
        "summary": env.summary(),
        "events": events,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a FounderBench single-company simulator episode.")
    parser.add_argument("--policy", choices=["random", "conservative", "heuristic"], default="heuristic")
    parser.add_argument("--seed", type=int, default=7)
    parser.add_argument("--weeks", type=int, default=52)
    parser.add_argument("--trace", action="store_true")
    args = parser.parse_args()

    print(json.dumps(run(args.policy, args.seed, args.weeks, args.trace), indent=2))


if __name__ == "__main__":
    main()
