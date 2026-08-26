"""Structural guards. Each one fails a specific mutation of real source.

These are not style checks. Each guard exists because a predecessor system
failed in exactly the way the guard forbids, and each is exercised by
scripts/mutations.py against the real file rather than against a fixture.
"""

from __future__ import annotations

import ast
import datetime as dt
import sqlite3
from dataclasses import fields
from pathlib import Path

import pytest

from insider.callstate import (
    ALL_STATES,
    OPERATIONAL_HEALTH_STATES,
    SAMPLE_COMPOSITION_STATES,
    CallState,
)
from insider.config import CONFIG
from insider.corpus.records import Transaction
from insider.paths import DISPERSION_DB

SRC = Path(__file__).resolve().parents[1] / "src" / "insider"
CONFIG_FILE = SRC / "config.py"
POWER = SRC / "power"

SEAL_TOKENS = ("SEALED_DB", "insider_sealed")
SEAL_MENTION_ALLOWED = {
    SRC / "paths.py",  # defines the path
    SRC / "portfolio" / "returns.py",  # writes, never reads
    SRC / "eval" / "evaluator.py",  # the one reader
}
SEAL_READER = SRC / "eval" / "evaluator.py"

# A field or function whose name says first moment. The compound rule catches a
# first moment OF A RETURN SERIES, which is what must never leave the power
# package. book_width_mean is a count statistic and is deliberately allowed.
FIRST_MOMENT_EXACT = frozenset(
    {"mean", "average", "avg", "alpha", "mu", "drift", "first_moment", "expectation"}
)
FIRST_MOMENT_A = ("mean", "avg", "average", "expected", "expectation")
FIRST_MOMENT_B = ("return", "excess", "alpha")

DISPERSION_FIELDS = (
    "hold_sessions",
    "weighting",
    "n_sessions",
    "sd_daily_excess",
    "annualized_tracking_error",
    "newey_west_lags",
    "variance_inflation",
    "effective_periods",
    "autocorr_lag_1",
    "autocorr_lag_5",
    "autocorr_lag_21",
    "book_width_mean",
    "book_width_min",
    "book_width_p10",
    "book_width_p50",
    "book_width_p90",
    "book_width_max",
)
MDE_FIELDS = (
    "hold_sessions",
    "weighting",
    "n_sessions",
    "effective_periods",
    "sd_daily_excess",
    "annualized_tracking_error",
    "newey_west_lags",
    "variance_inflation",
    "standard_error_monthly_bp",
    "mde_bp_per_month",
)


def source_files() -> list[Path]:
    return sorted(p for p in SRC.rglob("*.py"))


def names_first_moment(name: str) -> bool:
    lowered = name.lower()
    if lowered in FIRST_MOMENT_EXACT:
        return True
    return any(a in lowered for a in FIRST_MOMENT_A) and any(b in lowered for b in FIRST_MOMENT_B)


# --------------------------------------------------------------------------
# Guard 1. Every config field has an enforcement site.
# Six Level 1 keys in AiTrader were parsed, validated, printed, enforced nowhere.
# MUTATION 5 removes the throttle's read of sec_requests_per_second.
# --------------------------------------------------------------------------


