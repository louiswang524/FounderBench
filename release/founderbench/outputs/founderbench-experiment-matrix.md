# FounderBench Experiment Matrix

This generated matrix states which experiments are needed for a publishable benchmark paper and which evidence files currently prove them. Older v0.2 provider outputs are intentionally excluded from this matrix.

## Summary

| Metric | Value |
| --- | --- |
| experiments | 12 |
| complete | 5 |
| partial | 0 |
| missing | 7 |
| required_missing | 6 |

## Experiment Ledger

| ID | Section | Priority | Status | Evidence Files | Paper Use |
| --- | --- | --- | --- | --- | --- |
| deterministic_rule_baselines | core_baselines | required | complete | 3 | Shows the simulator works, is nontrivial, and separates policies with different business-decision capabilities. |
| capability_ladder_ablation | ablations | required | complete | 1 | Explains which capabilities move the benchmark score and where task-family conditioning matters. |
| action_space_ablation | ablations | required | complete | 2 | Shows that the expanded action space affects outcomes rather than serving as unused interface decoration. |
| random_repeated_seed_calibration | uncertainty | required | complete | 2 | Provides a sanity check for stochastic variance and interval reporting. |
| qualitative_trace_analysis | qualitative | required | complete | 2 | Supports failure analysis and shows that scores come from executable simulator trajectories. |
| deepseek_hosted_baseline | hosted_llm_baselines | required | missing | 0 | Provides a representative hosted LLM baseline. |
| deepseek_self_consistency_k3 | hosted_llm_ablations | recommended | missing | 0 | Tests whether sampling-based self-consistency improves business decision quality. |
| anthropic_hosted_baseline | hosted_llm_baselines | required | missing | 0 | Adds a second hosted LLM family for model differentiation. |
| gemini_hosted_baseline | hosted_llm_baselines | required | missing | 0 | Adds a third hosted LLM family for model differentiation. |
| local_open_source_baseline | open_source_baselines | required | missing | 0 | Makes the comparison accessible beyond closed hosted APIs. |
| hosted_llm_audit_traces | auditability | required | missing | 0 | Allows qualitative analysis of provider failures without exposing secrets. |
| private_holdout_execution | anti_gaming | required_for_final_submission | missing | 0 | Prevents optimization against visible public tasks and supports leaderboard credibility. |

## Missing Required Evidence

### deepseek_hosted_baseline

Run DeepSeek on the complete 50-task current release suite with submission validation.

- Missing `outputs/founderbench-deepseek.json`
- Missing `outputs/founderbench-deepseek-submission-report.md`

Commands:
- `python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek.json --resume`
- `python -m founderbench.submission --input ..\..\outputs\founderbench-deepseek.json --report ..\..\outputs\founderbench-deepseek-submission-report.md`

### anthropic_hosted_baseline

Run Claude/Anthropic on the complete 50-task current release suite with submission validation.

- Missing `outputs/founderbench-anthropic.json`
- Missing `outputs/founderbench-anthropic-submission-report.md`

Commands:
- `python -m founderbench.resumable_runner --policy anthropic --output ..\..\outputs\founderbench-anthropic.json --resume`
- `python -m founderbench.submission --input ..\..\outputs\founderbench-anthropic.json --report ..\..\outputs\founderbench-anthropic-submission-report.md`

### gemini_hosted_baseline

Run Gemini on the complete 50-task current release suite with submission validation.

- Missing `outputs/founderbench-gemini.json`
- Missing `outputs/founderbench-gemini-submission-report.md`

Commands:
- `python -m founderbench.resumable_runner --policy gemini --output ..\..\outputs\founderbench-gemini.json --resume`
- `python -m founderbench.submission --input ..\..\outputs\founderbench-gemini.json --report ..\..\outputs\founderbench-gemini-submission-report.md`

### local_open_source_baseline

Run at least one local/open-source model via the OpenAI-compatible protocol and validate the submission.

- Missing `outputs/founderbench-local-open-model.json`
- Missing `outputs/founderbench-local-open-model-submission-report.md`

Commands:
- `python -m founderbench.local_model health --output ..\..\outputs\local-health.json`
- `python -m founderbench.resumable_runner --policy llm --output ..\..\outputs\founderbench-local-open-model.json --resume --audit`
- `python -m founderbench.submission --input ..\..\outputs\founderbench-local-open-model.json --report ..\..\outputs\founderbench-local-open-model-submission-report.md`

### hosted_llm_audit_traces

Collect redacted audit traces for representative hosted LLM runs.

- Missing `outputs/founderbench-deepseek-audit.json`
- Missing `outputs/founderbench-anthropic-audit.json`
- Missing `outputs/founderbench-gemini-audit.json`

Commands:
- `python -m founderbench.resumable_runner --policy <provider> --output ..\..\outputs\<provider>-audit.json --resume --audit`

### private_holdout_execution

Execute the private holdout protocol on an evaluator-controlled host and report aggregate fields only.

- Missing `outputs/founderbench-private-holdout-results.json`

Commands:
- `Follow outputs/founderbench-private-holdout-evaluator-protocol.md on evaluator host.`
