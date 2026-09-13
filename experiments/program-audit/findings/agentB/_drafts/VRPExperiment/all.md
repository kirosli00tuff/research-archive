# Agent B draft findings — VRPExperiment (part "all")

**Repository:** VRPExperiment · **Anchored SHA:** `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30)
**Read from:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/VRPExperiment/` (tracked files),
plus the live repository's git history (read-only) and its untracked `data/raw/task6/*.json`
(**UNANCHORED**, read 2026-09-05T03:55:12Z).

**Reproduction note that governs every DERIVED finding below.** I reimplemented the registered
estimators (REGISTRATION.md §2.3, §2.4, §2.6, §6) independently in
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-vrp-all/rebuild.py` and ran them against
the untracked raw series. Every primary figure reproduces **exactly**: BTC mean 0.086607, HAC SE
0.014709, t 5.8879, p 2.2966e-09, CI lower 142.7401 bps, positive share 0.738619; ETH mean 0.052045,
SE 0.021528, t 2.4175, p 0.00785854, CI lower 38.0124 bps, positive share 0.645524. All six
rebalance distributions (bands 0.05 / 0.10 / 0.20, both assets) also reproduce exactly. The
repository's arithmetic is not in question anywhere in this report; what is in question is what it
was made to mean.

---

### DRAFT-all-1
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** H1 / `docs/ARTIFACT.md` — the deliverable's deciding conclusion on the MET (Micro Ether) route
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S1
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The ether premium's point estimate is **119.05 bps**. The **central, commission-only, lower-bound cost is 122.14 bps**. **The premium does not cover the commission.**" — VRPExperiment/docs/ARTIFACT.md:212-214. Restated at VRPExperiment/docs/ARTIFACT.md:38-39 ("**The commission is larger than the premium**"), VRPExperiment/README.md:23-24, VRPExperiment/HYPOTHESES.md:21, VRPExperiment/progress.md:790. Reinforced at VRPExperiment/docs/ARTIFACT.md:216-217: "Because every cost input is a lower bound, no further measurement can reverse this — additional cost data can only widen the gap."
- **Evidence:**
  - The 122.140 bps is built from two components that assume **mutually inconsistent position sizes**. The option leg is priced as **one** straddle: "A short ATM **straddle** is two option contracts, so a round trip is four contract fills … **MET** | 4 × $0.20 = **$0.80** | **32.571 bps**" (VRPExperiment/docs/COSTS.md:83-88). The hedge leg charges **one whole futures contract** per resize: "Each delta-hedge rebalance trades the underlying micro future once … **MET future** | $0.20 | **8.143 bps**" (VRPExperiment/docs/COSTS.md:91-95).
  - The registered rule that generates the count is "**Delta-hedge the short ATM straddle on the reachable futures contract, resized whenever the position delta moves more than ±0.10 from flat, evaluated once per calendar day**" (VRPExperiment/REGISTRATION.md:289-291). One MET option is written on **one** Micro Ether future (VRPExperiment/reports/task3/venue_table.md:61), so on a one-straddle position a ±0.10 resize is a **0.10-contract** order. The code confirms the delta is measured in units of one future: `return 2.0 * _normal_cdf(d1) - 1.0` (VRPExperiment/src/vrp/sealed_read.py:336), and the counter fires on `if drift > band` with no size or granularity term at all (VRPExperiment/src/vrp/sealed_read.py:397-399).
  - **The registration required the granularity to be recorded and it was not.** §3.2: "Contract size · **minimum order increment** · notional at current spot · initial margin …" (VRPExperiment/REGISTRATION.md:208). The venue table records a **price** increment instead — "| minimum price increment | … | **$0.50 per ether = $0.05 per contract** |" (VRPExperiment/reports/task3/venue_table.md:62). `grep -rn "minimum order increment"` over the whole snapshot returns exactly two hits: the registration line and the prompt transcript (VRPExperiment/progress.md:69). No document anywhere discusses integer-contract hedging.
  - The hedge leg is **73.3%** of the deciding total: 89.569 of 122.140 bps (VRPExperiment/docs/ARTIFACT.md:168,170; VRPExperiment/progress.md:780,782).
  - The deciding comparison turns on **one** rebalance. At k = 11, cost = 122.140 bps > 119.052; at k = 10, cost = **113.997 bps < 119.052**. The stated conclusion flips on a single modelled hedge.
  - The repository's own stored output shows the ±0.10 rule is not, in practice, a ±0.10 hedge: `"max_abs_drift_median": 0.4067` (BTC) and `0.4167` (ETH) at band 0.1 (VRPExperiment/reports/task6/real_attempt2_result.json:39,164) — the median path's peak mis-hedge is ~4.1× the stated band; my reproduction gives p90 0.688/0.700 and max 1.870/1.442. This field appears in no document.
- **Recomputation (if any):**
  - Inputs: MET commission USD 0.20/contract (VRPExperiment/docs/COSTS.md:41); MET notional 0.10 × ETH spot 2456.205 = USD 245.6205 (VRPExperiment/reports/task3/venue_table.md:12,64); rebalance counts from VRPExperiment/reports/task6/real_attempt2_result.json:159-178; ETH premium 119.0521 bps (VRPExperiment/reports/task6/real_attempt2_result.json:141); raw series `data/raw/task6/{dvol,underlying}_ETH_daily.json` (UNANCHORED, read 2026-09-05T03:55:12Z).
  - Method: recompute commission-only round-trip cost under two **self-consistent** granularity models, using the repository's own delta function and daily evaluation. Script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-vrp-all/gran.py`.
    - **ALT A — one straddle, integer futures hedge.** Hold `H = round(straddle_delta)` whole futures, re-evaluated daily over the tenor; count the days `H` changes and the contracts traded. Over the same n = 1,955 paths: hedge trades **median 2, p90 5**; contracts traded median 2, p90 5. Cost = (4 + 2) × 0.20 / 245.6205 = **48.856 bps central**, (4 + 5) × 0.20 / 245.6205 = **73.284 bps pessimistic**.
    - **ALT B — ten straddles**, the smallest position at which a 0.10-delta resize is ≥ 1 contract. Cost = (4 × 10 × 0.20 + 11 × 0.20) / (10 × 245.6205) = **41.527 bps central**, **45.599 bps pessimistic**.
  - Result: **119.052 bps > 73.284 bps** and **> 48.856** and **> 41.527**. Under every self-consistent size the ETH premium point estimate covers the MET commission comfortably. The repository's 122.140 bps is obtainable only by charging a whole contract's commission for a tenth of a contract's hedge, eleven times.
  - The same model applied to MBT gives 6.528 bps central / 9.792 pessimistic (ALT A) against the repository's 16.320 / 21.760.
  - **What survives.** The registered HARVESTABLE test still fails on MET under every variant: 2 × 73.284 = 146.568 > CI lower 38.012; 2 × 45.599 = 91.198 > 38.012. So the **VENUE_BLOCKED branch is unaffected** and MET remains cost-exceeded on the registered 2.0× margin. What does not survive is the headline sentence, and the sentence at VRPExperiment/docs/ARTIFACT.md:216-217 that no further measurement can reverse it: the rebalance count is a **rule output**, not a lower bound, and every correction to it points down.
