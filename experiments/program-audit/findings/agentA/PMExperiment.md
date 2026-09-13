# Agent A — PMExperiment (consolidated)

**Repository:** PMExperiment · **Anchored SHA:** `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project)
**Direction:** A — closed too early or too hard. **Agent:** A (honest advocate).
**Live HEAD equals the anchor** (`git -C … rev-parse HEAD` → `03d16e71…`; `git log 03d16e71..HEAD` empty; working tree clean, checked at 2026-09-04T04:57:34Z and twice by the drafting readers on 2026-09-04), so **no finding below can be invalidated by a later commit in this repository** as of 2026-09-04. The live tree additionally carries an untracked, git-excluded operator marker `_CLOSED_DO_NOT_RUN_HERE` forbidding further sessions (unanchored, read 2026-09-04T00:24Z).

**Framing, stated once so no finding is misread.** This repository never measured anything against H1 and says so on nearly every page. Its access verdicts are dated, quoted and documented; it convicts its own Stage A finding, retracts its own Amendment 1, overturns its own Dune verdict, and publishes a "what this stage did not read" table. **Nothing below disputes that no calibration statistic exists, and nothing below claims an edge exists.** What is challenged is narrower and is the Direction-A question: the *terminal apparatus* built around that absence — the exhaustiveness claim, the figure offered as the input to the decision to stop, and three foreclosures written into the reopening set.

## Summary — the strongest case for the thesis in this repository

Amendment 8 calls its reopening list **"stated precisely and exhaustively"** while two registered reopening paths are missing from it: Section 15.1's account path, whose only stated obstacle (ADR-002) the operator lifted on day 2 of 5 and which no document revisits, and Amendment 6's Polygon route, which this repository's own verification pass **strengthened** rather than closed. The **"thin"** band figure offered as the stated input to the decision to decline the entity path and end the project is produced by two assumptions the registration itself records as *overstating* cost: under the venue's own published fee schedule, quoted in the same table cell, the held-route floor at 95c falls from 0.03238 to **0.02237** at k = 12 and Bürgi's 3.0 points goes from failing to clearing, while the decisive sentence "fee and half-spread alone total **0.0300** … against a registered band bottom of **0.0200**" becomes a tie at **0.02000** rounded and **0.01333** unrounded — below the bottom. Three closing documents state that "the power question would still be unanswered" even if an authorization arrived, which the registration's own Section 0.4–0.5 derivation contradicts for the unrestricted cell: clearing the registered 1,000-market access floor entails MDE = **0.01676 → GO**, and a BLOCKED there would need fewer than **44** qualifying markets. And the one reopening condition that could fire without any operator action — "an academic tier offered by Kalshi, **if one is**", existence "**UNMEASURED**" — has the only instrument that could measure it pre-declared "**not a reopening**", pinned by a passing test in `tests/test_honesty.py`.

---

## Findings

### AUDIT-A-PMExperiment-1

- **ID:** AUDIT-A-PMExperiment-1
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** H1 — Amendment 8's terminal reopening set, declared exhaustive, against two reopening paths registered earlier in the same register (Section 15.1's third Kalshi path; Amendment 6's third Polymarket path)
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2 — the label "exhaustively" contradicts the register's own earlier text, and the omission removes the only two reopening paths that do not require an entity, a licence or a grant
- **Label:** READ (document-to-document comparison over the anchored snapshot; the grep counts are over the snapshot's tracked files)
- **Claim challenged (verbatim, with file:line):**
  > "**The reopening conditions, stated precisely and exhaustively.** Each is an
  > operator action, and none is a measurement:"
  — PMExperiment/REGISTRATION.md:1082-1083 (the three conditions follow at :1085-1098; Amendment 9 adds a fourth at :1161-1167)

  and, in the licence document that closes the search:
  > "Only these, and each is an operator decision rather than a measurement:"
  — PMExperiment/docs/LICENCES.md:773 (the list runs to :787 and contains three items)

  The same three-item set is what a cold reader meets at PMExperiment/HYPOTHESES.md:305-321 and PMExperiment/README.md:151-162.

- **Evidence (figures each with n, file:line):**
  1. **Dropped path A — the Kalshi account path.** Section 15.1 registers three reopening paths on 2026-08-29: "**What would reopen access:** written authorization from Kalshi for systematic retrieval and AI-mediated analysis, or a Kalshi-sanctioned bulk research channel not requiring an account, or an operator decision to register an account — which ADR-002 currently excludes." — PMExperiment/REGISTRATION.md:395-398; restated at PMExperiment/HYPOTHESES.md:33-35 and PMExperiment/DECISIONS.md:111-114 ("an operator reversal of ADR-002 by numbered amendment").
  2. **Its only stated obstacle expired the next day, by numbered amendment.** "**What changed.** The registration previously admitted only a measurement question. It now admits a terminal question of whether a tradeable edge exists that survives Canadian retail cost. The operator has stated that account creation is acceptable." — PMExperiment/REGISTRATION.md:754-757 (Amendment 3, 2026-08-30); same at PMExperiment/DECISIONS.md:182-183 ("account creation is acceptable to him").
  3. **The dropped path is the one the benchmark study used.** "The published benchmark study reached this data by registering an account — the path ADR-002 excludes." — PMExperiment/DECISIONS.md:97-98. That study is the source of the band's bottom: **313,972 Yes-and-No contract prices on 46,282 contracts across 12,403 events** — PMExperiment/REGISTRATION.md:226-228.
  4. **No document revisits it.** A grep of the whole snapshot for `ADR-002` returns **six** hits (REGISTRATION.md:398, DECISIONS.md:23, :98, :113, HYPOTHESES.md:35, docs/ACCESS.md:64) and for `register an account`/`account creation` **two** (REGISTRATION.md:398, DECISIONS.md:183). **None is dated after 2026-08-30**, and none records that the third path is now unobstructed or why it is dropped.
  5. **Dropped path B — the Polygon route.** Amendment 6 registers three Polymarket reopening paths on 2026-08-30: "**What would reopen access:** prior written consent from Adventure One QSS, Inc.; or enrolment in the builder program the Terms name; or a Polygon read performed through infrastructure that is not a Polymarket Interface, under a legal analysis this repository has not done. The third is recorded as an open question, **not** as a workaround adopted now." — PMExperiment/REGISTRATION.md:1001-1005; carried in the register at PMExperiment/HYPOTHESES.md:199-203.
  6. **The repository's own verification pass then strengthened route (c) rather than closing it.** "2. **The on-chain path is narrower than the licence read claimed.** … The bullet is scoped to 'the Site, any other Interface, or Features', and **a public Polygon ledger is none of the three on its face**. Amendment 6 already records the Polygon question as a live reopening path 'under a legal analysis this repository has not performed', and that remains its status — neither closed here nor opened here." — PMExperiment/docs/LICENCES.md:320-326; the same finding at PMExperiment/progress.md:1089-1092 and PMExperiment/DECISIONS.md:426-428 ("so Amendment 6's Polygon question stays open rather than being closed here").
  7. **Route (b) is answered on the merits; route (c) is answered nowhere.** The builder route is closed by its own published upgrade path — "Route orders through Polymarket and demonstrate consistent usage" — "closed to a repository that will never trade" (PMExperiment/docs/LICENCES.md:214-225). Amendment 9's fourth condition is route (a) restated — "**a Polymarket data licence or written authorization** — the same instrument Stage C found absent, obtained" (PMExperiment/REGISTRATION.md:1163-1167) — not route (c).
  8. **Count.** Registered reopening paths across Sections 15.1 and Amendment 6: **6** (three Kalshi, three Polymarket). The terminal set holds **4** conditions (Amendment 8's three plus Amendment 9's fourth), and they are not a subset of the six: condition 1 narrows 15.1(a) to an entity applying for Internal Use, condition 2 answers to 15.1(b), condition 4 restates A6(a), and condition 3 — a licensed dataset — is not one of the six at all. Of the six registered paths, **three** appear in some form, **A6(b)** is closed on its merits (evidence 7), and **two — 15.1(c) and A6(c) — appear in none of the four terminal lists**, with no document explaining either omission. The two missing are also the only two that require **no** grant, licence, entity or payment from a third party — one is an operator decision already made, the other is a legal analysis of the same document class Stage D read for 111 minutes (PMExperiment/progress.md:942) at zero dollars.
  9. **A third, weaker instance, recorded honestly rather than counted.** Section 16's own registered reopening — "**Reopening:** the permitted subset accumulates settled contracts with the calendar, so a later session may refire the gate on a fresh enumeration as a new numbered firing — the gate reads no outcome, so refiring is not a second look" (PMExperiment/REGISTRATION.md:651-654) — is also absent from Amendment 8's list. I do **not** count it as a dropped path: it presupposes an enumeration the access verdicts forbid, so its omission is defensible on the merits even though no document says so.
- **Recomputation:** none — this is a document-to-document comparison. The only figures are counts, given above with their greps.
- **What would resolve it:** one paragraph in Amendment 8, costing no venue, no request and no dollar. Either (a) "the account path of Section 15.1 is dropped because Kalshi's Data Terms condition systematic retrieval and AI-mediated use on written authorization regardless of account status, so an account does not cure condition 5" — or "it survives as reopening condition 5, unobstructed since Amendment 3"; and (b) either the legal analysis Amendment 6 says was never performed, recorded with its result, or route (c) restored to the list with its status ("open; requires a legal analysis not performed"). As written the register asserts exhaustiveness while doing neither.
- **Confidence:** HIGH — every quotation is verbatim and line-exact in the anchored snapshot, the dates are the documents' own, the greps are exhaustive over the snapshot, and both dropped paths are absent from all four terminal lists (REGISTRATION.md:1085-1098 and :1161-1167; HYPOTHESES.md:305-321 and :352-358; README.md:151-162; docs/LICENCES.md:773-787).
- **Could later commits invalidate this?:** No. Live HEAD equals the anchored SHA, `git log 03d16e71..HEAD` is empty, and Amendments 8 and 9 are the final commits.
- **Disclosed by authors?:** **No.** The register discloses each path where it registers it (REGISTRATION.md:395-398, :1001-1005), discloses the expiry of the ADR-002 obstacle (REGISTRATION.md:754-757), and discloses that the Polygon question stays open (docs/LICENCES.md:324-326, progress.md:1089-1092, DECISIONS.md:426-428). **No document connects any of that to Amendment 8's exhaustiveness claim, and none explains either omission.** ADR-018 lists "when a reopening condition is dropped" among the mutations the test suite must catch (PMExperiment/DECISIONS.md:711) — the guard exists, and these two are outside it.
- **Citation check:** corrected — evidence 8's count wording. Both verifiers recommend KEEP and both confirm every quote and grep line-exact (ADR-002 = 6 hits at the six cited locations; `register an account`/`account creation` = 2; none dated after 2026-08-30), but both independently flagged the 6-vs-4 count as apples-to-oranges: the terminal set's four *conditions* are not a subset of the six registered *paths* — condition 3, the licensed-dataset route, is not among the six, condition 1 narrows 15.1(a), and A6(b) is neither in the terminal set nor among the two counted as missing. Evidence 8 is rewritten to say exactly that. The load-bearing claim is unchanged and verified by both: 15.1(c) and A6(c) appear in none of the four terminal lists and no document explains either omission.

---

### AUDIT-A-PMExperiment-2

- **ID:** AUDIT-A-PMExperiment-2
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** H1 — the BAND-OPEN "thin band" figure used as the stated input to Amendment 7 / ADR-017's decision to decline the entity path and end the project
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2 — the "thin" label that carries the abandonment decision contradicts the venue-cost evidence recorded two hundred lines earlier in the same document
- **Label:** DERIVED (the cost model's constants were taken from `pmexperiment/registry.py:53-57, 66` and the MDE/floor recomputed with the audit venv; the counterfactual fee schedule is quoted from the registration's own Section 2 cell)
- **Claim challenged (verbatim, with file:line):**
  > "| **forming a personal legal entity** | **declined — disproportionate** | the cost is out of proportion to a stated prior of 5 to 8 percent, against a band verdict already recorded as thin |"
  — PMExperiment/REGISTRATION.md:1046

  and the figure that makes it thin:
  > "Every magnitude any cited source places inside
  > that bucket — Bürgi's **2.0** and **3.0** points — **fails** the cost floor of
  > **0.0300**, which the 3.0 exactly ties with FX at zero."
  — PMExperiment/REGISTRATION.md:1051-1053; restated at PMExperiment/report.md:419-420 and PMExperiment/README.md:145-149

  and the decisive published sentence:
  > "**The decisive figure, for a reader who reads one number:** fee and half-spread
  > alone total **0.0300** on the held route before any FX at all, against a
  > registered band bottom of **0.0200**. **No FX treatment, no venue price and no
  > exit route reaches the bottom of the band.**"
  — PMExperiment/REGISTRATION.md:456-459; restated with the same figures at PMExperiment/report.md:105-108 (the identical bolded sentence under a different lead-in, "The number a reader should keep.") and PMExperiment/HYPOTHESES.md:140 (a differently-worded table row carrying both figures)

- **Evidence (figures each with n, file:line):**
  1. **The cost floor is built from two assumptions the registration itself records as overstating cost.** Venue fee: "**2 cents per contract per side, both sides counted: 4 cents round trip** | assumption, conservative. Kalshi's published taker schedule is $0.07·P·(1−P) per contract rounded up (≈ 1.77 % of price at 50c, ≈ 0.33c at 5c), and settlement carries no fee, so the flat 4c **overstates** the venue cost at every price, most severely at the tails. Bias: against H1 surviving costs." — PMExperiment/REGISTRATION.md:199. FX: "**Overstates** low-cost channels (multi-currency brokers, Norbert's gambit ≈ 0.2–0.5 %)" — PMExperiment/REGISTRATION.md:201.
  2. **Neither assumption is ever varied anywhere in the repository.** A grep of the snapshot for the published fee schedule `0.07·P·(1−P)` returns exactly **two** hits — the Section 2 row (REGISTRATION.md:199) and its verbatim blockquote copy at docs/BAND.md:74 — and `Norbert` likewise returns exactly **two** (REGISTRATION.md:201, docs/BAND.md:76). No document computes a floor under either.
  3. **The only sensitivity that was run is chosen because it cannot change the verdict.** "**It does not decide the verdict.** Computed both ways in Task 4, the band's top clears the required underpricing at all ten registered buckets on both exit routes at k = 1, at k = 12 and in the k → ∞ limit" — PMExperiment/REGISTRATION.md:820-824.
  4. **n for the challenged magnitudes.** Bürgi's 2.0 and 3.0 points rest on **313,972 Yes-and-No contract prices on 46,282 contracts across 12,403 events** — PMExperiment/REGISTRATION.md:226-228.
  5. **The stated prior that the "thin" figure is weighed against is not a measurement and is not pre-registered:** "the stated prior of 5 to 8 percent is the operator's, given at closure, and it is not a result" — PMExperiment/REGISTRATION.md:585; Section 13 left permanently empty at :1015-1016.
- **Recomputation:** constants from `pmexperiment/registry.py` (`FEE_PER_SIDE_USD = 0.02`, `FEE_SIDES = 2`, `HALF_SPREAD_USD = 0.01`, `FX_PER_DIRECTION = 0.015`, `FX_DIRECTIONS = 2`, `FX_TURNOVER_REGISTERED = 1.0`, lines 53-57 and 66); held route = one side's fee + half-spread + 0.03·p/k. Script: `scratchpad/work/agentA-PM-consolidate/recheck.py`, run 2026-09-04.
  - **Registered case reproduces exactly.** C_H(0.91) = 0.05730, C_H(0.95) = **0.05850**, C_H(0.99) = 0.05970 — "5.73 points at 91c rising to 5.97 at 99c" and the 5.85 headline at PMExperiment/REGISTRATION.md:422-424 and PMExperiment/docs/BAND.md:314-318.
  - **The venue's own published fee, taken verbatim from REGISTRATION.md:199.** 0.07 · 0.95 · 0.05 = **$0.003325**, rounded up to the cent = **$0.01** per side — **half** the registered 2c — and settlement carries no fee, so the held route pays it once.
  - **Held-route floor at p = 0.95 under the published fee and the registered 3 % FX:** **0.04850** at k = 1 (Bürgi's 0.030 still fails, by 1.85 points) and **0.02237** at k = 12, where **Bürgi's 0.030 clears by 0.76 points**. Under the registered flat 2c the same k = 12 floor is **0.03238** and 0.030 fails by 0.24 points. **The k = 12 verdict flips on the fee assumption alone.**
  - **Held-route floor at p = 0.95 under the published fee and the Section 2-named Norbert's-gambit channel (0.4 % round trip), at the *binding* k = 1:** **0.02380** — Bürgi's 0.030 **clears by 0.62 points**. With the fee unrounded ($0.003325) the floor is 0.01713 and it clears by 1.29 points.
  - **The decisive "0.0300 … already above the band bottom of 0.0200, at every price and on every route" sentence:** under the published schedule rounded up to the cent, fee + half-spread = 0.01 + 0.01 = **0.02000 exactly** — a tie with the band bottom, not "above" it; unrounded it is **0.01333**, i.e. **below** the band bottom by 0.67 points.
  - **Honest counter-weight, recomputed and reported.** Section 2 also records that the 1c half-spread "likely **understates** the cost at the illiquid tails", where "Tail books on the platform are typically 1–3c wide" (PMExperiment/REGISTRATION.md:200). At a 1.5c half-spread with the published fee and Norbert's-gambit FX at k = 1 the floor is **0.02880** and Bürgi's 0.030 clears by only **0.12 points**. The reversal is real but is not robust to the spread caveat, and I say so.
- **What would resolve it:** a one-paragraph sensitivity in `docs/BAND.md` computing the floor under (i) Kalshi's published taker schedule and (ii) the two FX channels Section 2 already names, reported beside the registered case exactly as k = 12 and k → ∞ already are — or a sentence in Amendment 7 stating that "thin" is a property of the registered assumptions and not of the venue's actual cost. Neither requires venue access, data, or money.
- **Confidence:** MEDIUM — the arithmetic is certain and every input is either the repository's own code constant or a figure quoted in its own Section 2 cell, but the registration deliberately binds its assumptions, the reversal is not robust to the disclosed spread caveat, and the Stage-B operator prompt forbade proposing "a different fee assumption, a different effect band, or a different venue **to rescue an empty band**" (PMExperiment/progress.md:330-332). The band was not empty, so the prohibition does not literally reach a sensitivity reported beside the registered case — but it explains the omission.
- **Could later commits invalidate this?:** No — live HEAD equals the anchored SHA, and Amendment 8 forbids recomputing the band at all (PMExperiment/REGISTRATION.md:1106-1109), so the figure is now permanent.
- **Disclosed by authors?:** **No, for the limitation raised — and the components are disclosed, plainly and in the right place.** Section 2 discloses both assumptions, names the venue's published schedule, and names the direction of bias as "against H1 surviving costs" (PMExperiment/REGISTRATION.md:199, :200, :201). What is disclosed **nowhere** is the magnitude or the consequence: no document computes the floor under the venue's published schedule or under either named FX channel, and the "every cited magnitude fails" sentence that feeds the abandonment decision is stated at REGISTRATION.md:1051-1053, report.md:419-420 and README.md:145-149 without it.
- **Citation check:** corrected — two citation nits, both named by both verifiers, checked against SNAP and applied: (a) "identically at report.md:105-108 and HYPOTHESES.md:140" overstated — report.md:107-108 carries the identical bolded sentence but under a different lead-in and HYPOTHESES.md:140 is a differently-worded table row with the same two figures — now "restated with the same figures at"; (b) "Bias: against H1 surviving costs." is unbolded at REGISTRATION.md:199 and is now quoted unbolded. Otherwise verified (quote EXACT, figures YES): both verifiers reproduced every figure to the digit (C_H 0.05730/0.05850/0.05970; published fee 0.003325 → $0.01; floors 0.04850, 0.02237, 0.03238, 0.02380, 0.017125; 0.02000 rounded / 0.013325 unrounded; 0.02880 counter-weight) and both greps exactly (2 hits each for `0.07·P·(1−P)` and `Norbert`). Both confirmed DERIVED and both confirmed the S3 disclosure cap does not apply, because no document computes the floor under the published schedule or either named FX channel. Verifier 1 notes the paper prints 0.02237 where 0.02238 would be the rounded value; the finding follows the repository's own truncation.

---

### AUDIT-A-PMExperiment-3

- **ID:** AUDIT-A-PMExperiment-3
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** the Polymarket PENDING_ACCESS verdict as it reaches the on-chain (Polygon) route, and Amendment 9's use of that reach to hold the verdict where it stands
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2 — three ledger rows and a numbered amendment assert a conjunction that the register's own two component readings each qualify
- **Label:** READ (documentary; all four quotations are in the anchored snapshot)
- **Claim challenged (verbatim, with file:line):**
  > "| Polymarket | **PENDING_ACCESS** | Terms effective 2026-08-11 prohibit the data-gathering tool class, expressly including on-chain | 2026-08-30 |"
  — PMExperiment/README.md:116; the same row at PMExperiment/REGISTRATION.md:598 and, in different words, at PMExperiment/HYPOTHESES.md:174 ("scope expressly reaching API **and on-chain** access")

  restated as the ground of Amendment 9:
  > "The prohibition on data mining tools, robots and crawlers carries
  > **no entity-type qualification**, and the data clause reaches material taken
  > **directly, through an API, or by any other means, including on-chain**."
  — PMExperiment/REGISTRATION.md:1133-1136, used at :1137-1139 to leave "Stage C's PENDING_ACCESS verdict exactly where it stands"

- **Evidence (figures each with n, file:line):** the sentence conjoins two properties belonging to two different clauses, and the same register says the *restriction* attached to one of them does not bind this operator, while the other does not on its face reach a public ledger.
  1. **The reach to on-chain comes from the Data clause's subject-matter definition:** "the Data clause defines its subject as data 'contained on our Site, any Interface or Features **directly or through an API, or any other means, including on-chain**, whether in raw, derived, aggregated, or anonymized form'" — PMExperiment/REGISTRATION.md:952-955.
  2. **Twelve lines later the same amendment records that this clause's restriction does not bind:** "**One clause that does not bind, recorded for accuracy.** The Data restriction is conditional on entity type: it prohibits access by 'a non-retail, professional entity that engages in capital markets activities' or by 'a market data distributor'. A Canadian retail individual conducting measurement-only research is neither, so that clause is **not** the ground of this finding. The data-mining and crawlers prohibition carries no such condition, and it is." — PMExperiment/REGISTRATION.md:967-972.
  3. **The clause that does bind is scoped, and the repository measured that scope against a public ledger:** "the bullet is scoped to 'the Site, any other Interface, or Features', and **a public Polygon ledger is none of the three on its face**, so Amendment 6's Polygon question stays open rather than being closed here" — PMExperiment/DECISIONS.md:426-428; same at PMExperiment/docs/LICENCES.md:320-326 and PMExperiment/progress.md:1089-1092.
  4. **Amendment 6 leaves the route explicitly open:** "or a Polygon read performed through infrastructure that is not a Polymarket Interface, under a legal analysis this repository has not done. The third is recorded as an open question, **not** as a workaround adopted now." — PMExperiment/REGISTRATION.md:1002-1005.
  5. **Net.** On the repository's own two readings, the binding clause does not on its face reach a public Polygon ledger, and the on-chain reach comes only from the subject-matter *definition* of a clause whose *restriction* the same register records as not binding this operator. **Three summary rows and Amendment 9 nonetheless state the on-chain prohibition with neither qualification**, and Amendment 9 uses the conjunction to hold the verdict in place. Count: 3 ledger rows + 1 amendment assert it; 2 register passages deny each half. **The register does reason about the crawler bullet's scope once, and it must be recorded:** Amendment 6 sets out and rejects a narrow reading at PMExperiment/REGISTRATION.md:974-986 — "it can be argued those API hosts are not Interfaces and that bullet does not literally reach them", refused on three grounds including the Data clause's "directly or through an API" reach and standing rule 5 — cross-referenced at PMExperiment/DECISIONS.md:381-384. That passage is about the **API hosts** (`gamma-api.polymarket.com`), not about a public Polygon ledger, and it predates the ADR-013 verification pass that found the bullet reaches no such ledger on its face. **No document reaches the on-chain case.**
- **Recomputation:** none — this is a documentary inconsistency, not an arithmetic one.
- **What would resolve it:** either (a) restate the three route-ledger rows and Amendment 9 as "the binding clause is scoped to the Site, Interfaces and Features; whether it reaches a public Polygon ledger is UNRESOLVED, and the on-chain reach comes only from the subject-matter definition of a clause whose restriction this register records as not binding this operator" — one edit, no access — or (b) perform the legal analysis Amendment 6 says was not done and record its result.
- **Confidence:** MEDIUM — all four quotations are verbatim and line-exact in the anchored snapshot and neither qualification appears anywhere near the three summary rows, but the register does record and reject a narrow-scope counterargument at REGISTRATION.md:974-986; it is aimed at the API hosts rather than at a public Polygon ledger, and if a reader accepts it as an answer on the merits the finding narrows to the Amendment 9 / verification-pass mismatch alone.
- **Could later commits invalidate this?:** No — Amendment 9 (commit 03d16e7, 2026-09-02) is both the final word on this and the document that restates the conjunction; live HEAD equals the anchor.
- **Disclosed by authors?:** **Partially.** Each component is disclosed separately — REGISTRATION.md:967-972 discloses that the Data *restriction* does not bind; DECISIONS.md:426-428 discloses that the binding bullet does not reach a public ledger on its face; ADR-013 explicitly leaves the Polygon question open — and Amendment 6 additionally sets out and rejects a narrow reading of the crawler bullet's scope at REGISTRATION.md:974-986, cross-referenced at DECISIONS.md:381-384, though only for the API hosts. **Not disclosed:** that the three summary rows and Amendment 9 (2026-09-02) assert the on-chain conjunction unqualified *after* the repository's own verification pass found "a public Polygon ledger is none of the three on its face", and `tests/test_honesty.py` pins "This amendment does not reopen H1" as a passing assertion over the amendment that carries it.
- **Citation check:** corrected — the verifiers split (verifier 1 KEEP with one citation nit; verifier 2 CORRECT on three points), so I checked all three against SNAP and followed verifier 2, because each is right on the source. (a) HYPOTHESES.md:174 is the same assertion in different words, not the identical row — both verifiers agree — so the claim line now reads "the same row … and, in different words, at HYPOTHESES.md:174". (b) The register distinguishes the Data clause's subject-matter *definition* (which reaches on-chain, REGISTRATION.md:952-955) from the Data *restriction* (entity-conditional, does not bind, :967-972); the net paragraph and the resolution now rest on the definition rather than saying "the clause that does reach it does not bind". (c) "0 documents notice the conflict" overstated: REGISTRATION.md:974-986 sets out and rejects a narrow reading of the crawler bullet, expressly invoking the Data clause's "directly or through an API" reach and standing rule 5, cross-referenced at DECISIONS.md:381-384 — that count is removed and the passage is now quoted, with the observation that it addresses the API hosts and not a public Polygon ledger. Disclosure moved to **Partially** and confidence to MEDIUM. **Severity stays S2:** both verifiers marked severity_ok, and the residual — Amendment 9 restating the on-chain reach flatly on 2026-09-02 after the repository's own verification pass found "a public Polygon ledger is none of the three on its face" — is disclosed nowhere. All four claim quotations verify EXACT and line-exact.

---

### AUDIT-A-PMExperiment-4

- **ID:** AUDIT-A-PMExperiment-4
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** H1 — Amendment 8 reopening condition 2, "an academic tier offered by Kalshi, if one is", and the rule that a reply to the pending question is not a reopening
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2 — the register makes the *existence* of an academic tier a reopening condition and, in the next paragraph, pre-declares the only instrument that could establish that existence to be a non-reopening; both cannot be true of the same reply
- **Label:** READ (documentary; the test assertion is read from the snapshot's `tests/test_honesty.py`)
- **Claim challenged (verbatim, with file:line):**
  > "**A reply to the pending academic-tier question is not a reopening.** If one
  > arrives, it is **a one-line register update** recording what it said — nothing
  > more. Only condition 1, 2 or 3 actually being **satisfied** reopens anything, and
  > a reopening is a new numbered firing under Section 16, not a resumption of this
  > one."
  — PMExperiment/REGISTRATION.md:1100-1104; the same rule at PMExperiment/HYPOTHESES.md:318-321 and PMExperiment/README.md:164-166

- **Evidence (figures each with n, file:line):**
  1. **Condition 2 as registered is about the existence of an offer, not about a grant:** "2. **An academic tier offered by Kalshi, if one is.** A question about one is **pending** with the institutional desk and unanswered as of 2026-09-02. Its existence is **UNMEASURED** — not absent, not assumed." — PMExperiment/REGISTRATION.md:1092-1094; identically at PMExperiment/HYPOTHESES.md:312-314 and PMExperiment/README.md:159-160.
  2. **The pending reply is the only instrument that can measure that existence.** The question sits with the desk, unanswered, and the repository sends nothing further: Stage E sent **zero requests** to Kalshi or any other host (PMExperiment/REGISTRATION.md:526-527), and Stage D's verdicts were explicitly not re-asked ("One route answered; the rest were not re-asked" — PMExperiment/docs/LICENCES.md:844-846).
  3. **The foreclosure is hardened into the test suite, not left as prose.** ADR-018 lists the mutations the suite must catch, including "when a pending reply is promoted into a reopening" — PMExperiment/DECISIONS.md:711-712. The test exists: `tests/test_honesty.py:471-476`, `test_a_reply_to_the_pending_question_is_not_a_reopening`, asserting `"one-line register update" in doc` **and** `"not a reopening" in doc` across every closing document. A future session that reads a reply saying "yes, we run an academic tier" and treats condition 2 as satisfied fails the suite.
  4. **Context that raises the stakes.** This is the repository whose own Stage D completeness caveat was vindicated within two days by an unsolicited desk reply — "**Two days later a route surfaced that Stage D had not read.**" (PMExperiment/DECISIONS.md:575; same at PMExperiment/progress.md:1443-1449, "A route surfaced two days later. The caveat cost one paragraph and was load-bearing inside a week"). **The instrument class that overturned the previous terminal state is exactly the instrument class now pre-declared non-reopening.**
  5. **Count.** Of the four terminal reopening conditions, condition 2 is the **only one** whose trigger can arrive without any operator action; it is also the only one with a rule attached foreclosing its arrival.
  6. **Provenance of the rule, recorded because it matters.** The foreclosure is not a position the repository reasoned to: it is an operator instruction the stage carried out. The Stage E prompt, logged verbatim, reads "Note that a reply to the pending academic-tier question, if one arrives, is a one-line register update and not a reopening." — PMExperiment/progress.md:1304.
- **Recomputation:** none — documentary.
- **What would resolve it:** distinguish the two acts in the text — a reply confirming a tier **satisfies condition 2** (and therefore reopens under Section 16 as a new numbered firing), while applying for and being granted the tier is the separate operator action — or restate condition 2 as "an academic tier **granted to this operator**", which is consistent with the rule but is a materially narrower condition than "if one is".
- **Confidence:** MEDIUM — a charitable reading is that "offered" means "offered *to this operator*, i.e. granted", in which case the two paragraphs are consistent. But the text says "if one is", the status is "existence is **UNMEASURED**", and no document draws the distinction; the mutation guard at DECISIONS.md:711-712 treats the stricter reading as the invariant to protect.
- **Could later commits invalidate this?:** No — live HEAD equals the anchor. A reply arriving after 2026-09-02 would be the trigger this finding concerns, not an invalidation of it.
- **Disclosed by authors?:** **No.** Both sentences are printed within four lines of each other in all three closing documents and the tension is never named.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP; all quotations line-exact and `tests/test_honesty.py:471-476` confirmed by both, function name and both assertions. Verifier 2's optional provenance addition is applied as evidence 6: the non-reopening rule originates in the operator's Stage E prompt at progress.md:1304, so the foreclosure is an instruction the stage carried out rather than a position the repository reasoned to.

---

### AUDIT-A-PMExperiment-5

- **ID:** AUDIT-A-PMExperiment-5
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** the power gate — the closing claim, made in three documents, that an authorization would leave the power question unanswered, against the registration's own Section 0.4–0.5 derivation for the unrestricted cell U24
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2 — a stated closing conclusion contradicts a derivation printed in the same register, for one of the two verdict cells
- **Label:** DERIVED (MDE recomputed with the repository's own `pmexperiment/power.py:37-45` and `registry.Z_CRITICAL`, on the registered planning dispersion and the registered access floor)
- **Claim challenged (verbatim, with file:line):**
  > "**Even if an authorization arrived
  > tomorrow the power question would still be unanswered**, and nothing in five
  > stages has moved it. That is the honest end of it."
  — PMExperiment/report.md:483-485; the same claim at PMExperiment/DECISIONS.md:740-741 ("**If an authorization arrived tomorrow, the power question would still be unanswered.**") and PMExperiment/README.md:191-192 ("**Even if an authorization were granted tomorrow, the power question would still be unanswered** — nothing in five stages has moved it")

- **Evidence (figures each with n, file:line):**
  1. **The registration derives the answer for the unrestricted cell in advance, inside the access gate:** "3. At least 1,000 settled markets are enumerable in total. At the published two-thirds tail share, GO needs about 703 markets (475 / 0.676); the floor of 1,000 leaves margin for a lower realized share." — PMExperiment/REGISTRATION.md:148-150.
  2. **And again in Section 0.4, drawing exactly the U24/P30 distinction the closing sentences drop:** "The published benchmark (Section 3) reports two-thirds of its 313,972 contract prices in the 1–10c and 90–99c bands, so the unrestricted universe reaching 475 tail contracts is expected. Whether the Canadian-permitted subset retains even 30 is precisely the open question this gate exists to answer, and it is answerable without reading a single outcome." — PMExperiment/REGISTRATION.md:132-137.
  3. **The formula and the bars.** "MDE = z · sqrt(v̄ / n_T)" with z = 2.0 — PMExperiment/REGISTRATION.md:99-101 and `pmexperiment/power.py:37-45`, `registry.Z_CRITICAL = 2.0` (registry.py:9). GO at MDE ≤ 0.02, BLOCKED at MDE > 0.08 or n_T = 0 — PMExperiment/REGISTRATION.md:110-112. Planning dispersion v̄ ≈ 0.0475 and derived bars "GO, MDE ≤ 0.02 | ≥ 475" and "stay out of BLOCKED, MDE ≤ 0.08 | ≥ 30" — PMExperiment/REGISTRATION.md:122-129.
  4. **The benchmark's own counts:** n = **313,972** prices on **46,282** contracts across **12,403** events, two-thirds in the tail bands — PMExperiment/REGISTRATION.md:226-234.
  5. **The depth blocker is not a property of the archive:** "historical depth on the licence | **2021 onward, through historical endpoints**, expressly not subject to the live-data cutoff" — PMExperiment/REGISTRATION.md:538.
- **Recomputation:** `minimum_detectable_effect(n_T, v̄)` from the repository's own `pmexperiment/power.py`, v̄ = 0.0475 (REGISTRATION.md:122-123). Script `scratchpad/work/agentA-PM-consolidate/recheck.py`, run 2026-09-04.
  - n_T = **676** (the registered access floor of 1,000 settled markets × the published 0.676 tail share, both from REGISTRATION.md:148-150): MDE = **0.01676 → GO**.
  - n_T = **703** (the registration's own 475 / 0.676): MDE = **0.01644 → GO**.
  - n_T = **30,855** (two-thirds of the benchmark's 46,282 contracts): MDE = **0.00248 → GO**.
  - n_T = **209,315** (two-thirds of the benchmark's 313,972 prices): MDE = **0.00095 → GO**.
  - Inverting the BLOCKED bar: BLOCKED (MDE > 0.08) requires n_T < **29.69**, i.e. fewer than **44** qualifying markets at the published 0.676 tail share. Against a registered access floor of **1,000** markets, a U24 BLOCKED is excluded by the access condition alone.
  - **Conclusion:** for U24 the power question is not open in any meaningful sense — clearing the registered access condition 3 *entails* GO at planning dispersion, and the register says so at :148-150. What is genuinely unanswered is P30, the Canadian-permitted cell, exactly as :135-137 says.
- **What would resolve it:** replace the three unqualified sentences with the split the registration already makes — "the U24 power question is expected to clear on the published tail share (Section 0.4); the P30 power question, which is the one this design exists to answer, is unanswered" — or, if the authors mean "no *realized* MDE from this repository's own enumeration exists", say that instead, since it is true and much weaker.
- **Confidence:** MEDIUM — the arithmetic and the quoted derivation are certain, and the sentence is stated three times with "nothing in five stages has moved it", which Section 0.4 contradicts on its face. Two honest counter-arguments, both from the second reader: the charitable reading is "no realized MDE exists", which is true; and the registered gate requires a **measured** v̄ and n_T rather than published estimates, with standing rule 5 forbidding a synthesized value — so a pre-derived expectation is not a fired gate. That is why this is S2 (a claim at odds with its own register) rather than S1.
- **Could later commits invalidate this?:** No — live HEAD equals the anchor and the project is closed.
- **Disclosed by authors?:** **No.** The registration's own derivation at REGISTRATION.md:132-137 and :148-150 is never cited in the closure paragraphs at report.md:483-485, DECISIONS.md:736-744 or README.md:190-192, and none of the three distinguishes U24 from P30 — the distinction the register itself calls "precisely the open question this gate exists to answer".
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP. Both reproduced the MDEs independently with the repository's own `power.py` and `Z_CRITICAL = 2.0`: 0.016765 at n_T = 676, 0.016439 at 703, 0.002481 at 30,855, 0.000953 at 209,315, and the BLOCKED inversion n_T < 29.6875 → fewer than 44 qualifying markets at the 0.676 tail share. Verifier 2 confirmed by grep that "U24"/"P30" occur only at REGISTRATION.md:83-84, :104-105, :115-116 and :648-649 and in none of the three closing paragraphs. Both endorsed S2 over S1 on the two counter-arguments already carried in the confidence field.

---

### AUDIT-A-PMExperiment-6

- **ID:** AUDIT-A-PMExperiment-6
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** the BAND-OPEN surviving region fixed at 91–99c, and Amendment 8's permanent restriction of any reopened power gate to that region
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — the scope mismatch is disclosed by the authors, so this is capped at S3; what is added is the consequence for reopening, which is not
- **Label:** DERIVED (cost floors recomputed from `pmexperiment/registry.py:53-57, 66`, reproducing `docs/BAND.md`'s published table before extending it)
- **Claim challenged (verbatim, with file:line):**
  > "A
  > reopened measurement starts at the power gate over 91–99c held to resolution and
  > no other region, exactly where Stage C left it."
  — PMExperiment/REGISTRATION.md:1109-1111

  resting on:
  > "| the eight non-tail deciles | **no effect magnitude is registered outside the tail cell.** Supplying one would violate standing rule 5. |"
  — PMExperiment/docs/BAND.md:325; the same exclusion at PMExperiment/REGISTRATION.md:426-427

- **Evidence (figures each with n, file:line):**
  1. **The only clearing magnitude sits in the excluded decile, and the repository's own table marks it clearing on every treatment:** "| Krause, sub-30c/4.0 % → NO at 88.3c | 0.883 | 0.077 | 0.0565 **clears** | 0.0765 **clears** | 0.0300 **clears** |" — PMExperiment/docs/BAND.md:253; the direction table at PMExperiment/DECISIONS.md:250 and the bucket row "| 81–90 | 0.855 | 0.0556 | … | not registered — though Krause's exploitable complement lands here at 0.883 |" — PMExperiment/docs/BAND.md:209.
  2. **Both magnitudes inside the fired region fail:** "| Bürgi, 5c/3 % → NO at 95c | 0.950 | 0.020 | 0.0585 **fail** … | Bürgi, 95c/98 % → YES at 95c | 0.950 | 0.030 | 0.0585 **fail** …" — PMExperiment/docs/BAND.md:251-252. **The gate's region contains no cited magnitude that clears; the excluded neighbouring decile contains the only one that does.**
  3. **The verdict's own discrimination relies on the excluded bucket.** BAND-OPEN is chosen over BAND-NARROW because "the category clause is contradicted by Krause's permitted-category attribution" — PMExperiment/docs/BAND.md:306-309; same at PMExperiment/progress.md:478-481. Krause is the 88.3c figure. **It is in scope when it defeats BAND-NARROW and out of scope when it would widen the region the power gate fires over.**
  4. **The band's top is set by that same source.** "Its top, 0.08, rounds the largest single-category published figure, Krause's 7.7 points" — PMExperiment/REGISTRATION.md:253-255 — and "the band survives on its top alone" (PMExperiment/REGISTRATION.md:1053-1054). Krause's n is recorded nowhere: "**Krause's n is nowhere in the registration**, and Krause sets the band's top" — PMExperiment/DECISIONS.md:265-270; PMExperiment/HYPOTHESES.md:144. That is a real weakness of the top and I do not dispute it — it is a reason to *measure* the 81–90 decile, not to bar it.
  5. **The region was fixed before Stage B's own direction correction moved every exploitable price to 0.883–0.95** ("Restated that way every registered magnitude sits at a **high** entry price — 0.883 to 0.95", PMExperiment/progress.md:412-414), and the Stage C prompt had already frozen it ("Do not widen the region to improve the count", PMExperiment/progress.md:561-562).
- **Recomputation:** held route R_H(p) = 0.02 + 0.01 + 0.03·p/k, round trip R_X(p) = 0.04 + 0.01 + 0.03·p/k, constants from `pmexperiment/registry.py:53-57` and k = 1 from `:66`. Script `scratchpad/work/agentA-PM-consolidate/recheck.py`.
  - p = 0.883: R_H = **0.05649** (docs/BAND.md prints 0.0565), Krause's 0.077 **clears by +0.02051** — 2.05 points, at the binding k = 1. R_X = **0.07649**, clears by **+0.00051**.
  - p = 0.950: R_H = **0.05850**; Bürgi's 0.030 fails by −0.0285 and 0.020 by −0.0385.
  - **The round-trip clearing must not be relied on and I say so:** its 0.00051 margin is smaller than the 0.00195 by which Section 2's FX base is recorded as understating cost at that price (PMExperiment/REGISTRATION.md:427-429), i.e. inside its own slack. **The held-route clearing at 2.05 points is not.**
  - **Band-top survival margin, held route: 0.02435 at the 81–90 decile (p = 0.855) versus 0.02150 at the 91–99 decile (p = 0.950).** The excluded bucket has the larger margin as well as the only clearing citation.
  - Every figure reproduces `docs/BAND.md:205-210` and `:248-253` exactly before the extension.
- **What would resolve it:** a numbered amendment recording, before any reopened measurement, either (a) that the reopened power gate fires over 81–99c because ADR-009's direction correction moved the exploitable prices across the registered cell edge, or (b) that it fires over 91–99c only **and that the region therefore contains no cited magnitude that clears the registered cost floor** — which is a materially different sentence from the one Amendment 8 now carries.
- **Confidence:** MEDIUM — the arithmetic is certain and reproduces the repository's own table, but the exclusion is *registration-compliant*: Section 3 registers the band in the tail cell before any measurement, and DECISIONS.md:261-264 gives a principled reason for not moving it after the fact ("narrowing a registered band after seeing the arithmetic is precisely what Section 3 forbids"). The finding is that this faithfulness produces a **permanent** bar on the one bucket the repository's own arithmetic says clears, and no document weighs that.
- **Could later commits invalidate this?:** No — Amendment 2 fixes the band as computed once and Amendment 8 forbids adding a bucket afterwards (PMExperiment/REGISTRATION.md:1106-1109); live HEAD equals the anchor.
- **Disclosed by authors?:** **Yes, in part — and the finding is capped at S3 because of it.** The scope mismatch is disclosed at PMExperiment/DECISIONS.md:259-264 ("**A scope mismatch.** … Krause's exploitable complement at 88.3c lands in the 81–90 decile, outside that cell"), at PMExperiment/docs/BAND.md:330-334, and at PMExperiment/HYPOTHESES.md:144; the clearing arithmetic is published at PMExperiment/docs/BAND.md:209 and :253. **Not disclosed anywhere:** that the same excluded magnitude is what defeats BAND-NARROW, and that Amendment 8 carries the exclusion forward as the permanent scope of any reopened measurement.
- **Citation check:** corrected — one wrong line reference, found independently by both verifiers and confirmed by me against SNAP. "Do not widen the region to improve the count" is at PMExperiment/progress.md:561-562, inside the Stage C prompt (which begins at :548, under "Scope, fixed by Stage B and not reopenable here"); progress.md:327-328 belongs to the Stage B prompt and reads "that the power gate fires next over that region and no other. Do not design the / power gate here." The finding's attribution to the Stage C prompt was already correct; only the line number was wrong, and it is a regression introduced at consolidation (recorded there as `:562-563 → :327-328`), so the consolidation list is corrected too. Everything else verified (quote EXACT, figures YES): both verifiers reproduced R_H(0.883) = 0.05649, Krause's +0.02051 margin, R_X = 0.07649 against the disclosed 0.00195 FX slack, R_H(0.950) = 0.05850, and the band-top margins 0.02435 (81–90) vs 0.02150 (91–99).

---

### AUDIT-A-PMExperiment-7

- **ID:** AUDIT-A-PMExperiment-7
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** Stage D candidate 2 — published academic datasets, closed UNMEASURED on ADR-012 element (2), frozen at closure, and carried forward as terminal reopening condition 3
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — the gap is disclosed by the authors and named by them as "the sharpest", so this is capped at S3; what is added is that the closure three days later asserted an exhaustive quantifier without acting on a zero-cost cure
- **Label:** READ (documentary; every element is quoted from the repository's own documents)
- **Claim challenged (verbatim, with file:line):**
  > "**Element (2) fails.** The dataset card prints no effective, last-updated or
  > revision label; its only years are data-coverage bounds and a BibTeX citation
  > year, neither of which may be promoted."
  — PMExperiment/docs/LICENCES.md:398-400

  carried into the terminal verdict as:
  > "| **unmeasurable** | every route to the records either prohibits the reading, cannot show it is permitted, or requires standing this operator does not have |"
  — PMExperiment/REGISTRATION.md:586 (Section 15.5, 2026-09-02)

- **Evidence (figures each with n, file:line):**
  1. **The deciding element was never sought in the document class that carries it by construction, and the repository says so in its own words:** "| **Versioned repository deposits — Zenodo, Dataverse, OSF, figshare** | **the sharpest gap.** A DOI landing page prints a licence, a publication date and a version *by construction* — the one document class that routinely satisfies all three ADR-012 elements. Candidate 2 reached UNMEASURED on element (2) **without fetching a single deposit landing page**, recording only a search-result absence. |" — PMExperiment/docs/LICENCES.md:674; same at PMExperiment/report.md:306-311 and PMExperiment/HYPOTHESES.md:233-238.
  2. **A second named, unfetched document bearing on the same element:** "| the **CC BY 4.0 errata page**, named in the legal code's own footer | bears directly on element (2), the element candidate 2 fails |" — PMExperiment/docs/LICENCES.md:675; and at :405-411, "**There is one, it is named on the face of the legal code, and it was not read** — the footer points to an errata page carrying 'the date of change'."
  3. **The fetch is inside the stage's own permitted scope and costs nothing.** Stage D's scope is "Licence, terms, acceptable-use, contact, pricing and dataset-documentation pages **only**" (PMExperiment/docs/LICENCES.md:39-40), of which candidate 1 alone fetched **11** (PMExperiment/docs/LICENCES.md:125-131); the repository performed the same act four times for `robots.txt` on 2026-08-30 (PMExperiment/REGISTRATION.md:477-478). The dataset's own paper is a versioned deposit with a dated landing page: "`TimeSeventeen/Polymarket-v1` (Boka Qin, Rui Yang; paper arXiv:2606.04217)" — PMExperiment/docs/LICENCES.md:348. Set against the path that *was* weighed and declined: forming a legal entity with formation documents and beneficial-owner verification (PMExperiment/REGISTRATION.md:536, :1046).
  4. **The verdict was frozen at closure without re-asking:** "**And one thing this addendum does not do: it does not reopen Stage D's other two verdicts.** Polymarket and the three licence candidates are where Stage D left them. One route answered; the rest were not re-asked." — PMExperiment/docs/LICENCES.md:844-846, written 2026-09-02 — i.e. *after* the same document's completeness caveat had already been proven load-bearing once (PMExperiment/DECISIONS.md:570-579; PMExperiment/progress.md:1443-1449).
  5. **The register keeps the dataset route open as reopening condition 3** — "**A licensed dataset whose licensor held authority to license.**" (PMExperiment/REGISTRATION.md:1095-1098) — while never having sampled the class most likely to satisfy the element that closed the last candidate.
  6. **The repository's own answer does not reach the gap.** "Curing the date would not open it anyway: element (1), chain of title, and the AI-clause gap all remain" (PMExperiment/docs/LICENCES.md:768-769; PMExperiment/report.md:331-332) is about the **same** candidate (`TimeSeventeen/Polymarket-v1`). It does not reach a different, author-deposited corpus with a different chain of title, which is what the unfetched class would contain.
  7. **Scale of the candidate whose closure carries the route:** `TimeSeventeen/Polymarket-v1` documents all four gate inputs over **1,201,580,990 rows** spanning 2022-11-21 → 2026-04-28 (PMExperiment/DECISIONS.md:452-468; PMExperiment/HYPOTHESES.md:218).
- **Recomputation:** none — this is a document-availability argument.
- **What would resolve it:** four DOI-landing-page fetches (Zenodo, Dataverse, OSF, figshare searches for prediction-market settlement corpora, or the arXiv:2606.04217 record) plus the CC BY 4.0 errata page, each recorded in the ADR-012 shape and re-fired through `pmexperiment.admissibility`, **before** the register asserts that every route fails. Zero dollars, no account, no venue contact. The repository itself states this would still leave element (1), chain of title and the AI-clause search open — so the resolution here is a **label**, not necessarily a PERMITTED.
- **Confidence:** HIGH that the gap and the freeze are exactly as stated — both are in the repository's own words at docs/LICENCES.md:674 and :844-846; MEDIUM on weight, since the omission is squarely disclosed and its bias direction is named as fail-closed.
- **Could later commits invalidate this?:** No — live HEAD equals the anchor, and the addendum at docs/LICENCES.md:793-846 is the final word on this candidate.
- **Disclosed by authors?:** **Yes** (PMExperiment/docs/LICENCES.md:674, :675, :405-411; PMExperiment/report.md:306-314; PMExperiment/HYPOTHESES.md:233-238) — the authors disclose the unfetched class, call it "**the sharpest gap**", and name the direction of bias as fail-closed. This finding is therefore READ and capped at S3. It adds only that the closure of 2026-09-02 states an "every route" quantifier over a space the same repository says was **sampled, not enumerated**, in the one class it identified as most likely to pass, and froze the verdict rather than spending one HTTP GET.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP, and both singled out the disclosure handling as correct: READ, capped at S3, the authors credited in their own words ("the sharpest gap"), and the addition confined to the 2026-09-02 "every route" quantifier and the freeze at docs/LICENCES.md:844-846. Every citation line-exact; the four robots.txt reads confirmed as 1 + 3 at REGISTRATION.md:477-478, and the 1,201,580,990 rows spanning 2022-11-21 → 2026-04-28 confirmed at DECISIONS.md:458 and HYPOTHESES.md:218.

---

### AUDIT-A-PMExperiment-8

- **ID:** AUDIT-A-PMExperiment-8
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** the registered effect band, Section 3 — the companion CPI study registered as evidence *against* the effect inside the Canadian-permitted categories
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3 — a registered input to the band's "against" column carries an n but no power figure, in a repository whose founding premise is that an underpowered null is not a null
- **Label:** DERIVED (MDE computed with the repository's own `pmexperiment.power.minimum_detectable_effect` and `registry.Z_CRITICAL`, on the registered dispersion constants)
- **Claim challenged (verbatim, with file:line):**
  > "The companion CPI study
  > (*Zero-Price Contracts and the Favorite-Longshot Bias in CPI Prediction
  > Markets*, SSRN 7087538, 95 contracts over 12 months) finds **no** classic
  > favourite-longshot bias — registered here as evidence that the effect
  > inside the permitted categories is heterogeneous and may be absent in some
  > series."
  — PMExperiment/REGISTRATION.md:238-243; quoted verbatim into PMExperiment/docs/BAND.md:50-55, carried into the Pass-2 input table as an "against" row at PMExperiment/docs/BAND.md:285 and into the stage log at PMExperiment/progress.md:468-470

- **Evidence (figures each with n, file:line):**
  1. **The n travels with the figure (standing rule 13) but no minimum detectable effect is ever computed for it.** Grepping the snapshot, the n = 95 figure appears at REGISTRATION.md:240, docs/BAND.md:52, docs/BAND.md:285, progress.md:468-469 and DECISIONS.md:268-269, and **no power figure accompanies any occurrence**.
  2. **The repository's founding premise is that this is exactly the error to avoid:** "NPDExperiment closed at *unresolved-at-achievable-power*: realized minimum detectable contrast **0.0512** against an effect band of **0.01 to 0.05**, discovered after **415 days** of collection" — PMExperiment/CLAUDE.md:54-58.
  3. **Every input needed to compute it is in the repository:** the formula "MDE = z · sqrt(v̄ / n_T)" with z = 2.0 (PMExperiment/REGISTRATION.md:99-101; `pmexperiment/power.py:37-45`; `registry.Z_CRITICAL = 2.0`), the tail-cell planning dispersion "prices near 5c or 95c give p(1−p) ≈ 0.0475" (PMExperiment/REGISTRATION.md:122-123), and Krause's implied mean bucket price of **0.117** for a comparable "below 30c" bucket (PMExperiment/docs/BAND.md:132).
  4. **The verdict map the repository applies to its own cells would give this study DEGRADED at best, never GO** (PMExperiment/REGISTRATION.md:108-112) — i.e. the CPI study could not have detected an effect anywhere in the lower half of the very band it is registered against.
  5. **Direction of the error is against H1.** The CPI null is one of only **two** "against" rows in the Canadian-filter pass (PMExperiment/docs/BAND.md:285-286) and part of "the Canadian doubt, registered before any measurement and never tested" (PMExperiment/README.md:194).
- **Recomputation:** inputs n = 95 (REGISTRATION.md:240), z = 2.0 (`registry.py:9`), and three candidate dispersions — v̄ = 0.0475 (REGISTRATION.md:122-123), v̄ = 0.117 × 0.883 = 0.10331 (docs/BAND.md:132), v̄ = 0.04 × 0.96 = 0.0384 (the study's own comparator settle rate). Method: the repository's own `pmexperiment.power.minimum_detectable_effect`, plus a Wilson interval for illustration. Script `scratchpad/work/agentA-PM-consolidate/recheck.py`, run 2026-09-04:
  - MDE(n = 95, v̄ = 0.0475) = **0.04472** = 4.47 points → DEGRADED; n needed for GO (MDE ≤ 0.02) = **475**.
  - MDE(n = 95, v̄ = 0.10331) = **0.06595** = 6.60 points → DEGRADED, reaching only the top **23.4 %** of the registered 2–8 point band; n needed for GO = **1,033**.
  - MDE(n = 95, v̄ = 0.0384) = **0.04021** = 4.02 points → DEGRADED.
  - At a conventional 80 % power (two-sided α = 0.05) the same n = 95 gives **6.26** points (v̄ = 0.0475) and **9.24** points (v̄ = 0.10331) — the second lying entirely **above** the registered band top of 8.00.
  - Illustrative interval: 4 of 95 settling YES (Krause's 4.0 % rate, printed beside it at docs/BAND.md:48-49) gives a Wilson 95 % interval of **[0.0165, 0.1033]**, **8.68 points wide — wider than the whole 6-point registered band**. n = 95 is contracts *in total over 12 months*, so the longshot-bucket n is at most 95 and the true interval is at least this wide.
- **What would resolve it:** one sentence in Section 3 or `docs/BAND.md` recording the CPI study's MDE beside its n, and restating the registered inference from "the effect … may be absent in some series" to "that series is uninformative below roughly 4–6.6 points". Zero-cost, document-only, and exactly the arithmetic Section 0.4 already performs for this repository's own cells.
- **Confidence:** HIGH for the arithmetic (it uses the repository's own formula, constants and cited figures); MEDIUM for its weight, because the dispersion of the CPI study's own price bucket is not published in this repository and three plausible values were carried rather than one.
- **Could later commits invalidate this?:** No — Section 3 is registered and Amendment 2 fixes the band as computed once (PMExperiment/HYPOTHESES.md:153-157); live HEAD equals the anchor.
- **Disclosed by authors?:** **No.** The n is disclosed everywhere the figure appears (standing rule 13 working as designed) and DECISIONS.md:269-270 notes that "The band's bottom travels with a large n; its top travels with none" — but **no document computes or states what n = 95 could detect**, and the study is nonetheless registered as evidence that the effect "may be absent".
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP. Both reproduced every recomputation independently: MDE(95, 0.0475) = 0.04472, MDE(95, 0.10331) = 0.06595 (top 23.4 % of the 2–8 point band), MDE(95, 0.0384) = 0.04021, the GO thresholds n = 475 and n = 1,033, the 80 %-power values 0.06265 and 0.09239, and the Wilson interval [0.0165, 0.1033], 8.68 points wide. Both confirmed by grep that the n = 95 figure appears in exactly five places and that no power figure accompanies any of them.

---

### AUDIT-A-PMExperiment-9

- **ID:** AUDIT-A-PMExperiment-9
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** Stage A / the Kalshi access gate, condition 5 — the ground that "the API Developer Agreement is unreadable by automated means"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — a named ground of the fired gate rests on a blocker the same repository dissolved elsewhere one day later and never re-measured; the verdict itself very likely survives on the independent terms ground
- **Label:** READ (documentary; no request was sent by this audit)
- **Claim challenged (verbatim, with file:line):**
  > "**API Developer Agreement** — `https://kalshi.com/developer-agreement`,
  > **unreadable by automated means on 2026-08-29**: curl and server-side fetch
  > both received HTTP 429 with a Vercel bot-challenge page; a headless-browser
  > render timed out at the same checkpoint."
  — PMExperiment/docs/ACCESS.md:44-47

