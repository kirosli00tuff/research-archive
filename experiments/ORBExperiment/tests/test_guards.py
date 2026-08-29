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
    {"bars.py", "universe.py", "signal.py", "verdict.py", "dispersion.py"}
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


CARVE_OUT_BOUNDARY_FIELDS: tuple[str, ...] = (
    "pre_period_end_ms",
    "post_holdout_start_ms",
)
"""Both edges of the two-sided carve-out, registered by **Amendment 11**.

The second edge is guarded on exactly the same two terms as the first: the
literal is typed in ``config.py`` and nowhere else, and it is read from config
by ``preperiod.py`` and nowhere else. A second boundary with weaker enforcement
than the first would be the whole hole.
"""


@pytest.mark.guard
def test_no_module_outside_config_hardcodes_the_pre_period_boundary() -> None:
    """Neither carve-out boundary is re-typed outside config.py."""
    literals = {getattr(CONFIG, name): name for name in CARVE_OUT_BOUNDARY_FIELDS}
    offenders: list[str] = []
    for path in _module_paths():
        if path.name == "config.py":
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Constant) and node.value in literals:
                offenders.append(
                    f"{path.name}:{node.lineno} hardcodes {literals[node.value]}"
                )
    assert not offenders, (
        f"a carve-out boundary literal is hardcoded outside config.py: {offenders}"
    )


@pytest.mark.guard
def test_only_preperiod_reads_the_boundary_from_config() -> None:
    """One enforcement site per edge, so there is one place to audit."""
    reads = _config_field_reads()
    for name in CARVE_OUT_BOUNDARY_FIELDS:
        modules = {r.split(":")[0] for r in reads.get(name, [])}
        assert modules <= {"preperiod.py"}, (
            f"{name} must be read only by preperiod.py, found: {modules}"
        )


@pytest.mark.guard
def test_both_carve_out_edges_are_actually_read_by_preperiod() -> None:
    """A registered edge nobody reads is an unenforced boundary.

    The stale-entry guard on ``PENDING_ENFORCEMENT`` catches a field nobody
    reads at all. This catches the narrower failure: an edge read by *some*
    module while ``preperiod.py`` — the one enforcement site — has quietly
    stopped reading it.
    """
    reads = _config_field_reads()
    for name in CARVE_OUT_BOUNDARY_FIELDS:
        modules = {r.split(":")[0] for r in reads.get(name, [])}
        assert modules == {"preperiod.py"}, (
            f"{name} is not read by preperiod.py; the boundary is unenforced. "
            f"Readers found: {modules or 'none'}"
        )


# --------------------------------------------------------------------------
# Amendment 13 — the tape is a configured, guarded field, not a default
# --------------------------------------------------------------------------

TOOLS_ROOT = REPO_ROOT / "tools"
"""Call sites live here. A default is overridable **at a call site**, so a guard
that walks only ``src/orb`` would be guarding the wrong half of the risk."""

BAR_REQUEST_BUILDERS: frozenset[str] = frozenset(
    {"alpaca_minute_bars", "alpaca_minute_bars_on_feed"}
)
"""Every builder that turns a feed choice into a URL."""


def _call_sites() -> list[Path]:
    return sorted(SRC_ROOT.rglob("*.py")) + sorted(TOOLS_ROOT.rglob("*.py"))


@pytest.mark.guard
def test_the_configured_feed_is_the_consolidated_tape() -> None:
    """The registered feed is ``sip``, and this is what the value protects.

    A.1 TASK 4 measured the alternative. The single-venue Alpaca-IEX feed
    carries a **median 0.027761 of consolidated first-5-minute volume over
    `n = 100` session-ticker pairs**, IQR [0.021200, 0.037068], with **100
    percent of pairs below the registered 0.20 single-venue threshold** —
    `DIFFERENT_TAPE` against both Massive and Alpaca-SIP.

    **That is the whole reason this assertion exists.** A feed carrying under
    three percent of the tape still serves a real high, a real low and a real
    volume for every bar, so the wrong branch **looks entirely normal in every
    downstream figure**: the opening range is narrower, the trigger fires at a
    different minute or not at all, the relative-volume ranking selects
    different names, and nothing anywhere reports an error. The measured
    0.027761 is the size of the lie.
    """
    from orb.vendors import MEASURED_SINGLE_VENUE_FEED, consolidated_feed

    assert CONFIG.consolidated_feed == "sip", (
        "the registered feed is the consolidated tape; A.1 TASK 4 measured the "
        f"single-venue alternative at a median 0.027761 of it over n = 100 pairs, "
        f"and this config now says {CONFIG.consolidated_feed!r}"
    )
    assert consolidated_feed() == CONFIG.consolidated_feed
    assert CONFIG.consolidated_feed != MEASURED_SINGLE_VENUE_FEED


