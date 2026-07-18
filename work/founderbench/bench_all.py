from __future__ import annotations

import json
from statistics import mean

from founderbench.cli import run


def main() -> None:
    policies = ["random", "conservative", "heuristic"]
    seeds = list(range(10))
    rows = []
    for policy in policies:
        summaries = [run(policy, seed=seed, weeks=52)["summary"] for seed in seeds]
        rows.append(
            {
                "policy": policy,
                "mean_score": round(mean(item["score"] for item in summaries), 2),
                "mean_cash": round(mean(item["cash"] for item in summaries), 2),
                "mean_customers": round(mean(item["customers"] for item in summaries), 2),
                "bankruptcies": sum(1 for item in summaries if item["bankrupt"]),
                "runs": summaries,
            }
        )
    print(json.dumps(rows, indent=2))


if __name__ == "__main__":
    main()

