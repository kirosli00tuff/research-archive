# REOPEN LEDGER — retail-power-limits @ `dda39b2f148569a6fe9be956a979471b2330611d`

Factual, not advocacy. This repository registers no hypothesis of its own; it ships one note and
carries seven sibling closures as quoted figures. Entry 1 is the note itself; entries 2–9 are the
sibling closures **as recorded in this repository** — every `file:line` below is a line of
retail-power-limits, never of the sibling. Sibling-side reopen conditions whose text is not carried
here are marked "exists, text not carried". The final column flags conditions that work in a
different repository could satisfy; those are collected in the last section.

| # | entry | status | closure kind | closure date | deciding figure (n) | file:line | blockers (file:line) | reopen conditions (file:line) | other-repo? |
|---|---|---|---|---|---|---|---|---|---|
| 1 | retail-power-limits — the note ("the binding constraint was ... whether an achievable sample could detect an effect of the reported size") | shipped | n/a — secondary-source note, no verdict of its own | 2026-08-29 (commits `0974f96`, `710093d`, `dda39b2`, all 2026-08-29 00:19–00:21 -07:00) | four cases: MDE 0.0512 vs band 0.01–0.05 (n = 415 stored / 404 evaluable / 125.6 effective days); MDE 49.35 bp/mo vs floor 40 (N_eff 2,869.9; 4,585 events); 163 vs 300 admissible days (n = 11 at closure of a 336-row census); z 1.668 vs 2.50 (n = one 2.55-y holdout) | README.md:18-23; docs/the-power-limit.md:69-76; SOURCES.md:27-155 | Four of the seven source repositories unpublished — "A reader should discount the four accordingly" (docs:44-52; SOURCES.md:262-288; progress.md:113-127) | (a) "a domain whose effects are large relative to achievable samples" — a larger effect, a cheaper independent observation, or a lower-dispersion design (docs:370-391; README.md:48-49); (b) "evidence that this program's method is itself the constraint" (docs:393-401); (c) ADR-001 overturn — a document that must *change* one of the four (DECISIONS.md:49-52); (d) ADR-003 overturn — evidence a correction is itself wrong (DECISIONS.md:116-117); (e) ADR-004 overturn — a reading of the AiTrader round as a signal closure (DECISIONS.md:145-149); (f) ADR-006 overturn — NPDExperiment recording its own stage total (DECISIONS.md:192-193); (g) ADR-002 and ADR-005: "Nothing" (DECISIONS.md:82-83, 172-173) | yes — (a)/(b) by any repository producing a powered retail-scale positive or a same-sample estimator gain; the blocker expires if NPD / Insider / ETF / HF acquire a remote |
| 2 | NPDExperiment — numeric-LLM cross-sectional ranking vs mechanical baselines (carried) | closed | unresolved at achievable power ("Two serious attempts have produced zero positives") | 2026-08-25 (closing commit `2d3d0ae`, 13:26:58) | realized minimum detectable contrast 0.0512 vs band 0.01–0.05; pre-registered projection 0.026–0.047; realized contrast sd 0.36339 vs an assumed ≤0.2626 (n = 415 stored rankings of 432 window days / 404 evaluable / 125.6 independent-equivalent; 920 billed calls; 6.9378 USD) | SOURCES.md:28-58; rplimits/cases.py:80-128; docs:81-88, 161-178 | "Roughly four times the evaluable days, landing near 1,700 trading days of post-cutoff window. No model has one; the window accrues at about 21 trading days a month." (SOURCES.md:46); the one-shot sealed store is spent (docs:242, 248-253) | fresh collection on a fresh window under a new registration, "about 7 USD" (docs:243); post-hoc scoring at two more horizons voided as a second look (docs:250-252); better-powered secondary registered non-verdict-bearing and not promoted (docs:165-168); ADR-011 "reading realized power first" (SOURCES.md:230 — exists, text not carried) | yes — NPDExperiment itself (the secondary's registered power, the realized point contrast, whether an exploratory one-session rescoring is permitted); any repository using an earlier-cutoff model with a longer post-cutoff window |
| 3 | InsiderExperiment — opportunistic/cluster Form 4 purchases predict returns net of retail costs (carried) | closed | BLOCKED on the power gate, verdict row V7 | 2026-08-25 (gate commit `cb17046`; closing commit `12d9fd3`, 23:24:15) | MDE 49.35 bp/month vs a BLOCKED floor of 40 and a GO bar of 20; gross band 30–40, net 13.3–34.7; Newey-West stable at 50.19 / 49.11 / 49.53 for lags 5 / 63 / 126 (n = 4,585 qualifying events vs a floor of 1,000; 2,581 sessions at 99.5 % coverage; N_eff 2,869.9; 71.9 names behaving as 29.7; TE 9.993 %) | SOURCES.md:60-90; rplimits/cases.py:130-183; docs:90-97, 180-232 | Weight concentration — "The 9.993 percent annualized tracking error is the whole of the 49.35"; Section 0.4 required about 23 effective names (SOURCES.md:78); universe scope — 94.2 % of qualifying purchases fall outside the liquid-500 band (SOURCES.md:90); the realized alpha is sealed and unread (SOURCES.md:82) | equal-weighted secondary on the identical names → 34.29 bp = DEGRADED, "any future test naming equal-weight as primary would have to disclose that the choice was made after seeing this number" (docs:227-232, 386-391); ADR-011 "reopening boundary" (SOURCES.md:223; rplimits/sources.py:74-80 — exists, text not carried) | yes — a lower-dispersion (capped or equal-weight) registration in InsiderExperiment or a successor repository |
| 4 | ETFExperiment — US spot-BTC ETF flow prints → next-day BTC return net of a Hyperliquid round trip (carried) | closed | untestable at achievable power ("The signal was never read and this closure is not evidence about it") | 2026-08-28 (closing commit `3f5d629`; disarm commit `4d11002`) | 163 admissible days projected at the registered 2027-03-31 deadline vs a governing 300 at the published ρ 0.18 (E1 237 / E2 300); above 1,200 and 845 at the registered 0.09; shortfall 137 (n = 11 admissible at closure from a 336-row census; accrual 20.8/month; 220 charged requests; 0 USD) | SOURCES.md:92-122; rplimits/cases.py:185-238; docs:99-105, 132-139 | as-printed archive density 11/333 = 3.30 % against a registered 60 % bar (docs:101-104); the registered deadline 2027-03-31; the forward collector disarmed — "Disarm etf-snap; correct the reopen-path mislabel in Amendment 5 and ADR-019" (SOURCES.md:215; rplimits/sources.py:123-129) | Amendment 6: about 302 admissible days by 2027-10-31 clears the governing 300 at the published 0.18 "by two days" and clears nothing at 0.09 (docs:132-139; SOURCES.md:122; DECISIONS.md:101-104); the "reopen-path" in Amendment 5 / ADR-019 (SOURCES.md:215 — exists, text not carried) | yes — re-arming the collector (same repository), or any repository holding an as-revised flow history together with a measured revision magnitude |
| 5 | HFExperiment — EW top-5 by 12-1 momentum in U-LIQ-500 vs EW universe, forward shadow series (carried) | closed | BLOCKED on the broker (IBKR errors 10243/10244) plus operator decision; the power resolution is *inherited* from AiTrader | 2026-08-26 (rplimits/cases.py:243; terminal-closure commit `f13e1d3` dated 2026-08-25, SOURCES.md:218) | inherited: z 1.668 vs a corrected 2.50, interval −4.9 to +60.9 bp/day, 104.0 %/yr of excess needed vs 70.5 delivered (n = one 2.55-y holdout, touched once at `a0a9ef6`); its own Section 11: the CS lower bound clears zero at day 2,061 and the 4.07 bp/day hurdle at day 2,852 (n = 0 forward shadow observations) | SOURCES.md:124-154; rplimits/cases.py:240-295; docs:107-116, 141-146; DECISIONS.md:121-149 | IBKR refused fractional quantities through the API, errors 10243 and 10244 (docs:142-144; SOURCES.md:154); "Eight to eleven years" under the frozen confidence sequence (SOURCES.md:142) | none stated in this repository; the ADR-004 overturn condition concerns the *note's* classification, not HFExperiment's reopening (DECISIONS.md:145-149) | yes — AiTrader (the RETURN.md width table); HFExperiment Section 11 (the confidence-sequence family and α); a whole-share or paper-only re-registration would remove the broker blocker |
| 6 | AiTrader — H-F in the cross-sectional round (carried as HFExperiment's inheritance) | resolved (findings only, nothing applied) | "resolved on statistical power rather than absent signal" | 2026-07-26 (round commit `a0a9ef6`; RETURN.md `f819b68`, 2026-07-29) | z 1.668 vs 2.50; 27.99 bp/day excess; 90.3 %/yr against a benchmark's 19.7; TE 66.4 %; widening 5→50 names: TE 31.7 %, excess 10.04 bp/day, z 1.455 (n = one 2.55-y holdout) | SOURCES.md:130-136, 212-213; rplimits/cases.py:250-263 | "the binding constraint on this family is the position limit" (DECISIONS.md:147-148) | none stated here | yes — AiTrader's own register (the width table's z definition and SE) |
| 7 | MLCryptoEngine — eleven hypotheses (contrast case) | closed (9 of 11 tested and closed; H7 by decision; H6 negative) | cost-bound (H1, H3) / signal-absent (H2, H4) / decayed (H5) / hedged-out (H8) / insignificant after deflation (H9) / unidentifiable (H10) / six bars failed (H11) | register 2026-08-12 (`d2a0f05`); H1 note 2026-08-22 (`ae03bf6`) | H1: AUC 0.9432 with 0.0291 bps of capture at 100 ms vs Kraken's 50 bps round trip (≈1,700×) and Hyperliquid's 3 bps (≈100×); H4: break-even 300–550 bps vs 3 bps actual (100–180×) | SOURCES.md:166-176; rplimits/cases.py:300-325; docs:280-293 | fee floor 3 bps, "the cheapest venue reachable from the operator's jurisdiction at all" (SOURCES.md:172) | cost-bound entries "reopen at a lower fee tier" / "reopen on a fee schedule or not at all"; signal-absent entries do not reopen on a better model, a better feature set or lower fees (docs:281-285; SOURCES.md:176) | yes — a venue or fee-tier change in any crypto repository, against MLCryptoEngine's own "what would reopen it" field |
| 8 | solattn — attention-crawled pool selection lift (contrast case) | closed | powered null; kill criterion K1 fired at 100.0 % outcome coverage on every *analysed* cohort | 2026-08-28 (`b3f5062`) | lift −1.0779 net of a 450 bps cost band, 95 % day-clustered CI [−3.3354, +0.0204]; 120/120 computable cells negative (n = 12,798 amm pools over three birth days; 2,107 measurable at the d0+2 anchor; Q5 cell n = 412) | SOURCES.md:178-188, 233-234; rplimits/cases.py:327-348; docs:295-302 | none stated | Amendment 7 "records the Stage B readout and the horizon never analysed" (SOURCES.md:234; rplimits/sources.py:186-192 — a named un-analysed variant; text not carried) | yes — solattn itself (the un-analysed horizon); solattn is public (SOURCES.md:265) |
| 9 | solclear — Stage E outcome study on cleared pools, plus a confirming measurement (contrast case) | closed (mixed) | registered underpowered rule fired, no significance claimed in either direction; the confirming measurement "priced out rather than untested"; plus a crawler-survivorship result | 2026-08-14 (underpowered rule fired); findings at `c692032`, 2026-08-22 | 18 cleared vs a floor of 20 at 30 days, 4 at 90; all 18 realised −100 % net at 30 days and all 4 at 90; share ever above entry 0 % of 18; confirming measurement 4,695,489 weighted credits vs a stale 124,764 estimate (37.6×); survivorship 97.5 % death on 40 birth-ordered pools vs 18.75 % on 16 attention-crawled | SOURCES.md:190-200; rplimits/cases.py:350-375; docs:304-313 | cost: 4,695,489 weighted credits (SOURCES.md:192) | none stated in this repository beyond the cost figure; a cost-bound closure reopens on price | yes — a cheaper credit source in solclear or a sibling |

## Registered reopen conditions of the note itself, checked against later entries in this repository

Nothing in this repository postdates 2026-08-29; its three commits fall inside two minutes
(00:19:47, 00:20:34, 00:21:28 -07:00) and `dda39b2` is the anchored HEAD. **No reopen condition in
rows 1–9 is met by a later entry here.** Conditions that could be met elsewhere are flagged in the
last column and collected below.

One reopen condition of row 1 deserves a note rather than a check: condition (a), "a domain whose
effects are large relative to achievable samples ... **not a better estimator on the same ones**"
(docs:363, README.md:48-49), is contradicted by its own third bullet at docs:386-391, which offers a
same-sample estimator change worth a 30 % MDE reduction. That is finding
AUDIT-A-retail-power-limits-1. Until the wording is settled, the ledger cannot say whether a
same-sample estimator gain satisfies condition (a) or is excluded by it.

## Stated blockers, checked for expiry within this repository

- **Four sibling repositories unpublished** (docs:44-52; SOURCES.md:262-275; progress.md:113-116).
  Stated as checked "at push time rather than assumed" on 2026-08-29 (progress.md:113). Not
  revisited here — the repository has a single day of history. Cross-repo check required.
- **NPDExperiment's one-shot sealed store, spent** (docs:242, 248-253; SOURCES.md:50). No later
  dated entry here lifts it, and nothing in this repository could.
- **ETFExperiment's disarmed forward collector** (SOURCES.md:215; rplimits/sources.py:123-129). No
  later entry here re-arms it; the note records the disarm as final.
- **HFExperiment's broker blocker, IBKR errors 10243/10244** (docs:142-144; SOURCES.md:154). No
  later entry here lifts it.
- **MLCryptoEngine's 3 bps fee floor** and **solclear's 4,695,489-credit price** (SOURCES.md:172,
  192). Both are price blockers; nothing in this repository re-prices either.
- No other blocker in this repository has a later dated entry that could lift it.

## Leads for the cross-repository pass

Every blocker or reopen condition above that work in another repository might satisfy, with the
repository most likely to hold the answer.

1. **HFExperiment REGISTRATION.md Section 11** (`hf-registration` @ `f13e1d3`, SOURCES.md:221) —
   the confidence-sequence family and α, and whether a fixed-horizon alternative was registered and
   rejected. Satisfies or refutes AUDIT-A-retail-power-limits-2 (whether "eight to eleven years" is
   procedure or domain). **Best guess: HFExperiment.**
2. **NPDExperiment REGISTRATION.md Section 9 and progress.md Stage B.2** (`npd-registration`,
   `npd-progress` @ `2d3d0ae`, SOURCES.md:231-232) — the MDE convention (power target, sidedness,
   which N) and the realized point contrast with its interval. Settles
   AUDIT-A-retail-power-limits-3. **Best guess: NPDExperiment.**
3. **NPDExperiment DECISIONS.md ADR-007 and ADR-011** (`npd-decisions` @ `2d3d0ae`,
   SOURCES.md:230) — the registered power of the shorter-horizon secondary, and whether a
   non-verdict-bearing exploratory rescoring of the 404 stored evaluable days at the one-session
   horizon is permitted. This is the only reopen condition in the ledger that costs zero dollars on
   data already paid for. Settles AUDIT-A-retail-power-limits-6 and row 2's reopen column.
   **Best guess: NPDExperiment.**
4. **ETFExperiment REGISTRATION.md Amendments 5–6 and ADR-019** (`etf-registration` @ `4d11002`,
   SOURCES.md:217) — the "reopen-path" whose mislabel the disarm commit says it corrected; whether
   the registered 2027-03-31 deadline may be extended; what re-arming would require. Settles
   AUDIT-A-retail-power-limits-5 and row 4's reopen column. **Best guess: ETFExperiment.**
5. **ETFExperiment REGISTRATION.md Section 0 / Section 9 and Amendments 3–6** (same citation) —
   whether an as-revised flow history was considered and rejected, and on what measured revision
   magnitude. Settles AUDIT-A-retail-power-limits-8. **Best guess: ETFExperiment**; a secondary
   lead is any crypto repository holding a stored flow series with both as-printed and revised
   values (**MLCryptoEngine** is the only other crypto-data repository in the program, though the
   note does not say it holds ETF flows).
6. **AiTrader RETURN.md @ `f819b68`** (`aitrader-return`, SOURCES.md:212) — the width table's actual
   z for 50 names and how its standard error is defined. Settles AUDIT-A-retail-power-limits-11 and
   row 6. AiTrader is public (SOURCES.md:267). **Best guess: AiTrader.**
7. **solattn REGISTRATION.md Amendment 7** (`solattn-registration` @ `b3f5062`, SOURCES.md:234) —
   which horizon was never analysed, why, and whether K1's firing was registered as sufficient to
   skip it. Settles AUDIT-A-retail-power-limits-7 and row 8's reopen column. solattn is public
   (SOURCES.md:265) and anchored at the same `b3f5062` the note cites. **Best guess: solattn.**
8. **InsiderExperiment DECISIONS.md ADR-011, the "reopening boundary"** (`insider-decisions` @
   `12d9fd3`, SOURCES.md:223; rplimits/sources.py:74-80) — its text is not carried here; the ledger
   records only that it exists. It may already permit the equal-weight (lower-dispersion)
   re-registration that AUDIT-A-retail-power-limits-1 says the note's reopen condition excludes.
   **Best guess: InsiderExperiment.**
9. **Do NPDExperiment, InsiderExperiment, ETFExperiment or HFExperiment now have a remote?**
   (progress.md:113-116; SOURCES.md:262-275; docs:44-52). This is the note's only stated blocker on
   its own claim, checked at push time on 2026-08-29 and never revisited. If any of the four is now
   public, "A reader should discount the four accordingly" (docs:51-52) has partially expired.
   **Best guess: each of NPDExperiment, InsiderExperiment, ETFExperiment, HFExperiment** — a
   `git remote -v` in each live repository answers it.
10. **Row 1 condition (a)/(b) — "a domain whose effects are large relative to achievable samples"
    and "evidence that this program's method is itself the constraint"** (docs:370-401). Any
    repository in the program that produced a *powered* retail-scale positive, or that shows the
    same shared design blind spot across independent hypotheses, bears on these. **Best guess: the
    repositories the note does not carry at all** — ORBExperiment, VRPExperiment, NPLExperiment,
    PMExperiment — since a fifth and sixth pre-registered case from the same operator is exactly the
    evidence the note says it lacks ("Four cases are four cases", docs:39-42; "Four cases run by one
    person under one scaffold cannot distinguish 'retail-scale replication is power-bound' from
    'these four designs were underpowered'", docs:396-398).
11. **Row 7 and row 9 price blockers** — MLCryptoEngine's cost-bound entries "reopen at a lower fee
    tier" (docs:281-285; SOURCES.md:176) and solclear's 4,695,489-credit confirming measurement
    (SOURCES.md:192). A cheaper venue or credit source recorded anywhere in the program would meet
    them. **Best guess: MLCryptoEngine** for the fee tier, **solclear** for the credit price;
    secondarily any Solana-data repository (**solattn**, **solclear**) that records a cheaper
    provider.
