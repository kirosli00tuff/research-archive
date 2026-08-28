# report.md — ETFExperiment, stage by stage

Stage-sectioned in the MLCryptoEngine shape. **Each section is written for the
moment it landed**, not for someone reading months later. Nothing above a
section is rewritten when a later section contradicts it; the contradiction is
recorded where it happened.

Every figure travels with its n. Figures carried from outside this repository
are labelled **carried** and were not measured here.

---

## Stage A.0 — registration, before any network call

**2026-08-28, 07:53Z to 08:11Z. 18 minutes against 112 minutes of stated ETA.**

The repository was created, the governing prompt logged verbatim, and six
prior-art files read for patterns. Then the scaffold, the five standing guards,
CLAUDE.md, REGISTRATION.md Sections 0–14, and HYPOTHESES.md — **every one of
them committed before this repository had sent a single request to any
endpoint.** The request ledger did not exist at the moment Section 0 was
committed, and that ordering is what makes this a pre-registration rather than a
description.

**The ETAs were long by a factor of about six, and that is recorded rather than
smoothed.** They were drawn from InsiderExperiment's Stage A.1 table, where a
comparable scaffold-plus-registration took 18 of 51 recorded minutes; the error
was that those figures included corpus building and a power computation this
stage does not do.

**Three decisions taken inside A.0, each recorded at the time:**

1. **The Section 0 residual band was registered rather than left as a gap.** The
   three clauses of the outcome map leave one case unnamed — E1 power at the
   published magnitude between the 0.50 BLOCKED floor and the 0.80 GO floor,
   with observability passing in full. It was registered as DEGRADED. **That
   band is exactly where the measurement landed**, which is the argument for
   naming gaps before you are holding a number.
2. **Request caps are per source**, because a flow source at 200/day and a venue
   API at 5,000/day are different budgets and a single cap lets an archive sweep
   exhaust the flow snapshotter that is the actual experiment.
3. **The aggregate is absent when any one of the five funds is absent.** On a day
   the largest fund reports late, substituting zero fabricates the *sign* of the
   aggregate, which is the quantity the Section 4 rule trades on.

**The fifth guard**, specific to this repository, is the pre-period date pin: no
price or funding read stamped on or after 2025-05-01 outside the sealed writers.
Its boundary fixtures sit exactly on the instant — 2025-04-30T23:59:59.999Z
passes, 2025-05-01T00:00:00.000Z is refused.

---

## Stage A.1 Task 1 — access, and two findings larger than the access verdict

**2026-08-28, 19:57Z to 20:03Z. Terms recorded before the first repeated fetch.**

The `robots.txt` sweep across 8 hosts was the first network activity of this
repository, before any data surface was touched.

### The access verdict

| candidate | verdict |
|---|---|
| **Farside Investors** | **SELECTED, primary.** Keyless, server-rendered HTML, all five registered funds, **676 date rows** 2024-01-11 → 2026-08-28, **336 on or after 2025-05-01**, of which **333 print a value**. `robots.txt` is 33 bytes and names one agent (`Twitterbot`) with **no `User-agent: *` group**, so no directive applies. `/terms-of-use/` returns 404; the only legal page is a GDPR privacy notice silent on automated collection. |
| **SoSoValue** | **RETAINED, cross-check only.** A keyless `__NEXT_DATA__` payload of 756,748 bytes carries 660 daily rows. Its aggregate spans **all** US spot BTC ETFs rather than the registered five, differing by a mean of **47.42M USD** (median 27.20M, range −903.20M to +1,205.20M, n = 333) — large against the registered 100M threshold, so the two are **not interchangeable**. |
| **TheBlock** | **OUT.** `Disallow: /api/` under `User-agent: *`; the rendered page carries no server-rendered series and fetches from `/api/tbco`. **The endpoint was never requested.** |
| **Glassnode** | **OUT.** `Disallow: /api`; `api.glassnode.com/robots.txt` returns 401. Not keyless. **Never requested.** |

**The cross-check passes: 315 of 333 out-of-sample days agree within 2 percent
between two independently operated sources (n = 333).** The 18 that do not are
dominated by near-zero days where a relative test is unforgiving.

