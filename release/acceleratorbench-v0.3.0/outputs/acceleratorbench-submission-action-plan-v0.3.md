# FounderBench v0.3 Submission Action Plan

Reviewer-facing action plan for clearing the remaining FounderBench submission gates.

Submission gate status: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| steps | 18 |
| required_steps | 17 |
| owner_action_steps | 4 |
| provider_environment_steps | 5 |
| claim_alignment_steps | 3 |
| ready_for_submission | False |

## Action Steps

| ID | Gate | Owner | Priority | Status | Action |
| --- | --- | --- | --- | --- | --- |
| complete_deepseek_hosted_baseline | required_experiments | evaluator | required | missing | Run DeepSeek on the complete 50-task v0.3.0 suite with submission validation. |
| complete_anthropic_hosted_baseline | required_experiments | evaluator | required | missing | Run Claude/Anthropic on the complete 50-task v0.3.0 suite with submission validation. |
| complete_gemini_hosted_baseline | required_experiments | evaluator | required | missing | Run Gemini on the complete 50-task v0.3.0 suite with submission validation. |
| complete_local_open_source_baseline | required_experiments | evaluator | required | missing | Run at least one local/open-source model via the OpenAI-compatible protocol and validate the submission. |
| complete_hosted_llm_audit_traces | required_experiments | evaluator | required | missing | Collect redacted audit traces for representative hosted LLM runs. |
| complete_private_holdout_execution | required_experiments | evaluator | required_for_final_submission | missing | Execute the private holdout protocol on an evaluator-controlled host and report aggregate fields only. |
| configure_deepseek | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for DeepSeek. |
| configure_deepseek_sc | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for DeepSeek self-consistency. |
| configure_anthropic | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for Anthropic Claude. |
| configure_gemini | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for Google Gemini. |
| configure_llm | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for Local/OpenAI-compatible. |
| support_claim_hosted_llm_comparison | claim_evidence_alignment | paper_author | required_for_stronger_claim | unsupported_currently | Either collect evidence for `hosted_llm_comparison` or keep paper wording conservative. |
| support_claim_private_holdout_available | claim_evidence_alignment | paper_author | required_for_stronger_claim | unsupported_currently | Either collect evidence for `private_holdout_available` or keep paper wording conservative. |
| support_claim_real_world_startup_prediction | claim_evidence_alignment | paper_author | required_for_stronger_claim | unsupported_currently | Either collect evidence for `real_world_startup_prediction` or keep paper wording conservative. |
| finalize_license_choice | license_and_citation | project_owner | required | owner_action_required | Select a public release license. |
| finalize_author_metadata | license_and_citation | project_owner | required | owner_action_required | Replace placeholder author metadata in CITATION.cff. |
| finalize_repository_url | license_and_citation | project_owner | required | owner_action_required | Add public repository URL to CITATION.cff. |
| finalize_citation_license_field | license_and_citation | project_owner | required | owner_action_required | Set the CITATION.cff license field to the selected license identifier. |

## Step Details

### complete_deepseek_hosted_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Provides a representative hosted LLM baseline.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-deepseek-v0.3.json`
  - `outputs/acceleratorbench-deepseek-v0.3-submission-report.md`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy deepseek --output ..\..\outputs\acceleratorbench-deepseek-v0.3.json --resume
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-deepseek-v0.3.json --report ..\..\outputs\acceleratorbench-deepseek-v0.3-submission-report.md
```

### complete_anthropic_hosted_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Adds a second hosted LLM family for model differentiation.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-anthropic-v0.3.json`
  - `outputs/acceleratorbench-anthropic-v0.3-submission-report.md`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy anthropic --output ..\..\outputs\acceleratorbench-anthropic-v0.3.json --resume
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-anthropic-v0.3.json --report ..\..\outputs\acceleratorbench-anthropic-v0.3-submission-report.md
```

### complete_gemini_hosted_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Adds a third hosted LLM family for model differentiation.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-gemini-v0.3.json`
  - `outputs/acceleratorbench-gemini-v0.3-submission-report.md`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy gemini --output ..\..\outputs\acceleratorbench-gemini-v0.3.json --resume
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-gemini-v0.3.json --report ..\..\outputs\acceleratorbench-gemini-v0.3-submission-report.md
```

### complete_local_open_source_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Makes the comparison accessible beyond closed hosted APIs.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-local-open-model-v0.3.json`
  - `outputs/acceleratorbench-local-open-model-v0.3-submission-report.md`
- Commands:
```powershell
python -m moneybench.local_model health --output ..\..\outputs\local-health.json
python -m moneybench.resumable_runner --policy llm --output ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --resume --audit
python -m moneybench.submission --input ..\..\outputs\acceleratorbench-local-open-model-v0.3.json --report ..\..\outputs\acceleratorbench-local-open-model-v0.3-submission-report.md
```

