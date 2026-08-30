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

---

# The A.1 resumption — written for the moment it landed, 2026-08-29

**Two credentials arrived and the access verdict changed. Nothing else did.**

Section 0 had fired `PENDING_ACCESS` earlier the same day on **0 of 9 vendors
serving a bar**. Twelve tasks later it re-fired **`PENDING_REVISION`**, and the
distance between those two verdicts is the whole content of this section.

## What was believed on documented grounds, and what measurement did to it

**Three claims went in. Two came out falsified, and the third came out narrower
than it went in.**

**`docs/ACCESS.md` recommended Massive as the primary vendor** — *"the only
probed vendor that publishes a documented delisted-ticker reference endpoint and
minute aggregates on one host."* Every word of that reasoning is **documented**,
and it was the best available reasoning at the time. **The bisection measured
Massive's earliest served session at 2024-08-29: 0 of 1,762 in-sample sessions.**
The recommendation is not adjusted; it is **superseded by ADR-023**, and the
section that made it is left standing so a reader can see the shape of the
error — **a vendor chosen on what it publishes rather than on what it serves.**

**`CLAUDE.md` rule 3 said no API key exists anywhere in this project and none is
needed.** The first half still holds and is unweakened. The second half was
**falsified by measurement** and is amended in place with the original quoted and
struck through, so the gap between assumption and measurement is readable without
a git log.

**Amendment 2 said the 88.4 requests per minute measured against a 401 was
evidence about the refusal path and nothing more.** That was a prediction, and
this resumption tested it: **the authenticated path refuses at 5 per minute.**
The unauthenticated figure overstated the real ceiling by **17.7×**. An operator
pacing from it would have been **refused on 3 of every 8 requests**. The
prediction held in the direction that costs something rather than the direction
that flatters.

## What the measurements say

**Access, `n = 11` probes.** Both credentials authenticate. Massive's `403` on a
2015 request is an **entitlement** refusal, not an authentication failure —
separating those took a second probe round rather than an inference, and a recent
aggregate returned **861 bars**. Alpaca's `401` on the live trading host is a
**key-family** fact: these are **paper-account keys**, which is the correct shape
for a market-data-only use.

**Tape, `n = 100` session-ticker pairs.** Massive against Alpaca-SIP is
**`SAME_TAPE`** at a median first-5-minute volume ratio of **1.005197**. The
registered agreement thresholds apply as written.

**The controls are why that number is evidence rather than an assertion.**
Massive against Alpaca-IEX separated at **0.027856**; Alpaca-SIP against
Alpaca-IEX — **same vendor, same host, same request, one parameter changed** —
separated at **0.027761**. That second control removes every explanation for a
separation that is not the tape, **including this repository's own window
arithmetic**.

**Reach, `n = 32` probes over `n = 5,934` candidate sessions.** Alpaca's earliest
served session is **2016-01-04** and Massive's is **2024-08-29**. Both boundaries
were confirmed by probing the sessions either side.

**Delisted coverage, `n = 229` in-window names checked.** **203 served intraday
bars** for a session before the delisting — **`PASS`** against a registered bar of
100. **4,731** delisted names carry a delisting date inside the registered
window.

**Rate ceilings, `n = 53` requests.** Massive refuses at **5 per minute**, first
refusal at request **6 of 8** on **both** endpoints measured separately. Alpaca's
ceiling was **not reached**: 25 of 25 admitted at 134.05 per minute.

## Three numbers that are exactly what they look like

**Massive's earliest served session is 2024-08-29 and today is 2026-08-29.** A
rolling twenty-four-month window, measured to the day.

**Alpaca's earliest served session is 2016-01-04 — the exact first session of the
registered in-sample window.** The registration took that date from the source
study; Alpaca's history begins there independently. **The in-sample window is
therefore covered with zero margin.** One trimmed month of vendor history, or one
session moved earlier in the registration, and the coverage is gone. **This is
not a comfortable pass. It is an exact one, and calling it comfortable would be
the first step toward being surprised by it.**

**Alpaca-SIP reports more first-5-minute volume than Massive in 100 of 100
pairs**, with a **minimum ratio of 1.000905 — strictly above 1.0**. Noise
straddles 1.0. This does not, in a hundred consecutive observations. The
magnitude is about half a percent and the verdict is unaffected; **the direction
is the finding**, and it is left open rather than explained away.

## The thing that will not be hurried

**The two feeds share an upstream.** The evidence is not the level of agreement
but its **tightness**: an interquartile range **0.46 percentage points wide over
100 pairs**. Two independently constructed consolidations of US equity activity
do not agree that closely that consistently; **one SIP-derived upstream,
redistributed twice, does.**

**So the cross-vendor agreement gate — the one registered because of Concretum —
cannot run the Concretum test on this pair.** Concretum's **226,000 to 726,000
USD** spread came from **four vendors**, and it is a spread **across upstreams**.
Measuring agreement between two redistributors of one upstream cannot detect it.