def referenced_names(path: Path) -> set[str]:
    """Every identifier the module actually reads, from the parse tree.

    Deliberately not a text search. A config key left behind in a comment while
    the code that read it was replaced by a literal is the exact shape of the
    six unenforced Level 1 keys, and a text search calls that enforcement.
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


def test_every_config_field_has_an_enforcement_site() -> None:
    names = [f.name for f in fields(CONFIG)]
    assert names, "the config declares no fields"
    read_anywhere: set[str] = set()
    for path in source_files():
        if path != CONFIG_FILE:
            read_anywhere |= referenced_names(path)
    unenforced = sorted(set(names) - read_anywhere)
    assert not unenforced, (
        f"config fields with no enforcement site anywhere under src/insider: {unenforced}. "
        f"A key enforced nowhere is decoration."
    )


def test_the_throttle_derives_its_interval_from_the_registered_rate() -> None:
    from insider.edgar.throttle import Throttle

    assert Throttle().min_interval_seconds == pytest.approx(1.0 / CONFIG.sec_requests_per_second)
    assert CONFIG.sec_requests_per_second < 10.0, "the SEC states a ceiling of ten per second"


# --------------------------------------------------------------------------
# Guard 2. The sealed store has exactly one reader.
# MUTATION 2 makes a non-evaluator module read it.
# --------------------------------------------------------------------------


def test_only_the_permitted_set_names_the_sealed_store() -> None:
    offenders = []
    for path in source_files():
        if path in SEAL_MENTION_ALLOWED:
            continue
        text = path.read_text(encoding="utf-8")
        if any(token in text for token in SEAL_TOKENS):
            offenders.append(str(path.relative_to(SRC)))
    assert not offenders, f"modules naming the sealed store outside the permitted set: {offenders}"


def test_read_sealed_returns_has_one_definition_and_no_outside_callers() -> None:
    definitions = []
    callers = []
    for path in source_files():
        text = path.read_text(encoding="utf-8")
        if "def read_sealed_returns" in text:
            definitions.append(path)
        if path != SEAL_READER and "read_sealed_returns(" in text:
            callers.append(str(path.relative_to(SRC)))
    assert definitions == [SEAL_READER], f"unexpected definitions: {definitions}"
    assert not callers, f"modules calling the sealed reader: {callers}"


def test_the_power_package_cannot_reach_a_realized_return() -> None:
    """The power path to raw returns does not exist, rather than being avoided."""
    forbidden = ("insider.portfolio", "insider.market", "insider.eval")
    offenders = []
    for path in sorted(POWER.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if (
                isinstance(node, ast.ImportFrom)
                and node.module
                and any(node.module.startswith(f) for f in forbidden)
            ):
                offenders.append(f"{path.name} imports {node.module}")
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if any(alias.name.startswith(f) for f in forbidden):
                        offenders.append(f"{path.name} imports {alias.name}")
    assert not offenders, f"the power package reached outside its boundary: {offenders}"


# --------------------------------------------------------------------------
# Guard 3. The power module is structurally incapable of emitting a mean.
# MUTATION 1 gives it a first moment to return.
# --------------------------------------------------------------------------


def test_the_power_dataclasses_carry_exactly_the_registered_fields() -> None:
    from insider.power.dispersion import DispersionStats
    from insider.power.mde import MdeResult

    assert tuple(f.name for f in fields(DispersionStats)) == DISPERSION_FIELDS
    assert tuple(f.name for f in fields(MdeResult)) == MDE_FIELDS


def test_no_name_in_the_power_package_says_first_moment_of_a_return() -> None:
    offenders = []
    for path in sorted(POWER.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                for item in node.body:
                    target = getattr(item, "target", None)
                    if (
                        isinstance(item, ast.AnnAssign)
                        and isinstance(target, ast.Name)
                        and names_first_moment(target.id)
                    ):
                        offenders.append(f"{path.name}:{node.name}.{target.id}")
            if isinstance(node, ast.FunctionDef) and names_first_moment(node.name):
                offenders.append(f"{path.name}:{node.name}()")
    assert not offenders, (
        f"the power package named a first moment of a return series: {offenders}. "
        f"It returns dispersion, counts, and the derived MDE, and nothing else."
    )


def test_the_power_package_never_calls_a_mean_or_a_sum_over_returns() -> None:
    """Catches the arithmetic even when the name is innocent."""
    offenders = []
    for path in sorted(POWER.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            called = func.attr if isinstance(func, ast.Attribute) else getattr(func, "id", "")
            if called in {"mean", "average", "nanmean"}:
                offenders.append(f"{path.name}: calls {called}()")
    assert not offenders, f"the power package computed a first moment: {offenders}"


@pytest.mark.skipif(not DISPERSION_DB.exists(), reason="the dispersion store has not been built")
def test_the_dispersion_store_holds_no_first_moment() -> None:
    """What is stored sums to zero, so the mean cannot be read back out."""
    con = sqlite3.connect(f"file:{DISPERSION_DB}?mode=ro", uri=True)
    try:
        columns = {r[1] for r in con.execute("PRAGMA table_info(centered_excess)")}
        assert columns == {"hold_sessions", "weighting", "date", "centered", "book_width"}
        rows = con.execute(
            "SELECT hold_sessions, weighting, SUM(centered), SUM(centered*centered), COUNT(*) "
            "FROM centered_excess GROUP BY 1, 2"
        ).fetchall()
    finally:
        con.close()
    assert rows, "the dispersion store is empty"
    for hold, weighting, total, sumsq, n in rows:
        scale = (sumsq / n) ** 0.5
        assert abs(total) < 1e-9 * scale * n, (
            f"hold {hold} {weighting} sums to {total:.3e}, which is not zero. "
            f"It carries a first moment."
        )


# --------------------------------------------------------------------------
# Guard 4. The eight call states are never merged.
# --------------------------------------------------------------------------


def test_eight_distinct_call_states() -> None:
    assert len(ALL_STATES) == 8, f"expected eight states, found {len(ALL_STATES)}"
    values = [s.value for s in ALL_STATES]
    assert len(set(values)) == 8, f"two states share a value: {values}"
    assert set(values) == {
        "parsed",
        "unparseable",
        "filtered_code",
        "filtered_role",
        "filtered_routine",
        "filtered_programmatic",
        "no_bar",
        "outside_universe",
    }


def test_operational_health_and_sample_composition_never_overlap() -> None:
    assert not (OPERATIONAL_HEALTH_STATES & SAMPLE_COMPOSITION_STATES)
    assert CallState.UNPARSEABLE in OPERATIONAL_HEALTH_STATES
    assert CallState.FILTERED_ROUTINE in SAMPLE_COMPOSITION_STATES
    assert CallState.FILTERED_ROUTINE not in OPERATIONAL_HEALTH_STATES


# --------------------------------------------------------------------------
# Guard 5. The ex-ante classification rule.
# MUTATION 3 admits a sale. MUTATION 4 admits a routine insider.
# --------------------------------------------------------------------------


def _txn(
    code: str = "P", roles: frozenset[str] = frozenset({"officer"}), value: float = 50_000.0
) -> Transaction:
    return Transaction(
        accession="0000000000-00-000000",
        issuer_cik=1,
        symbol="AAA",
        filer_cik=7,
        roles=roles,
        transaction_date=dt.date(2020, 5, 4),
        filing_date=dt.date(2020, 5, 6),
        code=code,
        shares=value / 10.0,
        price_per_share=10.0,
        aff10b5one=False,
    )


def test_purchases_only_a_sale_is_refused() -> None:
    from insider.corpus.classify import prefilter

    assert prefilter(_txn(code="P")).state is CallState.PARSED
    for code in ("S", "A", "M", "F", "G", "C"):
        verdict = prefilter(_txn(code=code))
        assert verdict.state is CallState.FILTERED_CODE, (
            f"transaction code {code} reached the portfolio. Purchases only, code P only."
        )
        assert verdict.reason == f"code_{code}"


def test_ten_percent_owners_are_refused_even_when_also_titled() -> None:
    from insider.corpus.classify import prefilter

    assert prefilter(_txn(roles=frozenset({"director"}))).state is CallState.PARSED
    strict = prefilter(_txn(roles=frozenset({"officer", "tenpercentowner"})))
    assert strict.state is CallState.FILTERED_ROLE
    assert strict.reason == "tenpercentowner_also_titled"
    assert prefilter(_txn(roles=frozenset())).state is CallState.FILTERED_ROLE


def test_the_dollar_floor_and_the_10b5_1_flag_are_enforced() -> None:
    from insider.corpus.classify import prefilter

    assert (
        prefilter(_txn(value=CONFIG.min_transaction_usd - 1)).state
        is CallState.FILTERED_PROGRAMMATIC
    )
    assert prefilter(_txn(value=CONFIG.min_transaction_usd)).state is CallState.PARSED


def test_a_routine_insider_is_refused_by_the_three_year_rule() -> None:
    from insider.corpus.routine import RoutineClass, TradeHistory, classify

    assert CONFIG.routine_consecutive_years == 3, "the registered rule is three years"
    history = TradeHistory()
    # Ample history, and exactly three consecutive prior Mays. The May run sits
    # on the registered boundary on purpose: a fixture carrying a fourth May
    # would survive a raised requirement and the guard would not fire.
    history.add(7, dt.date(2016, 1, 20))
    for year in (2017, 2018, 2019):
        history.add(7, dt.date(year, 5, 12))
    label = classify(history, 7, dt.date(2020, 5, 4))
    assert label is RoutineClass.ROUTINE, (
        "an insider who traded the same calendar month for three consecutive prior "
        "years is routine and must not reach the portfolio as opportunistic"
    )


def test_an_opportunistic_insider_passes_the_three_year_rule() -> None:
    from insider.corpus.routine import RoutineClass, TradeHistory, classify

    history = TradeHistory()
    for when in (dt.date(2016, 2, 3), dt.date(2017, 9, 8), dt.date(2018, 11, 2)):
        history.add(7, when)
    assert classify(history, 7, dt.date(2020, 5, 4)) is RoutineClass.OPPORTUNISTIC


def test_too_little_history_is_a_third_state_not_opportunistic() -> None:
    from insider.corpus.routine import RoutineClass, TradeHistory, classify

    history = TradeHistory()
    history.add(7, dt.date(2019, 1, 2))
    assert classify(history, 7, dt.date(2020, 5, 4)) is RoutineClass.INSUFFICIENT_HISTORY


def test_the_routine_pattern_is_tested_before_the_history_gate() -> None:
    """The pattern is the definition. The history gate governs the residual.

    An insider whose earliest observed trade is eight days short of three full
    years, but who traded the candidate month in each of the three prior years,
    is routine. Gating her on the calendar would file her as unclassifiable.
    """
    from insider.corpus.routine import RoutineClass, TradeHistory, classify

    history = TradeHistory()
    for year in (2017, 2018, 2019):
        history.add(7, dt.date(year, 5, 12))
    assert classify(history, 7, dt.date(2020, 5, 4)) is RoutineClass.ROUTINE


def test_the_routine_rule_reads_only_prior_years() -> None:
    """A trade after the candidate date cannot change the candidate's label."""
    from insider.corpus.routine import TradeHistory, classify

    base = TradeHistory()
    for year in (2016, 2017, 2018):
        base.add(7, dt.date(year, 5, 12))
    before = classify(base, 7, dt.date(2019, 5, 4))
    base.add(7, dt.date(2021, 5, 12))
    base.add(7, dt.date(2022, 5, 12))
    assert classify(base, 7, dt.date(2019, 5, 4)) is before