- **Evidence (figures each with n, file:line):**
  1. **The unreadability is load-bearing in the closure record.** It is a named ground of the fired gate row — "5 — terms permit keyless automated reading | FAIL, fails closed (… **the API Developer Agreement is unreadable by automated means**)" — PMExperiment/REGISTRATION.md:382; of the stage-log access table (PMExperiment/progress.md:46); and of the register line (PMExperiment/HYPOTHESES.md:173).
  2. **One day later, in this same repository, the identical blocker class was dissolved by one header.** "**First, the unreadability claim is false.** Bare `curl` returns 403; the same `curl` with nothing added but a browser `User-Agent` returns **HTTP 200**. The in-force instruments were one header away." — PMExperiment/docs/LICENCES.md:522-524 (Stage D, 2026-08-30); same at PMExperiment/progress.md:1054-1056, PMExperiment/DECISIONS.md:528, PMExperiment/README.md:58, PMExperiment/report.md:271.
  3. **The repository generalised the discovery into a symmetric rule and then applied it to Dune only.** "**Second, PROHIBITED on an unread instrument is a synthesized value.** … **ADR-012 has no direction-of-travel exemption**, and standing rule 5 … forbids it in both directions" — PMExperiment/docs/LICENCES.md:534-539; "the rule runs both ways" — PMExperiment/README.md:52-54. A grep of the whole snapshot finds `User-Agent` in exactly **five** places, **all five the Dune correction** (README.md:58, DECISIONS.md:528, report.md:271, progress.md:1055, docs/LICENCES.md:523). **The method was never turned back on the Kalshi 429.**
  4. **The Kalshi surface is itself listed as unread:** "| **Kalshi's non-PDF surface** — main Terms of Use, help centre, API documentation licensing | one 3-page Data Terms PDF was the whole of the Kalshi reading in this stage |" — PMExperiment/docs/LICENCES.md:679.
  5. **A second recorded input to standing rule 12 rests on the same unretried challenge:** "`kalshi.com/robots.txt`: HTTP 429 bot-challenge page in 0.071 s (the Website refuses unauthenticated automated readers before robots.txt is even served)" — PMExperiment/docs/ACCESS.md:56-59.
