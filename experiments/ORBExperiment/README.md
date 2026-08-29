# ORBExperiment

**A measurement-only test of one hypothesis: among US common stocks with
elevated opening relative volume, a breakout of the first 5-minute
regular-session range predicts continuation to the session close, by enough to
clear modeled commissions, fees, borrow and slippage, out of sample from
2023-01-03.**

**Stage A never trades, never touches capital, and never reads an outcome
value.** There is **no live broker credential**, no order, no position, and no
stage in which one is planned. **A documented negative is a valid and expected
outcome.**

**Precise as of 2026-08-29**, because the repository now holds credentials and
the claim must be exact: the two market-data credentials are **Alpaca
paper-account keys**, and **the live trading host refuses them** — `401`,
`{"code":40110000,"message":"request is not authorized"}`, measured. They grant
**market data and no trading capability of any kind.**

**The measurement that decides this repository is not the return. It is bar
integrity.** If the vendor's own bars are not stable and not consistent, no model
here can mean anything, and **BLOCKED is the correct and cheap answer**.

---

## Status: Section 0 re-fired **PENDING_REVISION** on 2026-08-29

**Nothing is armed. Nothing is closed. H1 is OPEN.**

**Access passes.** Two credentials authenticate and both serve one-minute bars.
The primary reaches **every registered session**: Alpaca's earliest served
session is **2016-01-04** — **1,762 of 1,762 in-sample** and **875 of 875
holdout**, over `n = 16` bisection probes. Delisted coverage is **`PASS` at 203
names with intraday history, `n = 229` checked**. The two feeds carry the
**same tape**, median first-5-minute volume ratio **1.005197** over `n = 100`
pairs.

**And the measurement this repository turns on does not exist yet.** A.1 TASK 9
sealed the registered probe slice on 2026-08-29 — **480 files, 737,507 bars,
2,400 session-ticker pairs** — and the registered **14-calendar-day wait**
before the identical re-pull runs to **2026-09-12**. **The wait is the
measurement**: a re-pull sent early measures a revision rate biased toward zero,
and **zero is the shape of a `PASS`**.

> ### **The earliest eligible re-pull is 2026-09-12. That calendar date is the binding constraint on this repository, and no further work moves it.**

**`PENDING_REVISION` is a parked outcome, not a failure**, and it is explicitly
**not** a `source-integrity-blocked` closure — that kind requires a vendor whose
bars were *measured* and found unstable.

**Superseded:** Section 0 fired **`PENDING_ACCESS`** earlier on 2026-08-29, on
**0 of 9 vendors serving a bar**. It was right when it fired; two credentials
changed the world it described. **Its counterfactual still stands: had bar
integrity passed in full, the same power inputs fire `DEGRADED`** — exactly what
Section 0 predicted **in writing, before any measurement existed**.

### Re-fired **`PENDING_REVISION`** again on 2026-08-29, amendment pass

**The verdict did not move, and one input did.** **E2 power is now a number
rather than `Absent`** — **0.7435** at the registered 1.40 Sharpe assumption on
`n = 875` holdout sessions, from a dispersion of **2.029585 USD per share**
measured over `n = 550` priced trades on the **post-holdout half of an amended,
two-sided carve-out** (Amendment 11). **E1 is unchanged at 0.7435.**

**Why nothing moved.** The pending-integrity clause fires **ahead of** `GO` and
`DEGRADED`, and both integrity inputs are still recorded absences.
**And `GO` would have failed anyway**: it needs **both** co-primaries at or above
**0.80**, and both are **0.7435**.

### Re-fired **`PENDING_REVISION`** a third time on 2026-08-29, inference-repair pass

**The verdict did not move. The inference did.**

**A statistical error was corrected.** Section 8 registers a **conjunction** —
both co-primaries must pass — and applied a **union** correction to it. Under an
**intersection-union test** each component may run at the full nominal level
(**Berger 1982**), so **each co-primary now runs one-sided at `alpha = 0.05`**.
**E1 at the registered 1.40 Sharpe assumption moves 0.743521 → 0.832450 on the
achievable holdout, and the minimum n for 80 percent power falls 1,006 → 795
against 875 achievable.** **No datum changed.**

