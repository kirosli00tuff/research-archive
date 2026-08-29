# Hypothesis register

**Read this before proposing any new hypothesis on intraday US equity price
structure.**

**This file exists to prevent retrying a settled question because the number
that closed it is buried.** That is its whole job. A closed entry carries the
figure that closed it, with its n, and states what would reopen it — or states
that nothing would. A question that was answered expensively and then re-asked
because nobody could find the answer has cost this house real time before.

This file contains **no analysis**. It records what the registration and the
sealed reads established.

**Status at 2026-08-29: H1 OPEN, registered, Stage A in progress. Ten
candidates closed before opening at registration. H2 and H3 PARKED.**

**Updated 2026-08-29, A.1 resumption:** the **operator prior slot is filled** at
**0.30, INDEPENDENT** (Amendment 5), which satisfies **Section 10 clause 2**. Two
of the latch's three clauses remain unsatisfied and **Stage C does not open.**
**Section 0 re-fired `PENDING_REVISION`** (Amendment 10). **Two open operator
items remain and neither blocks the ladder: a third feed on a genuinely
different upstream, and a costed decision on the Massive tier. The binding
constraint is a calendar — the earliest eligible re-pull is 2026-09-12.**

---

## The closure kinds

Four are already in the house record and a fifth is new here. A future closure
is typed with one of these so that the *kind* of the answer survives even when
the details are skimmed.

| kind | meaning | precedent |
|---|---|---|
| **cost-bound** | The effect may be real; it does not survive the modeled cost. | MLCryptoEngine H6 — per-fill positive, negative under an order-lifecycle fill model |
| **signal-absent** | The effect is not present at a detectable magnitude on this sample. | NPLExperiment H1 — 197/312 positive, exact lower bound 0.5707 against a 0.60 bar |
| **unmeasurable-on-available-data** | The question is well-posed; the data to answer it is not served. | MLCryptoEngine H11 class B — a **measured 75-day** publication lag |
| **untestable-at-achievable-power** | The design's own arithmetic blocks it before any data exists. | InsiderExperiment — closed BLOCKED before measurement, the cheapest finding in the house record |
| **source-integrity-blocked** *(new here)* | The vendor's own bars are not stable or not consistent enough for any verdict computed on them to mean anything. | **The Concretum shape**: identical opening-range code, four vendors, identical dates, parameters and starting capital, final portfolio values **226,000 to 726,000 USD** — a threefold spread from vendor choice alone |

**The fifth kind is the one this repository is most likely to produce**, and it
is registered before the measurement so that a BLOCKED verdict reads as a
documented answer rather than a failure of process.

---

## Register

### H1 — H-ORB, the opening-range breakout on relative-volume-selected names

> Among US common stocks with elevated opening relative volume, a breakout of
> the first 5-minute regular-session range predicts continuation to the session
> close, net of modeled costs, out of sample from 2023-01-03.

