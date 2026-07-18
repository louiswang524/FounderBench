from __future__ import annotations

import random
from abc import ABC, abstractmethod

from .schema import Action, Observation


class Policy(ABC):
    @abstractmethod
    def act(self, observation: Observation) -> list[Action]:
        raise NotImplementedError


class RandomPolicy(Policy):
    def __init__(self, seed: int = 0):
        self.rng = random.Random(seed)

    def act(self, observation: Observation) -> list[Action]:
        actions: list[Action] = []
        markets = observation.markets
        offers = observation.offers
        choice = self.rng.choice(["research", "build", "campaign", "improve", "support", "hire", "price", "interview", "cut", "pivot", "fund", "partner", "nothing"])
        if choice == "research":
            market = self.rng.choice(markets)
            actions.append(Action("research_market", market_id=market["market_id"], budget=self.rng.randint(80, 240)))
        elif choice == "build":
            market = self.rng.choice(markets)
            actions.append(Action("build_offer", market_id=market["market_id"], budget=self.rng.randint(400, 2200), price=self.rng.randint(99, 499)))
        elif choice == "campaign" and offers:
            offer = self.rng.choice(offers)
            actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=self.rng.randint(150, 2200), message_quality=self.rng.random()))
        elif choice == "improve" and offers:
            offer = self.rng.choice(offers)
            actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=self.rng.randint(200, 1500)))
        elif choice == "support":
            actions.append(Action("support_customers", budget=self.rng.randint(80, 600)))
        elif choice == "hire":
            actions.append(Action("hire_agent", budget=self.rng.randint(900, 1800)))
        elif choice == "price" and offers:
            offer = self.rng.choice(offers)
            actions.append(Action("change_price", offer_id=offer["offer_id"], price=self.rng.randint(90, 520)))
        elif choice == "interview":
            market = self.rng.choice(markets)
            offer_id = self.rng.choice(offers)["offer_id"] if offers else None
            actions.append(Action("interview_customers", market_id=market["market_id"], offer_id=offer_id, budget=self.rng.randint(100, 700)))
        elif choice == "cut":
            actions.append(Action("cut_cost", budget=self.rng.randint(0, 400)))
        elif choice == "pivot" and offers:
            market = self.rng.choice(markets)
            offer = self.rng.choice(offers)
            actions.append(Action("pivot_market", market_id=market["market_id"], offer_id=offer["offer_id"], budget=self.rng.randint(500, 1800)))
        elif choice == "fund":
            actions.append(Action("raise_funding", budget=self.rng.randint(3000, 18000)))
        elif choice == "partner" and offers:
            offer = self.rng.choice(offers)
            actions.append(Action("partner_channel", offer_id=offer["offer_id"], budget=self.rng.randint(400, 1800), message_quality=self.rng.random()))
        else:
            actions.append(Action("do_nothing"))
        return actions


class ConservativePolicy(Policy):
    def act(self, observation: Observation) -> list[Action]:
        if observation.cash < 2500:
            return [Action("support_customers", budget=120)] if observation.offers else [Action("do_nothing")]

        unresearched = [m for m in observation.markets if not m["researched"]]
        if unresearched and observation.week <= 8:
            best = max(unresearched, key=lambda m: m["demand_signal"] - m["competition_signal"])
            return [Action("research_market", market_id=best["market_id"], budget=140)]

        if not observation.offers:
            best = max(observation.markets, key=lambda m: m["demand_signal"] * m["willingness_to_pay_signal"] * (1 - m["competition_signal"]))
            return [Action("build_offer", market_id=best["market_id"], budget=1450, price=best["willingness_to_pay_signal"] * 0.78)]

        strongest = max(observation.offers, key=lambda o: o["quality"] * (o["customers"] + 2))
        matching_market = next((m for m in observation.markets if m["market_id"] == strongest["market_id"]), None)
        if matching_market and (strongest["price"] < matching_market["willingness_to_pay_signal"] * 0.55 or strongest["price"] > matching_market["willingness_to_pay_signal"] * 1.25):
            return [Action("change_price", offer_id=strongest["offer_id"], price=matching_market["willingness_to_pay_signal"] * 0.78)]
        if strongest["quality"] < 0.68:
            return [Action("improve_offer", offer_id=strongest["offer_id"], budget=500)]
        if strongest["awareness"] < 0.72:
            return [Action("run_campaign", offer_id=strongest["offer_id"], budget=550, message_quality=0.78)]
        return [Action("support_customers", budget=260)]


