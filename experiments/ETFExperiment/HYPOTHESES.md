# Hypothesis register

**Read this before proposing any new hypothesis on ETF flow prediction.**

This file exists to prevent **retrying a settled question because the number
that closed it is buried**. Nobody remembers six weeks later that a free flow
source's publication lag measured 75 days when its own page described the data
as daily, or that a next-day coefficient halved on the author's own extended
sample before anyone tried to trade it. `report.md` runs stage-sectioned, each
section written for the moment it landed rather than for someone reading months
later, and a closure buried on line 2,700 of a report is a closure nobody will
find.

Every entry carries the claim, the registration pointer, the registered bars,
the power assumption with its rationale, the priors, and — where closed — the
measured figure that decided it, the sample it rests on, and **what would
reopen it**. That last field is the one that matters, because it distinguishes
the kinds of closure this house record has produced, and confusing them is the
expensive mistake.

**This file contains no analysis. It records what the registration and the
sealed read establish.**

## The closure kinds, stated so a future closure can be typed correctly

Three already stand in the house record:

- **Cost-bound.** A real signal exists but is smaller than the cost of
  capturing it. **Reopens at a materially lower fee tier**, and a better model
  could matter *if* costs fell. (MLCryptoEngine H1: 3.31 bps gross capture
  against an 80.00 bps round-trip maker cost, n = one day, later shown to range
  −2.44 to +3.05 bps across four days.)
- **Signal-absent.** There is nothing to capture. **Does not reopen on a better
  model, a better feature set, or lower fees.** Model quality was never the
  constraint. (MLCryptoEngine H11: 0 of 40 registered cells pass, best deflated
  Sharpe 0.499 against a 0.95 bar.)
- **Unmeasurable-on-available-data.** The question is well posed and the data
  needed to answer it does not exist freely. **Reopens on a data threshold, not
  on a revisit** — the threshold is stated numerically at closure.
  (MLCryptoEngine H10; and H11's class B, whose binding constraint was a
  **measured 75-day publication lag**, reopening only at ≤ 2 days with ≥ 3
  years of history.)

**This repository may produce a fourth**, and it is named here in advance so it
is not mistyped as one of the three above:

- **Untestable-at-achievable-power.** The signal may be real and the data may
  be obtainable, and the registered design still cannot resolve the effect at
  the sample size reachable by the registered deadline. **Reopens only on a
  materially larger achievable sample or a differently powered design, each
  requiring its own registration** — never on more analysis of the same days.
  This is the NPDExperiment shape, and InsiderExperiment produced it before
  measurement: MDE 49.35 bp per month against a registered BLOCKED floor of 40,
  closed on power alone, the cheapest finding in the house record.

---

## Register

### H1 — ETF flow prints predict the next day's BTC return, net of a Hyperliquid round trip

> A daily rule that takes a directional Hyperliquid BTC perp position after a
> US spot Bitcoin ETF net flow print, using only the value published and
> timestamped before the entry anchor, earns a positive return net of costs
> over the out-of-sample period beginning 2025-05-01.