**That is registered before the agreement figure exists**, which is the only time
such a statement is worth anything. Written afterwards it is an excuse; written
now it is a scope limit. And it **compounds** with the reach finding: the two
feeds overlap only from **2024-08-29**, so the gate covers **459 of 875 holdout
sessions and none of the 1,762 in-sample sessions**. **Together, the gate as it
can actually be run establishes that two redistributors of one upstream agree, on
459 of 2,637 registered sessions.**

## Where it stopped, and why that is the right place

**The probe slice is sealed: 480 files, 737,507 bars, 2,400 session-ticker
pairs, `HTTP 200` on every one.** The identical re-pull is eligible on
**2026-09-12** and `tools/repull_probe.py` refuses, loudly, until then — exit
**78**, naming the date, having sent nothing.

**The wait is the measurement.** A re-pull sent early does not produce a *weaker*
revision figure; it produces a **wrong** one, biased toward zero — **and zero is
the shape of a `PASS`**. MLCryptoEngine H11 died on a **measured 75-day
publication lag** in a source that regenerated whole files and revised past rows,
and **that lag was discovered rather than registered.** Here the clock was
started deliberately, its earliest eligible date was written down before any
re-pull was possible, and the refusal before that date is enforced in code.

**`PENDING_REVISION` is a parked outcome, not a failure.** It is a separate state
from `PENDING_ACCESS` for one reason: **the two have completely different next
actions. One needs a credential. The other needs a calendar.** Collapsing them
would have made the map report *"we cannot reach a vendor"* on a day this
repository holds 737,507 sealed bars from one.

**Nothing is armed.** `systemctl --user list-timers` shows **0 `orb-` units**.
The collector and the watcher stay inert until a revision verdict exists.

## One deviation, recorded rather than smoothed

**The first credentialed probe round recorded served response bodies as well as
refusals, and three of those fragments contained OHLCV values.** Under the
blindness field lists, a report file is not a sealed writer.

**Guard 5 cannot catch this class**, and that is the part worth keeping: it walks
parse trees for **field names in source**, and a value that only ever exists
inside a runtime string is invisible to it. **A structural guard has a shape, and
this leak was outside it.**

The sessions touched were **2015-06-01**, which served nothing on either vendor,
and **2026-07-15**, which is **after `holdout_end` = 2026-06-30** and therefore
outside both registered windows. **No bar from either registered window was read
or recorded.** The reports were rewritten before the commit, and the policy is now
**code rather than care**: a refusal is recorded verbatim, a served payload is not
recorded at all, and the asymmetry runs on **status code**, which is itself a
readable field.

## What a reader should take from this section

**Access was the cheap problem and it is solved.** Two credentials, one primary
that reaches every registered session, delisted coverage passing on a measured
count of 203 names, and a tape verdict that lets the registered thresholds fire.

**Integrity is the expensive problem and it is fourteen days away.** Everything
this repository turns on — whether the primary vendor rewrites bars it has
already served — is sealed, armed, and waiting on a calendar.

**And the honest reading of the two scope limits registered today is that the
agreement half of the integrity gate came out weaker than it was designed to
be**: narrower in window, and pointed at a redistribution pipeline rather than at
two independent feeds. **The revision half is intact, and it is the half that
killed H11 elsewhere in this house.**

---

# The amendment pass — written for the moment it landed, 2026-08-29

**Seven tasks. Six amendments, 11 through 16. Five ADRs, 027 through 031. Three
falsified planning figures and one falsified premise of the method. `n = 954`
requests sent, `0` dollars spent, and neither latch touched.**

**The verdict is unchanged: `PENDING_REVISION`.** That is not a null result. The
pass was asked to close gaps between what the registration *says* and what
measurement *shows*, and every one of them turned out to be a place where the
document was wrong rather than the world.

## What the registration got wrong, and what falsified each one

### 1. The carve-out was never reachable

Section 9 reserved the E2 dispersion input to bars stamped **strictly before
2016-01-04**. That is a clean rule with a clean rationale, and A.1 TASK 5 had
already measured it into the ground: **Alpaca's earliest served session is
2016-01-04 — exactly the in-sample start — and Massive's is 2024-08-29.**
**`n = 2` credentials, 0 serving.** The reserved region contained **no bar this
repository could ever have read**, and E2 power was recorded `Absent(not_served)`
for that reason and no other.

**The carve-out is now two-sided**, and the second half is the region **strictly
after the holdout ends** — at `2026-07-01T04:00:00.000Z`, which is Eastern
midnight rather than UTC midnight, because UTC midnight on 2026-07-01 is **20:00
Eastern on 2026-06-30** and would have admitted the last holdout session's
after-hours bars.

