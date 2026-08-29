"""The structural guards. Every one walks the parse tree, never the text.

A text grep is defeated by a rename, a line break, or a comment. These guards
compile each module and inspect its AST, so a read of a forbidden field is
caught wherever it hides.
"""

from __future__ import annotations

import ast
import dataclasses
from pathlib import Path

import pytest

from orb.config import CONFIG, Config
from orb.seal import PRICED_BAR_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src" / "orb"

SEALED_MODULES: frozenset[str] = frozenset({"seal.py", "comparator.py"})
"""The only modules permitted to touch a priced bar field.

``seal.py`` stores raw bytes and parses nothing. ``comparator.py`` is the sealed
comparator: it reads price and volume from two vendors, emits aggregate
mismatch counts and rates, and returns no bar value to any caller.
"""

SAFE_ATTRIBUTE_RECEIVERS: frozenset[str] = frozenset({"os"})
"""Receivers whose attribute of a colliding name is provably not a bar.

``os.close(fd)`` closes a file descriptor. ``close`` is in the forbidden field
list because it is a bar field in every vendor dialect, and the collision is
resolved here by naming the one receiver that is a standard-library module
rather than by widening the field list. A bar is never bound to the name ``os``.
"""


def _module_paths() -> list[Path]:
    return sorted(p for p in SRC_ROOT.rglob("*.py"))


