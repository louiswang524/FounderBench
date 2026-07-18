# FounderBench Human Calibration Protocol

Protocol for expert or human-founder calibration of the synthetic startup-agent task suite.

Status: `protocol_only_not_executed`

## Research Questions

- Do task incentives match expert startup-operator judgment?
- Do score components reward decisions that experts consider sensible under the stated constraints?
- Which task families are too easy, too hard, or underspecified for human operators?
- How should model scores be interpreted relative to human/expert action rankings?

## Participant Groups

| Group | Target N | Eligibility | Role |
| --- | --- | --- | --- |
| startup operators | 5-10 | Founders, operators, or accelerator mentors with experience evaluating early-stage startup decisions. | Rate scenario realism, action quality, and scoring alignment. |
| technical agent researchers | 3-5 | Researchers or engineers familiar with LLM agent evaluation and tool-use benchmarks. | Rate benchmark clarity, action interface coverage, and anti-gaming risks. |

## Task Sampling

| Field | Value |
| --- | --- |
| strategy | stratified_by_family |
| minimum_tasks | 20 |
| recommended_tasks | 30 |
| coverage_rule | Sample at least two tasks from each of the 10 task families; include public_dev and public_test tasks. |
| materials | task card, market catalog entry, action semantics, score rubric, representative baseline trace when available |

## Review Instrument

| Item | Scale | Prompt |
| --- | --- | --- |
| scenario_realism | 1-5 Likert | The startup situation is plausible enough for evaluating business-decision quality. |
| action_coverage | 1-5 Likert | The available structured actions cover the main reasonable moves in this scenario. |
| score_alignment | 1-5 Likert | The scoring rubric rewards decisions I would consider operationally sound. |
| difficulty | too_easy / appropriate / too_hard / ambiguous | The task difficulty is appropriate for differentiating agents. |
| best_action_ranking | ranked list | Rank the top three actions or action sequences you would recommend. |
| gaming_risk | free text | Describe any way a model could exploit the task without making a sensible business decision. |

## Analysis Plan

- Report mean and distribution of scenario_realism, action_coverage, and score_alignment by task family.
- Flag tasks with mean score_alignment below 3.5 or more than 30% ambiguous difficulty labels.
- Compute agreement between expert top-action rankings and high-scoring baseline/model trajectories.
- Qualitatively summarize gaming risks and convert accepted issues into task or rubric revisions.
- Keep expert calibration separate from the official leaderboard until the protocol has been executed.

## Reporting Fields

- `participant_count_by_group`
- `task_ids_reviewed`
- `family_coverage`
- `mean_scenario_realism`
- `mean_action_coverage`
- `mean_score_alignment`
- `difficulty_distribution`
- `flagged_tasks`
- `recommended_revisions`
- `limitations`

## Claim Guardrails

- Before execution, describe this only as a proposed calibration protocol.
- Do not claim that FounderBench is validated against human startup judgment until results are collected.
- Even after execution, treat expert agreement as construct-validity evidence, not proof of real-world startup success prediction.

## Ethics and Privacy

- Do not collect confidential company details or private customer data.
- Allow participants to skip scenarios that overlap with nonpublic work.
- Report aggregate ratings and anonymized free-text themes.
- Record compensation, recruitment source, and conflicts of interest in the final study report.

## Validation

Status: PASS

The protocol is internally valid and explicitly marked as not yet executed.
