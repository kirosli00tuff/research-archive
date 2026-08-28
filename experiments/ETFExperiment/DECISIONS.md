# DECISIONS.md — numbered architecture decision records

Every ADR is dated, states the context that forced it, the decision, the
alternatives rejected **with the reason they were rejected**, and its
consequences. An ADR is never edited after the fact; a reversal is a new ADR
that supersedes it by number.

Figures carried from outside this repository are labelled **carried**. Figures
measured here travel with their n.

---

## ADR-001: The entry anchor is provisional, and exactly one measurement may move it

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §3.2

**Context.** The signal is a flow print with no published timestamp. A rule that
enters "after the print" needs a clock time, and choosing that clock time after
seeing which choice admits more days is the selection this whole registration
exists to prevent.

**Decision.** The anchor is registered **provisionally at 08:00 UTC on day
D+1**. **The measured 95th percentile first-print time from A.1 Task 3 is the
only input that may move it**, and only in one direction: if that percentile
falls later than 07:00 UTC, the anchor moves to the next whole hour after it, by
dated amendment, **before any outcome read and before any admissibility count is
final**. The rule is a pure function (`etf.anchor.amended_anchor_hour`), the
percentile is nearest-rank and deterministic, and the tests sit exactly on the
trigger: a measured p95 of exactly 07:00 leaves the anchor at 08:00.

**Alternatives rejected.** *Registering the anchor from the source's documented
publication convention*: A.1 Task 1 measured that the source documents no
publication time at all — its own note says only "generated automatically, in
real time", and the words "evening" and "night" appear zero times across both
served pages (n = 2 pages). There was nothing to register from. *Choosing the
anchor after the census*: that is fitting the rule to the sample. *Letting the
admissible-day count move it*: the same objection, one step removed.

**Consequences.** The A.1 Task 4 retro evidence suggests the print lands between
roughly 04:00 and 08:00 UTC (Amendment 2 §4) and therefore that the anchor may
well move. **It has not moved and will not move on that evidence**, because
archived capture times are censored by a crawl schedule this project did not
choose. Recording the prediction now means the forward result cannot later be
read as confirming whatever was convenient.

---

## ADR-002: The as-printed value is the one in the capture, and a later value is never substituted

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §3.1

**Context.** The MLCryptoEngine H11 precedent: a free flow source with
whole-file regeneration whose past rows revise. A design that reads today's
value for a past day silently tests a number nobody could have traded, and H11
died on exactly that property, **discovered rather than registered**.

**Decision.** The as-printed value for trading day D is the aggregate net flow
for D **as served in a capture strictly before the entry anchor**. A later
value, however authoritative, is **never** substituted. Where the two differ the
day is flagged `revised` and the difference is recorded in USD and as a share.
**Strictly before**, with the boundary fixture sitting exactly on the anchor.

**Alternatives rejected.** *Taking the settled value and treating revisions as
noise*: it is not noise, it is look-ahead, and the sign-flip rate is precisely
the quantity that would corrupt E1 toward a false positive. *Averaging the
captures around the anchor*: an average is a value nobody could have read.

**Consequences.** Admissibility becomes a property of the archive rather than of
the source, which is what made the A.1 Task 4 density measurement decisive
rather than procedural. Measured: 11 of 333 days (Amendment 2).

---

## ADR-003: The directional primary is a permutation test on rank correlation, not a sign test

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §8

**Context.** The handover sketch proposed a distribution-free **sign test** as
the directional primary. Exact binomial power on roughly 330 days does not reach
80 percent at that test **even under the undecayed published effect**, so
registering it would register a bar the sample cannot reach — the
InsiderExperiment failure mode, where a design's own arithmetic blocks it before
any data exists.

**Decision.** **E1 is an exact permutation test on the Spearman rank correlation
between the admissible as-printed signal for day D and the next-day return, over
all admissible days, one-sided positive, no threshold.**

**Why threshold-free, deliberately.** It uses **every** admissible day. A
thresholded test discards every day inside the ±100M band, which the measured
signal distribution puts at 81 of 333 days (24.3 percent, n = 333). It is the
highest-powered distribution-free test available on this sample.

**Alternatives rejected.** *The sign test*: registers an unreachable bar.
*A t-test on returns*: not distribution-free, and daily crypto returns are not
the shape it assumes. *A thresholded rank test*: strictly lower powered, for no
gain the economic co-primary does not already provide.

