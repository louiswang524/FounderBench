# FounderBench Submission Action Plan

Reviewer-facing action plan for clearing the remaining FounderBench submission gates.

Submission gate status: `not_ready`

## Summary

| Metric | Value |
| --- | --- |
| steps | 25 |
| required_steps | 17 |
| owner_action_steps | 4 |
| provider_environment_steps | 12 |
| claim_alignment_steps | 3 |
| ready_for_submission | False |

## Action Steps

| ID | Gate | Owner | Priority | Status | Action |
| --- | --- | --- | --- | --- | --- |
| complete_deepseek_hosted_baseline | required_experiments | evaluator | required | missing | Run DeepSeek on the complete 50-task current release suite with submission validation. |
| complete_anthropic_hosted_baseline | required_experiments | evaluator | required | missing | Run Claude/Anthropic on the complete 50-task current release suite with submission validation. |
| complete_gemini_hosted_baseline | required_experiments | evaluator | required | missing | Run Gemini on the complete 50-task current release suite with submission validation. |
| complete_local_open_source_baseline | required_experiments | evaluator | required | missing | Run at least one local/open-source model via the OpenAI-compatible protocol and validate the submission. |
| complete_hosted_llm_audit_traces | required_experiments | evaluator | required | missing | Collect redacted audit traces for representative hosted LLM runs. |
| complete_private_holdout_execution | required_experiments | evaluator | required_for_final_submission | missing | Execute the private holdout protocol on an evaluator-controlled host and report aggregate fields only. |
| configure_openai | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for OpenAI GPT. |
| configure_deepseek | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for DeepSeek. |
| configure_deepseek_sc | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for DeepSeek self-consistency. |
| configure_anthropic | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for Anthropic Claude. |
| configure_gemini | provider_run_readiness | evaluator | required | blocked_on_environment | Configure provider environment for Google Gemini. |
| configure_kimi | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for Moonshot Kimi. |
| configure_qwen | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for Alibaba Qwen. |
| configure_mistral | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for Mistral. |
| configure_glm | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for Z.ai GLM. |
| configure_xai | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for xAI Grok. |
| configure_llama | provider_run_readiness | evaluator | recommended | blocked_on_environment | Configure provider environment for Llama/Open-weight endpoint. |
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
  - `outputs/founderbench-deepseek.json`
  - `outputs/founderbench-deepseek-submission-report.md`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy deepseek --output ..\..\outputs\founderbench-deepseek.json --resume
python -m founderbench.submission --input ..\..\outputs\founderbench-deepseek.json --report ..\..\outputs\founderbench-deepseek-submission-report.md
```

### complete_anthropic_hosted_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Adds a second hosted LLM family for model differentiation.
- Missing inputs/outputs:
  - `outputs/founderbench-anthropic.json`
  - `outputs/founderbench-anthropic-submission-report.md`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy anthropic --output ..\..\outputs\founderbench-anthropic.json --resume
python -m founderbench.submission --input ..\..\outputs\founderbench-anthropic.json --report ..\..\outputs\founderbench-anthropic-submission-report.md
```

### complete_gemini_hosted_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Adds a third hosted LLM family for model differentiation.
- Missing inputs/outputs:
  - `outputs/founderbench-gemini.json`
  - `outputs/founderbench-gemini-submission-report.md`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy gemini --output ..\..\outputs\founderbench-gemini.json --resume
python -m founderbench.submission --input ..\..\outputs\founderbench-gemini.json --report ..\..\outputs\founderbench-gemini-submission-report.md
```

### complete_local_open_source_baseline

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Makes the comparison accessible beyond closed hosted APIs.
- Missing inputs/outputs:
  - `outputs/founderbench-local-open-model.json`
  - `outputs/founderbench-local-open-model-submission-report.md`
- Commands:
```powershell
python -m founderbench.local_model health --output ..\..\outputs\local-health.json
python -m founderbench.resumable_runner --policy llm --output ..\..\outputs\founderbench-local-open-model.json --resume --audit
python -m founderbench.submission --input ..\..\outputs\founderbench-local-open-model.json --report ..\..\outputs\founderbench-local-open-model-submission-report.md
```

### complete_hosted_llm_audit_traces

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Allows qualitative analysis of provider failures without exposing secrets.
- Missing inputs/outputs:
  - `outputs/founderbench-deepseek-audit.json`
  - `outputs/founderbench-anthropic-audit.json`
  - `outputs/founderbench-gemini-audit.json`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy <provider> --output ..\..\outputs\<provider>-audit.json --resume --audit
```

### complete_private_holdout_execution

- Gate: `required_experiments`
- Owner: `evaluator`
- Claim impact: Prevents optimization against visible public tasks and supports leaderboard credibility.
- Missing inputs/outputs:
  - `outputs/founderbench-private-holdout-results.json`
