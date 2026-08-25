"""Credentials load or refuse loudly. Never silently."""
from pathlib import Path

import pytest

from hfexperiment.envfile import (
    MissingCredentialsError,
    load_credentials,
    parse_env,
)


def test_missing_env_file_is_blocked_on_operator(tmp_path: Path) -> None:
    with pytest.raises(MissingCredentialsError, match="BLOCKED-ON-OPERATOR"):
        load_credentials(tmp_path / ".env")


def test_missing_key_is_blocked_on_operator(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text("ALPACA_KEY_ID=abc\n")
    with pytest.raises(MissingCredentialsError, match="ALPACA_SECRET_KEY"):
        load_credentials(env)


def test_present_keys_load(tmp_path: Path) -> None:
    env = tmp_path / ".env"
    env.write_text(
        "# comment\nALPACA_KEY_ID=abc\nALPACA_SECRET_KEY='xyz'\nOTHER=1\n"
    )
    creds = load_credentials(env)
    assert creds == {"ALPACA_KEY_ID": "abc", "ALPACA_SECRET_KEY": "xyz"}


def test_parse_env_skips_comments_and_blanks() -> None:
    parsed = parse_env("\n# a\nX=1\n  Y = \"2\" \nnoequals\n")
    assert parsed == {"X": "1", "Y": "2"}
