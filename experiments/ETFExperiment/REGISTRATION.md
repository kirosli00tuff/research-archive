# REGISTRATION.md — the pre-registration

> **STATUS: SECTION 0 REGISTERED 2026-08-28, BEFORE ANY NETWORK CALL.**
>
> At the moment this document was first committed, **this repository had sent
> no request to any endpoint, held no flow value, no price, no funding row, and
> no census row of any kind.** The request ledger did not exist. That ordering
> is what makes this a pre-registration rather than a description.
>
> **From this point the specification is closed.** Where the specification and
> reality disagree, the session reports and stops rather than choosing.
> Changing anything here requires a **new dated amendment** appended at the
> bottom, with its reason and a statement of exactly what data existed at the
> time it was made. Nothing above an amendment line is ever edited.
>
> **Disclosure.** NPLExperiment (REGISTRATION.md, HYPOTHESES.md, progress.md),
> MLCryptoEngine (HYPOTHESES.md H11, report.md line 2734, DECISIONS.md
> ADR-055), solattn (DECISIONS.md ADR-019/021/022) and InsiderExperiment
> (progress.md) were read before this was written, and their measured figures
> are carried below with their sources. The external figures of Section 14 were
> supplied by the operator with their sources named and **none of them was
> measured by this repository**; each is labelled where it is used. No
> ETFExperiment data of any kind existed.

---

## 0. The outcome map — it judges collection feasibility and detectability, never returns

The Section 0 verdict fires in Stage A.2 Task 5 from the admissible-day census,
the power computation, and the Stage A.1 access, lag and observability
findings. **It reads no outcome value: every input is a count-derived power, a
measured share, or an operational verdict.**

- **GO:** **both** co-primaries of Section 8 reach **at least 80 percent power
  at alpha_adj** under the **registered effect assumption** of Section 9 (rank
  correlation 0.09), at the achievable admissible-day count by **2027-03-31**,
  **and** the as-printed observability test of A.1 Task 4 **passes in full**.
- **DEGRADED:** E1 reaches at least 80 percent power at the **published-
  magnitude** assumption (rank correlation 0.18) but under 80 percent at the
  registered assumption, **or** as-printed observability **passes partially**.
  Collection proceeds. Recomputed power is stated beside the registered target.

  **The verdict scope narrows, and the narrowing is stated here in plain words
  before any data exists: under DEGRADED a Stage B FAIL establishes that the
  effect is not present at its published magnitude, and cannot distinguish a
  decayed effect from no effect at all.**
- **BLOCKED:** E1 under **50 percent** power at the published-magnitude
  assumption at the achievable count by 2027-03-31, **or** as-printed
  observability **FAIL**, **or** a measured revision rate high enough that **no
  stable as-printed value exists before the entry anchor on a majority of
  days**. Nothing armed beyond the census.

**The residual band, registered rather than left as a gap.** The three clauses
above leave one case unnamed: E1 power at the published magnitude between the
0.50 BLOCKED floor and the 0.80 GO floor, with observability passing in full.
It is registered here as **DEGRADED** — it sits above the floor that stops
collection, so collection proceeds under the DEGRADED narrowing above. Naming
it now is cheaper than discovering the gap while holding a number.

**Precedence, fixed.** The three BLOCKED triggers are evaluated first and in
the order written; GO second; DEGRADED is the residual. A BLOCKED trigger fires
even at perfect power, because a design that cannot observe its own signal at
the anchor is not rescued by sample size.

Enforced by `etf.section0.fire_section0`, committed with this document and
pinned by `tests/test_section0.py`, with every boundary fixture sitting exactly
on the registered boundary: 0.80 and 0.50 on the power floors, 0.50 on the
majority share, and one-ULP steps across each. The observability verdict itself
is fired by `etf.observability.fire_observability`, pinned by
`tests/test_observability.py` with fixtures exactly on the 0.60 and 0.90 bars.

### Registered expectation, stated now so the verdict reads as a documented answer

**The Section 9 arithmetic and the decay evidence of Section 14 point to
DEGRADED.** The registered assumption is a rank correlation of 0.09; a
threshold-free permutation test needs several hundred admissible days to reach
80 percent power against it, and the achievable admissible-day count by
2027-03-31 is bounded by roughly 250 US trading days of out-of-sample history
plus forward accrual. The published-magnitude figure of 0.18 is reachable on
that sample; the registered half is likely not.

