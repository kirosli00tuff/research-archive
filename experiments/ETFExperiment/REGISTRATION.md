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

## 13. Priors

**Assistant prior, recorded 2026-08-27 in chat, before any census:**

> **0.10** that a real capturable edge exists here — an effect that survives
> publication, decay, the after-the-close information timing, and a 9 bp round
> trip.

Nothing found in the repositories or on the web since has moved it. The figure
is recorded with its date so a future calibration ledger can score it.

**The adoption warning, standing.** The NPDExperiment Amendment 0 lesson
applies: **an adopted prior corrupts the calibration ledger**, because a number
copied from the assistant measures the assistant twice and the operator not at
all. The assistant's 0.10 above is context, not the operator's number, and it
**must not be copied into the slot below**.

**The operator prior slot, reserved and empty:**

> **Operator prior on the Stage B bars clearing:** _(empty — reserved for the
> operator)_

The accepted formats for the fill are a probability in `[0, 1]` followed by
`(independent)` or `(adopted)` — nothing else parses. **The empty slot blocks
Stage B structurally** (`etf.registration_check.require_operator_prior`,
exercised by `tests/test_registration_check.py`). It is the one open operator
item this stage is expected to leave behind.

## 14. Carried external figures — sources named, none measured by this repository

**Every figure in this section was supplied to the design and is labelled
`carried` wherever it is used. None was measured here.** Standing rule 3 says
measured beats documented; nothing in this section is a measurement of this
repository's, and no bar depends on one being true.

### 14.1 The source study

**Boon Chuan Lim, "The Price Impact of Spot Bitcoin ETF Flows", SSRN
abstract_id 6592830, posted 2026-04-17.** Five largest US spot BTC ETFs,
January 2024 through April 2025, **313 trading days**, Databento.

| reported figure | value |
|---|---|
| same-day impact, OLS | **53 bp per 100M USD** |
| same-day impact, instrumental variables | **74 bp per 100M USD**, first-stage F **21.58** |
| share of daily return variation explained by flows | **21 percent**, t **8.99** |
| **next-day prediction** | **Newey-West t 3.12** |
| bidirectional Granger causality | beta **0.47**, t **9.75** |
| unconditional reversal, horizons 1–20 days | **none** |
| conditional reversal (controlling for future flows) | t **−2.42 to −3.99** |
| total impact at 10 days | **96 bp per 100M USD**, t **4.49** |

**Only the next-day leg is testable by this design** (Section 1, structural
doubt 2). The same-day figures are carried for the Section 8 sanity check and
for nothing else.

### 14.2 The same author, later and longer — the single most important figure

**SSRN abstract_id 6567058**, **563 days** January 2024 through April 2026,
Farside data: **causal IV impact 0.20 percent per 100M USD at t 2.65**, against
the earlier **0.41 percent OLS**.

**The author's own estimate roughly halves on the extended sample.** This is
the figure the registered 0.09 assumption of Section 9 rests on, and it is the
single most important number carried into this registration.

### 14.3 The claimed external replication — recorded as FAILED TO CONFIRM

**Citi's note of 2026-07-01** cut its twelve-month BTC target to **82,000 USD**
and cut assumed twelve-month net ETF inflows to **zero**. Reporting shows
**Citi cited an external academic study rather than running its own
regression**, and the dataset description is Lim's.

**Citi's own quantified claim, from analyst Alex Saunders, is that flows
explain roughly 45 percent of weekly BTC moves.** That is **weekly and
contemporaneous**, not next-day and predictive.

**Recorded here as FAILED TO CONFIRM, not as corroboration.** A weekly
contemporaneous variance share is not an out-of-sample replication of a
next-day predictive coefficient, and treating a citation of the original study
as independent confirmation would double-count one measurement. Recorded as
ADR-012.

### 14.4 Contradicting evidence

- **HashKey senior researcher Tim Sun, August 2026:** single-day ETF flows
  alone yield **very limited predictive power for the next trading day**;
  long-term correlation coefficient **below 0.5**; roughly **0.4 percent per
  100M USD**; **a lagging trend-confirmation indicator rather than a leading
  one**.
