from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from .analysis import markdown_table


VERSION = "0.3.0"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_report(bundle_root: Path) -> dict[str, Any]:
    manifest_path = bundle_root / "SHA256SUMS.json"
    rows = []
    problems = []
    if not manifest_path.exists():
        return {
            "benchmark": "FounderBench",
            "version": VERSION,
            "bundle_root": str(bundle_root),
            "status": "fail",
            "summary": {"manifest_entries": 0, "verified": 0, "missing": 1, "mismatched": 0, "extra_files": 0},
            "files": [],
            "extra_files": [],
            "problems": [f"Missing {manifest_path}"],
        }
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest_paths = {row["path"] for row in manifest}
    for entry in manifest:
        path = bundle_root / entry["path"]
        row = {
            "path": entry["path"],
            "expected_sha256": entry["sha256"],
            "expected_bytes": entry["bytes"],
            "exists": path.exists(),
            "actual_sha256": "",
            "actual_bytes": 0,
            "status": "missing",
        }
        if path.exists():
            row["actual_sha256"] = sha256(path)
            row["actual_bytes"] = path.stat().st_size
            row["status"] = "pass" if row["actual_sha256"] == entry["sha256"] and row["actual_bytes"] == entry["bytes"] else "mismatch"
        if row["status"] != "pass":
            problems.append(f"{row['path']}: {row['status']}")
        rows.append(row)
    extra_files = []
    ignored = {"SHA256SUMS.json", "BUNDLE-INTEGRITY.json", "BUNDLE-INTEGRITY.md"}
    for path in sorted(bundle_root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(bundle_root).as_posix()
        if rel in manifest_paths or rel in ignored:
            continue
        extra_files.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)})
    if extra_files:
        problems.append(f"{len(extra_files)} files are not listed in SHA256SUMS.json.")
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "bundle_root": str(bundle_root),
        "status": "pass" if not problems else "fail",
        "summary": {
            "manifest_entries": len(rows),
            "verified": sum(1 for row in rows if row["status"] == "pass"),
            "missing": sum(1 for row in rows if row["status"] == "missing"),
            "mismatched": sum(1 for row in rows if row["status"] == "mismatch"),
            "extra_files": len(extra_files),
        },
        "files": rows,
        "extra_files": extra_files,
        "problems": problems,
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["status"] == "pass" and payload["problems"]:
        problems.append("Passing integrity report cannot contain problems.")
    if payload["status"] == "pass" and payload["summary"]["manifest_entries"] != payload["summary"]["verified"]:
        problems.append("Passing integrity report must verify every manifest entry.")
    if payload["summary"]["manifest_entries"] <= 0:
        problems.append("Integrity report must include at least one manifest entry.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    problem_rows = [[problem] for problem in payload["problems"]]
    lines = [
        "# FounderBench Bundle Integrity Report",
        "",
        "This report verifies the release bundle files against `SHA256SUMS.json`. The integrity report itself is written after the checksum manifest and is intentionally not included in that manifest.",
        "",
        f"Bundle root: `{payload['bundle_root']}`",
        f"Status: `{payload['status']}`",
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Problems",
        "",
    ]
    if problem_rows:
        lines.append(markdown_table(["Problem"], problem_rows))
    else:
        lines.append("No checksum, size, missing-file, or extra-file problems were found.")
    lines.extend(["", "## Validation", ""])
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The integrity report is internally consistent.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(bundle_root: Path, json_output: Path, markdown_output: Path) -> None:
    payload = build_report(bundle_root)
    problems = validate_report(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify FounderBench release bundle integrity against SHA256SUMS.json.")
    parser.add_argument("--bundle-root", required=True)
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.bundle_root), Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
