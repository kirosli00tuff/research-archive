# TASK 5 — The bid-ask census, armed and not begun

**Outcome: ARMED, 0 of 20 windows collected.** The census cannot begin, and the
reason is the same two operator items that block Task 4. It is recorded as a
census with zero windows, not as a census that failed.

---

## 5.1 The task is clock-bound and cannot be compressed

Stated up front, as required, and derived from the registered rule rather than
estimated.

**The registered distinctness rule** (REGISTRATION.md Section 3.5):

> Two observation windows are distinct if and only if their local capture
> instants differ by at least **60 minutes**, and at most **4 windows** are drawn
> from any one **UTC calendar day**.

**The arithmetic that follows:** 20 windows ÷ 4 per day = **5 collection days
minimum.** CME crypto trades Sunday 17:00 CT to Friday 16:00 CT, so a UTC
collection day is Monday through Friday and the weekend is not one.

> **The rule fixes the DURATION at 5 collection days. It does not fix the
> START.** No amount of effort, parallelism or compute compresses it below 5
> days, and the projected completion date runs from the first day a Gateway
> session exists.

### Projected completion, computed from the rule

`tools/census_projection.py` computes this from a start date rather than
hard-coding one, because a hard-coded date goes stale the moment the start slips.

| if the first collection day is | five collection days are | **completes (UTC)** | elapsed |
|---|---|---|---|
| **2026-09-03 Thu** *(had a session existed today)* | 09-03, 09-04, 09-07, 09-08, 09-09 | **2026-09-09** | 7 calendar days |
| 2026-09-04 Fri | 09-04, 09-07, 09-08, 09-09, 09-10 | 2026-09-10 | 7 calendar days |
| 2026-09-05 Sat *(not a collection day)* | 09-07, 09-08, 09-09, 09-10, 09-11 | 2026-09-11 | 5 calendar days |
| 2026-09-07 Mon | 09-07, 09-08, 09-09, 09-10, 09-11 | 2026-09-11 | 5 calendar days |
| 2026-09-08 Tue | 09-08, 09-09, 09-10, 09-11, 09-14 | 2026-09-14 | 7 calendar days |

**The census has not begun, so none of these dates is the projection. The
projection is "five collection days from the first day a session exists."**

## 5.2 Subscription state on all three instruments, before any window

The task requires verifying and recording the real-time subscription state on
**both option legs and the MBT front future** before appending any window.

| instrument | subscription state | tick delay status |
|---|---|---|
| MBT option, ATM call | `Absent(gateway_unreachable)` | `Absent(gateway_unreachable)` |
| MBT option, ATM put | `Absent(gateway_unreachable)` | `Absent(gateway_unreachable)` |
| MBT front future, the hedge leg | `Absent(gateway_unreachable)` | `Absent(gateway_unreachable)` |

**None is assumed to be real-time.** `mbt.figures.status_from_market_data_type`
maps an unreported code to `TickDelayStatus.UNKNOWN`, and
`mbt.quotes.screen` refuses `UNKNOWN` with `Absent(delayed_tick)` carrying
*"an unreported status is never assumed to be real-time."* IBKR silently
downgrades to delayed data when no subscription covers an instrument, so "no
status" and "delayed" are made to fail the same way by design.

## 5.3 All three legs are sampled, and the harness enforces it

**A spread measured on the options alone understates the hedge leg**, which the
registered rule trades a median of **11** and a p90 of **16** times over the
tenor (n = 1,955 paths, VRPExperiment). The hedge leg is where most of the
rebalance cost lives.

`mbt.census.REQUIRED_LEGS` is `("option_call", "option_put", "future_hedge")`,
and `build_window` refuses a window missing any one of them **before screening
any leg**, so a window is never half recorded.
`tests/test_census.py::test_every_required_leg_is_actually_required` exercises
all three cases.

## 5.4 Per-window recording, implemented and unexercised by real data

Each accepted window records, per leg: **bid, ask, venue timestamp, local
timestamp, subscription note, and tick delay status.** The two clocks are held in
`mbt.clock.ObservationClock` and never conflated, because their difference **is**
the staleness the census refuses on and a single merged clock cannot express it.

Six refusal conditions are implemented and each returns a typed absence:
unquoted leg, crossed book, zero bid, stale timestamp, delayed tick, frozen tick.
All six are demonstrated in `reports/guards/refusals.json` as provoked refusals
carrying their actual messages.

**A refused window is recorded with its reason and never dropped.** Dropping
refusals to reach 20 would turn the count into a selection, and the selection
would be on exactly the book states the refusal conditions identify as unusual.

**No gap is ever filled by widening a figure from another venue.** Deribit's
22.50 bps is REFERENCE ONLY, per REGISTRATION.md Section 4 and ADR-008.

## 5.5 Discrete sampling, because the fans are not working

The census runs as **discrete sampling with the session closed between windows,
never as a resident collector.** `make b-census` appends **one** window and
exits. There is no daemon, no timer and no long-lived process in this repository,
and no systemd unit was installed.

**A missed window is a gap in a discrete sample and is recorded as one, never
backfilled.** The CLI records exactly that when it cannot append:

> *"no session, so no window was appended. A missed window is a gap in a discrete
> sample and is recorded as one, never backfilled."*

## 5.6 The census as it stands

| field | value |
|---|---|
| windows accepted | **0** |
| windows refused | **0** |
| windows required | **20** |
| meets minimum | **false** |
| median round-trip spread | `Absent(insufficient_sample)` |
| p90 round-trip spread | `Absent(insufficient_sample)` |

**The percentiles are absent, not zero and not nan.** `mbt.census.percentile`
refuses an empty sample rather than returning a number, and
`tests/test_census.py::test_an_empty_census_reports_absent_rather_than_zero`
pins it.

Artifact: `reports/task5/census_status.json`.