- **CoinDesk, 2026-05-14, using SoSoValue data:** the **90-day rolling
  coefficient** between daily BTC return and the daily change in cumulative net
  inflows stands at **0.16, indistinguishable from zero**, down from a
  **February peak of 0.68**.

### 14.5 Regime

**June 2026 net outflows reached 4.06 billion USD**, the worst month since
launch in January 2024, inside a **13-day consecutive outflow streak totalling
roughly 4.4 billion USD**. The out-of-sample window this design tests contains
that regime. It is recorded, not adjusted for: conditioning the sample on a
regime after seeing it is the selection this registration exists to prevent.

### 14.6 In-house figures, from the repositories

| figure | value | source |
|---|---|---|
| Hyperliquid base perp fees | **1.5 bp maker / 4.5 bp taker per side** | in-house |
| Kraken Pro base tier | **0.25 percent maker / 0.40 percent taker** | MLCryptoEngine ADR-055, verified live 2026-08-08 |
| Coinbase base tier | **0.40 maker / 0.60 taker** | MLCryptoEngine ADR-055, not in dispute |
| IBKR fractional-order refusal | **error 10243** | HFExperiment `reports/stage_a1b/a1b_report.md` line 52 |

### 14.7 The correction that governs this repository

**In NPLExperiment a main-dex accrual figure near 9.4 events per month entered
a registration as a planning number, and measurement falsified it at 0.5 events
per month (n = 3 over 182 days), killing H3 on a figure rather than on the
world.**

**Therefore: no accrual, coverage, lag, retention, revision, or capture-density
figure in this repository is registered before it is measured.** Every such
figure is named as an A.1 or A.2 **measurement target**, never as an input:

| figure | measured at |
|---|---|
| publication lag distribution, p50 / p90 / p95 | **A.1 Task 3** |
| rate at which the largest fund reports late | **A.1 Task 3** |
| rate at which a dash appears where a number later stands | **A.1 Task 3** |
| days with no value before the provisional anchor | **A.1 Task 3** |
| forward revision rate, sign-flip rate, threshold-cross rate | **A.1 Task 4** |
| archive capture density per US trading day | **A.1 Task 4** |
| retro revision rate | **A.1 Task 4** |
| admissible days per month and the trailing rate | **A.2 Task 1** |
| signal distribution and the trade count | **A.2 Task 2** |
| sealed candle and funding coverage | **A.2 Task 3** |
| per-endpoint rate ceilings and operating paces | **A.1 Task 2** |

---

## Amendments

None yet. An amendment is dated, reasoned, states exactly what data existed
when it was made, and never edits anything above its own line.

### Amendment 1 — 2026-08-28 — the flow source is selected, the paces are measured, and two structural constraints are recorded

**What data existed when this amendment was made.** Stage A.1 access and
rate-ceiling telemetry, the archive timemaps, and one capture each of the flow
source's two pages: HTTP statuses, byte counts, capture timestamps, row counts,
flow values, and the request ledger (143 charged requests). **Flow values are
signal under standing rule 7 and are readable. No outcome value has been read:
no BTC price has been parsed by any code path in this repository, and every
funding rate stamped at or after 2025-05-01 that has passed through a reader
has been gated — measured live at 572 of 572 post-boundary rows across three
pages.** No census row existed, no admissibility had been computed, and no
power number existed.

#### 1. The flow source, selected

**Farside Investors is the primary flow source** (`CONFIG.flow_recent_url`,
`CONFIG.flow_all_data_url`). Keyless, server-rendered HTML, per-fund columns
covering all five registered tickers, **676 date rows from 2024-01-11 to
2026-08-28, of which 336 fall on or after 2025-05-01 and 333 carry a printed
value**. Its `robots.txt` (33 bytes, verbatim in docs/ACCESS.md §1) contains one
group naming `Twitterbot` and **no `User-agent: *` group**, so no directive
applies to this collector; `/terms-of-use/` returns 404 and the only legal page
is a GDPR privacy notice that says nothing about automated collection.

**SoSoValue is retained as a cross-check and is never the signal**: its
`totalNetInflow` spans all US spot BTC ETFs rather than the registered five,
and the two differ by **a mean of 47.42M USD (median 27.20M, range −903.20M to
+1,205.20M, n = 333)** — large against the registered 100M threshold. The
cross-check passes: **315 of 333 out-of-sample days agree within 2 percent**.

