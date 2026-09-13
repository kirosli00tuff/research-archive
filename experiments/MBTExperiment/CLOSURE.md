# CLOSURE — MBTExperiment

**CLOSED 2026-09-03. Verdict: VENUE_BLOCKED, unqualified, on capital.**

Every claim carries its sample size in the same sentence as its number.

---

## The finding

**The MBT variance-harvest route does not fit a $1,000 sleeve, and the cheapest
single component of the position proves it at the exchange's own minimum.**

| | figure |
|---|---|
| registered MARGIN ceiling | **12.80% of notional** ($1,000 at the $7,812.46 registration notional) |
| measured notional, MBT front future | **$8,177.75** (touch 81,770.0 / 81,785.0, paper session 2026-09-03) |
| ceiling in dollars at that notional | **$1,046.75** |
| CME maintenance, ONE MBT future, front month 09/2026 | **$1,704.00** |
| as a share of notional | **20.837%** |
| **exceedance** | **1.628x** |

**Outcome: FAIL.** Recorded in `reports/task8/margin_gate_final.json`.

## Why the verdict is normalized to notional rather than left in dollars

A dollar ceiling moves with the bitcoin price. A fraction of notional does not.
Bitcoin fell roughly 42% between the registration and the measurement, so a
dollar-only verdict would have been hostage to a price move rather than robust
to one. **The gate fails on a ratio, so a bitcoin rally does not rescue it.**

## Why $1,704 is a floor and not an estimate

**It is the hedge leg alone.** The two short option legs are additional.

**It is maintenance, not initial.** Customer initial conventionally runs about
1.1x maintenance.

**It is the exchange minimum.** IBKR applies its own multiplier above it.

Every correction to this figure moves it up. None moves it down.

## Two independent corroborations, agreeing on the percentage

**18 paper what-if previews** across 9 strikes and both rights put a **single**
short MBT option at **$3,441.42 to $4,599.07, median $3,930.96, zero of 18 below
the ceiling**. That is **2.0x to 2.7x** the future figure, consistent with a
broker markup rather than a simulator artifact. This mattered: the standing
objection to the paper numbers was that IBKR's paper environment approximates
SPAN, and an independent exchange-published figure in the same family answers it.

**Schwab reported MBT initial margin near $2,800 as of 2026-03-24**, alongside
$140,000 for full-size BTC. Full-size BTC is 5 bitcoin, so $140,000 on $700,000
of notional is 20%, implying bitcoin near $140,000 in March. The same ~20% rule
at today's $81,777.50 gives ~$1,700.

**Two independent sources agree on the percentage, which is stronger
corroboration than either figure alone**, and it explains the apparent
discrepancy between $2,800 and $1,704 without either being wrong.

## What this closure does NOT claim

**The premium is not disputed.** VRPExperiment measured it at 198.111 bps of
notional, n = 1,955, p = 2.3e-9, and nothing here reopens that.

**The COST gate never fired.** It is `Absent(insufficient_sample)` at n = 0 of 20
registered windows, with its fee leg `Absent(not_served)` regardless. **No spread
was ever measured on CME, and none is claimed.** Deribit's 22.50 bps stayed
REFERENCE ONLY and no gate in this repository ever read it.

**The route is not shown to be unprofitable.** It is shown to be uncapitalizable
at $1,000. Those are different findings and only the second is made here.

**No live session was ever opened.** The paper-only clause held from 2026-09-02
to closure. No order was transmitted, no position sized, no capital committed.

## The gaps in the closing evidence, recorded rather than smoothed

The CME export carries **no effective or as-of date**, so the figure is undated
at source and must be re-pulled if it ever becomes load-bearing again. Its
**Product Code column is empty on all 10 rows**. **Maintenance Long reads `-` on
all 10 rows** with only Maintenance Short populated, and whether long is equal,
unspecified, or collapsed in the display is **unresolved from this file**.

Provenance and sha256 in
`docs/evidence/cme_outright_rates_crypto_20260903.provenance.json`.

## What this repository produced that outlives it

**A real defect the guard built to catch it could not see.** Stage B's mutation
harness found that `build_short_option_order` took the order class as a
parameter, so the package's only order construction sat outside the no-transmit
scan's constructor list. **The one call site that mattered was outside the guard
built to check it.** Review, `mypy --strict`, `ruff` and 156 passing tests all
missed it.

**The transmit/whatIf conflation.** IBKR error 321 on **4 of 4 products tried**:
a what-if is *required* to carry `transmit=True`. The package set
`transmit=False` and refused `True`, so it could not construct a preview the
venue would process, on any product, in any environment. **`transmit=False` was
serving as a proxy for a safety property it never provided.** The property that
prevents transmission is `whatIf=True`. A second defect sits behind it: with
`transmit=True` and no explicit TIF, IBKR warns 10349 and returns no OrderState
at all, isolated at n = 4 combinations. **TIF is load-bearing, the account field
is not.** See ADR-010.

**The marketDataType trap.** The ticker reported `marketDataType = 1`, meaning
real-time, while the feed served nothing. **Reading the status field alone would
have recorded an unsubscribed leg as a real-time observation.** The registered
check order caught it by checking structure before delay. Pinned at n = 7
conversion cases.

**Measured refusals rather than constructed ones.** All three registered legs
quoted under a delayed request and every one was refused under registered rule
3.4, at n = 3 legs across n = 5 independent sessions. Stage B could only
demonstrate that guard on synthetic inputs.

## Reintroduction

**This closure is final at $1,000.** A different capital constraint is a
different question and gets its own registration.

See `REINTRODUCTION.md` for the conditions under which the question reopens, the
arithmetic at a $7,000 sleeve, and the discipline that a reopening must carry.