**E2 was replaced, not repaired.** It was a linear rescale of E1 and constrained
nothing E1 did not. The amended E2 asks whether mean net PnL per trade **survives
the pessimistic end of the Section 6 cost band** — a null E1 cannot imply.

> ### **And then it collapsed. The measured pessimistic shift of 0.041455 USD per share exceeds the implied central mean of 0.040386 at the registered assumption, so the pessimistic-cost mean is −0.001068 — negative. E2 power is 0.043277, below the 0.05 size of the test, and JOINT power collapses with it. No session count reaches 80 percent.**

**Correcting the multiplicity error made E1 powered and left the design
unpowered.** Both are true. **Section 10.1 makes JOINT power the latch
condition**, bounded above by the smaller component, so neither component power
may be read as the design's power.

**Three routes are open to the operator and none is chosen here** — a narrower
verdict scope with E2 demoted to a named secondary, a cost band narrowed on
execution evidence this repository does not hold, or closure as
**`untestable-at-achievable-power`**. **None depends on the 2026-09-12
calendar.**

**And the hypothesis was restated.** At a measured trigger rate of **0.982143**,
`n = 560`, **the breakout is a direction rule, not a selector** — over roughly
385 minutes a liquid name almost always trades outside a five-minute range.
**The registered rule is unchanged; the description of it was wrong.**

---

**Two planning figures were falsified by measurement in this pass**, both
recorded rather than quietly corrected:

- the **pre-period carve-out** — **`n = 2` credentials, 0 serving** any session
  before 2016-01-04, so the region **was never reachable** (Amendment 11);
- the **0.55 trigger-rate assumption** — measured at **0.982143**, `n = 560`
  selected name-sessions (Amendment 15).

**And a premise of the method was falsified too:** **E2 power equals E1 power**
to five decimal places, because **E2's permutation clusters on session date**, so
the session is the independent unit and the per-trade dispersion **cancels**.
Section 9's rule applies — the computation wins and the disagreement is recorded.

---

## What is measured so far

Every figure carries its n. **Carried** figures were supplied with the design and
were **not** measured here.

### Access and terms — A.1

| figure | value | n |
|---|---|---|
| vendors probed | **9** | 9 |
| hosts fetched for `robots.txt` | 15 | 15 |
| live API probes sent | 25 | 25 |
| **vendors serving a 1-minute RTH bar** | **0** | 9 |
| vendors **refused by terms** | **4** — stooq, yfinance (`Disallow: /`), EODHD (`/api/`), Nasdaq Data Link (`/api/*.json*`) | 9 |
| vendors requiring a credential | 5 — Polygon/Massive **401**, Alpaca **401**, Databento **401**, Tiingo **403**, Alpha Vantage **200 carrying a refusal** | 9 |
| dollars spent | **0** | — |

### Rate ceilings — A.1

| figure | value | n |
|---|---|---|
| requests in the escalation | 18 | 18 |
| HTTP 429s observed | **0** | 18 |
| Polygon sustained rate admitted | **88.4/min**, all 401 | 8 |
| Alpha Vantage sustained rate admitted | **29.1/min**, all 200-carrying-a-refusal | 5 |

### Credentialed access — A.1 resumption, 2026-08-29

**Everything above was measured before any credential existed and is left
standing. `n = 1,026` requests charged on 2026-08-29. Dollars spent: 0.**

