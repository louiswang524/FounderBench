from __future__ import annotations

import argparse
import ast
import importlib
import json
import platform
import sys
from pathlib import Path
from typing import Any

from .analysis import markdown_table


ROOT = Path(__file__).resolve().parents[3]
PACKAGE_ROOT = ROOT / "work" / "founderbench"
SOURCE_ROOT = PACKAGE_ROOT / "founderbench"
VERSION = "0.3.0"


def _imports_from_file(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                names.add(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level:
                names.add("founderbench")
            elif node.module:
                names.add(node.module.split(".")[0])
    return names


def _all_imports() -> dict[str, list[str]]:
    by_file: dict[str, list[str]] = {}
    for path in sorted(SOURCE_ROOT.glob("*.py")):
        by_file[str(path.relative_to(PACKAGE_ROOT))] = sorted(_imports_from_file(path))
    return by_file


def _classify_import(name: str) -> str:
    if name == "founderbench":
        return "local_package"
    if name in sys.stdlib_module_names:
        return "stdlib"
    return "external_or_missing"


def _import_check(name: str) -> dict[str, Any]:
    try:
        importlib.import_module(name)
    except Exception as exc:  # noqa: BLE001 - report import environment, do not mask.
        return {"module": name, "ok": False, "error": f"{type(exc).__name__}: {exc}"}
    return {"module": name, "ok": True, "error": ""}


def build_report() -> dict[str, Any]:
    imports_by_file = _all_imports()
    imports = sorted({name for names in imports_by_file.values() for name in names})
    classified = [
        {"module": name, "classification": _classify_import(name)}
        for name in imports
    ]
    external = sorted(row["module"] for row in classified if row["classification"] == "external_or_missing")
    checks = [_import_check(name) for name in ["founderbench", "founderbench.release", "founderbench.task_runner", *external]]
    return {
        "benchmark": "FounderBench",
        "version": VERSION,
        "purpose": "Runtime and dependency report for the current release supplementary artifact.",
        "environment": {
            "python_version": sys.version.split()[0],
            "python_executable": sys.executable,
            "platform": platform.platform(),
            "machine": platform.machine(),
            "working_directory": str(PACKAGE_ROOT),
        },
        "dependency_policy": {
            "core_benchmark_dependencies": "Python standard library plus the local founderbench package.",
            "hosted_provider_runs": "Use stdlib urllib/json plus provider API keys in environment variables.",
            "local_open_source_runs": "Require a separately managed OpenAI-compatible inference server; the benchmark client itself does not vendor that server.",
            "recommended_python": "3.11+",
            "validated_python": sys.version.split()[0],
        },
        "imports_by_file": imports_by_file,
        "import_classification": classified,
        "import_checks": checks,
        "summary": {
            "source_files": len(imports_by_file),
            "imported_modules": len(imports),
            "stdlib_modules": sum(1 for row in classified if row["classification"] == "stdlib"),
            "local_package_modules": sum(1 for row in classified if row["classification"] == "local_package"),
            "external_or_missing_modules": len(external),
            "import_checks_passed": sum(1 for row in checks if row["ok"]),
            "import_checks_failed": sum(1 for row in checks if not row["ok"]),
            "core_has_external_runtime_dependencies": bool(external),
        },
    }


def validate_report(payload: dict[str, Any]) -> list[str]:
    problems: list[str] = []
    if payload.get("version") != VERSION:
        problems.append(f"Expected version {VERSION}, found {payload.get('version')}.")
    if payload["summary"]["source_files"] < 20:
        problems.append("Expected at least 20 source files in dependency scan.")
    if payload["summary"]["import_checks_failed"]:
        problems.append("One or more required import checks failed.")
    if payload["summary"]["external_or_missing_modules"]:
        problems.append("Core source imports external or missing modules.")
    if not payload["dependency_policy"]["recommended_python"]:
        problems.append("Recommended Python version is required.")
    return problems


def write_markdown(payload: dict[str, Any], output: Path) -> None:
    env_rows = [[key, value] for key, value in payload["environment"].items()]
    policy_rows = [[key, value] for key, value in payload["dependency_policy"].items()]
    summary_rows = [[key, value] for key, value in payload["summary"].items()]
    import_rows = [[row["module"], row["classification"]] for row in payload["import_classification"]]
    check_rows = [[row["module"], row["ok"], row["error"]] for row in payload["import_checks"]]
    lines = [
        "# FounderBench Environment Report",
        "",
        payload["purpose"],
        "",
        "## Environment",
        "",
        markdown_table(["Field", "Value"], env_rows),
        "",
        "## Dependency Policy",
        "",
        markdown_table(["Field", "Value"], policy_rows),
        "",
        "## Summary",
        "",
        markdown_table(["Metric", "Value"], summary_rows),
        "",
        "## Import Classification",
        "",
        markdown_table(["Module", "Classification"], import_rows),
        "",
        "## Import Checks",
        "",
        markdown_table(["Module", "OK", "Error"], check_rows),
        "",
        "## Validation",
        "",
    ]
    problems = validate_report(payload)
    if problems:
        lines.append("Status: FAIL")
        lines.extend(f"- {problem}" for problem in problems)
    else:
        lines.append("Status: PASS")
        lines.append("")
        lines.append("The core benchmark package imports only Python standard-library modules plus the local `founderbench` package.")
    lines.append("")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(lines), encoding="utf-8")


def write_report(json_output: Path, markdown_output: Path) -> None:
    payload = build_report()
    problems = validate_report(payload)
    if problems:
        raise ValueError("; ".join(problems))
    json_output.parent.mkdir(parents=True, exist_ok=True)
    json_output.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    write_markdown(payload, markdown_output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate runtime/dependency environment report.")
    parser.add_argument("--json-output", required=True)
    parser.add_argument("--markdown-output", required=True)
    args = parser.parse_args()
    write_report(Path(args.json_output), Path(args.markdown_output))
    print(f"Wrote {args.json_output}")
    print(f"Wrote {args.markdown_output}")


if __name__ == "__main__":
    main()