**TheBlock and Glassnode are routed out on stated prohibitions**
(`Disallow: /api/` and `Disallow: /api` under `User-agent: *`). **Their data
endpoints were never requested.** The HFExperiment Wealthsimple precedent
applies: a stated prohibition ends the enquiry.

#### 2. Section 12 pacing figures, recorded as measured

**No ceiling was found on any endpoint at or above this repository's own
absolute floor of 1.0 s: 96 probe requests across 6 endpoints, every one HTTP
200.** Operating paces are therefore set at **twice the fastest verified-clean
spacing**, the NPLExperiment pattern for an endpoint whose ceiling was not
found — half the highest verified-clean *rate*, because there is no ceiling to
halve. The figures are bounded by what was probed, not by what the server would
refuse, and that distinction is recorded rather than smoothed.

| endpoint | highest verified-clean rate | operating min spacing |
|---|---|---|
| `flow.table` | 12.17/min (n = 18) | **10.0 s** |
| `archive.availability` | 59.92/min (n = 18) | **2.0 s** |
| `archive.timemap` | 21.28/min (n = 18) | **2.0 s** |
| `venue.candleSnapshot` | 59.90/min (n = 12) | **2.0 s** |
| `venue.fundingHistory` | 59.91/min (n = 12) | **2.0 s** |
| `kraken.ohlc` | 58.73/min (n = 18) | **2.0 s** |
| `venue.meta`, `archive.snapshot` | **not measured** | keep the slower pre-measurement figure |

**Per endpoint, never per host** (solattn ADR-021): the two archive endpoints
share a host and were measured separately, as did the venue endpoints, and an
endpoint nobody measured **keeps its slower figure rather than inheriting a
sibling's** — that inheritance is the inference ADR-021 exists to forbid. The
per-source daily caps of Section 12 are unchanged; nothing measured asks them
to move.

#### 3. Two structural constraints, measured, that bind the retro cohort

Neither changes a registered bar. Both are recorded here because they decide
what the census can contain, and Section 14.7 requires such figures to be
measured before they are relied on.

**(a) The venue serves a rolling 5,001-candle window.** At `1h` that reaches
back only to **2026-02-01T11:00:00Z** and **slides forward one hour per hour**
(n = 17 bisection probes; 5,001 hours is 208.4 days and the served start
matches to the hour). Section 5's anchor-to-anchor-plus-24-hours return is not
computable from `1d` candles, whose boundaries are 00:00 UTC, so **a trading day
older than the rolling window has no registered outcome and is `underpowered` —
a recorded absence, never a return, and never a 1d substitute.**

**(b) Archive capture density is 37 of 333, and it fails on crawl rate rather
than on the registered window.** Measured across both flow pages' timemaps
(451 mementos, of which 153 fall on or after 2025-05-01): **admissible 37,
capture_too_late 53, no_capture 243, share 0.1111**, against the registered
0.60 bar. **48.37 percent of out-of-sample mementos already fall inside the
registered 20:00–08:00 UTC window, so the window is not the constraint**: the
archive crawls the page **0.316 times per calendar day**, and even an unbounded
window admitting any capture on D or D+1 would reach only **112 of 333
(33.63 percent)** — still short of the bar by a factor of 1.8. **Widening the
window is therefore foreclosed as an explanation, and no widening is proposed.**

**Their intersection is the retro cohort: 17 of 333 out-of-sample trading days
(5.11 percent) are both archive-admissible and inside the servable hourly
window.** That figure is recorded here, before any power computation, as the
ceiling on anything the retro cohort can ever contribute.

#### 4. What is unchanged

The hypothesis, the universe, the as-printed rule, the provisional 08:00 UTC
anchor and its single amendment rule, the position rule and its 100M threshold,
the outcome definition, the cost bands, the horizons, both co-primaries and
alpha_adj, the registered 0.09 effect assumption and its honest range, the
Stage B trigger, the epistemic boundary, the per-source caps, and the priors.
**The anchor has not moved and cannot move until the A.1 Task 3 measurement
exists.**

