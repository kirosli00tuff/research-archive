# REGISTRATION

InsiderExperiment. A net-of-cost survival test on Form 4 insider purchases.

Registered 2026-08-25, Stage A.1. Every parameter in this document is fixed
before any measurement runs. Section 0 is committed before Task 4 computes
anything, so the answer cannot be read against a threshold its own measurement
could see. Changing a registered value after that commit requires a numbered
amendment in Section 17 carrying its own evidence.

---

## Section 0. The gates

Two gates fire in Stage A.1. Neither reads a first moment. The corpus gate reads
counts. The power gate reads a minimum detectable effect, which is built from a
dispersion and a sample size and from nothing else.

### 0.1 Why this section exists

NPDExperiment closed at unresolved-at-achievable-power. Its realized minimum
detectable contrast came in at 0.0512 against a realistic effect band of 0.01 to
0.05, so the design could not have detected an effect anywhere in the range the
literature reports. That was discovered after 415 days of collection and 6.9378
USD of spend, in the same session that read the result. Its ADR-007 had
registered the risk in advance and the arithmetic still landed too late to
change anything.

The separation that makes an earlier answer possible: alpha is a first moment,
detectability is a second moment. The minimum detectable effect depends on the
portfolio's tracking error and its effective number of independent periods, and
neither requires knowing the mean.

### 0.2 The power gate

Fired on the minimum detectable monthly alpha for the primary calendar-time
portfolio at the registered six-month hold, value-weighted, at t 2.0.

| Verdict | Bar | Consequence |
|---|---|---|
| **GO** | MDE at or below 20 bp per month | The design can resolve the decayed effect band with margin. Stage B is authorized. |
| **DEGRADED** | MDE between 20 and 40 bp per month | The design can resolve the top of the decayed gross band but likely not the net residual after 32 to 100 bp round trip. Stage B is authorized only if the registration records, before B runs, that a gross-detectable net-undetectable outcome is a registered verdict row and not a disappointment. |
| **BLOCKED** | MDE above 40 bp per month | The design cannot detect an effect anywhere in the range the literature reports. Stage B is never written and the repo closes on the finding. |

Boundaries are inclusive at the lower edge. An MDE of exactly 20.00 bp is GO. An
MDE of exactly 40.00 bp is DEGRADED.

The bars are set against the decayed effect band, not the original one. Cohen,
Malloy and Pomorski report 82 bp per month value-weighted on opportunistic
purchases over 1989 to 2007. That replicates at roughly 30 to 40 bp per month on
2008 to 2024 data, a 60 to 70 percent decay. Ozlen and Batumoglu (SSRN 5966834,
December 2025, Russell 2000 Form 4) report 70 to 80 percent of total alpha
dissipating between the transaction date and the following trading day, before a
public filer can act, leaving a residual they describe as largely confirmatory
rather than informative.

The 20 bp GO bar sits below the bottom of the decayed gross band, so a GO design
resolves the whole band. The 40 bp BLOCKED bar sits at the top of it, so a design
above 40 bp cannot resolve any part of the band.

### 0.3 The corpus gate

| Verdict | Bar |
|---|---|
| **CORPUS-GO** | The EDGAR pipeline builds and qualifying events exceed the registered floor. |
| **CORPUS-BLOCKED** | EDGAR access fails, or qualifying events fall below the floor after the ex-ante filters. Record and stop. |

Registered floor, both conditions required:

- **1,000 qualifying events** over the bar span, counted after every ex-ante
  filter in Section 3.
- **80 percent of in-span sessions carrying a non-empty book** at the primary
  six-month hold.

### 0.4 How the qualifying-event floor was derived

The binding constraint is not the raw filing count. It is the number of
independent calendar periods and the portfolio's tracking error. The event count
enters only through book width, and book width enters only through tracking
error.

Write the minimum detectable monthly alpha as

    MDE_month = t * M * s_d / sqrt(N_eff)

with t the critical value 2.0, M the registered 21 sessions per month, s_d the
daily excess-return standard deviation, and N_eff the effective independent
period count after the serial-correlation penalty.

Take the planning figures fixed here: N of 2,520 daily observations over the
ten-year bar span and a variance inflation factor of 1.5, so N_eff is 1,680 and
sqrt(N_eff) is 40.99. Both are planning values. The realized N and the realized
inflation factor are measured in Task 5 and reported beside these.

Invert the expression at each bar:

| Bar | Daily excess-return SD | Annualized tracking error |
|---|---|---|
| 20 bp per month, the GO ceiling | 19.52 bp | 3.10 percent |
| 40 bp per month, the BLOCKED floor | 39.04 bp | 6.20 percent |

So the design stays out of BLOCKED as long as annualized tracking error is at or
below about 6.2 percent, and reaches GO at or below about 3.1 percent.

Now convert tracking error into book width. For a book of k names with average
idiosyncratic volatility sigma and residuals close to independent, tracking
error is about sigma over sqrt(k). Taking sigma at 30 percent annualized, which
is a standard figure for the liquid band this universe covers:

| Bar | Required book width k |
|---|---|
| 6.2 percent tracking error, the BLOCKED floor | 23.4 names |
| 3.1 percent tracking error, the GO ceiling | 93.7 names |

Now convert book width into event count. At a hold of H sessions and a steady
arrival of lambda qualifying events per session, expected book width is H times
lambda when no two events name the same issuer. At H of 126 sessions:

| Book width k | Events per session | Events over 2,520 sessions |
|---|---|---|
| 23.4, the BLOCKED floor | 0.186 | 468 |
| 50, the registered floor | 0.397 | 1,000 |
| 93.7, the GO ceiling | 0.744 | 1,875 |

**The floor is set at 1,000 qualifying events**, which is a book of about 50
names. Three reasons for placing it above the 468 that BLOCKED alone requires.

First, the H times lambda identity assumes distinct issuers. Insider purchases
cluster in the same name, and cluster buys are by construction three or more
filers at one issuer, so realized distinct-issuer width is below the arrival
count. The margin absorbs that.

Second, arrival is not steady. Insider purchases concentrate after price declines
and around earnings windows, so a book that averages 50 names will be thinner
than 24 on some stretches, and those stretches carry the variance.

Third, at 1,000 events the expected tracking error is about 4.24 percent and the
expected MDE about 27 bp per month, which sits inside DEGRADED with room on both
sides. A floor placed at the BLOCKED boundary would admit corpora whose verdict
was decided by rounding.

The coverage floor of 80 percent follows from the same expression. N enters as a
square root, so dropping from 2,520 to 2,016 sessions raises the MDE by 11.8
percent, which is tolerable. Below that the penalty compounds, and more to the
point a book that is empty on more than one day in five is not a calendar-time
portfolio.

### 0.5 What fires these gates

`insider.section0.fire_power_gate` and `insider.section0.fire_corpus_gate`. The
bars live in `insider.config.CONFIG` as `mde_go_ceiling_bp`,
`mde_degraded_ceiling_bp`, `corpus_event_floor` and `corpus_coverage_floor`, and
`tests/test_guards.py` fails if any of them has no enforcement site.

Neither function can read a realized return. `insider.power` takes its input from
`var/insider_dispersion.db`, which holds daily portfolio excess returns already
centered on their own mean. The mean is never written there, so it cannot be
recovered. The raw series lives in `var/insider_sealed.db` and
`insider.eval.evaluator` is its only permitted reader.

---

## Section 1. Hypothesis

Opportunistic and cluster insider purchases, disclosed on Form 4, predict
positive abnormal returns that survive the operator's measured cost band at
achievable size.

This is a net-of-cost survival test, not an alpha hunt. The primary contrast
asks whether a residual remains after a 32 to 100 bp round trip, not whether a
gross effect exists. A gross effect that does not survive the round trip is a
negative for this experiment and a registered verdict row, not a partial win.

Registered against the hypothesis: the published work reports **gross**
value-weighted returns and pre-commits **no net bar**. Cohen, Malloy and
Pomorski report 82 bp per month on opportunistic purchases over 1989 to 2007
before any trading cost. No study in the chain this experiment replicates states
a net threshold, so the net bar here is the operator's own and is not inherited
from the literature.

Prior evidence points at BLOCKED before any measurement runs. The 82 bp figure
replicates at roughly 30 to 40 bp per month on 2008 to 2024 data, a 60 to 70
percent decay. Ozlen and Batumoglu (SSRN 5966834, December 2025, Russell 2000
Form 4) report 70 to 80 percent of total alpha dissipating between the
transaction date and the following trading day, before a public filer can act,
leaving a residual they describe as largely confirmatory rather than
informative. Against the operator's measured 15.8 to 50.0 bp spread band, 32 to
100 bp round trip, the tradable residual is marginal at best.