class HeuristicPolicy(Policy):
    def act(self, observation: Observation) -> list[Action]:
        actions: list[Action] = []
        cash = observation.cash

        def market_score(m: dict) -> float:
            demand = m["demand_signal"]
            competition = m["competition_signal"]
            price = m["willingness_to_pay_signal"]
            friction_discount = max(0.05, 1 - competition) ** 1.45
            return demand * price * friction_discount + demand * 180 - competition * 150 + (45 if m["researched"] else 0)

        # Gather clean signals before making expensive commitments. This makes the
        # heuristic a stronger benchmark policy than the intentionally cautious
        # baseline while preserving the same information constraints.
        unresearched = [m for m in observation.markets if not m["researched"]]
        if unresearched and observation.week <= 8:
            best_unresearched = max(unresearched, key=market_score)
            return [Action("research_market", market_id=best_unresearched["market_id"], budget=160)]

        best_market = max(observation.markets, key=market_score)
        if not best_market["researched"]:
            actions.append(Action("research_market", market_id=best_market["market_id"], budget=160))

        matching_offers = [o for o in observation.offers if o["market_id"] == best_market["market_id"]]
        profitable_offers = [o for o in observation.offers if o["customers"] >= 8]
        stalled_offers = [o for o in observation.offers if o["age"] >= 8 and o["customers"] == 0 and o["awareness"] > 0.85]
        can_expand = not observation.offers or (profitable_offers and stalled_offers and len(observation.offers) < 2)
        if can_expand and not matching_offers and cash > 2600:
            budget = min(2600, max(1850, cash * 0.22))
            price = best_market["willingness_to_pay_signal"] * 0.74
            actions.append(Action("build_offer", market_id=best_market["market_id"], budget=budget, price=price))
            return actions[:2]

        if observation.offers:
            active = [o for o in observation.offers if not (o["age"] >= 8 and o["customers"] == 0 and o["awareness"] > 0.85)]
            offer_pool = active or observation.offers
            offer = max(offer_pool, key=lambda o: o["customers"] * o["price"] + o["quality"] * 900 + o["awareness"] * 250)
            offer_market = next((m for m in observation.markets if m["market_id"] == offer["market_id"]), None)
            if offer_market and (offer["price"] < offer_market["willingness_to_pay_signal"] * 0.58 or offer["price"] > offer_market["willingness_to_pay_signal"] * 1.2):
                actions.append(Action("change_price", offer_id=offer["offer_id"], price=offer_market["willingness_to_pay_signal"] * 0.76))
            if offer["quality"] < 0.86 and cash > 1800:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=min(1100, cash * 0.09)))
            if offer["awareness"] < 0.96 and cash > 1400:
                actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=min(950, cash * 0.075), message_quality=0.9))
            customer_count = sum(o["customers"] for o in observation.offers)
            if customer_count > observation.agent_capacity * 24 and cash > 3500:
                actions.append(Action("hire_agent", budget=1200))
            if (customer_count > 3 or observation.reputation < 0.9) and cash > 1200:
                actions.append(Action("support_customers", budget=min(520, cash * 0.045)))

        if not actions:
            if observation.offers and cash > 1000:
                actions.append(Action("support_customers", budget=300))
            else:
                actions.append(Action("do_nothing"))
        return actions[:4]