def _parse(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


# --------------------------------------------------------------------------
# Guard 5 — the priced-bar blindness pin
# --------------------------------------------------------------------------


@dataclasses.dataclass(frozen=True, slots=True)
class BarFieldRead:
    module: str
    lineno: int
    field: str
    form: str

    def __str__(self) -> str:
        return f"{self.module}:{self.lineno} reads {self.field!r} via {self.form}"


def _bar_field_reads(path: Path) -> list[BarFieldRead]:
    """Every read of a priced bar field in ``path``, by parse tree."""
    tree = _parse(path)
    found: list[BarFieldRead] = []
    module = path.name

    for node in ast.walk(tree):
        # bar.close / row.volume
        if isinstance(node, ast.Attribute) and node.attr in PRICED_BAR_FIELDS:
            receiver = node.value
            if (
                isinstance(receiver, ast.Name)
                and receiver.id in SAFE_ATTRIBUTE_RECEIVERS
            ):
                continue
            found.append(BarFieldRead(module, node.lineno, node.attr, "attribute"))

        # bar["close"] / row['o']
        elif isinstance(node, ast.Subscript):
            key = node.slice
            if (
                isinstance(key, ast.Constant)
                and isinstance(key.value, str)
                and key.value in PRICED_BAR_FIELDS
            ):
                found.append(BarFieldRead(module, node.lineno, key.value, "subscript"))

        # bar.get("close") / row.get('v', 0)
        elif isinstance(node, ast.Call):
            func = node.func
            if (
                isinstance(func, ast.Attribute)
                and func.attr in {"get", "pop", "setdefault"}
                and node.args
            ):
                first = node.args[0]
                if (
                    isinstance(first, ast.Constant)
                    and isinstance(first.value, str)
                    and first.value in PRICED_BAR_FIELDS
                ):
                    found.append(
                        BarFieldRead(
                            module, node.lineno, first.value, f".{func.attr}()"
                        )
                    )

    return found


@pytest.mark.guard
def test_no_module_reads_a_priced_bar_field_anywhere() -> None:
    """Guard 5. Outside a sealed writer, no priced bar field is read. Ever.

    Walks the parse tree of every module under ``src/orb``. A read of open,
    high, low, close, volume, vwap, trade count, bid or ask — under any
    spelling, as an attribute, a subscript or a ``.get`` — fails here.
    """
    violations: list[BarFieldRead] = []
    for path in _module_paths():
        if path.name in SEALED_MODULES:
            continue
        violations.extend(_bar_field_reads(path))

    assert not violations, (
        "priced bar fields read outside a sealed writer, n = "
        f"{len(violations)}:\n  " + "\n  ".join(str(v) for v in violations)
    )


@pytest.mark.guard
def test_the_blindness_guard_actually_binds() -> None:
    """A guard that cannot fire is decoration. This proves it fires.

    The InsiderExperiment mutation lesson: a boundary fixture comfortably
    inside its boundary lets a moved threshold pass unnoticed. The same applies
    to a structural guard — one that has never been shown to catch anything is
    an assertion about nothing.
    """
    source = (
        "def leak(bar):\n"
        "    a = bar.close\n"
        "    b = bar['volume']\n"
        "    c = bar.get('vwap')\n"
        "    return a, b, c\n"
    )
    tmp = SRC_ROOT.parent / "_guard_probe.py"
    tmp.write_text(source, encoding="utf-8")
    try:
        found = _bar_field_reads(tmp)
    finally:
        tmp.unlink()

    fields = sorted(f.field for f in found)
    assert fields == ["close", "volume", "vwap"], fields
    forms = sorted(f.form for f in found)
    assert forms == [".get()", "attribute", "subscript"], forms


@pytest.mark.guard
def test_readable_and_forbidden_field_lists_do_not_overlap() -> None:
    """The two blindness lists are disjoint. A field is readable or it is not."""
    from orb.seal import READABLE_FIELDS

    overlap = READABLE_FIELDS & PRICED_BAR_FIELDS
    assert not overlap, f"a field cannot be both readable and sealed: {overlap}"


# --------------------------------------------------------------------------
# Guard 2 — parse-tree config enforcement
# --------------------------------------------------------------------------

PENDING_ENFORCEMENT: dict[str, str] = {
    # field name -> the task that will read it
    "in_sample_start": "A.2 TASK 1 — session calendar",
    "in_sample_end": "A.2 TASK 1 — session calendar",
    "holdout_start": "A.2 TASK 1 — session calendar",
    "holdout_end": "A.2 TASK 1 — session calendar",
    "opening_range_minutes": "A.2 TASK 3 — signal built dark",
    "selection_width": "A.2 TASK 3 — universe built dark",
    "relvol_lookback_sessions": "A.2 TASK 3 — universe built dark",
    "min_session_open_usd": "A.2 TASK 3 — universe built dark",
    "min_avg_volume_shares": "A.2 TASK 3 — universe built dark",
    "min_atr_usd": "A.2 TASK 3 — universe built dark",
    "max_borrow_rate_annual": "A.2 TASK 3 — universe built dark",
    "entry_offset_fraction": "A.2 TASK 3 — signal built dark",
    "risk_fraction_per_trade": "A.2 TASK 3 — sizing built dark",
    "max_concurrent_positions": "A.2 TASK 3 — sizing built dark",
    "max_gross_notional_multiple": "A.2 TASK 3 — sizing built dark",
    "commission_per_share_usd": "A.2 TASK 2 — cost model",
    "commission_order_minimum_usd": "A.2 TASK 2 — cost model",
    "finra_taf_per_share_sold_usd": "A.2 TASK 2 — cost model",
    "entry_slippage_usd": "A.2 TASK 2 — cost model",
    "stop_slippage_usd": "A.2 TASK 2 — cost model",
    "close_slippage_usd": "A.2 TASK 2 — cost model",
    "n_co_primaries": "A.2 TASK 4 — power gate",
    "trial_count": "A.2 TASK 4 — power gate",
    "deflated_sharpe_bar": "A.2 TASK 3 — verdict built dark",
    "holdout_per_trade_t_gate": "A.2 TASK 3 — verdict built dark",
    "max_single_year_pnl_share": "A.2 TASK 3 — verdict built dark",
    "min_positive_holdout_years": "A.2 TASK 3 — verdict built dark",
    "registered_sharpe_assumption": "A.2 TASK 4 — power gate",
    "published_sharpe_assumption": "A.2 TASK 4 — power gate",
    "quartered_sharpe_assumption": "A.2 TASK 4 — power gate",
    "trading_days_per_year": "A.2 TASK 4 — power gate",
    "target_power": "A.0 TASK 4 — Section 0 fire function",
    "blocked_power_floor": "A.0 TASK 4 — Section 0 fire function",
    "revision_pass_max_share": "A.0 TASK 4 — Section 0 fire function",
    "revision_partial_max_share": "A.0 TASK 4 — Section 0 fire function",
    "agreement_pass_min_share": "A.0 TASK 4 — Section 0 fire function",
    "agreement_partial_min_share": "A.0 TASK 4 — Section 0 fire function",
    "delisted_pass_min_count": "A.0 TASK 4 — Section 0 fire function",
    "delisted_partial_min_count": "A.0 TASK 4 — Section 0 fire function",
    "revision_repull_wait_days": "A.1 TASK 3 — bar revision rate",
    "probe_sessions": "A.1 TASK 3 — bar revision rate",
    "probe_tickers": "A.1 TASK 3 — bar revision rate",
    "probe_min_age_days": "A.1 TASK 3 — bar revision rate",
    "integer_shares_only": "A.2 TASK 3 — sizing built dark",
}
"""Config fields not yet read outside ``config.py``, each with its task named.

A field sits here only while the task that will read it is still ahead. The
guard below fails if a field is neither read nor listed, and fails again if a
listed field has since been read — a stale entry hides the next real gap.
"""


def _config_field_reads() -> dict[str, list[str]]:
    """Every ``CONFIG.<field>`` read outside ``config.py``, by parse tree."""
    fields = {f.name for f in dataclasses.fields(Config)}
    reads: dict[str, list[str]] = {}
    for path in _module_paths():
        if path.name == "config.py":
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Attribute) and node.attr in fields:
                reads.setdefault(node.attr, []).append(f"{path.name}:{node.lineno}")
    return reads


