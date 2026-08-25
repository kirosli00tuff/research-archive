"""The deterministic seeded stratified draw of 30 names.

The draw reproduces from the registered seed and the date alone. It never
consults an outcome, and eligibility is decided by data availability, which is
known before any forward return exists.
"""

from __future__ import annotations

import hashlib
from collections.abc import Sequence
from dataclasses import dataclass
from random import Random

from npd.config import CONFIG, Config


@dataclass(frozen=True, slots=True)
class Draw:
    date: str
    formation_date: str
    picks: tuple[tuple[str, int], ...]
    eligible_pool: int

    @property
    def symbols(self) -> tuple[str, ...]:
        return tuple(s for s, _ in self.picks)


def seed_for(date: str, cfg: Config = CONFIG) -> int:
    """A stable integer seed from the registered seed and the session date."""
    digest = hashlib.blake2b(f"{cfg.panel_seed}:{date}".encode(), digest_size=8).digest()
    return int.from_bytes(digest, "big")


def stratum_of(rank: int, top_n: int, strata: int) -> int:
    """Which stratum a formation rank falls in, zero based.

    Ranks split into equal bands by rank, so the panel spans the liquidity
    range instead of concentrating in the largest names.
    """
    if rank < 1 or rank > top_n:
        raise ValueError(f"rank {rank} outside 1..{top_n}")
    band = top_n / strata
    return min(strata - 1, int((rank - 1) // band))


def draw(
    date: str,
    formation_date: str,
    eligible: Sequence[tuple[str, int]],
    cfg: Config = CONFIG,
) -> Draw | None:
    """Draw the registered panel size, stratified by formation rank.

    `eligible` is (symbol, formation rank) for members whose feature block is
    complete on this date. Returns None when the eligible pool cannot fill the
    panel, which the caller records as no_data rather than filling short.
    """
    if len(eligible) < cfg.panel_size:
        return None

    rng = Random(seed_for(date, cfg))
    buckets: dict[int, list[tuple[str, int]]] = {i: [] for i in range(cfg.strata_count)}
    for sym, rank in sorted(eligible):
        buckets[stratum_of(rank, 500, cfg.strata_count)].append((sym, rank))

    per_stratum = cfg.panel_size // cfg.strata_count
    picks: list[tuple[str, int]] = []
    shortfall: list[tuple[str, int]] = []
    for i in range(cfg.strata_count):
        pool = buckets[i]
        chosen = rng.sample(pool, per_stratum) if len(pool) >= per_stratum else list(pool)
        picks.extend(chosen)
        remaining = [x for x in pool if x not in set(chosen)]
        shortfall.extend(remaining)

    # A thin stratum is topped up from the remaining eligible names in a fixed
    # order, so the panel size is exact and the fill is reproducible.
    if len(picks) < cfg.panel_size:
        shortfall.sort()
        need = cfg.panel_size - len(picks)
        if len(shortfall) < need:
            return None
        picks.extend(rng.sample(shortfall, need))

    picks.sort()
    return Draw(
        date=date,
        formation_date=formation_date,
        picks=tuple(picks),
        eligible_pool=len(eligible),
    )
