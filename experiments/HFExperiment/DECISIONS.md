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
