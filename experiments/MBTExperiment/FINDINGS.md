# FINDINGS — MBTExperiment Stage B.1

**Every claim carries its sample size in the same sentence as its number.**
A negative with a hidden `n` is not a result, and neither is a positive.

**Stage verdict: HARNESS-BLOCKED**, 2 of 4 registered conditions held, down from
3 of 4 at Stage B. Recomputable with `uv run python -m mbt.cli verdict`.

**The blockers moved from the environment into this harness, and that is the
result.** Stage B was blocked because no Gateway session existed. A session now
exists, answers a validated preview in **0.24 to 0.26 seconds at n = 7
previews**, and the stage is blocked anyway, for two reasons Stage B could not
see.

---

## 1. The two gates

**Neither gate fired, and both are recorded with their reasons rather than
omitted from the table.**

| gate | outcome | ceiling | measured | n |
|---|---|---|---|---|
| **MARGIN** | **ABSENT** | $1,000 per contract, being 12.80% of $7,812.46 | `Absent(no_live_session)` | **n = 0 live sessions** |
| **COST** | **ABSENT** | 34.600 bps of notional | `Absent(insufficient_sample)` | **n = 0 of 20 registered windows** |

**The MARGIN gate is `Absent(no_live_session)`** and was registered as unfireable
in this stage before any measurement. Unchanged from Stage B, and unchanged by
the fact that paper margins are now readable: a margin is a property of the
ACCOUNT and needs a U-prefixed session.

**The COST gate is `Absent(insufficient_sample)` at n = 0 of 20 windows**, and it
carries a second block that survives the first: the fee leg is
`Absent(not_served)`, so the all-in sum cannot be formed and a strict lower bound
can FAIL but never PASS.

> **Both gates remain blocked from PASS for independent reasons.** Fixing the
> market-data subscription alone would not change either.

## 2. The reversal, measured

**IB Gateway now answers.** 5 of 5 TCP connects, against 0 of 13 last run.

| measurement | Stage B | Stage B.1 | n |
|---|---|---|---|
| TCP reachability | 0 reachable | **5 reachable** | n = 5 attempts |
| API handshake, distinct from the connect | `Absent(gateway_unreachable)` | **0.308 s** | n = 1 handshake |
| accounts read back | `Absent(gateway_unreachable)` | **1, D prefix, length 9** | n = 1 session |
| provenance guard | not reachable | **declared paper, measured paper, agree** | n = 1 session |
| listed MBT option series | `Absent(gateway_unreachable)` | **11 series, 4 underlying futures** | n = 11 series |
| expiry nearest the registered 30-day tenor | `Absent(gateway_unreachable)` | **W1E:20261002, settling 2026-10-02T15:00:00Z** | n = 11 candidates |
| futures options permission, CME crypto | `Absent(gateway_unreachable)` | **PRESENT** | n = 1 preview |

**Permission is PRESENT and is therefore not the terminal finding Task 1
registered.** The venue returned an initial margin for a short MBT option, so the
account may price the instrument, at n = 1 preview. **Measured through a
diagnostic outside the package**, because the package's own path cannot obtain a
margin at all. Through the package path it is `Absent(permission_unknown)` at
n = 1 attempt, and an unanswered request is never merged with a refused one.

## 3. There is no real-time market data subscription, and it blocks the census entirely

**Requesting real-time returned no touch on any of the three registered legs, at
n = 3 legs, with broker error 354.** Requesting delayed returned a touch on all
three, at n = 3 legs, with error 10167.

| leg | real-time requested | delayed requested |
|---|---|---|
| `future_hedge` MBTU6 | no touch, `Absent(unquoted_leg)` | 81770.0 / 81785.0, **refused `delayed_tick`** |
| `option_call` | no touch, `Absent(unquoted_leg)` | 1625.0 / 1860.0, **refused `delayed_tick`** |
| `option_put` | no touch, `Absent(unquoted_leg)` | 6895.0 / 7200.0, **refused `delayed_tick`** |

**The absence is persistent across n = 5 independent sessions between 19:11Z and
19:42Z**, so it is a subscription state rather than a transient outage.

