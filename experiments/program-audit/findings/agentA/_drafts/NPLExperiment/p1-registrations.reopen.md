# REOPEN LEDGER — NPLExperiment, part p1-registrations

**Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c (main, 2026-09-02;
live HEAD equals the anchor as of 2026-09-04, zero commits after it).
**Scope:** the five register entries as they are stated in my assigned documents — `REGISTRATION.md`,
`registrations/H2..H5/REGISTRATION.md`, `HYPOTHESES.md`, `report.md`, `README.md`. Factual, not
advocacy. Line references are into the anchored snapshot; paths are repo-relative.
**Register-wide rule that governs every row:** the five entries sit under one familywise budget
fixed by an outcome-blind cull at **k = 1, alpha_h = 0.05** (`HYPOTHESES.md`:143-147;
`registrations/H2/REGISTRATION.md`:261-266). H5 sits outside that budget
(`HYPOTHESES.md`:27-28).

---

## H1 — H-NPL, the naive new-listing short

| field | value |
|---|---|
| **Status** | **CLOSED — NEGATIVE** |
| **Closure kind** | Registered single sealed read; the mechanical FAIL row of a verdict table registered before the reader existed (`REGISTRATION.md`:459-479, 534-538) |
| **Closure date** | 2026-08-28 (latch 03:01:01Z, read completed 03:01:08Z) — `REGISTRATION.md`:540-545 |
| **Deciding figure (n)** | **P1** 197/312 positive (63.14 %), exact Clopper–Pearson lower bound **0.5707** at alpha_adj 0.016952 against a 0.60 bar — **FAIL** (n = 312) — `REGISTRATION.md`:554-558. **P2** 111/312 (35.58 %) at ≤ −15 % net, sign-test p = **1.000** — **FAIL** (n = 312) — `REGISTRATION.md`:559-561. **P3** 114/175 pairs (65.14 %), p = **3.767e-05** — **PASS** (n = 175) — `REGISTRATION.md`:562-565. Either P1 or P2 failing fires FAIL (`REGISTRATION.md`:475-479) |
| **Cost sensitivity** | P1 lb 0.5740 / 0.5707 / 0.5609 (198/197/194 of 312); P2 and P3 identical at every band — `REGISTRATION.md`:566-569 |
| **Secondary horizon, recorded but not verdict-bearing** | 90-day: share positive 208/312 = 66.67 %, lb **0.6069** (clears the 0.60 bar); P2-90d 159/312, p = 0.3886; P3-90d 111/175, p = 2.36e-04 (n = 312 / 312 / 175) — `REGISTRATION.md`:570-572, `report.md`:233-235 |
| **Blockers (stated)** | None outstanding at closure — "Open operator items: none." (`report.md`:306). The pre-closure blocker, the Section 13 operator prior slot, was filled 0.40 (adopted) 2026-08-27 and is spent with the closure (`REGISTRATION.md`:285-292, 653-656) |
| **Reopen conditions (stated)** | "**Nothing reopens H1 itself** — the registered short does not clear its bars on this sample, and the sample is spent." — `HYPOTHESES.md`:56. The residual is routed to H2/H3/H4 as new hypotheses on fresh data (`HYPOTHESES.md`:56; `REGISTRATION.md`:605-612) |
| **Possibly met by other repo?** | **No, for reopening.** But three carried external figures underpin its framing and belong in the cross-repo pass: MLCryptoEngine H8 (+43.68 %/yr funding vs −42.91 % price, 231 perps, 1,182 days, 4,411,046 hourly observations) and H5 (MERL −22.38, TNSR −32.41 %/yr) at `REGISTRATION.md`:58-76; solclear Finding 2 (60 points of death-rate gap) at `REGISTRATION.md`:193-194; and the three unverifiable third-party listing studies (Delphi 652 CEX listings 12 % profitable, median −82 %; Animoca 773 listings; Memento 118 TGEs 84.7 % below listing) at `REGISTRATION.md`:69-73 |
| **Audit note (advocacy, see p1-registrations.md)** | DRAFT-p1-registrations-5: the 90-day row clears P1's registered bar and appears in neither the closure entry (`REGISTRATION.md`:592-612), the register index row (`HYPOTHESES.md`:52), nor the README (`README.md`:6-10), while the reopen clause is unconditional |

---

## H2 — the age-contrast pair

