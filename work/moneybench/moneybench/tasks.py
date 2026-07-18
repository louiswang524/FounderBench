from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable

from .env import MoneyBenchEnv
from .schema import Action, CompanyState, Offer, StepResult


@dataclass(frozen=True)
class TaskScore:
    task_id: str
    name: str
    score: float
    passed: bool
    metrics: dict[str, float | int | bool]
    notes: list[str]


@dataclass(frozen=True)
class StartupTask:
    task_id: str
    name: str
    description: str
    seed: int
    weeks: int
    pass_threshold: float
    setup: Callable[[MoneyBenchEnv], None]
    score: Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]
    allowed_actions: set[str] = field(
        default_factory=lambda: {
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
        }
    )


def clamp_score(value: float) -> float:
    return round(max(0.0, min(100.0, value)), 2)


def active_customers(env: MoneyBenchEnv) -> int:
    return sum(offer.customers for offer in env.state.offers)


def recurring_revenue(env: MoneyBenchEnv) -> float:
    return sum(offer.customers * offer.price for offer in env.state.offers)


def max_weekly_revenue(results: list[StepResult]) -> float:
    return max((result.revenue for result in results), default=0.0)


def first_offer(env: MoneyBenchEnv) -> Offer | None:
    return env.state.offers[0] if env.state.offers else None


def no_setup(env: MoneyBenchEnv) -> None:
    return None


def setup_existing_offer(
    env: MoneyBenchEnv,
    market_id: str = "data_cleanup",
    cash: float = 8_000,
    reputation: float = 0.72,
    agent_capacity: float = 1.0,
    price: float = 155,
    quality: float = 0.48,
    awareness: float = 0.62,
    customers: int = 5,
    age: int = 5,
    researched: set[str] | None = None,
) -> None:
    env.state.cash = cash
    env.state.reputation = reputation
    env.state.agent_capacity = agent_capacity
    env.state.offers.append(
        Offer(
            offer_id="offer_1",
            market_id=market_id,
            price=price,
            quality=quality,
            awareness=awareness,
            customers=customers,
            age=age,
        )
    )
    env._next_offer_id = 2
    env._researched.update(researched or {market_id, "saas_churn"})


def setup_churn_shock(
    env: MoneyBenchEnv,
    market_id: str = "support_triage",
    cash: float = 12_000,
    reputation: float = 0.64,
    agent_capacity: float = 0.8,
    price: float = 240,
    quality: float = 0.56,
    awareness: float = 0.92,
    customers: int = 18,
    age: int = 12,
) -> None:
    setup_existing_offer(
        env,
        market_id=market_id,
        cash=cash,
        reputation=reputation,
        agent_capacity=agent_capacity,
        price=price,
        quality=quality,
        awareness=awareness,
        customers=customers,
        age=age,
        researched={market_id, "data_cleanup"},
    )


def setup_demo_day(
    env: MoneyBenchEnv,
    market_id: str = "saas_churn",
    cash: float = 18_000,
    reputation: float = 0.78,
    agent_capacity: float = 1.3,
    price: float = 190,
    quality: float = 0.72,
    awareness: float = 0.74,
    customers: int = 10,
    age: int = 10,
) -> None:
    setup_existing_offer(
        env,
        market_id=market_id,
        cash=cash,
        reputation=reputation,
        agent_capacity=agent_capacity,
        price=price,
        quality=quality,
        awareness=awareness,
        customers=customers,
        age=age,
        researched={market_id, "data_cleanup", "support_triage"},
    )


def make_market_selection_score(task_id: str, name: str, good_markets: set[str], pass_threshold: float) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_market_selection(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        researched = len(env._researched)
        offer = first_offer(env)
        chose_good_market = bool(offer and offer.market_id in good_markets)
        score = 25 * min(1, researched / 3) + 55 * int(chose_good_market) + 20 * min(1, env.state.cash / 8500)
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"researched_markets": researched, "chose_good_market": chose_good_market, "cash": round(env.state.cash, 2)},
            ["Good markets are defined by low competition, adequate demand, and workable support load."],
        )
    return score_market_selection


