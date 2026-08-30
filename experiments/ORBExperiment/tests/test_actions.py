"""The corporate-actions substrate. Symbols and dates; no price anywhere."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from orb.actions import ActionKind, ActionsSubstrate, CorporateAction
from orb.ledger import AppendOnlyLedger, TruncatedLedgerLine

SPLIT = CorporateAction(
    "AAPL", ActionKind.SPLIT, date(2020, 8, 31), ratio_numerator=4, ratio_denominator=1
)
DELIST = CorporateAction("XYZQ", ActionKind.DELISTING, date(2019, 5, 2))
RENAME = CorporateAction(
    "FB", ActionKind.SYMBOL_CHANGE, date(2022, 6, 9), new_ticker="META"
)


def _substrate(tmp_path: Path) -> tuple[ActionsSubstrate, AppendOnlyLedger]:
    ledger = AppendOnlyLedger(tmp_path / "actions.jsonl")
    return ActionsSubstrate(ledger), ledger


def test_actions_append_durably(tmp_path: Path) -> None:
    substrate, ledger = _substrate(tmp_path)
    assert substrate.record([SPLIT, DELIST, RENAME]) == 3
    rows = [r for r in ledger.read() if not isinstance(r, TruncatedLedgerLine)]
    assert len(rows) == 3
    assert rows[0]["ticker"] == "AAPL"
    assert rows[2]["new_ticker"] == "META"


def test_a_split_produces_the_session_ticker_key_it_would_collide_with() -> None:
    """This key is what lets a measured revision be attributed to an action."""
    substrate = ActionsSubstrate(AppendOnlyLedger(Path("/dev/null")))
    keys = substrate.collision_keys([SPLIT, DELIST, RENAME])
    assert keys == frozenset({"AAPL/2020-08-31"})


def test_a_delisting_is_not_a_rewrite_hazard_key() -> None:
    """Only splits and reverse splits rewrite an already-served bar."""
    substrate = ActionsSubstrate(AppendOnlyLedger(Path("/dev/null")))
    assert DELIST.key() not in substrate.collision_keys([DELIST])


def test_counts_by_kind_covers_every_kind_including_the_zeros() -> None:
    """A zero that was counted is different from a kind nobody looked for."""
    substrate = ActionsSubstrate(AppendOnlyLedger(Path("/dev/null")))
    counts = substrate.counts_by_kind([SPLIT, DELIST])
    assert set(counts) == {k.value for k in ActionKind}
    assert counts["split"] == 1
    assert counts["delisting"] == 1
    assert counts["reverse_split"] == 0
    assert counts["listing"] == 0


def test_delistings_per_year_respects_the_registered_window() -> None:
    substrate = ActionsSubstrate(AppendOnlyLedger(Path("/dev/null")))
    actions = [
        DELIST,
        CorporateAction("AAA", ActionKind.DELISTING, date(2015, 1, 2)),  # before
        CorporateAction("BBB", ActionKind.DELISTING, date(2026, 12, 1)),  # after
        CorporateAction("CCC", ActionKind.DELISTING, date(2019, 9, 9)),
    ]
    per_year = substrate.delistings_per_year(
        actions, date(2016, 1, 4), date(2026, 6, 30)
    )
    assert per_year == {2019: 2}


def test_no_action_field_is_a_priced_bar_field() -> None:
    """The substrate is symbols and dates. Guard 5 has nothing to catch here."""
    import dataclasses

    from orb.fields import PRICED_BAR_FIELDS

    for field in dataclasses.fields(CorporateAction):
        assert field.name not in PRICED_BAR_FIELDS, field.name
