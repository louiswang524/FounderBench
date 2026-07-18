from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import os
from pathlib import Path
from typing import Any


VERSION = "0.3.0"
HOLDOUT_VERSION = "0.1"
FAMILIES = [
    "Market selection",
    "First revenue",
    "Retention improvement",
    "Churn shock recovery",
    "Demo Day traction",
    "Pricing",
    "Runway preservation",
    "Pivot decision",
    "Fundraising",
    "Channel expansion",
]


def digest(secret: str, label: str) -> str:
    return hmac.new(secret.encode("utf-8"), label.encode("utf-8"), hashlib.sha256).hexdigest()


def public_blueprint() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "status": "proposal_for_private_evaluator",
        "private_holdout_size": 20,
        "family_distribution": {family: 2 for family in FAMILIES},
        "public_release_policy": [
            "Do not publish private task initial states, target markets, seeds, or score thresholds before the evaluation closes.",
            "Publish task ids, family names, and post-evaluation aggregate metrics.",
            "Release a SHA-256/HMAC fingerprint manifest before model submissions to commit to the hidden suite without revealing it.",
        ],
        "generation_inputs": {
            "required_secret_env": "FounderBench_HOLDOUT_SECRET",
            "recommended_secret_length": "at least 32 random bytes encoded as text",
            "determinism": "private task ids, seed material, and fingerprints are deterministic given the secret and protocol version",
        },
        "evaluation_protocol": [
            "Freeze public code and public_dev/public_test tasks.",
            "Generate private holdout fingerprints from a secret unavailable to model developers.",
            "Run submitted models against private tasks on an evaluation host.",
            "Return only aggregate private scores and selected redacted audit failures.",
            "After the benchmark cycle, optionally release the private task definitions as an expired holdout and rotate the secret.",
        ],
    }


