"""The two monitor views, structurally separated per Section 12.

The health view is the landing surface and may show anything: timer,
gaps, state counts, membership, the accrual ledger. The verdict view
shows only the confidence sequence against its two registered bars.

The separation is structural. verdict_view consumes verdict ledger
records alone, and it validates every line it emits against an
allowlist of confidence-sequence shapes, raising VerdictViewError
rather than rendering anything else. tests/test_monitor_guard.py fails
the render if anything else enters it, which is the registered guard.
"""
from __future__ import annotations

import re
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from hfexperiment.registered import (
    PROJECTION_CLEAR_HURDLE_DAY,
    PROJECTION_CLEAR_ZERO_DAY,
    PROJECTION_MEAN_BP,
    RHO_FROZEN,
    SHADOW_SERIES_START,
    THRESHOLDS,
)

# -- health view ------------------------------------------------------


@dataclass(frozen=True)
class HealthData:
    """Everything the landing surface shows. Assembled by daily_run."""

    generated_utc: str
    credentials: str
    timer_lines: Sequence[str]
    last_run: str
    last_complete_session: str | None
    next_formation: str | None
    days_to_next_formation: int | None
    gaps: Sequence[str]
    state_counts: Mapping[str, int]
    books: Mapping[int, Sequence[str]]
    benchmark_size: int | None
    pointers: Mapping[str, str]
    accrual_tail: Sequence[str]
    recent_fetches: Sequence[str]


def health_view(data: HealthData) -> str:
    """The landing surface. May show anything."""
    lines: list[str] = []
    lines.append(f"HEALTH VIEW  generated {data.generated_utc}")
    lines.append(f"series start: {SHADOW_SERIES_START} formation")
    lines.append(f"credentials: {data.credentials}")
    lines.append("timer:")
    lines.extend(f"  {line}" for line in data.timer_lines)
    lines.append(f"last run: {data.last_run}")
    lines.append(
        f"last complete session: {data.last_complete_session or 'unknown'}"
    )
    if data.next_formation is not None:
        days = (
            f", in {data.days_to_next_formation} days"
            if data.days_to_next_formation is not None
            else ""
        )
        lines.append(f"next formation: {data.next_formation}{days}")
    else:
        lines.append("next formation: unknown, calendar not yet fetched")
    if data.gaps:
        lines.append(f"gaps ({len(data.gaps)}): {', '.join(data.gaps)}")
    else:
        lines.append("gaps: none")
    lines.append("accrual state counts (all records):")
    if data.state_counts:
        for state, count in sorted(data.state_counts.items()):
            lines.append(f"  {state}: {count}")
    else:
        lines.append("  none, no accrual has run")
    lines.append("book membership:")
    if data.books:
        for width in sorted(data.books):
            names = ", ".join(data.books[width])
            lines.append(f"  width {width}: {names}")
    else:
        lines.append("  none, first formation has not run")
    size = data.benchmark_size
    lines.append(
        f"benchmark membership: {size if size is not None else 'not formed'}"
    )
    lines.append("chain pointers:")
    if data.pointers:
        for chain, asof in sorted(data.pointers.items()):
            lines.append(f"  {chain}: asof {asof}")
    else:
        lines.append("  none")
    lines.append("accrual ledger tail:")
    if data.accrual_tail:
        lines.extend(f"  {line}" for line in data.accrual_tail)
    else:
        lines.append("  empty")
    lines.append("recent fetches:")
    if data.recent_fetches:
        lines.extend(f"  {line}" for line in data.recent_fetches)
    else:
        lines.append("  none")
    return "\n".join(lines)


# -- verdict view -----------------------------------------------------


class VerdictViewError(RuntimeError):
    """Something other than the confidence sequence reached the render."""


