# ETFExperiment

**A measurement-only test of one hypothesis: US spot Bitcoin ETF net flow prints
predict the next day's BTC return, out of sample, by enough to clear a round trip
on Hyperliquid perps.**

**Stage A never trades, never touches capital, and never reads an outcome
value.** There is no wallet, no signer, no order, no venue credential, no
position, and no stage in which one is planned. Zero dollars spent; every source
is a keyless public endpoint and `.env.example` is empty on purpose.

## The measurement that decides this repository

**Not the return. The publication lag and the revision rate.** The direct
precedent is MLCryptoEngine H11: a free flow source with a *measured* 75-day
publication lag and whole-file regeneration that revised past rows killed the
last flow hypothesis this project ran — **the class died on the lag, not on the
model**, and the lag was discovered rather than registered. Here it is
registered as the first-class measurement, before any model exists.

## What is measured so far, each figure with its n

| finding | figure |
|---|---|
| Flow source selected | Farside Investors — keyless, server-rendered, all five registered funds, **676 date rows**, no stated prohibition |
| Sources routed out on stated prohibitions | TheBlock (`Disallow: /api/`), Glassnode (`Disallow: /api`, and not keyless) — **their endpoints were never requested** |
| Per-row publication timestamp served | **none, on either surviving source (n = 2 of 2)** |
| Documented publication convention | **none.** The source documents "generated automatically, in real time"; "evening" and "night" appear **0 times** across both served pages |
| Independent cross-check | **315 of 333** out-of-sample days agree within 2% between Farside and SoSoValue |
| Rate ceilings | **none found** at or above the repo's own 1.0 s floor — **96 probe requests, all HTTP 200** |
| Hourly candle horizon | a **rolling 5,001-row window**: `1h` reaches back to 2026-02-01T11:00Z and slides one hour per hour (n = 17 bisection probes) |
| Archive capture density | **11 of 333 = 3.30%** against a registered 60% bar — and it fails on crawl rate (0.316 mementos/day), not on the registered window |
| Retro revision rate | **0 of 11 revised**, 0 sign flips, 0 threshold crosses — the H11 hazard does **not** reproduce here, at an n below the registered minimum of 30 |
| Retro cohort | **8 trading days** (archive-served value ∩ servable hourly window) |
| Sealed outcome substrate | 5,002 hourly rows + 11 funding pages; **142 of 333** days covered at the registered 0.95/0.95 bars |
| Pre-period carve-out inputs | daily sd **0.027431** (n = 475 returns); mean hourly funding **0.00002226** (n = 11,423 hours), 19.5%/yr |
| Admissible-day census | **336 rows, 11 admissible** — 53 capture-too-late, 243 no-capture, 25 capture-served-no-value, 3 no-printed-value, 1 archive-fetch-failed |

## Layout

    REGISTRATION.md   the pre-registration: Sections 0-14 and the amendment log
    HYPOTHESES.md     the hypothesis register; read before proposing anything new
    DECISIONS.md      18 numbered ADRs
    CLAUDE.md         standing rules, the blindness field lists, the carve-out
    report.md         stage-sectioned, each section written for the moment it landed
    progress.md       the governing prompt verbatim, then ETA against actual
    docs/ACCESS.md    A.1 access verification, with verbatim fragments and codes
    src/etf/          the package
    scripts/          the runnable passes and the mutation harness
    ops/              systemd user units
    reports/          measured artifacts, one directory per sub-stage

## The five standing guards

1. **Recorded absence** (`etf.absence`) — refuses `float`, `int`, indexing and
   addition. A dash where a number will stand is not a zero.
2. **Parse-tree config enforcement** (`tests/test_guards.py`) — every registered
   field must be *read* somewhere. A text search passes vacuously on a key left
   in a comment; this walks the AST.
3. **Append-only fsynced ledgers** (`etf.ledger`) — a truncated line is reported,
   never repaired.
4. **Six call states** (`etf.callstate`) — operational health and sample
   composition never merge.
5. **The pre-period date pin** (`etf.preperiod`) — no price or funding read
   stamped on or after 2025-05-01 outside the sealed writers. One address, four
   structural guards, boundary fixtures on the instant.

## Running it

    make install     create the venv and install
    make all         lint, typecheck, test          # the gate
    make guards      the structural guards alone
    make mutations   the mutation harness

Collectors run as user units: `etf-snap.timer` every 20 minutes and
`etf-daily.timer` at 12:20 UTC, both `Persistent=true`, `MemoryMax=2G`. A manual
run refuses while a unit is active; `ETF_ALLOW_MANUAL_RUN=1` overrides it
deliberately.

## The open operator item

**REGISTRATION.md Section 13 reserves an operator prior and it is empty.** The
empty slot blocks Stage B structurally. The assistant's recorded 0.10 is not
that number and may not be copied into the slot — an adopted prior corrupts the
calibration ledger (the NPDExperiment Amendment 0 lesson).
