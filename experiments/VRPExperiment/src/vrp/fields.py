"""Guard 5, part one — the field registry the blindness pin is built on.

**Blind fields** carry an implied volatility, a realized volatility, an option
price, or a premium. Nothing outside a sealed writer or the sealed reader may
name one. **Readable fields** are metadata — instrument names, expiries,
timestamps, status codes, counts, contract specifications — and any module may
name them.

The separation is the whole of outcome blindness. The machinery of TASK 6 is
built and tested against synthetic fixtures with known answers, and no module
in the tree can read a real premium value until the latch is spent, because no
module in the tree can name the field that carries one.

Venue policy text, margins, commissions and bid-ask spreads are **readable**.
They are cost and reachability facts, they are the TASK 3 and TASK 5 deciding
measurements, and blinding them would blind the wrong half of the experiment.
"""

from __future__ import annotations

BLIND_FIELDS: frozenset[str] = frozenset(
    {
        # Implied volatility, in every serialisation this project may meet.
        "iv",
        "IV",
        "implied_vol",
        "implied_volatility",
        "mark_iv",
        "bid_iv",
        "ask_iv",
        "markIv",
        "bidIv",
        "askIv",
        "dvol",
        "DVOL",
        "vol_index",
        "volatility_index",
        "sigma_implied",
        # Realized volatility.
        "rv",
        "RV",
        "realized_vol",
        "realized_volatility",
        "realised_volatility",
        "sigma_realized",
        "close_to_close_vol",
        "parkinson_vol",
        # Option price and premium.
        "option_price",
        "mark_price",
        "markPrice",
        "premium",
        "premium_collected",
        "option_premium",
        "variance_premium",
        "variance_risk_premium",
        "vrp",
        "vrp_points",
        "vrp_bps",
        # The estimated endpoint itself.
        "premium_estimate",
        "premium_ci_low",
        "premium_ci_high",
    }
)
"""Field names that carry an implied volatility, a realized volatility, an
option price, or a premium. Naming one outside a sealed module is a guard
failure, not a style preference."""


READABLE_FIELDS: frozenset[str] = frozenset(
    {
        # Instrument and venue identity.
        "instrument_name",
        "instrument",
        "venue",
        "exchange",
        "currency",
        "underlying",
        "product_code",
        "option_type",
        "strike",
        "expiry",
        "settlement",
        "settlement_rule",
        "tenor_days",
        # Contract specification and cost. TASK 3 and TASK 5 deciding facts.
        "contract_size",
        "tick_size",
        "min_increment",
        "notional",
        "initial_margin",
        "maintenance_margin",
        "commission",
        "exchange_fee",
        "broker_fee",
        "bid",
        "ask",
        "bid_ask",
        "half_spread",
        "spread_bps",
        "positions_supported",
        # Policy and reachability.
        "policy_url",
        "policy_date",
        "policy_text",
        "restricted_jurisdictions",
        "canada_status",
        "british_columbia_status",
        "retrieved_at",
        # Operational metadata.
        "status_code",
        "sha256",
        "byte_count",
        "line_count",
        "n",
        "count",
        "recorded_at",
        "kind",
        "path",
        "reason",
        "detail",
        "health",
        "robots_txt",
        "terms_text",
    }
)
"""Metadata any module may name. Cost and reachability are deliberately here:
they decide the experiment and must be readable to decide it."""


SEALED_MODULES: frozenset[str] = frozenset(
    {
        "vrp/fields.py",
        "vrp/seal.py",
        "vrp/sealed_read.py",
    }
)
"""The only modules permitted to name a blind field. Every other module in
``src/vrp`` is walked by ``tests/test_guards.py`` and fails on a single
occurrence."""


_OVERLAP = BLIND_FIELDS & READABLE_FIELDS
if _OVERLAP:  # pragma: no cover - a registry defect, caught at import
    raise AssertionError(
        f"a field cannot be both blind and readable: {sorted(_OVERLAP)}"
    )
