# A.2 TASK 1 — the session calendar, computed

**Built 2026-08-29 from a recorded rule source** — the NYSE published
holiday and early-closing schedule, encoded as rules in `orb.calendar` rather
than downloaded as a list, so the calendar is reproducible without a vendor.
**Every session carries a DST-aware Eastern anchor.** This module reads no price.

## Sessions per calendar year, 2016-01-04 to 2026-06-30

| year | sessions | half sessions | note |
|---|---:|---:|---|
| 2016 | 252 | 1 | window opens 2016-01-04 |
| 2017 | 251 | 2 |  |
| 2018 | 251 | 3 | includes the 2018-12-05 closure |
| 2019 | 252 | 3 |  |
| 2020 | 253 | 2 | leap year, 253 sessions |
| 2021 | 252 | 1 |  |
| 2022 | 251 | 1 |  |
| 2023 | 250 | 2 |  |
| 2024 | 252 | 3 |  |
| 2025 | 250 | 3 | includes the 2025-01-09 closure |
| 2026 | 123 | 0 | window closes 2026-06-30, partial year |
| **total** | **2637** | **21** | n = 11 calendar years |

## The registered windows, computed against the registration's approximations

| window | dates | registration says | **computed** | delta |
|---|---|---:|---:|---:|
| in-sample | 2016-01-04 to 2022-12-30 | ~1,760 | **1762** | **+2** |
| holdout | 2023-01-03 to 2026-06-30 | ~880 | **875** | **-5** |
| full window | 2016-01-04 to 2026-06-30 | — | **2637** | — |

## Full-day closures, per year

| year | scheduled closures on a weekday | unscheduled |
|---|---:|---|
| 2016 | 9 | — |
| 2017 | 9 | — |
| 2018 | 9 | 2018-12-05 (national day of mourning, George H. W. Bush) |
| 2019 | 9 | — |
| 2020 | 9 | — |
| 2021 | 9 | — |
| 2022 | 9 | — |
| 2023 | 10 | — |
| 2024 | 10 | — |
| 2025 | 10 | 2025-01-09 (national day of mourning, Jimmy Carter) |
| 2026 | 10 | — |

## Half sessions, every one in the window

| date | reason |
|---|---|
| 2016-11-25 | day after Thanksgiving |
| 2017-07-03 | 3 July |
| 2017-11-24 | day after Thanksgiving |
| 2018-07-03 | 3 July |
| 2018-11-23 | day after Thanksgiving |
| 2018-12-24 | Christmas Eve |
| 2019-07-03 | 3 July |
| 2019-11-29 | day after Thanksgiving |
| 2019-12-24 | Christmas Eve |
| 2020-11-27 | day after Thanksgiving |
| 2020-12-24 | Christmas Eve |
| 2021-11-26 | day after Thanksgiving |
| 2022-11-25 | day after Thanksgiving |
| 2023-07-03 | 3 July |
| 2023-11-24 | day after Thanksgiving |
| 2024-07-03 | 3 July |
| 2024-11-29 | day after Thanksgiving |
| 2024-12-24 | Christmas Eve |
| 2025-07-03 | 3 July |
| 2025-11-28 | day after Thanksgiving |
| 2025-12-24 | Christmas Eve |

**n = 21 half sessions** across 11 calendar years. All are
**excluded from the sample and counted**, per Section 2.

---

## The second-source cross-check — **not completed, and not fabricated**

The task specifies: *"Cross-check the total against a second source and record
any disagreement rather than reconciling it."*

**The cross-check was not completed, and the reason is recorded rather than
papered over with a remembered number.** Every vendor that serves a machine-
readable US equity trading calendar is one of the nine measured at A.1 TASK 1,
and **all nine are either refused by terms or refused without a credential**.
Writing a comparison table here from recollection would be recording a figure
this repository did not measure, as though it were a source — which is exactly
the failure standing rule 4 names, and exactly the failure the NPLExperiment
correction closed a hypothesis over.