### complete_hosted_llm_audit_traces

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Allows qualitative analysis of provider failures without exposing secrets.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-deepseek-v0.3-audit.json`
  - `outputs/acceleratorbench-anthropic-v0.3-audit.json`
  - `outputs/acceleratorbench-gemini-v0.3-audit.json`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy <provider> --output ..\..\outputs\<provider>-audit.json --resume --audit
```

### complete_private_holdout_execution

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Prevents optimization against visible public tasks and supports leaderboard credibility.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-private-holdout-results-v0.3.json`
- Commands:
```powershell
Follow outputs/acceleratorbench-private-holdout-evaluator-protocol-v0.3.md on evaluator host.
```

### configure_deepseek

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `DEEPSEEK_API_KEY`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3.json --resume
python -m moneybench.resumable_runner --policy deepseek --output outputs/acceleratorbench-deepseek-v0.3-audit.json --resume --audit
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-v0.3.json --report outputs/acceleratorbench-deepseek-v0.3-submission-report.md
```

### configure_deepseek_sc

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `DEEPSEEK_API_KEY`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --resume
python -m moneybench.resumable_runner --policy deepseek_sc --output outputs/acceleratorbench-deepseek-sc-k3-v0.3-audit.json --resume --audit
python -m moneybench.submission --input outputs/acceleratorbench-deepseek-sc-k3-v0.3.json --report outputs/acceleratorbench-deepseek-sc-k3-v0.3-submission-report.md
```

### configure_anthropic

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `ANTHROPIC_API_KEY`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3.json --resume
python -m moneybench.resumable_runner --policy anthropic --output outputs/acceleratorbench-anthropic-v0.3-audit.json --resume --audit
python -m moneybench.submission --input outputs/acceleratorbench-anthropic-v0.3.json --report outputs/acceleratorbench-anthropic-v0.3-submission-report.md
```

### configure_gemini

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `GEMINI_API_KEY`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3.json --resume
python -m moneybench.resumable_runner --policy gemini --output outputs/acceleratorbench-gemini-v0.3-audit.json --resume --audit
python -m moneybench.submission --input outputs/acceleratorbench-gemini-v0.3.json --report outputs/acceleratorbench-gemini-v0.3-submission-report.md
```

### configure_llm

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `OPENAI_COMPAT_BASE_URL`
- Commands:
```powershell
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3.json --resume
python -m moneybench.resumable_runner --policy llm --output outputs/acceleratorbench-local-open-model-v0.3-audit.json --resume --audit
python -m moneybench.submission --input outputs/acceleratorbench-local-open-model-v0.3.json --report outputs/acceleratorbench-local-open-model-v0.3-submission-report.md
```

### support_claim_hosted_llm_comparison

- Gate: `claim_evidence_alignment`
- Owner: `paper_author`
- Claim impact: Permitted wording now: Provider adapters and experiment protocols are included; hosted v0.3 LLM results remain to be run.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-deepseek-v0.3.json`
  - `outputs/acceleratorbench-anthropic-v0.3.json`
  - `outputs/acceleratorbench-gemini-v0.3.json`

### support_claim_private_holdout_available

- Gate: `claim_evidence_alignment`
- Owner: `paper_author`
- Claim impact: Permitted wording now: v0.3.0 includes a private-holdout blueprint and evaluator protocol, not executed hidden results.
- Missing inputs/outputs:
  - `outputs/acceleratorbench-private-holdout-results-v0.3.json`

### support_claim_real_world_startup_prediction

- Gate: `claim_evidence_alignment`
- Owner: `paper_author`
- Claim impact: Permitted wording now: FounderBench is a synthetic controlled environment for studying startup-relevant decisions.
- Missing inputs/outputs:
  - `executed human/expert validation study`
  - `real-world outcome correlation study`

### finalize_license_choice

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: External users need explicit reuse, modification, and redistribution terms.
- Missing inputs/outputs:
  - `work/moneybench/LICENSE`
- Commands:
```powershell
python -m moneybench.release regenerate
python -m moneybench.release validate
```

### finalize_author_metadata

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Citation metadata must identify artifact authors before public release.
- Missing inputs/outputs:
  - `work/moneybench/CITATION.cff`
- Commands:
```powershell
python -m moneybench.release regenerate
python -m moneybench.release validate
```

### finalize_repository_url

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Reviewers and users need a stable source-code location.
- Missing inputs/outputs:
  - `work/moneybench/CITATION.cff`
- Commands:
```powershell
python -m moneybench.release regenerate
python -m moneybench.release validate
```

### finalize_citation_license_field

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Citation tooling expects machine-readable license metadata.
- Missing inputs/outputs:
  - `work/moneybench/CITATION.cff`
- Commands:
```powershell
python -m moneybench.release regenerate
python -m moneybench.release validate
```

## Validation

Status: PASS

The action plan is internally consistent with the current submission gate.
