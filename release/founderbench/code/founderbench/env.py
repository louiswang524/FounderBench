from __future__ import annotations

import math
import random
from dataclasses import asdict

from .schema import Action, CompanyState, Market, Observation, Offer, StepResult


DEFAULT_MARKETS = [
    Market("saas_churn", "Indie SaaS", "weekly churn-risk reports", 0.76, 0.38, 260, 0.45, 0.34, 0.11),
    Market("legal_summary", "Small Law Firms", "document summary packs", 0.82, 0.78, 420, 0.58, 0.52, 0.08),
    Market("shopify_seo", "Shopify Stores", "SEO product page refresh", 0.68, 0.61, 180, 0.32, 0.28, 0.17),
    Market("recruiting_brief", "Recruiters", "candidate briefing notes", 0.62, 0.44, 145, 0.25, 0.31, 0.13),
    Market("data_cleanup", "Ops Teams", "spreadsheet cleanup automation", 0.58, 0.32, 210, 0.40, 0.22, 0.10),
    Market("support_triage", "B2B Support", "ticket triage workflow", 0.72, 0.52, 330, 0.55, 0.47, 0.12),
    Market("grant_scan", "Research Labs", "grant opportunity scans", 0.47, 0.25, 390, 0.36, 0.29, 0.18),
    Market("sales_intel", "Sales Teams", "account intelligence briefs", 0.74, 0.66, 240, 0.42, 0.38, 0.15),
]


