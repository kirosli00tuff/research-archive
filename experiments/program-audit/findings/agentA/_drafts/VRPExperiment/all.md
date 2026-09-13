# Agent A draft findings — VRPExperiment (part: all)

**Repository:** VRPExperiment · **Anchored SHA:** `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30)
**Direction:** A — closed too early or too hard.
**Live HEAD at audit time equals the anchor** (`git -C … rev-parse HEAD` → `d37cf6d…`, no commits after), so no finding below can be invalidated by a later commit in this repository as of 2026-09-03.

Standing note carried into every finding: **the fired verdict itself (VENUE_BLOCKED) survives every recomputation below.** Nothing here shows HARVESTABLE should have fired. What the findings show is that several of the deciding *statements*, the *blockers*, and the *reopen conditions* are stated more strongly than the repository's own numbers and its own recorded evidence support, and that two of them reverse under parameterisations the repository itself registered and measured.

---

### DRAFT-all-1
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** H1 — the MET (Micro Ether) route's "COST-EXCEEDED — established" classification, and the deciding claim that the ETH premium does not cover the commission
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "And the failure does not depend on the margin at all: **the ETH premium's point estimate, 119.052 bps, is below the central commission-only cost of 122.140 bps.** The premium does not cover the commission." — VRPExperiment/HYPOTHESES.md:21 (restated at VRPExperiment/docs/ARTIFACT.md:38-39 "**the broker's commission alone, at $0.20 a contract, costs 122 basis points of notional over one hedged round trip.** The ether premium is worth about **119 basis points**. **The commission is larger than the premium**", at VRPExperiment/docs/ARTIFACT.md:212-214, at VRPExperiment/README.md:23-24, and at VRPExperiment/progress.md:788-790)
- **Evidence:**
  - The 122.140 bps figure is **32.571 bps straddle commission + 11 × 8.143 bps hedge commission**, where 11 is the **median rebalance count at the registered ±0.10 delta band** (VRPExperiment/docs/ARTIFACT.md:163, VRPExperiment/progress.md:780, n = 1,955 paths per asset).
  - The registration does **not** register ±0.10 as the only band. It registers a sweep: "the count is additionally reported at **±0.05 and ±0.20** as a sensitivity, with the ±0.10 figure as the registered primary" — VRPExperiment/REGISTRATION.md:296-297, on the stated ground that "a rebalancing band is a **trade-off between bounded capital and bounded trading cost** and is therefore **swept and reported, never chosen**" (VRPExperiment/REGISTRATION.md:294-296).
  - The sweep **was run and its full distribution recorded**: at band 0.20, ETH median **5**, p90 **9**, n = 1,955 — VRPExperiment/reports/task6/real_attempt2_result.json (ETH `rebalances`, band 0.2 entry; same values summarised at VRPExperiment/progress.md:753-754 "at ±0.20 both are 5 (p90 9)").
  - The swept counts are reported as counts only. **No document in the repository converts them into a cost.** README.md:62 lists "rebalances at ±0.05 / ±0.20 (swept, not chosen) | median 17 / median 5"; no bps figure follows. The deciding tables (VRPExperiment/docs/ARTIFACT.md:165-172, VRPExperiment/progress.md:777-786, VRPExperiment/HYPOTHESES.md:21) carry the ±0.10 numbers only.
  - At the swept ±0.20 band the quoted claim is **false**: MET central commission-only cost is **73.284 bps**, against an ETH premium point estimate of **119.052 bps** (VRPExperiment/reports/task6/real_attempt2_result.json, ETH `primary_overlapping_hac.mean_bps`, n = 1,955). The premium covers the commission with 45.8 bps to spare.
  - The claim that no further measurement can reverse the MET conclusion — "Because every cost input is a lower bound, no further measurement can reverse this — additional cost data can only widen the gap" (VRPExperiment/docs/ARTIFACT.md:216-217) — is true of the *spread and fee* legs but not of the *rebalance count*, which is not a lower bound but a modelled output of a band the registration explicitly declined to fix.
- **Recomputation (if any):**
  - Inputs: MET commission USD 0.20/contract (VRPExperiment/docs/COSTS.md:41), MET notional USD 245.62 (VRPExperiment/reports/task3/venue_table.md:64), rebalance medians/p90s from VRPExperiment/reports/task6/real_attempt2_result.json.
  - Method: `straddle = 4 × 0.20 / 245.62 × 1e4`; `per-fill = 0.20 / 245.62 × 1e4`; `central = straddle + median × per-fill`; `pessimistic = straddle + p90 × per-fill`; HARVESTABLE test `premium_CI_lower ≥ 2.0 × pessimistic` per VRPExperiment/REGISTRATION.md:316. Script: `/tmp/claude-1000/.../scratchpad/work/agentA-VRP/recompute.py`.
  - Result (MET / ETH, CI lower 38.0124 bps, point 119.0521 bps):
    - band ±0.05 (med 17, p90 22): central **170.996**, pessimistic **211.709**; 2× pess = 423.418 → fails by 11.14×; central > premium point.
    - band ±0.10 (med 11, p90 16): central **122.140**, pessimistic **162.853**; 2× pess = 325.706 → fails by 8.57×; central > premium point. *(reproduces the repository's published figures exactly)*
    - band ±0.20 (med 5, p90 9): central **73.284**, pessimistic **105.855**; 2× pess = 211.709 → fails by 5.57×; **central < premium point.**
  - So: the registered 2.0× margin test fails on MET at every swept band (the verdict is safe), but the *separate, freestanding* claim that the commission exceeds the premium — the one the artifact leads with and the one that needs no margin — holds only at the two finer bands and reverses at the third, which the repository registered and measured.
- **What would resolve it:** Publish the cost table at all three registered bands, as Section 4.3 requires the count to be reported; and restate the headline as "at the registered ±0.10 band the commission exceeds the premium; at the registered ±0.20 sensitivity it does not", or justify why the sensitivity that was registered as mandatory is not carried into the deciding comparison.
- **Confidence:** HIGH — every input is the repository's own published figure and the arithmetic reproduces its published numbers to three decimals before diverging only where the band changes.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA and the working tree is clean, so no later commit exists.
- **Disclosed by authors?:** no — the swept counts are published (VRPExperiment/README.md:62, VRPExperiment/progress.md:753-754) but the repository nowhere states or acknowledges that its headline comparison reverses at one of them.

---

### DRAFT-all-2
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** H1 — the registered delta-hedging rule (REGISTRATION.md §4.3) and the MET hedge cost it produces
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Delta-hedge the short ATM straddle on the reachable futures contract, resized whenever the position delta moves more than ±0.10 from flat, evaluated once per calendar day at the fixed UTC instant of Section 2.5, over the 30-day tenor.**" — VRPExperiment/REGISTRATION.md:289-291; and the cost it produces, "delta hedge, central (11 rebalances) | 89.57 bps" — VRPExperiment/docs/ARTIFACT.md:168
- **Evidence:**
  - The hedge instrument is the micro future itself: "The delta hedge is the **MET or MBT future itself**" — VRPExperiment/docs/COSTS.md:175. One MET future is **0.10 ETH**, i.e. exactly the underlying of one MET option (VRPExperiment/reports/task3/venue_table.md:61). A straddle's delta, as implemented, is `2·N(d₁) − 1` in units of **one futures contract** (VRPExperiment/src/vrp/sealed_read.py:319-337).
  - Therefore a ±0.10 band asks for a hedge adjustment of **0.10 of one futures contract**. Futures are not divisible. The registration required the census to record this: "Contract size · **minimum order increment** · notional at current spot · initial …" — VRPExperiment/REGISTRATION.md:208 (identically in the governing prompt at VRPExperiment/progress.md:69). **TASK 3 recorded a price increment instead of an order increment**: "| minimum price increment | **$5.00 per bitcoin = $0.50 per contract** … | **$0.50 per ether = $0.05 per contract** |" — VRPExperiment/reports/task3/venue_table.md:62. No quantity increment is recorded anywhere in the repository.
  - The sleeve makes the granularity floor binding even at maximum size: `$1,000 / $245.62 = 4.071` MET contracts (VRPExperiment/docs/ARTIFACT.md:142, "**4.07×**"). With at most 4 whole contracts the finest achievable delta step is **0.25**, still coarser than the registered 0.10; with 1 contract it is 1.00. On MBT the sleeve buys **0.128×** (VRPExperiment/docs/ARTIFACT.md:143), so the step is 1.00 at best.
  - The repository charges a **full contract's commission ($0.20 = 8.143 bps) for each 0.10-contract adjustment** (VRPExperiment/docs/COSTS.md:93-96). The model therefore prices a trade the venue will not accept, at the commission of a trade ten times larger.
  - Section 5's list of the three unmeasured error sources (VRPExperiment/REGISTRATION.md:320-336) names "the rebalance count is a rule, not an observed path" and cites gaps, halts and margin calls — all of which push the count *up*. The granularity floor pushes it sharply *down*, and is not among them.
- **Recomputation (if any):**
  - Inputs: the repository's own raw series, read read-only from the live working tree (untracked, gitignored: `data/` in VRPExperiment/.gitignore): `/home/kiros-li/Documents/GitHub/VRPExperiment/data/raw/task6/{dvol,underlying}_{BTC,ETH}_daily.json`, **read 2026-09-03T (this session), UNANCHORED** — these files are not in git and may have changed since the anchor; commission and notional inputs as in DRAFT-all-1.
  - Method: an independent re-implementation of `count_rebalances` (VRPExperiment/src/vrp/sealed_read.py:350-405) and `straddle_delta` (VRPExperiment/src/vrp/sealed_read.py:319-337) and of the driver's pairing (VRPExperiment/tools/task6_sealed_run.py:207-262), run in `/tmp/claude-1000/.../scratchpad/work/agentA-VRP/bands.py`. **Validation:** the re-implementation reproduces the repository's published premium means exactly (BTC 0.086607 vol pts = 198.111 bps, ETH 0.052045 = 119.052 bps, n = 1,955 each) and its published rebalance medians/p90s at bands 0.05/0.10/0.20 exactly, before being extended to bands the repository did not report.
  - Result — MET (ETH), commission-only, against an ETH premium point estimate of 119.052 bps and CI lower bound 38.012 bps:

    | band | median | p90 | central bps | pessimistic bps | central < premium point? | 2 × pess vs CI lower |
    |---|---|---|---|---|---|---|
    | 0.05 | 17 | 22 | 170.996 | 211.709 | no | fails 11.14× |
    | 0.10 *(registered)* | 11 | 16 | 122.140 | 162.853 | no | fails 8.57× |
    | 0.20 *(registered sweep)* | 5 | 9 | 73.284 | 105.855 | **yes** | fails 5.57× |
    | **0.25 (4 contracts — finest executable at the sleeve maximum)** | 4 | 7 | **65.141** | 89.569 | **yes** | fails 4.71× |
    | **0.50 (2 contracts)** | 1 | 3 | **40.713** | 56.999 | **yes** | fails 3.00× |
    | **1.00 (1 contract)** | 0 | 1 | **32.571** | 40.713 | **yes** | fails 2.14× |

  - At **every** hedging granularity the venue can actually execute at the registered $1,000 sleeve, the commission-only cost (32.6–65.1 bps central) is **between one third and one half** of the ETH premium point estimate of 119.05 bps.
  - MBT is unaffected in direction: it passes the 2.0× margin at every band from 0.05 to 1.00 (2 × pessimistic ranges 54.400 → 10.880 bps against a CI lower bound of 142.740 bps).
- **What would resolve it:** Record the minimum **order** increment that REGISTRATION.md:208 required (1 contract on MET and MBT), and either (a) re-run the registered rule at the coarsest band the sleeve can execute and restate the MET cost table, or (b) state explicitly that the ±0.10 rule is a notional-scale abstraction that no $1,000 sleeve could run, and that the MET cost is therefore not the cost of any executable sleeve.
- **Confidence:** HIGH on the arithmetic and the granularity fact (the contract size, the sleeve ratio and the delta units are all the repository's own published figures, and the re-implementation reproduces its published outputs); MEDIUM on the practical claim that an operator would in fact hedge at the coarse band rather than not hedge at all.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA. The raw-series read is unanchored, but the recomputation reproduces the anchored JSON's published statistics exactly, which establishes the files are the ones the anchored run used.
- **Disclosed by authors?:** no — the repository discloses that the rebalance count is "a rule, not an observed path" (VRPExperiment/REGISTRATION.md:330-332) and that "No fill was modelled" (VRPExperiment/docs/ARTIFACT.md:248), but nowhere observes that the registered band is finer than the smallest position the venue sells, nor that the required "minimum order increment" was not recorded.

---

### DRAFT-all-3
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the `Absent(not_served)` closure on the MET/MBT option and hedge bid-ask legs — two of the three legs that make HARVESTABLE structurally unfireable
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**No public source serves CME MET or MBT option quotes without an account.**" — VRPExperiment/docs/COSTS.md:127 (restated at VRPExperiment/docs/ARTIFACT.md:183 "No public source serves CME crypto option quotes without an account.")
- **Evidence:** the universal claim rests on **four probes, one URL each** (VRPExperiment/docs/COSTS.md:121-125), and **not one of them is an authentication or entitlement refusal**:
  - **Yahoo Finance.** The recorded payload is the repository's own verbatim evidence against its conclusion: "`query1.finance.yahoo.com/v7/finance/options/BTC=F` → **HTTP 401**, verbatim: `{"finance":{"result":null,"error":{"code":"Unauthorized","description":"Invalid Crumb"}}}`" — VRPExperiment/docs/COSTS.md:125. An "Invalid Crumb" is a missing per-session CSRF token, not an absent account. Separately, the symbol probed, `BTC=F`, is the **full-size CME bitcoin future**, not MET and not MBT — so this probe did not request the chain the conclusion is about.
  - **IBKR.** "`index.php?f=quote&symbol=MBT` → **HTTP 200 serving a "404 Page Not Found" body**, 17,301 bytes" — VRPExperiment/docs/COSTS.md:123. A 404 body at HTTP 200 is a wrong URL, not a paywall.
  - **Barchart.** "`barchart.com/futures/quotes/MET*0/options` → **HTTP 404**, 535,327 bytes" — VRPExperiment/docs/COSTS.md:124. A 404 on one guessed continuous-contract symbol, not retried with any other root or expiry-coded symbol.
  - **CME.** "**Not attempted for quotes.**" — VRPExperiment/docs/COSTS.md:122.
  - **The repository applies the correct standard elsewhere and not here.** For Volmex it wrote: "two candidate paths … both returned `{"name":"NotFoundError","code":404}`. The endpoint was **not located**, which is recorded as *not located* and **not** as *does not exist* — the difference matters and this repository did not establish the stronger claim" (VRPExperiment/docs/ACCESS.md:209-212; VRPExperiment/progress.md:555-556). Four 404/CSRF responses on CME option chains were converted into the stronger claim the Volmex note refuses to make.
  - This matters to the closure, not only to hygiene: it is one of the two `Absent` legs that make "HARVESTABLE cannot fire, and the reason is structural rather than arithmetic" (VRPExperiment/HYPOTHESES.md:42-49), and one of the two figures the open MBT route is said to turn on (VRPExperiment/docs/HANDOVER.md:24).
- **Recomputation (if any):** none — this is a document-internal finding. Count of probes supporting the universal claim: 4 (VRPExperiment/docs/COSTS.md:121-125); count that are authentication refusals: 0; count that requested an MET or MBT option chain: at most 2 (IBKR `symbol=MBT`, Barchart `MET*0`), both returning "not found" bodies.
- **What would resolve it:** Downgrade the claim to the Volmex standard ("not located"), or probe with verified symbol roots (e.g. Barchart's expiry-coded MET/MBT option symbols, Yahoo's options endpoint with a crumb obtained from its own cookie handshake, CME's delayed-quote pages retrieved by a means the Data Terms of Use permit) and record whatever those return.
- **Confidence:** HIGH that the stated evidence does not support the universal claim; MEDIUM that a public source in fact exists.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** no — the authors disclose that the leg is absent and why they did not substitute for it, but they do not disclose that the four probes are "not found" and "no CSRF token" rather than "account required", and they state the universal claim without qualification.

---

### DRAFT-all-4
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the registered reopen condition on the one open route (CME MBT options via IBKR Canada), and the CME exchange-and-regulatory-fee blocker
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Both are obtainable in one session by an operator with an IBKR Canada account, and by nobody without one.**" — VRPExperiment/HYPOTHESES.md:26 (restated at VRPExperiment/docs/HANDOVER.md:19 "Both are visible in an IBKR Canada client portal in a single session; neither is obtainable without an account", at VRPExperiment/docs/ARTIFACT.md:233-234, and at VRPExperiment/docs/HANDOVER.md:61-62 "**Not obtainable without an account**")
- **Evidence:**
  - The CME refusal the blocker rests on is an **IP-level anti-scraping block on a public, no-account endpoint**, and its own text names an alternative delivery route that was never tried. Verbatim, recorded by the repository itself: "`{"message": "This IP address is blocked due to suspected web scraping activity … If you are attempting to access data or content from the website via automated means or for commercial purposes, **CME has numerous other methods to deliver the content you require. Please contact CME Group's Global Command Center (GCC) at gcc@cmegroup.com** and your inquiry will be directed to the appropriate team."}`" — VRPExperiment/reports/task3/robots_and_terms.md:26. The endpoint blocked, `https://www.cmegroup.com/CmeWS/mvc/Margins/Outrights?exchange=CME&pageNumber=1` (VRPExperiment/reports/task3/robots_and_terms.md:20-21), requires **no account**; what it refused was an automated agent, not an unauthenticated one.
  - The repository's list of "What was NOT done, stated explicitly" (VRPExperiment/reports/task3/robots_and_terms.md:35-37) enumerates user-agent rotation, proxies, retry loops and third-party mirrors. **Contacting the address CME's own refusal supplies is not on the list, and is neither a workaround nor a terms violation** — it is the route the rights-holder offered. It costs nothing, which satisfies the standing "Spend nothing" rule (VRPExperiment/progress.md:33).
  - The repository separately records, in its own words, a figure from a sibling repository that **bounds the absent exchange-fee leg for the hedge instrument without any account**: "MLCryptoEngine's round turns (**$4.04** for MBT, **$1.94** for MET) are larger than IBKR Canada's commission alone (**$1.70** and **$0.40**). The most likely reason is that the recorded figures are **all-in**, including CME exchange and regulatory fees" — VRPExperiment/docs/VENUE_TABLE_UPDATE.md:91-96. The MBT residual is a **futures** round turn, which is exactly the instrument the delta hedge trades (VRPExperiment/docs/COSTS.md:175).
  - The blocker is load-bearing: it is the stated reason the repository's own qualification says "MBT is not shown to fail — it is shown to be **unmeasurable from outside a brokerage account**" (VRPExperiment/HYPOTHESES.md:78-80).
