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

### 1.1 — the claim restated to match the measured trigger rate, appended 2026-08-29 under Amendment 22

**This block is an append. Not one character above this line was edited**, and
the original statement of H-ORB is left standing so the correction is visible.

**What was falsified.** The phrase *"a **breakout** of the first 5-minute
regular-session range"* implies a **selective event** — that a breakout is
something that happens to some name-sessions and not others, and that selecting
on it is part of what the rule does. **Measurement falsified that implication.**

**A.1 TASK 5 measured the realized trigger rate at 0.982143**, `n = 560` selected
name-sessions over `n = 28` evaluable post-holdout sessions. A.1 TASK 3 of the
inference-repair pass measured the **ambiguous rate at 0.000000** on the same
`n = 560`, so essentially nothing is excluded on that ground either.

**Why it is nearly unconditional, in mechanical terms.** The opening range is
the **first five minutes**. The trigger window is everything after it to the
close — roughly **385 minutes**. Over that span a liquid name almost always
trades outside a five-minute range in one direction or the other. **The
condition selects on almost nothing. What carries whatever information exists is
the direction of the first excursion, not the fact that one occurred.**

> ### **H-ORB, restated.** Among US common stocks with **elevated opening relative volume**, **the sign of the first excursion past the opening 5-minute range predicts the direction of the remainder of the session**, **net of modeled commissions, fees, borrow and slippage**, out of sample from **2023-01-03**.

**The registered rule itself is unchanged.** Section 2's universe and event rule,
Section 3's entry, stop and exit, Section 4's sizing, Section 5's outcome and
Section 6's costs are exactly as registered. **The rule is what was registered
and it stands.** What changes is the **description of what the rule does**, and
the description was wrong.

**The joint claim survives the restatement, with its halves renamed.** It remains
a claim about **the selection** and about **the directional signal**. The
selection — top 20 by opening relative volume — is doing real conditioning work.
The **breakout half is not a selector**; it is a **direction rule**. The source
study's own numbers already said so, and this registration did not read them that
way: the plain broad-universe rule returned **3.2 percent annually at Sharpe
0.48, below passive**, while the relative-volume restriction returned **more than
1,600 percent at Sharpe 2.81** (carried, C-2 and C-3). **The selection did almost
all the work there too.**

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

### 10.1 — clause 1 restated as a joint condition, appended 2026-08-29 under Amendment 21

**This block is an append. Not one character above this line was edited**, and
clause 1 is left standing exactly as first registered so the correction is
visible.

**Clause 1 above reads as a per-component condition:** *"Both co-primaries at or
above 80 percent power at achievable N."* **That is not the quantity the latch
needs.**

Section 8 asserts the claim only if **both** co-primaries reject. The
probability that matters is therefore **the probability that both reject**, and
**that is not implied by either component power.** Two components at 0.80 each
can be jointly anywhere from **0.60** to **0.80** depending on their dependence,
and the honest statement of what the design can detect is the joint figure.

> ### **Clause 1, restated: JOINT power — the probability that both co-primaries reject — at or above 80 percent at achievable N, under the assumption Section 0 fired on.**

**Joint power is bounded above by the smaller component power, unconditionally.**
`P(A and B) <= P(A)` and `P(A and B) <= P(B)`, with no dependence assumption at
all and none that can escape it: **requiring two things is never easier than
requiring one.** So **a reader may never take the larger component power, or
either component power, as the design's power**, and
`orb.power.joint_power` returns the bound with the binding component named.

**Clauses 2 and 3 are unchanged.** The operator prior slot stays filled at
**0.30, `INDEPENDENT`** and clause 2 stays **SATISFIED**; clause 3 still requires
an **explicit operator instruction** and stays **UNSATISFIED**. **The latch
remains closed.**

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

### 11.1 — registered scope limitations, appended 2026-08-29 under Amendment 12

**This block is an append. Not one character above this line was edited**, and
the bullets above stand exactly as first registered. **Nothing here is a new
verdict branch.** The Section 0 branches are untouched, unweakened, unrequalified
and unreworded by this subsection. A scope limitation says what a verdict *means*
once it fires; it does not change *when* one fires.

**Numbering.** Two scope limitations were already registered elsewhere and are
named here so the list is complete rather than renumbered. **Nothing about them
is edited by naming them.**

- **SL-1 — the two feeds share an upstream.** ADR-022. The Massive-against-
  Alpaca-SIP first-5-minute volume ratio has an **IQR 0.46 percentage points
  wide over `n = 100` pairs**, which two independent consolidations would not
  produce. A cross-vendor `PASS` therefore establishes that **two redistributors
  of one upstream agree**, and it is **not the Concretum test**.
- **SL-2 — the two feeds overlap only from 2024-08-29.** Amendment 8. The
  agreement gate is narrowed to the overlap.

**SL-3 is registered here, in full, for the first time.**

#### SL-3 — the in-sample window rests on a single unverified feed

**The measurement.** A.1 TASK 5, 2026-08-29, `n = 16` reach probes per
credential:

| quantity | figure |
|---|---:|
| in-sample sessions, registered | **1,762** |
| in-sample sessions with **cross-vendor overlap** | **0** |
| holdout sessions, registered | **875** |
| holdout sessions with **cross-vendor overlap** | **459** |
| reference vendor's earliest served session | **2024-08-29** |
| primary vendor's earliest served session | **2016-01-04** |

**Stated plainly.** Cross-vendor agreement covers **459 holdout sessions and 0
in-sample sessions**, because the reference vendor's tier serves nothing before
**2024-08-29**. **All 1,762 in-sample sessions rest on a single unverified
feed.** The registered first-5-minute high-or-low agreement gate, **when it
fires, speaks only to the overlap region and carries no information whatsoever
about the in-sample window.**

**The exposure this names.** Concretum Research ran identical opening-range code
against **four vendors** with identical dates, parameters and starting capital
and reported final portfolio values from **226,000 to 726,000 USD** — a
threefold spread from vendor choice alone (**carried, C-13**). That spread is
the specific risk a cross-vendor agreement measurement exists to bound, and
**this repository cannot currently retire it for the in-sample window.**

**The consequence for the verdict, stated before any read exists.** **A PASS
computed on the in-sample window is conditional on a single vendor's rendering
of that window being faithful, and this repository holds no measurement
supporting that condition.** The conditional is not a caveat added afterwards;
it is part of what the PASS would mean. **Any in-sample figure this repository
reports is reported with this limitation attached in the same sentence**, on the
same terms as standing rule 13 attaches an n.

**What it is not.** It is **not** a claim that the primary vendor's in-sample
bars are wrong — no measurement says that, and none has been made. It is a
claim about **what is not known**, and standing rule 5 governs: absence is a
recorded state, never a synthesized value. It is also **not** a Section 0
branch, does not fire, and cannot fire.

**The two routes that would retire it, recorded without choosing between them
and without spending:**

1. **A reference credential whose tier reaches 2016-01-04.** This would make
   the agreement measurement runnable over the in-sample window and would
   retire SL-3 on measurement. **It costs money**, it requires an explicit
   operator instruction and its own ADR under Section 12, and **the reach a
   paid tier actually delivers is deliberately not recorded here as a number**
   — the honest way to get it is a month's spend and a second bisection.
2. **Explicit operator acceptance that the in-sample window is single-sourced.**
   This retires nothing by measurement; it records that the operator has read
   SL-3 and accepts the conditional. **It is a decision, not a finding**, and it
   would be recorded as such with its date.

**Neither route is chosen here, neither is recommended here, and no spend is
authorised by this subsection.** Both are carried to the open operator items of
`docs/HANDOVER.md`.

### 11.2 — what a positive result would and would not be evidence about, appended 2026-08-29 under Amendment 22

**This block is an append. Not one character above this line was edited.**

**Following Section 1.1**, the epistemic boundary gains one line, and it narrows
what a positive verdict may be quoted as showing:

- **A positive result would be evidence about the informational content of the
  first directional excursion** past the opening 5-minute range, among names
  with elevated opening relative volume, net of the registered cost model.
- **It would NOT be evidence that a breakout event, as commonly understood,
  selects profitable sessions.** At the measured trigger rate of **0.982143**,
  `n = 560` selected name-sessions, **almost every name-session produces one**.
  There is no meaningful population of non-breakout sessions for the breakout
  ones to be better than.

**This is a narrowing of what the same result may be claimed to show, and it
changes no threshold, no gate and no branch.**

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

### 13.1 — the operator prior, appended 2026-08-29 under Amendment 5

**This block is an append. Not one character above this line was edited**, and
the `<EMPTY>` placeholders above are left exactly as written so that a later
reader can see the slot in the state it was reserved in. The datum below is
registered by **Amendment 5**, and the amendment carries the full reasoning.

**"Do not fill this slot" above is addressed to the assistant and remains in
force for the assistant.** The slot below was filled by the **operator**.

```
operator_prior              = 0.30
operator_prior_label        = INDEPENDENT
operator_prior_recorded     = 2026-08-29
assistant_prior             = 0.15
assistant_prior_recorded    = 2026-08-28
blindness                   = independent_but_not_blind
prior_disagreement_ratio    = 2.0
calibration_eligible        = true
ambiguity_in_stated_reason  = unresolved_on_purpose
```

| field | value |
|---|---|
| **operator prior** | **0.30** |
| **label** | **INDEPENDENT** |
| **date recorded** | **2026-08-29** |
| **assistant prior** | **0.15**, recorded **2026-08-28** |
| **blindness** | **independent but not blind** |
| **disagreement** | the two priors differ by a **factor of 2.0** |
| **calibration eligibility** | **H1 is eligible for operator calibration scoring** |

**Blindness, stated as a field rather than as prose.** The label is
`INDEPENDENT`, not `adopted`: the operator formed 0.30 rather than taking the
assistant's number. But **the assistant prior of 0.15 was recorded first, on
2026-08-28, and was visible to the operator before the operator formed this
number.** So the datum is **independent but not blind**, and **a later reader
must not score 0.30 as an unanchored estimate.** The distinction matters to the
calibration ledger: an independent-but-anchored prior is a weaker observation of
the operator's belief than a blind one, and the ledger records which it has.

**The operator's stated reason, recorded in the operator's terms and not
paraphrased into something tidier:** prior house experiments have carried
pessimistic evaluations, and the operator's own research and knowledge of
intraday opening-range behaviour supports a figure above the assistant's 0.15.

**A recorded ambiguity in that reason, flagged at the time of writing and left
unresolved on purpose.** The stated reason admits two readings that push in
**opposite directions**:

1. **Harsh house gates argue for a lower prior.** If this house's evaluations
   are pessimistic because its *gates* are severe — a deflated Sharpe at 1.00, a
   per-trade t of 2.50, two co-primaries at `alpha_adj = 0.02532`, a
   concentration gate and a persistence gate — then the probability of H1
   **clearing those gates** is lower, not higher, than a typical prior on the
   underlying effect being real.
2. **Systematic under-forecasting of survival argues for a higher one.** If the
   house has repeatedly forecast death and observed survival, the correction is
   upward and 0.30 is that correction.

**The operator did not narrow between the two readings, and this registration
does not narrow on the operator's behalf.** Both are recorded. **The resolution
of H1 scores the number either way** — the prior is 0.30 against the registered
outcome, whichever reading generated it.

**Section 10 clause 2 — the latch precondition — now reads SATISFIED.** The slot
is filled and labelled `INDEPENDENT`, which is one of the two labels
`orb.latch.write_latch` accepts at runtime. **Clause 1 (both co-primaries at or
above 80 percent power) and clause 3 (explicit operator instruction) are
unchanged and both remain UNSATISFIED**, so the latch is still closed and this
entry does not open it.

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

---

## Amendment 4 — the Section 0 verdict, fired 2026-08-29

**Date:** 2026-08-29 · **Status:** accepted · records the **Section 0** firing of A.2 TASK 5

**Exactly what data existed when this amendment was made:** the session calendar
(2,637 sessions, 21 half sessions), the live access findings (n = 15 robots
fetches, n = 25 API probes), the live fee verification, and the computed power
table. **Zero bars, zero prices, zero volumes, zero trades, zero returns, and
zero PnL of any kind.**

### The verdict

> ## **PENDING_ACCESS** · clause `PENDING-ACCESS Amendment 1`
>
> *The integrity measurement this map fires on does not exist: bar revision
> (`not_yet_measured`) and cross-vendor agreement (`not_yet_measured`), both
> because A.1 TASK 1 measured **0 of 9 vendors serving a bar to this
> repository**. **Nothing is armed.** This is a verdict on access, not on H1,
> and it is **not** a source-integrity closure — no bar has been served to
> fail.*

### Every input, with its n

| input | value |
|---|---|
| `alpha_adj` | **0.02532057**, one-sided, per co-primary |
| sessions achievable (holdout) | **875**, computed from `orb.calendar` |
| **E1 power at the registered 1.40** | **0.7435** — below the 0.80 GO floor |
| **E1 power at the published 2.81** | **0.9995** — above the 0.80 GO floor |
| E1 minimum N for 80% at 1.40 | **1,006** — a shortfall of **131 sessions** |
| E1 power at the quartered 0.70 | **0.2578** — below the 0.50 BLOCKED floor |
| E2 power | **`Absent(not_yet_measured)`** — Section 9 restricts its dispersion input to the pre-period carve-out |
| bar revision rate (A.1 TASK 3) | **`Absent(not_yet_measured)`** — no credentialed vendor |
| cross-vendor agreement (A.1 TASK 4) | **`Absent(not_yet_measured)`** — no credentialed vendor |
| delisted names served | **`Absent(not_yet_measured)`** — no credentialed vendor |

### The counterfactual, computed and recorded

**Had bar integrity passed in full, the same power inputs would have fired
`DEGRADED`, clause `DEGRADED residual`.**

This matters, and it is why it is recorded here rather than left implicit.
**Section 0 registered, before any measurement existed, that "the Section 9
arithmetic and the decay evidence point to DEGRADED."** The power computation —
run on a session count derived from a NYSE rule set rather than from the prompt —
**confirms that prediction exactly**, and by the precise mechanism the DEGRADED
clause names: **E1 reaches 80 percent power at the published magnitude (0.9995)
and does not reach it at the registered assumption (0.7435).**

**The prediction was recorded before the evidence, and the evidence matched it.**
That is the only circumstance in which a DEGRADED reads as a documented answer
rather than a disappointment, and Section 0 said so in advance.

### What this changes, and what it does not

**It arms nothing.** Stage A.3 is registered as armed *"only on GO or
DEGRADED"*, and `PENDING_ACCESS` is neither. The A.3 machinery is **built and
left inert**: the collector, the corporate-actions watcher, the systemd units
and the latch machinery are written, tested and committed, and **no timer is
enabled**. Arming requires two things together — a vendor credential, and a
Section 0 re-firing at DEGRADED or better on real integrity measurements.

**It closes nothing.** H1 remains **OPEN**. `PENDING_ACCESS` is explicitly not
the `source-integrity-blocked` closure kind registered in `HYPOTHESES.md`: that
closure requires a vendor whose bars were *measured* and found unstable, and no
bar has been served.

**It costs power that is already spent.** The holdout window closed on
2026-06-30 and today is 2026-08-29, so **the 875 sessions are historical and no
further accrual is possible inside the registered window.** Reaching 80 percent
power at the registered assumption would require **extending the holdout end
date**, which is **pinned in Section 7** and would need its own dated amendment.
**This registration does not extend it**, and records here that the temptation to
do so must be met while holding no result — which is now.

---

## Amendment 5 — the operator prior, filled at 0.30 and labelled INDEPENDENT

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 13**, and records
**Section 10** clause 2 as satisfied

**Exactly what data existed when this amendment was made.** The session calendar
(2,637 sessions, 21 half sessions), the A.1 access findings (n = 15 robots
fetches, n = 25 API probes, **0 of 9 vendors serving a bar**), the live fee
verification, the computed power table, and the `PENDING_ACCESS` verdict of
Amendment 4. **Zero bars, zero prices, zero volumes, zero trades, zero returns
and zero PnL of any kind.** Three vendor credentials were present in a
git-ignored `.env` and **not one credentialed request had been sent** — the
credentialed probes of A.1 TASK 3 come after this amendment, not before it.
**The prior was therefore recorded while holding no result to fit it to**, which
is the only circumstance in which a prior is worth recording at all.

### The datum

| field | value |
|---|---|
| **operator prior** | **0.30** on a real capturable edge surviving the registered cost model out of sample |
| **label** | **INDEPENDENT** |
| **recorded** | **2026-08-29** |
| **assistant prior** | **0.15**, recorded **2026-08-28** |
| **disagreement** | **factor of 2.0** |
| **blindness** | **independent but not blind** |
| **calibration eligibility** | **eligible** |

### The conditional this amendment was told to check, and its answer

The prompt instructed: *"If an earlier amendment recorded an adopted prior of
0.15 in Section 13, do not edit that line. Supersede it with a new sequential
amendment, leave the original visible, and state in the new amendment that the
adopted figure is void and replaced."*

**The condition was checked and is false.** No earlier amendment recorded an
adopted prior. **Amendments 1 through 4 do not touch Section 13 at all**, and
Section 13 as written on 2026-08-28 carries `operator_prior = <EMPTY>`,
`operator_prior_label = <EMPTY>`, `operator_prior_recorded = <EMPTY>` together
with the instruction **"Do not fill this slot"** addressed to the assistant.
`HYPOTHESES.md` carried the same: *"Operator prior: EMPTY — reserved."*

