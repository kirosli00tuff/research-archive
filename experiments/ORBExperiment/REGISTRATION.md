# REGISTRATION.md — the pre-registration

> **STATUS: SECTION 0 REGISTERED 2026-08-29, BEFORE ANY VENDOR DATA REQUEST.**
>
> At the moment this document was first committed, **this repository held no
> bar, no price, no volume, no session census, no ticker list and no request
> ledger of any kind.** No vendor had been asked for data. That ordering is
> what makes this a pre-registration rather than a description.
>
> **From this point the specification is closed.** Where the specification and
> reality disagree, the session reports and stops rather than choosing.
> Changing anything here requires a **new dated amendment** appended at the
> bottom, with its reason and a statement of exactly what data existed at the
> time it was made. **Nothing above an amendment line is ever edited.**
>
> **Disclosure, one: three network calls preceded this document.** At
> approximately 2026-08-29T01:52Z, before `progress.md` existed, three GET
> requests were sent to establish whether outbound network access existed at
> all: `api.polygon.io/v1/marketstatus/now` (**401**),
> `stooq.com/q/d/l/?s=aapl.us&i=d` (**200**) and an Alpha Vantage
> `TIME_SERIES_INTRADAY` demo query (**200**), n = 3. **Every response body was
> discarded unread to `/dev/null`.** What was observed is three integers and
> three elapsed times, all inside the readable field list below. **This breaches
> the literal ordering clause of the operator prompt's TASK 4 and TASK 5 and is
> recorded here rather than argued away.** It is `progress.md` Entry 0a and
> `DECISIONS.md` ADR-001. No bar value was seen; no figure in this registration
> derives from it.
>
> **Disclosure, two: the prior art.** ETFExperiment (`CLAUDE.md`,
> `REGISTRATION.md`, `DECISIONS.md` ADR-001), NPLExperiment (`REGISTRATION.md`,
> `HYPOTHESES.md`, `progress.md`, `docs/STAGES.md`), MLCryptoEngine
> (`HYPOTHESES.md` H11, `DECISIONS.md` ADR-055), solattn (`DECISIONS.md`
> ADR-019, ADR-021) and InsiderExperiment (`progress.md`) were read before this
> was written, for patterns rather than text. Their measured figures are
> carried below with their sources named.
>
> **Disclosure, three: every external figure in Section 14 is carried, and
> none of them was measured by this repository.** Each is labelled **carried**
> where it is used. **No coverage, revision, agreement, delisting, trigger-rate
> or slippage figure is registered here as an input.** Every one is named as an
> A.1 or A.2 **measurement target**. This is the NPLExperiment correction: a
> main-dex accrual figure near 9.4 events per month entered a registration as a
> planning number and measurement falsified it at **0.5, n = 3 over 182 days**,
> killing H3 on a figure rather than on the world.

---

## 0. The outcome map — it judges collection feasibility, source integrity and detectability, never returns

The Section 0 verdict fires at **Stage A.2 TASK 5** from the power computation
of A.2 TASK 4, the bar-revision measurement of A.1 TASK 3, and the cross-vendor
agreement and delisted-coverage measurements of A.1 TASK 4. **It reads no
outcome value: every input is a count-derived power, a measured share, a
measured count, or an operational verdict.**

- **GO:** **both** co-primaries of Section 8 reach **at least 80 percent power
  at alpha_adj** under the **registered effect assumption** of Section 9
  (annualized net Sharpe 1.40) at the achievable session count, **and** the
  bar-integrity verdict of A.1 TASK 3 and A.1 TASK 4 **passes in full**, **and**
  delisted-name coverage **passes**.

- **DEGRADED:** E1 reaches at least 80 percent power at the **published-
  magnitude** assumption (annualized net Sharpe 2.81) but under 80 percent at
  the registered assumption, **or** bar integrity **passes partially**, **or**
  delisted coverage is **present but thin**. Collection proceeds.

  **The verdict scope narrows, and the narrowing is stated here in plain words
  before any data exists: under DEGRADED a later FAIL establishes that the
  effect is not present at its published magnitude, and cannot distinguish a
  decayed effect from no effect at all.**

- **BLOCKED:** E1 under **50 percent** power at the published-magnitude
  assumption, **or** bar integrity **FAIL**, **or zero delisted names served
  across the window**, **or** a measured cross-vendor disagreement rate high
  enough that the top-20 selection is not reproducible. Nothing is armed beyond
  the documentation stage.

### The residual band, registered rather than left as a gap

The clauses above leave one case unnamed: **E1 power at the published magnitude
strictly between the 0.50 BLOCKED floor and the 0.80 GO floor, with bar
integrity passing in full.** It is registered here as **DEGRADED** — it sits
above the floor that stops collection, so collection proceeds under the
DEGRADED narrowing above. Naming it now is cheaper than discovering the gap
while holding a number. Pinned by
`tests/test_section0.py::test_the_registered_residual_band_is_degraded_not_a_gap`.

### Precedence, fixed

The five BLOCKED triggers are evaluated **first and in the order written**; GO
second; **DEGRADED is the residual**. A BLOCKED trigger fires **even at perfect
power**, because a design that cannot trust its own bars is not rescued by
sample size. Pinned by
`tests/test_section0.py::test_precedence_is_fixed_blocked_before_go`.