- **Recomputation (if any):**
  - Inputs: MBT all-in round turn USD 4.04 and IBKR MBT commission USD 0.85/contract (VRPExperiment/docs/VENUE_TABLE_UPDATE.md:91-96, VRPExperiment/docs/COSTS.md:42); MBT notional USD 7,812.46 (VRPExperiment/reports/task3/venue_table.md:64); p90 rebalance count 16 at the registered band (VRPExperiment/reports/task6/real_attempt2_result.json, BTC band 0.1); reopen budget 49.61 bps (VRPExperiment/docs/HANDOVER.md:24).
  - Method: implied exchange+regulatory fee per fill = `(4.04 − 2 × 0.85) / 2 = $1.17`; in bps of notional = `1.17 / 7812.46 × 1e4 = 1.498 bps`; hedge leg at the pessimistic count = `16 × 1.498 = 23.96 bps`.
  - Result: the futures-side exchange-and-regulatory leg plausibly consumes **≈ 24 of the 49.61 bps** the open route has to spend, leaving ≈ 25.6 bps for the option-side fee plus all bid-ask — against a measured (reference-only) Deribit BTC straddle round-trip quoted spread of **22.50 bps** (VRPExperiment/docs/COSTS.md:253). **This is a bound built from figures already in the repository, not a substitution and not a settlement** — but it demonstrates the leg is not "obtainable by nobody without an account", which is what the reopen condition asserts.