**Consequences.** The null distribution depends on n alone, so the critical
value is computable without any distributional assumption. Pinned by test: the
simulated critical value agrees with the known 1/√(n−1) asymptotic, and the size
of the test under a zero true effect sits at its nominal alpha.

---

## ADR-004: The registered effect assumption is half the published one, and the halving is not discretionary

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §9

**Context.** The published next-day leg reports Newey-West **t 3.12 over 313
trading days** (carried), implying a rank correlation near **0.18**. Registering
power against 0.18 would register an assumption the pre-existing evidence
already contradicts.

**Decision.** **The registered primary assumption is a rank correlation of
0.09.** The rationale is registered with it and is not a judgement call:

- the **same author's** extended-sample IV estimate falls from **0.41 to 0.20
  percent per 100M USD** on 563 days against 313 — roughly half (carried);
- the independent 90-day rolling correlation fell from a **February 2026 peak of
  0.68 to 0.16** by 2026-05-14, inside the test window (carried).

Powers at the undecayed **0.18** and at a quartered **0.045** are computed and
reported beside it as the honest range — the NPLExperiment H3 pattern, where a
single assumption would have hidden how much the verdict turned on it.

**Alternatives rejected.** *Registering at 0.18*: contradicted by the author's
own longer sample. *Registering at 0.045*: no evidence supports a quartering
specifically; it is reported as the pessimistic end of a range, not as the
assumption. *Registering a range and picking after the census*: that is choosing
the bar after seeing the sample.

**Consequences.** Section 0's GO requires 80 percent power at **0.09**, which the
registration states in advance is unlikely — the registered expectation is
DEGRADED, recorded before any data existed.

---

## ADR-005: The cost bands, and the 3 bp end is never the central case

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §6

**Context.** Fee schedules are dated measurements, not constants — the ADR-055
pattern from MLCryptoEngine, where a Kraken tier recorded once was found stale
and corrected from 0.40/0.80 to 0.25/0.40 with an explicit statement of which
closures flipped (none did).

**Decision.**

| venue | band (low, central, high) | role |
|---|---|---|
| **Hyperliquid BTC perp** | **3, 9, 18 bp** round trip | **verdict-bearing at 9** |
| Kraken spot | 50 bp maker / 80 bp taker round trip | descriptive, reported beside |
| IBKR | **none** | closed by error 10243 |

**9 bp is taker both legs** at the venue's 4.5 bp taker per side (carried). **The
3 bp end is maker both legs and is reported as an upper-bound-of-optimism, never
as the central case, because a daily signal must fill**: a rule that must be in
the market at a fixed clock time cannot assume both legs rest passively.

**IBKR carries no band at all.** The API refuses fractional-sized orders with
error 10243 (HFExperiment `reports/stage_a1b/a1b_report.md` line 52), so no
equity-side implementation exists and a band would imply one. `etf.costs.ibkr_band`
returns `None`, pinned by test.

**Consequences.** The measured pre-period daily volatility is 2.74 percent
(n = 475 returns), so the 9 bp round trip is about **3.3 percent of one daily
standard deviation**. Costs are not the binding term on this design; effect size
is. That is worth stating because it is the opposite of every prior closure in
the house record.

---

## ADR-006: The blindness lists, stated exactly, and enforced on the parse tree

**Date:** 2026-08-28 · **Status:** accepted · stated in CLAUDE.md

**Context.** A blindness rule enforced by intention is not enforced.

**Decision.** Outside the sealed writers:

- **Flow payload fields: every field is readable**, including the values
  themselves, plus this repository's own capture timestamp. **Flow is signal.**
- **Price payload fields: `t`, `T`, and row count only.** Never `o`, `h`, `l`,
  `c`, `v`, in any spelling, in any module.
- **Funding fields: `time` always; `fundingRate` only strictly before
  2025-05-01**, under ADR-007.

Enforced by AST scans over **`src/etf` and `scripts`** (`tests/test_guards.py`):
no module may look up a forbidden price key by subscript or `.get`; the funding
key may be **read** only in the gated reader; the pre-period boundary may be
read from config in exactly one module and hardcoded in none.

**Alternatives rejected.** *A text search*: the InsiderExperiment mutation
exercise proved it passes vacuously — a config key left in a comment while its
enforcement site became a literal matched the text and was called enforcement.
*Scanning only `src/etf`*: scripts are real enforcement sites here (the census,
the power gate, the access probes), and a rule that stopped at the package
boundary would let a script read a close with nothing failing.

