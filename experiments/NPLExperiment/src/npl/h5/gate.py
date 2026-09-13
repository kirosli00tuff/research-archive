"""The H5 retrospective blindness gate. Read-only on the cohort ledgers.

The contemporaneous read (mark, reference, open interest, touch state) is
descriptive venue state under the same reasoning that made the entry-anchor
l2Book snapshot descriptive in H1 Section 5: it is a cost and state input,
not an outcome. **A historical deviation series is different.** Where the
venue serves one, it is a near-deterministic function of the funding rate,
so reading it across a registered event's open outcome window would be a
post-entry funding read wearing a different field name.

So the retrospective read alone is gated. A coin belonging to any registered
cohort — the H1 generating sample, the H2/H3/H4 fresh plan, or either leg of
an assigned H2 pair — records `excluded_quarantined` for the retrospective
series and contributes to the coverage census only. Its contemporaneous
snapshot is unaffected.

The cohort ledgers are **read** here and never written; `npl.h5.stores`
holds the write side. Reading is the mechanism by which the quarantine is
honoured, not a breach of it.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from npl.h5.stores import read_rows
from npl.paths import (
    FRESH_PLAN,
    GENERATING_SAMPLE_JSON,
    H2_PAIRS_LEDGER,
    H2_PAIRS_V2_LEDGER,
)

EXCLUDED_QUARANTINED = "excluded_quarantined"


class H5RetrospectiveGated(RuntimeError):
    """A registered-cohort coin reached the retrospective read. Refused."""


class CohortLedgerUnavailable(RuntimeError):
    """A cohort ledger is missing. The gate refuses to run open-loop."""


@dataclass(frozen=True, slots=True)
class Cohorts:
    """The registered cohorts, as coin strings. Counts travel with the set."""

    generating_sample: frozenset[str]
    fresh_plan: frozenset[str]
    h2_pairs: frozenset[str]

    @property
    def all_coins(self) -> frozenset[str]:
        return self.generating_sample | self.fresh_plan | self.h2_pairs

    def membership(self, coin: str) -> tuple[str, ...]:
        """Which cohorts claim this coin, in registered order."""
        found: list[str] = []
        if coin in self.generating_sample:
            found.append("generating_sample")
        if coin in self.fresh_plan:
            found.append("fresh_plan")
        if coin in self.h2_pairs:
            found.append("h2_pairs")
        return tuple(found)


def _require(path: Path) -> Path:
    if not path.exists():
        raise CohortLedgerUnavailable(
            f"{path} is absent. The H5 retrospective gate cannot run open-loop: the "
            f"cohort ledgers decide which histories are quarantined."
        )
    return path


def load_cohorts(
    generating_path: Path = GENERATING_SAMPLE_JSON,
    fresh_path: Path = FRESH_PLAN,
    pairs_path: Path = H2_PAIRS_LEDGER,
    pairs_v2_path: Path = H2_PAIRS_V2_LEDGER,
) -> Cohorts:
    """Read the cohort ledgers. Coin strings only; no value is read.

    **Both H2 pair ledgers are unioned** (Amendment H2-5). The tiered rule
    changed which instruments are pair legs: eight coins joined the cohort and
    twenty-two left it. Reading only one ledger would leave a hole either way,
    so both are read and the union is quarantined.

    The union is deliberately one-directional: a coin that *left* the cohort
    when its pair was reassigned stays quarantined, because H2 has already
    collected it as a pair leg. Un-quarantining is a loosening of a blindness
    gate and is never done as a side effect of a control-rule change.

    A missing v2 ledger is not an error — it simply did not exist before
    Amendment H2-5 — but a missing superseded ledger still is.
    """
    payload = json.loads(_require(generating_path).read_text(encoding="utf-8"))
    generating = frozenset(str(entry).split("|", 1)[0] for entry in payload["event_ids"])
    fresh = frozenset(str(row["coin"]) for row in read_rows(_require(fresh_path)))
    pair_coins: set[str] = set()
    ledgers = [_require(pairs_path)]
    if pairs_v2_path.exists():
        ledgers.append(pairs_v2_path)
    for ledger in ledgers:
        for row in read_rows(ledger):
            for key in ("event_coin", "control_coin"):
                value = row.get(key)
                if value is not None:
                    pair_coins.add(str(value))
    return Cohorts(generating_sample=generating, fresh_plan=fresh, h2_pairs=frozenset(pair_coins))


def is_gated(coin: str, cohorts: Cohorts) -> bool:
    """True where the coin belongs to any registered cohort."""
    return coin in cohorts.all_coins


def require_ungated(coin: str, cohorts: Cohorts) -> None:
    """The refusal: a registered-cohort coin never reaches the retrospective read."""
    claims = cohorts.membership(coin)
    if claims:
        raise H5RetrospectiveGated(
            f"{coin} belongs to the registered cohort(s) {list(claims)}; its historical "
            f"deviation series is a funding-rate proxy over a registered outcome window "
            f"and is refused. The instrument still carries its contemporaneous snapshot "
            f"and counts in the coverage census as {EXCLUDED_QUARANTINED}."
        )
