"""Keep REGISTRATION.md and npd.config from drifting apart.

A registration that says one thing while the code does another is worse than no
registration, because it looks binding. This module reads the committed
registration and asserts it agrees with the frozen config on every value that
appears in both. tests/test_registration.py runs it.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from npd.config import CONFIG, Config
from npd.paths import REPO_ROOT

REGISTRATION = REPO_ROOT / "REGISTRATION.md"


@dataclass(frozen=True, slots=True)
class Disagreement:
    field: str
    config_value: str
    registration_says: str


def check(path: Path = REGISTRATION, cfg: Config = CONFIG) -> list[Disagreement]:
    """Every value the registration and the config both state, compared."""
    text = path.read_text(encoding="utf-8")
    haystack = text.lower()
    out: list[Disagreement] = []

    def want(field: str, needle: str) -> None:
        # Case-insensitive, because a registration is prose and a sentence may
        # start with a value. The value itself still has to be present.
        if needle.lower() not in haystack:
            out.append(Disagreement(field, needle, "absent from REGISTRATION.md"))

    want("gate_model", cfg.gate_model)
    want("knowledge_cutoff", cfg.knowledge_cutoff.isoformat())
    want("cutoff_source_url", cfg.cutoff_source_url)
    want("cutoff_retrieved_on", cfg.cutoff_retrieved_on.isoformat())
    want("window_end", cfg.window_end.isoformat())
    want("universe_id", cfg.universe_id)
    want("panel_size", str(cfg.panel_size))
    want("min_trading_days", str(cfg.min_trading_days))
    want("bootstrap_resamples", f"{cfg.bootstrap_resamples:,}")
    want("spend_cap_usd", f"{cfg.spend_cap_usd:.2f} USD")
    want("primary_horizon_sessions", f"next-{cfg.primary_horizon_sessions}-session")
    want("reasoning_effort", cfg.reasoning_effort)
    for rung in cfg.reasoning_effort_ladder:
        want("reasoning_effort_ladder", f"`{rung}`")

    low, high = cfg.realistic_effect_band
    want("realistic_effect_band", f"{low:g} to {high:g}")

    for name in cfg.feature_names:
        want("feature_names", f"`{name}`")

    return out


def assert_agrees(path: Path = REGISTRATION, cfg: Config = CONFIG) -> None:
    bad = check(path, cfg)
    if bad:
        lines = "\n".join(f"  {d.field}: {d.config_value} {d.registration_says}" for d in bad)
        raise AssertionError(f"the registration and the config disagree:\n{lines}")