**The cost is registered, not argued away.** The post-holdout region is outside
both windows, so reading it leaks nothing a verdict is computed on — **and it is
not equivalent to what it replaced.** A dispersion estimated after 2026-06-30
reflects a **later** regime than the sample it is applied to; the original would
have reflected an **earlier** one. **The compromise now runs forward rather than
backward, and the figure may misstate in-sample dispersion in either direction by
an amount this repository has not measured and does not claim to bound.** That
sentence is attached to every E2 figure produced, in the amendment, in the
verdict record, in `HYPOTHESES.md` and in `README.md`.

### 2. The trigger rate was never 55 percent

A figure of **0.55** had been sitting in a non-binding per-trade power note. It
was never measured, and Section 9 says in as many words that the trigger rate is
*a measurement target and never an assumption*.

**Measured: 0.982143, `n = 560` selected name-sessions.** A disagreement of
**+0.432**. The measurement wins and the disagreement is recorded — the
NPLExperiment shape, where a planning figure near 9.4 events per month met
measurement at 0.5, `n = 3`.

**Stated narrowly, so it is not over-read.** It is the realized share of
registered top-20 selections producing a registered entry, on **28 post-holdout
sessions**, over a **200-name systematic sample of a 5,317-name listing**, in a
**post-holdout regime**. **It is not the in-sample trigger rate.**

**One coincidence is recorded with no claim attached.** The **long-only** rate is
**0.525**, close to 0.55. That is consistent with the assumption having been
about one side only, and it is consistent with chance. Nothing in the repository
records which was meant, and this pass does not decide it.

### 3. E2's power never needed a dispersion input at all

This is the one that matters most, and it is about the method rather than a
number.

**E2 power came out equal to E1 power to five decimal places at every assumption
and every horizon.** Not approximately: analytically, differing only by the
rounding of an implied trade count to a whole number.

The reason is Section 8's own design. **E2's permutation clusters on session
date.** A session holding `k` trades with per-trade mean `μ` and dispersion `σ`
has session mean `kμ` and session dispersion `σ√k`, so the session-level ratio is
`√k·(μ/σ)` — and **`σ` cancels**. A test whose independent unit is the session
has its power fixed by the session-level Sharpe, whatever the per-trade
dispersion happens to be.

**So Section 9's premise is wrong**, and Section 9 anticipated exactly this:
*where the computation disagrees with the figures in this table, the computation
wins and the disagreement is recorded as an amendment.* It is Amendment 15.

**The dispersion is not idle, though.** It converts a **dollar** net edge into an
information ratio, which is the use Section 9 actually describes — and that is
where the uncomfortable number lives.

## The uncomfortable number

Against the **carried** gross edge of **0.070 USD per share** (C-6, from the
independent replication of the **sibling index strategy** — a cross-application,
and labelled as one), scaled by `S / 2.81`, and the **modeled** round-trip cost:

| exit leg | assumption | gross/share | cost/share | **net/share** |
|---|---|---:|---:|---:|
| close | 2.81 | 0.070000 | 0.038631 | **+0.031369** |
| close | **1.40** | 0.034875 | 0.038631 | **−0.003756** |
| close | 0.70 | 0.017438 | 0.038631 | **−0.021193** |
| stop | 2.81 | 0.070000 | 0.068631 | **+0.001369** |
| stop | **1.40** | 0.034875 | 0.068631 | **−0.033756** |
| stop | 0.70 | 0.017438 | 0.068631 | **−0.051193** |

**At the registered assumption the modeled net edge per share is negative on both
exit legs.** At the published magnitude, on a stop exit, **two percent of the
gross edge survives the cost model**.

**This is not a verdict and it is not evidence about H1.** It is a statement
about what the registered cost model does to a carried edge at a discounted
effect size, recorded **before any read exists** so it cannot be discovered later
and rationalised.

## The measurement that was refused, and delivered anyway

**The frozen Section 6 cost model refused all 550 trades.** That is A.2 TASK 2
working exactly as designed: the SEC Section 31 rate was measured at
**0.0000206 per dollar** and **its effective date was not**, so the schedule is
empty and **the model refuses to price a trade rather than take a fee from the
wrong year.**

It was attempted again. **`sec.gov` returned HTTP 403 "Request Rate Threshold
Exceeded" on two further attempts — `n = 4` across two sessions** — and the
**stored** IBKR schedule carries the rate with **no effective date anywhere on
the page**, so it is not recoverable offline either.

**So the figure was delivered as a bracket rather than as an absence or an
invention.** The one unmeasured component was varied across **both** ends —
**zero**, because a fee cannot be negative, which is arithmetic rather than an
assumption; and **0.0000206**, the one rate measured — with everything else held
frozen.

**The bracket came out 0.0084 percent wide.** `2.0294139` against `2.0295850` USD
per share. **The unmeasured effective date does not matter for this figure, and
that is a measurement rather than a hope.** The registered figure under the
frozen model is still reported, and it is still **`Absent`**.

## Two structural holes closed, neither of which was a wrong value

