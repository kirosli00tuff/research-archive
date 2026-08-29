# The power limit

*A cross-experiment note. Four pre-registered experiments, closed between
2026-07-26 and 2026-08-28, that ended on detectability rather than on a
measured null.*

---

## The claim

Across four independent pre-registered experiments, the binding constraint was
not whether a published effect exists. It was whether a sample an individual
could actually assemble could detect an effect of the size that was reported.

Each of the four closed at *unresolved at achievable power*, at *untestable at
achievable power*, or *BLOCKED* on a power gate. Not one closed on a measured
null. In two of the four — InsiderExperiment and ETFExperiment — the outcome
variable was never read at all, and a third closed with its own forward series
never started.

## What this is not

The claim above is narrow, and it is easy to inflate into something it does not
support. Four limits, stated before the evidence rather than after it.

**This is not evidence that those anomalies are absent, and four cases are four
cases rather than a survey; the note claims a detectability result about
retail-scale replication and nothing more.**

That sentence carries the whole scope. Unpacked:

1. **Nothing here refutes the literature it tested against.** A design that
   cannot resolve an effect returns no information about whether the effect is
   there. InsiderExperiment's realized alpha sits sealed and unread on disk.
   ETFExperiment never read an outcome value at any point in its life. The
   correct reading of all four is *we could not tell*, which is a fact about the
   instruments, not about the markets.

2. **Four cases are four cases.** They were not sampled from a population of
   hypotheses; they are the hypotheses one operator happened to run in a
   five-week window. Nothing about the base rate of power-bound questions in
   quantitative finance follows from them.

3. **Four of the seven source repositories are not published.** The four power
   cases — NPDExperiment, InsiderExperiment, ETFExperiment and HFExperiment —
   exist only on the operator's machine and have no remote. The three contrast
   cases and AiTrader are public. So the evidence that *bounds* this claim is
   independently checkable and the evidence the claim *rests on* is not, until
   those repositories are published. [SOURCES.md](../SOURCES.md) records which
   is which, and every citation carries the commit hash that will resolve
   against them if they ever are. A reader should discount the four
   accordingly.

4. **"Independent" means independent hypotheses, not independent
   investigators.** One operator, one house scaffold, one set of standing rules,
   and — in two cases — one shared universe definition. The experiments are
   independent in hypothesis, data source, instrument and venue. They are not
   independent in method or in judgement, and a shared methodological blind spot
   would show up in all four at once. A reader who wants that ruled out should
   treat the four as one program's experience rather than four draws.

What *is* established is a fact about achievable samples. In each case a
quantity was computed from dispersion and sample size alone — no first moment
required — and that quantity sat outside the range the design would have needed
to say anything.

## The four cases

<!-- BEGIN GENERATED: headline-table -->
| experiment | effect band tested against | measured detectability | closed at |
|---|---|---|---|
| **NPDExperiment** | daily rank IC 0.01 to 0.05 | realized MDE **0.0512** — above the whole band | unresolved at achievable power |
| **InsiderExperiment** | 30 to 40 bp/month gross; 13.3 to 34.7 net | realized MDE **49.35 bp/month** — above both bands | BLOCKED on the power gate, verdict row V7 |
| **ETFExperiment** | rank correlation 0.09 registered, 0.18 published | needs **N = 300** governing; **163** projected at the deadline | untestable at achievable power |
| **HFExperiment** | 27.99 bp/day against ~418 bp/day of noise | **z 1.668** against a 2.50 bar; needed 104.0 %/yr of excess, delivered 70.5 | resolved on statistical power, not absent signal |
<!-- END GENERATED: headline-table -->

The full extraction — every figure with the repository, file and commit it came
from — is in [SOURCES.md](../SOURCES.md). In short:

**NPDExperiment** asked whether a frontier LLM, fed anonymized numeric feature
blocks, ranks next-window cross-sectional returns better than cheap mechanical
baselines. It collected 415 daily rankings, spent 6.9378 USD, opened its sealed
store once, and found that the realized minimum detectable contrast was 0.0512
against a realistic effect band of 0.01 to 0.05. The design could not have
detected an effect anywhere in the range the literature reports. The verdict
row fired as registered; the honest reading beside it is an underpowered
unresolved, not a tight null.

