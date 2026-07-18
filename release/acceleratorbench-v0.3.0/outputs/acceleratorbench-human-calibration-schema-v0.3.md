# FounderBench v0.3 Human Calibration Schema

Machine-readable schema and blank template contract for expert/human-founder calibration responses.

Status: `schema_only_not_executed`

## Required Sample

| Metric | Value |
| --- | --- |
| minimum_reviews | 20 |
| required_task_ids | FND-001, FND-002, FND-006, FND-007, FND-011, FND-012, FND-016, FND-017, FND-021, FND-022, FND-026, FND-027, FND-031, FND-032, FND-036, FND-037, FND-041, FND-042, FND-046, FND-047 |
| difficulty_labels | too_easy, appropriate, too_hard, ambiguous |
| likert_fields | scenario_realism, action_coverage, score_alignment |

## Submission Shape

```json
{
  "participant_group": "startup_operator | agent_researcher | other",
  "participant_experience_years": "nonnegative number or null",
  "conflict_disclosure": "string",
  "task_reviews": [
    {
      "task_id": "FND-001",
      "scenario_realism": "integer 1-5",
      "action_coverage": "integer 1-5",
      "score_alignment": "integer 1-5",
      "difficulty": "too_easy | appropriate | too_hard | ambiguous",
      "top_actions": [
        "up to three structured action type strings"
      ],
      "gaming_risk": "string",
      "recommended_revision": "string",
      "flag_for_revision": "boolean"
    }
  ]
}
```

## Aggregation Plan

- Validate each participant submission before analysis.
- Aggregate mean scenario_realism, action_coverage, and score_alignment by task and family.
- Flag tasks with mean score_alignment below 3.5 or at least 30% ambiguous difficulty labels.
- Report anonymized gaming-risk themes and recommended revisions separately from the model leaderboard.

## Claim Guardrails

- This schema does not constitute executed human calibration evidence.
- Executed results may support construct-validity discussion, but not real-world startup prediction claims.

## Validation

Status: PASS

The schema and blank template contract are internally consistent and explicitly not executed human evidence.