**Consequences.** The mutation harness must be able to **name** the funding key
without **reading** it; that allowance is explicit, narrow, and itself pinned by
a test asserting the harness never looks the key up.

---

## ADR-007: The pre-period carve-out has exactly one address

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §9

**Context.** The E2 economic-power computation needs a volatility and a funding
level to size a net return against a 9 bp round trip. Taking them from the test
window would be reading the outcome to plan the test of the outcome. Inventing
them would register a number this repository did not measure — the NPLExperiment
H3 failure exactly.

**Decision.** **Power inputs may read BTC price and funding stamped strictly
before 2025-05-01.** That window sits inside the source study's own sample
(January 2024 through April 2025) and outside this test sample, so reading it
cannot leak a single observation the Stage B verdict is computed on.

The carve-out has **one address**: `etf.preperiod` holds the pin and
`etf.preperiod_prices` is the only file in the repository permitted to read a
close. Four structural guards hold it there: the file allowlist is length one;
that file must call `require_pre_period` **on its parse tree**, so an inlined
comparison fails; it may not import a network module, so it cannot widen its own
window; and it has exactly one caller.

**The refusal is total, not selective.** A payload with one row at or after the
boundary raises; nothing is dropped quietly, because a silently truncated
volatility series is a synthesized one.

**Consequences.** Demonstrated live rather than only on fixtures: the venue's
funding pages returned **72 of 72 readable pre-boundary rates and 0 gated**, and
**500 of 500 gated** on a page starting 2025-05-01. Boundary fixtures sit exactly
on the instant — 2025-04-30T23:59:59.999Z passes, 2025-05-01T00:00:00.000Z is
refused.

---

## ADR-008: Pacing is measured per endpoint, and an unmeasured endpoint keeps the slower figure

**Date:** 2026-08-28 · **Status:** accepted · registered by Amendment 1 §2

**Context.** The solattn ADR-021 lesson, learned there the expensive way: two
GeckoTerminal endpoints on one host held 6.0 s and 12.0 s, and the project's own
earlier measurement of the first was exactly the kind of "documentation" the
measured-beats-documented rule warns about.

**Decision.** Paces are keyed **per endpoint**. Measured 2026-08-28 by an
escalation ladder, `BURST = 6` per rung, stopping at the first non-200:
**no ceiling was found on any endpoint at or above this repository's own
absolute floor of 1.0 s — 96 requests, every one HTTP 200.**

Operating paces are set at **twice the fastest verified-clean spacing**: half the
highest verified-clean **rate**, because there is no ceiling to halve. `flow.table`
10.0 s (clean 12.17/min, n = 18); `archive.availability` and `archive.timemap`
2.0 s (59.92 and 21.28/min, n = 18 each); `venue.candleSnapshot` and
`venue.fundingHistory` 2.0 s (59.90 and 59.91/min, n = 12 each); `kraken.ohlc`
2.0 s (58.73/min, n = 18). **`venue.meta` and `archive.snapshot` were not
measured and keep their slower pre-measurement figures** — inheriting a
sibling's is the inference ADR-021 forbids.

**Alternatives rejected.** *Probing below 1.0 s to find a real ceiling*: this
project will never send faster than its own floor, so a ceiling below it is not
actionable, and probing there is aggression without information. *Applying one
host figure across its endpoints*: the ADR this one ports exists because that
was wrong.

**Consequences.** The figures are bounded by what was probed, not by what the
server would refuse, and the record says so rather than implying a measured
ceiling exists.

---

## ADR-009: The daily pass seals the day that closed, never the open day

**Date:** 2026-08-28 · **Status:** accepted · the solattn ADR-019 shape, ported with its defect pre-fixed

**Context.** In solattn the daily pass sealed the UTC day it was *running in*, so
every seal attested a 40-minute-old partial file: **all eight seals mismatched
their contents** on 2026-08-24. The files were never damaged. An attestation of
the wrong content is worth less than no attestation, because it teaches readers
to expect mismatches.

**Decision.** The pass on day D+1 at **12:20 UTC** seals day D, now closed and
final. `seal_day` **refuses** a day that has not closed. **The seal runs first in
the pass**, so it lands within a minute of the timer fire rather than after a
multi-hour fetch, and a failed attestation stops the pass loudly before anything
else runs. `read_day` verifies before serving: a mismatched seal raises, and a
closed day with no seal past a 13-hour grace raises rather than reading
unattested — **a missing attestation is an error, never a pass**.

