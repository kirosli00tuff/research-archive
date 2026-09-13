# TASK 0 — Orientation, the read-only boundary, and feasibility probes

Stage B, 2026-09-03 (UTC). Every figure below is measured. Machine-readable
evidence sits beside this file and under `reports/boundary/`.

---

## 0.1 Working directory, confirmed as the first action

```
/home/kiros-li/Documents/GitHub/MBTExperiment
```

The path contains no `/closed/` segment and carries no `_CLOSED_DO_NOT_RUN_HERE`
marker at its root. Both checks were run before any file was written.

## 0.2 The read-only boundary, resolved by marker rather than by assumed path

`VRPExperiment` was located by searching for the closure marker rather than by
assuming either registered path. It sits at
`/home/kiros-li/Documents/GitHub/VRPExperiment` and carries
`_CLOSED_DO_NOT_RUN_HERE`, so `stage_move_closed.sh` has not yet run. Nine other
repositories carry the same marker.

### Opening snapshot

| field | value |
|---|---|
| entries hashed | **2,901** |
| total bytes | **324,887,193** |
| **full digest** | `c28e68609cca2d968427ac4485fb836cf9f11a4df62cd89262388f3850789f81` |
| **stable digest** (115 entries, caches and `.git` and `.venv` excluded) | `441495bce9a7af16c250a8de865b6565b81ce3273ef9ae4207e254f2cc153641` |
| unreadable paths | **0** |
| elapsed | **0.974 s** |

Two digests are recorded rather than one. The full digest covers the root in
full as registered and moves if a build cache breathes. The stable digest covers
the 115 entries that are the sealed artifacts. A reader comparing snapshots can
therefore tell "a sealed artifact changed" apart from "a cache byte moved",
which one digest cannot express.

Artifacts: `reports/boundary/vrp_boundary_open.json`,
`reports/boundary/vrp_manifest_open.txt`.

## 0.3 IB Gateway reachability — **UNREACHABLE, measured**

| probe | result |
|---|---|
| host and port, from config | `127.0.0.1:4002`, the paper port |
| TCP connect attempts | **5** |
| attempts reaching a listener | **0 of 5** |
| refusal | `ECONNREFUSED` (errno 111) on every attempt |
| time to refusal | **0.012 ms to 0.113 ms**, n = 5 |
| listening sockets on 4001, 4002, 7496, 7497 | **none** |
| IB Gateway or TWS process | **none running** |

IB Gateway **is installed**: `~/Downloads/ibgateway` holds release **10.45**, and
`~/Jts/jts.ini` records `tradingMode=p`, `ApiOnly=true` and
`TrustedIPs=127.0.0.1`. So the paper configuration the operator intends is
present and the process is simply not up.

**No headless start path exists.** There is no IBC or IBController install on
this machine, so IB Gateway starts only through its GUI login dialog and an
interactive IBKR credential entry. **This session did not start it and cannot**:
it holds no IBKR credential, and starting a broker gateway with the operator's
stored credentials is not an action a coding session takes on its own.

Artifact: `reports/task0/gateway_reachability.json`.

### A second configuration gap, found by the same probe

`MBT_IB_PAPER_CLIENT_ID` is **empty** in `.env`. `CLAUDE.md` requires a distinct
client id per environment, from config, because TradingView and TWS competing
for one Gateway session starve each other. The paper account itself **is**
configured and carries the expected **D** prefix at 9 characters, which is the
paper shape the provenance guard checks. The number itself is never written into
an artifact; only its prefix and length are.

## 0.4 What the probes could not reach, each recorded as a typed absence

Every item below needs an API handshake. None is estimated, and none is inferred
from the installed configuration.

| Task 0 probe | state | reason |
|---|---|---|
| connection and handshake latency | `Absent(gateway_unreachable)` | no listener on the paper port |
| the account list the session returns | `Absent(gateway_unreachable)` | needs a session |
| **futures options permission on CME crypto products** | `Absent(gateway_unreachable)` | **needs a session. This is NOT a measured absence of permission.** |
| MBT option chain enumeration and its size | `Absent(gateway_unreachable)` | needs a session |
| market data subscription state, MBT option | `Absent(gateway_unreachable)` | needs a session |
| market data subscription state, MBT front future | `Absent(gateway_unreachable)` | needs a session |
| tick delay status: real-time, delayed or frozen | `Absent(gateway_unreachable)` | needs a session |

### The distinction that decides which terminal state this stage reaches

