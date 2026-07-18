from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

ActionType = Literal[
    "research_market",
    "build_offer",
    "run_campaign",
    "improve_offer",
    "hire_agent",
    "support_customers",
    "change_price",
    "interview_customers",
    "cut_cost",
    "pivot_market",
    "raise_funding",
    "partner_channel",
    "do_nothing",
]


@dataclass(frozen=True)
class Market:
    market_id: str
    name: str
    need: str
    base_demand: float
    competition: float
    willingness_to_pay: float
    build_complexity: float
    support_load: float
    volatility: float


@dataclass
class Offer:
    offer_id: str
    market_id: str
    price: float
    quality: float
    awareness: float = 0.0
    customers: int = 0
    age: int = 0


@dataclass
class CompanyState:
    week: int = 1
    cash: float = 10_000.0
    reputation: float = 0.55
    agent_capacity: float = 1.0
    offers: list[Offer] = field(default_factory=list)
    memory: list[str] = field(default_factory=list)
    cumulative_revenue: float = 0.0
    cumulative_cost: float = 0.0
    cumulative_api_cost: float = 0.0
    total_risk_penalty: float = 0.0
    total_funding_raised: float = 0.0
    action_counts: dict[str, int] = field(default_factory=dict)
    bankrupt: bool = False


@dataclass(frozen=True)
class Action:
    type: ActionType
    market_id: str | None = None
    offer_id: str | None = None
    budget: float = 0.0
    price: float | None = None
    message_quality: float = 0.6
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class StepResult:
    revenue: float
    cost: float
    profit: float
    new_customers: int
    churned_customers: int
    risk_penalty: float
    notes: list[str]


@dataclass
class Observation:
    week: int
    cash: float
    reputation: float
    agent_capacity: float
    markets: list[dict[str, Any]]
    offers: list[dict[str, Any]]
    memory: list[str]
