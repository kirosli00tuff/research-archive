# POSITIVES LEDGER — HFExperiment

Repository: HFExperiment, anchored SHA 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28).
Factual, not advocacy. Every entry gives the claim as stated with file:line, the deciding figures
with n, the bar and its registration date, any amendment touching the bar, the corrections applied,
and the framing used in README / report / register.

**Repository-level fact that conditions every row:** the shadow series produced **zero** observations,
no live order was ever sent for the strategy, no fill and no commission were ever observed, and the
verdict was never computed (REGISTRATION.md:308-315; progress.md:5-21; reports/stage_a1b/a1b_report.md:96-98).
Live tree confirms: data/bars.db has 0 rows in all six tables, data/ledger/ is empty (UNANCHORED,
read 2026-09-04T00:09Z). No entry below is a positive *result* of the signal hypothesis; the positives
are measurement verdicts and shipped numeric artifacts.

**Commit dates used for provenance (UTC, from `git log --date=iso-strict` on the live repository):**
c4e9817 2026-08-23T22:23:16 (Section 0) · 0a0d214 2026-08-23T22:42:34 (A.1 evidence) ·
91a1dcb 2026-08-23T22:43:53 (A.1 docs) · a8f4b0d 2026-08-24T04:40:25 (A.2, Sections 1-12) ·
23d9ffa 2026-08-24T04:40:30 (A.2 docs) · 6ac61d2 / 8c4c3bc 2026-08-25T00:36:21 (B.1) ·
9634157 / b4a7a23 2026-08-25T02:46:28 (C.1) · 669eb5c 2026-08-25T03:09:06 (A.1b) ·
23b7791 2026-08-25T03:09:55 (lint) · f13e1d3 2026-08-25T07:45:29 (closure) ·
82e77a0 2026-08-28T21:14:08 (ADR-026, tip).

---

## 1. Section 0 verdict: BLOCKED (the headline positive measurement claim)

| field | content |
|---|---|
| Claim as stated | "BLOCKED. The IBKR TWS API refused fractional quantities however phrased on paper account [paper account ID removed], error 10243 on decimal totalQuantity across two book names and two order types, error 10244 on cashQty, while a whole-share control order was accepted" — REGISTRATION.md:299-302 |
| Kind | positive (measurement verdict); it terminated phases C and D |
| Deciding figures (n) | 3 decimal orders (2 symbols MU/TE, 2 order types) all cancelled at validation with error 10243; 1 cashQty order cancelled with error 10244; 1 whole-share control accepted (PreSubmitted) — reports/stage_a1b/evidence.jsonl:30, 33, 40, 43, 49. n = 5 orders, 1 account, 1 session (2026-08-25 03:05-03:07 UTC), 0 fills, market closed |
| Bar + registration date | Section 0 GO bar: "accepts fractional quantities through that API at 45 USD per name" — REGISTRATION.md:16-17, registered 2026-08-23 (c4e9817, 22:23:16Z, "before any broker measurement") |
| Amendments touching the bar | 2026-08-25 amendment fires BLOCKED and states "No parameter changes." (REGISTRATION.md:297-304), committed 669eb5c 03:09:06Z, 2 minutes after the run ended. Data existing: the A.1b evidence ledger only. ADR-026, 2026-08-28 (82e77a0), re-statuses the sub-tests but "changes no verdict" (DECISIONS.md:457-458) |
| Corrections applied | Eligibility control (all 20 names advertise MinSize/SizeIncrement 0.0001) used to exclude the instrument-level explanation; whole-share control used to exclude the Read-Only-API and dead-channel explanations; both order types and two names used to exclude order-type specificity |
| Corrections NOT applied | The account's own **Trade in Fractions permission** — the repository's registered precondition for every sub-test ("Every sub-test below is blocked until one exists, live, with the Trade in Fractions permission enabled in Client Portal, because a paper account inherits the live account's permissions", docs/ACCESS.md:184-186, struck by ADR-026) — was never verified. No permission check appears in scripts/a1b_capability_test.py or evidence.jsonl. The a1b report dismisses the confound with instrument-layer evidence: "The whole-share-only permission-sync escape of the stage prompt therefore does not apply: the instruments are eligible" (a1b_report.md:37-40) |
| Provenance issues | The control order was not placed by any committed code (see all.md DRAFT-all-1); the reported "server version 187" contradicts evidence.jsonl's 178 (DRAFT-all-2); the evidence ledger is truncated on every run (DRAFT-all-16) |
| Framing | README: absent entirely. Register: "BLOCKED" as a dated amendment. Report: "Section 0 fires BLOCKED" (a1b_report.md:107). Progress: "Fired. Section 0 verdict BLOCKED ... The shadow series carries the experiment alone" (progress.md:39-44). ACCESS.md sub-test table: 4 RESOLVED / 2 MOOT / 1 RUNNABLE (ACCESS.md:192-200) |