| figure | value | n |
|---|---|---|
| **credentials authenticating** | **2 of 2** | 2 |
| **primary vendor** | **Alpaca** (bar vendor) — ADR-023 | — |
| **reference vendor** | **Massive** (the only source of delisting dates) | — |
| **Alpaca earliest served session** | **2016-01-04** — 1,762/1,762 in-sample, 875/875 holdout | 16 probes |
| **Massive earliest served session** | **2024-08-29** — 0/1,762 in-sample, 459/875 holdout | 16 probes |
| **tape verdict, Massive vs Alpaca-SIP** | **`SAME_TAPE`**, median ratio **1.005197**, IQR [1.003096, 1.007726] | **100 pairs** |
| tape control, Massive vs Alpaca-IEX | `DIFFERENT_TAPE`, median **0.027856** | 100 pairs |
| tape control, Alpaca-SIP vs Alpaca-IEX | `DIFFERENT_TAPE`, median **0.027761** | 100 pairs |
| **delisted names enumerated in the registered window** | **4,731** of 6,421 served | 7 pages |
| **delisted names with intraday history** | **203** — **`PASS`**, share 0.8865 | **229 checked** |
| delisted names, out-of-window control | **0 served** — aligned with the measured reach boundary | 31 |
| **Massive measured rate ceiling** | **5.00/min**, first refusal at request 6 of 8, **both** endpoints | 16 |
| **Alpaca measured rate ceiling** | **not reached** — 25 admitted at 134.05/min, 0 refusals | 25 |
| **cross-vendor overlap** | from **2024-08-29** — **459 of 875** holdout, **0 of 1,762** in-sample | — |
| **probe slice sealed** | 60 sessions × 40 tickers = **2,400 pairs**, 480 files, **737,507 bars** | — |
| **bar revision rate** | **`Absent(not_yet_measured)`** — eligible **2026-09-12** | 0 |
| **cross-vendor agreement share** | **`Absent(not_yet_measured)`** | 0 |
| E2 power | **`Absent(not_served)`** — neither credential serves the carve-out | 2 credentials |
| dollars spent | **0** | — |
| **ceiling measured on a data endpoint** | **none** — every reachable path was an unauthenticated refusal | 0 |

### The amendment pass — 2026-08-29

**Everything above is left standing.** **`n = 979` further requests charged in
this pass** — 973 Alpaca, 6 Massive — counted from the append-only request
ledger, which charges before every send. **1,879 Alpaca of a 3,000 daily cap** in
the day as a whole, plus **2 uncharged `sec.gov` attempts, both refused `403`**.
**Dollars spent: 0.**

| figure | value | n |
|---|---|---|
| **measured trigger rate** | **0.982143** — against an assumption of **0.55** | **560 name-sessions** |
| trigger rate, long-only | **0.525** | 560 |
| ambiguous triggers | **0** | 560 |
| trades per session | **19.64** of a registered 20 | 28 sessions |
| **E2 dispersion input** | **2.029585 USD/share** | **550 priced trades** |
| E2 dispersion, bracket relative width | **8.43 × 10⁻⁵** — the unmeasured SEC effective date does not move it | 2 ends |
| **E2 dispersion under the frozen Section 6 model** | **`Absent`** — 550 of 550 trades refused | 550 |
| **E2 power at the registered 1.40, holdout** | **0.743533** | **875 sessions** |
| E2 power at the published 2.81, holdout | **0.999484** | 875 |
| E2 power at the quartered 0.70, holdout | **0.257809** | 875 |
| E2 power at 1.40 / 2.81 / 0.70, in-sample | **0.959721 / 1.000000 / 0.458773** | 1,762 |
| E2 minimum N for 80 percent | **1,006 / 250 / 4,021** | — |
| **E1 power at the registered 1.40** | **0.7435 — UNCHANGED by this pass** | 875 |
| **Alpaca ceiling, burst allowance** | **384 requests admitted in 55.96 s**, 385th refused `429` | 391 sent |
| **Alpaca ceiling, sustained** | **not reached** — 250 of 250 at **199.73/min** over 75.10 s, 0 refusals | 250 |
| Alpaca operating pace | **98.36/min** at 0.61 s spacing — half the maximum rate **sustained** | — |
| Alpaca daily cap | **3,000**, a circuit breaker, from **no** measured daily allowance | — |
| **sealed slice feed** | **`CONFIRMED_CONSOLIDATED`** — every sealed bar count equals the consolidated count, none equals the single-venue count | **7 discriminating chunks of 8** |
| carve-out sessions read / evaluated | **42 / 28**, 2026-07-01 to 2026-08-28 | **200 tickers, 1,927,156 bars** |
| carve-out universe | every **26th** of a **5,317**-name active US common-stock listing | 6 reference pages |
| **net edge per share at the registered 1.40** | **−0.003756** close exit, **−0.033756** stop exit | modeled |
| net edge per share at the published 2.81 | **+0.031369** close exit, **+0.001369** stop exit | modeled |

**Every E2 figure above carries the Amendment 11 caveat: the dispersion input
comes from a post-holdout regime, later than the sample it is applied to, and may
misstate in-sample dispersion in either direction by an amount this repository
has not measured and does not claim to bound.**

