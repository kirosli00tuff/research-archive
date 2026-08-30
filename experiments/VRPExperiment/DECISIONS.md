# DECISIONS — VRPExperiment

Numbered architecture decision records. Each records what was decided, the
context that forced it, and the consequence. **None is edited in place.**

---

## ADR-001: Cost and reachability fields are readable; only the premium is blind

**Date:** 2026-08-30 · **Status:** accepted

**Context.** The blindness pin must refuse "any read of an implied or realized
volatility value, option price or premium outside a sealed writer". Applied
naively that would also blind bid, ask, margin and commission — which are the
two *deciding* measurements of TASK 3 and TASK 5.

**Decision.** `BLIND_FIELDS` holds 38 names covering implied volatility,
realized volatility, option price and premium. `READABLE_FIELDS` holds 40
covering contract specification, margin, commission, **bid, ask, half-spread**,
policy text and operational metadata. The two sets are asserted disjoint at
import.

**Consequence.** A **spread** is a cost and is readable; a **level** is a
premium and is not. `tools/measure_spreads.py` therefore emits only
differences — spread, half-spread, half-spread as a fraction of notional — and
never a mid or a mark. Cost as a *fraction of premium collected* could not be
computed at TASK 5 and was deferred to TASK 6, which is the correct consequence
rather than a workaround.

---

## ADR-002: The `open()` guard is narrowed to text handles, and the narrowing is stated

**Date:** 2026-08-30 · **Status:** accepted

**Context.** The guard forbidding file handles outside the seal **fired on
`vrp/ledger.py:74`** on its first run against a real module — an `os.open` call
that is the only way Guard 3 obtains `O_APPEND` plus `fsync`.

**Decision.** Exempt `os.open` and `os.fdopen`; keep builtin `open` and
`Path.open` forbidden. A canary test plants all three and asserts exactly the
first two are caught.

**Consequence.** The exemption is narrow and reasoned rather than broad and
convenient. That the guard fired on a real module on its first run is the
evidence it binds on more than fixtures, and is recorded as such.

---

## ADR-003: A venue's own refusal binds, and is obeyed rather than routed around

**Date:** 2026-08-30 · **Status:** accepted

**Context.** CME Group returned **HTTP 403** with, verbatim: *"This IP address is
blocked due to suspected web scraping activity… strictly prohibited by CME
Group's website Data Terms of Use."*

**Decision.** All fetching of `cmegroup.com` stopped on receipt. No user-agent
rotation, no proxy, no retry loop, no third-party mirror substituted. Every
CME-sourced figure is recorded `Absent(not_served)` with the refusal verbatim.

**Consequence.** The exchange-fee leg of the cost model is permanently absent to
this repository, and the all-in cost cannot be completed. **That is a smaller
loss than the alternative**: a figure obtained by working around the refusal
would be a measurement of somebody's copy of the schedule, not of the schedule.
It also means every cost figure here is a **lower bound**, which turned out to
be sufficient to decide MET and insufficient to decide MBT — an asymmetry that
is the shape of the closure.

---

## ADR-004: `UNCLEAR` is never read as permission, and `CAPITAL_BLOCKED` is a distinct state

**Date:** 2026-08-30 · **Status:** accepted

**Context.** A venue can fail to be usable in four different ways, and collapsing
them would destroy the finding.

**Decision.** Five venue states, disjoint from the five operational health
states, with no arithmetic between the families: `PERMITTED`, `PROHIBITED`,
`CAPITAL_BLOCKED`, `UNCLEAR`, `NO_PRODUCT`. `CallStateTally.combined_total()`
raises structurally.

**Consequence.** The artifact distinguishes Deribit (**prohibited**, a
jurisdiction fact) from full-size CME (**capital-blocked**, an arithmetic fact)
from Hyperliquid (**no product**, an inventory fact) from MET
(**cost-exceeded**, a measured fact). A **403 status code is `ACCESS_REFUSED`,
an operational fact, and can never become a jurisdiction finding** — those come
only from published policy text.

---

## ADR-005: The observation instant is 08:00 UTC, forced by a measured misalignment

**Date:** 2026-08-30 · **Status:** accepted

**Context.** Section 2.5 registered "a fixed UTC instant… fixed at the first read
and never moved". Probing timestamps only, before the latch:
`get_volatility_index_data` at `resolution=1D` stamps buckets at **00:00 UTC**;
`get_tradingview_chart_data` at `resolution=1D` stamps **08:00 UTC**. Pairing
them at daily resolution would have offset the implied leg from the realized leg
by **eight hours on every one of ~1,900 observations**, silently.

**Decision.** Both series are fetched **hourly** and filtered to **08:00 UTC**.

**Consequence.** The instant is also correct on the merits rather than merely
convenient: **08:00 UTC is Deribit's option settlement time**, measured on the
live series in TASK 5, so a 30-day tenor runs 08:00 → 08:00 — exactly the
interval an option spans. The standing rule that "option expiries carry their
exchange settlement time" is satisfied by construction rather than by assertion.

---

## ADR-006: The rebalance count is computed inside the sealed read, not at TASK 5

**Date:** 2026-08-30 · **Status:** accepted