| field | value |
|---|---|
| **Status** | **OPEN — survivor, armed, amended to a two-look plan.** Section 0 fired **DEGRADED** 2026-08-28 (`registrations/H2/REGISTRATION.md`:268), recomputed to GO-level power after amendment but the DEGRADED record is deliberately not re-fired (`registrations/H2/REGISTRATION.md`:751-760) |
| **Closure kind** | None. Two registered looks remain: look 1 projects to **2026-11-26**, look 2 to **2027-03-01**, deadline 2027-03-31 (`registrations/H2/REGISTRATION.md`:742-749) |
| **Closure date** | n/a |
| **Deciding figure (n)** | At the cull: E1 **0.9743** / E2 **0.7604** at 141 projected deadline pairs, alpha_h 0.05 — weaker leg in [0.50, 0.80) → DEGRADED (`registrations/H2/REGISTRATION.md`:290-293). Post-amendment recomputed power at 135 projected pairs: **0.8886** single-look, **0.8629** two-look (`registrations/H2/REGISTRATION.md`:751-758). Achieved pairs **62/62** (38 same_dex + 24 cross_dex), match rate 0.613 → **1.000** (`registrations/H2/REGISTRATION.md`:638-639, 727-730) |
| **Read boundaries** | Look-1 min N **59** (E1 42, E2 59), look-2 min N **117** (E1 84, E2 117); at n₂ = 117: k₁ = 38, k₂ = 69, exact spend 0.0182 + 0.0240 = 0.0422 (`registrations/H2/REGISTRATION.md`:671-696). Futility at n₁ = 59: **E1 f₁ = 31, E2 f₁ = 27** (`registrations/H2/REGISTRATION.md`:712-718) |
| **Blockers (stated)** | (1) **The operator prior slot, reserved and empty — blocks H2's Stage B structurally at both looks** (`registrations/H2/REGISTRATION.md`:235-242 and 633; `README.md`:80-86; `report.md`:598-600). (2) Explicit operator instruction required at each look (`registrations/H2/REGISTRATION.md`:200, 592-594). (3) Achieved eligible pair count at the look's registered minimum N (`registrations/H2/REGISTRATION.md`:594-595). (4) The generating-sample quarantine bars all 312 retro events from every H2 verdict statistic (`registrations/H2/REGISTRATION.md`:64-66, 626-627) |
| **Blockers lifted since registration** | **Yes, one, and it was properly revisited by amendment:** the same-dex match-rate blocker (0.613; para/mkts/io unpairable until deterministic 2026-09-26 / 2026-12-26 / 2027-02-13 dates — `registrations/H2/REGISTRATION.md`:274-280) was lifted by the Amendment H2-3 main-dex fallback control, taking the backfill match rate to 1.000 (`registrations/H2/REGISTRATION.md`:401-443, 727-730). Recorded here because it is the pattern the audit hunts for — here the label *was* revisited |
| **Reopen conditions (stated)** | n/a — the entry is open. Its terminal rows are registered: GO / CONTINUE / futility-FAIL at look 1, GO / FAIL at look 2 (`registrations/H2/REGISTRATION.md`:564-578) |
| **Possibly met by other repo?** | No. H2 admits fresh NPLExperiment events only; no other repository can supply them |
| **Audit notes (advocacy)** | DRAFT-p1-registrations-2 (E1's futility n₂ = 84 versus the design's governing look-2 N of 117); DRAFT-p1-registrations-3 (look 2 fires at the deadline but the trigger requires the look-2 minimum N; no underpowered row exists) |

---

## H3 — the population-corrected naive short