## 2. "The instruments are fractional-eligible; the API channel is what refuses"

| field | content |
|---|---|
| Claim as stated | "all 20 names of the 2026-08-03 width-20 book advertise MinSize 0.0001 and SizeIncrement 0.0001. The instruments are fractional-eligible; the API channel is what refuses" — docs/ACCESS.md:196 |
| Kind | positive (causal attribution) |
| Deciding figures (n) | 20 `contract_details` records, MinSize 0.0001 and SizeIncrement 0.0001 on all 20 — evidence.jsonl:3-22; tabulated a1b_report.md:14-35 |
| Bar + registration date | Sub-test "MinSize and SizeIncrement from reqContractDetails on the same symbol", registered as BLOCKED-ON-OPERATOR in A.1's ACCESS.md, 2026-08-23 (0a0d214) |
| Amendments touching the bar | ADR-026, 2026-08-28 (82e77a0): status changed BLOCKED-ON-OPERATOR → "RESOLVED — ELIGIBLE"; the precondition column ("live account exists, Trade in Fractions enabled, paper gateway reachable") deleted in the same edit. Data existing: the A.1b evidence of 2026-08-25 and an operator statement of 2026-08-28 |
| Corrections applied | none beyond the 20-name census |
| Gap | SizeIncrement is a **contract** property; account-level fractional permission is a different object and was never read. The inference from instrument eligibility to "the API channel is what refuses" does not exclude the account-permission cause the repository itself registered as a precondition. The error text ("Fractional-sized order cannot be placed via API. Please use desktop version") is independent support for the API-channel reading and is the strongest evidence here |
| Framing | ACCESS.md and ADR-022 state it as settled; ADR-022: "the instruments are fractionable and the refusal is the API channel itself, which matches the error text's own words" (DECISIONS.md:423-425) |

## 3. Whole-share control ACCEPTED → "the channel works, Read-Only is off"

| field | content |
|---|---|
| Claim as stated | "One whole share of TE was ACCEPTED and queued for the 09:30 ET open, then cancelled. The channel works, Read-Only is off, and the fractional refusals are specific to fractional sizing." — reports/stage_a1b/a1b_report.md:91-93 |
| Kind | positive (shipped control result), also a new ACCESS.md sub-test row |
| Deciding figures (n) | n = 1 order, 1 share of TE (~4.35 USD notional against a registered bar of 45 USD/name), Warning 399 then PreSubmitted, 0 filled — evidence.jsonl:48-50 |
| Bar + registration date | Not a registered sub-test. The six registered sub-tests (ACCESS.md at 0a0d214, 2026-08-23) contain no control-order row |
| Amendments touching the bar | ADR-026, 2026-08-28 (82e77a0), **added** the row "| whole-share control order | RESOLVED — ACCEPTED |" (ACCESS.md:197) and counted it among "four RESOLVED" (DECISIONS.md:452). Data existing: the A.1b record of 2026-08-25 |
| Corrections applied | none |
| Provenance | Not produced by committed code: field set of evidence.jsonl:48-49 does not match scripts/a1b_capability_test.py:106-115 and :129-137 (extra `purpose`; missing `cash_qty`, `lmt_price`, `outside_rth`, `remaining`, `avg_fill_price`); placed 51 s after the script wrote `orders_placed_total count=4`; order_id/reqId 3 implies a fresh connection; no revision of the script in git history places a control order |
| Framing | Register: "while a whole-share control order was accepted" inside the binding BLOCKED amendment (REGISTRATION.md:302). ACCESS.md: "Whole-share through the API stays open; only slicing is closed" (ACCESS.md:197). Progress: "proving the channel works, Read-Only is off" (progress.md:35-37) |

## 4. ADR-022: the cashQty documentation contradiction, resolved by behaviour