A negative is the expected outcome and a fully acceptable one.

---

## Section 2. Regime

**Form 4 only.**

**13F is rejected.** It carries a 45-day reporting lag, so a position read from a
13F filing is between 45 and 135 days stale by the time a public filer can act
on it. Worse, the published cloning results select managers ex-post: a study that
identifies skilled managers over a sample and then reports the returns of
following them has chosen the followed set using the outcome. That is the
survivorship trap solclear was built to avoid, and importing it here would make
any positive result uninterpretable.

**Congressional disclosure is rejected.** It carries the same 45-day lag under
the STOCK Act. It is now tracked and publicized by several free ETFs and public
feeds within hours of filing, so any residual is competed away before a filer
reading the same public document can reach it.

Form 4 is chosen because the disclosure lag is two business days rather than
forty-five, and because the classification rule in Section 3 is computed purely
from the filing stream rather than from realized performance.

---

## Section 3. The ex-ante classification rule

Frozen here. Nothing in this rule reads a return, a price move after the filing,
or any realized outcome.

**3.1 Purchases only.** Sales carry diversification and liquidity motives and no
study finds signal in them. The rule admits acquisitions and nothing else.

**3.2 Transaction code P only.** Open-market purchase. A grants, M option
exercises and F tax withholding are dropped. None of the three is a
discretionary open-market purchase, and all three land on schedules the insider
does not choose.

**3.3 Officers and directors only.** Ten percent beneficial owners are excluded,
because their large transactions are often strategic-investor closings rather
than views on value.

The exclusion is on the flag, not on the filer's other roles. A filer who is both
an officer and a ten percent owner is excluded, because the hazard the exclusion
targets is the large strategic closing and that hazard does not go away when the
investor also holds a title. This is the strict reading and it is the more
costly one. The count it removes is reported separately in the attrition table
as `tenpercentowner_also_titled`, so a reader can see what the strict reading
cost without a second verdict path existing.

An unreadable relationship string yields no roles and is rejected. An absence of
evidence that a filer is an officer is not evidence that she is one.

**3.4 Routine versus opportunistic, the Cohen-Malloy-Pomorski rule.** An insider
is **routine** if she traded in the same calendar month for at least three
consecutive prior years. Otherwise she is **opportunistic**.

Computed purely look-back. Only trades strictly before the candidate transaction
enter, so the label a transaction carries on its own date can never move when
later filings arrive.

The look-back trade set is transaction codes P and S. Grants are excluded from
the look-back on purpose: they land in the same calendar month every year by
design, so including them would classify almost every insider as routine and
empty the opportunistic category the hypothesis rests on.

**Three years of trading history is required to classify at all.** An insider
whose first observed trade falls less than three years before the candidate
transaction is `insufficient_history`. That is a third state. It is not routine
and it is not opportunistic, and it is recorded as its own sub-reason inside
`filtered_routine` so the two are never merged in the data. The look-back window
opens 2013-01-01 and the event span opens 2016-04-01, so the requirement is
satisfiable on day one of the event span, but insiders whose first observed trade
falls inside the look-back window are unclassifiable until three years after it.
That truncates the usable window at the front and the count is reported in Task 4.

**3.5 Cluster buys.** Three or more distinct filer CIKs making P-code purchases
at the same issuer within a rolling five-day window, counted in calendar days as
the closed interval from the anchor date to the anchor date plus four.

**3.6 The Johnsen programmatic-event filter.** A cluster is rejected when a
single date-and-price pair accounts for eighty percent or more of the
contributing buys. Insiders who all bought at one price on one day were filled
by one mechanism, not by three independent judgements, and a cluster is only
interesting if the judgements are independent.

Individual transactions below 10,000 USD are dropped, at the same stage and for
the same reason. A transaction that small is a gesture rather than a position.

**3.7 10b5-1 trades are excluded.** A 10b5-1 trade executes a plan committed to
earlier, so it carries no information about what the insider believes today.

An **unreported** 10b5-1 box is a recorded absence and admits the transaction.
The checkbox became a Form 4 cover-page field in 2023. Treating its absence
before then as an affirmative "not 10b5-1" would read a decade of filings as
carrying a fact they do not carry. The share of the corpus for which the flag is
absent is reported in Task 4.

**3.8 What qualifies.** A transaction is a qualifying event when it clears 3.1
through 3.3, sits at a universe issuer, clears 3.6 and 3.7, and is **either**
placed by an opportunistic insider **or** belongs to a cluster that survives the
Johnsen filter. Both legs of the hypothesis in Section 1 feed one portfolio.