**There is therefore nothing to void.** This is recorded as a **checked and
false** condition rather than passed over in silence, because a later reader
finding the prompt's conditional and no answer to it cannot tell whether it was
evaluated or skipped. **Nothing in this repository is void, nothing is replaced,
and the slot moved from empty to filled in one step.**

**One consequence follows and is recorded with it.** Since no adopted prior ever
existed here, **no calibration exclusion was ever recorded on adopted-prior
grounds**, and so none is voided by this amendment either. The prompt's clause
*"any earlier exclusion recorded on adopted-prior grounds is void"* is **vacuous
in this repository** — it names a state this repository never entered. **H1 is
eligible for operator calibration scoring**, and it is eligible because the slot
was filled independently, not because an exclusion was lifted.

### Blindness — why the label is INDEPENDENT and why that is not the whole story

**`INDEPENDENT` is the correct label.** The operator did not adopt 0.15; the
operator formed 0.30. Section 13 registered the test before the answer existed:
a number is `independent` *"only if it was reached without reading the line
above, and `adopted` otherwise"* — and Section 13's own framing of `adopted`
is **taking the assistant's number**, which did not happen.

**And the label is not the whole story, so the whole story is a field.** The
assistant prior of **0.15 was recorded first, on 2026-08-28, and was visible to
the operator before the operator formed 0.30.** The datum is therefore
**`independent_but_not_blind`**, recorded as its own field so that it survives
skimming. **A later reader must not score 0.30 as an unanchored estimate.**

**Why this is registered rather than smoothed.** The NPDExperiment **Amendment
0** lesson is that *an adopted prior corrupts the calibration ledger* — it makes
the ledger measure the assistant twice and the operator never. The failure mode
this amendment guards against is the **weaker sibling** of that one: a prior
that is genuinely the operator's, but formed in sight of the assistant's, scored
later as though it had been formed in a vacuum. **Recording the anchor is what
keeps the ledger honest about how strong an observation it holds.**

### The operator's stated reason, and the ambiguity inside it

**Recorded in the operator's terms:** prior house experiments have carried
pessimistic evaluations, and the operator's own research and knowledge of
intraday opening-range behaviour supports a figure above the assistant's 0.15.

**The ambiguity, flagged now and left unresolved on purpose.** That reason
admits two readings that push in **opposite directions**, and the difference is
not cosmetic:

| reading | what "pessimistic evaluations" means | direction on H1 |
|---|---|---|
| **A — harsh gates** | the house's *gates* are severe: deflated Sharpe ≥ 1.00, per-trade t ≥ 2.50, two co-primaries at `alpha_adj = 0.02532`, a 50-percent concentration gate and a 3-of-4 persistence gate | **lower** prior on H1 *clearing those gates*, because the bar is the thing that is harsh |
| **B — under-forecast survival** | the house has repeatedly forecast death and observed survival | **higher** prior, and 0.30 is that correction |

**The operator did not narrow between them, and this registration does not
narrow on the operator's behalf.** Doing so would be the assistant writing the
operator's reasoning into the calibration ledger, which is the same error as
adopting the operator's number, run backwards.

**It is left unresolved on purpose and the resolution of H1 scores the number
either way.** The prior stands at 0.30 against the registered outcome, whichever
reading generated it. **If H1 later resolves, the ambiguity is a note on the
interpretation of one datum, not a reason to rescore it.**

### What this changes, and what it does not

**Section 10, clause 2 — the operator prior slot filled and labelled — now reads
SATISFIED.** `INDEPENDENT` normalises to one of the two labels
`orb.latch.write_latch` accepts at runtime, and the runtime refusal for an empty
or unlabelled slot no longer fires on this clause.

**The latch remains closed.** Clause 1 requires **both co-primaries at or above
80 percent power at achievable N** — E1 is **0.7435** at the registered
assumption on n = 875 holdout sessions and **E2 is `Absent(not_yet_measured)`**,
so clause 1 is **UNSATISFIED**. Clause 3 requires an **explicit operator
instruction** to open the sealed in-sample read, and **none exists** — the
prompt this amendment was written under instructs the opposite, that nothing is
armed. **Two of the three clauses remain unsatisfied and Stage C does not open.**

**Nothing else moved.** **No power figure, no co-primary, no structural gate, no
threshold and no Section 0 input changed as a result of this amendment.** A
prior is not an input to Section 0 — Section 0 reads a count-derived power, a
measured share, a measured count and an operational verdict, and **a prior is
none of those four.** The `PENDING_ACCESS` verdict of Amendment 4 stands
unaltered by this entry, and is re-fired on measured inputs at A.1 TASK 10 for
reasons that have nothing to do with this amendment.

---

## Amendment 6 — the falsified secrets rule, and Section 12 under a credential

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 12**, and records
the falsification of `CLAUDE.md` non-negotiable rule 3

**Exactly what data existed when this amendment was made.** Everything Amendment
5 listed, plus **three vendor credentials present in a git-ignored `.env`** —
`ORB_MASSIVE_API_KEY` at 32 characters, `ORB_ALPACA_API_KEY` at 26,
`ORB_ALPACA_SECRET_KEY` at 44, `n = 3` present and `0` missing — and **Guard 8**,
committed and passing. **Still zero bars, zero prices, zero volumes, zero
trades, zero returns and zero PnL.** **No credentialed request had been sent when
this amendment was written**; the A.1 TASK 3 probes come after it. The amendment
therefore records a **rule correction**, not a data finding.

### The falsified rule, quoted before it is corrected

`CLAUDE.md` non-negotiable rule 3, as written on 2026-08-28:

> **Secrets never enter the repo — and none are needed.** `.env.example` is
> empty on purpose. No API key exists anywhere in this project.

**The first half stands. The second half is false, and measurement is what
falsified it.**

`docs/ACCESS.md`, A.1 TASK 1, 2026-08-29, `n = 15` `robots.txt` fetches and
`n = 25` live API probes: **0 of 9 vendors serve a 1-minute regular-session US
equity bar to this repository without a credential.** Two vendors serve
keylessly and **both publish `User-agent: * / Disallow: /`**; two more disallow
the exact API path a collector needs; **the five whose terms permit collection
all refused without a key**, refusal payloads recorded verbatim.

**This is the NPLExperiment shape and it is named as such.** A planning number
near **9.4 events per month** entered a registration as though it were an input
and measurement falsified it at **0.5, `n = 3` over 182 days** (carried, C-20),
killing H3 on a figure rather than on the world. The failure was not the wrong
number; it was **a planning number wearing a measurement's clothes.**
*"No key is needed for any Stage A source"* was exactly that, and it is
corrected the same way: **named, dated, and amended rather than quietly worked
around.**

### The corrected rule, in force

- **Credentials are required.** Established by measurement;
  `docs/ACCESS.md` → *"PERMITTED and usable today: 0 of 9."*
- **Keys live in `.env`, git-ignored**, confirmed by `git check-ignore` before
  any credentialed request is sent.
- **`.env.example` carries names only and never values.**
- **Guard 8 enforces redaction at the recording boundary** — sealed writer,
  append-only ledger, HTTP response — and redaction is **deterministic**, so the
  byte-level revision comparison of A.1 TASK 3 survives it.
- **Recordable about a credential:** variable name, presence, character length.
  **Not recordable:** the value, any prefix, any suffix, **and any hash** — a
  hash of a 32-character key is a confirmation oracle for a guess.
- **The first half of the original rule stands unchanged and unweakened: no key
  is ever committed.**

### Section 12, amended

Section 12 opens *"Zero dollars in Stage A. Free and trial tiers only."* **That
sentence is unchanged and remains in force.** What changes is that Stage A now
**holds credentials**, and the section did not contemplate that state.

| clause | before | after this amendment |
|---|---|---|
| **spend in Stage A** | zero dollars | **zero dollars — unchanged** |
| **tiers** | free and trial only | **free and trial only — unchanged**, now exercised with a credential rather than anonymously |
| **credentials held** | none contemplated | **three, on free or trial tiers**, in a git-ignored `.env`; presence and character length recordable, values never |
| **paid tier** | requires explicit operator instruction | **requires explicit operator instruction and its own ADR — unchanged and restated** |
| **request ledger** | per-vendor daily cap, charges before sending | **unchanged**, and the caps are **re-measured against the authenticated endpoints at A.1 TASK 7**, since Amendment 2 registered them provisionally against a 401 |
| **pacing** | per endpoint, never per host | **unchanged** — and the Amendment 2 corollary now bites in the other direction: **the authenticated data endpoint is a different endpoint from the 401 path**, so the 88.4/min measured on the refusal path licenses nothing |

**Two things this amendment deliberately does not do.**

1. **It does not authorise any spend.** Holding a free-tier credential is not a
   step toward a paid one. **Any paid tier requires an explicit operator
   instruction and its own ADR**, and the carried figures stay labelled carried:
   **Polygon/Massive Starter near 29 USD per month, Databento near 125 USD per
   month for a medium universe** (carried, C-18), **neither measured.**
2. **It does not raise a single pace or cap.** Amendment 2's registered
   `DEFAULT_MIN_SPACING_S = 6.0` stands until A.1 TASK 7 measures the
   authenticated endpoints. **An unmeasured endpoint is not a licence to speed
   up**, and a credential does not make an unmeasured endpoint measured.

---

## Amendment 7 — the tape-identification branch, registered and fired SAME_TAPE

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 0** by adding a
branch **ahead of** the cross-vendor agreement thresholds, and records the
A.1 TASK 4 tape measurement

**Exactly what data existed when this amendment was made.** Everything Amendment
6 listed, plus the A.1 TASK 3 credentialed probes (`n = 11`, both credentials
authenticating) and the A.1 TASK 4 tape pulls (`n = 60` requests, 20 tickers ×
5 sessions × 3 feeds, `200` on every one). **Zero trades, zero returns, zero
PnL.** **No bar value has left the sealed comparator**, and none is recorded
here: every figure below is a ratio or a count.

**The branch text was written before the numbers were read**, and the three
verdicts, their thresholds and their consequences were fixed in
`orb.integrity.TapeVerdict` and pinned by boundary test **before**
`tools/tape_identify.py` sent its first request. That ordering is what stops the
band being chosen to contain the answer.

### Why a new branch was needed at all

**Section 0's cross-vendor agreement thresholds assume two feeds that are trying
to measure the same thing.** `PASS ≥ 0.95`, `PARTIAL ≥ 0.85`, `FAIL` below —
each is a statement about how often two measurements of *the consolidated tape*
disagree on a first-5-minute high or low.

**A feed carrying a single-venue subset is not a disagreeing measurement of the
consolidated tape. It is a correct measurement of a different thing.** IEX ran
about **2.8 percent** of consolidated volume in the measured window. Scoring an
IEX-only feed against the 0.95 bar would fire **BLOCKED-4, "the top-20 selection
is not reproducible across vendors"** — on a fact about **entitlement**, while
recording it as a fact about **integrity**. Standing rule 7's principle, applied
one level up: **an entitlement condition must never quietly become an integrity
condition.**

### The branch, registered

Evaluated **before** the agreement verdict, and it gates whether that verdict may
fire at all. Fired by `orb.integrity.TapeFinding.verdict`, computed by
`orb.comparator.SealedComparator.compare_tapes`, pinned by `tests/test_tape.py`
with **every fixture on the registered boundary and one ULP across it**.

| verdict | trigger | consequence |
|---|---|---|
| **`SAME_TAPE`** | median ratio in **`[0.90, 1.10]`**, inclusive both ends | **the registered agreement thresholds apply as written** |
| **`DIFFERENT_TAPE`** | median ratio **strictly below `0.50`** | **the registered agreement thresholds do not apply and must not fire.** A first-5-minute high-or-low disagreement is a **tape-coverage finding**, not an integrity finding. Routes to an open operator item: a second credential on a comparable tape, or explicit acceptance that the agreement gate is **unmeasured** with the verdict scope narrowed accordingly |
| **`AMBIGUOUS`** | anything between | **fire nothing.** Record the full distribution and hand the operator the numbers |

**The ratio** is `secondary first-5-minute volume / primary first-5-minute
volume` per session-ticker pair. A single-venue subset presents a systematically
small fraction of a consolidated feed's volume, so the **median** identifies the
tape and the **interquartile range** says how consistently.

### The window, and why it is not the one the ladder registered

**The tape measurement was specified to run inside the pre-period carve-out. It
could not, and the reason is measured rather than argued.** A.1 TASK 3, 2026-08-29:

- **Massive refuses the carve-out outright** — `403`,
  `{"status":"NOT_AUTHORIZED",…,"message":"Your plan doesn't include this data
  timeframe."}`, 189 bytes.
- **Alpaca serves an empty set for it** — `200`, 52 bytes,
  `{"bars":null,…}`, **0 bars**.

**`n = 2` credentials, `0` serving a bar inside the carve-out.**

**The substitute is not a relaxation. It is the same argument applied at the
other end of the registered windows.** The five sessions used —
**2026-07-01, 07-02, 07-06, 07-07, 07-08** — sit **strictly after
`holdout_end` = 2026-06-30**, so they lie **outside both the in-sample and the
holdout samples**. That is the carve-out's own stated rationale, word for word:
*"the window before it sits outside both the in-sample and the holdout samples,
and reading it cannot leak a single observation any verdict will be computed
on."* The window after the holdout has the identical property.

**And it did not need the carve-out at all, which is recorded so that the
carve-out is not read as having been widened.** The **sealed comparator is
already the registered exception** to the blindness field lists — *"it reads
price and volume values from two vendors, emits only aggregate mismatch counts
and rates, and returns no bar value to any caller"* — and that exception is
**not window-limited**. `compare_tapes` returns a `TapeFinding` whose every field
is a ratio or a count, pinned by
`tests/test_guards.py::test_comparator_findings_carry_only_counts`. **The
carve-out is untouched by this amendment, its boundary is unmoved, and its
enforcement site is unchanged.**

### The measurement

**`n = 20` tickers × `5` sessions = `100` session-ticker pairs per comparison,
`100` with volume in both feeds in all three comparisons, `0` missing on either
side. `n = 60` requests, `200` on every one, `0` dollars spent.**

| comparison | verdict | median ratio | IQR | min | max | share below 0.20 | n pairs |
|---|---|---:|---|---:|---:|---:|---:|
| **Massive vs Alpaca-SIP** | **`SAME_TAPE`** | **1.005197** | [1.003096, 1.007726] | 1.000905 | 1.034148 | **0.0000** | **100** |
| Massive vs Alpaca-IEX | `DIFFERENT_TAPE` | **0.027856** | [0.021235, 0.037195] | 0.007087 | 0.069102 | **1.0000** | 100 |
| Alpaca-SIP vs Alpaca-IEX | `DIFFERENT_TAPE` | **0.027761** | [0.021200, 0.037068] | 0.007035 | 0.068904 | **1.0000** | 100 |

**Bar rows served: Massive 61,094; Alpaca-SIP 61,099; Alpaca-IEX 37,234.**

**The verdict on the pair this experiment would use is `SAME_TAPE`. The
registered agreement thresholds apply as written, and nothing in Section 0 is
disapplied.**

### The two controls, and why they are in the amendment rather than a footnote

**A discriminator that has only ever been pointed at one pair is an assertion
about nothing.** Two controls were measured alongside:

1. **Massive vs Alpaca-IEX** — a positive control on a pair that *must* separate.
   It did: **0.0279**, with **100 of 100 pairs** below the 0.20 single-venue
   threshold.
2. **Alpaca-SIP vs Alpaca-IEX** — a **within-vendor** control. Same vendor, same
   host, same request, **one parameter changed**. It separated at **0.0278**.

**The second is the one that matters.** It removes every explanation for a
separation that is not the tape: not the vendor, not the host, not the request
shape, not this repository's window arithmetic. **The discriminator measures the
tape.**

### Documented against measured, and a rare agreement

| claim | label | figure |
|---|---|---|
| Massive aggregates cover all US exchanges plus the FINRA TRFs | **documented**, carried from vendor documentation, **not verified this session** | — |
| Alpaca `feed=sip` is all US exchanges; `feed=iex` is IEX alone | **documented**, carried, **not verified this session** | — |
| Massive against Alpaca-SIP | **measured** | **median 1.0052, n = 100** |
| Alpaca-IEX against either consolidated feed | **measured** | **median ≈ 0.028, n = 100** |

**Documented and measured agree here, and that is recorded as a finding rather
than assumed as a default.** Under standing rule 4 the measurement wins wherever
the two disagree; on this vendor pair, on this question, they do not.

### The one disagreement inside the SAME_TAPE verdict, recorded because it is systematic

**Alpaca-SIP reports more first-5-minute volume than Massive in `100` of `100`
pairs.** The **minimum** ratio is **1.000905** — strictly above 1.0 — and the
median is **1.005197**. **This is not noise.** Noise straddles 1.0; this does
not, in a hundred consecutive observations.

**The magnitude is about 0.5 percent and the verdict is unaffected** — 1.0052
sits far inside the `[0.90, 1.10]` band. **The direction is the finding**, and it
is left as an open question rather than explained away: a consistent one-sided
volume difference between two feeds of the same tape is most likely a difference
in **which prints each vendor includes** — odd lots, TRF prints, or the handling
of the fractional share volumes Massive serves on some bars. **This repository
has not measured which, and does not guess.** It is recorded here so that a
later cross-vendor agreement figure below 1.00 is read against a known
systematic offset rather than as fresh evidence.

### The common upstream, and what it costs the agreement gate

