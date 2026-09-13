# Agent B — NPLExperiment, part p1-registrations (draft findings)

Repository: NPLExperiment, anchored SHA `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` (main, 2026-09-02).
Primary documents read in full: `REGISTRATION.md` (659 lines), `registrations/H2/REGISTRATION.md` (789),
`registrations/H3/REGISTRATION.md` (188), `registrations/H4/REGISTRATION.md` (234),
`registrations/H5/REGISTRATION.md` (647), `HYPOTHESES.md` (154), `README.md` (91), and the
H2/H5-relevant sections of `report.md`. Recomputation used
`/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python` (scipy 
`binom`, `betabinom`, `beta`); scripts under
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-NPL-p1/`.

---

### DRAFT-p1-registrations-1
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2's registered two-look exact binomial boundary (Amendment H2-3 Change 3, Amendment H2-4 table 3) and H1's P3 — the register's only PASS and the sole basis for H2
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The look-2 spend is computed **conditional on not having rejected at look 1**, over the independent increment Bin(n₂ − n₁, ½), so the total type-I error is at most alpha₁ + alpha₂ = 0.05 exactly, with no asymptotic approximation anywhere." — NPLExperiment/registrations/H2/REGISTRATION.md:528-531. And: "Three co-primaries, distribution-free, one-sided, at **alpha_adj = 1 − 0.95^(1/3) = 0.016952 (0.0170)** each." — NPLExperiment/REGISTRATION.md:200-201
- **Evidence:**
  - Every verdict statistic in this repository is an exact binomial or exact sign test over per-event or per-pair indicators. Exactness of those tails requires the indicators to be **independent Bernoulli trials**. The registration never states that assumption, never justifies it, and never tests it. `grep -rn "independen|cluster|overlapping|design effect" --include=*.md .` over the whole snapshot returns only prior-slot labels ("`(independent)`"), "independent underlying feed" (H5), and "the independent increment" (the quote above). There is no discussion of dependence anywhere in REGISTRATION.md, HYPOTHESES.md, registrations/H2..H5, report.md, DECISIONS.md or progress.md.
  - The design **guarantees** dependence by construction. (a) Control reuse: "**With replacement**: one old perp may serve as control for many events." — NPLExperiment/REGISTRATION.md:176, carried verbatim into H2 at registrations/H2/REGISTRATION.md:129-130. (b) Overlapping holding windows: all pairs are 30-day windows on one venue, and H2's fresh cohort entries span 2026-05-30 to 2026-08-28 (NPLExperiment/report.md:516).
  - Measured from the live untracked pairs ledgers (read-only, **UNANCHORED**, read 2026-09-12T12:47:22Z): `data/controls/pairs.jsonl` (H1) = 176 rows, **82 distinct controls**, top control `xyz:XYZ100` serves **15** pairs, top five serve **47 of 176**, max 17 pairs with mutually overlapping 30-day windows. `data/controls/h2_pairs.jsonl` (H2) = 63 rows (62 at the anchor + 1 forward birth since), **34 distinct controls**, max reuse 7, entries 2026-05-30 → 2026-09-02, and **28 pairs whose 30-day windows all overlap**.
  - The repository corrects meticulously for *multiplicity* — Sidak across three co-primaries (REGISTRATION.md:200-201), a familywise alpha_h across hypotheses (registrations/H2/REGISTRATION.md:182-189), a two-look alpha split (registrations/H2/REGISTRATION.md:500-501), Sidak-within for H4's three cells (registrations/H4/REGISTRATION.md:79-81) — and nowhere for *dependence*, which is the assumption the exact tails actually rest on.
- **Recomputation (if any):** Inputs: n₁ = 59, k₁ = 38, n₂ = 117, k₂ = 69 (registrations/H2/REGISTRATION.md:696, reproduced exactly from `reports/stage_a_h2/ktable_amended.json` `boundaries.at_look2_min_n`); P3 = 114 of 175 (NPLExperiment/REGISTRATION.md:562-564). Method: replace the i.i.d. null Bin(n, ½) with a beta-binomial null of the same mean and intra-cluster correlation ρ (ρ = 0 reproduces the registered figure exactly), `scipy.stats.betabinom.sf`. Results:
    - Look-1 rejection P(S₁ ≥ 38 | n₁ = 59): ρ=0 → **0.0182** (the registered spend); ρ=0.01 → **0.0486**; ρ=0.02 → **0.0791**; ρ=0.05 → 0.1517.
    - Look-2 component P(S ≥ 69 | n = 117): ρ=0 → 0.0320; ρ=0.01 → **0.1050**; ρ=0.02 → 0.1575.
    - P3 p-value at 114/175: ρ=0 → **3.767e-05** (reproduces the registered figure to four digits); ρ=0.005 → 1.87e-03; ρ=0.01 → 8.35e-03; ρ=**0.02 → 3.13e-02**, i.e. **FAIL** against alpha_adj = 0.016952.
    - Equivalent framing for P3 by effective n at the observed share 0.6514: PASS holds at n_eff ≥ 50 (p = 1.64e-02) and fails at n_eff = 40 (p = 1.92e-02).
  I do **not** claim to have measured ρ — the outcome values are sealed and reading them is barred. The claim is that the registered error control is asserted as exact while resting on an assumption that is unstated, violated by the design's own control-reuse and window-overlap, and to which the registered boundaries are extremely sensitive: an intra-cluster correlation of one to two percent already consumes or exceeds the whole familywise budget at look 1, and flips the register's only PASS.
- **What would resolve it:** Either (a) a registered dependence model — a cluster-robust or permutation/bootstrap null over control clusters and calendar blocks, with the boundary recomputed under it; or (b) a stated, defended independence assumption plus a measurement of the design effect from quantities already on disk (control reuse and entry-date overlap are computable without opening any outcome); or (c) an explicit epistemic-boundary sentence saying the exact tails are conditional on independence which the design does not provide.
- **Confidence:** HIGH — the construction guarantees dependence, the registration is silent, and the sensitivity is arithmetic I reproduced from the repository's own boundary numbers.
- **Invalidated by later commits?:** no — the only post-anchor commit (dff1663, 2026-09-10, Amendment H5-3) touches H5's fire-date projection only; H2's boundary and H1's spent read are unchanged.
- **Disclosed by authors?:** no — the words "independent", "cluster", "overlapping" and "design effect" appear nowhere in the repository in this sense; the registrations describe the tests as "distribution-free" and "exact … with no asymptotic approximation anywhere", which is true of the tail arithmetic and silent about the dependence that governs it.

---

### DRAFT-p1-registrations-2
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** Amendment H2-1's register cull — the fixed point k = 1, alpha_h = 0.05, and H2's DEGRADED (survivor) verdict
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Projected pairs, by-dex measured model (governing):** 88 by 2026-12-31, **141 by 2027-03-31** … **Powers at the deadline (n = 141 pairs, alpha_h = 0.05):** E1 **0.9743**, E2 **0.7604** — the weaker required co-primary lands in [0.50, 0.80): **DEGRADED**, per the Section 0 map." — NPLExperiment/registrations/H2/REGISTRATION.md:283-293
- **Evidence:**
  - The cull's BLOCKED clause is "either co-primary **under 50 percent power** … at the achievable count by 2027-03-31" (registrations/H2/REGISTRATION.md:36-38), and the cull is fixed forever at that firing: "k and alpha_h are fixed at the cull, recorded here by amendment, never revisited after any outcome exists" (registrations/H2/REGISTRATION.md:187-189).
  - The 141 figure counts pairs **assigned** by 2027-03-31, not pairs readable by then: Section 9's recipe is "projected N by 2026-12-31 and 2027-03-31 using the **measured** accrual and match rates from A.1" (registrations/H2/REGISTRATION.md:176-181), and `reports/stage_a_h2/ktable_cull.json` records `"deadline_2027-03-31": {"events": 173, "pairs_bydex": 141, "pairs_flat": 106}`.
  - The same registration makes a pair unreadable until 92 days after entry: "A fresh pair becomes readable when its candle window seals at entry + 92 days (ADR-019); a forward birth's pair is readable at listing + 94 days." — registrations/H2/REGISTRATION.md:725-726; ADR-019 at NPLExperiment/DECISIONS.md:224-233. The Stage B trigger is stated on matured pairs: "both co-primaries at or above **80 percent power at achieved eligible pair N** (not projected)" (registrations/H2/REGISTRATION.md:195-196), eligibility requiring Section 7 coverage on both legs (registrations/H2/REGISTRATION.md:143-145).
  - Two hours later the same stage recomputes the projection on **readable** pairs and gets a smaller number even after the match rate rose from 0.613 to 1.000: 135 readable by 2027-03-31 (registrations/H2/REGISTRATION.md:732-740; `reports/stage_a_h2/ktable_amended.json` `projection_by_month`). And the repository states the counterfactual under the rule that was actually in force at the cull: "at the pre-amendment 0.613 the deadline count would be 82 instead of 135" (registrations/H2/REGISTRATION.md:729-730; `ktable_amended.json` `pair_projection_models.withdrawal_sensitivity`, computed 2026-08-28T07:44:41Z).
  - Amendment H2-1 itself applies a maturity lag when it states the earliest read date — "reached near **2027-05/06** at the measured by-dex rates, plus 30-day maturity" (registrations/H2/REGISTRATION.md:299-300) — so the same amendment uses the projection both with and without a maturity lag, and uses the lag-free version for the verdict that decided survival. (The 30-day lag there is itself inconsistent with the 92-day seal of ADR-019.)
- **Recomputation (if any):** Inputs: exact one-sided sign test, p₀ = 0.5, alpha = pass-1 alpha_h = 1 − 0.95^(1/3) = 0.016952 (registrations/H2/REGISTRATION.md:263-266), E2 true share 0.60 (registrations/H2/REGISTRATION.md:162). Method: k* = min{k : P(Bin(n,½) ≥ k) ≤ alpha}, power = P(Bin(n, 0.60) ≥ k*). Results (my recomputation reproduces both figures the amendment states, which validates the method): n = 141 → **0.5771** (amendment states 0.5771); n = 106 → **0.4318** (amendment states 0.4318). New: n = 135 (readable at match rate 1.000) → **0.5373**; n = **82** (the repository's own readable count under the pre-amendment rule) → **0.3041**, i.e. **below the 0.50 BLOCKED floor**. The first n at which the figure reaches 0.50 is 116, and it first stays above 0.50 from n = 130.
  Consequence: had the cull applied the readability lag its own registration imposes, H2's governing co-primary would have fired **BLOCKED** at pass 1 under the rule then in force, the cull would have reached k = 0, and no hypothesis would have survived. (Post-amendment, at 135 readable pairs, H2 does clear the floor at 0.5373 — the defect is that the verdict was fired in the pre-amendment world on a count that world could not reach.)
- **What would resolve it:** Re-run `npl.register.cull.run_cull` with the deadline scenario's pair counts replaced by the readable counts of `ktable_amended.json`'s `projection_by_month` (135 under the fallback; 82 under the same-dex rule), and record the resulting k/alpha_h beside the registered pair. If the authors intend "achievable count" to mean assigned-not-readable, say so in the registration and reconcile it with Section 10's "achieved eligible pair N".
- **Confidence:** HIGH for the arithmetic and the internal inconsistency; MEDIUM for the interpretation that "achievable count by 2027-03-31" must mean readable-by-then — Section 9's projection recipe is literally accrual × match rate, though Section 0, Section 10 and Amendment H2-4 all point the other way.
- **Invalidated by later commits?:** no — no post-anchor commit touches the cull, the k/alpha fixed point, or the projection.
- **Disclosed by authors?:** no — the readability lag is disclosed (registrations/H2/REGISTRATION.md:725-726) and the 82-pair counterfactual is disclosed (registrations/H2/REGISTRATION.md:729-730), but nowhere is it stated that the cull's deciding count ignored the lag, and no power figure is reported at a readable count at the pass-1 alpha.

---

### DRAFT-p1-registrations-3
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H4's BLOCKED verdict (Amendment H4-2) and the register-wide k = 1 / alpha_h = 0.05 it produces
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "At the optimistic H1-registered 0.85 (reported beside, the honest range): 0.7106 / 0.3382 / 0.1209 — under the GO floor even at the assumption the register declined to adopt." — NPLExperiment/registrations/H4/REGISTRATION.md:221-223; compressed in the register index as "best-cell deadline power 0.014 governing (0.711 even at the declined optimistic 0.85)" — NPLExperiment/HYPOTHESES.md:106
- **Evidence:**
  - H4's own Section 0 sets BLOCKED at a **0.50** floor, not the GO floor: "**BLOCKED:** every cell **under 50 percent power** (inside the register cull's k/alpha fixed point). Nothing armed for H4." — registrations/H4/REGISTRATION.md:24-25. The best cell at the alternative assumption is **0.7106**, which is above 0.50. So H4's BLOCKED is not robust to the assumption; at the alternative it fires DEGRADED and survives the cull.
  - The contrast with H3 is explicit and shows the authors know the difference: H3's record states "Both required co-primaries sit under the 0.50 floor at every alpha considered; **the verdict is insensitive** to the k/alpha question and to the magnitude-leg assumption" (registrations/H3/REGISTRATION.md:171-173, where the optimistic figure is 0.1160, genuinely under 0.50). H4's record makes no such statement and instead uses "even at", which reads as the same robustness claim without being one.
  - The consequence is register-wide, not local to H4. The cull is a fixed point over survivors: "Pass 1 (k = 3, alpha_h = 0.016952): H2 required power 0.5771, H3 0.0000, H4 best cell 0.0140 — H3 and H4 fire BLOCKED. Pass 2 (k = 1, alpha_h = 0.05): H2 required power 0.7604 — fixed point. **k = 1. alpha_h = 0.05.**" (registrations/H2/REGISTRATION.md:261-266).
  - H2's entire amended design is spendable only at alpha_h = 0.05: "**The alpha split, fixed here and never revisited: alpha₁ = 0.02, alpha₂ = 0.03, summing to alpha_h = 0.05 per co-primary.**" (registrations/H2/REGISTRATION.md:500-501). At k = 2 the budget is 0.0253 and that split cannot exist.
- **Recomputation (if any):** Inputs: H4 cell sizes at the deadline 30 / 22 / 13 (registrations/H4/REGISTRATION.md:217-218), p₀ = 0.60 bar (registrations/H4/REGISTRATION.md:92-94), Sidak-within alpha_cell = 1 − (1 − alpha_h)^(1/3) (registrations/H4/REGISTRATION.md:79-81), assumption 0.85. Method: k* = min{k : P(Bin(n, 0.60) ≥ k) ≤ alpha_cell}, power = P(Bin(n, 0.85) ≥ k*). Results: at k = 3 (alpha_h = 0.016952, alpha_cell = 0.005683): 0.710576 / 0.338177 / 0.120905 — reproduces the amendment's 0.7106 / 0.3382 / 0.1209 exactly. Best cell 0.7106 > 0.50 ⇒ H4 not BLOCKED at pass 1. Iterating the registered fixed point with H4 retained: k = 2, alpha_h = 1 − 0.95^(1/2) = **0.025321**, alpha_cell = 0.008512, H4 best cell = **0.710576** (still > 0.50) ⇒ fixed point k = 2. At that budget H2's governing E2 at n = 141 falls from 0.7604 to **0.6427**, and E2's single-look minimum N at the registered 0.60 rises from 169 to **210** pairs.
- **What would resolve it:** One sentence in Amendment H4-2 and in HYPOTHESES.md:106 stating that the BLOCKED row is contingent on the 0.631 assumption, that at the reported-beside 0.85 the best cell clears the 0.50 floor, and what k/alpha_h would then have been — exactly the sentence H3-1:171-173 supplies for H3.
- **Confidence:** HIGH — the floor, the alternative figure and the fixed-point procedure are all registered, and the arithmetic reproduces the repository's own numbers.
- **Invalidated by later commits?:** no — nothing after the anchor touches H4 or the cull.
- **Disclosed by authors?:** partly — the 0.7106 figure is disclosed at registrations/H4/REGISTRATION.md:222 and HYPOTHESES.md:106, and the choice of the governing assumption is reasoned at registrations/H4/REGISTRATION.md:100-107. What is not disclosed anywhere is that 0.7106 sits above H4's own BLOCKED floor, that the BLOCKED label therefore turns on the assumption, and that the surviving hypothesis's entire alpha budget turns on it with it.

---

### DRAFT-p1-registrations-4
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2's E2 power assumption (0.625) — Amendment H2-3 Change 2 — and the recomputed Section-0 GO it produces
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the registered assumption for the 1× floor is set by **linear interpolation in the floor multiple** between multiple 0 (E1's sign share, 0.65) and multiple 2 (the registered 0.60), evaluated at multiple 1: **h2_e2_true_share = 0.625**." — NPLExperiment/registrations/H2/REGISTRATION.md:465-469. Framing: "recomputed power at the deadline 0.889 single-look / 0.863 two-look" — NPLExperiment/README.md:15-16
- **Evidence:**
  - The register states a principle, twice, in the two registrations that fired BLOCKED, and states it as the thing that stops outcome-fitting: "**The generating-sample figure (0.356) governs the cull**; adopting the optimistic figure after seeing the pessimistic one would be outcome-fitting, and the register's principle is that generating-sample-derived assumptions govern wherever they exist." (registrations/H3/REGISTRATION.md:87-91); "**The generating-sample figure governs the cull** (the register's principle: generating-sample-derived assumptions govern wherever they exist …)" (registrations/H4/REGISTRATION.md:103-107); ADR-017 (NPLExperiment/DECISIONS.md:202-211).
  - For the survivor the principle runs the other way. The unamended H2 registration labels 0.60 as generating-sample-derived: "Registered assumption: true share **0.60** — generating-sample-derived (one notch under E1's 0.651 …)" (registrations/H2/REGISTRATION.md:162-164). The amendment that replaces it re-characterises the same number: "E2's true share was registered at **0.60** for the 2× floor — itself a judgment discount from E1's 0.651, **not a measurement** …" (registrations/H2/REGISTRATION.md:462-465). The optimistic, admittedly non-measured 0.625 then governs every minimum-N, both look dates, and the recomputed Section 0 row, and the previously registered 0.60 is demoted to "reported beside".
  - The decision the assumption carries is stated by the authors themselves: "a reader who rejects the interpolation and holds E2 at 0.60 should read **184 / 92**, and the design then **does not reach 0.80 by the deadline**." (registrations/H2/REGISTRATION.md:682-684). And the Section 0 recomputation that returns GO is computed only at 0.625: `reports/stage_a_h2/ktable_amended.json` `section0_gate_recomputed.single_look_gate` = `{"governing_power": 0.888596, "verdict": "GO"}`, with `single_look_k_table_extension_at_deadline."H2/E2".power_reported = 0.731814` at 0.60.
  - README.md carries only the favourable figure. The 0.60 alternative and the "does not reach 0.80" consequence appear in HYPOTHESES.md:74, report.md:541-544 and the registration, and are absent from README.md:10-17, which is the document the status line points a reader to first.
  - Separately, the headline two-look figure is evaluated at a sample size the registered stopping rule prevents the trial from reaching. "**Look 2** fires at the **earlier** of the registered deadline (2027-03-31) and the date both co-primaries reach their **look-2 minimum N**" (registrations/H2/REGISTRATION.md:493-494), and the repository projects that date as 2027-03-01 at n₂ = 117 (registrations/H2/REGISTRATION.md:744-745). Two-look power at (59, 117) is **0.8237** (registrations/H2/REGISTRATION.md:696), not the 0.8629 at n₂ = 135 that README.md:16, HYPOTHESES.md:70 and report.md:565 quote as the design's power.
- **Recomputation (if any):** Inputs as above; method: exact single-look power k* = min{k : P(Bin(n,½) ≥ k) ≤ 0.05}, power = P(Bin(n, p) ≥ k*); two-look power by the registered Π(n₁, n₂, p) formula (registrations/H2/REGISTRATION.md:537-538). Results, all reproducing the repository's own figures to six digits: single-look at n = 135 — E1 0.966471, E2@0.625 **0.888596**, E2@0.600 **0.731814**; two-look at (68, 135) — E1 0.955244, E2@0.625 **0.862922**, E2@0.600 **0.692372**; two-look at (59, 117) — E1 0.932234, E2@0.625 **0.823731**, E2@0.600 **0.647648**. Single-look minimum N (stays ≥ 0.80): E1 76, E2@0.625 111, E2@0.600 169 — all as registered. So the register's "both above the registered 0.80 target" holds at 0.625 and fails at 0.600 on every basis, and at the terminal look size 117 the reported-beside figure is 0.6476.
- **What would resolve it:** Either apply ADR-017's principle symmetrically — let the previously registered 0.60 govern H2's minimum N as the generating-sample end, with 0.625 reported beside — or state in the amendment why the survivor is exempt from the rule applied to the two hypotheses the same cull blocked. Carrying the 0.60 row into README.md, and quoting the two-look power at the projected terminal n₂ = 117 rather than at 135, would remove the framing half.
- **Confidence:** HIGH on the asymmetry and the arithmetic; MEDIUM on materiality, since a linear interpolation over a floor of 18–36 bp against a mean paired differential of +6.43 points is probably a small distortion in truth, and the authors say plainly that it is a choice.
- **Invalidated by later commits?:** no — no post-anchor commit touches H2's assumptions.
- **Disclosed by authors?:** partly — that 0.625 is a choice and not a measurement is disclosed (registrations/H2/REGISTRATION.md:469-474) and both minimum-N rows are carried. What is **not** disclosed is the inconsistency with the register's own stated principle (ADR-017 / H3 §8 / H4 §8), the re-characterisation of 0.60's provenance between Section 8 and the amendment that replaced it, the absence of the 0.60 row from README.md, and that the quoted two-look power is at a sample size the stopping rule excludes.

---

### DRAFT-p1-registrations-5
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2's main-dex fallback control (Amendment H2-3 Change 1) and the power assumptions carried across it
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Registered power assumption: true share **0.65** — generating-sample-derived (P3 pair share 114/175 = 0.651)." — NPLExperiment/registrations/H2/REGISTRATION.md:156-157, left unchanged by Amendment H2-3, which states of the new pairs only that "**The tag never filters anything.** Both types enter every primary statistic." — NPLExperiment/registrations/H2/REGISTRATION.md:422-423
- **Evidence:**
  - The generating-sample figure that supplies both power assumptions was computed on **same-dex pairs only**: the H1 control rule is "the perp on the **same dex** listed at least 180 days earlier" (NPLExperiment/REGISTRATION.md:165-167), and 114/175 is the share among those pairs (NPLExperiment/REGISTRATION.md:562-564).
  - The events that could not be matched same-dex were a large, systematically different group and were **dropped from P3 entirely**: "**176 of 312 events (56.4 percent)** have at least one same-dex candidate aged 180+ days by census dates; the 136 unmatched (young HIP-3 dexs, mostly) stay in P1 and P2 and **drop from P3 only**, counted." — NPLExperiment/REGISTRATION.md:400-402. Nothing was ever measured about the age contrast for that 136.
  - H2's amended cohort is 39 percent composed of exactly that population: "the H2 pairs ledger at **62 rows (38 `same_dex`, 24 `cross_dex`)**" (registrations/H2/REGISTRATION.md:638-639), and the 24 are the events whose own dex had no eligible elder — "All 24 previously unpairable events (para 18, mkts 4, io 2)" (NPLExperiment/report.md:507). The live ledger confirms the composition (`data/controls/h2_pairs.jsonl`, read-only, UNANCHORED, read 2026-09-12T12:47:22Z: `pair_type` counts cross_dex 24, same_dex 1, absent 38 — the 38 pre-amendment rows being same_dex by the rule that produced them, registrations/H2/REGISTRATION.md:434-440).
  - The registration names the reason the two pair types may differ and then makes the check unable to bind: "a cross-dex pair matches funding but **not venue microstructure**, and the reader must be able to see whether the primary rests on it" — registrations/H2/REGISTRATION.md:427-428 — but the `same_dex` stratum is "descriptive, never verdict-bearing" (registrations/H2/REGISTRATION.md:424-426, 597-601), so a same-dex/cross-dex disagreement cannot stop a GO.
  - The generating sample also carries direct evidence that the HIP-3 population differs: "the HIP-3 stratum was the weakest (share positive 0.584, n = 154, against vanilla 0.670, n = 112, and hyperp_conversion 0.696, n = 46)" — registrations/H3/REGISTRATION.md:43-46 — and H3 exists as a hypothesis precisely because of that.
  - Timing: look 1 fires at n₁ = 59 (registrations/H2/REGISTRATION.md:688-689) from a backfill cohort of 62, so a look-1 GO — which authorises drafting Stage C (registrations/H2/REGISTRATION.md:580-582) — would rest roughly 37 percent on the pairing construction whose effect size has never been measured at all.
- **Recomputation (if any):** none required beyond the counts above (24/62 = 0.387; 136/312 = 0.436 of generating-sample events unmatchable same-dex).
- **What would resolve it:** State a separate registered power assumption for the cross-dex stratum, or state that none exists and that the registered 0.65/0.625 are assumed to transfer; or make the `same_dex` stratum verdict-relevant (for example, a registered requirement that the primary and the same-dex stratum agree in direction before a GO).
- **Confidence:** HIGH on the facts and the composition; MEDIUM on magnitude — the true cross-dex share is unmeasured in either direction.
- **Invalidated by later commits?:** no — the fallback rule and the assumptions are unchanged after the anchor; the ledger has grown by one forward `same_dex` pair.
- **Disclosed by authors?:** partly — the fallback is declared a relaxation (registrations/H2/REGISTRATION.md:441-443), the microstructure difference is named (427-428), and the stratum is reported. Nowhere is it said that the registered effect assumption was measured only on same-dex pairs, that the cross-dex group is precisely the group the generating sample excluded from P3, or what fraction of a look-1 GO would rest on it.

---

### DRAFT-p1-registrations-6
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2's E1 power assumption (0.65) imported from H1's P3 share
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**E1, the sign.** Exact one-sided sign test on the share of pairs with **positive net pair return** at 30 days, central costs; bar: the share **exceeds one half** at alpha_h. Registered power assumption: true share **0.65** — generating-sample-derived (P3 pair share 114/175 = 0.651)." — NPLExperiment/registrations/H2/REGISTRATION.md:154-157
- **Evidence:**
  - P3's success event, read from the code that produced 114/175: `successes = sum(1 for _, net, control in pairs if net > control)` where both terms are `net_short_30` — NPLExperiment/src/npl/verdict.py:136, with `net_short = price + funding − cost` per instrument class at NPLExperiment/src/npl/outcome.py:24-27 and the registered rule "a control's class comes from its own dex" (NPLExperiment/REGISTRATION.md:519-522). So P3's indicator is `G − c_young + c_elder > 0`, where G is the gross pair differential.
  - E1's success event: `pair_net = young_leg_net_short + elder_leg_net_long`, both legs charged (NPLExperiment/src/npl/register/pairs.py:11-13 and :56-64, `cost_term` subtracted once for the summed pair cost). So E1's indicator is `G − c_young − c_elder > 0`.
  - The two thresholds differ by exactly **2 × the elder leg's round-trip cost** — 18 bp where the elder is main-dex vanilla (9 bp central) and 36 bp where it is HIP-3 (18 bp central), per the registered centrals at NPLExperiment/REGISTRATION.md:148-151 and `src/npl/config.py:180-181`. E1's event is therefore strictly harder than P3's on the same differential distribution, so the true E1 share is weakly **below** 0.651 and the registered 0.65 is optimistic in a known direction.
  - The assumption is load-bearing beyond E1: E2's interpolation anchors at "multiple 0 (E1's sign share, 0.65)" (registrations/H2/REGISTRATION.md:467-468), so the same optimism propagates into E2's 0.625 and into every minimum N and look date.
- **Recomputation (if any):** Algebraic, from the two code definitions above. P3: `(−p_y + f_y − c_y) − (−p_e + f_e − c_e) > 0` ⟺ `G > c_y − c_e`. E1: `(−p_y + f_y − c_y) + (p_e − f_e − c_e) > 0` ⟺ `G > c_y + c_e`. Difference in threshold = 2·c_e ∈ {18 bp, 36 bp}. The magnitude of the share difference cannot be computed without the sealed distribution; the sign is certain. For scale, the registered mean paired price differential is +6.43 points (NPLExperiment/REGISTRATION.md:578-580), so the shift is plausibly small — but it is not zero and is nowhere netted out.
- **What would resolve it:** A stated adjustment or a sentence in registrations/H2 Section 8 recording that 0.65 is an upper bound for E1's true share because E1 charges the elder leg's round trip twice relative to P3's indicator.
- **Confidence:** HIGH on the direction (it is algebra over two code paths); LOW on magnitude.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the registration presents 114/175 as the assumption's provenance without noting that E1's event is a strictly stricter one.

---

### DRAFT-p1-registrations-7
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5's Section 6 outcome map and its projected fire date — the census that will decide VIABLE / INDETERMINATE / CLOSED
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the entry now turns on whether the median absolute basis, over a full 30-day census **across all four session tags**, sits under 18 bp everywhere (CLOSED), between 18 and 54 (INDETERMINATE), or over 54 in at least one tag (VIABLE)." — NPLExperiment/HYPOTHESES.md:132; and "Over 30 days **and all four session tags**, how far does the mark sit from the venue's own oracle? … The map fires on **2026-09-26**, when the 20th-best-covered instrument reaches 30 covered days **at one pass per day**" — NPLExperiment/docs/STAGES.md:40
- **Evidence:**
  - The registered map is stated per session tag: VIABLE requires "the **median absolute basis in at least one session tag exceeds 54 bp**" (registrations/H5/REGISTRATION.md:239-242) and CLOSED requires it "**under 18 bp in every session tag**" (registrations/H5/REGISTRATION.md:253-255).
  - The registration makes the tags load-bearing and says why: "**Deviation is characterized within each tag separately.** The tags are not cosmetic: a perp on a closed underlying has no reference market at all, and pooling it with regular hours is the fastest way to manufacture a basis that is really just a stale reference." — registrations/H5/REGISTRATION.md:226-229; ADR-028 at NPLExperiment/DECISIONS.md:444-448.
  - The only scheduled H5 collection is one pass a day inside the daily unit: "**Order.** The H5 block runs **last** in the daily pass" (registrations/H5/REGISTRATION.md:308-309); "The collector is armed and runs last in the 01:40Z daily pass" (NPLExperiment/report.md:685-686); `ops/systemd/npl-daily.timer` = `OnCalendar=*-*-* 01:40:00 UTC`; `src/npl/cli.py:190-200` calls `run_daily_pass` once per daily invocation.
  - 01:40 UTC is 21:40 America/New_York in EDT and 20:40 in EST — after `POSTMARKET_CLOSE = 20:00` in both. The registered tagger therefore returns `closed_weekday` or `weekend` for every scheduled pass, and can never return `regular` or `extended` (`src/npl/h5/calendar.py:41-46, 154-175`).
  - Consequence: the verdict will be fired on a census in which the `regular` tag has **zero** observations, and the only tags with data are the two in which the underlying equity market is shut — precisely the "stale reference" condition Section 5 warns about. Amendment H5-1 Change 1 was written to stop exactly this failure mode ("a **single cross-sectional snapshot** lands entirely in one session tag, so the clause would be satisfied by that one tag and fire CLOSED — a verdict from one instant, on one session, dressed as a statement about every session", registrations/H5/REGISTRATION.md:394-398) and does not reach it, because it defers on *coverage days*, not on tag breadth.
- **Recomputation (if any):** (a) Registered tagger applied to the 29 remaining scheduled passes (2026-08-29T01:40Z … 2026-09-26T01:40Z) by loading `src/npl/h5/calendar.py` in isolation: `closed_weekday` 21, `weekend` 9, **`regular` 0, `extended` 0**. Same for a 30-day winter sample (2027-01-05 onward): `closed_weekday` 22, `weekend` 8, regular 0, extended 0. (b) Direct confirmation from the live untracked store (read-only, **UNANCHORED**, read 2026-09-12T12:43:59Z): `data/h5/snapshots.jsonl`, 3,639 rows over **14 passes** — session tags `closed_weekday` 2,533, `weekend` 832, `extended` 274 (the single manual 2026-08-28T22:00:14Z pass), **`regular` 0**. Every scheduled pass landed at 01:53–02:06Z and tagged `closed_weekday` or `weekend`. Live-instrument median |basis| by tag over that window: extended 5.14 bp (n = 150), closed_weekday 3.84 bp (n = 1,268), weekend 3.63 bp (n = 436).
- **What would resolve it:** Either add registered passes inside the `regular` and `extended` windows (13:30–20:00Z and 08:00–13:30Z / 20:00–24:00Z) before the map fires, or amend Section 6 to state that the map fires on the tags the registered cadence can observe and that `regular` is a recorded absence — and correct HYPOTHESES.md:132 and docs/STAGES.md:40, which both assert all four tags.
- **Confidence:** HIGH — the schedule, the tagger and 14 passes of collected data all agree.
- **Invalidated by later commits?:** no — the one post-anchor commit (dff1663, 2026-09-10, Amendment H5-3) moves the projected fire date from 2026-09-26 to ~2026-10-05 on measured pass accrual of 0.77/day and explicitly moves no bar; it does not mention session tags, and the post-anchor passes it tabulates are the same 01:40Z passes, all `closed_weekday`/`weekend`.
- **Disclosed by authors?:** no — the verdict record does note "`regular`, `closed_weekday`, `weekend` | **no observations yet** — recorded as absent, not as zero" (registrations/H5/REGISTRATION.md:575), which frames the gap as temporary. Nothing anywhere states that the registered collection cadence cannot produce a `regular` observation at all.

---

### DRAFT-p1-registrations-8
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H5 Amendment H5-2's justification for the delisted exclusion, and the "honesty clause, demonstrated" framing built on it
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "And the delisted stratum is where **every** observation above the 54 bp bar lived: median 30.5 bp with 45.6 % over the bar, against 3.72 bp and **0.0 %** for live instruments in the same snapshot." — NPLExperiment/HYPOTHESES.md:129; and unqualified in the narrative: "**57 of the 151 resolved instruments are delisted, and they are where every large basis lives.**" — NPLExperiment/report.md:652-653; and in the amendment itself: "The excluded stratum is where **every** observation above the 54 bp bar lives: 45.6 percent of delisted instruments clear it, against **0.0 percent** of live ones." — NPLExperiment/registrations/H5/REGISTRATION.md:518-520
- **Evidence:**
  - The repository's own fired artifact contradicts it for the live stratum: `reports/h5/verdict.json` records, for the 188 live-instrument observations that the verdict was fired on, `inputs.by_session_tag.extended.share_over_viable = 0.015957446808510637` — i.e. **3 of 188 live observations above the 54 bp bar** — beside `share_over_floor = 0.09574`. The same pair of figures is carried in the register index two rows above the claim: "**9.57 %** over the 18 bp floor, **1.60 %** over the 54 bp bar" (NPLExperiment/HYPOTHESES.md:126), and in the registration's verdict table (registrations/H5/REGISTRATION.md:574).
  - The "0.0 %" figure comes from a single earlier snapshot (`h5-census-2026-08-28T21:44:11Z`, registrations/H5/REGISTRATION.md:462, 479-484) and had already been falsified by the two snapshots taken seven and sixteen minutes later, which are the ones the map fired on (`h5-census-…21:51:54Z`, `…22:00:14Z`, registrations/H5/REGISTRATION.md:571).
  - Confirmed over a longer window from the live untracked store (read-only, **UNANCHORED**, read 2026-09-12T12:43:59Z), live instruments only: share of |basis| over 54 bp = **2.67 %** in `extended` (n = 150), **2.13 %** in `closed_weekday` (n = 1,268), **1.15 %** in `weekend` (n = 436); max live |basis| 276.6 bp. The live stratum routinely produces observations above the bar.
  - The claim is not decorative: it is the stated evidential basis for the amendment's direction-of-change argument ("Under the unamended universe this entry had a route to VIABLE through dead markets. The amendment removes it", registrations/H5/REGISTRATION.md:520-521) and for the "honesty clause, demonstrated" row in the register index. The *median*-based VIABLE clause is unaffected — no live tag median is anywhere near 54 bp — but the "every observation" statement is false as written and is stated unqualified in report.md.
- **Recomputation (if any):** 1.60 % × 188 = 3.0 observations, from `reports/h5/verdict.json` `inputs.by_session_tag.extended` (`n` = 188, `share_over_viable` = 0.0159574). Live-stratum shares over 18/54 bp recomputed directly from `data/h5/snapshots.jsonl` filtering `listing_status == "live"` and `basis_bp` present.
- **What would resolve it:** Qualify the sentence to the snapshot it was measured on (as HYPOTHESES.md:129 half-does with "in the same snapshot" while its lead clause does not), and replace "every observation above the 54 bp bar" with the measured live share from the verdict artifact.
- **Confidence:** HIGH — the contradicting figure is in the repository's own fired artifact and in HYPOTHESES.md itself, three rows apart.
- **Invalidated by later commits?:** no — no post-anchor commit edits these sentences.
- **Disclosed by authors?:** partly — the 1.60 % figure is published at HYPOTHESES.md:126 and registrations/H5/REGISTRATION.md:574, so the contradicting number is in the open; the finding is that the summary claim built on the other number was not corrected against it, and is stated without qualification at report.md:652-653.

---

### DRAFT-p1-registrations-9
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** Amendment H2-4 §3, "The boundary table" — a registered table of exact alpha spend per look
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| at look-1 min N | 59 | 30 | 22 | 37 | 0.0173 + 0.0200 = 0.0373 | 0.7031 | 0.5529 | … | at the deadline | 135 | 68 | 43 | 79 | 0.0176 + 0.0227 = 0.0403 | 0.9552 | **0.8629** |" — NPLExperiment/registrations/H2/REGISTRATION.md:695-697, introduced by "Every arithmetic input below is either a registered constant or one of those counts. Full record: `reports/stage_a_h2/ktable_amended.json`." — NPLExperiment/registrations/H2/REGISTRATION.md:644-646
- **Evidence:**
  - The cited artifact gives different per-look components for two of the three rows. `reports/stage_a_h2/ktable_amended.json` `boundaries.at_look1_min_n` (n₁ = 30, n₂ = 59): `alpha_spent_look1 = 0.008062`, `alpha_spent_look2 = 0.029206`, total 0.037268 — against the registration's "0.0173 + 0.0200". `boundaries.deadline_2027-03-31` / `two_look_at_deadline` (n₁ = 68, n₂ = 135): `alpha_spent_look1 = 0.01923`, `alpha_spent_look2 = 0.021113`, total 0.040343 — against the registration's "0.0176 + 0.0227".
  - The middle row is correct: `boundaries.at_look2_min_n` gives 0.018172 + 0.024025 = 0.042197, and the registration states "0.0182 + 0.0240 = 0.0422".
  - The totals in all three rows are right to four decimals; only the split between the looks is wrong, in the two rows where it is wrong. Every other figure in the table (n₁, k₁, k₂, both powers) reproduces exactly.
- **Recomputation (if any):** Inputs: the registered construction at registrations/H2/REGISTRATION.md:520-526, alpha₁ = 0.02, alpha₂ = 0.03, p₀ = ½. Method: `k1 = min{k : P(Bin(n1,½) ≥ k) ≤ 0.02}`; `spend1 = P(Bin(n1,½) ≥ k1)`; `k2 = min{k : Σ_{s<k1} P(Bin(n1,½)=s)·P(Bin(n2−n1,½) ≥ k−s) ≤ 0.03}`; `spend2` the same sum at k2. Results: (n₁=30, n₂=59) → k₁ = 22, k₂ = 37, spend **0.008062 + 0.029206 = 0.037268**; (59, 117) → k₁ = 38, k₂ = 69, spend **0.018172 + 0.024025 = 0.042197**; (68, 135) → k₁ = 43, k₂ = 79, spend **0.019230 + 0.021113 = 0.040343**. My independent computation reproduces the artifact exactly and the registration's components in one row of three.
- **What would resolve it:** A correction note in the amendment log (the repository already has the mechanism — see the H5 timestamp correction at registrations/H5/REGISTRATION.md:632-647) restating the two rows' components against `ktable_amended.json`.
- **Confidence:** HIGH — three independent sources (my recomputation, the artifact, the registration) and two of them agree against the third.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the table is presented as read from the artifact, and "The script refuses loudly if any row ever exceeds it" (registrations/H2/REGISTRATION.md:700-701) implies the numbers came from the script. The conclusion ("Every total spend sits **inside** alpha_h = 0.05") is unaffected; the stated per-look spends are not what the registered construction produces.

---

### DRAFT-p1-registrations-10
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** The delisting-observability gate of Section 0 / A.1 Task 4, and the survivorship claim carried on it
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Delisting observability PASS 6/6 — the cohort is not survivorship-manufactured." — NPLExperiment/HYPOTHESES.md:53; source row: "Delisting observability: **PASS in full** (A.1 Task 4, 6 of 6 probed delisted perps serve candles and funding)." — NPLExperiment/REGISTRATION.md:394-395
- **Evidence:**
  - The gate is binary and consequential: a partial pass "demot[es] the retrospective cohort to descriptive with the forward cohort carrying the verdict alone" and a FAIL "is treated as the partial case's limit: the retrospective cohort is demoted entirely" (NPLExperiment/REGISTRATION.md:34-37, 45-47). The retrospective cohort is the 312-event generating sample that supplies **every** power assumption in the successor register (registrations/H2/REGISTRATION.md:16-20).
  - The probe that cleared it is n = 6 against a census in which **179 instruments were flagged delisted** (NPLExperiment/REGISTRATION.md:385-387). The document reports the n honestly everywhere it reports the verdict; what it does not report is what 6/6 can and cannot establish.
  - The claim the figure is made to carry — "the cohort is not survivorship-manufactured" — is a statement about the whole 312-event cohort and the 179 delisted instruments in the census, and is rhetorically strengthened by the cross-repository citation "solclear Finding 2 measured that mechanism at 60 points of death-rate gap" (NPLExperiment/REGISTRATION.md:192-194).
- **Recomputation (if any):** Exact one-sided Clopper–Pearson lower bound on the serve rate from 6 successes in 6 trials at 95 percent: `0.05^(1/6)` = **0.6070**. So the probe is consistent with any true serve rate at or above ~61 percent, i.e. with up to roughly 39 percent of delisted instruments failing to serve candles or funding — a regime in which the retrospective cohort **would** be survivorship-affected. At the Section 0 gate's own alpha_adj of 0.016952, the bound is `0.016952^(1/6)` = 0.5000.
- **What would resolve it:** Either widen the probe (the census names 179 delisted instruments; the marginal cost is a few hundred keyless requests inside a 20,000/day cap), or restate the claim as what the probe supports — "no delisted instrument among six probed failed to serve" — and carry the lower bound beside it.
- **Confidence:** HIGH on the arithmetic and the gap between n = 6 and the claim's scope; MEDIUM on materiality, since the mechanism is plausible and the other 173 delisted instruments were never sampled in either direction.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** partly — the n travels with the figure everywhere ("6 of 6 probed"), so the reader can see it; the finding is that no document anywhere states what a 6/6 probe bounds, while the conclusion drawn from it ("not survivorship-manufactured") is stated without qualification in the register index.

---

### DRAFT-p1-registrations-11
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** `reports/stage_a_h2/ktable_cull.json` — the shipped k-table the three Section 0 verdicts cite
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Sidak within the hypothesis:** the three cells share H4's alpha_h as alpha_cell = 1 − (1 − alpha_h)^(1/3) (`npl.register.conditioning.sidak_within`, pinned to reproduce the H1 family split at 0.05/3)." — NPLExperiment/registrations/H4/REGISTRATION.md:79-81; and the verdict citing the artifact: "Fired by `npl.register.cull.fire_hypothesis_section0` at the cull's pass-1 alpha (k = 3, alpha_h = 0.016952; alpha_cell = 0.00568 Sidak-within)" — NPLExperiment/registrations/H4/REGISTRATION.md:206-208
- **Evidence:**
  - Every H4 row in `reports/stage_a_h2/ktable_cull.json` carries `"alpha_effective": 0.016952` — the hypothesis-level alpha_h, not the Sidak-within alpha_cell of 0.005683 the registration requires for the cells.
  - The stored cell powers follow that alpha, not the registered one. At the deadline the artifact records `le_-20pct_ann` n = 22 `power_governing` 0.015981 / `power_reported` 0.57518 and `le_-40pct_ann` n = 13 `power_governing` 0.021627, while Amendment H4-2 states 0.0037 / 0.0025 and 0.3382 for the same cells (registrations/H4/REGISTRATION.md:219-223).
  - The best cell (n = 30) agrees between the two because k* happens to be the same at both alphas; the other two cells do not.
  - Direction of the error is toward more power for H4, so the BLOCKED verdict is unaffected; the artifact and the amendment nonetheless disagree, and the artifact is the one shipped as the record.
- **Recomputation (if any):** Inputs: n = 22 and n = 13, p₀ = 0.60, p_true = 0.631 and 0.85. Method: k* = min{k : P(Bin(n,0.60) ≥ k) ≤ alpha}, power = P(Bin(n, p_true) ≥ k*). At alpha_cell = 0.005683: n = 22 → k* = 20, power 0.003702 (0.338177 at 0.85); n = 13 → k* = 13, power 0.002514 (0.120905 at 0.85) — matching the **amendment**. At alpha = 0.016952: n = 22 → k* = 19, power **0.015981** (0.575180 at 0.85); n = 13 → k* = 12, power **0.021627** — matching the **artifact** exactly. So the artifact applied alpha_h where the registration requires alpha_cell.
- **What would resolve it:** Regenerate the k-table with `sidak_within` applied to H4's cells, or record in the artifact that the H4 rows are computed at alpha_h with the Sidak figures in the amendment.
- **Confidence:** HIGH — the reverse-engineering is exact for both alphas.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

---

### DRAFT-p1-registrations-12
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** H2's Section 4 simplifications — the "no liquidation modelling" bias disclosure, dropped between H1 and H2
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "- **Equal constant notional on both legs**, no compounding, no liquidation modelling, no rebalancing — named Stage-scope simplifications, **as in H1 Section 4**." — NPLExperiment/registrations/H2/REGISTRATION.md:99-101
- **Evidence:**
  - What H1 Section 4 actually says is more than "a named simplification": "**No liquidation modelling**: the short is assumed to survive to horizon regardless of path. Named Stage-scope simplification, and **it biases the measured net in the hypothesis's favour** on instruments that rallied hard before falling; the H8 decomposition (Section 8 secondaries) is where that shows up." — NPLExperiment/REGISTRATION.md:138-142. The bias-direction clause is not carried into H2's registration, and H2 registers no H8-style decomposition as the place it would show up (its secondaries list at registrations/H2/REGISTRATION.md:168-172 includes a funding/price decomposition but no path or drawdown statistic).
  - H2's own feasibility memo treats the squeeze as the design's tail: "Young listings are squeeze-prone — thin books, no borrow, reflexive flows" and "beyond it, the isolated wall caps the loss at 1.2N regardless of how far the squeeze runs" (NPLExperiment/docs/PAIR_FEASIBILITY.md:34-35, 46-47). A realised pair whose young leg liquidates does not earn the modelled `pair_net`, so the bias applies to H2 at least as strongly as to H1.
  - Neither H2's epistemic boundary (registrations/H2/REGISTRATION.md:206-213), nor HYPOTHESES.md's H2 row (lines 60-76), nor README.md's status block (lines 3-19) mentions it.
- **Recomputation (if any):** none.
- **What would resolve it:** Carry H1's bias-direction sentence into H2 Section 4 by amendment, or state in H2's epistemic boundary that the pair net is computed without liquidation and that the omission favours the hypothesis on squeeze paths.
- **Confidence:** MEDIUM — the limitation is disclosed in the parent registration and the memo, and H2 incorporates H1 Section 4 "as in"; the concrete gap is that the sentence a reader of H2 would need is not in H2, HYPOTHESES.md or README.md.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** yes, elsewhere — NPLExperiment/REGISTRATION.md:138-142 for H1 and NPLExperiment/docs/PAIR_FEASIBILITY.md:34-52 for the squeeze mechanics. This finding is the absence of that disclosure from H2's own registration and from the register index and README, not a discovery of the limitation.

---

### DRAFT-p1-registrations-13
- **Repository / SHA:** NPLExperiment / 8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c
- **Hypothesis or artifact:** Two stale figures carried in the narrative and the code
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "(`reports/stage_a_h2/amend_preconditions.json`, PASS at 07:51:10Z on the project clock)" — NPLExperiment/report.md:446; and "E2: the economic floor — net at or above 2x the pair's central cost." — NPLExperiment/src/npl/register/pairs.py:177
- **Evidence:**
  - The cited artifact records `"checked_at": "2026-08-28T06:51:10Z"` (`reports/stage_a_h2/amend_preconditions.json`), and the registration and progress log both say 06:51:10Z (registrations/H2/REGISTRATION.md:376-377; progress.md:831). report.md:446 is one hour late. The 07:51Z timestamps in progress.md belong to Tasks 4–6 of the same stage (progress.md:958, 995, 1017), which is the likely source of the slip.
  - `src/npl/register/pairs.py:177` still documents the 2× floor while the function body two lines later uses `cfg.h2_cost_floor_multiple` (:187), which Amendment H2-3 Change 2 set to 1.0 (`src/npl/config.py:219`). The behaviour is correct; the docstring on the E2 primary is not.
- **Recomputation (if any):** none beyond reading the artifact and the config constant.
- **What would resolve it:** Correct report.md:446 against the artifact, and update the `e2_floor` docstring to the registered multiple.
- **Confidence:** HIGH.
- **Invalidated by later commits?:** no — both are unchanged at the anchor and after it.
- **Disclosed by authors?:** no. The repository does correct slips of exactly this kind elsewhere (registrations/H5/REGISTRATION.md:632-647, and `reports/h5/h2_verification.json` `checked_at_correction`), so the mechanism exists and was simply not applied here.

---

## What I checked and found sound

- **Every headline power, boundary and verdict figure reproduces exactly.** I independently recomputed, from the registered definitions: H1's P1 Clopper–Pearson lower bounds (197/312 → 0.5707; 198 → 0.5740; 194 → 0.5609; 208 → 0.6069, all at alpha_adj = 0.016952), P2 (111/312 → p = 1.000; 159/312 → 0.3886), P3 (114/175 → 3.767e-05; 111/175 → 2.36e-04) — NPLExperiment/REGISTRATION.md:554-572. Also H2-1's cull powers (E1 0.974266, E2 0.760372 at n = 141; 0.5771 at the pass-1 alpha; 0.4318 at the flat 106; achieved 0.533866 / 0.289678; interim 0.853049 / 0.528888), H3-1's (MAG 0.005718 / 0.116029 at n = 5; min-N 262 and 361), H4-2's per-cell figures, and all of H2-4's minimum-N (76 / 111 / 169 / 42 / 84 / 59 / 117 / 92 / 184), boundary k's (22/37, 38/69, 43/79), powers and futility numbers (E1 f₁ = 31 at n₂ = 84; E2 f₁ = 27 at n₂ = 117). Nothing in this arithmetic is invented or rounded in a favourable direction.
- **Amendment H2-4 §7's correction is mathematically right, not a rescue.** The corrected rule ("a co-primary passes at look 2 when `S₁ ≥ k₁` **or** `S₂ ≥ k₂`", registrations/H2/REGISTRATION.md:773-777) is exactly the union {S₁ ≥ k₁} ∪ {S₁ < k₁, S₂ ≥ k₂}, whose null probability is the sum of the two registered spends. The claim "This does not weaken the error control" (line 779) is correct under the independence assumption the design already makes, and the correction removes a genuine perversity rather than enlarging a rejection region opportunistically.
- **The alpha-split materiality test was written before it was applied and applied honestly.** The two clauses (registrations/H2/REGISTRATION.md:505-514) are stated before the six candidates are evaluated, and I reproduced every row of the evaluation table (registrations/H2/REGISTRATION.md:654-661) exactly from `ktable_amended.json`, including the two splits that gain power and are refused by clause (b). k₁ is correctly recomputed per candidate alpha₁ (43 at 0.02/0.025/0.03, 44 at 0.015, 45 at 0.01, 46 at 0.005) — I checked specifically for a frozen k₁ and did not find one (P(Bin(68,½) ≥ 42) = 0.0341 > 0.03, so 43 is right at all three).
- **The E2 floor is not the weak test its own description suggests.** Because `pair_net` already subtracts the central cost, E2 at the 1× multiple is `G ≥ 2 × central` — i.e. the pair must clear **twice** its central round trip in gross terms, which is exactly the registered high cost band (bands are half and double, registrations/H2/REGISTRATION.md:118; ADR-020 at DECISIONS.md:239-244). The pre-amendment 2× floor was `G ≥ 3 × central`. The amendment's self-description ("The bar still requires each pair to clear its own round-trip execution costs — 18, 27, or 36 basis points by pair class", registrations/H2/REGISTRATION.md:452-455) understates what the amended bar requires. I checked this specifically expecting to find that the weakening deleted the design's robustness to its own cost band; it does not.
- **The Section 0 map, the cull procedure and the quarantine are structurally serious.** The cull reads counts, rates and timestamps only; H3 and H4 fired BLOCKED against registered expectations that were written down in advance (registrations/H3/REGISTRATION.md:23-30; registrations/H4/REGISTRATION.md:27-31), and H3's BLOCKED is genuinely insensitive to its assumption (0.1160 at the optimistic end, well under the 0.50 floor — I verified). The generating-sample quarantine, the AST pins, the per-look latches and the mutation exercises are pinned by tests and the defect records (the 7.2M fake-coin trail files, Amendment H2-2; the backfill nearly writing to H1's ledger, report.md:524-528) are disclosed rather than smoothed.
- **H5-1 Change 1 and H5-2 Change 1 both move against the assistant's convenience,** and say so with the data in hand (registrations/H5/REGISTRATION.md:417-422 and 517-523). H5-2 deleted the entry's only route to VIABLE. I looked hard for a rescue amendment in H5 and did not find one; the H5 amendments make the terminal states harder, not easier.
- **H5's arithmetic and honesty clause.** The 54 bp bar is derived, not chosen (3 × the 18 bp HIP-3 round trip, ADR-029 / `h5_viable_basis_multiple = 3.0` at config.py:251); the `premium` series was correctly identified as an impact-price deviation by exact arithmetic against a served context (registrations/H5/REGISTRATION.md:440-444) and correctly demoted to a CLOSED-only secondary; the retrospective shortfall (39 observations, 2 instruments) is refused rather than read (registrations/H5/REGISTRATION.md:603-616). The Section 4 honesty clause is unusually candid about what a venue-internal reference can mean.
- **The H5 timestamp correction and the `para:IGV` refusal** (registrations/H5/REGISTRATION.md:632-647; 545-553) are exactly the behaviours a sceptic looks for and fails to find: an admitted estimate corrected against the commit clock, and a universe left un-extended after the census found an unmapped ticker.
- **No evidence of a bar moved after an outcome existed.** I checked every amendment's "what data existed" statement against `git log` timestamps (local clock is −07:00): the cull artifact `ktable_cull.json` `computed_at` 05:41:32Z vs the A.2 commit 2b44c59 at 05:45:38Z; `amend_preconditions.json` 06:51:10Z vs the H2-3 commit f31f7a3 at 07:01:06Z; `ktable_amended.json` `computed_at` 07:44:41Z vs the H2-4 commit 546b2e3 at 07:46:42Z; H5's census 21:44–22:00Z vs its commits 21:59–22:10Z. Every amendment precedes the artifact it governs or follows it by minutes with the stated inputs, and `ktable_amended.json` carries `"outcome_values_read": 0`. The weakening in H2-3 is real, is labelled a weakening in its own heading, and did precede any pair outcome.
- **The H2 pairs ledger has grown as registered.** The live ledger now has 63 rows (62 at the anchor plus one forward birth tagged `same_dex`, entry 2026-09-02), consistent with Amendment H2-3's tagging rule and with the pre-amendment rows carrying no `pair_type` (registrations/H2/REGISTRATION.md:434-440).

## Live-repo access log

`git -C /home/kiros-li/Documents/GitHub/NPLExperiment status --porcelain`

- **Before first access** (2026-09-12, before any live read): *(empty output — clean tree, exit 0)*
- **After last access** (2026-09-12, after `git log`, `git show dff1663`, and read-only reads of `data/h5/snapshots.jsonl`, `data/controls/pairs.jsonl`, `data/controls/h2_pairs.jsonl`, `data/h5/` and `data/` listings): *(empty output — clean tree, exit 0)*

Both outputs are empty. Nothing was modified; no pre-existing dirt was present in this repository.

Live-repo operations performed, all read-only: `git status --porcelain`, `git log --format=... -40`, `git show <sha> --stat`, `git show <sha> -- registrations/H5/REGISTRATION.md`, `ls -la data/ data/h5/`, `wc -l`, `head -c` and a read-only Python pass over three `.jsonl` files. No file under the audited repository was opened for writing, and no repository script was executed in place. Untracked data read this way is **UNANCHORED**; read times are stated with each figure (2026-09-12T12:43:59Z and 2026-09-12T12:47:22Z).
