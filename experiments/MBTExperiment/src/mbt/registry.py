"""Every registered constant, in one place, transcribed and never re-derived.

**Nothing in this module is computed from data.** Each figure is transcribed from
a named VRPExperiment document, read across the read-only boundary, and carries
the document and the sample size it was measured with. VRPExperiment's 1,955-day
sample is spent and no figure in it is recomputed, extended or re-read here.

``tests/test_registration.py`` pins every value below against the registration
text, so a figure cannot drift out of the documentation and into the code
unnoticed. The arithmetic identities at the bottom are **transcription checks**,
not recomputations: they confirm that the registered ceilings follow from the
registered inputs exactly as the source documents state, and they would fail if
a digit were mistyped.
"""

from __future__ import annotations

from enum import StrEnum, unique
from typing import Final

# ---------------------------------------------------------------------------
# The instrument. docs/ARTIFACT.md, docs/COSTS.md.
# ---------------------------------------------------------------------------

MBT_NOTIONAL_USD: Final = 7812.46
"""Notional of one CME Micro Bitcoin option, being an option on 0.10 BTC, at the
measured spot of BTC $78,124.575. docs/COSTS.md, n = 2 independent public
sources agreeing to 1.16 bps."""

SLEEVE_USD: Final = 1000.00
"""The registered sleeve size. docs/ARTIFACT.md."""

# ---------------------------------------------------------------------------
# Gate one: MARGIN. docs/HANDOVER.md, HYPOTHESES.md.
# ---------------------------------------------------------------------------

MARGIN_CEILING_FRACTION_OF_NOTIONAL: Final = 0.1280
"""Initial margin on a short MBT option must sit at or below 12.80% of notional.
Below this a $1,000 sleeve holds fewer than one position."""

MARGIN_CEILING_USD_PER_CONTRACT: Final = 1000.00
"""The same ceiling in dollars: $1,000 per contract."""

# ---------------------------------------------------------------------------
# The premium. docs/ARTIFACT.md, HYPOTHESES.md. MEASURED BY VRPExperiment,
# CLOSED 2026-08-30. Transcribed here, never recomputed, never extended.
# ---------------------------------------------------------------------------

VRP_SAMPLE_N: Final = 1955
"""Daily observations per asset, 2021-03-24 to 2026-07-30. HYPOTHESES.md."""

BTC_PREMIUM_POINT_BPS: Final = 198.111
"""BTC mean premium in bps of notional, n = 1,955, t = 5.888, p = 2.297e-9."""

BTC_PREMIUM_LOWER_BOUND_BPS: Final = 142.740
"""BTC one-sided 95% CI lower bound, FULL SAMPLE, n = 1,955. A LOWER BOUND."""

BTC_PREMIUM_QUARTERS_BPS: Final = (284.53, 250.59, 145.13, 112.72)
"""The four equal quarters, in order. n = 488, 488, 488, 491. POINT ESTIMATES,
not lower bounds: VRPExperiment records p-values for these and no CI bound."""

BTC_PREMIUM_QUARTER_NS: Final = (488, 488, 488, 491)
"""Sample size of each quarter above, in the same order."""

BTC_PREMIUM_RECENT_QUARTER_BPS: Final = 112.72
"""The most recent quarter, 2025-03-27 to 2026-07-30, n = 491, p = 0.018.
A POINT ESTIMATE. Its own one-sided lower bound is NOT recorded in
VRPExperiment and is not computed here."""

BTC_PREMIUM_DECAY_FRACTION: Final = 0.604
"""The monotone fall across the four quarters, 60.4%. HYPOTHESES.md."""

# ---------------------------------------------------------------------------
# Commission. docs/COSTS.md section 1. MEASURED against the live IBKR Canada
# schedule on 2026-08-30, lowest volume tier (<= 1,000 contracts per month).
# ---------------------------------------------------------------------------

