# registrations/H2/REGISTRATION.md — the age-contrast pair

> **STATUS: REGISTERED 2026-08-28, BEFORE ANY NEW NETWORK CALL.**
>
> At the moment this document was committed, this session had sent **zero
> requests**: the request ledger's last rows are the H1 collectors' final
> passes (2026-08-28T02:05Z). **No fresh-cohort eligibility had been
> computed, no fresh control had been assigned, no conditioning rate had
> been measured, no successor power number existed, and no outcome value
> beyond the spent H1 read has ever been parsed by this repository.**
>
> **From this point the specification is closed.** Changing anything here
> requires a dated amendment appended at the bottom, stating what data
> existed when it was made. Nothing above an amendment line is ever edited.
>
> **Disclosure.** Every carried figure below is **generating-sample-derived**
> — computed by the spent H1 Stage B read on the 312 retro events and 175
> effective pairs — and is usable as a power assumption only, never as a
> successor verdict input (standing rule 12; root REGISTRATION.md Amendment
> 4; `npl.register.generating_sample`).

---

## 0. The outcome map — it judges collection feasibility, never returns

Fired in register Stage A.2 Task 5 by `npl.register.cull.
fire_hypothesis_section0` (pinned by tests with boundary fixtures on the
registered floors), from counts, rates, and timestamps only:

- **GO:** both co-primaries of Section 8 reach **at least 80 percent power
  at alpha_h** under the registered assumptions, at the achievable pair
  count by **2027-03-31**.
- **DEGRADED:** the weaker co-primary lands between **50 and 80 percent**.
  Collection proceeds; recomputed power is stated beside the registered
  target at every later reading.
- **BLOCKED:** either co-primary **under 50 percent power** at the
  achievable count by 2027-03-31 (evaluated inside the register cull's
  k/alpha fixed point, Section 9). Nothing armed for H2.

## 1. The hypothesis

**H2.** A pair opened at the registered entry anchor (Section 3) — **short
the young listing, long its funding-matched elder on the same dex, at equal
constant notional** — held 30 days, earns a **positive net return**,
because listing-age drift exceeds what funding matching already prices.

This is the residual H1 measured and could not trade: on the generating
sample, young perps underperformed their funding-matched controls in
**114 of 175 pairs (65.1 percent, p = 3.767e-05)** with a mean paired
**price differential of +6.43 points** and funding differential **+0.88
points** over 30 days. The naive short failed its bars (H1, CLOSED); the
pair isolates exactly the differential that passed. All four figures are
generating-sample-derived and appear here as assumptions only.

## 2. The universe and event rule

**Every fresh event**: the **62 pending-at-closure events** of the H1
census **where windows are servable** (verified per event in register A.1
Task 3; an event out of retention is `excluded_ineligible` with its
reason, counted), **plus all forward births on every dex** — main dex and
every HIP-3 builder dex, birth-ordered, **no attention or performance
input**. Event types tagged exactly as H1 Section 2 / Amendment 1
(mechanical hyperp rule included); **the hyperp pre-conversion phase is
excluded from primaries as before**. **No generating-sample event enters
under any condition** (`data/state/generating_sample.json`, refusal by
`npl.register.generating_sample`, pinned by test).

## 3. Listing date and entry anchor

H1 Section 3 with Amendment 1, verbatim by reference: listing day from the
first served 1d candle cross-checked against the first archived funding
row at ±1 day; epoch censoring; the mechanical hyperp tag with the event
date at the funded phase's start. **Entry anchor: the second daily close**
(00:00:00Z of listing day + 2). Both legs of the pair enter at the same
anchor.

## 4. The outcome definition

**Pair net return over horizon H, four fills, constant notional per leg:**

    pair_net(H) = young_leg_net_short(H) + elder_leg_net_long(H)

    young_leg_net_short(H) = − price_return(young, entry → entry + H)
                             + Σ hourly funding a constant-notional short
                               receives on the young leg over (entry, entry + H]
                             − young-leg round-trip cost (Section 5)

    elder_leg_net_long(H)  = + price_return(elder, entry → entry + H)
                             − Σ hourly funding a constant-notional short
                               would receive on the elder leg over the same
                               window (the long PAYS what the short would
                               receive)
                             − elder-leg round-trip cost (Section 5)

- **Sign conventions, stated:** the venue's hourly `fundingRate` is the
  rate longs pay shorts. **A positive rate pays the short leg and costs
  the long leg**; each leg's funding term enters with its own sign as
  written above.
- **Equal constant notional on both legs**, no compounding, no
  liquidation modelling, no rebalancing — named Stage-scope
  simplifications, as in H1 Section 4.
