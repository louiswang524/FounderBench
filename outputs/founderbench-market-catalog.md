# FounderBench Market Catalog

Human-readable catalog of the fixed simulated markets used in current release.

## Summary

| Metric | Value |
| --- | --- |
| markets | 8 |
| mean_base_demand | 0.674 |
| mean_competition | 0.495 |
| mean_willingness_to_pay | 271.88 |
| mean_support_load | 0.351 |

## Observation Rules

- Unresearched markets expose noisy demand, competition, and willingness-to-pay signals.
- research_market or interview_customers with a market_id marks that market as researched.
- Researched markets expose exact current demand, exact competition, and exact willingness-to-pay signals.
- Current demand equals base_demand plus seed-dependent market momentum, clamped to [0.05, 1.2].
- Market momentum evolves each week using volatility-scaled shocks and decay.

## Settlement Rules

- Customer acquisition increases with demand, awareness, quality, price fit, and reputation.
- Competition subtracts from conversion.
- Churn depends on support load, offer quality, and reputation.
- Weekly support cost scales with customers and support load.
- Support overload can reduce reputation when support_required exceeds agent_capacity * 30.

## Market Parameters

| Market ID | Name | Demand | Competition | WTP | Build Complexity | Support Load | Volatility |
| --- | --- | --- | --- | --- | --- | --- | --- |
| saas_churn | Indie SaaS | 0.76 | 0.38 | 260 | 0.45 | 0.34 | 0.11 |
| legal_summary | Small Law Firms | 0.82 | 0.78 | 420 | 0.58 | 0.52 | 0.08 |
| shopify_seo | Shopify Stores | 0.68 | 0.61 | 180 | 0.32 | 0.28 | 0.17 |
| recruiting_brief | Recruiters | 0.62 | 0.44 | 145 | 0.25 | 0.31 | 0.13 |
| data_cleanup | Ops Teams | 0.58 | 0.32 | 210 | 0.4 | 0.22 | 0.1 |
| support_triage | B2B Support | 0.72 | 0.52 | 330 | 0.55 | 0.47 | 0.12 |
| grant_scan | Research Labs | 0.47 | 0.25 | 390 | 0.36 | 0.29 | 0.18 |
| sales_intel | Sales Teams | 0.74 | 0.66 | 240 | 0.42 | 0.38 | 0.15 |

## Market Bands

| Market ID | Demand | Competition | Build Complexity | Support Load | Volatility |
| --- | --- | --- | --- | --- | --- |
| saas_churn | high | low | medium | medium | medium |
| legal_summary | high | high | high | high | low |
| shopify_seo | medium | medium | low | low | high |
| recruiting_brief | medium | medium | low | medium | medium |
| data_cleanup | medium | low | medium | low | medium |
| support_triage | medium | medium | high | high | medium |
| grant_scan | low | low | medium | low | high |
| sales_intel | high | high | medium | medium | medium |

## Market Cards

### `saas_churn`: Indie SaaS

| Field | Value |
| --- | --- |
| need | weekly churn-risk reports |
| base_demand | 0.76 |
| competition | 0.38 |
| willingness_to_pay | 260 |
| build_complexity | 0.45 |
| support_load | 0.34 |
| volatility | 0.11 |
| bands | demand=high, competition=low, support=medium |

### `legal_summary`: Small Law Firms

| Field | Value |
| --- | --- |
| need | document summary packs |
| base_demand | 0.82 |
| competition | 0.78 |
| willingness_to_pay | 420 |
| build_complexity | 0.58 |
| support_load | 0.52 |
| volatility | 0.08 |
| bands | demand=high, competition=high, support=high |

### `shopify_seo`: Shopify Stores

| Field | Value |
| --- | --- |
| need | SEO product page refresh |
| base_demand | 0.68 |
| competition | 0.61 |
| willingness_to_pay | 180 |
| build_complexity | 0.32 |
| support_load | 0.28 |
| volatility | 0.17 |
| bands | demand=medium, competition=medium, support=low |

### `recruiting_brief`: Recruiters

| Field | Value |
| --- | --- |
| need | candidate briefing notes |
| base_demand | 0.62 |
| competition | 0.44 |
| willingness_to_pay | 145 |
| build_complexity | 0.25 |
| support_load | 0.31 |
| volatility | 0.13 |
| bands | demand=medium, competition=medium, support=medium |

### `data_cleanup`: Ops Teams

| Field | Value |
| --- | --- |
| need | spreadsheet cleanup automation |
| base_demand | 0.58 |
| competition | 0.32 |
| willingness_to_pay | 210 |
| build_complexity | 0.4 |
| support_load | 0.22 |
| volatility | 0.1 |
| bands | demand=medium, competition=low, support=low |

### `support_triage`: B2B Support

| Field | Value |
| --- | --- |
| need | ticket triage workflow |
| base_demand | 0.72 |
| competition | 0.52 |
| willingness_to_pay | 330 |
| build_complexity | 0.55 |
| support_load | 0.47 |
| volatility | 0.12 |
| bands | demand=medium, competition=medium, support=high |

### `grant_scan`: Research Labs

| Field | Value |
| --- | --- |
| need | grant opportunity scans |
| base_demand | 0.47 |
| competition | 0.25 |
| willingness_to_pay | 390 |
| build_complexity | 0.36 |
| support_load | 0.29 |
| volatility | 0.18 |
| bands | demand=low, competition=low, support=low |

### `sales_intel`: Sales Teams

| Field | Value |
| --- | --- |
| need | account intelligence briefs |
| base_demand | 0.74 |
| competition | 0.66 |
| willingness_to_pay | 240 |
| build_complexity | 0.42 |
| support_load | 0.38 |
| volatility | 0.15 |
| bands | demand=high, competition=high, support=medium |

## Validation

Status: PASS

All 8 fixed markets have unique ids, numeric simulator parameters, and documented observation/settlement rules.