**Consequences.** Ported with the defect already fixed rather than after
reproducing it. The refusal boundary is pinned with a fixture one second past
midnight, where yesterday is sealable and today is not.

---

## ADR-010: The snapshot cadence brackets the print window, and the wrap is the whole point

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §12

**Context.** The lag measurement's resolution is bounded below by the capture
cadence, and the print window straddles midnight UTC.

**Decision.** **Every 20 minutes across 20:00–14:00 UTC**, the window that
brackets the print and the revision window, and **every 2 hours otherwise**. The
peak window **wraps midnight**, so the membership test is a disjunction, not a
range. Getting that backwards would sample the print window at the off-peak rate
and understate the first-print time by up to two hours — the one figure this
repository turns on.

Fired by `etf-snap.timer` every 20 minutes with `Persistent=true`; the script
decides whether the registered cadence asks for a capture and **records a skip as
a skip rather than as a failure**.

**Consequences.** Every quoted lag figure carries its cadence floor of 20
minutes beside it, because no measurement of a first-print time can be sharper
than the interval that looked for it.

---

## ADR-011: A dash is never a zero, and the source's own Total column is never read

**Date:** 2026-08-28 · **Status:** accepted

**Context.** Measured at A.1 Task 1: **the flow table prints `0.0` in its
`Total` column on a day where every per-fund cell is a dash — 3 of 3 such rows
over n = 336 out-of-sample rows** (26 May 2025 Memorial Day, 19 Jun 2025
Juneteenth, and the open day at capture time).

**Decision.** The signal is computed from the **five registered per-fund cells**
and the source's `Total` column is **never** consumed. A dash is
`Absent(dash_in_cell)`, which refuses coercion to a number, and **one absent
fund makes the whole aggregate absent**.

**Why the strictness is not fussiness.** On the open day, *every capture taken
before the print lands* shows all dashes and a `Total` of `0.0`. Consuming
`Total` would have recorded a printed zero for the open day on every such
capture, and the A.1 Task 3 lag measurement would have reported that **every day
prints at 00:00 UTC** — a clean, precise, entirely fabricated answer to the
question this repository exists to ask.

**Alternatives rejected.** *Substituting zero for a fund that reported late*: on
a day the largest fund is missing, that fabricates the **sign** of the
aggregate, which is the quantity the Section 4 rule trades on. *Reading `Total`
and cross-checking*: it is the wrong universe anyway — the source's `Total`
spans 12 funds against the registered 5, differing by a mean of **47.42M USD**
(median 27.20M, range −903.20M to +1,205.20M, n = 333).

---

## ADR-012: Citi is recorded as FAILED TO CONFIRM, not as corroboration

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §14.3

**Context.** Citi's note of 2026-07-01 cut its twelve-month BTC target to 82,000
USD and cut assumed twelve-month net ETF inflows to zero, and has been reported
as external validation of the flow-impact result (carried).

**Decision.** **Recorded as FAILED TO CONFIRM.** Three reasons, each sufficient:

1. Reporting shows **Citi cited an external academic study rather than running
   its own regression**, and the dataset description is the source study's. A
   citation of a result is not an independent replication of it; treating it as
   one **double-counts a single measurement**.
2. Citi's own quantified claim (analyst Alex Saunders) is that flows explain
   roughly **45 percent of weekly BTC moves** — **weekly and contemporaneous**,
   not next-day and predictive.
3. **The tradable leg is the next-day one**, and nothing in the note addresses
   it.

**Alternatives rejected.** *Recording it as supporting evidence with a caveat*: a
caveat attached to a headline is read as the headline. *Omitting it*: the claim
exists in the public record and a registration that ignores it is choosing its
evidence.

**Consequences.** The registered prior is unmoved by it. The assistant prior of
0.10 was recorded with this note already known.

---

## ADR-013: The venue serves a rolling 5,001-candle window, so the sealed collection cannot wait

**Date:** 2026-08-28 · **Status:** accepted · registered by Amendment 1 §3(a)

