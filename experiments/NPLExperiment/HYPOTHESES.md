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
a 1× economic floor, and **amended again on 2026-09-13** (Amendments H2-5
and H2-6, still before any pair outcome existed) to **withdraw that fallback
and replace it with a class-constrained tiered control rule**: the fallback
had matched HIP-3 equity, index and rates young legs to main-dex crypto
elders, leaving 31 of 63 pairs cross-complex and hedging nothing for half
the sample. **Look 1 now projects to 2026-12-24 and look 2 to 2027-03-31**,
the deadline itself. The spent Stage B read and every value
inside it are quarantined from all successor code paths by AST pin and test;
the 312 retro events and their 176 control windows are the **generating
sample** — usable for power assumptions, labelled so wherever carried, and
never admissible to a successor verdict.

A fifth entry, **H5**, was registered on 2026-08-28 as a **feasibility
entry, not a trade hypothesis**: it authorizes no capital, no Stage B read of
a trading outcome, and no Stage C, and its terminal states are VIABLE
(meaning a successor is worth registering in a *fresh repo*) or CLOSED. It
sits outside the familywise budget because it decides no bar on returns.

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

> A pair opened at the second daily close — short the young listing, long a
> funding-matched elder **of the same asset class** at equal constant
> notional — held 30 days, earns a positive net return, because listing-age
> drift exceeds what funding matching already prices.

