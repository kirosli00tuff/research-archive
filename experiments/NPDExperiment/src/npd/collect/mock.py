"""The mock adapter. Five scenarios, no network, no spend.

Every collector behaviour that matters is proved here before B.1 sends one real
call: a clean full pass, a mid-run kill and resume, a forced model failure, a
forced source failure, and a spend refusal.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from random import Random

from npd.collect.adapter import Answer, TransientFault, Usage
from npd.collect.prompt import Prompt

SCENARIO_CLEAN = "clean"
SCENARIO_KILL_RESUME = "kill_resume"
SCENARIO_MODEL_FAILED = "model_failed"
SCENARIO_SOURCE_FAILED = "source_failed"
SCENARIO_SPEND_REFUSED = "spend_refused"

ALL_SCENARIOS = (
    SCENARIO_CLEAN,
    SCENARIO_KILL_RESUME,
    SCENARIO_MODEL_FAILED,
    SCENARIO_SOURCE_FAILED,
    SCENARIO_SPEND_REFUSED,
)

# Token counts a real call is expected to produce. Used so the mock exercises
# the same spend arithmetic the live run will.
MOCK_INPUT_TOKENS = 1600
MOCK_OUTPUT_TOKENS = 150
MOCK_REASONING_TOKENS = 1000


class KilledMidRun(RuntimeError):
    """The scripted kill. Simulates a reboot in the middle of a batch."""


@dataclass
class MockAdapter:
    """Answers from a script. Deterministic given its seed."""

    name: str = "mock"
    seed: int = 7
    fail_dates: frozenset[str] = frozenset()
    kill_after: int | None = None
    calls: list[str] = field(default_factory=list)
    _rng: Random = field(default_factory=lambda: Random(7))

    def rank(self, prompt: Prompt, date: str = "", effort: str | None = None) -> Answer:
        _ = effort
        self.calls.append(date)
        if self.kill_after is not None and len(self.calls) > self.kill_after:
            raise KilledMidRun(f"scripted kill after {self.kill_after} calls")
        if date in self.fail_dates:
            # A model that answers with something unusable. Retried by the
            # collector, then recorded as model_failed once retries run out.
            raise TransientFault("scripted model fault")

        order = list(prompt.labels)
        self._rng.shuffle(order)
        raw = json.dumps({"ranking": order})
        return Answer(
            ranking=tuple(order),
            raw=raw,
            usage=Usage(
                input_tokens=MOCK_INPUT_TOKENS,
                cached_input_tokens=0,
                output_tokens=MOCK_OUTPUT_TOKENS + MOCK_REASONING_TOKENS,
                reasoning_tokens=MOCK_REASONING_TOKENS,
            ),
            latency_s=0.001,
        )