**These are MEASURED refusals on real venue data**, where Stage B could only
demonstrate the same guards on constructed inputs.

**A trap, recorded because the harness nearly walked into it.** The ticker
reported `marketDataType = 1` while the feed served nothing, so **the status
field alone does not establish a subscription**. The registered check order saved
it: structure is checked before delay, so a NaN touch is refused as `unquoted_leg`
before the status is consulted. `tests/test_marketdata.py` now pins that
deliberately at **n = 7 conversion cases**.

## 4. The registered straddle was refused, exactly as registered

**`Absent(unquoted_leg)` on the at-the-money reference leg, so registered Section
3.1 refused the whole straddle**, at n = 3 attempts. No reference price means no
at-the-money strike, and none was substituted.

**The chain itself is healthy at n = 11 listed series.** The settlement instant
was read from the contract (`lastTradeTime 10:00:00` in `US/Central`) rather than
assumed, so registered rule 3.3 measured the tenor to the settlement instant and
not to midnight.

**One registered-rule tension is recorded and NOT amended.** The expiry universe
is every listed MBT option expiry across every underlying futures month, which is
what "the listed expiry" says. **Measured: the front future MBTU6 lists 6
expiries of which the longest is 22 days**, so a front-future-only universe would
contain no expiry near the registered 30-day tenor at all, while the full listed
chain contains one at 29 days. The registration does not restrict the universe,
and narrowing it here would be a rule invented after seeing the chain.

## 5. The census is begun and refused

| field | value |
|---|---|
| windows accepted | **0** of 20 required |
| windows refused | **3**, each recorded with its reason |
| refusal reason | `unquoted_leg` on `future_hedge`, **3 of 3** |
| median round-trip spread | `Absent(insufficient_sample)` at **n = 0** |
| p90 round-trip spread | `Absent(insufficient_sample)` at **n = 0** |
| **projected completion date** | **`Absent(insufficient_sample)`** |

**The percentiles are absent, not zero and not nan**, and a test pins that over an
empty sample.

**The projection runs from the first window actually collected, and none was.**
The registered duration of **5 collection days** is unchanged and is a property
of the rule, but it is **not a completion date**, because there is no start to
add it to. A date computed from a hypothetical start would be a schedule for a
census that cannot begin, and the blocker is not time. See ADR-011.

**No gap was filled from anywhere.** Deribit's 22.50 bps remains REFERENCE ONLY
and no gate reads it.

## 6. The paper margin, INDICATION ONLY

**All 18 paper previews returned an initial margin between 3,441.42 and 4,599.07
USD per contract, against a registered ceiling of 1,000.00, a ratio of 3.44x to
4.60x, at n = 18 previews across 9 listed strikes and both rights. Not one sat
below the ceiling.** Median 3,930.96 USD per contract at n = 18.

**No reference price was used**, so no registered rule was exercised or bypassed:
margins are reported across listed strikes and need no at-the-money determination.
**This is not the registered straddle**, which was refused.

> **A paper margin model is not the live one, and the MARGIN gate remains
> `Absent(no_live_session)`.** IBKR's paper environment approximates margin and
> does not reproduce the live SPAN calculation, so these figures measure the
> simulator rather than the account that would hold the position. **Nothing here
> is a gate result and nothing here is verdict-bearing.**

`tests/test_paper_margin.py` pins the refusal against these measured figures at
**n = 5 values and 12 cases**. The danger is specific: every measured paper margin
sits above the ceiling, so a promoted figure would produce a confident FAIL that
might point the same way the live answer does, and **a verdict that is right by
accident is not a result**.

## 7. Two harness defects block the what-if path, both measured

**`OrderState` carries 17 fields and zero exchange or regulatory fee fields,
confirmed against a live session at n = 3 previews.** Stage B established this by
reading the library; it is now measured against the venue, and Stage B's
expectation is confirmed rather than contradicted.

**Defect one: the venue rejects every what-if this package can construct.** IBKR
error 321, *"What-If order should have transmit flag set to TRUE"*, at **n = 4 of
4 products**. `build_short_option_order` sets `transmit=False` and
`what_if_order` refuses `transmit=True`. The request is never resolved, so the
call hangs rather than failing; the wait is now bounded at 20 s and recorded as a
typed absence.