This is stated **before the census exists** so that the verdict, when it fires,
reads as a documented answer rather than a disappointment. **A DEGRADED here
narrows a question rather than abandoning it, and a BLOCKED is a documented
answer, not a failure of process.** InsiderExperiment closed BLOCKED before
measurement and that closure is the cheapest finding in the house record.

---

## 1. The hypothesis

**H-ETF.** A daily rule that takes a directional Hyperliquid BTC perp position
after a US spot Bitcoin ETF net flow print, **using only the value published
and timestamped before the entry anchor**, earns a **positive return net of
costs** over the out-of-sample period beginning 2025-05-01.

This is a **joint claim about the signal and about information timing**, and
the two structural doubts below are part of the hypothesis rather than caveats
attached to it. Either one alone can make the claim false while the underlying
economic relationship is real.

**Structural doubt 1 — publication timing.** The signal was **published openly
in April 2026** (Lim, SSRN 6592830, posted 2026-04-17; Section 14). A published
daily signal on the single most-watched instrument in the asset class is a
signal many desks can act on, and the author's own estimate **roughly halves on
a longer sample** (SSRN 6567058: causal IV impact 0.20 percent per 100M USD at
t 2.65 over 563 days, against 0.41 percent OLS on the shorter one). The
hypothesis is therefore not "does the published relationship exist" but
"does enough of it survive publication and decay to clear a round trip."

**Structural doubt 2 — information timing.** **The flow print lands after the
US close the return is measured against.** The same-day leg reported by the
source study — 53 bp per 100M USD, the headline figure — is therefore
**untradable by construction** on this design: the return it describes has
already happened when the number appears. **Only the next-day leg is testable
here**, and that leg is the weaker one in the source study (Newey-West t 3.12,
against t 8.99 on the contemporaneous variance share). Section 11 states the
epistemic boundary this creates: this design can never produce evidence about
the same-day relationship, in either direction.

## 2. Universe and event rule

**One instrument: the Hyperliquid BTC perpetual.** One event per US trading day
on which an admissible as-printed flow value exists under Section 3.

**Days are never filtered on any price or return quantity**, and no code path
outside the sealed writers can read one (CLAUDE.md blindness lists,
`tests/test_guards.py`). A day is admitted or excluded on flow fields,
timestamps and capture times alone.

**The flow universe is the five largest US spot Bitcoin ETFs by assets, named
here explicitly by ticker so the universe cannot drift with an AUM table:**

| ticker | fund |
|---|---|
| **IBIT** | iShares Bitcoin Trust |
| **FBTC** | Fidelity Wise Origin Bitcoin Fund |
| **GBTC** | Grayscale Bitcoin Trust |
| **ARKB** | ARK 21Shares Bitcoin ETF |
| **BITB** | Bitwise Bitcoin ETF |

Registered in `CONFIG.flow_universe_tickers` and read through
`etf.signal.registered_universe`. **The aggregate net flow across these five is
the signal**; per-fund values are retained in every capture as descriptive and
are never verdict-bearing. The five match the source study's stated universe
(Section 14). If a source serves a sixth fund's column, the column is captured
and stored — captures are whole-table — and excluded from the aggregate.

## 3. The print, the anchor, and admissibility

**This is the section the repository turns on.**

### 3.1 The as-printed value

**The as-printed value for US trading day D is the aggregate net flow for D as
served by the flow source in a capture strictly before the entry anchor. The
value taken is the one in that capture.** A later value for the same day,
however authoritative, **is never substituted**, and where the two differ the
day is **flagged `revised`** and the difference recorded in USD and as a share
of the printed value.

This is the rule the MLCryptoEngine H11 precedent demands. That source
regenerated its whole file and revised past rows; a design that reads today's
value for a past day silently tests a number nobody could have traded.

**An absent cell is never a zero.** A dash where a number will later stand is
`Absent(dash_in_cell)`, which refuses coercion to a float
(`etf.absence`, `etf.flow.parse_cell`). **One absent fund makes the whole
aggregate absent** (`etf.flow.aggregate`): substituting zero for a fund that
reported late fabricates the sign of the aggregate, which is exactly the
quantity Section 4 trades on.