**3.9 No selection on performance.** No insider, filer, or issuer may be
selected by realized performance at any point. The cohort is birth-ordered by
first appearance in the filing stream.

---

## Section 4. Universe

`U-LIQ-500-stk-w60-m40-p5`, as reproduced from
`~/Documents/GitHub/AiTrader/backtest/universe.py`. Top 500 by median dollar
volume over a trailing 60-session window, minimum 40 bars in the window, minimum
5.00 USD median close, funds excluded, unclassified instruments excluded.
Membership is decided from bars dated strictly before the formation date.

An issuer qualifies on a given date if its symbol is a member at the most recent
formation date at or before that date. Point-in-time, no exceptions.

**This is a registered narrowing of scope, not an oversight.** The restriction
confines the test to the liquid band where the operator's measured spread applies.
It deliberately excludes the small and microcap names where the literature
reports the insider effect concentrates: Cohen, Malloy and Pomorski find the
opportunistic effect strongest in small firms, and Ozlen and Batumoglu study the
Russell 2000 precisely because that is where the residual lives.

The narrowing is registered because the operator cannot trade the illiquid tail
at his cost band. A 15.8 to 50.0 bp spread is a large-cap spread. Applying it to
microcaps would understate cost by a multiple, and the resulting number would be
a fiction rather than a conservative estimate. Testing where the effect is
largest and the costs are unmeasured would answer a question the operator cannot
act on.

The consequence is stated plainly: **a negative here does not refute the
literature.** It establishes that the effect, if it exists, is not reachable in
the liquid band at the operator's costs. Any verdict this experiment fires
carries that scope on its face.

---

## Section 5. Method

**Calendar-time portfolio.** One portfolio return per day, holding every name
currently inside its post-filing window. Carhart four-factor alpha on the
resulting daily series, in Stage B.

The calendar-time approach collapses overlapping event windows into one
portfolio return per day, which absorbs day-clustering structurally. When many
insiders buy on the same day, those events share the same market shock, and an
event-time approach counts that shock once per event.

The event-time BHAR approach is rejected for exactly that reason. It suffers the
overlapping-horizon variance inflation that cut NPDExperiment's 427 evaluable
days to 125.6 effective, a loss of 70 percent of the sample to a structure the
design had chosen. A six-month hold overlaps far more heavily than
NPDExperiment's five-session horizon did, so the same choice here would be
worse, not comparable.

**Benchmark.** The value-weighted return of the full universe at the same
weighting basis as the portfolio. Excess return is the portfolio return minus the
benchmark return on the same session. Stage B replaces this with the Carhart
four-factor residual. Stage A.1 uses the universe benchmark because the residual
dispersion after factor adjustment is bounded above by the raw excess-return
dispersion, so the Stage A.1 minimum detectable effect is conservative by
construction and cannot make the design look more powerful than it is.

---

## Section 6. Holding period

**Six months primary**, implemented as 126 trading sessions. Two reasons. It
amortizes the 32 to 100 bp round trip across roughly six months of holding,
which is the entire cost argument. And it is the Section 16(b) short-swing
horizon, so an insider who bought is barred from selling at a profit inside it.

**One month (21 sessions) and three months (63 sessions) as registered
secondaries.** Labelled, reported, and non-verdict-bearing.

The tension is stated plainly and is not resolved by the choice: **a longer hold
cuts cost drag and dilutes signal.** The literature concentrates the effect in
the first one to six months, so the hold that makes the cost bearable is also the
hold that dilutes the thing being measured. Six months is registered before any
number is seen precisely because that trade-off cannot be settled by looking.

**Entry** is the close of the first session strictly after the filing date. A
public filer reads the filing after it posts, so entry at or before the filing
date would be unreachable. The Ozlen and Batumoglu finding is that most of the
alpha is already gone by this point, and this entry rule is what makes the
experiment measure the part a public filer can actually reach.

---

## Section 7. Weighting

**Value-weighted primary. Equal-weighted secondary.**

Wide book, not concentrated. Concentrated books are what killed H-F at 42 to 66
percent tracking error, where the position count was small enough that single
names dominated the variance and no statistical statement survived.

Weighting basis is recorded as a deviation in Section 14.2. The permitted source
carries no shares outstanding, so value weighting is implemented as point-in-time
median dollar volume from the formation window.

