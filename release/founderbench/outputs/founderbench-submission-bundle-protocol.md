# FounderBench Submission Bundle Protocol

Combines single-run JSON files, existing run arrays, or existing {runs: [...]} payloads into one {runs: [...]} bundle and validates every run before comparison.

## Accepted Inputs

- single run object with a results array
- JSON list of run objects
- JSON object with top-level runs array

## Validation Checks

- each run passes moneybench.submission.validate_run
- bundle has benchmark=FounderBench and version=0.3.0
- bundle has at least one run
- no duplicate policy/run_seed pairs

## Output Shape

```json
{
  "benchmark": "FounderBench",
  "version": "0.3.0",
  "created_by": "moneybench.submission_bundle",
  "input_files": [
    "path/to/run-seed0.json"
  ],
  "runs": [
    "validated run objects"
  ]
}
```

## Commands

```powershell
python -m moneybench.submission_bundle --input outputs/founderbench-deepseek-seed0.json --input outputs/founderbench-deepseek-seed1.json --input outputs/founderbench-deepseek-seed2.json --output outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
```
```powershell
python -m moneybench.submission --input outputs/founderbench-deepseek-repeats.json --report outputs/founderbench-deepseek-repeats-submission-report.md
```

## Claim Rule

Repeated-run claims should cite the bundled submission report. Single-run claims must be labeled preliminary unless the statistical protocol permits otherwise.

## Validation

Status: PASS