"""Every registered constant, in one place — REGISTRATION.md in code.

Each value here is registered in REGISTRATION.md and changes only by a
numbered amendment there. tests/test_registry.py pins the figures to the
document, so code and registration cannot drift apart silently.
"""

# --- Section 0.3 / 9 — the power gate ---------------------------------------
Z_CRITICAL: float = 2.0
EFFECT_BAND_LO: float = 0.02
EFFECT_BAND_HI: float = 0.08

# --- Section 0.2 — buckets and snapshots ------------------------------------
BUCKET_EDGES_CENTS: tuple[tuple[int, int], ...] = (
    (1, 10),
    (11, 20),
    (21, 30),
    (31, 40),
    (41, 50),
    (51, 60),
    (61, 70),
    (71, 80),
    (81, 90),
    (91, 99),
)
TAIL_BUCKETS_CENTS: tuple[tuple[int, int], ...] = ((1, 10), (91, 99))
SNAPSHOT_S24_HOURS: int = 24
SNAPSHOT_S30_DAYS: int = 30

# --- Section 0.2 — the sampling rule ----------------------------------------
UNRESTRICTED_SAMPLE_SIZE: int = 2000
SAMPLE_SEED: int = 20260829
WILSON_Z: float = 1.96  # the 95% lower bound on the sampled tail share

# --- Section 0.5 — the access gate ------------------------------------------
ACCESS_MIN_SETTLED_MARKETS: int = 1000
ACCESS_OUTCOME_PRESENCE_MAX_RECORDS: int = 5

# --- Section 1 — the permitted filter ---------------------------------------
# The three categories and the volume floor are registered in Stage A Task 2,
# before the filter is applied. Only the maturity rule is fixed from Task 0.
PERMITTED_MIN_MATURITY_DAYS: int = 30

# --- Section 2 / 11 — the registered cost model -----------------------------
FEE_PER_SIDE_USD: float = 0.02
FEE_SIDES: int = 2
HALF_SPREAD_USD: float = 0.01
FX_PER_DIRECTION: float = 0.015
FX_DIRECTIONS: int = 2