- **What would resolve it:** Restate the reopen condition as "obtainable in one session by an account holder, and obtainable by other named routes that this repository chose not to pursue (CME's own GCC delivery channel; a bound derived from an all-in round turn already recorded in this programme)"; or try the GCC route and record what it returns.
- **Confidence:** HIGH that the "by nobody without one" claim is contradicted by the repository's own verbatim evidence; MEDIUM that the derived bound is the right magnitude (the all-in attribution is the repository's own hypothesis, flagged as "most likely", not an established decomposition).
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** partially — the refusal text is quoted in full at VRPExperiment/reports/task3/robots_and_terms.md:26 and the sibling round turns at VRPExperiment/docs/VENUE_TABLE_UPDATE.md:91-96, so the evidence is disclosed; the **conclusion drawn from it** ("by nobody without one") is not qualified anywhere, and the GCC route is not mentioned in any of the four documents that state the blocker.

---

### DRAFT-all-5
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** Section 3.3's candidate venue set, and the VENUE_BLOCKED leg "no lawfully reachable venue clears the cost hurdle at the sleeve size"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "| Canadian-listed covered-call crypto ETFs (BTCY, ETHY, BCCL) | TSX fund units | permitted | **NOT AN OPTION PRODUCT** — the buyer holds a fund, not an option." — VRPExperiment/docs/ARTIFACT.md:119 (criterion at VRPExperiment/reports/task3/venue_table.md:28 "These are packaged funds that write calls internally. The resident buys a unit, not an option.")
- **Evidence:**
  - The census tested whether **the fund unit** is an option. It never asked whether **exchange-listed options on those funds** exist. Those are two different products, and only the second is what registered criterion 3.1(2) asks for: "The venue lists an **option product** on BTC or ETH" (VRPExperiment/REGISTRATION.md:189).
  - The registration expressly permits the extension: "The set may be **extended** by TASK 3 if a candidate is found. It may not be **narrowed**." — VRPExperiment/REGISTRATION.md:222-223. The registered set (VRPExperiment/REGISTRATION.md:213-220) contains Deribit, CME micros via IBKR Canada, CME full-size, Canadian covered-call/volatility crypto **ETFs**, CIRO-registered Canadian venues, and Hyperliquid. **Listed options on a bitcoin or ether ETF appear nowhere**, on any exchange, in any document in this repository — a grep for `montreal`, `bourse`, `TMX`, `BTCC`, `listed option`, `equity option` across all markdown returns only IBKR Canada's registered-office address.
  - The omission is not neutral to the verdict, it is adjacent to its central tension. The closure turns on there being no contract between MET's **$245.62** and MBT's **$7,812.46** notional: "**MET is the only route that is unambiguously capital-feasible at $1,000, and it is the expensive one**" (VRPExperiment/docs/COSTS.md:104-105); "the only contract small enough for a $1,000 sleeve to certainly hold is the one whose commission exceeds the premium it would harvest" (VRPExperiment/DECISIONS.md:232-233). A listed equity option is 100 shares of its underlying ETF, which for the crypto ETFs in circulation lands squarely inside that gap.
  - Two further properties of the omitted class bear directly on the two blockers this repository could not clear: listed equity-option quotes are **publicly disseminated without an account** (relieving the `Absent` bid-ask leg of DRAFT-all-3), and equity-option margin is **published by the listing exchange and by CIRO/OCC schedules** rather than sitting behind a client portal (relieving the margin blocker of DRAFT-all-4).
  - This is a lead to be verified, not a measurement: this audit did not make a network call and does not assert what any specific ETF's option chain contains. What is established here is that **the question was not asked and no `Absent` was recorded for it**, in a census whose registration explicitly instructed extension when a candidate is found.
