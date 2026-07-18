# FounderBench v0.3 Provider Contract Audit

This generated audit checks parser and simulator-diagnostic behavior for provider outputs before hosted/local model runs are accepted. It is not LLM baseline evidence.

Status: `contract_validated_no_provider_results_claimed`

## Summary

| Metric | Value |
| --- | --- |
| parser_cases | 8 |
| parser_cases_passed | 8 |
| simulator_checks | 3 |
| simulator_checks_passed | 3 |
| llm_baseline_evidence | False |

## Parser Cases

| Case | Expected | Observed | Passed | Parsed Actions |
| --- | --- | --- | --- | --- |
| valid_minimal_do_nothing | pass | pass | yes | 1 |
| invalid_json | invalid_json | invalid_json | yes | 0 |
| invalid_root | invalid_response_root | invalid_response_root | yes | 0 |
| missing_actions | missing_actions | missing_actions | yes | 0 |
| invalid_actions_type | invalid_actions_type | invalid_actions_type | yes | 0 |
| invalid_action_schema | invalid_action_schema | invalid_action_schema | yes | 0 |
| missing_action_type | missing_action_type | missing_action_type | yes | 0 |
| invalid_numeric_field | invalid_numeric_field | invalid_numeric_field | yes | 0 |

## Simulator Diagnostic Checks

| Check | Expected | Observed | Passed |
| --- | --- | --- | --- |
| malformed_provider_output_counted | provider_errors_positive | 10 | yes |
| error_category_preserved | missing_actions | {"missing_actions": 10} | yes |
| malformed_output_fallback_is_diagnostic_counted | provider_error_for_each_fallback_step | {"invalid_actions": 0, "total_actions": 10} | yes |

## Claim Guardrails

- This audit does not unlock hosted/local LLM comparison claims.
- Malformed provider outputs remain counted as benchmark outcomes through diagnostics.
- Evaluator code must not manually repair invalid model outputs outside the adapter/parser contract; fallback actions must remain diagnostic-counted.
- Provider submissions still require complete 50-task JSON outputs and moneybench.submission validation.

## Validation

Status: PASS

Provider-output parsing and simulator diagnostics are internally consistent without claiming provider baseline evidence.