### 3.2 The entry anchor, and the one rule that may move it

**The entry anchor is registered provisionally at 08:00 UTC on day D+1**
(`CONFIG.entry_anchor_hour_utc`, `etf.anchor.entry_anchor`).

**A.1 Task 3 measures the distribution of first-print times.** If the measured
**95th percentile first-print time falls later than 07:00 UTC**, the anchor
moves to **the next whole hour after that percentile**, recorded by amendment
**before any outcome read and before any admissibility count is final**.

**No other input moves the anchor.** Not a power computation, not an
admissibility count, not a convenience. The rule is a pure function of one
measured percentile (`etf.anchor.amended_anchor_hour`), the percentile is
nearest-rank and deterministic, and the tests sit exactly on the trigger: a
measured p95 of exactly 07:00 UTC leaves the anchor at 08:00, and a p95 of
exactly 09:00 moves it to 10:00.

### 3.3 Admissibility

- A **retro day** (D on or after 2025-05-01, before forward collection began)
  is admissible **only if an archive capture strictly before the entry anchor
  serves a flow value for that day**.
- A **forward day** is admissible **only if this repository's own timestamped
  capture strictly before the entry anchor serves one**.
- **Strictly before**, and the boundary fixture sits exactly on it: a capture
  at 07:59:59Z on D+1 qualifies; one at 08:00:00Z does not
  (`etf.anchor.is_admissible_capture`).
- Days failing this are **`excluded_ineligible` and counted, never imputed**
  (`etf.callstate`). The exclusion reason is recorded and split at minimum into
  `no_capture` and `capture_too_late`.

## 4. Signal and position

**The signal is the admissible as-printed aggregate net flow in USD.**

**The primary position rule is symmetric:**

- **long** one unit of BTC perp when the signal **exceeds +T**,
- **short** one unit when it **falls below −T**,
- **flat** otherwise,

entered at the anchor and exited at **the same clock time 24 hours later**.
**T is registered at 100 million USD**, matching the source study's unit
(`CONFIG.signal_threshold_usd`, `etf.signal.position`). Strictly greater and
strictly less: a signal of exactly +100,000,000 USD is **flat**, and the test
fixture sits exactly there.

**Named Stage-scope simplifications**, each stated rather than discovered:
constant notional; no compounding; no leverage beyond one; no liquidation
modelling. None of them is a claim about how a position would actually behave.

**The long-only variant** of the handover sketch (long on +T, flat otherwise)
is a **named secondary, never verdict-bearing** (Section 8).

## 5. Outcome definition

**Net return for a day** equals:

    net(D) = position(D) × price_return(anchor → anchor + 24h)
             + position(D) × Σ hourly funding accruing over that window
             − registered round-trip cost (Section 6)

- **Sign convention, stated explicitly: a positive funding rate pays the
  short.** The venue's hourly `fundingRate` is the rate longs pay shorts, so a
  short receives `+rate` per hour on notional and a long pays it. The signed
  sum enters with the position's sign.
- **Funding over the hold is measured, never assumed** (Section 6).
- Constant notional: the funding leg accrues on the entry notional, not on the
  marked position.
- A day whose sealed candle or funding coverage falls under the Section 12 bars
  reports **`underpowered`**, never a return (A.2 Task 3).

## 6. Costs

| venue | central round trip | band (low, central, high) | role |
|---|---|---|---|
| **Hyperliquid BTC perp** | **9 bp** | 3, 9, 18 | **verdict-bearing** |
| Kraken spot | 50 bp maker / 80 bp taker | — | descriptive, reported beside |
| IBKR | **none** | **none** | closed; no band exists |

**Basis, carried:** Hyperliquid base perp fees **1.5 bp maker and 4.5 bp taker
per side** (in-house figure, Section 14), so 9 bp is taker both legs, 3 bp is
maker both legs, and 18 bp is a stress bound.

**The 3 bp end is an upper-bound-of-optimism and is never the central case,
because a daily signal must fill.** A rule that must be in the market at a
fixed clock time cannot assume both legs rest passively; reporting the maker
round trip as the headline would be quoting a fill this design cannot promise.