| | |
|---|---|
| **Status** | **OPEN — collection armed under a partially fired Section 0.** Seeded 2026-08-28 at Stage A.0 before any network call; updated the same day at Stage A.2 Task 5. **GO is eliminated and closed; the remaining DEGRADED-vs-BLOCKED choice awaits one measurement, earliest 2026-09-22.** |
| **Registration** | `REGISTRATION.md`, Sections 0–14. Section 0 (the outcome map) and Sections 1–12 were each committed before any network call; the amendment log is append-only. |
| **The joint claim** | Not "does the published relationship exist" but "does enough of it survive publication, decay, and after-the-close information timing to clear a round trip." Both structural doubts are part of the hypothesis (Section 1), not caveats: the signal was **published openly in April 2026**, and **the print lands after the US close the same-day return is measured against**, so the same-day leg is untradable by construction and only the next-day leg is testable here. |
| **Registered bars** | Two co-primaries at **alpha_adj = 1 − 0.95^(1/2) = 0.0253205655** each, **both** required for the Stage B GO row. **E1**, exact permutation test on the rank correlation between the admissible as-printed signal for day D and the next-day return, over all admissible days, one-sided positive. **E2**, mean net return per trade under the Section 4 rule at T = 100M USD, exact one-sided lower bound above zero by permutation, at the **9 bp central cost band** with **measured** funding, reported at 3 and 18 bp beside. |
| **Power assumption, and its rationale** | **Registered at a rank correlation of 0.09 — half the published next-day effect.** The published Newey-West t 3.12 over n = 313 trading days implies ρ ≈ 0.18. The halving is **not discretionary**: the author's own extended-sample IV estimate falls from **0.41 to 0.20 percent per 100M USD** (n = 563 days against 313), and the independent 90-day rolling correlation fell from a **February 2026 peak of 0.68 to 0.16** by 2026-05-14, inside the test window. Registering at the undecayed figure would register an assumption the pre-existing evidence already contradicts. Powers at **0.18** and at a quartered **0.045** are computed and reported beside it as the honest range. |
| **The measurement that decides this repository** | **Not the return. The publication lag and the revision rate** (A.1 Tasks 3 and 4). The MLCryptoEngine H11 precedent: a free flow source with a **measured 75-day publication lag** and whole-file regeneration that revised past rows killed the last flow hypothesis this project ran, and **the class died on the lag, not on the model**. Here the lag and the revision rate are registered as first-class measurements before any model exists. |
| **Assistant prior** | **0.10** on a real capturable edge existing here, recorded 2026-08-27 in chat, before any census. Context, never the operator's number. |
| **Operator prior slot** | **Reserved, empty.** Accepted format: a probability in [0, 1] followed by `(independent)` or `(adopted)`; nothing else parses. **The empty slot blocks Stage B structurally** (`etf.registration_check.require_operator_prior`, `tests/test_registration_check.py`). The NPDExperiment Amendment 0 lesson stands: an adopted prior corrupts the calibration ledger, and the assistant's 0.10 may not be copied into it. |
| **Registered expectation** | **DEGRADED**, stated in Section 0 before any data existed. Under DEGRADED a Stage B FAIL establishes that the effect is not present at its published magnitude, and cannot distinguish a decayed effect from no effect at all. |
| **Section 0 verdict** | **Partially fired 2026-08-28 (Amendment 3).** **GO eliminated**: as-printed observability cannot pass in full — archive capture density is **11 of 333 = 0.0330** against a 0.60 bar, and the captures that would restore it do not exist and cannot be created. **BLOCKED does not fire on power**: E1 reaches **0.6105** at the published magnitude at the achievable count by 2027-03-31, against a 0.50 floor — the Section 0 residual band, registered as DEGRADED before any data existed. **The remaining choice turns on the forward revision-integrity leg alone**, whose earliest completion is **2026-09-22** (15 US trading days from arming). PARTIAL → DEGRADED; FAIL → BLOCKED. |
| **Measured figures, each with its n** | Flow source: **676 date rows**, 336 out-of-sample, **333 printed**. Per-row publication timestamp served by neither surviving source (**n = 2 of 2**); no publication time documented at all. Independent cross-check **315 of 333** within 2%. Rate ceilings: **none found** at or above the 1.0 s floor across **96 requests**, all 200. Hourly candles: a **rolling 5,001-row window** reaching back to 2026-02-01T11:00Z and sliding one hour per hour (**n = 17** probes). Archive density **11/333 = 0.0330**, failing on crawl rate (**0.316 mementos/day**), not on the window — an unbounded window reaches only **112/333**. Retro revision **0 revised / 0 sign flips / 0 threshold crosses on n = 11**, below the registered minimum of 30. Retro cohort **8 days**. Census **336 rows, 11 admissible** (53 too-late, 243 no-capture, 25 served-no-value, 3 no-printed-value, 1 fetch-failed). Sealed substrate **142/333** days covered at 0.95/0.95. Pre-period inputs: daily sd **0.027431** (n = 475), mean hourly funding **0.00002226** (n = 11,423). |
| **Minimum N for E1** | **237** at the published 0.18; **845** at the registered 0.09; **3,776** at the quartered 0.045. **Both Section 9 sanity anchors held** — "near 250" and "high hundreds to low thousands". |
| **The deadline finding** | Recorded as distinct from the verdict. Section 10 needs **N = 237** at the assumption a DEGRADED would fire on. At the measured forward accrual rate, **achieved N = 237 arrives around 2027-07-26 — roughly four months past the registered 2027-03-31 deadline**, against a projected **163** at the deadline. **The power floor is cleared; the deadline is not.** If this closes, the type is **untestable-at-achievable-power**, arriving through the calendar rather than the arithmetic. |
| **Working** | `REGISTRATION.md`; `report.md` (stage-sectioned); `docs/ACCESS.md`; `DECISIONS.md`; `progress.md`. |
| **What would reopen it** | _Not applicable while OPEN._ On closure the field takes numeric thresholds, not intentions. The three that are already visible: **(a)** a flow source serving a **per-row publication timestamp**, which would remove the dependence on this repository's own capture cadence entirely; **(b)** an archive or mirror with **at least 60 percent** pre-anchor capture density over the test window, which is what the retro cohort died on; **(c)** a registered deadline beyond **2027-07**, or a design whose minimum N is under **163**, which is what the deadline finding turns on. None of the three is a better model, and none reopens on more analysis of the same days. |

---

## The register's rules, stated once

1. **The registration is append-only.** Nothing above an amendment line is ever
   edited, and an amendment states exactly what data existed when it was made.
2. **The anchor moves once, by one rule.** Section 3's provisional 08:00 UTC
   anchor moves only on the A.1 Task 3 measured 95th percentile first-print
   time, by amendment, before any admissibility count is final.
3. **A later value is never substituted for an as-printed one.** Where they
   differ the day is flagged `revised` and the difference recorded.
4. **No accrual, coverage, lag, retention, revision, or capture-density figure
   is registered before it is measured** (Section 14.7). The NPLExperiment H3
   correction governs: a planning number of 9.4 events per month entered a
   registration and measurement falsified it at 0.5 (n = 3 over 182 days),
   killing a hypothesis on a figure rather than on the world.
5. **Stage B opens the sealed outcomes exactly once**, behind a latch written
   first, recording module hashes; every value inside the read is quarantined
   from any successor code path by AST pin and by test.
6. **A closure is typed** as one of the four kinds above, with the number that
   decided it and its n in the same sentence.