The stage instruction makes **absent futures-options permission on the account** a
terminal finding that stops the stage. **That is not what was measured.**
Permission was not found absent; it was **not measurable**, because no session
exists to ask. `Absent(gateway_unreachable)` and `Absent(no_permission)` are
different states and are not merged. The first says nothing about the account and
leaves the harness worth building. The second would say the harness has nothing
to point at.

Work therefore continues through the session-independent tasks rather than
stopping here, and every session-dependent figure is recorded absent with this
reason.

## 0.5 Broker API surface, measured rather than assumed

Measured against the locked environment, `ib_async 2.1.0`:

| fact | measurement |
|---|---|
| `IB.placeOrder(contract, order) -> Trade` | **transmits.** Takes no `whatIf` keyword at all |
| `Order.whatIf` | a **field on the order object**, not a call argument |
| `IB.whatIfOrder(contract, order) -> OrderState` | copies the order, sets `whatIf = True`, then calls `client.placeOrder` |
| `OrderState` fields | `initMarginBefore/Change/After`, `maintMarginBefore/Change/After`, `equityWithLoan*`, `commission`, `minCommission`, `maxCommission`, `commissionCurrency`, `warningText` |
| **an exchange or regulatory fee field on `OrderState`** | **none exists** |

This measurement changes the shape of Guard 1 and is recorded before the guard is
written rather than discovered by it. A `whatIf=True` keyword on `placeOrder`
would be **theatre**, because `placeOrder` does not read one and would transmit
anyway. The guard is therefore built to ban the transmitting call outright and to
require the literal where the flag genuinely lives. ADR-002 records this.

The absent `OrderState` fee field is the first evidence bearing on Task 6 and is
carried there rather than concluded here.

---

## 0.6 ETAs, stated before each task is armed

**Measured pace probes this stage rests on**, all taken above:

| probe | measurement |
|---|---|
| boundary hash, full root | **0.974 s** over 2,901 entries and 324.9 MB |
| `uv sync --group dev` | **1.272 s**, 40 packages |
| check cycle on the empty tree: ruff + mypy + pytest | **0.042 + 0.284 + 0.546 = 0.872 s** |
| TCP probe | **0.5 ms** per attempt, n = 5 |

**The consequence, stated because it decides how every ETA below is built: the
check cycle is under one second, so no task here is check-bound. Every ETA is
authoring-bound**, and rests on the authoring rate this session measured writing
`tools/boundary_hash.py` and `tools/probe_gateway.py` — two standalone modules of
about 130 lines each, both correct on the first run with no rework.

| task | ETA | derived from, with the assumption it rests on named |
|---|---|---|
| **0** | 20 min | the four probes above plus reading six VRPExperiment documents totalling 78 KB; **assumes** the boundary resolves on the first marker search, which it did |
| **1** | 70 min | ten package modules and three test modules at the measured ~130-line, one-cycle authoring rate, plus five refusal artifacts; **assumes** the guard modules are comparable in size to the two probes already written and need no rework |
| **2** | 30 min | one document section, no code; **assumes** every figure is transcribed from the VRPExperiment documents already read and none is re-derived |
| **3** | 40 min | the same, plus four implementer rules that must be fixed rather than transcribed; **assumes** fixing a rule costs about twice transcribing one |
| **4** | **SKIPPED — blocked.** | no session exists. Recorded absent, not estimated |
| **5** | **clock-bound, see below** | not effort-bound and not compressible |
| **6** | 15 min | one determination from the `OrderState` surface already measured in 0.5 |
| **7** | 20 min | gate firing over recorded figures, offline |
| **8** | 35 min | five mutations at the measured cycle, each applied to real source and restored |
| **9** | 40 min | four documents plus the closing boundary re-hash at its measured 0.974 s |

### Task 5 is clock-bound and states its date

The census cannot be compressed. Under the window-distinctness rule registered in
Task 3 — **at least 60 minutes between windows and at most 4 windows from any one
UTC calendar day** — reaching the registered minimum of **20 distinct windows**
needs **at least 5 collection days**.

**Had collection been able to begin on 2026-09-03 (Thursday, UTC)**, the five
CME crypto trading days would be **2026-09-03, 09-04, 09-07, 09-08 and 09-09**,
skipping the 09-05 and 09-06 weekend, and the census would complete on
**2026-09-09**.

**It cannot begin.** The Gateway is unreachable, so **0 of 20 windows are
collected** and the projected completion date runs from the first day a session
exists, not from today. The rule fixes the duration at 5 trading days; it does
not fix the start.
