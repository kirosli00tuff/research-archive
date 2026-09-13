# Agent A draft findings — NPLExperiment, part p1-registrations

**Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c (main, 2026-09-02)
**Assigned documents (read complete):** `REGISTRATION.md` (659 lines), `HYPOTHESES.md` (154),
`README.md` (91), `report.md` (717), `registrations/H2/REGISTRATION.md` (789),
`registrations/H3/REGISTRATION.md` (188), `registrations/H4/REGISTRATION.md` (234),
`registrations/H5/REGISTRATION.md` (647). Context read: `DECISIONS.md` (ADR index + ADR-024/025/029/030/031),
`src/npl/h5/gate.py`, `reports/h5/retro.json`.
**Recomputation environment:** `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python`
(scipy exact binomial / Clopper–Pearson). Scripts and outputs:
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-NPL-p1/recompute{,2,3,4,5,6}.py`.

**Stated up front, because it bears on every finding below:** every published figure I could
re-derive in these documents reproduced **exactly** — P1 lb 0.5707 and 0.6069, P2/P3 sign-test
p-values, H3's min-N 262/361, H4's cell powers 0.0140/0.0037/0.0025 and 0.7106/0.3382/0.1209,
H4's "power at 1200 = 0.354", and the whole H2 two-look boundary table (k₁ 38, k₂ 69, spend
0.0182 + 0.0240 = 0.0422, powers 0.9322/0.8237; deadline row k₁ 43, k₂ 79, 0.9552/0.8629;
futility f₁ = 31 and 27). **I found no arithmetic error anywhere in this repository.** Every
finding below is about a *label*, a *scope choice*, or an *assumption* — never about a
miscomputation.

---

### DRAFT-p1-registrations-1
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H4, the funding-conditioned short — Amendment H4-2, Section 0 verdict record (BLOCKED)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the optimistic H1-registered 0.85 (reported beside, the honest range): 0.7106 / 0.3382 / 0.1209 — under the GO floor even at the assumption the register declined to adopt." — NPLExperiment/registrations/H4/REGISTRATION.md:221-223
- **Evidence:**
  - H4's own Section 0 map has **three** bands, not two: "**GO:** at least one registered cell reaches **80 percent power** …"; "**DEGRADED:** the best cell lands between **50 and 80 percent**."; "**BLOCKED:** every cell **under 50 percent power** … Nothing armed for H4." — NPLExperiment/registrations/H4/REGISTRATION.md:20-25.
  - The row that fired is BLOCKED — "**The verdict: BLOCKED. Nothing is armed for H4.**" (NPLExperiment/registrations/H4/REGISTRATION.md:205). Its registered precondition is *every cell under 0.50*. At the alternative assumption the amendment itself reports, the best cell is **0.7106**, which is **inside the registered DEGRADED band [0.50, 0.80)** — so under that assumption the fired row's own condition is not satisfied. The amendment describes 0.7106 only as "under the GO floor" and never as inside DEGRADED, i.e. it reports the alternative as if it corroborated BLOCKED when by H4's own map it selects a different row. DEGRADED means "Collection proceeds" (the same clause that kept H2 alive — NPLExperiment/registrations/H2/REGISTRATION.md:33-35).
  - The 0.85 is not an outcome-fitted number: it is H1's **pre-registered** P1 power assumption, fixed 2026-08-27 before any datum existed — "Registered power assumption: true share **0.85**." (NPLExperiment/REGISTRATION.md:207). The figure the register made governing instead, **0.631**, is the *unconditional* generating-sample share 197/312 (NPLExperiment/registrations/H4/REGISTRATION.md:102-103) — and H4's hypothesis is exactly that the *conditional* share exceeds the unconditional one (NPLExperiment/registrations/H4/REGISTRATION.md:35-39). Under 0.631 no achievable n powers the test at all: the registration's own figure is "power at 1200 = 0.354" against 30 achievable (NPLExperiment/registrations/H4/REGISTRATION.md:224-225), which I reproduce exactly (0.35397). A power assumption under which the hypothesis is false makes BLOCKED the only reachable row for any conditioning design, whatever its merit.
  - The deciding count and its n: conditioning rates **0.1774 (11/62)**, 0.1290 (8/62), 0.0806 (5/62), n = 62 fresh events, 0 absent (NPLExperiment/registrations/H4/REGISTRATION.md:210-212); deadline cell sizes 30 / 22 / 13 at rate × 173 (NPLExperiment/registrations/H4/REGISTRATION.md:217-218).
  - **No interval is reported on the rate that decides the cell size.** Exact 95 % Clopper–Pearson on 11/62 is **[0.0920, 0.2953]** — a factor of 3.2. At the upper bound the deadline cell is n = 51 and the best-cell power at the H1-registered 0.85 is **0.9286**, i.e. a **GO**.
  - Contrast, and it is the point: for H3 the same amendment style states insensitivity explicitly — "Both required co-primaries sit under the 0.50 floor at every alpha considered; the verdict is insensitive to the k/alpha question and to the magnitude-leg assumption." (NPLExperiment/registrations/H3/REGISTRATION.md:171-173). No such sensitivity statement exists for H4, and H4 is the one that is sensitive. H3's block is robust to the analogous sampling error (below); H4's is not.
  - Cost of keeping H4 alive: H4 conditions on the cohort H2 already collects — "The **full fresh cohort** of registrations/H2 Section 2" (NPLExperiment/registrations/H4/REGISTRATION.md:50-51) — so DEGRADED costs no additional collection. It does cost H2 alpha, because k would rise from 1; I state that honestly (NPLExperiment/registrations/H2/REGISTRATION.md:264-266).
- **Recomputation (if any):**
  - Inputs: p₀ = 0.60 (bar, NPLExperiment/registrations/H4/REGISTRATION.md:94); alpha_cell = 0.005683 Sidak-within at k = 3 (NPLExperiment/registrations/H4/REGISTRATION.md:207); n = 30 (NPLExperiment/registrations/H4/REGISTRATION.md:217); p_true 0.631 and 0.85 (NPLExperiment/registrations/H4/REGISTRATION.md:102-103, 221).
  - Method: exact binomial, k* = min{k : P(X ≥ k | 0.60) ≤ alpha_cell}, power = P(X ≥ k* | p_true). Clopper–Pearson two-sided 95 % interval on 11/62.
  - Result: n = 30 → k* = 25; power 0.01401 at 0.631 (document: 0.0140) and **0.71059 at 0.85** (document: 0.7106). Both reproduce. 0.71059 ∈ [0.50, 0.80) = the registered DEGRADED band. CP 95 % on 11/62 = [0.0920, 0.2953]; at 0.2953 × 173 = 51 events, power at 0.85 = **0.9286**. Minimum cell n for 0.80 power at 0.85 = **41** → 41 / 0.1774 = **231 fresh events** ≈ 12.4 months at the measured 18.57 events/month (NPLExperiment/report.md:340), i.e. ≈ 2027-09 — past the 2027-03-31 deadline but not structurally unreachable.
- **What would resolve it:** either (a) re-fire H4's Section 0 with the band that its own reported alternative selects, recording DEGRADED-under-0.85 / BLOCKED-under-0.631 as the honest pair, or (b) state in H4-2 why a power assumption set to the unconditional share is the right assumption for a conditional design, and report the exact interval on the conditioning rate beside the cell sizes it determines. Cheapest decisive step: nothing needs collecting — H4's events are already being collected for H2.
- **Confidence:** HIGH — the two power figures are the document's own, both reproduce to four decimals, and the band boundaries are quoted from H4's own Section 0.
- **Invalidated by later commits?:** no — HEAD equals the anchored SHA at read time (verified 2026-09-04 by `git -C … rev-parse HEAD`; zero commits after 8f1fef8), and H4 is closed with nothing armed, so nothing in flight can move it. A future amendment could of course re-fire it.
- **Disclosed by authors?:** partially — the alternative-assumption powers are reported (NPLExperiment/registrations/H4/REGISTRATION.md:221-223) and the assumption principle is argued (NPLExperiment/registrations/H4/REGISTRATION.md:104-107, DECISIONS.md ADR-017). What is **not** disclosed is that 0.7106 falls inside H4's own DEGRADED band rather than supporting the BLOCKED row, and no interval on the conditioning rate appears anywhere.

---

### DRAFT-p1-registrations-2
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2, the age-contrast pair — Amendment H2-4 §4, the look-1 futility boundary
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Named now, before any outcome exists: n₂ for the look-1 futility computation is the co-primary's registered look-2 minimum N (table 2), or the observed n₁ where that is larger.**" — NPLExperiment/registrations/H2/REGISTRATION.md:707-709
- **Evidence:**
  - The registered table that follows uses **n₂ = 84 for E1** and n₂ = 117 for E2, giving "**Futility fires at look 1 when E1's positive count is 31 or fewer of 59, or E2's floor-clearing count is 27 or fewer of 59.**" (NPLExperiment/registrations/H2/REGISTRATION.md:712-718). Futility at look 1 is **terminal**: "| look 1 | S₁ ≤ f₁ for either co-primary (where f₁ is registered) | **FAIL**, terminal |" (NPLExperiment/registrations/H2/REGISTRATION.md:569).
  - But look 2 cannot fire at 84 pairs. Look 2 "fires at the **earlier** of the registered deadline (2027-03-31) and the date both co-primaries reach their **look-2 minimum N**" (NPLExperiment/registrations/H2/REGISTRATION.md:492-494), and the amendment's own governing figure two pages earlier is "**The governing figures: look-1 minimum N = 59 pairs, look-2 minimum N = 117 pairs** (the larger of the two co-primaries' at each look)." (NPLExperiment/registrations/H2/REGISTRATION.md:688-689). The projection puts look 2 at 117 pairs on 2027-03-01 and 135 at the deadline (NPLExperiment/registrations/H2/REGISTRATION.md:732-745).
  - So E1's futility boundary is computed against a look-2 sample of 84 that the design will never have; E1 will be judged at look 2 on **117** pairs at minimum. Conditional power is increasing in the remaining increment n₂ − n₁, so understating n₂ **inflates** f₁ and makes the terminal FAIL fire on more outcomes. For E2 the registered n₂ (117) coincides with the projection, so the defect is E1-specific — and E1 is the co-primary whose f₁ moves most.
  - Direction is not stated for this choice, in a document that states direction for every other one: "**Direction of the change: a relaxation.**" (NPLExperiment/registrations/H2/REGISTRATION.md:441), "**This is a weakening, stated plainly.**" (NPLExperiment/registrations/H2/REGISTRATION.md:451), "**This makes CLOSED strictly harder**" (NPLExperiment/registrations/H5/REGISTRATION.md:417-418), "**This makes VIABLE strictly harder.**" (NPLExperiment/registrations/H5/REGISTRATION.md:517). The one choice in the amendment set that tightens a terminal stop carries no direction statement.
- **Recomputation (if any):**
  - Inputs: n₁ = 59 (NPLExperiment/registrations/H2/REGISTRATION.md:688), alpha₁ = 0.02 / alpha₂ = 0.03 (NPLExperiment/registrations/H2/REGISTRATION.md:500-501), p₀ = ½, registered true shares E1 0.65 / E2 0.625 (NPLExperiment/registrations/H2/REGISTRATION.md:673-674), conditional-power floor 0.10 (NPLExperiment/registrations/H2/REGISTRATION.md:555-557), boundary formulas as registered (NPLExperiment/registrations/H2/REGISTRATION.md:520-526, 553).
  - Method: k₁ = min{k : P(Bin(59, ½) ≥ k) ≤ 0.02}; k₂ from the registered conditional spend; f₁ = largest s < k₁ with P(Bin(n₂ − 59, p) ≥ k₂ − s) < 0.10. Evaluated at n₂ ∈ {84, 117, 135}.
  - Result (k₁ = 38 in every case, reproducing the document): **E1 f₁ = 31 at n₂ = 84 (registered), 26 at n₂ = 117, 23 at n₂ = 135.** E2 f₁ = 27 at n₂ = 117 (registered, reproduces), 25 at n₂ = 135. Probability of a terminal look-1 futility stop **under the registered alternative p = 0.65**: **0.0326 at the registered n₂ = 84 versus 0.0008 at n₂ = 117** — a ~40× difference. Five outcomes (S₁ ∈ {27 … 31} of 59) fire a terminal FAIL under the registered rule and would not under the sample the design projects.
- **What would resolve it:** amend the look-1 futility n₂ to the **governing** look-2 minimum N (117), or to the projected look-2 N, for both co-primaries — and state the direction of the change, as every other H2/H5 amendment does. This can be done now: no pair outcome has been read (NPLExperiment/report.md:594-598).
- **Confidence:** HIGH — every input is a registered constant, the registered f₁ values reproduce exactly, and the mismatch is between two clauses of the same amendment.
- **Invalidated by later commits?:** yes, possibly — H2 is live, look 1 projects to 2026-11-26, and an amendment before look 1 would moot this. No commit after the anchor existed at read time.
- **Disclosed by authors?:** no — the amendment names the choice (NPLExperiment/registrations/H2/REGISTRATION.md:707-709) but neither states its direction nor notes that E1's n₂ of 84 is below the design's own governing look-2 N of 117.

---

### DRAFT-p1-registrations-3
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2 — Amendment H2-3 Change 3, the look-2 firing rule versus the Section 10 trigger
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Look 2** fires at the **earlier** of the registered deadline (2027-03-31) and the date both co-primaries reach their **look-2 minimum N**." — NPLExperiment/registrations/H2/REGISTRATION.md:492-494
- **Evidence:**
  - Look 2's outcome map has exactly two rows: "| look 2 | E1 **and** E2 both reject at k₂ | **GO** |" and "| look 2 | otherwise | **FAIL**, terminal |" (NPLExperiment/registrations/H2/REGISTRATION.md:571-572). There is no underpowered / inconclusive row anywhere in the map.
  - The same amendment also says the Stage B trigger still binds at each look and that "**The power condition becomes the look's registered minimum N in achieved eligible pairs.**" (NPLExperiment/registrations/H2/REGISTRATION.md:594-595), the look-2 registered minimum being 117 pairs (NPLExperiment/registrations/H2/REGISTRATION.md:688-689).
  - These two clauses disagree whenever the deadline arrives with fewer than 117 achieved eligible pairs. The harsher branch fires a **terminal FAIL on a sample the design itself declares underpowered**; the other branch produces no verdict at all inside the registered horizon — the very failure the amendment was written to avoid ("A registered experiment that cannot report inside its own horizon is not a strict experiment; it is an experiment that never answers." — NPLExperiment/report.md:440-441).
  - Headroom, with its n: the projection is 135 pairs at the deadline against a look-2 minimum of 117 (NPLExperiment/registrations/H2/REGISTRATION.md:740, 688-689), i.e. 15 % — resting on an accrual of 18.57 events/month measured over 182 days on n = 113 listings (NPLExperiment/report.md:340) and a match rate of 1.000 (62/62) achieved on the backfill cohort (NPLExperiment/registrations/H2/REGISTRATION.md:638-639). Forward pairs supply 73 of the 135 (NPLExperiment/registrations/H2/REGISTRATION.md:740); the conflict bites if forward accrual runs below about three-quarters of the measured rate.
- **Recomputation (if any):** arithmetic only — 135 − 117 = 18 pairs of headroom; the forward component is 73 of 135, so the shortfall threshold is 55 of 73 forward pairs ≈ 13.9 events/month against 18.57 measured.
- **What would resolve it:** register the missing row now, before look 1 — an explicit INCONCLUSIVE/UNDERPOWERED terminal state for "deadline reached with n₂ below the registered look-2 minimum", or an explicit statement that look 2 fires only on N and the deadline may pass unread. Either is outcome-blind and free today.
- **Confidence:** MEDIUM-HIGH — the textual conflict is plain; whether it ever binds depends on accrual that has not yet happened.
- **Invalidated by later commits?:** yes, possibly — H2 is live and an amendment could add the missing row; no commit after the anchor existed at read time.
- **Disclosed by authors?:** no — neither Amendment H2-3 nor H2-4 discusses the case where the deadline arrives short of the look-2 minimum N.

---

### DRAFT-p1-registrations-4
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** HYPOTHESES.md — the register index's reopen conditions for H3 and H4
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Reopens only on an order-of-magnitude higher main-dex listing rate or a longer-horizon successor registration" — NPLExperiment/HYPOTHESES.md:89
- **Evidence:**
  - H3's own registration lists **three** reopeners: "**What would reopen it:** a main-dex listing rate near 40–50/month sustained (min-N 262 against 0.5/ month measured), a register deadline years longer, or **a successor registration on a different venue whose main-population listing rate supports the bars**." — NPLExperiment/registrations/H3/REGISTRATION.md:184-188. The index's word is "**only**", and the clause it drops — a different venue — is the cheapest and most actionable of the three, because it is the one that does not require this venue's listing rate to change by two orders of magnitude.
  - The same narrowing happens for H4. Index: "Reopens only on a persistent negative-funding listing regime — a new registration" (NPLExperiment/HYPOTHESES.md:106). Registration: "**What would reopen it:** a funding regime in which deeply negative entry funding stops being rare (conditioning rates several times higher, sustained), **a much larger listing rate**, or **a redesign of the conditioning claim strong enough to justify the near-0.85 conditional share** — each a new registration." — NPLExperiment/registrations/H4/REGISTRATION.md:230-234. Two of three reopeners are dropped, including the one that maps directly onto DRAFT-p1-registrations-1.
  - This matters because of what HYPOTHESES.md is for, in its own words: "**Read this before proposing any new hypothesis on new-listing drift.**" (NPLExperiment/HYPOTHESES.md:3) and "The failure mode this file exists to prevent is retrying a settled question because the number that closed it is buried." (NPLExperiment/HYPOTHESES.md:32-33). A reader who consults only the index — which the index instructs — sees an exclusive list that is strictly narrower than the registered one.
  - No reopen trigger in this repository has in fact been met by a later entry in this repository: the two measured rates that gate H3 and H4 (0.5 main-dex events/month, n = 3/182d, NPLExperiment/registrations/H3/REGISTRATION.md:161-163; conditioning 0.1774/0.1290/0.0806, n = 62, NPLExperiment/registrations/H4/REGISTRATION.md:210-212) have no later re-measurement anywhere in the snapshot.
- **Recomputation (if any):** none — a document-to-document comparison.
- **What would resolve it:** carry all three registered reopen clauses verbatim into each index row, or replace "Reopens only on …" with a pointer to the registration's own clause.
- **Confidence:** HIGH — both texts are quoted in full and the mismatch is exact.
- **Invalidated by later commits?:** no — both entries are BLOCKED with nothing armed; an index edit would fix rather than invalidate the finding.
- **Disclosed by authors?:** no — the index gives no sign that its "only" list is an abridgement.

---

### DRAFT-p1-registrations-5
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H1 (H-NPL) — the closure entry, the register row, and the absence of any 90-day successor
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Nothing reopens H1 itself** — the registered short does not clear its bars on this sample, and the sample is spent." — NPLExperiment/HYPOTHESES.md:56
- **Evidence:**
  - H1's hypothesis is stated over **two** horizons: "A short opened at the registered entry anchor (Section 3) on newly listed Hyperliquid perpetuals earns a **positive net return over 30 and 90 days**" (NPLExperiment/REGISTRATION.md:53-55; identically at NPLExperiment/HYPOTHESES.md:44-46 and NPLExperiment/README.md:21-23). Section 7 makes 30 days primary and 90 days secondary (NPLExperiment/REGISTRATION.md:188).
  - At the 90-day horizon the profitability co-primary **clears its registered bar**: "90-day versions (descriptive): share positive 208/312 = 66.67 percent, lower bound **0.6069**" (NPLExperiment/REGISTRATION.md:570-571), against the registered bar of 0.60 (NPLExperiment/REGISTRATION.md:206). P3 also clears at 90 days (111/175, p = 2.36e-04, same lines). Only the magnitude leg fails, and it fails as a null rather than a rejection: 159/312, p = 0.3886.
  - The register row and the closure entry carry **only** the 30-day figures. HYPOTHESES.md's "Deciding numbers" cell lists P1 0.5707, P2 p = 1.000, P3 3.767e-05 and no 90-day figure at all (NPLExperiment/HYPOTHESES.md:52); the closure entry says "the exact lower bound on the profitability share (0.5707) misses 0.60, and the ≥15-point magnitude share (35.6 percent) is nowhere near one half" (NPLExperiment/REGISTRATION.md:600-602) without saying that both numbers describe the primary horizon only; README.md:8 compresses this to "magnitude leg far under".
  - No successor carries the 90-day horizon. H2: "**30 days primary, 90 days secondary (descriptive).**" (NPLExperiment/registrations/H2/REGISTRATION.md:141). H3: "(30d primary, 90d secondary …)" (NPLExperiment/registrations/H3/REGISTRATION.md:65-66). H4 carries H1 Sections 3, 4, 7 verbatim (NPLExperiment/registrations/H4/REGISTRATION.md:85-87). The outcome-blind cull scored exactly three 30-day designs (NPLExperiment/report.md:362-367); **no power number for any 90-day variant appears anywhere in the register.**
  - The data for a 90-day successor is already being collected at zero marginal cost: the fresh cohort's candle windows seal at **entry + 92 days** and funding advances to entry + 91 days (NPLExperiment/registrations/H2/REGISTRATION.md:334-341; NPLExperiment/report.md:396), so a 90-day outcome is readable on exactly the same date as the 30-day one.
  - And the register itself names a longer-horizon successor as a reopener for a sibling entry: "Reopens only on … a longer-horizon successor registration" (NPLExperiment/HYPOTHESES.md:89).
- **Recomputation (if any):**
  - Inputs: 208/312 and 159/312 and 111/175 (NPLExperiment/REGISTRATION.md:570-572); alpha_adj 0.016952 (NPLExperiment/REGISTRATION.md:201); alpha_h 0.05 (NPLExperiment/HYPOTHESES.md:70); bar 0.60; accrual 18.57 events/month and 135 readable fresh events by 2027-03-31 (NPLExperiment/report.md:340, 561).
  - Method: Clopper–Pearson lower bound; exact one-sided sign test; exact binomial power at p₀ = 0.60.
  - Result: 90-day P1 lb = **0.60687** at alpha_adj (document: 0.6069) and 0.62011 at alpha 0.05 — clears the bar at both. 90-day P2 share = **0.50962** (159/312) — **the point estimate is on the hypothesis side of one half**, a fact stated nowhere in these documents; p = 0.38859 (document: 0.3886). 90-day P3 p = 2.3605e-04. So at the horizon the hypothesis names, **two of three co-primaries clear and the third's point estimate is on the hypothesis side**, against one of three at the primary horizon with the magnitude leg at p ≈ 1.000.
  - **Against my own thesis, honestly:** a *fresh* 90-day profitability-only successor would not have survived the register's cull. At the generating-sample 90-day share 0.6667 and the projected 135 readable fresh events, power is **0.2635 (k = 3) / 0.3270 (k = 2) / 0.4677 (k = 1)** — under the 0.50 BLOCKED floor. It reaches 0.80 at **347 events** (alpha 0.05), ≈ 18 months of accrual at 18.57/month, i.e. about 2028-03. So the practical decision not to register one is defensible; what is not is asserting it unconditionally without ever computing it.
- **What would resolve it:** put the 90-day row into the register index's H1 entry beside the 30-day row, and replace "Nothing reopens H1 itself" with the deadline-bounded version the arithmetic supports ("a 90-day successor needs ≈ 347 fresh events, ≈ 2028-03 at the measured accrual"). That is the same form as H3's registered "a register deadline years longer".
- **Confidence:** MEDIUM — the numbers are certain and reproduce exactly; the judgement that omitting them from the register index matters rests on the index's own stated purpose.
- **Invalidated by later commits?:** no — H1 is closed and its read is spent; only an edit to the register index could change it.
- **Disclosed by authors?:** yes, in part — report.md:233-234 reports the 90-day lower bound and adds "(would sit above 0.60 — descriptive only)", and REGISTRATION.md:570-572 carries the same figures inside the verdict record. The authors therefore disclosed the number. What is not disclosed is that the register index, the closure entry, and the README carry none of it while asserting unconditional non-reopening, and that no 90-day successor was ever scored.

---

### DRAFT-p1-registrations-6
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — the retrospective deviation secondary and its cohort gate
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Its coverage cannot be reached. The gate is permanent, the forward collector records the registered basis rather than the premium history, and 25 of the 27 ungated instruments have no funding history at all." — NPLExperiment/registrations/H5/REGISTRATION.md:609-613
- **Evidence:**
  - The gate's own stated rationale is **window-scoped**: "reading it across a registered event's **open outcome window** would be a post-entry funding read wearing a different field name" (NPLExperiment/registrations/H5/REGISTRATION.md:57-59; identically NPLExperiment/src/npl/h5/gate.py:6-9 and DECISIONS.md ADR-031).
  - The implemented rule is **instrument-scoped**. `npl/h5/gate.py` carries no timestamp of any kind: `is_gated(coin, cohorts)` returns `coin in cohorts.all_coins` (NPLExperiment/src/npl/h5/gate.py:93-95), where `all_coins` is the union of the generating sample, the fresh plan and both pair legs (NPLExperiment/src/npl/h5/gate.py:50-52). Any row of any age on such a coin is refused (NPLExperiment/src/npl/h5/gate.py:98-107).
  - The register's own standing rule 13 is window-scoped and says the opposite for pre-entry rows: "**A trailing funding rate stamped at or before its event entry is a feature, never an outcome. The pin lists say exactly this**" (NPLExperiment/registrations/H4/REGISTRATION.md:61-63; NPLExperiment/REGISTRATION.md:650-652). A gate that excluded only rows inside (entry, entry + 92 d] would honour the stated rationale exactly and would leave every pre-entry row admissible.
  - For the generating-sample subset the gate is doubly conservative: those windows are all closed and their read is spent — "this cohort matured ≥ 90 days by construction" (NPLExperiment/REGISTRATION.md:523-525) and the single read was spent 2026-08-28T03:01:08Z (NPLExperiment/REGISTRATION.md:540-545). There is no open outcome window on them to protect.
  - The cost of the breadth, with its n: "eligible after the retrospective cohort gate | **27 of 151**; **124 `excluded_quarantined`**" and "of those 27 | **25** return no funding rows at all … **2** are days-old listings" → "**39 observations, 2 instruments, 0 meeting coverage**" (NPLExperiment/registrations/H5/REGISTRATION.md:598-600; NPLExperiment/report.md:691-695). The residue that survives the gate is essentially empty, so the gate — not the venue — is what makes the secondary unmeasurable.
  - The 62 fresh events' entries lie between 2026-05-30 and 2026-08-28 (NPLExperiment/report.md:516) against a registered 180-day retrospective lookback (NPLExperiment/registrations/H5/REGISTRATION.md:314-317), so for those coins a large majority of the lookback window is pre-entry and rule-13 clean.
  - What was given up is not nothing. On the 39 observations that did survive, the retrospective series' medians sit at or above the 18 bp cost floor in two of three tags — `regular` 14.17 bp (n = 17, 11.8 % over the floor, **5.9 % over the 54 bp bar**), `extended` 14.12 bp (n = 14), `closed_weekday` **20.60 bp** (n = 8, 62.5 % over the floor) (NPLExperiment/reports/h5/retro.json, fields `pooled_by_session_tag`; also NPLExperiment/registrations/H5/REGISTRATION.md:601) — against the contemporaneous live-instrument median of **3.72 bp** (n = 94, NPLExperiment/report.md:659). I state plainly that n = 8–17 on 2 instruments is not a measurement of anything, that `premium` is an impact-price construction and not comparable in level to mark-vs-oracle (NPLExperiment/registrations/H5/REGISTRATION.md:438-444), and that the registered asymmetry bars it from firing VIABLE in any case (NPLExperiment/registrations/H5/REGISTRATION.md:273-282). The point is only that the endpoint the gate deleted is the one whose numbers ran toward the question, not away from it.
- **Recomputation (if any):** none arithmetic. Derivation is from source: `src/npl/h5/gate.py` contains no time or window parameter anywhere (whole file read, 107 lines), confirming instrument scope; the counts 27 / 124 / 39 / 2 are read from `reports/h5/retro.json` (`instruments_eligible` 27, `instruments_excluded_quarantined` 124, `observations_served` 39, `instruments_with_any_observation` 2) and match the registration.
- **What would resolve it:** an amendment narrowing the retrospective gate from coin-scoped to window-scoped — refuse rows in (entry, entry + 92 d] on fresh-plan and pair-leg coins, admit everything else, and admit the generating-sample coins outright since their windows are closed and their read is spent. Then re-run `make h5-retro` (a one-off, budgeted at 1,812 requests, NPLExperiment/registrations/H5/REGISTRATION.md:314-318).
- **Confidence:** MEDIUM — the rationale/implementation mismatch is certain from the source; how much coverage a window-scoped gate would actually restore I cannot measure without reading the premium histories, which I did not do.
- **Invalidated by later commits?:** yes, possibly — H5 is live and fires 2026-09-26; an amendment before then would moot it. No commit after the anchor existed at read time.
- **Disclosed by authors?:** partially — ADR-031 discloses the cost and defends keeping it: "It cost the entry its retrospective sample (27 of 151 eligible, 39 usable observations) and was kept anyway: a gate relaxed after it turns out to be expensive is not a gate." (NPLExperiment/DECISIONS.md:544-546). What is not disclosed is that the gate is broader than its own stated rationale and than standing rule 13, i.e. that a narrower gate exists which forgoes nothing the rationale protects.

---

### DRAFT-p1-registrations-7
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 — the retrospective branch declared absent
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**No retrospective basis exists.** The venue serves no historical mark and no historical oracle in the same row, and `candleSnapshot` is closed to this entry by standing rule 7." — NPLExperiment/HYPOTHESES.md:128
- **Evidence:**
  - Half of the stated reason is a **self-imposed rule, not a data-availability fact**: "a candle read with a price is a rule-7 violation. So Task 3's retrospective series can come only from a venue-served field that carries a **deviation** directly" (NPLExperiment/registrations/H5/REGISTRATION.md:38-45; same at DECISIONS.md ADR-031:530-533). The venue does serve historical candles — the H1 collectors sealed 312 event windows and 176 control windows from `candleSnapshot` (NPLExperiment/report.md:74-77) — and the measured retention is full (NPLExperiment/report.md:334-338).
  - The other half of the reference is available from outside the venue, and the same registration names it as exactly what is needed: "**The successor repo would need an independent underlying feed** — a real quote for the real equity, on the real exchange calendar" (NPLExperiment/registrations/H5/REGISTRATION.md:195-197), and a VIABLE row's only authorized consequence is "writing a registration in a different repository … against an independent underlying feed" (NPLExperiment/registrations/H5/REGISTRATION.md:328-330).
  - The entry's cost rule does not forbid it. Section 7 is "**Zero dollars. Keyless public endpoints only.**" (NPLExperiment/registrations/H5/REGISTRATION.md:286). Free, keyless, public daily OHLC for US equities and ETFs is available — e.g. Stooq's CSV endpoint `https://stooq.com/q/d/l/?s=aapl.us&i=d` (my own knowledge, not measured in this session; it is keyless and free at the time of writing). What actually forbids it is a scope sentence: "**This entry reads no external equity price feed.**" (NPLExperiment/registrations/H5/REGISTRATION.md:174).
  - Consequence for the entry's own question: the retrospective half of "Do HIP-3 equity-style perps trade at a **persistent**, measurable deviation" (NPLExperiment/registrations/H5/REGISTRATION.md:72-74) is answered by absence rather than by measurement, and the entry instead waits 29 daily passes for a forward census (NPLExperiment/registrations/H5/REGISTRATION.md:586-589). A 180-day retrospective mark series against a free external reference would have answered it at once, for 94 live instruments, without the delisted-stratum artefact that Amendment H5-2 had to exclude.
