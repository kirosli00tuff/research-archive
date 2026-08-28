# HFExperiment Registration

This document is the binding pre-registration for the H-F live execution experiment.
Sections beyond Section 0 land in Stage A.2. Amendments append. Nothing edits in place.

## Section 0: Broker outcome map

Registered 2026-08-23, before any broker measurement was taken. The three outcomes
below are fixed now so the broker answer cannot be read against a bar its own
measurement could see.

### GO

A broker accepts a Canadian resident individual account, serves US equities,
exposes an API that places orders and reads fills programmatically, and accepts
fractional quantities through that API at 45 USD per name.

Consequence: the settled configuration runs as recorded. 20 names at 45 USD.
900 deployed. 100 held as settlement and fee buffer.

### DEGRADED

A broker clears every bar except fractional-through-the-API.

Consequence, registered now: per-name notional rises to whole-share size. Book
width falls to what 900 USD supports at that size. Amendment 1 records that the
parameters were forced by execution mechanics rather than chosen, and states the
arithmetic. Whole-share sizing makes book width a function of share price. No
registered rule may inherit that property by accident. Task 4 of Stage A.1
measures the median share price of the top-20 book, which is the input that
decides whether this path is survivable at all.

### BLOCKED

No reachable broker clears the bars.

Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow
series needs no broker, no account, and no money. The signal question still gets
answered.

### Scope note

One week of live trading is enough to measure execution. One week is nowhere near
enough to measure signal. The verdict on the signal reads the shadow series and
only the shadow series.

## Section 1: The hypothesis

The equal-weighted top five names by 12-1 momentum with a skip month in
the U-LIQ-500 universe, re-formed on the first trading session of each
month, earn positive daily excess return over the equal-weighted
universe, because prices underreact to sustained firm-level change and
the effect, measured at 27.99 bp per day on the already-spent holdout,
exceeds the 4.07 bp per day that round-trip costs consume at the
measured 40 percent monthly churn, so a fee-paying participant keeps
most of it.

Sections 1 through 12 registered 2026-08-23. Binding once the operator
accepts them. Registered numeric thresholds live in
src/hfexperiment/registered.py and the structural guard test fails if
any lacks an enforcement site.

## Section 2: The two series

The SHADOW series is the signal instrument. It computes the registered
book daily from price data alone. No fills. No commissions. It would run
identically if nobody traded a dollar. The LIVE series is the execution
instrument, actual fills at a real broker at micro size. The difference
between them is the execution cost, measured rather than modelled.

The shadow series starts at the registration date and is never
backfilled before it, because backfilling spends a holdout already
spent. Daily bars backfill freely, so the honest guarantee is the
registration timestamp and not the collection start.

## Section 3: Universe and formation

Universe rule U-LIQ-500-stk-w60-m40-p5, copied verbatim from the
recorded round and reproduced by Stage A.1 against all 124 recorded
formation dates. Momentum is 12-1 with a skip month under the anchor
conventions ADR-006 fixed: far anchor the session before the formation
date 12 months back, near anchor the session before the formation date
1 month back, closes from the last bar at or before each anchor, a gap
above 20 sessions disqualifies, both bars in one listing segment.

Ties break on symbol ascending. A halted or delisted name marks at its
last available close and redeploys at the next scheduled formation,
never intra-month.

## Section 4: Widths

Width 5 is the PRIMARY width for the verdict. It carries the highest
recorded information ratio, 1.062, and it is chosen now, before any
forward data exists, on the already-spent holdout rather than on
anything the shadow series will produce.

Widths 20 and 50 are pre-registered secondaries. The primary spends
alpha 0.05 one-sided. The secondaries spend 0.025 each, Bonferroni, so
the family never outspends the primary.

Width 20 is the TRADED width, chosen for fill rate: 10.4 fills per month
against 4.0 at width 5, which reaches the roughly 200 fills the
execution measurement needs in about 19 months instead of 50. The traded
width is not the primary measured width, and that is legitimate here
because the live book never feeds the verdict. The primary width serves
information ratio. The traded width serves fill count. They are
different objectives and they select different widths. ADR-008 records
the correction that forced this split.

The recorded and interpolated width figures, from the two-point power
law fit (TE exponent -0.321, excess exponent -0.445):

| width | TE pct/yr | excess bp/day | IR | status |
|---|---|---|---|---|
| 5 | 66.40 | 27.99 | 1.062 | recorded |
| 10 | 53.15 | 20.56 | 0.975 | INTERPOLATED from two-point fit |
| 20 | 42.54 | 15.10 | 0.894 | INTERPOLATED from two-point fit |
| 50 | 31.70 | 10.04 | 0.798 | recorded |