### Finding 1 — there is no documented publication time to record

The brief carried an "evening and night" publication convention. **It is not
documented where the data is served.** The words "evening" and "night" appear
**zero times** across both served pages (n = 2 pages searched). What the source
does document, verbatim:

> *"Note: The above table is generated automatically, in real time. Farside
> Investors is not liable for any errors or inaccuracies in the data."*

So there is nothing to label `documented` for the print time, and the standing
rule that the measured lag wins has no documented figure to win against.
**"Generated automatically, in real time" is the whole-file-regeneration
signature** the MLCryptoEngine H11 precedent named, which is why A.1 Task 4 is
first-class here.

### Finding 2 — the source synthesizes a zero, and the parser was already built for it

**The `Total` column prints `0.0` on a day where every per-fund cell is a dash:
3 of 3 such rows over n = 336.** Two were US market holidays; the third was the
open day at capture time.

The second is the dangerous one. **On the open day, every capture taken before
the print lands shows all dashes and a `Total` of `0.0`.** Consuming `Total`
would have recorded a printed zero for the open day on every such capture, and
the A.1 Task 3 lag measurement would have reported that **every day prints at
00:00 UTC** — a clean, precise, entirely fabricated answer to the question this
repository exists to ask.

The parser was registered at A.0, before the source was fetched, to compute the
signal from the five per-fund cells and never to read `Total`. This measurement
is what it was registered against.

### Finding 3 — the hourly candle window is rolling, and it is sliding away

`candleSnapshot` caps at **5,001 rows** (n = 17 bisection probes). At `1h` that
reaches back only to **2026-02-01T11:00:00Z** and **slides forward one hour per
hour** — 5,001 hours is 208.4 days, and the served start matches to the hour.
Probes at 730, 550, 400, 300, 250 and 225 days back returned **0 rows**.

Section 5's anchor-to-anchor-plus-24-hours return is not computable from `1d`
candles, whose boundaries are 00:00 UTC. **So roughly 190 of 333 out-of-sample
days already have no registered outcome, and the boundary consumes one more day
every day.** Recorded as ADR-013, and it is why the sealed collection ran before
Section 0 fired rather than after.

### The pre-period pin, demonstrated live

Two funding probes were chosen to straddle the boundary. The pre-period page
returned **72 readable rates and 0 gated**; the post-period page returned **0
readable and 72 of 72 gated**; a third page from 2025-05-01 gated **500 of 500**.
The guard works on production payloads, not only on fixtures.

### A defect found and fixed inside the task

**Pacing lived in the client instance and paced nothing across processes.** Each
script invocation built a fresh limiter with an empty map. **The collectors fire
as separate systemd invocations, so in production it would have paced nothing at
all.** It is now ledger-backed and takes the longer of the two waits (ADR-014).

---

## Stage A.1 Task 2 — rate ceilings, measured per endpoint

**No ceiling was found on any endpoint at or above this repository's own
absolute floor of 1.0 s: 96 probe requests across 6 endpoints, every one HTTP
200.**

| endpoint | highest verified-clean rate | operating spacing |
|---|---|---|
| `flow.table` | 12.17/min (n = 18) | 10.0 s |
| `archive.availability` | 59.92/min (n = 18) | 2.0 s |
| `archive.timemap` | 21.28/min (n = 18) | 2.0 s |
| `venue.candleSnapshot` | 59.90/min (n = 12) | 2.0 s |
| `venue.fundingHistory` | 59.91/min (n = 12) | 2.0 s |
| `kraken.ohlc` | 58.73/min (n = 18) | 2.0 s |

Paces are set at **twice the fastest verified-clean spacing** — half the highest
verified-clean *rate*, because there is no ceiling to halve. **`venue.meta` and
`archive.snapshot` were not measured and keep their slower pre-measurement
figures**; inheriting a sibling's is the inference solattn ADR-021 forbids.

**The figures are bounded by what was probed, not by what the server would
refuse**, and the record says so rather than implying a measured ceiling exists.
Probing below 1.0 s was declined: this project will never send faster than its
own floor, so a ceiling below it is not actionable and probing there is
aggression without information.