def validate_blueprint(blueprint: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if blueprint.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if blueprint.get("benchmark_version") != VERSION:
        problems.append(f"benchmark_version must be {VERSION}.")
    if blueprint.get("private_holdout_size") != 20:
        problems.append("private_holdout_size must be 20.")
    distribution = blueprint.get("family_distribution", {})
    if set(distribution) != set(FAMILIES):
        problems.append("family_distribution must cover all public task families.")
    if sum(int(count) for count in distribution.values()) != blueprint.get("private_holdout_size"):
        problems.append("family_distribution counts must sum to private_holdout_size.")
    if "evaluation_protocol" not in blueprint:
        problems.append("evaluation_protocol is required.")
    return problems


def generate_private_fingerprint_manifest(secret: str) -> dict[str, Any]:
    tasks = []
    index = 1
    for family in FAMILIES:
        for variant in range(1, 3):
            task_id = f"PRIV-{index:03d}"
            seed_material = digest(secret, f"{HOLDOUT_VERSION}:{task_id}:seed")[:16]
            task_fingerprint = digest(secret, f"{HOLDOUT_VERSION}:{task_id}:{family}:v{variant}")
            tasks.append(
                {
                    "task_id": task_id,
                    "family": family,
                    "variant": variant,
                    "split": "private_holdout",
                    "seed_commitment": seed_material,
                    "task_fingerprint": task_fingerprint,
                }
            )
            index += 1
    return {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "secret_commitment": hashlib.sha256(secret.encode("utf-8")).hexdigest(),
        "task_count": len(tasks),
        "tasks": tasks,
        "disclosure": "This file commits to hidden task identities/fingerprints but does not disclose private task definitions.",
    }


def validate_fingerprint_manifest(manifest: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if manifest.get("benchmark") != "FounderBench":
        problems.append("benchmark must be FounderBench.")
    if manifest.get("benchmark_version") != VERSION:
        problems.append(f"benchmark_version must be {VERSION}.")
    if manifest.get("task_count") != 20:
        problems.append("task_count must be 20.")
    tasks = manifest.get("tasks", [])
    if len(tasks) != 20:
        problems.append("tasks must contain 20 entries.")
    task_ids = [task.get("task_id") for task in tasks]
    if len(set(task_ids)) != len(task_ids):
        problems.append("private task ids must be unique.")
    families = {task.get("family") for task in tasks}
    if families != set(FAMILIES):
        problems.append("fingerprint manifest must include every family.")
    if "secret_commitment" not in manifest:
        problems.append("secret_commitment is required.")
    for task in tasks:
        if task.get("split") != "private_holdout":
            problems.append(f"{task.get('task_id')}: split must be private_holdout.")
        if len(str(task.get("task_fingerprint", ""))) != 64:
            problems.append(f"{task.get('task_id')}: task_fingerprint must be a SHA-256 hex digest.")
    return problems


def evaluator_protocol() -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "role": "private_evaluator",
        "required_inputs": [
            "Frozen public release bundle with SHA256SUMS.json.",
            "Evaluator-held FounderBench_HOLDOUT_SECRET.",
            "Private task definitions generated in memory or stored outside the public repository.",
            "Submitted model adapter or provider configuration.",
        ],
        "pre_submission_commitments": [
            "Publish the public blueprint.",
            "Publish the HMAC/SHA-256 fingerprint manifest generated from the evaluator secret.",
            "Do not publish private initial states, seeds, score thresholds, or hidden templates before the cycle closes.",
        ],
        "evaluation_steps": [
            "Validate the submitted public-run JSON with founderbench.submission.",
            "Generate and run private episodes with python -m founderbench.private_holdout_evaluator on the evaluator host.",
            "Run the submitted model on private tasks using the same action schema and diagnostics.",
            "Reject or flag runs that manually repair invalid model outputs outside the adapter.",
            "Report private aggregate score, solve rate, diagnostics, provider-error taxonomy, token/cost metadata, and selected redacted traces.",
            "Archive private raw results and the evaluator secret commitment for post-cycle audit.",
        ],
        "public_report_fields": [
            "model/provider/version",
            "private_tasks",
            "private_solved",
            "private_solve_rate",
            "private_average_task_score",
            "private_provider_errors",
            "private_invalid_actions",
            "private_over_budget_decisions",
            "private_estimated_provider_cost_usd",
            "fingerprint_manifest_sha256",
        ],
        "anti_gaming_notes": [
            "Public test tasks are visible and must not be called a hidden holdout.",
            "Private task definitions should be generated, stored, and executed only on evaluator-controlled infrastructure.",
            "Public reports from the evaluator should include only aggregate private fields unless the benchmark cycle has closed.",
            "The evaluator should rotate the secret or release an expired holdout after each benchmark cycle.",
        ],
    }


def write_evaluator_protocol_markdown(output: Path) -> None:
    protocol = evaluator_protocol()
    lines = [
        "# FounderBench Private Holdout Evaluator Protocol",
        "",
        f"Benchmark version: `{VERSION}`",
        f"Holdout protocol version: `{HOLDOUT_VERSION}`",
        "",
        "This protocol describes how an independent evaluator can instantiate a hidden FounderBench suite without publishing private task definitions.",
        "",
        "## Required Inputs",
        "",
        *[f"- {item}" for item in protocol["required_inputs"]],
        "",
        "## Pre-Submission Commitments",
        "",
        *[f"- {item}" for item in protocol["pre_submission_commitments"]],
        "",
        "## Evaluation Steps",
        "",
        *[f"{idx}. {item}" for idx, item in enumerate(protocol["evaluation_steps"], start=1)],
        "",
        "## Public Report Fields",
        "",
        *[f"- `{item}`" for item in protocol["public_report_fields"]],
        "",
        "## Anti-Gaming Notes",
        "",
        *[f"- {item}" for item in protocol["anti_gaming_notes"]],
        "",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate FounderBench private holdout protocol artifacts.")
    parser.add_argument("command", choices=["blueprint", "fingerprints", "protocol"])
    parser.add_argument("--output", required=True)
    parser.add_argument("--secret-env", default="FounderBench_HOLDOUT_SECRET")
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    if args.command == "blueprint":
        blueprint = public_blueprint()
        problems = validate_blueprint(blueprint)
        if problems:
            raise SystemExit("; ".join(problems))
        output.write_text(json.dumps(blueprint, indent=2), encoding="utf-8")
        print(f"Wrote {output}")
        return

    if args.command == "protocol":
        if output.suffix.lower() == ".json":
            output.write_text(json.dumps(evaluator_protocol(), indent=2), encoding="utf-8")
        else:
            write_evaluator_protocol_markdown(output)
        print(f"Wrote {output}")
        return

    secret = os.environ.get(args.secret_env)
    if not secret:
        raise SystemExit(f"Set {args.secret_env} to generate private holdout fingerprints.")
    manifest = generate_private_fingerprint_manifest(secret)
    problems = validate_fingerprint_manifest(manifest)
    if problems:
        raise SystemExit("; ".join(problems))
    output.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(f"Wrote {output}")


if __name__ == "__main__":
    main()
