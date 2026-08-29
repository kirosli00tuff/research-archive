# Sources

Every figure in [the note](docs/the-power-limit.md) was measured somewhere else.
This file maps each one to the repository, the file and the commit it came from,
so a reader can check the note against the primary record without asking this
repository to vouch for itself.

The sibling repositories are closed. Their closing commits do not move, so the
short hashes below are stable references rather than moving branch tips.

**None of these figures was measured here.** This repository holds no market
data, opens no data source, and computes no statistic. It is a secondary source
and it is built to be checkable as one: every value below is typed in
`rplimits/cases.py` as a `Figure` carrying a source key, the keys resolve
against `rplimits/sources.py`, and the generated blocks in this file are
re-rendered and compared by `tests/test_render.py` on every build. A figure
edited in the prose but not in the data — or the reverse — fails the build.

---

## The four power cases

Each carries its hypothesis, the published or assumed effect band it was testing
against, the realized minimum detectable effect, the sample achieved and the
sample required, the cost in time and money, and the exact closure language.

<!-- BEGIN GENERATED: power-records -->
### NPDExperiment — closed 2026-08-25

**Hypothesis.** Given anonymized per-name numeric feature blocks, a frontier LLM ranks next-window cross-sectional returns better than cheap mechanical baselines.

*Source: NPDExperiment/REGISTRATION.md @ 2d3d0ae (2026-08-25).*

**Effect band it was testing against.** Daily rank IC 0.01 to 0.05, the realistic band from the literature, registered in Section 9.2 before any call went out.

*Source: NPDExperiment/REGISTRATION.md @ 2d3d0ae (2026-08-25).*

**Realized minimum detectable effect.** 0.0512 minimum detectable contrast, above the entire 0.01 to 0.05 band, against a pre-registered projection of 0.026 to 0.047. The realized daily contrast standard deviation came in at 0.36339 against a registered assumption of at most 0.2626.

*Source: NPDExperiment/progress.md @ 2d3d0ae (2026-08-25).*

**Sample achieved.** 415 stored daily rankings of 432 eligible window days, 96.1 percent coverage against a 90 percent bar; 404 evaluable days; 125.6 independent-equivalent days after the 3.4 variance inflation the five-session horizon induces.

*Source: NPDExperiment/progress.md @ 2d3d0ae (2026-08-25).*

**Sample required.** Roughly four times the evaluable days, landing near 1,700 trading days of post-cutoff window. No model has one; the window accrues at about 21 trading days a month.

*Source: NPDExperiment/REGISTRATION.md @ 2d3d0ae (2026-08-25).*

**Cost, in time and money.** 6.9378 USD of a 10.00 USD cap across 920 billed gate calls. 411 minutes of recorded stage time across six stages, of which B.1 collection alone was 194 minutes. One irrecoverable read of the sealed window.

*Source: NPDExperiment/progress.md @ 2d3d0ae (2026-08-25).*

**Closure language, exact.** The numeric-LLM question is unresolved at achievable power. Two serious attempts have produced zero positives.

*Source: NPDExperiment/REGISTRATION.md @ 2d3d0ae (2026-08-25).*

**Scope and correction.** The phrase carried into InsiderExperiment's Section 0.1 — discovered "after 415 days of collection" — means 415 days of *stored rankings*, not 415 days of elapsed wall-clock. Scaffold, registration, collection, evaluation and closure all ran on 2026-08-25. The elapsed cost was one day; the 415 is the sample.

### InsiderExperiment — closed 2026-08-25

**Hypothesis.** Opportunistic and cluster insider purchases, disclosed on Form 4, predict positive abnormal returns that survive the operator's measured cost band at achievable size.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Effect band it was testing against.** 30 to 40 bp per month decayed gross — Cohen, Malloy and Pomorski's 82 bp per month over 1989 to 2007, decayed 60 to 70 percent on 2008 to 2024 data — and 13.3 to 34.7 bp per month net at the registered six-month hold.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Realized minimum detectable effect.** 49.35 bp per month, above the whole gross band and the whole net band, against a registered BLOCKED floor of 40 bp committed before the measurement existed. Stable across Newey-West bandwidths: 50.19 at lag 5, 49.11 at lag 63, 49.53 at lag 126.

*Source: InsiderExperiment/(commit) @ cb17046 (2026-08-25).*