| field | value |
|---|---|
| **Status** | **BLOCKED** — "Nothing is armed for H3." (`registrations/H3/REGISTRATION.md`:157) |
| **Closure kind** | Outcome-blind power cull, Section 0 map fired at the register's k/alpha fixed point by `npl.register.cull.fire_hypothesis_section0`; the cull reads counts, rates and timestamps only (`registrations/H3/REGISTRATION.md`:150-159; `HYPOTHESES.md`:143-147) |
| **Closure date** | 2026-08-28 (Amendment H3-1) — `registrations/H3/REGISTRATION.md`:150 |
| **Deciding figure (n)** | Measured main-dex accrual **0.5 events/month (n = 3 listings in the trailing 182 days)**; achieved fresh main-dex N = **2**, projected **5 by 2027-03-31**; P1 power at n = 5 (true share 0.677) = **0.0000**; MAG power **0.0057** at the governing generating-sample share 0.356 (0.1160 at the H1-registered 0.65); P1 min-N **262** at alpha 0.05, **361** at the k = 3 alpha; MAG reaches 0.80 at **no n** because the governing true share sits below the sign-test null — `registrations/H3/REGISTRATION.md`:161-177. Eligibility: 2 eligible, 60 excluded `hip3_builder_dex` (`registrations/H3/REGISTRATION.md`:166-167) |
| **Blockers (stated)** | (1) The venue's measured main-dex listing rate, 0.5/month (`registrations/H3/REGISTRATION.md`:161-163) — this is the binding one. (2) The generating-sample quarantine: the 158 main-dex retro events are inadmissible, leaving N = 2 achieved (`registrations/H3/REGISTRATION.md`:56-57). (3) The 2027-03-31 register deadline (`registrations/H3/REGISTRATION.md`:17-21). (4) The operator prior slot, reserved and empty — moot, a BLOCKED design has no Stage B to gate (`registrations/H3/REGISTRATION.md`:134-141, 182-183) |
| **Reopen conditions (stated)** | **Three, in the registration:** "a main-dex listing rate near 40–50/month sustained (min-N 262 against 0.5/month measured), a register deadline years longer, or a successor registration on a **different venue** whose main-population listing rate supports the bars" — `registrations/H3/REGISTRATION.md`:184-188. **Two, in the register index**, and narrower: "Reopens only on an order-of-magnitude higher main-dex listing rate or a longer-horizon successor registration" — `HYPOTHESES.md`:89 |
| **Trigger met by a later entry in this repo?** | **No.** No main-dex accrual re-measurement exists after 2026-08-28 in the snapshot; the deadline is unchanged |
| **Possibly met by other repo?** | **Yes — flag for the cross-repo pass.** The third registered reopener is a successor "on a different venue whose main-population listing rate supports the bars". Any audited repository holding a measured token-listing rate for a different venue (e.g. a CEX-listing or new-token cohort in MLCryptoEngine, ETFExperiment, or NPDExperiment) would bear directly on it. The reopener is absent from `HYPOTHESES.md`:89, which is the document a reader is told to consult first (`HYPOTHESES.md`:3) |
| **Audit note (advocacy)** | DRAFT-p1-registrations-4. The BLOCK itself is sound and I verified it against sampling error: exact Poisson 95 % interval on 3 events/182 d is [0.103, 1.466]/month, yielding at most **10.4** events by 2027-03-31 against a min-N of 262 |

---

## H4 — the funding-conditioned short

| field | value |
|---|---|
| **Status** | **BLOCKED** — "Nothing is armed for H4." (`registrations/H4/REGISTRATION.md`:205) |
| **Closure kind** | Outcome-blind power cull, Section 0 map (best cell governs, grid disjunctive) fired at the cull's pass-1 alpha (k = 3, alpha_h = 0.016952; alpha_cell = 0.00568 Sidak-within) — `registrations/H4/REGISTRATION.md`:16-25, 205-208 |
| **Closure date** | 2026-08-28 (Amendment H4-2) — `registrations/H4/REGISTRATION.md`:197 |
| **Deciding figure (n)** | Measured conditioning rates, **n = 62 fresh events, 0 absent**: le −10 %/yr **0.1774 (11/62)**, le −20 % **0.1290 (8/62)**, le −40 % **0.0806 (5/62)**; fresh-cohort median trailing entry funding **+31.6 %/yr** (n = 62, min −132.4, max +403.5); deadline cell sizes 30 / 22 / 13; **best-cell power 0.0140** at the governing generating-sample share 0.631, **0.7106** at the H1-registered 0.85; min-N not reached by n = 1200 (power 0.354) at the governing share — `registrations/H4/REGISTRATION.md`:210-225 |
| **Blockers (stated)** | (1) The rarity of deeply negative entry funding on this venue (median +31.6 %/yr, n = 62) — `registrations/H4/REGISTRATION.md`:213-216. (2) The thinness of the fresh cohort (rate × 173 projected events) — `registrations/H4/REGISTRATION.md`:217-218. (3) The 2027-03-31 deadline (`registrations/H4/REGISTRATION.md`:20-25). (4) The generating-sample quarantine (`registrations/H4/REGISTRATION.md`:53-54). (5) The operator prior slot, reserved and empty — moot for a BLOCKED design (`registrations/H4/REGISTRATION.md`:151-158, 229-230) |
| **Reopen conditions (stated)** | **Three, in the registration:** "a funding regime in which deeply negative entry funding stops being rare (conditioning rates several times higher, sustained), **a much larger listing rate**, or **a redesign of the conditioning claim strong enough to justify the near-0.85 conditional share** — each a new registration" — `registrations/H4/REGISTRATION.md`:230-234. **One, in the register index:** "Reopens only on a persistent negative-funding listing regime — a new registration" — `HYPOTHESES.md`:106 |
| **Trigger met by a later entry in this repo?** | **No.** No conditioning-rate re-measurement exists after 2026-08-28 in the snapshot |
| **Possibly met by other repo?** | **Yes — flag for the cross-repo pass.** (a) The third registered reopener turns on the conditional share assumption; MLCryptoEngine H5/H8 hold measured funding-versus-price decompositions on 231 Hyperliquid perps over 1,182 days (carried at `REGISTRATION.md`:58-76) and any conditional-on-negative-funding profitability share measured there speaks directly to whether the near-0.85 conditional share is justifiable. (b) A negative-funding *regime* measurement in any crypto-funding repository (MLCryptoEngine, AiTrader) would bear on the first reopener. Neither reopener survives into `HYPOTHESES.md`:106 |
| **Audit note (advocacy)** | DRAFT-p1-registrations-1: the BLOCKED label's registered condition ("every cell under 50 percent power") is not satisfied at the alternative assumption the amendment itself reports (best cell 0.7106, inside the registered DEGRADED band 0.50–0.80); and the conditioning rate that fixes the cell size carries no interval — its exact 95 % CI is [0.0920, 0.2953], at whose upper end the deadline cell is n = 51 and power at 0.85 is 0.9286 |