| field | content |
|---|---|
| Claim as stated | "The staff claim stands, the third-party claim is refuted, and the rounding report is moot on this channel." — DECISIONS.md:418-419 |
| Kind | positive (a documentation conflict declared closed) |
| Deciding figures (n) | n = 1 cashQty order, error 10244 "Cash Quantity cannot be used for this order" — evidence.jsonl:43 |
| Bar + registration date | A.1 registered the conflict as unresolvable from documentation and requiring a test — original ACCESS.md text (deleted by ADR-026): "The documentation conflict stands unresolved on purpose ... Likely is not measured. The verdict waits for the test." Registered 2026-08-23 (0a0d214) |
| Amendments touching the bar | ADR-026, 2026-08-28: the "unresolved on purpose" paragraph rewritten in place (not struck) to "now resolved rather than open" (ACCESS.md:217-223) |
| Corrections applied | Both fractional phrasings tested (decimal quantity and cashQty); "no silent rounding because nothing was accepted to round" (ACCESS.md:195) |
| Limits | n = 1 order, 1 paper account, 1 session, 1 client library; the Elite Trader report concerned the **Web** API and is declared "moot on this channel" rather than tested |
| Framing | Register: not mentioned. ADR-022 and ACCESS.md state it as resolved; progress.md:48-50 "Resolved. The cashQty-versus-decimal documentation contradiction, ADR-022, by observed behaviour with verbatim errors as citation" |

## 5. The universe reproduction

| field | content |
|---|---|
| Claim as stated | "Reproduced. All 124 recorded formation dates identical. Universe exact at all 10 checked dates, all 500 rows each." — progress.md:207-208; and "Universe rule U-LIQ-500-stk-w60-m40-p5, copied verbatim from the recorded round and reproduced by Stage A.1 against all 124 recorded formation dates." — REGISTRATION.md:78-80 |
| Kind | positive (reproduction claim) |
| Deciding figures (n) | 124/124 formation dates identical; 10 dates × 500 rows exact_match true, 0 missing, 0 extra, 0 rank mismatches, 0 value mismatches — reports/stage_a1/universe_check.json (all 10 objects), reports/stage_a1/reproduce_log.txt:1-21; 19,744 symbols segmented; DB hash c30d3f4486e975a0 unchanged before and after (reports/stage_a1/db_hash_before.txt, db_hash_after.txt) |
| Bar + registration date | ADR-005/ADR-006, 2026-08-23 (91a1dcb): reproduction horizon pinned to `analysis_meta.universe_pull_end` = 2026-07-24 |
| Amendments touching the bar | none |
| Corrections applied | Partial-refresh horizon pinned (ADR-005); listing segments computed from full bar history; ties broken on symbol ascending |
| Not covered | **No book was ever compared.** "The recorded formation books at widths 5 and 50 are not stored in the permitted database, so the disagreement gate ran against the recorded universe membership instead" (DECISIONS.md:106-108). The 12-1 momentum ranking — the step that produces the books, the excess return and the whole hypothesis — is re-implemented from prose (DECISIONS.md:99-105) and unverified against the recorded round |
| Framing | Register: "reproduced ... against all 124 recorded formation dates" without the book caveat. Progress: "Reproduced. All 124 recorded formation dates identical" then separately "Books formed at widths 5, 20, 50 for the last 7 formations" (progress.md:209) — formed, not verified. ADR-006 discloses the gap plainly |

## 6. Price reconciliation: "The gap RECONCILES"

| field | content |
|---|---|
| Claim as stated | "The gap RECONCILES as market movement. No stale adjustment exists in the stored series for these 20 names." — reports/stage_b1/price_reconciliation.md:74-75; "The gap RECONCILES. Proceed authorized." — progress.md:118-119 |
| Kind | positive (a hygiene check declared passed, gating the B.1 build) |
| Deciding figures (n) | 20 names checked; 0 splits in 2026; 0 ex-dividends in 2026-07-24 → 2026-08-24; 3 names pay dividends at all, largest 0.37 % of price; ratio of medians 0.7176 (143.89 → 103.25), a 28.2 % gap; per-name ratios run 0.52-1.06 with no split-shaped outlier; two suspicious names (MXL 0.518, WOLF 0.546) checked individually — price_reconciliation.md:27-70 |
| Bar + registration date | B.1 Task 0, 2026-08-24; ADR-016 registered the same day (8c4c3bc, 2026-08-25T00:36:21Z) |
| Amendments touching the bar | none |
| Corrections applied | Named-source check (stockanalysis.com, retrieved 2026-08-24), splits calendar plus per-name pages to close the 2026-07-24 → 2026-08-02 window, a 52-week-range basis cross-check, and a stated falsifier ("a corporate action the public source missed", :81-82) |
| Support limits | Single public source, no stored raw evidence (no HTML, no JSON, no per-name table of ex-dates beyond three names named in prose); the "median close, this check 97.45" row is 19 names plus MU at its A.2 mid because "the MU page fetched was its dividend page" (:60-63) |
| Framing | Register: not mentioned. ADR-016: "the Task 0 reconciliation confirmed the 28 percent A.1-to-A.2 price gap was market movement, not a stale adjustment: zero corporate actions ... checked name by name against a public corporate-actions source" (DECISIONS.md:259-264). Progress: "The gap RECONCILES. Proceed authorized." |