class TaskHeuristicPolicy(HeuristicPolicy):
    def act_task(self, task_id: str, observation: Observation) -> list[Action]:
        task_num = int(task_id.split("-")[1])
        family = (task_num - 1) // 5

        if family == 0:
            unresearched = [m for m in observation.markets if not m["researched"]]
            if unresearched and observation.week <= 3:
                best = max(unresearched, key=lambda m: m["demand_signal"] * (1 - m["competition_signal"]))
                return [Action("research_market", market_id=best["market_id"], budget=150)]
            if not observation.offers:
                best = max(observation.markets, key=lambda m: m["demand_signal"] * m["willingness_to_pay_signal"] * max(0.1, 1 - m["competition_signal"]))
                return [Action("build_offer", market_id=best["market_id"], budget=1900, price=best["willingness_to_pay_signal"] * 0.74)]

        if family == 1:
            if observation.week <= 4 and not all(m["researched"] for m in observation.markets[:3]):
                best = max([m for m in observation.markets if not m["researched"]], key=lambda m: m["demand_signal"] * max(0.1, 1 - m["competition_signal"]))
                return [Action("research_market", market_id=best["market_id"], budget=140)]
            if not observation.offers:
                best = max(observation.markets, key=lambda m: m["demand_signal"] * m["willingness_to_pay_signal"] * max(0.1, 1 - m["competition_signal"]))
                return [Action("build_offer", market_id=best["market_id"], budget=2200, price=best["willingness_to_pay_signal"] * 0.68)]

        if family == 2 and observation.offers:
            offer = observation.offers[0]
            actions: list[Action] = []
            if offer["quality"] < 0.82:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=800))
            if observation.reputation < 0.86:
                actions.append(Action("support_customers", budget=500))
            return actions or [Action("support_customers", budget=320)]

        if family == 3 and observation.offers:
            actions = []
            if observation.agent_capacity < 1.15 and observation.cash > 2500:
                actions.append(Action("hire_agent", budget=1400))
            if observation.reputation < 0.82:
                actions.append(Action("support_customers", budget=650))
            offer = observation.offers[0]
            if offer["quality"] < 0.72 and observation.cash > 2500:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=650))
            return actions[:3] or [Action("support_customers", budget=450)]

        if family == 4 and observation.offers:
            offer = observation.offers[0]
            actions = []
            if offer["quality"] < 0.86:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=900))
            if offer["awareness"] < 0.98:
                actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=900, message_quality=0.92))
            customers = sum(o["customers"] for o in observation.offers)
            if customers > observation.agent_capacity * 20 and observation.cash > 3000:
                actions.append(Action("hire_agent", budget=1300))
            if observation.reputation < 0.92 or customers > 12:
                actions.append(Action("support_customers", budget=550))
            return actions[:4] or [Action("support_customers", budget=350)]

        if family == 5 and observation.offers:
            offer = observation.offers[0]
            market = next((m for m in observation.markets if m["market_id"] == offer["market_id"]), None)
            actions = []
            if market:
                actions.append(Action("interview_customers", market_id=market["market_id"], offer_id=offer["offer_id"], budget=300))
                actions.append(Action("change_price", offer_id=offer["offer_id"], price=market["willingness_to_pay_signal"] * 0.78))
            if offer["awareness"] < 0.9:
                actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=650, message_quality=0.88))
            return actions[:3] or [Action("do_nothing")]

        if family == 6 and observation.offers:
            offer = observation.offers[0]
            actions = []
            if observation.cash < 5200:
                actions.append(Action("cut_cost", budget=100))
            if observation.reputation < 0.78:
                actions.append(Action("support_customers", budget=260))
            if offer["quality"] < 0.72 and observation.cash > 2400:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=360))
            return actions[:3] or [Action("cut_cost", budget=100)]

        if family == 7 and observation.offers:
            offer = observation.offers[0]
            target = max(observation.markets, key=lambda m: m["demand_signal"] * m["willingness_to_pay_signal"] * max(0.1, 1 - m["competition_signal"]))
            actions = []
            if not target["researched"]:
                actions.append(Action("research_market", market_id=target["market_id"], budget=160))
            if offer["customers"] <= 1 and offer["age"] >= 8 and observation.week <= 2 and offer["market_id"] != target["market_id"]:
                actions.append(Action("pivot_market", offer_id=offer["offer_id"], market_id=target["market_id"], budget=900))
                actions.append(Action("change_price", offer_id=offer["offer_id"], price=target["willingness_to_pay_signal"] * 0.76))
                return actions[:3]
            current_market = next((m for m in observation.markets if m["market_id"] == offer["market_id"]), target)
            if current_market and (offer["price"] < current_market["willingness_to_pay_signal"] * 0.58 or offer["price"] > current_market["willingness_to_pay_signal"] * 1.2):
                actions.append(Action("change_price", offer_id=offer["offer_id"], price=current_market["willingness_to_pay_signal"] * 0.76))
            if offer["quality"] < 0.66:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=650))
            if offer["awareness"] < 0.75:
                actions.append(Action("partner_channel", offer_id=offer["offer_id"], budget=700, message_quality=0.88))
            elif offer["awareness"] < 0.95:
                actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=650, message_quality=0.88))
            return actions[:4] or [Action("interview_customers", offer_id=offer["offer_id"], budget=240)]

        if family == 8 and observation.offers:
            offer = observation.offers[0]
            actions = []
            if observation.reputation < 0.84:
                actions.append(Action("support_customers", budget=420))
            if offer["quality"] < 0.82:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=650))
            if observation.cash < 18000:
                actions.append(Action("raise_funding", budget=14000))
            return actions[:3] or [Action("raise_funding", budget=12000)]

        if family == 9 and observation.offers:
            offer = observation.offers[0]
            actions = []
            if offer["awareness"] < 0.9:
                actions.append(Action("partner_channel", offer_id=offer["offer_id"], budget=950, message_quality=0.9))
            if offer["quality"] < 0.8:
                actions.append(Action("improve_offer", offer_id=offer["offer_id"], budget=600))
            actions.append(Action("run_campaign", offer_id=offer["offer_id"], budget=700, message_quality=0.9))
            if sum(o["customers"] for o in observation.offers) > observation.agent_capacity * 22 and observation.cash > 3000:
                actions.append(Action("hire_agent", budget=1200))
            return actions[:4]

        return self.act(observation)


def get_policy(name: str, seed: int = 0) -> Policy:
    if name == "random":
        return RandomPolicy(seed)
    if name == "conservative":
        return ConservativePolicy()
    if name == "heuristic":
        return HeuristicPolicy()
    if name == "task_heuristic":
        return TaskHeuristicPolicy()
    raise ValueError(f"Unknown policy: {name}")
