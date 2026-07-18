from __future__ import annotations

import json
import os
import re
import hashlib
import urllib.request
from dataclasses import asdict
from typing import Any, get_args

from .provider_adapter import ProviderResponseError, parse_provider_response
from .schema import Action, ActionType, Observation
from .tasks import StartupTask


KEY_PATTERN = re.compile(r"\b(?:sk-[A-Za-z0-9_\-]{12,}|AQ\.[A-Za-z0-9_\-]{12,}|AIza[0-9A-Za-z_\-]{20,})\b")
PROMPT_VERSION = "founderbench-task-agent-v0.3"
SYSTEM_PROMPT = "You are an LLM startup agent in FounderBench. Return only valid JSON."
DEEPSEEK_SYSTEM_PROMPT = "You are an LLM startup agent. Return only valid JSON."
PROMPT_OBJECTIVE = (
    "Choose actions that maximize the bounded 0-100 task score. Preserve runway, "
    "avoid unsafe/spammy behavior, and satisfy the task objective."
)
ACTION_TYPE_TEXT = " | ".join(get_args(ActionType))
RESPONSE_SCHEMA = {
    "rationale": "brief reason",
    "actions": [
        {
            "type": ACTION_TYPE_TEXT,
            "market_id": "required for research_market/build_offer/pivot_market; optional for interview_customers",
            "offer_id": "required for run_campaign/improve_offer/change_price/pivot_market/partner_channel; optional for interview_customers",
            "budget": 0,
            "price": "used for build_offer/change_price; used as funding ask for raise_funding",
            "message_quality": 0.8,
        }
    ],
}
PROMPT_RULES = [
    "Return only JSON with keys rationale and actions.",
    "Use at most 4 actions per week.",
    "Do not spend more cash than available.",
    "If an action needs market_id or offer_id, use one from the observation.",
    "Use do_nothing only when no useful action remains.",
    "Do not make unsupported claims; the simulator only executes structured actions.",
]


def build_prompt_payload(task: StartupTask, observation: Observation) -> dict[str, Any]:
    return {
        "benchmark": "FounderBench",
        "prompt_version": PROMPT_VERSION,
        "task": {
            "task_id": task.task_id,
            "name": task.name,
            "description": task.description,
            "weeks_remaining": max(0, task.weeks - observation.week + 1),
            "pass_threshold": task.pass_threshold,
        },
        "objective": PROMPT_OBJECTIVE,
        "allowed_actions": sorted(task.allowed_actions),
        "observation": asdict(observation),
        "response_schema": RESPONSE_SCHEMA,
        "rules": PROMPT_RULES,
    }


def render_task_prompt(task: StartupTask, observation: Observation) -> str:
    return json.dumps(build_prompt_payload(task, observation), indent=2)


def redact_text(text: str) -> str:
    return KEY_PATTERN.sub("[REDACTED_API_KEY]", text)


def _usage_tokens(body: dict[str, Any]) -> dict[str, int]:
    usage = body.get("usage") or body.get("usageMetadata") or {}
    prompt_tokens = int(usage.get("prompt_tokens") or usage.get("input_tokens") or usage.get("promptTokenCount") or 0)
    completion_tokens = int(usage.get("completion_tokens") or usage.get("output_tokens") or usage.get("candidatesTokenCount") or 0)
    total_tokens = int(usage.get("total_tokens") or usage.get("totalTokenCount") or prompt_tokens + completion_tokens)
    return {
        "prompt_tokens": prompt_tokens,
        "completion_tokens": completion_tokens,
        "total_tokens": total_tokens,
    }


def _estimated_cost_usd(tokens: dict[str, int]) -> float:
    input_per_million = float(os.environ.get("MODEL_INPUT_COST_PER_MILLION", "0") or 0)
    output_per_million = float(os.environ.get("MODEL_OUTPUT_COST_PER_MILLION", "0") or 0)
    return round(
        tokens["prompt_tokens"] * input_per_million / 1_000_000
        + tokens["completion_tokens"] * output_per_million / 1_000_000,
        6,
    )


class ProviderAuditMixin:
    provider_name = "unknown"

    def _reset_provider_calls(self) -> None:
        self.provider_calls: list[dict[str, Any]] = []

    def _record_provider_call(self, *, task: StartupTask, observation: Observation, prompt: str, body: dict[str, Any], content: str, latency_s: float) -> None:
        if not hasattr(self, "provider_calls"):
            self._reset_provider_calls()
        tokens = _usage_tokens(body)
        self.provider_calls.append(
            {
                "provider": self.provider_name,
                "model": getattr(self, "model", None),
                "task_id": task.task_id,
                "week": observation.week,
                "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
                "raw_response_redacted": redact_text(content),
                "usage": tokens,
                "estimated_cost_usd": _estimated_cost_usd(tokens),
                "latency_s": round(latency_s, 4),
            }
        )

    def consume_provider_calls(self) -> list[dict[str, Any]]:
        calls = list(getattr(self, "provider_calls", []))
        self._reset_provider_calls()
        return calls