- **Recomputation (if any):** none — this is a scope claim, not an arithmetic one.
- **What would resolve it:** either an amendment permitting a keyless external daily reference for the *retrospective* series only (leaving the contemporaneous venue-internal basis untouched and comparable), or — cheaper and sufficient for honesty — restating the claim as "no retrospective basis is available **within this entry's registered scope**" wherever it appears unqualified, notably NPLExperiment/HYPOTHESES.md:128.
- **Confidence:** LOW-MEDIUM — the scope decision is deliberate, argued at length and consistent; the finding is that the *summary* states it as a fact about the world.
- **Invalidated by later commits?:** yes, possibly — H5 is live until 2026-09-26. No commit after the anchor existed at read time.
- **Disclosed by authors?:** yes — the reason is given in the same sentence at HYPOTHESES.md:128 and in full at registrations/H5/REGISTRATION.md:38-45 and 174-197, and report.md:644 states it in the properly qualified form ("A retrospective basis **of the registered construction** does not exist"). This finding is therefore a wording/scope objection, not a discovery.

---

### DRAFT-p1-registrations-8
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 Section 4 — the carried IBKR execution blocker
- **Direction:** A
- **Class:** CROSS_REPO_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The equity leg through IBKR refuses fractional orders (error 10243) and bills whole-share round trips at **40 to 100 bp** at this operator's sizes (HFExperiment ADR-026, closed and carried), so **no cross-venue pair design is registrable here** even if the deviation were real and large." — NPLExperiment/registrations/H5/REGISTRATION.md:199-204
- **Evidence:**
  - The figure is an external, cross-repository carry with no in-repo verification: it is attributed to HFExperiment ADR-026 and no NPLExperiment measurement of it exists anywhere in the snapshot (`grep` for "10243" and "IBKR" returns only registrations/H5/REGISTRATION.md:199-204 and report.md:713-717).
  - It is load-bearing. It is the sentence that forecloses the whole cross-venue family "even if the deviation were real and large", and it is repeated as a closing line of the H5 narrative — "mean no cross-venue pair is registrable here in any case" (NPLExperiment/report.md:714-717).
  - Its scope is one broker at one operator's size. The claim generalised from it — that *no* cross-venue pair design is registrable — does not follow from a single broker's fee schedule, and the registration itself elsewhere contemplates a successor "in a different repository, against an independent underlying feed" whose execution venue is unspecified (NPLExperiment/registrations/H5/REGISTRATION.md:328-330).
  - **This is flagged for the cross-repository pass** rather than resolved here: whether HFExperiment ADR-026 has since been superseded, re-measured, or scoped to a size band is a question about HFExperiment (anchored 82e77a021256d917c665ff6d4304c25b08f35451), which is outside my assignment.
