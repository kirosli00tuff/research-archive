"""Model adapters and the retry taxonomy that maps faults onto the five states.

Two adapters exist. The OpenAI adapter calls the registered snapshot. The mock
adapter answers from a scripted scenario and never touches the network, so every
collector behaviour is provable before a cent is spent.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass
from typing import Protocol

import httpx

from npd.collect.prompt import Prompt
from npd.config import CONFIG, Config

OPENAI_URL = "https://api.openai.com/v1/chat/completions"


class TransientFault(RuntimeError):
    """Rate limit, timeout, or server error. Retried with backoff."""


class UnparseableResponse(RuntimeError):
    """The model answered, but not with a usable ranking. Retried."""


class QuotaExhausted(RuntimeError):
    """The account has no balance left. A clean stop, never a failure."""


class AuthFault(RuntimeError):
    """The key was rejected. Not retried, because retrying cannot help."""


@dataclass(frozen=True, slots=True)
class Usage:
    input_tokens: int
    cached_input_tokens: int
    output_tokens: int
    reasoning_tokens: int


@dataclass(frozen=True, slots=True)
class Answer:
    ranking: tuple[str, ...]
    raw: str
    usage: Usage
    latency_s: float


class Adapter(Protocol):
    name: str

    def rank(self, prompt: Prompt, date: str = "") -> Answer:
        """Rank one panel. `date` is passed by the mock so a scenario can script
        a fault on a specific day. The live adapter ignores it, because the date
        is exactly what must never reach the model."""
        ...


def parse_ranking(raw: str, expected: tuple[str, ...]) -> tuple[str, ...]:
    """Pull the ranking out of a response and check it covers every label once.

    A ranking that repeats or omits a label is not a partial answer that can be
    patched. It is an unusable answer, and it is reported as one.
    """
    text = raw.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    try:
        payload = json.loads(text)
    except json.JSONDecodeError as exc:
        raise UnparseableResponse(f"response is not JSON: {exc}") from exc
    if not isinstance(payload, dict) or "ranking" not in payload:
        raise UnparseableResponse("response has no ranking field")
    ranking = payload["ranking"]
    if not isinstance(ranking, list) or not all(isinstance(x, str) for x in ranking):
        raise UnparseableResponse("ranking is not a list of strings")
    if len(ranking) != len(expected):
        raise UnparseableResponse(f"ranking has {len(ranking)} entries, expected {len(expected)}")
    if set(ranking) != set(expected):
        missing = sorted(set(expected) - set(ranking))
        extra = sorted(set(ranking) - set(expected))
        raise UnparseableResponse(f"label mismatch. missing={missing[:5]} extra={extra[:5]}")
    return tuple(ranking)


class OpenAIAdapter:
    """Calls the registered snapshot. Never logs or echoes the key."""

    name = "openai"

    def __init__(self, cfg: Config = CONFIG, *, send_temperature: bool | None = None) -> None:
        self._cfg = cfg
        # Amendment 1. gpt-5-2025-08-07 rejects any temperature other than its
        # default, so the registered value is not sent. Determinism now rests on
        # the seeded panel draw and the frozen prompt.
        self._send_temperature = (
            cfg.send_temperature if send_temperature is None else send_temperature
        )
        key = os.environ.get("OPENAI_API_KEY", "").strip()
        if not key:
            raise AuthFault("OPENAI_API_KEY is not set")
        self._client = httpx.Client(
            timeout=cfg.request_timeout_seconds,
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        )

    @property
    def send_temperature(self) -> bool:
        return self._send_temperature

    def disable_temperature(self) -> None:
        self._send_temperature = False

    def rank(self, prompt: Prompt, date: str = "") -> Answer:
        _ = date  # never sent. See the Adapter protocol.
        body: dict[str, object] = {
            "model": self._cfg.gate_model,
            "messages": [
                {"role": "system", "content": prompt.system},
                {"role": "user", "content": prompt.user},
            ],
            "response_format": {"type": "json_object"},
            "max_completion_tokens": self._cfg.max_output_tokens,
            "reasoning_effort": self._cfg.reasoning_effort,
        }
        if self._send_temperature:
            body["temperature"] = self._cfg.temperature

        t0 = time.monotonic()
        try:
            resp = self._client.post(OPENAI_URL, json=body)
        except httpx.TimeoutException as exc:
            raise TransientFault(f"timeout after {self._cfg.request_timeout_seconds}s") from exc
        except httpx.HTTPError as exc:
            raise TransientFault(f"transport error: {exc}") from exc
        latency = time.monotonic() - t0

        if resp.status_code == 401:
            raise AuthFault("the API key was rejected")
        if resp.status_code == 429 or resp.status_code >= 500:
            detail = _error_code(resp)
            if detail == "insufficient_quota":
                raise QuotaExhausted("the account has no balance left")
            raise TransientFault(f"http {resp.status_code} {detail}")
        if resp.status_code == 400:
            detail = _error_message(resp)
            if "temperature" in detail.lower():
                raise UnsupportedParameter(detail)
            raise UnparseableResponse(f"http 400 {detail}")
        if resp.status_code != 200:
            detail = _error_code(resp)
            if detail == "insufficient_quota":
                raise QuotaExhausted("the account has no balance left")
            raise TransientFault(f"http {resp.status_code} {detail}")

        payload = resp.json()
        raw = payload["choices"][0]["message"]["content"] or ""
        usage_block = payload.get("usage", {}) or {}
        details = usage_block.get("completion_tokens_details", {}) or {}
        cached = (usage_block.get("prompt_tokens_details", {}) or {}).get("cached_tokens", 0)
        usage = Usage(
            input_tokens=int(usage_block.get("prompt_tokens", 0)),
            cached_input_tokens=int(cached or 0),
            output_tokens=int(usage_block.get("completion_tokens", 0)),
            reasoning_tokens=int(details.get("reasoning_tokens", 0) or 0),
        )
        ranking = parse_ranking(raw, prompt.labels)
        return Answer(ranking=ranking, raw=raw, usage=usage, latency_s=latency)


class UnsupportedParameter(RuntimeError):
    """The endpoint rejected a registered parameter. Recorded as an amendment."""


def _error_code(resp: httpx.Response) -> str:
    try:
        return str((resp.json().get("error") or {}).get("code") or "")
    except Exception:
        return ""


def _error_message(resp: httpx.Response) -> str:
    try:
        return str((resp.json().get("error") or {}).get("message") or resp.text[:300])
    except Exception:
        return resp.text[:300]