- **What would resolve it:** State the position size the cost model prices, and price the hedge at the venue's own minimum order increment on that size — either by charging a fractional-contract hedge (impossible, and then the rule is unexecutable and must be re-registered), or by counting integer hedge changes on a one-straddle position, or by scaling the option leg to the position size at which ±0.10 is executable. Any of the three, reported alongside the ±0.10 figure, would settle it. Recording the minimum order increment §3.2 already required would have surfaced it at TASK 3.
- **Confidence:** HIGH — the inconsistency is visible in the repository's own two cost tables (one straddle in the option leg, one whole future per 0.10-delta resize in the hedge leg), and the reversal is reproduced exactly from the repository's own delta function and raw series.
- **Invalidated by later commits?:** no — d37cf6d is the final commit; the repository is CLOSED (VRPExperiment/README.md:6) and `docs/HANDOVER.md:69-72` forbids re-running the read.
- **Disclosed by authors?:** no — the registration lists three limitations of the §2.6 conversion (VRPExperiment/REGISTRATION.md:168-173) and three unmeasured error sources behind the 2.0× margin (VRPExperiment/REGISTRATION.md:320-336), none of which is contract granularity or position size; no document in the repository mentions integer contracts, order increments or position size in the cost model.

---

### DRAFT-all-2
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** H1 / the MET cost figure and the registered ±0.05/±0.20 rebalance sweep
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "And the failure does not depend on the margin at all: **the ETH premium's point estimate, 119.052 bps, is below the central commission-only cost of 122.140 bps.** The premium does not cover the commission." — VRPExperiment/HYPOTHESES.md:21
- **Evidence:**
  - The registration makes the band sweep mandatory reporting, not optional: "a rebalancing band is a **trade-off between bounded capital and bounded trading cost** and is therefore **swept and reported, never chosen**: the count is additionally reported at **±0.05 and ±0.20** as a sensitivity" (VRPExperiment/REGISTRATION.md:294-297).
  - The sweep is reported **only as counts** — "at ±0.05 both medians are 17 (p90 21–22); at ±0.20 both are 5 (p90 9)" (VRPExperiment/progress.md:753-754); "rebalances at ±0.05 / ±0.20 (swept, not chosen) | median 17 / median 5 | 1,955 each" (VRPExperiment/README.md:62). It is **never propagated into a cost figure**. `docs/COSTS.md`, `docs/ARTIFACT.md`, `HYPOTHESES.md` and `progress.md` each carry exactly one MET cost pair, the ±0.10 one.
  - Stored counts, n = 1,955 paths per band per asset: band 0.05 median 17 / p90 22 (ETH); band 0.10 median 11 / p90 16; band 0.20 median **5** / p90 **9** (VRPExperiment/reports/task6/real_attempt2_result.json:148-178). Reproduced exactly.
- **Recomputation (if any):**
  - Inputs as DRAFT-all-1. Script `/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-vrp-all/recompute.py`.
  - MET commission-only cost = (4 + k) × 0.20 / 245.6205 × 10⁴ bps.
    - band ±0.05: central (k=17) **170.995 bps**, pessimistic (k=22) 211.709 → premium 119.052 does **not** cover it.
    - band ±0.10: central (k=11) **122.140 bps**, pessimistic (k=16) 162.853 → premium does **not** cover it (the reported case).
    - band ±0.20: central (k=5) **73.284 bps**, pessimistic (k=9) 105.854 → premium 119.052 **covers it by 1.62×**.
  - So the repository's deciding sentence holds at two of the three registered bands and **reverses at the third**, and the third is one the registration explicitly ordered to be swept and reported. The "FAILS BY 8.57×" headline (VRPExperiment/HYPOTHESES.md:21) becomes 5.57× at ±0.20 (2 × 105.854 / 38.012).
  - The HARVESTABLE verdict is unchanged at every band (2 × pessimistic exceeds the CI lower bound of 38.012 bps in all three cases), so the **branch is safe**; the claim of a margin-free failure is not.
- **What would resolve it:** Publish the MET and MBT cost pair at all three registered bands, as §4.3 requires, and state which of the repository's conclusions are band-invariant.
- **Confidence:** HIGH — every input is the repository's own stored figure and the arithmetic is one division.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** no — the counts at ±0.05/±0.20 are disclosed (VRPExperiment/README.md:62, progress.md:753-754) but no document states or implies that the deciding cost comparison reverses at ±0.20; VRPExperiment/HYPOTHESES.md:21 asserts the opposite ("does not depend on the margin at all").

---

### DRAFT-all-3
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the one open route — CME MBT options via IBKR Canada — and its "3.28×" headroom
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**MBT (BTC): commission-only cost 16.320 bps central / 21.760 bps pessimistic, against a BTC premium CI lower bound of 142.740 bps — passes the 2.0× margin by 3.28× on commission alone.**" — VRPExperiment/HYPOTHESES.md:21. Also "it clears the registered 2× hurdle by **3.28×**, and would still clear it at the maximum possible **29** rebalances" (VRPExperiment/docs/ARTIFACT.md:222-224).
- **Evidence:**
  - The 3.28× uses the **full-sample** one-sided 95% lower bound, 142.7401 bps over n = 1,955 (VRPExperiment/reports/task6/real_attempt2_result.json:13).
  - The repository's own stability table shows BTC decaying monotonically to 112.719 bps in the final quarter, n = 491, p = 0.0182 (VRPExperiment/reports/task6/real_attempt2_result.json:104-114; VRPExperiment/docs/ARTIFACT.md:94). No quarterly confidence bound is stored or published — `stability()` records mean, t, p and positive share but **not** `ci_lower_bps` (VRPExperiment/tools/task6_sealed_run.py:290-295).
  - The repository applies the instability standard asymmetrically. For ETH it carries instability into the reopening rule — "Reopening on the ETH side additionally requires the quarterly instability above to resolve" (VRPExperiment/HYPOTHESES.md:26) and "**Do not rely on the ETH premium**" (VRPExperiment/docs/HANDOVER.md:80). For BTC it warns "A reader planning around this should assume the decay continues rather than that the average persists" (VRPExperiment/docs/ARTIFACT.md:97-98) and then prices the open route on the average anyway.
- **Recomputation (if any):**
  - Inputs: raw series (UNANCHORED, read 2026-09-05T03:55:12Z); MBT commission USD 0.85 (VRPExperiment/docs/COSTS.md:42); MBT notional 0.10 × 78,124.575 = 7,812.4575 (VRPExperiment/reports/task3/venue_table.md:11,64); p90 rebalance count 16 (VRPExperiment/reports/task6/real_attempt2_result.json:44). Script `.../work/agentB-vrp-all/rebuild.py`.
  - MBT pessimistic commission-only cost = (4+16) × 0.85 / 7,812.4575 = **21.760 bps**; the registered bar is 2 × 21.760 = **43.520 bps**.
  - BTC one-sided 95% CI lower bound, same estimator (HAC bw 30, t critical at df = n−1), computed on the repository's own quarterly split:
    | quarter | n | mean bps | t | CI lower bps | headroom vs 43.520 |
    |---|---|---|---|---|---|
    | Q1 2021-03-24→2022-07-24 | 488 | 284.530 | 3.498 | 150.493 | 3.46× |
    | Q2 →2023-11-24 | 488 | 250.587 | 3.845 | 143.191 | 3.29× |
    | Q3 →2025-03-26 | 488 | 145.132 | 2.619 | 53.796 | **1.24×** |
    | Q4 →2026-07-30 | 491 | 112.719 | 2.098 | **24.172** | **0.56× — FAILS** |
  - On the registered minimum depth of 730 daily observations (VRPExperiment/REGISTRATION.md:145-146), i.e. 2024-07-31→2026-07-30: BTC mean 127.434 bps, t 2.966, p 0.00156, **CI lower 56.669 bps → headroom 1.30×**. On the most recent 365 observations: mean 61.706, t 0.973, p 0.166, CI lower **−42.861 → fails**.
  - So "passes by 3.28×" is a property of the 2021–2023 half of the sample. On the sample's own final quarter the open route does not clear its own registered bar.
  - Separately, VRPExperiment/HYPOTHESES.md:62 compresses this into "passes the margin by 3.28× on commission alone, **at any rebalance count up to the daily maximum of 29**". At 29 rebalances the cost is (4+29) × 0.85 / 7,812.4575 = 35.904 bps, 2× = 71.808, and the headroom against 142.740 is **1.99×**, not 3.28×. `docs/ARTIFACT.md:222-224` states the two clauses correctly; `HYPOTHESES.md:62` merges them into a figure that holds at neither end.