**Every in-sample figure above carries SL-3: all 1,762 in-sample sessions rest on
a single unverified feed.**

### The inference-repair pass — 2026-08-29

**Everything above is left standing.** **`n = 0` requests sent and 0 dollars
spent** — every figure here comes from arithmetic or from bytes already sealed.

| figure | value | n |
|---|---|---|
| **alpha per co-primary** | **0.05** — superseded **0.02532057** | — |
| **E1 power at 1.40, holdout** | **0.832450** — was 0.743521 | 875 |
| E1 power at 2.81 / 0.70, holdout | **0.999835** / **0.366747** — were 0.999484 / 0.257802 | 875 |
| E1 power at 1.40 / 2.81 / 0.70, in-sample | **0.980162** / **1.000000** / **0.581652** | 1,762 |
| **E1 minimum n for 80 percent** | **795** — was **1,006**, against **875 achievable** | — |
| **measured stop-exit share** | **0.381818** — 210 stop, 340 close | **550** |
| **measured ambiguous rate** | **0.000000**, rule-of-three upper bound **0.005357** | **560** |
| **measured pessimistic shift** | **0.041455 USD/share** — bounds 0.030 all-close, 0.060 all-stop | 550 |
| E2 central mean at 1.40 | **+0.040386 USD/share** | — |
| **E2 pessimistic-cost mean at 1.40** | **−0.001068 USD/share — NEGATIVE** | — |
| **E2 power at 1.40, holdout** | **0.043277** — below the 0.05 size of the test | 875 |
| E2 power at 2.81 / 0.70, holdout | **0.819524** / **0.001271** | 875 |
| **E2 minimum n for 80 percent at 1.40** | **Absent — unreachable at any n** | — |
| **JOINT power at 1.40, holdout** | **0.043277**, binding component **E2** | 875 |
| JOINT power at 2.81, holdout | **0.819524**, binding component E2 | 875 |
| **JOINT minimum n for 80 percent at 1.40** | **Absent — unreachable at any n** | — |
| JOINT minimum n for 80 percent at 2.81 | **827** | — |
| **break-even Sharpe** — where the pessimistic mean reaches zero | **1.437035** | — |
| the registered 1.40 sits **below** it by | **2.577 percent** | — |
| break-even stop share at 1.40 | **0.346206** against a measured 0.381818 | — |
| **measured trigger rate** (A.1 TASK 5) | **0.982143** — the breakout is a **direction rule** | 560 |
| dollars spent | **0** | — |

**Every E2 and joint figure carries the Amendment 11 caveat**: the dispersion
input comes from a **post-holdout regime** and may misstate in-sample dispersion
in either direction by an unmeasured, unbounded amount. **Every in-sample figure
carries SL-3.**

### Bar integrity — A.1 TASK 3 and TASK 4, **the two that decide this repository**

| figure | value | n |
|---|---|---|
| bar revision rate | **`Absent(not_yet_measured)`** | 0 |
| cross-vendor first-5-minute agreement | **`Absent(not_yet_measured)`** | 0 |
| delisted names served with intraday history | **`Absent(not_yet_measured)`** | 0 |

### Session calendar — A.2

| figure | value | n |
|---|---|---|
| sessions, 2016-01-04 to 2026-06-30 | **2,637** | 11 calendar years |
| half sessions | **21** | 11 calendar years |
| in-sample sessions | **1,762** (registration said ~1,760) | — |
| holdout sessions | **875** (registration said ~880) | — |
| unscheduled closures | 2 — 2018-12-05, 2025-01-09 | 2 |
| second-source cross-check | **`Absent`** — not completed, **and not fabricated** | 0 |

### Cost model, re-verified live — A.2

| component | carried | **measured 2026-08-29** | verdict |
|---|---:|---:|---|
| IBKR tiered commission | 0.0035/share | **0.0035** | agrees |
| IBKR order minimum | 0.35 | **0.35** | agrees |
| FINRA TAF per share sold | 0.000166 | **0.000195** | **carried figure STALE, 14.9% low** |
| IBKR maximum per order | not modeled | **1% of trade value** | **not previously modeled** |
| FINRA CAT | not modeled | **0.000003/share** | **not previously modeled** |
| NSCC/DTC clearing | not modeled | **0.00020/share** | **not previously modeled** |
| SEC Section 31 rate | per session date | **0.0000206** measured; **effective date not** | schedule registered **empty**; the model **refuses** |

