# registrations/H3/REGISTRATION.md — the population-corrected naive short

> **STATUS: REGISTERED 2026-08-28, BEFORE ANY NEW NETWORK CALL.** The same
> closure applies as registrations/H2: this session had sent zero requests
> at commit time, no fresh-cohort figure of any kind existed, and every
> carried figure below is **generating-sample-derived** — a power
> assumption, never a successor verdict input (standing rule 12). Changes
> only by dated amendment below; nothing above an amendment line is edited.

---

## 0. The outcome map — it judges collection feasibility, never returns

Fired in register Stage A.2 Task 5 by `npl.register.cull.
fire_hypothesis_section0`, counts and rates only:

- **GO:** both co-primaries reach **at least 80 percent power at alpha_h**
  at the achievable main-dex event count by **2027-03-31**.
- **DEGRADED:** the weaker co-primary lands between **50 and 80 percent**.
- **BLOCKED:** either co-primary **under 50 percent power** (inside the
  register cull's k/alpha fixed point). Nothing armed for H3.

**The registered expectation, stated now, before any measurement: this
hypothesis likely fires BLOCKED on the magnitude leg** at achievable
main-dex accrual (carried planning figure: near **9.4 events/month**
main-dex, superseded by the A.1 measurement). **A BLOCKED here is a
documented answer, not a failure of process** — it records that the
population-corrected question cannot be powered on this venue's main-dex
listing rate by the deadline, which is itself the answer the register
needs.

## 1. The hypothesis

**H3.** The H1 short — entry at the second daily close, 30-day horizon,
net of received funding and registered costs — **restricted by a
mechanical instrument-class rule to main-dex listings (vanilla and hyperp
conversions)** clears the unchanged H1 bars.

**The population argument:** HIP-3 builder dexs list index- and
equity-style instruments (xStocks, indices, commodities baskets) outside
the token-listing population that the external drift studies measured
(Delphi 652 CEX listings; Animoca 773; Memento 118 TGEs — carried in H1
Section 1). On the generating sample the HIP-3 stratum was the weakest
(share positive 0.584, n = 154, against vanilla 0.670, n = 112, and
hyperp_conversion 0.696, n = 46 — all generating-sample-derived), and it
was 154 of H1's 312 events. H3 asks whether the H1 claim holds on the
population the studies were actually about.

## 2. The universe and event rule

**Fresh main-dex events only**: the fresh cohort of registrations/H2
Section 2 (62 pending-at-closure with servable windows, plus all forward
births), restricted to `dex == ""` — **the exclusion rule reads the dex
field only, outcome-blind** (`npl.register.views.h3_main_dex_view`,
pinned). Vanilla and hyperp-conversion tags enter (conversions at the
Amendment 1 funded-phase anchor); HIP-3 events are `hip3_builder_dex`
exclusions, counted. No generating-sample event enters (refusal pinned).

## 3–7. Design, carried from H1 verbatim

Listing date and entry anchor: H1 Section 3 + Amendment 1. Outcome: H1
Section 4 verbatim (net short return, positive funding pays the short,
constant notional, no compounding, no liquidation modelling). Costs: H1
Section 5 vanilla band — **9 bp central (3, 9, 18)** — every H3 event is
main-dex by construction. Horizons and deaths: H1 Section 7 verbatim
(30d primary, 90d secondary, truncation at last served close retained and
flagged, pending never partial). No matched control exists in H3: the
population correction is the design, and the H1 P3 contrast already
established the age effect on the generating sample.

## 8. Inference

**Two co-primaries at alpha_h, both required, bars unchanged from H1 in
structure and level:**

- **P1, profitability.** Exact binomial (Clopper–Pearson) lower confidence
  bound at alpha_h on the share of main-dex events with positive 30-day
  net short return; bar: **at or above 0.60**. Registered power
  assumption: true share **0.677** — generating-sample-derived (main-dex
  strata: 0.670 × 112 vanilla + 0.696 × 46 conversions = 107/158).
- **MAG, magnitude.** Exact one-sided sign test on the share of main-dex
  events at or below **−15 percent net** asset-side (net short ≥ +15
  points, inclusive); bar: the share **exceeds one half** at alpha_h.
  **The magnitude share on the main-dex subset is unknown — no subset
  figure was computed by the spent read — so power computes at both ends
  of the honest range: the H1 registered 0.65 and the H1 measured overall
  0.356 (111/312), both reported.** **The generating-sample figure (0.356)
  governs the cull**; adopting the optimistic figure after seeing the
  pessimistic one would be outcome-fitting, and the register's principle
  is that generating-sample-derived assumptions govern wherever they
  exist.
- Tie rules as H1 (a value exactly on a strict bar counts against the
  hypothesis; the −15 bound is inclusive).
- **Named secondaries, descriptive:** 90-day versions; vanilla-versus-
  conversion strata; the H8 decomposition; the truncated subgroup; the
  backfill-versus-forward split.

## 9. Power method and the register cull

As registrations/H2 Section 9, with **H3's n = fresh main-dex events**
(achieved backfillable, projected by the A.1-measured main-dex accrual to
2026-12-31 and 2027-03-31). **Requirement mode: all — P1 and MAG are both
required and the weaker governs the cull.** k and alpha_h fixed at the
cull by amendment here.

## 10. The H3 Stage B trigger

As registrations/H2 Section 10, mutatis mutandis: both co-primaries at or
above 80 percent power at achieved eligible N, **the H3 operator prior
slot filled**, explicit operator instruction, one sealed read behind its
own latch under its own allowlist amendment.

## 11. The epistemic boundary

As registrations/H2 Section 11: a positive supports only that the
registered short would have cleared its bars on this fresh main-dex
sample. Never a forward prediction, never a recommendation.

## 12. Spend and pacing

As registrations/H2 Section 12: zero dollars, keyless, ledgered, measured
pacing, drift-checked.

## 13. Priors

**Assistant prior, recorded 2026-08-28 in chat:** **0.10** that the H3
Stage B bars clear on the registered fresh sample.

**The adoption warning, standing (carried verbatim):** the NPD Amendment 0
lesson applies — an adopted prior corrupts the calibration ledger. The
assistant's number above is context, not the operator's number, and it
must not be copied into the slot below.

**The operator prior slot, reserved and empty:**

> Operator prior on the H3 Stage B bars clearing: _reserved, empty — only
> the operator fills this, as a probability in [0, 1] followed by
> `(independent)` or `(adopted)`. Nothing else parses._

**The empty slot blocks H3's Stage B structurally**
(`npl.register.priors`, exercised by `tests/test_register.py`).

---

## Amendments

None yet. An amendment is dated, reasoned, states exactly what data
existed when it was made, and never edits anything above its own line.