Time to verdict scales as one over IR squared, so width 20 on the signal
clock costs 1.41 times width 5. ADR-009 records the correction from the
15 to 20 percent figure chat Claude stated.

Registered risk: the TE exponent of -0.321 against the -0.5 of
independent names says the book diversifies far worse than name count
suggests. The A.1 formations show why. The book is four correlated
sector bets wearing twenty tickers: crypto miners, uranium and nuclear,
metals, optical and storage. This is a property of the rule, not a
defect to correct, and the rule does not change.

## Section 5: Sizing and cadence

Total 1,000 USD. 900 deployed. 100 held as settlement and fee buffer.
Formation on the first trading session of each calendar month.

Per-name notional stays DEFERRED to Amendment 1 as
per_name_notional_usd, because the fractional billing regime decides it
and only a paper fill settles that. The two candidate outcomes, both
priced in Section 7: under whole-share Tiered billing 45 USD deploys the
full stake at the 50 bp cap rate, and under fractional billing notional
stops mattering for the rate because the schedule is flat at 100 bp per
side. The broker minimum order size, broker_min_notional_usd, and the
billing regime of a mixed integer-plus-fraction order,
mixed_order_billing_regime, are DEFERRED to the same amendment. The
order gate refuses to price any order while these are deferred.

## Section 6: The DEGRADED branch, closed

Section 0 left DEGRADED open pending the median share price of the book.
A.1 measured it: 144 USD at the last two formations, up from 36 in March
and April. At 144, whole-share sizing on 900 USD cannot fill a 20-name
book at all, because 20 names at one share each already cost about
2,880 USD. A 5-name book gets one share per name, 720 of 900 deployed,
with equal weighting destroyed by per-name prices from 22 to 1,595 USD.

The registered consequence of a DEGRADED Task 3 result is therefore NO
live sleeve at this stake, not a reduced one. Phase B continues either
way, because the shadow series needs no broker. ADR-012 records the
closure.

## Section 7: The cost model

Three billing regimes, never blended: whole-share Tiered, whole-share
Fixed, and fractional. Every regime reports its commission term and its
spread term separately. Commission is deterministic, known before
submission, and subtracts exactly, so it is a P&L drag and not a
measurement contaminant. The measured quantity is fill price against
arrival mid, and commission never enters it.

Spreads are MEASURED on the real book, not assumed from a band. All 20
names of the 2026-07-01 width-20 book were measured on the consolidated
tape over sessions 2026-08-19 to 2026-08-21: median 12.77 bp, p75 17.2,
p90 20.7, max 27.4. The inherited 15.8 to 50 bp band predicted the wide
end and measured wrong in the favourable direction, because the book's
names currently trade at large dollar volume. The measured distribution
replaces the band. Any future unmeasured name carries the band's upper
bound of 50 bp, never its middle.

The one cent TAF floor stays UNMEASURED and held as a worst-case bound
until a real fill statement settles it. Whether a mixed
integer-plus-fraction order bills whole on the fractional schedule stays
UNMEASURED and deferred per Section 5. Tables live in
reports/stage_a2/cost_table.md, generated by scripts/cost_table_a2.py
from src/hfexperiment/costmodel.py. Annual deterministic drag at the
traded width and measured churn: 28.76 USD per year under whole-share
Tiered, 56.84 under fractional.

## Section 8: The order gate and the spend ledger

Every order is priced before sending. The gate refuses on:

1. Insufficient settled cash for a buy.
2. Notional below the broker minimum.
3. A non-fractionable symbol.
4. A formation that failed its reproduction check.
5. Cumulative spend at or above the registered cap of 100 USD per
   rolling 365 days, about 1.75 times the worst-case fractional
   projection.
6. A non-SmartRouted route, which forfeits Tiered pricing in IBKR's own
   words, per docs/ACCESS.md.
7. Any required parameter still DEFERRED.

A refusal names the arithmetic and writes nothing. The gate logic is
src/hfexperiment/gate.py. Stage C.1 wires it to the append-only spend
ledger and may add refusals by amendment, never remove one.

## Section 9: Kill criteria

The equity floor is a RESTART, not a termination. A termination ends the
experiment. A restart pauses the capital. On breach of the floor the
sleeve halts, appends the breach record, and requires an explicit
operator decision to resume. It does not delete the fill history and it
does not void the execution measurement, because a drawdown is not
evidence about execution cost.