**Sample achieved.** 4,585 qualifying events against a registered floor of 1,000; 2,581 sessions at 99.5 percent coverage against a floor of 80 percent; 2,869.9 effective independent periods, which exceeds the raw session count because the variance inflation of 0.899 is below one.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Sample required.** Not a sample requirement. Section 0.4 required about 23 effective names to stay out of BLOCKED; the value-weighted book held 71.9 names behaving like 29.7 effective names, top name 14.9 percent and top five 33.8 percent. The 9.993 percent annualized tracking error is the whole of the 49.35.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Cost, in time and money.** Zero dollars. No paid API was used. 214 wire requests totalling 2.78 GB with zero non-200 responses. About 51 minutes for Stage A.1 and 20 for Z.1 by the commit record. The realized alpha was never read and sits sealed.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Closure language, exact.** The registered primary design cannot resolve the effect at achievable power. The minimum detectable effect is 49.35 bp per month against a registered BLOCKED floor of 40 and against a decayed literature band of 30 to 40 bp per month gross and 13 to 35 bp per month net at the six-month hold. Stage B is never written. The repo closes on the finding.

*Source: InsiderExperiment/REGISTRATION.md @ 12d9fd3 (2026-08-25).*

**Scope and correction.** The corpus is explicitly not the cause: it cleared its floor by a factor of four and a half. The finding is also scoped by universe — 94.2 percent of qualifying-shaped insider purchases happen outside the liquid-500 band this design could trade — so it does not refute the literature it tested against.

### ETFExperiment — closed 2026-08-28

**Hypothesis.** US spot Bitcoin ETF net flow prints predict the next day's BTC return, out of sample, by enough to clear a round trip on Hyperliquid perps.

*Source: ETFExperiment/README.md @ fe60a22 (2026-08-28).*

**Effect band it was testing against.** Rank correlation 0.09 registered, against a published magnitude of 0.18; powers were also computed at a quartered 0.045 and reported beside the registered figure.

*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*

**Realized minimum detectable effect.** Expressed as a required N rather than an effect size. E1 needs 237 admissible days at the published 0.18 and 845 at the registered 0.09; E2 needs 300 at 0.18 and above 1,200 at 0.09. Section 10 requires both co-primaries, so the governing minimum is 300 at the published magnitude and above 1,200 at the registered one.

*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*

**Sample achieved.** 11 admissible days at closure, from a 336-row census — 53 capture-too-late, 243 no-capture, 25 capture-served-no-value, 3 no-printed-value, 1 archive-fetch-failed. 163 projected at the registered 2027-03-31 deadline at the measured forward accrual of 20.8 admissible days per month.

*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*

**Sample required.** 300 governing at the published magnitude, above 1,200 at the registered one. The shortfall at the deadline is 137 days against the governing figure, and 74 days against E1's 237, the most favourable figure anywhere on the record.

*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*

**Cost, in time and money.** Zero dollars, no capital and no credential at any point. 220 charged requests over the repository's lifetime. No outcome value was ever read.

*Source: ETFExperiment/REGISTRATION.md @ 4d11002 (2026-08-28).*

**Closure language, exact.** H1 closes at untestable-at-achievable-power. The registered design cannot resolve the effect at the sample size reachable by the registered deadline of 2027-03-31. The signal was never read and this closure is not evidence about it.

*Source: ETFExperiment/(closing commit) @ 3f5d629 (2026-08-28).*

**Scope and correction.** The 845 / above-1,200 / about-302 triple is real but does not belong to the closure firing. Those are Amendment 6's numbers for what fourteen further months of forward collection would buy: about 302 admissible days by 2027-10-31, which clears the governing 300 at the published 0.18 by two days and clears nothing at the registered 0.09. The closure itself fired on 163 projected against 300 governing at the 2027-03-31 deadline.

### HFExperiment — closed 2026-08-26

**Hypothesis.** The equal-weighted top five names by 12-1 momentum with a skip month in the U-LIQ-500 universe, re-formed on the first trading session of each month, earn positive daily excess return over the equal-weighted universe.

*Source: HFExperiment/REGISTRATION.md @ f13e1d3 (2026-08-25).*

**Effect band it was testing against.** 27.99 bp per day, measured on the already-spent AiTrader holdout, against daily noise near 418 bp implied by 66.4 percent annualized tracking error. The band is the measurement, not a literature range: this design tested its own prior estimate.

*Source: HFExperiment/REGISTRATION.md @ f13e1d3 (2026-08-25).*

