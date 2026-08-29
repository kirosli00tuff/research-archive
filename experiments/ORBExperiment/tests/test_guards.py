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
from orb.fields import PRICED_BAR_FIELDS

REPO_ROOT = Path(__file__).resolve().parent.parent
SRC_ROOT = REPO_ROOT / "src" / "orb"

FIELD_REGISTRY_MODULE: str = "fields.py"
"""The declaration site of the two field lists. Names only; it reads nothing."""

LATCHED_MODULES: frozenset[str] = frozenset(
    {"bars.py", "universe.py", "signal.py", "verdict.py"}
)
"""The dark strategy modules. They name priced fields; nothing in Stage A reaches them.

These are **Stage C code, written in Stage A**. The blindness pin cannot apply —
an opening-range rule is a statement about highs and lows — so a **stronger**
guarantee replaces it: `test_no_stage_a_module_imports_a_latched_module` walks
every import in the repository and requires that **no module outside this set
imports one of them**. Nothing on the Stage A collection path can reach the
strategy, by construction rather than by discipline. At runtime a second pin
holds: every entry point refuses a bar carrying `SEALED_VENDOR` provenance until
the Stage C latch is written.
"""

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


FORM_SPECIFICITY: dict[str, int] = {
    "attribute": 3,
    "subscript": 2,
    ".get()": 2,
    "string constant": 1,
}
"""A constant subscript is also a string constant. Keep the specific form."""


def _bar_field_reads(path: Path) -> list[BarFieldRead]:
    """Every read of a priced bar field in ``path``, by parse tree.

    Four forms are caught. The fourth — a bare string constant naming a priced
    field — closes the hole the comparator found in this guard on the day the
    comparator was written: ``for k in ("o", "open"): bar[k]`` reads a priced
    field through a **variable**, which no constant-subscript walk can see.
    Naming the field at all is the reachable signal, so the guard flags the name
    wherever it is spelled.
    """
    tree = _parse(path)
    found: dict[tuple[int, str], BarFieldRead] = {}
    module = path.name

    def record(lineno: int, field: str, form: str) -> None:
        key = (lineno, field)
        existing = found.get(key)
        if existing is None or FORM_SPECIFICITY[form] > FORM_SPECIFICITY[existing.form]:
            found[key] = BarFieldRead(module, lineno, field, form)

    for node in ast.walk(tree):
        # bar.close / row.volume
        if isinstance(node, ast.Attribute) and node.attr in PRICED_BAR_FIELDS:
            receiver = node.value
            if (
                isinstance(receiver, ast.Name)
                and receiver.id in SAFE_ATTRIBUTE_RECEIVERS
            ):
                continue
            record(node.lineno, node.attr, "attribute")

        # bar["close"] / row['o']
        elif isinstance(node, ast.Subscript):
            key_node = node.slice
            if (
                isinstance(key_node, ast.Constant)
                and isinstance(key_node.value, str)
                and key_node.value in PRICED_BAR_FIELDS
            ):
                record(node.lineno, key_node.value, "subscript")

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
                    record(first.lineno, first.value, f".{func.attr}()")

        # A bare string constant naming a priced field, anywhere.
        elif (
            isinstance(node, ast.Constant)
            and isinstance(node.value, str)
            and node.value in PRICED_BAR_FIELDS
        ):
            record(node.lineno, node.value, "string constant")

    return sorted(found.values(), key=lambda r: (r.lineno, r.field))


@pytest.mark.guard
def test_no_module_reads_a_priced_bar_field_anywhere() -> None:
    """Guard 5. Outside a sealed writer, no priced bar field is read. Ever.

    Walks the parse tree of every module under ``src/orb``. A read of open,
    high, low, close, volume, vwap, trade count, bid or ask — under any
    spelling, as an attribute, a subscript or a ``.get`` — fails here.
    """
    exempt = SEALED_MODULES | LATCHED_MODULES | {FIELD_REGISTRY_MODULE}
    violations: list[BarFieldRead] = []
    for path in _module_paths():
        if path.name in exempt:
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
    indirect = "def sneak(bar):\n    for k in ('high',):\n        return bar[k]\n"
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

    # The indirect form: a variable subscript that a constant walk cannot see.
    tmp2 = SRC_ROOT.parent / "_guard_probe_indirect.py"
    tmp2.write_text(indirect, encoding="utf-8")
    try:
        indirect_found = _bar_field_reads(tmp2)
    finally:
        tmp2.unlink()
    assert [f.field for f in indirect_found] == ["high"], indirect_found
    assert [f.form for f in indirect_found] == ["string constant"], indirect_found


@pytest.mark.guard
def test_readable_and_forbidden_field_lists_do_not_overlap() -> None:
    """The two blindness lists are disjoint. A field is readable or it is not."""
    from orb.fields import READABLE_FIELDS

    overlap = READABLE_FIELDS & PRICED_BAR_FIELDS
    assert not overlap, f"a field cannot be both readable and sealed: {overlap}"


# --------------------------------------------------------------------------
# Guard 2 — parse-tree config enforcement
# --------------------------------------------------------------------------

