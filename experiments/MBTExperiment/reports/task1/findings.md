# Task 1 — the re-probe, and what reversed

**Two of the three named blockers cleared. A third was never named, and it binds
harder than either.**

## What Stage B could not measure, now measured

| measurement | Stage B | Stage B.1 | n |
|---|---|---|---|
| TCP reachability | 0 reachable, all ECONNREFUSED | **5 reachable** | n = 5 attempts |
| API handshake, distinct from the connect | `Absent(gateway_unreachable)` | **0.308 s** | n = 1 handshake |
| accounts read back | `Absent(gateway_unreachable)` | **1 account, D prefix, length 9** | n = 1 session |
| provenance guard verdict | not reachable | **declared paper, measured paper, agree** | n = 1 session |
| listed MBT option series | `Absent(gateway_unreachable)` | **11 series across 4 underlying futures** | n = 11 series |
| futures options permission, CME crypto | `Absent(gateway_unreachable)` | **`Absent(permission_unknown)`** | n = 1 attempt |
| real-time subscription, 3 legs | `Absent(gateway_unreachable)` | **not subscribed, all three** | n = 3 legs |

**A TCP connect proves a listener, not a session; a session proves a handshake,
not a subscription.** Each is recorded separately because each failed separately.

## The finding that binds: there is no real-time market data subscription

**Requesting real-time returned no touch on any of the three registered legs, at
n = 3 legs, with broker error 354, "Requested market data is not subscribed".**
Requesting delayed returned a touch on all three, at n = 3 legs, with error 10167,
"Displaying delayed market data".

| leg | real-time requested | delayed requested |
|---|---|---|
| `future_hedge` MBTU6 | no touch, `Absent(unquoted_leg)` | bid 81770.0 / ask 81785.0, **refused `delayed_tick`** |
| `option_call` | no touch, `Absent(unquoted_leg)` | bid 1625.0 / ask 1860.0, **refused `delayed_tick`** |
| `option_put` | no touch, `Absent(unquoted_leg)` | bid 6895.0 / ask 7200.0, **refused `delayed_tick`** |

**Zero of three legs are admissible under either request, so the census cannot
accept a single window.** Registered rule 3.4 refuses a delayed tick, and this
stage obeys it rather than widening a delayed spread into a cost band.

> **The refusals above are MEASURED refusals, not synthetic ones.** The delayed
> quotes are real touches from the venue that the registered rule then refused.
> Stage B could only demonstrate this guard on constructed inputs.

### A trap the harness walked into and now refuses

**The ticker reported `marketDataType = 1` while the feed served nothing.** The
status field said real-time and the subscription did not exist. Reading the
status alone would have recorded an unsubscribed leg as a real-time observation.

The registered check order saves this by accident of good design rather than by
foresight: structure is checked before delay, so a NaN touch is refused as
`unquoted_leg` before the status is ever consulted. `tests/test_marketdata.py`
now pins it deliberately, at n = 7 conversion cases.

## Permission is UNKNOWN, and that is not the same as absent

**`Absent(permission_unknown)` at n = 1 attempt.** The what-if built by this
package was not processed by the venue, so nothing was learned about permission.
The two states are not merged: one says the account may not, the other says
nobody successfully asked.

**This is not a terminal finding**, because the terminal condition registered for
Task 1 is permission *absent*, and permission was not found absent. The reason
the question went unanswered is a defect in this harness, recorded in
`reports/task1/harness_defects.md`, not a property of the account.

## Nothing was transmitted

**0 open orders, 0 trades, 0 positions and 0 fills after the probe**, enumerated
from the session rather than asserted.