@pytest.mark.guard
def test_no_bar_request_builder_defaults_its_feed() -> None:
    """A default is silently overridable at any call site. There is none.

    ``orb.vendors.alpaca_minute_bars`` carried ``feed: str = "sip"`` until
    Amendment 13. The default was correct and the risk was structural: nothing
    made a call site say which tape it wanted, so nothing would have noticed a
    call site that said the wrong one.
    """
    tree = _parse(SRC_ROOT / "vendors.py")
    offenders: list[str] = []
    checked = 0
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef):
            continue
        args = node.args
        for index, arg in enumerate(args.kwonlyargs):
            if arg.arg != "feed":
                continue
            checked += 1
            default = args.kw_defaults[index]
            if default is not None:
                offenders.append(
                    f"{node.name}:{node.lineno} defaults feed to {ast.unparse(default)}"
                )
    assert checked >= 2, f"expected both bar builders to take a feed, saw {checked}"
    assert not offenders, (
        "a bar request builder defaults its feed; the tape must be named at "
        f"every call site: {offenders}"
    )


@pytest.mark.guard
def test_every_bar_request_call_site_names_its_feed() -> None:
    """No request is constructed without an explicit feed. Anywhere."""
    offenders: list[str] = []
    checked = 0
    for path in _call_sites():
        for node in ast.walk(_parse(path)):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            name = (
                func.id
                if isinstance(func, ast.Name)
                else (func.attr if isinstance(func, ast.Attribute) else "")
            )
            if name not in BAR_REQUEST_BUILDERS:
                continue
            checked += 1
            if not any(kw.arg == "feed" for kw in node.keywords):
                offenders.append(f"{path.name}:{node.lineno} calls {name} with no feed")
    assert checked >= 5, f"expected the known bar call sites, saw {checked}"
    assert not offenders, (
        f"a bar request is constructed without an explicit feed: {offenders}"
    )


@pytest.mark.guard
def test_only_config_names_the_consolidated_feed_literal() -> None:
    """The feed value is read from config, never re-typed at a call site.

    The same rule the carve-out boundaries live under: a literal typed twice is
    a literal that can disagree with itself.
    """
    literal = CONFIG.consolidated_feed
    offenders: list[str] = []
    for path in _call_sites():
        if path.name == "config.py":
            continue
        for node in ast.walk(_parse(path)):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value == literal
            ):
                offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, (
        f"the consolidated feed literal {literal!r} is typed outside config.py: "
        f"{offenders}"
    )


@pytest.mark.guard
def test_a_manifest_without_a_recorded_feed_is_refused() -> None:
    """A re-pull on an unrecorded feed measures a tape difference as a revision."""
    from orb.vendors import TapeFeedError, require_manifest_feed

    assert require_manifest_feed({"feed": CONFIG.consolidated_feed}, "ctx") == (
        CONFIG.consolidated_feed
    )
    with pytest.raises(TapeFeedError, match="records no"):
        require_manifest_feed({"pulled_at": "2026-08-29"}, "ctx")
    with pytest.raises(TapeFeedError):
        require_manifest_feed({"feed": "iex"}, "ctx")
    with pytest.raises(TapeFeedError, match="not a string"):
        require_manifest_feed({"feed": 1}, "ctx")


@pytest.mark.guard
def test_the_sealed_probe_manifest_records_the_consolidated_feed() -> None:
    """The sealed slice's own manifest is held to the rule, not assumed to meet it."""
    import json

    manifest_path = REPO_ROOT / "reports" / "stage_a1r" / "task9_probe_manifest.json"
    if not manifest_path.exists():  # pragma: no cover - present in this repo
        pytest.skip("the probe manifest has not been written")
    from orb.vendors import require_manifest_feed

    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert require_manifest_feed(manifest, "task9") == CONFIG.consolidated_feed
    assert manifest["files_stored"] == 480
    assert manifest["bars_stored"] == 737_507


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
        # Registered by Amendment 7, A.1 TASK 4. Every field is a ratio or a
        # count, pinned below by test_comparator_findings_carry_only_counts.
        "TapeFinding",
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
    from orb.integrity import AgreementFinding, RevisionFinding, TapeFinding

    for cls in (RevisionFinding, AgreementFinding, TapeFinding):
        for field in dataclasses.fields(cls):
            assert field.type in {"int", "float"}, (
                cls.__name__,
                field.name,
                field.type,
            )
            assert field.name not in PRICED_BAR_FIELDS, (cls.__name__, field.name)