| clause | trigger | threshold |
|---|---|---|
| BLOCKED-1 | E1 power at the published magnitude | `< 0.50` |
| BLOCKED-2 | bar revision rate | `> 0.020` |
| BLOCKED-3 | delisted names served with intraday history | `== 0` |
| BLOCKED-4 | cross-vendor first-5-minute high-or-low agreement | `< 0.85` |
| BLOCKED-5 | delisted names served with intraday history | `< 20` |
| GO | both co-primaries at the registered assumption **and** both integrity verdicts PASS | `>= 0.80`, PASS, PASS |
| DEGRADED | everything else | residual |

### The component verdicts, with their boundaries stated inclusively

**Bar revision, A.1 TASK 3.** `PASS` at a changed-bar share **at or below
0.005**; `PARTIAL` **above 0.005 and at or below 0.020**, recorded as a
registered scope limitation carried into every downstream figure; `FAIL`
**above 0.020**, which fires BLOCKED.

**Cross-vendor agreement, A.1 TASK 4.** `PASS` at a first-5-minute
high-or-low agreement share **at or above 0.95** of session-ticker pairs;
`PARTIAL` **at or above 0.85 and below 0.95**, demoting selection
reproducibility to a recorded scope limitation; `FAIL` **below 0.85**.

**Delisted coverage, A.1 TASK 4.** `PASS` at **100 or more** delisted names
served with intraday history; `PARTIAL` at **20 to 99**; `FAIL` **below 20**.

**The combined A.1 TASK 4 verdict is the worst of the two**, because perfect
cross-vendor agreement does not offset a survivor-only universe: a universe
missing its delisted names inflates every downstream figure and is
unrecoverable after the fact.

### Enforcement

Fired by `orb.section0.fire_section0`, committed with this document and pinned
by `tests/test_section0.py`, **with every boundary fixture sitting exactly on
the registered boundary** and stepping one ULP or one count across it: 0.005
and 0.020 on the revision bars, 0.95 and 0.85 on the agreement bars, 100 and 20
on the delisted counts, and 0.80 and 0.50 on the power floors. The component
verdicts are fired by `orb.integrity.RevisionFinding.verdict` and
`orb.integrity.AgreementFinding.verdict`. A totality test walks the full
4 × 4 × 6 × 6 input lattice, **n = 576 combinations**, and requires that every
one fires exactly one registered verdict and that all three verdicts are
reachable.

### Registered expectation, stated now so the verdict reads as a documented answer

**The Section 9 arithmetic and the decay evidence of Section 14 point to
DEGRADED.** The registered assumption is an annualized net Sharpe of 1.40,
which is a daily Sharpe of `1.40 / sqrt(252) = 0.0882`. The holdout window
2023-01-03 to 2026-06-30 holds roughly 880 sessions, giving
`0.0882 * sqrt(880) = 2.62` — above 2.0 and **below the 3.0 that Harvey, Liu
and Zhu argue a new claim should clear**. The deflated-Sharpe bar of E1 carries
a registered trial count of 8, and the holdout alone does not clear a
factor-zoo hurdle at the discounted effect size.

This is stated **before any measurement exists** so that the verdict, when it
fires, reads as a documented answer rather than a disappointment. **A DEGRADED
here narrows a question rather than abandoning it, and a BLOCKED is a documented
answer, not a failure of process.** InsiderExperiment closed BLOCKED before
measurement and that closure is the cheapest finding in the house record.

**And the honest converse, registered with it:** if bar integrity FAILs, this
repository fires BLOCKED and stops, and that is the **correct and cheap**
outcome. The Concretum finding — identical opening-range code against four
vendors with identical dates, parameters and starting capital producing final
portfolio values from **226,000 to 726,000 USD**, a threefold spread from
vendor choice alone (**carried**, Section 14) — is the reason bar integrity is
a first-class verdict here rather than a footnote.

---

## 1. The hypothesis

**H-ORB.** Among US common stocks with **elevated opening relative volume**, a
**breakout of the first 5-minute regular-session range** predicts continuation
to the session close, **net of modeled commissions, fees, borrow and
slippage**, out of sample from **2023-01-03**.

This is a **joint claim about the selection and about the breakout**, and it can
fail on either half while the other half is real. The three structural doubts
below are **part of the hypothesis rather than caveats attached to it**.

**Structural doubt 1 — publication.** The signal was published openly in 2024
(SSRN 4729284, Swiss Finance Institute 24-98) and has been popularized
commercially since. McLean and Pontiff (*Journal of Finance* 71, pages 5–32)
measured published predictor returns falling **26 percent out of sample and 58
percent after publication across 97 predictors from 80 studies** (**carried**).
A published intraday rule on the most-watched names of the session is a rule
many desks can act on. The hypothesis is therefore not "does the published
relationship exist" but **"does enough of it survive publication and decay to
clear a realistic cost model."**

**Structural doubt 2 — cost.** The independent replication of the sibling index
strategy measured a **gross edge of 0.070 USD per share** and found **net PnL
crossing zero at roughly 0.022 USD per share of entry slippage, against a QQQ
spread near 0.010 USD** (**carried**, Section 14). **The entire gross edge of
the index version measured smaller than a realistic slippage assumption.** This
registration's central entry-slippage assumption is 0.020 USD per share, which
sits **just under** that measured break-even. **The cost band is not a
robustness check in this design. It is the experiment's second axis, and
Section 6 says so.**

