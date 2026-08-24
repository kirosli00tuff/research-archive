# Progress

Append-only. One dated entry per stage, newest at top.

## 2026-08-23: Stage A.2

ETA stated before starting: 60 minutes. Actual: 35 minutes.

Measured. Quoted spreads for all 20 names of the 2026-07-01 width-20
book, consolidated tape via the route AiTrader owns, sessions 2026-08-19
to 2026-08-21, 9 cells per name. Book median 12.77 bp, p75 17.2, p90
20.7, max 27.4. The inherited 15.8 to 50 bp band predicted the wide end
and measured wrong in the favourable direction. No name UNMEASURED. The
TAF one cent floor stays UNMEASURED as a worst-case bound.

Built. Cost model with three billing regimes that never blend,
commission and spread terms apart (costmodel.py). Registered thresholds
and machine-detectable deferred parameters (registered.py). Kill
criteria with the restart-versus-termination distinction (kill.py).
Pure order-gate refusal logic (gate.py). Asymptotic confidence sequence
boundary with rho frozen at 0.071641 (verdict.py). Rebuilt round-trip
and drag tables in reports/stage_a2/cost_table.md.

Registered. REGISTRATION.md Sections 1 through 12 appended below
Section 0, unchanged. Primary width 5, traded width 20, secondaries 20
and 50 at alpha 0.025. Kill floor 500 USD as a restart. DEGRADED branch
closed: no live sleeve at this stake. Cost hurdle 4.07 bp per day.
Spend cap 100 USD per rolling year. Three parameters DEFERRED to
Amendment 1 and the gate refuses while they are. Both chat-Claude
corrections recorded as ADR-008 and ADR-009.

Tested. 76 tests green under mypy strict and ruff. Both required
mutations applied to real source, caught, restored green. Evidence in
reports/stage_a2/mutation_tests.txt.

Open. Operator acceptance of Sections 1 through 12, including the
drafted 0.15 prior. Amendment 1 waits on the paper fill. B.1 starts the
shadow series.

## 2026-08-23: Stage A.1

ETA stated before starting: 75 minutes. Actual: 25 minutes.

Built. Repository scaffolded with uv, ruff, mypy strict, pytest,
pre-commit, Makefile. REGISTRATION.md Section 0 committed at c4e9817
before any broker measurement. Universe rule copied verbatim from
AiTrader backtest/universe.py. Formation module, commission module,
append-only ledger, read-only database access, structural config guard.

Measured. Broker field verified at source in docs/ACCESS.md. IBKR Canada
is the only reachable broker with residency, US equities, and an order
API. Cap rule confirmed in IBKR's own words. Crossovers confirmed at 70
and 100 USD. New finding: a separate fractional-order schedule, greater
of 1 percent or one cent, which doubles projected commission if it
applies to whole orders. SmartRouting confirmed required for Tiered on
API orders. SEC Section 31 at 20.60 per million effective 2026-04-04.
FINRA TAF at 0.000195 effective 2026-01-01. The assumed one cent TAF
floor is confirmed nowhere and is held as a worst-case bound.

Reproduced. All 124 recorded formation dates identical. Universe exact at
all 10 checked dates, all 500 rows each. Books formed at widths 5, 20,
50 for the last 7 formations. Churn at width 20 averaged 5.2 names per
month. Median book share price at width 20 ranged 36 to 144 USD over the
last 6 months. Database hash unchanged: c30d3f4486e975a0 before and
after.

Blocked. Task 3 fractional-through-API resolves only by paper test. No
IBKR account exists. Every sub-test recorded BLOCKED-ON-OPERATOR with
its precondition in docs/ACCESS.md.

Tested. 27 tests green under mypy strict and ruff. Three mutations
applied to real source, each caught by the suite, source restored green.
Evidence in reports/stage_a1/mutation_tests.txt.

Verdict inputs for A.2. GO versus DEGRADED undecided pending Task 3.
BLOCKED ruled out on documented bars.