- **Truncation by delisting on either leg** values that leg at its **last
  served close**, retains the pair in the primaries, and flags it
  `truncated_by_delisting` with the leg named; the count travels with
  every figure it enters (H1 Section 7 rationale, verbatim).

## 5. Costs

Four fills = two round trips, one per leg, charged once per pair, by each
leg's venue class (H1 Section 5 basis, verbatim):

| pair class | central | band (low, central, high) |
|---|---|---|
| both legs vanilla main-dex | **18 bp** | 9, 18, 36 |
| both legs HIP-3 | **36 bp** | 18, 36, 72 |
| mixed (one vanilla, one HIP-3) | **27 bp** | 13.5, 27, 54 |

Bands are **half and double the central**, per the register prompt. A
leg's class comes from its own dex (a control on the main dex is vanilla
regardless of its event's class). **Forward pairs additionally record
measured touch spreads on both legs** at the entry anchor (A.3 Task 2, one
l2Book fetch per leg), **descriptive only**.

## 6. The matched control

**The H1 Section 6 rule, verbatim:** at each event entry, the control is
the perp on the **same dex, listed at least 180 days earlier, with funding
coverage (at least 95 percent of the trailing 168 hours served), nearest
by signed trailing 168-hour mean hourly funding, with replacement.** Ties
break to the earlier listing date, then coin name ascending. Pairs are
written to an append-only ledger (`data/controls/h2_pairs.jsonl`) **at
assignment time** with the entry timestamp, both trailing means, and the
candidate count. **Matching reads no row stamped after the event entry** —
the trailing-only pin (`npl.controls.PostEntryRead`) is produced by test.
An event with no eligible candidate **cannot form a pair and is excluded
from H2 entirely**, recorded `no_control_candidate`, counted (unlike H1,
where unmatched events stayed in P1/P2 — H2 has no unpaired statistic).

## 7. Horizons and deaths

**30 days primary, 90 days secondary (descriptive).** Truncation per
Section 4. **Pairs younger than their horizon at read time are pending,
never partially filled.** Both legs must satisfy the H1 coverage bars
(candles ≥ 0.90, funding hours ≥ 0.95 inside the window) or the pair is
excluded **underpowered** with its count — never a negative.

## 8. Inference

**Two co-primaries at alpha_h (Section 9), both must pass. The
intersection carries no extra multiplicity** — E2 implies a stronger
version of E1's direction, and the familywise budget is spent at the
hypothesis level by the register's alpha_h, not within it.

- **E1, the sign.** Exact one-sided sign test on the share of pairs with
  **positive net pair return** at 30 days, central costs; bar: the share
  **exceeds one half** at alpha_h. Registered power assumption: true share
  **0.65** — generating-sample-derived (P3 pair share 114/175 = 0.651).