PENDING_ENFORCEMENT: dict[str, str] = {
    # field name -> the task that will read it
    "in_sample_end": "A.2 TASK 1 — session calendar",
    "holdout_start": "A.2 TASK 1 — session calendar",
    "opening_range_minutes": "A.2 TASK 3 — signal built dark",
    "risk_fraction_per_trade": "A.2 TASK 3 — sizing built dark",
    "max_concurrent_positions": "A.2 TASK 3 — sizing built dark",
    "max_gross_notional_multiple": "A.2 TASK 3 — sizing built dark",
    "commission_per_share_usd": "A.2 TASK 2 — cost model",
    "commission_order_minimum_usd": "A.2 TASK 2 — cost model",
    "finra_taf_per_share_sold_usd": "A.2 TASK 2 — cost model",
    "entry_slippage_usd": "A.2 TASK 2 — cost model",
    "stop_slippage_usd": "A.2 TASK 2 — cost model",
    "close_slippage_usd": "A.2 TASK 2 — cost model",
    "trial_count": "A.2 TASK 4 — power gate",
    "holdout_per_trade_t_gate": "A.2 TASK 3 — verdict built dark",
    "quartered_sharpe_assumption": "A.2 TASK 4 — power gate",
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


# --------------------------------------------------------------------------
# The sealed comparator — the single exception, and its limit
# --------------------------------------------------------------------------


@pytest.mark.guard
def test_comparator_returns_no_bar_value() -> None:
    """The sealed comparator emits aggregate counts and rates. Nothing else.

    Walks the parse tree of ``comparator.py`` and requires that **every public
    method's return annotation** is a counts-only findings record or a scalar.
    A method returning a bar, a price, or a container of either would fail
    here, and that is the whole content of the exception granted to this module.
    """
    allowed_returns = {
        "RevisionFinding",
        "AgreementFinding",
        "int",
        "float",
        "bool",
        "None",
    }
    tree = _parse(SRC_ROOT / "comparator.py")
    checked = 0
    offenders: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        if node.name.startswith("_"):
            continue  # private; unreachable from outside the module
        checked += 1
        returns = node.returns
        rendered = ast.unparse(returns) if returns is not None else "<missing>"
        if rendered not in allowed_returns:
            offenders.append(f"{node.name} -> {rendered}")

    assert checked >= 2, f"expected the two comparator entry points, saw {checked}"
    assert not offenders, (
        "the sealed comparator may return only counts-only findings records: "
        f"{offenders}"
    )


@pytest.mark.guard
def test_comparator_findings_carry_only_counts() -> None:
    """Every field of every record the comparator returns is an int or a float."""
    from orb.integrity import AgreementFinding, RevisionFinding

    for cls in (RevisionFinding, AgreementFinding):
        for field in dataclasses.fields(cls):
            assert field.type in {"int", "float"}, (
                cls.__name__,
                field.name,
                field.type,
            )
            assert field.name not in PRICED_BAR_FIELDS, (cls.__name__, field.name)


@pytest.mark.guard
def test_only_the_registered_modules_are_sealed() -> None:
    """The blindness exception is granted to exactly two modules, both present."""
    present = {p.name for p in _module_paths()}
    assert present >= SEALED_MODULES, SEALED_MODULES - present
    assert {"seal.py", "comparator.py"} == SEALED_MODULES


@pytest.mark.guard
def test_the_comparator_is_the_only_module_that_reads_a_priced_field() -> None:
    """seal.py names the fields; comparator.py is the only one that reads them."""
    reads = {
        p.name: _bar_field_reads(p) for p in _module_paths() if p.name in SEALED_MODULES
    }
    assert reads["comparator.py"], "the comparator must actually read priced fields"
    assert not reads["seal.py"], (
        "seal.py stores bytes and parses nothing; it must read no priced field: "
        f"{reads['seal.py']}"
    )


# --------------------------------------------------------------------------
# The latched modules — built dark, structurally unreachable from Stage A
# --------------------------------------------------------------------------


def _imported_orb_modules(path: Path) -> set[str]:
    """Every ``orb.<name>`` this module imports, by parse tree."""
    out: set[str] = set()
    for node in ast.walk(_parse(path)):
        if isinstance(node, ast.ImportFrom) and node.module:
            if node.module == "orb" or node.module.startswith("orb."):
                parts = node.module.split(".")
                if len(parts) > 1:
                    out.add(f"{parts[1]}.py")
                for alias in node.names:
                    out.add(f"{alias.name}.py")
        elif isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name.startswith("orb."):
                    out.add(f"{alias.name.split('.')[1]}.py")
    return out


@pytest.mark.guard
def test_no_stage_a_module_imports_a_latched_module() -> None:
    """The structural guarantee that replaces the blindness pin for dark code.

    An opening-range rule is a statement about highs and lows, so the strategy
    modules cannot be blind. What they can be is **unreachable**: if no Stage A
    module imports them, no Stage A code path can call them, whatever anyone
    later forgets. This walks every import in the package and requires it.
    """
    offenders: list[str] = []
    for path in _module_paths():
        if path.name in LATCHED_MODULES:
            continue
        leaked = _imported_orb_modules(path) & LATCHED_MODULES
        for name in sorted(leaked):
            offenders.append(f"{path.name} imports {name}")
    assert not offenders, (
        "a Stage A module imports a latched strategy module, n = "
        f"{len(offenders)}: {offenders}"
    )


@pytest.mark.guard
def test_every_latched_module_exists_and_is_named() -> None:
    present = {p.name for p in _module_paths()}
    assert present >= LATCHED_MODULES, LATCHED_MODULES - present
    assert not (LATCHED_MODULES & SEALED_MODULES), "a module is latched or sealed"


@pytest.mark.guard
def test_latched_modules_refuse_sealed_vendor_provenance_at_runtime() -> None:
    """The second pin: unreachable is structural, refusal is behavioural."""
    from orb.bars import Bar, Provenance, ProvenanceViolationError, require_readable

    sealed = Bar(
        timestamp_ms=1_700_000_000_000,
        open_c=1000,
        high_c=1050,
        low_c=950,
        close_c=1025,
        volume=100,
        provenance=Provenance.SEALED_VENDOR,
    )
    with pytest.raises(ProvenanceViolationError, match="built dark"):
        require_readable((sealed,), "probe", latched=False)
    require_readable((sealed,), "probe", latched=True)