class OpenAICompatibleTaskPolicy(ProviderAuditMixin):
    """Task policy for OpenAI-compatible chat-completion APIs.

    Intended for local/open-source providers served by vLLM, LM Studio, Ollama
    OpenAI-compatible mode, or any compatible hosted endpoint.
    """

    provider_name = "openai_compatible"

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        timeout_s: int = 60,
    ):
        self.base_url = (base_url or os.environ.get("OPENAI_COMPAT_BASE_URL") or "").rstrip("/")
        self.api_key = api_key or os.environ.get("OPENAI_COMPAT_API_KEY") or os.environ.get("OPENAI_API_KEY")
        self.model = model or os.environ.get("OPENAI_COMPAT_MODEL")
        self.temperature = temperature
        self.timeout_s = timeout_s
        if not self.base_url:
            raise ValueError("Set OPENAI_COMPAT_BASE_URL, for example http://localhost:8000/v1")
        if not self.model:
            raise ValueError("Set OPENAI_COMPAT_MODEL, for example Qwen/Qwen2.5-14B-Instruct")

    def act_task(self, task: StartupTask, observation: Observation) -> list[Action]:
        self._reset_provider_calls()
        prompt = self._prompt(task, observation)
        payload = {
            "model": self.model,
            "temperature": self.temperature,
            "messages": [
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {"role": "user", "content": prompt},
            ],
        }
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=data,
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {self.api_key}"} if self.api_key else {}),
            },
            method="POST",
        )
        import time
        started = time.perf_counter()
        with urllib.request.urlopen(request, timeout=self.timeout_s) as response:
            body = json.loads(response.read().decode("utf-8"))
        latency_s = time.perf_counter() - started
        content = body["choices"][0]["message"]["content"]
        self._record_provider_call(task=task, observation=observation, prompt=prompt, body=body, content=content, latency_s=latency_s)
        return parse_provider_response(content)

    def _prompt(self, task: StartupTask, observation: Observation) -> str:
        return render_task_prompt(task, observation)


def _request_json(url: str, payload: dict[str, Any] | None, headers: dict[str, str], timeout_s: int = 60, method: str | None = None) -> dict[str, Any]:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    request = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method or ("POST" if payload is not None else "GET"),
    )
    with urllib.request.urlopen(request, timeout=timeout_s) as response:
        return json.loads(response.read().decode("utf-8"))


def _extract_json_object(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?", "", text).strip()
        text = re.sub(r"```$", "", text).strip()
    if text.startswith("{"):
        return text
    match = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not match:
        raise ProviderResponseError("no_json_object", f"Provider did not return a JSON object: {text[:200]}")
    return match.group(0)


class BaseHostedTaskPolicy(ProviderAuditMixin):
    def _prompt(self, task: StartupTask, observation: Observation) -> str:
        return render_task_prompt(task, observation)


class DeepSeekTaskPolicy(BaseHostedTaskPolicy):
    provider_name = "deepseek"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout_s: int = 60, temperature: float = 0.2):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
        self.model = model or os.environ.get("DEEPSEEK_MODEL") or "deepseek-chat"
        self.timeout_s = int(os.environ.get("PROVIDER_TIMEOUT_S", timeout_s))
        self.temperature = temperature
        if not self.api_key:
            raise ValueError("Set DEEPSEEK_API_KEY.")

    def act_task(self, task: StartupTask, observation: Observation) -> list[Action]:
        self._reset_provider_calls()
        return self._sample_actions(task, observation, self.temperature)

    def _sample_actions(self, task: StartupTask, observation: Observation, temperature: float) -> list[Action]:
        import time
        prompt = self._prompt(task, observation)
        started = time.perf_counter()
        body = _request_json(
            "https://api.deepseek.com/chat/completions",
            {
                "model": self.model,
                "temperature": temperature,
                "messages": [
                    {"role": "system", "content": DEEPSEEK_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            },
            {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}",
            },
            timeout_s=self.timeout_s,
        )
        latency_s = time.perf_counter() - started
        content = body["choices"][0]["message"]["content"]
        self._record_provider_call(task=task, observation=observation, prompt=prompt, body=body, content=content, latency_s=latency_s)
        return parse_provider_response(_extract_json_object(content))


class DeepSeekSelfConsistencyTaskPolicy(DeepSeekTaskPolicy):
    """Sample k DeepSeek action plans and select a consensus candidate."""

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout_s: int = 60, k: int | None = None):
        super().__init__(api_key=api_key, model=model, timeout_s=timeout_s, temperature=float(os.environ.get("SC_TEMPERATURE", "0.7")))
        self.k = k or int(os.environ.get("SC_K", "3"))

    def act_task(self, task: StartupTask, observation: Observation) -> list[Action]:
        self._reset_provider_calls()
        candidates = [self._sample_actions(task, observation, self.temperature) for _ in range(self.k)]
        return self._select_candidate(task, observation, candidates)

    def _select_candidate(self, task: StartupTask, observation: Observation, candidates: list[list[Action]]) -> list[Action]:
        signatures = [self._signature(actions) for actions in candidates]
        counts = {signature: signatures.count(signature) for signature in set(signatures)}
        best_count = max(counts.values())
        majority_indices = [i for i, signature in enumerate(signatures) if counts[signature] == best_count]
        if best_count > 1:
            return candidates[majority_indices[0]]
        return min(candidates, key=lambda actions: self._risk_tie_break(task, observation, actions))

    def _signature(self, actions: list[Action]) -> tuple[tuple[str, str | None, str | None], ...]:
        return tuple((action.type, action.market_id, action.offer_id) for action in actions[:4])

    def _risk_tie_break(self, task: StartupTask, observation: Observation, actions: list[Action]) -> float:
        task_num = int(task.task_id.split("-")[1])
        family = (task_num - 1) // 5
        budget = sum(max(0.0, action.budget) for action in actions)
        score = 0.0
        if budget > observation.cash:
            score += 10_000 + budget - observation.cash
        if budget > observation.cash * 0.65:
            score += 1_000 + budget - observation.cash * 0.65
        if len(actions) > 4:
            score += 500
        useful_by_family = [
            {"research_market", "build_offer"},
            {"research_market", "build_offer", "run_campaign", "improve_offer"},
            {"improve_offer", "support_customers"},
            {"hire_agent", "support_customers", "improve_offer"},
            {"improve_offer", "run_campaign", "support_customers", "hire_agent"},
            {"change_price", "interview_customers", "run_campaign"},
            {"cut_cost", "support_customers", "improve_offer"},
            {"research_market", "pivot_market", "interview_customers", "partner_channel"},
            {"raise_funding", "support_customers", "improve_offer"},
            {"partner_channel", "run_campaign", "hire_agent", "improve_offer"},
        ][family]
        types = {action.type for action in actions}
        if not types & useful_by_family:
            score += 250
        if types == {"do_nothing"}:
            score += 200
        return score + budget / 1000


