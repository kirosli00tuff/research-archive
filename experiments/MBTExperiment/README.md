# MBTExperiment

**Two venue facts, measured. No premium, no order, no position.**

Status: **Stage B closed HARNESS-BLOCKED, 2026-09-03.** The harness is built,
the registration is written, and the five guards fire under mutation. **No margin
was read and no spread was measured**, because no IB Gateway session exists. See
`FINDINGS.md` for every figure with its `n`, and `progress.md` for the run log.

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

**Stage B reached HARNESS-BLOCKED on 3 of 4 conditions.** The binding one is the
known-answer test: the what-if reader has never reproduced an independently
checkable margin, so its output is not trusted. Two further items block the
census: `MBT_IB_PAPER_CLIENT_ID` is unset, and IB Gateway is not running.

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
make b-census      # PAPER  append one bid-ask window; clock-bound to 20
make b-gates       # offline, fires what can be fired and records what cannot
make b-whatif-live # REFUSES: the paper-only clause is in force
```

`uv run python -m mbt.cli verdict` recomputes the stage verdict from the recorded
artifacts, so it changes the moment a condition is met.

## Read next

`FINDINGS.md` for every claim with its `n`. `REGISTRATION.md` for what was
registered and when. `CLAUDE.md` for the contract and the boundaries.
`DECISIONS.md` for the nine ADRs. `progress.md` for the run log and the ETAs
re-quoted against their up-front figures.

MIT licensed. **Not financial advice.** The premium this route would harvest is
payment for bearing crash risk. VRPExperiment measured the payment and states
plainly that it did not measure the liability.