**The tape was a function default.** `feed: str = "sip"` on
`orb.vendors.alpaca_minute_bars`. **The default was correct.** Every call site
passed or inherited it, and the sealed slice really was pulled on the
consolidated tape. **The defect was that nothing made a call site say which tape
it wanted**, so nothing would have noticed one that said the wrong thing — and
the measured cost of the wrong branch is a feed carrying a **median 0.027761 of
consolidated first-5-minute volume over `n = 100` pairs**, whose bars are all
real, all wrong about the market, and **invisible in every downstream figure**.

It is now a guarded config field, required at every call site across `src/orb`
**and** `tools/`, with a **named escape hatch that demands a stated reason** for
the one registered use — the Amendment 7 tape control. **Mutation 14** flips the
configured value and is caught by a **guard**, not by a number that moved.

**And the sealed slice's feed was confirmed rather than assumed.** The manifest
records `"feed": "sip"`, which is an assertion about a code path written by the
tool that chose the feed. So each of eight sampled chunks was re-requested on
**both** feeds and each served bar count compared against the sealed file's own
recount. **Seven discriminated; all seven matched the consolidated count and none
matched the single-venue count.** One served **0 bars on both feeds** and is
recorded as **uninformative and excluded** — the first run counted that `0 == 0`
tie as a match to the single-venue feed and returned `NOT_CONFIRMED`, and **the
classifier was fixed rather than the verdict.**

**The in-sample window is single-sourced, and that now lives in the
registration.** Cross-vendor agreement covers **459 holdout sessions and 0
in-sample sessions**. **All 1,762 in-sample sessions rest on a single unverified
feed.** Until this pass that fact lived only as a field on a verdict record. It
is now **SL-3**, a numbered scope limitation in Section 11, and it says what a
PASS would mean: **conditional on one vendor's rendering of that window being
faithful, with no measurement supporting the condition.**

## The ceiling, measured — and then measured properly

A.1 TASK 7 recorded Alpaca's ceiling as *not reached*. **The registered protocol
could not have reached it**, and the reason is structural: a sequential client
sends at most `60 / latency` per minute whatever spacing it asks for, and the
documented figure is 200 per minute. Escalating spacing measures latency.

**With bounded concurrency the refusal came at cumulative request 385**, after
**384 admitted in 55.96 s** — `{"message": "too many requests."}`.

**And that is a burst allowance, not a ceiling.** The whole escalation fit inside
one rolling minute, so **a token bucket of capacity near 400 refilling at the
documented 200 per minute produces exactly that observation** — and so does a
hard 411-per-minute limiter. The measurement does not distinguish them, and
recording **411.72 per minute** as *the ceiling* would have been ADR-026's error
running in reverse. **The tool's first analysis did exactly that**, proposing an
operating pace of **689.37 per minute**, and it was corrected before anything was
registered.

**So the missing quantity was measured.** After a cooldown, **250 of 250 admitted
over 75.10 s at a scheduled 200 per minute, 0 refusals** — longer than one
rolling minute. **The sustained ceiling is at or above 199.73 per minute and is
not known exactly**, the ceiling entry stays `None`, and the test now refuses to
let a lower bound be written into it.

**One figure was falsified in passing**: the A.1 TASK 7 **134.05 per minute** was
that moment's latency and not a limiter — the identical request shape achieved
**223.16 per minute** today, `n = 25`.

## What the harness caught that a reader would not have

**Mutation 13 changed category, and the harness is what noticed.** It was written
at TASK 1 to demonstrate the InsiderExperiment lesson on the new post-holdout
edge, and it **went green**: the edge had exactly one pin, and disabling it left
nothing behind. That demonstration is on the record.

**Then TASK 5 added `orb.dispersion`, whose own boundary fixture sits on the same
instant** and is not among the tests mutation 13 disables. The next run reported
**`HARNESS FAILURE`** — **and the failure was the harness being right.** The
mutation's premise had stopped being true. It is now `expect_green=False` and is
**caught**. **Nothing about the mutation changed; what changed is that the
boundary is pinned twice.**

**One test fixture was caught by a registered filter rather than by an
assertion.** The first draft of the dispersion tests built sessions with a
**0.20 USD** range and evaluated **nothing**, because the registered 14-session
ATR filter requires **above 0.50 USD**. The fixture was wrong and the filter was
right — the InsiderExperiment lesson arriving from the other side.

## What a reader should take from this section

**Nothing here moved the verdict, and that is the correct outcome.** The binding
constraint was a calendar before this pass and it is a calendar after it:
**2026-09-12**.

**What changed is that four things this repository was asserting are now things
it has measured** — the reachability of the carve-out, the trigger rate, the
feed the sealed slice was pulled on, and Alpaca's rate behaviour — **and one
thing it was asserting turned out not to be true of its own method**, in that
E2's clustered permutation makes the per-trade dispersion cancel.

**The uncomfortable number is the net edge.** At the registered assumption the
modeled net edge per share is **negative on both exit legs**. That is not a
verdict on H1 and it does not close anything. **It is the cost model, measured,
applied to a carried edge, at the effect size this registration chose in advance
for reasons it wrote down** — and it is on the record before any read exists,
which is the only place it can be honest.