**Structural doubt 3 — regime.** In the same replication, **76 percent of the
filtered strategy's PnL came from 2022 alone**, and the filter **lost money in
2017, 2020 and early 2023** (**carried**). A 2026 arXiv falsification study on
MNQ micro futures found ORB long, short and pullback variants **all failing
after 2-point friction**, best long variant at **t = 1.50**, with 2022
negative, 2023 near zero and 2024 strongly positive — **the same one-good-year
signature** (**carried**). Section 8 therefore registers a **concentration
gate** as a first-class pass-fail condition rather than as a diagnostic.

**The source result this repository tests is a single, unreplicated, in-sample
result produced by authors who sell day-trading education.** That sentence is
registered here because it is a fact about the evidence, and because a reader of
a later positive verdict needs to meet it before the verdict rather than after.

---

## 2. Universe and event rule

**Instruments.** US **common stocks**. **No ETFs** — the index-ETF variant is
excluded by ADR-013 on the replication figures that forced it.

**Evaluation instant.** **09:35:00 America/New_York**, each regular session.
That is 13:35 UTC under daylight time and 14:35 UTC under standard time; the
anchor is resolved through `orb.sessionclock`, never through a fixed offset.

**Opening relative volume.** First-5-minute share volume divided by the
**trailing 14-session median** first-5-minute share volume for that name.

**Selection.** Rank descending on opening relative volume; **take the top 20**.
Ties are broken by ticker symbol ascending, so the selection is deterministic
and reproducible without reference to any price.

**Filters, all evaluated on the session in question or its trailing window:**

| filter | threshold |
|---|---|
| session open | **above 5.00 USD** |
| 14-session average volume | **above 1,000,000 shares** |
| 14-session ATR | **above 0.50 USD** |

**Short-side exclusion.** A name with **no locate**, or a **borrow rate above
25 percent annualized**, is excluded on the short side and **counted**. Where a
borrow rate is not served, the name is excluded on the short side and counted —
**never assumed cheap**.

**Delisted tickers are included for every historical session in which they
traded.** A survivor-only universe inflates every downstream figure and is
unrecoverable after the fact. This is why delisted coverage is a **BLOCKED
trigger** in Section 0 and not a diagnostic.

**Sessions are never filtered on any return quantity.**

**Half sessions are excluded and counted.** The count is a reported figure with
its n.

---

## 3. The signal, the entry and the exit

**This is the section the repository turns on.**

**Opening range.** The high and the low of **09:30:00.000 to 09:34:59.999
Eastern**, inclusive of both endpoints of that half-open five minutes.

**Entry.** The **first trade through the range high goes long**; the **first
trade through the range low goes short**. Modeled as a **marketable limit at
the range boundary plus 0.05 percent of price** (5 basis points), in the
direction of the break.

- **One entry per name per session.**
- **No re-entry after a stop.**
- **If both sides trigger inside the same bar, the session is recorded
  `ambiguous` and excluded**, and **the ambiguous rate is a measured figure**
  reported with its n. It is not assumed to be small.

**Stop.** The **opposite extreme of the opening range**, held as a resting stop.

**Exit.** The **session close**, modeled in the window **15:55:00 to 15:59:00
Eastern**, with **no profit target**. On a half session the window shifts by
three hours; half sessions are excluded from the sample regardless and the
shift exists so that the excluded rows are still well-formed.

**Two registered departures from the source study, each with an ADR.**

1. **The entry rule is a true breakout, not the source study's immediate
   first-candle directional entry** (ADR-002). The source study's rule enters at
   09:35 on the first candle's direction and **does not require a later break of
   the range**, so it is **early-momentum with an opening-range stop rather than
   a breakout**. Registering the paper's rule under the paper's name would carry
   the paper's label onto a different claim. Section 11 states what this costs
   in evidential scope.
2. **The 10R profit target is removed** (ADR-003). It fills on **2 to 3 percent
   of trades** (**carried**) and is a **mined parameter**: a target that binds
   on one trade in forty is fitted to the tail of the sample it was chosen on.

---

## 4. Sizing

- **Equal risk, 0.25 percent of equity per trade**, where risk is the
  **entry-to-stop distance**.
- **Integer share counts only.** IBKR refuses fractional-sized orders through
  the API with **error 10243**, measured by HFExperiment
  (`reports/stage_a1b/a1b_report.md` line 52, **carried**). This is registered
  **as a design constraint** rather than discovered at execution (ADR-010).
- **Maximum 20 concurrent positions.**
- **Gross notional capped at 1.0x equity. No leverage.**
- **No compounding. Constant equity base.**

Each of the last three is named as a **Stage-scope simplification**: they make
the daily net return series a clean sum over a fixed base, which is what the E1
statistic is defined on. None is a claim about how capital would be deployed.

---

## 5. Outcome definition

**Net PnL per trade** equals the **signed price difference from the modeled
entry fill to the modeled exit fill**, times **shares**, minus **commissions**,
minus **regulatory fees**, minus **borrow accrued on short positions**, with
**slippage applied at the registered per-leg figures of Section 6**.

**Sign convention, stated explicitly.** For a **long**, net PnL is
`(exit_fill − entry_fill) × shares − costs`. For a **short**, net PnL is
`(entry_fill − exit_fill) × shares − costs`. **A positive number is a gain in
both directions.** Costs are always subtracted and are always positive.

**The portfolio daily net return** is the **sum of that session's trade net PnL
over the constant equity base**. Sessions with no triggered trade contribute a
return of exactly zero and **are retained in the series**, because dropping them
would silently condition the series on the trigger rate.