- **Recomputation:** none. No request was sent by this audit; re-probing a third-party host is outside the audit's read-only scope. The counts above (5 `User-Agent` hits, all Dune) are greps over the snapshot.
- **What would resolve it:** one single-shot fetch of `https://kalshi.com/developer-agreement` with a browser `User-Agent`, recorded in the ADR-012 shape (clause, effective date, fetch date). Either it returns the instrument — in which case a leg of the Stage A verdict must be rewritten from "unreadable" to whatever it says — or it returns 429 again, in which case the blocker is confirmed measured rather than assumed.
- **Confidence:** MEDIUM — the asymmetry of treatment is documented beyond doubt, but a Vercel 429 bot challenge is not the same mechanism as the Cloudflare-style 403 the header defeated at Dune, so the blocker may well be genuine. What is certain is that it was never re-measured after the method existed. The gate verdict would very likely survive either way, because the Data Terms of Use prohibition (PMExperiment/docs/ACCESS.md:26-42) is independent of it.
- **Could later commits invalidate this?:** No — live HEAD equals the anchor and nothing in the repository after 2026-08-30 re-probes any Kalshi host.
- **Disclosed by authors?:** **Partially** — PMExperiment/docs/LICENCES.md:679 records Kalshi's non-PDF surface as unread. **Not disclosed:** that the browser-`User-Agent` discovery of 2026-08-30 was never connected to the Kalshi 429 of 2026-08-29, while the "unreadable" ground is repeated unqualified in the closure record.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP. The decisive grep reproduces exactly for both: case-sensitive `User-Agent` occurs in exactly five places in the snapshot (README.md:58, DECISIONS.md:528, report.md:271, progress.md:1055, docs/LICENCES.md:523) and all five are the Dune correction. Verifier 1 adds that a case-insensitive grep would additionally hit `User-agent: *` robots.txt lines at REGISTRATION.md:477, progress.md:724, report.md:170 and docs/ACCESS.md:108, which are not header-method uses and do not disturb the claim.