---

## Section 8. Cost model

The operator's measured band, applied to both the portfolio and any statement
about it:

| Quantity | Optimistic | Pessimistic |
|---|---|---|
| One-way spread | 15.8 bp | 50.0 bp |
| Round trip | 32 bp | 100 bp |

**The pessimistic 100 bp round trip is the primary bar. The optimistic 32 bp is
a registered secondary.** A result that survives only at 32 bp is reported as
surviving only at the optimistic bar and does not fire the primary verdict.

Amortized across the primary 126-session hold, which is 6.0 trading months:

| Bar | Monthly drag |
|---|---|
| 32 bp round trip | 5.33 bp per month |
| 100 bp round trip | 16.67 bp per month |

Against the decayed gross band of 30 to 40 bp per month, the net band at the
six-month hold is **13.3 to 34.7 bp per month**. `insider.cost` computes this
rather than asserting it.

**P26 is the standing reference point.** 19,648 trades at minus 1.97 bp per
trade, exactly the fee, gross edge precisely zero. A cost model that is not
applied to the gross number reproduces that outcome one layer up, where the
gross edge is reported and the fee is left as an exercise.

---

## Section 9. The verdict table

Written now, before any measurement. Every row is a registered outcome.

| Row | Condition | Verdict |
|---|---|---|
| **V1** | Net alpha positive and significant at t 2.0 against the 100 bp round trip | The hypothesis survives at the primary bar. Stage C may be considered. |
| **V2** | Gross alpha significant, net indistinguishable from zero at the 100 bp round trip | **A registered verdict, not a disappointment.** The effect exists gross and does not survive the operator's cost band. This is the outcome the prior evidence points at. |
| **V3** | Gross alpha not significant | No effect detected in the liquid band at this design. Reported with the realized MDE beside it, so the reader can tell a null from an underpowered null. |
| **V4** | Net alpha positive and significant only at the 32 bp optimistic round trip | Survives at the optimistic bar only. Non-verdict-bearing at the primary bar. |
| **V5** | Section 0 fires GO | Stage B is authorized. |
| **V6** | Section 0 fires DEGRADED | Stage B is authorized only after this registration records that V2 is a verdict row and not a disappointment. That sentence is already in row V2, written before the gate fired. |
| **V7** | Section 0 fires BLOCKED | Stage B is never written. The repo closes on the finding. No alpha is ever read. |
| **V8** | Section 0 fires CORPUS-BLOCKED | Record and stop. The power gate does not fire, because a corpus below the floor has no portfolio to measure. |

V3 and V7 are different findings and are never reported as the same one. V3 says
the design looked and found nothing. V7 says the design could not have found
anything, and says it before looking.

---

## Section 10. Inference

**Day-clustered standard errors on the calendar-time series.** The unit of
observation is the trading day, and the portfolio return on a day already
aggregates every name in the book, so clustering is on the day and nothing else.
Serial correlation across days is handled by a Newey-West Bartlett kernel at a
registered lag of 21 sessions, one trading month, with the grid 5, 21, 63 and 126
reported beside it.

The registered lag is longer than the standard automatic bandwidth, which at N
of 2,520 would select 8. Membership persists for the full 126-session hold, so
the automatic rule is too short here and would understate the variance. The lag
is registered before measurement and the grid is reported so a reader can see the
sensitivity rather than take the choice on trust.

**A single pre-registered primary contrast.** Net alpha of the value-weighted
six-month calendar-time portfolio against zero, at the 100 bp round trip. One
contrast, so no family correction applies. A correction exists to control the
error rate across a family of tests, and there is no family here: the secondaries
are labelled non-verdict-bearing before any of them is computed, so they cannot
be promoted to the primary after the fact.

**Secondaries, all non-verdict-bearing.** The 21-session and 63-session holds.
The equal-weighted book. The 32 bp optimistic cost bar. The Newey-West lag grid.
Each is reported. None fires a verdict.

**Critical value 2.0.** Registered, two-sided, applied identically to the power
computation in Stage A.1 and to the inference in Stage B.

---

## Section 11. What Stage A.1 does not do

It reads no alpha, computes no abnormal return, fires no hypothesis verdict,
places no order, and spends no money. It answers whether the question is
answerable, and it answers that before anyone can see what the answer would have
been.

`insider.power` returns dispersion statistics, counts, and the derived minimum
detectable effect, and nothing else. `tests/test_guards.py` fails if any
dataclass in that package grows a first-moment field, and fails if any module
outside `insider.eval.evaluator` names the sealed store.