## 7. Measured spread distribution replaces the inherited band (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "Spreads are MEASURED on the real book, not assumed from a band. All 20 names ... median 12.77 bp, p75 17.2, p90 20.7, max 27.4. The inherited 15.8 to 50 bp band predicted the wide end and measured wrong in the favourable direction ... The measured distribution replaces the band." — REGISTRATION.md:170-176 |
| Kind | shipped artifact (reports/stage_a2/book_spreads.json, cost_table.md) |
| Deciding figures (n) | 20 names × 9 cells; 3 sessions (2026-08-19/20/21) × 3 fixed intraday windows (14:00, 16:30, 19:30 UTC); ≤50 quotes per cell; 0 names UNMEASURED; discards crossed 6, locked 88, zero 0, no_size 0 — book_spreads.json:11-15, 138-156. Width-5 sub-figure: **n = 5 names**, median 13.075 bp at median mid 201.91 |
| Bar + registration date | Section 7, registered 2026-08-23 (text) / committed a8f4b0d 2026-08-24T04:40:25Z, alongside the measurement (book_spreads.json `measured_utc` 2026-08-24T04:23:29Z, 17 minutes before the commit) |
| Amendments touching the bar | none. The band it replaced is retained as the unmeasured carry: "Any future unmeasured name carries the band's upper bound of 50 bp, never its middle" (REGISTRATION.md:176-177), enforced at costmodel.py:46-47, 158 |
| Corrections applied | Locked and crossed quotes discarded (biases the median up); the inherited band's **upper** bound, not its middle, held for unmeasured names; entitlement probe with AAPL whose numbers never enter the output |
| Corrections NOT applied | The opening 30 minutes and the closing auction are excluded by the window constants (measure_book_spreads.py:55); the 50-quote limit is un-paginated and unsorted, so each "5-minute cell" is the earliest 50 quotes; measured 7 weeks after the book's formation on names that will differ in any future month; percentile estimator is a floor index (measure_book_spreads.py:153-154) |
| Framing | Register: "MEASURED on the real book" in capitals; "measured wrong in the favourable direction" is stated as the band's error, not as this measurement's optimism. ADR-013 discloses the route and that "Re-measuring near each future formation would change it" (DECISIONS.md:207-215). README: absent |

## 8. The registered cost hurdle, 4.07 bp/day (SHIPPED, load-bearing)

| field | content |
|---|---|
| Claim as stated | "Success when the lower bound clears the measured cost hurdle of 4.07 bp per day, computed at the primary width under the worst-case fractional regime with the measured width-5 spread." — REGISTRATION.md:249-251 |
| Kind | shipped artifact + registered threshold (`cost_hurdle_bp_per_day: float = 4.07`, registered.py:78) |
| Deciding figures (n) | width 5, churn 2.0 names/month (n = 6 formations), per-name notional 180 USD, round trip 213.84 bp = 200.00 commission + 13.08 spread (n = 5 names) + 0.76 regulatory, 21 trading days/month — reports/stage_a2/cost_table.md:36. Recomputed: 4.0731 → 4.07, exact |
| Bar + registration date | Section 11, registered 2026-08-23 (text) / committed a8f4b0d 2026-08-24T04:40:25Z |
| Amendments touching the bar | The 2026-08-25 BLOCKED amendment (669eb5c) proved the fractional regime unavailable through the API and explicitly states "No parameter changes." (REGISTRATION.md:304). Data existing at that entry: the A.1b evidence. The hurdle was left at 4.07 |
| Corrections applied | Worst-case regime chosen; worst-case one-cent TAF floor held; unmeasured names carry the band's upper bound |
| Support | 93.5 % of the figure (200.00/213.84 bp) is an unbilled commission projection from a published web page under a regime the same repository then measured as refused; 0.36 % rests on a floor ACCESS.md:98 calls "CONFIRMED NOWHERE"; 6.1 % is measured. Under the only available regime (whole-share Tiered) the same arithmetic gives 1.00 bp/day |
| Framing | Register: "the measured cost hurdle". Code comment: "computed at registration from the measured cost model under the worst-case fractional regime" (registered.py:71-78) — more accurate. Shipped monitor: "success bar: lower bound above 4.07 bp/day" (reports/monitor/verdict.txt:8, 17, 26) with no regime qualifier. README: absent |

