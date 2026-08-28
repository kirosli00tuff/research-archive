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

### Amendment H2-3 — 2026-08-28 — the two-look sequential plan, the fallback control, and the recalibrated economic floor

**What data existed when this amendment was made.** Counts, timestamps,
coverage figures, and pre-entry funding features — and nothing else.
Specifically: the A.1 recovery/census/retention record; the A.2
eligibility ledgers (`data/eligibility/`, 62 rows for H2: 38 pairable,
24 `no_control_candidate`); the H2 pairs ledger at 38 append-only rows;
the measured accrual and conditioning rates; the exact-power arithmetic
of Amendment H2-1 (`reports/stage_a_h2/ktable_cull.json`); the fresh
plan at 100 rows; the census at 504 distinct instruments across 11 dexs;
and this stage's precondition scan
(`reports/stage_a_h2/amend_preconditions.json`, PASS at
2026-08-28T06:51:10Z: `data/state/h2_read.json` absent, the registered
latch `data/state/h2_read_latch.json` absent, zero H2 outcome artifacts
under `reports/`, gates green, tree clean, origin equal to HEAD,
`npl-daily.service` inactive). **No pair net return, no candle close, and
no post-entry funding rate has been read. The H2 pair reader has seen
only synthetic fixtures.** Every figure carried below from the H1 read is
generating-sample-derived and labelled so, usable as a power assumption
only (standing rule 12).

**This amendment weakens the registered bar. It is made for calendar
reasons, on operator instruction dated 2026-08-28.** Amendment H2-1
recorded that H2's governing co-primary E2 needed **169 achieved pairs**
before its Stage B trigger could fire, reached near 2027-05/06 at the
measured by-dex accrual, plus 30-day maturity — past the registered
2027-03-31 projection deadline. Three changes below buy calendar: a
fallback control that pairs the 24 events the same-dex rule cannot pair,
a lower economic floor, and a two-look plan that creates an earlier
opportunity to stop. **Each is a weakening or a relaxation, each is
stated as such, and each was chosen before any pair outcome existed.**
Nothing here is a second look at a spent read: no H2 outcome value has
ever been parsed.

---

#### Change 1 — the fallback control rule (a relaxation of Section 6)

Section 6's rule is unchanged where it applies. **At each event entry the
control is the same-dex perp, listed at least 180 days earlier, with
funding coverage of at least 95 percent of the trailing 168 hours,
nearest by signed trailing 168-hour mean hourly funding, with
replacement; ties to the earlier listing date, then coin name
ascending.**

**The fallback, registered now:** where that same-dex candidate set is
empty — no instrument on the event's dex satisfies both the 180-day age
condition and the coverage condition — the control is **the nearest
funding-matched elder on the main dex** (`dex == ""`) meeting the same
180-day and coverage conditions, selected by the identical distance,
tie-break, and replacement rules. The fallback is consulted **only** when
the same-dex set is empty; a same-dex candidate always wins, and an event
with no candidate on either dex is still excluded, recorded
`no_control_candidate`, counted.

- **Pair type is tagged at assignment.** Every pair row carries
  `pair_type` ∈ {`same_dex`, `cross_dex`}, written at assignment time to
  the append-only pairs ledger. **The tag never filters anything.** Both
  types enter every primary statistic.
- **The `same_dex` subset is a named stratum, reported beside every
  primary figure at every look** — n, successes, and share for E1 and E2,
  descriptive, never verdict-bearing. The registered reason to report it:
  a cross-dex pair matches funding but not venue microstructure, and the
  reader must be able to see whether the primary rests on it.
- **Matching stays trailing-only, assignment-time, and append-only.** The
  fallback path runs through the same pinned matcher: a funding row
  stamped after the event entry raises `npl.controls.PostEntryRead`, and
  the refusal is produced through the fallback path by test
  (`tests/test_amend.py`), not asserted.