@pytest.mark.guard
def test_the_dispersion_writer_returns_two_scalars() -> None:
    """The carve-out writer emits two scalars and their counts. Nothing else.

    ``orb.dispersion`` is the one module that runs the registered Section 2
    selection, the Section 3 entry, stop and exit and the Section 6 cost model
    over **real bars** before the Stage C latch. The carve-out of Amendment 11
    permits it to read them; **nothing permits it to hand one back.**

    Two checks, because either alone is a hole. The **return annotations** stop
    a method handing back a trade, a series or a bar. The **field types** stop
    the record itself growing a mean, a per-name figure or a ranking: exactly
    two ``float`` fields are allowed and every other field must be an ``int``
    count, so that each scalar travels with its n.

    **The mean is deliberately not among them.** A mean net PnL *is* the outcome
    this repository is blind to; a dispersion is not.
    """
    import dataclasses as _dc

    allowed_returns = {"CarveOutDispersion", "int", "float", "bool", "None"}
    tree = _parse(SRC_ROOT / "dispersion.py")
    checked = 0
    offenders: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.FunctionDef) or node.name.startswith("_"):
            continue
        checked += 1
        rendered = (
            ast.unparse(node.returns) if node.returns is not None else "<missing>"
        )
        if rendered not in allowed_returns:
            offenders.append(f"{node.name} -> {rendered}")
    assert checked >= 1, "expected the carve-out writer's entry point"
    assert not offenders, (
        "the carve-out dispersion writer may return only two scalars and their "
        f"counts: {offenders}"
    )

    from orb.dispersion import CarveOutDispersion

    floats = [f.name for f in _dc.fields(CarveOutDispersion) if f.type == "float"]
    others = [f for f in _dc.fields(CarveOutDispersion) if f.type != "float"]
    assert floats == ["net_pnl_per_share_stdev", "trigger_rate"], floats
    assert all(f.type == "int" for f in others), [(f.name, f.type) for f in others]
    for field in _dc.fields(CarveOutDispersion):
        assert field.name not in PRICED_BAR_FIELDS, field.name
    assert "mean" not in " ".join(f.name for f in _dc.fields(CarveOutDispersion)), (
        "a mean net PnL is the outcome; the writer emits dispersion, never it"
    )


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


# --------------------------------------------------------------------------
# The quarantine — a spent read reaches no successor code path
# --------------------------------------------------------------------------

QUARANTINE_EXEMPT: frozenset[str] = frozenset({"latch.py"})
"""Only the latch module itself may name a read artifact path."""


@pytest.mark.guard
def test_no_module_reads_a_spent_read_artifact() -> None:
    """A successor runs on fresh data or it does not run.

    Walks every module for a string constant naming a Stage C or Stage D read
    artifact. `latch.py` builds those paths and is exempt; anything else naming
    one is a successor code path reaching into a spent read.
    """
    needles = ("stage_c_read", "stage_d_read", "reports/stage_c", "reports/stage_d")
    offenders: list[str] = []
    for path in _module_paths():
        if path.name in QUARANTINE_EXEMPT:
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                for needle in needles:
                    if needle in node.value:
                        offenders.append(f"{path.name}:{node.lineno} names {needle!r}")
    assert not offenders, f"a module reaches into a spent read artifact: {offenders}"


@pytest.mark.guard
def test_the_latch_module_is_the_only_writer_of_a_read_latch() -> None:
    """One place writes the latch, so there is one place to audit."""
    offenders: list[str] = []
    for path in _module_paths():
        if path.name in QUARANTINE_EXEMPT:
            continue
        for node in ast.walk(_parse(path)):
            if isinstance(node, ast.Call):
                func = node.func
                name = (
                    func.attr
                    if isinstance(func, ast.Attribute)
                    else (func.id if isinstance(func, ast.Name) else "")
                )
                if name in {"write_latch"}:
                    offenders.append(f"{path.name}:{node.lineno}")
    assert not offenders, f"write_latch called outside latch.py: {offenders}"


@pytest.mark.guard
def test_the_cli_entry_points_are_inert_and_exit_non_zero() -> None:
    """A collector that runs and stores nothing must not look like one that
    ran and found nothing. Section 0 fired PENDING_ACCESS; both passes refuse."""
    from orb.cli import ARM_MESSAGE, main

    assert "NOT ARMED" in ARM_MESSAGE
    assert "PENDING_ACCESS" in ARM_MESSAGE
    assert main(["daily"]) == 78
    assert main(["actions"]) == 78
    assert main([]) == 2
    assert main(["nonsense"]) == 2