**Realized minimum detectable effect.** z 1.668 against a corrected bar of 2.50 over a 2.55-year holdout, interval -4.9 to +60.9. Clearing the bar needed 104.0 percent per year of excess; the book delivered 70.5, a shortfall of 1.5x. Widening 5 names to 50 halves tracking error (66.4 to 31.7 percent) and cuts excess proportionally (27.99 to 10.04 bp per day), so z moves only 1.668 to 1.455 and neither width clears.

*Source: AiTrader/RETURN.md @ f819b68 (2026-07-29).*

**Sample achieved.** One 2.55-year holdout, touched once at commit a0a9ef6. Zero forward shadow observations: the series was disarmed before its first accrual and the verdict was never computed.

*Source: HFExperiment/progress.md @ 82e77a0 (2026-08-28).*

**Sample required.** Under the frozen confidence sequence, with the sample mean holding at 27.99 bp per day, the lower bound clears zero at day 2,061 and clears the measured 4.07 bp per day cost hurdle at day 2,852. Eight to eleven years.

*Source: HFExperiment/REGISTRATION.md @ f13e1d3 (2026-08-25).*

**Cost, in time and money.** Zero dollars deployed and zero capital; the live track was never funded. The cost already sunk is the 2.55-year holdout, spent once and not repeatable, plus four stages of instrument build across 2026-08-23 to 2026-08-25.

*Source: HFExperiment/progress.md @ 82e77a0 (2026-08-28).*

**Closure language, exact.** H-F is 12-1 cross-sectional momentum, tested once in the AiTrader cross-sectional round of 2026-07-26 and resolved on statistical power rather than absent signal.

*Source: HFExperiment/README.md @ 0a0d214 (2026-08-23).*

**Scope and correction.** HFExperiment is a power case by inheritance and by its own registered forward arithmetic, not by a power gate firing inside it. Its own Section 0 fired BLOCKED on the *broker* — IBKR refused fractional quantities through the API, errors 10243 and 10244 — and the repository then closed by operator decision on 2026-08-26 with the shadow series never started. The power resolution belongs to the AiTrader round of 2026-07-26, which HFExperiment's README states in its first sentence and its Section 11 prices at eight to eleven years.
<!-- END GENERATED: power-records -->

---

## The contrast cases

Closures from the same program that were **not** power closures. They are here
so the note cannot be read as though every negative in this program were a power
negative.

<!-- BEGIN GENERATED: contrast-records -->
### MLCryptoEngine

**What kind of closure.** Eleven hypotheses, nine tested and closed, and not one closed on power. The register's own two-way split is cost-bound versus signal-absent: H1 and H3 cost-bound, H2 and H4 signal-absent, H5 decayed, H8 signal present and cancelled by its own hedge, H9 insignificant after deflation, H10 unidentifiable in available data, H11 failing all six registered bars, H7 closed by decision, H6 negative under an order-lifecycle fill model.

*Source: MLCryptoEngine/HYPOTHESES.md @ d2a0f05 (2026-08-12).*

**Deciding number.** A short-horizon model scored AUC 0.9432 at 100 ms and captured 0.0291 bps per trade on Kraken BTC/USD, which charges 50 bps round trip — a miss of roughly 1,700x. Against the cheapest venue reachable from the operator's jurisdiction at all, Hyperliquid at 3 bps, it still misses by roughly 100x. Separately, H4 cointegration break-even transaction costs ran 300 to 550 bps against that same 3 bps actual, a margin of 100 to 180x.

*Source: MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md @ ae03bf6 (2026-08-22).*

**Why it is not a power closure.** The samples were large and the discrimination was real. AUC 0.94 is not an underpowered measurement; it is a well-measured quantity that turns out not to be the quantity that pays. These closures reopen on a fee schedule or not at all, and the register says so in the field it calls 'what would reopen it'.

### solattn

**What kind of closure.** A powered null. Kill criterion K1 fired at 100.0 percent outcome coverage on every analysed cohort, and all 120 computable cells carry a negative point lift with none positive at any significance level.

*Source: solattn/FINDINGS.md @ b3f5062 (2026-08-28).*

**Deciding number.** Primary trial lift −1.0779 net of the central 450 bps cost band, 95 percent day-clustered bootstrap interval [−3.3354, +0.0204], n = 12,798 amm pools over three birth days, 2,107 measurable at the d0+2 anchor, Q5 cell n = 412.

*Source: solattn/FINDINGS.md @ b3f5062 (2026-08-28).*