- **The 38 pair rows written 2026-08-28T05:37–05:38Z carry no
  `pair_type` field.** The rule in force when they were written admitted
  same-dex candidates only, so those 38 pairs are `same_dex` **by the
  registered rule that produced them**, not by imputation of a missing
  value. A reader treats an absent `pair_type` on a pre-amendment row as
  `same_dex` and on any row written after this amendment as a defect.
  Pinned by test.
- **Direction of the change: a relaxation.** It admits pairs the
  registered rule refused. It does not change any bar, any alpha, or any
  outcome definition.

#### Change 2 — the economic floor moves from 2× to 1× the pair's central cost

**E2's bar was: the share of pairs whose 30-day net return is at or above
`h2_cost_floor_multiple` = 2.0 times the pair's registered central cost
(Section 5) exceeds one half. The multiple becomes 1.0.**

- **This is a weakening, stated plainly.** A pair that returns between
  one and two times its own execution cost now counts as a success where
  it did not before. The bar still requires each pair to clear its own
  round-trip execution costs — 18, 27, or 36 basis points by pair class —
  so E2 remains an economic test and not a restatement of E1's sign test.
  What it no longer requires is a doubling of that cost.
- **The 2× figure is retained as a named secondary at every look**: the
  E2 statistic recomputed at multiple 2.0, reported beside the primary,
  descriptive and never verdict-bearing. The cost of the weakening stays
  legible in the same artifact that records the benefit.
