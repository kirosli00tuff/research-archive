"""The settled stage A configuration.

These values are inputs recorded by the operator before stage A.1 ran. They
become binding only when REGISTRATION.md registers them in stage A.2, and
Amendment 1 in stage C.2 may overwrite the ones Task 3 forces.

Every field must have an enforcement or consumption site outside this file.
tests/test_structural_guard.py fails when one does not, which is how a
config value is kept from becoming decoration.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StageAConfig:
    """The configuration the arithmetic in docs/ACCESS.md is computed against."""

    book_width: int = 20
    per_name_notional_usd: float = 45.0
    deployed_usd: float = 900.0
    buffer_usd: float = 100.0
    total_usd: float = 1000.0
    plan_name: str = "tiered"

    def __post_init__(self) -> None:
        if self.book_width * self.per_name_notional_usd != self.deployed_usd:
            raise ValueError("book width times notional must equal deployed")
        if self.deployed_usd + self.buffer_usd != self.total_usd:
            raise ValueError("deployed plus buffer must equal total")


CONFIG = StageAConfig()