- **Recomputation (if any):** none. Gap arithmetic quoted from the repository: MET notional $245.62, MBT notional $7,812.46, ratio 31.8× (VRPExperiment/docs/COSTS.md:101-102); sleeve $1,000.
- **What would resolve it:** Extend the TASK 3 table by one row per candidate — listed options on Canadian-listed crypto ETFs (Bourse de Montréal) and on US-listed spot-bitcoin ETFs reachable through the same IBKR Canada account the census established is permissioned — classify each PERMITTED / NO_PRODUCT / CAPITAL_BLOCKED / UNCLEAR on published text with its date, and record `Absent` with a reason if the answer cannot be obtained.
- **Confidence:** MEDIUM — the omission from the candidate set is certain and documented; whether an admissible option product exists in that class, and at what notional and cost, is not established by this audit.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** no — the ETF row is disposed of on the fund-unit test alone, and no document records the option-on-ETF question as asked, answered, or absent.

---

### DRAFT-all-6
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the BTC premium "decay" finding, and the instruction it generates against relying on the measured premium
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**BTC is significant in every quarter but decaying monotonically — down 60.4% across the sample.** A reader planning around this should assume the decay continues rather than that the average persists." — VRPExperiment/docs/ARTIFACT.md:96-98 (imperative form at VRPExperiment/docs/HANDOVER.md:82-83: "**Do not read the BTC premium as stationary.** It decays monotonically across the sample, **284.53 → 250.59 → 145.13 → 112.72 bps**, a 60.4% fall.")
- **Evidence:**
  - The four quarterly BTC means and their t statistics are published with n: 284.53 (t 3.498, n 488), 250.587 (t 3.845, n 488), 145.132 (t 2.619, n 488), 112.719 (t 2.098, n 491) — VRPExperiment/reports/task6/real_attempt2_result.json (`BTC.stability_quarters`); same figures at VRPExperiment/docs/ARTIFACT.md:91-94 and VRPExperiment/progress.md:741-744.
  - No test of the decay is performed anywhere in the repository. The claim rests on the ordering of four point estimates and on their ratio.
  - A heterogeneity test on those same four numbers does **not** reject a constant BTC premium.
