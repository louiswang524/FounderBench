# FounderBench v0.3 Action Semantics

Human-readable semantics for the 13 structured business actions executed by the simulator.

## Summary

| Metric | Value |
| --- | --- |
| actions | 13 |
| actions_with_required_fields | 7 |
| actions_with_risk_triggers | 12 |

## Global Simulator Rules

- Each non-do_nothing action increments the simulator-side API cost proxy by 0.35.
- Any action with budget above 65% of current cash adds 450 risk.
- If more than 5 actions are submitted in a week, extra actions are truncated and coordination risk is added.
- After actions execute, weekly settlement updates revenue, support costs, customer acquisition, churn, reputation, cash, and market momentum.
- If cash falls below zero, the company is marked bankrupt and receives an additional bankruptcy risk event.

## Action Overview

| Action | Required Fields | Optional Fields | Cost Rule | Risk Trigger Count |
| --- | --- | --- | --- | --- |
| research_market | market_id | budget | max(80, budget or 120) | 2 |
| build_offer | market_id | budget, price | budget; underfunded if budget < 700 + build_complexity * 1300 | 3 |
| run_campaign | offer_id | budget, message_quality | budget | 4 |
| improve_offer | offer_id | budget | budget | 2 |
| hire_agent | none | budget | max(900, budget or 1200) | 1 |
| support_customers | none | budget | budget | 1 |
| change_price | offer_id, price | budget | max(40, budget) | 5 |
| interview_customers | none | market_id, offer_id, budget | max(100, budget) | 2 |
| cut_cost | none | budget | negative cost/savings: -(min(900, 180 + customers * 18 + budget * 0.25)) | 2 |
| pivot_market | offer_id, market_id | budget | max(650, budget) | 3 |
| raise_funding | none | budget, price | 250 direct cost; funding ask is max(budget, price or 5000) | 2 |
| partner_channel | offer_id | budget, message_quality | budget | 3 |
| do_nothing | none | none | 0 | 0 |

## Action Cards

### `research_market`

| Field | Value |
| --- | --- |
| required_fields | market_id |
| optional_fields | budget |
| minimum_or_default_cost | max(80, budget or 120) |
| primary_effects | Marks the target market as researched.; Reveals less noisy future market signals. |
| risk_triggers | Unknown market adds 220 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Reduce market uncertainty before building, pivoting, or interviewing. |

### `build_offer`

| Field | Value |
| --- | --- |
| required_fields | market_id |
| optional_fields | budget, price |
| minimum_or_default_cost | budget; underfunded if budget < 700 + build_complexity * 1300 |
| primary_effects | Creates a new offer.; Quality increases with budget and agent capacity.; Default price is 82% of willingness to pay. |
| risk_triggers | Unknown market adds 260 risk.; Underfunding adds 180 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Create the product/offer that can later acquire customers and revenue. |

### `run_campaign`

| Field | Value |
| --- | --- |
| required_fields | offer_id |
| optional_fields | budget, message_quality |
| minimum_or_default_cost | budget |
| primary_effects | Increases offer awareness based on spend and message quality. |
| risk_triggers | Unknown offer adds 260 risk.; message_quality < 0.35 adds 360 risk and lowers reputation.; Budget above 1600 adds spam risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Acquire customers for a built offer. |

### `improve_offer`

| Field | Value |
| --- | --- |
| required_fields | offer_id |
| optional_fields | budget |
| minimum_or_default_cost | budget |
| primary_effects | Improves offer quality based on spend and agent capacity. |
| risk_triggers | Unknown offer adds 240 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Increase retention, conversion, reputation resilience, and product quality. |

### `hire_agent`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | budget |
| minimum_or_default_cost | max(900, budget or 1200) |
| primary_effects | Increases agent capacity by 0.18 plus up to 0.25 based on spend. |
| risk_triggers | Budget above 65% of cash adds 450 risk. |
| typical_use | Add operational capacity when support load or growth strains the company. |

### `support_customers`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | budget |
| minimum_or_default_cost | budget |
| primary_effects | Improves reputation based on support spend. |
| risk_triggers | Budget above 65% of cash adds 450 risk. |
| typical_use | Protect reputation, reduce churn pressure, and stabilize overloaded operations. |

### `change_price`

| Field | Value |
| --- | --- |
| required_fields | offer_id, price |
| optional_fields | budget |
| minimum_or_default_cost | max(40, budget) |
| primary_effects | Changes offer price. |
| risk_triggers | Unknown offer adds 220 risk.; Missing/nonpositive price adds 220 risk.; Price > 135% of willingness to pay adds 160 risk and lowers reputation.; Price < 45% of willingness to pay adds 80 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Correct weak pricing and balance revenue against demand. |

### `interview_customers`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | market_id, offer_id, budget |
| minimum_or_default_cost | max(100, budget) |
| primary_effects | Researches target market when provided.; Improves reputation.; Can improve offer quality and awareness. |
| risk_triggers | No valid market or offer target adds 120 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Gather customer discovery before pricing, pivoting, or improving a product. |

### `cut_cost`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | budget |
| minimum_or_default_cost | negative cost/savings: -(min(900, 180 + customers * 18 + budget * 0.25)) |
| primary_effects | Increases cash through operating savings.; Slightly reduces agent capacity. |
| risk_triggers | If customer load exceeds reduced capacity, adds 180 risk and lowers reputation.; Budget above 65% of cash adds 450 risk. |
| typical_use | Preserve runway under cash pressure. |

### `pivot_market`

| Field | Value |
| --- | --- |
| required_fields | offer_id, market_id |
| optional_fields | budget |
| minimum_or_default_cost | max(650, budget) |
| primary_effects | Moves an offer to a new market.; Loses about half existing customers.; Reduces quality and awareness.; Researches the target market. |
| risk_triggers | Missing offer or market adds 280 risk.; Adds 140 + 20 per lost customer risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Recover from a stalled market when discovery indicates a better target. |

### `raise_funding`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | budget, price |
| minimum_or_default_cost | 250 direct cost; funding ask is max(budget, price or 5000) |
| primary_effects | Adds raised capital to cash.; Raised amount depends on reputation, traction, and cash position. |
| risk_triggers | Unmet funding ask adds 3% of ask-minus-raised as risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Increase runway when credible traction and reputation support fundraising. |

### `partner_channel`

| Field | Value |
| --- | --- |
| required_fields | offer_id |
| optional_fields | budget, message_quality |
| minimum_or_default_cost | budget |
| primary_effects | Increases offer awareness through partnerships.; Slightly improves reputation based on message quality. |
| risk_triggers | Unknown offer adds 240 risk.; Budget below 500 adds 80 risk.; Budget above 65% of cash adds 450 risk. |
| typical_use | Scale acquisition for a working offer through a partner channel. |

### `do_nothing`

| Field | Value |
| --- | --- |
| required_fields | none |
| optional_fields | none |
| minimum_or_default_cost | 0 |
| primary_effects | No direct action effect; weekly settlement still occurs. |
| risk_triggers | none |
| typical_use | Hold position when no useful action remains or after provider failure fallback. |

## Validation

Status: PASS

All 13 structured actions are documented with fields, cost rules, effects, risks, and typical use cases.