---

## Stage A.1 Task 3 — the publication lag: armed, and calendar-bound

**Armed 2026-08-28T20:17:11Z. The first capture recorded the open day as
`Absent(dash_in_cell)` — not yet printed — which is exactly the state that makes
the measurement meaningful.**

`etf-snap.timer` fires every 20 minutes with `Persistent=true`; the script
applies the registered cadence (20 minutes across the wrapping 20:00–14:00 UTC
print window, 2 hours otherwise) and records a skip as a skip. `etf-daily.timer`
fires at 12:20 UTC. No unit-name collision; the four pre-existing timers were
verified untouched — npl-watch (60 min), news-collect (22:31 UTC), solattn-daily
(00:40 UTC), npl-daily (01:40 UTC).

**No lag figure is quoted in this section.** The registration requires at least
**15 US trading days** of forward capture before any is, and one day exists.
**The 15th US trading day is 2026-09-21 and its print lands 2026-09-22.** An
absence is a recorded state.

---

## Stage A.1 Task 4 — as-printed observability: the measurement this repository turns on

### The retro leg, measured in full

**Archive capture density: 11 of 333 out-of-sample trading days = 0.0330,
against a registered 0.60 bar.** Short by a factor of 18.

**It fails on crawl rate, not on the registered window.** 48.37 percent of
out-of-sample mementos already fall inside the registered 20:00–08:00 UTC window
— roughly what a 12-hour window should catch — and the archive crawls the page
**0.316 times per calendar day**. Even an unbounded window admitting any capture
on D or D+1 reaches only **112 of 333 (33.63 percent)**. **Widening the window is
foreclosed as an explanation, and no widening is proposed.**

### The correction: my own figure, falsified by measurement

**Amendment 1 recorded this density as 37 of 333 (0.1111), from the timemap
alone.** The timemap answers *"was there a capture"*. Section 3 asks *"did a
capture strictly before the anchor serve a flow value"*. Fetching all 37:

| outcome of the pre-anchor archived capture | n |
|---|---|
| **served the day's value** | **11** |
| showed the day still dashed — not yet printed | **23** |
| carried no row for the day | 2 |
| fetch returned HTTP 403 (operational; admissibility unknown) | 1 |

**Measurement moved the figure by a factor of 3.4.** Amendment 1 stands
unedited, as the append-only rule requires, and Amendment 2 records it as
falsified. This is Section 14.7's own correction — the NPLExperiment lesson
about planning numbers entering registrations — **landing on this repository
rather than being quoted at it**. It landed in about six hours.

### The retro revision rate — the H11 hazard does not reproduce

On the 11 comparable days: **0 revised, 0 sign flips, 0 threshold crosses, 11 of
11 intact.** Every archived as-printed value matched the value the source serves
today, to the digit it prints.

**This is genuinely reassuring about the source, and it is below the registered
minimum sample of 30, so it carries no verdict.** It is not promoted to fill the
gap in Section 0 (see A.2 Task 5). The temptation to promote it is the
InsiderExperiment temptation exactly: a labelled non-verdict-bearing figure that
happens to point the convenient way.

### A retro estimate of the print window — corroborating, not registered

The 34 parseable archived captures separate cleanly, in hours past midnight UTC
on D+1 (the provisional anchor sits at +08:00):

- **served a value (n = 11): +04:05 to +08:00**;
- **still dashed (n = 23): −03:38 to +04:29.**

The ranges overlap only between +04:05 and +04:29, so **the print appears to
land between roughly 04:00 and 08:00 UTC on D+1**.

**The anchor has not moved and will not move on this.** Archived capture times
are censored by a crawl schedule this project did not choose. Section 3 permits
exactly one input to move the anchor, and it does not yet exist. The estimate is
recorded because it makes a prediction the forward measurement will confirm or
falsify — **and recording it now means the forward result cannot be read as
confirming whatever turns out to be convenient.**

### The forward leg

**Not measured. Calendar-bound. Earliest completion 2026-09-22.**

### The verdict

**PASS is closed** — the density leg cannot be restored, because the archive
captures that would be needed do not exist and cannot be created. **The verdict
is PARTIAL or FAIL, and which one turns on the forward leg alone.**

