"""H5 spend and pacing (Section 7). Zero dollars, one shared request ledger.

The H5 census rides the existing daily pass under the measured pacing of
`npl.pacing`, charging the one request ledger like every other collector
(standing rule 9). Two protections keep it from displacing H2 work:

1. a **per-pass H5 cap** of its own, well under the registered daily cap; and
2. an **entry check** against the H2 soft budget: H5 runs last in the daily
   pass and refuses to start when the day's spend has already reached the
   soft budget, so a long H2 catch-up simply postpones H5 to tomorrow rather
   than the reverse.
"""

from __future__ import annotations

from dataclasses import dataclass

from npl.clock import MS_PER_DAY
from npl.config import CONFIG, Config


class H5BudgetExceeded(RuntimeError):
    """A planned H5 pass exceeds its own registered cap. Refused before sending."""


@dataclass(frozen=True, slots=True)
class PassBudget:
    """The arithmetic of one H5 pass, stated before a single request is sent."""

    dexs: int
    instruments: int
    perp_dexs_requests: int
    meta_requests: int
    ctx_requests: int
    l2_requests: int

    @property
    def total(self) -> int:
        return self.perp_dexs_requests + self.meta_requests + self.ctx_requests + self.l2_requests


def daily_pass_budget(dexs: int, instruments: int) -> PassBudget:
    """One perpDexs, one meta and one metaAndAssetCtxs per dex, one l2Book each."""
    if dexs < 0 or instruments < 0:
        raise ValueError("a request budget cannot be negative")
    return PassBudget(
        dexs=dexs,
        instruments=instruments,
        perp_dexs_requests=1,
        meta_requests=dexs,
        ctx_requests=dexs,
        l2_requests=instruments,
    )


def refuse_over_h5_cap(budget: PassBudget, cfg: Config = CONFIG) -> None:
    """The H5 pass cap, charged as arithmetic before anything is sent."""
    if budget.total > cfg.h5_daily_request_cap:
        raise H5BudgetExceeded(
            f"the planned H5 pass is {budget.total} requests "
            f"({budget.dexs} dexs, {budget.instruments} instruments) against the "
            f"registered H5 cap of {cfg.h5_daily_request_cap}. Nothing was sent."
        )


def share_of_daily_cap(budget: PassBudget, cfg: Config = CONFIG) -> float:
    """The pass's share of the registered daily request cap."""
    return budget.total / cfg.request_cap_per_day


def retro_request_budget(instruments: int, cfg: Config = CONFIG) -> int:
    """Worst-case fundingHistory pages for the retrospective read."""
    return instruments * cfg.h5_retro_page_budget


def retro_window_ms(now_ms: int, cfg: Config = CONFIG) -> tuple[int, int]:
    """The registered retrospective span: lookback days back from now."""
    return now_ms - cfg.h5_retro_lookback_days * MS_PER_DAY, now_ms
