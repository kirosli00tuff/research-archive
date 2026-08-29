# ORBExperiment

**A measurement-only test of one hypothesis: among US common stocks with
elevated opening relative volume, a breakout of the first 5-minute
regular-session range predicts continuation to the session close, by enough to
clear modeled commissions, fees, borrow and slippage, out of sample from
2023-01-03.**

**Stage A never trades, never touches capital, and never reads an outcome
value.** There is no broker credential, no order, no position, and no stage in
which one is planned. **A documented negative is a valid and expected outcome.**

**The measurement that decides this repository is not the return. It is bar
integrity.** If the vendor's own bars are not stable and not consistent, no model
here can mean anything, and **BLOCKED is the correct and cheap answer**.

---

## Status: Section 0 fired **PENDING_ACCESS** on 2026-08-29

**Nothing is armed. Nothing is closed. H1 is OPEN.**

**Measured: 0 of 9 vendors serve a 1-minute regular-session US equity bar to this
repository.** The two that serve keylessly both publish `User-agent: *
/ Disallow: /`; two more disallow the exact API path a collector needs; and the
five whose terms permit collection all refused without a credential. **The
integrity measurements this repository turns on cannot run**, so Section 0
reports on **access** rather than pretending to report on the hypothesis.

**Had bar integrity passed in full, the same power inputs fire `DEGRADED`** —
which is exactly what Section 0 predicted **in writing, before any measurement
existed**.

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

## Open operator items — there are exactly two

1. **Two free-tier vendor credentials, from two different vendors** (a primary
   and a secondary, so the cross-vendor comparison has two feeds). This
   repository will not create accounts on the operator's behalf. See
   `docs/ACCESS.md` for the recommended pair and the integrity reasoning.
2. **The Section 13 operator prior slot**, which is **empty and reserved**. The
   assistant prior of **0.15** is recorded beside it with its date. **The empty
   slot blocks the Stage C latch structurally.** Do not fill it from the
   assistant's number — an adopted prior corrupts the calibration ledger.

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
