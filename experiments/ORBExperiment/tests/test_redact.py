"""Guard 8 unit tests — the redactor, and the credential store around it."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from orb.credentials import (
    CREDENTIAL_NAMES,
    CredentialMissingError,
    CredentialPresence,
    CredentialStore,
    load_credentials,
    parse_env_file,
)
from orb.redact import (
    MIN_REDACTABLE_LENGTH,
    Redactor,
    SecretTooShortError,
    active_redactor,
    install_redactor,
    placeholder_for,
    redact_data,
    redact_row,
    redact_text,
)

SECRET_A = "AAAA-secret-value-one-0123456789"
SECRET_B = "BBBB-secret-value-two-9876543210-longer"


@pytest.fixture(autouse=True)
def _restore_empty_redactor() -> object:
    """Leave the process-wide redactor as it was found. Tests share a process."""
    yield None
    install_redactor(Redactor({}))


def test_a_registered_secret_becomes_a_placeholder_naming_its_variable() -> None:
    # Arrange
    redactor = Redactor({"ORB_ONE": SECRET_A})
    # Act
    out = redactor.text(f"refused: key {SECRET_A} is unknown")
    # Assert
    assert SECRET_A not in out
    assert placeholder_for("ORB_ONE") in out


def test_the_longest_needle_wins_so_a_contained_secret_is_replaced_whole() -> None:
    # Arrange — one secret is a strict prefix of the other.
    short = "PREFIX-secret-0123456789"
    long = short + "-EXTENDED"
    redactor = Redactor({"ORB_SHORT": short, "ORB_LONG": long})
    # Act
    out = redactor.text(f"body carries {long} here")
    # Assert — the long one replaced whole, leaving no fragment behind.
    assert out == f"body carries {placeholder_for('ORB_LONG')} here"


def test_a_percent_encoded_secret_is_redacted_too() -> None:
    # Arrange — a secret whose URL-encoded form differs from its raw form.
    secret = "slash/and+plus=equals-0123456789"
    redactor = Redactor({"ORB_URLY": secret})
    import urllib.parse

    encoded = urllib.parse.quote(secret, safe="")
    assert encoded != secret
    # Act
    out = redactor.text(f"https://x.invalid/?apiKey={encoded}")
    # Assert
    assert encoded not in out
    assert placeholder_for("ORB_URLY") in out


def test_a_secret_shorter_than_the_floor_is_refused_not_redacted() -> None:
    # Arrange — one character below the floor, sitting exactly on the boundary.
    too_short = "x" * (MIN_REDACTABLE_LENGTH - 1)
    # Act / Assert
    with pytest.raises(SecretTooShortError, match="below the"):
        Redactor({"ORB_TINY": too_short})


def test_a_secret_exactly_on_the_floor_is_accepted() -> None:
    # Arrange — the boundary fixture sits ON the boundary, not comfortably inside.
    on_floor = "y" * MIN_REDACTABLE_LENGTH
    # Act
    redactor = Redactor({"ORB_FLOOR": on_floor})
    # Assert
    assert redactor.text(on_floor) == placeholder_for("ORB_FLOOR")


def test_redaction_is_deterministic_so_byte_comparison_survives_it() -> None:
    """A.1 TASK 3 compares stored bytes across two pulls 14 days apart."""
    # Arrange
    redactor = Redactor({"ORB_ONE": SECRET_A})
    first = f'{{"error":"key {SECRET_A}","bar":1}}'.encode()
    second = f'{{"error":"key {SECRET_A}","bar":1}}'.encode()
    third = f'{{"error":"key {SECRET_A}","bar":2}}'.encode()
    # Act
    a, b, c = redactor.data(first), redactor.data(second), redactor.data(third)
    # Assert — equal payloads stay equal, differing payloads stay different.
    assert a == b
    assert a != c


def test_a_nested_ledger_row_is_redacted_in_keys_values_and_sequences() -> None:
    # Arrange
    redactor = Redactor({"ORB_ONE": SECRET_A})
    row = {
        f"key-{SECRET_A}": {"inner": [f"a{SECRET_A}", 3, None]},
        "plain": 1,
    }
    # Act
    out = json.dumps(redactor.row(row), sort_keys=True)
    # Assert
    assert SECRET_A not in out
    assert placeholder_for("ORB_ONE") in out


def test_an_empty_redactor_is_an_identity_function_not_a_bypass() -> None:
    # Arrange
    redactor = Redactor({})
    # Act / Assert
    assert redactor.text("nothing to hide") == "nothing to hide"
    assert redactor.secret_count == 0
    assert redactor.names == ()


def test_a_redactor_never_reveals_a_value_in_its_own_repr() -> None:
    # Arrange
    redactor = Redactor({"ORB_ONE": SECRET_A, "ORB_TWO": SECRET_B})
    # Act
    shown = repr(redactor)
    # Assert
    assert SECRET_A not in shown
    assert SECRET_B not in shown
    assert "ORB_ONE" in shown


def test_the_module_level_helpers_use_the_installed_redactor() -> None:
    # Arrange
    install_redactor(Redactor({"ORB_ONE": SECRET_A}))
    # Act / Assert
    assert SECRET_A not in redact_text(SECRET_A)
    assert SECRET_A.encode() not in redact_data(SECRET_A.encode())
    assert SECRET_A not in json.dumps(redact_row({"a": SECRET_A}))
    assert active_redactor().names == ("ORB_ONE",)


# --- the credential store -------------------------------------------------


def test_presence_records_a_name_a_flag_and_a_length_and_nothing_else() -> None:
    # Arrange
    store = CredentialStore(dict.fromkeys(CREDENTIAL_NAMES, SECRET_A))
    # Act
    rows = [p.as_row() for p in store.presence()]
    # Assert
    assert len(rows) == 3
    blob = json.dumps(rows)
    assert SECRET_A not in blob
    assert all(r["character_length"] == len(SECRET_A) for r in rows)


def test_a_store_repr_carries_lengths_and_no_values() -> None:
    # Arrange
    store = CredentialStore({CREDENTIAL_NAMES[0]: SECRET_A})
    # Act
    shown = repr(store)
    # Assert
    assert SECRET_A not in shown
    assert f"len={len(SECRET_A)}" in shown


def test_require_refuses_loudly_rather_than_falling_back_to_no_credential() -> None:
    # Arrange
    store = CredentialStore({})
    # Act / Assert
    with pytest.raises(CredentialMissingError, match="recorded absence"):
        store.require(CREDENTIAL_NAMES[0])


def test_missing_names_every_absent_credential() -> None:
    # Arrange
    store = CredentialStore({CREDENTIAL_NAMES[0]: SECRET_A})
    # Act / Assert
    assert store.missing() == list(CREDENTIAL_NAMES[1:])


def test_parse_env_file_strips_quotes_and_skips_comments(tmp_path: Path) -> None:
    # Arrange
    path = tmp_path / ".env"
    path.write_text(
        "\n".join(
            [
                "# a comment",
                "",
                f'{CREDENTIAL_NAMES[0]}="{SECRET_A}"',
                f"{CREDENTIAL_NAMES[1]}={SECRET_B}",
                "NOT_A_PAIR",
            ]
        ),
        encoding="utf-8",
    )
    # Act
    parsed = parse_env_file(path)
    # Assert
    assert parsed[CREDENTIAL_NAMES[0]] == SECRET_A
    assert parsed[CREDENTIAL_NAMES[1]] == SECRET_B
    assert "NOT_A_PAIR" not in parsed


def test_parse_env_file_on_a_missing_path_is_empty_not_an_error(
    tmp_path: Path,
) -> None:
    assert parse_env_file(tmp_path / "absent.env") == {}


def test_loading_installs_the_redactor_before_any_caller_holds_a_value(
    tmp_path: Path,
) -> None:
    """The ordering is the guarantee: no credentialed request can be sent by a
    process whose recording boundary is not already redacting."""
    # Arrange
    path = tmp_path / ".env"
    path.write_text(f"{CREDENTIAL_NAMES[0]}={SECRET_A}\n", encoding="utf-8")
    install_redactor(Redactor({}))
    # Act
    store = load_credentials(path)
    # Assert
    assert store.require(CREDENTIAL_NAMES[0]) == SECRET_A
    assert active_redactor().names == (CREDENTIAL_NAMES[0],)
    assert SECRET_A not in redact_text(f"body {SECRET_A}")


def test_an_environment_value_wins_over_the_env_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Arrange
    path = tmp_path / ".env"
    path.write_text(f"{CREDENTIAL_NAMES[0]}={SECRET_A}\n", encoding="utf-8")
    monkeypatch.setenv(CREDENTIAL_NAMES[0], SECRET_B)
    # Act
    store = load_credentials(path)
    # Assert
    assert store.require(CREDENTIAL_NAMES[0]) == SECRET_B


def test_presence_of_an_unregistered_variable_is_dropped() -> None:
    # Arrange — a stray key in .env is not silently promoted to a credential.
    store = CredentialStore({"ORB_NOT_REGISTERED": SECRET_A})
    # Act / Assert
    assert store.missing() == list(CREDENTIAL_NAMES)
    assert [p.name for p in store.presence()] == list(CREDENTIAL_NAMES)


def test_credential_presence_is_frozen() -> None:
    presence = CredentialPresence("ORB_X", is_present=True, character_length=9)
    with pytest.raises(AttributeError):
        presence.character_length = 10  # type: ignore[misc]
