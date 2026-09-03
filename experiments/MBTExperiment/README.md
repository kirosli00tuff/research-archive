# MBTExperiment

**Two venue facts, measured. No premium, no order, no position.**

Status: **Stage A.1 not yet run.** Scaffold and operating manual only. No
registration exists, nothing has been measured, and no claim is made here.

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

## Commands

```bash
make install           # uv sync + pre-commit hooks
make all               # lint, typecheck, test
make guards            # the structural guards, including the no-transmit scan
make a1-probe          # PAPER  connect, verify permission, record provenance
make a1-chain          # PAPER  resolve the ATM 30-day straddle
make a1-whatif-paper   # PAPER  margin read, development only
make a1-census         # PAPER  one bid-ask window; clock-bound to 20
make a1-gates          # offline, fires MARGIN and COST from recorded figures
```

## Read next

`CLAUDE.md` for the contract and the boundaries, `REGISTRATION.md` once Stage
A.1 writes it, `progress.md` for the stage record.

MIT licensed. **Not financial advice.** The premium this route would harvest is
payment for bearing crash risk. VRPExperiment measured the payment and states
plainly that it did not measure the liability.
