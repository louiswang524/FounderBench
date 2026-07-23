"""Freeze the private holdout: secret (local), public fingerprints, baseline aggregates."""

from __future__ import annotations

import argparse
import json
import os
import secrets
from pathlib import Path
from typing import Any

from .analysis import markdown_table
from .holdout import (
    HOLDOUT_VERSION,
    VERSION,
    generate_private_fingerprint_manifest,
    public_blueprint,
    validate_blueprint,
    validate_fingerprint_manifest,
)
from .private_holdout_evaluator import run_private_holdout, validate_private_report


ROOT = Path(__file__).resolve().parents[3]
OUTPUTS = ROOT / "outputs"
LOCAL_DIR = ROOT / ".local"
SECRET_PATH = LOCAL_DIR / "FounderBench_HOLDOUT_SECRET"
BASELINE_POLICIES = ("random", "conservative", "heuristic", "task_heuristic")


def ensure_secret(path: Path = SECRET_PATH) -> str:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        secret = path.read_text(encoding="utf-8").strip()
        if len(secret) < 32:
            raise SystemExit(f"Existing secret at {path} is too short; refusing to reuse.")
        return secret
    secret = secrets.token_urlsafe(48)
    path.write_text(secret + "\n", encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:
        pass
    return secret


def freeze(secret: str) -> dict[str, Any]:
    blueprint = public_blueprint()
    problems = validate_blueprint(blueprint)
    if problems:
        raise SystemExit("; ".join(problems))

    manifest = generate_private_fingerprint_manifest(secret)
    problems = validate_fingerprint_manifest(manifest)
    if problems:
        raise SystemExit("; ".join(problems))

    baseline_rows: list[dict[str, Any]] = []
    for policy in BASELINE_POLICIES:
        report = run_private_holdout(policy, secret, audit=False, seed=0)
        problems = validate_private_report(report)
        if problems:
            raise SystemExit(f"{policy}: " + "; ".join(problems))
        baseline_rows.append(
            {
                "policy": policy,
                "private_average_task_score": report["private_average_task_score"],
                "private_solved": report["private_solved"],
                "private_solve_rate": report["private_solve_rate"],
                "private_tasks": report["private_tasks"],
                "fingerprint_manifest_sha256": report["fingerprint_manifest_sha256"],
            }
        )

    fingerprint_path = OUTPUTS / "founderbench-private-holdout-fingerprints.json"
    blueprint_path = OUTPUTS / "founderbench-private-holdout-blueprint.json"
    calibration_path = OUTPUTS / "founderbench-private-holdout-calibration.json"
    calibration_md = OUTPUTS / "founderbench-private-holdout-calibration.md"
    freeze_path = OUTPUTS / "founderbench-private-holdout-freeze.json"

    OUTPUTS.mkdir(parents=True, exist_ok=True)
    fingerprint_path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    blueprint_path.write_text(json.dumps(blueprint, indent=2), encoding="utf-8")

    freeze_payload = {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "status": "frozen",
        "private_tasks": 20,
        "secret_location": str(SECRET_PATH.relative_to(ROOT)).replace("\\", "/"),
        "secret_committed_not_published": True,
        "secret_commitment": manifest["secret_commitment"],
        "fingerprint_manifest": str(fingerprint_path.relative_to(ROOT)).replace("\\", "/"),
        "fingerprint_manifest_sha256": baseline_rows[0]["fingerprint_manifest_sha256"],
        "hosted_models_evaluated": False,
        "deterministic_baselines_evaluated": True,
        "public_disclosure": [
            "Publish fingerprints and aggregate calibration metrics only.",
            "Do not publish private task templates, seeds, or raw private results.",
            "Hosted private-holdout leaderboard remains future work until models are run on the evaluator host.",
        ],
    }
    calibration_payload = {
        "benchmark": "FounderBench",
        "benchmark_version": VERSION,
        "holdout_protocol_version": HOLDOUT_VERSION,
        "status": "frozen_private_calibration_only",
        "purpose": "Aggregate-only deterministic baseline scores on the frozen 20-task private holdout.",
        "official_claim_guardrail": (
            "These are deterministic calibration rows on the frozen private holdout. "
            "They are not an official hosted private leaderboard."
        ),
        "fingerprint_manifest_sha256": freeze_payload["fingerprint_manifest_sha256"],
        "secret_commitment": freeze_payload["secret_commitment"],
        "baselines": baseline_rows,
    }
    freeze_path.write_text(json.dumps(freeze_payload, indent=2), encoding="utf-8")
    calibration_path.write_text(json.dumps(calibration_payload, indent=2), encoding="utf-8")

    rows = [
        [
            row["policy"],
            row["private_average_task_score"],
            f"{row['private_solved']}/{row['private_tasks']}",
            row["private_solve_rate"],
        ]
        for row in baseline_rows
    ]
    lines = [
        "# FounderBench Frozen Private Holdout Calibration",
        "",
        "Aggregate-only deterministic baselines on the frozen 20-task private holdout.",
        "",
        f"Status: `{calibration_payload['status']}`",
        "",
        "## Claim Guardrail",
        "",
        calibration_payload["official_claim_guardrail"],
        "",
        f"Secret commitment (SHA-256 of secret): `{freeze_payload['secret_commitment']}`",
        "",
        f"Fingerprint manifest SHA-256: `{freeze_payload['fingerprint_manifest_sha256']}`",
        "",
        "## Baselines",
        "",
        markdown_table(["Policy", "Private avg score", "Solved", "Solve rate"], rows),
        "",
        "## Notes",
        "",
        "- Private task definitions are generated from the evaluator-held secret and are not published.",
        "- Hosted model private-holdout runs are not included in this freeze.",
        "- Public `public_test` remains visible and is not a hidden split.",
        "",
    ]
    calibration_md.write_text("\n".join(lines), encoding="utf-8")
    return {
        "freeze": freeze_payload,
        "calibration": calibration_payload,
        "paths": {
            "secret": str(SECRET_PATH),
            "fingerprints": str(fingerprint_path),
            "blueprint": str(blueprint_path),
            "calibration_json": str(calibration_path),
            "calibration_md": str(calibration_md),
            "freeze": str(freeze_path),
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Freeze FounderBench private holdout artifacts.")
    parser.add_argument("--secret-path", type=Path, default=SECRET_PATH)
    args = parser.parse_args()
    secret = ensure_secret(args.secret_path)
    result = freeze(secret)
    print(json.dumps(result["paths"], indent=2))


if __name__ == "__main__":
    main()
