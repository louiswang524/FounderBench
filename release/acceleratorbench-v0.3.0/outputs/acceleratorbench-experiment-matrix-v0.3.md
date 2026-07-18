# FounderBench v0.3 Experiment Matrix

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

Run DeepSeek on the complete 50-task v0.3.0 suite with submission validation.

- Missing `outputs/acceleratorbench-deepseek-v0.3.json`
- Missing `outputs/acceleratorbench-deepseek-v0.3-submission-report.md`

Commands:
- `python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3.json --resume`
- `python -m moneybench.submission --input ..\..\outputs\acceleratorbench-deepseek-v0.3.json --report ..\..\outputs\acceleratorbench-deepseek-v0.3-submission-report.md`

### anthropic_hosted_baseline

Run Claude/Anthropic on the complete 50-task v0.3.0 suite with submission validation.

- Missing `outputs/acceleratorbench-anthropic-v0.3.json`
- Missing `outputs/acceleratorbench-anthropic-v0.3-submission-report.md`

Commands:
- `python -m moneybench.resumable_runner --policy anthropic --output ..\..\outputs\acceleratorbench-anthropic-v0.3.json --resume`
- `python -m moneybench.submission --input ..\..\outputs\acceleratorbench-anthropic-v0.3.json --report ..\..\outputs\acceleratorbench-anthropic-v0.3-submission-report.md`

### gemini_hosted_baseline

Run Gemini on the complete 50-task v0.3.0 suite with submission validation.

- Missing `outputs/acceleratorbench-gemini-v0.3.json`
- Missing `outputs/acceleratorbench-gemini-v0.3-submission-report.md`

Commands:
- `python -m moneybench.resumable_runner --policy gemini --output ..\..\outputs\acceleratorbench-gemini-v0.3.json --resume`
- `python -m moneybench.submission --input ..\..\outputs\acceleratorbench-gemini-v0.3.json --report ..\..\outputs\acceleratorbench-gemini-v0.3-submission-report.md`

### local_open_source_baseline

Run at least one local/open-source model via the OpenAI-compatible protocol and validate the submission.

- Missing `outputs/acceleratorbench-local-open-model-v0.3.json`
- Missing `outputs/acceleratorbench-local-open-model-v0.3-submission-report.md`

Commands:
- `python -m moneybench.local_model health --output ..\..\outputs\local-health.json`
- `python -m moneybench.resumable_runner --policy llm --output ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --resume --audit`
- `python -m moneybench.submission --input ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --report ..\..\outputs\acceleratorbench-local-open-model-v0.3-submission-report.md`

### hosted_llm_audit_traces

Collect redacted audit traces for representative hosted LLM runs.

- Missing `outputs/acceleratorbench-deepseek-v0.3-audit.json`
- Missing `outputs/acceleratorbench-anthropic-v0.3-audit.json`
- Missing `outputs/acceleratorbench-gemini-v0.3-audit.json`

Commands:
- `python -m moneybench.resumable_runner --policy <provider> --output ..\..\outputs\<provider>-audit.json --resume --audit`

### private_holdout_execution

Execute the private holdout protocol on an evaluator-controlled host and report aggregate fields only.

- Missing `outputs/acceleratorbench-private-holdout-results-v0.3.json`

Commands:
- `Follow outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md on evaluator host.`