**The two feeds appear to redistribute a common upstream, and the evidence is
the tightness rather than the level.** The interquartile range of the
Massive-against-Alpaca-SIP ratio is **[1.003096, 1.007726] — 0.46 percentage
points wide, over 100 session-ticker pairs.** Two independently constructed
consolidations of US equity activity would not agree to within half a percent
with that consistency; a **shared SIP-derived upstream, redistributed twice,**
would.

**The consequence is registered now, before the agreement figure exists, and it
narrows what that figure can establish:**

> **The A.1 TASK 4 cross-vendor agreement measurement on this pair scores a
> redistribution pipeline, not two independent feeds.** A `PASS` establishes
> that **two redistributors of one upstream agree**. It does **not** establish
> that the first-5-minute high and low are vendor-independent, and it is
> **not** the Concretum test.

**Concretum ran identical opening-range code against four vendors and reported
final portfolio values from 226,000 to 726,000 USD** — a threefold spread from
vendor choice alone (carried, C-13). **That spread is a spread across
upstreams.** Measuring agreement between two redistributors of one upstream
**cannot detect it**, and this registration says so **before** the number is in
hand rather than after it comes back high.

**This is recorded as an open operator item**, and it is the honest one: a third
feed on a **genuinely different upstream** would be needed to run the Concretum
test as intended. **It does not block the ladder**, because the registered
agreement gate is a test of *this* pair and is stated as such — but the epistemic
boundary of Section 11 gains a line, and the vendor selection ADR states it in
the decision text rather than in a footnote.

---

## Amendment 8 — measured historical reach, and the agreement gate narrowed to the overlap

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 0**'s cross-vendor
agreement clause by narrowing the window it can be measured over, and records
the A.1 TASK 5 reach bisection

**Exactly what data existed when this amendment was made.** Everything Amendment
7 listed, plus the A.1 TASK 5 bisection: **`n = 32` probes across 2 credentials
over `n = 5,934` candidate sessions spanning 2003-01-02 to 2026-07-29**. **Zero
trades, zero returns, zero PnL**, and **no bar value recorded anywhere** — the
bisection reads a **status code** and a **bar count**, both on the readable field
list, and the count is computed inside the sealed comparator.

### The measurement

**Reach was bisected, not read from a pricing page.** Standing rule 4 forbids
recording a documented tier limit as though it were measured, and this is the
task where that rule has teeth: **both figures below contradict what a planning
assumption would have produced.**

| credential | earliest served session | probes | in-sample reachable | holdout reachable |
|---|---|---:|---|---|
| **Alpaca** | **2016-01-04** | **16** | **1,762 of 1,762 — shortfall 0** | **875 of 875 — shortfall 0** |
| **Massive** | **2024-08-29** | **16** | **0 of 1,762 — shortfall 1,762** | **459 of 875 — shortfall 416** |

**Monotonicity was checked rather than assumed.** After each boundary was found,
the sessions immediately before and after it were probed directly:

- Massive: **2024-08-28 → `403`, 0 bars** · **2024-08-29 → `200`, 814 bars** ·
  **2024-08-30 → `200`, 707 bars.**
- Alpaca: **2015-12-31 → `200`, 0 bars** · **2016-01-04 → `200`, 718 bars** ·
  **2016-01-05 → `200`, 694 bars.**

**The boundary refusal payload, verbatim and redacted** (Massive, 189 bytes):

> `{"status":"NOT_AUTHORIZED","request_id":"…","message":"Your plan doesn't
> include this data timeframe. Please upgrade your plan at
> https://polygon.io/pricing"}`

**Alpaca's boundary is not a refusal at all**, and that difference is a finding
in its own right: **`200` with `0` bars** on 2015-12-31 and every session before
it. Under standing rule 7 those are different families — Massive states a
`source_failed`-shaped refusal, Alpaca serves a `no_data`-shaped empty set — and
**bisecting on bar count alone would have merged them.** The search separates the
three cases by **status code plus bar count**, never by count alone.

### Two figures that are exactly what they are, recorded without smoothing

**Massive's earliest served session is 2024-08-29 and today is 2026-08-29 — a
rolling window of exactly 24 months.** The free tier is a moving two-year
window, measured to the day.

**Alpaca's earliest served session is 2016-01-04, which is the exact first
session of the registered in-sample window.** The registration chose that date
from the source study; Alpaca's history begins independently at the same point.
**The coincidence is recorded as a coincidence, and it is a fragile one:** the
in-sample window is covered with **zero margin**. A vendor trimming one month of
history, or a registration moving its start one session earlier, breaks the
coverage immediately. **This is not a comfortable pass. It is an exact one.**

### What the shortfall is decisive about, stated precisely

**Massive's free tier cannot serve the registered windows. That is decisive, it
is not worked around, and it removes Massive from consideration as the primary
collection vendor.** `docs/ACCESS.md` recommended Massive as primary on
**documented** grounds — the only probed vendor publishing a delisted-ticker
reference endpoint *and* minute aggregates on one host. **Standing rule 4 says
the measurement wins**, and the measurement says the tier serves **none of the
1,762 in-sample sessions.**

**Swapping the primary on a measurement is the rule working, not a work-around**,
and the amendment states the difference because the distinction matters: a
work-around would be keeping Massive as primary and shrinking the window to fit
it. **The registered windows do not move.**

**The registered windows remain fully reachable, on Alpaca.** E1 power on the
reachable holdout is **0.7435 at the registered 1.40** and **0.9995 at the
published 2.81** — **identical to the figures Amendment 4 fired on**, because
the reachable count *is* the registered count. **No power figure moves.**

### What the shortfall does cost — the agreement gate, narrowed

**The cross-vendor agreement measurement needs two feeds over the same sessions,
and the two feeds overlap only from 2024-08-29.**

| window | sessions registered | sessions with **both** feeds | share |
|---|---:|---:|---:|
| in-sample, 2016-01-04 to 2022-12-30 | **1,762** | **0** | **0.0 percent** |
| holdout, 2023-01-03 to 2026-06-30 | **875** | **459** | **52.5 percent** |

**The amendment.** The Section 0 cross-vendor agreement clause — `PASS ≥ 0.95`,
`PARTIAL ≥ 0.85`, `FAIL` below, firing **BLOCKED-4** — is **unchanged in
threshold and in precedence**, and is narrowed in **scope**:

> **The registered cross-vendor first-5-minute agreement share is measurable
> only over sessions on or after 2024-08-29 — `n = 459` holdout sessions and
> `n = 0` in-sample sessions.** A `PASS` establishes agreement over **the last
> 52.5 percent of the holdout and none of the in-sample window**. It is
> **not** evidence about vendor agreement in 2016 through 2024, and no
> downstream figure may treat it as such.

**Why the narrowing is registered rather than absorbed.** The agreement gate
exists because of the Concretum finding — **identical opening-range code, four
vendors, final portfolio values from 226,000 to 726,000 USD** (carried, C-13).
That spread is a claim about **the whole sample**, and a gate measured on the
recent half of the holdout is a **weaker instrument than the one registered**.
**Recording that it is weaker is the difference between a scope limit and a
silent substitution.**

**And it compounds with Amendment 7.** The pair already scores **a
redistribution pipeline rather than two independent feeds**. So the agreement
gate, as it can actually be run, establishes that **two redistributors of one
upstream agree, on 459 of 2,637 registered sessions**. Both limits are stated
here, together, before the number exists.

### The costed decision, handed to the operator

**No spend is authorised by this amendment and none is recommended by it. Zero
dollars have been spent and Section 12 is unchanged.**

| item | value | label |
|---|---|---|
| what a paid Massive tier would buy | **restoration of the cross-vendor agreement gate to the full registered windows** — nothing else | reasoned from the measurement |
| what it would **not** buy | primary collection. **Alpaca already covers the registered windows in full at zero cost** | **measured** |
| monthly figure | **near 29 USD per month, Polygon/Massive Starter** | **carried**, C-18, vendor pricing page, **never measured by this repository** |
| what the tier is claimed to unlock | the vendor's own refusal payload states an upgrade unlocks the timeframe: *"Your plan doesn't include this data timeframe. Please upgrade your plan."* | **measured** — this is the refusal, verbatim |
| the reach a paid tier actually delivers | **not measured, and not recorded here as a number** | — |

**The last row is the point.** A paid tier's reach is exactly the kind of figure
this repository refuses to carry from a pricing page — that is standing rule 4,
and the free tier's measured 24-month window is a live demonstration that a
bisection is worth running. **If the operator wants that number, the honest way
to get it is to buy one month and bisect again**, at which point it becomes a
measurement. **This repository will not record an unmeasured reach as a figure,
and it will not spend to find out without an explicit operator instruction and
its own ADR.**

### What did not change

**No power figure, no co-primary, no threshold and no registered window moved.**
The in-sample window opens 2016-01-04 and the holdout opens 2023-01-03, exactly
as Section 7 pins them. E1 power is **0.7435 at 1.40** and **0.9995 at 2.81** on
`n = 875` reachable holdout sessions — the same figures Amendment 4 fired on.
**Section 0's clauses are unchanged in text, threshold and precedence; only the
scope over which one of its inputs can be measured is narrowed, and the
narrowing is written down.**

---

## Amendment 9 — rate ceilings measured on the authenticated endpoints

**Date:** 2026-08-29 · **Status:** accepted · **supersedes Amendment 2's
provisional pacing**, which registered figures explicitly labelled *unmeasured*
and stated they would be re-measured at the first task holding a credential.
**This is that task.** Amendment 2 is left visible and unedited.

**Exactly what data existed when this amendment was made.** Everything Amendment
8 listed, plus the A.1 TASK 6 delisted measurement and the A.1 TASK 7
escalation: **`n = 53` requests across 4 endpoint-spacing cells, all against
authenticated paths.** **Zero trades, zero returns, zero PnL.**

### What Amendment 2 said would happen, and did

Amendment 2 registered `DEFAULT_MIN_SPACING_S = 6.0` and stated that the
88.4-per-minute figure measured against a 401 was **evidence about the refusal
path and nothing else**. That prediction is now testable, and it held: **the
authenticated path refuses at 5 per minute, not 88.** The unauthenticated
measurement over-stated the authenticated ceiling by a factor of **17.7**, and
**an operator who had paced from it would have been refused on 3 of every 8
requests.**

### The measurement

| vendor | endpoint | spacing | n | achieved | admitted | status distribution | first refusal |
|---|---|---:|---:|---:|---:|---|---:|
| Massive | `/v3/reference/tickers` | 2.0 s | 8 | 30.45/min | **5** | `{200: 5, 429: 3}` | **request 6** |
| Massive | `/v2/aggs/…/1/minute/…` | 2.0 s | 8 | 28.67/min | **5** | `{200: 5, 429: 3}` | **request 6** |
| Massive | `/v2/aggs/…/1/minute/…` | 0.5 s | 12 | 90.08/min | **0** | `{429: 12}` | request 1 |
| Alpaca | `/v2/stocks/AAPL/bars` | 0.2 s | 25 | 134.05/min | **25** | `{200: 25}` | **none** |

**The Massive refusal, verbatim and redacted** (`HTTP 429`):

> `{"status":"ERROR","request_id":"…","error":"You've exceeded the maximum
> requests per minute, please wait or upgrade your subscription to continue.
> https://massive.com/pricing"}`

**This is the first HTTP 429 this repository has ever measured.** A.1 TASK 2
recorded *"no endpoint returned HTTP 429, n = 18, 0 refusals on a limit"* and
was explicit that this was a fact about the refusal path. **The limiter exists,
it is on the authenticated path, and it is now measured.**

### The three readings, stated separately because they are different claims

**1. Massive's measured ceiling is 5 requests per minute, on both endpoints.**
First refusal at request **6 of 8** in both `n = 8` cells. **The two endpoints
were measured separately and agreed.** Under solattn ADR-021 a ceiling is a
property of an endpoint, so agreement between two endpoints is **evidence that
they share a limiter**, not an assumption that they do — and it is recorded as
evidence, on `n = 2` endpoints.

**2. Documented and measured agree, and that is recorded as a finding.**
Massive's documented free-tier limit is **5 per minute** and the measured
boundary is **5 per minute**. Standing rule 4 says the measurement wins wherever
the two disagree; here they do not. **The rule still earned its keep**, because
the 88.4-per-minute figure from the unauthenticated path would have been read as
a measurement beating that documentation, and Amendment 2 refused to read it
that way. **The refusal was correct.**

**3. Alpaca's ceiling was not reached and is not recorded as a number.**
**25 of 25 admitted at 134.05 per minute, `0` refusals.** The honest statement is
**"the ceiling is at or above 134 per minute and is not known exactly"**, and
`MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` is **`None`** rather than a large
number. *"The ceiling was not reached"* is a different claim from *"there is no
ceiling"*, and conflating them is how an unmeasured figure enters a registration.

### The registered operating pace

**Half the measured ceiling, per endpoint, reduced further where recorded terms
ask for it.**

| endpoint | operating spacing | per minute | basis |
|---|---:|---:|---|
| `massive:aggs` | **24.0 s** | **2.50** | **measured** — half of a measured 5.0/min 429 boundary |
| `massive:reference` | **24.0 s** | **2.50** | **measured** — half of a measured 5.0/min 429 boundary |
| `massive:grouped` | 24.0 s | 2.50 | **unmeasured endpoint**; carries its vendor's measured figure |
| `alpaca:bars` | **1.0 s** | **60.0** | **unmeasured ceiling**; half of a **134.05/min observed admitted rate** is 67/min, and 60 sits below it |
| `alpaca:multibars`, `alpaca:account`, `alpaca:assets` | 1.0 s | 60.0 | **unmeasured endpoints**; carry their vendor's figure |

**Half of an observed admitted rate is not half of a measured ceiling**, and
`orb.vendors.PACE_BASIS` says which each endpoint rests on, per endpoint, in the
source. Pinned by
`tests/test_vendors.py::test_the_operating_pace_is_at_most_half_the_measured_ceiling`,
which walks every endpoint with a measured ceiling and fails if any is paced
above half of it, and by
`test_an_unmeasured_endpoint_is_never_paced_faster_than_a_measured_sibling`.

### The per-vendor daily caps, and what they are not

| vendor | cap | reasoning |
|---|---:|---|
| Massive | **600** | at a measured 5/min, about two hours of continuous full-rate use |
| Alpaca | **2,000** | covers the 40-ticker probe slice, its identical re-pull, and headroom |

**The cap charges before the request is sent** — `orb.ledger.RequestLedger.charge`
— so an exhausted budget **refuses rather than overspends**, and an unregistered
vendor has no cap and is **refused outright**.

**Neither cap is a throughput target and neither is derived from a daily
allowance, because no daily allowance was measured on either vendor.** Deriving
a cap from an unmeasured daily allowance would be exactly the pricing-page
reasoning standing rule 4 forbids. **They are circuit breakers against a runaway
loop, and the amendment says so rather than dressing them up as limits.**

### What did not change

**Zero dollars spent.** Section 12's *"Zero dollars in Stage A. Free and trial
tiers only"* is unchanged. **No power figure, no threshold, no window and no
Section 0 clause moved.** Amendment 2's text stands unedited above; only the
figures it registered **as provisional and unmeasured, and explicitly promised
to re-measure**, are superseded.

---

## Amendment 10 — two further Section 0 states, and the verdict re-fired PENDING_REVISION

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 0** by adding two
states and refining one ordering, and records the A.1 TASK 10 firing

**Exactly what data existed when this amendment was made.** Everything Amendment
9 listed, plus the A.1 TASK 9 probe pull: **480 sealed files, 737,507 bars, 40
tickers × 60 sessions = 2,400 session-ticker pairs, `HTTP 200` on every file.**
**Zero trades, zero returns, zero PnL, and no bar value read outside the sealed
comparator.** **The bar revision measurement does not exist and cannot exist
before 2026-09-12**, so nothing in this amendment can have been shaped by it.

### The two new states

**`PENDING_SPEND`.** A credentialed vendor **serves bars**, and its **measured**
historical reach does **not** cover the registered windows. **It arms nothing and
authorises no spend** — it hands the operator a costed decision. **It did not
fire today**, and the reason is the measurement: Alpaca reaches **1,762 of 1,762
in-sample and 875 of 875 holdout sessions**. It is registered anyway, **so that a
later reach shortfall has a clause to land in rather than being discovered
without one.**

**`PENDING_REVISION`.** Access passes — a vendor serves and its measured reach
covers the registered windows — and an integrity measurement **still does not
exist**, because the registered **14-calendar-day wait** between the probe pull
and its identical re-pull has not elapsed.

**Why it is a separate state rather than a variety of `PENDING_ACCESS`.** The two
have **completely different next actions**: one needs a credential, the other
needs a **calendar**. Collapsing them would make the map say *"we cannot reach a
vendor"* on a day when this repository holds 737,507 sealed bars from one. **The
wait is the measurement** — a re-pull sent early measures a revision rate biased
toward zero, **and zero is the shape of a `PASS`** — so `PENDING_REVISION` is a
**legitimate parked outcome, not a failure.**

### The ordering refinement, and the case Amendment 1 could not have contemplated

**Amendment 1 put its clause ahead of every BLOCKED trigger.** It was written
while **no vendor served any bar at all**, so **no BLOCKED input could be
measured** and the ordering was **untestable in practice**. That is no longer
true: one integrity input can now be **measured** while another is **absent** —
delisted coverage is measured at **203 names, n = 229**, while bar revision
cannot be measured until 2026-09-12.

**The refinement, registered:**