**Context.** Measured at A.1 Task 1 by bisection (n = 17 probes): `candleSnapshot`
caps at **5,001 rows**. At `1h` that reaches back only to **2026-02-01T11:00Z**
and **slides forward one hour per hour** — 5,001 hours is 208.4 days, and the
served start matches to the hour. `1d` candles reach 2020-08-19 and are not
constrained.

**Decision.** Three consequences, registered rather than worked around:

1. **A day older than the rolling window has no registered outcome.** Section 5's
   anchor-to-anchor-plus-24-hours return is not computable from `1d` candles,
   whose boundaries are 00:00 UTC. Such a day is `underpowered` — a recorded
   absence, never a return, and **never a 1d substitute**, which would silently
   redefine the anchor the whole design turns on.
2. **The sealed collection of A.2 Task 3 runs before Section 0 fires**, because
   every day of delay permanently destroys one day of retro coverage and there
   is no archive for it. This is the durability argument the brief makes for the
   forward flow ledger, binding harder.
3. **The sealed span is wider than the registered hold**: 48 hours per trading
   day, from D+1 00:00Z, which contains the anchor-plus-24-hours window for
   **any** anchor hour ADR-001's amendment could choose. Sealing wide is
   anchor-agnostic and is not a second look, because nothing in the sealing path
   reads a value.

**Consequences.** Sealed 2026-08-28: **5,002 hourly rows and 11 funding pages
covering 5,002 hours**; **142 of 333 out-of-sample trading days** are covered at
the registered 0.95/0.95 bars.

---

## ADR-014: Pacing is ledger-backed, because a limiter that dies with its process paces nothing

**Date:** 2026-08-28 · **Status:** accepted

**Context.** Found during A.1 Task 1. `PacedClient` held its last-sent times in
the instance, so each script invocation started with an empty map and the
registered spacing was enforced only *within* a single run. **The collectors fire
as separate systemd invocations, so in production the limiter would have paced
nothing at all.**

**Decision.** `_pace` waits the **longer** of two gaps: the in-process monotonic
gap, and the gap since the endpoint's last **charge row in the request ledger** —
the only state shared across processes. Pinned by a test that builds a brand-new
client and asserts it still sleeps.

**Consequences.** The request ledger is now load-bearing for pacing as well as
for the cap, which is a dependency worth naming: a corrupted ledger stops
collection loudly (`require_intact` at startup) rather than silently unpacing it.

---

## ADR-015: Admissibility needs a served value, not merely a capture

**Date:** 2026-08-28 · **Status:** accepted · supersedes the density figure of Amendment 1 §3(b) · registered by Amendment 2

**Context.** Amendment 1 recorded archive capture density as **37 of 333
(0.1111)** from the timemap alone. The timemap answers *"was there a capture"*.
Section 3 asks *"did a capture strictly before the anchor **serve a flow value**
for that day"*, and those are different questions.

**Decision.** Admissibility is tested by **fetching the qualifying capture and
parsing it**. Measured across all 37: **11 served a value, 23 showed the day
still dashed, 2 carried no row, 1 returned HTTP 403.** **The archive capture
density is 11 of 333 = 0.0330.**

**Consequences.** Amendment 1's figure is **falsified, and recorded as falsified
rather than corrected in place** — the registration is append-only. This is
Section 14.7's own correction landing on this repository: a figure that was not
measured end-to-end entered a record, and measurement moved it by a factor of
3.4. Two further census defects surfaced with it: an **unbounded**
`capture_too_late` test (296 reported against a true 53), and a failed archive
fetch filed as an **exclusion** rather than as `source_failed`, which let an
instrument fault masquerade as a narrowed cohort.

---

## ADR-016: The trading-day universe is the source's own date rows

**Date:** 2026-08-28 · **Status:** accepted

**Context.** The census needs a US trading-day calendar for 2025-05-01 onward.

**Decision.** **The flow source's own date rows are the universe.** Section 2
defines an event as "one per US trading day on which an admissible as-printed
flow value exists", so the days the table serves a row for **are** the universe,
and that is measured rather than assumed from a hardcoded holiday calendar which
would itself be an unverified carried figure.

**Consequences.** Measured: **336 date rows on or after 2025-05-01, of which 333
print a value**; the 3 that do not are 26 May 2025, 19 Jun 2025 and the open day.
The two closed ones are US market holidays, which the rule excludes correctly
without ever being told what a holiday is.

---

## ADR-017: The verdict machinery is built dark and refuses sealed paths in code

**Date:** 2026-08-28 · **Status:** accepted · registered as REGISTRATION.md §10