---

## 6. Costs and the modeled fill

**Implemented exactly as stated here, then frozen and hashed at A.2 TASK 2.**
Every figure below is **carried** and **must be re-verified live before the
model freezes**, under standing rule 4 and the MLCryptoEngine ADR-055 pattern.

| component | registered figure | status |
|---|---|---|
| commission | **0.0035 USD per share**, **0.35 USD order minimum** | carried, IBKR Canada tiered |
| FINRA TAF | **0.000166 USD per share sold** | carried |
| SEC fee | **the rate in force on the session date**, recorded per date | carried, **never a single constant** |
| FX conversion | **~0.2 bp above interbank, 2.00 USD per order minimum** | carried, IBKR |

**Slippage, registered as three-point bands. The central figure is the
registered case; the optimistic end is reported as an upper bound of optimism
and never as the central case.**

| leg | optimistic | **central** | pessimistic |
|---|---|---|---|
| entry | 0.010 | **0.020** | 0.040 |
| stop exit | 0.020 | **0.040** | 0.080 |
| close exit | 0.005 | **0.010** | 0.020 |

All in USD per share. **The stop band is widest because a stop is marketable
and gap-prone**; a stop is not a limit and does not get the limit's price.

**Borrow** accrues **daily at the measured rate where served**. Where a rate is
**not served, the name is excluded on the short side and counted** — **never
assumed cheap**.

**Why this band is the whole experiment.** The independent replication measured
the sibling index strategy's **net PnL crossing zero at roughly 0.022 USD per
share of entry slippage** (**carried**, Section 14). **The registered central
entry assumption of 0.020 USD per share sits 0.002 USD below that measured
break-even.** A design whose central cost assumption sits two-tenths of a cent
inside its own break-even is not a design with a robustness question attached;
**the cost band is a second axis of the verdict and is reported as one.**

---

## 7. Horizons and windows

| window | dates | sessions, approximate |
|---|---|---|
| **pre-period carve-out** | strictly before **2016-01-04T14:30:00.000Z** | power inputs only |
| **in-sample** | **2016-01-04** to **2022-12-30** | ~1,760 |
| **holdout** | **2023-01-03** to **2026-06-30** | ~880 |

**The holdout window is pinned.** Both endpoints are fixed here, before any
session census exists, so that neither can be moved by what the census turns out
to hold.

**Session-close exit only. No overnight horizon is verdict-bearing.**

---

## 8. Inference

**Two co-primaries, one-sided, and both must pass.**

`alpha_adj = 1 − 0.95^(1/2) = 0.02532057...`, applied to **each**.

### E1 — risk-adjusted

**Deflated Sharpe ratio** of the **daily net portfolio return series** over the
holdout, computed by the **Bailey and López de Prado** method (SSRN 2460551,
**carried**), with:

- **trial count registered at 8**, being **four opening-range lengths (5, 15, 30
  and 60 minutes) crossed with two entry rules (immediate-direction and
  true-breakout)**;
- **skewness and kurtosis taken from the realized series**, not assumed.

**Bar: deflated Sharpe at or above 1.00.**

### E2 — economic

**Mean net PnL per trade**, one-sided **lower bound above zero at alpha_adj**,
by **permutation on session labels with trades clustered by session date**, so
that **a single strong session cannot masquerade as many independent
observations**.

### The two structural gates, registered as pass-fail and not as tests

Applied alongside the co-primaries. **Neither carries alpha; both must pass.**

1. **Concentration gate.** **No single holdout calendar year contributes more
   than 50 percent of holdout net PnL.** This exists because **76 percent of the
   replication's filtered profit came from 2022 alone** (**carried**). ADR-006.
2. **Persistence gate.** **Holdout net PnL is positive in at least 3 of the 4
   holdout calendar years** (2023, 2024, 2025, and 2026 through 06-30).

### Named secondaries — descriptive, never verdict-bearing

The 15, 30 and 60-minute range lengths; the immediate-direction entry; the
long-only and short-only legs separately; the top-10 and top-40 selection
widths; performance conditioned on the **VIX close against its trailing
252-session median**; the **ambiguous-trigger subset**; and the **gap-size
decile profile**. **None of these moves a verdict row**, and the registered
trial count of 8 already prices the range-length and entry-rule crossings into
E1's deflation.

---

## 9. Power method and the registered effect assumption

### The registered assumption

**Annualized net Sharpe 1.40 — half the published 2.81.** The rationale is
registered with it and **is not discretionary**:

1. McLean and Pontiff measured a **58 percent post-publication decay across 97
   predictors** (**carried**);
2. the source result is **unreplicated** and **commercially motivated**;
3. the **one independent replication of the sibling index strategy found the
   edge inside the spread** (**carried**).

### The arithmetic, to be reproduced in code at A.2 TASK 4 and not taken from this document

| quantity | value |
|---|---|
| daily Sharpe | `1.40 / sqrt(252)` = **0.0882** |
| t over n sessions | `0.0882 × sqrt(n)` |
| sessions to clear t = 2.0 | **514**, roughly **2.04 years** |
| sessions to clear t = 3.0 | **1,157**, roughly **4.59 years** |
| in-sample sessions | ~**1,760** — powered for t = 3.0 |
| holdout sessions | ~**880** → **t = 2.62** |

