# registrations/H4/REGISTRATION.md — the funding-conditioned short

> **STATUS: REGISTERED 2026-08-28, BEFORE ANY NEW NETWORK CALL.** The same
> closure applies as registrations/H2: this session had sent zero requests
> at commit time, no fresh-cohort figure of any kind existed — in
> particular **no conditioning rate had been measured** — and every carried
> figure below is **generating-sample-derived**, a power assumption and
> never a successor verdict input (standing rule 12). Changes only by
> dated amendment below; nothing above an amendment line is edited.

---

## 0. The outcome map — it judges collection feasibility, never returns

Fired in register Stage A.2 Task 5 by `npl.register.cull.
fire_hypothesis_section0`, counts and rates only. H4's grid is
**disjunctive within the hypothesis** (Section 8), so its **best cell
governs**:

- **GO:** at least one registered cell reaches **80 percent power at the
  within-corrected alpha** at its achievable conditioned count by
  **2027-03-31**.
- **DEGRADED:** the best cell lands between **50 and 80 percent**.
- **BLOCKED:** every cell **under 50 percent power** (inside the register
  cull's k/alpha fixed point). Nothing armed for H4.

**The registered expectation, stated now, before any conditioning rate is
measured: likely BLOCKED at every cell by 2027-03-31** — the conditioned
counts are fractions of an already-thin fresh cohort, and the governing
true-share assumption sits close to the bar. A BLOCKED here is a
documented answer, not a failure of process.

## 1. The hypothesis

**H4.** The H1 naive short, **restricted to events whose signed trailing
168-hour mean hourly funding at entry sits at or below a registered
threshold**, clears the H1 profitability bar — because deeply negative
entry funding marks the listings whose decline the market has not fully
priced.

Motivation, generating-sample-derived: H1's decomposition showed the
average short's profit dominated by funding (+1.33 funding vs +1.00 price
per event over 30 days, n = 312), and the H8 lesson is that the market
prices decline into funding when sorted on funding alone. H4 asks whether
funding-at-entry, used as a **pre-entry conditioning feature** rather than
a matched control, selects a subset where the short's bars clear.

## 2. The universe and event rule

The **full fresh cohort** of registrations/H2 Section 2 — every fresh
event on every dex (62 pending-at-closure with servable windows plus all
forward births), tags per H1 Amendment 1, hyperp pre-conversion phase
excluded — **conditioned per cell** on the entry-time trailing funding
feature. No generating-sample event enters (refusal pinned).

## 3. The conditioning feature and the registered grid

**The feature:** the signed trailing 168-hour mean hourly funding at the
event entry — the same quantity the H1 Section 6 matcher computes, through
the same trailing-only code path (`npl.controls.trailing_mean`), whose
post-entry refusal is produced by test. **Standing rule 13: a funding rate
stamped at or before its event entry is a feature, never an outcome. The
pin lists say exactly this** (`npl.blindness`, tests/test_blindness.py).

**The grid, pre-registered as exactly three cells** (`npl.register.
conditioning`, `h4_funding_thresholds_annualized`):

| cell | threshold, annualized | threshold, mean hourly |
|---|---|---|
| `le_-10pct_ann` | −10 percent/yr | −0.10 / 8760 |
| `le_-20pct_ann` | −20 percent/yr | −0.20 / 8760 |
| `le_-40pct_ann` | −40 percent/yr | −0.40 / 8760 |

**At or below is inclusive** (a mean exactly on the threshold clears its
cell; boundary fixture pinned). An event with an absent trailing mean
(coverage under the 0.95 bar over the trailing window) is excluded from
every cell with its reason, counted — absence as state, never a zero.

**Sidak within the hypothesis:** the three cells share H4's alpha_h as
alpha_cell = 1 − (1 − alpha_h)^(1/3) (`npl.register.conditioning.
sidak_within`, pinned to reproduce the H1 family split at 0.05/3).

## 4–7. Design, carried from H1 verbatim

Entry anchor, outcome definition, horizons, and deaths: H1 Sections 3, 4,
7 with Amendment 1, verbatim. Costs: H1 Section 5 by the event's venue
class (9 bp vanilla / 18 bp HIP-3 central, registered bands). No matched
control exists in H4; the conditioning is the design.

## 8. Inference

**Primary, per cell, at the within-corrected alpha_cell:** exact binomial
(Clopper–Pearson) lower confidence bound on the share of conditioned
events with positive 30-day net short return; bar: **at or above 0.60**
(the H1 P1 bar, unchanged in structure and level). **The hypothesis
passes if any registered cell passes at alpha_cell** — the grid is
disjunctive within H4 and the Sidak correction above is what that
disjunction costs.

**Power assumptions, the honest range, both reported:** the conditional
share positive is unknown — no conditioned subset figure exists — so
power computes at the H1 registered **0.85** and at the generating-sample
overall **0.631** (197/312). **The generating-sample figure governs the
cull** (the register's principle: generating-sample-derived assumptions
govern wherever they exist; the conditional share would need to exceed
the unconditional one for the hypothesis to be true, but assuming that in
the power computation would assume the conclusion).

**Named secondaries, descriptive:** 90-day versions per cell; per-dex
strata; the H8 decomposition per cell; monotonicity of the share across
the three cells (descriptive only — no trend test is registered).

## 9. Power method and the register cull

As registrations/H2 Section 9, with **H4's n per cell = the measured
conditioning rate (A.2 Task 3, from funding archives, pre-entry reads
only, pinned) × the achievable fresh N** — achieved backfillable,
projected to 2026-12-31 and 2027-03-31 at the A.1-measured accrual.
**Requirement mode: any — the best cell governs the cull** (a hypothesis
whose best cell cannot be powered is BLOCKED; a weak sibling cell blocks
nothing). k and alpha_h fixed at the cull by amendment here.