| | |
|---|---|
| **Status** | **OPEN** · registered 2026-08-29 · **Section 0 re-fired `PENDING_REVISION` 2026-08-29** (A.1 resumption TASK 10, Amendment 10), superseding the `PENDING_ACCESS` of Amendment 4 |
| **Section 0 verdict, re-fired 2026-08-29 (amendment pass TASK 6)** | **PENDING_REVISION**, clause `PENDING-REVISION Amendment 10`, recorded by **Amendment 16**. **E2 power is now a number rather than `Absent`**: **0.743533** at the registered 1.40 on n = 875 holdout sessions, **0.999484** at the published 2.81, **0.257809** at the quartered 0.70, and **0.959721 / 0.999999 / 0.458773** on the in-sample n = 1,762; minimum N for 80 percent **1,006 / 250 / 4,021**. The dispersion input is **2.029585 USD per share, n = 550 priced trades**, measured on the post-holdout half of the amended carve-out (**Amendment 11**), and **every E2 figure carries that amendment's caveat: the input comes from a post-holdout regime and may misstate in-sample dispersion in either direction by an unmeasured, unbounded amount**. Under the **frozen** Section 6 model the figure is **`Absent`** — 550 of 550 trades refused, because the SEC Section 31 effective date is unmeasured and the model refuses rather than take a fee from the wrong year. **E1 is unchanged at 0.7435** and is not presented as changed; **E2 equals E1 to five decimal places because E2's permutation clusters on session date and the per-trade dispersion cancels** (Amendment 15, a falsified premise of Section 9, not a copied figure). **The verdict did not move**: both integrity inputs are still recorded absences, eligible **2026-09-12**, and `GO` would fail anyway at 0.7435 against the 0.80 floor. **Storing bars is not reading them** — the probe slice overlaps the holdout from 2026-05-05 to 2026-06-30 as **collection**, and **the Stage D latch continues to govern the holdout in full and has not been written**. |
| **Measured trigger rate** | **0.982143**, n = **560 selected name-sessions** (28 post-holdout sessions × the registered 20), against an assumption of **0.55** used until now in a non-binding per-trade note — **a disagreement of +0.432, and the measurement wins** (Amendment 15, the NPLExperiment shape). Long-only rate **0.525**; ambiguous triggers **0**; trades per session **19.64** of a registered 20. **Stated narrowly: this is a post-holdout figure over a 200-name systematic sample of 5,317, and it is not the in-sample trigger rate.** |
| **Section 0 verdict** | **PENDING_REVISION** (Amendment 10, clause `PENDING-REVISION Amendment 10`). **Access passes** — two credentials authenticate, the primary reaches **1,762/1,762 in-sample and 875/875 holdout** sessions — **and the integrity measurement still does not exist**, because the registered **14-calendar-day wait** between the probe pull and its identical re-pull has not elapsed. **The wait is the measurement**: a re-pull sent early measures a revision rate biased toward zero, and **zero is the shape of a PASS**. **Nothing is armed. Nothing is closed.** This is a **parked outcome, not a failure**, and explicitly **not** a `source-integrity-blocked` closure — that kind requires a vendor whose bars were *measured* and found unstable, and the measurement that could do that is **fourteen days away**. **Earliest eligible re-pull: 2026-09-12.** |
| **Superseded verdict** | **PENDING_ACCESS** (Amendment 4, 2026-08-29), fired on **0 of 9 vendors serving a bar**, n = 15 robots fetches and n = 25 API probes. It is superseded rather than corrected: it was right when it fired, and two credentials changed the world it described. **Counterfactual recorded then and still standing: had bar integrity passed in full, the same power inputs fire `DEGRADED`.** |
| **What this resumption measured** | **Tape:** `SAME_TAPE` on Massive vs Alpaca-SIP, median first-5-minute volume ratio **1.005197**, IQR [1.003096, 1.007726], **n = 100** pairs; two controls separated at **≈0.028**. **Reach, bisected:** Alpaca **2016-01-04** (1,762/1,762 and 875/875), Massive **2024-08-29** (0/1,762 and 459/875), **n = 16 probes each**. **Delisted coverage:** **203 names with intraday history**, n = **229** in-window names checked, share **0.8865** — **`PASS`** against the registered 100. **4,731** delisted names enumerated inside the window. **Rate ceilings:** Massive **5.00/min** measured (first refusal at request 6 of 8, both endpoints); Alpaca's ceiling **not reached** at 134.05/min. **Probe slice sealed:** 60 sessions × 40 tickers = **2,400 pairs**, 480 files, **737,507 bars**. |
| **Power, computed** | At the computed holdout **n = 875** (from `orb.calendar`, not the prompt): **E1 power 0.7435 at the registered 1.40**, below the 0.80 GO floor; **0.9995 at the published 2.81**, above it; **0.2578 at the quartered 0.70**, below the 0.50 BLOCKED floor. Minimum N for 80 percent at 1.40 is **1,006** — a shortfall of **131 sessions**. **E2 power is `Absent`**: Section 9 restricts its dispersion input to the pre-period carve-out and no vendor serves one. |
| **Cost model, measured** | Frozen and hashed `3789221b…`. Live re-verification found the carried FINRA TAF rate **stale at 0.000166 against a measured 0.000195**, and **three components not modeled at all** — the 1 percent maximum per order, the FINRA CAT fee, and NSCC/DTC clearing. At the central band on a 50 USD name a round trip costs **≈ 0.0386/share on a close exit and ≈ 0.0686 on a stop exit**, against the replication's measured gross edge of **0.070/share**: **55 percent and 98 percent of the edge respectively.** (Amendment 3.) |
| **Registration** | `REGISTRATION.md` Sections 0–14. Section 0 fires at A.2 TASK 5. |
| **The claim is joint** | It is a claim about **the selection** and about **the breakout**, and it can fail on either half while the other is real. In the source study the **selection by relative volume, not the breakout, did almost all the work**: the plain broad-universe 5-minute ORB returned **3.2 percent annually at Sharpe 0.48, below passive** (carried, C-2), while the top-20-by-relative-volume restriction returned **more than 1,600 percent net at Sharpe 2.81** (carried, C-3). |
| **Registered bars** | **E1** deflated Sharpe **≥ 1.00** on the daily net portfolio return series over the holdout, trial count **8**, skew and kurtosis from the realized series. **E2** mean net PnL per trade, one-sided lower bound **> 0** at alpha_adj **0.02532**, by permutation on session labels clustered by session date. **Both must pass.** Plus two pass-fail structural gates: **no single holdout calendar year above 50 percent of holdout net PnL**, and **positive net PnL in at least 3 of 4 holdout years**. |
| **Power assumption, with its rationale** | **Annualized net Sharpe 1.40 — half the published 2.81.** Not discretionary: McLean and Pontiff measured **58 percent post-publication decay across 97 predictors from 80 studies** (carried, C-12); the source result is unreplicated and commercially motivated; and the one independent replication of the sibling index strategy **found the edge inside the spread** (carried, C-6). Powers are also computed at the undecayed **2.81** and a quartered **0.70** and reported beside, the NPLExperiment H3 pattern. |
| **The registered shortfall** | The holdout holds ~880 sessions and yields **t = 2.62** at the registered assumption, **below the 3.0 Harvey, Liu and Zhu argue a new claim should clear** (carried, C-10). Registered openly as ADR-005 rather than discovered at the read; the holdout gate is set at a per-trade **t of 2.50** with E1's deflation carrying the multiple-testing correction. |
| **What decides this repository** | **Not the return. Bar integrity.** A.1 TASK 3 measures the bar revision rate; A.1 TASK 4 measures cross-vendor first-5-minute agreement and delisted-name coverage. Either can fire **BLOCKED** at perfect power. |
| **Registered scope limits, both recorded before the number exists** | **1.** The two feeds **share an upstream** (ADR-022): the ratio IQR is **0.46 percentage points wide over n = 100 pairs**, which two independent consolidations would not produce. A cross-vendor `PASS` establishes that **two redistributors of one upstream agree** — **it is not the Concretum test**, because Concretum's threefold spread is a spread *across upstreams*. **2.** The two feeds **overlap only from 2024-08-29** (Amendment 8): **459 of 875 holdout sessions and 0 of 1,762 in-sample**. **Together: the gate as it can actually be run covers 459 of 2,637 registered sessions, on a redistribution pipeline.** |
| **SL-3 — the in-sample window is single-sourced** | **Registered 2026-08-29, REGISTRATION.md §11.1 under Amendment 12.** Cross-vendor agreement covers **459 holdout sessions and 0 in-sample sessions**, because the reference vendor's tier serves nothing before **2024-08-29**. **All 1,762 in-sample sessions rest on a single unverified feed.** The registered first-5-minute high-or-low agreement gate, **when it fires, speaks only to the overlap region and carries no information about the in-sample window**. The exposure this names is Concretum's **226,000 to 726,000 USD** spread in final equity across **four vendors** on identical opening-range code, dates, parameters and starting capital (carried, C-13), and **this repository cannot currently retire it for the in-sample window**. **Consequence for the verdict, recorded before any read exists: a PASS computed on the in-sample window is conditional on a single vendor's rendering of that window being faithful, and this repository holds no measurement supporting that condition. Any in-sample figure is reported with this limitation attached in the same sentence.** It is **not** a claim that the in-sample bars are wrong — none has been measured — and it is **not a Section 0 branch**: it fires nothing and changes no figure. **Two routes would retire it, neither chosen and neither costed here:** a reference credential whose tier reaches **2016-01-04**, or **explicit operator acceptance** that the in-sample window is single-sourced. |
| **H-ORB restated, Amendment 22** | **The breakout is a direction rule, not a selector.** The measured trigger rate is **0.982143**, n = **560** selected name-sessions over n = **28** evaluable post-holdout sessions, and the measured ambiguous rate is **0.000000** on the same n. Over roughly 385 minutes after a five-minute range, a liquid name almost always trades outside it, so **the condition selects on almost nothing** and **the sign of the first excursion carries whatever information exists**. Restated: *among US common stocks with elevated opening relative volume, the sign of the first excursion past the opening 5-minute range predicts the direction of the remainder of the session, net of modeled costs, out of sample from 2023-01-03*. **The registered rule is unchanged** — only the description was wrong. **Consequence (§11.2): a positive result would be evidence about the informational content of the first directional excursion, and NOT evidence that a breakout event as commonly understood selects profitable sessions.** The joint claim survives with its halves renamed: the relative-volume selection does the conditioning, which the source study's own C-2 against C-3 already said. |
| **Inference repair, Amendments 18 to 21** | **The multiplicity treatment was wrong.** Section 8 is a conjunction and carried a union correction; Berger 1982 gives an intersection-union test the full nominal level per component, so each co-primary now runs one-sided at **0.05**. **E1 at the registered 1.40 on 875 holdout sessions moves 0.743521 → 0.832450**, minimum n **1,006 → 795**. **E2 was replaced**, not repaired: it was a rescale of E1 and constrained nothing E1 did not. The amended E2 tests whether mean net PnL per trade stays above zero at the **pessimistic** end of the Section 6 band. **Measured stop-exit share 0.381818** (n = 550), **pessimistic shift 0.041455 USD/share**, against an implied central mean of **0.040386** at 1.40 — so the **pessimistic-cost mean is −0.001068, negative**, **E2 power is 0.043277** and **joint power collapses to 0.043277 with no n reaching 80 percent**. **Section 10.1 makes the latch condition JOINT power**, bounded above by the smaller component. **Correcting the multiplicity made E1 powered and left the design unpowered; both are true and neither may be reported without the other.** Break-even Sharpe **1.437035**, and the registered 1.40 sits **2.577 percent** below it. **Three routes are open to the operator and none is chosen here.** |
| **Assistant prior** | **0.15**, recorded 2026-08-28, before any measurement. |
| **Operator prior** | **0.30**, label **INDEPENDENT**, recorded **2026-08-29** by the operator (Amendment 5). **Blindness: `independent_but_not_blind`** — the operator formed 0.30 rather than adopting the assistant's number, but the assistant's **0.15** was recorded first, on 2026-08-28, and was visible to the operator before this number was formed. **A later reader must not score 0.30 as an unanchored estimate.** **Disagreement: a factor of 2.0**, recorded as a field so both priors are scored against the same outcome. **Operator's stated reason, in the operator's terms:** prior house experiments have carried pessimistic evaluations, and the operator's own research and knowledge of intraday opening-range behaviour supports a figure above 0.15. **Recorded ambiguity, unresolved on purpose:** harsh house gates argue for a *lower* prior on H1 clearing them, while systematic house under-forecasting of survival argues for a *higher* one; the operator did not narrow between them and this register does not narrow on the operator's behalf. **The resolution of H1 scores the number either way.** |
| **Calibration eligibility** | **ELIGIBLE.** H1 is eligible for operator calibration scoring. **No exclusion on adopted-prior grounds ever existed here** — the condition was checked at Amendment 5 and is false, so none is voided. |
| **Stage C latch, Section 10** | Clause 2 (**operator prior slot filled and labelled**) now reads **SATISFIED**. Clause 1 (**both co-primaries ≥ 0.80 power**) is **UNSATISFIED** — E1 **0.7435** at the registered assumption on n = 875, E2 **`Absent`**. Clause 3 (**explicit operator instruction**) is **UNSATISFIED**. **The latch remains closed.** |
| **Working** | `REGISTRATION.md`, `progress.md`, `report.md`, `DECISIONS.md`. |