- When the access verdict is **`NO_VENDOR_SERVES`**, **Amendment 1's clause
  stands unchanged in text, threshold and precedence**: an absent integrity input
  fires `PENDING_ACCESS` ahead of everything.
- When a vendor **serves**, a BLOCKED trigger whose input is **measured** fires
  **ahead of** the pending states, and a BLOCKED trigger whose input is
  **absent** is **skipped**.

**The principle is Amendment 1's own, applied consistently.** Its objection was
to closing H1 *"on evidence that does not exist"*. **That objection does not
apply to evidence that does.** A measured zero delisted count is evidence, and
waiting fourteen days does not make it less so.

**One structural consequence.** The delisted count and the agreement share travel
together in a single `AgreementFinding`, but they are **measured at different
times**. Without a separate route into the map, an absent agreement share would
**hide a measured delisted count**, and **a measured zero could not fire
BLOCKED-3** — the clause that exists to stop a survivor-only universe. So
`fire_section0` gains a keyword-only `delisted_with_intraday` input, used when
the agreement record is absent. **Pinned on the boundary**: 20 fires
`PENDING_REVISION`, **19 fires BLOCKED-5**.

### Enforcement

The full clause order, fired by `orb.section0.fire_section0` and pinned by
`tests/test_section0.py`:

| order | clause | condition |
|---:|---|---|
| 1 | `PENDING_ACCESS` (Amendment 1) | no vendor serves **and** an integrity input is absent |
| 2 | `BLOCKED-1` | E1 power at the published magnitude `< 0.50` |
| 3 | `BLOCKED-2` | revision **measured** and `FAIL` |
| 4 | `BLOCKED-3` | delisted count **measured** and `== 0` |
| 5 | `BLOCKED-4` | agreement **measured** and `FAIL` |
| 6 | `BLOCKED-5` | delisted count **measured** and `< 20` |
| 7 | `PENDING_SPEND` (Amendment 10) | measured reach does not cover the registered windows |
| 8 | `PENDING_REVISION` (Amendment 10) | access passes and an integrity input is absent |
| 9 | `GO` | unchanged |
| 10 | `DEGRADED` | unchanged, the residual |

**`GO` and `DEGRADED` are unchanged in text, threshold and precedence**, and
`test_neither_go_nor_degraded_is_reachable_while_an_input_is_absent` walks every
access state crossed with every absent-input combination and requires that
neither can fire. **`test_pending_revision_is_not_reachable_when_both_inputs_are_present`**
does for the new clause what Amendment 1's pin did for the old one: **it is inert
the moment the measurements exist, and it is not a bypass.**
**`test_all_five_registered_verdicts_are_reachable`** requires that no clause is
decoration.

### The verdict

> ## **PENDING_REVISION** · clause `PENDING-REVISION Amendment 10`
>
> *Access passes and the integrity measurement still does not exist. **Nothing
> is armed.** The registered 14-calendar-day wait between the probe pull and its
> identical re-pull has not elapsed, and **that wait is the measurement**. This
> is a **parked outcome, not a failure**, and it is **not** a source-integrity
> closure.*

### Every input, with its n

| input | value |
|---|---|
| `alpha_adj` | **0.02532057**, one-sided, per co-primary |
| sessions achievable, holdout | **875** |
| **E1 power at the registered 1.40** | **0.7435** — below the 0.80 GO floor |
| **E1 power at the published 2.81** | **0.9995** — above the 0.50 BLOCKED floor |
| E1 minimum N for 80 percent at 1.40 | **1,006** — a shortfall of **131** |
| **E2 power** | **`Absent(not_served)`** — **`n = 2` credentials, `0` serving the pre-period carve-out.** Massive refuses it (`403`), Alpaca serves `0` bars |
| **collection access** | **`SERVING_FULL_REACH`** |
| primary vendor | **Alpaca**, earliest served session **2016-01-04**, `n = 16` probes |
| in-sample reachable | **1,762 of 1,762** |
| holdout reachable | **875 of 875** |
| reference vendor | **Massive**, earliest served session **2024-08-29**, `n = 16` probes |
| cross-vendor overlap | starts **2024-08-29** — **459 of 875** holdout, **0 of 1,762** in-sample |
| **tape verdict** | **`SAME_TAPE`**, median ratio **1.005197**, `n = 100` pairs |
| **delisted names enumerated in window** | **4,731** of 6,421 served |
| **delisted names with intraday history** | **203**, `n = 229` checked — **`PASS`** |
| **bar revision** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** |
| probe slice | **60 sessions × 40 tickers = 2,400 pairs**, 480 files, **737,507 bars** |
| **earliest eligible re-pull** | **2026-09-12** |

### What moved from PENDING_ACCESS, and what did not

**Amendment 4 fired `PENDING_ACCESS` on `n = 9` vendors and `0` usable.** Three
of its inputs have moved from **absent** to **measured**, and the movement is the
whole content of this resumption:

| input | Amendment 4 | now |
|---|---|---|
| vendors serving a 1-minute RTH bar | **0 of 9** | **2 of 2 credentialed** |
| delisted names with intraday history | **`Absent`** | **203, n = 229 — `PASS`** |
| tape | not a registered question | **`SAME_TAPE`**, median 1.005197, n = 100 |
| measured reach | **`Absent`** | **Alpaca 2016-01-04, Massive 2024-08-29**, n = 16 each |
| measured rate ceiling | **unmeasured, against a 401** | **Massive 5.00/min**; Alpaca **not reached** |
| bar revision | **`Absent`** | **`Absent`** — the clock now exists and runs to **2026-09-12** |
| cross-vendor agreement share | **`Absent`** | **`Absent`** |

**Not one power figure changed.** E1 is **0.7435** at the registered assumption
and **0.9995** at the published one, on `n = 875` — **identical to Amendment 4**,
because the reachable session count *is* the registered session count.

**`GO` and `DEGRADED` were unreachable today and the code says so rather than the
prose.** Both require the revision and agreement measurements, and neither
exists. `tools/refire_section0.py` **refuses and exits 78** if the map ever hands
it one, so a future run cannot record a verdict this repository does not hold.

**It arms nothing.** Stage A.3 arms only on `GO` or `DEGRADED`.
`systemctl --user list-timers` shows **0 `orb-` units** and both timers report
**`not-found`**.

**It closes nothing.** H1 remains **OPEN**. `PENDING_REVISION` is explicitly not
the `source-integrity-blocked` closure kind: that requires a vendor whose bars
were *measured* and found unstable, and **the measurement that could do that is
fourteen days away.**

---

## Amendment 11 — the pre-period carve-out, falsified by measurement and amended two-sided

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 9, dispersion
inputs**, and the carve-out stated in `CLAUDE.md`

**What data existed when this amendment was made.** Everything measured on
2026-08-29 and recorded in Amendments 6 through 10: two credentials
authenticating, `n = 2`; measured historical reach on both, `n = 16` probes each
— **Alpaca serves from 2016-01-04, Massive from 2024-08-29**; a tape verdict of
`SAME_TAPE` at median ratio **1.005197**, `n = 100` pairs; delisted coverage
`PASS` at **203** names, `n = 229`; a sealed probe slice of **480 files** and
**737,507 bars**; and a Section 0 verdict of `PENDING_REVISION`. **No bar
revision measurement and no cross-vendor agreement share existed, and neither is
eligible before 2026-09-12.** **Zero dollars had been spent.** This amendment
was written while holding all of that and **no** dispersion figure of any kind.

### 1. The falsification, recorded before the remedy

**The registration reserved the E2 dispersion input to a carve-out strictly
before 2016-01-04.** Section 9 states it, `CLAUDE.md` states it, and
`orb.preperiod` enforced it at one site with the boundary in one place
(ADR-012).

**Measurement falsified the assumption the reservation rested on.** A.1 TASK 5,
2026-08-29, bisected historical reach on both credentials at `n = 16` probes
each:

| credential | earliest served session | sessions served before 2016-01-04 |
|---|---|---:|
| **Alpaca** | **2016-01-04** — *exactly* `CONFIG.in_sample_start` | **0** |
| **Massive** | **2024-08-29** | **0** |
| | | **`n = 2` credentials, 0 serving** |

**The carve-out was never reachable.** E2 power was therefore recorded
`Absent(not_served)` at Amendment 10 rather than computed, and it entered the
Section 0 firing as an absence.

**This is the NPLExperiment shape and the `CLAUDE.md` rule 3 shape together**: a
planning assumption entered a registration, and measurement falsified it. It is
**amended rather than worked around**, and the original text is left standing
everywhere it appears so the correction is auditable.

### 2. The amended carve-out, stated exactly

**The permitted region is two-sided.** A bar is readable through the carve-out
when **either** holds:

1. its session is **strictly before** `CONFIG.in_sample_start` = **2016-01-04** —
   enforced at the instant `CONFIG.pre_period_end_ms` =
   **2016-01-04T14:30:00.000Z**, **exclusive**, which is 09:30:00 US Eastern
   (EST, UTC−05:00) on that session. **Measurement shows this region is empty
   for both credentials**; it is retained unweakened, not deleted.
2. its session is **strictly after** `CONFIG.holdout_end` = **2026-06-30** —
   enforced at the instant `CONFIG.post_holdout_start_ms` =
   **2026-07-01T04:00:00.000Z**, **inclusive**, which is 00:00:00.000 US Eastern
   (EDT, UTC−04:00) on 2026-07-01.

**Every other session remains sealed**, including the whole of the in-sample
window 2016-01-04 to 2022-12-30 and the whole of the holdout 2023-01-03 to
2026-06-30.

**Why the second boundary is Eastern midnight and not UTC midnight.** UTC
midnight on 2026-07-01 is **20:00 Eastern on 2026-06-30**, which is inside the
last holdout session date; a carve-out beginning there would admit that
session's after-hours bars. Eastern midnight seals the whole of 2026-06-30.
Standing rule 14 binds here: the registered windows are stated in session dates,
and a session date is an Eastern date.

### 3. The cost, stated in full, and not in a commit message

**The post-holdout region sits outside both registered windows, so reading it
leaks no observation any verdict is computed on.** That is the whole of what it
has in common with the original boundary.

**It is not equivalent to the original boundary, and this registration does not
claim it is.** A dispersion figure estimated **after** 2026-06-30 reflects a
regime **later** than the sample it will be applied to. A pre-2016 estimate
would have reflected an **earlier** one. **Neither is neutral. The compromise
now runs forward rather than backward.**

**A dispersion figure drawn from a post-holdout regime may misstate in-sample
dispersion in either direction by an amount this repository has not measured and
does not claim to bound.** It is not asserted to be conservative, it is not
asserted to be small, and no bound on it is registered here — because none was
measured. **Every E2 figure produced from a post-holdout dispersion input
carries this caveat attached in the same sentence.**

**What this does to E2's meaning.** E2's power computation asks how large a
sample is needed for a mean net per-trade PnL to clear zero at `alpha_adj`
against a given per-trade dispersion. A dispersion input that is too small
overstates power; one that is too large understates it. **The direction of the
error is unknown here**, so the resulting power figure is a **point estimate
with an unquantified regime bias**, and it is registered as such rather than as
a measurement of the in-sample window's dispersion.

### 4. The region moves, and what is recorded instead

**The post-holdout region grows as real time advances.** It is defined by a
fixed lower edge and an open upper end, so it is larger tomorrow than today.

**It never intersects a registered window.** `CONFIG.holdout_end` is
**2026-06-30** and is pinned; the lower edge sits after it; nothing the passage
of time does can move the region backwards across it.

**The specific sessions used in any computation are recorded in the append-only
ledger at the time of that computation, and are not fixed in advance here.** A
registration that named a session list today would be naming sessions that did
not exist when the design was registered, which is a different and worse thing
than recording what was actually read when it was read.

### 5. The enforcement site, extended rather than replaced

**`orb.preperiod.require_pre_period` and `orb.preperiod.gate_pre_period` are now
two-sided window checks.** **Nothing already pushed is renamed**, per Section 14
rule 1:

- `require_pre_period` and `gate_pre_period` keep their names and now admit both
  halves. `require_carve_out` and `is_carve_out` are added as the names that say
  what the check now does; `require_pre_period` delegates to `require_carve_out`.
- `is_pre_period` keeps its **exact original meaning** — strictly before the
  2016 boundary — because `orb.bars` uses it to validate a bar claiming
  `PRE_PERIOD` provenance, and that claim is still the narrow one.
- `PrePeriodViolationError` keeps its name.
- `orb.bars.Provenance` gains **`POST_HOLDOUT`**, validated at construction
  against `is_post_holdout`. It **widens nothing**: it names a region the
  amended carve-out already permits, so that readability is a field on the bar
  rather than something a caller remembers to assert.

**Both boundaries are held to the same two structural guards**, in
`tests/test_guards.py`:

- `test_no_module_outside_config_hardcodes_the_pre_period_boundary` — **neither**
  literal is re-typed outside `config.py`;
- `test_only_preperiod_reads_the_boundary_from_config` — **neither** is read
  from config outside `preperiod.py`;
- and a new third, `test_both_carve_out_edges_are_actually_read_by_preperiod`,
  which fails if an edge stops being read by the one enforcement site. A second
  boundary with weaker enforcement than the first would be the whole hole.

### 6. The four boundary fixtures, all sitting exactly on their edges

`tests/test_preperiod.py`, per the InsiderExperiment lesson that a fixture
comfortably inside its boundary lets a moved threshold pass unnoticed:

| # | fixture | instant | expected | test |
|---:|---|---|---|---|
| 1 | one millisecond **before** the pre-period edge | `1451917799999` = 2016-01-04T14:29:59.999Z | **passes** | `test_one_millisecond_before_the_boundary_passes` |
| 2 | the pre-period edge **itself** | `1451917800000` = 2016-01-04T14:30:00.000Z | **refused** | `test_the_boundary_instant_itself_is_refused` |
| 3 | the **last instant of 2026-06-30** | `1782878399999` = 2026-07-01T03:59:59.999Z = 2026-06-30T23:59:59.999 ET | **refused** | `test_the_last_instant_of_the_holdout_is_refused` |
| 4 | the **first instant of 2026-07-01** | `1782878400000` = 2026-07-01T04:00:00.000Z = 2026-07-01T00:00:00.000 ET | **passes** | `test_the_first_instant_after_the_holdout_passes` |

**All four are exercised, `n = 4` edges, and the sealed interior is swept
separately** at the first and last session of each registered window by
`test_the_sealed_window_between_the_two_edges_is_refused_throughout`.

**Mutation 13 was added and run.** It moves fixture 3 off its edge — from
`POST_MS − 1` to `POST_MS − 172,800,000`, two days inside the sealed side — and
moves `is_post_holdout`'s threshold a day with it. **The suite goes green**,
which is the point: the fixture stops binding, and the harness records that it
stopped rather than the reader having to notice. `n = 13` mutations, **0 harness
failures**, bytecode purged before every run.

### 7. What this amendment does not do

- **It does not open the Stage C or Stage D latch, and does not touch either.**
  Both latch files remain absent; `data/state/` holds no `stage_c_read.json` and
  no `stage_d_read.json`.
- **It authorises no spend.** Zero dollars.
- **It does not weaken, requalify or reword any Section 0 branch.**
- **It does not change E1.** E1 remains **0.7435** at the registered 1.40 Sharpe
  assumption on `n = 875` achievable holdout sessions, against a minimum
  **1,006** for 80 percent power.
- **It does not claim the post-holdout region is a good substitute for the
  pre-period one.** It claims only that it is **outside both registered
  windows**, which is the property that makes it readable at all.

---

## Amendment 12 — the in-sample single-source scope limitation, registered as SL-3

**Date:** 2026-08-29 · **Status:** accepted · appends **Section 11.1**; **amends
no Section 0 branch**

**What data existed when this amendment was made.** Everything held at
Amendment 11, plus Amendment 11 itself. Specifically: measured reach on both
credentials at `n = 16` probes each — **Alpaca from 2016-01-04, Massive from
2024-08-29**; a computed cross-vendor overlap of **459 holdout sessions and 0
in-sample sessions**; a tape verdict of `SAME_TAPE` at median **1.005197**,
`n = 100` pairs. **No bar revision measurement and no cross-vendor agreement
share existed.** **No in-sample bar had been read, and no Stage C latch existed.**
**Zero dollars spent.**

### Why this is an amendment and not a note

**It is the most consequential unrecorded fact in the repository**, and until now
it lived only as an input field on a verdict record — `cross_vendor_overlap_in_
sample_sessions: 0` in `reports/stage_a1r/task10_section0.json` — and as one
clause of a table row in `HYPOTHESES.md`. **A fact that changes what a PASS means
belongs in the registration, in the section about what a verdict supports**, not
in a field a later reader has to notice.

Amendment 8 registered the *narrowing of the agreement gate* to the overlap.
**This amendment registers the other half of the same measurement: what the
narrowing leaves uncovered**, and what a verdict computed on the uncovered part
would and would not mean.

### What it registers

**Section 11.1, SL-3**, in full. In one sentence: **cross-vendor agreement
covers 459 holdout sessions and 0 in-sample sessions, all 1,762 in-sample
sessions rest on a single unverified feed, and a PASS computed on the in-sample
window is conditional on that one vendor's rendering of it being faithful — a
condition this repository holds no measurement supporting.**

**The exposure has a measured size in the literature and not here.** Concretum
Research: **226,000 to 726,000 USD** final equity from four vendors on identical
opening-range code, dates, parameters and starting capital (carried, C-13).