class AnthropicTaskPolicy(BaseHostedTaskPolicy):
    provider_name = "anthropic"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout_s: int = 60):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        self.model = model or os.environ.get("ANTHROPIC_MODEL") or "claude-sonnet-4-5"
        self.timeout_s = int(os.environ.get("PROVIDER_TIMEOUT_S", timeout_s))
        if not self.api_key:
            raise ValueError("Set ANTHROPIC_API_KEY.")

    def act_task(self, task: StartupTask, observation: Observation) -> list[Action]:
        self._reset_provider_calls()
        import time
        prompt = self._prompt(task, observation)
        started = time.perf_counter()
        body = _request_json(
            "https://api.anthropic.com/v1/messages",
            {
                "model": self.model,
                "max_tokens": 900,
                "temperature": 0.2,
                "system": SYSTEM_PROMPT,
                "messages": [{"role": "user", "content": prompt}],
            },
            {
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
            timeout_s=self.timeout_s,
        )
        latency_s = time.perf_counter() - started
        text_blocks = [block.get("text", "") for block in body.get("content", []) if block.get("type") == "text"]
        content = "\n".join(text_blocks)
        self._record_provider_call(task=task, observation=observation, prompt=prompt, body=body, content=content, latency_s=latency_s)
        return parse_provider_response(_extract_json_object(content))


class GeminiTaskPolicy(BaseHostedTaskPolicy):
    provider_name = "gemini"

    def __init__(self, api_key: str | None = None, model: str | None = None, timeout_s: int = 60):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        self.model = model or os.environ.get("GEMINI_MODEL") or "gemini-2.5-flash"
        self.timeout_s = int(os.environ.get("PROVIDER_TIMEOUT_S", timeout_s))
        if not self.api_key:
            raise ValueError("Set GEMINI_API_KEY.")

    def act_task(self, task: StartupTask, observation: Observation) -> list[Action]:
        self._reset_provider_calls()
        import time
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent?key={self.api_key}"
        prompt = self._prompt(task, observation)
        started = time.perf_counter()
        body = _request_json(
            url,
            {
                "contents": [
                    {
                        "role": "user",
                        "parts": [
                            {
                                "text": SYSTEM_PROMPT + "\n\n" + prompt
                            }
                        ],
                    }
                ],
                "generationConfig": {"temperature": 0.2, "maxOutputTokens": 1600},
            },
            {"Content-Type": "application/json"},
            timeout_s=self.timeout_s,
        )
        latency_s = time.perf_counter() - started
        parts = body["candidates"][0]["content"]["parts"]
        text = "\n".join(part.get("text", "") for part in parts)
        self._record_provider_call(task=task, observation=observation, prompt=prompt, body=body, content=text, latency_s=latency_s)
        return parse_provider_response(_extract_json_object(text))