- **What would resolve it:** Publish the quarterly and trailing-two-year confidence bounds for BTC (the estimator already computes them; only the reporting dict omits them) and state the MBT headroom against each, so the operator sent to settle the route on two figures knows the premium side is decaying through the bar.
- **Confidence:** HIGH — the quarterly CI bounds are computed with the repository's own estimator on the repository's own series and the full-sample figures reproduce exactly.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** partly — the monotonic 60.4% decay and the four quarterly means are disclosed at VRPExperiment/HYPOTHESES.md:23, docs/ARTIFACT.md:96-98 and docs/HANDOVER.md:82-83, and I say so plainly. What is disclosed nowhere is any confidence bound below the full-sample one, or the fact that the open route's registered margin is not met on the sample's last quarter or on the registered 730-observation depth.

---

### DRAFT-all-4
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** H1's premium conjunct for ETH; the precondition of the fired VENUE_BLOCKED branch
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**SIGNAL_ABSENT does not fire.** Both assets reject H₀: mean(VRP) ≤ 0 at the registered one-sided α = 0.05 with the registered HAC bandwidth 30 — **BTC p = 2.297 × 10⁻⁹ (n = 1,955), ETH p = 7.859 × 10⁻³ (n = 1,955)**" — VRPExperiment/HYPOTHESES.md:37-39. The branch that fires requires "The premium is **positive and material**" (VRPExperiment/REGISTRATION.md:30, HYPOTHESES.md:34-36).
- **Evidence:**
  - The registration fixed the primary depth at two years: "**Registered minimum depth:** **730 daily observations per asset** (two years) for the primary analysis" (VRPExperiment/REGISTRATION.md:145-146). The design was powered against that depth: "At the registered depth of **730 daily observations** per asset … the effective independent sample is approximately `730/30 ≈ 24`" (VRPExperiment/REGISTRATION.md:426-428).
  - Deribit served 1,985 days and the analysis used all of them (n = 1,955 after the forward-window drop) — permitted, because 730 is a floor and not a window. But no document reports what the endpoint does on the window the registration named.
  - The repository's own quarterly table already shows ETH significant in only one of four quarters and negative in another (VRPExperiment/docs/ARTIFACT.md:91-94), and states "**The full-sample ether result rests heavily on the 2022–2023 window**" (VRPExperiment/docs/ARTIFACT.md:101-102).
- **Recomputation (if any):**
  - Inputs: raw series (UNANCHORED, read 2026-09-05T03:55:12Z); same estimator, HAC bandwidth 30, one-sided α = 0.05. Script `.../work/agentB-vrp-all/rebuild.py`.
  - | asset | window | n | mean bps | t | one-sided p | CI lower bps |
    |---|---|---|---|---|---|---|
    | ETH | full 2021-03-24→2026-07-30 | 1,955 | 119.052 | 2.418 | 0.00786 | 38.012 |
    | ETH | second half 2023-11-26→2026-07-30 | 978 | **19.590** | 0.368 | **0.356** | −67.985 |
    | ETH | last 730 (registered depth) 2024-07-31→2026-07-30 | 730 | **26.813** | 0.435 | **0.332** | −74.589 |
    | BTC | last 730 (registered depth) | 730 | 127.434 | 2.966 | 0.00156 | 56.669 |
  - Section 6's endpoint is the conjunction "a variance risk premium exists in BTC **and** ETH", tested as an intersection-union in which "*every* component must reject" (VRPExperiment/REGISTRATION.md:377-386). On the registered 730-observation depth the ETH component does not reject (p = 0.332), so the conjunction fails, and by Section 0's precedence rule — "If the premium fails Section 6, **SIGNAL_ABSENT fires regardless of the venue finding**" (VRPExperiment/REGISTRATION.md:52-53) — the branch that fires on the registered depth is SIGNAL_ABSENT, not VENUE_BLOCKED.
  - The reported "119.05 bps" ETH premium — carried into the README headline (VRPExperiment/README.md:22-24), the deliverable's plain-words answer ("The ether premium is worth about **119 basis points**", VRPExperiment/docs/ARTIFACT.md:38) and the deciding MET comparison — is therefore a figure that exists only over 5.4 years and is absent over the most recent two.
- **What would resolve it:** Report the endpoint on the registered 730-observation depth alongside the full-sample figure, and state which branch each supports. If the full-sample window is the intended primary, say so in the registration's own terms and record that the choice of window is what decides between two of the three registered branches for ETH.
- **Confidence:** HIGH — exact reproduction of the published figures on the same code path, and the sub-window figures use no free parameter beyond the depth the registration itself named.
- **Invalidated by later commits?:** no — d37cf6d is the final commit and the latch is spent.
- **Disclosed by authors?:** partly — the ETH instability is disclosed forcefully and repeatedly (VRPExperiment/HYPOTHESES.md:23, docs/ARTIFACT.md:100-102, docs/HANDOVER.md:80-81), and I say so plainly. What is disclosed nowhere is the ETH premium on the registered 730-observation depth or on the sample's second half, nor that the fired branch's own precondition ("positive and material") does not hold on either.

---

### DRAFT-all-5
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the registered non-overlapping robustness check (REGISTRATION.md §6)
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**BTC n = 66 non-overlapping windows: … ETH n = 66: 0.058053 = 132.793 bps, t = 2.088, p = 0.0203, CI lower 26.688 bps.** Both agree with the primary in **sign and in significance**, so the registered clause \"if they disagree, the disagreement is the finding\" is not triggered." — VRPExperiment/HYPOTHESES.md:20
- **Evidence:**
  - The registered clause: "**Robustness, registered now:** the same test on **non-overlapping** 30-day windows … **If they disagree in sign or significance, the disagreement is the finding and neither is suppressed.**" (VRPExperiment/REGISTRATION.md:372-375).
  - The implementation takes one arbitrary phase of thirty: `def non_overlapping(premium: list[float], stride: int = TENOR_DAYS) -> list[float]: return premium[::stride]` (VRPExperiment/src/vrp/sealed_read.py:304-306). Phase 0 is not registered anywhere; §6 registers only "non-overlapping 30-day windows", of which there are thirty equally valid thinnings.
  - The only test of this function checks its length, not its stability: `assert len(thinned) == math.ceil(len(series) / TENOR_DAYS)` (VRPExperiment/tests/test_estimators.py:237-238). The fixture never exercised it — both fixture runs returned `"robustness_non_overlapping_iid": "insufficient_sample: 29 observations is below the registered floor of 60"` / `"… 9 observations …"` (git show ef07f19 -- reports/task6/fixture_result.json), so the registered robustness estimator was never run against a planted premium before the sealed read.