---

### AUDIT-A-PMExperiment-10

- **ID:** AUDIT-A-PMExperiment-10
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** Stage A access gate, condition 4 — price history retrievable to 30 days before close, and the feasibility of the registered S30 snapshot
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — a "fails closed" condition rests on n = 1 whose qualifying property is unrecorded; condition 5 fails independently, so the verdict stands
- **Label:** READ (documentary; the grep is over the snapshot)
- **Claim challenged (verbatim, with file:line):**
  > "| 4 | price history retrievable to 30 days before close | **NOT DEMONSTRATED — fails closed** | candlesticks endpoint works keylessly on a just-settled traded market (1 candle, fields `price`, `yes_bid`, `yes_ask`, `volume_fp`, `open_interest_fp`); the one ≥ 30-day-old settled market tested (`NASDAQ100-24OCT25-T21499.99`, closed 2024-10-25) returned HTTP 200 and **0 daily candles** over T−40d..T; ambiguous, counted as ambiguous, attributed to nothing |"
  — PMExperiment/docs/ACCESS.md:21

- **Evidence (figures each with n, file:line):**
  1. **n = 1 market, one interval.** The whole evidence for the failing side of condition 4 is a single ticker at a single `daily` granularity; the request log records "3 candlestick reads (2 returned zero candles, 1 returned one candle)" — PMExperiment/docs/ACCESS.md:84-85 — inside a total probe budget of **13** requests (PMExperiment/progress.md:59). No second market, no second series, no hourly or minute interval and no second date range was tried.
  2. **The condition's own precondition is unrecorded.** The registered condition reads "4. Price history is retrievable back to 30 days before close **for markets whose lifetime reaches that far**, so S30 is computable." — PMExperiment/REGISTRATION.md:151-152. The tested market's open time or lifetime appears nowhere: grepping the snapshot, `NASDAQ100` occurs **exactly once**, at docs/ACCESS.md:21. "≥ 30-day-old" in that row means *closed ≥ 30 days before the probe*, which is a different property from *open for ≥ 30 days*. A zero-candle response over T−40d..T is the expected result for a market that did not exist 40 days before its close, in which case the probe cannot bear on the condition either way.
  3. **The row's own label is internally split.** The cell says "ambiguous, counted as ambiguous, attributed to nothing" (docs/ACCESS.md:21) and PMExperiment/progress.md:44 repeats "ambiguous, counted ambiguous" — while the verdict paragraph converts it into a failing condition ("conditions 3 and 4 fail closed as unmeasured or undemonstrated", PMExperiment/docs/ACCESS.md:9-12) and the fired gate row states it as a finding ("NOT DEMONSTRATED, fails closed (0 daily candles on the one ≥ 30-day-old market tested; recent-market candles work)", PMExperiment/REGISTRATION.md:381).
  4. **Consequence is bounded and must be said.** Condition 5 fails independently on the recorded terms (PMExperiment/docs/ACCESS.md:22, :26-42), so PENDING_ACCESS stands whatever condition 4 does. What changes is the *number of independent grounds* the closure claims, and whether S30 — the snapshot the entire Canadian question rests on (PMExperiment/REGISTRATION.md:63-67) — is on record as infeasible.