---

## Section 12. The operator prior, reserved

The calibration ledger needs an independently formed number to be worth
anything. NPDExperiment's prior was adopted rather than formed, which made its
calibration row a record of agreement rather than a test of judgement.

> Operator prior, probability that net alpha survives at the operator's measured
> cost band and inside this universe:
>
> [ EMPTY. The operator writes a number here himself, before Stage B runs. ]

**This slot blocks Stage B while it is empty.**
`insider.registration_check.require_operator_prior` raises `OperatorPriorMissing`
rather than warning. Absence of the empty marker is not presence of a prior: a
number must be present and parseable or the slot reads as empty.

**The assistant's prior, recorded beside it and never inside it: 0.12.**

Formed from four things. The 60 to 70 percent decay of the Cohen-Malloy-Pomorski
effect on modern data. The Ozlen and Batumoglu finding that 70 to 80 percent of
what remains dissipates before a public filer can act. The Section 4 narrowing to
the liquid band, which excludes where the literature says the effect
concentrates. And the 16.67 bp per month pessimistic cost drag against a decayed
gross band whose bottom is 30 bp per month.

---

## Section 13. Recorded call states

Eight states. Never merged. Operational health and sample composition never
share a representation.

| State | Class | Meaning |
|---|---|---|
| `parsed` | qualifying | Cleared every ex-ante filter and enters the portfolio |
| `unparseable` | operational health | A required field was missing or unreadable |
| `filtered_code` | sample composition | Transaction code is not P |
| `filtered_role` | sample composition | Not an officer or director, or flagged ten percent owner |
| `filtered_routine` | sample composition | Routine insider, or too little history to classify |
| `filtered_programmatic` | sample composition | 10b5-1 flagged, below the dollar floor, or in a Johnsen-rejected cluster |
| `no_bar` | operational health | No daily bar to enter on |
| `outside_universe` | sample composition | Issuer is not a universe member at the governing formation date |

`unparseable` is a pipeline fault. `filtered_routine` is a sample the rule
deliberately excluded. Collapsing the pair destroys the distinction between a
corpus that could not be read and a corpus that was correctly narrowed, which is
exactly the distinction a thin-corpus verdict turns on.

Each state carries a **sub-reason** recorded alongside it. `filtered_routine`
covers both a routine insider and an insider with too little history to classify,
and those are different facts about the sample, so the sub-reason column keeps
them apart in the data even though the registered state list has eight entries.

---

## Section 14. Deviations recorded at registration

Recorded before measurement, each with the arithmetic that forced it.

**14.1 The corpus is built from the SEC's structured Form 345 data sets rather
than from every filing's XML.** See ADR-002. The per-filing XML route needs one
request per filing. The universe issuers file on the order of two million Form 4
documents across the 2013 to 2026 span, and at the registered 8 requests per
second that is above 69 hours of wall clock. The structured data sets are the
SEC's own parse of those same XML documents, published free, in 53 quarterly
files. All three access routes named in the stage brief are exercised: the
structured data sets carry the corpus, the full-index archives supply an
independent per-quarter filing count, and the per-filing XML route validates the
data sets field by field on a sample.

**14.2 Value weighting uses point-in-time median dollar volume, not market
capitalization.** The permitted source carries no shares outstanding. The free
SEC route for shares outstanding is `company_tickers.json` joined to XBRL cover
facts, and that route lists only current registrants, so a portfolio weighted
through it would be survivorship-biased at the weight level across a ten-year
span. Median dollar volume is complete for every member, is measured
point-in-time in the 60-session formation window, and is the same quantity the
universe is ranked on. It is more dispersed than market capitalization, so the
book is slightly less concentrated and the tracking error slightly higher, which
moves the minimum detectable effect toward BLOCKED rather than away from it.

**14.3 Stage A.1 measures dispersion against the universe benchmark, not against
the Carhart residual.** Residual dispersion after factor adjustment is bounded
above by raw excess-return dispersion, so the Stage A.1 minimum detectable effect
is an upper bound on the Stage B one. The gate can therefore fire BLOCKED on a
design Stage B would have found marginally better, and cannot fire GO on a design
Stage B would have found worse.

---

## Section 15. Results

Filled by Task 4 and Task 5. Empty at the time Section 0 was committed.

## Section 16. Amendments

None in force.
