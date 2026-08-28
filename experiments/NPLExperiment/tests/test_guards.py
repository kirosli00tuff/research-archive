"""Structural guards. Each one fails a specific mutation of real source.

Ported by shape from InsiderExperiment. These are not style checks: each
exists because a predecessor system failed in exactly the way the guard
forbids, and scripts/mutations.py exercises them against real files.
"""

from __future__ import annotations

import ast
from pathlib import Path

from npl.config import CONFIG
from npl.stageb import STAGE_B_OUTCOME_EXEMPT

SRC = Path(__file__).resolve().parents[1] / "src" / "npl"
CONFIG_FILE = SRC / "config.py"
BLINDNESS_FILE = SRC / "blindness.py"

# Fields whose registered consumer lands in a later Stage A task. Each entry
# names the task. The test asserts the unread set EQUALS this set, so landing
# a consumer forces the entry off this list, and the list must be empty by the
# end of Stage A.3.
PENDING_ENFORCEMENT: frozenset[str] = frozenset()

# OHLCV keys, and the l2Book level keys, as subscripts or .get() lookups.
# The l2Book touch state (px, sz) is a registered descriptive cost input
# (Section 5) and is readable ONLY in spread.py; candle price fields are
# readable nowhere outside the sealed raw writers, which never parse at all.
FORBIDDEN_PRICE_KEYS = {"o", "h", "l", "c", "v", "open", "high", "low", "close", "volume"}
L2_KEYS = {"px", "sz"}
L2_ALLOWED_FILES = {"spread.py"}

FUNDING_RATE_KEY = "fundingRate"
FUNDING_RATE_ALLOWED_FILES = {"blindness.py"}


def source_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py"))


def referenced_names(path: Path) -> set[str]:
    """Every identifier the module actually reads, from the parse tree.

    Deliberately not a text search. A config key left behind in a comment
    while the code that read it was replaced by a literal is the exact shape
    of the defect this guard exists for, and a text search calls that
    enforcement. The InsiderExperiment mutation exercise proved the text
    version passes vacuously.
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


def test_no_module_reads_a_priced_candle_field_anywhere() -> None:
    """The blindness rule, repo-wide: OHLCV keys are read by no code path.

    Amendment 3: the allowlist gains exactly one module, the Stage B sealed
    reader; the length-one pin below holds it there.
    """
    offenders: list[str] = []
    for path in source_files():
        if path.relative_to(SRC).as_posix() in STAGE_B_OUTCOME_EXEMPT:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"))
        keys = _string_key_lookups(tree)
        priced = keys & FORBIDDEN_PRICE_KEYS
        if priced:
            offenders.append(f"{path.relative_to(SRC)} reads {sorted(priced)}")
        l2 = keys & L2_KEYS
        if l2 and path.name not in L2_ALLOWED_FILES:
            offenders.append(f"{path.relative_to(SRC)} reads l2 keys {sorted(l2)}")
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


def test_the_stage_b_exemption_is_exactly_one_module() -> None:
    """Amendment 3: the blindness allowlist gains exactly one module, ever.

    The equality pin (not just the length) means widening the allowlist to a
    second module, or swapping the registered one, is a caught mutation.
    """
    assert STAGE_B_OUTCOME_EXEMPT == ("stageb/reader.py",)


def test_only_the_stage_b_cli_imports_the_reader() -> None:
    """Amendment 3: npl.stageb.reader has exactly one importer, the Stage B CLI."""
    importers: list[str] = []
    for path in source_files():
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.ImportFrom) and node.module:
                names.append(node.module)
            elif isinstance(node, ast.Import):
                names.extend(alias.name for alias in node.names)
            if any("stageb.reader" in name for name in names):
                importers.append(path.relative_to(SRC).as_posix())
                break
    assert importers == ["stageb/cli.py"], (
        f"the sealed reader's importers drifted from the registered single CLI: {importers}"
    )


def test_the_gated_reader_compares_time_against_the_entry_before_reading_a_rate() -> None:
    """The gate is a comparison in the parse tree, not a comment.

    funding_rows must contain a Compare node, and every fundingRate subscript
    must sit under a conditional. This is the pin a delete-the-gate mutation
    trips.
    """
    tree = ast.parse(BLINDNESS_FILE.read_text(encoding="utf-8"))
    func = next(
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.FunctionDef) and node.name == "funding_rows"
    )
    compares = [n for n in ast.walk(func) if isinstance(n, ast.Compare)]
    assert compares, "funding_rows contains no comparison: the blindness gate is gone"
    rate_reads_under_if = 0
    for node in ast.walk(func):
        if isinstance(node, ast.If):
            for sub in ast.walk(node):
                if (
                    isinstance(sub, ast.Subscript)
                    and isinstance(sub.slice, ast.Constant)
                    and sub.slice.value == FUNDING_RATE_KEY
                ):
                    rate_reads_under_if += 1
    total_rate_reads = sum(
        1
        for sub in ast.walk(func)
        if isinstance(sub, ast.Subscript)
        and isinstance(sub.slice, ast.Constant)
        and sub.slice.value == FUNDING_RATE_KEY
    )
    assert total_rate_reads >= 1, "funding_rows never reads a rate; the reader is hollow"
    assert rate_reads_under_if == total_rate_reads, (
        "a fundingRate read escaped the entry-time conditional: the gate does not cover it"
    )
