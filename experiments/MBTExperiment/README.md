# MBTExperiment

**Two venue facts, measured. No premium, no order, no position.**

Status: **CLOSED 2026-09-03. VENUE_BLOCKED, unqualified, on capital.**

The MARGIN gate **FAILED**: CME maintenance on the delta-hedging future alone,
at the exchange minimum, is **20.837% of notional against a registered 12.80%
ceiling**, an exceedance of **1.628x** on the cheapest single component of the
position. The MBT variance-harvest route does not fit a $1,000 sleeve.

The COST gate never fired and is `Absent(insufficient_sample)` at n = 0 of 20
registered windows. **No CME spread was ever measured and none is claimed.** No
live session was ever opened.

Read `CLOSURE.md` for the finding and `REINTRODUCTION.md` for the conditions
under which the question reopens.

---

## The question

VRPExperiment measured a large BTC variance risk premium and closed
**VENUE_BLOCKED, qualified**, on 2026-08-30. Its handover names one route still
open, CME options on Micro Bitcoin futures through IBKR Canada, and states that
the route turns on exactly two figures neither obtainable without an account.

This repository obtains them.

| figure | threshold |
|---|---|
| initial margin, short MBT option | ≤ $1,000 per contract, being 12.80% of $7,812.46 notional |
| absent cost legs at p90, being option and future bid-ask plus CME exchange and regulatory fees | ≤ 49.610 bps of notional |

Both PASS gives HARVESTABLE-CONFIRMED and authorizes a sleeve registration in a
**third** repository. Either FAIL closes the question unqualified.

## What it does not do

It does not measure a premium, place an order, size a position, or authorize
capital. Every broker interaction is a `whatIf` preview or a market-data read.
The no-transmit property is proved by an AST walk in `tests/test_guards.py`, not
asserted in prose, and a registered mutation flips the flag to confirm the guard
fires.

## Paper and live

**Paper only, from 2026-09-02.** No live Gateway session runs here until the
operator lifts the clause in `CLAUDE.md`. Two recorded operator constraints: the
machine's internal fans are not functioning, so concurrent sessions are not run,
and no separate live profile exists for this project yet.

The consequence is not symmetric across the two gates. A margin figure is a
property of the account and needs a U-prefixed session, so **the MARGIN gate does
not fire and is recorded `Absent(no_live_session)`**. A quote is a property of the
market data feed, which IBKR routes by subscription rather than by account type,
so **the COST gate's spread legs are collectible now**, provided the session
verifies a real-time subscription. Its fee leg stays `Absent(not_served)` in
either environment, because paper fills are simulated.

The stage therefore terminates at **HARNESS-READY** or **HARNESS-BLOCKED**, never
at HARVESTABLE-CONFIRMED, and the live margin read becomes a named open operator
item rather than a missing number.

**Stage B.1 reached HARNESS-BLOCKED on 2 of 4 conditions**, down from 3 of 4,
because the census projection now runs from a window actually collected and none
was. Stage B's two named blockers cleared: the Gateway runs and the client id is
set. Two new ones took their place, both measured and both inside this
repository.

**The venue rejects every what-if this package can construct**, with IBKR error
321, *"What-If order should have transmit flag set to TRUE"*, at 4 of 4 products
tried. `build_short_option_order` sets `transmit=False` and `what_if_order`
refuses `transmit=True`. **The flag was not flipped.** Doing so would clear the
binding blocker and reach HARNESS-READY on a safety property rewritten after
seeing what the venue demands, so the evidence is recorded and the decision is
left to the operator. See ADR-010.

**And no real-time market data subscription covers CME crypto on this account**,
measured as error 354 on all three legs across 5 independent sessions. Delayed
quotes were served, measured, and refused under registered rule 3.4 rather than
widened into a cost band.

**The registered COST ceiling is 34.600 bps, not 49.610.** Section 0.6 fixed the
premium basis on the most recent quarter before any spread was measured, because
the BTC premium decays monotonically across all four quarters (284.53 → 250.59 →
145.13 → 112.72 bps, a 60.4% fall, n = 1,955). Both ceilings stay registered so
the choice is visible.

## Commands

```bash
make install       # uv sync + pre-commit hooks
make all           # lint, typecheck, no-transmit scan, test
make guards        # the structural guards alone
make no-transmit   # guard one alone: the AST walk over the package
make mutations     # the five registered mutations, applied to real source
make b-probe       # PAPER  connect, read the account back, record provenance
make b-probe-full  # PAPER  handshake, permission, subscription state on 3 legs
make b-straddle    # PAPER  resolve the registered ATM 30-day straddle
make b-known-answer# PAPER  reproduce a checkable margin through the MBT path
make b-census      # PAPER  append one bid-ask window; clock-bound to 20
make b-gates       # offline, fires what can be fired and records what cannot
make b-whatif-live # REFUSES: the paper-only clause is in force
```

`uv run python -m mbt.cli verdict` recomputes the stage verdict from the recorded
artifacts, so it changes the moment a condition is met.

## Read next

`FINDINGS.md` for every claim with its `n`. `REGISTRATION.md` for what was
registered and when. `CLAUDE.md` for the contract and the boundaries.
`DECISIONS.md` for the twelve ADRs. `progress.md` for the run log and the ETAs
re-quoted against their up-front figures.

MIT licensed. **Not financial advice.** The premium this route would harvest is
payment for bearing crash risk. VRPExperiment measured the payment and states
plainly that it did not measure the liability.
