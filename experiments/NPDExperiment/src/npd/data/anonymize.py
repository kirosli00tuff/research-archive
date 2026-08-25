"""Per-call anonymization. Row labels are random letters, remapped every call.

Two things leak identity and both are removed. The label, which is redrawn from
a fresh nonce on every call, and the row order, which is shuffled so position
carries no information about rank, symbol, or alphabet.

tests/test_anonymization.py fails if a ticker string ever reaches a prompt.
"""

from __future__ import annotations

import secrets
import string
from dataclasses import dataclass
from random import Random

LABEL_ALPHABET = string.ascii_uppercase
LABEL_LENGTH = 2


@dataclass(frozen=True, slots=True)
class Anonymization:
    """One call's mapping. The nonce is stored so the mapping can be replayed."""

    nonce: str
    label_to_symbol: dict[str, str]
    presentation_order: tuple[str, ...]

    @property
    def symbol_to_label(self) -> dict[str, str]:
        return {sym: lab for lab, sym in self.label_to_symbol.items()}


def _all_labels() -> list[str]:
    return [a + b for a in LABEL_ALPHABET for b in LABEL_ALPHABET]


def new_nonce() -> str:
    """A fresh nonce per call. Never derived from the date, so two calls on the
    same day cannot share a mapping."""
    return secrets.token_hex(8)


def build(symbols: list[str], nonce: str) -> Anonymization:
    """Assign random labels and a random presentation order.

    The nonce seeds the shuffle, so the mapping replays exactly from the stored
    nonce while remaining unpredictable to the model.
    """
    if not symbols:
        raise ValueError("cannot anonymize an empty panel")
    # Two-letter codes collide with real tickers. KO is Coca-Cola, GE is General
    # Electric, HD is Home Depot. A label that equals a symbol standing in the
    # same panel puts that ticker in front of the model, which is the one thing
    # anonymization exists to prevent. The panel symbols are struck from the pool
    # before any label is drawn.
    taken = {s.strip().upper() for s in symbols}
    pool = [lab for lab in _all_labels() if lab not in taken]
    if len(symbols) > len(pool):
        raise ValueError(f"{len(symbols)} symbols exceed the {len(pool)} available labels")

    rng = Random(int(nonce, 16))
    labels = rng.sample(pool, len(symbols))
    order = list(symbols)
    rng.shuffle(order)

    mapping = dict(zip(labels, symbols, strict=True))
    label_by_symbol = {sym: lab for lab, sym in mapping.items()}
    return Anonymization(
        nonce=nonce,
        label_to_symbol=mapping,
        presentation_order=tuple(label_by_symbol[s] for s in order),
    )
