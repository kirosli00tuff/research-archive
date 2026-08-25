# Decisions

Numbered ADRs, append-only. Each records the decision, the reason, and
what would change it.

## ADR-001: Two series, two questions

The SHADOW series is the signal instrument. The registered book computed
daily from price data alone, no fills, no commissions. It accumulates the
statistics the verdict reads. It would run identically if nobody traded a
dollar. The LIVE series is the execution instrument. Actual fills at a
real broker at micro size. The difference between the two IS the
execution cost, measured directly rather than modelled.

One week is enough to measure execution. One week is nowhere near enough
to measure signal. The registration must say so in those words.

Changes it: nothing at this stage. This is the design's spine.

## ADR-002: The stage map, and B.1's independence from the broker

Stages A.1 through D.1 as registered in the stage prompt. The property
that matters: B.1 does not wait on the broker. The shadow series needs no
account and no money. If the broker question resolves BLOCKED, phase B
still runs and still answers the signal question. Only phases C and D
die. This property is the reason the two-series design was chosen.

Changes it: nothing. A later stage that couples the shadow series to a
broker dependency violates this ADR.

## ADR-003: Broker verdict under the Section 0 outcome map

Measured in docs/ACCESS.md. IBKR Canada is the only reachable broker
clearing residency, US equities, and an order-placing API at once.
Alpaca excludes Canadian residents. Questrade's API trades for partner
developers only. Wealthsimple has no official API and its terms prohibit
API trading.

BLOCKED is ruled out on documented bars. The GO versus DEGRADED verdict
is UNDECIDED, because the deciding bar, fractional through the API at 45
USD, resolves only by the Task 3 paper test and the operator holds no
IBKR account yet. Every Task 3 sub-test is recorded BLOCKED-ON-OPERATOR
in docs/ACCESS.md. The verdict was not read from documentation because
the documentation contradicts itself, which is the reason the outcome map
demanded a test.

Two facts from the measurement bind stage C regardless of the verdict.
SmartRouting is required to keep Tiered pricing on API orders, in IBKR's
own words. And fractional orders carry their own schedule, the greater of
1 percent of value or one cent, which doubles the projected commission
against the settled 50 bp assumption if it applies to the whole order.
Neither touches the slippage measurement. Commission is deterministic and
subtracts exactly.

Changes it: the Task 3 test resolves GO or DEGRADED. An Alpaca Canadian
launch would reopen the table.

## ADR-004: Width 20, chosen for the measurement, not the book

The live book's information ratio does not matter, because the verdict
reads the shadow series. Width serves the execution measurement, which is
fill-count-limited: per-fill slippage carries a sigma near 10 to 20 bp,
so a mean tight to 1 bp needs a couple of hundred fills. Width buys
calendar speed at roughly flat commission. A.2 registers 20 as the
primary, since it is what trades, with 5 and 50 as pre-registered
secondaries under a multiplicity correction. The traded book stays
identical to the primary measured book, the principle that ruled out a
buffer rule.

Measured input from Task 4: churn at width 20 averaged 5.2 names per
month over the last 6 months, about 10 to 11 fills per month. The A.2
cost model must project fill accumulation from this measured rate rather
than from an assumed one.

Changes it: Amendment 1, if Task 3 forces whole-share sizing.

## ADR-005: Reproduction horizon pinned to the recorded pull end

The database carries daily bars past the recorded round's pull end of
2026-07-24 for exactly 1,535 symbols, a partial refresh. A universe
computed on that partial pool would be garbage. The reproduction uses
analysis_meta.universe_pull_end as its horizon, which reproduces the
recorded 124 formation dates identically.

Changes it: a full-pool refresh with a recorded new pull end.

## ADR-006: Momentum anchor convention, fixed by this repository

The recorded round's formation code is outside the two permitted read
paths, so the 12-1 ranking is implemented from its registered
description. Conventions fixed here: far anchor is the session before the
formation date 12 months back in the formation-date sequence, near anchor
is the session before the formation date 1 month back, each close is the
last bar at or before its anchor, a bar more than 20 sessions before its
anchor disqualifies, and both bars must sit in the same listing segment.
The recorded formation books at widths 5 and 50 are not stored in the
permitted database, so the disagreement gate ran against the recorded
universe membership instead and matched exactly at every checked date,
including all 500 rows at each of the last 7 formations and 3 historical
spot checks.

Changes it: A.2 registers these conventions as binding. If the recorded
round's formation code ever enters scope and differs, the reproduction
reruns and the difference is reported, not reconciled.

