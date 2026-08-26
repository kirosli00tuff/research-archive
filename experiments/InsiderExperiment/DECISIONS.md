# DECISIONS

Numbered architecture decision records. Each one states what was decided, what
it costs, and what would overturn it.

---

## ADR-001. The power question is answered before the alpha question

**Status.** Accepted, Stage A.1, 2026-08-25.

**Context.** NPDExperiment closed at unresolved-at-achievable-power. Its
realized minimum detectable contrast came in at 0.0512 against a realistic
effect band of 0.01 to 0.05, so the design could not have detected an effect
anywhere in the range the literature reports. That was discovered after 415 days
of collection and 6.9378 USD of spend, in the same session that read the result.
Its ADR-007 had registered the risk in advance and the arithmetic still landed
too late to change anything.

**Decision.** Compute the minimum detectable effect first, fire a registered
verdict on it, and let that verdict decide whether Stage B is ever written. No
abnormal return is computed in Stage A.1.

**What makes it possible.** Alpha is a first moment. Detectability is a second
moment. The minimum detectable effect is `t * M * sd / sqrt(N_eff)`, and none of
`sd`, `M` or `N_eff` requires knowing the mean. So the variance side can be
computed and fired on while the mean stays sealed.

**Cost.** The Stage A.1 number is measured against the universe benchmark rather
than the Carhart residual, because a factor regression on uncentered data
produces an intercept and the intercept is the alpha. That makes the Stage A.1
figure an upper bound. See ADR-003.

**What would overturn it.** Nothing available. A design that needs the mean to
estimate its own power would have to abandon the separation, and no such design
is required here.

---

## ADR-002. The corpus is built from the SEC structured Form 345 data sets

**Status.** Accepted, Stage A.1, 2026-08-25.

**Context.** The stage brief names three access routes: the full-index archives,
the submissions JSON API at data.sec.gov, and the structured Form 4 XML inside
each filing. The third route needs one request per filing.

**The arithmetic that forced the decision.** The corpus needs Form 4 coverage
from 2013q1 to 2026q1 so the Cohen-Malloy-Pomorski rule has its three-year
look-back on day one of the event span. The full-index archives report 2.04 to
2.14 index rows per Form 4 document across those 53 quarters, and the data sets
carry on the order of two million Form 4 documents over the span. At the
registered 8 requests per second, one request per filing is above 69 hours of
wall clock, before any per-filing directory listing.

**Decision.** The SEC's own quarterly structured Form 345 data sets carry the
corpus. They are the SEC's parse of the same XML documents, published free, in
53 files totalling about 750 MB. All three named routes are still exercised:

- **Structured data sets.** The corpus.
- **Full-index archives.** An independent per-quarter Form 4 count. The ratio of
  index rows to data set documents is 2.04 to 2.14 and stable across all 53
  quarters, so no quarter is short.
- **Per-filing XML.** Field-by-field validation on a 25-document sample spread
  across the whole corpus by entry session. 25 agree, 0 disagree.
- **Submissions JSON API.** Issuer CIK to ticker confirmation on 25 issuers.

**Cost.** The corpus depends on the SEC's parse rather than on this
repository's. The sample validation is what bounds that risk, and it is a
sample, not a census.

**What would overturn it.** A disagreement in the XML sample, or a full-index
ratio that moved across quarters, either of which would say the data sets are
not a faithful rendering of the filing stream.

---

## ADR-003. Form 4 only. 13F and congressional disclosure are rejected

**Status.** Accepted, Stage A.1, 2026-08-25.

**Decision.** Form 4 is the only regime.

**13F is rejected on two grounds.** It carries a 45-day reporting lag, so a
position read from a filing is between 45 and 135 days stale before a public
filer can act. And the published cloning results select managers ex-post: a
study that identifies skilled managers over a sample and then reports the
returns of following them has chosen the followed set using the outcome. That is
the survivorship trap solclear was built to avoid, and importing it would make
any positive result uninterpretable.

**Congressional disclosure is rejected on two grounds.** The same 45-day lag
under the STOCK Act, and the fact that several free ETFs and public feeds now
track and publicize the filings within hours, so any residual is competed away
before a filer reading the same public document can reach it.

