"""The SEC access layer. Throttle, contact header, cache, and date parsing."""

from __future__ import annotations

import datetime as dt
import time

import pytest

from insider.config import CONFIG
from insider.edgar.bulk import parse_dera_date, quarter_url, quarters
from insider.edgar.client import UserAgentMissing, user_agent
from insider.edgar.fullindex import form_index_url
from insider.edgar.throttle import Throttle


def test_the_throttle_holds_the_registered_rate() -> None:
    throttle = Throttle()
    throttle.wait()
    started = time.monotonic()
    for _ in range(3):
        throttle.wait()
    elapsed = time.monotonic() - started
    assert elapsed >= 3 * throttle.min_interval_seconds * 0.9


def test_a_non_positive_rate_is_refused() -> None:
    from dataclasses import replace

    with pytest.raises(ValueError, match="must be positive"):
        Throttle(replace(CONFIG, sec_requests_per_second=0.0))


def test_a_user_agent_without_a_contact_email_is_refused(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv(CONFIG.sec_user_agent_env, "InsiderExperiment")
    with pytest.raises(UserAgentMissing, match="contact email"):
        user_agent()
    monkeypatch.delenv(CONFIG.sec_user_agent_env, raising=False)
    with pytest.raises(UserAgentMissing):
        user_agent()
    monkeypatch.setenv(CONFIG.sec_user_agent_env, "InsiderExperiment a@b.com")
    assert user_agent() == "InsiderExperiment a@b.com"


def test_the_registered_quarter_span_is_enumerated_without_gaps() -> None:
    tags = quarters()
    assert tags[0] == CONFIG.dera_first_quarter
    assert tags[-1] == CONFIG.dera_last_quarter
    assert len(tags) == 53
    assert "2013q4" in tags and "2014q1" in tags


def test_the_urls_are_the_free_sec_endpoints() -> None:
    assert quarter_url("2024q1").startswith("https://www.sec.gov/files/structureddata/")
    assert form_index_url("2024q1") == (
        "https://www.sec.gov/Archives/edgar/full-index/2024/QTR1/form.idx"
    )


def test_a_blank_date_parses_to_none_rather_than_a_substituted_date() -> None:
    assert parse_dera_date("31-JAN-2024") == dt.date(2024, 1, 31)
    for bad in ("", "   ", "2024-01-31", "31-XXX-2024", "32-JAN-2024"):
        assert parse_dera_date(bad) is None, f"{bad!r} produced a date"


def test_role_normalization_reads_an_unknown_string_as_no_roles() -> None:
    from insider.corpus.classify import normalize_roles

    assert normalize_roles("Director") == frozenset({"director"})
    assert normalize_roles("Director|Officer") == frozenset({"director", "officer"})
    assert normalize_roles("TenPercentOwner") == frozenset({"tenpercentowner"})
    assert normalize_roles("") == frozenset()
    assert normalize_roles("!!!") == frozenset()
