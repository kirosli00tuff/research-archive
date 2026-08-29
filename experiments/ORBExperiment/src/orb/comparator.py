"""The sealed comparator — the single exception to the blindness field lists.

**It is a sealed writer.** It reads price and volume values from two vendors,
emits **only aggregate mismatch counts and rates**, and **returns no bar value
to any caller**. Pinned by
``tests/test_guards.py::test_comparator_returns_no_bar_value``.

Why the exception exists. Concretum Research ran identical opening-range code
against four vendors with identical dates, parameters and starting capital and
reported final portfolio values from **226,000 to 726,000 USD** — a threefold
spread from vendor choice alone (carried, C-13). Measuring that spread requires
comparing prices. **Measuring it is not the same as reading it**, and the
difference is enforced here: every public method returns an `int`, a `float`
share, or a frozen findings record whose fields are all counts.

The two measurements this module exists for:

- **A.1 TASK 3, bar revision.** Identical request set, re-sent after at least 14
  calendar days. What share of stored bytes changed?
- **A.1 TASK 4, cross-vendor agreement.** Identical slice from a second vendor.
  What share of session-ticker pairs disagree on the **first-5-minute high or
  low** — the only disagreement that changes an entry price?
"""

from __future__ import annotations

import hashlib
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Final, final

from orb.integrity import AgreementFinding, RevisionFinding

CENT: Final[int] = 100
"""Prices are compared in integer cents. Float equality on money is a bug."""

_OHLC_KEYS: Final[tuple[tuple[str, ...], ...]] = (
    ("o", "open"),
    ("h", "high"),
    ("l", "low"),
    ("c", "close"),
)
"""Vendor dialects for the four priced fields, read only inside this module."""


def _to_cents(value: object) -> int | None:
    """Round a served price to integer cents. Non-numeric returns None."""
    if isinstance(value, bool) or not isinstance(value, int | float):
        return None
    return round(float(value) * CENT)


def _ohlc_cents(bar: Mapping[str, object]) -> tuple[int | None, ...]:
    """The four priced fields of one bar, in cents. Never returned to a caller."""
    out: list[int | None] = []
    for aliases in _OHLC_KEYS:
        found: int | None = None
        for alias in aliases:
            if alias in bar:
                found = _to_cents(bar[alias])
                break
        out.append(found)
    return tuple(out)


def _timestamps(bars: Sequence[Mapping[str, object]]) -> set[int]:
    """Bar timestamps. A **readable** field: no gate applies."""
    stamps: set[int] = set()
    for bar in bars:
        for alias in ("t", "timestamp"):
            if alias in bar:
                raw = bar[alias]
                if isinstance(raw, int) and not isinstance(raw, bool):
                    stamps.add(raw)
                break
    return stamps