**A.2 TASK 4 recomputes every one of these in code, and where the computation
disagrees with the figures in this table, the computation wins and the
disagreement is recorded as an amendment.**

### The shortfall, registered openly rather than discovered at the read

**The holdout yields t = 2.62 at the registered assumption, which is below the
3.0 that Harvey, Liu and Zhu argue a new claim should clear** (**carried**).
This is registered now, as **ADR-005**, rather than met at the read.

**The holdout gate is therefore set at a per-trade t of 2.50**, with the
**deflated-Sharpe bar of E1 carrying the multiple-testing correction**. And the
registration states in plain words: **the holdout alone cannot clear a
factor-zoo hurdle at the discounted effect size.** A holdout pass is evidence
that the rule cleared its registered bars on this sample under this cost model
from this vendor. It is not evidence that the effect would clear a t of 3.0.

### The honest range, reported beside — the NPLExperiment H3 pattern

Powers are computed and reported at **all three** assumptions:

| assumption | annualized Sharpe | status |
|---|---|---|
| undecayed / published | **2.81** | the source study's own figure |
| **registered** | **1.40** | half, per the decay evidence |
| quartered | **0.70** | the pessimistic end |

**Minimum-N statements for each co-primary at each of the three assumptions**
are computed and recorded.

### Per-trade power, computed and reported as non-binding

At 20 names per session and **a trigger rate that is a measurement target and
never an assumption**, the holdout carries thousands of trades, and clearing
t = 3.0 needs a per-trade information ratio near **0.031**. **The portfolio-day
series is the binding constraint and this registration says so**: the trades
inside a session are not independent, they share the session's market factor,
and E2's permutation clusters on session date precisely because of that.

### Dispersion inputs

**Dispersion inputs to the E2 power computation come from the pre-period
carve-out only, strictly before 2016-01-04T14:30:00.000Z.** Enforced by
`orb.preperiod.require_pre_period` and `orb.preperiod.gate_pre_period`.

---

## 10. The Stage C latch

**Stage C opens the sealed in-sample read exactly once.** It requires **all** of:

1. **Both co-primaries at or above 80 percent power at achievable N**, under
   **the assumption Section 0 fired on**;
2. **the operator prior slot of Section 13 filled and labelled `independent` or
   `adopted`** — the assistant never fills it, and **the empty slot blocks the
   latch structurally**;
3. **explicit operator instruction.**

The read happens **behind a latch written first, recording module hashes**.
**Stage D opens the holdout exactly once, behind its own latch**, and cannot run
before Stage C's latch exists.

**A second read of either window voids the hypothesis.**

**Every value inside a read is quarantined from any successor code path by AST
pin and by test.** A spent read is a spent read; a successor hypothesis runs on
fresh data or it does not run.

---

## 11. Epistemic boundary

A positive verdict supports **exactly one** claim: **that the registered rule
would have cleared its registered bars on this sample, under this cost model,
from this vendor.**

- **It is never a forward return prediction.**
- **It is never evidence about any range length or entry rule other than the
  registered one.** The 15, 30 and 60-minute lengths and the immediate-direction
  entry are named secondaries and are already priced into E1's trial count of 8.
- **It is never evidence that the source study's reported figures are correct**,
  **because the entry rule registered here differs from theirs by design**
  (ADR-002). A pass here does not replicate SSRN 4729284, and a failure here does
  not refute it.
- **It is never evidence about index ETFs.** That variant is excluded by ADR-013.
- **Under a DEGRADED Section 0, a later FAIL establishes that the effect is not
  present at its published magnitude, and cannot distinguish a decayed effect
  from no effect at all.**

---

## 12. Spend and pacing

**Zero dollars in Stage A. Free and trial tiers only.**

- A **request ledger with a per-vendor daily cap** set from the **A.1 TASK 2
  measurement**, recorded by amendment if it moves. The cap **charges before
  sending** (`orb.ledger.RequestLedger.charge`), so an exhausted budget refuses
  rather than overspends. **An unregistered vendor has no cap and is refused
  outright** — an unmeasured endpoint is not a licence to send.
- **Pacing respects the recorded terms of service**, and is **measured per
  endpoint, never per host** (solattn ADR-021: one endpoint refused **47.5
  percent of n = 1,863 attempts** while a second endpoint on the same host and
  the same IP took **0 of 360**).
- **Terms of service bind.** `robots.txt` and the published terms are recorded
  verbatim for every vendor **before the first repeated fetch**. If automated
  collection is disallowed, it is recorded loudly and the access verdict is
  routed accordingly. **This repository does not proceed against a stated
  prohibition.**
- **Any paid tier requires an explicit operator instruction and its own ADR.**
  The expected monthly figures are named here as **carried, not measured**:
  **Polygon Starter near 29 USD per month**; **Databento consumption-based near
  125 USD per month for a medium universe.**

---

## 13. Priors

**Assistant prior, recorded 2026-08-28 in chat, before any measurement:**

> **0.15** on a real capturable edge surviving the registered cost model out of
> sample.

**Nothing in the repositories read at TASK 0, and nothing on the web, has moved
it.** It is recorded here with its date so that a later verdict can be scored
against a number that existed before the evidence did.

**Operator prior slot: EMPTY. Reserved. To be filled only by the operator.**

```
operator_prior          = <EMPTY>
operator_prior_label    = <EMPTY: "independent" | "adopted">
operator_prior_recorded = <EMPTY: date>
```