- **Recomputation:** none — there is no arithmetic to redo; the point is that the deciding sample is n = 1 and its qualifying property is unrecorded.
- **What would resolve it:** record the tested market's open time beside its close time, and either (a) a second probe on a market whose lifetime demonstrably exceeds 30 days, or (b) restate condition 4 as **NOT MEASURED** rather than **NOT DEMONSTRATED**, since a probe whose precondition is unverified measures nothing. Both cost one line of document or one request inside the existing budget.
- **Confidence:** MEDIUM — that the record is silent on the tested market's lifetime is certain and checkable by grep; that the market in fact had a short lifetime is an inference from the ticker's form (a dated strike on an index-close series) and is **not** established by anything in the repository.
- **Could later commits invalidate this?:** No — Stage A's probe budget was spent on 2026-08-29 and no later stage sent a Kalshi request; live HEAD equals the anchor.
- **Disclosed by authors?:** **Partially** — the ambiguity and the n = 1 are stated in the same cell (docs/ACCESS.md:21) and repeated at progress.md:44. **Not disclosed:** that the registered condition is conditional on the tested market's lifetime, and that this property was never recorded.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP. The load-bearing grep reproduces for both (`NASDAQ100` occurs exactly once in the whole snapshot, at docs/ACCESS.md:21), the "3 candlestick reads (2 returned zero candles, 1 returned one candle)" log and the 13-request budget are exact, and the internal split between "ambiguous, counted as ambiguous" and "NOT DEMONSTRATED — fails closed" is confirmed at both ends.