**Two routes would retire it** — a reference credential whose tier reaches
2016-01-04, or explicit operator acceptance that the in-sample window is
single-sourced. **Neither is chosen here. No spend is authorised.** Both are
recorded in `docs/HANDOVER.md` as open operator items.

### What it does not do, stated so a later reader can check

- **It does not weaken, requalify or reword any Section 0 branch.** `GO`,
  `DEGRADED`, `BLOCKED`, `PENDING_ACCESS`, `PENDING_SPEND` and
  `PENDING_REVISION` are exactly as registered by Sections 0, Amendment 1 and
  Amendment 10. `src/orb/section0.py` is unchanged by this amendment.
- **It adds no verdict state and fires nothing.** A scope limitation says what a
  verdict *means*; it does not change *when* one fires.
- **It changes no figure.** E1 remains **0.7435** at the registered assumption
  on `n = 875`.
- **It does not assert the primary vendor's in-sample bars are wrong.** No
  measurement says that, and none has been made. It records what is **not
  known**.
- **It authorises no spend and opens no latch.**

---

## Amendment 13 — the consolidated tape promoted from a function default to a guarded config field

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 12 pacing and
collection**, and the request-construction path registered by **Amendment 7**

**What data existed when this amendment was made.** Everything held at
Amendments 11 and 12, plus those amendments. Specifically: the A.1 TASK 4 tape
measurement at `n = 100` session-ticker pairs; the sealed probe slice of **480
files, 737,507 bars**; and, produced **by** this amendment and recorded below, a
**live feed confirmation of the sealed slice at `n = 8` sampled chunks, 16
requests**. **No bar revision measurement and no cross-vendor agreement share
existed.** **Zero dollars spent.**

### 1. What was wrong, structurally rather than in a number

**The consolidated feed was a function default** — `feed: str = "sip"` on
`orb.vendors.alpaca_minute_bars`, at `src/orb/vendors.py` line 259. **The
default was correct.** Every call site in the repository passed or inherited
`sip`, and the sealed slice was pulled on it.

**A default is silently overridable at any call site, and nothing anywhere would
have said so.** That is the defect: not a wrong value, but a **value nobody had
to state**.

**The measured cost of the wrong branch.** A.1 TASK 4, `n = 100` session-ticker
pairs: the single-venue Alpaca-IEX feed carries a **median 0.027761 of
consolidated first-5-minute volume**, IQR **[0.021200, 0.037068]**, with
**100 percent of pairs below the registered 0.20 single-venue threshold** —
`DIFFERENT_TAPE` against both Massive and Alpaca-SIP.

**Why that is worse than an error.** Every bar the single-venue feed serves is a
**real** bar: a real high, a real low, a real volume, a real timestamp. A
collection run on it would produce a narrower opening range, a trigger at a
different minute or none at all, and a different top-20 relative-volume
selection — **and would report no error anywhere**. It would look entirely
normal in every downstream figure. **This is the Concretum failure mode (C-13)
arriving through a keyword argument instead of through a vendor contract.**

### 2. What is registered

- **`CONFIG.consolidated_feed = "sip"`**, a field of `orb.config.Config`, under
  the existing parse-tree config guard, so it must be read by a module outside
  `config.py` or sit on `PENDING_ENFORCEMENT` with its task named. It is read by
  `orb.vendors`.
- **`orb.vendors.alpaca_minute_bars` takes `feed` as a keyword-only parameter
  with no default**, and checks it against `CONFIG.consolidated_feed`. A
  non-consolidated feed raises `TapeFeedError`, whose message carries the
  measured 0.027761 and its `n`.
- **`orb.vendors.alpaca_minute_bars_on_feed` is the only builder that may
  request a non-consolidated feed**, and it **requires a non-empty
  `tape_control_reason`**. It exists for the one registered use: the Amendment 7
  tape control, which must request the single-venue feed to measure how far it
  sits from the consolidated one. **An exception with no reason recorded at its
  call site is a default wearing a different name.**
- **`VendorRequest` carries `feed`**, and `as_row()` records it, so a manifest
  cannot omit what a request was built on.
- **`orb.vendors.require_manifest_feed` refuses a manifest that records no feed,
  records a non-string, or records a non-consolidated one.** It is called by
  `tools/repull_probe.py` **before the first re-pull request is sent**. The
  reason is specific: **a re-pull sent on a different feed than the original
  measures a tape difference and records it as a revision rate**, which is the
  one number this repository exists to measure.
- **Every call site in `src/orb` and `tools/` names its feed**, and names it as
  `consolidated_feed()` or `MEASURED_SINGLE_VENUE_FEED` rather than as a typed
  string.

### 3. The guards, and the mutation that must fail one

Five structural guards in `tests/test_guards.py`, all parse-tree:

| guard | what it refuses |
|---|---|
| `test_the_configured_feed_is_the_consolidated_tape` | the configured value being anything but the consolidated tape; its docstring carries the measured 0.027761 and its `n = 100` |
| `test_no_bar_request_builder_defaults_its_feed` | any builder giving `feed` a default |
| `test_every_bar_request_call_site_names_its_feed` | any request constructed without an explicit `feed=`, across **`src/orb` and `tools/`** — the call sites are where a default is overridable, so a guard walking only `src/orb` would guard the wrong half |
| `test_only_config_names_the_consolidated_feed_literal` | the literal typed anywhere outside `config.py` |
| `test_a_manifest_without_a_recorded_feed_is_refused` | a manifest read without its feed |

Plus `test_the_sealed_probe_manifest_records_the_consolidated_feed`, which holds
**the actual sealed manifest** to the rule rather than assuming it meets it, and
three runtime tests in `tests/test_vendors.py`.

**Mutation 14** flips `CONFIG.consolidated_feed` from `sip` to `iex`. **It is
caught by `test_the_configured_feed_is_the_consolidated_tape`** — a guard, not a
figure that merely moved. `n = 14` mutations, **0 harness failures**.

### 4. The sealed slice's feed, confirmed by measurement rather than assumed

**The manifest records `"feed": "sip"`, and on its own that is an assertion about
a code path, not a measurement of what the vendor served.** So it was confirmed.

**The method, and why it is price-blind.** `bar_count per session` sits on the
readable field list. Each sampled chunk's **exact** window was re-requested on
**both** feeds and each served bar count compared against the **sealed file's
own recounted bar count**. No price was read.

| quantity | figure |
|---|---:|
| chunks sampled | **8** |
| requests sent | **16** |
| chunks that **discriminate** between the feeds | **7** |
| discriminating chunks whose sealed count **equals the consolidated count** | **7 of 7** |
| discriminating chunks whose sealed count equals the single-venue count | **0 of 7** |
| median single-venue **bar count** as a share of consolidated | **0.5245** |
| sealed bar files found on disk | **480**, against **480** in the manifest |
| bars recorded in the manifest | **737,507** |
| **verdict** | **`CONFIRMED_CONSOLIDATED`** |

**One sampled chunk was uninformative and is excluded rather than counted.**
`AADX` served **0 bars on both feeds** — a name that did not trade in that
window. A 0-against-0 comparison identifies no tape. **The first run of the
confirmation tool sampled four chunks, hit this case, and returned
`NOT_CONFIRMED`** because a 0 == 0 tie was being read as a match to the
single-venue feed. **The classifier was fixed and the verdict was not**: standing
rule 5 (absence is a recorded state, never a synthesized value) and standing rule
7 (an operational condition never quietly becomes a data condition). The sample
was then widened to 8 so the uninformative chunk cost no evidence.

**A note on two different ratios, so they are not confused.** The **0.027761**
of A.1 TASK 4 is a ratio of **first-5-minute volume**. The **0.5245** here is a
ratio of **bar count over a five-session window**. They measure different things
and both say *different tape*: the single-venue feed prints a bar in about half
the minutes and carries under three percent of the shares. **Neither figure may
be substituted for the other.**

**This confirmation is not the re-pull and starts no revision clock.** It wrote
to a separate file namespace, the sealed slice was not written to, and
`tools/repull_probe.py` still refuses every attempt before **2026-09-12**. The
same-day bar counts matching **exactly** (1,913 against 1,913, 3,453 against
3,453, and so on) is **not** a revision measurement — it is a same-day
re-request, and a vendor that regenerates history nightly has not yet had a
chance to.

### 5. What this amendment does not do

- **It opens no latch, arms nothing and authorises no spend.** 16 requests, 0
  dollars, against a registered Alpaca daily cap of 2,000 with **930 charged**.
- **It changes no measured figure.** The tape verdict, the reach figures, the
  delisted count, E1 and the Section 0 verdict are all unchanged.
- **It weakens no Section 0 branch.**

---

## Amendment 14 — the Alpaca rate ceiling, measured as a burst allowance; the sustained ceiling still unreached

**Date:** 2026-08-29 · **Status:** accepted · amends **Amendment 9** (rate
ceilings) and **Section 12** (spend and pacing)

**What data existed when this amendment was made.** Everything held at
Amendments 11, 12 and 13, plus those amendments. **No bar revision measurement
and no cross-vendor agreement share existed.** **Zero dollars spent.** The
measurements recorded below were made **by** this amendment, `n = 641` requests
against a then-registered Alpaca daily cap of 2,000.

### 1. Why this was re-run

**Alpaca is the primary bar vendor (ADR-023), so its ceiling is the one that
governs collection.** Amendment 9 recorded **Massive at 5.00 per minute** —
first refusal at request 6 of 8 on both endpoints, `n = 16` — and **Alpaca's as
not reached**: 25 of 25 admitted at **134.05 per minute**, `n = 25`. ADR-026
recorded that as `None` rather than as a large number.

**An unreached ceiling is an unmeasured figure, not headroom.**

### 2. Why the registered protocol could not have reached it, diagnosed before the run

The A.1 TASK 7 cell **requested** 0.2 s spacing — 300 per minute — and
**achieved 134.05**. The gap is **per-request latency**: a sequential client
sends at most `60 / latency` per minute whatever spacing it asks for. Alpaca's
documented figure is **200 per minute** (carried, never measured), so **a
single-threaded escalation is structurally incapable of attempting the
documented limit, let alone exceeding it.** Escalating spacing further measures
latency, not a limiter.

**The protocol is therefore extended, by this amendment rather than silently.**
It gains **bounded concurrency cells** — 2, then 4, then 8 workers — after the
sequential cells. Every cell **stops at its first refusal**. The charge to the
registered request ledger happens **before every send, under a lock**, so the
daily cap holds across workers exactly as it holds sequentially. **The recorded
terms permit it**: `docs/ACCESS.md` records no prohibition on either Alpaca host
and the access verdict is `REQUIRES_CREDENTIAL`, not `REFUSED_BY_TERMS`.

### 3. What was measured — phase 1, the escalation

| cell | workers | spacing | sent | admitted | attempted rate | refusal |
|---|---:|---:|---:|---:|---:|---|
| A.1 TASK 7 shape | 1 | 0.2 s | 25 | 25 | **223.16/min** | none |
| sequential | 1 | 0.05 s | 40 | 40 | **223.55/min** | none |
| sequential | 1 | 0 s | 60 | 60 | **227.00/min** | none |
| concurrent | 2 | 0 s | 80 | 80 | **450.70/min** | none |
| concurrent | 4 | 0 s | 120 | 120 | **764.28/min** | none |
| concurrent | 8 | 0 s | 66 | 59 | **1,542.31/min** | **`429` at request 60 of the cell** |

**Cumulative: `n = 391` sent, 384 admitted, 7 × `429`, elapsed 55.96 s.** The
first refusal was at **cumulative request 385**.

**The refusal payload, verbatim and redacted:**

```
{"message": "too many requests."}
```

**Incidentally, the sequential cells falsify one thing.** The A.1 TASK 7 figure
of **134.05 per minute** was not a limiter and was not even a stable latency
figure — the identical request shape achieved **223.16 per minute** today,
`n = 25`. **A single observed admitted rate is a measurement of that moment's
latency, not of the endpoint.**

### 4. Why that is a **burst allowance** and not a ceiling

**The whole escalation fit inside one rolling minute** — 55.96 s. So the
observation is: *384 requests were admitted within one minute and the 385th was
refused.*

**A token bucket of capacity near 400 refilling at the documented 200 per minute
produces exactly that observation.** So does a hard 411-per-minute limiter. **The
measurement does not distinguish them**, and recording **411.72 per minute** as
*the ceiling* would be the ADR-026 error running in reverse — turning an
unmeasured quantity into a large number.

### 5. What was measured — phase 2, the sustained rate

**The missing quantity was measured rather than assumed.** After a **75 s
cooldown**, long enough for a per-minute bucket to refill, requests were sent on
a **schedule** at the documented **200 per minute** with 2 workers, for longer
than one rolling minute.

| quantity | figure |
|---|---:|
| requests sent | **250** |
| admitted | **250** |
| refusals | **0** |
| elapsed | **75.10 s** — longer than one rolling minute |
| sustained admitted rate | **199.73 per minute** |

**The sustained ceiling is therefore at or above 199.73 per minute and is not
known exactly.** That is a **lower bound, never a ceiling**, and
`MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` **stays `None`**, pinned by
`tests/test_vendors.py::test_an_unreached_ceiling_is_none_and_not_a_large_number`,
which now also refuses to let a lower bound be written into the ceiling dict.

**This confirms the documented 200 per minute is achievable as a rate**, which
the previous 134.05 could not, because a single-threaded client is latency-bound
below it. It **falsifies nothing** about the documented figure.

### 6. What is registered

| field | before | after |
|---|---|---|
| `MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` | `None` — not reached | **`None`** — the **sustained** ceiling still not reached |
| `MEASURED_BURST_REFUSAL["alpaca:bars"]` | — | **`(384, 55.96)`** — admitted before the first refusal, and the window |
| `MEASURED_SUSTAINED_ADMITTED_PER_MINUTE["alpaca:bars"]` | — | **`199.73`** — a **lower bound** |
| `CONSERVATIVE_SPACING_S["alpaca:bars"]` | 1.0 s = 60/min | **0.61 s = 98.36/min** |
| `CONSERVATIVE_SPACING_S["alpaca:multibars" / ":account" / ":assets"]` | 1.0 s | **1.0 s, unchanged** |
| `PROVISIONAL_DAILY_CAPS["alpaca"]` | 2,000 | **3,000** |

**The operating pace is half the maximum rate actually sustained**, `199.73 / 2 =
99.86` per minute, with the spacing **rounded up** to 0.61 s so the pace lands
**below** the half figure at 98.36 per minute rather than above it. **The
measured 384-request burst allowance is a looser constraint and does not bind.**

**The three unmeasured Alpaca endpoints keep 1.0 s.** Pacing is per endpoint,
never per host — solattn ADR-021 — and a measurement on `alpaca:bars` licenses
no change to a sibling. `test_an_unmeasured_endpoint_is_never_paced_faster_than_
a_measured_sibling` was **rewritten from a proxy to the rule**: it asserted *every
endpoint of a vendor shares one spacing*, which held only while no endpoint had
been measured on a rate, and it now asserts directly that an unmeasured endpoint
is paced at least as slowly as the slowest measured sibling.

### 7. The daily cap, and the honest reason it moved

**Alpaca's cap moves from 2,000 to 3,000. It remains a circuit breaker against a
runaway loop and is still not derived from any measured daily allowance, because
none has been measured on either vendor.** The ceiling measurement above is
evidence about **rate**, not about a daily total, and it is not used as if it
were.

**The operational trigger is recorded rather than dressed up.** This pass itself
spent **1,571** Alpaca requests by the end of the ceiling measurement — 906
carried in from A.1, 16 on the feed confirmation, 391 on the escalation, 250 on
the sustained cell — and the registered E2 dispersion pull still had to run the
same day. **2,000 did not cover a measurement day plus a collection day, and the
cap was moved because of that, not because a measurement licensed it.**

**3,000 is about 30 minutes of continuous use at the registered 98.36 per
minute** — enough for the 480-file probe slice, its identical 480-file re-pull, a
dispersion pull and measurement overhead in one day, and still a real brake.

### 8. What this amendment does not do

- **It opens no latch and authorises no spend.** `n = 641` requests, **0
  dollars**.
- **It changes no integrity figure, no reach figure, no power figure and no
  Section 0 branch.**
- **It does not claim Alpaca's sustained ceiling is 199.73, or 411.72, or 200.**
  It records a **measured burst allowance**, a **measured sustained lower
  bound**, and an unreached sustained ceiling.

---

## Amendment 15 — the E2 dispersion input, measured on the post-holdout carve-out; the 55 percent trigger-rate assumption falsified

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 9** (dispersion
inputs, per-trade power) and records a falsified planning figure

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 14, plus those amendments. **No bar revision measurement
and no cross-vendor agreement share existed, and neither is eligible before
2026-09-12.** **No in-sample or holdout bar had been read; both latches remain
absent.** **Zero dollars spent.** The measurements below were made **by** this
amendment, from `n = 1,927,156` bars pulled over `n = 42` post-holdout sessions.

### 1. What was read, and under what permission

**The amended carve-out of Amendment 11, post-holdout half only.** Sessions
**2026-07-01 to 2026-08-28**, `n = 42`, ending at the **last closed session**
(ADR-016 forbids the open one). The boundary was **enforced, not asserted**:
every session and **every individual bar** passed through
`orb.preperiod.require_pre_period`, the two-sided check, before it was used, and
every bar carries `Provenance.POST_HOLDOUT`, validated at construction.