## 9. Annual deterministic drag, 28.76 / 56.84 USD per year (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "Annual deterministic drag at the traded width and measured churn: 28.76 USD per year under whole-share Tiered, 56.84 under fractional." — REGISTRATION.md:184-186 |
| Kind | shipped artifact (reports/stage_a2/cost_table.md:25-32) |
| Deciding figures (n) | width 20, churn 5.2 names/month (n = 6 formations), 10.4 fills/month, notional 45 USD; commission 28.08 / 56.16 + regulatory 0.68. All four rows recomputed exactly from costmodel.annual_commission_drag |
| Bar + registration date | Section 7 / Section 12, 2026-08-23 (a8f4b0d) |
| Amendments touching the bar | none; the fractional row is the one A.1b later showed cannot be executed |
| Corrections applied | Spread deliberately excluded from the drag figure ("it belongs to the measurement", costmodel.py:188-190); regulatory ride on the sell leg only |
| Framing | Register also uses it for the cost of a negative result: "A documented negative is a valid outcome at a cost of roughly 30 to 60 USD a year at the traded width" (REGISTRATION.md:279-280). At the **primary** width the same table gives 86.73 USD/yr under fractional (cost_table.md:32), outside the quoted range |

## 10. The width table: IR 1.062 / 0.975 / 0.894 / 0.798 (SHIPPED, partly interpolated)

| field | content |
|---|---|
| Claim as stated | "The recorded and interpolated width figures, from the two-point power law fit (TE exponent -0.321, excess exponent -0.445)" with rows width 5 / 10 / 20 / 50 — REGISTRATION.md:110-118 |
| Kind | shipped artifact; feeds the primary-width choice, the traded-width choice, the 1.41 signal-clock cost and the kill floor |
| Deciding figures (n) | **n = 2 recorded points** (widths 5 and 50) fitted with a 2-parameter power law → 0 residual degrees of freedom, no uncertainty estimate. Widths 10 and 20 are interpolations. Recomputed exponents −0.3211 / −0.4453, IRs 1.0623 / 0.9747 / 0.8943 / 0.7981 — all reproduce the registered figures |
| Bar + registration date | Section 4 / ADR-009 / ADR-010, 2026-08-23 (a8f4b0d, 23d9ffa) |
| Amendments touching the bar | none. ADR-009: "Changes it: recorded measurements at more widths would replace the two-point fit" (DECISIONS.md:157-158) |
| Corrections applied | Interpolated rows labelled "INTERPOLATED from two-point fit" in the table and in ADR-009 ("labelled as such everywhere they appear"); the anomalous TE exponent registered as a risk rather than smoothed away (REGISTRATION.md:124-129) |
| Downstream use of the interpolated value | The kill floor's sigma and all three touch probabilities are computed from the **interpolated** width-20 TE of 42.54 %/yr (DECISIONS.md:172-179; registered.py:53-55) |
| Framing | Register labels the interpolation honestly; README absent. Progress does not repeat the caveat |

## 11. Kill floor 500 USD = 1.31 sigma, 19 % touch (SHIPPED threshold)

| field | content |
|---|---|
| Claim as stated | "The floor is 500 USD of total account equity, a 400 USD loss on 900 deployed after the 100 buffer, 1.31 sigma of the width-20 tracking error, driftless touch probability near 19 percent in year one." — REGISTRATION.md:216-219 |
| Kind | shipped registered threshold (`restart_floor_usd: float = 500.0`, registered.py:56) |
| Deciding figures (n) | Candidate floors 600 / 500 / 400 → 1.04σ / 1.31σ / 1.57σ and 30 % / 19 % / 12 % (DECISIONS.md:172-179). Recomputed by the reflection principle at TE 42.54 %/yr: 1.045σ/29.6 %, 1.306σ/19.2 %, 1.567σ/11.7 % — all three reproduce |
| Bar + registration date | Section 9 / ADR-011, 2026-08-23 (a8f4b0d, 23d9ffa) |
| Amendments touching the bar | none. "The floor level itself changes only by amendment before the first live order" (DECISIONS.md:189-190); no live order ever existed |
| Corrections applied | Restart-versus-termination distinction enforced in code and mutation-tested (kill.py:29-47; reports/stage_a2/mutation_tests.txt); both neighbouring floors priced and rejected with stated arithmetic; two acknowledged omissions stated: "The figures ignore market beta, which the high-beta book makes optimistic, and ignore positive drift, which cuts the other way" (REGISTRATION.md:221-224) |
| Defect | The parenthetical "a 400 USD loss on 900 deployed" is inconsistent with the 1.31σ / 19 % in the same sentence, which require a 500 USD loss; 400/900 = 1.045σ is the figure ADR-011 assigns to the rejected 600 floor. See all.md DRAFT-all-15 |
| Framing | Register and ADR-011 both state it; registered.py:53-55 states the correct version. README absent |