- **Recomputation (if any):**
  - Inputs: the four (mean, t) pairs above, from VRPExperiment/reports/task6/real_attempt2_result.json; standard errors backed out as `SE = mean / t` → 0.035559, 0.028491, 0.024226, 0.023488 vol points. Script: `/tmp/claude-1000/.../scratchpad/work/agentA-VRP/quarters.py`.
  - Method: Cochran's Q with inverse-variance weights, 3 df; and a two-sample z on the Q1−Q4 difference.
  - Result: **Q = 4.784 on 3 df, p = 0.188** — the four quarterly BTC means are not distinguishable from a common mean. Q1 − Q4 = 0.075110 vol points = **171.8 bps, SE 97.5 bps, z = 1.762, two-sided p = 0.078** (one-sided p = 0.039). Monotone ordering of four exchangeable draws has probability 1/24 = 4.2%, so the *pattern* is suggestive; the *magnitudes* are inside noise.
  - For contrast, the same test on ETH — where the repository draws the same kind of conclusion — **does** reject homogeneity: **Q = 9.789 on 3 df, p = 0.020**. The repository's ETH instability conclusion survives a proper test; its BTC decay conclusion does not.
- **What would resolve it:** Run and report a heterogeneity or trend test on the quarterly means, and downgrade "assume the decay continues" to "the point estimates decline monotonically; a formal test on the same four numbers does not reject a constant premium (Q = 4.78, 3 df, p = 0.19), so the decline is suggestive and not established."
- **Confidence:** HIGH on the arithmetic (inputs are the repository's own published means and t statistics); MEDIUM on the framing, because the four quarters are contiguous blocks of an overlapping-window series and the implied HAC standard errors are treated as independent across blocks, which is approximate at the block boundaries.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** no — the decay is presented as a finding and converted into an instruction to a successor ("Do not read the BTC premium as stationary"), with no statement that it is not statistically established.

---

### DRAFT-all-7
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the p90 ("pessimistic") half-spread statistic that the registered 2.0× margin is applied to, and the sampling recipe handed to the operator to settle the open route
- **Direction:** A
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Sampling instructions are already registered and need no further decisions:** Section 4.1 (≥ 20 distinct observation windows on the ATM 30-day series, median and 90th percentile with `n`), Section 4.2 (central = median, pessimistic = p90, assignment fixed before anything downstream), Section 4.3 (±0.10 delta band evaluated daily, swept at ±0.05 and ±0.20)." — VRPExperiment/docs/HANDOVER.md:33-37
- **Evidence:**
  - Section 4.1 registers a count of windows but **no spacing**: "sampled across **at least 20 distinct observation windows**" — VRPExperiment/REGISTRATION.md:255. The spacing was therefore chosen after registration, in the tool: `WINDOWS = 24` and `SPACING_SECONDS = 20.0` — VRPExperiment/tools/measure_spreads.py:36 and :39.
  - As executed, the 24 "distinct observation windows" span **eight minutes of one morning**: first observation `2026-08-30T06:33:34Z`, last `…06:41:34Z` (VRPExperiment/reports/task5/reference_spreads_deribit.json, `observations` timestamps and `finished_at`). A p90 of a spread over eight minutes is not a p90 of the spread a sleeve would pay across a session, a week, or an expiry cycle.
  - The consequence is not confined to the reference measurement. The repository's own margin doctrine puts the entire safety factor on this statistic: "**For HARVESTABLE, the lower bound of the premium's one-sided 95% confidence interval must exceed the PESSIMISTIC end of the all-in round-trip cost by a factor of 2.0**" (VRPExperiment/REGISTRATION.md:312-314), with pessimistic defined as the 90th-percentile half-spread (VRPExperiment/REGISTRATION.md:274). The operator is then told this design "need[s] no further decisions" — so the one figure that would settle the open MBT route would, followed literally, be an eight-minute p90.
  - The repository partly recognises the exposure and argues it away for the reference case only: "a 24-window sample of a tick-bound quantity is a much better estimate of its central tendency than 24 windows of a freely-moving one" (VRPExperiment/docs/COSTS.md:239-241). That argument is about **central tendency on a tick-bound book** and does not transfer to a p90 on MET/MBT, whose tick structure and book are exactly what is unmeasured.
- **Recomputation (if any):** window span computed from the recorded timestamps: 24 windows × 20.0 s spacing = 460 s ≈ 7 min 40 s of elapsed sampling, consistent with `at` = 06:33:34Z (window 1) through `finished_at` = 06:41:34Z (VRPExperiment/reports/task5/reference_spreads_deribit.json).
- **What would resolve it:** Amend the handover instruction to specify the spacing and the calendar span of the ≥ 20 windows (e.g. spread over ≥ 5 trading sessions and across the session's open, midday and close), since the p90 is the statistic the 2.0× margin is applied to.
- **Confidence:** HIGH that the sampling spans eight minutes and that the spacing was not registered; MEDIUM on the practical size of the distortion, which is unmeasured here.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** partially — the 20-second spacing is published in the tool and in the JSON, and COSTS.md:229-241 argues the sample is stable **for the tick-bound reference book**; the repository does not disclose that the p90 handed to the operator as needing "no further decisions" is an intra-eight-minute statistic.

---

### DRAFT-all-8
- **Repository / SHA:** VRPExperiment / d37cf6d190dfdaef8e613daf099a507fe1a77dcf
- **Hypothesis or artifact:** the 49.61 bps reopen threshold on the open MBT route
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **All-in MBT option + futures bid-ask, plus CME exchange and regulatory fees**, at the pessimistic (90th-percentile) end | **≤ 49.61 bps of notional** | The room between the BTC premium's one-sided 95% lower bound (142.740 bps) and twice the measured commission-only pessimistic cost (2 × 21.760 = 43.520 bps) |" — VRPExperiment/docs/HANDOVER.md:24 (same description at VRPExperiment/docs/ARTIFACT.md:229-231 and VRPExperiment/HYPOTHESES.md:26 "which is the room left between the BTC premium's CI lower bound and twice the measured commission")
- **Evidence:** the stated description and the stated number are different quantities. "The room between 142.740 and 43.520" is **99.220 bps**. The figure actually used, 49.61 bps, is `142.740 / 2 − 21.760`, i.e. the room in *cost* space once the registered rule `premium_CI_lower ≥ 2.0 × cost_pessimistic` (VRPExperiment/REGISTRATION.md:316) is inverted. The **number is right and the sentence explaining it is wrong**, in all three places the threshold is published; an operator applying the description as written would carry a budget exactly 2× too large and could report the route as clearing when it does not.
- **Recomputation (if any):** `142.740 − 43.520 = 99.220`; `142.740 / 2 − 21.760 = 49.610`. Inputs: BTC CI lower 142.7401 bps and MBT pessimistic commission 21.760 bps (VRPExperiment/reports/task6/real_attempt2_result.json; VRPExperiment/progress.md:783). Script: `/tmp/claude-1000/.../scratchpad/work/agentA-VRP/recompute.py`.
- **What would resolve it:** Restate as "half the BTC premium's CI lower bound (71.370 bps) less the measured pessimistic commission (21.760 bps) = 49.610 bps".
- **Confidence:** HIGH — one subtraction, on two figures the repository publishes.
- **Invalidated by later commits?:** no — live HEAD equals the anchored SHA.
- **Disclosed by authors?:** no.

---

## What I checked and found sound

Read completely: `README.md`, `REGISTRATION.md` (all 589 lines incl. Amendment 1), `HYPOTHESES.md`, `DECISIONS.md` (ADR-001…011), `progress.md` (all 861 lines), `docs/ARTIFACT.md`, `docs/ACCESS.md`, `docs/COSTS.md`, `docs/DUPLICATION.md`, `docs/HANDOVER.md`, `docs/VENUE_TABLE_UPDATE.md`, `reports/task3/{venue_table,robots_and_terms,deribit_restricted_jurisdictions_verbatim}.md`, all six `reports/task{4,5,6}/*.json` and `reports/env_report.json`, and the relevant parts of `src/vrp/sealed_read.py`, `tools/task6_sealed_run.py`, `tools/measure_spreads.py`.

Where the Direction-A thesis did **not** hold:

1. **The Deribit PROHIBITED closure is airtight.** The policy's own `<time datetime="2026-03-19T16:49:36Z">` stamp is recorded verbatim, the retrieval date is recorded, "Canada" is listed bare, and the five qualified entries are enumerated to show the contrast — `reports/task3/deribit_restricted_jurisdictions_verbatim.md:5,23-48,52-66`. There is no unexplored reading of the text and the repository correctly refuses to work around it.
2. **The premium measurement reproduces exactly.** My independent re-implementation of the registered estimators over the repository's own raw series returns BTC mean 0.086607 vol points (198.111 bps) and ETH 0.052045 (119.052 bps) at n = 1,955 each — identical to `reports/task6/real_attempt2_result.json`. The realized leg is genuinely forward-looking, `ddof=1`, `√365`, as registered (`src/vrp/sealed_read.py:54-74`, `REGISTRATION.md:104-122`).
3. **The HAC choice is registered before data and is the conservative one.** Newey-West bandwidth 30 on overlapping 30-day windows, registered at `REGISTRATION.md:366-371` with the ORB audit-A3 precedent named, and a test asserting the IID SE would have been narrower (`progress.md:689-691`). The non-overlapping robustness check agrees in sign and significance on both assets (n = 66), so no suppressed disagreement.
4. **The ETH instability conclusion survives a better test than the one used.** The repository's stated rationale — "Only one of four quarters is individually significant and one is negative" (`HYPOTHESES.md:23`) — is *not* diagnostic on its own: at the measured per-quarter dispersion, a perfectly homogeneous ETH premium equal to the full-sample mean would yield an expected 1.70 significant quarters, and P(at most 1 of 4) = 0.428. But Cochran's Q on the same four numbers gives **Q = 9.789, 3 df, p = 0.020**, which does reject homogeneity. The conclusion is right; only the argument offered for it is weak. No finding raised.
5. **The MBT open route's classification is robust to the hedging band.** At every band from ±0.05 to ±1.00 the BTC CI lower bound of 142.740 bps exceeds twice the MBT pessimistic commission (54.400 → 10.880 bps). The "passes by 3.28× on commission alone, at any rebalance count up to the daily maximum of 29" claim checks out: 4.352 + 29 × 1.088 = 35.904 bps, 2× = 71.808 ≤ 142.740.
6. **The `Absent` discipline is real, not decorative.** `Absent` refuses `float()`, `int()`, indexing and every arithmetic path (`src/vrp/absence.py`), the blind/readable field registries are asserted disjoint at import (`DECISIONS.md:17-21`), and the deferral of the rebalance count to TASK 6 because `d₁` needs a blind σ (ADR-006, `DECISIONS.md:114-129`) is a genuine structural consequence rather than an excuse.
7. **Amendment 1 is exemplary.** The aborted first latch is kept, the second is separately named, the diff between attempts is a single string literal, and the four checkable facts establishing no outcome was observed are stated as things a reader can verify (`REGISTRATION.md:535-589`; both latches present in `reports/task6/`). `real_result.json` is indeed absent from the tree, as claimed.
8. **The revision question was answered correctly, including the false positive.** ADR-009's point that the JSON-RPC envelope's `usIn`/`usOut`/`usDiff` change every call, and that the comparison must be on the canonicalised `result.data`, is right; `reports/task4/revision_recheck.json` shows `all_identical: true` on all six windows across ≈70 minutes, and the CDD re-check is explicitly labelled a weak test.
9. **The conversion constant is registered before data and computes correctly.** `√(2/π)·√(30/365)·10⁴ = 2287.46` bps per unit decimal vol = 22.875 bps per vol point (`REGISTRATION.md:152-173`, `src/vrp/sealed_read.py:43-51`), with its three limitations stated in advance rather than discovered.
10. **The commission tier chosen is the right one.** `reports/task5/ibkr_ca_commissions.json` shows cheaper tiers at >1,000 contracts/month; a $1,000 sleeve trading ~15-60 contracts a month cannot reach them, so the lowest tier is correct and not a conservative flourish.
11. **The duplication screen is honest work.** The two-pass `grep -w` correction (raw 4,154 VRP hits in solattn → 0 word-boundary) and the line-by-line reading of `realized volatility` and `straddle` are the right method, and the three named closures are distinguished on mechanism rather than asserted CLEAR.
12. **A figure that cuts the other way, recorded for completeness rather than as a Direction-A finding.** The open MBT route is justified against the *full-sample* BTC CI lower bound of 142.740 bps. On the most recent quarter alone (2025-03-27 → 2026-07-30, n = 491, mean 112.719 bps, t 2.098 → SE 53.73 bps), the one-sided 95% lower bound is **24.34 bps**, which is **below** 2 × 21.760 = 43.520 bps. On current-regime data the open route would not clear its own hurdle even on commission alone. This is an over-claim in the *opposite* direction to this agent's thesis and is flagged here rather than written up as a Direction-A finding.

## Live-repo access log

Read-only access to `/home/kiros-li/Documents/GitHub/VRPExperiment` was used for (i) `git log`/`rev-parse` provenance and (ii) reading the untracked, gitignored `data/raw/task6/*.json` series for DRAFT-all-2. No write, checkout, stash, reset or script execution occurred in the repository; the recomputation ran from a copy in the audit scratchpad.

BEFORE — `git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`:

```
(empty output — clean working tree)
```

AFTER — `git -C /home/kiros-li/Documents/GitHub/VRPExperiment status --porcelain`:

```
(empty output — clean working tree)
```

`git rev-parse HEAD` → `d37cf6d190dfdaef8e613daf099a507fe1a77dcf`, identical to the anchored SHA; `git log d37cf6d..HEAD` is empty.

**One entry reported for completeness, not dirt caused by this audit.** The working tree contains an untracked file `_CLOSED_DO_NOT_RUN_HERE` (dated 2026-09-02, i.e. after the anchor) which does not appear in `status --porcelain` because it is excluded via `.git/info/exclude:7`. Its content is a self-describing marker: "THIS REPOSITORY IS CLOSED. DO NOT RUN A CODING SESSION HERE. … Marker written 2026-09-02 after a session was opened here by mistake." It was read, not modified.

**Unanchored reads (working tree only, may have changed since the anchor):** `data/raw/task6/dvol_BTC_daily.json`, `data/raw/task6/dvol_ETH_daily.json`, `data/raw/task6/underlying_BTC_daily.json`, `data/raw/task6/underlying_ETH_daily.json`, read 2026-09-03 (this session, UTC date). Their consistency with the anchor is evidenced by the fact that the re-implementation reproduces the anchored `reports/task6/real_attempt2_result.json` statistics exactly.