---

## H5 — HIP-3 equity-style perpetual basis (feasibility entry, not a trade hypothesis)

| field | value |
|---|---|
| **Status** | **PENDING — non-terminal, census window open.** Fired 2026-08-28 (record headed 22:20Z; actual firing time corrected to **22:04:30Z** by an appended correction) — `registrations/H5/REGISTRATION.md`:555, 632-639. Terminal states are VIABLE / INDETERMINATE / CLOSED (`registrations/H5/REGISTRATION.md`:231-264) |
| **Closure kind** | n/a yet. **29 daily passes needed; projected fire date 2026-09-26** — `registrations/H5/REGISTRATION.md`:586-589 |
| **Closure date** | n/a |
| **Deciding figure (n)** | Structural clauses both clear: **94 of 94** live instruments carry a served reference (`oraclePx`), bar 20; funding served **94 of 94, share 1.000**, bar 0.500. Coverage clause open: **0** instruments at 30 days of coverage, bar 20. Contemporaneous basis: **median absolute 4.14 bp**, IQR 0.71–9.15, **n = 188** observations (94 instruments × 2 snapshots, both session tag `extended`), 9.57 % over the 18 bp floor, 1.60 % over the 54 bp bar; `regular` / `closed_weekday` / `weekend` have **no observations yet** — `registrations/H5/REGISTRATION.md`:562-589. Live-versus-delisted split, n = 94 / 57: median 3.72 bp (max 51.4, **0.0 %** over 54 bp) versus 30.52 bp (max 2,481, **45.6 %** over 54 bp) — `report.md`:657-660 |
| **Named secondary (venue `premium`)** | **PENDING and not projectable; fires nothing.** 27 of 151 eligible after the cohort gate, **124 `excluded_quarantined`**; of the 27, 25 return no funding rows and 2 are days-old listings → **39 observations, 2 instruments, 0 meeting coverage** — `registrations/H5/REGISTRATION.md`:597-616, `report.md`:691-701. Registered asymmetry: it may fire CLOSED, never VIABLE (`registrations/H5/REGISTRATION.md`:273-282) |
| **Blockers (stated)** | (1) **No retrospective basis of the registered construction**: the venue serves no historical mark and no historical oracle in the same row, and `candleSnapshot` is closed to the entry by **standing rule 7** — `registrations/H5/REGISTRATION.md`:38-45, 433-437; `HYPOTHESES.md`:128; `report.md`:644. (2) **The retrospective cohort gate**: "Its coverage cannot be reached. The gate is permanent" — `registrations/H5/REGISTRATION.md`:609-616. (3) **Amendment H5-2's delisted exclusion**, which "deleted this entry's only route to VIABLE" — `HYPOTHESES.md`:129; `registrations/H5/REGISTRATION.md`:517-523. (4) **The IBKR equity-leg economics carried from HFExperiment ADR-026** — fractional orders refused (error 10243), whole-share round trips 40–100 bp at this operator's sizes, "so **no cross-venue pair design is registrable here**" — `registrations/H5/REGISTRATION.md`:199-204; `report.md`:713-717. (5) The operator prior slot, reserved and empty — blocks only the **successor draft**, never the map: "a verdict is never withheld for want of a prior" — `registrations/H5/REGISTRATION.md`:348-359; `README.md`:87-91. (6) Section 4's self-imposed scope: "**This entry reads no external equity price feed.**" — `registrations/H5/REGISTRATION.md`:174 |
| **Reopen / consequence conditions (stated)** | A **VIABLE** row authorizes exactly one action: "writing a registration in a **different repository** … against an independent underlying feed", no capital (`registrations/H5/REGISTRATION.md`:243-246, 328-330; `HYPOTHESES.md`:124). **CLOSED** stops collection and closes the family (`registrations/H5/REGISTRATION.md`:253-257). "**What would close it early:** Nothing measured so far." (`HYPOTHESES.md`:132) |
| **Trigger met by a later entry in this repo?** | **No.** The entry is pending and no later measurement exists in the snapshot |
| **Possibly met by other repo?** | **Yes — two, flag for the cross-repo pass.** (a) **Blocker (4), the IBKR figure**, is a carried, unverified-in-repo external from **HFExperiment ADR-026** (anchor 82e77a021256d917c665ff6d4304c25b08f35451); if ADR-026 has been superseded, re-measured, or scoped to a size band, the categorical "no cross-venue pair design is registrable here" is stale. (b) **The independent underlying feed** that blockers (1) and (6) turn on is precisely the resource a VIABLE row would require; any audited repository already holding a licensed or free equity/ETF reference feed (ETFExperiment is the obvious candidate) bears on whether that blocker is real for the program as a whole, even though it is real for this entry's registered scope |
| **Audit notes (advocacy)** | DRAFT-p1-registrations-6 (the gate is instrument-scoped where its own rationale and standing rule 13 are window-scoped); DRAFT-p1-registrations-7 (the retrospective absence is a scope fact stated as a world fact); DRAFT-p1-registrations-8 (the carried IBKR blocker) |