---

### AUDIT-A-PMExperiment-11

- **ID:** AUDIT-A-PMExperiment-11
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** the terminal data-availability closure — "the calibration question is unmeasurable at this house's standard" — and the bar that stops the search
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3 — the unasked route is disclosed in the repository's own completeness table, so this is capped at S3; what is added is that the stated bar does not on its face reach it
- **Label:** READ (documentary)
- **Claim challenged (verbatim, with file:line):**
  > "**The consequence, stated plainly: the calibration question is unmeasurable at
  > this house's standard until an authorization is granted.** Not unmeasurable in
  > principle, and not unmeasured because the arithmetic came out badly — the power
  > gate has still never fired, on any venue, over any region. Unmeasurable because
  > every route to the records either prohibits the reading or cannot show it is
  > permitted"
  — PMExperiment/docs/LICENCES.md:706-712

- **Evidence (figures each with n, file:line):**
  1. **A whole class of route to the same records was named and never asked:** "| **regulatory disclosure routes** | Kalshi is a CFTC-designated contract market with public reporting obligations; whether settlement history is obtainable from a **regulator** rather than a venue was never asked |" — PMExperiment/docs/LICENCES.md:682; same item at PMExperiment/progress.md:1104-1105.
  2. **The bar the repository uses to stop searching does not, on its own words, reach this route:** "**No fourth venue is proposed.** … proposing a new venue after three routes close is how a measurement-only project turns into a search for a venue that will say yes" — PMExperiment/docs/LICENCES.md:759-763, repeated as "**And no fourth venue.**" at PMExperiment/REGISTRATION.md:1113-1116. A regulator is not a venue and holds no terms of use over a market participant's reading; the objection stated is about **venues**.
  3. **The route bears on the deciding element.** A regulator's public disclosure file is published under a statutory obligation — the document class most likely to satisfy ADR-012 with a printed effective date, the element on which candidate 2 failed (PMExperiment/docs/LICENCES.md:398-403).
  4. **It appears in none of the four terminal reopening conditions** (PMExperiment/REGISTRATION.md:1085-1098 and :1161-1167; PMExperiment/HYPOTHESES.md:305-321 and :352-358; PMExperiment/README.md:151-162), and Stage E did not re-ask it: "the rest were not re-asked" (PMExperiment/docs/LICENCES.md:846).
  5. **The repository's own record shows that asking outside the read set is what produced its only new information in five stages:** the Kalshi institutional-desk reply of 2026-09-01 came from a route Stage D had not read — "**Two days later a route surfaced that Stage D had not read.**" (PMExperiment/DECISIONS.md:575; PMExperiment/progress.md:1443-1449). Totals for the five stages: **0** dollars, **0** contracts enumerated, **0** market-data requests to Polymarket, **0** requests in Stage E (PMExperiment/REGISTRATION.md:628-630) — the search was stopped at zero marginal cost, not at an exhausted budget.