**Kraken Pro base tier 0.25 percent maker and 0.40 percent taker per side**
(MLCryptoEngine ADR-055, verified live 2026-08-08) gives a 50 bp maker and
80 bp taker round trip. It is **reported beside every economic figure to show
the venue dependence** and is **descriptive only** — it moves no bar. Under the
ADR-055 pattern this is a **dated measurement, not a constant**, and it is
re-verified before any verdict-bearing use with the correction recorded.

**IBKR carries no band because error 10243 closes it.** The API refuses
fractional-sized orders (HFExperiment `reports/stage_a1b/a1b_report.md` line
52), so no equity-side implementation exists and a band would imply one
(`etf.costs.ibkr_band` returns `None`, pinned by test).

## 7. Horizons

- **One day: primary.** The hold is anchor to anchor + 24 hours.
- **The reversal profile at 1 through 20 days: a named secondary.**
- **No horizon other than one day is verdict-bearing.** The source study's
  10-day total-impact figure and its 1–20 day reversal profile are interesting
  and are computed as secondaries; neither can move the Stage B row.

## 8. Inference

**Two co-primaries, distribution-free, one-sided, at
`alpha_adj = 1 − 0.95^(1/2) = 0.0253205655` each. Both must pass for the
Stage B GO row.**

### E1 — directional

**Exact permutation test on the rank (Spearman) correlation between the
admissible as-printed signal for day D and the next-day return, over all
admissible days, no threshold, one-sided positive.** The null is the
permutation distribution of the signal against the return series.

**The threshold-free form is registered deliberately: it uses every admissible
day and is the highest-powered distribution-free test available on this
sample.** A thresholded test discards every day inside the band, which on a
100M USD threshold is a large fraction of them.

### E2 — economic

**Mean net return per trade under the Section 4 rule at T = 100 million USD;
exact one-sided lower bound above zero at alpha_adj by permutation**, at the
**9 bp central cost band with measured funding**, and **reported at 3 and 18 bp
beside**. The permutation is over the signed position labels against the
realised net returns.

### Named secondaries — descriptive, never verdict-bearing

1. The **same-day coefficient**, as a sanity check against the published 53 bp
   per 100M USD. **It is a sanity check and nothing more**: Section 11 forbids
   reading it as evidence about the same-day relationship, because the print
   lands after the close and the design cannot test tradability there.
2. The **reversal profile at 1 through 20 days**.
3. **Threshold sensitivity** over the grid **0, 50, 100, 200 million USD**,
   with **Sidak correction inside the secondary** (four cells).
4. The **out-of-sample halves split**, to expose decay within the test window.
5. The **long-only variant**.
6. The **revised-day subset compared against the unrevised subset**.

**A statistic not named here is a second look and is refused at Stage B.**

### Deliberate departure from the handover sketch, with its reason

The handover proposed a **distribution-free sign test** as the directional
primary. **Exact binomial power on roughly 330 days does not reach 80 percent
at that test even under the undecayed published effect**, so registering it
would register a bar the sample cannot reach — the InsiderExperiment failure
mode, where the design's own arithmetic blocks it. **The permutation test on
rank correlation replaces it.** Recorded as ADR-003.

## 9. Power method and the registered effect assumption

**Exact permutation power by simulation at the registered assumptions,
computed in A.2 Task 4 from the measured admissible-day count. No number is
invented before the census.**

### The registered primary assumption

**The registered primary assumption is half the published next-day effect: a
rank correlation of 0.09.**

The published next-day leg reports **Newey-West t 3.12 over 313 days**, which
implies a rank correlation near **0.18** (t ≈ ρ√(n−2)/√(1−ρ²) gives
ρ ≈ 0.176 at n = 313).

**The rationale is registered with it and is not discretionary:**

- the author's own extended-sample IV estimate falls from **0.41 to 0.20
  percent per 100M USD**, roughly half, on 563 days against 313;
- the independent 90-day rolling correlation between daily BTC return and the
  daily change in cumulative net inflows fell from a **February 2026 peak of
  0.68 to 0.16** by 2026-05-14, inside the test window.

