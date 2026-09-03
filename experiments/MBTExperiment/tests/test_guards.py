"""The five structural guards. Each pins a standing rule and fails loudly.

These are not unit tests of behaviour. They are the mechanical enforcement of the
non-negotiable rules in ``CLAUDE.md``, and every one of them **provokes a real
refusal and records it** through the ``refusals`` fixture, so the evidence under
``reports/guards/refusals.json`` is produced rather than described.
"""

from __future__ import annotations

import ast
import sys
from collections.abc import Callable
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest
from conftest import RefusalRecorder

from mbt.absence import (
    AbsenceReason,
    Absent,
    AbsentCoercionError,
    is_absent,
    require_present,
)
from mbt.broker import TransmitRefusedError, build_short_option_order, what_if_order
from mbt.clock import NaiveDatetimeError, NonUtcDatetimeError, ObservationClock, require_utc
from mbt.config import GatewayConfig, MissingConfigError, PaperOnlyClauseError
from mbt.figures import Figure, TickDelayStatus
from mbt.gates import (
    DelayedQuoteInadmissibleError,
    GateName,
    GateOutcome,
    PaperFigureInadmissibleError,
    fire,
    fire_lower_bound,
)
from mbt.latch import Latch, LatchAlreadySpentError, LatchedFigure, LatchNotWrittenError
from mbt.provenance import (
    Environment,
    EnvironmentMismatchError,
    ProvenanceKind,
    SessionProvenance,
    UnknownAccountPrefixError,
    environment_from_account,
)
from mbt.quotes import Quote, screen

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.no_transmit_scan import (
    BANNED_TRANSMIT_METHODS,
    Rule,
    scan_package,
    scan_source,
)

REPO = Path(__file__).resolve().parents[1]
PACKAGE = REPO / "src" / "mbt"


def _clock(lag_seconds: float = 0.0) -> ObservationClock:
    local = datetime(2026, 9, 3, 12, 0, 0, tzinfo=UTC)
    return ObservationClock(venue=local - timedelta(seconds=lag_seconds), local=local)


def _quote(**overrides: object) -> Quote:
    base: dict[str, object] = {
        "leg": "option_call",
        "bid": 100.0,
        "ask": 110.0,
        "clock": _clock(),
        "tick_delay": TickDelayStatus.REALTIME,
    }
    base.update(overrides)
    return Quote(**base)  # type: ignore[arg-type]


# ===========================================================================
# GUARD ONE — no transmit. An AST walk over the package's parse trees.
# ===========================================================================


def test_guard_one_the_package_is_clean_right_now() -> None:
    findings = scan_package()
    assert findings == [], f"the package is not transmit-clean: {findings}"


def test_guard_one_walks_parse_trees_rather_than_text() -> None:
    """A banned name inside a comment and inside a docstring is NOT a finding.

    This is the defect the guard exists to avoid: a previous project's config
    guard scanned raw text, matched its key inside a trailing comment, and called
    that enforcement.
    """
    source = '''
"""A docstring that mentions placeOrder and cancelOrder by name."""
# placeOrder appears in this comment too
NAMES = "placeOrder cancelOrder"

def preview(broker, contract, order):
    return broker.whatIfOrder(contract, order)
'''
    findings = scan_source(source, PACKAGE / "synthetic.py", full=True)
    assert findings == [], f"a text scan would have fired here; an AST walk must not: {findings}"


def test_guard_one_fires_on_a_transmitting_call_site(refusals: RefusalRecorder) -> None:
    source = "def go(broker, contract, order):\n    return broker.placeOrder(contract, order)\n"
    findings = scan_source(source, PACKAGE / "synthetic.py", full=True)
    assert len(findings) == 1
    assert findings[0].rule is Rule.TRANSMIT_CALL_SITE
    refusals.record_finding(
        guard="one: no transmit",
        scenario="a placeOrder call site appears in the package",
        expectation="the build fails; no transmitting call site exists here",
        finding=findings[0],
    )