---

# The inference-repair pass — written for the moment it landed, 2026-08-29

**Seven tasks. Six amendments, 18 through 23. Four ADRs, 032 through 035. One
statistical error corrected, one co-primary replaced, one hypothesis restated,
and one design shown to be unpowered against its own registered cost band. `n =
0` requests sent, `0` dollars spent, neither latch touched.**

**The verdict is unchanged: `PENDING_REVISION`. Almost nothing else is.**

## The error that was there from the first commit

Section 8 says two things that do not agree. It says *"Two co-primaries,
one-sided, and **both must pass**"*, and then it applies
`alpha_adj = 1 − 0.95^(1/2) = 0.02532057` to **each**.

**`1 − 0.95^(1/k)` is the Šidák correction for a union.** It is the right answer
when a family "succeeds" if **any** component rejects, and
`test_alpha_adj_is_the_registered_figure` has pinned its arithmetic since the
first commit — two independent tests at 0.02532057 give a family-wise rate of
exactly 0.05. **It is the correct answer to a question Section 8 does not ask.**

**Section 8's rule is a conjunction — an intersection-union test.** Berger
(1982) establishes that an IUT whose components each run at level `a` has overall
size **at most `a`**, and the argument fits on one line: under the global null,
the event that **all** components reject is a **subset** of the event that **any
single one** does. **No correction is owed.**

**So the registration had been paying a penalty it did not owe, in every power
figure it had ever reported.** At `alpha = 0.05`, **E1 at the registered 1.40
Sharpe assumption moves 0.743521 → 0.832450 on the achievable holdout, and the
minimum session count for 80 percent power falls 1,006 → 795 against 875
achievable.** **A shortfall of 131 sessions becomes a surplus of 80.**

**No datum changed. No vendor changed. No session was added.** A power shortfall
this repository has reported in every document since its first commit was an
**artefact of correcting for a union that Section 8 never described.** ADR-005
registered that shortfall openly rather than meeting it at the read, and that
judgement was right on the facts as they stood; **ADR-032 supersedes its
arithmetic and leaves it unedited.**

## The co-primary that was not one

Amendment 15 had already measured the symptom: **E2 power equalled E1 power to
between 1e-05 and 1e-12** at every assumption and horizon. The cause is
arithmetic — E2's implied mean was derived from the same Sharpe assumption E1
uses, so `implied_mean / annual_sharpe` was a **constant 0.02884727**, and the
dispersion divided out.

**Under a conjunction, a co-primary that is a rescale of the other is not a
second hurdle.** Whichever rejects first, both do.

**Repairing it was not available.** Any null of the form *"the mean is positive
at central costs"* sits **inside E1's alternative**, because it is the same claim
in different units. **The null had to change.**

> **The amended E2 asks whether mean net PnL per trade remains above zero when
> every slippage leg is set to the pessimistic end of the band Section 6
> registered before any data existed.**

That is a question E1 cannot imply. **And the dispersion stops cancelling**,
because the pessimistic shift is an **absolute dollar quantity per share** rather
than a ratio: `(central_mean − shift) / dispersion` does not reduce. **The A.1
TASK 5 dispersion of 2.029585 USD per share became load-bearing, having been
inert.**

**The amendment was written and committed before the shift was measured**, and it
**pre-registered what a collapse would mean**. That ordering is the only reason
what follows can be read as a finding rather than as a story told afterwards.

## Then it collapsed

**The measured pessimistic shift is 0.041455 USD per share.** It comes from a
**measured stop-exit share of 0.381818**, `n = 550` triggered trades with a
resolved exit — 210 stop, 340 close — mixed against hard arithmetic bounds of
**0.030** if every trade closed out and **0.060** if every trade stopped out.

**The implied central mean at the registered 1.40 assumption is 0.040386 USD per
share.**

> ## **0.041455 exceeds 0.040386. The pessimistic-cost mean is −0.001068 USD per share. It is negative.**

E2's alternative lies **inside its own null**. **E2 power is 0.043277 on the
achievable holdout — below the 0.05 size of the test.** `trades_for_e2_power`
returns a **recorded absence** rather than a large number, because **no sample
size reaches 80 percent when the effect the test is powered against does not
exist in the direction the test looks.**

**And joint power collapses with it, to 0.043277.**

## The two questions that must not be conflated

| question | answer |
|---|---|
| **Does the corrected alpha alone move E1 across its 80 percent bar?** | **YES.** 0.743521 → 0.832450; minimum n 1,006 → 795 against 875 achievable. |
| **Does JOINT power clear its 80 percent bar?** | **NO.** 0.043277, and **no session count reaches it at any n.** |

**Correcting the multiplicity error made E1 powered and left the design
unpowered.** Both are true. **The verdict record carries them as separate fields
so a later reader cannot collapse them into one claim.**

