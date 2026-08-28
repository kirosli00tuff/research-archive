"""Structural guards. Each one fails a specific mutation of real source.

Ported by shape from NPLExperiment and InsiderExperiment. These are not style
checks: each exists because a predecessor system failed in exactly the way the
guard forbids, and scripts/mutations.py exercises them against real files.
"""

from __future__ import annotations

import ast
from pathlib import Path

from etf.config import CONFIG

SRC = Path(__file__).resolve().parents[1] / "src" / "etf"
CONFIG_FILE = SRC / "config.py"
BLINDNESS_FILE = SRC / "blindness.py"
PREPERIOD_FILE = SRC / "preperiod.py"

# Fields whose registered consumer lands in a later Stage A task. Each entry
# names the task. The test asserts the unread set EQUALS this set, so landing a
# consumer forces the entry off this list, and the list must be empty by the
# end of Stage A.3.
PENDING_ENFORCEMENT: frozenset[str] = frozenset(
    {
        "hyperliquid_info_url",  # A.1 Task 1, access verification
        "kraken_ohlc_url",  # A.1 Task 1, cross-check source
        "wayback_availability_url",  # A.1 Task 1, archive access
        "wayback_timemap_url",  # A.1 Task 4, archive capture density
        "perp_coin",  # A.1 Task 1, venue probes
        "horizon_primary_days",  # A.3 Task 5, verdict machinery
        "reversal_horizon_max_days",  # A.3 Task 5, named secondary
        "threshold_grid_usd",  # A.3 Task 5, named secondary
        "permutation_draws",  # A.3 Task 5, verdict machinery
        "alpha_adj",  # A.2 Task 4, power gate
        "rho_registered",  # A.2 Task 4, power gate
        "rho_undecayed",  # A.2 Task 4, power gate
        "rho_quartered",  # A.2 Task 4, power gate
        "power_simulations",  # A.2 Task 4, power gate
        "lag_min_trading_days",  # A.1 Task 3, lag measurement
        "retro_revision_sample_min",  # A.1 Task 4, retro revision rate
        "revision_settle_hours",  # A.1 Task 4, forward revision rate
        "min_outcome_coverage_candles",  # A.2 Task 3, sealed coverage
        "min_outcome_coverage_funding",  # A.2 Task 3, sealed coverage
        "interim_deadline",  # A.2 Task 4, projection
    }
)

# OHLCV keys as subscripts or .get() lookups, in every spelling. Candle price
# fields are readable nowhere outside the sealed raw writers, which never parse.
FORBIDDEN_PRICE_KEYS = {"o", "h", "l", "c", "v", "open", "high", "low", "close", "volume"}

FUNDING_RATE_KEY = "fundingRate"
FUNDING_RATE_ALLOWED_FILES = {"blindness.py"}

# The Stage B sealed reader is the only module that may ever join the
# allowlist, and it does not exist in Stage A. The equality pin below means
# widening this tuple is a caught mutation.
STAGE_B_OUTCOME_EXEMPT: tuple[str, ...] = ()


def source_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py"))


def referenced_names(path: Path) -> set[str]:
    """Every identifier the module actually reads, from the parse tree.

    Deliberately not a text search. A config key left behind in a comment while
    the code that read it was replaced by a literal is the exact shape of the
    defect this guard exists for, and a text search calls that enforcement. The
    InsiderExperiment mutation exercise proved the text version passes
    vacuously.
    """
    tree = ast.parse(path.read_text(encoding="utf-8"))
    out: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute):
            out.add(node.attr)
        elif isinstance(node, ast.Name):
            out.add(node.id)
        elif isinstance(node, ast.keyword) and node.arg:
            out.add(node.arg)
    return out


def _string_key_lookups(tree: ast.AST) -> set[str]:
    """String keys read via subscript or .get() anywhere in a module."""
    keys: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript):
            sl = node.slice
            if isinstance(sl, ast.Constant) and isinstance(sl.value, str):
                keys.add(sl.value)
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        ):
            keys.add(node.args[0].value)
    return keys


