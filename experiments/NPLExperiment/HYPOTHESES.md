# Hypothesis register

**Read this before proposing any new hypothesis on new-listing drift.**

NPLExperiment converted from a single-hypothesis experiment into a
multi-hypothesis register on 2026-08-28 (root REGISTRATION.md, Amendment 4).
The register holds four entries: **H1, the founding H-NPL naive short, closed
negative on 2026-08-28** by the single registered Stage B read; and **H2, H3,
H4, three co-registered successors** that test on fresh, unread data only,
share one collection substrate, and sit under one familywise error budget
with an outcome-blind power cull. **The cull fired 2026-08-28: k = 1,
alpha_h = 0.05. H2 survives; H3 and H4 fired BLOCKED on measured rates —
documented answers, closed below with what would reopen them.** H2 was
**amended the same day** (Amendments H2-3 and H2-4, before any pair outcome
existed) to a two-look sequential plan with a main-dex fallback control and
a 1× economic floor: **look 1 projects to 2026-11-26 and look 2 to
2027-03-01**, both inside the registered deadline, where the unamended
design had put the earliest read past it. The spent Stage B read and every value
inside it are quarantined from all successor code paths by AST pin and test;
the 312 retro events and their 176 control windows are the **generating
sample** — usable for power assumptions, labelled so wherever carried, and
never admissible to a successor verdict.

Every entry carries the claim, the design pointer, the verdict with the
figures that decided it, and — where closed — what would reopen it. The
failure mode this file exists to prevent is retrying a settled question
because the number that closed it is buried.

This file contains no analysis. It records what the registrations and the
sealed reads established.

---

## Register

### H1 — H-NPL, the naive new-listing short

> A short opened at the second daily close on newly listed Hyperliquid
> perpetuals earns a positive net return over 30 and 90 days, because
> listing-age drift exceeds the funding the short pays plus costs.

| | |
|---|---|
| **Status** | **CLOSED — NEGATIVE** · 2026-08-28 |
| **Registration** | Root `REGISTRATION.md` (archived; Sections 0–13, Amendments 1–3, the Stage B verdict record, and the H-NPL closure entry). Nothing in it may be revised. |
| **Deciding numbers** | The Amendment 3 table fired **FAIL** on the sealed retro cohort at alpha_adj 0.016952, central costs: **P1** 197/312 positive (63.14%), exact lower bound **0.5707** against the 0.60 bar — FAIL; **P2** 111/312 at ≤ −15% net (35.58%), sign-test p = **1.000** — FAIL; **P3** 114/175 pairs young-below-control (65.14%), p = **3.767e-05** — PASS. Cost-insensitive across the registered bands (P1 lb 0.5740 / 0.5707 / 0.5609, n = 312 each). |
| **Sample** | 312 retro events (112 vanilla, 46 hyperp_conversion, 154 hip3; 10 truncated_by_delisting retained), 175 effective pairs, 224,633 funding rows inside the 30-day windows. Delisting observability PASS 6/6 — the cohort is not survivorship-manufactured. |
| **The spent read** | Latch `data/state/stage_b_read.json` sha256 `2d204ccb23c4961597d2e4a3263b2abffeb1f8f2e32230ee3c4b97857438f67e` (21 module hashes inside); artifact `reports/stage_b/read.json` sha256 `4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c`. Read 2026-08-28T03:01:08Z, exactly once. **Quarantined from every successor code path** (AST pin, tests/test_guards.py). |
| **Working** | `report.md` §"Stage B — the sealed read"; REGISTRATION.md Stage B verdict record and closure entry. |
| **What would reopen it** | **Nothing reopens H1 itself** — the registered short does not clear its bars on this sample, and the sample is spent. The residual worth testing is precisely what P3 and the H8 decomposition measured: a real listing-age effect (+6.43 price points paired differential, n = 175, generating-sample figure) too thin per event for the naive short. That residual is H2, H3, and H4 below — each a **new hypothesis on fresh data under its own registration**, never a second look at the sealed outcomes. |

---

### H2 — the age-contrast pair

> A pair opened at the second daily close — short the young listing, long its
> funding-matched elder on the same dex at equal constant notional (or, where
> that dex has no eligible elder, on the main dex) — held 30 days, earns a
> positive net return, because listing-age drift exceeds what funding matching
> already prices.

