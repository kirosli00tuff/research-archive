# AGENT A — CROSS-REPOSITORY PASS

Agent A (direction A: closed too early). Cross-repository reader over all thirteen per-repository ledgers
(`findings/agentA/*.reopen.md`), all thirteen findings files (`findings/agentA/*.md`) and the accumulated lead
list `provenance/launch-args/agentA-leads.json` (136 leads). Written 2026-09-12.

**Method.** For every stated blocker and registered reopen condition in every ledger I asked whether a
*different* repository's later, dated work concretely meets it, reading both sides in the anchored snapshots
(`SNAP/<repo>`, paths and lines identical to `git show <SHA>:<path>`). Git history was read from the live
repositories with `log`, `blame`, `reflog` and `remote -v` only; two untracked live files were read
(recorded below, unanchored). Nothing under any audited repository was written. All recomputations are in
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-crossrepo/`.

**Result in one paragraph.** Seven findings, none above S3. The programme's cross-repository record is mostly
sound: carried figures (the 15.8–50.0 bp spread band, the 27.99 bp/day H-F figures, IBKR error 10243, the Kraken
and Hyperliquid fee tiers, NPD's 0.0512 and Insider's 49.35) trace to their sources and none has moved at its
source's anchor. The failures are of one shape: a repository states a blocker or a sibling's status as a fact
about the world, and a sibling's dated record says otherwise — solclear's reopening population exists in solattn;
AiTrader's "no shares outstanding" has a verified free route in InsiderExperiment; VRPExperiment's "obtainable by
nobody without an account" CME fee leg was obtained keylessly by MLCryptoEngine; ORBExperiment's two DUPLICATE
culls were already stale when written and its absent SEC Section 31 effective date sits in HFExperiment; and
NPDExperiment records two AiTrader layers as "measured to nothing" that AiTrader records as never measured. One
cross-repository fact cuts against an existing Agent A finding (MLCryptoEngine-8) and is recorded plainly in its
own section. The binding family-separation constraint in solattn (REGISTRATION.md:396-400) was honoured: nothing
below pools solattn's null with AiTrader's news-drift experiment.

Categories used, per the task: **(a)** trigger met, closure not revisited → a finding; **(b)** trigger met and
the repository noticed → "Triggers met and already handled"; **(c)** partially met → "Partial".

---

## Findings

### AUDIT-A-solclear-11

- **Repository / anchored SHA:** solclear / `d2985769229ad40a3f02f0fe5a2fe0ad4fca295f` (main, 2026-08-22)
- **Hypothesis or artifact:** ADR-015 / progress.md "What would reopen the outcome question" / README "Status:
  closed (re-closed 2026-08-22)" — the project-level closure of "does a cleared basket beat holding SOL", whose
  sole registered reopening condition is a population, and the Stage G re-closure and 2026-09-02 closure marker
  that never evaluated the sibling repository holding that population.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S3 · **Label:** READ
- **Claim challenged (verbatim):** "**The reopening condition, stated so it is not mistaken for pessimism.** The
  outcome question reopens on a **genuinely different population** — graduated or AMM pools carrying real
  liquidity, enumerated without survivorship bias — **not on a different model**." — solclear/DECISIONS.md:534-537
  (same text at solclear/progress.md:548-551, README.md:236-240, CLAUDE.md:134-137). And the scope statement of
  the re-closing stage: "MLCryptoEngine is **read-only** for the whole stage; solattn is not touched." —
  solclear/progress.md:253.
- **Evidence.**
  - *The trigger, as solclear states it.* Beyond the sentence above, solclear's own feasibility note declares the
    forward route open: "**Forward, on a live cleared cohort: feasible.** A pool cleared today has its launch
    inside any plausible retention window, so the same free daily candles cover launch→+90 d" —
    solclear/progress.md:1490-1492. The Stage E cohort that fired the closure was **77 pools against a
    registered target of 300** with "keyless enumeration sources were exhausted" — solclear/FINDINGS.md:102-103;
    its only graduated pools are **16** attention-crawled coins (FINDINGS.md:98-100).
  - *The population, in solattn (dated after ADR-015 of 2026-08-14).* solattn's registered universe rule: "Take
    **every new Solana AMM pool at the moment of its birth**, in birth order, from a keyless public new-pools
    feed, with **no attention input of any kind in the enumeration**" — solattn/README.md:19-21; primary universe
    is the `amm` subset under a denylist of bonding-curve venues — solattn/REGISTRATION.md:80-88. Size: "n =
    12,798 amm pools over the three birth days 2026-08-16..18; 2,107 measurable at the registered `d0+2` entry
    anchor" — solattn/README.md:40-42; 70,894 `amm` pools enumerated over the 13 sealed birth days (sum of
    `enumeration.amm` in solattn/docs/digests/2026-08-16.json … 2026-08-28.json; e.g. 5,907 on 2026-08-17,
    docs/digests/2026-08-17.json:5). Forward outcomes at h = 1, 3, 7 days on the 2,107 measurable pools, with
    the birth-ordered death rate at 7 days measured at **78.8 %** (README.md:107-108). The enumeration source is
    keyless and free — solattn/docs/ACCESS.md:12. "Collection ran **2026-08-16 to 2026-08-29** and is stopped and
    disabled." — solattn/README.md:152.
  - *Timeline.* ADR-015 2026-08-14 → solattn registration and first cohort 2026-08-16 → solclear Stage G
    re-closes 2026-08-22 with "solattn is not touched" (progress.md:253) → solattn's Stage B readout 2026-08-29
    (README.md:33-45) → solclear's untracked closure marker, "Marker written 2026-09-02 after a session was opened
    here by mistake" (live `solclear/_CLOSED_DO_NOT_RUN_HERE`, 747 bytes, read 2026-09-12T07:38:00Z, UNANCHORED;
    it does not mention solattn).
  - *What is not attested.* solattn records no liquidity field for a pool (a grep of `solattn/solattn/*.py` for
    `reserve`, `liquidity`, `volume_usd` returns 0 hits) and **83.5 %** of the birth-ordered cohort printed no
    `d0+2` candle at all (README.md:60-61), so the qualifier "carrying real liquidity" is unmeasured; the 2,107
    measurable pools printed candles through the entry anchor. The enumeration half of the condition — the half
    solclear calls "the hard part" that "must come first" (progress.md:550-552) — is met verbatim.
- **Recomputation** (`work/agentA-crossrepo/solclear_cost.py`). Cost of applying solclear's clearance scorer to
  a birth-ordered subsample at solclear's own measured prices — per-pool enhanced cost "typical ≈ 1,400 credits,
  conservative ≈ 2,000" (solclear/DECISIONS.md:265-266, ADR-008) against the account's "measured 1,000,000
  credits per month" (solclear/DECISIONS.md:644): **300 pools = 420,000–600,000 credits = 0.42–0.60 months**;
  all 2,107 measurable pools = 2,949,800–4,214,000 credits = 2.95–4.21 months. The registered Stage E target of
  300 pools (FINDINGS.md:102) is therefore inside one month's allowance on solattn's population.
- **What would resolve it.** A dated entry (in a successor repository reading both across a read-only boundary,
  since the marker forbids sessions in solclear) stating whether solattn's `amm` birth cohort satisfies
  ADR-015's population — and either applying a liquidity filter and the clearance scorer to a ≤ 300-pool
  birth-ordered subsample at the price above, or amending ADR-015 to say why the population does not qualify.
- **Confidence:** MEDIUM — the enumeration half is met verbatim on a sibling's dated record; the "real
  liquidity" qualifier is not attested in solattn; and solattn's outcomes matured after solclear's anchor (the
  first cohort reached h = 7 on 2026-08-23) though before the 2026-09-02 re-affirmation.
- **Could later commits invalidate this?** solclear and solattn HEADs both equal their anchors (verified
  2026-09-04 by the per-repository passes; `git status --porcelain` clean at both my reads, below). A later
  solclear or successor entry evaluating solattn against ADR-015 would resolve, not invalidate, it.
- **Disclosed by the authors?** Partly: solclear names solattn once, as out of scope ("solattn is not touched",
  progress.md:253), and names the forward route as feasible (progress.md:1490-1494). It never states whether
  solattn's population meets ADR-015. Severity capped at S3 accordingly.
- **Other-repo refs:** solattn/README.md:19-21, :40-42, :60-61, :107-108, :152; solattn/REGISTRATION.md:80-88;
  solattn/docs/ACCESS.md:12; solattn/docs/digests/2026-08-17.json:5.
- **Cross-references:** AUDIT-A-solclear-9 (keyless sources "exhausted"), AUDIT-A-solclear-2 (affordability
  variants never priced).

### AUDIT-A-AiTrader-19

- **Repository / anchored SHA:** AiTrader / `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24)
- **Hypothesis or artifact:** News-drift experiment AMENDMENT 2 (the 10.00 USD price floor) — the "what the floor
  removes" analysis answered by an ADV-stratum proxy because market capitalisation "cannot be computed"; and the
  cross-sectional round's pre-code rejections of Size and Turnover as UNTESTABLE for want of shares outstanding.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S3 · **Label:** READ
- **Claim challenged (verbatim):** "**MARKET CAP CANNOT BE COMPUTED. Stated plainly rather than approximated.**
  `analysis_bars.db` holds no shares outstanding and no market capitalisation" — AiTrader/EXPERIMENT.md:858-859
  (same at RETURN.md:655); and the registered redo condition: "**Market cap was not measurable**, so the size
  question is answered by an ADV-stratum proxy. If shares outstanding become available the removal analysis
  should be redone directly." — AiTrader/RETURN.md:688. Also: "| Size | UNTESTABLE. No shares outstanding, so no
  market capitalisation …" and "| Turnover (volume over shares outstanding) | UNTESTABLE. No shares outstanding."
  — AiTrader/RETURN.md:2788-2789.
- **Evidence.** InsiderExperiment ADR-007, dated 2026-08-25 (one day after AiTrader's anchor; AiTrader's last
  session commit is `f819b68`, 2026-07-29): "**The route not taken.** SEC XBRL cover facts give
  `dei:EntityCommonStockSharesOutstanding` free, about 70 quarterly points per issuer, and it was verified
  working." — InsiderExperiment/DECISIONS.md:203-206 (restated at InsiderExperiment/REGISTRATION.md:567-570).
  Insider rejected it for its own design for two stated reasons, both recorded with figures: the symbol-to-CIK
  map `company_tickers.json` "lists only current registrants", carrying the symbol "for only 21 of 25 sampled
  corpus issuers" across a ten-year span, and shares outstanding "are not split-adjusted while the bars carry
  adjustment `all`" — DECISIONS.md:206-212. Both are limitations for a ten-year backtest; neither bites on
  AiTrader's removal analysis, which is a snapshot of the news band at the 2026-07-01 formation (live
  COLLECTION_LOG.md, every run: `formation: 2026-07-01`; anchored COLLECTION_LOG.md:117-277) on current names.
  Insider's universe is the same operator's liquid-500 US-equity universe (InsiderExperiment/REGISTRATION.md:
  303-329), so the route was verified on the same population AiTrader draws from.
- **Recomputation:** none required; the trigger is a data-availability statement.
- **What would resolve it.** A dated AiTrader (or successor) entry recording that a free shares-outstanding
  route exists and was verified in InsiderExperiment on 2026-08-25, then either redoing the AMENDMENT 2 removal
  analysis against actual market capitalisation on the 2026-07-01 formation (current registrants suffice) or
  recording why the 21-of-25 symbol coverage disqualifies it. The Size/Turnover rejections would need the
  survivorship caveat addressed before any ten-year re-run.
- **Confidence:** MEDIUM — the sibling's verification is verbatim and dated; the route carries two disclosed
  limitations that matter for one of the two uses and not the other.
- **Could later commits invalidate this?** Yes: AiTrader is a live repository (the collector appends to
  COLLECTION_LOG.md daily); a session after 2026-08-24 could record the route. InsiderExperiment's HEAD equals its
  anchor.
- **Disclosed by the authors?** No. AiTrader names no SEC route; InsiderExperiment does not cite AiTrader's
  statement.
- **Other-repo refs:** InsiderExperiment/DECISIONS.md:203-212; InsiderExperiment/REGISTRATION.md:567-570,
  :303-329.
- **Cross-references:** AUDIT-A-InsiderExperiment-4 (the same route, plus DERA data sets, as an Insider-side
  lead); AiTrader cross-repo lead 3.

### AUDIT-A-AiTrader-20

- **Repository / anchored SHA:** AiTrader / `705e0ed128b7e184be6c1a23dcd06750c524c525` (main, 2026-08-24)
- **Hypothesis or artifact:** The capacity round's candidate table (2026-07-26) — "Variance or skew risk premia"
  rejected before testing as UNTESTABLE on data availability.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S4 · **Label:** READ
- **Claim challenged (verbatim):** "| Variance or skew risk premia | risk premium | not computable | n/a |
  UNTESTABLE, no options data in analysis_bars.db |" — AiTrader/RETURN.md:3177.
- **Evidence.** VRPExperiment (closed 2026-08-30) obtained the data keylessly and measured the candidate: "**Every
  endpoint this measurement needs is served with no account.**" — VRPExperiment/docs/ACCESS.md:44 (n = 11 probes,
  docs/ACCESS.md:31-42; DVOL history 1,992 days per asset, docs/ACCESS.md:84-113). Result: "**BTC: mean 0.086607
  annualised volatility points = 198.111 bps of notional, n = 1,955 daily observations** … **t = 5.888, one-sided
  p = 2.297 × 10⁻⁹** … **ETH: mean 0.052045 vol points = 119.052 bps, n = 1,955** … **t = 2.418**" —
  VRPExperiment/HYPOTHESES.md:16; non-overlapping robustness at n = 66 windows agrees in sign and significance
  (HYPOTHESES.md:17). VRP's verdict is VENUE_BLOCKED (HYPOTHESES.md:16, status row), i.e. the premium exists
  and is material and harvesting is blocked on venue access at a $1,000 sleeve — a different answer from
  "untestable". VRPExperiment does not cite AiTrader's rejection (a grep of VRPExperiment for `aitrader` finds
  only an ADX regime-detector mention at progress.md:135 and the duplication table at docs/DUPLICATION.md:21,
  :65).
- **Recomputation:** none; the closure was a data-availability statement about `analysis_bars.db`, which remains
  true of that database. Whether the candidate would clear AiTrader's 2,500 USD/yr capacity floor is not
  computable from VRP's $1,000-sleeve figures.
- **What would resolve it.** One line in AiTrader's candidate table (or the programme index) recording that the
  candidate was run as VRPExperiment with the outcome above. No AiTrader verdict changes.
- **Confidence:** HIGH on the facts (both records verbatim and dated); materiality is low, hence S4.
- **Could later commits invalidate this?** Yes, if an AiTrader session records the cross-reference; VRPExperiment
  HEAD equals its anchor.
- **Disclosed by the authors?** No, in either repository.
- **Other-repo refs:** VRPExperiment/HYPOTHESES.md:16-17; VRPExperiment/docs/ACCESS.md:31-46, :84-113.

### AUDIT-A-VRPExperiment-8

- **Repository / anchored SHA:** VRPExperiment / `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` (main, 2026-08-30)
- **Hypothesis or artifact:** H1 (VENUE_BLOCKED, qualified) — the one route left open (CME MBT options via IBKR
  Canada), its reopen figure (2), and the CME exchange-and-regulatory fee leg recorded as `Absent(not_served)`.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S3 · **Label:** READ (recomputation
  DERIVED)
- **Claim challenged (verbatim):** "**Both are obtainable in one session by an operator with an IBKR Canada
  account, and by nobody without one.**" — VRPExperiment/HYPOTHESES.md:26 (same at docs/ARTIFACT.md:233-234,
  docs/HANDOVER.md:18-19); and "**The exchange and regulatory legs are additional, and their magnitudes are CME's
  published schedule — which is `Absent(not_served)` because CME refused automated access citing its own Data
  Terms of Use (TASK 3).**" — VRPExperiment/docs/COSTS.md:60-62.
- **Evidence.** MLCryptoEngine holds the leg, dated, from a public source and without any IBKR account: "Per
  contract PER SIDE, all-in, small non-member account: CME exchange execution + clearing $1.15 MBT non-member
  rate, TradeStation published exchange fee schedule, retrieved 2026-08-02. … NFA regulatory fee $0.02 standard
  per-side rate. Broker commission (IBKR) $0.85 … $2.02 per side = $4.04 round turn." —
  MLCryptoEngine/config/venues.yaml:235-251 (comment block); narrative at MLCryptoEngine/progress.md:1137-1144
  (Stage C.8, 2026-08-02): "its CME exchange fee is **$1.15/side against MES's $0.35** … the exchange component
  rests on a broker's republication because CME's own fee finder is interactive, and CME changed its schedule
  effective **2026-04-01**". MLCryptoEngine flags the figure honestly: "NOT verified directly against
  cmegroup.com" (venues.yaml:259-262). VRPExperiment saw the $4.04 and inferred its composition — "The most
  likely reason is that the recorded figures are **all-in**, including CME exchange and regulatory fees" —
  docs/VENUE_TABLE_UPDATE.md:92-96 — but recorded the leg as not served and the two open figures as obtainable
  "by nobody without" an account. The sibling's record shows the fee leg was obtained keylessly 28 days before
  VRP's closure; only the initial-margin figure (1) has no source anywhere in the programme (MLCryptoEngine's
  venues.yaml MBT block, :205-262, carries no margin row, as VRP's own grep recorded at
  reports/task3/venue_table.md:123-126).
- **Recomputation** (`work/agentA-crossrepo/vrp_fee_leg.py`). Inputs: MBT notional $7,812.46
  (docs/VENUE_TABLE_UPDATE.md:86); commission-only straddle round trip 4 × $0.85 = 4.352 bps and one rebalance fill
  $0.85 = 1.088 bps (docs/COSTS.md:86-96); commission-only totals 16.320 central / 21.760 pessimistic bps and the
  49.61 bps residual budget (HYPOTHESES.md:26). The implied rebalance counts recover exactly: (16.320 − 4.352)/1.088
  = **11.00** central, (21.760 − 4.352)/1.088 = **16.00** pessimistic. Applying MLCryptoEngine's $1.17/side
  exchange + NFA fee (1.498 bps per fill on this notional): hedge fills only, **16.47 bps central / 23.96 bps
  pessimistic**; if the four option fills carry the same per-side fee, **22.46 / 29.95 bps**. Room left of the
  49.61 bps budget for the two bid-ask legs: **33.14 / 25.65 bps** (hedge-only) or **27.15 / 19.66 bps** (full).
  Check: $2.02/side on $7,812.46 = 2.586 bps per fill, 5.171 bps per round turn, against MLCryptoEngine H2's
  5.33 bps at its own ~$7,608 sample notional (progress.md:1139) — consistent.
- **What would resolve it.** A dated VRP (or successor) entry carrying the TradeStation-republished MBT
  exchange + NFA fee as a labelled lower bound for the hedge-leg fee component, restating reopen figure (2) as
  "the two bid-ask legs ≤ ≈ 25.65 bps pessimistic (≈ 19.66 if option fills carry the same fee)", and replacing
  "by nobody without one" with "not obtained here". The option-contract exchange fee, if it differs from the
  futures fee, would need its own retrieval.
- **Confidence:** MEDIUM — the sibling's figure is dated and sourced but is a broker republication that
  MLCryptoEngine itself did not verify against CME, CME changed its schedule inside the range, and the options
  fee may differ from the futures fee; the "by nobody without an account" claim is contradicted regardless.
- **Could later commits invalidate this?** Both HEADs equal their anchors. A VRP amendment carrying the leg would
  resolve it.
- **Disclosed by the authors?** Partly: VRP disclosed that MLCryptoEngine holds an all-in figure and inferred its
  composition (docs/VENUE_TABLE_UPDATE.md:92-107). It did not disclose that the sibling's source is a public
  broker schedule needing no account. Severity S3 accordingly.
- **Other-repo refs:** MLCryptoEngine/config/venues.yaml:205-262; MLCryptoEngine/progress.md:1137-1144;
  MLCryptoEngine/report.md:981.
- **Cross-references:** AUDIT-A-VRPExperiment-3 (the same claim, challenged on the never-tried GCC route);
  VRPExperiment cross-repo leads 1 and 2.

### AUDIT-A-ORBExperiment-18

- **Repository / anchored SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29)
- **Hypothesis or artifact:** HYPOTHESES.md "Closed before opening — the ten candidates culled at registration",
  rows 9 and 10, whose cull reasons are statements about two sibling repositories' current states.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S4 · **Label:** DERIVED
- **Claim challenged (verbatim):** "| 9 | **New Hyperliquid listing drift** | **DUPLICATE.** Closed as H1 in
  **NPLExperiment** on 2026-08-28 — FAIL on the sealed read, **197/312 positive, exact lower bound 0.5707
  against a 0.60 bar**. Its live successors H2, H3, H4 are registered there. **This repository does not re-ask
  it.** |" — ORBExperiment/HYPOTHESES.md:130; "| 10 | **Spot Bitcoin ETF flow** | **DUPLICATE.** Registered and
  running in **ETFExperiment** as H-ETF. **This repository does not re-ask it.** |" — ORBExperiment/HYPOTHESES.md:131.
- **Evidence (git objects, read 2026-09-12T07:39Z).** Both rows were introduced by ORBExperiment commit
  `14d37ea`, 2026-08-28 19:13:02 −0700 = **2026-08-29T02:13:02Z** (`git blame -L 128,131 HYPOTHESES.md`) and are
  unchanged at the anchor after six further HYPOTHESES.md commits through `34a91b3` (2026-08-29 20:43:15 −0700).
  - Row 9: NPLExperiment commit `2b44c59`, 2026-08-27 22:45:38 −0700 = **2026-08-28T05:45:38Z** — "cull fires
    k=1 alpha_h=0.05: H2 DEGRADED, H3 BLOCKED, H4 BLOCKED" — i.e. **20.5 hours before** ORB wrote "live
    successors H2, H3, H4". At NPL's anchor: "Nothing is armed for H3." (NPLExperiment/registrations/H3/
    REGISTRATION.md:157) and "Nothing is armed for H4." (registrations/H4/REGISTRATION.md:205). Only H2 survived
    the cull (registrations/H2/REGISTRATION.md:268). The row's first clause (H1 FAIL, 197/312, lower bound 0.5707)
    is correct — NPLExperiment/REGISTRATION.md:554-565.
  - Row 10: ETFExperiment commit `3f5d629`, 2026-08-28 16:39:33 −0700 = **2026-08-28T23:39:33Z** — "Close H1 at
    untestable-at-achievable-power on the deadline finding" — **2.6 hours before** ORB wrote "Registered and
    running"; the collector was disarmed at `4d11002`, 2026-08-28 19:43:48 −0700 (30 minutes after ORB's row).
    At ETF's anchor: "**CLOSED — untestable-at-achievable-power** · 2026-08-28" — ETFExperiment/HYPOTHESES.md:69.
- **Recomputation:** none; the finding is two timestamp comparisons across three repositories.
- **What would resolve it.** Amend the two rows to the siblings' states with dates: NPL H1 FAIL with H3/H4 BLOCKED
  and H2 the sole armed successor; ETF H1 closed untestable-at-achievable-power on 2026-08-28. Neither changes an
  ORB verdict: the culls rest on "no shared substrate", not on the siblings being live.
- **Confidence:** HIGH — commit clocks in three repositories, the same operator, hours apart.
- **Could later commits invalidate this?** ORBExperiment HEAD equals its anchor (verified 2026-09-04 and at my
  read); an amendment would resolve it.
- **Disclosed by the authors?** No.
- **Other-repo refs:** NPLExperiment commit `2b44c59`; NPLExperiment/registrations/H3/REGISTRATION.md:157;
  NPLExperiment/registrations/H4/REGISTRATION.md:205; ETFExperiment commits `3f5d629`, `4d11002`;
  ETFExperiment/HYPOTHESES.md:69.
- **Cross-references:** ORBExperiment cross-repo lead 5 (which asked exactly this).

### AUDIT-A-ORBExperiment-19

- **Repository / anchored SHA:** ORBExperiment / `f2aa675a80fc06b74979040b3028154d1add5ec0` (main, 2026-08-29)
- **Hypothesis or artifact:** The registered absence `Absent(sec_section_31_effective_date_not_measured)` behind
  the frozen Section 6 cost model, which "refuses 550 of 550 trades" (README.md:223) and was bracketed rather than
  filled by ADR-031.
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S4 · **Label:** READ
- **Claim challenged (verbatim):** "**It was attempted again.** `sec.gov` returned **HTTP 403 "Request Rate
  Threshold Exceeded"** on `n = 2` further attempts, **`n = 4` across two sessions**. The stored IBKR page carries
  the rate and **no effective date anywhere**, so it is not recoverable offline either. **The registered figure is
  `Absent(sec_section_31_effective_date_not_measured)` and it is recorded as such.**" —
  ORBExperiment/progress.md:2679-2683; with "A.2 TASK 2 measured the SEC Section 31 rate at 0.0000206 per dollar
  and **did not measure its effective date**, so the schedule is empty and the model refuses rather than take a
  fee from the wrong year." — ORBExperiment/DECISIONS.md:1078-1080 (ADR-031); README.md:378.
- **Evidence.** HFExperiment, verified 2026-08-23 and anchored 2026-08-28 — five days before ORBExperiment's first
  commit (`840de7c`, 2026-08-28 18:37 −0700) — holds the dated schedule with its primary source: "| SEC Section
  31 | 20.60 USD per million of sale proceeds, effective 2026-04-04 |
  https://www.sec.gov/rules-regulations/fee-rate-advisories/2026-2 and
  https://www.finra.org/rules-guidance/notices/information-notice-20260317 |" — HFExperiment/docs/ACCESS.md:93;
  "SEC Section 31 at 20.60 per million effective 2026-04-04." — HFExperiment/progress.md:203; "# Regulatory
  rates, verified 2026-08-23. … USD 20.60 per million # effective 2026-04-04. SEC_SECTION_31_RATE = 0.0000206" —
  HFExperiment/src/hfexperiment/commission.py:15-18. ORB's measured rate 0.0000206/USD is the same figure; only
  the effective date was absent, and the sibling's entry names the SEC Fee Rate Advisory that ORB's per-repository
  ledger recorded as named by no repository in the programme.
- **Recomputation:** none. Materiality is bounded by ORB itself: ADR-031's bracket neutralises the absence for the
  deciding dispersion figure at 8.43 × 10⁻⁵ relative (ORBExperiment/DECISIONS.md:1067-1130).
- **What would resolve it.** Carry HF's dated entry (20.60/million, effective 2026-04-04, SEC Fee Rate Advisory
  2026-2) into ORB's Section 6 schedule as a dated carried figure, so the frozen model prices the 550 trades it
  currently refuses; or record why a sibling's dated primary-source figure does not qualify.
- **Confidence:** HIGH — both records verbatim, the sibling's dated and sourced, and the rate identical.
- **Could later commits invalidate this?** ORB HEAD equals its anchor; an amendment would resolve it.
- **Disclosed by the authors?** ORB disclosed the absence and its neutralisation (DECISIONS.md:1077-1083); it did
  not disclose that a sibling holds the date. S4.
- **Other-repo refs:** HFExperiment/docs/ACCESS.md:93; HFExperiment/progress.md:203;
  HFExperiment/src/hfexperiment/commission.py:15-18.
- **Cross-references:** AUDIT-A-ORBExperiment-14; ORB cross-repo lead 7.

### AUDIT-A-NPDExperiment-5

- **Repository / anchored SHA:** NPDExperiment / `2d3d0aebf977fb2821ec78c25b370c84ec055920` (main, 2026-08-25)
- **Hypothesis or artifact:** Z.1 closure, "Layer accounting" — the table that records the status of AiTrader's
  four engine layers so that "The closure will otherwise be read as larger than it is."
- **Direction:** A · **Class:** CROSS_REPO_INCONSISTENCY · **Severity:** S4 · **Label:** READ
- **Claim challenged (verbatim):** "| L3 DNN advisory | measured to nothing independently |" and "| L4 whale
  tracking | measured to nothing independently |" — NPDExperiment/REGISTRATION.md:753-754 (repeated at
  NPDExperiment/progress.md:75-80).
- **Evidence.** AiTrader's own record of the same two layers, dated 2026-07-27: "`dnn_advisory` (0.15) served a
  synthetic-trained champion throughout and never passed its real-data promotion gate. `whale_signal` (0.10)
  has never been scored against outcomes at all." — AiTrader/CONTEXT.md:90; "I could not connect `whale_signal`
  to a recorded need beyond "it is advisory and bounded." It has no demonstrated skill" — AiTrader/AUDIT.md:94;
  the whale tables hold 0 rows in both databases (AiTrader/DATA_AUDIT.md:15-28). "Never scored against outcomes"
  and "never passed its real-data promotion gate" are statements that no measurement exists; "measured to nothing
  independently" is a statement that a measurement exists and was null. The NPD table converts two unmeasured
  layers into measured negatives in the programme's cross-repository record — the direction the retail-power-limits
  note and InsiderExperiment's "eight families … zero positives" accounting (InsiderExperiment/progress.md:103-106)
  later lean on.
- **Recomputation:** none.
- **What would resolve it.** Restate the two rows as "never scored against outcomes (AiTrader CONTEXT.md:90);
  deactivated by zero weight, code retained". Nothing in NPD's own verdict turns on the table.
- **Confidence:** HIGH — both texts verbatim.
- **Could later commits invalidate this?** NPD HEAD equals its anchor and the repository carries a 2026-09-02
  closure marker; only a successor entry could restate it.
- **Disclosed by the authors?** No.
- **Other-repo refs:** AiTrader/CONTEXT.md:90; AiTrader/AUDIT.md:94; AiTrader/DATA_AUDIT.md:15-28.
- **Cross-references:** AUDIT-A-AiTrader-2 (the "unmeasurable" inference on `whale_signal`); NPD cross-repo lead
  L4.

---

## Triggers met and already handled (category b), and carried figures verified unchanged

1. **The "measured 15.8 to 50.0 bp consolidated-tape spread band"** (NPDExperiment/REGISTRATION.md:654;
   InsiderExperiment/REGISTRATION.md:406 "One-way spread | 15.8 bp | 50.0 bp"; HFExperiment/REGISTRATION.md:173
   "The inherited 15.8 to 50 bp band"). Source located and verified: AiTrader's tick measurement of 2026-07-29 —
   "Per stratum, ticks median (bp median): S1 7.0 (15.8), S2 8.0 (21.1), S3 6.5 (30.6), S4 12.0 (50.0)" on
   "1,402 rows kept of 1,440 cells over 157 symbols" across sessions 2026-07-24/27/28 (AiTrader/PROGRESS.md:266;
   RETURN.md:249, with p90 63.9/95.1/121.1/211.6). Unchanged at AiTrader's anchor. NPD omits the source; the
   figure is correct. (NPD lead L2.)
2. **HF's inherited effect size** — 27.99 bp/day, TE 66.40 %/yr, IR 1.062 at width 5; 10.04 / 31.70 / 0.798 at
   width 50 (HFExperiment/REGISTRATION.md:113-118). AiTrader's record: holdout excess +27.99 bp/day, 95 % CI
   [−4.9, +60.9], z 1.668 vs bar 2.50, n = 31 holdout months (AiTrader/RETURN.md:2857, :2921 per the AiTrader
   ledger). Unchanged; nothing later in AiTrader re-measures the family. (HF leads L1–L3; rpl lead 6.)
3. **PMExperiment's imported premises**: NPD's realized MDC 0.0512 vs the 0.01–0.05 band after 415 days
   (NPDExperiment/REGISTRATION.md:695-697) and Insider's BLOCKED at 49.35 bp before spend
   (InsiderExperiment/REGISTRATION.md:712) are unchanged at their anchors. PM's uncited n for MLCryptoEngine H2's
   AUC 0.501 is **224,425,675 events / 989 scheduled-open hours / 53 days / one clean walk-forward fold**
   (MLCryptoEngine/HYPOTHESES.md:66-67; report.md:981); H2 was not superseded (its MES and Hyperliquid doors were
   never opened — AUDIT-A-MLCryptoEngine-1, -12). (PM leads X7–X9.)
4. **IBKR error 10243**, carried into ETFExperiment (REGISTRATION.md:269-272), NPLExperiment
   (docs/STAGES.md:74-76; registrations/H5/REGISTRATION.md:199-204) and ORBExperiment (DECISIONS.md:268-270,
   ADR-010): the source measurement stands (HFExperiment/reports/stage_a1b/a1b_report.md:64-70) and ADR-026
   (2026-08-28) reaffirms "The fractional closure stands unchanged. It rested on error 10243 and error 10244
   against an accepted whole-share control, which is measurement" (HFExperiment/DECISIONS.md:459-461). Not
   superseded. (ETF lead 4; NPL lead L4; ORB lead 11 C-17.)
5. **ETF's carried fee tiers.** Kraken 0.25/0.40 verified 2026-08-08 in MLCryptoEngine (HYPOTHESES.md:305); no
   later verification exists. The **undated** Hyperliquid 1.5/4.5 bp per side (ETFExperiment/REGISTRATION.md:
   253-255) has a dated source in the programme: "Hyperliquid perps, base tier | 1.5 bps | **3.0 bps** |
   2026-08-01" (MLCryptoEngine/HYPOTHESES.md:307), also carried at NPLExperiment/REGISTRATION.md:153-154. The
   missing date exists elsewhere; not raised (S4 at most). (ETF leads 5, 6.)
6. **ORB's slippage band** (0.076572 median / 0.333662 p90, n = 550; ORBExperiment/REGISTRATION.md:3975-3980)
   re-verified by VRPExperiment (progress.md:183 per the VRP ledger). Not reopened. (VRP lead 5.)
7. **ORB's other carried house figures**: C-19 MLCryptoEngine H11's 75-day lag (MLCryptoEngine/HYPOTHESES.md:
   182, 185 — itself contested by AUDIT-A-MLCryptoEngine-2); C-20 NPL H1 197/312 (NPLExperiment/REGISTRATION.md:
   554-565); C-21 solattn's 47.5 % refusal share of n = 1,863 (solattn/REGISTRATION.md:1062-1089); C-16 solattn's
   8-of-8 seal mismatch (solattn/progress.md:1443-1512). None moved at its anchor. (ORB lead 11.)
8. **NPL's carried lessons**: solclear Finding 2's 97.5 % vs 18.75 % gap (solclear/FINDINGS.md:122-123), solattn
   ADR-019/ADR-021 pacing and seal discipline, InsiderExperiment ADR-012's AST-guard lesson — all unchanged at the
   source anchors. (NPL leads L8, L9, L11.)
9. **HF's Alpaca-eligibility reopener** (HFExperiment/DECISIONS.md:427-429; docs/ACCESS.md:19-20). The only
   later dated broker fact in the programme is ORBExperiment's 2026-08-29 credential check: Alpaca authenticates
   on the market-data host and the **paper** trading host and returns 401 on the **live** trading host
   (ORBExperiment/progress.md:1314). That is the same state HF already held (B.1 paper keys), not a Canadian
   launch. Recorded; no trigger met. (HF lead L4.)
10. **MLCryptoEngine's UNVERIFIED Helius credit weight** (lead 12) — handled by solclear, not by MLCryptoEngine:
    see the section on Agent A's own findings below.
11. **AiTrader's price-only reopen ("a genuinely new information axis")** (AiTrader/AUDIT.md:160;
    PROGRESS.md:849). Four non-price axes were subsequently opened as pre-registrations in separate repositories —
    InsiderExperiment (SEC Form 4), NPDExperiment (LLM cross-sectional ranking), ETFExperiment (ETF flow),
    VRPExperiment (options-implied variance) — which is the reopening honoured by construction, in new
    repositories, as AiTrader's own text requires ("should start from a pre-registration against the corrected
    universe"). (AiTrader lead 1.)
12. **ORB's parked H2/H3** — trigger (H1 closed) met 2026-08-30 and explicitly acknowledged at
    ORBExperiment/HYPOTHESES.md:140-144. In-repository, recorded as the positive control.

---

## Partial (category c) — and leads checked and not met

1. **retail-power-limits: "four of the seven source repositories are not published … exist only on the
   operator's machine and have no remote"** (docs/the-power-limit.md:44-52; SOURCES.md:262-275 "no — local only,
   no remote"; progress.md:113-116 "Checked at push time"). **Partially expired.** All four now have a GitHub
   remote: `origin https://github.com/kirosli00tuff/{NPDExperiment,InsiderExperiment,ETFExperiment,
   HFExperiment}.git` (`git remote -v`, read 2026-09-12T07:35:50Z). Each remote-tracking ref was created by push
   at 2026-08-29 11:45:06–11:45:18 −0700 (`git reflog show refs/remotes/origin/<branch>`: "update by push"), and
   GitHub records `createdAt` 2026-08-29T18:45:20–32Z — about eleven hours after retail-power-limits' own push
   (its repository `createdAt` 2026-08-29T07:20:25Z; commits 00:19–00:21 −0700). **But all four are `PRIVATE`**
   (`gh repo view --json isPrivate,visibility`, read 2026-09-12T07:37:58Z), as is retail-power-limits itself. So
   the sentence "no remote" is stale, while the operative claim — the four are not independently checkable and
   "A reader should discount the four accordingly" — still holds. Not a finding. (rpl lead 9.)
2. **AiTrader news-drift "verdict remains due at 60 clusters"** (NPDExperiment/REGISTRATION.md:758-762;
   InsiderExperiment/progress.md:122-123). Live AiTrader/COLLECTION_LOG.md (482 lines, UNANCHORED, read
   2026-09-12T07:41:18Z; pre-existing dirt ` M COLLECTION_LOG.md`): **29** runs recorded `action: collected`,
   targets 2026-07-30 … 2026-09-10, one gap "UNRECOVERABLE by design: 2026-08-28". About half of 60; no verdict
   has fired. (NPD lead L3; Insider lead 5.)
3. **VRP's MBT reopen figure (2)** beyond finding VRP-8: MLCryptoEngine also holds the MBT *futures* fee-only
   round turn (5.33 bps at its sample notional, report.md:981) and mbp-10 book data from which the futures touch
   spread could be read (H3: CME MBT spread − adverse − cost −4.25 on n = 148,768, report.md:1198-1214), but no
   option bid-ask exists anywhere in the programme and no repository holds a CME initial-margin figure (VRP's own
   grep, reports/task3/venue_table.md:123-126, re-confirmed against venues.yaml:205-262). (VRP leads 1–3.)
4. **HF's runnable B10 billing-plan sub-test, trigger "whenever an equity leg is next proposed"**
   (HFExperiment/progress.md:268-271, ADR-026 committed `82e77a0` 2026-08-28 14:14:08 −0700 = 21:14Z). Within the
   hour, NPLExperiment's H5 registration (commits `98e7e01` … `449ff1e`, 2026-08-28 14:38–15:11 −0700) considered
   and rejected an IBKR equity leg on HF's carried whole-share economics — "bills whole-share round trips at **40
   to 100 bp** at this operator's sizes (HFExperiment ADR-026, closed and carried), so **no cross-venue pair design
   is registrable here**" (NPLExperiment/registrations/H5/REGISTRATION.md:199-202) — and ORBExperiment registered
   a US-equity strategy the same evening without a broker. B10 is unrun. **Two facts for the record:** (i) ADR-026
   (HFExperiment/DECISIONS.md:432-479) contains no "40 to 100 bp" figure; the range is derivable only from HF's
   commission table as the whole-share **Tiered** plan at 45–180 USD notionals (cap 50 bp/side below 70 USD,
   0.35 USD minimum above — docs/ACCESS.md:66-67, :140-146), i.e. ≈ 39–100 bp round trip; under the **Fixed**
   plan the same table gives 55.6–100 bp/side, ≈ 111–200 bp round trip. (ii) B10 decides Tiered versus Fixed
   (docs/ACCESS.md:199), so running it could only leave NPL's figure unchanged or worsen it. Trigger arguably met;
   no verdict moves. (HF lead L5; NPL lead L4; cf. AUDIT-A-NPLExperiment-11.)
5. **ORB H1's only reopen route, "real execution evidence", blocked as "This repository holds none, has no broker
   credential, and none is planned"** (ORBExperiment/REGISTRATION.md:4156). The credential half exists in a
   sibling: HFExperiment's IBKR paper account [paper account ID removed] accepted and queued a whole-share US-equity order on
   2026-08-25 ("One whole share of TE was ACCEPTED and queued for the 09:30 ET open, then cancelled. The channel
   works" — HFExperiment/reports/stage_a1b/a1b_report.md:90-92) and the operator "holds a funded live IBKR
   account and a paper account … reachable through a running Gateway on port 4002" (docs/ACCESS.md:187-189,
   2026-08-28). The evidence half does not: A.1b produced no fills. Cheapest known route to ORB's reopen; not a
   met trigger. (ORB lead 1.)
6. **MLCryptoEngine H5 "current funding above roughly 10 % annualised sustained for a quarter, measured live"**
   (HYPOTHESES.md:118) and H8's dispersion condition (:135). NPLExperiment is the only repository still recording
   Hyperliquid funding after MLCryptoEngine's 2026-08-13 stop: fresh-cohort trailing entry funding **median +31.6
   %/yr, n = 62** (registrations/H4/REGISTRATION.md:210-216) — on *new listings only*, one month, not the carry
   instruments; and H5's collector serves funding on 94 HIP-3 equity perps to 2026-09-26 (registrations/H5/
   REGISTRATION.md:562-589). Neither is "sustained for a quarter" on a comparable universe. (MLCrypto lead 7; NPL
   lead L3.)
7. **NPL H3's third reopen clause — a different venue whose main-population listing rate supports the bars
   (≈ 37–50 listings/month)**. MLCryptoEngine's H8 sample is the same venue over its life: **232 perps considered
   over 1,182 days = 5.97 listings/month** (MLCryptoEngine/HYPOTHESES.md:132) — twelve times NPL's trailing
   0.5/month (NPLExperiment/docs/ACCESS.md:265-266) but six to eight times short of the clause. solattn's
   ~5,000–7,000 `amm` births/day are a different asset class with no short leg. Not met. (NPL lead L1.)
8. **NPL H4's third clause (a redesign justifying a near-0.85 conditional share)**: MLCryptoEngine H8's
   decomposition (+43.68 %/yr funding vs −42.91 % price, n = 231 perps, HYPOTHESES.md:131) is cross-sectional
   evidence, not a conditional share on negative-funding new listings. Not met. (NPL lead L2.)
9. **InsiderExperiment's "a different universe" needs a measured cost band for the next liquidity tier**
   (REGISTRATION.md:319-324, :872-874). AiTrader's by-stratum one-way spreads on the ADV 2.07M–65.3M news band
   are that measurement: S4 (thinnest) **median 50.0 bp, p90 211.6 bp** (AiTrader/RETURN.md:249; PROGRESS.md:266,
   n = 1,402 rows / 157 symbols). The tier below liquid-500 is measured at the median exactly at Insider's
   pessimistic bar and four times worse at p90. Partial. (Insider lead 1.)
10. **NPL H5's VIABLE consequence requires "an independent underlying feed"** (registrations/H5/REGISTRATION.md:
    195-197, :328-330) — held in the programme: ORBExperiment's two US-equity vendors (Alpaca SIP minute bars
    reaching 2016-01-04; Massive from 2024-08-29 — ORBExperiment/DECISIONS.md:672-732, ADR-023) and AiTrader's
    Alpaca SIP historical quotes (AiTrader/EXPERIMENT.md:2565-2579). The blocker is real for H5's registered
    scope, not for the programme. H5 has not fired VIABLE, so nothing is due yet. (NPL lead L5; cf.
    AUDIT-A-NPLExperiment-12.)
11. **MLCryptoEngine D2 / solclear §7–§8 "affordable decontaminated label — a live forward-recorded cohort that
    observes insider sells as they happen"** (MLCryptoEngine/HYPOTHESES.md:257; solclear/DECISIONS.md:700-702).
    solattn is a live forward-recorded Solana birth cohort but records no on-chain transactions and no
    creator/insider sell events (its sources are GeckoTerminal, Coinbase, Farcaster, Bluesky, Telegram —
    solattn/docs/ACCESS.md:10-16); solclear's re-price of the label is 4,695,489 credits against 1,000,000/month
    (solclear/DECISIONS.md:644-653). Cohort exists, label does not. (solclear lead L3; MLCrypto lead 11.)
12. **InsiderExperiment's "the calibration ledger still holds zero independently formed entries"**
    (REGISTRATION.md:884-885, 2026-08-25). ORBExperiment's operator prior of **0.30**, labelled `INDEPENDENT`
    (`independent_but_not_blind`), against the assistant's 0.15, was recorded 2026-08-29 (ORBExperiment/
    DECISIONS.md:550-586, ADR-020). The programme-level "zero" expired four days later; Insider's own slot remains
    empty and nothing in Insider turns on it. (Insider lead 4; ETF lead 8.)
13. **rpl lead 1 — is HF's "eight to eleven years" procedure or domain?** HF registers a studentized asymptotic
    confidence sequence, rho 0.071641 tuned for 1,600 days, and no fixed-horizon alternative
    (HFExperiment/REGISTRATION.md:246-252; reports/stage_a2/cost_table.md:38-40). Recomputed
    (`work/agentA-crossrepo/hf_fixed_horizon.py`): a fixed-horizon one-sided test at HF's own inputs (mean 27.99,
    sigma 418, hurdle 4.07 bp/day) needs **1,888 days (7.5 y) at alpha 0.05 / power 0.80**, 2,615 days (10.4 y) at
    power 0.90, and 2,397 days (9.5 y) at alpha 0.025 / power 0.80, against the registered ACS crossing at 2,852
    days (11.3 y). Roughly two-thirds domain, one-third procedure; both are multi-year. Supplement to
    AUDIT-A-retail-power-limits-2, not a finding.
14. **rpl lead 3 — NPD's zero-dollar one-session rescoring.** NPD forbids it: "Promoting the better powered
    secondary after seeing a result is exactly the move this repository exists to prevent"
    (NPDExperiment/REGISTRATION.md:256-258) and Amendment 7 voids post-read horizons — "Scoring spent data against
    new horizons is a second look however it is labelled" (:668-669). Resolved against AUDIT-A-retail-power-limits-6's
    hope; recorded here.
15. **rpl lead 10 — fifth and sixth pre-registered cases.** ORBExperiment (cost-bound on measured slippage, E2
    power 0.000000), VRPExperiment (VENUE_BLOCKED, premium measured at t 5.888), NPLExperiment H1 (a *powered*
    negative: FAIL at n = 312, lower bound 0.5707 vs 0.60) with H3/H4 BLOCKED on power before data, and
    PMExperiment (never measured). None is a powered retail-scale positive; three more closures are power- or
    cost-bound before any signal was read. This supports the note's thesis rather than reopening it. Partial.
16. **Insider lead 6 — the uncited 30–40 bp decayed band.** retail-power-limits' transcription attributes it:
    "Cohen, Malloy and Pomorski's 82 bp per month over 1989 to 2007, decayed 60 to 70 percent on 2008 to 2024
    data" (retail-power-limits/SOURCES.md:66); InsiderExperiment cites Cohen, Malloy and Pomorski only for the
    small-firm concentration (DECISIONS.md:115-116). The 82 bp figure now has an author; the "decayed 60 to 70
    percent on 2008 to 2024 data" step still has no citation anywhere in the programme.
17. **solclear lead L7 (crawler-bias invalidation) applied to siblings.** MLCryptoEngine's D2 populations derive
    from SolRPDS, which "covers only the post-graduation stratum" (MLCryptoEngine ledger; progress.md:2266-2268)
    — a listing-derived population to which solclear's 60–79-point bias applies by solclear's own argument.
    solattn is birth-ordered and reproduced the gap forward at 50.7 points (solattn/README.md:105-110). An
    invalidation lead for MLCryptoEngine's D2 sample, not a reopen; recorded for the consolidators.
18. **HF lead L9 (prior provenance).** Registered priors elsewhere: NPD 0.05 adopted; Insider assistant 0.12;
    ETF assistant 0.10; VRP 0.12/0.76/0.12; solattn 5–8 %; NPL H1 0.40 adopted; PM 5–8 % (given at closure); ORB
    assistant 0.15 vs operator 0.30. HF's 0.15 (REGISTRATION.md:289) equals ORB's assistant prior on an unrelated
    hypothesis — a weak boilerplate signal, nothing more.
19. **Checked and not met, by grep and reading (no sibling holds the item):** NPD L7 Qwen 3.8 Max cutoff (only
    NPDExperiment mentions Qwen); NPD L9 analytic null-sd IC sizing (no sibling uses `1/sqrt(n−1)`; ETF, Insider,
    ORB, MLCryptoEngine size by simulation, measured dispersion or deflated Sharpe); NPD L8 successor repository
    (none among the audited set; NPL's and PM's 2026-09-02 commits are ADR-032 and PM's own closure); HF L6
    futility template (only NPLExperiment H2 registers a futility boundary, an exact-binomial conditional-power
    construction, not HF's ACS bar); HF L7 stage prompt (siblings store their own operator prompts, never HF's);
    HF L8 factor/sector betas (only InsiderExperiment names Carhart, unbuilt); Insider L2/L3/L7 (no EW-primary
    successor, no factor panel, no ported membership code found); VRP 7–9 (no CME option chain, no crypto-ETF
    options — no sibling mentions BTCY/ETHY/covered calls — no IV-snapshot recording); ETF 1–3, 7 (no source with
    per-row publication timestamps, no non-Wayback archive measurement, no Farside capture outside ETF, no
    ETF-flow rank correlation measured anywhere); ETF 10 (MLCryptoEngine H7 "Closed by decision — the C.17 end
    condition, not evidence", design preserved, HYPOTHESES.md:216-220 — the analogy holds on "decision, not
    evidence" only); ETF 11 (HF's Wealthsimple no-API precedent, docs/ACCESS.md:14, :35-36, not amended); PM
    X1–X6, X10, X12, X13 (no Kalshi/Polymarket licence, tier, corpus, Polygon read, challenged-page fetch, Krause
    citation, event-contract enumeration or Canadian FX cost measurement anywhere; the only non-PM mentions of
    Kalshi/Polymarket are AiTrader prose); PM X11 (the programme's measured retail latencies — AiTrader news API
    median 0.17 s / p95 0.49 s, PM's own Kalshi 99.9–213.8 ms — are all above 100 ms, consistent with the
    premise; its n is still absent); solattn L1–L3 (solclear's attention-crawled cohort predates solattn and is
    cited in its registration, REGISTRATION.md:373-374 — not a later entry), L4 (solclear's 35 launch-venue
    positions, 0 graduated, DECISIONS.md:452, are the excluded class, at 100 % death), L5/L6 (no paid CoinGecko
    tier anywhere: MLCryptoEngine progress.md:2041 "CoinGecko: not needed"; solclear keyless at 30 req/min,
    progress.md:1331), L7 (no sibling reads a clustered bootstrap off k ≤ 3), L8 (honoured — nothing pooled);
    solclear L2 (MLCryptoEngine's C.23 0.574 on the n = 194 2024 fold and C.25's 57 % exclusion read consistently
    at HYPOTHESES.md:253-254; the retrospective KAT and the 422-vs-447 reconciliation remain unexercised), L4–L6,
    L8 (solattn's `amm`-only universe never applied a v1 death rule to launch-venue positions; ADR-013 v2 honoured
    by construction); NPL L6, L7, L10 (NPD Amendment 0's lesson carried and self-applied with the label
    "adopted", NPLExperiment/REGISTRATION.md:285-292); ORB 2, 4, 6, 8–10, 12 (no second minute-bar vendor on a
    non-SIP upstream, no ETF-side C-6 carry, PM holds no measurement, no Alpaca sustained-rate figure elsewhere,
    no paid Polygon credential, no futures curve); MLCrypto 1 (VRP's IBKR MBT commission of 2.176 bps round turn
    on $7,812.46 is commission-only; all-in it is MLCryptoEngine's own 5.17 bps — nothing below 3 bps all-in),
    2, 3, 5, 6, 8, 9, 10, 13 (no L3/MBO data, resting-order fills, ≤ 2-day exchange-flow source, pre-2022 basis
    series, liquidation labels, multi-venue capture, broader shorts venue, or Databento account — ORB's Databento
    probe is 401 uncredentialed, docs/ACCESS.md:111, :198), 4 (VRP handed corrected notionals $7,812.46 / $245.62
    to MLCryptoEngine, docs/VENUE_TABLE_UPDATE.md:16-137; MLCryptoEngine predates them and is unchanged), 14
    (precedents unchanged at anchors); AiTrader 2, 4–11, 13 (no head-to-head of the same model strings, no
    borrow-cost history, no US-equity fill rates — HF's A.1b had no fills — NPD's mechanical-baseline design is
    the comparator pattern on a different task, NPD's 415 rankings carry no confidence field, Insider's Form 4
    corpus is a different disclosure regime from 13F, ORB's NBBO quotes sit inside the same Alpaca window, ORB
    read its own 875 holdout sessions, no sector map or earnings calendar elsewhere, no shared model registry).

---

## Cross-repository facts bearing on Agent A's own per-repository findings

Recorded because an advocate who hides evidence against his own findings is not an advocate but a liar.

- **AUDIT-A-MLCryptoEngine-8** (D2 "measured-unaffordable" denominated in an UNVERIFIED `{rpc:1, enhanced:10}`
  unit; the finding notes that rescaled at weight 1 the estimate is ≈ 50,976, below the cap). **The sibling's
  record cuts the other way.** solclear ADR-008 (2026-08-13): "The gate priced `enhanced` at the vendor's
  published 100/call" (solclear/DECISIONS.md:258-259), and ADR-017: "the parent's ledger priced `enhanced` at
  **10 credits per call** where the vendor publishes **100** (solclear corrected this in Stage C, commit
  `ad453f9`, before its first enhanced call)" (solclear/DECISIONS.md:641-643). solclear's re-price of the same
  test is **4,695,489 weighted credits, 37.6× the 124,764** (solclear/FINDINGS.md:287-299), of which "only a
  quarter of the gap is the credit weight". The provenance point of MLCryptoEngine-8 stands (the unit was never
  reconciled against a statement; solclear too records "No response carries credit/usage headers", DECISIONS.md:
  261-262) but its affordability implication reverses: the vendor's documented weight is ten times MLCryptoEngine's
  assumed one, not one-tenth. The consolidators should read MLCryptoEngine-8 as PROVENANCE only and consider S3/S4.
- **AUDIT-A-VRPExperiment-3** is strengthened: beyond the untried GCC route, a sibling obtained the fee leg from a
  public broker republication (finding VRP-8 above).
- **AUDIT-A-NPLExperiment-11**: the "40 to 100 bp" carry is not in HF ADR-026 as cited; it is derivable from HF's
  commission table as the *favourable* (Tiered) reading — see Partial 4. The finding's core (categorical foreclosure
  on an unverified carry) stands; the direction of any correction is against NPL's figure, not for it.
- **AUDIT-A-solclear-9** ("keyless enumeration sources were exhausted"): solattn enumerated 70,894 `amm` pools over
  13 days from the same keyless GeckoTerminal feed (solattn/docs/ACCESS.md:12) — the forward route solclear itself
  called feasible (progress.md:1490-1494). The exhausted sources were retrospective (2025 births); the finding
  should be read as narrowed to "retrospective keyless enumeration".
- **AUDIT-A-AiTrader-2** ("unmeasurable" inference on `whale_signal`): the mischaracterisation propagated —
  NPDExperiment records the layer as "measured to nothing independently" (finding NPD-5 above).
- **AUDIT-A-retail-power-limits (the unpublished-repositories discount):** partially expired — private remotes
  exist since 2026-08-29T18:45Z (Partial 1).

---

## Lead coverage — every lead in `agentA-leads.json`, with disposition

Key: **F** = finding above; **H** = handled/verified unchanged (section "Triggers met and already handled");
**P** = partial (section "Partial", item number); **N** = checked, not met (Partial 19 unless noted).

| repository | leads → disposition |
|---|---|
| NPDExperiment | L1 N (HF's ADR-022 reopeners unmet at HF's anchor; ADR-026 reaffirms, DECISIONS.md:427-429, :459-461) · L2 H1 · L3 P2 · L4 **F NPD-5** · L5 H (AiTrader PROGRESS.md:775 / RETURN.md:2437 unchanged) · L6 N (figure at AiTrader PROGRESS.md:754; no rationale-emitting variant registered anywhere) · L7 N · L8 N · L9 N |
| retail-power-limits | 1 P13 · 2 H3 · 3 P14 · 4 H (ETF reopen (c) text confirmed, HYPOTHESES.md:84) · 5 N (ETF retro revision n = 11 carries no verdict; forward revision forgone) · 6 H2 · 7 H (solattn Amendment 7; per-repo) · 8 P (Insider ADR-011 permits EW-primary only in a fresh registration with disclosure, DECISIONS.md:328-333) · 9 P1 · 10 P15 · 11 N |
| HFExperiment | L1 H2 · L2 N (no AiTrader pull-end, formation-code, width or member-handling entry after 2026-07-29) · L3 H2 · L4 H9 · L5 P4 · L6 N · L7 N · L8 N · L9 P18 |
| InsiderExperiment | 1 P9 / N · 2 N · 3 N · 4 P12 · 5 P2 (+ note: "tested across … HFExperiment" while HF's own record is n = 0 shadow observations, HFExperiment/REGISTRATION.md:314-315 — the family was tested in AiTrader) · 6 P16 · 7 N (AST-guard lesson carried into NPL, DECISIONS.md:50-54; membership code not found elsewhere) |
| VRPExperiment | 1 **F VRP-8** · 2 P3 · 3 N · 4 N (MLCryptoEngine predates the corrections; unchanged) · 5 H6 · 6 H (precedents unchanged; ADR-034 contested by MLCryptoEngine-9) · 7 N · 8 N · 9 N |
| ETFExperiment | 1 N · 2 N · 3 N · 4 H4 · 5 H5 · 6 H5 · 7 N · 8 P12 · 9 P (Insider and NPD both closed on arithmetic; ETF on a calendar — supports AUDIT-A-ETFExperiment-3) · 10 N · 11 N |
| PMExperiment | X1 N · X2 N · X3 N · X4 N · X5 N · X6 N · X7 H3 · X8 H3 · X9 H3 · X10 N · X11 N · X12 N · X13 N |
| solclear | L1 **F solclear-11** · L2 N (consistent) · L3 P11 · L4 N (MLCryptoEngine ADR-054 carries the same 0-of-8; solattn holds no creators; cf. AUDIT-A-solclear-6) · L5 N · L6 N · L7 P17 · L8 N (honoured) · L9 P (solattn forward cohort; see solclear-11 and the section above) |
| solattn | L1 N · L2 N · L3 N · L4 N · L5 N · L6 N · L7 N · L8 H (constraint honoured) |
| NPLExperiment | L1 P7 · L2 P8 · L3 P6 · L4 P4 · L5 P10 · L6 H8 · L7 N · L8 H8 · L9 H8 · L10 N · L11 H8 |
| ORBExperiment | 1 P5 · 2 N · 3 P (ORB's cost-bound rests on measured slippage, not a PnL as in MLCryptoEngine H6 — supports AUDIT-A-ORBExperiment-12) · 4 N · 5 **F ORB-18** · 6 N · 7 **F ORB-19** · 8 N · 9 N · 10 N · 11 H7 · 12 N |
| MLCryptoEngine | 1 N · 2 N · 3 N · 4 N · 5 N · 6 N · 7 P6 · 8 N · 9 N · 10 N · 11 P11 · 12 H10 (see Agent-A section) · 13 N · 14 H |
| AiTrader | 1 H11 · 2 N · 3 **F AiTrader-19** · 4 N · 5 N · 6 N · 7 N · 8 N · 9 N · 10 N · 11 N · 12 **F AiTrader-20** (options) / N (earnings dates) · 13 N |

---

## Access record (rules: status before first and after last live access, per repository)

All live accesses were read-only: `git remote -v`, `git reflog show`, `git for-each-ref`, `git log`, `git blame`,
`gh repo view` (network read), and two untracked files. Outputs verbatim:

| repository | before | after |
|---|---|---|
| NPDExperiment | (empty) | (empty) |
| InsiderExperiment | (empty) | (empty) |
| ETFExperiment | (empty) | (empty) |
| HFExperiment | `?? Accept:` `?? GET` `?? Host:` `?? User-Agent:` | same (pre-existing owner files) |
| solclear | (empty) | (empty) |
| AiTrader | ` M COLLECTION_LOG.md` | ` M COLLECTION_LOG.md` (pre-existing collector append) |
| ORBExperiment | (empty) | (empty) |
| NPLExperiment | (empty) | (empty) |

Unanchored reads: `solclear/_CLOSED_DO_NOT_RUN_HERE` (untracked, 747 bytes, mtime 2026-09-02 22:38, read
2026-09-12T07:38:00Z); `AiTrader/COLLECTION_LOG.md` (live, 482 lines, read 2026-09-12T07:41:18Z). GitHub
metadata read 2026-09-12T07:37:58Z. No audited repository was modified; no `.env`, key or session file was opened.

## What I checked and did not find (so the clean areas are stated)

- No repository's registered reopen condition is met *in full* by another repository's dated work. The seven
  findings are all stale blockers, stale sibling-status statements or data-availability closures where a sibling
  holds the datum; none reverses a verdict.
- No carried figure has moved at its source (twelve carries traced, section "Triggers met and already handled").
- No cross-repository double-counting or pooling was found across the solattn/AiTrader family boundary.
- No sibling holds any of: a Kalshi/Polymarket licence, a CME margin figure, a paid CoinGecko tier, order-level
  book data, a pre-2022 crypto basis series, a Farside capture, a Carhart factor panel, a US-equity borrow-rate
  history, or a second US-equity minute-bar upstream — the seven most-requested items across the ledgers.
