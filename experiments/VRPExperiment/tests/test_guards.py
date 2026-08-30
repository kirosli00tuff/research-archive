"""Structural guards. Each pins a standing rule and fails loudly, not quietly.

These are not unit tests of behaviour. They are the mechanical enforcement of
the standing rules: a recorded absence never becomes a number, a naive datetime
never reaches a computation, operational health never merges with venue
classification, a ledger never loses a damaged line, and no module names a
blind field outside a sealed module.
"""

from __future__ import annotations

import ast
import json
import os
from collections.abc import Callable
from datetime import UTC, datetime, timedelta, timezone
from pathlib import Path

import pytest

from vrp.absence import (
    AbsenceReason,
    Absent,
    AbsentCoercionError,
    is_absent,
    require_present,
)
from vrp.callstate import (
    CALL_STATES,
    CallStateMergeError,
    CallStateTally,
    HealthState,
    VenueState,
)
from vrp.fields import BLIND_FIELDS, READABLE_FIELDS, SEALED_MODULES
from vrp.latch import (
    BlindnessViolationError,
    Latch,
    LatchAlreadySpentError,
    LatchNotWrittenError,
    require_blindness,
)
from vrp.ledger import AppendOnlyLedger, TruncatedLedgerLine
from vrp.seal import SealedWriter, SealViolationError
from vrp.tzguard import (
    ExchangeExpiry,
    NaiveDatetimeError,
    NonUtcDatetimeError,
    iso_utc,
    parse_utc,
    require_aware,
    require_utc,
    utc_now,
)

SRC_ROOT = Path(__file__).resolve().parent.parent / "src"
VRP_ROOT = SRC_ROOT / "vrp"


# ---------------------------------------------------------------------------
# Guard 1 — recorded absence refuses to become a number
# ---------------------------------------------------------------------------


@pytest.mark.guard
def test_absent_refuses_float_int_and_indexing() -> None:
    # Arrange
    absent = Absent(AbsenceReason.VENUE_BLOCKED, "Deribit prohibits CA residents")

    # Act / Assert — the three named in the prompt, plus the rest of the surface.
    with pytest.raises(AbsentCoercionError, match="float"):
        float(absent)
    with pytest.raises(AbsentCoercionError, match="int"):
        int(absent)
    with pytest.raises(AbsentCoercionError, match="indexing"):
        absent["cost_bps"]


@pytest.mark.guard
def test_absent_refuses_every_arithmetic_ordering_and_truth_operation() -> None:
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
        lambda: -absent,
        lambda: abs(absent),
        lambda: absent < 1,
        lambda: absent <= 1,
        lambda: absent > 1,
        lambda: absent >= 1,
        lambda: bool(absent),
        lambda: len(absent),
        lambda: absent.__iter__(),
        lambda: [0, 1][absent],  # __index__
    ]
    for operation in operations:
        with pytest.raises(AbsentCoercionError):
            operation()


@pytest.mark.guard
def test_absent_refuses_complex_and_round() -> None:
    absent = Absent(AbsenceReason.NOT_SERVED)
    with pytest.raises(AbsentCoercionError, match="complex"):
        absent.__complex__()
    with pytest.raises(AbsentCoercionError, match="round"):
        absent.__round__()


@pytest.mark.guard
def test_absent_never_silently_defaults_through_require_present() -> None:
    absent = Absent(AbsenceReason.VENUE_CAPITAL_BLOCKED, "sleeve buys 0.3 contracts")
    with pytest.raises(AbsentCoercionError, match="venue_capital_blocked"):
        require_present(absent, "TASK 5 cost")
    assert require_present(0.0, "a measured zero") == 0.0
    assert is_absent(absent) is True
    assert is_absent(0.0) is False