**InsiderExperiment** asked whether opportunistic and cluster Form 4 insider
purchases predict returns that survive a retail cost band. It computed a
minimum detectable effect of 49.35 bp per month against a registered BLOCKED
floor of 40, a decayed gross band of 30 to 40, and a net band of 13.3 to 34.7.
The corpus was not the problem — 4,585 qualifying events against a floor of
1,000, at 99.5 percent session coverage. Weight concentration was: a book of
71.9 names that behaves like 29.7, whose 9.993 percent tracking error is the
whole of the 49.35.

**ETFExperiment** asked whether US spot Bitcoin ETF net flow prints predict the
next day's BTC return by enough to clear a Hyperliquid round trip. It never
reached the return question. The as-printed flow history needed to test the
design does not exist in any free archive: archive capture density measured
11 of 333 days, 3.30 percent, against a registered 60 percent bar. Forward
accrual at 20.8 admissible days per month projects 163 days by the registered
deadline against a governing minimum of 300.

**HFExperiment** carried 12-1 cross-sectional momentum forward from an AiTrader
round that had already resolved it on power: holdout excess of 27.99 bp per day,
z 1.668 against a corrected bar of 2.50, where clearing the bar over a 2.55-year
holdout needed 104.0 percent per year of excess against the 70.5 delivered. The
raw outperformance was the largest that project ever measured — 90.3 percent
per year against a benchmark's 19.7 — and it still could not clear a
significance bar, because a five-position limit gave the book 66.4 percent
annualized tracking error. Its own registration priced the forward version at
2,061 trading days to clear zero and 2,852 to clear the cost hurdle. Eight to
eleven years.

### Four figures corrected

This note was commissioned with a set of figures already attached. Four needed
correcting against the record, and the corrections are here rather than in a
footnote.

1. **NPDExperiment's "415 days" is 415 days of *data*, not 415 days of
   elapsed collection.** The phrase travels verbatim from InsiderExperiment's
   own Section 0.1, so it is faithfully quoted — but a reader outside this
   program will read it as fourteen months of waiting. It was not. Scaffold,
   registration, collection, evaluation and closure all ran on 2026-08-25, with
   the collection stage itself taking 194 minutes. The 415 is the sample: 415
   stored daily rankings covering a 432-day historical window.

2. **ETFExperiment's 845 / above-1,200 / about-302 triple is real but belongs to
   a different question than the closure.** Those are Amendment 6's numbers for
   what fourteen further months of forward collection would buy: roughly 302
   admissible days by 2027-10-31, which clears the governing 300 at the
   *published* 0.18 magnitude by two days and clears nothing at the *registered*
   0.09 assumption, where E1 needs 845 and E2 needs above 1,200. The closure
   itself fired on a different comparison — 163 projected against 300 governing
   at the 2027-03-31 deadline.

3. **HFExperiment did not fire a power gate.** It is a power case by
   inheritance. Its own Section 0 fired BLOCKED on the *broker* — IBKR refused
   fractional quantities through the API, errors 10243 and 10244 — and the
   repository then closed by operator decision on 2026-08-26 with the shadow
   series never started. The power resolution belongs to the AiTrader round of
   2026-07-26, which HFExperiment's README states in its first sentence.

4. **MLCryptoEngine's 0.03 bps was measured against 50 bps, not 3.** The precise
   pair is AUC 0.9432 with 0.0291 bps of capture at 100 ms on Kraken BTC/USD,
   which charges 50 bps round trip — a miss of roughly 1,700x. The 3 bps is the
   cheapest venue reachable from the operator's jurisdiction at all, and against
   *that* floor the same edge still misses by roughly 100x. Both framings hold;
   only the second was quoted.

## The progression

The transferable output of this program is not any individual closure. It is
the distance between two of them, and the second began five hours after the
first closed.

**NPDExperiment discovered the problem at the end.** Its ADR-007 had registered
the exact failure mode as a risk before collection began: the primary contrast
sat at a five-session horizon, consecutive days shared four fifths of their
forward window, variance inflated by 3.4, and the effective day count fell from
427 to 125.6. The registration said so, in writing, before a cent was spent, and
chose not to repair it by promoting the better-powered secondary — because
promoting a secondary after seeing a result is the move the repository existed
to prevent.