@pytest.mark.guard
def test_the_systemd_units_do_not_collide_with_the_house_units() -> None:
    """npl-daily, npl-watch, etf-snap, etf-daily, solattn-daily and news-collect
    are in use and must be left untouched."""
    in_use = {
        "npl-daily",
        "npl-watch",
        "etf-snap",
        "etf-daily",
        "solattn-daily",
        "solattn-watch",
        "solattn-collect",
        "news-collect",
        "hfexperiment-bars",
    }
    unit_dir = REPO_ROOT / "systemd"
    ours = {p.stem for p in unit_dir.glob("*")}
    assert ours == {"orb-daily", "orb-actions"}, ours
    assert not (ours & in_use), ours & in_use


@pytest.mark.guard
def test_the_units_carry_the_registered_schedule_and_limits() -> None:
    unit_dir = REPO_ROOT / "systemd"
    daily = (unit_dir / "orb-daily.timer").read_text()
    actions = (unit_dir / "orb-actions.timer").read_text()
    assert "22:15:00 UTC" in daily
    assert "22:45:00 UTC" in actions
    for timer in (daily, actions):
        assert "Persistent=true" in timer
    for service in ("orb-daily.service", "orb-actions.service"):
        assert "MemoryMax=2G" in (unit_dir / service).read_text()


@pytest.mark.guard
def test_the_manual_run_guard_has_a_named_override() -> None:
    """The ADR-018 shape: refusing is cheaper than repairing interleaved rows."""
    from orb.manualrun import OVERRIDE_ENV, UNITS

    assert OVERRIDE_ENV == "ORB_ALLOW_MANUAL_RUN"
    assert set(UNITS) == {"orb-daily.service", "orb-actions.service"}


# --------------------------------------------------------------------------
# Guard 8 — secret redaction at the recording boundary
# --------------------------------------------------------------------------

RECORDING_BOUNDARIES: dict[tuple[str, str], str] = {
    ("ledger.py", "append"): "redact_row",
    ("seal.py", "store"): "redact_data",
    ("http.py", "__post_init__"): "redact_text",
}
"""Every function that turns a string into a record, and the redactor it calls.

Redaction sits **here** rather than at each call site because a credentialed
endpoint can return the key inside its own error body and a sealed writer stores
what it is handed without looking at it. A call site can be forgotten; a
recording boundary is one of three places and each is pinned by parse tree.
"""

SYNTHETIC_CREDENTIAL: str = "SYNTHETIC-ORB-CREDENTIAL-VALUE-0123456789abcdefXYZ"
"""A planted secret. It is not, and has never been, a real credential."""


@pytest.mark.guard
def test_no_credential_value_reaches_a_recorded_string(tmp_path: Path) -> None:
    """Guard 8. A synthetic credential planted in a fake refusal body reaches
    no sealed file, no ledger line, no response field and no console string.

    The shape is taken from what the vendors actually do: Polygon carries the
    key in the **query string**, and a credentialed endpoint can echo the key
    back **inside its own error body**. `docs/ACCESS.md` records refusal
    payloads verbatim, so both paths end in a recorded artifact.
    """
    import io
    import json
    from contextlib import redirect_stdout

    from orb.callstate import HealthState
    from orb.http import Response
    from orb.ledger import AppendOnlyLedger, RequestLedger
    from orb.redact import Redactor, install_redactor, placeholder_for, say
    from orb.seal import SealedWriter

    name = "ORB_SYNTHETIC_KEY"
    marker = placeholder_for(name)
    install_redactor(Redactor({name: SYNTHETIC_CREDENTIAL}))
    try:
        url = f"https://api.example.invalid/v2/aggs?apiKey={SYNTHETIC_CREDENTIAL}"
        body = json.dumps(
            {
                "status": "ERROR",
                "error": f"unknown api key {SYNTHETIC_CREDENTIAL} for this tier",
                "request_id": "0000",
            }
        ).encode("utf-8")

        seals = AppendOnlyLedger(tmp_path / "seals.jsonl")
        writer = SealedWriter(tmp_path / "sealed", seals)
        record = writer.store("probe.raw", body)

        requests = RequestLedger(tmp_path / "requests.jsonl", {"vendorx": 5})
        requests.charge("vendorx", "2026-08-30", url)

        response = Response(
            url=url,
            status_code=401,
            byte_count=len(body),
            elapsed_s=0.1,
            body=body,
            health=HealthState.SOURCE_FAILED,
            sent_at="2026-08-30T00:00:00.000Z",
        )

        console = io.StringIO()
        with redirect_stdout(console):
            say("probing", url, response.refusal_fragment())

        artifacts: dict[str, bytes] = {
            "sealed file": (tmp_path / "sealed" / "probe.raw").read_bytes(),
            "seal ledger": (tmp_path / "seals.jsonl").read_bytes(),
            "request ledger": (tmp_path / "requests.jsonl").read_bytes(),
            "response.url": response.url.encode("utf-8"),
            "response.body": response.body,
            "refusal_fragment": response.refusal_fragment().encode("utf-8"),
            "repr(response)": repr(response).encode("utf-8"),
            "console": console.getvalue().encode("utf-8"),
            "seal record path": str(record.path).encode("utf-8"),
        }

        needle = SYNTHETIC_CREDENTIAL.encode("utf-8")
        leaks = [where for where, blob in artifacts.items() if needle in blob]
        assert not leaks, f"credential value reached a recorded string: {leaks}"

        # The placeholder must be present where the value was, naming its
        # variable — a silently *dropped* secret would pass the check above
        # while destroying the evidence the artifact exists to carry.
        marker_bytes = marker.encode("utf-8")
        for where in (
            "sealed file",
            "request ledger",
            "response.url",
            "response.body",
            "console",
        ):
            assert marker_bytes in artifacts[where], (
                f"{where} lost the secret without recording that it was there"
            )
    finally:
        install_redactor(Redactor({}))


