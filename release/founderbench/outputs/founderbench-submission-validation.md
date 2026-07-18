# FounderBench Model Submission Report

Input: `C:\Users\louis\Documents\Codex\2026-07-14\use\outputs\founderbench-baseline-raw.json`
Benchmark version: `0.3.0`
Runs checked: 4

## Validation

Status: PASS

The submission contains complete task coverage, split summaries, and required diagnostics.

## Leaderboard Summary

| Policy | Tasks | Solved | Solve Rate | Avg Score | Public Dev | Public Test | Provider Errors | Invalid Actions | Over-Budget | Provider Tokens | Cost USD |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | 50 | 37 | 0.74 | 80.90 | 81.73 | 79.66 | 0 | 0 | 5 | 0 | 0.0000 |
| heuristic | 50 | 19 | 0.38 | 61.01 | 65.10 | 54.87 | 0 | 0 | 0 | 0 | 0.0000 |
| conservative | 50 | 13 | 0.26 | 54.04 | 55.31 | 52.13 | 0 | 0 | 0 | 0 | 0.0000 |
| random | 50 | 4 | 0.08 | 33.30 | 26.11 | 44.07 | 0 | 0 | 15 | 0 | 0.0000 |

## Repeated-Run Summary

When multiple runs share a policy name, intervals estimate stochastic variation across submitted runs. Single runs are marked `n/a`.

| Policy | Runs | Mean Avg Score | Score 95% CI | Solve Rate 95% CI |
| --- | --- | --- | --- | --- |
| conservative | 1 | n/a | n/a | n/a |
| heuristic | 1 | n/a | n/a | n/a |
| random | 1 | n/a | n/a | n/a |
| task_heuristic | 1 | n/a | n/a | n/a |

## Split Coverage

| Split | Task Results |
| --- | --- |
| public_dev | 120 |
| public_test | 80 |
