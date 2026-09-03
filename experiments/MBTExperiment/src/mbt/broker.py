"""The only module in this package that holds an order object.

**No order is transmitted from here or from anywhere else in this package.** The
transmitting calls do not appear: ``tools/no_transmit_scan.py`` walks this parse
tree and fails the build on any call site of ``placeOrder`` and its neighbours,
on any order construction missing a literal ``whatIf=True``, and on any call of
:func:`what_if_order` whose flag is not a build-time literal.

Measured against ``ib_async 2.1.0`` rather than assumed:

- ``IB.placeOrder(contract, order)`` **transmits** and takes no ``whatIf``
  keyword. It is never called here.
- ``IB.whatIfOrder(contract, order)`` copies the order, sets ``whatIf = True``,
  and returns an ``OrderState``. It previews and does not transmit.
- ``OrderState`` carries ``initMarginChange``, ``maintMarginChange``,
  ``commission``, ``minCommission``, ``maxCommission`` and ``commissionCurrency``,
  and **no exchange or regulatory fee field**.

:func:`what_if_order` takes ``whatIf`` as an explicit keyword even though the
underlying API does not, so that the guard has a literal to verify at every call
site and the flag is checked again at run time. A keyword the callee ignores
would be theatre; this one is read, asserted, and applied to the order.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol, final

from mbt.clock import iso_utc, utc_now

if TYPE_CHECKING:  # pragma: no cover - typing only
    from ib_async import Contract, Order, OrderState


class TransmitRefusedError(PermissionError):
    """A run-time refusal to preview an order that is not marked what-if.

    The AST scan is the build-time guarantee and this is the run-time one. Both
    exist because they fail at different moments: the scan cannot see an order
    object mutated after construction, and a run-time check cannot fail a build.
    """


class WhatIfBroker(Protocol):
    """The narrow slice of the broker this package uses.

    Typed as a Protocol so tests exercise the real code path against a stub
    rather than against a mock of a mock. The protocol deliberately does **not**
    declare ``placeOrder``: a method that is not in the interface cannot be
    reached through it.
    """

    def whatIfOrder(self, contract: Contract, order: Order) -> OrderState: ...


@final
@dataclass(frozen=True, slots=True)
class MarginPreview:
    """The parsed result of one what-if preview.

    ``exchange_and_regulatory_fee`` is deliberately absent from this dataclass.
    ``OrderState`` carries no such field, and inventing one here would create a
    place for a synthesized number to live. Task 6 records the leg as a typed
    absence instead.
    """

    init_margin_change: str
    maint_margin_change: str
    equity_with_loan_change: str
    commission: float | None
    min_commission: float | None
    max_commission: float | None
    commission_currency: str
    warning_text: str
    status: str
    previewed_at: str

    @classmethod
    def from_order_state(cls, state: Any) -> MarginPreview:
        """Parse an ``OrderState``. Margin changes stay STRINGS, deliberately.

        IBKR returns these fields as strings and serves the sentinel
        ``"1.7976931348623157E308"`` for "not computed". Parsing to float here
        would turn that sentinel into a finite-looking number of order 1e308 that
        a later comparison would silently treat as a margin. The strings are
        carried verbatim and interpreted where the sentinel is recognised.
        """
        return cls(
            init_margin_change=str(getattr(state, "initMarginChange", "")),
            maint_margin_change=str(getattr(state, "maintMarginChange", "")),
            equity_with_loan_change=str(getattr(state, "equityWithLoanChange", "")),
            commission=_optional_float(getattr(state, "commission", None)),
            min_commission=_optional_float(getattr(state, "minCommission", None)),
            max_commission=_optional_float(getattr(state, "maxCommission", None)),
            commission_currency=str(getattr(state, "commissionCurrency", "")),
            warning_text=str(getattr(state, "warningText", "")),
            status=str(getattr(state, "status", "")),
            previewed_at=iso_utc(utc_now(), "MarginPreview.from_order_state"),
        )

    def as_row(self) -> dict[str, object]:
        return {
            "init_margin_change": self.init_margin_change,
            "maint_margin_change": self.maint_margin_change,
            "equity_with_loan_change": self.equity_with_loan_change,
            "commission": self.commission,
            "min_commission": self.min_commission,
            "max_commission": self.max_commission,
            "commission_currency": self.commission_currency,
            "warning_text": self.warning_text,
            "status": self.status,
            "previewed_at": self.previewed_at,
            "exchange_and_regulatory_fee": (
                "absent: OrderState carries no such field, measured against "
                "ib_async 2.1.0. See reports/task6/."
            ),
        }


#: IBKR's "not computed" sentinel for a numeric field, being the IEEE 754 double
#: maximum. It arrives as a string and must never be read as a quantity.
IBKR_UNSET_SENTINEL = "1.7976931348623157E308"


def _optional_float(value: object) -> float | None:
    """Parse a numeric field, mapping IBKR's sentinel and blanks to None."""
    if value is None:
        return None
    text = str(value).strip()
    if not text or text.upper() == IBKR_UNSET_SENTINEL.upper():
        return None
    try:
        parsed = float(text)
    except ValueError:
        return None
    return None if parsed >= 1e307 else parsed


def is_unset(field: str) -> bool:
    """True when a margin field carries IBKR's not-computed sentinel."""
    text = field.strip()
    return not text or text.upper() == IBKR_UNSET_SENTINEL.upper()


def build_short_option_order(order_cls: Any, *, quantity: int) -> Any:
    """Build the short-option order used for the margin preview.

    ``whatIf=True`` and ``transmit=False`` are both literals, and both are
    verified by the AST scan. Two flags rather than one because they fail
    differently: ``whatIf`` makes the request a preview, and ``transmit=False``
    means that even a hypothetically mis-routed order would sit unsent.
    """
    if quantity <= 0:
        raise ValueError(f"quantity must be positive, got {quantity}")
    return order_cls(
        action="SELL",
        orderType="MKT",
        totalQuantity=quantity,
        whatIf=True,
        transmit=False,
    )


def what_if_order(
    broker: WhatIfBroker,
    contract: Contract,
    order: Any,
    *,
    whatIf: bool,
) -> MarginPreview:
    """Preview an order. The only broker order path in this package.

    ``whatIf`` is required, is verified as a literal ``True`` at every call site
    by the AST scan, and is asserted again here. The order's own ``whatIf`` field
    is checked too, because the scan sees construction and cannot see a later
    mutation.
    """
    if whatIf is not True:
        raise TransmitRefusedError(
            "REFUSED: what_if_order was called with whatIf=False. This repository "
            "transmits no order, ever. Every broker interaction is a whatIf "
            "preview or a market-data read."
        )
    if getattr(order, "whatIf", None) is not True:
        raise TransmitRefusedError(
            "REFUSED: the order object does not carry whatIf=True. The AST scan "
            "verifies construction and cannot see a mutation applied afterwards, "
            "so the flag is checked again on the object at the moment of use."
        )
    if getattr(order, "transmit", False) is not False:
        raise TransmitRefusedError(
            "REFUSED: the order object carries transmit=True. A preview never "
            "needs it, and an order that could be transmitted is not a preview."
        )
    return MarginPreview.from_order_state(broker.whatIfOrder(contract, order))