**Why it is not a power closure.** The design measured what it set out to measure, at full outcome coverage, and the answer was no. This is what a closure looks like when detectability is not the binding term, and it is the reason the four power cases cannot be read as though every negative in this program were a power negative.

### solclear

**What kind of closure.** Mixed, and the earliest power-shaped refusal in the program. The Stage E outcome study fired a registered underpowered rule — 18 cleared against a floor of 20 at 30 days, and 4 at 90 days — so no significance was claimed in either direction. Its other closures are selection and cost: the confirming measurement is priced out at 4,695,489 weighted credits, 37.6x the stale 124,764 estimate.

*Source: solclear/FINDINGS.md @ c692032 (2026-08-22).*

**Deciding number.** Every one of the 18 cleared pools realized −100 percent net at 30 days, and all 4 with a realized 90-day horizon did the same; share ever above entry 0 percent of 18. Separately, the transferable result: archived-page sampling manufactures survivorship by 60 points at 30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools against 18.75 percent on 16 attention-crawled ones.

*Source: solclear/FINDINGS.md @ c692032 (2026-08-22).*

**Why it is not a power closure.** solclear matters here for the date rather than the type. Its underpowered rule was registered before the measurement and fired on 2026-08-14, eleven days before NPDExperiment. So the ingredient existed already; what it did was refuse an inference after the measurement had been made, not refuse the measurement.
<!-- END GENERATED: contrast-records -->

---

## The source registry

Every citable location referenced above.

<!-- BEGIN GENERATED: source-registry -->
| key | repository | file | commit | date | what it carries |
|---|---|---|---|---|---|
| `aitrader-return` | AiTrader | `RETURN.md` | `f819b68` | 2026-07-29 | the cross-sectional round headline and the H-F width tables |
| `aitrader-round` | AiTrader | `(round commit)` | `a0a9ef6` | 2026-07-26 | "Cross-sectional hypothesis round against the breadth universe, scored as a 5-position book at Level 1 sizing, holdout touched once, findings only, nothing applied" |
| `etf-close` | ETFExperiment | `(closing commit)` | `3f5d629` | 2026-08-28 | "Close H1 at untestable-at-achievable-power on the deadline finding, artifacts preserved" |
| `etf-disarm` | ETFExperiment | `(closing commit)` | `4d11002` | 2026-08-28 | "Disarm etf-snap; correct the reopen-path mislabel in Amendment 5 and ADR-019" |
| `etf-readme` | ETFExperiment | `README.md` | `fe60a22` | 2026-08-28 | the measured-so-far table, each figure with its n |
| `etf-registration` | ETFExperiment | `REGISTRATION.md` | `4d11002` | 2026-08-28 | Section 0 outcome map, Section 9 power method, Amendments 3 to 6 |
| `hf-close` | HFExperiment | `(closing commit)` | `f13e1d3` | 2026-08-25 | "docs: terminal closure, shadow timer disarmed, closure recorded in amendment log and progress" |
| `hf-progress` | HFExperiment | `progress.md` | `82e77a0` | 2026-08-28 | the 2026-08-26 closure entry and the Stage A.1b broker verdict |
| `hf-readme` | HFExperiment | `README.md` | `0a0d214` | 2026-08-23 | the one-line statement of what H-F is and how it resolved |
| `hf-registration` | HFExperiment | `REGISTRATION.md` | `f13e1d3` | 2026-08-25 | Section 4 widths, Section 11 verdict schedule, and the amendment log closure entry |
| `insider-close` | InsiderExperiment | `(closing commit)` | `12d9fd3` | 2026-08-25 | "Close at BLOCKED on the power gate, weight concentration not corpus, artifacts preserved" |
| `insider-decisions` | InsiderExperiment | `DECISIONS.md` | `12d9fd3` | 2026-08-25 | ADR-001 answering power before alpha; ADR-010 closure; ADR-011 reopening boundary |
| `insider-gate` | InsiderExperiment | `(commit)` | `cb17046` | 2026-08-25 | "feat: the power gate, computed without reading alpha. BLOCKED at 49.35 bp" |
| `insider-registration` | InsiderExperiment | `REGISTRATION.md` | `12d9fd3` | 2026-08-25 | Section 0 gates, Section 15.5-15.7 the fired gate, Section 17 closure |
| `insider-section0` | InsiderExperiment | `(commit)` | `fbfc74e` | 2026-08-25 | "feat: scaffold, standing guards, and REGISTRATION Section 0 power gate" — the gate committed before the measurement it judges |
| `mlc-h1note` | MLCryptoEngine | `docs/notes/h1-predictability-without-capturability.md` | `ae03bf6` | 2026-08-22 | the AUC-versus-capture note and the fee-floor arithmetic |
| `mlc-hypotheses` | MLCryptoEngine | `HYPOTHESES.md` | `d2a0f05` | 2026-08-12 | the eleven-entry hypothesis register with each closure type and deciding number |
| `npd-close` | NPDExperiment | `(closing commit)` | `2d3d0ae` | 2026-08-25 | "Close the experiment at unresolved-at-achievable-power, two attempts and zero positives, artifacts preserved" |
| `npd-decisions` | NPDExperiment | `DECISIONS.md` | `2d3d0ae` | 2026-08-25 | ADR-007 registering the contrast power honestly; ADR-011 reading realized power first |
| `npd-progress` | NPDExperiment | `progress.md` | `2d3d0ae` | 2026-08-25 | Stage Z.1 closure, B.2 evaluation, B.1 collection, A.2 registration |
| `npd-registration` | NPDExperiment | `REGISTRATION.md` | `2d3d0ae` | 2026-08-25 | Section 9 power derivation, Section 17 amendments, and the Closure section |
| `solattn-findings` | solattn | `FINDINGS.md` | `b3f5062` | 2026-08-28 | the Stage B documented negative, with every figure carrying its n |
| `solattn-registration` | solattn | `REGISTRATION.md` | `b3f5062` | 2026-08-28 | Amendment 7, which records the Stage B readout and the horizon never analysed |
| `solclear-findings` | solclear | `FINDINGS.md` | `c692032` | 2026-08-22 | the Stage E outcome study, the crawler-survivorship result, and the priced-out confirmation |
<!-- END GENERATED: source-registry -->