def test_guard_one_fires_on_a_false_literal(refusals: RefusalRecorder) -> None:
    """Registered mutation 1, exercised as a unit rather than only end to end."""
    source = "o = Order(action='SELL', whatIf=False, transmit=False)\n"
    findings = scan_source(source, PACKAGE / "synthetic.py", full=True)
    assert [f.rule for f in findings] == [Rule.WHATIF_FALSE_LITERAL]
    refusals.record_finding(
        guard="one: no transmit",
        scenario="whatIf is written as the literal False",
        expectation="the build fails on the False literal",
        finding=findings[0],
    )


def test_guard_one_fires_when_the_flag_comes_from_a_variable(refusals: RefusalRecorder) -> None:
    """Registered mutation 2. A non-literal cannot be verified at build time."""
    source = "flag = True\no = Order(action='SELL', whatIf=flag, transmit=False)\n"
    findings = scan_source(source, PACKAGE / "synthetic.py", full=True)
    assert [f.rule for f in findings] == [Rule.WHATIF_NOT_A_LITERAL]
    refusals.record_finding(
        guard="one: no transmit",
        scenario="whatIf is supplied from a variable rather than a literal",
        expectation="the build fails; a non-literal cannot be verified statically",
        finding=findings[0],
    )


@pytest.mark.parametrize(
    ("source", "expected"),
    [
        ("o = Order(action='SELL', transmit=False)\n", Rule.WHATIF_MISSING),
        ("o = Order(action='SELL', whatIf=cfg.flag)\n", Rule.WHATIF_NOT_A_LITERAL),
        ("o = Order(action='SELL', whatIf=compute())\n", Rule.WHATIF_NOT_A_LITERAL),
        ("o = Order(action='SELL', **kwargs)\n", Rule.WHATIF_NOT_A_LITERAL),
        ("r = what_if_order(b, c, o, whatIf=False)\n", Rule.WHATIF_FALSE_LITERAL),
        ("r = what_if_order(b, c, o)\n", Rule.WHATIF_MISSING),
        ("m = getattr(ib, 'placeOrder')\n", Rule.DYNAMIC_ATTRIBUTE_DODGE),
        ("exec('ib.placeOrder(c, o)')\n", Rule.DYNAMIC_EXECUTION),
    ],
)
def test_guard_one_covers_every_registered_failure_mode(source: str, expected: Rule) -> None:
    findings = scan_source(source, PACKAGE / "synthetic.py", full=True)
    assert expected in {f.rule for f in findings}, f"{source!r} produced {findings}"


def test_guard_one_accepts_only_the_true_literal() -> None:
    source = "o = Order(action='SELL', whatIf=True, transmit=False)\n"
    assert scan_source(source, PACKAGE / "synthetic.py", full=True) == []


def test_guard_one_banned_set_covers_every_transmit_path() -> None:
    """The neighbours are banned too, not only the registered name."""
    assert "placeOrder" in BANNED_TRANSMIT_METHODS
    for neighbour in ("cancelOrder", "reqGlobalCancel", "exerciseOptions"):
        assert neighbour in BANNED_TRANSMIT_METHODS