MBT_COMMISSION_PER_CONTRACT_USD: Final = 0.85
"""USD per MBT contract at the lowest volume tier."""

STRADDLE_ROUND_TRIP_COMMISSION_BPS: Final = 4.352
"""Four contract fills, 4 x $0.85 = $3.40, as bps of the MBT notional."""

REBALANCE_FILL_COMMISSION_BPS: Final = 1.088
"""One rebalance fill on the MBT micro future, $0.85, as bps of notional."""

COMMISSION_CENTRAL_BPS: Final = 16.320
"""All-in commission alone at the central end: straddle plus 11 rebalances."""

COMMISSION_P90_BPS: Final = 21.760
"""All-in commission alone at the pessimistic end: straddle plus 16 rebalances."""

# ---------------------------------------------------------------------------
# The hedging rule and its measured rebalance counts.
# VRPExperiment REGISTRATION.md 4.3, README.md. n = 1,955 paths per asset.
# ---------------------------------------------------------------------------

DELTA_BAND_PRIMARY: Final = 0.10
"""The registered primary band. Resize when position delta moves more than
+/-0.10 from flat, evaluated once per calendar day at the fixed UTC instant,
over the 30-day tenor. A registered choice, not an optimum."""

DELTA_BAND_SWEEPS: Final = (0.05, 0.20)
"""Registered sensitivity sweeps. Reported alongside the primary, never
substituted for it."""

REBALANCE_COUNT_MEDIAN: Final = 11
"""Median rebalances at the +/-0.10 band, n = 1,955 paths."""

REBALANCE_COUNT_P90: Final = 16
"""90th-percentile rebalances at the +/-0.10 band, n = 1,955 paths."""

REBALANCE_COUNT_BTC_MAX: Final = 20
"""The measured BTC maximum, n = 1,955 paths. README.md."""

REBALANCE_COUNT_ETH_MAX: Final = 22
"""The measured ETH maximum, n = 1,955 paths. Recorded for completeness; this
repository measures no ETH figure."""

REBALANCE_COUNT_SWEEP_MEDIANS: Final = {0.05: 17, 0.20: 5}
"""Median counts at the swept bands, n = 1,955 each."""

REBALANCE_DAILY_STRUCTURAL_MAX: Final = 29
"""The structural maximum a daily-evaluated rule can reach over a 30-day tenor.
A property of the rule, not a measurement of a path."""

# ---------------------------------------------------------------------------
# Gate two: COST. Both ceilings registered so the choice stays visible.
# ---------------------------------------------------------------------------


@unique
class PremiumBasis(StrEnum):
    """Which premium figure the COST ceiling rests on. Fixed in Section 0.6."""

    FULL_SAMPLE_LOWER_BOUND = "full_sample_lower_bound"
    """Half of 142.740 less 21.760 = 49.610 bps. NOT SELECTED."""

    RECENT_QUARTER_POINT = "recent_quarter_point"
    """Half of 112.72 less 21.760 = 34.600 bps. **SELECTED.**"""


COST_CEILING_FULL_SAMPLE_BPS: Final = 49.610
"""The ceiling the full-sample basis gives. Registered and NOT selected."""

COST_CEILING_RECENT_QUARTER_BPS: Final = 34.600
"""The ceiling the most-recent-quarter basis gives. **The registered ceiling.**"""

REGISTERED_PREMIUM_BASIS: Final = PremiumBasis.RECENT_QUARTER_POINT
"""Fixed in REGISTRATION.md Section 0.6 before any spread was measured.
Selecting a basis after seeing a spread measurement voids the registration."""

COST_CEILING_BPS: Final = COST_CEILING_RECENT_QUARTER_BPS
"""The ceiling the COST gate fires against."""

# ---------------------------------------------------------------------------
# Sampling. VRPExperiment REGISTRATION.md 4.1 and 4.2, plus the four rules
# those sections leave to an implementer, fixed in REGISTRATION.md Section 3.
# ---------------------------------------------------------------------------