## 10. The H4 Stage B trigger

As registrations/H2 Section 10, mutatis mutandis: the governing cell at or
above 80 percent power at achieved eligible conditioned N, **the H4
operator prior slot filled**, explicit operator instruction, one sealed
read behind its own latch under its own allowlist amendment.

## 11. The epistemic boundary

As registrations/H2 Section 11. Additionally: a pass in one cell supports
only that cell's registered claim; it licenses no interpolation to
unregistered thresholds.

## 12. Spend and pacing

As registrations/H2 Section 12: zero dollars, keyless, ledgered, measured
pacing, drift-checked.

## 13. Priors

**Assistant prior, recorded 2026-08-28 in chat:** **0.05** that the H4
Stage B bars clear on the registered fresh sample.

**The adoption warning, standing (carried verbatim):** the NPD Amendment 0
lesson applies — an adopted prior corrupts the calibration ledger. The
assistant's number above is context, not the operator's number, and it
must not be copied into the slot below.

**The operator prior slot, reserved and empty:**

> Operator prior on the H4 Stage B bars clearing: _reserved, empty — only
> the operator fills this, as a probability in [0, 1] followed by
> `(independent)` or `(adopted)`. Nothing else parses._

**The empty slot blocks H4's Stage B structurally**
(`npl.register.priors`, exercised by `tests/test_register.py`).

---

## Amendments

An amendment is dated, reasoned, states exactly what data existed when it
was made, and never edits anything above its own line.

### Amendment H4-1 — 2026-08-28 — the conditioning feature's absence rule, resolved before any conditioning value existed

**What data existed when this amendment was made.** The A.1 recovery and
census refresh only: archive timestamps, row counts, servability, and
rates. **No conditioning value had been computed: no trailing mean of any
fresh event had been read**, and no eligibility ledger row existed.

**The contradiction, reported rather than silently chosen.** Section 3's
governing sentence defines the feature as "the same quantity the H1
Section 6 matcher computes" — `npl.controls`' event-side trailing mean,
which is **partial by design** (the mean over the present pre-entry rows
inside the 168-hour window; absent only when no pre-entry row exists),
because a two-day-old instrument cannot have 168 funded hours. The
parenthetical in the same section ("coverage under the 0.95 bar over the
trailing window") contradicts that: under a 0.95-of-168h bar every fresh
event's feature would be absent and H4's universe would be empty by
construction.

**The amended rule.** The governing sentence governs, verbatim: the
conditioning feature is the event-side trailing mean exactly as
`npl.controls._event_trailing_mean` computes it — the mean over present
pre-entry rows in the trailing 168-hour window, **absent only when no
pre-entry row exists** (and then excluded from every cell with its
reason, counted). **The 0.95 coverage bar applies to control candidates
only** (H2 Section 6 / H1 Section 6), never to the event's own
conditioning feature. The bias direction: a partial-window mean over a
young instrument's first funded hours is exactly the information a
forward trader would have at entry, so the rule is implementable and
introduces no look-ahead.

### Amendment H4-2 — 2026-08-28 — Section 0 verdict record: BLOCKED

**What data existed when this amendment was made.** Counts, rates, and
timestamps only (docs/ACCESS.md "Register A.1"; data/eligibility/h4.jsonl
— eligibility flags and pre-entry trailing means, standing rule 13;
reports/stage_a_h2/ktable_cull.json). **No outcome value of any fresh
event has been read.**

**The verdict: BLOCKED. Nothing is armed for H4.** Fired by
`npl.register.cull.fire_hypothesis_section0` at the cull's pass-1 alpha
(k = 3, alpha_h = 0.016952; alpha_cell = 0.00568 Sidak-within); every
input beside it:

- **Measured conditioning rates (A.2 Task 3, n = 62 fresh events, 0
  absent trailing means, Amendment H4-1 rule):** le −10%/yr **0.1774**
  (11/62), le −20%/yr **0.1290** (8/62), le −40%/yr **0.0806** (5/62).
  The fresh cohort's trailing entry funding is predominantly positive:
  median **+31.6 percent/yr annualized** (n = 62, min −132.4, max
  +403.5) — longs pay shorts on most new listings, and deep negative
  entry funding is rare.
- **Cell sample sizes at the deadline (rate × 173 projected events):**
  30 / 22 / 13; at achieved 62: 11 / 8 / 5.
- **Powers at the deadline, governing generating-sample share 0.631:**
  best cell **0.0140** (le −10%), 0.0037, 0.0025 — every cell far under
  the 0.50 floor. At the optimistic H1-registered 0.85 (reported beside,
  the honest range): 0.7106 / 0.3382 / 0.1209 — under the GO floor even
  at the assumption the register declined to adopt.
- Minimum-N per cell at the governing share: not reached by n = 1200
  (power at 1200 = 0.354 at the k = 3 alpha) against 30 achievable.

**Consequence, per Section 0 and the registered expectation ("likely
BLOCKED at every cell"): BLOCKED is the documented answer.** Nothing is
armed for H4; the operator prior slot stays reserved and empty; the
register records the closure in HYPOTHESES.md. **What would reopen it:**
a funding regime in which deeply negative entry funding stops being rare
(conditioning rates several times higher, sustained), a much larger
listing rate, or a redesign of the conditioning claim strong enough to
justify the near-0.85 conditional share — each a new registration.