---

## Closed before opening — the ten candidates culled at registration

Each was considered as an alternative to H1 and closed **before any data
existed**, with a one-line reason. **None was closed on a measurement**, and
none of them is reopened by anything H1 does.

| # | candidate | reason closed |
|---|---|---|
| 1 | **Index-ETF opening-range breakout** (the QQQ/TQQQ variant) | **Closed on the replication figures.** The independent replication reproduced the QQQ result within noise — **1,775 trades against the paper's 1,795, gross Sharpe 1.06** — and then showed **the entire gross edge of 0.070 USD per share sits inside the spread**, with **net PnL crossing zero at ~0.022 USD/share against a QQQ spread near 0.010** (carried, C-5, C-6). Testing it again would spend the sample re-measuring a settled cost problem. ADR-013. |
| 2 | **CME Bitcoin weekend gap fill** | Wrong asset class for this repo's substrate, and the gap is a well-known retail-documented pattern with no cost analysis attached. |
| 3 | **S&P index addition and Russell reconstitution** | Event count per year is small and the effect is the most-arbitraged index event in the literature; power at achievable N fails before costs are modeled. |
| 4 | **Turn-of-the-month** | A calendar effect with decades of publication behind it; McLean and Pontiff decay applies at full strength and the effect size is below any realistic cost floor for a retail account. |
| 5 | **Short-term reversal** | Requires holding overnight or shorting hard-to-borrow names at scale; the borrow term dominates the signal and this repo excludes names above a 25 percent borrow rate by design. |
| 6 | **Post-earnings announcement drift** | Multi-day horizon, so it shares no substrate with an intraday collector; a separate repository, not a variant. |
| 7 | **Prediction-market mispricing** | Different venue, different cost structure, no shared substrate. |
| 8 | **Perpetual funding carry** | Crypto perpetuals; no shared substrate with US equities. |
| 9 | **New Hyperliquid listing drift** | **DUPLICATE.** Closed as H1 in **NPLExperiment** on 2026-08-28 — FAIL on the sealed read, **197/312 positive, exact lower bound 0.5707 against a 0.60 bar**. Its live successors H2, H3, H4 are registered there. **This repository does not re-ask it.** |
| 10 | **Spot Bitcoin ETF flow** | **DUPLICATE.** Registered and running in **ETFExperiment** as H-ETF. **This repository does not re-ask it.** |