## ADR-007: Worst-case cost bounds held until a fill measures them

The one cent TAF floor is confirmed nowhere. FINRA's schedule has no
per-trade minimum. The model holds the floor as a worst-case bound. The
fractional schedule's treatment of mixed integer-plus-fraction orders is
not determinable from IBKR's page. The model holds the whole-order 1
percent reading. Both resolve from a real fill statement in stage C.

Changes it: measured billing on paper and live fills.

## ADR-008: Correction one, the traded book need not equal the primary book

Chat Claude asserted the traded book must equal the primary measured
book, importing a principle from the buffer question where a divergence
would confound attribution. The principle does not apply here. The live
book never feeds the verdict, so nothing the live book does can confound
it. The primary width is chosen for information ratio and the traded
width for fill rate. They are different objectives and they select
different widths. This supersedes the coupling sentence in ADR-004.
Recorded here so a later session does not restore the wrong version from
the conversation.

Changes it: any design change that lets live data feed the verdict, which
ADR-001 forbids.

## ADR-009: Correction two, width 20 costs 41 percent on the signal clock

Chat Claude stated 15 to 20 percent. Fitting a power law to the two
recorded widths gives TE exponent -0.321 and excess exponent -0.445, so
excess decays faster than tracking error as the book widens. Width 20
carries IR 0.894 against width 5's 1.062, and time to verdict scales as
one over IR squared, giving 1.41. Widths 10 and 20 are interpolations
from a two-point fit and are labelled as such everywhere they appear.
Recorded here so a later session does not restore the wrong figure.

The exponent itself is a registered risk. Independent names would give
-0.5 on tracking error. The measured -0.321 says the book is four
correlated sector bets wearing twenty tickers: crypto miners, uranium
and nuclear, metals, optical and storage. A property of the rule, not a
defect to correct. The rule does not change.

Changes it: recorded measurements at more widths would replace the
two-point fit.

## ADR-010: Primary width 5, traded width 20, secondaries under Bonferroni

Width 5 is the primary for the verdict on its recorded IR of 1.062,
chosen before any forward data exists, on the already-spent holdout.
Widths 20 and 50 are pre-registered secondaries at alpha 0.025 each.
Width 20 is the traded width for fill rate, 10.4 fills per month against
4.0. ADR-008 makes the split legitimate. This supersedes ADR-004's
choice of 20 as primary.

Changes it: an amendment before the shadow series starts. Nothing after.

## ADR-011: The kill floor is a restart at 500 USD

Chat Claude proposed 600, which the A.1 numbers break: at width 20's
interpolated 42.54 percent tracking error, 600 is 1.04 sigma with a
driftless touch probability near 30 percent in year one, before beta
inflation on a high-beta book. A floor that fires on noise near fill 100
of the roughly 200 needed teaches nothing. 500 is 1.31 sigma, near 19
percent. 400 is 1.57 sigma, near 12 percent, and buys those 7 points at
the price of resuming with too little capital to matter.

The floor is a RESTART, not a termination. Breach halts the sleeve,
appends the breach record, and waits for an explicit operator decision.
Fill history survives, because a drawdown is not evidence about
execution cost. The four operational stops in Section 9 are
terminations. src/hfexperiment/kill.py enforces the distinction and a
mutation removing it is caught.

Changes it: a measured book beta would refine the touch probabilities.
The floor level itself changes only by amendment before the first live
order.

## ADR-012: The DEGRADED branch is closed

Section 0 left DEGRADED open as reduced whole-share sizing. A.1's
measured median book share price of 144 USD closes it: a 20-name
whole-share book needs about 2,880 USD against 900 deployed, and a
5-name book collapses to one share per name with equal weighting
destroyed. The registered consequence of a DEGRADED Task 3 result is no
live sleeve at this stake. Phase B continues either way.

Changes it: a materially larger stake, which is a new registration, not
an amendment. A collapse in book share prices does not reopen it,
because the branch decision must not track the thing it sizes.

## ADR-013: Choices this stage made autonomously

Spread measurement: the 2026-07-01 width-20 book was measured over the
three most recent complete sessions, 2026-08-19 to 2026-08-21, using the
same route, windows, and discard taxonomy as AiTrader's tick-multiple
measurement, through AiTrader's credential resolver, read-only. Result:
book median 12.77 bp, below the inherited band's lower edge, because the
book's names currently trade at large dollar volume. The measured
distribution replaces the band. Measuring at recent sessions rather than
at the formation date was chosen for relevance to what trading costs
now. Re-measuring near each future formation would change it.

