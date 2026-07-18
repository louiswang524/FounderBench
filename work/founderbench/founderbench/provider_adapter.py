from __future__ import annotations

import json
import urllib.error
from abc import ABC, abstractmethod
from json import JSONDecodeError

from .schema import Action, Observation


class ProviderResponseError(ValueError):
    def __init__(self, category: str, message: str):
        super().__init__(message)
        self.category = category


class ProviderAdapter(ABC):
    """Adapter contract for external LLM providers.

    A provider receives an Observation and must return validated FounderBench
    actions. Real adapters can call OpenAI, Anthropic, Google, local models, or
    a hosted agent runtime. The simulator never trusts free-form text directly.
    """

    @abstractmethod
    def act(self, observation: Observation) -> list[Action]:
        raise NotImplementedError


def observation_to_prompt(observation: Observation) -> str:
    payload = {
        "task": "Maximize risk-adjusted company score in FounderBench.",
        "rules": [
            "Return only JSON.",
            "Use supported action types.",
            "Do not spend more cash than the company has.",
            "Avoid spam, false claims, and excessive risk.",
        ],
        "supported_actions": [
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
        ],
        "observation": observation.__dict__,
        "response_schema": {
            "rationale": "short string",
            "actions": [
                {
                    "type": "build_offer",
                    "market_id": "market id when relevant",
                    "offer_id": "offer id when relevant",
                    "budget": 1000,
                    "price": 249,
                    "message_quality": 0.8,
                }
            ],
        },
    }
    return json.dumps(payload, indent=2)


def parse_provider_response(text: str) -> list[Action]:
    try:
        data = json.loads(text)
    except JSONDecodeError as exc:
        raise ProviderResponseError("invalid_json", f"Provider response is not valid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise ProviderResponseError("invalid_response_root", "Provider response JSON root must be an object.")
    if "actions" not in data:
        raise ProviderResponseError("missing_actions", "Provider response missing required 'actions' key.")
    actions = data.get("actions", [])
    if not isinstance(actions, list):
        raise ProviderResponseError("invalid_actions_type", "Provider response 'actions' must be a list.")
    parsed: list[Action] = []
    for idx, action in enumerate(actions):
        if not isinstance(action, dict):
            raise ProviderResponseError("invalid_action_schema", f"Action {idx} must be an object.")
        if "type" not in action:
            raise ProviderResponseError("missing_action_type", f"Action {idx} missing required 'type'.")
        try:
            budget = float(action.get("budget", 0.0) or 0.0)
            price = float(action["price"]) if action.get("price") is not None else None
            message_quality = float(action.get("message_quality", 0.6) or 0.6)
        except (TypeError, ValueError) as exc:
            raise ProviderResponseError("invalid_numeric_field", f"Action {idx} contains a nonnumeric budget, price, or message_quality.") from exc
        parsed.append(
            Action(
                type=action["type"],
                market_id=action.get("market_id"),
                offer_id=action.get("offer_id"),
                budget=budget,
                price=price,
                message_quality=message_quality,
                metadata={k: v for k, v in action.items() if k not in {"type", "market_id", "offer_id", "budget", "price", "message_quality"}},
            )
        )
    return parsed


def classify_provider_exception(exc: Exception) -> str:
    if isinstance(exc, ProviderResponseError):
        return exc.category
    if isinstance(exc, urllib.error.HTTPError) and exc.code == 429:
        return "provider_rate_limit"
    if isinstance(exc, TimeoutError):
        return "provider_timeout"
    if isinstance(exc, OSError):
        return "provider_io_error"
    return "provider_exception"