**Defect two: an unset TIF returns no `OrderState` at all.** IBKR warning 10349,
and the request ends empty. Isolated at **n = 4 combinations**: TIF is
load-bearing, the account field is not.

**Neither was changed.** See ADR-010. Flipping the transmit flag would clear the
binding blocker and, with an operator margin supplied, reach HARNESS-READY on a
safety property rewritten after seeing what the venue demands.

## 8. The fee leg is still absent, and one observation is recorded without inference

**`Absent(not_served)`**, unchanged, now with a fourth independent reason
alongside Stage B's three: **the response carries no breakdown at all**, at n = 3
previews against a live session.

**The what-if commission scalar was 2.01 USD per contract at n = 18 previews**,
against the registered IBKR Canada figure of **0.85 USD per contract** measured on
the live schedule on 2026-08-30, a difference of 1.16 USD.

**That difference is NOT attributed to fees.** A paper commission report is
synthetic, so the excess is equally consistent with the simulator's own model,
and no field in the response separates the two. **The absence of a fee field is
not the absence of the fee from the scalar, and the presence of an excess is not
evidence of one either.**

**Direction of the resulting error, unchanged:** every absent leg is
non-negative, so the measured legs form a strict lower bound erring
**permissively**, and the registered 34.600 bps ceiling overstates the room by
exactly the unmeasured fee `F >= 0`, bounded below at zero and **not bounded above
by any evidence held here, at n = 0 measurements of it**.

## 9. Two configuration defects, found before any measurement

**The client id slot held the account number**, at n = 1 variable. The TWS API
`clientId` is an int32, so a 9-character D-prefixed string cannot be one.

**And the loader echoed it.** `int()` raises `ValueError` carrying the string it
failed on, which is not a `ConfigError`, so the CLI died on an uncaught traceback
**with the account number in it**. `tests/test_honesty.py` scans **tracked files**
and was clean the entire time the hole was open, because it cannot see a runtime
exception path.

**Both fixed.** The refusal is now a typed `ConfigError` naming the variable and
reporting the observed shape, never the value. See ADR-012. **This is the same
family as ADR-009**, arriving from a different direction: a guard refusing
correctly while the path that matters goes unchecked.

## 10. The guards and the boundary

**All 5 registered mutations behave as registered**, at **0 failures across 5
mutations**, each applied to real source, the right check failing, the file
restored byte for byte, and the whole suite green on the restored tree.

**The no-transmit scan is CLEAN over 22 package files and 6 tool files, 0
findings.** **181 tests pass**, `mypy --strict` clean over 36 source files.

**The read-only boundary is unchanged across all three snapshots**: 2,901
entries, 324,887,193 bytes, 0 unreadable paths.

| digest | Stage B open | Stage B close | Stage B.1 close | equal |
|---|---|---|---|---|
| full | `c28e6860…89f81` | `c28e6860…89f81` | `c28e6860…89f81` | **yes** |
| stable, 115 non-cache entries | `441495bc…53641` | `441495bc…53641` | `441495bc…53641` | **yes** |

**The Stage B and Stage B.1 manifests are byte-identical**, an independent check
that does not rely on the digest. VRPExperiment's working tree is clean and its
HEAD is unchanged at `d37cf6d`.

## 11. What this stage does not establish

- **No live margin was read**, at **n = 0 live sessions**. The paper-only clause
  is in force and the MARGIN gate is absent.
- **No spread was measured**, at **n = 0 accepted observation windows**.
- **No fee was determined**, at **n = 0 measurements**.
- **No premium was recomputed, extended or re-read.** VRPExperiment's 1,955-day
  sample is spent and was read only as text across a hashed boundary.
- **No order was transmitted.** 0 open orders, 0 trades, 0 positions and 0 fills
  after every session, enumerated from the broker rather than asserted, across
  **n = 9 sessions**.
- **No capital was authorized and no position was sized.**
- **The harness has still not reproduced a known answer**, so its MBT output
  would not be trusted. That remains the binding condition, and its reason is now
  a defect in this repository rather than a missing session.