**Cost.** Form 4's advantage is a two-business-day lag, and the realized lag
distribution confirms it: 51.3 percent of qualifying events file within one
calendar day and 95.9 percent within four. But Ozlen and Batumoglu report 70 to
80 percent of total alpha dissipating between the transaction date and the
following trading day, which is inside even that lag.

---

## ADR-004. The universe is narrowed to the liquid band, and that excludes where the effect lives

**Status.** Accepted, Stage A.1, 2026-08-25.

**Decision.** `U-LIQ-500-stk-w60-m40-p5`, ported by copy from
`AiTrader/backtest/universe.py` and verified against the source's own stored
membership at three formation dates spanning the corpus, 500 of 500 members
reproduced exactly at each.

**What it excludes, stated rather than discovered.** The literature reports the
insider effect concentrating in small and microcap names. Cohen, Malloy and
Pomorski find the opportunistic effect strongest in small firms. Ozlen and
Batumoglu study the Russell 2000 precisely because that is where the residual
lives. This universe holds neither.

**The corpus measured the cost of the narrowing.** 148,883 officer and director
P-code purchases were rejected as `outside_universe`, against 9,160 that reached
the universe filter and passed it. **Only 5.8 percent of qualifying-shaped
insider purchases happen at a liquid-500 name.** The narrowing removes
sixteen of every seventeen candidate events, and it removes exactly the ones the
literature says carry the signal.

**Why it stands anyway.** The operator cannot trade the illiquid tail at his
measured cost band. A 15.8 to 50.0 bp spread is a large-cap spread. Applying it
to microcaps would understate cost by a multiple and produce a fiction rather
than a conservative estimate.

**The consequence, on the record.** A negative from this repository does not
refute the literature. It establishes that the effect, if it exists, is not
reachable in the liquid band at the operator's costs. Every verdict carries that
scope on its face.

---

## ADR-005. Calendar-time portfolio, not event-time BHAR

**Status.** Accepted, Stage A.1, 2026-08-25.

**Decision.** One portfolio return per session, holding every name currently
inside its post-filing window.

**Why.** The calendar-time approach collapses overlapping event windows into one
return per day, which absorbs day-clustering structurally. Insider purchases
cluster hard in time: the corpus shows 717 qualifying events in 2020 against 297
in 2021, and cluster buys are by construction several filers at one issuer inside
five days. An event-time approach counts the shared market shock once per event.

**Against the alternative.** Event-time BHAR suffers the overlapping-horizon
variance inflation that cut NPDExperiment's 427 evaluable days to 125.6
effective, a loss of 70 percent of the sample to a structure the design chose. A
126-session hold overlaps far more heavily than NPDExperiment's five-session
horizon, so the same choice here would be worse, not comparable.

**Measured outcome.** The realized variance inflation on the primary series is
0.899, which is below one. The daily excess-return series is mildly mean
reverting, so the effective period count of 2,869.9 exceeds the 2,581 sessions
rather than falling below it. The structure did what it was chosen to do.

---

## ADR-006. The realized alpha is sealed, and the power path cannot reach it

**Status.** Accepted, Stage A.1, 2026-08-25.

**Decision.** Two stores, written by one module and read by two different ones.

- `var/insider_sealed.db` holds the raw daily portfolio excess returns. Their
  mean is the realized alpha. `insider.eval.evaluator` is the only permitted
  reader, and it refuses before it opens the file while the operator prior slot
  is empty.
- `var/insider_dispersion.db` holds the same series with its own mean already
  subtracted. The mean is never written there. `insider.power` is its reader.

`insider.portfolio.returns` writes both and reads neither.

**Four guards enforce it.** Only `paths.py`, the writer and the evaluator may
name the sealed store. `read_sealed_returns` is defined once and called nowhere
else. The power package may not import `insider.portfolio`, `insider.market` or
`insider.eval`, so the path from the power computation to a raw return does not
exist rather than being avoided. And `DispersionStats` and `MdeResult` are
asserted against exact registered field tuples, so a first moment cannot be
added beside the dispersion it came from.

