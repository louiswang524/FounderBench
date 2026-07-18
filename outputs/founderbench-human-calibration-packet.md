# FounderBench Human Calibration Recruitment Packet

Recruitment and operator packet for executing expert/human-founder calibration without treating planned work as evidence.

Status: `recruitment_packet_not_executed`

## Participant Plan

| Group | Minimum N |
| --- | --- |
| startup_operators | 6 |
| accelerator_or_investor_mentors | 3 |
| agent_evaluation_researchers | 3 |
| minimum_total | 12 |

Separate startup-judgment validity from benchmark-interface validity while keeping the first calibration wave feasible.

## Required Task Sample

| Field | Value |
| --- | --- |
| strategy | stratified_by_family |
| minimum_reviews_per_participant | 20 |
| coverage_rule | Sample at least two tasks from each of the 10 task families; include public_dev and public_test tasks. |
| required_task_ids | FND-001, FND-002, FND-006, FND-007, FND-011, FND-012, FND-016, FND-017, FND-021, FND-022, FND-026, FND-027, FND-031, FND-032, FND-036, FND-037, FND-041, FND-042, FND-046, FND-047 |

## Materials

| Path | Use |
| --- | --- |
| outputs/founderbench-human-calibration-protocol.md | Study purpose, participant groups, instrument, analysis plan, privacy notes, and claim guardrails. |
| outputs/founderbench-human-calibration-schema.json | Machine-readable response contract for validating completed reviews. |
| outputs/founderbench-human-calibration-template.json | Blank participant response template; do not treat blanks or synthetic examples as data. |
| outputs/founderbench-task-cards.md | Scenario cards for the required sampled tasks and optional extra review tasks. |
| outputs/founderbench-action-semantics.md | Action vocabulary reference so participants can rank structured actions consistently. |
| outputs/founderbench-score-rubric.md | Score-component reference for judging whether incentives match operator judgment. |
| outputs/founderbench-task-feasibility-audit.md | Task-level ledger for prioritizing external calibration on unsolved or ambiguous tasks. |
| outputs/founderbench-human-calibration-analysis.md | Generated analysis report; currently should state no executed submissions unless real responses are supplied. |

## Collection Workflow

1. Confirm ethics/IRB requirements, compensation, recruitment source, and conflict-disclosure policy before contacting participants.
2. Give each participant the task cards, action semantics, score rubric, and blank JSON response template.
3. Ask participants to complete all required sampled tasks and optionally mark any scenario they skip because of confidentiality overlap.
4. Validate each returned JSON response with `founderbench.human_calibration_schema.validate_submission` before analysis.
5. Run `python -m founderbench.human_calibration_analysis --input <submission.json> --json-output <analysis.json> --markdown-output <analysis.md>` after real submissions are collected.
6. Update the claim-evidence report, validity report, paper draft, and task revisions only after executed calibration has passed validation.

## Review Questions

- Is the startup situation plausible under the stated cash, market, and time constraints?
- Do the available actions cover the main reasonable operator moves?
- Does the scoring reward decisions you would consider sound for this scenario?
- Which task should be revised first, and why?
- What is the most likely way a model could exploit the task without making a sensible business decision?
- Which top three structured actions or action sequences would you recommend?

## Expected Post-Collection Outputs

- validated participant JSON submissions stored outside the public release unless consent permits release
- regenerated human calibration analysis JSON and Markdown
- task revision ledger for accepted calibration issues
- paper wording update that reports participant counts, recruitment sources, conflicts, and limitations

## Claim Guardrails

- This packet is not executed human calibration evidence.
- Do not claim human agreement, construct validity, or expert validation until real participant submissions are collected and analyzed.
- Do not use synthetic, blank, or internally generated responses as human evidence.
- Even executed calibration can support task-realism and score-alignment discussion only; it cannot prove real-world startup success prediction.

## Ethics Guardrails

- Do not collect confidential company, customer, financial, or investment information.
- Record recruitment source, compensation, conflicts of interest, and any institutional ethics/IRB determination.
- Allow participants to skip scenarios that overlap with nonpublic work.
- Publish only aggregate ratings and anonymized themes unless explicit participant consent covers broader release.

## Validation

Status: PASS

The packet is internally consistent and explicitly marked as not executed human evidence.