---

## Stage A.2 Tasks 1–3 — the census, the signal, and the substrate sealed before it slid

**Census: 336 rows, 11 admissible.**

| | n |
|---|---|
| **admissible** (all retro-archive; forward-capture 0) | **11** |
| excluded — capture too late | 53 |
| excluded — no capture | 243 |
| excluded — capture served no value | 25 |
| excluded — no printed value | 3 |
| **operational — archive fetch failed, admissibility unknown** | **1** |

The last row is separate on purpose. A failed fetch is an instrument fault, and
recording it as an exclusion would let it masquerade as a narrowed cohort —
which is what the six never-merging call states exist to prevent. Two census
defects surfaced building this: the `capture_too_late` test was **unbounded**
(reporting 296 against the true 53), and the failed fetch was being filed as an
exclusion. Both are recorded in Amendment 2 §5.

**The trading-day universe is the source's own date rows** (ADR-016), so the two
closed US market holidays in the window are excluded correctly without the code
ever being told what a holiday is.

**Signal distribution, outcome-blind.** Admissible as-printed (n = 11): median
86.8M USD, 5 long, 3 short, 3 flat, trade share 0.7273. Live descriptive
(n = 333, **not admissible**, labelled): median 27.4M, 138 long, 114 short, 81
flat, **trade share 0.7568** — the figure E2's power computation uses, with its
n and its label attached.

**The sealed substrate.** 5,002 hourly candle rows (2026-02-01T11:00Z onward)
and 11 funding pages covering 5,002 hours, sealed as raw bytes. **142 of 333
out-of-sample trading days are covered at the registered 0.95/0.95 bars.** The
span sealed per day is a **48-hour window from D+1 00:00Z**, wider than the
registered hold, so it stays valid under **any** anchor the amendment rule could
choose. Sealing wide is anchor-agnostic and is not a second look, because
nothing on the sealing path reads a value.

**Pre-period carve-out inputs**, strictly before 2025-05-01: daily log-return sd
**0.027431** (n = 475 returns, 2024-01-11 to 2025-04-30); mean hourly funding
**0.00002226** (n = 11,423 hours, 23 pages), a 24-hour hold sum of **0.000534**
and **19.5 percent per year**.

**One thing that reads oddly against every prior closure in this house record:
costs are not the binding term here.** A 9 bp round trip is **3.3 percent of one
daily standard deviation**. MLCryptoEngine H1 closed cost-bound by 23×. This
design fails, if it fails, on effect size and on sample — not on fees.

---

## Stage A.2 Task 4 — the power gate

**Minimum N clearing the registered 0.80 target for E1**, exact permutation
power by simulation at alpha_adj = 0.0253205655, one-sided:

| assumption | minimum N | Section 9's registered anchor | held? |
|---|---|---|---|
| published **0.18** | **237** | "near 250 admissible days" | **yes** |
| registered **0.09** | **845** | "high hundreds to low thousands" | **yes** |
| quartered 0.045 | 3,776 | — | — |

**Both registered anchors held.** They were recorded so a disagreement would be
visible rather than absorbed; there is none to record.

| cohort basis | N | E1 @ 0.18 | E1 @ 0.09 | E2 @ 0.18 | E2 @ 0.09 |
|---|---|---|---|---|---|
| achieved today | 11 | 0.0815 | 0.0500 | 0.0600 | 0.0375 |
| forward-only by 2026-12-31 | 88 | 0.3870 | 0.1155 | 0.3325 | 0.1075 |
| forward-only by 2027-03-31 | 152 | 0.6000 | 0.1910 | 0.5325 | 0.1650 |
| **all cohorts by 2027-03-31** | **163** | **0.6105** | **0.2015** | **0.5225** | 0.1700 |

Simulation budgets are stated rather than implied: E1 at 20,000 permutation
draws and 2,000 simulations; E2 at 1,500 draws and 400 simulations, whose
simulation error near a power of one half is about 0.025. Both registered floors
sit far from these values.

The engine is pinned by known answers before it is trusted: **its size under a
zero true effect sits at its nominal alpha**, and its simulated critical value
agrees with the known 1/√(n−1) asymptotic.