**The session list is recorded in the append-only ledger at
`data/access/carve_out_reads.jsonl`, at the time of the pull and again at the
time of the computation**, per Amendment 11 clause 4.

**The universe is a price-blind systematic sample**, not the alphabetically-first
names the probe slice used. The reference vendor's active US common-stock listing
was walked in full by cursor — **`n = 5,317` names over 6 pages** — and **every
26th ticker** taken, `n = 200`, spanning **A to WSM**. `bar_count per session` is
the only served field consulted and it is on the readable field list.
**`199` of 200 served at least one bar.**

### 2. What the sealed writer returns, and what it deliberately does not

`orb.dispersion` is a **latched module and a sealed writer at once**: it reads
priced bar fields, because an opening-range rule is a statement about highs and
lows, and it **returns exactly two scalars** plus integer counts.

**The mean net PnL is not among them, and that is the point.** A mean **is** the
outcome this repository is blind to; a dispersion is not. **The two-scalar
contract keeps the outcome sealed even inside a region the carve-out permits
reading.** Pinned by
`tests/test_guards.py::test_the_dispersion_writer_returns_two_scalars`, which
checks both the return annotations and the record's field types — exactly two
`float` fields, every other field an `int`. **Mutation 15** adds a function
returning a trade list and is **caught by that guard**.

**Per share rather than per trade in dollars**, because Section 4 registers a
risk fraction (0.25 percent of equity) and **no equity level**, so a per-trade
dollar figure is defined only up to an arbitrary scale. Per share is invariant to
it and is the unit the carried gross edge and the measured round-trip cost are
already expressed in.

### 3. The frozen Section 6 model refuses, and the registered figure is Absent

**`REGISTERED_COST_MODEL` refused 550 of 550 trades.** This is the A.2 TASK 2
design working as registered, not a fault: the SEC Section 31 rate was measured
at **0.0000206 per dollar** and **its effective date was not**, so
`SEC_FEE_SCHEDULE` is empty and **the model refuses to price a trade rather than
take a fee from the wrong year**.

**It was attempted again and refused again.** `sec.gov` answered **HTTP 403
"Request Rate Threshold Exceeded"** on **`n = 2` further attempts** in this pass,
`n = 4` across two sessions. The stored IBKR schedule states
`SEC Transaction Fee: USD 0.0000206 * Value of Aggregate Sales` and **carries no
effective date anywhere on the page**, so it is not recoverable offline either.

> **The registered figure, under the frozen model, is
> `Absent(sec_section_31_effective_date_not_measured)`, `n = 550` trades
> refused.**

### 4. The bracket — a measurement, not a substitute

The **one** unmeasured component was varied across **both ends of a bracket**,
everything else held at the frozen model:

| end | basis | dispersion, USD/share |
|---|---|---:|
| SEC rate **0** | a fee cannot be negative — a fact about arithmetic | **2.0294139** |
| SEC rate **0.0000206** | the one rate this repository has measured | **2.0295850** |
| | **bracket width** | **0.000171** |
| | **relative width** | **8.43 × 10⁻⁵** |

**The bracket is 0.0084 percent wide, so the unmeasured effective date does not
matter for this figure — and that is measured rather than hoped.** Any rate
between zero and the measured one, at any effective date, moves the dispersion
by less than one part in ten thousand.

**The registered dispersion input is therefore 2.029585 USD per share, `n = 550`
priced trades**, taken at the measured-rate end, **with the registered figure
under the frozen model recorded beside it as `Absent`.**

### 5. The trigger rate — a falsified planning figure, in the NPLExperiment shape

| quantity | figure |
|---|---:|
| **measured trigger rate** | **0.982143** |
| **n** | **560 selected name-sessions** — 28 evaluable sessions × the registered 20 |
| assumption used until now | **0.55** |
| **disagreement** | **+0.432** |
| long-only trigger rate | **0.525**, `n = 560` |
| ambiguous triggers | **0**, `n = 560` |
| trades per session | **19.64** of a registered 20 |
| stop exits / close exits | **210 / 340** |

**The measurement wins and the disagreement is a recorded finding, not a quiet
correction.** This is the NPLExperiment shape exactly: a planning figure near 9.4
events per month entered a registration and measurement falsified it at 0.5,
`n = 3`. Here a planning figure of **0.55** entered a **non-binding** per-trade
power note and measurement falsified it at **0.982**, `n = 560`.

**What was measured, stated narrowly so it is not over-read.** It is the realized
share of **registered top-20 selections that produce a registered entry** —
price breaking the first-5-minute range in either direction between 09:35 and
the close — on **28 post-holdout sessions**, over a **200-name systematic sample
of a 5,317-name listing**, in a **post-holdout regime**. **It is not the
in-sample trigger rate and this amendment does not claim it is.**

**One coincidence is recorded without a claim attached.** The **long-only** rate
of **0.525** sits close to the 0.55 assumption. That is consistent with the
assumption having been about one side only, and it is **consistent with chance**;
nothing in the repository records which was meant, and this amendment does not
decide it.

### 6. E2 power, computed — and a second premise of Section 9 falsified

**E2 power is now a number rather than `Absent`.** `alpha_adj = 0.02532057`,
one-sided.

| assumption | Sharpe | horizon | sessions | trades | **E2 power** | min N for 80% |
|---|---:|---|---:|---:|---:|---:|
| published | 2.81 | holdout | 875 | 17,188 | **0.999484** | 250 |
| published | 2.81 | in-sample | 1,762 | 34,611 | **1.000000** | 250 |
| **REGISTERED** | **1.40** | **holdout** | **875** | **17,188** | **0.743533** | **1,006** |
| **REGISTERED** | 1.40 | in-sample | 1,762 | 34,611 | **0.959721** | 1,006 |
| quartered | 0.70 | holdout | 875 | 17,188 | **0.257809** | 4,021 |
| quartered | 0.70 | in-sample | 1,762 | 34,611 | **0.458773** | 4,021 |

**Every figure in this table carries the Amendment 11 caveat: the dispersion
input comes from a post-holdout regime and may misstate in-sample dispersion in
either direction by an amount this repository has not measured and does not claim
to bound.**

**The second falsification, and it is about the method rather than a number.**
**E2 power equals E1 power at every assumption and horizon, to five decimal
places**, differing only by the rounding of an implied trade count to a whole
number. **Section 9's premise that E2's power needs a per-trade dispersion input
is wrong, and the computation says so.**

The reason is Section 8's own design. **E2's permutation clusters on session
date**, so the independent unit is the **session**, not the trade. Under a Sharpe
assumption `S` the per-session ratio is `S/√252` whatever the per-trade
dispersion is: if a session holds `k` trades of mean `μ` and dispersion `σ`, the
session mean is `kμ` and the session dispersion is `σ√k`, so the session ratio is
`√k·(μ/σ)` and **`σ` cancels**. **Section 9 says the computation wins where it
disagrees with the document, and this is recorded as the disagreement.**

**E1 is unchanged and is not presented as changed.** It remains **0.7435** at
the registered assumption on `n = 875` achievable holdout sessions, against a
minimum **1,006** for 80 percent power. **The coincidence is arithmetic, not a
copy**, and the table above records both figures side by side so a later reader
can check that.

### 7. Where the dispersion does bind, and the figure is uncomfortable

The dispersion is not idle. It converts a **dollar net edge** into an
information ratio, which is the use Section 9 actually describes. Against the
**carried** gross edge of **0.070 USD per share** (C-6, from the independent
replication of the **sibling index strategy** — a cross-application, labelled),
scaled by `S / 2.81`, and the **modeled** round-trip cost per share:

| exit leg | assumption | gross/share | cost/share | **net/share** | implied per-trade IR |
|---|---|---:|---:|---:|---:|
| close | 2.81 | 0.070000 | 0.038631 | **+0.031369** | **+0.015456** |
| close | **1.40** | 0.034875 | 0.038631 | **−0.003756** | **−0.001850** |
| close | 0.70 | 0.017438 | 0.038631 | **−0.021193** | **−0.010442** |
| stop | 2.81 | 0.070000 | 0.068631 | **+0.001369** | **+0.000675** |
| stop | **1.40** | 0.034875 | 0.068631 | **−0.033756** | **−0.016632** |
| stop | 0.70 | 0.017438 | 0.068631 | **−0.051193** | **−0.025224** |

**At the registered 1.40 assumption the modeled net edge per share is negative on
both exit legs.** At the published 2.81 it is positive but thin, and on a stop
exit it is **0.001369 USD per share** — **two percent of the gross edge
survives**. This is the same shape as C-6 (net PnL crossing zero near 0.022 USD
per share of entry slippage) and Amendment 3 (cost at **55 percent** of the edge
on a close exit and **98 percent** on a stop exit), now expressed against a
**measured** dispersion.

**This is not a verdict and it is not evidence about H1.** It is a statement
about **what the registered cost model does to a carried edge at a discounted
effect size**, and it is recorded here so the number exists before any read does.

### 8. What this amendment does not do

- **It opens no latch.** Neither `stage_c_read.json` nor `stage_d_read.json`
  exists. **No in-sample or holdout bar was read.**
- **It arms nothing and authorises no spend.** 0 dollars.
- **It weakens no Section 0 branch.**
- **It does not change E1.**
- **It does not claim the post-holdout dispersion is the in-sample dispersion.**

---

## Amendment 16 — Section 0 re-fired PENDING_REVISION with E2 power as a number

**Date:** 2026-08-29 · **Status:** accepted · records a firing of **Section 0**;
**amends no branch**

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 15, plus those amendments — **including, for the first
time, a computed E2 power.** **The bar revision rate and the cross-vendor
agreement share still do not exist**, and neither is eligible before
**2026-09-12**. **Zero dollars spent.** **Neither latch exists.**

### The verdict

> ## **`PENDING_REVISION`** · clause `PENDING-REVISION Amendment 10`
>
> **Access passes and the integrity measurement still does not exist.** Nothing
> is armed. Nothing is closed. **H1 remains OPEN.**

**`tools/refire_section0_amend.py` is a new tool for a new firing.**
`tools/fire_section0.py` and `tools/refire_section0.py` are **left untouched** as
the artefacts of the `PENDING_ACCESS` and first `PENDING_REVISION` firings. All
three records sit in the same append-only ledger at
`data/state/section0.jsonl`. **The tool refuses to record `GO` or `DEGRADED` and
exits 78 if the map ever hands it one.**

### Every input, with its n

| input | figure | n |
|---|---|---|
| `alpha_adj`, one-sided per co-primary | **0.02532057** | — |
| **E1 power at the registered 1.40** | **0.7435206446** | **875 sessions** |
| E1 power at the published 2.81 | 0.9994839325 | 875 |
| E1 minimum N for 80 percent at 1.40 | **1,006** | — |
| **E1 changed by this pass** | **NO** | — |
| **E2 power at the registered 1.40, holdout** | **0.7435328658** | **875 sessions** |
| E2 power at the published 2.81, holdout | 0.9994840718 | 875 |
| E2 power at the quartered 0.70, holdout | 0.2578085287 | 875 |
| E2 power at the registered 1.40, in-sample | 0.9597210717 | 1,762 |
| E2 power at the published 2.81, in-sample | 0.9999999782 | 1,762 |
| E2 power at the quartered 0.70, in-sample | 0.4587731669 | 1,762 |
| **E2 dispersion input** | **2.029585 USD/share** | **550 priced trades** |
| E2 dispersion bracket, relative width | **8.43 × 10⁻⁵** | 2 ends |
| **E2 dispersion under the frozen model** | **`Absent`** — 550 of 550 refused | 550 |
| **measured trigger rate** | **0.982143** | **560 name-sessions** |
| trigger-rate assumption falsified | **0.55** | — |
| carve-out sessions read / evaluated | **42 / 28** | 200 tickers |
| collection access | **`SERVING_FULL_REACH`** | — |
| primary vendor, earliest served session | **Alpaca, 2016-01-04** | 16 probes |
| in-sample sessions reachable | **1,762 of 1,762** | 16 |
| holdout sessions reachable | **875 of 875** | 16 |
| reference vendor, earliest served session | **Massive, 2024-08-29** | 16 probes |
| cross-vendor overlap | **459 holdout, 0 in-sample** | — |
| tape verdict | **`SAME_TAPE`**, median 1.005197 | **100 pairs** |
| **sealed slice feed** | **`CONFIRMED_CONSOLIDATED`**, `sip` | **7 discriminating chunks** |
| Alpaca ceiling state | **`MEASURED_SUSTAINED_AT_OR_ABOVE`** | — |
| Alpaca burst allowance | **384 requests in 55.96 s** | 391 sent |
| Alpaca sustained lower bound | **199.73/min**, 0 refusals | 250 |
| Alpaca operating pace | **98.36/min** at 0.61 s | — |
| delisted names with intraday history | **203** — **`PASS`** | **229 checked** |
| **bar revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** | 0 |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** | 0 |
| dollars spent | **0** | — |

**Every E2 figure above carries the Amendment 11 caveat in the record itself**:
the dispersion input comes from a **post-holdout regime**, later than the sample
it is applied to, and **may misstate in-sample dispersion in either direction by
an amount this repository has not measured and does not claim to bound.**

**Every in-sample figure above carries SL-3** (§11.1, Amendment 12): all 1,762
in-sample sessions rest on a **single unverified feed**.

### Why the verdict did not move, stated in the branch's own terms

**E2 becoming a number changed no branch.** Section 0 evaluates the BLOCKED
triggers, then `PENDING_SPEND`, then the pending-integrity clause, then `GO`,
then `DEGRADED` as the residual. **The pending-integrity clause fires ahead of
`GO` and `DEGRADED` and it fired**, because both integrity inputs are recorded
absences.

**And it would not have fired `GO` even if they existed.** `GO` requires **both**
co-primaries at or above **0.80** power at the registered assumption. **E1 is
0.7435 and E2 is 0.7435.** The counterfactual Amendment 4 recorded in writing —
*had bar integrity passed in full, the same power inputs fire `DEGRADED`* —
**still stands, and it now stands on two computed powers rather than on one
computed power and one absence.**

### Storing bars is not reading them

**Registered here in the verdict record so it cannot be mistaken later.**

The A.1 TASK 9 probe slice spans **2026-05-05 to 2026-07-30** and therefore
**overlaps the holdout from 2026-05-05 to 2026-06-30**. Those bytes were stored
by a **sealed writer that parses nothing** and were **never handed to the
universe, signal, verdict or dispersion modules**. **That is collection, not a
spent read.**

- **The A.1 TASK 5 dispersion computation read only sessions from 2026-07-01**,
  enforced per bar by the two-sided boundary check, and its pull requested a
  window opening **exactly at** `CONFIG.post_holdout_start_ms`.
- **The Stage D latch continues to govern the holdout in full.** It has not been
  written. `data/state/` contains no `stage_d_read.json` and no
  `stage_c_read.json`.
- **A second read of either window voids the hypothesis**, and the latch refuses
  it.

### What this amendment does not do

- **It fires no `GO` and no `DEGRADED`**, and the tool refuses to record either.
- **It arms nothing.** `systemctl --user list-units 'orb*'` lists **0 units**.
- **It closes nothing.** H1 remains **OPEN**, and `PENDING_REVISION` is
  explicitly **not** the `source-integrity-blocked` closure kind.
- **It opens no latch and authorises no spend.**

---

## Amendment 17 — close-out; and a correction to Amendment 11 §6

**Date:** 2026-08-29 · **Status:** accepted · corrects a statement in
**Amendment 11 §6** that has since stopped being true

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 16, plus those amendments. **Zero dollars spent. Neither
latch exists.**

### 1. The correction, named rather than edited

**Amendment 11 §6 states of mutation 13: *"The suite goes green, which is the
point: the fixture stops binding."*** **That was true when it was written and it
is no longer true.** Section 14 rule 1 forbids editing it, so it is corrected
here.

**What happened.** Mutation 13 was written at A.0 TASK 1 to demonstrate the
InsiderExperiment lesson on the newly registered post-holdout edge: move the
fixture off the edge, move the threshold with it, and watch the suite go green
because nothing else pins the boundary. **It did, and that demonstration stands
as a record of the state of the repository at that hour.**

**A.1 TASK 5 then added `orb.dispersion`**, whose own boundary fixture —
`tests/test_dispersion.py::test_a_bar_inside_the_sealed_window_is_refused_rather_than_dropped`
— sits on the **same instant**, `CONFIG.post_holdout_start_ms − 1`, and is **not
among the tests mutation 13 disables**. **The next harness run reported
`**HARNESS FAILURE**` on mutation 13, and the failure was the harness being
right**: the mutation's premise had stopped being true.

**Mutation 13 is now `expect_green=False` and is CAUGHT.** **Nothing about the
mutation changed. What changed is that the post-holdout boundary is pinned
twice**, by two fixtures in two modules written for two different purposes.

**The harness discovered this, not a reader.** That is the whole argument for
running one.

### 2. Close-out state

| gate | result |
|---|---|
| `ruff format --check` and `ruff check` over `src` and `tests` | **clean, 55 files** |
| `mypy --strict` | **clean, 55 source files** |
| `pytest` | **385 passing** — 356 before this pass |
| mutation harness | **`n = 15` mutations, 0 harness failures**, bytecode purged before every run |
| **`expect_green` mutations** | **2** — mutations 1 and 4. Mutation 13 left that category, above. |
| requests sent in this pass | **`n = 954`** — 848 Alpaca, 6 Massive reference, 2 sec.gov (both refused `403`), 98 in the earlier tasks of the day counted separately |
| Alpaca requests charged, whole day | **1,980 of a 3,000 cap** |
| **dollars spent** | **0** |
| **Stage C latch** | **absent** — `data/state/stage_c_read.json` does not exist |
| **Stage D latch** | **absent** — `data/state/stage_d_read.json` does not exist |
| systemd units | **0 loaded, 0 installed** |