@pytest.mark.guard
def test_the_redaction_guard_actually_binds() -> None:
    """A guard that cannot fire is decoration. This proves it fires.

    With no redactor installed, the identical planted credential reaches the
    identical artifacts. The guard above is therefore an assertion about the
    redactor rather than about an input that never contained a secret.
    """
    import json

    from orb.callstate import HealthState
    from orb.http import Response
    from orb.redact import Redactor, install_redactor

    install_redactor(Redactor({}))
    body = json.dumps({"error": f"key {SYNTHETIC_CREDENTIAL} rejected"}).encode("utf-8")
    response = Response(
        url=f"https://x.invalid/?apiKey={SYNTHETIC_CREDENTIAL}",
        status_code=401,
        byte_count=len(body),
        elapsed_s=0.0,
        body=body,
        health=HealthState.SOURCE_FAILED,
        sent_at="2026-08-30T00:00:00.000Z",
    )
    assert SYNTHETIC_CREDENTIAL in response.url
    assert SYNTHETIC_CREDENTIAL.encode("utf-8") in response.body


@pytest.mark.guard
def test_every_recording_boundary_routes_through_the_redactor() -> None:
    """Guard 8, structurally. Each boundary function calls its redactor."""
    missing: list[str] = []
    for (module, function), redactor in RECORDING_BOUNDARIES.items():
        tree = _parse(SRC_ROOT / module)
        target: ast.FunctionDef | None = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == function:
                target = node
                break
        if target is None:
            missing.append(f"{module}:{function} does not exist")
            continue
        calls = {
            n.func.id
            for n in ast.walk(target)
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
        }
        if redactor not in calls:
            missing.append(f"{module}:{function} does not call {redactor}")
    assert not missing, (
        f"recording boundaries not redacting, n = {len(missing)}: {missing}"
    )


@pytest.mark.guard
def test_no_module_hardcodes_a_credential_variable_outside_the_registry() -> None:
    """The three credential names live in one module, as Guard 6 does for the
    carve-out boundary. A name re-typed elsewhere is a second place to audit."""
    from orb.credentials import CREDENTIAL_NAMES

    offenders: list[str] = []
    for path in _module_paths():
        if path.name == "credentials.py":
            continue
        for node in ast.walk(_parse(path)):
            if (
                isinstance(node, ast.Constant)
                and isinstance(node.value, str)
                and node.value in CREDENTIAL_NAMES
            ):
                offenders.append(f"{path.name}:{node.lineno} names {node.value}")
    assert not offenders, f"credential variable named outside the registry: {offenders}"


@pytest.mark.guard
def test_the_credential_presence_row_carries_no_value_shaped_field() -> None:
    """Presence, name and character length are recordable. Nothing else is.

    A hash is excluded by name: a hash of a 32-character key is a confirmation
    oracle for a guess, and that is the half of the rule that is easy to miss.
    """
    from orb.credentials import CredentialPresence

    row = CredentialPresence("ORB_X", is_present=True, character_length=32).as_row()
    assert set(row) == {"kind", "credential", "is_present", "character_length"}
    forbidden = {"value", "secret", "sha256", "hash", "digest", "prefix", "suffix"}
    assert not (set(row) & forbidden), row