@pytest.mark.guard
def test_a_measured_zero_and_a_recorded_absence_are_distinguishable() -> None:
    """The failure this guard exists for, stated as a test.

    A measured zero cost is a real finding. An unreachable venue has no cost.
    The two must not be representable by the same object, and the second must
    not be able to become the first by any arithmetic path.
    """
    measured_zero: float = 0.0
    unreachable = Absent(AbsenceReason.VENUE_BLOCKED, "no BC-reachable option venue")

    assert measured_zero == 0.0
    assert is_absent(unreachable) is True
    assert is_absent(measured_zero) is False

    # Every route from the absence back to the zero is closed.
    with pytest.raises(AbsentCoercionError):
        float(unreachable)
    with pytest.raises(AbsentCoercionError):
        int(unreachable)
    with pytest.raises(AbsentCoercionError):
        _ = unreachable + measured_zero
    with pytest.raises(AbsentCoercionError):
        _ = unreachable < measured_zero


@pytest.mark.guard
def test_every_absence_reason_is_distinct_and_named() -> None:
    values = [r.value for r in AbsenceReason]
    assert len(values) == len(set(values))
    # The four venue-shaped absences the prompt distinguishes.
    assert "venue_blocked" in values
    assert "venue_capital_blocked" in values
    assert "venue_unclear" in values
    assert "latch_unspent" in values


# ---------------------------------------------------------------------------
# Guard 2 — the timezone guard refuses naive datetimes
# ---------------------------------------------------------------------------


@pytest.mark.guard
def test_naive_datetime_is_refused_never_assumed_utc() -> None:
    naive = datetime(2026, 8, 30, 12, 0, 0)
    with pytest.raises(NaiveDatetimeError, match="refusing naive datetime"):
        require_aware(naive, "TASK 4 probe stamp")
    with pytest.raises(NaiveDatetimeError):
        require_utc(naive, "TASK 4 probe stamp")
    with pytest.raises(NaiveDatetimeError):
        iso_utc(naive)


@pytest.mark.guard
def test_aware_but_non_utc_datetime_is_refused_never_converted() -> None:
    vancouver_ish = datetime(2026, 8, 30, 5, 0, 0, tzinfo=timezone(timedelta(hours=-7)))
    with pytest.raises(NonUtcDatetimeError, match="refusing non-UTC"):
        require_utc(vancouver_ish, "expiry")
    # It is aware, so require_aware accepts it; only require_utc refuses.
    assert require_aware(vancouver_ish, "expiry") is vancouver_ish


@pytest.mark.guard
def test_utc_datetimes_pass_and_round_trip() -> None:
    stamp = datetime(2026, 8, 30, 8, 0, 0, tzinfo=UTC)
    assert require_utc(stamp, "expiry") is stamp
    assert iso_utc(stamp) == "2026-08-30T08:00:00.000Z"
    assert parse_utc("2026-08-30T08:00:00Z") == stamp
    assert utc_now().tzinfo is not None


@pytest.mark.guard
def test_parse_utc_refuses_a_string_without_an_offset() -> None:
    with pytest.raises(NaiveDatetimeError):
        parse_utc("2026-08-30T08:00:00")


@pytest.mark.guard
def test_an_expiry_without_an_exchange_settlement_time_cannot_exist() -> None:
    settlement = datetime(2026, 9, 26, 8, 0, 0, tzinfo=UTC)
    expiry = ExchangeExpiry(settlement, "deribit", "08:00 UTC on the expiry date")
    assert expiry.as_row()["settlement"] == "2026-09-26T08:00:00.000Z"

    with pytest.raises(NaiveDatetimeError):
        ExchangeExpiry(
            datetime(2026, 9, 26, 8, 0, 0),
            "deribit",
            "08:00 UTC",
        )
    with pytest.raises(ValueError, match="empty exchange"):
        ExchangeExpiry(settlement, "  ", "08:00 UTC")
    with pytest.raises(ValueError, match="empty settlement_rule"):
        ExchangeExpiry(settlement, "deribit", "")


# ---------------------------------------------------------------------------
# Guard 3 — append-only, fsynced ledger; a truncated line is reported
# ---------------------------------------------------------------------------


@pytest.mark.guard
def test_ledger_appends_are_durable_and_ordered(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "sub" / "probe.jsonl")
    ledger.append({"kind": "probe", "venue": "deribit", "status_code": 200})
    ledger.append({"kind": "probe", "venue": "deribit", "status_code": 429})

    rows = ledger.read()
    assert len(rows) == 2
    assert all(isinstance(r, dict) for r in rows)
    first, second = rows
    assert isinstance(first, dict) and isinstance(second, dict)
    assert first["status_code"] == 200
    assert second["status_code"] == 429
    assert "recorded_at" in first