- **Recomputation:** none.
- **What would resolve it:** one document fetch of a CFTC / DCM public reporting page for Kalshi, recorded in the ADR-012 shape, and either a PERMITTED / PROHIBITED / UNMEASURED verdict on it or an explicit register line saying the route is out of scope and why. Zero dollars, no account, and inside the licence-document scope Stage D already used.
- **Confidence:** MEDIUM — the route's existence and its non-asking are recorded verbatim in the repository; whether a regulator actually publishes contract-level settlement history at the depth the gate needs is unknown to this audit and is not asserted.
- **Could later commits invalidate this?:** No — live HEAD equals the anchor; the closure addendum explicitly declines to re-ask.
- **Disclosed by authors?:** **Yes** (PMExperiment/docs/LICENCES.md:682 and PMExperiment/progress.md:1104-1105 list it among what was not read, and docs/LICENCES.md:684-688 names the direction of bias). This finding is therefore READ and capped at S3. **Not disclosed:** that the "no fourth venue" bar, which is what stops the search, is stated about **venues** and does not on its face cover a regulator.
- **Citation check:** verified (quote EXACT, figures YES) — both verifiers KEEP. Every quotation line-exact, including the unasked regulatory route at docs/LICENCES.md:682, the venue-shaped stopping bar at :759-763 and REGISTRATION.md:1113-1116, and the zero-totals at REGISTRATION.md:628-630; both endorsed the READ label and the S3 cap, and both noted the finding states plainly that it does not assert a regulator publishes the needed depth.

---

### AUDIT-A-PMExperiment-12

- **ID:** AUDIT-A-PMExperiment-12
- **Repository / anchored SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact concerned:** Section 14 reproducibility, applied to the Stage A access-gate figures — the only gate in the repository that ever fired on measured inputs
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S4 — hygiene: a registered requirement stands unmet and unamended. No conclusion is wrong because of it
- **Label:** DERIVED (directory state read from the anchored snapshot and, separately, from the live working tree)
- **Claim challenged (verbatim, with file:line):**
  > "The gate verdict must be regenerable from: the stored raw enumeration and
  > candlestick responses under `data/raw/`, the registered constants in
  > `pmexperiment.registry`, and the registered seed 20260829. A rerun may depend
  > on no other state."
  — PMExperiment/REGISTRATION.md:359-362

- **Evidence (figures each with n, file:line):**
  1. **The probe artefacts were not kept:** "the raw probe responses were not retained beyond this report and the two tickers named above" — PMExperiment/docs/ACCESS.md:88-89.
  2. **`data/` is empty in both trees.** In the anchored snapshot, `data/` contains only `.gitkeep` (0 bytes) and no `data/raw/` exists. In the live tree the same holds and `git status --porcelain --ignored` lists no data artefact — read from `/home/kiros-li/Documents/GitHub/PMExperiment` at **2026-09-04T00:24Z** (**unanchored**; may have changed after the anchor, though the tree is clean at 03d16e71 and carries an operator marker forbidding further sessions). `scripts/` likewise contains exactly one 0-byte `.gitkeep`.
  3. **The consequence for the closure.** The deciding figures of the Stage A gate — "earliest retrievable settled close sits between 2024-01-01 (empty page) and 2024-05-31 (present) … **n = 6** probes" (PMExperiment/docs/ACCESS.md:72, which enumerates the six brackets, and PMExperiment/REGISTRATION.md:391; the phrase "n = 6 bracketing probes" verbatim is at PMExperiment/DECISIONS.md:104 and PMExperiment/progress.md:43), the **11**-request latency range 99.9–213.8 ms (PMExperiment/docs/ACCESS.md:71), the 0-daily-candles reading (:21) — cannot be re-derived by anyone, including a later operator, from anything in the repository. They are re-obtainable only by re-probing a venue the repository has closed itself off from.
  4. **The rigour was available and was applied elsewhere.** Stage E audited "**32 commits, 189 reachable objects, every blob decompressed**" for credentials (PMExperiment/progress.md:1537-1539) — whole-history rigour applied to secrets but not to the gate's own inputs.
- **Recomputation:** none; a directory listing and a `git status` are the whole evidence.
- **What would resolve it:** a one-line amendment to Section 14 recording that the Stage A probe responses were not retained and that the access-gate figures are therefore reproducible only by re-probing — bringing Section 14 into line with docs/ACCESS.md:88-89, rather than leaving a registered reproducibility requirement standing unmet.
- **Confidence:** HIGH — the non-retention is stated by the authors and the empty `data/` is directly observed in both the snapshot and the live tree.
- **Could later commits invalidate this?:** No — no commit after 2026-08-29 adds a data artefact, and live HEAD equals the anchor with a clean tree.
- **Disclosed by authors?:** **Partially** — the non-retention is disclosed at PMExperiment/docs/ACCESS.md:88-89. **Not disclosed:** that this leaves Section 14's registered requirement unmet for the only gate that ever fired on measured inputs. Hygiene, not a wrong conclusion, hence S4.
- **Citation check:** corrected — two citation fixes, each rechecked against SNAP: (a) the Section 14 quote runs to PMExperiment/REGISTRATION.md:359-**362** ("A rerun may depend on no other state." ends on :362), not :359-361, as verifier 2 noted — a short range, not a mislocation; (b) the composite phrase "n = 6 bracketing probes" was a blend — REGISTRATION.md:391 reads "n = 6 probes" and docs/ACCESS.md:72 enumerates the six brackets without the phrase, while the exact phrase sits at DECISIONS.md:104 and progress.md:43, now cited. Otherwise verified (quote EXACT, figures YES): both verifiers independently confirmed the empty `data/` and `scripts/`, the absent `data/raw/`, and every deciding figure at its cited line, and both endorsed S4.

---

## What Agent A checked and found sound

Each of these is a place where the Direction-A thesis would have bitten if the record were weaker. It is not. Listed with what I would have expected to find if the thesis held there, and did not.

1. **The zero-measurement claims are true in the artefact record.** "No price bucket was built, no dispersion computed, and no statistic relating a price to an outcome exists in this repository" (PMExperiment/progress.md:681-682, :1370-1372; PMExperiment/REGISTRATION.md:588-591) is consistent with `data/` holding only a 0-byte `.gitkeep` in both snapshot and live tree, with `pmexperiment/` containing no I/O, no network call and no outcome field, and with `power.py` never being invoked on real inputs anywhere in the package or tests. I expected a retained probe dump or a stray CSV contradicting "zero enumerated"; there is none.
2. **The band arithmetic reproduces exactly.** Every figure in `docs/BAND.md`'s Pass-1 table, the crossing points, the 0.0300 fee+spread floor, the 0.0015 route-X margin, the 0.00195 FX-base understatement and the 0.00135 held-route counterpart all reproduce from `registry.py`'s constants; C(0.95) = 0.0785 and C(0.05) = 0.0515 match PMExperiment/REGISTRATION.md:338. **No arithmetic error found anywhere in the band work.**
3. **The k-turnover sensitivity is reported and non-load-bearing, exactly as claimed.** I reproduced C_H at k = 1, 12 and ∞ for all ten buckets: the band top clears at every bucket on both routes under every k and the band bottom clears at none. Amendment 4's claim at PMExperiment/REGISTRATION.md:820-824 is arithmetically correct. (Finding 2 is that the *other* two assumptions were never varied, not that this one was mishandled.) k = 1 binds and biases toward BAND-EMPTY, and `registry.FX_TURNOVER_REGISTERED = 1.0` leaves no path by which a favourable k enters a verdict.
4. **The direction correction (ADR-009) is right and is the opposite of self-serving.** Restating the published longshot overpricing as its exploitable complement moves every magnitude to 0.883–0.95, where the price-proportional FX is largest — a correction that made the repository's own case harder. `return = gap ÷ price` reproduces −40.0 % at 5c and +3.16 % at 95c, and the return reading of Krause's −0.077 would imply a mean price of 0.043 and make the largest cited figure the smallest.
5. **The z = 2.0 gate convention is permissive, not restrictive.** MDE = 2·sqrt(v̄/n) is a detection threshold at roughly 50 % power; an 80 %-power MDE would be about 1.4× larger and the required n 1.96× larger. This makes the gate *easier* to pass, so it cuts against the thesis rather than for it, and it is recorded here rather than as a finding.
6. **The Stage-A depth blocker's later expiry is handled correctly.** Section 15.4 records 2021 depth on the licence (PMExperiment/REGISTRATION.md:538) and ADR-016 checks the wording of the earlier claim against it: "Stage A wrote that the 2021→Apr 2025 span is *'not reproducible keylessly'* — a claim about the keyless surface, not about the archive — and that phrasing is exactly right under the reply. **Had it been written as 'the history does not reach 2021' it would now be false.**" (PMExperiment/DECISIONS.md:621-626). That is the expired-blocker check performed by the authors on themselves, correctly.
7. **The BAND-OPEN label is not inflated.** Everywhere it appears it carries "It must not be written anywhere as evidence that an edge exists" (PMExperiment/REGISTRATION.md:614-618, PMExperiment/HYPOTHESES.md:290-293, PMExperiment/README.md:143-145). The Direction-B failure mode is guarded hard.
8. **Bürgi's 3.0 "exactly ties the 0.0300 floor"** (PMExperiment/REGISTRATION.md:1052-1053) is stated as a tie, not rounded into a failure, in the same sentence that calls the pair "fails". The tie arises only at k → ∞, which does not bind. Calling a zero-expected-profit tie a failure at the non-binding limit is defensible and is disclosed in the same clause; not a finding.
9. **The Section 13 empty-prior discipline.** The prior arrives at closure, is deliberately not backfilled (PMExperiment/REGISTRATION.md:1015-1029), may never be described as pre-registered, and the closure explicitly says no verdict may be read against it. This is the opposite of the failure I was hunting for.
10. **The operator-decline is correctly quarantined from the evidence.** ADR-017 (PMExperiment/DECISIONS.md:648-664) files it as a cost decision, not a finding, and states the reason a reader would otherwise conflate them; the route stays EXISTS-AND-UNTRAVELLED rather than becoming a refusal (PMExperiment/REGISTRATION.md:1065-1067). I could not construct an honest over-closure finding out of the decline itself; finding 2 attacks only the *figure* offered as its input.
11. **Section 16's registered closure conditions are recorded as never met, not as satisfied by a substitute** (PMExperiment/REGISTRATION.md:605-612, :636-641). A repository closing on access could easily have passed this off as the registered closure; it does the opposite and pins the distinction with a mutation test.
12. **The Kalshi reply was not promoted beyond what it is.** It is recorded UNMEASURED under the repository's own procedure, with the strongest argument for admitting it stated at full strength and refused (PMExperiment/docs/ACCESS.md:261-283); the three questions that survive the entity requirement — fee, publishing rights, AI/ML consent — are recorded absent rather than as zero (PMExperiment/docs/ACCESS.md:302-315).
13. **The Dune self-correction is real and complete**, and ADR-015 generalises the lesson symmetrically (PMExperiment/docs/LICENCES.md:512-544). I checked for the same failure surviving elsewhere in the licence read and found only the Kalshi 429 case, raised as finding 9.
14. **Amendment 1's retraction and the ADR-013 self-conviction on the undated Kalshi terms** are honest reversals against the repository's own interest. I checked for the pattern where a self-criticism is used decoratively while the verdict quietly survives; each correction is stated as narrowing the record, and PMExperiment/report.md:303-304 says so plainly ("Every correction made the record narrower or weaker. None changed a verdict") — which is true of all of them.
15. **BAND-NARROW's unevaluated volume clause.** Section 15.2 says the clause "cannot be evaluated, because Section 1's volume floor was never registered" (PMExperiment/REGISTRATION.md:417), and the floor is registered the next day as Amendment 5. Re-evaluation would not have changed the verdict — the clause also needs an enumeration that never existed, and firing BAND-NARROW would have been a *harsher* verdict, not a softer one. Not a Direction-A finding.
16. **The two settled records with `result` fields.** PMExperiment/README.md:102-106 refuses to round "eleven probe requests received two settled records carrying `last_price_dollars` and `result`" into "no market price was ever read". The outcome-blindness claim is stated with its own exception; sound.
17. **The mutation harness faults are recorded, not hidden**, and Stage E reports zero harness faults against fourteen mutations (PMExperiment/progress.md:1529-1535). I looked for a mutation reported green that had not mutated and found the repository had already caught every instance itself.
18. **ETA discipline is honest against itself.** Every stage records actuals against stated ETAs including the one stage that overran by 5.5× (PMExperiment/progress.md:947-965); no ETA cell was filled retrospectively, and Stage C's 2b cell is left "never stated, never armed" (PMExperiment/progress.md:691).
19. **Amendment 9 is not a rationalisation.** I checked whether "a regulatory change to trading access is not evidence about data permission" (PMExperiment/REGISTRATION.md:1141-1143) was being used to bar a real reopening. On the data-permission point it is not: the data terms it cites carry no entity-type qualification (PMExperiment/docs/ACCESS.md:132-136), and the amendment **adds** a reopening condition rather than only removing one. (Finding 3 concerns a different sentence in the same amendment — the on-chain conjunction — not this rule.)