The arithmetic was right and it still landed too late. The projection ran 0.026
to 0.047 across a grid of assumed correlations from 0.0 to 0.7. The realized
figure came in at 0.0512, outside and above the entire grid, because the model
and the momentum baseline turned out to be strongly *negatively* correlated —
the realized contrast standard deviation of 0.36339 sits at 98 percent of the
theoretical maximum reachable only at correlation minus one. Nothing in the
registration contemplated that cell. The number that disqualified the design
appeared in the same session that read the result, after the sealed store had
been opened, which under this program's rules can happen exactly once.

**InsiderExperiment registered a gate because of it.** Its Section 0.1 is headed
"Why this section exists" and opens by naming NPDExperiment. Its ADR-001 is
titled "The power question is answered before the alpha question". Both quote
the predecessor directly:

> NPDExperiment closed at unresolved-at-achievable-power. Its realized minimum
> detectable contrast came in at 0.0512 against a realistic effect band of 0.01
> to 0.05, so the design could not have detected an effect anywhere in the range
> the literature reports. That was discovered after 415 days of collection and
> 6.9378 USD of spend, in the same session that read the result. Its ADR-007 had
> registered the risk in advance and the arithmetic still landed too late to
> change anything.

And then it states the separation that makes an earlier answer possible:

> Alpha is a first moment. Detectability is a second moment. The minimum
> detectable effect is `t * M * sd / sqrt(N_eff)`, and none of `sd`, `M` or
> `N_eff` requires knowing the mean. So the variance side can be computed and
> fired on while the mean stays sealed.

That separation was then enforced structurally rather than by intention. The
raw daily excess returns went into one store whose mean *is* the answer, with a
single permitted reader. A second store held the same series with its own mean
already subtracted, and the mean was never written there, so it could not be
recovered. The power module was forbidden by import guard from reaching the
portfolio, market or evaluation packages — the path from the power computation
to a first moment does not exist, rather than existing and being avoided.

The gate fired BLOCKED at 49.35 bp per month. Stage B was never written. The
alpha is still sealed.

The clock is the part worth keeping. NPDExperiment's closing commit is stamped
2026-08-25 13:26:58. InsiderExperiment's first commit — the one carrying the
gate — is stamped 18:34:56 the same day, five hours and eight minutes later. Its
own closure came at 23:24:15. The whole distance from paying for the lesson to
spending nothing on the next one is under ten hours, which says the lesson was
cheap to transfer once somebody had paid for it.