- **Recomputation (if any):**
  - Inputs: raw series (UNANCHORED, read 2026-09-05T03:55:12Z); estimator with `bandwidth=0` exactly as the driver calls it (VRPExperiment/tools/task6_sealed_run.py:395-398). Script `.../work/agentB-vrp-all/phases.py`.
  - Phase 0 reproduces the published figures exactly: ETH n = 66, mean 132.793 bps, t 2.0883, p 0.0203447, CI lower 26.688; BTC n = 66, 220.872 bps, t 4.5679, p 1.12791e-05, CI lower 140.188.
  - Across all 30 phases: **BTC 30/30 significant** (p 0.0000–0.00016) — robust. **ETH 26/30 significant.** Four phases fail the registered one-sided α = 0.05:
    | phase | n | mean bps | t | p | CI lower bps |
    |---|---|---|---|---|---|
    | 19 | 65 | 92.739 | 1.5473 | **0.06336** | **−7.295** |
    | 20 | 65 | 93.581 | 1.5723 | **0.06041** | **−5.757** |
    | 21 | 65 | 96.014 | 1.6095 | **0.05621** | **−3.548** |
    | 22 | 65 | 97.639 | 1.6668 | **0.05022** | **−0.128** |
  - ETH's non-overlapping mean ranges 92.74–140.41 bps and its lower bound ranges **−7.29 to +36.42 bps** across the thirty thinnings. On 4 of 30, the registration's own clause "if they disagree in significance, the disagreement is the finding" **would have been triggered**.
  - Mitigant, stated: the phase was fixed in code at commit `adac707` (2026-08-29 23:55:29 −0700 = 06:55:29Z), six seconds before the first latch was written at 06:55:35.492Z (VRPExperiment/reports/task6/task6.latch.json). It is therefore a **pre-read** choice, not a post-hoc selection, and I do not allege p-hacking. The finding is that a stated robustness result is presented as a property of the data when it is a property of one of thirty equally admissible versions of the registered check.
- **What would resolve it:** Report the non-overlapping check over all thirty phases (or their distribution), which costs one loop and no new data, and state the fraction that agree.
- **Confidence:** HIGH — exact reproduction of the reported phase, and the other 29 phases use the identical code path with no free parameter.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** no — no document mentions the phase, the stride offset, or any sensitivity of the robustness check; the claim at VRPExperiment/HYPOTHESES.md:20 is stated unconditionally.

---

### DRAFT-all-6
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the revision test — the prompt's "mandatory" TASK 4 question — and its shipped figure
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **revision** | **all six fixed windows byte-identical after ≈ 70 minutes** | 6 windows × 169 rows |" — VRPExperiment/README.md:91. Identically at VRPExperiment/docs/ARTIFACT.md:279-281, VRPExperiment/DECISIONS.md:189-190 ("Six baselines were recorded and re-checked after ≈ 70 minutes"), and VRPExperiment/progress.md:818-821 ("The six data-only baselines recorded at 06:05Z were re-fetched at ~07:15Z, a gap of **≈ 70 minutes**").
- **Evidence:**
  - The repository's own machine-written evidence file gives both endpoints of the interval for all six windows. Baselines: `"taken_at": "2026-08-30T06:26:08.230000Z"` … `"2026-08-30T06:26:09.144000Z"` (VRPExperiment/reports/task4/revision_recheck.json, six `taken_at` fields). Re-checks: `"recheck_taken_at": "2026-08-30T07:03:22Z"` … `"2026-08-30T07:03:23Z"` (six `recheck_taken_at` fields).
  - The same file also carries the wrong label hardcoded into itself: `"gap": "≈70 minutes"` (VRPExperiment/reports/task4/revision_recheck.json, second key). The gap string was written by the tool, not derived from the timestamps it stored beside it.
  - `reports/task4/rate_and_revision_baseline.json` independently gives `"retrieved_at": "2026-08-30T06:25:49.532000Z"`, corroborating the 06:26Z baseline and contradicting progress.md's "06:05Z".
- **Recomputation (if any):**
  - Inputs: `VRPExperiment/reports/task4/revision_recheck.json` (`taken_at` 2026-08-30T06:26:08.230Z, `recheck_taken_at` 2026-08-30T07:03:22Z, window 1).
  - Method: elapsed = 07:03:22 − 06:26:08.230.
  - Result: **37 minutes 13.77 seconds.** The claimed "≈ 70 minutes" is **1.88×** the interval actually measured. The claimed baseline time (06:05Z) is 21 minutes early and the claimed re-check time (~07:15Z) is 12 minutes late; the overstatement is the sum of two independent errors in the same direction.
  - Consequence for what the test establishes: the mandatory question the prompt set was "whether values are ever revised after publication" (VRPExperiment/progress.md:77). A 37-minute re-check of six closed windows establishes less than a 70-minute one, and neither establishes anything about revision at the horizons that matter. The repository applies exactly this scepticism to the corroborating source — "**this is a weak test and is recorded as one** … it establishes only that they are not rewritten *continuously*" (VRPExperiment/progress.md:825-827) — and applies none of it to the Deribit result, which is the one that gates the primary series.
- **What would resolve it:** Correct the interval to 37 minutes in README.md, docs/ARTIFACT.md, DECISIONS.md ADR-009 and progress.md, derive the `gap` field from the stored timestamps rather than hardcoding it, and carry the same "this is a weak test" qualification the CDD row already carries.
- **Confidence:** HIGH — both endpoints are machine-written into a committed artifact and the subtraction is unambiguous.
- **Invalidated by later commits?:** no — `reports/task4/revision_recheck.json` was introduced by d37cf6d, the final commit (`git log --oneline -- reports/task4/revision_recheck.json`).
- **Disclosed by authors?:** no — the interval is asserted as ≈ 70 minutes in four places and contradicted only by the stored artifact none of them quotes.

---

### DRAFT-all-7
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the venue classification of CME MBT options, which is what makes the verdict "qualified"
- **Direction:** B
- **Class:** PROCESS
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| 3 | **CME options on Micro Bitcoin futures (MBT) via Interactive Brokers Canada Inc.** | option on 1 MBT future = **0.10 BTC** | permitted | permitted | **PERMITTED, capital status UNRESOLVED** | …" — VRPExperiment/reports/task3/venue_table.md:24; carried to VRPExperiment/docs/ARTIFACT.md:115 and VRPExperiment/HYPOTHESES.md:62.
- **Evidence:**
  - The registration defines exactly five venue states — PERMITTED, PROHIBITED, CAPITAL_BLOCKED, UNCLEAR, NO_PRODUCT (VRPExperiment/REGISTRATION.md:184-204) — and ADR-004 declares them structural: "**Five venue states**, disjoint from the five operational health states, with no arithmetic between the families: `PERMITTED`, `PROHIBITED`, `CAPITAL_BLOCKED`, `UNCLEAR`, `NO_PRODUCT`" (VRPExperiment/DECISIONS.md:79-81).
  - Guard 4's enum contains those five and no other: `class VenueState(StrEnum): PERMITTED … PROHIBITED … CAPITAL_BLOCKED … UNCLEAR … NO_PRODUCT` (VRPExperiment/src/vrp/callstate.py:39-58), and `AbsenceReason` likewise has `VENUE_BLOCKED`, `VENUE_CAPITAL_BLOCKED`, `VENUE_UNCLEAR` and no unresolved-capital reason (VRPExperiment/src/vrp/absence.py:26-48). "capital status UNRESOLVED" is a **sixth** classification that the guard the repository presents as enforcing this discipline cannot represent, and therefore cannot bind on.
  - The registration's own amendment rule was not followed: "Any amendment is appended here with its date, its reason, and the commit that introduced it. **No section above is edited in place.**" (VRPExperiment/REGISTRATION.md:532-533). The amendment log contains exactly one entry, Amendment 1, about the aborted latch (VRPExperiment/REGISTRATION.md:535-589). `git log --oneline -- REGISTRATION.md` returns only `7827592` (TASK 2) and `ef07f19` (Amendment 1); the new venue state was introduced at `3ad6098` (TASK 3, 2026-08-29 23:22:23 −0700) with no amendment.
  - The new state is load-bearing and it is the one that preserves the more favourable reading. The registered CAPITAL_BLOCKED test is "a **$1,000** sleeve supports **fewer than one position** at the venue's own contract size **and margin**" (VRPExperiment/REGISTRATION.md:195-197); the margin is `Absent(not_served)` (VRPExperiment/reports/task3/venue_table.md:106-107), so the test cannot be evaluated. Classifying MBT CAPITAL_BLOCKED would have made VENUE_BLOCKED unqualified and closed the question; the sixth state instead keeps open the reading that "**the registered HARVESTABLE condition was met on MBT**" (VRPExperiment/docs/HANDOVER.md:26-27).
  - The registration's own rule for the analogous unresolved case points the other way: "**UNCLEAR is a recorded state and is never read as permission.** An unclear venue **cannot support HARVESTABLE**." (VRPExperiment/REGISTRATION.md:200-202). An unresolvable jurisdiction question is registered as fatal to HARVESTABLE; an unresolvable capital question is treated as merely open.
