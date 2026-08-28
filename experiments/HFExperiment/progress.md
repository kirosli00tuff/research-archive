# Progress

Append-only. One dated entry per stage, newest at top.

## 2026-08-26: Closure

Closed. Experiment closed by operator decision, instruction dated
2026-08-26. The live track was never funded, zero capital was
deployed, and the closure is terminal. The repository is preserved as
the record.

Disarmed. hfexperiment-bars.timer stopped and disabled via systemctl
--user before its first accrual, verified that no HFExperiment unit
remains scheduled. The shadow series never produced an observation and
the verdict was never computed.

End state. Stages A.1 through C.1 complete and green. A.1b verdict
BLOCKED. B.2 registered and unrun. B.1a cancelled as moot: no
formation will ever call the assets endpoint. Recorded in the
REGISTRATION.md amendment log as a dated closure entry. Nothing
deleted.

## 2026-08-25: Stage A.1b

ETA stated before starting: 60 minutes. Actual: 35 minutes.

Measured. The fractional question, settled by paper order behaviour on
[paper account ID removed], market closed, which did not matter because every answer
came at order validation. All 20 names of the 2026-08-03 width-20 book
advertise MinSize 0.0001 and SizeIncrement 0.0001, fractionable at the
instrument layer. Every fractional order was refused by the API
channel: error 10243 on decimal totalQuantity, market and limit, MU
and TE, and error 10244 on cashQty. A one-share control order was
accepted and queued for the open, proving the channel works, Read-Only
is off, and the refusal is specific to fractional sizing. Five of the
ten authorized orders used. No fills, no commissions, positions
verified flat twice. Evidence ledger and report in reports/stage_a1b.

Fired. Section 0 verdict BLOCKED, recorded in the REGISTRATION.md
amendment log as a dated factual entry. Per Section 0 phases C and D
stop and phase B proceeds unchanged. Per Section 6 the DEGRADED
whole-share branch stays closed at this stake. The shadow series
carries the experiment alone and answers the signal question, which
was the design's point. ADR-003's reopening clause stands: an Alpaca
Canadian launch or IBKR shipping API fractional support reopens the
table as a new measurement.

Resolved. The cashQty-versus-decimal documentation contradiction,
ADR-022, by observed behaviour with verbatim errors as citation.

Open. Operator re-checks Read-Only API in the Gateway, which stays on
until a live phase exists to need otherwise. The B.1a assets-endpoint
fix before 2026-09-01 remains the critical pre-start item. C.2 and
D.1 as previously scoped are now moot at this stake.

## 2026-08-25: Stage C.1

ETA stated before starting: 120 minutes. Actual: 50 minutes.

Built. The order intent pipeline as pure data: formation to target
book to diff to intents to gate (intents.py). The wired gate with the
eight refusals, account pinning first (gatewire.py, brokerconfig.py).
The spend ledger on the A.1 append-only primitive with the
rolling-year query and D.1's reconciliation stub (spendledger.py).
The read-only connectivity probe speaking minimal v100 TWS wire with
an encoder that can only emit START_API and REQ_CURRENT_TIME
(ibkrprobe.py). The mock broker with the adapter shape and no submit
method (mockbroker.py). Nothing places an order, paper or live.

Demonstrated. All eight refusals produced with named arithmetic
against the real 2026-08-03 width-20 formation, computed fresh into
C.1's own store. The account pin shown four ways at the gate plus the
construction wall. The steady state shown: all 20 intents refused at
deferred_parameter_unresolved because Amendment 1 has not landed. One
intent reached priced-and-ready under DEMO-resolved parameters and
stopped exactly at Amendment 1 under the registered ones. Evidence in
reports/stage_c1/refusals.md with the demonstration ledgers beside it.

Probed. The paper Gateway is live at 127.0.0.1:4002, server version
187. [paper account ID removed] verified in a managed list of exactly one account,
server time read, disconnected. Mode-port asserted before connecting.
Read-Only API stays on.

Found. Alpaca serves trading-API endpoints for paper keys from
paper-api.alpaca.markets. B.1 pinned api.alpaca.markets, which 401s on
/v2/assets. B.1's nightly runs succeed until 2026-08-31 because no
assets call happens before a formation is due, and the 2026-09-01
formation run will fail loudly until a one-line fix lands under B.1
authorization. Recorded in ADR-021. The fix should land before
2026-09-01.

Tested. 158 tests green under mypy strict and ruff, the B.1 monitor
guard among them. All four required mutations applied to real source,
each caught, restored green: pin check deleted, empty account passing
as default, SmartRouting bypassed, deferred parameter read as 45.0.
Evidence in reports/stage_c1/mutation_tests.txt.

Open. C.2 waits on A.1b's paper fills for the three deferred
parameters. The B.1 paper-api fix before 2026-09-01. Alpaca keys are
in .env and the timer's first collection runs tonight 23:30 UTC.

## 2026-08-24: Stage B.1

ETA stated before starting: 150 minutes. Actual: 80 minutes.

