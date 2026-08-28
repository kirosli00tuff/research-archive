"""Structural guards. Each one fails a specific mutation of real source.

Ported by shape from NPLExperiment and InsiderExperiment. These are not style
checks: each exists because a predecessor system failed in exactly the way the
guard forbids, and scripts/mutations.py exercises them against real files.
"""

from __future__ import annotations

import ast
from pathlib import Path

from etf.config import CONFIG

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src" / "etf"
SCRIPTS = ROOT / "scripts"
CONFIG_FILE = SRC / "config.py"
BLINDNESS_FILE = SRC / "blindness.py"
PREPERIOD_FILE = SRC / "preperiod.py"

# Fields whose registered consumer lands in a later Stage A task. Each entry
# names the task. The test asserts the unread set EQUALS this set, so landing a
# consumer forces the entry off this list, and the list must be empty by the
# end of Stage A.3.
PENDING_ENFORCEMENT: frozenset[str] = frozenset({})

# OHLCV keys as subscripts or .get() lookups, in every spelling. Candle price
# fields are readable nowhere outside the sealed raw writers, which never parse.
FORBIDDEN_PRICE_KEYS = {"o", "h", "l", "c", "v", "open", "high", "low", "close", "volume"}

FUNDING_RATE_KEY = "fundingRate"
FUNDING_RATE_ALLOWED_FILES = {"blindness.py"}

# The Section 9 pre-period carve-out has exactly one address. This is the only
# file in the repository permitted to read a close, and only strictly before
# 2025-05-01, enforced inside it by etf.preperiod.require_pre_period.
PRE_PERIOD_PRICE_ALLOWED_FILES = {"preperiod_prices.py"}

# The Stage B sealed reader is the only module that may ever join the
# allowlist, and it does not exist in Stage A. The equality pin below means
# widening this tuple is a caught mutation.
STAGE_B_OUTCOME_EXEMPT: tuple[str, ...] = ()


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def source_files() -> list[Path]:
    """Every module the blindness and enforcement guards scan.

    Scripts are scanned too. They are real enforcement sites in this repository
    - the census, the power gate and the access probes live there - and a
    blindness rule that stops at the package boundary would let a script read a
    close with nothing failing.
    """
    return sorted([*SRC.rglob("*.py"), *SCRIPTS.rglob("*.py")])


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
        if _rel(path) in STAGE_B_OUTCOME_EXEMPT:
            continue
        if path.name in PRE_PERIOD_PRICE_ALLOWED_FILES:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        priced = _string_key_lookups(tree) & FORBIDDEN_PRICE_KEYS
        if priced:
            offenders.append(f"{_rel(path)} reads {sorted(priced)}")
    assert not offenders, f"outcome blindness violated: {offenders}"


def test_funding_rate_is_read_only_inside_the_gated_reader() -> None:
    offenders: list[str] = []
    for path in source_files():
        if path.name in FUNDING_RATE_ALLOWED_FILES:
            continue
        if _rel(path) in STAGE_B_OUTCOME_EXEMPT:
            continue
        if FUNDING_RATE_KEY in path.read_text(encoding="utf-8"):
            offenders.append(_rel(path))
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
    assert sorted(readers) == ["preperiod.py", "preperiod_inputs.py"], (
        f"the carve-out boundary is read outside its enforcement site: {sorted(readers)}. "
        "Only the pin itself and the single A.2 input script that bounds its own fetch "
        "window may name it."
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


def test_the_pre_period_price_reader_is_exactly_one_file() -> None:
    """Widening the carve-out's allowlist is a caught mutation."""
    assert sorted(PRE_PERIOD_PRICE_ALLOWED_FILES) == ["preperiod_prices.py"]
    assert (SRC / "preperiod_prices.py").exists()


def test_the_pre_period_reader_reads_only_t_T_and_c() -> None:
    tree = ast.parse((SRC / "preperiod_prices.py").read_text(encoding="utf-8"))
    keys = _string_key_lookups(tree)
    assert keys <= {"t", "T", "c"}, f"the carve-out reader reads more than t, T, c: {sorted(keys)}"
    assert "c" in keys, "the carve-out reader must actually read a close, or it is decoration"


def test_the_pre_period_reader_gates_every_row_through_the_pin() -> None:
    """The mutation this catches: dropping require_pre_period, or inlining a date."""
    tree = ast.parse((SRC / "preperiod_prices.py").read_text(encoding="utf-8"))
    called = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    assert "require_pre_period" in called
    imported = {
        alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "etf.preperiod"
        for alias in node.names
    }
    assert imported == {"require_pre_period"}


def test_the_pre_period_reader_cannot_open_a_socket_or_choose_its_own_window() -> None:
    """It parses what it is handed. A reader that fetches could widen its own window."""
    source = (SRC / "preperiod_prices.py").read_text(encoding="utf-8")
    tree = ast.parse(source)
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            modules.add(node.module)
        elif isinstance(node, ast.Import):
            modules |= {a.name for a in node.names}
    forbidden = {"etf.http", "urllib", "urllib.request", "http.client", "socket"}
    assert not (modules & forbidden), f"the carve-out reader imports a network module: {modules}"


# The carve-out reader has exactly one caller, and it is a script that fetches a
# window wholly inside the carve-out and hands it over. A second caller could
# hand it a window that straddles the boundary.
PRE_PERIOD_READER_CALLERS = {"preperiod_inputs.py"}


def test_the_carve_out_reader_has_exactly_one_caller() -> None:
    callers = sorted(
        path.name
        for path in source_files()
        if path.name not in PRE_PERIOD_PRICE_ALLOWED_FILES
        and path != CONFIG_FILE
        and "pre_period_closes" in path.read_text(encoding="utf-8")
    )
    assert callers == sorted(PRE_PERIOD_READER_CALLERS), (
        f"the carve-out reader's caller set changed: {callers}"
    )


def test_no_module_under_src_calls_the_carve_out_reader() -> None:
    """The package itself never reads a close. Only the one A.2 input script does."""
    offenders = [
        p.name
        for p in SRC.rglob("*.py")
        if p.name not in PRE_PERIOD_PRICE_ALLOWED_FILES
        and "pre_period_closes" in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"the carve-out reader is called from the package: {offenders}"


def test_the_pending_enforcement_list_is_empty_at_the_close_of_stage_a() -> None:
    """Every registered config field has a real enforcement site. No decoration."""
    assert not PENDING_ENFORCEMENT