## 12. Spend cap 100 USD per rolling 365 days (SHIPPED threshold)

| field | content |
|---|---|
| Claim as stated | "Cumulative spend at or above the registered cap of 100 USD per rolling 365 days, about 1.75 times the worst-case fractional projection." — REGISTRATION.md:196-198 |
| Kind | shipped registered threshold (`spend_cap_usd_per_year: float = 100.0`, registered.py:59) |
| Deciding figures (n) | 100 / 56.84 = 1.759 at the **traded** width 20. At the primary width 5 the worst-case fractional projection is 86.73 USD/yr (cost_table.md:32), giving 1.15× |
| Bar + registration date | Section 8 / ADR-013, 2026-08-23 (a8f4b0d, 23d9ffa) |
| Amendments touching the bar | none |
| Corrections applied | Demonstrated in C.1 with a rolling-year query that correctly excludes an out-of-window record (reports/stage_c1/refusals.md:131-151) |
| Framing | Consistent between register and ADR-013; the "1.75×" holds only at the traded width, which is stated ("the worst-case fractional projection of 56.84", DECISIONS.md:217-219) |

## 13. Time-to-verdict projection: 2,061 / 2,852 days (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "Under this exact frozen construction, with the sample mean holding at 27.99, the lower bound clears zero at day 2,061 and clears the hurdle at day 2,852. Eight to eleven years." — REGISTRATION.md:259-262 |
| Kind | shipped artifact; the figure on which "the operator knows this and proceeds" rests (REGISTRATION.md:262-263) |
| Deciding figures (n) | mean 27.99 bp/day, sigma 418 bp/day, rho 0.071641, alpha 0.05. Recomputed exactly: rho 0.07164133, clear-zero 2061, clear-hurdle 2852, pointwise n = 603 vs "about 600 days" |
| Bar + registration date | Section 11, 2026-08-23 (a8f4b0d); constants pinned at registered.py:104-107 |
| Amendments touching the bar | none |
| Assumptions the repository itself flags elsewhere | The mean is the already-spent-holdout maximum over widths (REGISTRATION.md:52, :92-95); `first_crossing_day` is documented as "Planning arithmetic only. It assumes the sample mean sits at mean_bp forever, which no sample does." (verdict.py:123-127). The book-forming step that produced 27.99 was never reproduced (DECISIONS.md:106-108) |
| Framing | Register calls it "The honest arithmetic" and states 8-11 years plainly — the most self-critical framing in the repository. But the shipped monitor prints the **same** 2061/2852 under the width-20 and width-50 headings, where the registered means and TEs give 3,429/6,645 and 4,352/13,178 (reports/monitor/verdict.txt:13-29; see all.md DRAFT-all-11) |

## 14. Bonferroni multiplicity control across three widths

| field | content |
|---|---|
| Claim as stated | "The primary spends alpha 0.05 one-sided. The secondaries spend 0.025 each, Bonferroni, so the family never outspends the primary." — REGISTRATION.md:97-99 |
| Kind | shipped statistical claim (verdict.alpha_for_width, verdict.py:104-116) |
| Deciding figures (n) | 3 registered one-sided success tests; union bound 0.05 + 0.025 + 0.025 = **0.10** experiment-wise, twice the primary's nominal level. "the family" in the sentence excludes the primary |
| Bar + registration date | Section 4 / ADR-010, 2026-08-23 (a8f4b0d, 23d9ffa) |
| Amendments touching the bar | none |
| Corrections applied | The secondary split itself (0.025 each) |
| Framing | Register and the code comment (verdict.py:108-110) state the same, narrower reading; no experiment-wise figure appears anywhere. Shipped monitor renders all three widths with success and futility bars (reports/monitor/verdict.txt:4-29) |

## 15. The DEGRADED branch closed: no live sleeve at this stake (thresholded negative)