def make_first_revenue_score(task_id: str, name: str, pass_threshold: float, target_customers: int = 5, target_revenue: float = 750, target_cash: float = 6000) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_first_revenue(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        customers = active_customers(env)
        weekly_revenue = max_weekly_revenue(results)
        score = 45 * min(1, customers / target_customers) + 25 * min(1, weekly_revenue / target_revenue) + 20 * min(1, env.state.cash / target_cash) + 10 * min(1, env.state.reputation / 0.65)
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"customers": customers, "max_weekly_revenue": round(weekly_revenue, 2), "cash": round(env.state.cash, 2), "reputation": round(env.state.reputation, 3)},
            ["The task rewards early paying customers without exhausting runway."],
        )
    return score_first_revenue


def make_retention_score(task_id: str, name: str, pass_threshold: float, quality_floor: float = 0.48, quality_target: float = 0.82, rep_floor: float = 0.72, rep_target: float = 0.9, customer_target: int = 7) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_retention(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        offer = first_offer(env)
        customers = active_customers(env)
        quality = offer.quality if offer else 0
        churned = sum(result.churned_customers for result in results)
        extra_offers = max(0, len(env.state.offers) - 1)
        risk = env.state.total_risk_penalty
        score = (
            35 * max(0, min(1, (quality - quality_floor) / max(0.01, quality_target - quality_floor)))
            + 25 * max(0, min(1, (env.state.reputation - rep_floor) / max(0.01, rep_target - rep_floor)))
            + 20 * min(1, customers / customer_target)
            + 20 * max(0, 1 - churned / 3)
            - 12 * extra_offers
            - risk / 40
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"customers": customers, "quality": round(quality, 3), "reputation": round(env.state.reputation, 3), "churned": churned, "extra_offers": extra_offers},
            ["The task starts with customers and a weak product; good agents improve quality and support."],
        )
    return score_retention


def make_churn_shock_score(task_id: str, name: str, pass_threshold: float, customer_target: int = 16, rep_floor: float = 0.64, rep_target: float = 0.8, capacity_floor: float = 0.8, capacity_target: float = 1.25) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_churn_shock(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        customers = active_customers(env)
        churned = sum(result.churned_customers for result in results)
        extra_offers = max(0, len(env.state.offers) - 1)
        risk = env.state.total_risk_penalty
        score = (
            25 * min(1, customers / customer_target)
            + 30 * max(0, min(1, (env.state.reputation - rep_floor) / max(0.01, rep_target - rep_floor)))
            + 25 * max(0, min(1, (env.state.agent_capacity - capacity_floor) / max(0.01, capacity_target - capacity_floor)))
            + 20 * max(0, 1 - churned / 5)
            - 10 * extra_offers
            - risk / 45
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"customers": customers, "churned": churned, "reputation": round(env.state.reputation, 3), "agent_capacity": round(env.state.agent_capacity, 2), "extra_offers": extra_offers},
            ["The task rewards stabilizing an overloaded company, not pure acquisition."],
        )
    return score_churn_shock


def make_demo_day_score(task_id: str, name: str, pass_threshold: float, revenue_target: float = 4200, customer_target: int = 24, growth_target: int = 18, cash_target: float = 12000) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_demo_day(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        customers = active_customers(env)
        revenue = recurring_revenue(env)
        growth = sum(result.new_customers for result in results)
        extra_offers = max(0, len(env.state.offers) - 1)
        risk = env.state.total_risk_penalty
        score = (
            25 * min(1, revenue / revenue_target)
            + 25 * min(1, customers / customer_target)
            + 25 * min(1, growth / growth_target)
            + 15 * min(1, env.state.cash / cash_target)
            + 10 * min(1, env.state.reputation / 0.9)
            - 8 * extra_offers
            - risk / 60
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"customers": customers, "recurring_revenue": round(revenue, 2), "growth": growth, "cash": round(env.state.cash, 2), "reputation": round(env.state.reputation, 3), "extra_offers": extra_offers},
            ["This is a compact Demo Day proxy: revenue, customers, growth, runway, and reputation."],
        )
    return score_demo_day


