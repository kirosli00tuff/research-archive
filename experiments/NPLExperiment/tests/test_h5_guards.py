"""Structural guards for register entry H5. Each fails a specific mutation.

The repo-wide guards in tests/test_guards.py already cover every module added
under src/npl/h5 — no OHLCV key, no `fundingRate` outside the gated reader,
no reach into the spent Stage B surface. These are the H5-specific ones: the
write containment, the funding-value abstention, the candle abstention, and
the equality pins on the registered field names.
"""

from __future__ import annotations

import ast
from pathlib import Path

from npl.h5 import basis as h5basis
from npl.h5 import calendar as h5cal
from npl.h5 import outcome as h5out
from npl.paths import DATA, H5_DIR

SRC = Path(__file__).resolve().parents[1] / "src" / "npl"
H5 = SRC / "h5"

STORE_MODULE = "stores.py"
WRITE_ATTRS = {"write_text", "write_bytes", "mkdir", "unlink", "rename", "replace"}
WRITE_MODES = {"w", "a", "x", "w+", "a+", "x+", "wb", "ab", "xb"}


def h5_files() -> list[Path]:
    return sorted(p for p in H5.rglob("*.py"))


def _tree(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"))


def test_the_h5_package_has_modules_to_guard() -> None:
    """A guard over an empty set passes vacuously. This one refuses to."""
    assert len(h5_files()) >= 8


def test_only_the_store_module_constructs_an_append_only_ledger() -> None:
    """Every H5 write goes through the containment gate, by construction."""
    offenders: list[str] = []
    for path in h5_files():
        if path.name == STORE_MODULE:
            continue
        for node in ast.walk(_tree(path)):
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and node.func.id == "AppendOnlyLedger"
            ):
                offenders.append(path.name)
    assert offenders == [], (
        f"H5 modules constructing a ledger outside the containment gate: {offenders}. "
        f"Every H5 write goes through npl.h5.stores.h5_store."
    )


def test_no_h5_module_writes_a_file_outside_the_store_module() -> None:
    """No direct write_text, no open() in a write mode, anywhere else in H5."""
    offenders: list[str] = []
    for path in h5_files():
        if path.name == STORE_MODULE:
            continue
        for node in ast.walk(_tree(path)):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
                if node.func.attr in WRITE_ATTRS:
                    offenders.append(f"{path.name}:{node.func.attr}")
                if node.func.attr == "open":
                    for arg in list(node.args) + [k.value for k in node.keywords]:
                        if isinstance(arg, ast.Constant) and arg.value in WRITE_MODES:
                            offenders.append(f"{path.name}:open({arg.value!r})")
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Name)
                and (node.func.id == "open")
            ):
                for arg in node.args[1:]:
                    if isinstance(arg, ast.Constant) and arg.value in WRITE_MODES:
                        offenders.append(f"{path.name}:open({arg.value!r})")
    assert offenders == [], f"H5 modules writing outside the containment gate: {offenders}"


def test_the_h5_write_root_is_data_h5_and_nothing_else() -> None:
    assert H5_DIR == DATA / "h5"
    assert H5_DIR.name == "h5" and H5_DIR.parent == DATA


def test_no_h5_module_reads_a_funding_value() -> None:
    """Service, never a rate: the `funding` key is tested for presence only.

    A subscript or .get() on the funding key would read the number. The
    presence test (`"funding" in ctx`) is a Compare node and is admitted.
    """
    offenders: list[str] = []
    for path in h5_files():
        for node in ast.walk(_tree(path)):
            if (
                isinstance(node, ast.Subscript)
                and isinstance(node.slice, ast.Constant)
                and node.slice.value in {"funding", "fundingRate", "premium"}
            ):
                offenders.append(f"{path.name}[{node.slice.value!r}]")
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and node.args[0].value in {"funding", "fundingRate"}
            ):
                offenders.append(f"{path.name}.get({node.args[0].value!r})")
    assert offenders == [], (
        f"H5 modules reading a funding value: {offenders}. H5 records funding "
        f"SERVICE and never a rate."
    )


def test_no_h5_module_requests_a_candle() -> None:
    """Rule 7 forbids a candle price field, so H5 never asks for a candle."""
    offenders: list[str] = []
    forbidden = {"EP_CANDLE_SNAPSHOT", "candle_snapshot_body", "candle_times", "candles"}
    for path in h5_files():
        for node in ast.walk(_tree(path)):
            name = None
            if isinstance(node, ast.Name):
                name = node.id
            elif isinstance(node, ast.Attribute):
                name = node.attr
            if name in forbidden:
                offenders.append(f"{path.name}:{name}")
    assert offenders == [], (
        f"H5 modules reaching for a candle: {offenders}. A candle read blind is not a "
        f"price, and a candle read with a price violates standing rule 7."
    )


def test_the_registered_reference_fields_are_pinned_by_equality() -> None:
    """Widening the reference list, or admitting a book field, is a mutation."""
    assert h5basis.MARK_FIELD == "markPx"
    assert h5basis.REFERENCE_FIELDS == ("oraclePx", "indexPx")
    assert h5basis.NON_REFERENCE_FIELDS == ("midPx", "prevDayPx", "impactPxs")


def test_the_registered_session_tags_are_pinned_by_equality() -> None:
    assert h5cal.SESSION_TAGS == ("regular", "extended", "closed_weekday", "weekend")
    assert h5cal.SATURDAY == 5
    assert sorted(h5cal.COVERED_YEARS) == [2024, 2025, 2026, 2027]


def test_the_registered_terminal_states_are_exactly_the_operators_three() -> None:
    assert h5out.TERMINAL_STATES == ("VIABLE", "INDETERMINATE", "CLOSED")
    assert h5out.STATE_PENDING not in h5out.TERMINAL_STATES
    assert h5out.REGISTERED_SERIES_KINDS == ("registered_basis", "secondary_deviation")


def test_no_h5_module_imports_the_stage_b_package() -> None:
    """Belt and braces over the repo-wide pin: the spent read is unreachable."""
    offenders: list[str] = []
    for path in h5_files():
        for node in ast.walk(_tree(path)):
            names: list[str] = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            elif isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            if any(name.startswith("npl.stageb") for name in names):
                offenders.append(path.name)
    assert offenders == []


def test_the_deviation_reader_has_exactly_one_importer() -> None:
    """`deviation_rows` reads the venue premium index; only H5's gated
    retrospective path may reach it, and the pin is equality, not a subset."""
    importers: list[str] = []
    for path in sorted(p for p in SRC.rglob("*.py")):
        for node in ast.walk(_tree(path)):
            names: list[str] = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names = [alias.name for alias in node.names]
            if "deviation_rows" in names:
                importers.append(path.relative_to(SRC).as_posix())
    assert importers == ["h5/retro.py"], (
        f"the deviation reader's importers drifted from the registered single "
        f"gated path: {importers}"
    )


def test_the_retrospective_gate_runs_before_the_first_request() -> None:
    """`fetch_series` calls require_ungated before anything else in its body.

    The mutation target: deleting the gate call. A structural pin, because a
    gate the caller may forget is not a gate.
    """
    tree = _tree(H5 / "retro.py")
    func = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "fetch_series"
    )
    first = func.body[1] if len(func.body) > 1 else func.body[0]
    assert isinstance(first, ast.Expr), "fetch_series does not open with a bare call"
    call = first.value
    assert isinstance(call, ast.Call) and isinstance(call.func, ast.Name)
    assert call.func.id == "require_ungated", (
        "fetch_series no longer opens with the cohort gate; a quarantined coin "
        "could reach the network"
    )