- **E2, the economic floor.** Exact one-sided sign test on the share of
  pairs with net pair return **at or above two times the pair's registered
  central cost** (Section 5; the multiple is `h2_cost_floor_multiple` = 2.0);
  bar: the share **exceeds one half** at alpha_h. Registered assumption:
  true share **0.60** — generating-sample-derived (one notch under E1's
  0.651, reflecting that the +6.43-point mean paired differential sits far
  above 2 × 36 bp while the pair distribution's spread is unmeasured).
- **Tie rule, registered now:** a pair net exactly at zero fails E1; a
  pair net exactly at the E2 floor **passes E2** (the registered bound is
  inclusive, mirroring H1's P2).
- **Named secondaries, descriptive and never verdict-bearing:** the 90-day
  versions of E1 and E2; per-dex strata; the funding-term and price-term
  decomposition of every pair; the truncated-by-delisting subgroup; and
  the backfill-versus-forward split. A statistic not named here is a
  second look and is refused.

## 9. The power method and the register cull

Exact binomial power at the registered assumptions, computed in A.2 Task 4
at **alpha_h for k = 1, 2, and 3** (alpha_h = 1 − 0.95^(1/k)), at achieved
backfillable pair N and at projected N by 2026-12-31 and 2027-03-31 using
the **measured** accrual and match rates from A.1 (the carried
generating-sample figures — 18.5 events/month, match rate 0.564 — are
stated for context and superseded by measurement). Minimum-N statements
per co-primary. **The cull** (register rule, `npl.register.cull.run_cull`):
starting from all three hypotheses, any hypothesis under 50 percent power
on a **required** co-primary at the achievable N by 2027-03-31 at the
current alpha_h fires BLOCKED and is removed; alpha_h is recomputed and
the pass repeats to the fixed point. **H2's requirement mode: all — both
E1 and E2 are required and the weaker governs.** k and alpha_h are fixed
at the cull, recorded here by amendment, never revisited after any outcome
exists.

## 10. The H2 Stage B trigger

H2's sealed read runs only when **all** of:

1. both co-primaries at or above **80 percent power at achieved eligible
   pair N** (not projected),
2. **the H2 operator prior slot (Section 13) filled and labelled**
   independent or adopted (`npl.register.priors.require_operator_prior`,
   refusal produced by test),
3. **explicit operator instruction.**

The read opens H2's sealed outcomes **exactly once**, behind its own latch,
under its own future amendment extending the blindness allowlist — which
stays at length one (the spent H1 reader) until that amendment.

## 11. The epistemic boundary

A positive result supports the claim that **the registered pair would have
cleared its bars on this fresh sample**. It is never a forward return
prediction, never an expected-value claim about future listings, and never
a trading recommendation. This stage produces no tradeable artifact.
docs/PAIR_FEASIBILITY.md (A.3 Task 6) is analysis only: no capital, no
orders.

## 12. Spend and pacing

**Zero dollars. Keyless public endpoints only.** The H1 request ledger and
its 20,000/day cap carry over unchanged; the measured per-endpoint pacing
(H1 Amendment 1, `npl.pacing`) governs every fetch; the A.1 Task 4 drift
check re-probes the ceilings and amends only if they moved.

## 13. Priors

**Assistant priors, recorded 2026-08-28 in chat, before any successor
measurement:**

- **0.25** that a real capturable pair edge exists overall.
- **0.35** that the H2 Stage B bars clear on the registered fresh sample.

**The adoption warning, standing (carried verbatim):** the NPD Amendment 0
lesson applies — an adopted prior corrupts the calibration ledger. The
assistant's numbers above are context, not the operator's number, and they
must not be copied into the slot below.

**The operator prior slot, reserved and empty:**

> Operator prior on the H2 Stage B bars clearing: _reserved, empty — only
> the operator fills this, as a probability in [0, 1] followed by
> `(independent)` or `(adopted)`. Nothing else parses._

**The empty slot blocks H2's Stage B structurally**
(`npl.register.priors`, exercised by `tests/test_register.py`).

---

## Amendments

An amendment is dated, reasoned, states exactly what data existed when it
was made, and never edits anything above its own line.

### Amendment H2-1 — 2026-08-28 — Section 0 verdict record: DEGRADED; k and alpha_h fixed

**What data existed when this amendment was made.** Counts, rates, and
timestamps only: the A.1 recovery/census/retention/drift record
(docs/ACCESS.md "Register A.1"), the A.2 eligibility ledgers
(data/eligibility/), the H2 pairs ledger (38 rows), the measured
conditioning rates, and the exact-power arithmetic
(reports/stage_a_h2/ktable_cull.json). **No outcome value of any fresh
event has been read; the H2 verdict machinery does not yet exist.**

**k and alpha_h, fixed now and never revisited after any outcome exists:**
the register cull (Section 9 procedure, `npl.register.cull.run_cull`) ran
at the k/alpha fixed point on the deadline sample sizes. Pass 1 (k = 3,
alpha_h = 0.016952): H2 required power 0.5771, H3 0.0000, H4 best cell
0.0140 — H3 and H4 fire BLOCKED. Pass 2 (k = 1, alpha_h = 0.05): H2
required power 0.7604 — fixed point. **k = 1. alpha_h = 0.05.**

**The verdict: DEGRADED. Collectors are armed for H2.** Fired by
`npl.register.cull.fire_hypothesis_section0`; every input beside it:

- Fresh cohort 62 (60 hip3, 2 vanilla), reproducing the registered
  pending-at-closure count; retention 62/62 servable; funding archives
  complete with 0 unrecoverable hours (60,010 hours).
- H2 eligibility: **38 pairable of 62** (24 `no_control_candidate`,
  counted); assignment **38 of 38** at entry, trailing-only, 0 candidates
  skipped for coverage, 16 distinct controls, pairs ledger
  `data/controls/h2_pairs.jsonl` at 38 append-only rows.
- Measured match rate 38/62 = **0.613** (xyz 36/36, main 2/2, para 0/18,
  mkts 0/4, io 0/2 — the young dexs cross the 180-day candidate age at
  deterministic dates: para 2026-09-26, mkts 2026-12-26, io 2027-02-13).
- Measured accrual **18.57 events/month** (trailing 182d, n = 113).
- **Projected pairs, by-dex measured model (governing):** 88 by
  2026-12-31, **141 by 2027-03-31** — per-dex accrual × deterministic
  pairability onsets, all A.1-measured quantities. The flat summary
  (0.613 × forward events: 72 / 106) is reported beside as sensitivity;
  **under the flat variant H2's E2 leg sits at 0.4318 at the pass-1
  alpha and the cull would fire k = 0** — recorded plainly. The by-dex
  model governs because pairability is a deterministic function of
  measured dex age (xyz measured 36/36 pairable), not a stationary share.
- **Powers at the deadline (n = 141 pairs, alpha_h = 0.05):** E1 **0.9743**,
  E2 **0.7604** — the weaker required co-primary lands in [0.50, 0.80):
  **DEGRADED**, per the Section 0 map. At achieved n = 38: E1 0.5339,
  E2 0.2897. At interim n = 88: E1 0.8530, E2 0.5289.
- **Minimum-N statements (stays-at-or-above-0.80 semantics, as H1):**
  E1 **76 pairs** at alpha 0.05 (103 at the k = 3 alpha — the register
  prompt's sanity anchors, near 67 first-crossing and 95–105 at k 3,
  bracket these; computation authoritative), E2 **169 pairs** at 0.05.
  The Stage B trigger therefore projects to achieved-pair count 169,
  reached near **2027-05/06** at the measured by-dex rates, plus 30-day
  maturity.

**Consequence.** Collection proceeds for H2 under the DEGRADED rule:
recomputed power is stated beside the registered 0.80 target at every
later reading; A.3 arms the collectors for H2 alone (H3 and H4 armed
nothing, per their own Section 0 records).

### Amendment H2-2 — 2026-08-28 — the re-arm record (register A.3)

**What data existed when this amendment was made.** Everything in
Amendment H2-1, plus the fresh plan (100 rows: 62 events + 38 control
legs) and the dark pair machinery's synthetic-fixture test record. **No
outcome value of any fresh event has been read; the pair reader has only
ever seen synthetic fixtures.**

**The re-arm, executed and verified 2026-08-28T06:21–06:23Z:**

- `systemctl --user enable --now npl-watch.timer npl-daily.timer` from
  the retained unit files. Schedules verified: npl-watch hourly at :05
  (next 07:05Z; its Persistent catch-up pass ran clean at 06:22:18Z — 11
  dexs, 0 failed, 504 instruments, 0 births); npl-daily at 01:40 UTC
  (next 2026-08-29 — today's pass ran before the H1 disarm, so
  Persistent did not double-fire). Nothing else npl is scheduled (4 npl
  units total: the two timers and their services). The AiTrader
  news-collect timer (next 15:31 PDT) and solattn-daily are untouched,
  verified in the same listing. The manual-run guard refuses while the
  timers are active, verified by invocation.
- **The watcher extension (A.3 Task 2):** on each birth, the entry-anchor
  watch pass assigns the H2 control trailing-only through the pinned
  matcher, writes the pair row, queues both legs on the fresh plan, and
  takes the two-leg l2Book snapshot inside the registered 30-minute
  window (a late pass writes a loud expired row; the 01:40Z daily pass is
  the assignment catch-up). `npl.register.forward`, pinned by tests with
  a socketless client.
- **The funding recorder (A.3 Task 3):** the daily pass advances every
  fresh-plan row's archive to min(now, entry+91d) under the soft budget,
  and seals each leg's full candle window once, at maturity (now ≥
  entry+92d) — the H1 retro-backfill shape, chosen because the venue's
  1d retention is measured-full and a write-once seal of a partial
  window would block its own completion. Backfillable-cohort checkpoints
  before the re-arm date are superseded by the mature-window seal;
  forward births checkpoint normally.
- **Checkpoints (A.3 Task 4):** +2/+32/+92 for forward events and both
  pair legs (the elder leg checkpoints on its event's schedule);
  MIN_OUTCOME_COVERAGE unchanged (0.90 candles / 0.95 funding hours);
  the H2 coverage view requires both legs (`npl.register.pairs.
  pair_covered`).
- **The dark machinery (A.3 Task 5, survivors only):** the H2 pair
  reader (`npl.register.pairs`) reproduces known answers to the digit,
  with sign pins on all four legs; the per-hypothesis latch exists for
  H2 alone (`npl.register.latches` — a BLOCKED hypothesis has no Stage B
  to latch, and asking for one refuses loudly, by test). The subset and
  conditioned readers were not built: H3 and H4 fired BLOCKED and
  nothing arms for them.

**A defect found and corrected during hardening, recorded rather than
smoothed over:** the first version of the forward-pass test let the
trail fetcher write into the real data/funding store (two fake test
coins, ELDER and NEW, accumulated ~3.6M trail seal files each before the
run was stopped). The pollution was verified test-only (neither coin
exists in any census, ledger, or plan) and removed; the fetcher now takes
an explicit funding_root, the test pins that trail seals land there and
nowhere else, and a page cap bounds the fetch loop. No experiment data
was touched.