**Round trip at the central band on a 50 USD name: ≈ 0.0386 USD/share on a close
exit, ≈ 0.0686 on a stop exit**, against the replication's measured gross edge of
**0.070 USD/share** (carried) — **55 percent and 98 percent of the edge**, with
**slippage 78 percent of the close-exit total**.

### Power — A.2

`alpha_adj = 0.02532057`, one-sided, per co-primary. n = **875** holdout
sessions, computed from the calendar.

| assumption | annual Sharpe | **E1 power** | min N for 80% |
|---|---:|---:|---:|
| published (undecayed) | 2.81 | **0.9995** | 250 |
| **REGISTERED (half)** | **1.40** | **0.7435** | **1,006** |
| quartered | 0.70 | **0.2578** | 4,021 |

**Superseded 2026-08-29 by Amendment 18.** The table above is left standing
because it is the correct arithmetic **at `alpha = 0.02532057`**, and that alpha
was the wrong one — a union correction on a conjunction. **At the corrected
`alpha = 0.05`:**

| assumption | annual Sharpe | **E1 power, holdout 875** | **E1 power, in-sample 1,762** | min N for 80% |
|---|---:|---:|---:|---:|
| published (undecayed) | 2.81 | **0.999835** | **1.000000** | **198** |
| **REGISTERED (half)** | **1.40** | **0.832450** | **0.980162** | **795** |
| quartered | 0.70 | **0.366747** | **0.581652** | **3,180** |

**E1 clears its 80 percent bar at the registered assumption for the first time.
The design does not.** See the joint power figures above.

~~**E2 power: `Absent` in all nine cells** — Section 9 restricts its dispersion
input to the pre-period carve-out, and no vendor serves one.~~

**Superseded 2026-08-29 by Amendments 11 and 15. The sentence above is left
standing because it was true when written**, and because *"no vendor serves one"*
is the measurement that forced the carve-out to be amended.

| assumption | annual Sharpe | **E2 power, holdout 875** | **E2 power, in-sample 1,762** | min N for 80% |
|---|---:|---:|---:|---:|
| published (undecayed) | 2.81 | **0.999484** | **1.000000** | 250 |
| **REGISTERED (half)** | **1.40** | **0.743533** | **0.959721** | **1,006** |
| quartered | 0.70 | **0.257809** | **0.458773** | 4,021 |

**E2 equals E1 to five decimal places, and that is a finding rather than a
copy.** E2's permutation clusters on session date, so the session is the
independent unit: a session of `k` trades with mean `μ` and dispersion `σ` has
session mean `kμ` and session dispersion `σ√k`, so the ratio is `√k·(μ/σ)` and
**`σ` cancels**. **Section 9's premise that E2's power needs a per-trade
dispersion input is falsified**, and Section 9's own rule applies.

**Every cell carries the Amendment 11 caveat**: the dispersion input comes from a
**post-holdout** regime and may misstate in-sample dispersion in either direction
by an unmeasured, unbounded amount.

### Software

| figure | value |
|---|---|
| tests | **410 passing** |
| mypy strict | **clean, 56 source files** |
| mutations applied to real source | **16**, **0 harness failures** |
| guards | every one exercised by a mutation or a boundary fixture |

---

## The three structural doubts, registered as part of the claim

1. **Publication.** Published openly in 2024 and popularized commercially.
   McLean and Pontiff measured **58 percent post-publication decay across 97
   predictors from 80 studies** (carried).
2. **Cost.** The index version's **entire gross edge measured smaller than a
   realistic slippage assumption** (carried). The registered central entry
   assumption of 0.020 USD/share sits **0.002 below** the replication's measured
   break-even.
3. **Regime.** **76 percent of the replication's filtered profit came from 2022
   alone**, and the filter lost money in 2017, 2020 and early 2023 (carried).

**The source result is a single, unreplicated, in-sample result produced by
authors who sell day-trading education.**

---

## Open operator items — there are exactly four, and one is now the binding one

