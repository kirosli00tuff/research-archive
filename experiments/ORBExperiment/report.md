# report.md — ORBExperiment, stage by stage

Each section is written for the moment it landed and is not revised afterwards.
A later correction is a new line, never an edit.

---

## Stage A.1 — access

**2026-08-29.** Nine vendors, terms first.

**Standing rule 12 was executed before any repeated fetch**: `robots.txt` was
recorded verbatim for **n = 15 hosts**, and the access verdict routed from what
those files say rather than from what the vendors sell.

**The finding is the split, and the split is on terms rather than on price.**

- **`stooq.com` and `query1.finance.yahoo.com` — the only two hosts serving US
  equity data without a credential — both publish `User-agent: * / Disallow:
  /`.** Standing rule 12 is not advisory. Neither is fetched again.
  `finance.yahoo.com` additionally names **`ClaudeBot`, `anthropic-ai`,
  `Claude-Web`, `GPTBot`, `CCBot`, `Scrapy`** and 30 others in a group carrying
  `Disallow: /`.
- **`eodhd.com` disallows `/api/`** and **`data.nasdaq.com` disallows
  `/api/*.json*` and `/api/*.csv*`** — the exact paths a collector needs.
- **The five whose terms permit collection all refused without a credential**,
  n = 7 probes: Polygon **401 `"API Key was not provided"`**, Alpaca **401**,
  Databento **401 `"Not authenticated"`**, Tiingo **403 `"Please supply a
  token"`**, Alpha Vantage **200 carrying a refusal**.

**0 of 9 vendors serve a bar to this repository.** That falsifies the operator
prompt's assumption that *"no key is needed for any Stage A source"*, and it is
recorded as falsified rather than worked around — the NPLExperiment correction,
where a planning figure near 9.4 events per month met measurement at **0.5, n = 3
over 182 days**.

**Two findings inside the finding.** `polygon.io` **301-redirects to
`massive.com`** — the prompt's "also branded Massive", measured rather than
assumed. And `alpaca.markets/robots.txt` returns **200 with 81,041 bytes of
HTML**, a styled 404 page: **a 200 is not a robots.txt**, and it is recorded as
"none served".

**Alpha Vantage refuses with HTTP 200.** The demo key returns `200` with an
`Information` string and no series; the delisted query returns a **2-byte `{}`**,
also at `200`. **This is the exact health/composition merge Guard 4 exists to
prevent**, and it caught this repository's own client: `PacedClient` labelled the
refusal `stored`. Recorded as ADR-008; the body-aware classifier lives in
`orb.collector.classify`.

**One request is on the record and is not excused by this section.** The
connectivity probe of Entry 0a sent one GET to `stooq.com` **before** any
`robots.txt` had been recorded — exactly the ordering standing rule 12 exists to
prevent. It is recorded, it is not repeated, and it is why the rule is ordered
the way it is.

---

## Stage A.1 — rate ceilings

**2026-08-29.** **n = 18 requests, 3 endpoint-spacing cells, 0 refusals on a
limit.** Polygon admitted **8 of 8 at 88.4/min**; Alpha Vantage **5 of 5 at
29.1/min**.

**None of this licenses a pace.** solattn ADR-021's corollary applies to this
repository's own measurement: **the only reachable path on every permitted vendor
is the unauthenticated refusal path, and a ceiling measured on a 401 is not
evidence about the authenticated data endpoint.** Polygon documents 5/min; the
measured 88/min **does not contradict it**, because they are different endpoints.
Pacing is registered **provisionally and labelled unmeasured** at the
conservative 6.0 s default (Amendment 2).

---

## Stage A.1 — revision, agreement and delisted coverage

**2026-08-29. Not measured. `Absent(not_yet_measured)` on all three.**

**These are the two tasks this repository turns on**, and both are blocked on an
operator item rather than on a design question. **No figure is invented and no
zero is written**: `orb.absence.Absent` refuses `float()`, `int()`, addition in
both directions, ordering and truth-testing, so not one of these cells can be
summed into a coverage figure by accident.

**What was built instead, and armed.** `orb.comparator.SealedComparator` compares
in **integer cents** — float equality on money is a bug — and returns **only**
counts-only findings records. It is pinned four ways: an AST walk over every
public method's return annotation; a field-type walk over both records; a runtime
check that the returned object holds the fixture's own opening-range high in
**neither dollars nor cents**; and an assertion that `seal.py` reads no priced
field while `comparator.py` does.

**Known answers, hand-computed.** One revised bar in five measures **exactly
0.20** and fires FAIL; an unchanged re-pull measures **0.0** and fires PASS; a
one-cent disagreement **inside** the opening range breaks the pair while one
**outside** it does not; a bar stamped **exactly at 09:35:00.000** is outside the
half-open range; and a clean re-pull taken at **13 days** reports
`wait_satisfied() == False` — **a re-pull taken too early is not evidence of a
clean vendor.**

**Guard 5 had a hole and the comparator found it.** The comparator reads OHLC
through a variable alias, and a constant-subscript walk reported **zero reads
from a module that reads every priced field on every bar**. The guard was
widened, not the test relaxed: a fourth detection form was added, the field
registry moved to `orb/fields.py` so the declaration site does not flag itself,
and findings are deduplicated by `(line, field)`.

---

## Stage A.2 — the session calendar and the corporate-actions substrate

**2026-08-29.** **2,637 sessions and 21 half sessions**, 2016-01-04 to
2026-06-30, from the NYSE rules encoded in `orb.calendar` rather than downloaded.

**Two disagreements with the registration, recorded not reconciled.** In-sample
computes **1,762** against a stated ~1,760; the holdout computes **875** against
a stated ~880. The holdout shortfall is carried into the power gate and **the
computation wins**: `t` moves from 2.616 at n = 880 to **2.609 at n = 875**, and
**no verdict row moves.**