Spend cap: 100 USD per rolling 365 days, about 1.75 times the worst-case
fractional projection of 56.84. A measured billing regime halves the
projection under Tiered and the cap stays as a guard.

Registered prior: drafted at 0.15 for the operator to confirm or replace
at acceptance, before the shadow series starts.

Section numbering: the stage prompt lists 13 items for 12 sections. The
registered prior folded into Section 12 with monitors and amendments.

Changes it: the operator at acceptance, for the prior. The others stand
unless a stated assumption fails.

## ADR-014: Acceptance by delegation, recorded

The operator accepted Sections 1 through 12 by delegation on
2026-08-24, with the drafted 0.15 prior standing unchanged. The act of
running the B.1 stage prompt was the acceptance, and the REGISTRATION.md
amendment log carries the dated record. Data existing at acceptance:
the A.1 reproduction through the 2026-07-24 pull, the A.2 spread
measurement over 2026-08-19 to 2026-08-21, and zero shadow
observations. The shadow series is authorized to start at the
2026-09-01 formation. Amendment 1 stays reserved for the Section 5
deferred parameters.

Changes it: nothing. An acceptance is a fact about a date.

## ADR-015: Formation-aligned start on 2026-09-01

The first accrual day is the 2026-09-01 formation, equal-weighted, so
no pre-registration price history enters weight computation. A
mid-month start would demand reconstructing drifted weights from a
formation the series never observed, and every reconstruction choice
would be a researcher degree of freedom. The roughly five sessions this
forfeits against a mid-month start cost 0.2 percent of a 2,061-day
clock. Formation-aligned entry removes every question about mid-month
weight reconstruction at a price too small to measure.

Changes it: nothing after the series starts. Section 12 forbids
amendments that respond to observed shadow outcomes.

## ADR-016: Fresh-adjustment queries, append-only store

The Task 0 reconciliation confirmed the 28 percent A.1-to-A.2 price gap
was market movement, not a stale adjustment: zero corporate actions in
the 2026-07-24 to 2026-08-24 window across all 20 names of the width-20
book, checked name by name against a public corporate-actions source
(reports/stage_b1/price_reconciliation.md). The pipeline is designed so
that check never has to be run by hand again. Every daily run
re-queries the session fresh with adjustment=all. Every formation run
re-queries the full trailing window fresh rather than trusting stored
history. Every result is appended with its query timestamp, reads take
the latest row per key, and no stored row is ever mutated, so an
adjustment landing between runs re-enters the store rather than aging
out of it. tests/test_barstore.py pins the no-mutation property.

Changes it: nothing. This is the stage's spine against the fabrication
class that sank the predecessor project.

## ADR-017: Choices Stage B.1 made autonomously

Benchmark member handling: a halted or delisted member marks at its
last available close, contributes exactly zero return, and stays in the
denominator until the next formation, which is Section 3's rule applied
to members as to book names. A member with a missing bar or failed
source excludes the day for every width, because a mean over a silently
shrunken membership is a different benchmark. Changes it: evidence that
the recorded round handled a missing member differently, which must be
reported and corrected before 2026-09-01.

Halt confirmation: an active name with no bar classifies missing_bar
until evidence arrives. Evidence is a bar at a later session, meaning
the name skipped this one while listed, or three consecutive absent
sessions under successful fetches. Both resolve to halted. This keeps
missing_bar strictly transient so no day blocks forever. Changes it: a
real halt feed, which Alpaca's daily bars do not carry.

Sequential lineage accrual: sessions accrue strictly in order within a
formation lineage, an excluded day blocks its lineage until retry heals
it, and the session return into a formation date belongs to the old
membership. The benchmark chain gates every width. Changes it: nothing,
this is arithmetic necessity, since day t+1 needs day t's state.

Credential separation: HFExperiment reads its own Alpaca keys from its
own .env, never AiTrader's resolver, and its timer fires at 23:30 UTC
against AiTrader's 22:30, so the two collectors never share a rate
window. The Task 0 corporate-actions check used a public web source for
the same reason. Changes it: nothing this stage.

Monitor rendering: plain-text renders written to reports/monitor/, no
service, per the Section 12 choice left to the session. The verdict
view validates every line it emits against an allowlist of
confidence-sequence shapes and fails the render otherwise. Changes it:
a later stage may add HTML on top of the same data, never bypassing the
guard.

Changes them: a stated assumption failing, or the operator before
2026-09-01. Nothing after the series starts.