Accepted. Sections 1 through 12 accepted by operator delegation,
2026-08-24, prior standing at 0.15, recorded in the REGISTRATION.md
amendment log. Shadow series authorized to start at the 2026-09-01
formation.

Reconciled. The 28 percent gap between A.1's 143.89 median (adjusted
closes, 2026-07-01) and A.2's 103.25 median mid (live quotes,
2026-08-19 to 21) is market movement. All 20 width-20 names checked
against a public corporate-actions source: zero splits, zero in-window
dividends between 2026-07-24 and 2026-08-24. The two suspicious ratios,
MXL at 0.518 and WOLF at 0.546, are real declines confirmed by
current-basis 52-week ranges. Evidence in
reports/stage_b1/price_reconciliation.md. The gap RECONCILES. Proceed
authorized.

Built. Append-only bar store with query timestamps, no row ever mutated
(barstore.py). Alpaca source with adjustment=all on every bar query and
injected transport (alpaca_source.py). Credential loader that refuses
loudly with BLOCKED-ON-OPERATOR (envfile.py). The five accrual states
with a single classification site (states.py). Book and panel accrual
arithmetic that refuses to accrue past an absence (shadow.py). The
cited benchmark definition (benchmark.py). Fresh-full-window formation
runs (formationrun.py). Sequential lineage accrual over append-only
ledgers (accrual.py). The verdict engine at frozen rho 0.071641 with
the registered projection in every record (verdictengine.py). The two
structurally separated monitor views with the render-failing guard
(monitor.py). The 23:30 UTC daily entry point (scripts/daily_run.py).

Armed. systemd user timer installed and enabled: Mon to Fri 23:30 UTC,
Persistent=true, MemoryMax=2G, one hour staggered from AiTrader's
22:30. Linger confirmed. Next trigger 2026-08-25 23:30 UTC. First run
will fail loudly with exit 2 until the operator copies Alpaca keys into
.env. The verdict view renders its empty pre-start state. First accrual
lands after the 2026-09-02 close if keys exist by then.

Tested. 123 tests green under mypy strict and ruff. All three required
mutations applied to real source, each caught, restored green:
synthesized carried-forward price, source_failed merged into
missing_bar, accrual row in the verdict view. Evidence in
reports/stage_b1/mutation_tests.txt.

Open. Operator copies Alpaca data keys into .env, the only blocker on
the signal clock. IBKR account for Stage A.1b Task 3 remains open.
Benchmark missing-member handling recorded as ADR-017's first entry:
if the recorded round differed, correct before 2026-09-01.

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


## 2026-08-28T22:10Z — ADR-026: the stale no-account blocker, corrected

Not a stage. A record-hygiene amendment, made in chat with the operator
present, touching two documents and no code.

The defect. docs/ACCESS.md Task 3 opened with "The operator holds no IBKR
account" and marked all six sub-tests BLOCKED-ON-OPERATOR. ADR-003 recorded
the GO-versus-DEGRADED verdict as UNDECIDED on the same ground. Both were
true when A.1 wrote them. A.1b overtook them on 2026-08-25 by connecting to
paper Gateway 127.0.0.1:4002, server version 187, account [paper account ID removed], and
settling the deciding bar by behaviour. Neither document was amended, so the
repository advertised a blocker that had already dissolved and an UNDECIDED
verdict that A.1b had resolved to BLOCKED.

How it surfaced. The assistant quoted the stale ACCESS.md line to the
operator as current on 2026-08-28. The operator replied that he holds a
funded live account and a paper account behind a running Gateway. The A.1b
session log corroborates him, so the correction rests on the repository's
own evidence rather than on the statement alone.

The fix. ACCESS.md Task 3 re-headed SUPERSEDED, the false sentence struck
rather than deleted, the sub-test table re-statused against A.1b: four
RESOLVED (decimal REFUSED at 10243, cashQty REFUSED at 10244, MinSize and
SizeIncrement ELIGIBLE at 0.0001 on all 20 names, whole-share control
ACCEPTED), two MOOT (routing comparison, mixed-order billing, both moot
because decimal refuses however routed), one RUNNABLE (billing plan on a
real paper fill). ADR-003 keeps its text with a superseded note beneath it.
ADR-026 written. Nothing rewritten to look as though it was always right.

What did not change, and this is the point. The fractional closure rested on
measurement, not on absent access, so the Section 0 BLOCKED stands exactly as
recorded. The commission arithmetic is read off published tiers and account
access does not move a fee schedule. Whole-share API trading was never
closed; only slicing is.

Safety, reaffirmed rather than revised. ADR-018's account pinning now guards
a stated fact instead of a hypothetical one: the Gateway authenticates from
the full-access main login and a funded live account sits behind it. Work on
the runnable sub-test pins [paper account ID removed], refuses every other account id, asserts
port 4002 before connecting, and leaves Read-Only API on outside a registered
order test.

Open item: the billing-plan sub-test is runnable and unscheduled. It is not
required by any live hypothesis, since HFExperiment is closed at the
registered stake. It resolves a documentation contradiction cheaply whenever
an equity leg is next proposed.