- **Recomputation (if any):** none — this is a comparison of the classification used against the enumerated set registered before data, with the commit that introduced it dated against the registration's own amendment rule.
- **What would resolve it:** Either record an amendment adding a sixth venue state with its date and reason (the registration's own procedure), or classify MBT under one of the five and record the consequence.
- **Confidence:** MEDIUM — the departure from the registered state set and the missing amendment are unambiguous; whether the sixth state is the *wrong* call is a judgement, and the repository's transparency about the open route is real.
- **Invalidated by later commits?:** no — d37cf6d is the final commit and REGISTRATION.md was not touched after ef07f19.
- **Disclosed by authors?:** partly — the open status and its two deciding figures are disclosed prominently (VRPExperiment/README.md:6-8, HYPOTHESES.md:75-83, docs/HANDOVER.md:14-31) and I say so plainly. What is disclosed nowhere is that "capital status UNRESOLVED" is not one of the five states the repository registered and enumerated, and that its introduction was not recorded as an amendment.

---

### DRAFT-all-8
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** ADR-011 / docs/COSTS.md §1.3 / docs/VENUE_TABLE_UPDATE.md Correction 3 — "the central tension of this experiment, in one number"
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The two permitted routes differ by **7.48× in commission basis points** — MET **32.571 bps** against MBT **4.352 bps** per straddle round trip — **entirely because MET's notional is 31.8× smaller**." — VRPExperiment/DECISIONS.md:229-231. Identically: "purely because MET's notional is 31.8× smaller" (VRPExperiment/docs/COSTS.md:100-102); "purely because MET's notional is 31.8× smaller" (VRPExperiment/progress.md:604-606); "a 7.5× spread on the same schedule, **purely from notional**" (VRPExperiment/docs/VENUE_TABLE_UPDATE.md:135-136).
- **Evidence:**
  - The two per-contract commissions are not equal: MET USD 0.20, MBT USD 0.85 (VRPExperiment/docs/COSTS.md:41-42; VRPExperiment/reports/task5/commission_bps.json). MBT's per-contract commission is **4.25× MET's**.
  - The notional ratio quoted in the same sentence is 31.8× (VRPExperiment/reports/task3/venue_table.md:64: $7,812.46 vs $245.62).
- **Recomputation (if any):**
  - Inputs: MET 0.20 / 245.6205; MBT 0.85 / 7,812.4575. Script `.../work/agentB-vrp-all/recompute.py`.
  - notional ratio MBT/MET = 7,812.4575 / 245.6205 = **31.8070**.
  - bps ratio MET/MBT = (0.20/245.6205) / (0.85/7,812.4575) = **7.4840**.
  - commission ratio MBT/MET = 0.85 / 0.20 = **4.2500**, and 31.8070 / 4.2500 = **7.4840**.
  - If the difference were "entirely"/"purely" notional the ratio would be **31.81×**, not 7.48×. The schedule's own per-contract difference removes 4.25× of it, in MET's favour. The claim contradicts the two figures it quotes in the same sentence.
- **What would resolve it:** Restate as "7.48×, which is the 31.8× notional ratio partly offset by MBT's 4.25× larger per-contract commission" — and correct it in `docs/VENUE_TABLE_UPDATE.md`, where it is being carried to another repository as a proposed standing note.
- **Confidence:** HIGH — two divisions on the repository's own published figures.
- **Invalidated by later commits?:** no — d37cf6d is the final commit; VENUE_TABLE_UPDATE.md was introduced by it.
- **Disclosed by authors?:** no — the word "entirely"/"purely" is used in all four places and no document qualifies it.

---

### DRAFT-all-9
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the shipped Deribit reference straddle-spread figures (BTC 22.50 bps, ETH 25.00 bps) and the structural claim they carry
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the same 30-day ATM straddle's quoted round-trip spread was measured across **24 observation windows per leg, 96 observations, zero unquoted**: **BTC 22.50 bps, ETH 25.00 bps** at the medians." — VRPExperiment/docs/ARTIFACT.md:196-198. Supported by "a 24-window sample of a tick-bound quantity is a much better estimate of its central tendency than 24 windows of a freely-moving one" (VRPExperiment/docs/COSTS.md:240-241).
- **Evidence:**
  - The 96 observations are one burst. The stored file gives `"started_at": "2026-08-30T06:33:33Z"`, `"finished_at": "2026-08-30T06:41:34Z"`, `"spacing_seconds": 20.0`, `"windows_registered": 24` (VRPExperiment/reports/task5/reference_spreads_deribit.json). First and last observation on every leg: 06:33:34Z → 06:41:33Z. Total span **8 minutes 1 second**, on one morning, on one strike per asset, at one expiry, at one time of day.
  - The tool hard-codes it: `WINDOWS = 24` (VRPExperiment/tools/measure_spreads.py:36), `SPACING_SECONDS = 20.0` (VRPExperiment/tools/measure_spreads.py:39).
  - The registered requirement the figure is presented against is "sampled across **at least 20 distinct observation windows**, reported as **median, 90th percentile, and the full distribution, each with its `n`**" (VRPExperiment/REGISTRATION.md:253-256). §4.1 formally binds only on PERMITTED venues, and Deribit is PROHIBITED — but `docs/COSTS.md:194-196` presents the sample as "**24 registered observation windows**" and the README lists it as a measured figure with n (VRPExperiment/README.md:67: "24 windows/leg, 96 observations, 0 unquoted").
  - The justification is made from inside the burst. "This makes the 24-window sample a good estimate of a *stable* quantity rather than a lucky draw on a moving one" (VRPExperiment/progress.md:661-662) is inferred from the fact that all 96 observations took the values 5.0/7.5/10.0/12.5 bps within those 8 minutes. A sample confined to 8 minutes cannot detect time-of-day, session or regime variation, which is the variation the claim of stability excludes.
  - The ETH leg is not at the money: strike 2,500 against `"spot_index": 2457.21` — 1.74% away (VRPExperiment/reports/task5/reference_spreads_deribit.json, `series.ETH`), against §4.1's "the ATM series at the 30-day tenor, not a proxy instrument" (VRPExperiment/REGISTRATION.md:253-254). The BTC leg is 0.23% away. Both are consequences of listed strike granularity and neither is flagged.
  - The figure is not inert: ADR-008 says "**The reference still earns its place, because it supports one claim that needs no substitution: the commission alone on the affordable permitted route exceeds the entire quoted spread on the prohibited one.**" (VRPExperiment/DECISIONS.md:172-175), and the claim is repeated in the deliverable (VRPExperiment/docs/ARTIFACT.md:202-205), COSTS.md §4.4 and progress.md:668-676.
- **Recomputation (if any):**
  - Inputs: `VRPExperiment/reports/task5/reference_spreads_deribit.json`, all four legs' `at` fields and `half_spread_bps_of_notional` values.
  - Method: span = last `at` − first `at`; count distinct 20-second polls.
  - Result: span 06:33:34Z → 06:41:34Z = **8 min 0 s**; 24 polls per leg; effective independent observations of a quoted touch over an 8-minute window is on the order of **one**, not 24. The distributions are near-degenerate (BTC put 19×5.0 and 5×7.5; ETH call 15×5.0 and 9×7.5), consistent with sampling one state repeatedly rather than a distribution.
  - Note that the comparison the figure supports is also asymmetric in the venues' cost components: it sets MET's *commission* against Deribit's *spread*, and Deribit's own commission is neither measured nor mentioned. The sentence is worded to survive this ("the venue they may use is more expensive in commission alone than the other is in total spread", VRPExperiment/docs/COSTS.md:264-266), so I do not raise it as a separate defect, but it is part of why the comparison reads stronger than it is.
- **What would resolve it:** Sample across days and times of day, or relabel the figure as "one 8-minute snapshot on 2026-08-30, 24 polls 20 s apart" everywhere it appears, and drop the "stable rather than lucky" inference, which the sample cannot support.
- **Confidence:** HIGH — the span is read directly from the timestamps stored with every observation.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** partly — the 20-second spacing is stated at VRPExperiment/docs/COSTS.md:196 and progress.md:648, so a reader who multiplies can recover the 8 minutes; the 26.06-day expiry is disclosed at COSTS.md:214-216. No document states the total span or qualifies the "24 windows / 96 observations" framing that appears in the README and the deliverable.

---

### DRAFT-all-10
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the provenance of the deciding premium — the instruments it was measured on versus the route it is priced against
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**No figure was substituted for any of these.** In particular, no spread was carried from another instrument or another venue. That substitution is a known way to get this kind of measurement badly wrong" — VRPExperiment/docs/ARTIFACT.md:187-189
- **Evidence:**
  - The implied leg is **Deribit's** DVOL index, computed by Deribit from **Deribit's own option book** (VRPExperiment/REGISTRATION.md:90-93). Deribit is the venue classified PROHIBITED for the resident whose question this is (VRPExperiment/reports/task3/venue_table.md:22).
  - The costs the premium is compared against are **CME MET/MBT option and futures** commissions through IBKR Canada (VRPExperiment/docs/COSTS.md:39-45). No CME crypto-option implied volatility was ever observed — "**No public source serves CME MET or MBT option quotes without an account.**" (VRPExperiment/docs/COSTS.md:127).
  - So the deciding comparison sets a premium measured on one venue's book against costs measured on a different venue's book, and this cross-venue step is not named in any document, while the repository forbids the corresponding step on the cost side in four places (VRPExperiment/DECISIONS.md:159-175 ADR-008; docs/COSTS.md:135-140; docs/HANDOVER.md:73-76; docs/ARTIFACT.md:187-193).
  - The realized leg has a second, smaller mismatch. The code fetches `f"{currency}-PERPETUAL"` closes (VRPExperiment/tools/task6_sealed_run.py:150-152) — which the deliverable does name ("Deribit's own perpetual for the underlying", VRPExperiment/docs/ARTIFACT.md:56-57). But the perpetual is not the index DVOL is computed on, the registration names no price series at all — §2.3 says only "the 30 daily log returns `r_i = ln(P_i / P_{i-1})`" (VRPExperiment/REGISTRATION.md:105-107) — and docs/ACCESS.md certified the requirement met against a **different** endpoint: "| underlying closes for the realized leg | daily, same UTC instant | `get_index_price` served, HTTP 200 | **met** |" (VRPExperiment/docs/ACCESS.md:266). `get_index_price` serves a current index level and cannot supply a daily history; the series actually used came from `get_tradingview_chart_data`, an endpoint TASK 4 validated only for its bucket timestamps (VRPExperiment/docs/ACCESS.md:284-287). That gap is exactly what TASK 6 attempt 1 crashed on.
- **Recomputation (if any):** none required — the substitution is established from the registration, the driver source and the access document, not from a number. Direction of the perpetual-vs-index error is likely conservative (basis noise raises realized volatility and so lowers the measured premium), which is why this is S3 and not higher; the Deribit-vs-CME implied-volatility substitution has no sign this repository can establish, because it never observed a CME crypto-option implied volatility.
- **What would resolve it:** State in the deliverable that the premium is measured on the prohibited venue's book and applied to the permitted venue's costs, and that no CME crypto-option implied volatility was ever observed; name the perpetual (rather than the index) as the realized-leg series in the registration's own terms and correct docs/ACCESS.md:266.
- **Confidence:** MEDIUM — the substitution is factual and its cross-venue half is undocumented; its magnitude is unmeasured by anyone, including this audit, and could be small.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** partly — the deliverable names both Deribit sources plainly (VRPExperiment/docs/ARTIFACT.md:56-59, 270-271), so the facts are on the page, and I say so. What no document states is the *inference step*: that the deciding premium was measured on a venue the route cannot trade, that no CME crypto-option implied volatility was observed, and that this is the same class of cross-venue substitution the repository refuses four times on the cost side. Section 8's epistemic boundary (VRPExperiment/REGISTRATION.md:451-467) lists five things the repository does not measure and this is not among them.

---

### DRAFT-all-11
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the shipped DVOL history-depth figure
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| DVOL history depth, **bisected** | **1,992 days** (≈ 2021-03-17) | 22 probes/asset |" — VRPExperiment/README.md:87. Also "| history available | **1,992 days**, established by bisection, ≈ 2021-03-17 |" (VRPExperiment/docs/ARTIFACT.md:272) and "| **BTC** | **1,992 days back** | 1,993 days back | **2021-03-17T06:23:58Z** |" under a column headed "approximate earliest served" (VRPExperiment/docs/ACCESS.md:89-92).
- **Evidence:**
  - The repository's own bisection probe at 1,992 days back returned **exactly one row**, and that row is dated 2021-03-24: `{"days_back": 1992, "row_count": 1, "first_utc": "2021-03-24T00:00:00Z", "last_utc": "2021-03-24T00:00:00Z", "status_code": 200}` for both assets (VRPExperiment/reports/task4/deribit_probe.json, `history_depth[*].probes`). The 1,984-day probe returned rows beginning 2021-03-25.
  - The `approx_earliest_served_utc` field is not the earliest served row; it is the probe window's start, i.e. `retrieved_at − 1992 days`. `retrieved_at` is `2026-08-30T06:23:36.709000Z` and the field reads `2021-03-17T06:23:58.039000Z` — the same clock time of day, 1,992 days earlier.
  - The sealed read settles it independently: `"implied_days_served": 1985`, `"implied_span": ["2021-03-24", "2026-08-29"]` for both assets (VRPExperiment/reports/task6/real_attempt2_result.json:6-10, 129-133).
  - The corroborating source agrees: CryptoDataDownload's oldest DVOL row is 2021-03-24, and the CSVs carry 1,986 daily rows spanning 2021-03-24→2026-08-30 (VRPExperiment/docs/ACCESS.md:94-95, 219-220).
- **Recomputation (if any):**
  - Inputs as above. Method: compare the published depth against the earliest served row in the repository's own probe and in its own sealed read.
  - Result: DVOL depth is **1,985 days** to **2021-03-24**, not 1,992 days to 2021-03-17 — an overstatement of **7 days (0.35%)**. The derived multiple "2.73× the registered minimum depth of 730" (VRPExperiment/docs/ACCESS.md:98, 262) is correspondingly 2.72×. Nothing downstream changes; the analysis used the 1,985 days it actually had.
- **What would resolve it:** Report the earliest served DVOL observation (2021-03-24) rather than the window start, and rename `approx_earliest_served_utc` to what it holds.
- **Confidence:** HIGH — the probe row, the sealed read and the third-party corroboration all give 2021-03-24.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** partly — docs/ACCESS.md:94-96 notes CDD's oldest row is 2021-03-24, "one week later, which is consistent with a series beginning in the second half of March 2021", so the discrepancy is visible; but the repository treats its own computed window start as the measurement and the true first row as merely "consistent", and the 1,992/2021-03-17 pair is what the README and the deliverable ship.

---

### DRAFT-all-12
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the append-only progress ledger and its "ETA against actual" table
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| 6 · the sealed read | 50 min | **~55 min** | overran on attempt 1's abort and Amendment 1 |" and "**The only overrun was TASK 6**, and it was the abort … **The recovery cost ~15 minutes**" — VRPExperiment/progress.md:850, 855-857. Header: "Single-stage scoped census. Append-only. **Timestamps timezone-aware UTC.**" (VRPExperiment/progress.md:3).
- **Evidence:**
  - The ledger's own entry timestamps give TASK 5 COMPLETE at 07:00Z (VRPExperiment/progress.md:578) and TASK 6 COMPLETE at 07:05Z (VRPExperiment/progress.md:698) — **5 minutes**, against a recorded actual of ~55.
  - The machine-written TASK 6 artifacts bound it independently: attempt-1 latch `"written_at": "2026-08-30T06:55:35.492Z"` (VRPExperiment/reports/task6/task6.latch.json), fixture re-run `"finished_at": "2026-08-30T06:57:32Z"` (VRPExperiment/reports/task6/fixture_result.json), attempt-2 latch `"written_at": "2026-08-30T06:58:05.858Z"`, result `"finished_at": "2026-08-30T06:59:48Z"` (VRPExperiment/reports/task6/real_attempt2_result.json:253, 271). Latch 1 to result = **4 min 12.5 s**. Latch 1 to latch 2 — the "recovery" — = **2 min 30.4 s**, against a recorded ~15 minutes.
  - TASK 4's stated measurement window closes before its own evidence exists. "**Measured 2026-08-30, 05:45Z–06:10Z.** Machine-readable evidence in `reports/task4/deribit_probe.json` and `reports/task4/rate_and_revision_baseline.json`" (VRPExperiment/docs/ACCESS.md:3-4). Those two files carry `"retrieved_at": "2026-08-30T06:23:36.709000Z"` and `"retrieved_at": "2026-08-30T06:25:49.532000Z"` respectively — 13 and 15 minutes **after** the stated window closed, and 11 and 13 minutes after progress.md:477 declares "TASK 4 COMPLETE" at 06:12Z.
  - `reports/task3/venue_table.md:3` states TASK 3 was "Measured 2026-08-30, **04:32Z**–05:35Z", which begins 15 minutes before the registration commit `7827592` (2026-08-29 21:47:08 −0700 = 2026-08-30 **04:47:08Z**). **I found no evidence of any pre-registration network call** — the earliest dated TASK 3 retrieval in the repository is 05:13Z (VRPExperiment/reports/task3/deribit_restricted_jurisdictions_verbatim.md:7) and the CME refusal is stamped 05:27Z (VRPExperiment/reports/task3/robots_and_terms.md:20). 04:32:03Z is the session-start stamp at progress.md:7, apparently reused. I record it because REGISTRATION.md:3 and progress.md:252 both rest on "before any network call", and the one document that dates the first measurement contradicts them on its face.
- **Recomputation (if any):**
  - Inputs: the nine "TASK n COMPLETE" timestamps in progress.md (lines 7, 114, 194, 249, 347, 477, 578, 698, 758, 814) and the "actual" column at progress.md:844-853.
  - Method: sum the per-task actuals and compare with the ledger's own wall-clock span.
  - Result: 6 + 14 + 12 + 36 + 32 + 48 + **55** + 7 + 23 = **233 min**, reported as "≈ 3 h 53 m" (progress.md:853). Wall clock from TASK 0 START 04:32:03Z to TASK 8 COMPLETE 07:35Z = **183 min**. The 50-minute excess is exactly TASK 6's 55 − 5. Every other row reconciles to the minute.
  - `git log` shows the commit that introduced the "TASK 8 COMPLETE — 07:35Z" entry is `d37cf6d`, dated 2026-08-30 00:08:02 −0700 = **07:08:02Z** — 27 minutes before the completion time the entry it contains asserts.
- **What would resolve it:** Derive the ledger's actuals from the entry timestamps (or from commit times), and correct TASK 6's actual, TASK 4's measurement window and TASK 3's stated start.
- **Confidence:** HIGH — every figure is either in the ledger itself or machine-written into a committed artifact.
- **Invalidated by later commits?:** no — d37cf6d is the final commit and introduced the affected entries.
- **Disclosed by authors?:** partly — progress.md:678 discloses that "TASK 6 machinery [was] built while TASK 5's measurement ran", which explains overlapping work but not a per-task actual that exceeds the ledger's own span, and no document reconciles the totals.

---

### DRAFT-all-13
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the units of the headline premium figures in README.md and HYPOTHESES.md
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| BTC premium, mean | **0.086607 vol points = 198.111 bps of notional** | **1,955 daily observations** |" — VRPExperiment/README.md:36. Also "**BTC: mean 0.086607 annualised volatility points = 198.111 bps of notional**" (VRPExperiment/HYPOTHESES.md:19) and "0.096558 vol points = 220.872 bps", "0.058053 = 132.793 bps" (VRPExperiment/HYPOTHESES.md:20).
- **Evidence:**
  - The registered conversion is "**One volatility point of premium is 22.875 bps of notional**" (VRPExperiment/REGISTRATION.md:166), and the code's own docstring says the series is in decimal: "``premium`` is in **decimal** volatility (0.05 = five volatility points)" (VRPExperiment/src/vrp/sealed_read.py:272).
  - So 0.086607 **decimal** volatility is 8.6607 volatility points, not 0.086607 volatility points. `docs/ARTIFACT.md:71` gets it right — "**mean premium** | **8.66 volatility points** | **5.20 volatility points**" — while README.md and HYPOTHESES.md label the decimal as "vol points".
  - The stored field carries the same mislabel: `"mean_vol_points": 0.086607` (VRPExperiment/reports/task6/real_attempt2_result.json:19).
- **Recomputation (if any):**
  - Method: apply the repository's own registered conversion to its own headline figure as labelled.
  - Result: 0.086607 "vol points" × 22.875 bps/vol point = **1.981 bps**, against the 198.111 bps printed in the same table cell — a factor of 100. Applying it to the value's true units, 8.6607 vol points × 22.874639 = **198.111 bps**, which is correct. The bps figures throughout are right; only the volatility-point labels in README.md and HYPOTHESES.md are wrong, and a reader who checks the repository's own conversion against its own headline finds a 100× mismatch.
- **What would resolve it:** Write "0.086607 in decimal volatility = 8.66 volatility points = 198.111 bps" in README.md and HYPOTHESES.md, matching docs/ARTIFACT.md:71, and rename the JSON field.
- **Confidence:** HIGH — the repository states the conversion, the code states the units, and the deliverable uses the correct form.
- **Invalidated by later commits?:** no — d37cf6d is the final commit.
- **Disclosed by authors?:** no — no document notes the discrepancy between README.md:36 and docs/ARTIFACT.md:71.

---

## What I checked and found sound

Everything below is something the thesis "this repository claimed more than it earned" predicted I would find and did not.

1. **The primary estimator is exactly right.** I reimplemented §2.3, §2.4, §2.6 and §6 independently (`.../work/agentB-vrp-all/rebuild.py`) from the untracked raw series and reproduced every published primary figure to the last stored digit for both assets: mean, HAC standard error, t, one-sided p, CI lower in volatility points and in bps, and positive share (VRPExperiment/reports/task6/real_attempt2_result.json:12-24, 135-147). The realized leg is genuinely forward-looking (`window_days = [day + timedelta(days=k) for k in range(TENOR_DAYS + 1)]`, VRPExperiment/tools/task6_sealed_run.py:216), `ddof=1` and √365 are as registered (src/vrp/sealed_read.py:73-74), the sign is `IV − RV` applied once (src/vrp/sealed_read.py:109), and the percent-to-decimal conversion is correct (`implied_pct[day] / 100.0`, tools/task6_sealed_run.py:225).
2. **The Newey–West implementation is standard and correct**, Bartlett weights `1 - lag/(bandwidth+1)`, autocovariance divided by n, and it refuses rather than returning a value when the long-run variance is non-positive (VRPExperiment/src/vrp/sealed_read.py:135-149). Bandwidth 30 was registered before any data (REGISTRATION.md:366-371), for a stated reason, and the non-overlapping check gives a *lower* t on both assets, which is the direction a slightly-too-narrow HAC would predict and which the repository reports rather than hides.
3. **All six rebalance distributions reproduce exactly** — every min, median, mean, p90 and max at bands 0.05/0.10/0.20 for both assets (`.../work/agentB-vrp-all/reb.py` against VRPExperiment/reports/task6/real_attempt2_result.json:25-55, 148-178).
4. **Amendment 1's central factual claim is true and I verified it against the diff.** It asserts "the only change between attempt 1 and attempt 2 is a **single string literal** in a request parameter — `\"3600\"` to `\"60\"` — plus the attempt-numbering that keeps the first latch. No estimator, no window, no estimator parameter, no tenor, no sign convention and no inference rule was touched." (VRPExperiment/REGISTRATION.md:578-584). `git show ef07f19 -- tools/task6_sealed_run.py` shows exactly that: the resolution literal plus a comment, a `latch_path()` helper, an `--attempt` argument and an output-filename suffix. Nothing in `src/vrp/` changed in that commit. This is an amendment that records a mechanical failure and rescues nothing.
5. **REGISTRATION.md was never edited in place.** `git log --oneline -- REGISTRATION.md` returns only `7827592` (TASK 2) and `ef07f19` (Amendment 1), and the ef07f19 diff touches only the amendment log (58 insertions, 2 deletions, all below "## Amendment log").
6. **The registration genuinely precedes the network calls.** Commit `7827592` is dated 2026-08-30T04:47:08Z; the earliest dated retrieval anywhere in the repository is 05:13Z (Deribit policy). The one document that says otherwise (venue_table.md:3, "04:32Z") is a stamp reused from the session start and is raised only as hygiene in DRAFT-all-12; I found no evidence of a pre-registration fetch.
7. **The margin, the estimator, the tenor, the sign convention, the α, the HAC bandwidth, the ±0.10 band, the central/pessimistic statistic assignment and the conversion were all fixed before data** (REGISTRATION.md §2, §4.2, §4.3, §5, §6) and none was changed afterwards. The Berger (1982) intersection-union argument for applying no multiplicity correction (REGISTRATION.md:381-393) is correctly stated and correctly applied: the endpoint really is a conjunction, and an IUT is conservative at nominal α per component.
8. **The refusals were obeyed.** CME's 403 stopped all cmegroup.com fetching with the refusal recorded verbatim and no user-agent rotation, proxy or mirror (VRPExperiment/reports/task3/robots_and_terms.md:18-39, DECISIONS.md ADR-003). Laevitas and Amberdata were recorded `Absent(not_served)` rather than worked around. Volmex was recorded "not located" rather than "does not exist" (docs/ACCESS.md:209-212) — a distinction most repositories collapse.
9. **`Absent` is structurally enforced, not merely promised.** `src/vrp/absence.py` refuses `float()`, `int()`, `__index__`, arithmetic both ways, ordering, `bool()`, `len()`, iteration and indexing; the ten reasons are enumerated; and `CallStateTally.combined_total()` raises rather than returning a merged count (src/vrp/callstate.py:111-118).
10. **The guards carry canaries that demonstrably fire**, including a blindness-pin canary on a planted `payload["mark_iv"]` and an open-guard canary that asserts exactly two of three planted calls are caught (progress.md:238-243; tests/test_guards.py). 50 tests, matching the claim at README.md:122 (`grep -c "^def test"`: 22 + 28).
11. **The two self-corrections in TASK 4 are real corrections, honestly recorded**: the whole-response digest false positive on revision (ADR-009), and the sequential-burst measurement of a rate ceiling that measured latency instead (docs/ACCESS.md:119-140), where the honest statement "an upper bound that was not reached, not a measured ceiling" is exactly right and is the kind of sentence this audit usually has to write itself.
12. **The DOGE finding is a genuine and well-recorded trap**: an unsupported currency returns HTTP 200 with an empty array, and the repository records that a caller reading "empty" as "no volatility" would synthesize a value (docs/ACCESS.md:68-82).
13. **The carried-figure re-verification did its job and the measurement won**: MBT notional $6,505 → $7,812.46 (+20.1%) and MET $191 → $245.62 (+28.6%), both disagreements recorded and both used downstream (reports/task3/venue_table.md:93-98). The prior's own reasoning was then scored against the outcome and marked "right for a partly wrong reason" (HYPOTHESES.md:94-117, docs/HANDOVER.md:56-57) — a stricter self-scoring than the audit would have imposed.
14. **The duplication screen is reasoned rather than asserted**, including a two-pass acronym screen that correctly identifies 4,154 `VRP` substring hits in solattn as Bluesky-DID artifacts with zero word-boundary hits, and three closure-by-closure arguments (docs/DUPLICATION.md:1-171).
15. **The epistemic boundary is unusually honest and is repeated in the deliverable**: no strategy, no fill model, no margin path, and above all "**No tail is measured** … the premium is compensation for exactly that risk, so measuring the premium without the tail measures the payment and not the liability" (REGISTRATION.md:460-464, docs/ARTIFACT.md:250-253). The IBKR daily Exposure Fee was found, recorded verbatim and used to mark the cost as incomplete in a known direction (reports/task3/venue_table.md:139-153).
16. **The verdict's qualification is not buried.** "This is not a clean VENUE_BLOCKED … MBT is **not shown to fail** — it is shown to be **unmeasurable from outside a brokerage account**" (HYPOTHESES.md:77-83), and the README carries "qualified — one route open on two named figures" in its status line (README.md:6-8). I considered raising the structural point that a design in which any unmeasurable cost yields VENUE_BLOCKED makes the registered expectation partly self-fulfilling, and did not, because the authors state it themselves in those words.
17. **All the headline commission arithmetic checks out**: MET/MBT straddle round trips (32.571 / 4.352 bps), the hedge legs at 11 and 16 rebalances, the totals (122.140 / 162.853 / 16.320 / 21.760), the 8.57× and 3.28× ratios, the 49.61 bps room, the 12.80% margin threshold, the 390.6× and 122.8× capital multiples, the 4.07× and 0.128× sleeve ratios, the 60.4% BTC decay, the §2.6 conversion (2287.464 bps per unit decimal volatility) and the Section 7.2 power arithmetic (119.4 and 477.5 weeks). Every one reproduces.

---

## Live-repo access log

**Before** (`git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`, run before the first live access):

```
```
(empty — working tree clean)

**After** (same command, run after the last live access):

```
```
(empty — working tree clean)

`git rev-parse HEAD` = `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` before and after, matching the anchored SHA.

Live-repo operations performed, all read-only: `git status --porcelain`, `git rev-parse HEAD`, `git log --oneline --pretty`, `git log -S`, `git log -- <path>`, `git show --stat`, `git show <sha> -- <path>`, `cat .gitignore`, `ls -la data/raw/task6/`, `du -sh data`, and `cp data/raw/task6/*.json` into
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentB-vrp-all/data/` (copy out only; nothing written into the audited repository). The four raw series files are **UNANCHORED** working-tree data, read 2026-09-05T03:55:12Z; they may have changed after the anchor, though their content reproduces the anchored `reports/task6/real_attempt2_result.json` exactly, which is strong evidence they have not.