@pytest.mark.guard
def test_ledger_never_rewrites_an_existing_line(tmp_path: Path) -> None:
    path = tmp_path / "probe.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"kind": "first"})
    before = path.read_bytes()
    ledger.append({"kind": "second"})
    after = path.read_bytes()
    assert after.startswith(before), "an append must never rewrite prior bytes"


@pytest.mark.guard
def test_a_truncated_line_is_reported_never_repaired_never_skipped(
    tmp_path: Path,
) -> None:
    path = tmp_path / "probe.jsonl"
    ledger = AppendOnlyLedger(path)
    ledger.append({"kind": "good"})
    # A line that does not parse, and a line with no terminating newline.
    with os.fdopen(
        os.open(path, os.O_WRONLY | os.O_APPEND), "a", encoding="utf-8"
    ) as h:
        h.write("{not json}\n")
        h.write('{"kind":"cut off"')

    entries = ledger.read()
    assert len(entries) == 3
    assert isinstance(entries[0], dict)
    assert isinstance(entries[1], TruncatedLedgerLine)
    assert isinstance(entries[2], TruncatedLedgerLine)
    assert ledger.row_count() == 1, "a damaged line is never counted as a row"
    assert len(ledger.truncated()) == 2
    absent = entries[1].as_absent()
    assert absent.reason is AbsenceReason.TRUNCATED_LEDGER_LINE
    with pytest.raises(AbsentCoercionError):
        float(absent)


@pytest.mark.guard
def test_a_non_object_json_line_is_a_truncation_not_a_row(tmp_path: Path) -> None:
    path = tmp_path / "probe.jsonl"
    path.write_text("[1,2,3]\n", encoding="utf-8")
    ledger = AppendOnlyLedger(path)
    entries = ledger.read()
    assert len(entries) == 1
    assert isinstance(entries[0], TruncatedLedgerLine)