**Section 10.1 now says which one the latch runs on.** Clause 1 read *"Both
co-primaries at or above 80 percent power"*, which is a per-component condition
and not the quantity a conjunction needs. **Two components at 0.80 each can be
jointly anywhere from 0.60 to 0.80** depending on their dependence. **Joint power
is bounded above by the smaller component, unconditionally — requiring two things
is never easier than requiring one — so neither component power may be reported
as the design's power.**

## How close it is, and why closeness is not comfort

**A test with 0.043 power detects nothing**, whether it misses by a little or a
lot. But the margin bears on which route is reasonable, so it was measured
rather than left to be estimated:

| quantity | figure |
|---|---:|
| **break-even Sharpe** — where the pessimistic-cost mean reaches zero | **1.437035** |
| the registered **1.40** sits below it by | **2.577 percent** |
| **break-even stop-exit share** at 1.40 | **0.346206** |
| the measured stop share exceeds it by | **0.035612** |

**Half of the published 2.81 is 1.405. The break-even is 1.437.** **The design
was registered just on the wrong side of its own cost band**, and nobody could
have known that before this pass, because the shift depends on a
stop-versus-close mix that did not exist as a figure until it was measured.

## What was deliberately not done

**Each of these was available and each would have been wrong**, and they are
listed in the registration so a later reader can check the diff:

- **The cost band was not adjusted.** 0.040 / 0.080 / 0.020 exactly as
  registered before any data existed.
- **The effect assumption was not adjusted.** Still 1.40.
- **The alpha was not adjusted to rescue the figure.** 0.05 was fixed **before**
  the table existed, for a reason unrelated to it.
- **No weaker E2 was substituted.** The null was fixed before the shift was
  measured.
- **A negative power was not clamped** to the size of the test or to zero.
- **The ambiguous exclusion was not changed** — and at a measured rate of
  **0.000000**, `n = 560`, it was not a candidate for change.
- **No Section 0 branch was touched.** `src/orb/section0.py` is byte-identical.

**And one observation was recorded without being acted on.** BLOCKED-1 is
registered on E1 power at the **published** magnitude against the 0.50 floor;
E1 at 2.81 is 0.999835, so it does not fire and the map behaved as registered.
**Had BLOCKED-1 been defined on joint power at the registered assumption it would
fire, at 0.043277.** The branch was not changed. The observation is in the
verdict record because it is material to the operator's choice.

## The hypothesis, restated

**At a measured trigger rate of 0.982143**, `n = 560` selected name-sessions,
**the breakout condition is very nearly unconditional.** Over roughly 385 minutes
after a five-minute range, a liquid name almost always trades outside it. **The
condition selects on almost nothing, and what carries whatever information exists
is the direction of the first excursion.**

> **H-ORB, restated: among US common stocks with elevated opening relative
> volume, the sign of the first excursion past the opening 5-minute range
> predicts the direction of the remainder of the session, net of modeled costs,
> out of sample from 2023-01-03.**

**The registered rule is unchanged and stands.** Sections 2, 3, 4, 5 and 6 are
byte-for-byte as registered. **Only the description was wrong**, and a rule that
fires on 98 percent of name-sessions is still a well-defined rule with a
well-defined direction. **Changing it now would be changing the experiment after
seeing a measurement.**

**The cost to a later positive verdict is recorded in Section 11.2.** A `PASS`
would be evidence about **the informational content of the first directional
excursion** — and **not** evidence that a breakout event, as commonly
understood, **selects profitable sessions**, because at 0.982143 there is no
meaningful population of non-breakout sessions for the breakout ones to be better
than.

**The source study's own numbers already said this.** The plain broad-universe
rule returned **3.2 percent annually at Sharpe 0.48, below passive**; the
top-20-by-relative-volume restriction returned **more than 1,600 percent at
Sharpe 2.81**. **The selection did almost all the work there too.** What was
missing was the step from *"the selection does the work"* to *"then the breakout
is not selecting anything"* — **and it took a measured trigger rate to force
it.**

## What a reader should take from this section

**The verdict did not move and four things about the experiment did.**

**One was an error in this repository's own arithmetic**, present from the first
commit, which had been making the design look weaker than it was.

**One was a co-primary that had never been a second hurdle**, which had been
making the design look stronger than it was.

**Correcting both at once produced the answer neither correction produced
alone**: **E1 is powered and the design is not.**

**And the finding that matters most is the one the pass was built to be able to
produce.** The registered design, at its registered effect assumption, **cannot
detect its own effect against its own registered pessimistic cost band, at any
achievable sample size.** That is not a statement about opening-range breakouts.
**It is a statement about this design**, and it is exactly the kind of negative a
registration exists to make sayable.

**Three routes are open, none is chosen here, and none of them waits for
2026-09-12.**

---

# The rescue pass — written for the moment it landed, 2026-08-30