MIN_OBSERVATION_WINDOWS: Final = 20
"""At least 20 distinct observation windows on the ATM 30-day series."""

MIN_MINUTES_BETWEEN_WINDOWS: Final = 60
"""Two windows are distinct only if their local capture instants differ by at
least this. An option book's touch persists over minutes."""

MAX_WINDOWS_PER_UTC_DAY: Final = 4
"""At most this many windows from any one UTC calendar day, so the sample
spans sessions rather than re-measuring one book state."""

MIN_COLLECTION_DAYS: Final = 5
"""20 windows at 4 per day. The census cannot be compressed below this."""

TENOR_TARGET_DAYS: Final = 30
"""The registered tenor. VRPExperiment REGISTRATION.md 2.1."""

STALE_TICK_TOLERANCE_SECONDS: Final = 5.0
"""A venue stamp trailing local capture by more than this is stale."""

# ---------------------------------------------------------------------------
# Reference only. NEVER a cost input. ADR-008 and the ORBExperiment precedent.
# ---------------------------------------------------------------------------

DERIBIT_REFERENCE_BTC_ROUND_TRIP_BPS: Final = 22.50
"""Deribit's BTC straddle round-trip quoted spread, medians, n = 24 windows per
leg and 96 observations with zero unquoted. **REFERENCE ONLY.** Deribit
prohibits Canadian residents and its spread may never be substituted for a CME
spread. See ADR-008."""

ORB_PRECEDENT_LEGS_UNDERSTATED: Final = 5
ORB_PRECEDENT_LEGS_TOTAL: Final = 6
ORB_PRECEDENT_SHIFT_FACTOR: Final = 11.27
"""ORBExperiment carried a slippage band from QQQ onto US single names. When
measured on the traded instrument, 5 of 6 legs were understated and the shift
was 11.27 times larger than the carried one, while a sixth was OVERstated, so
"assume worse" would not have rescued it either."""

# ---------------------------------------------------------------------------
# The trial grid and its deflation. REGISTRATION.md Section 3.7.
# ---------------------------------------------------------------------------

TRIAL_GRID_DISCRETE_COMBINATIONS: Final = 48
"""2 premium bases x 3 delta bands x 2 end assignments x 2 ATM tie rules x
2 tenor tie rules. Every one is fixed before any quote is stored."""

TRIAL_GRID_CONTINUOUS_TOLERANCES: Final = 3
"""Staleness tolerance, window spacing, windows per day. Each pinned to one
registered value."""

TRIAL_GRID_AFTER_DEFLATION: Final = 1
"""What the registration leaves selectable: nothing."""


# ---------------------------------------------------------------------------
# Transcription checks. These confirm the registered ceilings follow from the
# registered inputs as the source documents state them. They recompute no
# premium: every input below is transcribed, and the identity is arithmetic on
# transcribed numbers, which is how a mistyped digit is caught.
# ---------------------------------------------------------------------------


def _round_bps(value: float) -> float:
    return round(value, 3)


COMMISSION_CENTRAL_IDENTITY: Final = _round_bps(
    STRADDLE_ROUND_TRIP_COMMISSION_BPS + REBALANCE_COUNT_MEDIAN * REBALANCE_FILL_COMMISSION_BPS
)
COMMISSION_P90_IDENTITY: Final = _round_bps(
    STRADDLE_ROUND_TRIP_COMMISSION_BPS + REBALANCE_COUNT_P90 * REBALANCE_FILL_COMMISSION_BPS
)
COST_CEILING_FULL_SAMPLE_IDENTITY: Final = _round_bps(
    BTC_PREMIUM_LOWER_BOUND_BPS / 2.0 - COMMISSION_P90_BPS
)
COST_CEILING_RECENT_QUARTER_IDENTITY: Final = _round_bps(
    BTC_PREMIUM_RECENT_QUARTER_BPS / 2.0 - COMMISSION_P90_BPS
)
