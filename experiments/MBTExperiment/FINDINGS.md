# FINDINGS — MBTExperiment Stage B

**Every claim carries its sample size in the same sentence as its number.**
A negative with a hidden `n` is not a result, and neither is a positive.

**Stage verdict: HARNESS-BLOCKED**, 3 of 4 registered conditions held.
Recomputable with `uv run python -m mbt.cli verdict`.

---

## 1. The two gates

**Neither gate fired, and both are recorded with their reasons rather than
omitted from the table.**

| gate | outcome | ceiling | measured | n |
|---|---|---|---|---|
| **MARGIN** | **ABSENT** | $1,000 per contract, being 12.80% of $7,812.46 | `Absent(no_live_session)` | **n = 0 live sessions** |
| **COST** | **ABSENT** | 34.600 bps of notional | `Absent(insufficient_sample)` | **n = 0 of 20 registered windows** |

**The MARGIN gate is `Absent(no_live_session)` and was registered as unfireable
in this stage before any measurement was taken.** A margin is a property of the
account and needs a U-prefixed session. Two operator constraints block one, both
recorded rather than worked around: the machine's internal fans are not
functioning, so concurrent live and paper sessions are not run, and no separate
live profile exists for this project.

**The COST gate is `Absent(insufficient_sample)` at n = 0 of 20 windows, and it
carries a second block that survives the first.** Even a complete 20-window
census could not produce a PASS while the fee leg is absent, because the all-in
sum cannot be formed and a strict lower bound can FAIL but never PASS.

> **Both gates are blocked from PASS for independent reasons, so the terminal
> state is over-determined: fixing the Gateway alone would not change it.**

## 2. The premium basis, fixed before any spread was measured

**The registered COST ceiling is 34.600 bps of notional, from the most recent
quarter's 112.72 bps at n = 491, not 49.610 bps from the full sample's 142.740
bps lower bound at n = 1,955.**

**Reason, in mechanism terms:** the BTC premium decays monotonically across all
four quarters, **284.53, 250.59, 145.13 and 112.72 bps at n = 488, 488, 488 and
491, a 60.4% fall**, so the sample is non-stationary by its own measurement, and
the mean of a trending series describes its history rather than estimating its
next value. A seller collects the premium in force over the 30-day tenor held.

**The qualification, stated rather than buried:** 142.740 bps is a one-sided 95%
lower bound and 112.72 bps is a point estimate, so the swap changes level and
confidence together. **The most recent quarter's own lower bound is
`Absent(not_recorded)` at n = 0 recorded confidence bounds in VRPExperiment**, and
is not computed here because that would re-read a spent sample. A one-sided lower
bound never exceeds its point estimate, so **the registered 34.600 bps ceiling is
an upper bound on the like-for-like ceiling: too generous if anything, never too
strict.**

## 3. IB Gateway is unreachable, measured

**0 of 13 TCP connect attempts across three probes reached a listener, all
`ECONNREFUSED`, with refusals timed at 0.012 to 0.113 ms over n = 5 in the
opening probe.**

Release **10.45** is installed and `~/Jts/jts.ini` records `tradingMode=p`,
`ApiOnly=true` and `TrustedIPs=127.0.0.1`, so the paper configuration is present
and the process is not up. **No IBC or IBController exists on this machine (n = 0
install directories found)**, so IB Gateway starts only through its GUI login and
an interactive IBKR credential entry, which this session holds none of.

A second gap: **`MBT_IB_PAPER_CLIENT_ID` is empty**, and the config guard refuses
before opening a socket, naming the variable.

**Futures options permission on CME crypto products is
`Absent(gateway_unreachable)`, which is NOT `Absent(no_permission)`.** Permission
was not found absent; it was not measurable, because no session exists to ask.
The two states are not merged, and the distinction is why the harness was still
worth building.

## 4. The exchange and regulatory fee leg is absent for three independent reasons

**`Absent(not_served)`, with n = 3 independent sufficient reasons:**

1. **`OrderState` in `ib_async 2.1.0` carries 17 fields, one commission triple,
   and zero exchange or regulatory fee fields.** There is no breakdown to record,
   with or without a session.
2. **Paper fills are simulated**, so a fee read from one measures the simulator
   rather than CME.