# --------------------------------------------------------------------------
# Guard 6. The operator prior blocks Stage B while it is empty.
# --------------------------------------------------------------------------


def test_the_registered_operator_prior_slot_is_still_empty_and_blocks_stage_b() -> None:
    from insider.registration_check import (
        OperatorPriorMissing,
        operator_prior,
        operator_prior_filled,
        require_operator_prior,
    )

    assert operator_prior() is None, "the operator prior must be written by the operator"
    assert not operator_prior_filled()
    with pytest.raises(OperatorPriorMissing):
        require_operator_prior()


def test_a_section_that_claims_a_prior_without_recording_one_is_blank(tmp_path: Path) -> None:
    from insider.registration_check import operator_prior_filled

    hollow = tmp_path / "REGISTRATION.md"
    hollow.write_text(
        "## Section 12. The operator prior, reserved\n\n"
        "The operator recorded his prior.\n\n## Section 13. States\n",
        encoding="utf-8",
    )
    assert not operator_prior_filled(hollow)


def test_a_recorded_prior_unblocks_stage_b(tmp_path: Path) -> None:
    from insider.registration_check import operator_prior, require_operator_prior

    filled = tmp_path / "REGISTRATION.md"
    filled.write_text(
        "## Section 12. The operator prior, reserved\n\n"
        "> Operator prior, probability that net alpha survives: 0.07\n\n"
        "## Section 13. States\n",
        encoding="utf-8",
    )
    assert operator_prior(filled) == pytest.approx(0.07)
    assert require_operator_prior(filled) == pytest.approx(0.07)


def test_the_evaluator_refuses_before_it_opens_the_seal() -> None:
    """The refusal is produced, not asserted."""
    from insider.eval.evaluator import read_sealed_returns
    from insider.registration_check import OperatorPriorMissing

    with pytest.raises(OperatorPriorMissing):
        read_sealed_returns(CONFIG.primary_hold_sessions, CONFIG.primary_weighting)
