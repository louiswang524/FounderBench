# FounderBench Environment Report

Runtime and dependency report for the current release supplementary artifact.

## Environment

| Field | Value |
| --- | --- |
| python_version | 3.12.10 |
| python_executable | C:\Users\louis\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.12_qbz5n2kfra8p0\python.exe |
| platform | Windows-11-10.0.26200-SP0 |
| machine | AMD64 |
| working_directory | C:\Users\louis\Documents\Codex\2026-07-14\use\work\moneybench |

## Dependency Policy

| Field | Value |
| --- | --- |
| core_benchmark_dependencies | Python standard library plus the local moneybench package. |
| hosted_provider_runs | Use stdlib urllib/json plus provider API keys in environment variables. |
| local_open_source_runs | Require a separately managed OpenAI-compatible inference server; the benchmark client itself does not vendor that server. |
| recommended_python | 3.11+ |
| validated_python | 3.12.10 |

## Summary

| Metric | Value |
| --- | --- |
| source_files | 85 |
| imported_modules | 25 |
| stdlib_modules | 24 |
| local_package_modules | 1 |
| external_or_missing_modules | 0 |
| import_checks_passed | 3 |
| import_checks_failed | 0 |
| core_has_external_runtime_dependencies | False |

## Import Classification

| Module | Classification |
| --- | --- |
| __future__ | stdlib |
| abc | stdlib |
| argparse | stdlib |
| ast | stdlib |
| collections | stdlib |
| copy | stdlib |
| dataclasses | stdlib |
| hashlib | stdlib |
| hmac | stdlib |
| importlib | stdlib |
| json | stdlib |
| math | stdlib |
| moneybench | local_package |
| os | stdlib |
| pathlib | stdlib |
| platform | stdlib |
| random | stdlib |
| re | stdlib |
| shutil | stdlib |
| statistics | stdlib |
| subprocess | stdlib |
| sys | stdlib |
| time | stdlib |
| typing | stdlib |
| urllib | stdlib |

## Import Checks

| Module | OK | Error |
| --- | --- | --- |
| moneybench | True |  |
| moneybench.release | True |  |
| moneybench.task_runner | True |  |

## Validation

Status: PASS

The core benchmark package imports only Python standard-library modules plus the local `moneybench` package.