- Commands:
```powershell
Follow outputs/founderbench-private-holdout-evaluator-protocol.md on evaluator host.
```

### configure_openai

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `OPENAI_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai.json --resume
python -m founderbench.resumable_runner --policy openai --output outputs/founderbench-openai-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-openai.json --report outputs/founderbench-openai-submission-report.md
```

### configure_deepseek

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `DEEPSEEK_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek.json --resume
python -m founderbench.resumable_runner --policy deepseek --output outputs/founderbench-deepseek-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-deepseek.json --report outputs/founderbench-deepseek-submission-report.md
```

### configure_deepseek_sc

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `DEEPSEEK_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3.json --resume
python -m founderbench.resumable_runner --policy deepseek_sc --output outputs/founderbench-deepseek-sc-k3-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-deepseek-sc-k3.json --report outputs/founderbench-deepseek-sc-k3-submission-report.md
```

### configure_anthropic

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `ANTHROPIC_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic.json --resume
python -m founderbench.resumable_runner --policy anthropic --output outputs/founderbench-anthropic-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-anthropic.json --report outputs/founderbench-anthropic-submission-report.md
```

### configure_gemini

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `GEMINI_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini.json --resume
python -m founderbench.resumable_runner --policy gemini --output outputs/founderbench-gemini-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-gemini.json --report outputs/founderbench-gemini-submission-report.md
```

### configure_kimi

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `KIMI_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi.json --resume
python -m founderbench.resumable_runner --policy kimi --output outputs/founderbench-kimi-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-kimi.json --report outputs/founderbench-kimi-submission-report.md
```

### configure_qwen

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `QWEN_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen.json --resume
python -m founderbench.resumable_runner --policy qwen --output outputs/founderbench-qwen-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-qwen.json --report outputs/founderbench-qwen-submission-report.md
```

### configure_mistral

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `MISTRAL_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral.json --resume
python -m founderbench.resumable_runner --policy mistral --output outputs/founderbench-mistral-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-mistral.json --report outputs/founderbench-mistral-submission-report.md
```

### configure_glm

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `GLM_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm.json --resume
python -m founderbench.resumable_runner --policy glm --output outputs/founderbench-glm-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-glm.json --report outputs/founderbench-glm-submission-report.md
```

### configure_xai

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
  - `XAI_API_KEY`
- Commands:
```powershell
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai.json --resume
python -m founderbench.resumable_runner --policy xai --output outputs/founderbench-xai-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-xai.json --report outputs/founderbench-xai-submission-report.md
```

### configure_llama

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
- Commands:
```powershell
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama.json --resume
python -m founderbench.resumable_runner --policy llama --output outputs/founderbench-llama-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-llama.json --report outputs/founderbench-llama-submission-report.md
```

### configure_llm

- Gate: `provider_run_readiness`
- Owner: `evaluator`
- Claim impact: Required before hosted/local LLM comparison claims can be made.
- Missing inputs/outputs:
- Commands:
```powershell
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model.json --resume
python -m founderbench.resumable_runner --policy llm --output outputs/founderbench-local-open-model-audit.json --resume --audit
python -m founderbench.submission --input outputs/founderbench-local-open-model.json --report outputs/founderbench-local-open-model-submission-report.md
```

### support_claim_hosted_llm_comparison

- Gate: `claim_evidence_alignment`
- Owner: `paper_author`
- Claim impact: Permitted wording now: Provider adapters and experiment protocols are included; hosted current release LLM results remain to be run.
- Missing inputs/outputs:
  - `outputs/founderbench-deepseek.json`
  - `outputs/founderbench-anthropic.json`
  - `outputs/founderbench-gemini.json`

### support_claim_private_holdout_available

- Gate: `claim_evidence_alignment`
- Owner: `paper_author`
- Claim impact: Permitted wording now: The benchmark includes a private-holdout blueprint and evaluator protocol, not executed hidden results.
- Missing inputs/outputs:
  - `outputs/founderbench-private-holdout-results.json`

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
  - `work/founderbench/LICENSE`
- Commands:
```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
```

### finalize_author_metadata

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Citation metadata must identify artifact authors before public release.
- Missing inputs/outputs:
  - `work/founderbench/CITATION.cff`
- Commands:
```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
```

### finalize_repository_url

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Reviewers and users need a stable source-code location.
- Missing inputs/outputs:
  - `work/founderbench/CITATION.cff`
- Commands:
```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
```

### finalize_citation_license_field

- Gate: `license_and_citation`
- Owner: `project_owner`
- Claim impact: Citation tooling expects machine-readable license metadata.
- Missing inputs/outputs:
  - `work/founderbench/CITATION.cff`
- Commands:
```powershell
python -m founderbench.release regenerate
python -m founderbench.release validate
```

## Validation

Status: PASS

The action plan is internally consistent with the current submission gate.
