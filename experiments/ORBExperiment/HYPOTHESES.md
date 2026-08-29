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
| **Status** | **OPEN** · registered 2026-08-29 · **Section 0 fired `PENDING_ACCESS` 2026-08-29** |
| **Section 0 verdict** | **PENDING_ACCESS** (Amendment 4). The integrity measurement the map fires on does not exist: **A.1 TASK 1 measured 0 of 9 vendors serving a bar to this repository**, n = 15 robots fetches and n = 25 API probes. **Nothing is armed. Nothing is closed.** Explicitly **not** a `source-integrity-blocked` closure — that kind requires a vendor whose bars were measured and found unstable, and no bar has been served to fail. **Counterfactual, computed: had bar integrity passed in full, the same power inputs fire `DEGRADED`** — which is exactly what Section 0 predicted in writing before any measurement existed. |
| **Power, computed** | At the computed holdout **n = 875** (from `orb.calendar`, not the prompt): **E1 power 0.7435 at the registered 1.40**, below the 0.80 GO floor; **0.9995 at the published 2.81**, above it; **0.2578 at the quartered 0.70**, below the 0.50 BLOCKED floor. Minimum N for 80 percent at 1.40 is **1,006** — a shortfall of **131 sessions**. **E2 power is `Absent`**: Section 9 restricts its dispersion input to the pre-period carve-out and no vendor serves one. |
| **Cost model, measured** | Frozen and hashed `3789221b…`. Live re-verification found the carried FINRA TAF rate **stale at 0.000166 against a measured 0.000195**, and **three components not modeled at all** — the 1 percent maximum per order, the FINRA CAT fee, and NSCC/DTC clearing. At the central band on a 50 USD name a round trip costs **≈ 0.0386/share on a close exit and ≈ 0.0686 on a stop exit**, against the replication's measured gross edge of **0.070/share**: **55 percent and 98 percent of the edge respectively.** (Amendment 3.) |
| **Registration** | `REGISTRATION.md` Sections 0–14. Section 0 fires at A.2 TASK 5. |
| **The claim is joint** | It is a claim about **the selection** and about **the breakout**, and it can fail on either half while the other is real. In the source study the **selection by relative volume, not the breakout, did almost all the work**: the plain broad-universe 5-minute ORB returned **3.2 percent annually at Sharpe 0.48, below passive** (carried, C-2), while the top-20-by-relative-volume restriction returned **more than 1,600 percent net at Sharpe 2.81** (carried, C-3). |
| **Registered bars** | **E1** deflated Sharpe **≥ 1.00** on the daily net portfolio return series over the holdout, trial count **8**, skew and kurtosis from the realized series. **E2** mean net PnL per trade, one-sided lower bound **> 0** at alpha_adj **0.02532**, by permutation on session labels clustered by session date. **Both must pass.** Plus two pass-fail structural gates: **no single holdout calendar year above 50 percent of holdout net PnL**, and **positive net PnL in at least 3 of 4 holdout years**. |
| **Power assumption, with its rationale** | **Annualized net Sharpe 1.40 — half the published 2.81.** Not discretionary: McLean and Pontiff measured **58 percent post-publication decay across 97 predictors from 80 studies** (carried, C-12); the source result is unreplicated and commercially motivated; and the one independent replication of the sibling index strategy **found the edge inside the spread** (carried, C-6). Powers are also computed at the undecayed **2.81** and a quartered **0.70** and reported beside, the NPLExperiment H3 pattern. |
| **The registered shortfall** | The holdout holds ~880 sessions and yields **t = 2.62** at the registered assumption, **below the 3.0 Harvey, Liu and Zhu argue a new claim should clear** (carried, C-10). Registered openly as ADR-005 rather than discovered at the read; the holdout gate is set at a per-trade **t of 2.50** with E1's deflation carrying the multiple-testing correction. |
| **What decides this repository** | **Not the return. Bar integrity.** A.1 TASK 3 measures the bar revision rate; A.1 TASK 4 measures cross-vendor first-5-minute agreement and delisted-name coverage. Either can fire **BLOCKED** at perfect power. |
| **Assistant prior** | **0.15**, recorded 2026-08-28, before any measurement. |
| **Operator prior** | **EMPTY — reserved. The empty slot blocks the Stage C latch structurally.** The assistant never fills it (NPDExperiment Amendment 0: an adopted prior corrupts the calibration ledger). |
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