**The empty slot blocks the Stage C latch structurally** (Section 10, clause 2).
This is not a formality and it is not a reminder. It is a gate.

**Why the assistant must not fill it, stated with the precedent.** The
NPDExperiment **Amendment 0** lesson: **an adopted prior corrupts the
calibration ledger.** A prior the operator adopted from the assistant is not an
independent observation of the operator's belief; recording it as one makes the
ledger's calibration statistics measure the assistant twice and the operator
never. If the operator's number happens to equal 0.15, it is still recorded as
**`independent`** only if it was reached without reading the line above, and as
**`adopted`** otherwise. **The label is part of the datum.**

**Do not fill this slot.**

---

## 14. The amendment log

**Rules, in force from this line.**

1. **Append-only.** An amendment is added at the bottom. **Nothing above an
   amendment line is ever edited**, including to fix an error — an error is
   corrected by a new amendment that names it.
2. **Dated.**
3. **Reasoned.**
4. **Stating exactly what data existed when the amendment was made.** An
   amendment written while holding a measurement is a different object from one
   written before it, and the log records which.

**Figures carried into this registration, sources named, none measured by this
repository.** Every one is labelled **carried** where it is used.

| # | figure | source |
|---|---|---|
| C-1 | QQQ/TQQQ 5-min ORB, 10R target, 4x cap, 0.0005 USD/share commission, **explicitly zero slippage**; QQQ **1,484 percent** against **169 percent** buy-and-hold, annualized alpha near **33 percent**, Jan 2016 – Feb 2023 | Zarattini and Aziz, SSRN 4416622 |
| C-2 | >7,000 US stocks, 2016–2023, delisted included; plain broad-universe 5-min ORB **3.2 percent annually at 6.6 percent vol, Sharpe 0.48**, below passive | Zarattini, Barbon and Aziz, SSRN 4729284, SFI 24-98 |
| C-3 | Top-20 by opening relative volume: **>1,600 percent net, Sharpe 2.81, annualized alpha 36 percent**, against **198 percent** for the S&P 500 over the same window; 15-minute variant **272 percent at Sharpe 1.43** | SSRN 4729284 |
| C-4 | Filters: open above 5 USD, 14-day average volume above 1,000,000 shares, 14-day ATR above 0.50 USD | SSRN 4729284 |
| C-5 | Independent replication: **1,775 trades against the paper's 1,795**, gross Sharpe **1.06** | giovannibrusco/zarattini-2023-orb-qqq |
| C-6 | **Gross edge 0.070 USD per share; net PnL crosses zero at ~0.022 USD per share of entry slippage, against a QQQ spread near 0.010 USD** | same |
| C-7 | 09:25 NQ futures agreement filter: per-trade edge **0.125 USD/share at t 2.05**; strategy Sharpe **0.77** against buy-and-hold **0.72**, **overlapping bootstrap intervals 0.05–1.41 against −0.03–1.47** | same |
| C-8 | **76 percent of filtered PnL from 2022 alone**; the filter **lost money in 2017, 2020 and early 2023** | same |
| C-9 | MNQ micro futures falsification: ORB long, short and pullback **all fail after 2-point friction**, best long **t 1.50**; 2022 negative, 2023 near zero, 2024 strongly positive | 2026 arXiv falsification study |
| C-10 | A new claim should clear **t near 3.0** rather than 2.0 | Harvey, Liu and Zhu |
| C-11 | Deflated Sharpe: deflate for trial count plus skewness and kurtosis | Bailey and López de Prado, SSRN 2460551 |
| C-12 | Published predictor returns fall **26 percent out of sample and 58 percent after publication**, **97 predictors, 80 studies** | McLean and Pontiff, *JF* 71, 5–32 |
| C-13 | **Threefold spread in final equity — 226,000 to 726,000 USD — from four vendors on identical opening-range code, dates, parameters and starting capital** | Concretum Research |
| C-14 | IBKR Canada tiered US stock commission **0.0035 USD/share, 0.35 USD order minimum**, plus pass-through exchange, SEC and FINRA fees | IBKR |
| C-15 | FINRA trading activity fee near **0.000166 USD per share sold** | FINRA |
| C-16 | IBKR FX conversion near **0.2 bp above interbank, 2.00 USD per order minimum** | IBKR |
| C-17 | **IBKR refuses fractional-sized orders through the API, error 10243** | HFExperiment `reports/stage_a1b/a1b_report.md` line 52 |
| C-18 | Polygon Starter near **29 USD per month**; Databento consumption-based near **125 USD per month** for a medium universe | vendor pricing pages |
| C-19 | MLCryptoEngine H11: **measured 75-day publication lag** in a free flow source with whole-file regeneration revising past rows; lag **discovered rather than registered** | MLCryptoEngine `HYPOTHESES.md` H11 |
| C-20 | NPLExperiment: a planning figure near **9.4 events per month** falsified at **0.5, n = 3 over 182 days** | NPLExperiment `progress.md` |
| C-21 | solattn ADR-021: **47.5 percent refusals over n = 1,863 attempts** on one endpoint while a second endpoint on the same host and IP took **0 of 360** | solattn `DECISIONS.md` ADR-021 |

**C-14, C-15, C-16 and C-17 are broker figures and are re-verified live at A.2
TASK 2 before the cost model freezes**, under standing rule 4 and the ADR-055
pattern. **Measured is recorded against carried, in the same sentence, with its
date. Any deviation is written as an amendment before A.2 TASK 4, never
silently absorbed.**