@final
class SealedComparator:
    """Reads two vendors' bars. Returns counts. Never returns a bar value."""

    __slots__ = ()

    # --- A.1 TASK 3 — bar revision ------------------------------------

    def compare_pulls(
        self,
        first: Mapping[str, bytes],
        second: Mapping[str, bytes],
        first_bars: Mapping[str, Sequence[Mapping[str, object]]],
        second_bars: Mapping[str, Sequence[Mapping[str, object]]],
        corporate_action_keys: frozenset[str],
        wait_days_observed: int,
    ) -> RevisionFinding:
        """Measure what changed between two identical request sets.

        ``first`` and ``second`` map a session-ticker key to the **raw stored
        bytes** of each pull. The byte comparison needs no parse at all.
        """
        keys = sorted(set(first) & set(second))
        changed_files = 0
        changed_count_pairs = 0
        timestamp_change_pairs = 0
        corporate_action_overlap = 0
        bars_compared = 0
        changed_bars = 0

        for key in keys:
            if (
                hashlib.sha256(first[key]).digest()
                != hashlib.sha256(second[key]).digest()
            ):
                changed_files += 1
                if key in corporate_action_keys:
                    corporate_action_overlap += 1

            a = first_bars.get(key, ())
            b = second_bars.get(key, ())
            bars_compared += max(len(a), len(b))

            if len(a) != len(b):
                changed_count_pairs += 1

            stamps_a, stamps_b = _timestamps(a), _timestamps(b)
            if stamps_a != stamps_b:
                timestamp_change_pairs += 1

            by_stamp_a = {
                s: _ohlc_cents(bar) for bar, s in zip(a, sorted(stamps_a), strict=False)
            }
            by_stamp_b = {
                s: _ohlc_cents(bar) for bar, s in zip(b, sorted(stamps_b), strict=False)
            }
            for stamp in set(by_stamp_a) | set(by_stamp_b):
                if by_stamp_a.get(stamp) != by_stamp_b.get(stamp):
                    changed_bars += 1

        share = changed_bars / bars_compared if bars_compared else 0.0
        return RevisionFinding(
            changed_bar_share=share,
            bars_compared=bars_compared,
            changed_bar_count=changed_bars,
            session_ticker_pairs_compared=len(keys),
            pairs_with_changed_bar_count=changed_count_pairs,
            pairs_with_timestamp_change=timestamp_change_pairs,
            changes_coinciding_with_corporate_action=corporate_action_overlap,
            wait_days_observed=wait_days_observed,
        )

    # --- A.1 TASK 4 — cross-vendor agreement --------------------------

    def compare_vendors(
        self,
        primary: Mapping[str, Sequence[Mapping[str, object]]],
        secondary: Mapping[str, Sequence[Mapping[str, object]]],
        opening_range_windows: Mapping[str, tuple[int, int]],
        delisted_served: int,
        delisted_with_intraday: int,
    ) -> AgreementFinding:
        """Measure cross-vendor agreement. Returns counts only.

        ``opening_range_windows`` maps a session-ticker key to the half-open
        ``[start_ms, end_ms)`` of its opening range, resolved by
        ``orb.sessionclock`` so that the window is DST-correct.
        """
        keys = sorted(set(primary) & set(secondary))
        present_in_both = 0
        agreeing_to_the_cent = 0
        pairs_agreeing_first5 = 0

        for key in keys:
            a_bars = {s: bar for bar, s in self._stamped(primary[key])}
            b_bars = {s: bar for bar, s in self._stamped(secondary[key])}
            shared = set(a_bars) & set(b_bars)
            present_in_both += len(shared)
            for stamp in shared:
                if _ohlc_cents(a_bars[stamp]) == _ohlc_cents(b_bars[stamp]):
                    agreeing_to_the_cent += 1

            start, end = opening_range_windows.get(key, (0, 0))
            if self._first5_extremes(a_bars, start, end) == self._first5_extremes(
                b_bars, start, end
            ):
                pairs_agreeing_first5 += 1

        share = pairs_agreeing_first5 / len(keys) if keys else 0.0
        return AgreementFinding(
            first5_high_low_agreement_share=share,
            session_ticker_pairs_compared=len(keys),
            bars_present_in_both=present_in_both,
            bars_agreeing_to_the_cent=agreeing_to_the_cent,
            delisted_names_served=delisted_served,
            delisted_names_with_intraday_history=delisted_with_intraday,
        )

    @staticmethod
    def _stamped(
        bars: Sequence[Mapping[str, object]],
    ) -> list[tuple[Mapping[str, object], int]]:
        out: list[tuple[Mapping[str, object], int]] = []
        for bar in bars:
            for alias in ("t", "timestamp"):
                raw = bar.get(alias)
                if isinstance(raw, int) and not isinstance(raw, bool):
                    out.append((bar, raw))
                    break
        return out

    @staticmethod
    def _first5_extremes(
        bars: Mapping[int, Mapping[str, object]], start_ms: int, end_ms: int
    ) -> tuple[int | None, int | None]:
        """The opening range high and low in cents. **Internal only.**

        Returned to `compare_vendors` for an equality test and to nothing else.
        A caller outside this module cannot reach it: the method is private and
        `compare_vendors` returns an `AgreementFinding` of counts.
        """
        highs: list[int] = []
        lows: list[int] = []
        for stamp, bar in bars.items():
            if not (start_ms <= stamp < end_ms):
                continue
            _, high, low, _ = _ohlc_cents(bar)
            if high is not None:
                highs.append(high)
            if low is not None:
                lows.append(low)
        return (max(highs) if highs else None, min(lows) if lows else None)


@final
@dataclass(frozen=True, slots=True)
class ComparatorContract:
    """What the comparator may return, asserted as data for the guard to read."""

    returns: tuple[str, ...] = ("RevisionFinding", "AgreementFinding")
    every_field_is_a_count: bool = True
