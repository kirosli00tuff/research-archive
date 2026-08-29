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

**E2 power: `Absent` in all nine cells** — Section 9 restricts its dispersion
input to the pre-period carve-out, and no vendor serves one.

### Software

| figure | value |
|---|---|
| tests | **270 passing** |
| mypy strict | **clean, 46 source files** |
| mutations applied to real source | **10**, **0 harness failures** |
| guards | **7 standing + 4 repo-specific**, every one exercised by a mutation or a boundary fixture |

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

## Open operator items — there are exactly two, and neither blocks the ladder

**Both earlier items are discharged.** The two vendor credentials exist and both
authenticate; the Section 13 operator prior is filled at **0.30, `INDEPENDENT`**
(Amendment 5), which satisfies **Section 10 clause 2**.

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

**Neither is required for the ladder to continue. The binding constraint is a
calendar: the earliest eligible re-pull is 2026-09-12.**

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