| field | content |
|---|---|
| Claim as stated | "The registered consequence of a DEGRADED Task 3 result is therefore NO live sleeve at this stake, not a reduced one." — REGISTRATION.md:156-157 |
| Kind | thresholded negative (a branch closed on a measured threshold) |
| Deciding figures (n) | median width-20 book share price 144 USD "at the last two formations, up from 36 in March and April" (REGISTRATION.md:150); n = 7 recorded formations, 2 used. Stated arithmetic: 20 names ≈ 2,880 USD; 5-name book "720 of 900 deployed"; "per-name prices from 22 to 1,595 USD" |
| Recomputation | From reports/stage_a1/formations.json (2026-07-01): one share of each width-20 name = **7,890.47** USD; one share of each width-5 name = **3,554.82** USD; width-5 price range **48.25-2,273.73**. None of the three stated figures is reproducible; the conclusion survives a fortiori. See all.md DRAFT-all-7 |
| Bar + registration date | Section 0's DEGRADED consequence, registered 2026-08-23 at c4e9817 (22:23:16Z), reads: "per-name notional rises to whole-share size. Book width falls to what 900 USD supports at that size" — a **reduced** sleeve |
| Amendment touching the bar | Section 6 / ADR-012, committed a8f4b0d **2026-08-24T04:40:25Z**, ~6 hours after the deciding measurement landed at 0a0d214 (2026-08-23T22:42:34Z). It re-specifies the consequence to "no live sleeve" and calls the new version "the registered consequence". Data existing at that point: the full A.1 formation and price measurement |
| Ratchet | "A collapse in book share prices does not reopen it, because the branch decision must not track the thing it sizes." (DECISIONS.md:202-204). The same measured series ran 36.47 and 40.59 in March and April, where a 20-name whole-share basket is affordable at the stake |
| Framing | Register presents the post-measurement rule as registered; ADR-012 discloses the measurement that prompted it. README absent |

