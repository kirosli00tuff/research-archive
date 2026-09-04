# Agent A — PMExperiment, part p1-register — draft findings

Repository: PMExperiment, anchored SHA `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project).
Assigned primary documents: `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `report.md`, `README.md`.
All content read from SNAP; the live repo was touched read-only for `git log` / `rev-parse` / `status` only (see access log at the end).
Recomputations run with the audit venv; script at
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentA-PM-p1/recompute.py`.

**Framing, stated once so no finding is misread.** This repository never measured anything against H1
and says so on nearly every page. Its access verdicts are documented, dated and quoted, and I am not
challenging the fact that no calibration statistic exists. What I challenge is narrower and is the
Direction-A question: the *terminal* label and the *decision to stop* rest on (a) a "the band is
already thin" characterisation whose thinness is produced by two registered assumptions the
registration itself names as overstating cost, (b) a "the power question would still be unanswered"
claim contradicted by the registration's own Section 0.5 derivation, and (c) a closure whose
"exhaustive" reopening list drops one registered reopening path and pre-declares the only possible
trigger of another to be a non-reopening.

---

### DRAFT-p1-register-1
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** H1 / the BAND-OPEN "thin band" figure used as the stated input to Amendment 7's decision to decline the entity path and close the project
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| **forming a personal legal entity** | **declined — disproportionate** | the cost is out of proportion to a stated prior of 5 to 8 percent, against a band verdict already recorded as thin |" — PMExperiment/REGISTRATION.md:1046; and the figure that makes it thin, "Every magnitude any cited source places inside that bucket — Bürgi's **2.0** and **3.0** points — **fails** the cost floor of **0.0300**" — PMExperiment/REGISTRATION.md:1052-1053
- **Evidence:**
  - The cost floor is built from two registered assumptions. The venue-fee row registers "**2 cents per contract per side, both sides counted: 4 cents round trip**" and, in the same cell, records the venue's actual published schedule: "Kalshi's published taker schedule is $0.07·P·(1−P) per contract rounded up (≈ 1.77 % of price at 50c, ≈ 0.33c at 5c), and settlement carries no fee, so the flat 4c **overstates** the venue cost at every price, most severely at the tails. Bias: against H1 surviving costs." — PMExperiment/REGISTRATION.md:199.
  - The FX row registers 1.5 % per direction and records: "**Overstates** low-cost channels (multi-currency brokers, Norbert's gambit ≈ 0.2–0.5 %)" — PMExperiment/REGISTRATION.md:201.
  - The decisive published figure is stated as fee-plus-spread alone: "| fee + half-spread alone, held route, before any FX | **0.0300** — already above the registered band bottom of 0.0200, at every price and on every route |" — PMExperiment/HYPOTHESES.md:140; restated as "**No FX treatment, no venue price and no exit route reaches the bottom of the band.**" — PMExperiment/REGISTRATION.md:459 and PMExperiment/report.md:107-108.
  - The only sensitivity the repository actually ran is the FX turnover k, and Amendment 4 records that it is chosen precisely because it does not change the verdict: "**It does not decide the verdict.** Computed both ways in Task 4, the band's top clears the required underpricing at all ten registered buckets on both exit routes at k = 1, at k = 12 and in the k → ∞ limit" — PMExperiment/REGISTRATION.md:820-824. The two assumptions that *do* move the verdict — the fee schedule and the FX channel — are named in Section 2 with their direction of bias and are never varied anywhere in the repository (grep over the snapshot returns the Section 2 row and its verbatim copy in `docs/BAND.md:74`, and nothing else).
  - n for the challenged magnitudes: Bürgi's 2.0 and 3.0 points come from "313,972 Yes-and-No contract prices on 46,282 contracts across 12,403 events" — PMExperiment/REGISTRATION.md:227-228.
- **Recomputation (if any):**
  - Inputs: held-route floor C_H(p,k) = fee + half-spread + 0.03·p/k, from PMExperiment/REGISTRATION.md:206 (C(p) = 0.04 + 0.01 + 0.03·p, four-cent round-trip form), PMExperiment/REGISTRATION.md:335 (C(p) = 0.05 + 0.03·p) and PMExperiment/REGISTRATION.md:799 (FX(p) = 0.03·p/k). Verified against the registered outputs: C_H(0.91)=0.05730, C_H(0.95)=0.05850, C_H(0.99)=0.05970 — reproducing "5.73 points at 91c rising to 5.97 at 99c" and the 5.85 headline at PMExperiment/REGISTRATION.md:422-424.
  - Kalshi's published schedule, taken verbatim from PMExperiment/REGISTRATION.md:199: 0.07·P·(1−P) at P = 0.95 is $0.003325 (0.33c), rounded up to the cent $0.01 — i.e. **half** the registered 2c per side, and settlement carries no fee, so the held route pays it once.
  - Held-route floor at p = 0.95 under the venue's own published fee (rounded up to $0.01) and the registered 3 % FX: **0.04850** at k = 1 (Bürgi's 0.030 still fails by 1.85 points) and **0.02237** at k = 12 (Bürgi's 0.030 **clears by 0.76 points**). Under the registered flat 2c the same k = 12 floor is 0.03238 and 0.030 fails by 0.24 points. **The k = 12 verdict flips on the fee assumption alone.**
  - Held-route floor at p = 0.95 under the published fee (rounded) and the Section 2-named Norbert's-gambit channel at 0.4 % round trip, at the **binding** k = 1: **0.02380** — Bürgi's 0.030 **clears by 0.62 points**. With the fee unrounded ($0.003325) the floor is 0.01713 and it clears by 1.29 points.
  - The "0.0300 fee-plus-spread floor is already above the band bottom of 0.0200 at every price and on every route" claim: under the published schedule rounded up to the cent, fee + half-spread = 0.01 + 0.01 = **0.02000 exactly** — a tie with the band bottom, not "above" it; unrounded it is 0.01333, i.e. **below** the band bottom by 0.67 points.
  - Honest counter-weight, recomputed and reported: Section 2 also records that the 1c half-spread "likely **understates** the cost at the illiquid tails" where "Tail books on the platform are typically 1–3c wide" (PMExperiment/REGISTRATION.md:200). Pushing the half-spread to 1.5c with the published fee and Norbert's-gambit FX at k = 1 gives a floor of 0.02880 and Bürgi's 0.030 clears by only **0.12 points**. So the reversal is real but not robust to the spread caveat, and I say so.
- **What would resolve it:** a one-paragraph sensitivity table in `docs/BAND.md` computing the band under (i) Kalshi's published taker schedule and (ii) the two FX channels Section 2 already names, reported beside the registered case exactly as k = 12 and k → ∞ already are — or an explicit statement in Amendment 7 that "thin" is a property of the registered assumptions and not of the venue's actual cost. Neither requires any venue access, any data, or any money.
- **Confidence:** MEDIUM — the arithmetic is certain and every input is quoted from the registration itself, but the registration deliberately binds its assumptions and the operator prompt at PMExperiment/progress.md:330 forbade proposing "a different fee assumption … to rescue an empty band" (the band was not empty, so the prohibition does not literally reach this, but it explains the omission).
- **Invalidated by later commits?:** no — the live repo's HEAD at read time (2026-09-04T00:26:41Z) is the anchored SHA and the working tree is clean; the project is declared closed and Amendment 8 forbids recomputing the band (PMExperiment/REGISTRATION.md:1107-1108).
- **Disclosed by authors?:** partly (PMExperiment/REGISTRATION.md:199, 200, 201) — Section 2 discloses both assumptions, names the published schedule, and names the direction of bias as "against H1 surviving costs". What is **not** disclosed anywhere is the magnitude: no document computes the floor under the venue's published schedule, and the "every cited magnitude fails" sentence that feeds the abandonment decision is stated at PMExperiment/REGISTRATION.md:1052-1053, PMExperiment/report.md:419-420 and PMExperiment/README.md:145-149 without it.

---

### DRAFT-p1-register-2
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the power gate, verdict cell U24 (unrestricted universe at the S24 snapshot)
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Even if an authorization arrived tomorrow the power question would still be unanswered**, and nothing in five stages has moved it. That is the honest end of it." — PMExperiment/report.md:483-485; same claim at PMExperiment/DECISIONS.md:740-741 ("**If an authorization arrived tomorrow, the power question would still be unanswered.**") and PMExperiment/README.md:191-192.
- **Evidence:**
  - The registration derives the answer for the unrestricted cell in advance, inside the access gate: "3. At least 1,000 settled markets are enumerable in total. At the published two-thirds tail share, GO needs about 703 markets (475 / 0.676); the floor of 1,000 leaves margin for a lower realized share." — PMExperiment/REGISTRATION.md:148-150.
  - And again in Section 0.4: "The published benchmark (Section 3) reports two-thirds of its 313,972 contract prices in the 1–10c and 90–99c bands, so the unrestricted universe reaching 475 tail contracts is **expected**. **Whether the Canadian-permitted subset retains even 30** is precisely the open question this gate exists to answer" — PMExperiment/REGISTRATION.md:133-136 (emphasis in the "expected"/"even 30" contrast is mine; the words are verbatim).
  - The MDE formula and bars: "MDE = z · sqrt(v̄ / n_T)" with z = 2.0 — PMExperiment/REGISTRATION.md:101 and 301; GO at MDE ≤ 0.02, BLOCKED at MDE > 0.08 or n_T = 0 — PMExperiment/REGISTRATION.md:110-112; planning dispersion v̄ ≈ 0.0475 and the derived bars "GO, MDE ≤ 0.02 | ≥ 475" and "stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30" — PMExperiment/REGISTRATION.md:123-129.
  - The benchmark's own counts, n = 313,972 prices on 46,282 contracts, with two-thirds in the tail bands — PMExperiment/REGISTRATION.md:227-234.
  - Section 15.4 records that the depth blocker is not a property of the archive: "historical depth on the licence | **2021 onward, through historical endpoints**, expressly not subject to the live-data cutoff" — PMExperiment/REGISTRATION.md:538.
- **Recomputation (if any):**
  - MDE = 2·sqrt(0.0475 / n_T), inputs from PMExperiment/REGISTRATION.md:101 and :123-124.
  - n_T = 676 (the registered access floor of 1,000 settled markets × the published 0.676 tail share, both from PMExperiment/REGISTRATION.md:148-150): MDE = **0.01676 → GO**.
  - n_T = 703 (the registration's own 475/0.676): MDE = 0.01644 → GO.
  - n_T = 30,855 (two-thirds of the benchmark's 46,282 contracts): MDE = **0.00248 → GO**.
  - n_T = 209,315 (two-thirds of the benchmark's 313,972 prices): MDE = 0.00095 → GO.
  - Inverting the BLOCKED bar: BLOCKED (MDE > 0.08) requires n_T < **29.69**, i.e. fewer than **44 qualifying markets** at the published 0.676 tail share. Against a registered access floor of 1,000 markets, a U24 BLOCKED is excluded by the access condition alone.
  - Conclusion: for U24 the power question is not open in any meaningful sense — clearing the registered access condition 3 *entails* GO at planning dispersion, and the registration says so at :148-150. What is genuinely unanswered is P30, the Canadian-permitted cell, exactly as :135-136 says.
- **What would resolve it:** replacing the three unqualified sentences with the split the registration already makes — "the U24 power question is expected to clear on the published tail share (Section 0.5); the P30 power question, which is the one this design exists to answer, is unanswered" — or, if the authors mean "no *realized* MDE exists", saying that instead, since it is true and much weaker.
- **Confidence:** MEDIUM — the arithmetic and the quoted derivation are certain; the charitable reading is that "the power question" means "a realized MDE from this repository's own enumeration", which is genuinely absent. But the sentence is stated three times without that qualification and with "nothing in five stages has moved it", which Section 0.5 contradicts on its face.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA and the project is closed.
- **Disclosed by authors?:** no — the registration's own derivation at PMExperiment/REGISTRATION.md:133-136 and :148-150 is never cited in the closure paragraphs at PMExperiment/report.md:483-485, PMExperiment/DECISIONS.md:739-744 or PMExperiment/README.md:190-192, and none of the three distinguishes U24 from P30.

---

### DRAFT-p1-register-3
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the Polymarket PENDING_ACCESS verdict of 2026-08-30 as it reaches the on-chain (Polygon) route, and Amendment 9's foreclosure of that route
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "| Polymarket | **PENDING_ACCESS** | Terms effective 2026-08-11 prohibit the data-gathering tool class, expressly including on-chain | 2026-08-30 |" — PMExperiment/README.md:116; identically at PMExperiment/REGISTRATION.md:598 and PMExperiment/HYPOTHESES.md:174; and restated as the ground of Amendment 9: "The prohibition on data mining tools, robots and crawlers carries **no entity-type qualification**, and the data clause reaches material taken **directly, through an API, or by any other means, including on-chain**." — PMExperiment/REGISTRATION.md:1134-1136.
- **Evidence:** the two properties that sentence conjoins belong to two different clauses, and the same registration says one of them does not bind this operator.
  - The clause that reaches on-chain is the **Data clause** — "the Data clause defines its subject as data 'contained on our Site, any Interface or Features **directly or through an API, or any other means, including on-chain**'" — PMExperiment/REGISTRATION.md:952-955.
  - Six paragraphs later the same amendment records: "**One clause that does not bind, recorded for accuracy.** The Data restriction is conditional on entity type: it prohibits access by 'a non-retail, professional entity that engages in capital markets activities' or by 'a market data distributor'. A Canadian retail individual conducting measurement-only research is neither, so that clause is **not** the ground of this finding. The data-mining and crawlers prohibition carries no such condition, and it is." — PMExperiment/REGISTRATION.md:967-972.
  - The clause that does bind — the crawlers bullet — is scoped, and the repository's own verification pass measured that scope against a public ledger: "the bullet is scoped to 'the Site, any other Interface, or Features', and **a public Polygon ledger is none of the three on its face**, so Amendment 6's Polygon question stays open rather than being closed here." — PMExperiment/DECISIONS.md:426-428.
  - Amendment 6 leaves the route explicitly open: "or a Polygon read performed through infrastructure that is not a Polymarket Interface, under a legal analysis this repository has not done. The third is recorded as an open question, **not** as a workaround adopted now." — PMExperiment/REGISTRATION.md:1002-1005.
  - Net: on the repository's own two readings, the binding clause does not on its face reach a public Polygon ledger and the clause that does reach it does not bind a Canadian retail individual. The three summary rows and Amendment 9 nonetheless state an on-chain prohibition without either qualification, and Amendment 9 uses that conjunction to hold the verdict "exactly where it stands" (PMExperiment/REGISTRATION.md:1138).
- **Recomputation (if any):** none — this is a documentary inconsistency, not an arithmetic one.
- **What would resolve it:** either (a) restate the three route-ledger rows and Amendment 9 as "the binding clause is scoped to the Site, Interfaces and Features; whether it reaches a public Polygon ledger is UNRESOLVED, and the on-chain reach comes only from a clause this repository has recorded as not binding it", or (b) perform the legal analysis Amendment 6 says was not done and record its result. (a) costs one edit and no access.
- **Confidence:** HIGH — all four quotations are verbatim from the anchored snapshot and none of them is qualified where the summary rows are written.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA; Amendment 9 (commit 03d16e7, 2026-09-02) is the last word on this and is the document that restates the conjunction.
- **Disclosed by authors?:** partly — the two components are each disclosed (PMExperiment/REGISTRATION.md:967-972 and PMExperiment/DECISIONS.md:426-428), and ADR-013 explicitly leaves the Polygon question open. No document notices that the summary rows and Amendment 9 assert the conjunction the components deny, and `tests/test_honesty.py:599-601` pins "This amendment does not reopen H1" as a passing assertion over it.

---

### DRAFT-p1-register-4
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** H1 / Section 15.1's registered Kalshi reopening paths versus Amendment 8's "exhaustive" reopening list
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**The reopening conditions, stated precisely and exhaustively.** Each is an operator action, and none is a measurement:" — PMExperiment/REGISTRATION.md:1082-1083 (followed by three conditions at :1085-1098, none of which is the account path).
- **Evidence:** a registered reopening path whose only stated obstacle expired on day 2 of 5, and which the "exhaustive" list silently drops.
  - Section 15.1 registers three Kalshi reopening paths on 2026-08-29: "**What would reopen access:** written authorization from Kalshi for systematic retrieval and AI-mediated analysis, or a Kalshi-sanctioned bulk research channel not requiring an account, **or an operator decision to register an account — which ADR-002 currently excludes.**" — PMExperiment/REGISTRATION.md:395-398. Restated in the register at PMExperiment/HYPOTHESES.md:33-35 and in ADR-006 at PMExperiment/DECISIONS.md:111-114 ("an operator reversal of ADR-002 by numbered amendment").
  - The obstacle is lifted the next day, by a numbered amendment: "The registration previously admitted only a measurement question. It now admits a terminal question of whether a tradeable edge exists that survives Canadian retail cost. **The operator has stated that account creation is acceptable.**" — PMExperiment/REGISTRATION.md:754-757 (Amendment 3, made 2026-08-30). Same at PMExperiment/DECISIONS.md:182-183 (ADR-008): "account creation is acceptable to him."
  - The path is the one the benchmark study itself used: "The published benchmark study reached this data by registering an account — the path ADR-002 excludes." — PMExperiment/DECISIONS.md:97-98. That study is the source of the 313,972 prices on 46,282 contracts that set the registered effect band (PMExperiment/REGISTRATION.md:227-228).
  - No document after 2026-08-30 revisits it. A grep of the whole snapshot for `ADR-002`, `account creation`, `register an account` and `reversal of ADR-002` returns exactly six hits, all listed above plus `docs/ACCESS.md:64`; none is dated after 2026-08-30 and none records that the third reopening path is now unobstructed or why it should be dropped.
  - Amendment 8 (2026-09-02) then lists three conditions and calls them exhaustive; Amendment 9 adds a fourth (Polymarket licence, PMExperiment/REGISTRATION.md:1163-1167). The account path appears in none of the four.
- **Recomputation (if any):** none — documentary.
- **What would resolve it:** one line in Amendment 8 saying either "the account path of Section 15.1 is dropped because Kalshi's Data Terms condition systematic retrieval and AI-mediated use on written authorization regardless of account status, so an account does not cure condition 5", or "it survives as reopening condition 5, unobstructed since Amendment 3". Either is free; the register currently does neither and asserts exhaustiveness.
- **Confidence:** HIGH — every quotation is verbatim, the dates are the documents' own, and the grep is exhaustive over the snapshot.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA and Amendment 8/9 are the final commits.
- **Disclosed by authors?:** no — the expiry of the ADR-002 obstacle is recorded (PMExperiment/REGISTRATION.md:756-757) and the reopening path is recorded (PMExperiment/REGISTRATION.md:398), but no document connects them, and Amendment 8's exhaustiveness claim is stated without reference to Section 15.1's third path.

---

### DRAFT-p1-register-5
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** H1 / Amendment 8 reopening condition 2, "an academic tier offered by Kalshi, if one is"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "**A reply to the pending academic-tier question is not a reopening.** If one arrives, it is **a one-line register update** recording what it said — nothing more. Only condition 1, 2 or 3 actually being **satisfied** reopens anything" — PMExperiment/REGISTRATION.md:1100-1102; the same rule in the register at PMExperiment/HYPOTHESES.md:318-321 and in README at PMExperiment/README.md:164-166.
- **Evidence:**
  - Condition 2 as registered is about the *existence of an offer*, not about a grant: "2. **An academic tier offered by Kalshi, if one is.** A question about one is **pending** with the institutional desk and unanswered as of 2026-09-02. Its existence is **UNMEASURED** — not absent, not assumed." — PMExperiment/REGISTRATION.md:1092-1094.
  - The pending reply is the only instrument that can measure that existence: the question is with the desk, unanswered, and the repository sends no further requests ("Stage E sent **zero requests** to Kalshi or to any other host" — PMExperiment/REGISTRATION.md:526-527). So the register simultaneously (i) makes the existence of an academic tier a reopening condition, and (ii) pre-declares the only evidence that could establish that existence to be "nothing more" than a one-line update.
  - The foreclosure is hardened into the test suite, not left as prose: ADR-018 lists the mutations the suite must catch, including "**when a pending reply is promoted into a reopening**" — PMExperiment/DECISIONS.md:713. The test exists: `tests/test_honesty.py:471-476`, `test_a_reply_to_the_pending_question_is_not_a_reopening`, asserting `"not a reopening" in doc` across the closing documents. A future session that reads a reply saying "yes, we run an academic tier" and treats condition 2 as satisfied will fail the suite.
  - Context: this is the same repository whose own Stage D completeness caveat was vindicated within two days by an unsolicited desk reply — "**Two days later a route surfaced that Stage D had not read.**" (PMExperiment/DECISIONS.md:575). The instrument that overturned the previous terminal state is exactly the instrument class now pre-declared non-reopening.
- **Recomputation (if any):** none — documentary.
- **What would resolve it:** distinguish the two acts in the text: a reply confirming a tier **satisfies condition 2** (and therefore reopens under Section 16 as a new numbered firing), while *applying for and being granted* the tier is the separate operator action. As written, the register's own condition 2 and its "not a reopening" rule cannot both be true of the same reply.
- **Confidence:** MEDIUM — a charitable reading is that "offered" means "offered *to this operator*, i.e. granted", in which case the two sentences are consistent; but the text says "if one is", the status is "existence is UNMEASURED", and no document draws the distinction.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA; a reply arriving after 2026-09-02 would be the trigger this finding concerns, not an invalidation of it.
- **Disclosed by authors?:** no — both sentences are printed adjacently and the tension is never named; the mutation guard at PMExperiment/DECISIONS.md:713 treats the stricter reading as the invariant to protect.

---

### DRAFT-p1-register-6
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the BAND-OPEN surviving region, and Amendment 8's permanent restriction of any reopened power gate to 91–99c
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "the eight non-tail deciles are excluded because no effect magnitude is registered outside the tail cell" — PMExperiment/REGISTRATION.md:426-427; with the consequence made permanent at "A reopened measurement starts at the power gate over 91–99c held to resolution and **no other region**, exactly where Stage C left it." — PMExperiment/REGISTRATION.md:1110-1111.
- **Evidence:**
  - The repository's own direction analysis places the only clearing magnitude in the excluded 81–90 decile: "| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 |" — PMExperiment/DECISIONS.md:250 (ADR-009), reproduced at PMExperiment/README.md:88.
  - The register states the same: "| the only cited magnitude that clears | Krause's **0.077**, at an exploitable entry price of **0.883** — the 81–90 decile, outside the registered tail cell, **n not recorded anywhere** |" — PMExperiment/HYPOTHESES.md:144; and Section 15.2: "The only cited magnitude large enough to clear is Krause's 7.7 points, whose exploitable entry price is 88.3c — the 81–90 decile, outside the tail cell the band is registered for." — PMExperiment/REGISTRATION.md:437-439.
  - So the 8.00-point band top — the sole reason BAND-OPEN fires at all ("the band survives on its top alone", PMExperiment/REGISTRATION.md:621) — is set by a source whose exploitable price sits in a decile the same verdict excludes from measurement, permanently.
  - n: Krause's n "appears nowhere in this repository" (PMExperiment/report.md:119; PMExperiment/DECISIONS.md:266-270). That is a real weakness of the top and I do not dispute it — it is a reason to *measure* the 81–90 decile, not to bar it.
- **Recomputation (if any):**
  - Inputs: C_H(p) = 0.03 + 0.03·p at k = 1 (PMExperiment/REGISTRATION.md:206, 335, 799); Krause 0.077 at p = 0.883 (PMExperiment/DECISIONS.md:250).
  - C_H(0.883) = **0.05649**; margin = 0.077 − 0.05649 = **+0.02051**, i.e. the only cited clearing magnitude clears the registered held-route floor at its own price by **2.05 points**, at the binding k = 1.
  - Round trip: C_X(0.883) = 0.07649; margin = **+0.00051**, which is smaller than the 0.00195 by which Section 2's FX base is recorded as understating cost (PMExperiment/REGISTRATION.md:847-849) — so the round-trip clearing is inside its own slack and should not be relied on. The held-route clearing is not.
  - This matches `docs/BAND.md:253` ("Krause, sub-30c/4.0 % → NO at 88.3c | 0.883 | 0.077 | 0.0565 **clears** | 0.0765 **clears** | 0.0300 **clears**"), which is another reader's document; the recomputation is included so the figure travels with this finding.
- **What would resolve it:** a numbered amendment extending the power gate's admissible region to the 81–90 decile *for the reopened case only*, on the ground the repository already records — that the band's top is attributed there — or an explicit statement in Amendment 8 that the reopened gate is barred from the only bucket where a cited magnitude clears, and why that is the right trade.
- **Confidence:** MEDIUM — the exclusion is faithful to Section 3, which registers the band in the tail cell and forbids narrowing or widening it after the fact; the finding is that faithfulness here produces a permanent bar on the one bucket the repository's own arithmetic says clears, and no document weighs that.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA and Amendment 8 forbids recomputation.
- **Disclosed by authors?:** yes, in part — the scope mismatch is disclosed at PMExperiment/DECISIONS.md:258-264 ("Krause's exploitable complement at 88.3c lands in the 81–90 decile, outside that cell. The band is **not narrowed** on this ground … but the mismatch is stated wherever the band's top carries a conclusion") and the clearing arithmetic is in `docs/BAND.md:209, 253`. What is disclosed nowhere is the consequence for reopening: that Amendment 8:1110-1111 permanently excludes that decile from any future measurement.

---

### DRAFT-p1-register-7
- **Repository / SHA:** PMExperiment / 03d16e71dbf25a86c529884662d02136f8e82334
- **Hypothesis or artifact:** the Stage D licence closure ("no candidate returns PERMITTED") carried unchanged into the 2026-09-02 terminal verdict, and reopening condition 3
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**unmeasurable** | every route to the records either prohibits the reading, cannot show it is permitted, or requires standing this operator does not have" — PMExperiment/REGISTRATION.md:586 (Section 15.5, 2026-09-02); with the underlying licence row at "published **academic datasets** | **UNMEASURED** | … **no date is printed on the card or in the CC BY 4.0 legal code**" — PMExperiment/HYPOTHESES.md:218.
- **Evidence:**
  - The single element that failed the leading dataset candidate is a printed date, and the repository names the document class that carries one by construction and records that it never fetched it: "**What the stage did not read is stated, because a sampled space is not an enumerated one.** Versioned repository deposits — Zenodo, Dataverse, OSF, figshare — were never fetched, and a DOI landing page prints a licence, a date and a version *by construction*. The dataset candidate therefore reached UNMEASURED on the effective-date element **without fetching the one document class that carries that element by construction.**" — PMExperiment/report.md:306-311; same at PMExperiment/HYPOTHESES.md:233-238.
  - Cost of the omitted step: a single HTTP GET of a DOI landing page — the same act the repository performed four times for `robots.txt` on 2026-08-30 (PMExperiment/REGISTRATION.md:477-478). It is set against the path that was actually weighed and declined: forming a legal entity with formation documents and beneficial-owner verification (PMExperiment/REGISTRATION.md:536, 1046).
  - The closure two days later does not revisit it. Reopening condition 3 remains "**A licensed dataset whose licensor held authority to license.**" — PMExperiment/REGISTRATION.md:1095-1098 — i.e. the register keeps a dataset route open as a reopening condition while never having sampled the class most likely to satisfy the element that closed the last candidate.
  - The repository's own answer to this — "Curing the date would not open it: the chain of title, the grant's own limits, and an unrun AI-clause search all survive the fix" (PMExperiment/report.md:331-332) — is about the *same* candidate (`TimeSeventeen/Polymarket-v1`). It does not reach a different, author-deposited corpus with a different chain of title, which is what the unfetched class would contain.
  - Context that raises the stakes rather than lowering them: the identical completeness caveat on the *venue* side was vindicated within two days (PMExperiment/DECISIONS.md:570-579, "**Two days later a route surfaced that Stage D had not read.**"). The dataset-side caveat was left unacted-on through the closure.
- **Recomputation (if any):** none — documentary.
- **What would resolve it:** four DOI-landing-page fetches (Zenodo, Dataverse, OSF, figshare searches for prediction-market settlement corpora), each recorded under ADR-012's three elements, before the register asserts that every route fails. Zero dollars, no account, no venue contact.
- **Confidence:** MEDIUM — the omission is squarely disclosed by the authors and the direction of its bias is named by them; my addition is only that the terminal verdict of 2026-09-02 states an "every route" quantifier over a space the same repository says was sampled rather than enumerated, in the one class it identified as most likely to pass.
- **Invalidated by later commits?:** no — HEAD is the anchored SHA and the project is closed.
- **Disclosed by authors?:** yes (PMExperiment/report.md:306-314; PMExperiment/HYPOTHESES.md:233-238; and `docs/LICENCES.md:674` calls it "**the sharpest gap**"). The authors disclose the unfetched class and name the bias direction as fail-closed. This finding is therefore READ and capped at S3, and it adds only the observation that the closure three days later did not act on the disclosure while asserting an exhaustive quantifier.

---

## What I checked and found sound

Each of these was a place where the Direction-A thesis would have bitten if the record were weaker. It is not.

1. **The Stage A access verdict as a whole** (PMExperiment/REGISTRATION.md:371-400). The decisive condition is 5, the terms, and ADR-006 says so explicitly ("The decisive one is condition 5", PMExperiment/DECISIONS.md:89-90). Conditions 3 and 4 fail closed on thin evidence — condition 4 rests on "0 daily candles on the **one** ≥ 30-day-old market tested" (:381), n = 1, and condition 3 is "NOT MEASURED" (:380) — but neither is load-bearing and the registration says which condition decided it. I do not raise an n = 1 blocker as a finding when the document already says the blocker did not decide anything.
2. **The Kalshi depth blocker's later expiry is handled correctly.** Section 15.4 records 2021 depth on the licence (:538) and ADR-016 checks the wording of the earlier claim against it: "Stage A wrote that the 2021→Apr 2025 span is *'not reproducible keylessly'* — a claim about the keyless surface, not about the archive — and that phrasing is exactly right under the reply. **Had it been written as 'the history does not reach 2021' it would now be false.**" (PMExperiment/DECISIONS.md:621-626). That is the expired-blocker check performed by the authors on themselves, correctly.
3. **The BAND-OPEN label is not inflated.** Everywhere it appears it carries "It must not be written anywhere as evidence that an edge exists" (PMExperiment/REGISTRATION.md:614-618, PMExperiment/HYPOTHESES.md:290-293, PMExperiment/README.md:143-145). The Direction-B failure mode is guarded hard.
4. **The k-turnover sensitivity is reported and non-load-bearing, exactly as claimed.** I reproduced C_H at k = 1, 12 and ∞ for all ten buckets: the band top clears at every bucket on both routes under every k, and the band bottom clears at none. Amendment 4's claim at PMExperiment/REGISTRATION.md:820-824 is arithmetically correct. (My finding 1 is that the *other* two assumptions were never varied, not that this one was mishandled.)
5. **Bürgi's 3.0 "exactly ties the 0.0300 floor"** (PMExperiment/REGISTRATION.md:1053) is stated as a tie, not rounded into a failure, in the same sentence that calls the pair "fails". The tie only arises at k → ∞, which does not bind. Calling a zero-expected-profit tie a failure at the non-binding limit is defensible and is disclosed in the same clause; not a finding.
6. **The Section 13 empty-prior discipline.** The prior arrives at closure and is deliberately not backfilled (PMExperiment/REGISTRATION.md:1015-1029), may never be described as pre-registered, and the closure explicitly says no verdict may be read against it. This is the opposite of the failure I was hunting for.
7. **The operator-decline is correctly quarantined from the evidence.** ADR-017 (PMExperiment/DECISIONS.md:648-664) files it as a cost decision, not a finding, and states the reason a reader would otherwise conflate them. The route stays EXISTS-AND-UNTRAVELLED rather than becoming a refusal (PMExperiment/REGISTRATION.md:1065-1067). I could not construct an honest over-closure finding out of the decline itself; my finding 1 attacks only the *figure* offered as its input.
8. **Section 16's registered closure conditions are recorded as never met, not as satisfied by a substitute** (PMExperiment/REGISTRATION.md:605-612, 636-641). A repository closing on access could easily have passed this off as the registered closure; it does the opposite and pins the distinction with a mutation test.
9. **Amendment 1's retraction (Amendment 6) and the ADR-015 self-conviction on Dune** are both honest reversals against the repository's own interest, and ADR-013's self-conviction on the undated Kalshi terms (PMExperiment/DECISIONS.md:434-440) removes the repository's own finding from the "met the bar" column. I checked for the pattern where a self-criticism is used decoratively while the verdict quietly survives; here each correction is stated as narrowing the record, and PMExperiment/report.md:303-304 says so plainly ("Every correction made the record narrower or weaker. None changed a verdict") — which is true of all of them.
10. **BAND-NARROW's unevaluated volume clause.** Section 15.2:417 says the clause "cannot be evaluated, because Section 1's volume floor was never registered", and the floor is registered the next day as Amendment 5. I checked whether re-evaluation would have changed the verdict: it would not, because the clause also needs an enumeration that never existed, and firing BAND-NARROW would have been a *harsher* verdict, not a softer one. Not a Direction-A finding.
11. **The two settled records with `result` fields.** README:102-106 refuses to round "eleven probe requests received two settled records carrying `last_price_dollars` and `result`" into "no market price was ever read". The outcome-blindness claim is stated with its own exception; sound.

## Candidates recorded for the cross-repository pass (not raised as findings here)

- **MLCryptoEngine H2 at AUC 0.501** is cited five times as one of three grounds that H1t (transfer) may not be assumed (PMExperiment/HYPOTHESES.md:103, 190-191, 300-301; PMExperiment/REGISTRATION.md:624-626, 1150-1151). Whether a cross-venue transfer null measured in MLCryptoEngine is about a comparable question is a cross-repo check.
- **NPDExperiment's 0.0512 realized MDE against a 0.01–0.05 band, after 415 days**, and **InsiderExperiment's BLOCKED at 49.35 bp**, are quoted verbatim as the precedents that shaped Section 0 (PMExperiment/REGISTRATION.md:29-49; PMExperiment/DECISIONS.md:41-44). Figures to verify against those repositories at their own anchors.
- **Reopening conditions possibly met by work in another repository:** condition 1 (an established legal entity applying for Kalshi Internal Use) and condition 2 (a Kalshi academic tier) would be met if any other repository in the program holds Kalshi data access or an institutional entity. Nothing in PMExperiment answers that.

## Live-repo access log

Before first live access, `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`:

```
```

(empty — clean working tree)

After last live access, `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain`:

```
```

(empty — clean working tree)

Live-repo commands used, all read-only: `git status --porcelain`, `git log --oneline -12 --pretty`, `git rev-parse HEAD`. HEAD at read time 2026-09-04T00:26:41Z is `03d16e71dbf25a86c529884662d02136f8e82334`, identical to the anchored SHA; no commits exist after the anchor. No untracked or gitignored data files were read (the repository's `data/` holds only `.gitkeep` in the snapshot and the tree is clean).