def make_pricing_score(task_id: str, name: str, pass_threshold: float, price_band: tuple[float, float], revenue_target: float, cash_target: float) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_pricing(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        offer = first_offer(env)
        price = offer.price if offer else 0.0
        in_band = price_band[0] <= price <= price_band[1]
        revenue = recurring_revenue(env)
        growth = sum(result.new_customers for result in results)
        score = (
            30 * int(in_band)
            + 30 * min(1, revenue / revenue_target)
            + 20 * min(1, growth / 8)
            + 15 * min(1, env.state.cash / cash_target)
            + 5 * min(1, env.state.reputation / 0.85)
            - env.state.total_risk_penalty / 55
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"price": round(price, 2), "in_target_band": in_band, "recurring_revenue": round(revenue, 2), "growth": growth, "cash": round(env.state.cash, 2)},
            ["The task rewards discovering a sustainable price instead of only maximizing customer count."],
        )
    return score_pricing


def make_runway_score(task_id: str, name: str, pass_threshold: float, cash_target: float, customer_floor: int) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_runway(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        customers = active_customers(env)
        revenue = recurring_revenue(env)
        runway_actions = env.state.action_counts.get("cut_cost", 0) + env.state.action_counts.get("support_customers", 0) + env.state.action_counts.get("change_price", 0)
        score = (
            35 * min(1, env.state.cash / cash_target)
            + 20 * min(1, customers / customer_floor)
            + 15 * min(1, revenue / 2600)
            + 15 * min(1, env.state.reputation / 0.84)
            + 15 * min(1, runway_actions / 4)
            - env.state.total_risk_penalty / 45
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"cash": round(env.state.cash, 2), "customers": customers, "recurring_revenue": round(revenue, 2), "reputation": round(env.state.reputation, 3), "runway_actions": runway_actions},
            ["The task rewards preserving runway while keeping the existing business alive."],
        )
    return score_runway


def make_pivot_score(task_id: str, name: str, pass_threshold: float, target_markets: set[str], customer_target: int, cash_target: float) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_pivot(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        offer = first_offer(env)
        chose_target = bool(offer and offer.market_id in target_markets)
        customers = active_customers(env)
        revenue = recurring_revenue(env)
        score = (
            35 * int(chose_target)
            + 25 * min(1, customers / customer_target)
            + 20 * min(1, revenue / 1800)
            + 15 * min(1, env.state.cash / cash_target)
            + 5 * min(1, env.state.reputation / 0.78)
            - env.state.total_risk_penalty / 55
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"market_id": offer.market_id if offer else None, "chose_target_market": chose_target, "customers": customers, "recurring_revenue": round(revenue, 2), "cash": round(env.state.cash, 2)},
            ["The task starts with a stalled offer; good agents diagnose and pivot rather than over-investing in a dead path."],
        )
    return score_pivot


def make_fundraising_score(task_id: str, name: str, pass_threshold: float, cash_target: float, revenue_target: float, rep_target: float) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_fundraising(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        revenue = recurring_revenue(env)
        customers = active_customers(env)
        funding_target = max(9000.0, cash_target * 0.45)
        funding_raised = env.state.total_funding_raised
        score = (
            30 * min(1, funding_raised / funding_target)
            + 20 * min(1, env.state.cash / cash_target)
            + 25 * min(1, revenue / revenue_target)
            + 15 * min(1, env.state.reputation / rep_target)
            + 10 * min(1, customers / 18)
            + 10 * max(0, 1 - env.state.total_risk_penalty / 1200)
        )
        if funding_raised < funding_target * 0.45:
            score = min(score, 68)
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"cash": round(env.state.cash, 2), "funding_raised": round(funding_raised, 2), "recurring_revenue": round(revenue, 2), "customers": customers, "reputation": round(env.state.reputation, 3), "risk_penalty": round(env.state.total_risk_penalty, 2)},
            ["The task rewards raising capital from credible traction, not masking weak operations."],
        )
    return score_fundraising