def test_guard_one_no_package_module_imports_a_transmitting_name() -> None:
    """Banning call sites is not enough if a transmit path is imported by name."""
    for path in sorted(PACKAGE.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    assert alias.name not in BANNED_TRANSMIT_METHODS, f"{path}: {alias.name}"


def test_guard_one_run_time_refusal_backs_the_build_time_one(refusals: RefusalRecorder) -> None:
    """The scan cannot see a mutation applied after construction. This can."""

    class _Order:
        whatIf = False
        transmit = False

    class _Broker:
        def whatIfOrder(self, contract: object, order: object) -> object:
            raise AssertionError("must not be reached")

    with pytest.raises(TransmitRefusedError) as excinfo:
        what_if_order(_Broker(), object(), _Order(), whatIf=True)  # type: ignore[arg-type]
    refusals.record(
        guard="one: no transmit",
        scenario="an order object was mutated to whatIf=False after construction",
        expectation="the run-time check refuses; the AST scan cannot see a later mutation",
        exception=excinfo.value,
    )


def test_guard_one_builder_emits_a_preview_order() -> None:
    class _Order:
        def __init__(self, **kwargs: object) -> None:
            self.__dict__.update(kwargs)

    order = build_short_option_order(_Order, quantity=1)
    assert order.whatIf is True
    assert order.transmit is False


# ===========================================================================
# GUARD TWO — environment provenance is measured, never declared.
# ===========================================================================


@pytest.mark.parametrize(
    ("account", "expected"),
    [
        ("DU1234567", Environment.PAPER),  # SYNTHETIC-FIXTURE
        ("U1234567", Environment.LIVE),  # SYNTHETIC-FIXTURE
        ("dur12345", Environment.PAPER),  # SYNTHETIC-FIXTURE
    ],
)
def test_guard_two_derives_environment_from_the_account_prefix(
    account: str, expected: Environment
) -> None:
    assert environment_from_account(account) is expected


def test_guard_two_refuses_a_live_declaration_on_a_paper_account(
    refusals: RefusalRecorder, tmp_path: Path
) -> None:
    """Registered mutation 3. The refusal must also write NOTHING."""
    target = tmp_path / "should_never_exist.json"
    with pytest.raises(EnvironmentMismatchError) as excinfo:
        provenance = SessionProvenance.from_connection(
            declared=Environment.LIVE,
            connected_account="DU1234567",  # SYNTHETIC-FIXTURE
            client_id=7,
            host="127.0.0.1",
            port=4002,
        )
        target.write_text(str(provenance.as_row()), encoding="utf-8")

    assert not target.exists(), "a mismatched session must write nothing at all"
    refusals.record(
        guard="two: environment provenance",
        scenario="a session declaring live connected to a D-prefixed account",
        expectation="construction raises and the recorder is never handed an object, so nothing is written",
        exception=excinfo.value,
    )


def test_guard_two_refuses_an_unknown_prefix_rather_than_defaulting(
    refusals: RefusalRecorder,
) -> None:
    with pytest.raises(UnknownAccountPrefixError) as excinfo:
        environment_from_account("X1234567")
    refusals.record(
        guard="two: environment provenance",
        scenario="an account carried neither a D nor a U prefix",
        expectation="the guard fails rather than defaulting to either side",
        exception=excinfo.value,
    )


def test_guard_two_refuses_an_empty_account() -> None:
    with pytest.raises(UnknownAccountPrefixError):
        environment_from_account("   ")


def test_guard_two_accepts_a_matching_declaration_and_masks_the_number() -> None:
    provenance = SessionProvenance.from_connection(
        declared=Environment.PAPER,
        connected_account="DU1234567",  # SYNTHETIC-FIXTURE
        client_id=7,
        host="127.0.0.1",
        port=4002,
    )
    assert provenance.measured is Environment.PAPER
    row = provenance.as_row()
    assert "DU1234567" not in str(row)  # SYNTHETIC-FIXTURE
    assert row["account_masked"] == "D*******7"


def test_guard_two_config_refuses_a_live_request(refusals: RefusalRecorder) -> None:
    with pytest.raises(PaperOnlyClauseError) as excinfo:
        GatewayConfig.load(Environment.LIVE)
    refusals.record(
        guard="two: environment provenance",
        scenario="a live session was requested while the paper-only clause is in force",
        expectation="refused before a socket is opened; lifting the clause is an operator edit to CLAUDE.md",
        exception=excinfo.value,
    )


def test_guard_two_config_names_the_missing_variable(
    refusals: RefusalRecorder, tmp_path: Path
) -> None:
    with pytest.raises(MissingConfigError) as excinfo:
        GatewayConfig.load(Environment.PAPER, environ={}, dotenv_path=tmp_path / "absent.env")
    assert "MBT_IB_HOST" in str(excinfo.value)
    refusals.record(
        guard="two: environment provenance",
        scenario="a required environment variable was unset",
        expectation="the error names the variable, so a reader is not sent to the wrong file",
        exception=excinfo.value,
    )


# ===========================================================================
# GUARD THREE — paper figures are never verdict-bearing.
# ===========================================================================


def _paper_margin() -> Figure:
    return Figure.record(
        name="initial_margin_short_mbt_option",
        value=880.0,
        unit="USD_per_contract",
        kind=ProvenanceKind.MARGIN,
        environment=Environment.PAPER,
    )


def test_guard_three_a_paper_margin_reaching_a_gate_raises(refusals: RefusalRecorder) -> None:
    """Registered mutation 4."""
    with pytest.raises(PaperFigureInadmissibleError) as excinfo:
        fire(GateName.MARGIN, _paper_margin(), ceiling=1000.0, unit="USD_per_contract")
    refusals.record(
        guard="three: paper inadmissibility",
        scenario="a paper-tagged margin figure was fed to the MARGIN gate",
        expectation="raises; a paper margin is development evidence and never verdict-bearing",
        exception=excinfo.value,
    )


def test_guard_three_a_paper_commission_report_also_raises(refusals: RefusalRecorder) -> None:
    figure = Figure.record(
        name="exchange_and_regulatory_fee",
        value=1.5,
        unit="bps_of_notional",
        kind=ProvenanceKind.COMMISSION_REPORT,
        environment=Environment.PAPER,
    )
    with pytest.raises(PaperFigureInadmissibleError) as excinfo:
        fire(GateName.COST, figure, ceiling=34.6, unit="bps_of_notional")
    refusals.record(
        guard="three: paper inadmissibility",
        scenario="a paper-tagged commission report was fed to the COST gate",
        expectation="raises; paper fills are simulated and their reports synthetic",
        exception=excinfo.value,
    )


def test_guard_three_a_live_margin_is_admissible_and_the_gate_fires() -> None:
    figure = Figure.record(
        name="initial_margin_short_mbt_option",
        value=880.0,
        unit="USD_per_contract",
        kind=ProvenanceKind.MARGIN,
        environment=Environment.LIVE,
    )
    result = fire(GateName.MARGIN, figure, ceiling=1000.0, unit="USD_per_contract")
    assert result.outcome is GateOutcome.PASS


def test_guard_three_a_realtime_paper_quote_is_admitted_but_labelled() -> None:
    """The registered asymmetry: a quote is a property of the FEED, not the account."""
    figure = Figure.record(
        name="straddle_round_trip_bps",
        value=12.0,
        unit="bps_of_notional",
        kind=ProvenanceKind.QUOTE,
        environment=Environment.PAPER,
        tick_delay=TickDelayStatus.REALTIME,
    )
    result = fire(GateName.COST, figure, ceiling=34.6, unit="bps_of_notional")
    assert result.outcome is GateOutcome.PASS
    assert "DOCUMENTED, NOT MEASURED" in result.admissibility_note


@pytest.mark.parametrize(
    "status",
    [
        TickDelayStatus.DELAYED,
        TickDelayStatus.FROZEN,
        TickDelayStatus.DELAYED_FROZEN,
        TickDelayStatus.UNKNOWN,
    ],
)
def test_guard_three_a_non_realtime_quote_is_refused(status: TickDelayStatus, refusals) -> None:  # type: ignore[no-untyped-def]
    figure = Figure.record(
        name="straddle_round_trip_bps",
        value=12.0,
        unit="bps_of_notional",
        kind=ProvenanceKind.QUOTE,
        environment=Environment.PAPER,
        tick_delay=status,
    )
    with pytest.raises(DelayedQuoteInadmissibleError) as excinfo:
        fire(GateName.COST, figure, ceiling=34.6, unit="bps_of_notional")
    refusals.record(
        guard="three: paper inadmissibility",
        scenario=f"a quote carrying tick delay status {status.value!r} reached the COST gate",
        expectation="raises; only a real-time tick is admissible and an unreported status is never assumed live",
        exception=excinfo.value,
    )


def test_guard_three_an_absent_figure_records_absent_rather_than_zero() -> None:
    absent = Absent(AbsenceReason.NO_LIVE_SESSION, "needs a U-prefixed session")
    result = fire(GateName.MARGIN, absent, ceiling=1000.0, unit="USD_per_contract")
    assert result.outcome is GateOutcome.ABSENT
    assert result.measured is None
    assert "no_live_session" in result.reason


# ===========================================================================
# GUARD FOUR — the deciding-read latch. One spend per registered figure.
# ===========================================================================


def test_guard_four_a_second_spend_raises(refusals: RefusalRecorder, tmp_path: Path) -> None:
    """Registered mutation 5."""
    latch = Latch(tmp_path / "latches")
    modules = [REPO / "src" / "mbt" / "whatif.py"]
    latch.spend(LatchedFigure.MARGIN_SHORT_MBT_OPTION, modules, "first and only spend")

    with pytest.raises(LatchAlreadySpentError) as excinfo:
        latch.spend(LatchedFigure.MARGIN_SHORT_MBT_OPTION, modules, "second attempt")
    refusals.record(
        guard="four: deciding-read latch",
        scenario="the deciding latch for one registered figure was spent twice",
        expectation="the second attempt raises LatchAlreadySpentError; a second deciding read voids the registration",
        exception=excinfo.value,
    )


def test_guard_four_is_keyed_per_registered_figure(tmp_path: Path) -> None:
    """Spending one figure must not lock out the other."""
    latch = Latch(tmp_path / "latches")
    modules = [REPO / "src" / "mbt" / "whatif.py"]
    latch.spend(LatchedFigure.MARGIN_SHORT_MBT_OPTION, modules, "margin")
    latch.spend(LatchedFigure.COST_ABSENT_LEGS_P90, modules, "cost")
    assert latch.is_spent(LatchedFigure.MARGIN_SHORT_MBT_OPTION)
    assert latch.is_spent(LatchedFigure.COST_ABSENT_LEGS_P90)


def test_guard_four_reading_an_unwritten_latch_raises(
    refusals: RefusalRecorder, tmp_path: Path
) -> None:
    latch = Latch(tmp_path / "latches")
    with pytest.raises(LatchNotWrittenError) as excinfo:
        latch.read_record(LatchedFigure.COST_ABSENT_LEGS_P90)
    refusals.record(
        guard="four: deciding-read latch",
        scenario="a latched read was attempted with no latch on disk",
        expectation="raises; a latch is written before the read, not after",
        exception=excinfo.value,
    )


def test_guard_four_records_module_hashes_and_detects_drift(tmp_path: Path) -> None:
    latch = Latch(tmp_path / "latches")
    module = tmp_path / "participant.py"
    module.write_text("x = 1\n", encoding="utf-8")
    latch.spend(LatchedFigure.COST_ABSENT_LEGS_P90, [module], "with a participant")
    assert latch.drifted_modules(LatchedFigure.COST_ABSENT_LEGS_P90, [module]) == {}
    module.write_text("x = 2\n", encoding="utf-8")
    assert latch.drifted_modules(LatchedFigure.COST_ABSENT_LEGS_P90, [module]) != {}


def test_guard_four_the_latch_file_is_durable_on_disk(tmp_path: Path) -> None:
    """Fsynced before returning: the record is readable the instant spend returns."""
    latch = Latch(tmp_path / "latches")
    latch.spend(LatchedFigure.COST_ABSENT_LEGS_P90, [REPO / "src" / "mbt" / "latch.py"], "durable")
    path = latch.path_for(LatchedFigure.COST_ABSENT_LEGS_P90)
    assert path.exists() and path.stat().st_size > 0


# ===========================================================================
# GUARD FIVE — recorded absence. An absence is a state, never a value.
# ===========================================================================


def test_guard_five_absent_refuses_float_int_and_indexing(refusals: RefusalRecorder) -> None:
    absent = Absent(AbsenceReason.NO_LIVE_SESSION, "needs a U-prefixed session")
    with pytest.raises(AbsentCoercionError) as excinfo:
        float(absent)
    with pytest.raises(AbsentCoercionError):
        int(absent)
    with pytest.raises(AbsentCoercionError):
        absent["margin"]
    refusals.record(
        guard="five: recorded absence",
        scenario="an absent live-session margin was coerced with float()",
        expectation="raises; a synthesized zero is indistinguishable from a measured one",
        exception=excinfo.value,
    )


def test_guard_five_absent_refuses_every_arithmetic_ordering_and_truth_path() -> None:
    absent = Absent(AbsenceReason.NOT_SERVED)
    operations: list[Callable[[], object]] = [
        lambda: absent + 1,
        lambda: 1 + absent,
        lambda: absent - 1,
        lambda: 1 - absent,
        lambda: absent * 2,
        lambda: 2 * absent,
        lambda: absent / 2,
        lambda: 2 / absent,
        lambda: absent**2,
        lambda: 2**absent,
        lambda: -absent,
        lambda: abs(absent),
        lambda: absent < 1,
        lambda: absent <= 1,
        lambda: absent > 1,
        lambda: absent >= 1,
        lambda: bool(absent),
        lambda: len(absent),
        lambda: list(absent),
        lambda: [0, 1][absent],
        lambda: round(absent),
        lambda: complex(absent),
    ]
    for operation in operations:
        with pytest.raises(AbsentCoercionError):
            operation()


def test_guard_five_truth_testing_is_refused_rather_than_falsey() -> None:
    """`if spread:` on an absent spread must not quietly take the false branch."""
    absent = Absent(AbsenceReason.UNQUOTED_LEG, "no bid")
    with pytest.raises(AbsentCoercionError):
        # mypy reports the body unreachable, which is the same guarantee reached
        # statically: __bool__ returns Never, so no branch can follow the test.
        if absent:
            pass  # type: ignore[unreachable]


def test_guard_five_require_present_never_substitutes(refusals: RefusalRecorder) -> None:
    absent = Absent(AbsenceReason.INSUFFICIENT_SAMPLE, "3 of 20 windows")
    with pytest.raises(AbsentCoercionError) as excinfo:
        require_present(absent, "cost gate")
    assert is_absent(absent)
    refusals.record(
        guard="five: recorded absence",
        scenario="an under-sampled census was narrowed with require_present",
        expectation="raises loudly rather than substituting a value",
        exception=excinfo.value,
    )


@pytest.mark.parametrize(
    ("overrides", "expected"),
    [
        ({"bid": None}, AbsenceReason.UNQUOTED_LEG),
        ({"ask": None}, AbsenceReason.UNQUOTED_LEG),
        ({"bid": 120.0, "ask": 110.0}, AbsenceReason.CROSSED_BOOK),
        ({"bid": 0.0}, AbsenceReason.ZERO_BID),
        ({"bid": -1.0}, AbsenceReason.ZERO_BID),
        ({"clock": _clock(30.0)}, AbsenceReason.STALE_TIMESTAMP),
        ({"tick_delay": TickDelayStatus.DELAYED}, AbsenceReason.DELAYED_TICK),
        ({"tick_delay": TickDelayStatus.FROZEN}, AbsenceReason.FROZEN_TICK),
        ({"tick_delay": TickDelayStatus.UNKNOWN}, AbsenceReason.DELAYED_TICK),
    ],
)
def test_guard_five_each_registered_refusal_condition_is_typed(
    overrides: dict[str, object], expected: AbsenceReason, refusals: RefusalRecorder
) -> None:
    result = screen(_quote(**overrides))
    assert isinstance(result, Absent)
    assert result.reason is expected
    refusals.record(
        guard="five: recorded absence",
        scenario=f"a quote leg with {overrides} was screened",
        expectation=f"refused as Absent({expected.value}), never coerced to a number",
        exception=AbsentCoercionError(result.detail),
    )


def test_guard_five_a_clean_quote_passes_screening() -> None:
    assert screen(_quote()) == _quote()


def test_guard_five_a_crossed_book_beats_a_delayed_feed_in_reporting_order() -> None:
    """Structure before staleness: a broken book is the more specific fact."""
    result = screen(_quote(bid=120.0, ask=110.0, tick_delay=TickDelayStatus.DELAYED))
    assert isinstance(result, Absent)
    assert result.reason is AbsenceReason.CROSSED_BOOK


def test_guard_five_naive_and_non_utc_datetimes_are_refused(refusals: RefusalRecorder) -> None:
    with pytest.raises(NaiveDatetimeError) as naive:
        require_utc(datetime(2026, 9, 3, 12, 0, 0), "test")
    with pytest.raises(NonUtcDatetimeError):
        require_utc(datetime(2026, 9, 3, 12, 0, 0, tzinfo=timezone(timedelta(hours=-7))), "test")
    refusals.record(
        guard="five: recorded absence",
        scenario="a naive datetime reached a boundary",
        expectation="refused; a naive stamp is never assumed UTC and never assumed local",
        exception=naive.value,
    )


# ===========================================================================
# The one-sided lower-bound gate. It can FAIL and it can never PASS.
# ===========================================================================


def test_a_lower_bound_above_the_ceiling_fails_soundly() -> None:
    """Every absent leg is non-negative, so exceeding the ceiling is decisive."""
    result = fire_lower_bound(
        GateName.COST,
        40.0,
        ceiling=34.6,
        unit="bps_of_notional",
        absent_legs=["exchange_and_regulatory_fee"],
    )
    assert result.outcome is GateOutcome.FAIL
    assert result.measured == 40.0


def test_a_lower_bound_below_the_ceiling_is_absent_and_never_a_pass() -> None:
    """Nothing follows: the absent legs could carry the total past the ceiling."""
    result = fire_lower_bound(
        GateName.COST,
        12.0,
        ceiling=34.6,
        unit="bps_of_notional",
        absent_legs=["exchange_and_regulatory_fee"],
    )
    assert result.outcome is GateOutcome.ABSENT
    assert result.measured is None
    assert "cannot be concluded from a lower bound" in result.reason


@pytest.mark.parametrize("bound", [0.0, 1.0, 34.5, 34.6])
def test_no_lower_bound_at_or_below_the_ceiling_ever_passes(bound: float) -> None:
    result = fire_lower_bound(
        GateName.COST, bound, ceiling=34.6, unit="bps_of_notional", absent_legs=["fee"]
    )
    assert result.outcome is not GateOutcome.PASS


def test_the_absent_legs_are_named_in_the_result() -> None:
    result = fire_lower_bound(
        GateName.COST,
        12.0,
        ceiling=34.6,
        unit="bps_of_notional",
        absent_legs=["exchange_and_regulatory_fee", "ibkr_daily_exposure_fee"],
    )
    assert "exchange_and_regulatory_fee" in result.reason
    assert "ibkr_daily_exposure_fee" in result.reason


def test_summing_a_measured_leg_with_an_absent_one_raises(refusals: RefusalRecorder) -> None:
    """This is WHY the lower-bound gate exists: the all-in sum cannot be formed."""
    fee = Absent(AbsenceReason.NOT_SERVED, "CME refused automated access to its schedule")
    with pytest.raises(AbsentCoercionError) as excinfo:
        _ = 12.0 + fee
    refusals.record(
        guard="five: recorded absence",
        scenario="a measured spread was added to the absent exchange and regulatory fee",
        expectation="raises; the all-in cost cannot be formed, so the gate falls back to a lower bound",
        exception=excinfo.value,
    )