---

## Cross-repository items extracted from this part, consolidated

| item | carried from | where it appears here | why it matters |
|---|---|---|---|
| IBKR: fractional orders refused (error 10243), 40–100 bp whole-share round trips at this operator's sizes | HFExperiment ADR-026, "closed and carried" | `registrations/H5/REGISTRATION.md`:199-204; `report.md`:713-717 | Load-bearing: it forecloses the cross-venue family "even if the deviation were real and large" |
| MLCryptoEngine H8: +43.68 %/yr funding vs −42.91 % price, 231 perps, 1,182 days, 4,411,046 hourly observations, net +0.11 % | MLCryptoEngine HYPOTHESES.md H8 | `REGISTRATION.md`:58-67 | The premise of H1's whole framing and of H4's motivation |
| MLCryptoEngine H5: MERL funding −22.38 %/yr, TNSR −32.41 %/yr | MLCryptoEngine HYPOTHESES.md H5 | `REGISTRATION.md`:73-76 | Sizes the funding leg the short pays |
| solclear Finding 2: 60 points of death-rate gap from dropping delistings | solclear findings | `REGISTRATION.md`:193-194 | The stated reason delistings are retained and truncated rather than dropped |
| Delphi (652 CEX listings since Jan 2025, 12 % profitable, median −82 %); Animoca (773 listings, median −40 to −70 %); Memento (118 TGEs, 84.7 % below listing) | third-party, "not independently verifiable live" | `REGISTRATION.md`:69-73 | The external base rate behind H1's registered 0.85 P1 assumption and behind H3's population argument |
| NPD Amendment 0 lesson: an adopted prior corrupts the calibration ledger | NPDExperiment | `REGISTRATION.md`:280-283 and each successor's Section 13 | The standing adoption warning; H1's own slot was nonetheless filled **0.40 (adopted)** (`REGISTRATION.md`:287) |
| solattn lesson: rate ceilings are per endpoint, measured never assumed | solattn | `REGISTRATION.md`:267-271 | Basis for the Amendment 1 pacing figures |