**Six tasks. Four amendments, 24 through 27. Three ADRs, 036 through 038. One
lever applied to H1, one new hypothesis registered without being opened, and a
criterion written before the measurement that judged it.**

## The criterion came first, and the commit order proves it

**A pass that measures a cost input after seeing a cost-driven null is exactly
the shape a reader should distrust.** The measurer knows which direction of
answer rescues the hypothesis. There is only one defence against that, and it is
not a promise.

**Amendment 24 was written, committed and pushed as `4ae14dc` before a single
line of the measuring tool existed.** It states the tiers, it states the
consequence of failure, and **the ordering is checkable in `git log` by anyone
who doubts it.**

**It also ruled `GO` out in advance, arithmetically.** For E2 to reach 80 percent
power on 875 sessions at the registered 1.40 assumption, with the measured
dispersion of 2.029585 USD per share and 19.642857 trades per session, the
pessimistic-cost mean must be at least **0.038493 USD per share** — which means
the shift must fall to **0.001893 or below**, a **21.89-fold reduction** from the
measured 0.041455. **That is below a single tick across both legs.** No
measurement of a real instrument can land there, and the amendment said so before
the measurement rather than after it.

**So the pass had exactly one degree of freedom left: what the data says.** The
effect assumption, the alpha, the stop share, every registered rule, and **the
assignment of median to the central band end and 90th percentile to the
pessimistic end** were all nailed down in advance.

## Why the band was worth measuring at all

**Section 6's slippage band is carried from an ETF.** 0.020 central and 0.040
pessimistic on entry, 0.040 and 0.080 on stop exits, 0.010 and 0.020 on close
exits — all from the QQQ replication (C-6), an instrument whose spread sits near
one cent.

**The registered universe selects news-driven single names.** The carried figures
were never measured on the instruments actually traded, and **Amendment 21's
collapse turns on the band's width** — the pessimistic end minus the central end,
mixed on the measured stop-exit share.

**So the one honest lever available was to measure it.** Not to move it, not to
narrow it, not to argue about it: to find out what it is on this universe.

## What one-minute data can and cannot support

**This is the limit that bounds everything below, and it was written into the
tool's docstring before the tool ran.**

**When the trigger bar opens through the boundary**, the first trade of that bar
**is** the first trade through it, and the overshoot is **exactly measurable**.

**When the bar opens inside the range and crosses within the minute**, the first
trade through the boundary lies somewhere in that bar and **one-minute data
cannot locate it.** The writer records **0.0** for that trade.

**So the overshoot distributions are LOWER BOUNDS, the measured band is a lower
bound, and any power computed on it is an UPPER bound on power.** The two cases
are counted separately, so a reader can see how much of the distribution is
bounded rather than measured.

**That asymmetry is the whole epistemic value of the result.** A design that
fails at **the most favourable honest reading of its own costs** has failed. A
design that passes there has passed **only under a bound**.

**The spread half was not bounded, because the tier serves quotes.** That was
probed and confirmed before the tool was written, so the **time-weighted quoted
half spread** across each entry and stop minute is **measured** and added to the
overshoot. Weighting is by **time held**, not by quote count, so a quote that
stood for twenty milliseconds cannot dominate a minute. **A minute whose quotes
are unusable is a refused minute, counted as such, never a zero spread.**

## What the measurement said

**It went hard against the hypothesis.**

| leg / end | **carried** (QQQ) | **measured** | ratio |
|---|---:|---:|---:|
| entry, central | 0.0200 | **0.087019** | **4.35×** |
| entry, pessimistic | 0.0400 | **0.354645** | **8.87×** |
| stop, central | 0.0400 | **0.033529** | *0.84×* |
| stop, pessimistic | 0.0800 | **0.198061** | **2.48×** |
| close, central | 0.0100 | **0.040000** | **4.00×** |
| close, pessimistic | 0.0200 | **0.261000** | **13.05×** |

**Five of six ends were understated by the carried band. One was overstated** —
the central stop exit, at 0.033529 against 0.040, `n = 210` — **and it is
recorded, because a measurement is not a reduction.**

**The driver is the entry half spread**: **median 0.076572, 90th percentile
0.333662 USD per share**, over **550 minutes served and 0 refused**. The carried
figure came from **QQQ, whose spread sits near one cent**.

**That is not a surprise once it is stated.** The registered universe selects the
**top 20 names by elevated opening relative volume** — the names with the most
unusual activity in the first five minutes of the session. **The selection rule
and the wide-spread population are the same population.** The carried figure was
an ETF's spread applied to news-driven single names **at the one moment of the
day they are least like an ETF.**

**The resulting shift is 0.467065 USD per share against a carried-band shift of
0.041455 — 11.27 times larger**, of which the entry width is **57.3 percent**.

## The verdict the criterion had already fixed

> ## **`NOT_RESCUED`.** The criterion required the shift to fall **strictly below 0.040386**. It rose to **0.467065**, **11.56 times** the central mean.
>
> **Pessimistic-cost mean −0.426679. E2 power 0.000000. Joint power 0.000000. No session count reaches 80 percent at any assumption.**