The floor is 500 USD of total account equity, a 400 USD loss on 900
deployed after the 100 buffer, 1.31 sigma of the width-20 tracking
error, driftless touch probability near 19 percent in year one. Against
the table: 600 touches near 30 percent before beta inflation and would
fire on noise as the expected case. 400 buys only 7 more points of touch
probability and leaves too little capital for any resumed sleeve to
mean anything. Both neighbours lose. The figures ignore market beta,
which the high-beta book makes optimistic, and ignore positive drift,
which cuts the other way. ADR-011 records the choice.

To resume after a breach the operator reviews the breach record, decides
continue or stop in writing, appends a resume record naming the breach,
and re-arms the gate. No automatic resume exists.

Terminations, each final:

1. Two consecutive formation failures.
2. Any order-gate bypass.
3. Any fill recorded without an arrival mid captured.
4. Any formation that cannot reproduce from the price store.

## Section 10: The claim boundary

Live P&L is an execution-cost measurement. It is never the signal
verdict. The signal verdict comes only from the pre-registered
always-valid monitor on the shadow series. A profitable live week says
nothing about the hypothesis and a losing one says nothing either.

## Section 11: The verdict schedule

Studentized asymptotic confidence sequence on daily shadow excess
return, alpha 0.05 one-sided, tuning parameter rho set by minimizing the
boundary at a crossing time of 1,600 trading days, frozen at 0.071641.
Success when the lower bound clears the measured cost hurdle of 4.07 bp
per day, computed at the primary width under the worst-case fractional
regime with the measured width-5 spread. Futility when the upper bound
falls below 10 bp per day. Peeking is permitted at any time and inflates
nothing, which is the whole reason for the construction.

The honest arithmetic, registered beside it: at the primary width's
27.99 bp per day against daily noise near 418 bp, implied by 66.4
percent annualised, pointwise arithmetic needs about 600 days and
sequential inflation puts the expectation at order 1,000 to 2,000
trading days before the lower bound clears zero. Under this exact frozen
construction, with the sample mean holding at 27.99, the lower bound
clears zero at day 2,061 and clears the hurdle at day 2,852. Eight to
eleven years. The operator knows this and proceeds because the execution
question is answerable now and the signal question is not.

## Section 12: Monitor views, amendments, and the registered prior

The health view and the verdict view are structurally separated, per
Stage B.1. The health view may show anything. The verdict view shows
only the confidence sequence against its two registered bars.

Amendments are dated, numbered, appended, and each records what data
existed when it was made. No amendment may respond to an observed shadow
outcome. Amendment 1 is reserved for the deferred parameters of Section
5 and must land before the first live order.

The registered prior: this session drafts the operator's probability
that the sleeve ever clears its verdict at 0.15, and the operator
confirms or replaces that number at acceptance, before the shadow series
starts. A documented negative is a valid outcome at a cost of roughly 30
to 60 USD a year at the traded width, per the Section 7 drag table.

## Amendment log

Append-only.

### 2026-08-24: Acceptance record

Sections 1 through 12 accepted by operator delegation. The registered
prior stands at 0.15 as drafted. The shadow series is authorized to
start at the 2026-09-01 formation. Data existing at this entry: the A.1
reproduction against the recorded round through the 2026-07-24 pull,
the A.2 spread measurement over sessions 2026-08-19 to 2026-08-21, and
zero shadow observations, because the series has not started. Amendment
1 stays reserved for the deferred parameters of Section 5 and has not
landed. Nothing above this log changes.

### 2026-08-25: Section 0 verdict

BLOCKED. The IBKR TWS API refused fractional quantities however
phrased on paper account [paper account ID removed], error 10243 on decimal
totalQuantity across two book names and two order types, error 10244
on cashQty, while a whole-share control order was accepted, evidence
in reports/stage_a1b. Per Section 0 phases C and D stop and phase B
proceeds unchanged. No parameter changes.

### 2026-08-26: Closure

Experiment closed by operator decision, instruction dated 2026-08-26.
The live track was never funded and zero capital was deployed. The
shadow series was disarmed before its first accrual:
hfexperiment-bars.timer stopped and disabled via systemctl --user,
verified that no HFExperiment unit remains scheduled. The verdict was
never computed. Closure is terminal. The repository is preserved as
record. Data existing at this entry: everything recorded above, and
zero shadow observations, because the series never started.