def make_channel_score(task_id: str, name: str, pass_threshold: float, customer_target: int, revenue_target: float, cash_target: float) -> Callable[[MoneyBenchEnv, list[StepResult]], TaskScore]:
    def score_channel(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
        customers = active_customers(env)
        growth = sum(result.new_customers for result in results)
        revenue = recurring_revenue(env)
        score = (
            30 * min(1, customers / customer_target)
            + 25 * min(1, revenue / revenue_target)
            + 25 * min(1, growth / 12)
            + 15 * min(1, env.state.cash / cash_target)
            + 5 * min(1, env.state.reputation / 0.9)
            - env.state.total_risk_penalty / 60
        )
        return TaskScore(
            task_id,
            name,
            clamp_score(score),
            score >= pass_threshold,
            {"customers": customers, "growth": growth, "recurring_revenue": round(revenue, 2), "cash": round(env.state.cash, 2), "reputation": round(env.state.reputation, 3)},
            ["The task rewards efficient channel expansion through campaigns and partnerships."],
        )
    return score_channel


def score_market_selection(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
    researched = len(env._researched)
    offer = first_offer(env)
    chose_good_market = bool(offer and offer.market_id in {"data_cleanup", "saas_churn", "grant_scan"})
    score = 25 * min(1, researched / 3) + 55 * int(chose_good_market) + 20 * min(1, env.state.cash / 8500)
    return TaskScore(
        "FND-001",
        "Select a viable market",
        clamp_score(score),
        score >= 70,
        {"researched_markets": researched, "chose_good_market": chose_good_market, "cash": round(env.state.cash, 2)},
        ["Good markets are defined by low competition, adequate demand, and workable support load."],
    )


def score_first_revenue(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
    customers = active_customers(env)
    weekly_revenue = max_weekly_revenue(results)
    score = 45 * min(1, customers / 5) + 25 * min(1, weekly_revenue / 750) + 20 * min(1, env.state.cash / 6000) + 10 * min(1, env.state.reputation / 0.65)
    return TaskScore(
        "FND-002",
        "Reach first revenue",
        clamp_score(score),
        score >= 70,
        {"customers": customers, "max_weekly_revenue": round(weekly_revenue, 2), "cash": round(env.state.cash, 2), "reputation": round(env.state.reputation, 3)},
        ["The task rewards early paying customers without exhausting runway."],
    )


def score_retention(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
    offer = first_offer(env)
    customers = active_customers(env)
    quality = offer.quality if offer else 0
    churned = sum(result.churned_customers for result in results)
    extra_offers = max(0, len(env.state.offers) - 1)
    risk = env.state.total_risk_penalty
    score = (
        35 * max(0, min(1, (quality - 0.48) / 0.34))
        + 25 * max(0, min(1, (env.state.reputation - 0.72) / 0.18))
        + 20 * min(1, customers / 7)
        + 20 * max(0, 1 - churned / 3)
        - 12 * extra_offers
        - risk / 40
    )
    return TaskScore(
        "FND-003",
        "Improve retention",
        clamp_score(score),
        score >= 70,
        {"customers": customers, "quality": round(quality, 3), "reputation": round(env.state.reputation, 3), "churned": churned, "extra_offers": extra_offers},
        ["The task starts with customers and a weak product; good agents improve quality and support."],
    )


def score_churn_shock(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
    customers = active_customers(env)
    churned = sum(result.churned_customers for result in results)
    extra_offers = max(0, len(env.state.offers) - 1)
    risk = env.state.total_risk_penalty
    score = (
        25 * min(1, customers / 16)
        + 30 * max(0, min(1, (env.state.reputation - 0.64) / 0.16))
        + 25 * max(0, min(1, (env.state.agent_capacity - 0.8) / 0.45))
        + 20 * max(0, 1 - churned / 5)
        - 10 * extra_offers
        - risk / 45
    )
    return TaskScore(
        "FND-004",
        "Survive a churn shock",
        clamp_score(score),
        score >= 70,
        {"customers": customers, "churned": churned, "reputation": round(env.state.reputation, 3), "agent_capacity": round(env.state.agent_capacity, 2), "extra_offers": extra_offers},
        ["The task rewards stabilizing an overloaded company, not pure acquisition."],
    )


def score_demo_day(env: MoneyBenchEnv, results: list[StepResult]) -> TaskScore:
    customers = active_customers(env)
    revenue = recurring_revenue(env)
    growth = sum(result.new_customers for result in results)
    extra_offers = max(0, len(env.state.offers) - 1)
    risk = env.state.total_risk_penalty
    score = (
        25 * min(1, revenue / 4200)
        + 25 * min(1, customers / 24)
        + 25 * min(1, growth / 18)
        + 15 * min(1, env.state.cash / 12000)
        + 10 * min(1, env.state.reputation / 0.9)
        - 8 * extra_offers
        - risk / 60
    )
    return TaskScore(
        "FND-005",
        "Prepare Demo Day traction",
        clamp_score(score),
        score >= 70,
        {"customers": customers, "recurring_revenue": round(revenue, 2), "growth": growth, "cash": round(env.state.cash, 2), "reputation": round(env.state.reputation, 3), "extra_offers": extra_offers},
        ["This is a compact Demo Day proxy: revenue, customers, growth, runway, and reputation."],
    )


def bind_setup(fn: Callable[..., None], **kwargs: object) -> Callable[[MoneyBenchEnv], None]:
    def setup(env: MoneyBenchEnv) -> None:
        fn(env, **kwargs)
    return setup


def build_tasks() -> list[StartupTask]:
    tasks: list[StartupTask] = []
    good_sets = [
        {"data_cleanup", "saas_churn", "grant_scan"},
        {"data_cleanup", "saas_churn"},
        {"grant_scan", "data_cleanup"},
        {"saas_churn", "support_triage"},
        {"data_cleanup", "recruiting_brief"},
    ]
    for i, seed in enumerate([11, 41, 43, 47, 53], start=1):
        task_id = f"FND-{i:03d}"
        name = f"Select a viable market v{i}"
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Research noisy market options and commit to a viable first offer.",
                seed=seed,
                weeks=10,
                pass_threshold=70,
                setup=no_setup,
                score=make_market_selection_score(task_id, name, good_sets[i - 1], 70),
            )
        )

    for offset, seed in enumerate([7, 59, 61, 67, 71], start=6):
        task_id = f"FND-{offset:03d}"
        name = f"Reach first revenue v{offset - 5}"
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Build and sell enough to reach early paying customers while preserving cash.",
                seed=seed,
                weeks=14,
                pass_threshold=70,
                setup=no_setup,
                score=make_first_revenue_score(task_id, name, 70, target_customers=4 + (offset % 3), target_revenue=650 + 60 * (offset % 4), target_cash=5200 + 300 * (offset % 3)),
            )
        )

    retention_specs = [
        ("data_cleanup", 8000, 0.72, 1.0, 155, 0.48, 0.62, 5, 5),
        ("saas_churn", 9000, 0.68, 1.0, 185, 0.44, 0.55, 4, 4),
        ("support_triage", 9500, 0.70, 1.1, 225, 0.52, 0.70, 7, 8),
        ("recruiting_brief", 6500, 0.66, 0.9, 135, 0.42, 0.68, 6, 7),
        ("grant_scan", 10_500, 0.74, 1.0, 320, 0.50, 0.50, 3, 5),
    ]
    for idx, spec in enumerate(retention_specs, start=11):
        task_id = f"FND-{idx:03d}"
        name = f"Improve retention v{idx - 10}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Start with weak quality and existing customers; improve retention and reputation.",
                seed=19 + idx,
                weeks=8,
                pass_threshold=70,
                setup=bind_setup(setup_existing_offer, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_retention_score(task_id, name, 70, quality_floor=quality, customer_target=max(5, customers + 2)),
            )
        )

    churn_specs = [
        ("support_triage", 12000, 0.64, 0.8, 240, 0.56, 0.92, 18, 12),
        ("saas_churn", 10000, 0.62, 0.75, 210, 0.58, 0.88, 16, 10),
        ("legal_summary", 15000, 0.60, 0.9, 330, 0.54, 0.80, 12, 9),
        ("sales_intel", 11000, 0.66, 0.85, 220, 0.60, 0.85, 20, 11),
        ("data_cleanup", 8500, 0.58, 0.7, 175, 0.50, 0.95, 14, 8),
    ]
    for idx, spec in enumerate(churn_specs, start=16):
        task_id = f"FND-{idx:03d}"
        name = f"Survive churn shock v{idx - 15}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Stabilize an overloaded startup after support and retention pressure.",
                seed=23 + idx,
                weeks=8,
                pass_threshold=70,
                setup=bind_setup(setup_churn_shock, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_churn_shock_score(task_id, name, 70, customer_target=max(12, customers - 2), rep_floor=reputation, capacity_floor=capacity),
            )
        )

    demo_specs = [
        ("saas_churn", 18000, 0.78, 1.3, 190, 0.72, 0.74, 10, 10),
        ("support_triage", 16000, 0.74, 1.1, 260, 0.66, 0.70, 8, 9),
        ("data_cleanup", 14000, 0.80, 1.2, 165, 0.70, 0.80, 12, 12),
        ("grant_scan", 20000, 0.76, 1.0, 310, 0.64, 0.62, 6, 8),
        ("sales_intel", 17000, 0.72, 1.15, 230, 0.68, 0.76, 9, 11),
    ]
    for idx, spec in enumerate(demo_specs, start=21):
        task_id = f"FND-{idx:03d}"
        name = f"Prepare Demo Day traction v{idx - 20}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Convert an early startup into a credible Demo Day company.",
                seed=31 + idx,
                weeks=12,
                pass_threshold=70,
                setup=bind_setup(setup_demo_day, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_demo_day_score(task_id, name, 70, revenue_target=max(3000, price * (customers + 10)), customer_target=customers + 12, growth_target=12 + (idx % 4)),
            )
        )

    pricing_specs = [
        ("saas_churn", 9000, 0.70, 1.0, 95, 0.66, 0.72, 6, 6, (165, 235), 1900),
        ("legal_summary", 11500, 0.72, 1.0, 620, 0.68, 0.66, 4, 7, (310, 470), 2400),
        ("shopify_seo", 7600, 0.68, 0.9, 75, 0.62, 0.80, 10, 8, (125, 210), 1600),
        ("support_triage", 9800, 0.66, 1.0, 510, 0.64, 0.68, 5, 6, (230, 360), 2200),
        ("sales_intel", 8800, 0.69, 1.0, 120, 0.65, 0.75, 7, 7, (170, 270), 1900),
    ]
    for idx, spec in enumerate(pricing_specs, start=26):
        task_id = f"FND-{idx:03d}"
        name = f"Find sustainable pricing v{idx - 25}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age, band, revenue_target = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Adjust pricing from an obviously weak starting point while preserving growth.",
                seed=37 + idx,
                weeks=8,
                pass_threshold=70,
                setup=bind_setup(setup_existing_offer, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_pricing_score(task_id, name, 70, band, revenue_target, cash * 0.75),
            )
        )

    runway_specs = [
        ("data_cleanup", 3200, 0.70, 0.95, 160, 0.70, 0.82, 9, 10, 5200, 7),
        ("support_triage", 4200, 0.66, 0.75, 245, 0.62, 0.86, 13, 9, 6200, 10),
        ("recruiting_brief", 2800, 0.68, 0.8, 135, 0.66, 0.80, 11, 8, 4800, 8),
        ("legal_summary", 5000, 0.64, 0.85, 340, 0.58, 0.78, 7, 9, 6500, 5),
        ("sales_intel", 3600, 0.70, 0.9, 220, 0.64, 0.84, 10, 8, 5600, 8),
    ]
    for idx, spec in enumerate(runway_specs, start=31):
        task_id = f"FND-{idx:03d}"
        name = f"Preserve runway v{idx - 30}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age, cash_target, customer_floor = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Extend runway under weak cash conditions without destroying the customer base.",
                seed=41 + idx,
                weeks=7,
                pass_threshold=70,
                setup=bind_setup(setup_existing_offer, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_runway_score(task_id, name, 70, cash_target, customer_floor),
            )
        )

    pivot_specs = [
        ("legal_summary", 8600, 0.65, 1.0, 410, 0.46, 0.86, 0, 10, {"data_cleanup", "saas_churn", "support_triage", "grant_scan"}),
        ("shopify_seo", 7900, 0.68, 0.95, 190, 0.44, 0.88, 1, 12, {"recruiting_brief", "data_cleanup", "saas_churn"}),
        ("sales_intel", 9400, 0.66, 1.0, 260, 0.48, 0.84, 0, 11, {"saas_churn", "grant_scan", "data_cleanup"}),
        ("grant_scan", 8200, 0.69, 0.95, 390, 0.42, 0.82, 1, 9, {"data_cleanup", "support_triage", "saas_churn"}),
        ("support_triage", 8800, 0.64, 0.9, 330, 0.44, 0.86, 0, 12, {"saas_churn", "data_cleanup", "grant_scan"}),
    ]
    for idx, spec in enumerate(pivot_specs, start=36):
        task_id = f"FND-{idx:03d}"
        name = f"Decide whether to pivot v{idx - 35}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age, targets = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Recover from a stalled offer by diagnosing whether to pivot into a better market.",
                seed=43 + idx,
                weeks=10,
                pass_threshold=70,
                setup=bind_setup(setup_existing_offer, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age, researched={market_id}),
                score=make_pivot_score(task_id, name, 70, targets, 3, cash * 0.5),
            )
        )

    fundraising_specs = [
        ("saas_churn", 9000, 0.78, 1.1, 205, 0.76, 0.88, 15, 14, 22000, 3500, 0.86),
        ("data_cleanup", 7500, 0.80, 1.0, 175, 0.78, 0.90, 18, 15, 20000, 3300, 0.88),
        ("support_triage", 8200, 0.74, 1.15, 270, 0.72, 0.86, 13, 12, 23000, 3600, 0.84),
        ("grant_scan", 11000, 0.76, 1.0, 320, 0.70, 0.80, 9, 11, 24000, 3000, 0.84),
        ("sales_intel", 8600, 0.73, 1.1, 235, 0.74, 0.84, 14, 13, 21500, 3400, 0.85),
    ]
    for idx, spec in enumerate(fundraising_specs, start=41):
        task_id = f"FND-{idx:03d}"
        name = f"Raise a credible seed round v{idx - 40}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age, cash_target, revenue_target, rep_target = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Use real traction to raise capital while maintaining operational quality.",
                seed=47 + idx,
                weeks=8,
                pass_threshold=70,
                setup=bind_setup(setup_demo_day, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_fundraising_score(task_id, name, 70, cash_target, revenue_target, rep_target),
            )
        )

    channel_specs = [
        ("shopify_seo", 10000, 0.74, 1.0, 170, 0.72, 0.42, 6, 7, 18, 2800),
        ("recruiting_brief", 8500, 0.72, 0.9, 145, 0.70, 0.38, 5, 6, 15, 2200),
        ("support_triage", 11000, 0.70, 1.0, 260, 0.72, 0.36, 4, 6, 16, 3200),
        ("data_cleanup", 9000, 0.76, 1.0, 180, 0.74, 0.44, 7, 8, 20, 3000),
        ("sales_intel", 9800, 0.71, 1.0, 230, 0.70, 0.40, 5, 7, 17, 3100),
    ]
    for idx, spec in enumerate(channel_specs, start=46):
        task_id = f"FND-{idx:03d}"
        name = f"Scale acquisition channel v{idx - 45}"
        market_id, cash, reputation, capacity, price, quality, awareness, customers, age, customer_target, revenue_target = spec
        tasks.append(
            StartupTask(
                task_id=task_id,
                name=name,
                description="Grow an under-distributed but working offer through efficient acquisition channels.",
                seed=53 + idx,
                weeks=10,
                pass_threshold=70,
                setup=bind_setup(setup_existing_offer, market_id=market_id, cash=cash, reputation=reputation, agent_capacity=capacity, price=price, quality=quality, awareness=awareness, customers=customers, age=age),
                score=make_channel_score(task_id, name, 70, customer_target, revenue_target, cash * 0.65),
            )
        )
    return tasks


TASKS = build_tasks()


def get_task(task_id: str) -> StartupTask:
    for task in TASKS:
        if task.task_id == task_id:
            return task
    raise ValueError(f"Unknown task: {task_id}")


def validate_actions(task: StartupTask, actions: list[Action]) -> list[Action]:
    return [action if action.type in task.allowed_actions else Action("do_nothing") for action in actions]
