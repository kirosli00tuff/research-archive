"""Guard 8 — secret redaction, at the recording boundary rather than the call site.

Three credentials now exist. A credentialed endpoint can return the key **inside
its own error body**, `docs/ACCESS.md` records refusal payloads **verbatim**, and
`orb.seal.SealedWriter` stores raw vendor bytes without parsing them. Put those
three facts together and a key reaches a recorded artifact without any module
ever printing one on purpose.

So redaction is placed where a string becomes a **record** — the sealed writer,
the append-only ledger, the HTTP response object and the console — and not at
the call site. A call site can be forgotten. A recording boundary is one of four
places, each pinned by parse tree in
``tests/test_guards.py::test_every_recording_boundary_routes_through_the_redactor``.

**Replacement is deterministic**: the same secret always becomes the same
placeholder, so the byte-level revision comparison of A.1 TASK 3 is unaffected —
two pulls that differ only in a redacted key still compare equal, and two pulls
that differ in a bar still compare unequal.
"""

from __future__ import annotations

import sys
import urllib.parse
from collections.abc import Mapping, Sequence
from typing import Any, Final, final

MIN_REDACTABLE_LENGTH: Final[int] = 8
"""A secret shorter than this is refused rather than redacted.

Redacting a two-character needle would rewrite every artifact in the repository
into noise. A short credential is a loud refusal, never a silent corruption.
"""


class SecretTooShortError(ValueError):
    """Raised when a registered secret is too short to redact safely."""


def placeholder_for(name: str) -> str:
    """The placeholder that stands in for a secret, naming its variable."""
    return f"<redacted:{name}>"


@final
class Redactor:
    """Replaces every registered secret with a placeholder naming its variable.

    Needles are ordered **longest first**, so a secret that contains another
    secret as a substring is replaced whole rather than in pieces.
    """

    __slots__ = ("_names", "_pairs")

    def __init__(self, secrets: Mapping[str, str]) -> None:
        pairs: list[tuple[str, str]] = []
        for name, value in secrets.items():
            if not value:
                continue
            if len(value) < MIN_REDACTABLE_LENGTH:
                raise SecretTooShortError(
                    f"{name} is {len(value)} characters, below the "
                    f"{MIN_REDACTABLE_LENGTH}-character floor; redacting it "
                    "would rewrite unrelated text. Refusing rather than "
                    "corrupting every artifact this process writes."
                )
            marker = placeholder_for(name)
            pairs.append((value, marker))
            quoted = urllib.parse.quote(value, safe="")
            if quoted != value:
                pairs.append((quoted, marker))
        pairs.sort(key=lambda pair: len(pair[0]), reverse=True)
        self._pairs: tuple[tuple[str, str], ...] = tuple(pairs)
        self._names: tuple[str, ...] = tuple(sorted(secrets))

    @property
    def names(self) -> tuple[str, ...]:
        """The variable names registered. **Never the values.**"""
        return self._names

    @property
    def secret_count(self) -> int:
        """How many needles are active. A count, never a value."""
        return len(self._pairs)

    def __repr__(self) -> str:
        return f"Redactor(names={list(self._names)}, needles={len(self._pairs)})"

    # --- the three shapes a record arrives in --------------------------

    def text(self, value: str) -> str:
        """Redact a string bound for a log, a report, a message or the console."""
        out = value
        for needle, marker in self._pairs:
            if needle in out:
                out = out.replace(needle, marker)
        return out

    def data(self, value: bytes) -> bytes:
        """Redact raw bytes bound for a sealed file. Deterministic."""
        out = value
        for needle, marker in self._pairs:
            needle_bytes = needle.encode("utf-8")
            if needle_bytes in out:
                out = out.replace(needle_bytes, marker.encode("utf-8"))
        return out

    def row(self, value: Any) -> Any:
        """Redact a ledger row recursively: keys, values, nested rows, sequences."""
        if isinstance(value, str):
            return self.text(value)
        if isinstance(value, bytes):
            return self.data(value)
        if isinstance(value, Mapping):
            return {self.row(k): self.row(x) for k, x in value.items()}
        if isinstance(value, Sequence) and not isinstance(value, str | bytes):
            return [self.row(x) for x in value]
        return value


_INSTALLED: Redactor = Redactor({})
"""The process-wide redactor. Empty until credentials are loaded, which is
correct: the uncredentialed path has nothing to redact, and an empty redactor is
an identity function rather than a silent bypass."""


def install_redactor(redactor: Redactor) -> None:
    """Install the process-wide redactor. Called once, when credentials load."""
    global _INSTALLED
    _INSTALLED = redactor


def active_redactor() -> Redactor:
    """The installed redactor. Every recording boundary calls this."""
    return _INSTALLED


def redact_text(value: str) -> str:
    """Redact a string through the installed redactor."""
    return _INSTALLED.text(value)


def redact_data(value: bytes) -> bytes:
    """Redact bytes through the installed redactor."""
    return _INSTALLED.data(value)


def redact_row(value: Any) -> Any:
    """Redact a ledger row through the installed redactor."""
    return _INSTALLED.row(value)


def say(*parts: object) -> None:
    """Print to the console through the redactor. The only console writer.

    Flushed on every line: a long-running probe whose progress sits in a pipe
    buffer is indistinguishable from one that has hung, and this repository
    would rather be slow than ambiguous about which of the two it is.
    """
    sys.stdout.write(redact_text(" ".join(str(p) for p in parts)) + "\n")
    sys.stdout.flush()