---

## Checking a figure yourself

The sibling repositories live beside this one. To check any row:

    git -C ../<repository> show <commit>:<file> | less

For a closing-commit citation, where the claim is in the commit message rather
than in a file:

    git -C ../<repository> log -1 --format='%H%n%ad%n%n%B' --date=iso <commit>

Two citations point at commit messages rather than file contents, because that
is where the claim is recorded: `npd-close`, `insider-close`, `etf-close`,
`etf-disarm`, `hf-close`, `insider-gate`, `insider-section0` and
`aitrader-round`. The commit subject is quoted in the registry's final column in
each case.

## Which of these repositories a stranger can actually reach

Stated plainly, because this file's whole promise is that its figures are
checkable and for four of the seven that promise is currently **conditional**.

| repository | published | how to check a citation |
|---|---|---|
| MLCryptoEngine | yes — `github.com/kirosli00tuff/MLCryptoEngine` | clone and `git show` |
| solattn | yes — `github.com/kirosli00tuff/solattn` | clone and `git show` |
| solclear | yes — `github.com/kirosli00tuff/solclear` | clone and `git show` |
| AiTrader | yes — `github.com/kirosli00tuff/AiTrader` | clone and `git show` |
| **NPDExperiment** | **no — local only, no remote** | requires the operator's working copy |
| **InsiderExperiment** | **no — local only, no remote** | requires the operator's working copy |
| **ETFExperiment** | **no — local only, no remote** | requires the operator's working copy |
| **HFExperiment** | **no — local only, no remote** | requires the operator's working copy |

The four unreachable ones are the four power cases. That is the awkward
direction for this note: the contrast cases, which bound the claim, are
independently checkable, and the cases the claim rests on are not.

Two things follow, and neither is a repair.

**The commit hashes are still doing work.** They pin *which* state of each
repository was read, so if any of the four is published later, every citation in
this file resolves against it without amendment. A hash recorded now against a
closed repository is a real commitment, not a placeholder.

**Until then, the four power cases rest on this note's transcription.** A reader
who does not have the operator's machine is trusting a secondary source, and
should discount the four accordingly. The mechanisms in ADR-002 protect against
drift *within* this repository; they cannot attest to a repository the reader
cannot open. Saying so is cheaper than being caught assuming otherwise.

---

## One derived figure, flagged as derived

**NPDExperiment's 411 minutes of recorded stage time** is not a figure the
repository states. It is the sum of the per-stage actuals that `progress.md`
records for stages A.1 (22), A.2 (34), B.0 (68), B.0b (52), B.1 (194) and B.2
(41). Every addend is quoted; the total is this note's arithmetic. It excludes
the Z.1 closure stage, which the repository does not time.

Every other number in this repository is quoted, not computed.