**Status: `Absent(not_yet_measured, "no second calendar source reachable")`.**
It is an open item, cleared by the same credential that clears A.1 TASK 3 and
A.1 TASK 4.

### What was done instead — an internal cross-check that is real

The session count is derived **twice, by different arithmetic**, and the two
derivations must agree for every year:

1. `session_counts` walks every calendar day in the window, skipping weekends
   and closures.
2. `test_session_count_equals_weekdays_minus_weekday_closures` computes
   **weekdays in the year minus closures falling on a weekday**, independently.

**They agree on all 10 complete years, n = 10.** Worked for 2018, by hand:
**261 weekdays − 10 weekday closures = 251 sessions.** The ten are New Year's
Day (Mon 1 Jan), MLK (Mon 15 Jan), Washington's Birthday (Mon 19 Feb), Good
Friday (Fri 30 Mar), Memorial Day (Mon 28 May), Independence Day (Wed 4 Jul),
Labor Day (Mon 3 Sep), Thanksgiving (Thu 22 Nov), **the 5 December national day
of mourning for George H. W. Bush**, and Christmas Day (Tue 25 Dec).

Six further structural checks hold the calendar in place, and each is a real
assertion rather than a smoke test:

| check | what it pins |
|---|---|
| no session on a weekend or a closure | n = 2,637 sessions |
| every early-close date is present **and** typed `HALF` | n = 21 |
| Juneteenth absent before 2022, present from 2022 | the rule change is dated |
| Saturday holidays observed Friday, Sunday holidays observed Monday | 3 Jul 2020, 2 Jan 2023 |
| Good Friday **computed**, not listed | 2016, 2018, 2024, 2026 |
| the Eastern offset moves across **both** DST transitions | −300 / −240 on real sessions |

**And one that ties the calendar to the carve-out:** the opening-range start of
the **first in-sample session** equals `CONFIG.pre_period_end_ms` exactly. The
calendar and the pre-period boundary are therefore the same instant computed two
independent ways — one from a NYSE rule set, one from a registered literal.

---

## Two disagreements with the registration, recorded not reconciled

| quantity | registration | computed | delta | consequence |
|---|---:|---:|---:|---|
| in-sample sessions | ~1,760 | **1,762** | **+2** | none; the window is already powered for t = 3.0 |
| holdout sessions | ~880 | **875** | **−5** | **carried into A.2 TASK 4**; the power computation uses 875, not 880 |

**The holdout shortfall is the one that matters.** At the registered assumption
the Section 9 arithmetic gives `t = 0.0882 × sqrt(n)`. At the stated n = 880
that is **2.616**; at the computed **n = 875** it is **2.609**. Both sit below
the registered 3.0 hurdle and above the 2.50 holdout gate, so **no verdict row
moves** — but **A.2 TASK 4 computes on 875, and the computation wins over the
prompt's figure**, as Section 9 requires.

---

## The corporate-actions substrate

Built at `orb.actions`: splits, reverse splits, symbol changes, delistings and
listings, each with its effective date, recorded to an append-only fsynced
ledger. **It reads no price.** A split ratio is stored because it *identifies*
the event, never because anything in Stage A divides a bar by it.

**Population status: `Absent(not_yet_measured, "no credentialed vendor")`.**
Counts per kind, delistings per year, and the delisted-name census of A.1 TASK 4
all require a vendor reference endpoint, and none is reachable. **No count is
guessed and no zero is written**, because a zero that was measured and a zero
that was never looked for are different facts and `orb.absence.Absent` refuses
to let them merge.

**What is built and armed:** `collision_keys` produces the session-ticker keys
where a split or reverse split lands on a stored session, and hands them to the
sealed comparator so that a measured bar revision is **attributed** to a
corporate action rather than merely coinciding with one. **A split landing on a
stored session is the event most likely to trigger a silent vendor rewrite**,
which is why A.3 TASK 2 watches it daily rather than discovering it.