_ALLOWED_VERDICT_LINES = (
    re.compile(r"^VERDICT VIEW$"),
    re.compile(
        r"^Confidence sequence only, per REGISTRATION\.md Section 12\.$"
    ),
    re.compile(r"^$"),
    re.compile(
        r"^width \d+ \((?:primary|secondary), alpha 0\.\d+ one-sided, "
        r"rho 0\.071641\)$"
    ),
    re.compile(r"^  observations: \d+$"),
    re.compile(r"^  mean -?[0-9.]+ bp/day, sigma [0-9.]+ bp$"),
    re.compile(r"^  bounds: lower -?[0-9.]+ bp/day, upper -?[0-9.]+ bp/day$"),
    re.compile(r"^  bounds: none, the series has not started$"),
    re.compile(r"^  bounds: not computable before 2 observations$"),
    re.compile(r"^  verdict: (?:SUCCESS|FUTILITY|CONTINUE)$"),
    re.compile(r"^  success bar: lower bound above 4\.07 bp/day$"),
    re.compile(r"^  futility bar: upper bound below 10\.0 bp/day$"),
    re.compile(
        r"^  registered projection at the recorded width-5 mean "
        r"27\.99 bp/day:$"
    ),
    re.compile(r"^    clears zero at day 2061, clears the hurdle at day 2852$"),
    re.compile(
        r"^  at the current mean: (?:success at day \d+"
        r"|success not reachable within 20000 days)$"
    ),
)


def _verdict_widths() -> tuple[int, ...]:
    return (
        THRESHOLDS.primary_width,
        *(
            w
            for w in THRESHOLDS.secondary_widths
            if w != THRESHOLDS.primary_width
        ),
    )


def _width_lines(width: int, record: Mapping[str, Any] | None) -> list[str]:
    from hfexperiment.verdict import alpha_for_width

    role = "primary" if width == THRESHOLDS.primary_width else "secondary"
    alpha = alpha_for_width(width)
    lines = [
        f"width {width} ({role}, alpha {alpha:g} one-sided, "
        f"rho {RHO_FROZEN:g})"
    ]
    t = int(record["t"]) if record is not None else 0
    lines.append(f"  observations: {t}")
    if record is None or t == 0:
        lines.append("  bounds: none, the series has not started")
        lines.append("  verdict: CONTINUE")
    elif record["lower_bp"] is None:
        lines.append("  bounds: not computable before 2 observations")
        lines.append("  verdict: CONTINUE")
    else:
        lines.append(
            f"  mean {record['mean_bp']:.2f} bp/day, "
            f"sigma {record['sigma_bp']:.2f} bp"
        )
        lines.append(
            f"  bounds: lower {record['lower_bp']:.2f} bp/day, "
            f"upper {record['upper_bp']:.2f} bp/day"
        )
        lines.append(f"  verdict: {str(record['state']).upper()}")
    lines.append(
        f"  success bar: lower bound above "
        f"{THRESHOLDS.cost_hurdle_bp_per_day:.2f} bp/day"
    )
    lines.append(
        f"  futility bar: upper bound below "
        f"{THRESHOLDS.futility_bp_per_day:.1f} bp/day"
    )
    lines.append(
        f"  registered projection at the recorded width-5 mean "
        f"{PROJECTION_MEAN_BP:.2f} bp/day:"
    )
    lines.append(
        f"    clears zero at day {PROJECTION_CLEAR_ZERO_DAY}, "
        f"clears the hurdle at day {PROJECTION_CLEAR_HURDLE_DAY}"
    )
    if record is not None and record.get("lower_bp") is not None:
        days = record.get("days_to_success_at_current_mean")
        if days is None:
            lines.append(
                "  at the current mean: success not reachable within "
                "20000 days"
            )
        else:
            lines.append(f"  at the current mean: success at day {days}")
    return lines


def verdict_view(records: Sequence[Mapping[str, Any]]) -> str:
    """The verdict surface. Confidence sequence outputs and nothing else.

    Consumes verdict ledger records alone. Every emitted line must
    match the allowlist of confidence-sequence shapes: the render
    itself fails on anything else, which is Section 12's structural
    separation enforced at the only exit.
    """
    latest: dict[int, Mapping[str, Any]] = {}
    for record in records:
        latest[int(record["width"])] = record
    lines = ["VERDICT VIEW",
             "Confidence sequence only, per REGISTRATION.md Section 12."]
    for width in _verdict_widths():
        lines.append("")
        lines.extend(_width_lines(width, latest.get(width)))
    for line in lines:
        if not any(p.match(line) for p in _ALLOWED_VERDICT_LINES):
            raise VerdictViewError(
                f"verdict view guard refused the line: {line!r}"
            )
    return "\n".join(lines)