## Dropped at consolidation

**Nothing was dropped for lack of a locatable quote, a figure, or an `n`.** Every draft finding carried a verbatim quote with file:line, and each quote was re-verified line-exact against `SNAP/PMExperiment` at the anchored SHA during consolidation, along with every recomputed figure. What changed:

- **DRAFT-p1-register-4 and DRAFT-p2-progress-1 were merged into AUDIT-A-PMExperiment-1.** Both attacked the same closure — Amendment 8's "stated precisely and exhaustively" reopening set — on the same ground, that a registered reopening path was dropped from it without a recorded reason, differing only in *which* path (Section 15.1's Kalshi account path; Amendment 6's Polygon route). The merged finding keeps both quotes, every distinct file:line from both drafts, both resolution paths, and adds the Section 16 calendar-accrual omission as a third, explicitly weaker instance that is **not** counted. Severity stays S2 and confidence HIGH.
- **DRAFT-p1-register-6 and DRAFT-p2-progress-5 were merged into AUDIT-A-PMExperiment-6.** Both attacked the same closure — the permanent restriction of any reopened power gate to 91–99c — on the same ground, that the only cited magnitude which clears the registered cost floor sits in the excluded 81–90 decile. The merge keeps p2's argument that the same magnitude is what defeats BAND-NARROW, p2's band-top margin comparison (0.02435 vs 0.02150), and p1's round-trip-margin-inside-its-own-slack caveat. Label resolved to **DERIVED** because the cost constants were taken from `pmexperiment/registry.py`, not from a document.
- **DRAFT-p1-register-7 and DRAFT-p2-progress-3 were merged into AUDIT-A-PMExperiment-7.** Both attacked the same closure — Stage D candidate 2's UNMEASURED on ADR-012 element (2) — on the same ground, that the deciding element was never sought in the document class that carries it by construction. The merge keeps p2's CC BY 4.0 errata-page evidence and the LICENCES.md:844-846 freeze, and p1's terminal "every route" quantifier and reopening-condition-3 point. Disclosed = yes, so severity is capped at **S3**.
- **DRAFT-p2-progress's "found sound" item 11 was folded into AUDIT-A-PMExperiment-5 rather than dropped.** The second reader identified the same U24/P30 inconsistency the first reader raised as a finding, and declined to raise it. Both of that reader's counter-arguments — that the registered gate requires a *measured* v̄ and n_T, and that standing rule 5 forbids synthesizing them — are now carried in the finding's confidence field, which is why it is S2 and MEDIUM rather than S1.
- **Line-number corrections made during verification** (no substance affected): `REGISTRATION.md:1052-1053 → :1051-1053` (the "every magnitude … fails" sentence begins at 1051); `REGISTRATION.md:133-136 → :132-137` (the Section 0.4 expectation sentence); `REGISTRATION.md:457-459 → :456-459`; `REGISTRATION.md:227-228 → :226-228`; `REGISTRATION.md:1082-1083` confirmed exact; `DECISIONS.md:713 → :711-712` (the ADR-018 mutation list item); `DECISIONS.md:266-270 → :265-270`; `DECISIONS.md:270-271 → :268-269` (the n = 95 occurrence); `docs/LICENCES.md:215-225 → :214-225`; `progress.md:330 → :330-332`; `progress.md:1445-1447 → :1443-1449`; `progress.md:562-563 → :561-562` (the "do not widen the region" prompt line — consolidation wrote `:327-328` here, which is the Stage B prompt; both verifiers caught it and it is corrected in finding 6); `README.md:151-166 → :151-162` (the three-item list; :164-166 is the separate non-reopening rule).
- **No draft finding was downgraded or relabelled other than as stated above.** DRAFT-p1-register-1's label was reconfirmed as DERIVED after checking that the cost constants it recomputes from live in `pmexperiment/registry.py:53-57, 66` rather than only in prose; DRAFT-p2-progress-2's severity was left at S3 because the verdict it attacks survives independently on the terms ground, which the finding states.
- **One item points against this agent's thesis and is flagged for Agent B rather than raised here:** the z = 2.0 convention makes the power gate *easier* to pass (item 5 of "found sound"), so any Direction-B reading of the gate's strictness should start there.

## Verification pass — two independent verifiers

Two verifiers re-read every finding against `SNAP/PMExperiment` at the anchored SHA: verifier 1 on
citation fidelity (quote, line, figure, n), verifier 2 on disclosure and labelling. **No finding was
dropped:** neither verifier returned a NOT_FOUND quote or a failed figure anywhere, and both
independently reproduced every recomputation in this file to the digit and every grep count exactly.

**Outcome: 12 findings in, 12 out — 7 kept as written, 5 corrected, 0 dropped.** The per-finding
record is the `Citation check` line at the end of each finding. Corrected: 1 (a count wording), 2
(two citation nits), 3 (three points, on which the verifiers split), 6 (one wrong line number), 12
(a short quote range and a phrase attribution). No severity, class, direction or label changed;
finding 3's disclosure field moved from **No** to **Partially** and its confidence from HIGH to
MEDIUM, both on evidence I re-read myself at REGISTRATION.md:974-986 and DECISIONS.md:381-384.
One non-corrective addition was also applied, at verifier 2's suggestion and confirmed against the
snapshot: finding 4 gains an evidence item recording that its non-reopening rule originates in the
operator's Stage E prompt, logged verbatim at progress.md:1304.

**The one place the verifiers disagreed** is finding 3, where verifier 1 recommended KEEP with a
single citation nit and verifier 2 recommended CORRECT on three points. I checked all three against
the snapshot and followed verifier 2, because each is right on the source — most importantly that
the register does record and reject a narrow-scope counterargument to the crawler bullet, so
"0 documents notice the conflict" could not stand as written. The reasoning is recorded in that
finding's `Citation check` line, and the residual that survives all three corrections is stated
there.

**One regression this pass caught in the consolidation itself.** The "Dropped at consolidation"
list above recorded `progress.md:562-563 → :327-328` as a line-number correction for the "Do not
widen the region to improve the count" prompt line. The correction was wrong: the sentence is at
progress.md:561-562, inside the Stage C prompt, and :327-328 is the Stage B prompt. Both verifiers
found it independently. Finding 6 and the consolidation list are both fixed.


## Live-repo access log

Merged from both drafts, plus the consolidator's own single read-only check. Purposes used: (1) git history/provenance; (2) untracked or gitignored working-tree state under `data/` and `scripts/`. **No file in the audited repository was opened for writing, and no git command other than `status`, `rev-parse` and `log` was run.**

**Reader p2-progress — BEFORE**, `git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` (2026-09-04T00:23Z):

```
```

(empty — clean working tree; `git rev-parse HEAD` = `03d16e71dbf25a86c529884662d02136f8e82334`, identical to the anchored SHA)

**Reader p2-progress — AFTER**, same command (2026-09-04T00:34Z):

```
```

(empty — unchanged)

**Reader p1-register — BEFORE and AFTER**, same command (both around 2026-09-04T00:26Z):

```
```

(both empty — clean working tree; HEAD at read time `03d16e71dbf25a86c529884662d02136f8e82334`, no commits after the anchor)

**Consolidator — BEFORE**, same command (2026-09-04T04:57:34Z):

```
```

**Consolidator — AFTER**, same command (2026-09-04T04:57:34Z):

```
```

(both empty; `git rev-parse HEAD` = `03d16e71dbf25a86c529884662d02136f8e82334` and `git log 03d16e71dbf25a86c529884662d02136f8e82334..HEAD` returned nothing, so **no commit exists after the anchor**)

**Ignored entries observed** (`git status --porcelain --ignored`, 2026-09-04T00:24Z), recorded because one of them is not tooling dirt:

```
!! .mypy_cache/
!! .pytest_cache/
!! .ruff_cache/
!! .venv/
!! _CLOSED_DO_NOT_RUN_HERE
!! pmexperiment/__pycache__/
!! tests/__pycache__/
```

`_CLOSED_DO_NOT_RUN_HERE` (747 bytes, mtime 2026-09-02 22:38, untracked and excluded via `.git/info/exclude`) is an **operator closure marker**, not repository dirt caused by this audit and not tracked at the anchored SHA. It reads in part: "THIS REPOSITORY IS CLOSED. DO NOT RUN A CODING SESSION HERE. … Marker written 2026-09-02 after a session was opened here by mistake." Read 2026-09-04T00:24Z; **unanchored**.

`data/` and `scripts/` each contain exactly one 0-byte `.gitkeep` and nothing else (read 2026-09-04T00:24Z, unanchored). **No untracked or gitignored data artefact of any kind exists in this repository.** No `.env`, keystore, session or credential file was opened at any point.

All finding content was read from `SNAP/PMExperiment/` at the anchored SHA. Recomputations were run with the audit venv; scripts under `scratchpad/work/agentA-PM-p1/`, `scratchpad/work/agentA-PMExperiment-p2/` and `scratchpad/work/agentA-PM-consolidate/`. Nothing was written to any audited repository.
