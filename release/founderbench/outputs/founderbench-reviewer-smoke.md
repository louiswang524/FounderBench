# FounderBench Reviewer Smoke Report

Reviewer smoke report for quickly checking that the benchmark artifact loads, executes one deterministic task, and validates included baseline outputs.

Status: `pass`

## Checks

| ID | Status | Detail |
| --- | --- | --- |
| python_runtime | pass | Python 3.12.10 |
| task_suite_size | pass | 50 tasks loaded. |
| manifest_present | pass | {'path': 'outputs\\founderbench-task-manifest.json', 'exists': True, 'bytes': 33747} |
| single_task_execution | pass | FND-001 task_heuristic score=20.0 |
| baseline_submission_validation | pass | Included baseline raw output passes submission validation. |

## Quick Commands

```powershell
python -m founderbench.reviewer_smoke --json-output ..\..\outputs\founderbench-reviewer-smoke.json --markdown-output ..\..\outputs\founderbench-reviewer-smoke.md
python -m founderbench.task_cli --policy task_heuristic --task FND-001
python -m founderbench.submission --input ..\..\outputs\founderbench-baseline-raw.json --report ..\..\outputs\founderbench-submission-validation.md
```

## Full Validation

```powershell
python -m unittest discover -s tests -v
python -m founderbench.release validate
python -m founderbench.release bundle
```

## Validation

Status: PASS

The smoke report is internally consistent.
