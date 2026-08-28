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

None yet. An amendment is dated, reasoned, states exactly what data
existed when it was made, and never edits anything above its own line.
