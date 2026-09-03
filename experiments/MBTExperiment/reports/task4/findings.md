# TASK 4 — The paper harness, and why it produced no margin figure

**Outcome: BLOCKED. No what-if preview ran, no margin was read, and the
known-answer test did not execute.** Every figure this task exists to produce is
recorded as a typed absence carrying its reason. None is estimated.

---

## 4.1 The two blockers, in the order the harness hit them

The harness fails closed in a registered order, and it reached the **first**
blocker before the second. Both are recorded because fixing only one leaves the
task blocked.

### Blocker 1 — `MBT_IB_PAPER_CLIENT_ID` is unset

`GatewayConfig.load` refused **before a socket was opened**, with:

> `MBT_IB_PAPER_CLIENT_ID is unset or empty. Set it in .env, copying the shape
> from .env.example. This repository holds no default for it, because a default
> account number or a default port is how a session ends up somewhere nobody
> chose.`

`CLAUDE.md` requires a distinct client id per environment, from config, because
TradingView and TWS competing for one Gateway session starve each other. The
value is an operator choice and this repository holds no default for it.

Artifact: `reports/task0/probe_session.json`, stage `config`.

### Blocker 2 — IB Gateway is not running

Measured three times across this stage, **13 TCP connect attempts in total, 0
reaching a listener**, `ECONNREFUSED` on every one.

| probe | attempts | reachable | refusal |
|---|---|---|---|
| Task 0, opening | 5 | **0** | ECONNREFUSED, 0.012–0.113 ms |
| Task 4, recheck | 3 | **0** | ECONNREFUSED |
| Task 4, port and process scan | — | **0** | no listener on 4001 or 4002, no `ibgateway`, `jts` or `tws` process |

Release **10.45** is installed at `~/Downloads/ibgateway` and `~/Jts/jts.ini`
records `tradingMode=p`, `ApiOnly=true` and `TrustedIPs=127.0.0.1`, so the paper
configuration the operator intends is present. The process is simply not up, and
**no IBC or IBController exists on this machine**, so IB Gateway starts only
through its GUI login dialog and an interactive IBKR credential entry.

**This session did not start it and cannot.** It holds no IBKR credential, and
starting a broker gateway with the operator's stored credentials is not an action
a coding session takes on its own.

## 4.2 What this task was to produce, and what each is instead

| deliverable | state | reason |
|---|---|---|
| connect on the paper port | `Absent(gateway_unreachable)` | 0 of 13 attempts reached a listener |
| resolve the ATM 30-day MBT straddle from the live chain | `Absent(gateway_unreachable)` | needs a chain enumeration |
| what-if preview: initial margin change | `Absent(gateway_unreachable)` | needs a session |
| what-if preview: maintenance margin change | `Absent(gateway_unreachable)` | needs a session |
| what-if preview: commission estimate | `Absent(gateway_unreachable)` | needs a session |
| **known-answer test on a liquid product** | **`Absent(gateway_unreachable)`, and additionally `Absent(not_served)` on its expected value** | see 4.4 |

**No figure produced by this task is admissible to any gate**, and that holds
whether or not it ran. `tests/test_guards.py` pins it: a paper-tagged margin fed
to the MARGIN gate raises `PaperFigureInadmissibleError`, and the refusal is
recorded in `reports/guards/refusals.json` rather than asserted here.

## 4.3 The harness is built and its code path is exercised

Being blocked on a session is not the same as being unbuilt. The following are
implemented, type-checked under mypy strict, and exercised by tests against a
stub implementing the `Session` and `WhatIfBroker` protocols:

- `mbt.session.probe` — connect, read the account back, build measured provenance
- `mbt.chain.resolve_straddle` — both registered selection rules
- `mbt.broker.what_if_order` — the only broker order path in the package
- `mbt.broker.MarginPreview.from_order_state` — parses the preview
- `mbt.whatif.known_answer_check` — the comparison, with its absence handling

**One parsing decision is worth naming, because it is a trap.** IBKR returns the
margin fields as **strings**, and serves `1.7976931348623157E308` for "not
computed". Parsing that to a float yields a finite-looking number of order 1e308
that every later comparison would treat as an enormous but real margin, and every
ceiling test would then fail for the wrong reason. `MarginPreview` keeps the
fields as strings and `mbt.whatif.margin_from_preview` maps the sentinel to
`Absent(not_served)`.

## 4.4 The known-answer test, and where its expected value comes from

**A new path reproduces a previously measured answer before its output is
trusted.** The check is implemented and it did not run, so **the code path has
not been checked against a known answer and its MBT output would not be
trusted even if a session existed.** That is recorded as an absence, not as a
pass.

**The expected value is an operator input, and this is a design decision rather
than an omission.** CME refused automated access to its margin schedule, citing
its own Data Terms of Use. VRPExperiment obeyed that refusal and this repository
obeys it too. The known answer is therefore read by a **person** from the IBKR
client portal or CME's published schedule and supplied through the environment.
This repository does not scrape it, does not infer it from a third party, and
does not carry one from another repository.

With no operator value supplied, `known_answer_check` returns `agrees=False`
carrying the detail *"no operator-supplied expected margin, so the code path has
not been checked against a known answer and its MBT output is not trusted. This
is an absence, not a pass."*

## 4.5 Does the what-if commission estimate include exchange and regulatory fees?

**Answered by measurement, on the API surface, and the answer is NO — there is no
field for them at all.**

Measured against the locked `ib_async 2.1.0`, `OrderState` carries exactly these
fields:

```
status, initMarginBefore, maintMarginBefore, equityWithLoanBefore,
initMarginChange, maintMarginChange, equityWithLoanChange,
initMarginAfter, maintMarginAfter, equityWithLoanAfter,
commission, minCommission, maxCommission, commissionCurrency,
warningText, completedTime, completedStatus
```

**There is one commission triple and no exchange or regulatory fee field.** So
the question "does the estimate include them?" has a structural answer before any
session exists: **the response carries no place to report them separately.**

**What this does NOT establish**, stated because it is easy to overread. The
absence of a field does not prove the absence of the fee from the `commission`
number. It proves only that the response cannot distinguish them. Whether the
scalar `commission` is fee-inclusive is a question about **the paper
environment's simulator**, and answering it needs a session. It is carried to
Task 6 as `Absent(gateway_unreachable)` on that narrower question, and Task 6
records the leg itself as absent for a separate and stronger reason.

`MarginPreview.as_row` emits an explicit
`exchange_and_regulatory_fee: "absent: OrderState carries no such field..."` line
rather than omitting the key, so a downstream reader meets the absence rather
than missing it.

## 4.6 What unblocks this task

Both, in order, and neither is a code change:

1. **Set `MBT_IB_PAPER_CLIENT_ID` in `.env`** to a client id distinct from the
   one TradingView or TWS uses.
2. **Start IB Gateway in paper mode** and log in interactively.

Then `make b-probe` re-runs the whole probe and overwrites
`reports/task0/probe_session.json` with a measured result. The harness needs no
edit to accept a session that appears.