**The second-source cross-check was not completed and was not fabricated.** Every
vendor serving a machine-readable calendar is one of the nine that refused.
Writing a comparison table from recollection would be recording a **documented**
figure as a **measured** one — the failure standing rule 4 names. Recorded
`Absent`.

**What stands in is real.** The session count is derived **twice by different
arithmetic** and the two agree on all **10** complete years; worked by hand for
2018, **261 weekdays − 10 weekday closures = 251**. And the opening-range start
of the **first in-sample session equals `CONFIG.pre_period_end_ms` exactly** — the
calendar and the carve-out boundary, computed two independent ways.

**The actions substrate is built and unpopulated.** `Absent`, no zero written: a
zero that was measured and a zero that was never looked for are different facts.

---

## Stage A.2 — cost verification

**2026-08-29. The MLCryptoEngine ADR-055 pattern firing exactly as designed.**

Live against IBKR's published schedule, **HTTP 200, 584,282 bytes**, terms
checked first. **`www.sec.gov/robots.txt` returned HTTP 403 "Request Rate
Threshold Exceeded" on both attempts, 20 s apart** — recorded as a state, read
neither as permission nor as prohibition.

**Commission 0.0035/share and the 0.35 order minimum agree with carried. The
FINRA TAF rate does not: carried 0.000166, measured 0.000195 — the carried figure
is 14.9 percent low.** And **three components were not modeled at all**: the
**1 percent maximum per order**, the **FINRA CAT fee at 0.000003/share**, and
**NSCC/DTC clearing at 0.00020/share**. All three make the model **more
expensive**.

**The 1 percent cap can bind below the 0.35 minimum**, and the minimum does not
survive it: 10 shares at 1.00 USD is a 10.00 USD trade whose cap is **0.10**.

**The SEC fee schedule is registered empty on purpose.** One rate was measured;
**its effective date was not.** Placing the 2026 rate in the schedule would
silently apply it to a 2016 session, so `rate_on` returns `Absent` for **every
session in the registered window** and the whole round-trip cost refuses. **The
model will not price a trade it cannot price honestly.**

**What it costs the hypothesis, measured.** At the central band on a 50 USD name:
**≈ 0.0386 USD/share on a close exit, ≈ 0.0686 on a stop exit**, against the
replication's measured gross edge of **0.070**. **A close exit consumes 55
percent of the edge; a stop exit consumes 98 percent. Slippage is 78 percent of
the close-exit total.** Section 6's claim that the cost band is the experiment's
second axis is now a number.

Frozen `3789221b9dd3fea5a9680547dfdf8ec7b1febaf246042fe1fa70e27ca610fba3`,
latched, and pinned by a test that recomputes it. **Amendment 3**, written before
A.2 TASK 4.

---

## Stage A.2 — power

**2026-08-29. The registered expectation was recorded before the evidence, and
the evidence matched it.**

| assumption | annual Sharpe | **E1 power at n = 875** | verdict against the floors |
|---|---:|---:|---|
| published (undecayed) | 2.81 | **0.9995** | above the 0.80 GO floor |
| **REGISTERED (half)** | **1.40** | **0.7435** | **below the 0.80 GO floor** |
| quartered | 0.70 | **0.2578** | below the 0.50 BLOCKED floor |

That is the DEGRADED clause **word for word**: *E1 reaches at least 80 percent
power at the published magnitude but under 80 percent at the registered
assumption.*

**Minimum N at the registered assumption is 1,006 against 875 achieved — a
shortfall of 131 sessions.** And a knife-edge recorded exactly: extending to
**2026-12-31** gives **1,003 sessions and power 0.7991**, short of 0.80 by
**0.0009** and short of the required count by **three trading days**. 2027-06-30
gives 1,126 and **0.8425**. **Recorded while this repository holds no result that
would make the extension tempting.**

**Two disagreements with the prompt, the computation winning as Section 9
requires.** Minimum N for t = 2.0 is **515, not 514** (at 514 the statistic is
**1.9994**); for t = 3.0 it is **1,158, not 1,157** (at 1,157 it is **2.9998**).
The prompt states floors; a minimum-N ceilings. One session each, conservative.

**And one prompt figure turned out to contain an assumption.** The stated
per-trade information ratio "near 0.031" corresponds to a **53.5 percent trigger
rate** — and the prompt itself says the trigger rate is *"to be measured rather
than assumed."* At a 100 percent trigger rate the figure is **0.0227**.

**E2 power is `Absent` in all nine cells.**

---

## Stage A.2 — the Section 0 verdict

**2026-08-29.**

> ## **PENDING_ACCESS** · `PENDING-ACCESS Amendment 1`

**Nothing is armed. Nothing is closed. H1 remains OPEN.**

It is explicitly **not** the `source-integrity-blocked` closure kind: that
requires a vendor whose bars were **measured** and found unstable, and **no bar
has been served to fail.**

**The counterfactual is computed and recorded: had bar integrity passed in full,
the same power inputs fire `DEGRADED`.** Section 0 predicted DEGRADED **in
writing, before any measurement existed**, and the computation confirms it by the
precise mechanism the clause names. **That is the only circumstance in which a
DEGRADED reads as a documented answer rather than a disappointment**, and Section
0 said so in advance.

Inputs recorded beside the verdict, each with its n, in Amendment 4, in
`HYPOTHESES.md`, and in the append-only ledger.

---

## Stage C — the in-sample read

*Reserved. **This section is written once, and only after the Stage C latch
exists.** It is empty because the latch does not exist and the window is
unspent.*

---

## Stage D — the holdout read

*Reserved. **This section is written once, and only after the Stage D latch
exists.** It is empty because the latch does not exist and the window is
unspent.*