---

## Stage A.2 Task 5 — the Section 0 verdict, fired as far as the measured inputs determine it

**GO is eliminated, and closed.** GO requires as-printed observability to pass in
full; its density leg is 11 of 333 against a 0.60 bar, and **no later
measurement can restore it**, because the archive captures that would be needed
do not exist and cannot be created.

**BLOCKED does not fire on power.** Its trigger is E1 under 0.50 at the published
magnitude by 2027-03-31; measured **0.6105**.

**The remaining choice between DEGRADED and BLOCKED turns on exactly one
unmeasured input** — the forward revision-integrity leg — and that input is not
synthesized. **Earliest completion 2026-09-22.**

**The deadline finding, recorded as distinct from the verdict.** Section 10 opens
Stage B only at 80 percent power at *achieved* admissible N. Under DEGRADED that
assumption is the published magnitude, needing **N = 237**. At the measured
forward accrual rate, **achieved N = 237 arrives around 2027-07-26 — roughly four
months past the registered 2027-03-31 deadline**, against a projected 163 at the
deadline.

**Section 0's BLOCKED floor is a statement about power, and it is cleared. The
registered deadline is what is not met.** The design is not unpowered in
principle; it is unpowered **within the window this registration gave itself** —
the untestable-at-achievable-power shape named in HYPOTHESES.md, arriving through
the calendar rather than through the arithmetic. It is recorded now, before the
verdict completes, so it cannot later be presented as a discovery that happened
to excuse a disappointing result.

---

## Stage A.3 — what is armed, and what is deliberately not

**Armed.** The flow snapshotter and the daily pass, under A.1 Task 3's own
authority as the measurement instrument Section 0 depends on — without them the
missing input can never be measured, and A.1 Task 3 precedes A.2 Task 5 in the
registered stage order. The sealed price and funding recorder, under Amendment 1
§3(a), because the rolling window destroys one day of coverage per day.

**Not armed.** The A.3 Task 2 retro backfill: it runs **only on observability
PASS**, and PASS is closed. **The retro cohort — 8 trading days — is demoted to
descriptive and will carry no verdict.** No Stage B path: `verdict.py` is built
dark, refuses sealed paths in code, and is imported by nothing.

**The verdict machinery, dark.** E1, E2 and every named secondary, against
synthetic fixtures with known answers. **The canary fires on a planted signal
and neither primary fires on noise** — an engine that cannot detect a planted
effect proves nothing about a null.

---

## Stage A.4 — gates and mutations

`make lint`, `make typecheck` and `make test` are green: ruff clean, **mypy
strict clean across 76 files**, and the full suite passing. Every guard is
exercised, including the pre-period date pin.

**All six registered mutations were applied to real source, each caught, source
restored green, bytecode purged before every run:**

| mutation | caught | what it would have done |
|---|---|---|
| delete a blindness pin | ✅ | every post-2025-05-01 funding rate readable outside the carve-out |
| coerce an absence to zero | ✅ | a dash becomes a fabricated flat day; on the open day, every pre-print capture looks like a printed zero |
| merge `rate_limited` into `no_data` | ✅ | a source refusing a request becomes indistinguishable from one answering emptily |
| move the anchor boundary fixture onto the instant | ✅ | a capture at exactly the anchor becomes admissible |
| substitute a live value for a missing archived one | ✅ | a day with no qualifying capture admitted anyway, its value drawn from today's page |
| read a post-2025-05-01 price through the carve-out | ✅ | a window straddling the boundary serves test-sample closes to the power computation |

**Two of the six required fixing the harness rather than the source**, and both
failures were the harness failing to *find* its anchor text after `ruff format`
reflowed the line — the same class of defect InsiderExperiment recorded, where a
harness reported on source no longer on disk. The bytecode purge was ported from
that lesson and is in place from the first commit.

---

## Stage B — reserved

**Written once, and only after the latch.** Nothing may be added to this section
before the registered Stage B read of Section 10, which requires both
co-primaries at 80 percent power at achieved admissible N, the operator prior
slot filled and labelled, and explicit operator instruction.