**Context.** TASK 5 must report "the number of rebalances a registered hedging
rule would require, with the cost of each". A straddle's delta is `2·N(d₁) − 1`
and `d₁` requires σ — **an implied volatility, a blind field**.

**Decision.** TASK 5 measures the **price per rebalance**; TASK 6 measures the
**count**, inside `src/vrp/sealed_read.py`; the two multiply only after the
latch is spent.

**Consequence.** Computing the count at TASK 5 would have required reading an
implied volatility before the latch — precisely what the blindness pin exists to
prevent. The decomposition is recorded rather than assumed, so a reader can see
that the deferral is structural and not an omission.

---

## ADR-007: An aborted sealed read keeps its latch; the correction is amended, never erased

**Date:** 2026-08-30 · **Status:** accepted

**Context.** TASK 6 attempt 1 wrote its latch and then failed on its first
underlying-leg request with HTTP 400 — `{"reason":"unsupported resolution"}`.
Cause: `get_volatility_index_data` takes `resolution` in **seconds**,
`get_tradingview_chart_data` in **minutes**; the same literal `60` means one
minute on one and one hour on the other. No estimator ran; no result file was
written; `data/raw/task6/` was empty; the only output was a traceback.

**Decision.** `reports/task6/task6.latch.json` is **kept permanently** as the
record that a read was begun and aborted. Attempt 2 writes a separately named
latch. `REGISTRATION.md` **Amendment 1** records the failure, the diagnosis, the
four checkable facts establishing no outcome was observed, and — explicitly —
what the dishonest alternative would have been.

**Consequence.** The registration's protection is intact: the only change
between attempts is **one string literal** in a request parameter. No estimator,
window, tenor, sign convention or inference rule was touched, and the diff is
auditable in the commit preceding attempt 2. **Deleting the first latch would
have left no trace that a read had been begun**, which is exactly the quiet
rewrite the latch exists to make impossible.

---

## ADR-008: Deribit's spread is measured as a labelled reference and never substituted

**Date:** 2026-08-30 · **Status:** accepted

**Context.** The bid-ask on the permitted instruments is `Absent(not_served)`.
Deribit's is freely measurable — and Deribit is prohibited.

**Decision.** Measure it, label it **REFERENCE ONLY, not a cost input**, and let
no verdict read it.

**Consequence.** This is the ORBExperiment lesson applied in advance rather than
in hindsight: a band carried from a different instrument understated **five of
six legs** and produced a shift **11.27× too small**, while *over*stating a
sixth — so "assume worse" would not have rescued it either. The reference still
earns its place, because it supports one claim that needs no substitution:
**the commission alone on the affordable permitted route exceeds the entire
quoted spread on the prohibited one.**

---

## ADR-009: A revision test compares data, not responses

**Date:** 2026-08-30 · **Status:** accepted

**Context.** The first revision check reported that a fixed, closed historical
window had **changed** between two fetches five seconds apart. It had not:
Deribit's JSON-RPC envelope carries `usIn`, `usOut` and `usDiff` server-timing
fields that change on every call. The 169 data rows were byte-identical.

**Decision.** Revision is tested on the SHA-256 of the canonicalised
`result.data` array alone. Six baselines were recorded and re-checked after
≈ 70 minutes: **all six identical**.

**Consequence.** A whole-response digest is the wrong instrument for this
question and **would have reported a revision that did not happen** — the exact
false alarm that would have disqualified the only usable history in the survey.
Recorded because the mistake is easy and its consequence is a wrong closure.

---

## ADR-010: The premium is the endpoint because a strategy Sharpe is unmeasurable here

**Date:** 2026-08-30 · **Status:** accepted

**Context.** Registered in Section 7 before any data: a strategy-Sharpe endpoint
of **1.32 annualised** needs ≈ **119 weekly observations** to reach t = 2, and
≈ **478** at the halved 0.66 required by McLean and Pontiff — **more than nine
years**.

**Decision.** The endpoint is the **premium**, a per-observation quantity with
daily sampling, not a strategy return.

**Consequence.** The design reached **n = 1,955** on each asset and detected the
BTC premium at **t = 5.888**. It also means the artifact must say loudly what it
does not establish: **a premium is not a return**, no sleeve was simulated, and
the tail — which is the entire risk a variance seller bears — is unmeasured.

---

## ADR-011: Notional decides everything, and it decided this

**Date:** 2026-08-30 · **Status:** accepted

**Context.** MLCryptoEngine ADR-023 recorded that CME's per-contract fees make
cost in basis points a function of notional, so the same $2 ticket lands
anywhere from 0.4 to 102 bps. That was recorded as a curiosity about a venue
table.

**Decision.** Record it here as **the binding constraint of this experiment**.

**Consequence.** The two permitted routes differ by **7.48× in commission
basis points** — MET **32.571 bps** against MBT **4.352 bps** per straddle round
trip — **entirely because MET's notional is 31.8× smaller**. And the direction is
adverse: **the only contract small enough for a $1,000 sleeve to certainly hold
is the one whose commission exceeds the premium it would harvest.** The prior in
Section 9.1 anticipated a capital problem on MBT and got the asset right and the
mechanism backwards.