### Amendment 2 — 2026-08-28 — the Amendment 1 archive-density figure is falsified by measurement, and the retro revision rate is recorded

**What data existed when this amendment was made.** Everything in Amendment 1,
plus 37 archived captures of the flow source fetched from the Wayback Machine
(the pre-anchor capture for every archive-admissible out-of-sample day), the
sealed outcome substrate (5,002 hourly candle rows and 11 funding pages), the
pre-period carve-out inputs, the admissible-day census (336 rows), and one
forward flow capture taken at 2026-08-28T20:17:11Z. **Flow values are signal and
are readable. No outcome value has been read. The only price and funding values
this repository has parsed are the pre-period carve-out inputs, every one
stamped strictly before 2025-05-01 and gated by `etf.preperiod`.** No power
number existed when this amendment was written.

#### 1. The correction: 11 of 333, not 37 of 333

**Amendment 1 recorded an archive capture density of 37 of 333 (0.1111).** That
figure was computed from the timemap alone, and it counted **captures**, not
**served values**. Section 3 requires a capture that *serves a flow value for
that day*, and a capture showing a dash serves no value.

**Measured, by fetching all 37 archived captures:**

| outcome of the pre-anchor archived capture | n |
|---|---|
| **served the day's value** | **11** |
| showed the day still dashed — not yet printed at capture time | **23** |
| carried no row for the day at all | 2 |
| fetch returned HTTP 403 (operational, admissibility unknown) | 1 |
| **total archive-admissible days by the timemap** | **37** |

**The archive capture density is therefore 11 of 333 = 0.0330**, against the
registered 0.60 bar — short by a factor of 18. **Amendment 1's 0.1111 is
falsified and is recorded here as falsified rather than corrected in place**;
Amendment 1 stands unedited above, as the append-only rule requires.

This is Section 14.7's correction landing on this repository rather than being
quoted at it: **a figure that was not measured end-to-end entered a record, and
measurement moved it by a factor of 3.4.** The lesson generalises exactly as
NPLExperiment stated it — *the timemap answers "was there a capture", and only
fetching the capture answers "was there a value", and only the second question
is the registered one.*

#### 2. The retro cohort is 8 days

Intersecting the 11 days whose archived capture served a value with the days
inside the measured rolling hourly-candle window (2026-02-01 onward), **the
retro cohort is 8 trading days**: 2026-06-15, 2026-07-07, 2026-07-09,
2026-07-10, 2026-07-30, 2026-07-31, 2026-08-25, 2026-08-26.

**Eight days is not a cohort.** It is recorded here as the ceiling on anything
the retrospective leg can contribute to any verdict, before any power number
exists.

#### 3. The retro revision rate, measured — and the H11 hazard does not reproduce

On the 11 days where an as-printed archived value can be compared against the
value the source serves today:

| figure | value |
|---|---|
| days revised | **0 of 11** |
| sign flips | **0 of 11** |
| threshold crosses | **0 of 11** |
| intact | **11 of 11** |

**The MLCryptoEngine H11 whole-file-regeneration hazard does not reproduce on
this source at n = 11.** Every archived as-printed value matched the current
live value to the digit the source prints.

**This is below the registered minimum sample of 30** (Section 12 / A.1 Task 4),
and it is recorded as below it. **The retro revision leg does not meet its
registered minimum and cannot carry a verdict.** It is genuinely reassuring
about the source and it is not evidence at the registered strength.

#### 4. A retro estimate of the print window — corroborating, NOT the registered measurement

The 34 archived captures that parsed carry their own capture times, and they
separate cleanly. Expressed as hours past midnight UTC on day D+1 (the
provisional anchor sits at +08:00):

- **captures that served a value (n = 11): +04:05 to +08:00**, the earliest at
  **+04:05**;
- **captures that showed a dash (n = 23): −03:38 to +04:29**, the latest at
  **+04:29**.

The two ranges overlap only between +04:05 and +04:29. **The print appears to
land between roughly 04:00 and 08:00 UTC on D+1.**