def test_every_config_field_has_an_enforcement_site_or_a_named_pending_task() -> None:
    names = set(CONFIG.field_names())
    assert names, "the config declares no fields"
    read_anywhere: set[str] = set()
    for path in source_files():
        if path != CONFIG_FILE:
            read_anywhere |= referenced_names(path)
    unread = names - read_anywhere
    assert unread == set(PENDING_ENFORCEMENT), (
        f"config enforcement drifted. Unread fields not on the pending list: "
        f"{sorted(unread - set(PENDING_ENFORCEMENT))}. Pending entries now read "
        f"(remove them): {sorted(set(PENDING_ENFORCEMENT) - unread)}. "
        f"A key enforced nowhere is decoration."
    )


def test_no_module_reads_a_priced_candle_field_anywhere() -> None:
    """The blindness rule, repo-wide: OHLCV keys are read by no code path."""
    offenders: list[str] = []
    for path in source_files():
        if path.relative_to(SRC).as_posix() in STAGE_B_OUTCOME_EXEMPT:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        priced = _string_key_lookups(tree) & FORBIDDEN_PRICE_KEYS
        if priced:
            offenders.append(f"{path.relative_to(SRC)} reads {sorted(priced)}")
    assert not offenders, f"outcome blindness violated: {offenders}"


def test_funding_rate_is_read_only_inside_the_gated_reader() -> None:
    offenders: list[str] = []
    for path in source_files():
        if path.name in FUNDING_RATE_ALLOWED_FILES:
            continue
        if path.relative_to(SRC).as_posix() in STAGE_B_OUTCOME_EXEMPT:
            continue
        if FUNDING_RATE_KEY in path.read_text(encoding="utf-8"):
            offenders.append(str(path.relative_to(SRC)))
    assert not offenders, (
        f"modules naming {FUNDING_RATE_KEY} outside the gated blindness reader: {offenders}"
    )


def test_the_stage_b_exemption_is_empty_in_stage_a() -> None:
    """Stage A has no sealed reader at all. Widening this tuple is a caught mutation."""
    assert STAGE_B_OUTCOME_EXEMPT == ()


def test_the_funding_reader_gates_on_the_pre_period_pin_not_on_a_literal() -> None:
    """The fifth guard, structurally: blindness.py must call the pin, not inline a date.

    The mutation this catches: replacing `gate_pre_period(...)` with a bare
    `float(row["fundingRate"])`, or with a literal comparison against an
    inlined timestamp. Either one reads a post-2025-05-01 funding rate through
    a reader the registration says is gated.
    """
    tree = ast.parse(BLINDNESS_FILE.read_text(encoding="utf-8"))
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "gate_pre_period" in called, (
        "blindness.funding_rows must route every rate through etf.preperiod.gate_pre_period; "
        "an inlined comparison is not the registered enforcement site"
    )
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "etf.preperiod"
        for alias in node.names
    }
    assert "gate_pre_period" in imported


def test_the_pre_period_boundary_is_read_from_config_in_exactly_one_module() -> None:
    """No second module may inline the carve-out boundary and drift from it."""
    readers: list[str] = []
    for path in source_files():
        if path == CONFIG_FILE:
            continue
        if "pre_period_end_ms" in referenced_names(path):
            readers.append(path.name)
    assert readers == ["preperiod.py"], (
        f"the carve-out boundary is read outside its enforcement site: {readers}"
    )


def test_no_module_hardcodes_the_carve_out_timestamp() -> None:
    """A literal 1746057600000 anywhere but config.py is a second, driftable boundary."""
    literal = str(CONFIG.pre_period_end_ms)
    offenders = [
        path.name
        for path in source_files()
        if path != CONFIG_FILE and literal in path.read_text(encoding="utf-8")
    ]
    assert not offenders, f"the carve-out boundary is hardcoded in {offenders}"
