# FounderBench Result Integrity Audit

Raw-to-report integrity audit for deterministic baseline results.

## Source Files

| Role | Path |
| --- | --- |
| raw | outputs\founderbench-baseline-raw.json |
| leaderboard | outputs\founderbench-baseline-leaderboard.json |
| paper_tables | outputs\founderbench-paper-tables.json |
| model_comparison | outputs\founderbench-model-comparison.json |

## Summary

| Metric | Value |
| --- | --- |
| raw_runs | 4 |
| policies_checked | 4 |
| policies_passed | 4 |
| policies_failed | 0 |
| all_ordering_checks_passed | True |
| all_integrity_checks_passed | True |

## Ordering Checks

| Check | Passed |
| --- | --- |
| leaderboard_order_matches_raw | True |
| paper_table_order_matches_raw | True |
| model_comparison_order_matches_raw | True |

## Policy Checks

| Policy | Status | Raw Tasks | Raw Avg | Leaderboard Avg | Paper Table Avg | Model Comparison Avg | Problems |
| --- | --- | --- | --- | --- | --- | --- | --- |
| task_heuristic | pass | 50 | 80.9 | 80.9 | 80.90 | 80.90 |  |
| heuristic | pass | 50 | 61.01 | 61.01 | 61.01 | 61.01 |  |
| conservative | pass | 50 | 54.04 | 54.04 | 54.04 | 54.04 |  |
| random | pass | 50 | 33.3 | 33.3 | 33.30 | 33.30 |  |

## Claim Guardrail

Deterministic baseline tables are paper-eligible only while this audit passes; hosted/local provider rows require separate submission validation before inclusion.

## Validation

Status: PASS

Raw deterministic baseline results exactly reproduce leaderboard, paper-table, and model-comparison rows.
