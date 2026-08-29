# HANDOVER.md — for a fresh session

**Read this before touching anything.**

## What this repository tests

**One hypothesis, H1.** Among US common stocks with **elevated opening relative
volume**, a **breakout of the first 5-minute regular-session range** predicts
continuation to the session close, **net of modeled costs**, out of sample from
**2023-01-03**.

It is a **joint claim about the selection and about the breakout**, and it can
fail on either half while the other is real. In the source study the **selection
by relative volume, not the breakout, did almost all the work**: the plain
broad-universe rule returned **3.2 percent annually at Sharpe 0.48 — below
passive** — while the top-20-by-relative-volume restriction returned **more than
1,600 percent at Sharpe 2.81** (both carried, unreplicated, in-sample, from
authors who sell day-trading education).

**Stage A never trades, never touches capital, and never reads an outcome
value.** A documented negative is a valid and expected outcome.

## What Stage A measured

**Section 0 fired `PENDING_ACCESS` on 2026-08-29. Nothing is armed. Nothing is
closed. H1 is OPEN.**

| finding | figure | n |
|---|---|---|
| **vendors serving a 1-minute RTH bar** | **0 of 9** | 9 vendors, 15 robots fetches, 25 probes |
| refused by terms | 4 — stooq and yfinance publish `Disallow: /`; EODHD and Nasdaq disallow the API path | 9 |
| require a credential | 5 | 9 |
| **bar revision rate** | **`Absent`** | 0 |
| **cross-vendor first-5-min agreement** | **`Absent`** | 0 |
| **delisted names served** | **`Absent`** | 0 |
| sessions in the window | **2,637**, of which **21** half | 11 years |
| holdout sessions | **875** (registration said ~880) | — |
| **E1 power at the registered 1.40** | **0.7435** — below the 0.80 GO floor | 875 |
| **E1 power at the published 2.81** | **0.9995** — above it | 875 |
| minimum N for 80% at 1.40 | **1,006** — a shortfall of **131** | — |
| E2 power | **`Absent`** — dispersion is carve-out-only and no vendor serves one | 0 |
| **FINRA TAF, carried vs measured** | **0.000166 vs 0.000195 — carried is stale** | 1 |
| cost of a round trip, central band, 50 USD name | **≈ 0.0386/share close exit, ≈ 0.0686 stop exit** against a carried gross edge of **0.070** | — |
| tests / mypy / mutations | **270 passing** / **clean over 46 files** / **10 mutations, 0 harness failures** | — |

**The counterfactual, computed: had bar integrity passed in full, the same power
inputs fire `DEGRADED`** — exactly what Section 0 predicted in writing before any
measurement existed.

## What is armed

**Nothing.** A.3 arms only on GO or DEGRADED, and `PENDING_ACCESS` is neither.

- The collector, the corporate-actions watcher, the systemd units and the latch
  machinery are **written, tested and committed**.
- **No timer is enabled.** `systemctl --user list-timers` shows no `orb-*` unit.
- `python -m orb.cli daily` and `... actions` **refuse loudly and exit 78**,
  because *a collector that runs and stores nothing looks identical in a log to
  one that ran and found nothing.*

## What the next decision is, and when it arrives

**The next decision is not a design question. It is one operator action.**

### Open operator item 1 — two vendor credentials

**Two free-tier credentials, from two different vendors** — a primary and a
secondary, so the cross-vendor agreement measurement has two feeds to compare.
**This repository will not create accounts on the operator's behalf.**

`docs/ACCESS.md` records the recommended pair with its reasoning, chosen on **the
two integrity questions and not on price**: does the tier serve **delisted
names**, and does it **retroactively rewrite already-served bars**. Recommended:
**Polygon/Massive** as primary (the only probed vendor publishing a
delisted-ticker reference endpoint and minute aggregates on one host), with
**Alpaca or Tiingo** as secondary. **If the two share an upstream consolidated
tape, the agreement measurement is labelled as measuring a redistribution
pipeline rather than two independent feeds**, and the selection ADR must say so.

Keys go in `.env`, which is git-ignored. **`.env.example` gains key *names* only.
No key is ever committed.**

### Open operator item 2 — the Section 13 prior slot

**Empty and reserved.** The assistant prior of **0.15** (recorded 2026-08-28) sits
beside it. **The empty slot blocks the Stage C latch structurally**, and the latch
refuses an empty or unlabelled slot at runtime.

**Do not fill it from the assistant's number.** NPDExperiment Amendment 0: an
adopted prior corrupts the calibration ledger. If the operator's number happens
to equal 0.15 it is recorded `independent` **only** if reached without reading
the assistant's, and `adopted` otherwise. **The label is part of the datum.**

### When the next real evidence arrives

**Credential date + ~1 day + 14 calendar days, at the earliest.** A.1 TASK 3
registers a **≥ 14 calendar-day wait** between the probe pull and the identical
re-pull, because that wait is what makes the revision measurement mean anything.
**The wait has not started and cannot start until a credential exists.**

## What a fresh session must read before touching anything

1. **`CLAUDE.md`** — the operating manual. Standing rules 1–14, the blindness
   field lists stated exactly, the carve-out with its enforcement site.
2. **`REGISTRATION.md` §0** (the outcome map and its fixed precedence),
   **§8–10** (the co-primaries, the power method, the latch), **and all four
   amendments**.
3. **`HYPOTHESES.md`** — H1's state, the five closure kinds, the ten culls, and
   the two parked entries.
4. **`docs/ACCESS.md`** — why 0 of 9 vendors are usable, and what unblocks it.
5. **`progress.md`, last entry** — where the session stopped.

## Rules that bind whatever the task is

- **`REGISTRATION.md` is append-only.** Nothing above an amendment line is ever
  edited. An amendment is dated, reasoned, and **states exactly what data existed
  when it was made**.
- **Never point `orb.verdict`, `orb.signal` or `orb.universe` at a real bar
  before the Stage C latch.** They are latched modules; a guard walks every
  import and fails if a Stage A module reaches one.
- **A second read of either window voids the hypothesis.** The latch refuses it,
  and a failed latch attempt leaves no file so a refusal never consumes the
  window's one read.
- **Measured beats documented**, always, and a vendor page is documented.
- **Absence is a recorded state.** Do not write a zero where a measurement is
  missing; `Absent` refuses to become one.
- **Every figure travels with its n in the same sentence.**
- **Terms of service bind.** `stooq.com` and `query1.finance.yahoo.com` publish
  `Disallow: /`. **Do not fetch them.**
- **`make all` is the gate.** Commit at every task boundary and push.

## The thing most likely to go wrong next

**Being handed a credential and rushing to the model.** The two measurements this
repository turns on — **bar revision** and **cross-vendor agreement plus delisted
coverage** — come *first*, and a FAIL on either fires **BLOCKED** at perfect
power. The Concretum finding is why: **identical opening-range code, four
vendors, identical dates, parameters and starting capital, final portfolio values
from 226,000 to 726,000 USD.** If bar integrity fails here, **BLOCKED is the
correct and cheap answer**, and it is a documented answer rather than a failure
of process.