**This is corroborating evidence and explicitly not the registered A.1 Task 3
measurement**, which requires this repository's own captures at the registered
20-minute cadence across at least 15 US trading days. These archived capture
times are censored by whenever the archive happened to crawl, which is a
schedule this project did not choose and cannot characterise. **The anchor has
not moved and will not move on this evidence.** Section 3 permits exactly one
input to move it — the measured 95th percentile first-print time — and that
measurement does not yet exist.

It is recorded because it makes a prediction the forward measurement will
either confirm or falsify, and recording it now means the forward result cannot
be read as confirming whatever was convenient.

#### 5. Two census defects found and fixed, recorded because both were silent

1. **The `capture_too_late` test was unbounded.** It asked whether *any*
   memento anywhere in the archive's history landed at or after the anchor,
   which is true for almost every day once one late capture exists. It reported
   296 days too-late against the true 53. Now bounded to the day following the
   anchor.
2. **A failed archive fetch was recorded as an exclusion.** One day returned
   HTTP 403, and it was being filed `excluded_ineligible` — an instrument fault
   masquerading as a narrowed cohort, which is precisely what the six
   never-merging call states exist to prevent. It is now `source_failed`, and
   its admissibility is recorded as **unknown** rather than as excluded.

#### 6. What is unchanged

Every registered bar, both co-primaries, alpha_adj, the effect assumptions, the
cost bands, the anchor and its single amendment rule, the Stage B trigger, the
priors, and the Section 0 map. **Nothing above this amendment line has been
edited.**

### Amendment 3 — 2026-08-28 — the Section 0 verdict record: GO is eliminated on measured inputs; the remaining choice awaits one measurement

**What data existed when this amendment was made.** Everything in Amendments 1
and 2, plus the admissible-day census (336 rows), the outcome-blind signal
distribution, the pre-period carve-out inputs, and the completed power
computation. **No outcome value has been read.** Every power figure below is a
simulation at a registered assumption; every empirical input to it is a count, a
timestamp, a flow value, or a pre-period figure stamped strictly before
2025-05-01.

#### 1. The power computation, and the registered sanity anchors held

**Minimum N clearing the registered 0.80 power target for E1**, exact
permutation power by simulation at alpha_adj = 0.0253205655, one-sided:

| assumption | minimum N | Section 9's registered anchor | held? |
|---|---|---|---|
| **published 0.18** | **237** | "near 250 admissible days" | **yes** |
| **registered 0.09** | **845** | "high hundreds to low thousands" | **yes** |
| quartered 0.045 | 3,776 | — | — |

**Both anchors registered in Section 9 held.** They were recorded so that a
disagreement would be visible as a disagreement rather than absorbed; there is
no disagreement to record.

**Power at the achievable admissible-day counts:**

| cohort basis | N | E1 @ 0.18 | E1 @ 0.09 | E1 @ 0.045 | E2 @ 0.18 | E2 @ 0.09 |
|---|---|---|---|---|---|---|
| achieved today | **11** | 0.0815 | 0.0500 | 0.0385 | 0.0600 | 0.0375 |
| forward-only by 2026-12-31 | 88 | 0.3870 | 0.1155 | 0.0495 | 0.3325 | 0.1075 |
| forward-only by 2027-03-31 | 152 | 0.6000 | 0.1910 | 0.0675 | 0.5325 | 0.1650 |
| **all cohorts by 2027-03-31** | **163** | **0.6105** | **0.2015** | 0.0860 | **0.5225** | 0.1700 |

Economic inputs, pre-period only: daily sd **0.027431** (n = 475 returns,
2024-01-11 to 2025-04-30); 24-hour funding sum **0.000534** from a mean hourly
rate of 0.00002226 (n = 11,423 hours); round trip **9 bp**; trade share
**0.7568** (n = 333). Simulation budget stated: E1 at 20,000 permutation draws
and 2,000 simulations; E2 at 1,500 draws and 400 simulations, whose simulation
error near a power of one half is about 0.025 — both registered floors sit far
from these values.

#### 2. The Section 0 verdict, fired as far as the measured inputs determine it

**GO is eliminated.** GO requires the as-printed observability test of A.1 Task 4
to pass **in full**. Its archive-capture-density leg is measured at **11 of 333 =
0.0330 against the registered 0.60 bar** (Amendment 2), short by a factor of 18.
**No subsequent measurement can restore it**, because the archive captures that
would be needed do not exist and cannot be created. **GO is closed.**

