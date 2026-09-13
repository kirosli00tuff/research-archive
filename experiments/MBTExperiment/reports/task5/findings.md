# Task 4 — the census, begun and refused

**0 of 20 windows accepted, 3 refused, at n = 3 attempts. The percentiles are
absent, not zero.**

| field | value |
|---|---|
| windows accepted | **0** of 20 required |
| windows refused | **3**, every one recorded with its reason |
| refusal reason | `unquoted_leg` on `future_hedge`, 3 of 3 |
| median round-trip spread | `Absent(insufficient_sample)` at **n = 0** |
| p90 round-trip spread | `Absent(insufficient_sample)` at **n = 0** |
| projected completion date | **`Absent(insufficient_sample)`** |

## Why every window was refused

**The at-the-money reference leg served no real-time touch, so registered
Section 3.1 refuses the whole straddle.** No reference price means no
at-the-money strike, and one is never substituted.

The cause is upstream of the census and is not a market condition. **No real-time
market data subscription covers CME crypto on this account.** Measured as broker
error 354 on all three registered legs under a real-time request, with error
10167 offering delayed data instead, **across n = 5 independent sessions between
19:11Z and 19:42Z**. The absence is persistent across sessions rather than a
transient outage in one, which is why the census is blocked rather than delayed.

## Delayed data was served, measured, and refused

**All three legs quote under a delayed request**, at n = 3 legs: the front future
at 81770.0 / 81785.0, the call at 1625.0 / 1860.0, the put at 6895.0 / 7200.0.

**Every one was refused as `delayed_tick` under registered Section 3.4**, and
none was widened into a cost band. These are **measured refusals on real venue
data**, which Stage B could only demonstrate on constructed inputs.

**No gap was filled from anywhere.** Deribit's 22.50 bps remains REFERENCE ONLY
and no gate in this repository reads it.

## The projection runs from a window actually collected, so it is absent

**None was collected, so there is no start to project from.** The registered rule
fixes the duration at **5 collection days** and does not fix the start; that
figure is a property of the rule and is unchanged from Stage B. It is not a
completion date, because there is nothing to add it to.

> **A projected completion date computed from a hypothetical start would be a
> schedule for a census that cannot begin.** The blocker is not time. No day of
> collection produces an accepted window while the subscription is absent.

## What the census ran as

**Discrete sampling with the session closed between windows**, never a resident
collector, because the machine's internal fans are not functioning. Each of the
3 attempts opened a session, took its reading, recorded its outcome and
disconnected.