- **Recomputation (if any):** none — the underlying measurement is in another repository.
- **What would resolve it:** confirm ADR-026's current status and size scoping in HFExperiment at its anchor; if it is scoped to a size band or has been superseded, restate the H5 sentence as size-conditional rather than categorical.
- **Confidence:** MEDIUM — the quote and its carried-external status are certain; whether the blocker is stale is exactly what the cross-repo pass must decide.
- **Invalidated by later commits?:** no — the sentence is in a registered section that is never edited; only an amendment could restate it.
- **Disclosed by authors?:** partially — the source is named ("HFExperiment ADR-026, closed and carried"), which is good provenance practice; what is not disclosed is that the conclusion drawn is broader than the carried measurement's scope.

---

## What I checked and found sound

Listed with what I would have expected to find had the thesis held.

1. **Every recomputable figure in these documents.** P1 30d lb 0.5707 (197/312) and the cost-band variants 0.5740/0.5609; P2 30d p ≈ 1.000; P3 30d p = 3.767e-05; the 90-day trio; H3's min-N 262 at alpha 0.05 and 361 at the k = 3 alpha; H3's n = 5 powers of 0.0000/0.0057/0.1160; H4's 0.0140/0.0037/0.0025 and 0.7106/0.3382/0.1209 and "power at 1200 = 0.354"; H2's whole two-look boundary table including k₁ = 38, k₂ = 69, spend 0.0182 + 0.0240 = 0.0422, powers 0.9322/0.8237/0.8629, min-N 42/84/76 and 59/117/111 and 92/184/169, and the futility values f₁ = 31 and 27. **All reproduce to four or more decimals.** I expected to find a rounded-in-the-favourable-direction figure somewhere and did not find one. (NPLExperiment/REGISTRATION.md:554-580; registrations/H3/REGISTRATION.md:168-177; registrations/H4/REGISTRATION.md:219-225; registrations/H2/REGISTRATION.md:671-721.)
2. **H3's BLOCKED verdict is robust, and robust in a way the document itself claims.** Achieved fresh main-dex N = 2, deadline N = 5, against a P1 min-N of 262 (NPLExperiment/registrations/H3/REGISTRATION.md:161-177). I tested the obvious Direction-A attack — that a rate estimated on n = 3 events in 182 days is too thin to close a hypothesis on — and it fails: the exact Poisson 95 % interval on 3 events/182 d is [0.103, 1.466]/month, so even the upper bound yields at most **10.4** main-dex events by 2027-03-31 against a min-N of 262. The magnitude leg is worse than under-powered: at the governing generating-sample share 0.356 the true share sits below the sign test's null, so no n reaches 0.80 — the registration says exactly this (NPLExperiment/registrations/H3/REGISTRATION.md:174-177). H3 is a genuinely closed question on this venue.
3. **The H1 FAIL row itself.** The verdict table was registered before the reader existed (Amendment 3, commit 6399d63, NPLExperiment/report.md:157-158), the row is mechanical, secondaries move no row, the read is single and latched with 21 module hashes, and 3/3 mutations on the new surface were caught. I looked specifically for a bar quietly tightened between registration and read and found the opposite: every bar in Section 8 is unchanged from the pre-network commit (NPLExperiment/REGISTRATION.md:200-226 versus the verdict record at 547-581).
4. **Amendment 1 and the pre-epoch censoring.** Every rule change is argued toward the null and says so: "The mechanical hyperp rule moves conversion events' anchors LATER … and, if anything, biases the measured listing-age effect toward the null" (NPLExperiment/REGISTRATION.md:368-375). Epoch censoring removes instruments that cannot have a measurable funding leg. I expected a censoring rule that quietly removed unfavourable events and did not find one.
5. **The delisting-truncation rule.** Delistings are valued at the last served close and **retained**, with the solclear survivorship finding cited as the reason (NPLExperiment/REGISTRATION.md:189-194), and the truncated subgroup is reported (5/10 positive). This is the single most common place a closure gets manufactured and it is handled the hard way here.
6. **The H2 interim tripwire omission.** The prompt offered an optional 2026-09-30 E1-only check "to be omitted if it cannot be built without touching the reader, stating which" (NPLExperiment/registrations/H2/REGISTRATION.md:604-608). The reasoning for omitting it is correct on its own terms — the E1 statistic cannot be computed without reading a pair outcome — and the pair-count half that needs no reader is explicitly kept available. This is a named-variant-not-run that I checked hard and cannot fault.
7. **Amendment H2-4 §7, the look-2 GO correction.** A prose defect that would have fired FAIL *because the look-1 evidence was too strong* was found and corrected before any outcome existed, with the exact spend shown to be unchanged (NPLExperiment/registrations/H2/REGISTRATION.md:762-789). This is the opposite of my thesis and deserves saying so.
8. **Amendment H5-1 and H5-2 directions.** Both amendments were made with data in hand and both move against the assistant's convenience: H5-1 makes CLOSED strictly harder and cost the entry a same-day close (NPLExperiment/registrations/H5/REGISTRATION.md:417-422); H5-2 makes VIABLE strictly harder and, in the register's own words, "deleted this entry's only route to VIABLE" (NPLExperiment/HYPOTHESES.md:129, DECISIONS.md ADR-030:509-513). The delisted-exclusion rule is conjunctive on three fields with 57/57 and 0/94 agreement and zero conflicting cases. I went looking for an amendment that bought a convenient answer and found two that sold one.
9. **The alpha-split materiality test (Amendment H2-4 §1).** Six splits evaluated against a two-clause test written before it was applied; the two that gain power fail clause (b) by cutting the interim's firing probability 0.193 and 0.277 (NPLExperiment/registrations/H2/REGISTRATION.md:648-665). The registered split stands on a rule, not a preference.
10. **The E2 floor weakening (2× → 1×).** Labelled a weakening in its own heading, the interpolated power assumption is labelled a choice rather than a measurement, and **every** minimum-N is reported twice so a reader who rejects the interpolation can read 184/92 instead of 117/59 (NPLExperiment/registrations/H2/REGISTRATION.md:461-474, 675-684). This is the standard place a Direction-A audit finds a bar moved quietly; here the move is announced, quantified, and its cost carried at every look.
11. **The generating-sample quarantine.** Structural (AST string pin, import isolation, recorded event-ID set, refusals produced by test rather than asserted), and it is enforced against the assistant's own interest: the H1 main-dex subset 107/158 would give a Clopper–Pearson lower bound of **0.6107 at alpha 0.05** — clearing H3's 0.60 bar — and the register uses it only as a power assumption, never as an answer (NPLExperiment/registrations/H3/REGISTRATION.md:79-80; NPLExperiment/REGISTRATION.md:642-649). That is the correct call and I want it on the record that they made it.
12. **Reopen-trigger sweep within this repository.** I compared every registered reopen condition against every later-dated entry in the snapshot. **None has been met**: main-dex accrual stands at 0.5/month against a 40–50/month reopener; the conditioning rates stand at 0.177/0.129/0.081 against "several times higher, sustained"; H1's reopener is "nothing". Cross-repository candidates are listed in the ledger file.

## Live-repo access log

Purpose of access: git history/provenance only (`rev-parse`, `log`). No file in the live repository
was opened; no untracked data was read; no write of any kind.

BEFORE — `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain` (2026-09-04, exit 0):

```
```
(empty — clean tree)

AFTER — `git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain` (2026-09-04, exit 0):

```
```
(empty — clean tree; unchanged)

Provenance read: `git rev-parse HEAD` = `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c`, identical to the
anchored SHA; `git log 8f1fef8..HEAD` returns nothing, so **no commit exists after the anchor** as of
this read. The repository is nonetheless live — H5's map fires 2026-09-26 and H2's look 1 projects to
2026-11-26 — so findings 2, 3, 6 and 7 concern designs that may be amended before they fire.