**The order matters more than the outcome.** The gate was committed in the
repository's first commit, `fbfc74e`, titled "scaffold, standing guards, and
REGISTRATION Section 0 power gate" — before the corpus existed, before the
portfolio existed, and before there was anything for it to judge. The bars were
fixed at 20 bp for GO and 40 bp for BLOCKED, derived from a decayed literature
band, with the boundary conventions written down ("An MDE of exactly 20.00 bp is
GO"). A gate written after the measurement is not a gate; it is a rationalization
with a threshold attached.

**The refusal was also honest about what it forwent.** The equal-weighted
secondary, on the identical 71.9 names, would have landed at 34.29 bp and fired
DEGRADED. It was registered as non-verdict-bearing before any number was
visible, and it was not promoted. The repository recorded the temptation
explicitly, and recorded that any future test naming equal-weight as primary
would have to disclose that the choice was made after seeing this number.

### The cost asymmetry, in numbers

| | before the gate existed | after the gate existed |
|---|---|---|
| | **NPDExperiment**, closed 2026-08-25 | **InsiderExperiment**, closed 2026-08-25 |
| money | **6.9378 USD** across 920 billed model calls | **0 USD**. No paid API was used |
| network | 920 billed calls plus 2 calibration calls | 214 wire requests, 2.78 GB, zero non-200 responses |
| time | **411 minutes** of recorded stage time across six stages, of which collection alone was 194 | about **51 minutes** for Stage A.1 and 20 for the closure |
| the one-shot resource | **spent** — the sealed window was opened, and the registration permits exactly one read | **intact** — the sealed alpha was never opened |
| what a rerun costs | a fresh collection on a fresh window under a new registration, about 7 USD, because the spent data cannot answer a new question | nothing was spent, so nothing needs replacing |

The dollars are not the story; under seven dollars is not an expensive mistake.
Two other columns are.

The first is the **one-shot resource**. NPDExperiment's design permitted a single
evaluation of its sealed store, and that read is what produced the disqualifying
number. When a post-hoc amendment proposed scoring the same data at two more
horizons, the registration voided it: *scoring spent data against new horizons
is a second look however it is labelled*. The 6.9378 USD is recoverable in an
afternoon. The clean read is not recoverable at all.

The second is **what the number could still have changed**. At NPDExperiment's
B.2 stage, nothing. The collection was complete, the money was spent, the store
was open, and the realized MDE arrived as a description of a result rather than
as a decision about whether to produce one. At InsiderExperiment's Stage A.1 the
same class of number arrived while every downstream decision was still open, and
it closed the repository before the expensive part began.

**And the ingredient was not new — the ordering was.** ADR-007 proves
NPDExperiment already knew how to compute this. solclear had already registered
an *underpowered rule* that fired on 2026-08-14, eleven days earlier, refusing
to claim significance in either direction when its cleared basket came in at 18
against a floor of 20. HFExperiment's Section 11, registered 2026-08-23,
priced its own forward verdict at eight to eleven years and the operator
proceeded anyway, deliberately, because the *execution* question was answerable
even though the signal question was not. In every one of those cases the power
arithmetic was present, correct, and non-binding. What changed on 2026-08-25 was
that the number was promoted from a recorded limitation to a committed verdict
with a bar, fired before the measurement it judges.

## The contrast cases

Not every closure in this program was a power closure, and a note that did not
say so would read as though every negative here were a power negative. Three
counterexamples, two of them larger than the four cases above.

**MLCryptoEngine** ran eleven hypotheses and closed nine on measurement. Not one
closed on power. Its register maintains an explicit two-way split — *cost-bound*
(a real signal smaller than the cost of capturing it, which reopens at a lower
fee tier) versus *signal-absent* (nothing to capture, which does not reopen on a
better model, a better feature set, or lower fees) — and treats confusing the
two as the expensive mistake. The deciding numbers are not close calls. A
short-horizon model scored AUC 0.9432 and captured 0.0291 bps per trade against
Kraken's 50 bps round trip, missing by about 1,700x, and by about 100x even
against the cheapest reachable venue at 3 bps. Cointegration pairs trading
showed break-even transaction costs of 300 to 550 bps against 3 bps actual — a
margin of 100 to 180x, which the register calls the cleanest demonstration in
the project that removing cost does not reveal an edge underneath. These are
well-measured quantities that turn out not to be the quantity that pays. They
are the opposite of underpowered.

**solattn** returned a powered null. Its kill criterion fired at 100.0 percent
outcome coverage on every analysed cohort, and all 120 computable cells carry a
negative point lift with none positive at any significance level. The primary
trial measured a lift of −1.0779 net of a 450 bps cost band with a 95 percent
day-clustered interval of [−3.3354, +0.0204], on 12,798 pools over three birth
days. That is what a closure looks like when detectability is not the binding
term: the design measured what it set out to measure, at full coverage, and the
answer was no.

**solclear** is mixed, and it matters here for its date rather than its type.
Its Stage E outcome study fired a *registered underpowered rule* — 18 cleared
against a floor of 20 at 30 days, 4 at 90 — and claimed no significance in
either direction, on 2026-08-14. Its other closures are selection and cost: the
confirming measurement was re-priced at 4,695,489 weighted credits, 37.6x a
stale estimate of 124,764, and closed as priced out rather than untested. Its
most transferable finding is neither — archived-page sampling manufactures
survivorship by 60 points at 30 days and 79 at 90, with 97.5 percent death on 40
birth-ordered pools against 18.75 percent on 16 attention-crawled ones.

Together these date the shift. Power was one closure mode among many, and became
the *first-asked question* only at the end of August 2026.

## The practice

Stated so someone outside this program could adopt it. It is four rules, and the
third is the one that does the work.

**1. Compute the minimum detectable effect from dispersion and sample size
alone, before any first moment is read.** The identity is
`MDE = t * scale * sd / sqrt(N_eff)`. None of the terms needs the mean. Whatever
form the test takes — a t-statistic on a calendar-time portfolio, a permutation
test on a rank correlation, a simulated minimum N for a sign test — the
detectability side can be computed while the answer stays sealed. If a design
genuinely cannot estimate its own power without its own answer, that is worth
knowing early too.

**2. Fix the effect band from the published record, and derive the bars from
it.** InsiderExperiment placed GO below the bottom of the decayed literature
band and BLOCKED at its top, so a GO design resolves the whole band and a
BLOCKED design resolves none of it. This is the step most easily skipped and it
is what makes the verdict mean anything: an MDE with no band beside it is a
number, not a decision.

**3. Commit the gate before the measurement it judges.** Not the same day —
before. In the first commit, with the boundary conventions written down and an
enforcement site in code that a test fails without. A power bar chosen after
seeing the MDE is not a bar. The structural version is stronger than the
procedural one: put the first moment in a store the power path cannot import, so
the separation is a property of the dependency graph rather than of anyone's
discipline.

**4. Treat BLOCKED as a cheap and legitimate outcome, not a failure.** This is
cultural and it is where the practice usually dies. A power gate that nobody is
willing to let fire is decoration. Three habits make it survivable: register the
BLOCKED branch as a *verdict row* with its own consequence, so firing it is
following the protocol rather than abandoning it; write the closure language
before the measurement, so the finding cannot be softened afterwards; and record
what the refusal forwent — the tempting secondary, the reopening path, the
measurement now permanently unmade — because a refusal that hides its own cost
invites a later session to quietly reverse it.

One corollary, learned the expensive way. **Registering a power risk is not the
same as gating on it.** NPDExperiment's ADR-007 named the exact failure mode
before collection and it changed nothing, because a risk is a note and a gate is
a decision. The difference is whether the number is allowed to stop the work.

## What would change the conclusion

Not a better estimator on the same samples. The four designs were not badly
built; all four ran their pipelines against mutation-tested guards, and the
arithmetic that closed them is the arithmetic that would close a better
model just as fast. Halving a standard error is a factor of four in sample size,
and NPDExperiment's shortfall alone was a factor of four in evaluable days
against a window no model's knowledge cutoff makes available.

What would change it is **a domain whose effects are large relative to
achievable samples**. Three shapes qualify:

- **A larger effect.** The bands here were 0.01 to 0.05 in rank IC, 30 to 40 bp
  per month decayed to 13 net, and 27.99 bp per day against 418 of daily noise.
  A domain where the published effect is a multiple of its own dispersion, not a
  fraction of it, resolves at samples an individual can build.

- **A cheaper independent observation.** Every case here was bound by the count
  of *independent* periods, not raw rows. NPDExperiment lost 70 percent of its
  sample to overlapping five-session horizons. ETFExperiment could not buy
  history at any price, because the as-printed record was never archived — its
  binding constraint was calendar time, and no budget shortens it. A domain
  where independent observations accrue quickly, or can be bought, is a
  different arithmetic problem.

- **A design whose dispersion is lower rather than whose mean is higher.**
  InsiderExperiment is the clearest instance: its verdict turned entirely on
  tracking error, and its own equal-weighted secondary on the identical names
  would have landed at 34.29 bp instead of 49.35. It was not promoted, and
  correctly so. But the general lesson is that the denominator is often the
  cheaper term to attack, and it is almost always the one nobody looks at.

The conclusion would also change on evidence that this program's method is
itself the constraint — that four experiments closed on power because of a
shared blind spot in how one operator designs tests, rather than because of the
domain. That is a live possibility and nothing here rules it out. Four cases run
by one person under one scaffold cannot distinguish "retail-scale replication is
power-bound" from "these four designs were underpowered". The contrast cases are
the only evidence against it: the same operator, the same scaffold, produced a
powered null at 100 percent coverage and nine measured closures that were not
power closures at all. That is weak evidence and it is offered as weak evidence.

---

*Every figure in this note is quoted from a closed repository and carries its
source in [SOURCES.md](../SOURCES.md). Nothing here was measured by this
repository, which holds no data and computes no statistic.*