**BLOCKED does not fire on power.** Its power trigger is E1 under 0.50 at the
published-magnitude assumption at the achievable count by 2027-03-31. Measured:
**0.6105**. The trigger is not met.

**The remaining choice between DEGRADED and BLOCKED turns on exactly one
unmeasured input**: the forward revision-integrity leg of A.1 Task 4.

- If the forward revision rate leaves the signal's sign and threshold intact on
  **at least 90 percent** of days, as-printed observability fires **PARTIAL** —
  one leg holds, one does not — and **Section 0 fires DEGRADED**, demoting the
  retro cohort to descriptive and leaving the forward cohort to carry the verdict
  alone.
- If it does not, observability fires **FAIL** and **Section 0 fires BLOCKED**.

**That measurement does not exist and is not synthesized.** It requires this
repository's own captures at the registered 20-minute cadence across at least 15
US trading days (Section 12 / A.1 Task 3). The snapshotter was armed
2026-08-28T20:17Z. **The 15th US trading day is 2026-09-21 and its print lands
2026-09-22, which is the earliest date Section 0 can complete.**

**The retro revision figure is not promoted to fill the gap.** It measured 0
revisions, 0 sign flips and 0 threshold crosses on 11 comparable days — 11 of 11
intact, which would clear the 90 percent bar — **and n = 11 is below the
registered minimum sample of 30, which the registration set before any of it was
visible.** Promoting it would be the InsiderExperiment temptation exactly: a
labelled non-verdict-bearing figure that happens to point the convenient way.
**It is not promoted.**

#### 3. The verdict scope, stated now in the plain words Section 0 requires

**Under DEGRADED, a Stage B FAIL establishes that the effect is not present at
its published magnitude, and cannot distinguish a decayed effect from no effect
at all.** Recomputed power at the registered 0.09 assumption is **E1 0.2015 and
E2 0.1700** at the achievable count by 2027-03-31, against the registered 0.80
target.

#### 4. The deadline finding, recorded because it is not what the map measures

Section 10 opens Stage B only at **80 percent power at achieved admissible N**
under the assumption Section 0 fires on. Under DEGRADED that assumption is the
published magnitude, requiring **N = 237** for E1.

**At the measured forward accrual rate the achievable N by 2027-03-31 is 163.
Achieved N = 237 arrives around 2027-07-26 — roughly four months past the
registered deadline.**

**This is a distinct finding from the Section 0 verdict and it is recorded as
distinct.** Section 0's BLOCKED floor is a statement about *power*, and it is
cleared. The registered *deadline* is what is not met. The design is not
unpowered in principle; it is unpowered **within the window this registration
gave itself**, which is the untestable-at-achievable-power shape named in
HYPOTHESES.md, arriving through the calendar rather than through the arithmetic.

Recording it now, before the verdict completes, means it cannot later be
presented as a discovery that happened to excuse a disappointing result.

#### 5. Consequences, armed and not armed

- **Armed**, under A.1 Task 3's own authority as the measurement instrument
  Section 0 depends on: `etf-snap.timer` (20 minutes) and `etf-daily.timer`
  (12:20 UTC). Without them the missing input can never be measured, and A.1
  Task 3 precedes A.2 Task 5 in the registered stage order.
- **Armed**, under Amendment 1 §3(a): the sealed price and funding recorder,
  because the rolling 5,001-candle window destroys one day of coverage per day
  and has no archive.
- **Not armed**: the A.3 Task 2 retro backfill. It runs **only on as-printed
  observability PASS**, and PASS is closed. The retro cohort — 8 trading days —
  is **demoted to descriptive** and will carry no verdict.
- **Not armed**: any Stage B path. `verdict.py` is built dark against synthetic
  fixtures, refuses sealed paths in code, and is imported by nothing.

#### 6. What is unchanged

Every registered bar, both co-primaries, alpha_adj, the three effect
assumptions, the cost bands, the anchor and its single amendment rule, the
Stage B trigger, the epistemic boundary, and the priors. **The operator prior
slot remains empty and continues to block Stage B structurally.**