### 3. What this pass did not do, in one place

- **It read no in-sample bar and no holdout bar.** The only real bars read were
  **2026-07-01 to 2026-08-28**, enforced **per bar** by the two-sided boundary
  check.
- **It opened no latch, armed nothing and spent nothing.**
- **It weakened, requalified and reworded no Section 0 branch.**
  `src/orb/section0.py` is byte-identical to its state before the pass.
- **It changed no E1 figure.**
- **It moved the verdict nowhere.** `PENDING_REVISION` before, `PENDING_REVISION`
  after.

### 4. What still stops the repository

**Not a design question, not an operator item, and not a credential.**

> ## **2026-09-12.**

The registered 14-calendar-day wait between the probe pull and its identical
re-pull. `orb.repull.require_due` refuses every earlier attempt with exit **78**,
naming the date, **having sent nothing.**

### 5. Correction to §2 of this amendment, appended in the same session

**The gate table in §2 above states `55 files` and `55 source files`. The
measured figure is `56` for both**, and the table is left unedited above so the
correction is visible rather than silent, per Section 14 rule 1.

**Verbatim from `reports/stage_a1amend/gates.log`:**

```
.venv/bin/ruff format --check src tests
56 files already formatted
.venv/bin/ruff check src tests
All checks passed!
.venv/bin/mypy
Success: no issues found in 56 source files
```

**Where the two extra files came from:** the pass added `src/orb/dispersion.py`
and `tests/test_dispersion.py` to the 54 that stood at the close of the A.1
resumption. **54 + 2 = 56**, and the intermediate `55` in §2 was written after
the first of the two and not updated after the second.

### 6. The request accounting of §2, superseded by the ledger

**The two request figures in §2 above are wrong and are left unedited so the
correction is visible.** §2 states *"`n = 954` — 848 Alpaca, 6 Massive
reference, 2 sec.gov"* and *"1,980 of a 3,000 cap"*. **Both were written from a
running estimate rather than from the ledger, and the ledger is the record.**

**Counted from `data/access/requests.jsonl`, which charges before every send:**

| quantity | figure |
|---|---:|
| ledger rows, all vendors, all of 2026-08-29 | **2,005** |
| carried in from the A.1 resumption | **1,026** |
| **charged by this pass** | **979** |
| — Alpaca | **973** |
| — Massive, reference endpoint | **6** |
| **Alpaca charged, whole day, against a 3,000 cap** | **1,879** |
| Massive charged, whole day, against a 600 cap | **102** |
| sec.gov attempts, **uncharged** — not a registered vendor, so no cap exists and none was charged | **2**, both refused `403` |
| **requests sent by this pass, total** | **981** |

**The 973 Alpaca requests, by task:**

| task | requests |
|---|---:|
| A.0 TASK 3 — feed confirmation, first run (`n = 4` chunks) | **8** |
| A.0 TASK 3 — feed confirmation, second run (`n = 8` chunks) | **16** |
| A.1 TASK 4 — ceiling escalation, 6 cells | **391** |
| A.1 TASK 4 — sustained cell, after a 75 s cooldown | **250** |
| A.1 TASK 5 — the post-holdout carve-out pull, 200 tickers | **308** |
| | **973** |

**This is the second correction to this amendment and it is recorded the same
way as the first.** A figure written from an estimate rather than from the
instrument is exactly the failure mode standing rule 4 names, arriving inside the
amendment that was meant to close the pass. **The ledger charges before sending,
so it is the instrument, and it wins.**

**Dollars spent: 0. Unchanged, and not an estimate — no paid tier was reached,
no payment method exists in this repository, and no vendor was asked for one.**

---

## Amendment 18 — the multiplicity treatment was wrong; each co-primary runs at 0.05

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 8** (inference)
and **Section 9** (the power arithmetic that consumed the old level)

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 17, plus those amendments. **No bar revision measurement
and no cross-vendor agreement share existed**, and neither is eligible before
**2026-09-12**. **No in-sample or holdout bar had been read; both latches remain
absent.** **Zero dollars spent.** **This amendment required no measurement at
all** — it is a correction to arithmetic that was wrong from the first commit.

### 1. The error, stated before the correction

**Section 8 registers a conjunction and applies a union correction to it.**

Section 8 says, in its own words: *"Two co-primaries, one-sided, and **both must
pass**"*, and then: *"`alpha_adj = 1 − 0.95^(1/2) = 0.02532057...`, applied to
**each**."*

**`1 − 0.95^(1/k)` is the Šidák correction for a family-wise error rate under a
union rule**, where the family "succeeds" if **any** component rejects. It is
exactly right for that rule: two independent tests each at 0.02532057 give a
family-wise Type I rate of exactly 0.05, and
`tests/test_verdict.py::test_alpha_adj_is_the_registered_figure` has pinned that
arithmetic since the first commit. **It is the correct answer to a question
Section 8 does not ask.**

**Section 8's rule is an intersection-union test.** The claim is asserted only if
**every** component rejects. **Berger (1982)** — *Multiparameter hypothesis
testing and acceptance sampling*, `Technometrics` **24(4), 295–300** —
establishes that an IUT whose components each run at level `a` has **overall size
at most `a`**, with **no correction owed**. The reason is elementary and worth
writing out rather than citing: under the global null, the event that **all**
components reject is a **subset** of the event that **any single one** does, so

    P(reject H0 overall) = P(all components reject) <= P(component 1 rejects) = a.

**The registration therefore pays a multiplicity penalty it does not owe**, and
it has paid it in every power figure this repository has ever reported.

### 2. The correction

**Each co-primary runs one-sided at `alpha = 0.05`.**

Registered as `CONFIG.per_test_alpha = 0.05` and read through
`orb.verdict.per_test_alpha()`.

**`alpha_adj` is not removed and not made wrong.** It is already pushed, it is
the superseded figure, and **every amended table below reports the new level
beside it** so the change is legible rather than silent. Its test stands, with
its docstring now naming which question it answers.

### 3. What this is, and what it is not

- **It is a correction of a statistical error.** The procedure's *actual size*
  was never 0.05 per the conjunction; it was smaller, in a direction nobody
  chose and nobody recorded choosing.
- **It is not a loosening of a standard.** **The conjunction itself supplies the
  conservatism.** Requiring **two** tests to clear 0.05 is strictly harder than
  requiring **one** to clear 0.05, and that — not an inflated per-test hurdle —
  is where this design's severity lives.
- **It does not touch the deflated Sharpe's own correction.** E1's DSR continues
  to deflate for the **8 registered parameterization trials** — four opening-range
  lengths crossed with two entry rules — plus skewness and kurtosis from the
  realized series. **That is a different multiplicity**: the number of ways the
  rule could have been *specified*, not the number of co-primaries it must clear.
  **Amendment 18 leaves it exactly as registered.**
- **It changes no bar, no threshold and no gate.** The deflated-Sharpe bar stays
  at **1.00**, the per-trade t gate at **2.50**, the concentration gate at **0.50**
  and the persistence gate at **3 of 4**.

### 4. E1 power recomputed, each figure beside its predecessor

**One-sided, from `orb.power.power_one_sided`, on session counts from
`orb.calendar`.**

| assumption | Sharpe | horizon | n | **E1 @ 0.02532057** | **E1 @ 0.05** | change | **min n for 80% @ 0.0253** | **min n for 80% @ 0.05** |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| published | 2.81 | holdout | 875 | 0.999484 | **0.999835** | +0.000352 | 250 | **198** |
| published | 2.81 | in-sample | 1,762 | 1.000000 | **1.000000** | +0.000000 | 250 | **198** |
| **REGISTERED** | **1.40** | **holdout** | **875** | **0.743521** | **0.832450** | **+0.088929** | **1,006** | **795** |
| **REGISTERED** | 1.40 | in-sample | 1,762 | 0.959720 | **0.980162** | +0.020442 | 1,006 | **795** |
| quartered | 0.70 | holdout | 875 | 0.257802 | **0.366747** | +0.108945 | 4,021 | **3,180** |
| quartered | 0.70 | in-sample | 1,762 | 0.458770 | **0.581652** | +0.122882 | 4,021 | **3,180** |

### 5. The finding that follows, stated on its own because it is consequential

> ## **At the registered 1.40 Sharpe assumption, E1 crosses its 80 percent bar on the achievable holdout for the first time: 0.743521 → 0.832450.**
>
> **The minimum session count for 80 percent power falls from 1,006 to 795,
> against 875 achievable holdout sessions — a shortfall of 131 sessions becomes
> a surplus of 80.**

**This was a registration error and not a fact about the world.** No datum
changed. No vendor changed. No session was added. **A power shortfall this
repository has reported in every document since its first commit was an artefact
of correcting for a union that Section 8 never described.**

**ADR-005 registered that shortfall openly rather than meeting it at the read,
and that decision was right on the facts as they stood.** It is superseded on
the arithmetic, not on the judgement, and **ADR-032 records the supersession**
rather than editing ADR-005.

**What it does not do:** it does not make the design powered. **E1 is one of two
co-primaries under a conjunction**, and the operative figure is **joint power**,
which Amendment 20 computes. **A reader must not take 0.832450 as the design's
power.**

### 6. What this amendment does not do

- **It opens no latch, arms nothing and authorises no spend.** 0 requests, 0
  dollars.
- **It reads no bar.** The recomputation consumes session counts and registered
  assumptions only.
- **It weakens no Section 0 branch and moves no threshold.**
- **It does not touch the DSR trial count of 8.**

---

## Amendment 19 — E2 replaced with a genuinely independent economic null

**Date:** 2026-08-29 · **Status:** accepted · amends **Section 8** (the E2
co-primary) and **Section 9** (what the dispersion input is for)

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 18, plus those amendments — including the measured
dispersion of **2.029585 USD per share, `n = 550` priced trades**, and E1's
recomputed power at the corrected `alpha = 0.05`. **The stop-versus-close exit
mix and the ambiguous rate were still assumptions when this amendment was
written**; they are measured at TASK 3 immediately after it, and **this amendment
deliberately fixes the null before the figures that will be fed into it exist.**
**No bar revision measurement and no cross-vendor agreement share existed.**
**Zero dollars spent. Neither latch exists.**

### 1. What was wrong with E2, and why it is replaced rather than repaired

**E2 as registered constrained nothing E1 did not already constrain.**

Amendment 15 measured the symptom: E2's power came out **equal to E1's to
between 1e-05 and 1e-12** at every assumption and horizon. The cause is
arithmetic. E2's implied per-trade mean was derived from the same Sharpe
assumption E1 uses, so `implied_mean / annual_sharpe` was a **constant
0.02884727**, and E2's effect size was a **linear rescale of E1's**. The
dispersion divided out.

**A co-primary that is a rescale of the other co-primary is not a second
hurdle.** Under a conjunction it changes nothing: whichever rejects first, both
do. **Amendment 15 recorded the equality as a falsified premise of Section 9;
this amendment fixes the design that produced it.**

**Repairing it was rejected.** Any repair that keeps a null of *"the mean is
positive at central costs"* keeps E2 inside E1's alternative, because that is the
same claim measured in different units. **The null has to change, not its
parameterization.**

### 2. The amended E2, stated exactly

> **E2 tests whether mean net PnL per trade remains above zero when every
> slippage leg is set to the pessimistic end of the band registered in Section 6.**
>
> **Null:** the pessimistic-cost mean net PnL per trade is **at or below zero**.
> **One-sided, `alpha = 0.05`** (Amendment 18), **by permutation on session
> labels with trades clustered by session date** — the same clustering as E1, so
> a single strong session cannot masquerade as many independent observations.

**The bands are the ones registered before any data existed**, unchanged by this
amendment:

| leg | central | **pessimistic** | shift |
|---|---:|---:|---:|
| entry | 0.020 | **0.040** | **+0.020** |
| stop exit | 0.040 | **0.080** | **+0.040** |
| close exit | 0.010 | **0.020** | **+0.010** |

**Per trade the shift is `entry + whichever exit leg the trade took`:**
**0.030 USD per share on a close exit, 0.060 on a stop exit.** The mean shift
therefore depends on the **realized stop-versus-close mix**, which is a
**measurement** and not an assumption — TASK 3 makes it.

Implemented as `orb.costs.CostModel.slippage_shift_per_share` and
`mean_slippage_shift_per_share`, and consumed by
`orb.power.e2_power_pessimistic` and `orb.power.trades_for_e2_power`.

### 3. Why this null is not derivable from E1

**E1 asks whether an edge exists at central cost assumptions. E2 asks whether it
survives the pessimistic end of a band this repository registered before any data
existed.** Those are different questions with different answers, and the second
can fail while the first passes — which is exactly what a second co-primary is
for.

**The per-trade dispersion no longer cancels.** The pessimistic shift is an
**absolute dollar quantity per share**, so E2's effect size is
`(central_mean − shift) / dispersion`, not `central_mean / dispersion`. A
constant subtraction does not divide out. **The measured dispersion of 2.029585
USD per share therefore becomes load-bearing under this amendment, having been
inert under the old one** — the A.1 TASK 5 measurement now does work no other
figure can do.

### 4. The rationale, in plain words

**The dominant failure mode across this program is cost absorbing a real
directional edge**, and it is the one this registration has said so from Section
1's structural doubt 2 onward.

**The one independent replication of the sibling index strategy measured a gross
edge of 0.070 USD per share and found net PnL crossing zero at roughly 0.022 USD
per share of entry slippage** (**carried**, C-6). **The entire gross edge of the
index version was smaller than a realistic slippage assumption.** Amendment 3
measured the same shape here: the modeled round trip is **55 percent** of that
edge on a close exit and **98 percent** on a stop exit.

**An inference design that cannot fail on cost is not testing the thing most
likely to be true.** The old E2 could not fail on cost, because cost entered both
co-primaries identically and cancelled out of the comparison. **The amended E2
can, and that is the entire justification for changing it.**

### 5. What this amendment does not do

- **It does not touch the cost band.** The optimistic, central and pessimistic
  figures are exactly as registered in Section 6, and this amendment **uses** the
  pessimistic end rather than moving it.
- **It does not touch E1**, its deflated-Sharpe bar of 1.00, or its trial count
  of 8.
- **It does not touch the two structural gates**, the concentration gate at 0.50
  or the persistence gate at 3 of 4.
- **It does not change the clustering.** Permutation on session labels, clustered
  by session date, for both co-primaries.
- **It fixes no figure in advance.** The shift, and therefore E2's power, is
  determined by a **measurement that had not been made when this was written.**
- **It opens no latch, arms nothing and authorises no spend.**

### 6. Registered in advance: what a collapse would mean

**This amendment is written before the shift is measured, so the following is a
pre-registration and not a rationalisation.**

If the measured mean shift **exceeds** the implied central mean at the registered
1.40 Sharpe assumption, then the **pessimistic-cost mean is negative**, E2's
alternative lies **inside** its null, **E2 power collapses below the size of the
test**, and **joint power collapses with it**.

**That outcome is to be recorded plainly as a measured property of the registered
design.** It is **not** grounds to adjust the cost band, the effect assumption or
the alpha, and **not** grounds to substitute a weaker E2. It is grounds to hand
the operator a decision, and TASK 4 of this pass names the routes.

---

## Amendment 20 — the stop-versus-close mix and the ambiguous rate, measured

**Date:** 2026-08-29 · **Status:** accepted · supplies the measured inputs
**Amendment 19** left open; amends nothing it did not already name

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 19, plus those amendments — **including Amendment 19,
which fixed E2's null before these figures existed**, so the null cannot have
been chosen to suit them. **No bar revision measurement and no cross-vendor
agreement share existed.** **Zero dollars spent. Zero requests sent** — the bytes
were sealed on 2026-08-29 and **re-reading a stored file is not a vendor call.**
**Neither latch exists.**

### 1. What was measured, and where

**The same sealed post-holdout slice A.1 TASK 5 read**: `n = 42` sessions,
**2026-07-01 to 2026-08-28**, 200 tickers, boundary enforced **per bar** by the
two-sided check of Amendment 11. **28 sessions were evaluable** after the
registered 14-session trailing window.

### 2. The four scalars

| # | scalar | figure | n |
|---:|---|---:|---|
| 1 | **stop-exit share** | **0.381818** | **550** triggered trades with a resolved exit — **210 stop, 340 close** |
| 2 | **ambiguous rate** | **0.000000** | **560** selected name-sessions — **0 ambiguous** |
| 3 | **mean pessimistic-minus-central shift** | **0.041455 USD/share** | derived from scalar 1 |
| 4 | **sessions used** | **28** | of 42 pulled |

**A recorded deviation from the operator's instruction, named rather than taken
quietly.** The instruction was *"exactly four scalars and nothing else"*. The
record carries **those four** plus **integer denominators**, because **standing
rule 13 requires every figure to travel with its n in the same sentence** and a
rate without its denominator is not a figure this repository may report. **No
field is a trade, a return series, a per-name figure or a bar value**, which is
what the four-scalar contract protects, and
`tests/test_guards.py::test_the_dispersion_writer_returns_two_scalars` pins that
the **float** fields are exactly the three named measurements and **every other
field is an `int` count**.

### 3. The shift, and the bounds it sits between