**Registering at the undecayed figure would register an assumption the
pre-existing evidence already contradicts.**

### The honest range

**Powers at the undecayed 0.18 and at a quartered 0.045 are computed and
reported beside the registered 0.09** — the NPLExperiment H3 pattern, where a
single assumption would have hidden how much the verdict turned on it.
**Minimum-N statements for each co-primary at each of the three assumptions.**

### The pre-period carve-out on the E2 inputs

**Volatility and funding inputs to the E2 power computation come from the
pre-period carve-out only: strictly before 2025-05-01.** That window sits
inside the source study's own sample and outside this test sample, so reading
it cannot leak an observation the Stage B verdict is computed on. The
enforcement site is `etf.preperiod` and the pin is
`tests/test_preperiod.py` with fixtures exactly on the boundary; three
structural guards in `tests/test_guards.py` hold it there. **Every other price
and funding read is sealed.**

### Rough anchors for sanity — the computation is authoritative

Order-of-magnitude expectations, recorded now so a computation that disagrees
is visible as a disagreement rather than absorbed:

- **E1 near 250 admissible days at the undecayed 0.18 assumption**;
- **E1 in the high hundreds to low thousands at the registered 0.09.**

**If the computation disagrees with these anchors, the computation wins and the
disagreement is recorded** in the report and in progress.md. These are
expectations, not registered figures; the NPLExperiment correction that governs
this repository is precisely that a planning number must never become a
registered one.

## 10. Stage B trigger

Stage B runs only when **all** of:

1. **both co-primaries at or above 80 percent power at achieved admissible N**
   (not projected) under **the assumption Section 0 fired on**;
2. the **operator prior slot of Section 13 filled and labelled** `independent`
   or `adopted`;
3. **explicit operator instruction.**

**Stage B opens the sealed outcomes exactly once, behind a latch written
first**, recording the sha256 of every module on the read surface. A crash
after the latch spends the read; recovery works from partial artifacts under an
amendment, never a silent re-run.

**Every value inside the read is quarantined from any successor code path by
AST pin and by test.** `verdict.py` is built dark in A.3 against synthetic
fixtures and is never pointed at real sealed data before that single registered
read.

## 11. The epistemic boundary

A positive result supports the claim that **the registered rule would have
cleared its bars on this sample**. It is **never a forward return prediction**,
never an expected-value claim about future flows, and never a trading
recommendation. Stage A produces no tradeable artifact at all.

**It is also never evidence about the same-day relationship.** The print lands
after the US close the same-day return is measured against, so this design
cannot test whether that relationship is tradable — in either direction. A
strong same-day secondary coefficient would confirm the source study's
measurement and would say nothing whatsoever about whether it can be captured.

## 12. Spend and pacing

**Zero dollars. Keyless public sources only.** No API key, token or credential
exists anywhere in this project, and `.env.example` is empty on purpose.

**A request ledger charges before sending and refuses past a daily cap**
(`etf.ledger.requests`). **Caps are per source**, because a flow source and a
venue API are different budgets and one exhausting the other is exactly the
failure a single shared cap invites. Provisional caps registered at A.0:
`flow` 200/day, `archive` 2,000/day, `venue` 5,000/day. **Each is set per
source from the A.1 Task 2 measurement and recorded by amendment if it moves.**

**Pacing is measured per endpoint and never generalised across endpoints**
(`etf.pacing`; the solattn ADR-021 lesson, where two endpoints on one host held
6.0 s and 12.0 s and the project's own earlier measurement of the first was
exactly the kind of "documentation" the measured-beats-documented rule warns
about). An endpoint with no registered pace is **refused, not defaulted fast**.

**Pacing respects the recorded terms of service.** `robots.txt` and the
published terms of every source are recorded verbatim in `docs/ACCESS.md`
before the first automated fetch. **If automated collection is disallowed, that
is recorded loudly and the access verdict is routed accordingly; this
repository does not proceed against a stated prohibition.** The HFExperiment
Wealthsimple finding is the precedent.

**Sealed coverage bars (A.2 Task 3):** `MIN_OUTCOME_COVERAGE` **0.95** for
candles and **0.95** for funding hours over the hold windows. An under-covered
day reports `underpowered`, never a return.