**What the seal is and is not.** It is a procedural guarantee that no module on
the power path computes or emits a first moment, and it is enforced by tests
that fail on real mutations of real source. It is not cryptographic. The market
data is local, so anyone who chose to could recompute the series from scratch.
The seal prevents the accident, not the intent, and that is the failure mode
that actually occurred in the predecessor.

---

## ADR-007. Value weighting uses point-in-time median dollar volume

**Status.** Accepted, Stage A.1, 2026-08-25.

**Context.** The registration names value weighting as primary. The permitted
source carries no shares outstanding.

**The route not taken.** SEC XBRL cover facts give
`dei:EntityCommonStockSharesOutstanding` free, about 70 quarterly points per
issuer, and it was verified working. It was rejected for two reasons. The
symbol-to-CIK map, `company_tickers.json`, lists only current registrants, so a
book weighted through it would be survivorship-biased at the weight level across
a ten-year span. The validation sample measured this directly: the SEC's current
ticker list carries the symbol for only 21 of 25 sampled corpus issuers. And
shares outstanding are not split-adjusted while the bars carry adjustment
`all`, so the two would have to be reconciled per corporate action.

**Decision.** Weight by the median dollar volume measured in the 60-session
formation window, which the source already stores per member. It is complete for
every member, point-in-time, carries no survivorship, and is the quantity the
universe is ranked on.

**Direction of the error, stated before the result was read.** Dollar volume is
more dispersed than market capitalization, so the book is less concentrated,
tracking error is higher, and the minimum detectable effect moves toward BLOCKED
rather than away from it. The substitution cannot flatter the design.

---

## ADR-008. The routine pattern is tested before the history gate

**Status.** Accepted, Stage A.1, 2026-08-25. Corrects an implementation defect
found by tightening a guard fixture.

**Context.** The first implementation checked the three-year history requirement
first and the same-calendar-month pattern second.

**The defect.** An insider who traded the candidate's calendar month in each of
the three prior years, but whose earliest observed trade fell eight days short of
three full calendar years, was labelled `insufficient_history`. She is
definitionally routine: trading the same month in three consecutive prior years
*is* three years of trading history.

**Decision.** Test the routine pattern first. The history gate governs only the
residual. Cohen, Malloy and Pomorski define a routine trader by the pattern and
impose the three-year requirement on the opportunistic category, which is what
this ordering now reproduces.

**Impact on the corpus.** One transaction moved from `insufficient_history` to
`routine`. The qualifying set is unchanged at 4,585, because both labels are
excluded unless the buy is rescued by a surviving cluster, and the minimum
detectable effect is unchanged at 49.35 bp per month. The defect was in the
reported composition, not the sample.

**How it was found.** A registered mutation raised `routine_consecutive_years`
from 3 to 4 and the guard did not fire, because the guard's fixture gave the
insider four years of history and survived the raised requirement. Tightening the
fixture to the registered boundary exposed the ordering.

---

## ADR-009. A name that leaves the universe mid-hold is dropped from the book

**Status.** Accepted with a recorded limitation, Stage A.1, 2026-08-25.

**Decision.** A position is held for the registered hold, but on any session
where the name is not a member at the governing formation date it is dropped from
that session's book. This removed 13,750 name-sessions from the primary series,
about 7.4 percent of held name-sessions.

**Why.** The benchmark is the universe, so a name outside it has no weight basis,
and the operator's measured spread only applies inside the liquid band.

**The limitation, recorded rather than fixed.** Membership depends on data dated
after entry. A name that falls below the 5.00 USD price floor after a collapse
leaves the universe and is dropped, so the rule removes some bad outcomes. That
is a survivorship leak in the first moment.

**Why it does not touch this stage's verdict.** Stage A.1 reads only second
moments, and dropping crashed names reduces dispersion, which lowers the
minimum detectable effect and moves the verdict toward GO. The gate fired
BLOCKED, so the leak makes the finding conservative rather than fragile. The leak
would have to be fixed before any Stage B first moment, and Stage B is not
authorized.