| | |
|---|---|
| **Status** | **OPEN — SURVIVOR, AMENDED TO A TWO-LOOK PLAN** · Section 0 fired DEGRADED 2026-08-28 (Amendment H2-1): k = 1, alpha_h = 0.05. Amended the same day, before any pair outcome existed (H2-3, H2-4): **62/62 pairs achieved (38 same_dex + 24 cross_dex)**; **look 1 projects to 2026-11-26 at 59 pairs, look 2 to 2027-03-01 at 117**, inside the 2027-03-31 deadline; recomputed power at the deadline 0.8886 single-look / 0.8629 two-look, both above the registered 0.80 target |
| **Registration** | `registrations/H2/REGISTRATION.md` — Sections 0–13 and Amendments H2-1 … H2-4 |
| **Design in one line** | Every fresh event (the 62 pending-at-closure events with servable windows plus all forward births, every dex); the H1 Section 6 control, **with a main-dex fallback where the same-dex candidate set is empty** (H2-3 Change 1, tagged `same_dex`/`cross_dex`, never filtered); pair net = young-leg net short + elder-leg net long, four fills; co-primaries E1 (share of pairs positive) and E2 (share at or above **1×** the pair's central cost — H2-3 Change 2, down from 2×), both exact sign tests above one half, **decided at two registered looks** against an exact binomial boundary with alpha_1 = 0.02 and alpha_2 = 0.03 summing to alpha_h = 0.05 (H2-3 Change 3). Both co-primaries at a common look for a GO; look 1 can only GO, CONTINUE, or fire the registered futility boundary. |
| **Look boundaries** | Look-1 min N **59** (E1 42, E2 59), look-2 min N **117** (E1 84, E2 117). At the look-2 minimum: k₁ = 38, k₂ = 69, exact spend 0.0182 + 0.0240 = 0.0422 inside alpha_h. Futility at n₁ = 59: E1 f₁ = 31, E2 f₁ = 27 at the 0.10 conditional-power floor. Full table: `reports/stage_a_h2/ktable_amended.json`. |
| **Power assumptions** | E1 true share 0.65; **E2 true share 0.625** under the 1× floor, by stated linear interpolation between multiple 0 (E1's 0.65) and multiple 2 (the registered 0.60) — a choice, not a measurement, so **every minimum N is also reported at the unchanged 0.60** (E2 then needs 92/184 and does not reach 0.80 by the deadline). All generating-sample-derived (P3 pair share 114/175 = 0.651; paired price differential +6.43 points, funding differential +0.88, n = 175). |
| **Named secondaries added** | The `same_dex` stratum and the pre-amendment **2× floor**, both computed beside every primary figure at every look, both descriptive and never verdict-bearing. |
| **Operator prior slot** | Reserved, empty. Blocks H2's Stage B structurally (`npl.register.priors`) — **at both looks**. |

---

### H3 — the population-corrected naive short

> The H1 short, restricted by a mechanical instrument-class rule to main-dex
> listings (vanilla and hyperp conversions), clears the unchanged H1 bars —
> because HIP-3 builder dexs list index- and equity-style instruments outside
> the token-listing population the external drift studies measured.

| | |
|---|---|
| **Status** | **BLOCKED** · Section 0 fired 2026-08-28 (Amendment H3-1) — measured main-dex accrual 0.5/month (n = 3/182d) against a P1 min-N of 262; deadline N = 5; both required legs at ~0 power. A documented answer. Reopens only on an order-of-magnitude higher main-dex listing rate or a longer-horizon successor registration |
| **Registration** | `registrations/H3/REGISTRATION.md` |
| **Design in one line** | Fresh main-dex events only (the exclusion reads the dex field, outcome-blind); bars unchanged from H1 in structure and level — profitability lower bound ≥ 0.60 and the ≥15-point magnitude majority, both at alpha_h, both required. |
| **Power assumptions** | Share positive 0.677 (generating-sample-derived, main-dex strata 107/158); magnitude share unknown — no subset figure exists — so power computes at the H1 registered 0.65 and the H1 measured overall 0.356, both reported, the honest range. **Registered expectation: likely BLOCKED on the magnitude leg** at achievable main-dex accrual; a BLOCKED is a documented answer, not a failure of process. |
| **Operator prior slot** | Reserved, empty. Blocks H3's Stage B structurally. |

---

### H4 — the funding-conditioned short

> The naive short restricted to events whose signed trailing 168-hour mean
> hourly funding at entry sits at or below a registered threshold clears the
> H1 profitability bar — because deeply negative entry funding marks the
> listings whose decline the market has not fully priced.

| | |
|---|---|
| **Status** | **BLOCKED** · Section 0 fired 2026-08-28 (Amendment H4-2) — measured conditioning rates 0.177/0.129/0.081 (n = 62; median trailing entry funding +31.6%/yr — deep negative entry funding is rare); best-cell deadline power 0.014 governing (0.711 even at the declined optimistic 0.85). The registered expectation confirmed. Reopens only on a persistent negative-funding listing regime — a new registration |
| **Registration** | `registrations/H4/REGISTRATION.md` |
| **Design in one line** | Fresh events on every dex, conditioned on a pre-registered grid of three entry-funding thresholds (−10, −20, −40 percent annualized), Sidak-corrected within the hypothesis; the conditioning feature is pre-entry and readable under standing rule 13. Primary per cell: profitability lower bound ≥ 0.60 at the within-corrected alpha. |
| **Power assumptions** | Depend on measured conditioning rates (Stage A.2 Task 3, from funding archives, pre-entry reads only). **Registered expectation: likely BLOCKED at every cell by 2027-03-31.** |
| **Operator prior slot** | Reserved, empty. Blocks H4's Stage B structurally. |

---

## The register's rules, stated once

1. **Fresh data only.** Successor verdicts admit no event from the generating
   sample (the 312 retro events; IDs in `data/state/generating_sample.json`,
   refusal produced by `npl.register.generating_sample`, pinned by test).
2. **One familywise budget.** k = the survivors of the A.2 cull; alpha_h =
   1 − 0.95^(1/k), fixed at the cull, recorded in every surviving
   registration by amendment, never revisited after any outcome exists.
3. **The cull is outcome-blind.** It reads counts, rates, and timestamps
   only. Any hypothesis under 50 percent power on a required co-primary at
   the achievable N by 2027-03-31 fires BLOCKED, at the k/alpha fixed point
   (registered in each successor's Section 9).
4. **One substrate.** One census, one watcher, one funding recorder, one
   checkpoint scheduler; per-hypothesis eligibility views on top
   (`docs/SUBSTRATE.md`). Per-hypothesis latches and readers are dark until
   each hypothesis's own registered Stage B.
5. **The quarantine.** `reports/stage_b/read.json`, every value inside it,
   and every outcome window read on 2026-08-28 are quarantined from all
   successor code paths — enforced by AST pin and by test, not by intention.