- **The registered power assumption moves with the floor, and the move is
  stated.** E2's true share was registered at **0.60** for the 2× floor —
  itself a judgment discount from E1's 0.651, not a measurement, taken
  because the pair distribution's spread is unmeasured. Halving the floor
  halves the distance from the sign test's zero, so the registered
  assumption for the 1× floor is set by **linear interpolation in the
  floor multiple** between multiple 0 (E1's sign share, 0.65) and
  multiple 2 (the registered 0.60), evaluated at multiple 1:
  **h2_e2_true_share = 0.625**. Linear is chosen as the neutral
  interpolation, not because the distribution is known to be linear
  there; it is not known at all.
- **Because that assumption is a choice and not a measurement, every
  minimum-N figure for E2 is reported twice** — at 0.625 and at the
  unchanged 0.60 — so no reader has to take the interpolation on trust.
- **Chosen before any pair outcome existed.** At the moment this line was
  written, zero pair net returns had been computed by this repository,
  and the reader that computes them had seen only synthetic fixtures.

#### Change 3 — the two-look sequential plan (a relaxation of Sections 8, 9, and 10)

Section 8's two co-primaries are unchanged in form: **E1**, the exact
one-sided sign test that the share of pairs with positive 30-day net pair
return exceeds one half; **E2**, the same test on the share at or above
the (now 1×) floor. What changes is that the pair is tested at **two
registered looks** instead of one.

**The looks.**

- **Look 1** fires at the earliest date at which **both** co-primaries
  have reached their **look-1 minimum N** in achieved eligible pairs
  (Section 7 coverage bars on both legs).
- **Look 2** fires at the **earlier** of the registered deadline
  (2027-03-31) and the date both co-primaries reach their **look-2
  minimum N**.
- **Look sizes are outcome-blind by construction.** n₁ and n₂ are set by
  eligible-pair counts and the calendar — quantities the coverage modules
  compute from row counts and timestamps — and never by an observed
  statistic. This is what makes the exact boundary below valid.

**The alpha split, fixed here and never revisited: alpha₁ = 0.02,
alpha₂ = 0.03, summing to alpha_h = 0.05 per co-primary.**

The register prompt permits replacing this split only if the power
computation shows a *materially better* split at the same total. The
materiality test, defined here before it is applied: a candidate split
(α₁′, α₂′) with α₁′ + α₂′ = 0.05 replaces (0.02, 0.03) only if, at the
projected look-2 N, it (a) raises the **governing** co-primary's overall
two-look power by at least **0.01 absolute**, **and** (b) does not reduce
that co-primary's probability of a look-1 GO under the registered
alternative by more than **0.05 absolute**. Clause (b) exists because
look 1's entire purpose is the early stop; a split that buys power by
making look 1 nearly inert has not improved a two-look design, it has
deleted one of its looks. Both clauses are arithmetic over registered
assumptions and contain no data.

**The exact binomial boundary construction, registered.** With n₁ pairs
and S₁ successes at look 1, n₂ ≥ n₁ pairs and S₂ successes at look 2, and
the null p₀ = 1/2:

    k₁ = min { k : P(Bin(n₁, ½) ≥ k) ≤ alpha₁ }

    k₂ = min { k : Σ_{s=0}^{k₁−1} P(Bin(n₁, ½) = s)
                     · P(Bin(n₂ − n₁, ½) ≥ k − s)  ≤ alpha₂ }

    reject at look 1  ⟺  S₁ ≥ k₁
    reject at look 2  ⟺  S₁ < k₁  and  S₂ ≥ k₂

The look-2 spend is computed **conditional on not having rejected at look
1**, over the independent increment Bin(n₂ − n₁, ½), so the total type-I
error is at most alpha₁ + alpha₂ = 0.05 exactly, with no asymptotic
approximation anywhere. **A look at which no k satisfies its inequality
cannot reject**; that is recorded as such and the alpha is never relaxed
to manufacture one.

**Power at the registered true share p:**

    Π(n₁, n₂, p) = P(Bin(n₁, p) ≥ k₁)
                 + Σ_{s=0}^{k₁−1} P(Bin(n₁, p) = s) · P(Bin(n₂ − n₁, p) ≥ k₂ − s)

**Minimum-N semantics, as H1 and Amendment H2-1:** the smallest n from
which power stays at or above 0.80, never the first crossing. The
**planning interim fraction is one half** — minimum-N figures are
computed at n₁ = ⌈n₂ / 2⌉ — and the **look-1 minimum N of a co-primary is
⌈(its look-2 minimum N) / 2⌉**. At the actual looks the boundaries are
recomputed from the actual (n₁, n₂); the planning fraction sizes the
design, it does not bind the reader.

**The futility boundary, registered as a construction; its numbers
computed in Task 3 and recorded in Amendment H2-4.** At look 1, define
the conditional power of a look-2 rejection given S₁ = s, at the
co-primary's registered true share p:

    CP(s) = P( Bin(n₂ − n₁, p) ≥ k₂ − s )

and let **f₁ = the largest s in [0, k₁) with CP(s) < 0.10**, taken from
s = 0 upward (CP is non-decreasing in s, so the qualifying set is a lower
interval and f₁ is well defined). **Futility fires at look 1 when S₁ ≤ f₁
for either co-primary** — both are required, so one hopeless co-primary
makes the conjunction hopeless. Where no s in [0, k₁) has CP(s) < 0.10,
**no futility boundary exists at that (n₁, n₂) and none is registered**;
the look then has no futility stop at all. **Futility is never declared
on inspection**, only on this boundary, evaluated once at look 1.

**The outcome map, per look, mechanical:**

| at | condition | row |
|---|---|---|
| look 1 | E1 **and** E2 both reject at k₁ | **GO** |
| look 1 | S₁ ≤ f₁ for either co-primary (where f₁ is registered) | **FAIL**, terminal |
| look 1 | otherwise | **CONTINUE** — no row fires, collection proceeds |
| look 2 | E1 **and** E2 both reject at k₂ | **GO** |
| look 2 | otherwise | **FAIL**, terminal |

**Both co-primaries must reject at the same look for a GO.** A look at
which one co-primary rejects and the other does not is **not** a FAIL and
is **not** a partial GO: at look 1 it is a CONTINUE, at look 2 it is a
FAIL. **Only look 2 (and the look-1 futility boundary) fires a terminal
row.**

**A GO authorizes drafting Stage C — paper software — and never capital.**
No wallet, no signer, no order, no venue credential, no position. A GO
changes what may be written, not what may be traded.

**Section 10 is extended, and the extension is stated plainly.** H2's
sealed outcomes were registered to open **exactly once**. They now open
**exactly twice — once at each registered look — behind a per-look latch
written before that look's read**, so a crash after the latch spends that
look. Look 1's latch is `data/state/h2_look1_latch.json`, look 2's is
`data/state/h2_look2_latch.json`, each write-once and fsynced. A look
whose latch exists refuses loudly and is never silently re-run. **Look 2
cannot run before look 1's latch exists**; the order is pinned. The rest
of Section 10's trigger is unchanged and still required at each look: the
H2 operator prior slot (Section 13) filled and labelled, and explicit
operator instruction. The power condition becomes the look's registered
minimum N in achieved eligible pairs.

**Named secondaries, extended.** The Section 8 list gains exactly two
entries, both descriptive and never verdict-bearing, computed at every
look: **(i) the `same_dex` stratum** — n, successes, and share for E1 and
E2 restricted to same-dex pairs; **(ii) the 2× economic floor** — the E2
statistic recomputed at `h2_cost_floor_multiple` = 2.0. A statistic not
named in Section 8 or here is a second look and is refused.

#### The interim tripwire: OMITTED, and why

The register prompt offers an optional E1-only status check on
2026-09-30, descriptive, spending no alpha — **to be omitted if it cannot
be built without touching the reader, stating which. It is omitted.**

The E1 statistic is the share of pairs with positive 30-day net pair
return. Computing it requires each leg's entry and exit closes and each
leg's funding over the holding window — that is, opening the sealed
outcomes. There is no construction of the E1 statistic that does not read
an outcome value, so a 2026-09-30 tripwire that reported it would be an
unregistered third opening of the sealed data, in direct breach of
standing rule 7 and of Section 10 as amended above. **A descriptive
framing does not change what the code would have to read.** The
pair-count half of the proposed tripwire needs no registration: pair
counts and per-leg coverage are already computed from row counts and
timestamps by the coverage modules and can be reported at any time
without opening anything. **Nothing is registered for 2026-09-30.**

#### What this amendment does not change

k = 1 and alpha_h = 0.05, fixed by the cull and never revisited. The
generating-sample quarantine: the 312 retro events remain barred from
every H2 verdict statistic. The event rule and universe (Section 2), the
entry anchor (Section 3), the four-leg outcome definition and its sign
conventions (Section 4), the cost table and bands (Section 5), the
horizons, truncation rule, and coverage bars (Section 7), the epistemic
boundary (Section 11), the zero-dollar keyless spend rule (Section 12),
and the reserved, empty operator prior slot (Section 13) — all unchanged.
**The operator prior slot remains the structural block on every H2 look.**

### Amendment H2-4 — 2026-08-28 — the boundary record, the futility numbers, and one correction to H2-3

**What data existed when this amendment was made.** Everything listed in
Amendment H2-3, plus the Task 2 backfill: the H2 pairs ledger at **62 rows
(38 `same_dex`, 24 `cross_dex`)**, its 62 entry timestamps, the pair tags,
the fresh plan at 124 rows, 24 control-leg funding archives caught up (133
pages, 57,584 rows), and 24 loud `expired` control-leg l2Book records.
**Counts, tags, and timestamps only. No pair net return, no candle close,
and no post-entry funding rate has been read; the H2 pair reader has still
seen only synthetic fixtures.** Every arithmetic input below is either a
registered constant or one of those counts. Full record:
`reports/stage_a_h2/ktable_amended.json`.

#### 1. The alpha split, confirmed as registered: alpha_1 = 0.02, alpha_2 = 0.03

Amendment H2-3 permitted replacement only on its two-clause materiality
test. Evaluated at the projected look-2 N of **135 pairs**, on the
governing co-primary E2:

| split | two-look power | P(look-1 boundary fires) | min n₂ | clause (a) gain ≥ 0.01 | clause (b) stop-loss ≤ 0.05 | replaces? |
|---|---|---|---|---|---|---|
| **0.02 / 0.03 (registered)** | **0.8629** | **0.5042** | **117** | — | — | — |
| 0.025 / 0.025 | 0.8629 | 0.5042 | 120 | no (0.0000) | yes | no |
| 0.015 / 0.035 | 0.8574 | 0.4050 | 114 | no (−0.0055) | no | no |
| 0.01 / 0.04 | 0.8900 | 0.3112 | 112 | yes (+0.0270) | **no** (−0.1930) | no |
| 0.005 / 0.045 | 0.8891 | 0.2277 | 109 | yes (+0.0262) | **no** (−0.2765) | no |
| 0.03 / 0.02 | 0.8262 | 0.5042 | 123 | no (−0.0367) | yes | no |

**No candidate passes both clauses. The registered split stands.** The two
splits that buy power do it by nearly halving the chance the interim ever
fires — exactly what clause (b) was written to refuse.

#### 2. Minimum N per co-primary, both looks, at both E2 assumptions

Stays-at-or-above-0.80 semantics; planning interim n₁ = ⌈n₂/2⌉.

| co-primary | look-1 min N | look-2 min N | single-look min N at alpha_h |
|---|---|---|---|
| **E1** (share 0.65) | **42** | **84** | 76 |
| **E2, 1× floor** (share 0.625, governing) | **59** | **117** | **111** |
| E2, 1× floor at the unchanged 0.60 (reported beside) | 92 | 184 | 169 |
| **E2, pre-amendment 2× floor** (share 0.60, one look) | — | — | **169** |

**The cost of the weakening, legible in one line.** Under the old 2× floor
H2 needed **169** achieved pairs at a single look. Under the 1× floor it
needs **117** at look 2 and can stop at **59**. Of that saving, the part
attributable to the *interpolated* share is the difference between the
0.625 row and the 0.600 row — 117 against 184 — so a reader who rejects the
interpolation and holds E2 at 0.60 should read **184 / 92**, and the design
then does not reach 0.80 by the deadline. **Both figures are carried at
every look.** The 169 recomputes here from the same registered inputs and
reproduces Amendment H2-1 exactly, which is the arithmetic's own check.

**The governing figures: look-1 minimum N = 59 pairs, look-2 minimum N =
117 pairs** (the larger of the two co-primaries' at each look).

#### 3. The boundary table

| scenario | n₂ | n₁ | k₁ | k₂ | alpha spent (look 1 + look 2) | E1 power | E2 power |
|---|---|---|---|---|---|---|---|
| at look-1 min N | 59 | 30 | 22 | 37 | 0.0173 + 0.0200 = 0.0373 | 0.7031 | 0.5529 |
| **at look-2 min N** | **117** | **59** | **38** | **69** | 0.0182 + 0.0240 = **0.0422** | **0.9322** | **0.8237** |
| at the deadline | 135 | 68 | 43 | 79 | 0.0176 + 0.0227 = 0.0403 | 0.9552 | **0.8629** |

Every total spend sits **inside** alpha_h = 0.05 — the exact construction
is conservative, never at the budget, and never over it. The script refuses
loudly if any row ever exceeds it.

#### 4. The look-1 futility boundary, and the n₂ it uses

Amendment H2-3 defined f₁ as a function of (n₁, n₂) but did not name which
n₂ the look-1 computation uses, because the real n₂ is not observable at
look 1. **Named now, before any outcome exists: n₂ for the look-1 futility
computation is the co-primary's registered look-2 minimum N (table 2), or
the observed n₁ where that is larger.** At the projected look-1 size
n₁ = 59, with the registered conditional-power floor of 0.10:

| co-primary | n₁ | n₂ used | k₁ | k₂ | **f₁** |
|---|---|---|---|---|---|
| E1 | 59 | 84 | 38 | 51 | **31** |
| E2 | 59 | 117 | 38 | 69 | **27** |

**Futility fires at look 1 when E1's positive count is 31 or fewer of 59,
or E2's floor-clearing count is 27 or fewer of 59.** Both boundaries are
registrable and are registered. They are recomputed at the actual n₁ by the
same function; the numbers above are the projection, not a substitute for
the computation.

#### 5. The projected look dates

A fresh pair becomes readable when its candle window seals at entry + 92
days (ADR-019); a forward birth's pair is readable at listing + 94 days.
At the A.1-measured accrual of **18.57 events/month** and the amended match
rate of **1.000** (62/62 — the fallback removes the same-dex age gate, so
by-dex and flat projections now coincide; at the pre-amendment 0.613 the
deadline count would be 82 instead of 135):

| as of | backfill pairs readable | forward | total |
|---|---|---|---|
| 2026-09-30 | 18 | 0 | 18 |
| 2026-10-31 | 34 | 0 | 34 |
| **2026-11-30** | **62** | 0 | **62** |
| 2026-12-31 | 62 | 18 | 80 |
| 2027-01-31 | 62 | 37 | 99 |
| 2027-02-28 | 62 | 54 | 116 |
| **2027-03-31** | 62 | 73 | **135** |

- **Look 1 projects to 2026-11-26** — the day the 59th backfill pair
  becomes readable.
- **Look 2 projects to 2027-03-01** — the day the 117th pair becomes
  readable, one month inside the registered 2027-03-31 deadline.

**What the amendment bought, stated plainly:** Amendment H2-1 put H2's
earliest read near 2027-06, past its own deadline. The amended design reads
at **2026-11-26** and terminates by **2027-03-01**.

#### 6. Recomputed power beside the registered target (the DEGRADED rule)

At the projected deadline N of 135, on single-look power — the basis
Section 0's map is stated on — E1 reaches **0.9665** and E2 **0.8886**
(0.7318 at the reported-beside 0.60), so the governing figure is **0.8886**
and the Section 0 function returns **GO**. On the two-look design that
actually governs, the governing figure is **0.8629**. **Both are above the
registered 0.80 target.** Section 0's DEGRADED record of Amendment H2-1 is
not edited and is not re-fired; this is the recomputed power the DEGRADED
rule requires to travel beside the target at every later reading.

#### 7. A correction to Amendment H2-3's look-2 outcome map

**The defect, found while implementing the reader and recorded rather than
smoothed over.** Amendment H2-3 wrote the look-2 GO condition as "E1 and E2
both reject at k₂", with the look-2 rejection event defined as
`S₁ < k₁ and S₂ ≥ k₂`. Read literally, a co-primary whose look-1 count had
already crossed k₁ — while the *other* co-primary had not, so the trial
correctly continued — could never satisfy `S₁ < k₁` at look 2, and the
design would fire **FAIL** at look 2 precisely because the evidence at look
1 was too strong. That is perverse, and it is not what the plan is for.

**The correction, made now, before any outcome value exists and before the
reader has seen anything but synthetic fixtures: a co-primary passes at
look 2 when the two-look procedure has rejected its null *by* look 2 — that
is, when `S₁ ≥ k₁` **or** `S₂ ≥ k₂`.** A GO at look 2 still requires both
co-primaries to have done so.

**This does not weaken the error control.** The rejection region is the
union of the two registered regions, whose null probability is exactly
alpha_spent(look 1) + alpha_spent(look 2) ≤ alpha_1 + alpha_2 = 0.05 — the
same construction, the same budget, the same numbers in table 3. The
conjunction's familywise error is bounded by the weaker co-primary's, so it
too stays at or under 0.05.

`S₁ < k₁ and S₂ ≥ k₂` remains the definition of the **look-2 rejection
event** used to compute the exact spend. Only the verdict question — has
this co-primary rejected by this look — is corrected. Everything else in
Amendment H2-3 stands unchanged.