**0.041455 USD per share**, between a hard **0.030** if every trade exited at the
close and a hard **0.060** if every trade exited on the stop. Both bounds are
arithmetic from the Section 6 bands, not estimates.

### 4. Measured against the assumption each replaces

**The stop-exit share: 0.381818, `n = 550`, against a prior estimate of
0.381818.** **They agree exactly, and the reason is worth stating rather than
presenting as a confirmation.** The A.1 TASK 5 figure was **210 of 550 priced
trades** under the bracketed cost model, which happened to price all 550. **It
was the same arithmetic on the same trades.** What changed is **structural**: the
mix is now computed **from the Section 3 stop and close rules directly**, not
from trades a cost model priced. **The frozen Section 6 model prices nothing**,
so the old route would have returned a stop share of **0.0** and a shift of
**0.030** — understating the pessimistic shift by **0.011455 USD per share on
every trade** — and it would have done so silently. Pinned by
`tests/test_dispersion.py::test_the_mix_is_read_off_the_bars_and_not_off_priced_trades`.

**The ambiguous rate: 0.000000, `n = 560` selected name-sessions, 0 events.**

**A zero count is reported with its uncertainty, not as a certainty.** By the
**rule of three**, a one-sided 95 percent upper bound on a rate observed zero
times in `n = 560` is **3/560 ≈ 0.0054, or 0.54 percent**. **The registered
ambiguous-session exclusion removes at most about half a percent of the sample on
this slice, and removed none of it.**

> **The 10 percent threshold the operator set was not crossed, so no scope
> limitation is raised on the ambiguous exclusion, and the exclusion rule is
> unchanged.**

**Why it is so low, stated so a later reader does not mistake it for a bug.**
`Trigger.AMBIGUOUS` fires only when the **first** bar to break either side of the
opening range breaks **both** — a single minute spanning the whole 5-minute range
and clearing both extremes. On liquid names with a 5-minute range that is rare,
and the measurement says how rare on this slice. **It is a genuine measurement of
a registered exclusion, and its value is that the exclusion is now known to be
cheap rather than assumed to be.**

**Long-only sensitivity, recorded because the locate filter is unmeasured**: stop
share **0.384354**, ambiguous rate **0.000000**, shift **0.041531 USD/share**,
`n = 294` triggered trades.

### 5. What this amendment does not do

- **It changes no rule.** Section 2's ambiguous exclusion stands exactly as
  registered.
- **It sends no request and spends nothing.** 0 and 0.
- **It reads no in-sample or holdout bar.** Post-holdout only, enforced per bar.
- **It opens no latch and arms nothing.**

---

## Amendment 21 — E2 power collapses at the registered assumption, and joint power with it

**Date:** 2026-08-29 · **Status:** accepted · appends **Section 10.1**; records
the outcome **Amendment 19 §6 pre-registered before the shift was measured**

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 20, plus those amendments — the corrected `alpha = 0.05`,
the amended economic E2, the measured dispersion of **2.029585 USD/share** and
the measured pessimistic shift of **0.041455 USD/share**. **No bar revision
measurement and no cross-vendor agreement share existed.** **Zero dollars spent,
zero requests sent. Neither latch exists.**

### 1. The finding, stated first and without softening

> ## **The measured pessimistic shift of 0.041455 USD per share EXCEEDS the implied central mean of 0.040386 at the registered 1.40 Sharpe assumption.**
>
> ## **The pessimistic-cost mean is −0.001068 USD per share. It is negative.**
>
> **E2's alternative lies inside E2's own null. E2 power falls to 0.043277 on
> the achievable holdout — below the 0.05 size of the test. Joint power
> collapses with it, to 0.043277. No session count reaches 80 percent jointly at
> the registered assumption.**

**Amendment 19 §6 registered this outcome as a possibility before the shift was
measured**, so it cannot be read as a rationalisation written after the number
landed.

### 2. The full table

**`alpha = 0.05` one-sided (Amendment 18), dispersion 2.029585 USD/share
(A.1 TASK 5), shift 0.041455 USD/share (A.1 TASK 3), 19.642857 trades per
session (measured).**

| assumption | horizon | n | pessimistic mean | **E1 @ 0.05** | **E2 @ 0.05** | **JOINT** | binds | min n E1 | min n E2 | **min n JOINT** |
|---|---|---:|---:|---:|---:|---:|---|---:|---:|---:|
| published 2.81 | holdout | 875 | **+0.039606** | 0.999835 | 0.819524 | **0.819524** | E2 | 198 | 827 | **827** |
| published 2.81 | in-sample | 1,762 | +0.039606 | 1.000000 | 0.976463 | **0.976463** | E2 | 198 | 827 | **827** |
| **REGISTERED 1.40** | **holdout** | **875** | **−0.001068** | **0.832450** | **0.043277** | **0.043277** | **E2** | **795** | **none** | **none** |
| **REGISTERED 1.40** | in-sample | 1,762 | −0.001068 | 0.980162 | 0.040686 | **0.040686** | E2 | 795 | none | **none** |
| quartered 0.70 | holdout | 875 | −0.021261 | 0.366747 | 0.001271 | **0.001271** | E2 | 3,180 | none | **none** |
| quartered 0.70 | in-sample | 1,762 | −0.021261 | 0.581652 | 0.000163 | **0.000163** | E2 | 3,180 | none | **none** |

**"none" is a recorded absence, not a large number**: the alternative the test is
powered against lies inside the null, so **no sample size reaches the target**.
The same rule ADR-026 applies to an unreached rate ceiling.

**Every figure carries the Amendment 11 caveat**: the dispersion input comes from
a **post-holdout regime** and may misstate in-sample dispersion in either
direction by an unmeasured, unbounded amount.

### 3. Two questions the verdict must not conflate

**They have different answers and they are recorded separately.**

1. **Does the corrected alpha alone move E1 across its 80 percent bar?**
   **YES.** E1 at the registered 1.40 on the achievable holdout moves
   **0.743521 → 0.832450**, and the minimum n falls **1,006 → 795** against 875
   achievable.
2. **Does joint power clear 80 percent?**
   **NO. It is 0.043277**, and **no session count reaches 80 percent at the
   registered assumption**, because E2's pessimistic-cost mean is negative.

**Correcting the multiplicity error made E1 powered and left the design
unpowered.** Both are true, and reporting either without the other would
misdescribe the repository.

### 4. How close it is, recorded because the operator's decision turns on it

**The collapse is by a thin margin, and thinness is not comfort.** A test with
0.043 power detects nothing whether it misses by a little or a lot. But the
margin bears on which route is reasonable, so it is measured rather than left
for the operator to estimate:

| quantity | figure |
|---|---:|
| pessimistic-cost mean at 1.40 | **−0.001068 USD/share** |
| shift as a fraction of the central mean at 1.40 | **1.0265** |
| **break-even Sharpe** — where the pessimistic-cost mean reaches zero | **1.437035** |
| the registered 1.40 sits **below** it by | **2.577 percent** |
| **break-even stop-exit share** at 1.40 | **0.346206** |
| the measured stop share exceeds it by | **0.035612** |

**Read plainly: the registered effect assumption sits about two and a half
percent below the Sharpe at which the design's own pessimistic cost band breaks
even.** Half of the published 2.81 is 1.405; **the break-even is 1.437.** The
design was registered just on the wrong side of its own cost band, and **nobody
could have known that before the shift was measured**, because the shift depends
on a stop-versus-close mix that did not exist as a figure until A.1 TASK 3 of
this pass.

### 5. What was NOT done

**Registered explicitly, because each was available and each would have been
wrong:**

- **The cost band was not adjusted.** Section 6's pessimistic figures are
  0.040 / 0.080 / 0.020 exactly as registered before any data existed.
- **The effect assumption was not adjusted.** It remains **1.40**, half the
  published 2.81, for the reasons ADR-005 registered.
- **The alpha was not adjusted to rescue the figure.** 0.05 is Amendment 18's
  correction to a **conjunction**, made **before** this table existed and for a
  reason that has nothing to do with it.
- **No weaker E2 was substituted.** The null is the one Amendment 19 fixed
  before the shift was measured.
- **The ambiguous exclusion was not changed**, and at a measured rate of
  0.000000, `n = 560`, it was not a candidate for change.

### 6. The three routes, for the operator, none chosen here

**This amendment hands over a decision. It does not make one.**

1. **Accept a narrower verdict scope conditional on central costs alone, with
   E2 demoted to a named secondary.** E1 is powered at **0.832450** on the
   achievable holdout at the registered assumption. The verdict would then say
   what it can support: *the rule cleared its bar under the **central** cost
   assumptions*, with the pessimistic band reported as a **descriptive**
   secondary that carries no verdict row. **The cost this buys is exactly the
   thing Section 1's structural doubt 2 said mattered most**, and the
   registration would have to say so where the verdict is stated.
2. **Narrow the registered cost band on measured execution evidence.** The
   pessimistic entry figure of 0.040 USD per share is **carried and registered,
   never measured**. Real fill data would let the band be narrowed on evidence.
   **This repository does not hold that evidence, has no broker credential, and
   none is planned.** It is a real route and it is not currently open.
3. **Close H1 as `untestable-at-achievable-power` under its own registered cost
   assumptions.** This is a **legitimate documented closure** and it is the
   **fourth closure kind already named in `HYPOTHESES.md`**. It would record
   that the design, as registered, cannot detect the effect it was built to
   detect at the sample size it can reach — **which is a finding about the
   design, not about the world**, and is exactly the kind of negative this
   repository exists to be able to produce.

**A note the operator is entitled to before choosing.** Route 3 does not depend
on the bar-integrity measurement due **2026-09-12**, and routes 1 and 2 do not
either. **This decision is orthogonal to the calendar**, and taking it does not
require waiting.

### 7. What this amendment does not do

- **It fires no verdict.** Section 0 is fired at TASK 6 of this pass and
  **PENDING_REVISION is still expected**, because both integrity inputs remain
  recorded absences.
- **It closes nothing.** H1 remains **OPEN**.
- **It opens no latch, arms nothing and authorises no spend.**
- **It changes no rule of Sections 2, 3, 5 or 6.**

---

## Amendment 22 — Section 1 restated: the breakout is a direction rule, not a selector

**Date:** 2026-08-29 · **Status:** accepted · appends **Section 1.1** and
**Section 11.2**; **changes no registered rule**

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 21, plus those amendments — the measured trigger rate of
**0.982143**, `n = 560` selected name-sessions over `n = 28` evaluable
post-holdout sessions, and the measured ambiguous rate of **0.000000** on the
same `n = 560`. **Zero dollars spent, zero requests sent. Neither latch exists.**

### 1. The implication that was falsified

**Section 1 says *"a breakout of the first 5-minute regular-session range"*.**
The word **breakout** implies a **selective event** — something that happens on
some name-sessions and not others, whose occurrence is part of what the rule
conditions on.

**Measurement falsified the implication at `n = 28` sessions and `n = 560`
selected name-sessions: the trigger rate is 0.982143.** Almost every selected
name-session produces one. **The condition selects on almost nothing.**

**The mechanics make it unsurprising once stated.** The opening range spans the
**first five minutes**; the trigger window spans everything after it to the
close, roughly **385 minutes**. A liquid name almost always trades outside a
five-minute range in one direction or the other over that span. **What carries
whatever information exists is the direction of the first excursion, not the
fact that one occurred.**

### 2. What is amended, and what is emphatically not

**Amended: the description.** Section 1.1 restates H-ORB as a claim about **the
sign of the first excursion** past the opening 5-minute range. Section 11.2 adds
the consequence to the epistemic boundary.

**Not amended: the rule.** Section 2's universe and event rule, Section 3's
entry, stop and exit, Section 4's sizing, Section 5's outcome definition and
Section 6's cost model are **byte-for-byte as registered**. **The rule is what
was registered and it stands.** A rule that fires on 98 percent of name-sessions
is still a well-defined rule with a well-defined direction, and changing it now
would be changing the experiment after seeing a measurement.

**This distinction is the whole of the amendment**: the registration described
the rule wrongly, and the description is what is corrected.

### 3. The joint claim survives, with its halves renamed

H-ORB remains **a joint claim about the selection and about the signal**, and it
can still fail on either half while the other is real. What changed is which
half does which job:

- **The selection — top 20 by opening relative volume — is doing real
  conditioning work.**
- **The breakout half is not a selector. It is a direction rule.**

**The source study's own numbers already said this and this registration did not
read them that way.** The plain broad-universe 5-minute ORB returned **3.2
percent annually at Sharpe 0.48, below passive** (carried, C-2), while the
top-20-by-relative-volume restriction returned **more than 1,600 percent at
Sharpe 2.81** (carried, C-3). **The selection did almost all the work there
too**, and `HYPOTHESES.md` has recorded that since the first commit. **What was
missing was the step from "the selection does the work" to "then the breakout is
not selecting anything", and it took a measured trigger rate to force it.**

### 4. What it costs a later positive verdict

**A narrowing, recorded before any read exists.** A positive result would be
evidence about **the informational content of the first directional excursion**.
It would **not** be evidence that a breakout event, as commonly understood,
**selects profitable sessions** — because at a rate of 0.982143 there is no
meaningful population of non-breakout sessions for the breakout ones to be
better than.

**A reader who arrives at a later `PASS` expecting a statement about breakouts
would be reading a statement about direction.** Section 11.2 says so where the
epistemic boundary is stated.

### 5. What this amendment does not do

- **It changes no rule, no threshold, no gate and no Section 0 branch.**
- **It changes no figure.** E1, E2, joint power and every measured input are
  exactly as Amendment 21 recorded them.
- **It opens no latch, arms nothing, sends nothing and spends nothing.**

---

## Amendment 23 — Section 0 re-fired PENDING_REVISION on the corrected inference

**Date:** 2026-08-29 · **Status:** accepted · records a firing of **Section 0**;
**amends no branch**

**What data existed when this amendment was made.** Everything held at
Amendments 11 through 22, plus those amendments. **The bar revision rate and the
cross-vendor agreement share still do not exist**, and neither is eligible before
**2026-09-12**. **Zero dollars spent, zero requests sent. Neither latch exists.**

### The verdict

> ## **`PENDING_REVISION`** · clause `PENDING-REVISION Amendment 10`
>
> **Access passes and the integrity measurement still does not exist.** Nothing
> is armed. Nothing is closed. **H1 remains OPEN.**

`tools/refire_section0_repair.py` is the **fourth** firing tool; the three
earlier ones are left untouched, and all four records sit in the same
append-only ledger.

### The two questions, kept apart because they have different answers

| question | answer | figures |
|---|---|---|
| **Does the corrected alpha alone move E1 across its 80 percent bar?** | **YES** | **0.743521 → 0.832450** at the registered 1.40 on `n = 875`; minimum n **1,006 → 795** |
| **Does JOINT power clear its 80 percent bar?** | **NO** | **0.043277**; minimum n **unreachable at any sample size** |

**Correcting the multiplicity error made E1 powered and left the design
unpowered. Both are true, and the verdict record carries both as separate
fields** so a later reader cannot collapse them.

### Every input, with its n

| input | figure | n |
|---|---|---|
| alpha per co-primary | **0.05** (superseded 0.02532057) | — |
| **E1 power at the registered 1.40** | **0.832450** | 875 |
| E1 power at the published 2.81 | 0.999835 | 875 |
| E1 minimum n for 80 percent | **795** | — |
| **E2 power at the registered 1.40** | **0.043277** | 875 |
| E2 power at the published 2.81 | 0.819524 | 875 |
| E2 minimum n for 80 percent at 1.40 | **Absent — unreachable** | — |
| **E2 pessimistic-cost mean at 1.40** | **−0.001068 USD/share** | — |
| E2 central mean at 1.40 | +0.040386 USD/share | — |
| **measured pessimistic shift** | **0.041455 USD/share** | 550 exits |
| **measured stop-exit share** | **0.381818** | **550** |
| **measured ambiguous rate** | **0.000000**, rule-of-three upper bound **0.005357** | **560** |
| E2 dispersion input | 2.029585 USD/share | 550 |
| **JOINT power at the registered 1.40** | **0.043277**, binding component **E2** | 875 |
| JOINT power at the published 2.81 | 0.819524, binding component E2 | 875 |
| delisted names with intraday history | **203** — `PASS` | 229 |
| **bar revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** | 0 |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** | 0 |
| dollars spent | **0** | — |

**Every E2 and joint figure carries the Amendment 11 caveat**; **every in-sample
figure carries SL-3**; **every statement about what a PASS would mean carries
§11.2** (Amendment 22).

### An observation recorded for the operator and deliberately not acted on

**BLOCKED-1 is registered on E1 power at the *published* magnitude against the
0.50 floor.** E1 at 2.81 is **0.999835**, so **it does not fire**, and the map
behaved exactly as registered.

**Had BLOCKED-1 been defined on JOINT power at the registered assumption, it
would fire — that figure is 0.043277, an order of magnitude below the floor.**

**This pass does not change the branch.** It is recorded here because it is
material to the routes Amendment 21 hands the operator, and because a reader
comparing a 0.043277 joint power against a 0.50 BLOCKED floor is entitled to
know the branch was evaluated on the input it was registered with rather than on
the one that would have fired.

### What this amendment does not do

- **It fires no `GO` and no `DEGRADED`**, and the tool exits 78 if the map ever
  hands it one.
- **It arms nothing, opens no latch and authorises no spend.**
- **It closes nothing.** H1 remains **OPEN**.
- **It changes no Section 0 branch.** `src/orb/section0.py` is byte-identical to
  its state before this pass.