**Context.** A verdict engine written after seeing the data is a second look
wearing a first look's clothes.

**Decision.** `etf/verdict.py` computes E1, E2 and every named secondary
**against synthetic fixtures only**. `refuse_sealed_path` raises on any path
under `data/outcomes`, `data/funding`, `data/retro` or `data/census`. Tests pin
that **no Stage A module imports it at all**, and that it imports no network or
sealing module. **A statistic not named in Section 8 does not exist in the
file.**

**The canary is mandatory.** A planted-signal fixture must fire both primaries,
and a pure-noise fixture must fire neither. An engine that cannot detect a
planted effect proves nothing about a null.

**Consequences.** Stage B calls it exactly once, behind a latch written first.

---

## ADR-018: The manual-run guard, and the override is named so it appears in the record

**Date:** 2026-08-28 · **Status:** accepted

**Context.** Two processes appending to one ledger produce rows ordered by
neither clock nor file position, and the standing rule that multi-process logs
are ordered by clock only holds if the writers are known.

**Decision.** A hand-run collector **refuses while its systemd unit is active**.
The override is a named environment variable, `ETF_ALLOW_MANUAL_RUN=1`, so the
override appears in the shell history of whoever took the risk. A missing
`systemctl` reads as not-active rather than raising, so the guard never blocks a
machine that has no systemd at all.

**Consequences.** The scheduled invocations pass `--scheduled` and bypass the
check by design; nothing else does.

## ADR-019: H1 closes on the deadline finding, and the closure is deliberately robust to the one unpinned figure

**Date:** 2026-08-28 · **Status:** accepted

**Context.** Amendment 3 eliminated GO on measured inputs and left the
DEGRADED-versus-BLOCKED choice turning on a forward revision-integrity leg whose
earliest completion was 2026-09-22. Amendment 4 then established that Section
10's Stage B trigger needs a governing minimum N of 300 against a projected 163
at the registered deadline. **The two findings are independent, and the second
governs.** Waiting 24 days for a label that changes no operational consequence
is a delay, not a decision.

**Decision.** H1 closes at `untestable-at-achievable-power`, by operator
decision, on 2026-08-28. Section 0 is left partially fired and the residual
choice is recorded as moot rather than resolved.

**The closure is constructed so it does not rest on the weakest figure in the
record.** Amendment 4's governing minimum of 300 comes from an E2 power estimate
reading exactly 0.8000 at 300 simulations, where the binomial standard error is
0.0231. An estimate sitting precisely on its own bar is not pinned, and the true
minimum could be 350 or 400. **Rather than close on it, the closure is stated
against E1's 237** — the smallest minimum anywhere on the record, at the
undecayed published magnitude, discarding the second co-primary entirely. The
projected 163 falls short of even that by 74 days. **Every direction the
unpinned figure could move enlarges the shortfall.** The caveat is carried on
the reopen path, where it does bind, and a reopening under threshold (c) must
pin it first.

**Alternatives rejected.** *Waiting for 2026-09-22*: the revision leg
distinguishes DEGRADED from BLOCKED and neither branch alters the accrual rate
or the deadline, so it buys a label. *Amending the deadline to 2027-12-31 and
continuing*: legitimate, outcome-blind, and nearly free in compute, and it was
declined on what it purchases rather than on what it costs. An extension buys
the **published 0.18** assumption only; at the **registered 0.09** assumption
the minimum N exceeds 1,200, which at 20.8 admissible days per month arrives
around 2031. A Stage B under the extension answers only whether the effect
persists at its published magnitude, and a FAIL still cannot separate decay from
absence, which is the distinction the registered assumption exists to draw.
*Closing at `signal-absent`*: refused, and refused emphatically. No outcome
value was read. Mistyping a power closure as a signal closure would be the
precise failure this register was written to prevent.

**Consequences.** `etf-daily` is disarmed. `etf-snap` continues, decoupled from
any registered hypothesis, because §4 of Amendment 5 establishes forward capture
as the only route to as-printed flow data and a forward ledger gap cannot be
backfilled. The operator prior slot stays empty; no verdict was formed, so there
is nothing to score, and the assistant's 0.10 was never copied into it. The
archive-density finding (0.0330 measured, 0.3363 unbounded ceiling, 0.316
mementos per calendar day) outlives this hypothesis and constrains any future
as-printed retrospective design in this house.
