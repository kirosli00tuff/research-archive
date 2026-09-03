# TASK 7 — What fired, what did not, and the stage verdict

**Stage verdict: HARNESS-BLOCKED.** Computed from the recorded artifacts by
`mbt.verdict.decide`, not written by hand, and re-runnable with
`uv run python -m mbt.cli verdict`.

---

## 7.1 The gates

| gate | outcome | ceiling | measured | why |
|---|---|---|---|---|
| **MARGIN** | **ABSENT** | $1,000 per contract, being 12.80% of $7,812.46 | — | `Absent(no_live_session)`. A margin is a property of the ACCOUNT and needs a U-prefixed session. |
| **COST** | **ABSENT** | 34.600 bps of notional | — | `Absent(insufficient_sample)`: **0 of 20** registered windows, and the fee leg is `Absent(not_served)` regardless. |

**Neither gate fired, and both are recorded with their reasons rather than
omitted from the table.** An absent gate is a recorded state. It is never an
unfired gate quietly dropped from a verdict, and never a paper figure promoted to
stand in for a live one.

### The MARGIN gate, and why it is not merely unfired

It is registered `Absent(no_live_session)` naming both operator constraints: the
machine's internal fans are not functioning, so concurrent live and paper
sessions are not run, and no separate live profile exists for this project.

**It was never going to fire in this stage**, and Section 0.3 registered that
before any measurement. This is not a shortfall against a target; it is the
registered state.

### The COST gate, and its two independent blocks

**Block 1, the census: 0 of 20 windows.** The registered minimum is 20 distinct
observation windows and the census has not begun, because the Gateway is
unreachable and `MBT_IB_PAPER_CLIENT_ID` is unset.

**Block 2, the fee leg, which survives block 1.** Even a complete 20-window
census could not produce a PASS. The fee leg is `Absent(not_served)`, so the
all-in sum cannot be formed at all, and the gate falls back to the measured legs
as a strict lower bound. **A lower bound can FAIL and can never PASS** (Task 6,
§6.5). `mbt.gates.fire_lower_bound` implements exactly that asymmetry and
`tests/test_guards.py` pins that no bound at or below the ceiling ever returns
PASS.

> **So both gates are blocked from PASS for independent reasons, and the stage's
> terminal state is over-determined.** Fixing the Gateway alone would not change
> the verdict.

## 7.2 Interim figures, labelled as interim

**There are none.** The census holds 0 accepted and 0 refused windows, so there
is no interim spread figure to report, and the percentiles are
`Absent(insufficient_sample)` rather than zero or nan.

Reported as required, with `n` in the same sentence as the number: **the median
and 90th-percentile round-trip spreads are absent at n = 0 of a registered
minimum of 20.**

## 7.3 The verdict, condition by condition

REGISTRATION.md Section 0.1 registers HARNESS-READY as requiring four things at
once. Two hold.

| condition | held | evidence |
|---|---|---|
| the harness builds | **yes** | no-transmit scan CLEAN over 16 package files, 0 findings |
| all five guards fire under mutation | **pending Task 8** | `reports/mutations/mutations.json` |
| **the known-answer test reproduces an independently checkable margin** | **NO** | the check did not run: no session, and no operator-supplied expected value |
| the census is armed with its projected completion date | **yes** | 5 collection days required, 0 of 20 collected |

**The verdict is HARNESS-BLOCKED, and the binding condition is the known-answer
test.** The harness has not been checked against an independently known margin,
so its MBT output would not be trusted even if a session appeared tomorrow.

**HARVESTABLE-CONFIRMED and VENUE_BLOCKED are not reachable from this stage and
are not represented in the verdict machinery.** Both need the MARGIN gate.

**HARNESS-BLOCKED is an expected outcome and a fully acceptable one.** No
threshold was softened, no friendlier spread source was substituted, no refused
window was dropped to reach twenty, no paper figure was promoted into a gate, and
the premium basis was fixed in Section 0.6 before any spread existed and has not
been reselected.

## 7.4 The live margin read, as a named open operator item

Named rather than left as a missing number.

> **OPEN OPERATOR ITEM — the initial margin on a short MBT option.**
> It is a property of the **account** and needs a session on a **U-prefixed**
> account. Two operator constraints block it, both recorded rather than worked
> around:
>
> 1. **The machine's internal fans are not functioning**, so concurrent live and
>    paper sessions are not run.
> 2. **No separate live profile exists for this project yet.**
>
> Lifting the paper-only clause is an operator edit to `CLAUDE.md`, never a flag.
> The harness needs no change to accept a live session: `SessionProvenance`
> derives the environment from the account the broker reports, and the MARGIN
> gate fires the moment it receives a U-tagged figure.

### Two further open operator items, both smaller

1. **`MBT_IB_PAPER_CLIENT_ID` is unset in `.env`.** The config guard refuses
   before opening a socket and names the variable.
2. **IB Gateway is not running.** Release 10.45 is installed and configured for
   paper. There is no IBC on this machine, so it starts only through an
   interactive IBKR login.

**Neither of those unblocks the MARGIN gate**, which needs the live profile. They
unblock the census and the known-answer test.