class FounderBenchEnv:
    def __init__(self, seed: int = 0, weeks: int = 52, markets: list[Market] | None = None):
        self.seed = seed
        self.rng = random.Random(seed)
        self.weeks = weeks
        self.markets = markets or DEFAULT_MARKETS
        self.state = CompanyState()
        self._market_momentum = {m.market_id: self.rng.uniform(-0.04, 0.04) for m in self.markets}
        self._researched: set[str] = set()
        self._next_offer_id = 1

    def reset(self) -> Observation:
        self.rng = random.Random(self.seed)
        self.state = CompanyState()
        self._market_momentum = {m.market_id: self.rng.uniform(-0.04, 0.04) for m in self.markets}
        self._researched = set()
        self._next_offer_id = 1
        return self.observe()

    def observe(self) -> Observation:
        market_rows = []
        for market in self.markets:
            demand = self._current_demand(market)
            row = {
                "market_id": market.market_id,
                "name": market.name,
                "need": market.need,
                "demand_signal": round(demand if market.market_id in self._researched else self._noisy(demand, 0.12), 3),
                "competition_signal": round(market.competition if market.market_id in self._researched else self._noisy(market.competition, 0.10), 3),
                "willingness_to_pay_signal": round(market.willingness_to_pay if market.market_id in self._researched else self._noisy(market.willingness_to_pay, 28), 2),
                "researched": market.market_id in self._researched,
            }
            market_rows.append(row)

        return Observation(
            week=self.state.week,
            cash=round(self.state.cash, 2),
            reputation=round(self.state.reputation, 3),
            agent_capacity=round(self.state.agent_capacity, 2),
            markets=market_rows,
            offers=[asdict(offer) for offer in self.state.offers],
            memory=self.state.memory[-8:],
        )

    def step(self, actions: list[Action]) -> StepResult:
        if self.state.bankrupt:
            return StepResult(0, 0, 0, 0, 0, 0, ["Company is bankrupt."])

        notes: list[str] = []
        revenue = 0.0
        cost = 0.0
        risk = 0.0
        new_customers = 0
        churned_customers = 0

        if len(actions) > 5:
            risk += (len(actions) - 5) * 120
            notes.append("Too many actions created coordination risk.")
            actions = actions[:5]

        for action in actions:
            action_cost, action_risk, action_notes = self._apply_action(action)
            cost += action_cost
            risk += action_risk
            notes.extend(action_notes)

        weekly_revenue, weekly_cost, acquired, churned, ops_notes = self._settle_week()
        revenue += weekly_revenue
        cost += weekly_cost
        new_customers += acquired
        churned_customers += churned
        notes.extend(ops_notes)

        profit = revenue - cost
        self.state.cash += profit
        self.state.cumulative_revenue += revenue
        self.state.cumulative_cost += cost
        self.state.total_risk_penalty += risk
        self.state.reputation = max(0.0, min(1.0, self.state.reputation - risk / 5000))
        self._advance_markets()

        if self.state.cash < 0:
            self.state.bankrupt = True
            risk += 2000
            notes.append("Company went bankrupt.")

        self.state.memory.extend(notes[-6:])
        self.state.memory = self.state.memory[-40:]
        self.state.week += 1

        return StepResult(
            revenue=round(revenue, 2),
            cost=round(cost, 2),
            profit=round(profit, 2),
            new_customers=new_customers,
            churned_customers=churned_customers,
            risk_penalty=round(risk, 2),
            notes=notes,
        )

    def done(self) -> bool:
        return self.state.week > self.weeks or self.state.bankrupt

    def score(self) -> float:
        recurring_revenue = sum(offer.customers * offer.price for offer in self.state.offers)
        active_customers = sum(offer.customers for offer in self.state.offers)
        score = (
            self.state.cash
            + 8 * recurring_revenue
            + 500 * self.state.reputation
            + 120 * active_customers
            - 2 * self.state.total_risk_penalty
            - 1.5 * self.state.cumulative_api_cost
        )
        if self.state.bankrupt:
            score -= 5000
        return round(score, 2)

    def summary(self) -> dict[str, float | int | bool]:
        return {
            "seed": self.seed,
            "weeks": self.state.week - 1,
            "cash": round(self.state.cash, 2),
            "score": self.score(),
            "reputation": round(self.state.reputation, 3),
            "offers": len(self.state.offers),
            "customers": sum(offer.customers for offer in self.state.offers),
            "cumulative_revenue": round(self.state.cumulative_revenue, 2),
            "cumulative_cost": round(self.state.cumulative_cost, 2),
            "cumulative_api_cost": round(self.state.cumulative_api_cost, 2),
            "funding_raised": round(self.state.total_funding_raised, 2),
            "risk_penalty": round(self.state.total_risk_penalty, 2),
            "bankrupt": self.state.bankrupt,
        }

    def _apply_action(self, action: Action) -> tuple[float, float, list[str]]:
        notes: list[str] = []
        risk = 0.0
        cost = max(0.0, action.budget)
        self.state.cumulative_api_cost += 0.35
        self.state.action_counts[action.type] = self.state.action_counts.get(action.type, 0) + 1

        if action.type == "do_nothing":
            return 0.0, 0.0, ["Held position."]

        if cost > self.state.cash * 0.65:
            risk += 450
            notes.append("Action risk increased because budget exceeded 65% of cash.")

        market = self._find_market(action.market_id)
        offer = self._find_offer(action.offer_id)

        if action.type == "research_market":
            if not market:
                return cost, 220, ["Research targeted an unknown market."]
            self._researched.add(market.market_id)
            notes.append(f"Researched {market.name}.")
            return max(80, cost or 120), risk, notes

        if action.type == "build_offer":
            if not market:
                return cost, 260, ["Build targeted an unknown market."]
            minimum = 700 + market.build_complexity * 1300
            if cost < minimum:
                risk += 180
                quality = max(0.15, cost / minimum * 0.45)
                notes.append(f"Underfunded offer for {market.name}.")
            else:
                quality = min(0.92, 0.38 + (cost / (minimum * 2.2)) + self.state.agent_capacity * 0.08)
                notes.append(f"Built offer for {market.name}.")
            price = action.price or market.willingness_to_pay * 0.82
            self.state.offers.append(Offer(f"offer_{self._next_offer_id}", market.market_id, price, quality))
            self._next_offer_id += 1
            return cost, risk, notes

        if action.type == "run_campaign":
            if not offer:
                return cost, 260, ["Campaign targeted an unknown offer."]
            if action.message_quality < 0.35:
                risk += 360
                self.state.reputation = max(0, self.state.reputation - 0.04)
                notes.append("Low-quality outreach damaged reputation.")
            if cost > 1600:
                risk += (cost - 1600) * 0.12
                notes.append("Aggressive outreach created spam risk.")
            offer.awareness = min(1.0, offer.awareness + math.sqrt(max(cost, 0) / 2200) * (0.45 + action.message_quality * 0.35))
            notes.append(f"Ran campaign for {offer.offer_id}.")
            return cost, risk, notes

        if action.type == "improve_offer":
            if not offer:
                return cost, 240, ["Improvement targeted an unknown offer."]
            gain = math.sqrt(max(cost, 0) / 1800) * 0.18 * self.state.agent_capacity
            offer.quality = min(0.98, offer.quality + gain)
            notes.append(f"Improved {offer.offer_id}.")
            return cost, risk, notes

        if action.type == "hire_agent":
            hire_cost = max(900, cost or 1200)
            self.state.agent_capacity += 0.18 + min(0.25, hire_cost / 8000)
            notes.append("Hired an additional agent worker.")
            return hire_cost, risk, notes

        if action.type == "support_customers":
            support_gain = math.sqrt(max(cost, 0) / 1000) * 0.04
            self.state.reputation = min(1.0, self.state.reputation + support_gain)
            notes.append("Invested in customer support.")
            return cost, risk, notes

        if action.type == "change_price":
            if not offer:
                return cost, 220, ["Price change targeted an unknown offer."]
            market = self._find_market(offer.market_id)
            old_price = offer.price
            if action.price is None or action.price <= 0:
                return cost, 220, ["Price change omitted a valid price."]
            offer.price = float(action.price)
            if market and offer.price > market.willingness_to_pay * 1.35:
                risk += 160
                self.state.reputation = max(0.0, self.state.reputation - 0.015)
                notes.append("Price increased above market tolerance.")
            elif market and offer.price < market.willingness_to_pay * 0.45:
                risk += 80
                notes.append("Price cut may anchor the offer as low-value.")
            notes.append(f"Changed {offer.offer_id} price from {old_price:.2f} to {offer.price:.2f}.")
            return max(40, cost), risk, notes

        if action.type == "interview_customers":
            if market:
                self._researched.add(market.market_id)
            target_offer = offer or (self.state.offers[0] if self.state.offers else None)
            insight = math.sqrt(max(cost, 80) / 900)
            self.state.reputation = min(1.0, self.state.reputation + 0.012 * insight)
            if target_offer:
                target_offer.quality = min(0.98, target_offer.quality + 0.035 * insight)
                target_offer.awareness = min(1.0, target_offer.awareness + 0.025 * insight)
                notes.append(f"Interviewed customers and learned how to improve {target_offer.offer_id}.")
            elif market:
                notes.append(f"Interviewed buyers in {market.name}.")
            else:
                risk += 120
                notes.append("Customer interviews lacked a valid market or offer target.")
            return max(100, cost), risk, notes

        if action.type == "cut_cost":
            customer_count = sum(o.customers for o in self.state.offers)
            savings = min(900.0, 180.0 + customer_count * 18.0 + max(cost, 0) * 0.25)
            self.state.agent_capacity = max(0.45, self.state.agent_capacity - 0.06)
            if customer_count > self.state.agent_capacity * 28:
                risk += 180
                self.state.reputation = max(0.0, self.state.reputation - 0.025)
                notes.append("Cost cuts strained customer operations.")
            notes.append("Reduced operating costs.")
            return -savings, risk, notes

        if action.type == "pivot_market":
            if not offer or not market:
                return cost, 280, ["Pivot needs both a valid offer and target market."]
            old_market = offer.market_id
            lost_customers = offer.customers // 2
            offer.customers -= lost_customers
            offer.market_id = market.market_id
            offer.quality = max(0.28, offer.quality * 0.72)
            offer.awareness = min(0.35, offer.awareness * 0.45)
            self._researched.add(market.market_id)
            risk += 140 + lost_customers * 20
            notes.append(f"Pivoted {offer.offer_id} from {old_market} to {market.name}.")
            return max(650, cost), risk, notes

        if action.type == "raise_funding":
            traction = sum(o.customers * o.price for o in self.state.offers)
            investor_confidence = self.state.reputation * 0.45 + min(0.35, traction / 9000) + min(0.2, self.state.cash / 20000)
            ask = max(cost, action.price or 5000)
            raised = ask * min(1.0, max(0.05, investor_confidence))
            self.state.cash += raised
            self.state.total_funding_raised += raised
            risk += max(0.0, ask - raised) * 0.03
            notes.append(f"Raised {raised:.2f} in funding against an ask of {ask:.2f}.")
            return 250, risk, notes

        if action.type == "partner_channel":
            if not offer:
                return cost, 240, ["Partnership targeted an unknown offer."]
            channel_gain = math.sqrt(max(cost, 0) / 1600) * (0.28 + action.message_quality * 0.22)
            offer.awareness = min(1.0, offer.awareness + channel_gain)
            self.state.reputation = min(1.0, self.state.reputation + 0.01 * action.message_quality)
            if cost < 500:
                risk += 80
                notes.append("Partnership was under-resourced.")
            notes.append(f"Opened a partner channel for {offer.offer_id}.")
            return cost, risk, notes

        return cost, 300, ["Unknown action type."]

    def _settle_week(self) -> tuple[float, float, int, int, list[str]]:
        notes = []
        revenue = 0.0
        cost = 0.0
        acquired = 0
        churned = 0

        for offer in self.state.offers:
            market = self._find_market(offer.market_id)
            if not market:
                continue
            demand = self._current_demand(market)
            price_fit = max(0.08, 1.25 - offer.price / max(1, market.willingness_to_pay))
            conversion = demand * offer.awareness * offer.quality * price_fit * self.state.reputation
            conversion -= market.competition * 0.18
            expected_new = max(0, conversion * 5.5)
            new = self._poisson(expected_new)
            churn_rate = max(0.01, market.support_load * 0.08 + (0.65 - offer.quality) * 0.05 - self.state.reputation * 0.025)
            churn = min(offer.customers, self._poisson(offer.customers * churn_rate))
            offer.customers += new - churn
            offer.age += 1
            revenue += offer.customers * offer.price
            cost += offer.customers * market.support_load * 18
            acquired += new
            churned += churn
            if new:
                notes.append(f"{offer.offer_id} acquired {new} customers.")
            if churn:
                notes.append(f"{offer.offer_id} churned {churn} customers.")

        support_required = sum((self._find_market(o.market_id).support_load if self._find_market(o.market_id) else 0) * o.customers for o in self.state.offers)
        if support_required > self.state.agent_capacity * 30:
            overload = support_required - self.state.agent_capacity * 30
            self.state.reputation = max(0, self.state.reputation - overload / 800)
            notes.append("Support overload reduced reputation.")

        return revenue, cost, acquired, churned, notes

    def _advance_markets(self) -> None:
        for market in self.markets:
            old = self._market_momentum[market.market_id]
            shock = self.rng.uniform(-market.volatility, market.volatility) * 0.18
            self._market_momentum[market.market_id] = max(-0.2, min(0.2, old * 0.82 + shock))

    def _current_demand(self, market: Market) -> float:
        return max(0.05, min(1.2, market.base_demand + self._market_momentum[market.market_id]))

    def _noisy(self, value: float, scale: float) -> float:
        return max(0.0, value + self.rng.uniform(-scale, scale))

    def _find_market(self, market_id: str | None) -> Market | None:
        return next((market for market in self.markets if market.market_id == market_id), None)

    def _find_offer(self, offer_id: str | None) -> Offer | None:
        return next((offer for offer in self.state.offers if offer.offer_id == offer_id), None)

    def _poisson(self, lam: float) -> int:
        if lam <= 0:
            return 0
        if lam > 30:
            return max(0, round(self.rng.gauss(lam, math.sqrt(lam))))
        limit = math.exp(-lam)
        k = 0
        product = 1.0
        while product > limit:
            k += 1
            product *= self.rng.random()
        return k - 1