**Both original items are discharged.** The two vendor credentials exist and both
authenticate; the Section 13 operator prior is filled at **0.30, `INDEPENDENT`**
(Amendment 5), which satisfies **Section 10 clause 2**. **Item 3 was added by the
amendment pass of 2026-08-29.**

1. **A third feed on a genuinely different upstream.** The two feeds this
   repository holds **share an upstream** — the ratio IQR is **0.46 percentage
   points wide over `n = 100` pairs**, which two independent consolidations would
   not produce. So a cross-vendor agreement `PASS` establishes that **two
   redistributors of one upstream agree**, and **it is not the Concretum test**:
   Concretum's **226,000 to 726,000 USD** spread is a spread *across upstreams*
   (carried, C-13). **ADR-022.**
2. **A costed decision on the Massive tier.** Massive's free tier reaches only
   **2024-08-29**, so the agreement gate covers **459 of 875 holdout sessions and
   none of the 1,762 in-sample sessions**. A paid tier would buy that scope back
   and **nothing else** — Alpaca already covers the registered windows at zero
   cost. The monthly figure is **near 29 USD, carried, never measured** (C-18),
   and **the reach a paid tier actually delivers is not recorded as a number**,
   because that would be a pricing-page figure. **The honest way to get it is one
   month's spend and a second bisection.** **Amendment 8.**

3. **Retire SL-3, or accept it.** **`REGISTRATION.md` §11.1, Amendment 12.**
   Cross-vendor agreement covers **459 holdout sessions and 0 in-sample
   sessions**, so **all 1,762 in-sample sessions rest on a single unverified
   feed**, and **a PASS computed on the in-sample window is conditional on that
   one vendor's rendering of it being faithful — a condition this repository
   holds no measurement supporting.** This is the Concretum exposure, and it is
   the one that cannot currently be retired for the in-sample window. **Two
   routes, neither chosen here and neither costed here:**
   **(a)** a reference credential whose tier reaches **2016-01-04**, which
   retires SL-3 **on measurement** — this is item 2 widened, since item 2 buys
   back only the holdout overlap; **(b)** **explicit operator acceptance** that
   the in-sample window is single-sourced, which retires nothing by measurement
   and is **a decision, not a finding**. **ADR-028.**

4. **Choose a route for the collapsed E2 — and this one is different from the
   other three, because it does not wait for anything.** **Amendment 21,
   ADR-034.** The measured pessimistic shift of **0.041455 USD/share** exceeds
   the implied central mean of **0.040386** at the registered 1.40 assumption,
   so the pessimistic-cost mean is **−0.001068**, **E2 power is 0.043277** and
   **joint power collapses with it — no session count reaches 80 percent.**
   **Three routes, none chosen here:**
   - **(a) A narrower verdict scope conditional on central costs alone**, with
     E2 demoted to a **named secondary**. E1 is powered at **0.832450**. The
     verdict would then say only that the rule cleared its bar under **central**
     cost assumptions — **and that is precisely the thing Section 1's structural
     doubt 2 says matters most**, so the registration would have to say so where
     the verdict is stated.
   - **(b) Narrow the registered cost band on measured execution evidence.** The
     pessimistic entry figure of 0.040 USD/share is **carried and registered,
     never measured.** Real fill data would let the band narrow on evidence.
     **This repository holds no such evidence, has no broker credential, and none
     is planned.** A real route, not currently open.
   - **(c) Close H1 as `untestable-at-achievable-power`** under its own
     registered cost assumptions — **the fourth closure kind already in the house
     record**, and a **legitimate documented negative** about the design rather
     than about the world.

   **None of the three depends on the 2026-09-12 bar-integrity calendar**, so
   this decision can be taken today.

**Items 1 to 3 are not required for the ladder to continue, and the binding
constraint there is a calendar: the earliest eligible re-pull is 2026-09-12.
Item 4 is not on that calendar at all.**

---

## Reading order for a fresh session

`CLAUDE.md` → `REGISTRATION.md` §0 and §8–10 → `HYPOTHESES.md` →
`docs/HANDOVER.md` → the last entry of `progress.md`.

## Commands

    make install     create the venv and install
    make lint        ruff format --check and ruff check
    make typecheck   mypy strict
    make test        pytest
    make all         the gate
    make guards      the structural guards alone
    make mutations   the mutation harness