@pytest.mark.guard
def test_every_config_field_is_read_or_pending_with_its_task_named() -> None:
    """Guard 2. A registered constant nobody reads is an unimplemented intention."""
    declared = {f.name for f in dataclasses.fields(Config)}
    read = set(_config_field_reads())
    pending = set(PENDING_ENFORCEMENT)

    unknown_pending = pending - declared
    assert not unknown_pending, (
        f"PENDING_ENFORCEMENT names fields that do not exist: {sorted(unknown_pending)}"
    )

    unaccounted = declared - read - pending
    assert not unaccounted, (
        f"config fields neither read outside config.py nor pending, n = "
        f"{len(unaccounted)}: {sorted(unaccounted)}"
    )


@pytest.mark.guard
def test_pending_enforcement_has_no_stale_entries() -> None:
    """A field that has since been read must leave the pending list."""
    read = set(_config_field_reads())
    stale = sorted(set(PENDING_ENFORCEMENT) & read)
    assert not stale, (
        "these fields are now read outside config.py and must be removed from "
        f"PENDING_ENFORCEMENT, n = {len(stale)}: {stale}"
    )


@pytest.mark.guard
def test_pending_enforcement_entries_name_a_task() -> None:
    """A pending field with no named task is a gap wearing a label."""
    unnamed = sorted(k for k, v in PENDING_ENFORCEMENT.items() if "TASK" not in v)
    assert not unnamed, f"pending fields with no task named: {unnamed}"


# --------------------------------------------------------------------------
# Guard 6 — the boundary literal lives in exactly one place
# --------------------------------------------------------------------------


@pytest.mark.guard
def test_no_module_outside_config_hardcodes_the_pre_period_boundary() -> None:
    """The carve-out boundary is read from config, never re-typed."""
    literal = CONFIG.pre_period_end_ms
    offenders: list[str] = []
    for path in _module_paths():
        if path.name == "config.py":
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Constant) and node.value == literal:
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, (
        f"pre-period boundary literal {literal} hardcoded outside config.py: "
        f"{offenders}"
    )


@pytest.mark.guard
def test_only_preperiod_reads_the_boundary_from_config() -> None:
    """One enforcement site, so there is one place to audit."""
    readers = _config_field_reads().get("pre_period_end_ms", [])
    modules = {r.split(":")[0] for r in readers}
    assert modules <= {"preperiod.py"}, (
        f"pre_period_end_ms must be read only by preperiod.py, found: {modules}"
    )


# --------------------------------------------------------------------------
# Guard 7 — no fixed-offset Eastern anywhere
# --------------------------------------------------------------------------


@pytest.mark.guard
def test_no_module_builds_eastern_from_a_fixed_offset() -> None:
    """Guard 7. ``timezone(timedelta(hours=-5))`` mis-slices a third of the sample."""
    offenders: list[str] = []
    for path in _module_paths():
        for node in ast.walk(_parse(path)):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = (
                func.attr
                if isinstance(func, ast.Attribute)
                else func.id
                if isinstance(func, ast.Name)
                else ""
            )
            if name == "timezone" and node.args:
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, (
        "a fixed UTC offset was used to build a zone; the Eastern anchor must "
        f"be the DST-aware ZoneInfo: {offenders}"
    )


@pytest.mark.guard
def test_exactly_one_module_names_the_eastern_zone() -> None:
    """The Eastern zone is constructed once, in sessionclock.py."""
    offenders: list[str] = []
    for path in _module_paths():
        for node in ast.walk(_parse(path)):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value == "America/New_York"
                and path.name != "sessionclock.py"
            ):
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, (
        f"America/New_York is constructed outside sessionclock.py: {offenders}"
    )
