from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from dataclasses import replace
from pathlib import Path
from typing import Any

from .holdout import FAMILIES, HOLDOUT_VERSION, VERSION, generate_private_fingerprint_manifest, validate_fingerprint_manifest
from .schema import StepResult
from .task_runner import make_policy, run_task
from .tasks import TASKS, StartupTask, TaskScore


FAMILY_RANGES = {
    "Market selection": (1, 5),
    "First revenue": (6, 10),
    "Retention improvement": (11, 15),
    "Churn shock recovery": (16, 20),
    "Demo Day traction": (21, 25),
    "Pricing": (26, 30),
    "Runway preservation": (31, 35),
    "Pivot decision": (36, 40),
    "Fundraising": (41, 45),
    "Channel expansion": (46, 50),
}


def _digest(secret: str, label: str) -> str:
    return hmac.new(secret.encode("utf-8"), label.encode("utf-8"), hashlib.sha256).hexdigest()


def _int(secret: str, label: str, low: int, high: int) -> int:
    span = high - low + 1
    value = int(_digest(secret, label)[:12], 16)
    return low + (value % span)


def _family_tasks(family: str) -> list[StartupTask]:
    low, high = FAMILY_RANGES[family]
    ids = {f"FND-{idx:03d}" for idx in range(low, high + 1)}
    return [task for task in TASKS if task.task_id in ids]


def _private_score(task_id: str, name: str, base: StartupTask):
    def score(env, results: list[StepResult]) -> TaskScore:
        original = base.score(env, results)
        return TaskScore(
            task_id=task_id,
            name=name,
            score=original.score,
            passed=original.passed,
            metrics=original.metrics,
            notes=[
                "Private holdout score computed with a secret-selected public-family template.",
                *original.notes,
            ],
        )

    return score


def generate_private_tasks(secret: str) -> list[StartupTask]:
    tasks: list[StartupTask] = []
    index = 1
    for family in FAMILIES:
        candidates = _family_tasks(family)
        for variant in range(1, 3):
            task_id = f"PRIV-{index:03d}"
            name = f"Private {family.lower()} v{variant}"
            base_index = _int(secret, f"{HOLDOUT_VERSION}:{task_id}:base", 0, len(candidates) - 1)
            seed = _int(secret, f"{HOLDOUT_VERSION}:{task_id}:seed", 10_000, 9_999_999)
            base = candidates[base_index]
            tasks.append(
                replace(
                    base,
                    task_id=task_id,
                    name=name,
                    description="Private holdout task. Initial state and selected template are evaluator-held until the cycle closes.",
                    seed=seed,
                    score=_private_score(task_id, name, base),
                )
            )
            index += 1
    return tasks


def run_private_holdout(policy_name: str, secret: str, *, audit: bool = False, seed: int = 0) -> dict[str, Any]:
    tasks = generate_private_tasks(secret)
    policy = make_policy(policy_name, seed=seed)
    results = [run_task(task, policy, trace=audit, audit=audit) for task in tasks]
    solved = sum(1 for result in results if result["score"]["passed"])
    diagnostics: dict[str, Any] = {
        "private_provider_errors": sum(int(result["diagnostics"]["provider_errors"]) for result in results),
        "private_invalid_actions": sum(int(result["diagnostics"]["invalid_actions"]) for result in results),
        "private_over_budget_decisions": sum(int(result["diagnostics"]["over_budget_decisions"]) for result in results),
        "private_estimated_provider_cost_usd": round(sum(float(result["diagnostics"]["estimated_provider_cost_usd"]) for result in results), 6),
        "private_decision_latency_s": round(sum(float(result["diagnostics"]["decision_latency_s"]) for result in results), 4),
        "provider_error_categories": {},
    }
    for result in results:
        for category, count in result["diagnostics"].get("provider_error_categories", {}).items():
            diagnostics["provider_error_categories"][category] = diagnostics["provider_error_categories"].get(category, 0) + int(count)
    fingerprint_manifest = generate_private_fingerprint_manifest(secret)
    manifest_text = json.dumps(fingerprint_manifest, sort_keys=True)
    return {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "policy": policy_name,
        "run_seed": seed,
        "private_tasks": len(results),
        "private_solved": solved,
        "private_solve_rate": round(solved / len(results), 3),
        "private_average_task_score": round(sum(float(result["score"]["score"]) for result in results) / len(results), 2),
        **diagnostics,
        "fingerprint_manifest_sha256": hashlib.sha256(manifest_text.encode("utf-8")).hexdigest(),
        "secret_values_recorded": False,
        "public_report_note": "This file intentionally excludes private task initial states, selected public-family template ids, hidden seeds, and raw traces unless audit mode is explicitly enabled on the evaluator host.",
        **({"private_results": results} if audit else {}),
    }


def validate_private_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if payload.get("benchmark_version") != VERSION:
        problems.append(f"benchmark_version must be {VERSION}.")
    if payload.get("private_tasks") != 20:
        problems.append("private_tasks must be 20.")
    if not 0 <= payload.get("private_solve_rate", -1) <= 1:
        problems.append("private_solve_rate must be in [0, 1].")
    if not 0 <= payload.get("private_average_task_score", -1) <= 100:
        problems.append("private_average_task_score must be in [0, 100].")
    if len(str(payload.get("fingerprint_manifest_sha256", ""))) != 64:
        problems.append("fingerprint_manifest_sha256 must be a SHA-256 hex digest.")
    if payload.get("secret_values_recorded") is not False:
        problems.append("secret_values_recorded must be false.")
    text = json.dumps(payload)
    if "FounderBench_HOLDOUT_SECRET" in text:
        problems.append("Report must not include the holdout secret environment variable name as a value.")
    return problems


def write_report(policy_name: str, secret: str, output: Path, *, audit: bool = False, seed: int = 0) -> None:
    payload = run_private_holdout(policy_name, secret, audit=audit, seed=seed)
    problems = validate_private_report(payload)
    if problems:
        raise ValueError("; ".join(problems))
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a private FounderBench holdout on an evaluator host.")
    parser.add_argument("--policy", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--secret-env", default="FounderBench_HOLDOUT_SECRET")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--seed", type=int, default=0)
    args = parser.parse_args()

    secret = os.environ.get(args.secret_env)
    if not secret:
        raise SystemExit(f"Set {args.secret_env} on the evaluator host.")
    manifest = generate_private_fingerprint_manifest(secret)
    problems = validate_fingerprint_manifest(manifest)
    if problems:
        raise SystemExit("; ".join(problems))
    write_report(args.policy, secret, Path(args.output), audit=args.audit, seed=args.seed)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