### Amendments

---

## Amendment 1 — the PENDING_ACCESS state, registered 2026-08-29

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 0**

**Exactly what data existed when this amendment was made: none.** At the moment
of writing, this repository held **zero bars, zero prices, zero volumes, zero
sessions and zero census rows**. **No vendor had served a single bar to it.**
`n = 7` API probes had been sent and **`n = 0`** had returned data. That
ordering is what makes this amendment un-fittable to a result: there is no
result.

**What was measured, and it falsified a planning assumption.** A.1 TASK 1
measured, live, that **0 of 9 vendors serve 1-minute regular-session US equity
bars to this repository** (`docs/ACCESS.md`). The two vendors that serve
keylessly — `stooq.com` and `query1.finance.yahoo.com` — **both publish
`User-agent: * / Disallow: /`**, and standing rule 12 forbids proceeding against
a stated prohibition. `eodhd.com` disallows `/api/` and `data.nasdaq.com`
disallows `/api/*.json*`, which are the exact paths a collector needs. **The
five vendors whose terms permit collection all refused without a credential**,
refusal payloads recorded verbatim. The operator prompt's assumption that
**"no key is needed for any Stage A source"** is therefore **falsified by
measurement**, and is recorded as falsified rather than worked around.

**The gap this opens in Section 0.** As registered, Section 0 fires from a
revision finding and an agreement finding. Both are now **recorded absences**:
`Absent(not_yet_measured)`. The map as written has no state for *"the
measurement does not exist"*, and the nearest states are wrong in opposite
directions — GO would pretend, and BLOCKED would close H1 as
`source-integrity-blocked` **on evidence that does not exist**. Standing rule 5
governs: **absence is a recorded state, never a synthesized value.**

**The amendment.** A fourth Section 0 state, **`PENDING_ACCESS`**, is
registered, and its clause is evaluated **ahead of every BLOCKED trigger**:

> **PENDING_ACCESS:** either integrity input is `Absent`. **Nothing is armed.**
> It is **a verdict on this repository's access, not a verdict on H1**, and it
> is explicitly **not** a `source-integrity-blocked` closure — no bar has been
> served that could fail.

**It is not a bypass and is pinned as not being one.**
`tests/test_section0.py::test_pending_access_is_not_reachable_when_both_inputs_are_present`
walks the present-input space and requires that the clause is **inert** the
moment both measurements exist. The GO, DEGRADED and BLOCKED clauses are
**unchanged in text, threshold and precedence**.

**What clears it.** Two free-tier credentials from two different vendors, one
primary and one secondary. **This is an operator action** — it requires creating
accounts, which this repository does not do on the operator's behalf. It is
recorded as an open operator item beside the Section 13 prior slot, and it is
the only other one.

---

## Amendment 2 — pacing registered provisionally, and labelled unmeasured

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 12**

**Exactly what data existed when this amendment was made:** the A.1 TASK 2
escalation, `n = 18` requests across 3 endpoint-spacing cells, **all of them
against unauthenticated paths**, and **zero bars**.

**What was measured.** No endpoint returned HTTP 429. Polygon's
`/v3/reference/tickers` admitted **8 of 8 requests at a sustained 88.4 per
minute** with 401 on every one; Alpha Vantage's `TIME_SERIES_INTRADAY` demo
admitted **5 of 5 at 29.1 per minute** with 200-carrying-a-refusal on every one.

**Why that measurement does not license a pace, and the corollary that says so.**
solattn ADR-021 established that **a measurement of one endpoint is not evidence
about another, even on the same host** — 47.5 percent refusals over `n = 1,863`
attempts on one endpoint while a second on the same host and IP took **0 of
360** (carried, C-21). **The corollary applies to this repository's own
measurement**: the only reachable path on every permitted vendor is the
*unauthenticated refusal* path, and **a ceiling measured on a 401 is not
evidence about the authenticated data endpoint.** The absence of 429s at 88 per
minute is evidence that **the refusal path is not metered by the data-tier
limiter**, and nothing more. Polygon's documented free tier is **5 requests per
minute** (documented, never measured); the measured 88 per minute on a 401 path
does **not** contradict it, because they are different endpoints.

**The amendment.** Per-vendor daily caps and per-endpoint spacings are
registered **provisionally** and **labelled unmeasured**, at deliberately
conservative values: `DEFAULT_MIN_SPACING_S = 6.0` seconds for any endpoint
nobody has measured, and daily caps set per vendor in the request ledger. **They
are re-measured against the authenticated data endpoints, per endpoint, at the
first task that holds a credential, and moved by a further dated amendment if
the measurement disagrees.** An unmeasured endpoint keeps its vendor's figure
rather than a faster default: **an unmeasured endpoint is not a licence to speed
up.**

---

## Amendment 3 — the cost model, re-verified live; one carried figure stale and three components missing

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 6**

**Exactly what data existed when this amendment was made:** the session
calendar of A.2 TASK 1, the A.1 access findings, and the live fee pages fetched
below. **Zero bars, zero prices, zero volumes, zero trades and zero returns.**
No PnL figure of any kind existed, so nothing here can have been chosen for the
effect it would have on one.

**This amendment is written before A.2 TASK 4**, as Section 6 and standing rule
4 require: a deviation is written as an amendment, **never silently absorbed**.

### What was re-verified, and where

