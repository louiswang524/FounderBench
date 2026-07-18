# FounderBench v0.3 Reviewer Smoke Report

Reviewer smoke report for quickly checking that the benchmark artifact loads, executes one deterministic task, and validates included baseline outputs.

Status: `pass`

## Checks

| ID | Status | Detail |
| --- | --- | --- |
| python_runtime | pass | Python 3.12.10 |
| task_suite_size | pass | 50 tasks loaded. |
| manifest_present | pass | {'path': 'outputs\\acceleratorbench-task-manifest-v0.3.json', 'exists': True, 'bytes': 33738} |
| single_task_execution | pass | FND-001 task_heuristic score=20.0 |
| baseline_submission_validation | pass | Included baseline raw output passes submission validation. |

## Quick Commands

```powershell
python -m moneybench.reviewer_smoke --json-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.json --markdown-output ..\..\outputs\acceleratorbench-reviewer-smoke-v0.3.md
python -m moneybench.task_cli --policy task_heuristic --task FND-001
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-baseline-raw-v0.3.json --report ..\..\outputs\acceleratorbench-submission-validation-v0.3.md
```

## Full Validation

```powershell
python -m unittest discover -s tests -v
python -m moneybench.release validate
python -m moneybench.release bundle
```

## Validation

Status: PASS

The smoke report is internally consistent.