## 16. Test and mutation evidence (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "Tested. 158 tests green under mypy strict and ruff ... All four required mutations applied to real source, each caught, restored green" — progress.md:92-96 (and 123/76/27 at the earlier stages) |
| Kind | shipped process evidence |
| Deciding figures (n) | Test counts verified by counting `def test_` at each stage commit: 27 (91a1dcb), 76 (23d9ffa), 123 (8c4c3bc), 158 (b4a7a23) — all exact. Mutations: 3 + 2 + 3 + 4 = 12 across reports/stage_a1, a2, b1, c1 mutation_tests.txt |
| Bar + registration date | Stage-prompt requirement, per stage; no registered numeric bar |
| Amendments touching the bar | none |
| Corrections applied | Mutations applied to real source and restored; the structural guard test requires every registered threshold to have a consumption site outside registered.py (registered.py:1-6) |
| Caveat | I did not execute the suite (running an audited repository's code in place is out of bounds), so "green" is not independently verified; the counts are |
| Framing | Progress states counts and mutation outcomes per stage; register does not reference them |

## 17. The eight-refusal order gate and the read-only probe (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "Demonstrated. All eight refusals produced with named arithmetic against the real 2026-08-03 width-20 formation ... Nothing places an order, paper or live." — progress.md:69-77 |
| Kind | shipped artifact (src/hfexperiment/gate.py, gatewire.py, intents.py, ibkrprobe.py; reports/stage_c1/refusals.md, demo_ledger.jsonl) |
| Deciding figures (n) | 20 intents, 34 refusal records, 1 would_submit, 3 spend records (refusals.md:339); 8 refusal reasons + 3 construction-wall refusals; formation hash 0b28a5cfda7516fa reproduced (self-reproduction, same code and store) |
| Bar + registration date | Section 8 (seven refusals), registered 2026-08-23 (a8f4b0d); refusal 8 (account pin) added by ADR-018 at C.1, 2026-08-25 (b4a7a23) under Section 8's clause "Stage C.1 wires it to the append-only spend ledger and may add refusals by amendment, never remove one" (REGISTRATION.md:204-206) |
| Amendments touching the bar | none to the registered seven |
| Corrections applied | Four mutations applied and caught (pin deleted, empty account passing as default, SmartRouting bypassed, deferred parameter read as 45.0) — reports/stage_c1/mutation_tests.txt |
| Timing note | The gate prices fractional orders only (demo quantity 0.037 of SNDK, refusals.md:289) and was demonstrated at 2026-08-25T02:40:23Z, 25 minutes before A.1b measured that channel as refusing fractional orders. progress.md:17 nonetheless records "Stages A.1 through C.1 complete and green" |
| Framing | Progress and ADR-020/ADR-021 state it accurately; register describes the gate's obligations. README absent |

## 18. Monitor views (SHIPPED)

| field | content |
|---|---|
| Claim as stated | "The health view and the verdict view are structurally separated ... The verdict view shows only the confidence sequence against its two registered bars." — REGISTRATION.md:266-270 |
| Kind | shipped artifact (reports/monitor/health.txt, verdict.txt; src/hfexperiment/monitor.py) |
| Deciding figures (n) | 0 observations in every width block; the pre-start state renders honestly ("observations: 0", "bounds: none, the series has not started") |
| Bar + registration date | Section 12 / ADR-017, 2026-08-24 (8c4c3bc) |
| Amendments touching the bar | none |
| Corrections applied | Render-failing allowlist guard on the verdict view, mutation-tested (accrual row in the verdict view — reports/stage_b1/mutation_tests.txt) |
| Defect | The projection line is the width-5 constant repeated under all three widths (see entry 13 and all.md DRAFT-all-11) |
| Framing | Register and ADR-017 accurate; health.txt honestly records "credentials: ... does not exist. BLOCKED-ON-OPERATOR" and "last run: never" |

## 19. Open hypotheses / open items at the anchored SHA

| item | status as stated | file:line | should it have closed on its own rule? |
|---|---|---|---|
| Amendment 1 (per_name_notional_usd, broker_min_notional_usd, mixed_order_billing_regime) | "Amendment 1 is reserved for the deferred parameters of Section 5 and must land before the first live order." | REGISTRATION.md:273-274; registered.py:109-133 | No — no live order ever existed, so it correctly never landed. But `broker_min_notional_usd`'s stated reason ("a live-permissioned account that does not exist yet", registered.py:119-120) is stale twice over: the account exists and A.1b already read MinSize/SizeIncrement for all 20 names (ACCESS.md:196) |
| Billing plan of a SmartRouted API order on a real paper fill | "**RUNNABLE** ... The one sub-test still worth running" | docs/ACCESS.md:199; progress.md:268-271 | It is the only registered sub-test never resolved and never run, left open by an ADR whose stated purpose was record hygiene: "the billing-plan sub-test is runnable and unscheduled" (progress.md:268-269). Its output would move the commission term that is 93.5 % of the registered cost hurdle |
| B.1a paper-api fix | "B.1a cancelled as moot: no formation will ever call the assets endpoint." | progress.md:19-20 | Closed by the experiment's closure, not by its own rule. The trace behind it ("nightly runs succeed until 2026-08-31") is contradicted by daily_run.py:120 — see all.md DRAFT-all-5 |
| Read-Only API re-check in the Gateway | "Open. Operator re-checks Read-Only API in the Gateway" | progress.md:51-53 | Left open; A.1b turned it off by behaviour and ADR-026 reaffirms "leaves Read-Only API on outside a registered order test" (DECISIONS.md:475-476). No record of the re-check |
| Benchmark missing-member handling vs the recorded round | "if the recorded round differed, correct before 2026-09-01" | progress.md:149-150; DECISIONS.md:277-285 | Never checked; superseded by closure. The benchmark's daily-rebalancing convention is asserted to match the recorded round (benchmark.py:6-13) and was never verified |
| Registered prior 0.15 | "the operator confirms or replaces that number at acceptance" (REGISTRATION.md:277-278); recorded as "accepted by operator delegation ... The act of running the B.1 stage prompt was the acceptance" (DECISIONS.md:232-235) | REGISTRATION.md:286-295; DECISIONS.md:230-242 | Closed by inference from an action, not by an explicit operator statement. Data existing at acceptance is stated correctly (A.1 reproduction, A.2 spreads, zero shadow observations) |

## 20. Thresholded negatives whose verdict rested on a bar

| verdict | bar | deciding figure (n) | file:line |
|---|---|---|---|
| BLOCKED (Section 0) | "accepts fractional quantities through that API at 45 USD per name" | 4 fractional orders refused, 1 whole-share accepted (n = 5) | REGISTRATION.md:16-17, 299-302 |
| DEGRADED closed | whether 900 USD supports a whole-share book at the measured median share price | median 144 USD at the last 2 of 7 formations | REGISTRATION.md:149-159 |
| Futility bar (never reached) | "Futility when the upper bound falls below 10 bp per day" | 0 observations | REGISTRATION.md:252-253; registered.py:70 |
| Success bar (never reached) | lower bound above 4.07 bp/day | 0 observations | REGISTRATION.md:249-251; registered.py:78 |
| "BLOCKED is ruled out on documented bars" (A.1, superseded) | residency + US equities + order API at one broker | 4 brokers surveyed, 8 cited sources, 0 tested | DECISIONS.md:39-45; docs/ACCESS.md:9-42 |