**And the direction is the pass's own control.** A rescue pass that measures a
cost input after seeing a cost-driven null is exactly the shape a reader should
distrust. **Amendment 24 answered that with a pre-committed criterion and a
checkable commit order. The result answers it a second way: no search for a
favourable number produces an eleven-fold worse one.**

## One thing the closure was expected to say, and does not

**The instruction anticipated a closure conditional on the halving heuristic**,
on the grounds that E2 passes at the published 2.81 where power reaches 0.820.
**That was true under the carried band and is not true under the measured one.**

| E2 power at 2.81, holdout `n = 875` | figure |
|---|---:|
| under the **carried** band | **0.819524** |
| under the **measured** band | **0.000000** |

**At the source study's own undecayed magnitude the pessimistic-cost mean is
−0.386004 and E2 power is zero.** **The closure holds there too**, which makes it
**stronger than expected, not weaker**, and removes the one conditionality the
instruction asked to be recorded. **Repeating that sentence as though it still
applied would have been the easy thing and the wrong one.**

## H1, closed

**`cost-bound`.** The effect may be real; **it does not survive the modeled
cost.** Precedent MLCryptoEngine H6.

**What it rests on, stated so it can be attacked:** the registered Section 6
model and its pessimistic band, registered before any data existed; a slippage
band measured on **42 post-holdout sessions**, which is **a different regime from
the holdout it is applied to** and **a lower bound**; and a dispersion of
2.029585 USD per share.

**The honest attack is the second**, and it is Amendment 21's route (b): **real
execution evidence could narrow the band.** This repository holds none, has no
broker credential, and none is planned — **and the measurement it does hold
points the other way by a factor of 11.27.**

**What the closure is not.** **It is not a finding that the opening-range effect
does not exist.** **E1 remains powered at 0.832450.** **No in-sample or holdout
bar was ever read. Both latches remain absent.** **Nothing in this repository
measured whether the directional edge is real.** **It is a finding that this
design cannot clear its own registered cost band** — a statement about the
design.

## The calibration ledger, and an event that did not resolve

**Assistant prior 0.15**, recorded 2026-08-28. **Operator prior 0.30**, label
`INDEPENDENT`, recorded 2026-08-29.

**Neither is scored correct or incorrect by a closure of this kind.** Both were
probabilities on *"a real capturable edge surviving the registered cost model out
of sample"*, and **H1 closed before any out-of-sample read occurred.** **The event
they were about did not resolve.** The ledger records the closure, its kind and
that fact, **and does not convert an unresolved event into a scored one.** The
factor-of-2.0 disagreement between the two priors stays unresolved with it.

## H1b, registered and not opened

**A filter change proposed after seeing a null is a new hypothesis.** Folding the
price floor into H1 would have let H1 be re-specified until it passed while the
verdict carried **none** of the cost. **So it is H1b, `REGISTERED_NOT_OPEN`, and
it increments the deflated-Sharpe trial count from 8 to 9 — for H1b.** H1's count
of 8 is unchanged. **The ninth trial exists because the change was proposed after
seeing a null**, and that is the cost of having looked.

**The scan confirmed both halves of the registered mechanism**, which is the most
interesting thing in it. **The central-mean-to-shift ratio rises monotonically
0.9742 → 0.9983 → 1.1415 → 1.4767 → 2.1424** while the shift stays inside a **4
percent band** — the price-invariance H1b asserted, measured. **And mean relative
volume of the selection falls 2.0652 → 1.4103** — the rank-tail dilution it also
predicted. **Both are real and they run in opposite directions.**

**One column is a sample artefact and is labelled as one.** The scan ran on a
**200-name systematic sample of a 5,317-name listing**. A floor that fails to fill
20 names in a **1-in-26 subsample** says nothing about a universe **26.6 times
larger**. **The 50 and 100 USD rows are not evidence that those floors empty the
registered universe.**

## What a reader should take from this section

**A registration exists to make a negative sayable, and this is what that looks
like when it happens.**

**The lever was honest and it was the only one available**: the cost band was
carried from an ETF and had never been measured on the instruments the rule
actually trades. **Measuring it was the right thing to do whichever way it came
out.**

**It came out eleven times worse.**

**The one structural doubt this registration named first is the one that closed
it.** Section 1's structural doubt 2, written before any data existed: *the
independent replication measured a gross edge of 0.070 USD per share and found
net PnL crossing zero at roughly 0.022 USD per share of entry slippage — the
entire gross edge of the index version measured smaller than a realistic slippage
assumption.* **The measured entry half spread on this universe has a median of
0.076572.** **The doubt was right, and it was right for the reason it gave.**

**What stopped this repository in the end was not the calendar.** The
bar-integrity re-pull is still due **2026-09-12**, and it is still the right
measurement — **but H1 closed on cost before it arrived.**