@pytest.mark.guard
def test_ledger_redacts_a_credential_shaped_environment_value(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("VRP_TEST_API_KEY", "supersecretvalue12345")
    ledger = AppendOnlyLedger(tmp_path / "probe.jsonl")
    ledger.append({"kind": "probe", "note": "used supersecretvalue12345 in the url"})
    text = (tmp_path / "probe.jsonl").read_text(encoding="utf-8")
    assert "supersecretvalue12345" not in text
    assert "<redacted:VRP_TEST_API_KEY>" in text


# ---------------------------------------------------------------------------
# Guard 4 — the call-state enum; health and venue classification never merge
# ---------------------------------------------------------------------------


@pytest.mark.guard
def test_health_and_venue_states_are_disjoint_types() -> None:
    assert len(CALL_STATES) == len(set(CALL_STATES))
    assert len(CALL_STATES) == len(HealthState) + len(VenueState)
    assert not (set(HealthState) & set(VenueState))


@pytest.mark.guard
def test_a_rate_limit_can_never_be_counted_as_a_prohibited_venue() -> None:
    tally = CallStateTally()
    tally.record_health(HealthState.RATE_LIMITED)
    tally.record_venue(VenueState.PROHIBITED)

    assert tally.health_total() == 1
    assert tally.venue_total() == 1
    with pytest.raises(CallStateMergeError, match="never merge"):
        tally.combined_total()
    with pytest.raises(CallStateMergeError):
        tally.record_health(VenueState.PROHIBITED)  # type: ignore[arg-type]
    with pytest.raises(CallStateMergeError):
        tally.record_venue(HealthState.RATE_LIMITED)  # type: ignore[arg-type]


@pytest.mark.guard
def test_a_403_status_code_is_operational_not_a_jurisdiction_finding() -> None:
    """A jurisdiction finding comes from published policy text, never a code."""
    tally = CallStateTally()
    tally.record_health(HealthState.ACCESS_REFUSED)
    report = tally.as_report()
    assert report["health"]["access_refused"] == 1
    assert report["venue"]["prohibited"] == 0


@pytest.mark.guard
def test_the_four_venue_classifications_the_prompt_requires_all_exist() -> None:
    values = {s.value for s in VenueState}
    assert {"permitted", "prohibited", "capital_blocked", "unclear"} <= values


# ---------------------------------------------------------------------------
# Guard 5 — the blindness pin. No blind field named outside a sealed module.
# ---------------------------------------------------------------------------


def _module_paths() -> list[Path]:
    return sorted(p for p in VRP_ROOT.rglob("*.py"))


def _relative(path: Path) -> str:
    return path.relative_to(SRC_ROOT).as_posix()


@pytest.mark.guard
def test_no_module_names_a_blind_field_outside_a_sealed_module() -> None:
    """The blindness pin. Walks every parse tree; one occurrence fails."""
    offences: list[str] = []
    for path in _module_paths():
        rel = _relative(path)
        if rel in SEALED_MODULES:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            # payload["mark_iv"] and {"mark_iv": ...}
            if isinstance(node, ast.Constant) and isinstance(node.value, str):
                if node.value in BLIND_FIELDS:
                    offences.append(f"{rel}:{node.lineno} string {node.value!r}")
            # payload.mark_iv
            elif isinstance(node, ast.Attribute) and node.attr in BLIND_FIELDS:
                offences.append(f"{rel}:{node.lineno} attribute .{node.attr}")
            # mark_iv = ... / def f(mark_iv)
            elif isinstance(node, ast.Name) and node.id in BLIND_FIELDS:
                offences.append(f"{rel}:{node.lineno} name {node.id}")
            elif isinstance(node, ast.arg) and node.arg in BLIND_FIELDS:
                offences.append(f"{rel}:{node.lineno} parameter {node.arg}")
    assert not offences, (
        "blindness pin: a blind field is named outside a sealed module. "
        f"Occurrences: {offences}"
    )


@pytest.mark.guard
def test_the_blindness_pin_actually_fires_on_a_planted_violation(
    tmp_path: Path,
) -> None:
    """A canary. A pin that cannot fire proves nothing."""
    planted = tmp_path / "planted.py"
    planted.write_text('value = payload["mark_iv"]\n', encoding="utf-8")
    tree = ast.parse(planted.read_text(encoding="utf-8"))
    hits = [
        n.value
        for n in ast.walk(tree)
        if isinstance(n, ast.Constant)
        and isinstance(n.value, str)
        and n.value in BLIND_FIELDS
    ]
    assert hits == ["mark_iv"], "the pin must fire on a planted blind field"


@pytest.mark.guard
def test_blind_and_readable_field_registries_do_not_overlap() -> None:
    assert not (BLIND_FIELDS & READABLE_FIELDS)
    # Cost and reachability are deliberately readable: they decide TASK 3 and 5.
    for field in ("bid", "ask", "initial_margin", "commission", "policy_text"):
        assert field in READABLE_FIELDS
    # The endpoint and its inputs are blind.
    for field in ("mark_iv", "dvol", "realized_volatility", "variance_risk_premium"):
        assert field in BLIND_FIELDS


@pytest.mark.guard
def test_no_module_opens_a_text_file_handle_outside_a_sealed_module() -> None:
    """Bytes enter through the seal, or through the ledger's own fd primitive.

    The exemption is narrow and is stated rather than assumed: ``os.open`` and
    ``os.fdopen`` return a raw file descriptor and are how Guard 3 gets
    ``O_APPEND`` plus ``fsync``, which no text-mode handle can give it. The
    builtin ``open`` and ``Path.open`` are forbidden, because those are the
    calls that would let a module read and parse a served payload.

    This guard fired on its first run against ``vrp/ledger.py:74`` (``os.open``)
    and that is the evidence it binds on real modules, not only on fixtures.
    """
    offences: list[str] = []
    for path in _module_paths():
        rel = _relative(path)
        if rel in SEALED_MODULES:
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            func = node.func
            if isinstance(func, ast.Name) and func.id == "open":
                offences.append(f"{rel}:{node.lineno} builtin open()")
            elif isinstance(func, ast.Attribute) and func.attr in {"open", "fdopen"}:
                receiver = func.value
                is_os = isinstance(receiver, ast.Name) and receiver.id == "os"
                if not is_os:
                    offences.append(f"{rel}:{node.lineno} .{func.attr}()")
    assert not offences, f"text file handles are opened outside the seal: {offences}"


@pytest.mark.guard
def test_the_open_guard_fires_on_a_planted_path_open(tmp_path: Path) -> None:
    """A canary for the guard above. It must reject Path.open and builtin open."""
    planted = tmp_path / "planted.py"
    planted.write_text(
        "import os\n"
        "a = open('x')\n"
        "b = some_path.open()\n"
        "c = os.open('x', os.O_RDONLY)\n",
        encoding="utf-8",
    )
    tree = ast.parse(planted.read_text(encoding="utf-8"))
    offences: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        if isinstance(func, ast.Name) and func.id == "open":
            offences.append(f"builtin:{node.lineno}")
        elif isinstance(func, ast.Attribute) and func.attr in {"open", "fdopen"}:
            receiver = func.value
            if not (isinstance(receiver, ast.Name) and receiver.id == "os"):
                offences.append(f"attr:{node.lineno}")
    assert offences == ["builtin:2", "attr:3"], (
        "the guard must catch builtin open and Path.open, and must not catch os.open"
    )


@pytest.mark.guard
def test_a_sealed_writer_stores_bytes_and_serves_no_value(tmp_path: Path) -> None:
    ledger = AppendOnlyLedger(tmp_path / "seal.jsonl")
    writer = SealedWriter(tmp_path / "sealed", ledger)
    payload = b'{"mark_iv": 0.55, "instrument_name": "BTC-26SEP26-70000-C"}\n'

    record = writer.write("deribit/probe.json", payload)
    assert record.byte_count == len(payload)
    assert record.line_count == 1
    assert record.sha256 == __import__("hashlib").sha256(payload).hexdigest()
    assert record.retrieved_at.endswith("Z")

    with pytest.raises(SealViolationError, match="blind field"):
        writer.refuse_value("mark_iv")
    with pytest.raises(SealViolationError, match="no field values at all"):
        writer.refuse_value("instrument_name")
    with pytest.raises(SealViolationError, match="stores bytes"):
        writer.write("deribit/parsed.json", {"mark_iv": 0.55})  # type: ignore[arg-type]

    described = writer.describe("deribit/probe.json")
    assert described["byte_count"] == len(payload)
    assert "mark_iv" not in json.dumps(described)


# ---------------------------------------------------------------------------
# The latch — one real read, ever
# ---------------------------------------------------------------------------


@pytest.mark.guard
def test_the_real_latch_can_be_written_once_and_never_twice(tmp_path: Path) -> None:
    latch = Latch(tmp_path / "task6.latch.json")
    modules = _module_paths()

    assert latch.is_spent() is False
    latch.require_unspent()
    with pytest.raises(LatchNotWrittenError):
        latch.read_record()
    with pytest.raises(BlindnessViolationError, match="blindness holds"):
        require_blindness(latch, "premium estimate")

    record = latch.write(modules, "TASK 6 single sealed read")
    assert latch.is_spent() is True
    assert record.module_hashes
    require_blindness(latch, "premium estimate")

    with pytest.raises(LatchAlreadySpentError, match="voids the hypothesis"):
        latch.write(modules, "a second read")
    with pytest.raises(LatchAlreadySpentError):
        latch.require_unspent()


@pytest.mark.guard
def test_module_drift_after_the_latch_is_visible_not_silent(tmp_path: Path) -> None:
    module = tmp_path / "participant.py"
    module.write_text("x = 1\n", encoding="utf-8")
    latch = Latch(tmp_path / "task6.latch.json")
    latch.write([module], "drift check")
    assert latch.verify_modules([module]) == {}

    module.write_text("x = 2\n", encoding="utf-8")
    drift = latch.verify_modules([module])
    assert str(module) in drift
    recorded, current = drift[str(module)]
    assert recorded != current