---

## Parked

**No second repository opens while H1 is unresolved.** That is the reason, and
it is the only reason. Neither entry below is closed and neither is refuted.

### H2 — pre-FOMC drift

> Equity index returns are systematically positive in the window before a
> scheduled FOMC announcement.

**Status: PARKED**, 2026-08-29. Not closed, not refuted, not tested. It shares
a session-calendar substrate with H1 and would be cheap to add **after** H1
resolves. Opening it now would split attention across two registrations and put
two hypotheses under one unbudgeted familywise error rate.

### H3 — VIX term-structure roll yield

> The slope of the VIX futures term structure predicts the return to a short
> volatility position by enough to clear costs.

**Status: PARKED**, 2026-08-29. Same reason. It shares no substrate with H1 at
all, which makes it a genuinely separate repository rather than a variant, and
that is another reason not to open it here.

---

## Rules for adding an entry

1. **A new hypothesis needs its own registration, written before any read.**
2. **A spent read is spent.** A successor runs on fresh data or it does not run.
   Every value inside a spent read is quarantined from all successor code paths
   by AST pin and by test.
3. **A closure is typed** with one of the five kinds above.
4. **Every figure travels with its n in the same sentence.**
5. **A DUPLICATE is labelled DUPLICATE and names the repository that holds it.**