3. **CME refused automated access to its schedule**, citing its own Data Terms of
   Use. VRPExperiment obeyed that refusal and this repository obeys it.

**What this does not establish:** the absence of a field does not prove the fee is
absent from the scalar `commission`, only that the response cannot distinguish
them.

**Direction and magnitude of the resulting error:** every absent leg is
non-negative, so the measured legs form a strict lower bound and the bound errs
**permissively**. **The registered 34.600 bps ceiling overstates the room
available to the spread legs by exactly the unmeasured fee `F ≥ 0`, a quantity
bounded below at zero and not bounded above by any evidence held here (n = 0
measurements of it).** A number would be the estimate the stage forbids.

**A second absent leg pushes the same way:** IBKR charges a daily Exposure Fee and
names short options as its largest generator. Its magnitude is account-specific
and `Absent(not_served)`.

## 5. The census is armed and has not begun

| field | value |
|---|---|
| windows accepted | **0** |
| windows refused | **0** |
| windows required | **20** |
| median round-trip spread | `Absent(insufficient_sample)` at **n = 0** |
| p90 round-trip spread | `Absent(insufficient_sample)` at **n = 0** |

**The percentiles are absent, not zero and not nan**, and a test pins that over
an empty sample.

**The census is clock-bound at 5 collection days minimum**, from 20 windows at a
registered maximum of 4 per UTC calendar day with 60 minutes between them. **The
rule fixes the duration and not the start**, so the projection runs from the
first day a session exists. Had one existed on 2026-09-03 the census would have
completed **2026-09-09** across 5 collection days and 7 calendar days.

**Subscription state on all three instruments is `Absent(gateway_unreachable)`,
and none is assumed real-time**: an unreported market data type maps to UNKNOWN
and screening refuses UNKNOWN exactly as it refuses delayed, because IBKR
silently downgrades when no subscription covers an instrument.

## 6. The five guards, demonstrated rather than asserted

**28 refusals were provoked and captured** in `reports/guards/refusals.json`, each
carrying the exception type and message the guard actually produced, across
**n = 5 guards**.

**All 5 registered mutations behave as registered**, in
`reports/mutations/mutations.json`: each applied to real source, the right check
failed, the file restored byte for byte, the check returned green, and the whole
suite is green on the restored tree, with **0 failures across 5 mutations**.

### The mutation harness found a real defect, at n = 1

**Mutations 1 and 2 stayed green on the first run.** `build_short_option_order`
took the order class as a parameter, so the package's **only** order construction
read `order_cls(...)` and sat outside Guard 1's constructor list. **The defect
survived review, `mypy --strict`, `ruff`, and 156 passing tests, and was found by
flipping a flag and observing that nothing broke.**

Two fixes were kept: the site now constructs `Order` directly, and the scan holds
any call carrying a `whatIf` keyword to the literal requirement, keyed on the
argument rather than the callee.

> **A guard can refuse correctly while its test asserts nothing about the code
> that matters.** The refusal artifact showed Guard 1 refusing on synthetic
> sources the whole time, while the one real call site went unchecked.

## 7. The read-only boundary is unchanged

**Hashed before any work and again at closure: 2,901 entries, 324,887,193 bytes,
0 unreadable paths, on both snapshots.**

| digest | open | close | equal |
|---|---|---|---|
| full | `c28e6860…89f81` | `c28e6860…89f81` | **yes** |
| stable, 115 non-cache entries | `441495bc…53641` | `441495bc…53641` | **yes** |

**The two manifests are byte-identical**, which is an independent check that does
not rely on the digest. VRPExperiment's working tree is clean and its HEAD is
unchanged at `d37cf6d`.

## 8. What this stage does not establish

- **No margin was read**, in any environment, at **n = 0 what-if previews**.
- **No spread was measured**, at **n = 0 observation windows**.
- **No fee was determined**, at **n = 0 measurements**.
- **No premium was recomputed, extended or re-read.** VRPExperiment's 1,955-day
  sample is spent and was read only as text across a hashed boundary.
- **No order was transmitted**, and no path in the package can transmit one:
  the transmitting call sites number **0 across 17 package files**.
- **No capital was authorized and no position was sized.**
- **The harness has not been checked against a known answer**, so its MBT output
  would not be trusted even if a session appeared tomorrow. That is the binding
  condition on the verdict.