| | |
|---|---|
| **Status** | **OPEN — SURVIVOR, TWO-LOOK PLAN, CONTROL RULE TIGHTENED** · Section 0 fired DEGRADED 2026-08-28 (Amendment H2-1): k = 1, alpha_h = 0.05. Amended to the two-look plan 2026-08-28 (H2-3, H2-4) and **re-amended 2026-09-13 (H2-5, H2-6), still before any pair outcome existed**, to withdraw the main-dex fallback for a class-constrained tiered rule: **55 pairs of 63 events (33 tier 1, 18 tier 2, 4 tier 3)**, 6 `excluded_unclassifiable`, 2 `excluded_no_class_elder`; **look 1 projects to 2026-12-24 at 59 pairs, look 2 to 2027-03-31** — the deadline itself, reached before the 117-pair look-2 minimum N. Recomputed power at the projected deadline N of 110: **0.8088 two-look** (above the 0.80 target) and **0.7994 single-look**, so **Section 0 returns DEGRADED** from H2-4's GO |
| **Registration** | `registrations/H2/REGISTRATION.md` — Sections 0–13 and Amendments H2-1 … H2-6 |
| **Design in one line** | Every fresh event (the 63 pending-at-closure events with servable windows plus all forward births, every dex); the H1 Section 6 control **constrained by asset class through a three-tier rule** (H2-5: tier 1 same dex + exact class, tier 2 any dex + exact class, tier 3 any dex within the equity complex for equity-complex legs only; **cross-complex refused at every tier**; tier tagged and never filtered), which **supersedes the H2-3 main-dex fallback in full**; pair net = young-leg net short + elder-leg net long, four fills; co-primaries E1 (share of pairs positive) and E2 (share at or above **1×** the pair's central cost — H2-3 Change 2, down from 2×), both exact sign tests above one half, **decided at two registered looks** against an exact binomial boundary with alpha_1 = 0.02 and alpha_2 = 0.03 summing to alpha_h = 0.05 (H2-3 Change 3). Both co-primaries at a common look for a GO; look 1 can only GO, CONTINUE, or fire the registered futility boundary. |
| **Look boundaries** | **Unchanged by H2-5** — no bar, alpha, horizon or true share moved. Look-1 min N **59** (E1 42, E2 59), look-2 min N **117** (E1 84, E2 117). At the look-2 minimum: k₁ = 38, k₂ = 69, exact spend 0.0182 + 0.0240 = 0.0422 inside alpha_h. Futility at n₁ = 59: E1 f₁ = 31, E2 f₁ = 27 at the 0.10 conditional-power floor. Tables: `reports/stage_a_h2/ktable_tiered.json` (current), `ktable_amended.json` (superseded). |
| **The asset-class taxonomy** | Eight classes by mechanical string mapping (H2-5 §1): `crypto` by dex rule (main and hyna), then a full builder-dex ticker table over `equity`, `etf`, `index`, `commodity`, `fx`, `rates`, `vol`. **24 instruments are `excluded_unclassifiable` with their reasons and are never guessed.** The **equity complex** is `equity`, `etf`, `index` and nothing else. `npl.register.assetclass`, pure and path-free. |
| **Power assumptions** | E1 true share 0.65; **E2 true share 0.625** under the 1× floor, by stated linear interpolation between multiple 0 (E1's 0.65) and multiple 2 (the registered 0.60) — a choice, not a measurement, so **every minimum N is also reported at the unchanged 0.60** (E2 then needs 92/184 and does not reach 0.80 by the deadline). All generating-sample-derived (P3 pair share 114/175 = 0.651; paired price differential +6.43 points, funding differential +0.88, n = 175). |
| **Named secondaries added** | The **tier stratum** and the **class-pair stratum** (H2-5), plus the `same_dex` stratum and the pre-amendment **2× floor** (H2-3) — all computed beside every primary figure at every look, all descriptive and never verdict-bearing. |
| **What the tightening cost, measured** | Match rate 1.000 → **0.873**; pairs at the deadline 135 → **110**; look 1 +28 days, look 2 +30 days; two-look power 0.8629 → **0.8088**; Section 0 single-look **GO → DEGRADED** at 0.7994. Mean absolute event-to-elder funding distance widens 4.886e-05 → **5.679e-05** (+16.2 %), the registered accepted degradation — funding carries 12.0 % of the paired signal (0.88 of 6.43 + 0.88, n = 175) and a cross-complex pair destroyed the other 88 %. |
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

### H5 — HIP-3 equity-style perpetual basis (a feasibility entry, not a hypothesis)

> Do HIP-3 equity-style perps trade at a persistent, measurable deviation
> from their underlying reference, and is that deviation large relative to
> the 18 bp round-trip cost floor?

| | |
|---|---|
| **Status** | **PENDING — the census window is open** · fired 2026-08-28T22:20Z. Both structural clauses **clear**; what is missing is time. **29 daily passes needed; projected fire date 2026-09-26.** Collector armed |
| **Registration** | `registrations/H5/REGISTRATION.md` — Sections 0–9, Amendments H5-1 and H5-2, and the Section 6 verdict record |
| **What it is** | **A feasibility entry.** No capital, no Stage B read of a trading outcome, no Stage C. A VIABLE row authorizes exactly one thing: writing a registration in a **different repository**, against an independent underlying feed. |
| **Design in one line** | Every instrument on every HIP-3 dex whose ticker resolves, by an **exact-string mapping registered before any price was read**, to an equity, ETF or index underlying; a daily snapshot of mark, the venue's own oracle, funding **service**, open interest and one `l2Book`; basis = (mark − reference)/reference in bp, **computed only from fields the venue served in the same snapshot**, tagged by US market session against a calendar registered before collection. |
| **Deciding numbers so far** | **94** live instruments carry a served reference (bar 20) — **clears**. Funding served on **94 of 94**, share **1.000** (bar 0.500) — **clears**. **0** instruments at 30 days of coverage (bar 20) — the window is open. Two snapshots, **188** observations, **0 absent**, session tag `extended`: **median absolute basis 4.14 bp**, IQR 0.71–9.15, **9.57 %** over the 18 bp floor, **1.60 %** over the 54 bp bar. |
| **Universe** | 273 HIP-3 instruments over 10 dexs → **151 resolved** (118 equity, 15 ETF, 18 index), 80 `excluded_non_equity`, 42 `excluded_unresolvable`, → **94 live** after the three-field delisted rule (57 excluded, **0 conflicting**). The live family is two dexs: `xyz` 73, `para` 16. |
| **The retrospective answer** | **No retrospective basis exists.** The venue serves no historical mark and no historical oracle in the same row, and `candleSnapshot` is closed to this entry by standing rule 7. It serves `premium` hourly — measured to be an **impact-price** deviation, so a **named secondary** that may fire CLOSED and never VIABLE. The secondary's cohort gate leaves **27 of 151** eligible, of which 25 have no funding history at all and 2 are days old: **39 observations, 2 instruments, 0 meeting coverage.** Fires nothing, recorded as a shortfall. |
| **The honesty clause, demonstrated** | **32 delisted instruments — zero open interest, zero volume, no book — are still served an unbroken hourly funding series**, latest row 2026-08-28T21:00Z. And the delisted stratum is where **every** observation above the 54 bp bar lived: median 30.5 bp with 45.6 % over the bar, against 3.72 bp and **0.0 %** for live instruments in the same snapshot. Amendment H5-2 excludes them, which deleted this entry's only route to VIABLE. |
| **Quarantine** | H2's collectors, ledgers, latches and stores are **read-only** to every H5 path, enforced by `npl.h5.stores` (write containment) and pinned by test; the cohort ledgers are read precisely so the quarantine can be honoured. H5 reads **no candle** and **no funding rate value**, anywhere. |
| **Operator prior slot** | Reserved, empty. It blocks **the successor draft**, not the map: a verdict is never withheld for want of a prior. |
| **What would close it early** | Nothing measured so far. Both structural CLOSED clauses are already cleared; the entry now turns on whether the median absolute basis, over a full 30-day census across all four session tags, sits under 18 bp everywhere (CLOSED), between 18 and 54 (INDETERMINATE), or over 54 in at least one tag (VIABLE). On the first 188 observations it sits at **4.14 bp**. |

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