Terms first, per standing rule 12. `www.interactivebrokers.com/robots.txt`
(**200**, 265 B) disallows only `/smf/`, `/fluxbb/`, `/search/`, `/referral/`
and one insights path — **the pricing page is permitted**.
`www.finra.org/robots.txt` (**200**, 9,068 B) carries **no bare `Disallow: /`**.
**`www.sec.gov/robots.txt` returned HTTP 403 "Request Rate Threshold
Exceeded"** — an anti-bot rate limit, not a robots file — on **both** attempts,
20 s apart. **That is recorded as a state, not read as permission and not read
as prohibition.**

Source: `https://www.interactivebrokers.com/en/pricing/commissions-stocks.php`,
**HTTP 200, 584,282 bytes, retrieved 2026-08-29**, stored at
`data/access/fees/ibkr_stocks.html`.

### Measured against carried, in the same sentence, with its date

| component | carried (C-14/C-15) | **measured 2026-08-29** | verdict |
|---|---:|---:|---|
| IBKR Pro Tiered, ≤ 300,000 shares/month | 0.0035 USD/share | **0.0035 USD/share** | **agrees** |
| IBKR minimum per order | 0.35 USD | **0.35 USD** | **agrees** |
| FINRA Trading Activity Fee, per share sold | 0.000166 USD | **0.000195 USD** | **CARRIED FIGURE IS STALE — 14.9 percent low** |
| SEC transaction fee | "the rate in force on the session date" | **0.0000206 × value of aggregate sales** | measured; **effective date NOT measured** |
| IBKR maximum per order | **not modeled** | **1 percent of trade value** | **NOT PREVIOUSLY MODELED** |
| FINRA Consolidated Audit Trail | **not modeled** | **0.000003 USD × quantity** | **NOT PREVIOUSLY MODELED** |
| NSCC / DTC clearing pass-through | **not modeled** | **0.00020 USD per share** | **NOT PREVIOUSLY MODELED** |

Verbatim, as served: *"SEC Transaction Fee: USD 0.0000206 * Value of Aggregate
Sales. FINRA Trading Activity Fee: USD 0.000195 * Quantity Sold. FINRA
Consolidated Audit Trail Fees: USD 0.000003 * Quantity"* and *"NSCC, DTC Fees:
USD 0.00020 per share"*, alongside *"Minimum per order (shares) USD 0.35"* and
*"Maximum per order 1% of Trade Value"*.

### The amendment, in four parts

1. **The FINRA TAF rate moves from 0.000166 to 0.000195 USD per share sold.**
   The carried figure is stale. **This is the ADR-055 pattern firing exactly as
   designed** — a fee schedule is a dated measurement, and re-verification is
   the reason it was re-verified.
2. **Three previously unmodeled components are added**: the **1 percent
   maximum per order**, the **FINRA CAT fee at 0.000003 per share on every
   leg**, and the **NSCC/DTC clearing pass-through at 0.00020 per share on
   every leg**. All three make the model **more expensive**, never less.
3. **The 1 percent cap can bind below the 0.35 minimum**, and the minimum does
   not survive it. Pinned: 10 shares at 1.00 USD is a 10.00 USD trade whose 1
   percent cap is **0.10**, below the 0.35 floor, and the cap wins.
4. **The SEC fee schedule is registered EMPTY.** One rate was measured; **its
   effective date was not**, and `sec.gov` refused twice. Placing the measured
   2026 rate in the schedule would silently apply it to a 2016 session.
   `SecFeeSchedule.rate_on` therefore returns `Absent` for **every session in
   the registered window**, and the whole round-trip cost refuses rather than
   under-charging. **The model will not price a trade it cannot price
   honestly.** Pinned by
   `test_the_registered_model_refuses_every_session_in_the_window`.

### What this costs the hypothesis, stated now

Per round trip per share, at the registered central band, the newly-measured
components add **0.000606 USD** (clearing 0.00040 + CAT 0.000006 + the TAF
correction 0.000029 + rounding), before the SEC fee. Against the replication's
measured **gross edge of 0.070 USD per share** (carried, C-6) that is small.
**It is not small against the margin.** A full round trip at the central band on
a 50 USD name costs roughly:

| component | USD per share |
|---|---:|
| commission, both legs | 0.00700 |
| slippage, entry + close exit | **0.03000** |
| SEC fee on the sale | ~0.00103 |
| clearing, both legs | 0.00040 |
| FINRA TAF | 0.000195 |
| FINRA CAT, both legs | 0.000006 |
| **total, close exit** | **≈ 0.03863** |
| **total, stop exit** | **≈ 0.06863** |

Against a gross edge of **0.070 USD per share**, a close exit consumes **55
percent** of it and **a stop exit consumes 98 percent**. **Slippage is 78
percent of the close-exit total.** This is Section 6's claim — that the cost
band is the experiment's second axis and not a robustness check — restated in
measured numbers rather than asserted, and it **strengthens the registered
expectation of DEGRADED** recorded in Section 0 before any of this was measured.

### The freeze

The model is frozen at `orb.costs_registered.REGISTERED_COST_MODEL`, hashed
**`3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3`**, and the
hash is recorded in the append-only ledger at `data/state/cost_model.jsonl` with
a latch at `data/state/cost_model_latch.json`. **A test recomputes the hash from
the model and fails if the two diverge.** Cost parameters cannot change from
here without a further dated amendment naming what data existed when it was
made.
