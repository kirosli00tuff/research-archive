# DECISIONS.md — numbered architecture decision records

Every ADR is dated, states the context that forced it, the decision, the
alternatives rejected **with the reason they were rejected**, and its
consequences. **An ADR is never edited after the fact; a reversal is a new ADR
that supersedes it by number.**

Figures carried from outside this repository are labelled **carried**. Figures
measured here travel with their n.

---

## ADR-001: Three network calls preceded the registration, and are recorded rather than argued away

**Date:** 2026-08-29 · **Status:** accepted · recorded at `progress.md` Entry 0a and REGISTRATION.md §0

**Context.** STAGE A.0 TASK 4 and TASK 5 require REGISTRATION.md to be committed
**before any network call**. Three GET requests were sent at ~01:52Z, before
`progress.md` existed, to establish whether outbound network access existed at
all before stating an ETA table.

**Decision.** Record them, in full, at the top of the log and in the
registration's own disclosure block. `api.polygon.io/v1/marketstatus/now` (401),
`stooq.com/q/d/l/?s=aapl.us&i=d` (200), Alpha Vantage `TIME_SERIES_INTRADAY`
demo (200), **n = 3, every body discarded unread to `/dev/null`**.

**Alternatives rejected.** *Omitting them as immaterial*: three status codes are
immaterial to the hypothesis and **entirely material to whether this document is
a pre-registration**, which is a claim about ordering and nothing else.
*Describing them only in the commit message*: a reader of the registration must
meet the exception where the claim is made.

**Consequences.** One of the three went to `stooq.com`, which **A.1 TASK 1 later
measured as publishing `User-agent: * / Disallow: /`** — a host this repository
had no standing to fetch from. That is precisely why standing rule 12 orders
terms **before** the first fetch, and the sequence is on the record as the reason
rather than as a rule nobody tested. No further request was sent to that host.

---

## ADR-002: The entry is a true breakout, not the source study's immediate first-candle entry

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §3

**Context.** The source study (SSRN 4729284, **carried**) enters at 09:35 on the
first candle's **direction** and does **not** require a later break of the
opening range. That is early-momentum with an opening-range stop. It is
routinely described, including by its own authors' framing, as an
"opening-range breakout".

**Decision.** Register the **true breakout**: the first trade **through** the
range high goes long, the first through the range low goes short.

**Alternatives rejected.** *Registering the paper's rule under the paper's
name*: it would carry the paper's label, and the paper's reported figures, onto
a different claim, and a later reader would take a result here as bearing on
SSRN 4729284 when it does not. *Registering both*: the second rule is already a
**named secondary** and is priced into E1's trial count of 8; promoting it to a
co-primary would double the alpha spend for a question this repository is not
asking.

**Consequences.** Section 11 states the cost explicitly: **a result here is never
evidence that the source study's figures are correct, and a failure here does not
refute them.** The two rules are different claims that share a name.

---

## ADR-003: The 10R profit target is removed

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §3

**Context.** The source study exits at a 10R target or at the session close. The
target **fills on 2 to 3 percent of trades** (**carried**).

**Decision.** No profit target. The exit is the session close, 15:55–15:59
Eastern, or the stop.

**Alternatives rejected.** *Keeping 10R*: a threshold that binds on one trade in
forty is fitted to the tail of the sample it was chosen on, and its contribution
to a reported return is dominated by a handful of observations. *Registering a
smaller target*: any target is a mined parameter unless it is registered for a
reason independent of the sample, and no such reason exists here.

**Consequences.** The registered rule is **strictly simpler** than the source
study's, which makes it a weaker test of their result and a cleaner test of the
breakout itself. Named in Section 11.

---

## ADR-004: The E1 statistic is the annualized deflated Sharpe **value**, not the DSR probability

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §8

**Context.** Section 8 registers *"deflated Sharpe at or above 1.00"*. Bailey and
López de Prado's **Deflated Sharpe Ratio** is a **probability** in [0, 1], which
cannot reach 1.00 except degenerately. The registered bar and the named method
are in tension as written.

**Decision.** E1 is the **annualized Sharpe net of the deflation benchmark**,
`annualize(SR_hat − SR0)`, where `SR0` is the expected maximum Sharpe over the
registered 8 trials by the Bailey and López de Prado construction. The **DSR
probability is computed and reported beside it as a named secondary.**

**Alternatives rejected.** *Reading the bar as "DSR probability ≥ 0.95"*: it
changes the registered number, and inventing a threshold to fit a method is the
selection this registration exists to prevent. *Dropping the deflation*: the
trial count of 8 is the whole reason E1 carries the multiple-testing correction.

**Consequences.** `SR0` scales with **the dispersion of Sharpes across the
trials**, which is a measured quantity. Where that dispersion is unmeasured,
`expected_max_sharpe` returns `Absent` and **E1 refuses rather than deflating by
an invented amount**. That is its state today.

---

## ADR-005: The registered assumption is half the published effect, and the power shortfall is registered openly

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §9

**Context.** The source study reports **Sharpe 2.81** (**carried**). Registering
power against a study's own headline figure assumes no decay, no publication
effect, and no selection in the reporting.

**Decision.** Register **annualized net Sharpe 1.40**, half of 2.81. The
rationale is registered with it and is **not discretionary**: McLean and Pontiff
measured **58 percent post-publication decay across 97 predictors from 80
studies** (**carried**); the result is unreplicated and commercially motivated;
and the one independent replication of the sibling index strategy **found the
edge inside the spread** (**carried**). Powers at 2.81 and at a quartered 0.70
are computed and reported beside, the NPLExperiment H3 pattern.

**And the shortfall is registered, not discovered.** At 1.40 the holdout yields
**t = 2.609 at the computed n = 875** — **above the 2.50 holdout gate and below
the 3.0 that Harvey, Liu and Zhu argue a new claim should clear** (**carried**).
The registration states in plain words that **the holdout alone cannot clear a
factor-zoo hurdle at the discounted effect size.**

**Alternatives rejected.** *Registering 2.81*: it would report ~0.9995 power and
conceal that the design is powered only against a figure nobody has replicated.
*Registering 0.70*: **measured power 0.2578**, below the 0.50 BLOCKED floor at
every reachable horizon — registering it would block the experiment on an
assumption chosen to block it.

**Consequences, measured 2026-08-29.** **E1 power 0.7435 at 1.40 and 0.9995 at
2.81**, which is the DEGRADED clause firing exactly. **Minimum N for 80 percent
at 1.40 is 1,006 against 875 achieved.** Extending to 2026-12-31 gives 1,003 and
**0.7991** — three trading days short. **Recorded while holding no result**, so
that a later extension of the Section 7 holdout window cannot be made quietly.

---

## ADR-006: A concentration gate and a persistence gate, as pass-fail conditions and not as tests

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §8

**Context.** In the independent replication, **76 percent of the filtered
strategy's PnL came from 2022 alone**, and the filter **lost money in 2017, 2020
and early 2023** (**carried**). A 2026 MNQ falsification study found the same
one-good-year signature (**carried**). A Sharpe computed over a window containing
one exceptional year is not a claim about the other years.

**Decision.** Two structural gates, applied alongside the co-primaries, **both
pass-fail, neither carrying alpha**: **no single holdout calendar year above 50
percent of holdout net PnL**, and **positive net PnL in at least 3 of the 4
holdout calendar years**.

**Alternatives rejected.** *Reporting concentration as a diagnostic*: a
diagnostic is read after the verdict and changes nobody's mind. *Spending alpha
on it as a third co-primary*: it is not a claim about the effect's existence, it
is a condition on what kind of evidence counts.

**Consequences.** The gates are **not free**: a genuinely real effect
concentrated in one regime fails here. That is registered as intended. Pinned by
`test_all_four_conditions_are_required`, which shows a run passing E1, E2 and
persistence but failing concentration **still failing overall**, so no gate can
quietly become advisory. A non-positive total also fails, so a losing strategy
cannot pass by shrinking its own denominator.

---

## ADR-007: Vendor selection on integrity grounds — deferred, because no vendor is reachable

**Date:** 2026-08-29 · **Status:** **deferred** · A.1 TASK 3 prerequisite

**Context.** A.1 TASK 3 requires selecting a primary and a secondary vendor **on
integrity grounds**, recording the reasoning. A.1 TASK 1 measured **0 of 9
vendors serving a bar to this repository**.

**Decision.** **Record no selection.** Record instead the two questions that will
decide it, both integrity questions and neither a price question: **does the tier
serve delisted names**, and **does it retroactively rewrite already-served bars
on a split or a correction.**

**Alternatives rejected.** *Selecting on documented capability*: standing rule 4
forbids treating a pricing page as a measurement, and the whole point of the
selection is the property a pricing page never states.

**Consequences.** `docs/ACCESS.md` records a **recommended pair with its
reasoning** — Polygon/Massive as primary, because it is the only probed vendor
publishing a delisted-ticker reference endpoint and minute aggregates on one
host; Alpaca or Tiingo as secondary — and records that **if the two share an
upstream consolidated tape, the agreement measurement is labelled as measuring a
redistribution pipeline rather than two independent feeds.** Selection is made
when a credential exists, in its own dated ADR.

---

## ADR-008: A vendor refusal served at HTTP 200, and a body-aware health classifier

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 1 finding

**Context.** **Measured:** Alpha Vantage's demo key returns **HTTP 200** carrying
`{"Information": "The **demo** API key is for demo purposes only..."}` and no
time series; its delisted `LISTING_STATUS` query returns a **2-byte body, `{}`**,
also at **200**. **n = 2 probes.**

**Decision.** Health is classified from the **status code and the body**. A 429
is `rate_limited`; a 5xx or a transport failure is `source_failed`; a 200
carrying a known refusal marker is `source_failed`; an empty or `{}`/`[]` body at
200 is `no_data`; anything else is `stored`.

**Alternatives rejected.** *Classifying on the status code alone*: this is
exactly how a refusal becomes a session with zero bars — the health/composition
merge standing rule 7 forbids, and Guard 4 exists to prevent.

**Consequences.** **It caught this repository's own client.**
`orb.http.PacedClient` labelled the Alpha Vantage refusal `stored`, because it
classifies on status and non-empty body. That is recorded in `docs/ACCESS.md`
rather than smoothed. The fix lives in `orb.collector.classify` and is scoped to
A.3, because **no Alpha Vantage row is admitted to anything before then**.

---

## ADR-009: Three-point cost bands, with the optimistic end labelled an upper bound of optimism

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §6

**Context.** The independent replication measured the sibling index strategy's
**gross edge at 0.070 USD per share** and its **net PnL crossing zero at roughly
0.022 USD per share of entry slippage**, against a QQQ spread near **0.010 USD**
(**carried**). The source study assumed **explicitly zero slippage** (**carried**).

**Decision.** Every slippage leg carries a **three-point band**. Entry
(0.010 / **0.020** / 0.040), stop exit (0.020 / **0.040** / 0.080) — widest,
because a stop is marketable and gap-prone — and close exit
(0.005 / **0.010** / 0.020). **The optimistic end is reported as an upper bound
of optimism and never as the central case.**

**Alternatives rejected.** *A single central figure*: the whole question is
whether the edge survives cost, and a point estimate hides that the answer
depends on it. *Adopting the source study's zero*: it is not a cost assumption,
it is the absence of one.

**Consequences, measured 2026-08-29.** At the central band on a 50 USD name a
round trip costs **≈ 0.0386 USD/share on a close exit and ≈ 0.0686 on a stop
exit**, against a gross edge of 0.070 — **55 percent and 98 percent of the edge**,
with **slippage 78 percent of the close-exit total**. The registered central
entry figure of **0.020 sits 0.002 below the replication's measured
break-even**. Section 6's claim that the cost band is the experiment's second
axis is a measured number, not an assertion.

---

## ADR-010: Integer share counts only, from a measured broker constraint

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §4

**Context.** **HFExperiment measured IBKR refusing fractional-sized orders
through the API with error 10243** (`reports/stage_a1b/a1b_report.md` line 52,
**carried**).

**Decision.** Sizing produces **integer share counts only**, and the registration
states it as a **design constraint** rather than discovering it at execution.
`CostModel.commission` refuses a non-positive share count outright.

**Alternatives rejected.** *Modelling fractional sizing and rounding at
execution*: the rounding is where the 0.25 percent risk target actually breaks,
and deferring it moves a known constraint into the part of the pipeline that has
no tests.

**Consequences.** On a low-priced name with a wide opening range, the integer
floor makes the realized risk per trade differ materially from 0.25 percent. That
is a registered property of the design, not an implementation detail.

---

## ADR-011: The blindness field lists, and a third module category for dark strategy code

**Date:** 2026-08-29 · **Status:** accepted · registered as CLAUDE.md and REGISTRATION.md

**Context.** Stage A must read **no** priced bar field. But an opening-range rule
**is** a statement about highs and lows, so `universe.py`, `signal.py` and
`verdict.py` cannot be blind — and they must still be written in Stage A.

**Decision.** Three categories, not two.

1. **Ordinary modules** — Guard 5 forbids every priced field, by parse tree,
   across attribute, subscript, `.get`, **and bare string constant** forms.
2. **Sealed modules** (`seal.py`, `comparator.py`) — may touch priced fields;
   `seal.py` parses nothing and `comparator.py` returns only counts.
3. **Latched modules** (`bars.py`, `universe.py`, `signal.py`, `verdict.py`) —
   may read priced fields, and are held by a **stronger** guarantee instead:
   `test_no_stage_a_module_imports_a_latched_module` walks **every import in the
   package** and requires that no module outside the set imports one. **Nothing
   on the Stage A collection path can reach the strategy, by construction.** At
   runtime every bar carries a `Provenance`, and `SEALED_VENDOR` is refused by
   every entry point until the Stage C latch.

**Alternatives rejected.** *Making the strategy modules sealed*: it would grant
four more modules the blindness exception and weaken what "sealed" means.
*Leaving the strategy unwritten until Stage C*: it would put the entire signal
implementation on the far side of a latch, untested, at the moment it matters.

**Consequences.** The string-constant form was added **after the comparator
defeated the guard**: `for alias in ("o", "open"): bar[alias]` reads every
priced field and a constant-subscript walk reported **zero**. The field registry
moved to `orb/fields.py` — names, no logic — so the declaration site does not
flag itself, and it is the guard's **single** structural exemption.

---

## ADR-012: The pre-period carve-out, enforced at one site with the boundary in one place

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §9

**Context.** The E2 economic-power computation needs a per-trade dispersion
figure. Taking it from the test window is **reading the outcome to plan the test
of the outcome**; inventing it registers a number this repository did not
measure.

**Decision.** Power inputs may read bars stamped **strictly before**
`2016-01-04T14:30:00.000Z`. Enforcement is `orb.preperiod.require_pre_period` and
`gate_pre_period`; the boundary lives **only** in `CONFIG.pre_period_end_ms`; two
guards hold it there — no module outside `config.py` may hardcode the literal,
and no module outside `preperiod.py` may read it from config.

**Alternatives rejected.** *Using the in-sample window*: the window the verdict is
computed on. *Assuming a dispersion*: standing rule 4.

**Consequences.** Verified independently: 14:30Z **is** 09:30 Eastern on
2016-01-04 because that date falls in standard time, and the calendar's own first
in-sample opening-range start equals the literal **exactly**. Mutation 4
discovered that the boundary is pinned in **three** independent places, and it
took seven edits across three test modules plus the source before the guard
stopped binding.

---

## ADR-013: The index-ETF opening-range variant is excluded

**Date:** 2026-08-29 · **Status:** accepted · registered as HYPOTHESES.md cull 1

**Context.** The sibling study (SSRN 4416622, **carried**) reports QQQ **1,484
percent against 169 percent** buy-and-hold. The independent replication
reproduced it **within noise — 1,775 trades against the paper's 1,795, gross
Sharpe 1.06** — and then showed **the entire gross edge of 0.070 USD/share sits
inside the spread**, with net PnL crossing zero at **~0.022 USD/share** against a
QQQ spread near **0.010** (**carried**). Its 09:25 NQ filter lifted per-trade
edge to **0.125 at t 2.05**, yet strategy Sharpe **0.77** barely beat
buy-and-hold **0.72**, with **overlapping bootstrap intervals** (0.05–1.41
against −0.03–1.47).

**Decision.** **Excluded.** Section 2 admits US common stocks and no ETFs.

**Alternatives rejected.** *Testing it as a control*: it would spend sample and
attention re-measuring a **settled cost problem**, and the replication already
answered it more carefully than this repository could.

**Consequences.** Section 11 states that a result here is **never evidence about
index ETFs**. And the replication's figures are carried into Section 6 as the
reason the cost band is first-class — the excluded variant supplies this
repository's most important cost input.

---

## ADR-014: A session-clock guard, because a fixed UTC offset mis-slices a third of the sample

**Date:** 2026-08-29 · **Status:** accepted · registered as CLAUDE.md standing rule 14

**Context.** The opening range is anchored to **09:30 Eastern**, which is 13:30
UTC in summer and 14:30 UTC in winter. A fixed offset takes the range from the
**wrong five minutes**, and does so **silently** — producing a range rather than
an error.

**Decision.** One Eastern zone, `ZoneInfo("America/New_York")`, constructed in
`sessionclock.py` and nowhere else. Every function refuses a naive datetime. Two
AST guards: **no module may call `timezone(...)`**, and **no module outside
`sessionclock.py` may name the string `America/New_York`.**

**Alternatives rejected.** *Storing everything in UTC and converting at the
edge*: the conversion is the bug, and moving it to the edge moves it out of
sight. *Trusting review*: the failure is invisible in output.

**Consequences.** **Measured rather than asserted**: over 2016-01-04 to
2026-06-30, **n = 3,831 calendar days**, a fixed −05:00 offset resolves 09:30
Eastern to the wrong UTC instant on **more than one third** of them. A test
counts it. Mutation 5 confirms the guard fires.

---

## ADR-015: Pacing is per endpoint, and today's measurement licenses no pace

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md §12, Amendment 2

**Context.** solattn ADR-021: one endpoint refused **47.5 percent of n = 1,863
attempts** while a second, on the same host and the same IP, took **0 of 360**
(**carried**). A.1 TASK 2 measured **n = 18 requests, 0 refusals on a limit** —
Polygon **8 of 8 at 88.4/min**, Alpha Vantage **5 of 5 at 29.1/min**.

**Decision.** Pacing is keyed **per endpoint**, the ledger stays keyed per
vendor, and **the A.1 TASK 2 measurement licenses no pace at all.** Every
reachable path was an **unauthenticated refusal** path, and **a ceiling measured
on a 401 is not evidence about the authenticated data endpoint.**
`DEFAULT_MIN_SPACING_S = 6.0` stands as a conservative default, **labelled
unmeasured**.

**Alternatives rejected.** *Reading 88.4/min as the ceiling*: Polygon documents
**5/min**, and the measured figure does not contradict it because **they are
different endpoints**. Treating it as a rebuttal would be standing rule 4 run
backwards — a measurement of the wrong thing beating documentation of the right
one.

**Consequences.** An **unregistered vendor has no cap and is refused outright**.
Every pacing figure is re-measured per endpoint at the first task holding a
credential, and moved by a dated amendment if it disagrees.

---

## ADR-016: The seal target is the closed session, never the open one

**Date:** 2026-08-29 · **Status:** accepted · the solattn ADR-019 shape

**Context.** solattn measured **all eight seals mismatching their files**
(recorded 640–9,675 rows against finals of 14,556–44,813) because the daily pass
sealed the day it was *running in* rather than the day that had *closed*
(**carried**). The files were never damaged; the attestation target was wrong.
**An attestation of the wrong content is worth less than no attestation**,
because it teaches readers to expect mismatches.

**Decision.** `seal_closed_session` **raises** for any session on or after the
current date. The 22:15 UTC pass seals the **prior** session. A changed bar on a
closed session appends a revision row carrying **both hashes and both pull
timestamps**.

**Alternatives rejected.** *Sealing at the end of the session*: the boundary is
exactly where straggler rows land. *Re-sealing on change*: it destroys the
evidence the revision row exists to record.

**Consequences.** This is where the MLCryptoEngine H11 hazard becomes a
**measurement** instead of a discovery. Mutation 9 confirms the refusal fires.

---

## ADR-017: A fourth Section 0 state, PENDING_ACCESS, for a measurement that does not exist

**Date:** 2026-08-29 · **Status:** accepted · registered as REGISTRATION.md Amendment 1

**Context.** A.1 TASK 1 measured **0 of 9 vendors serving a bar**. Section 0 as
registered fires from a revision finding and an agreement finding, and both are
`Absent`. The map had **no state for "the measurement does not exist"**, and the
two nearest states are wrong in opposite directions: GO would pretend, and
BLOCKED would close H1 as `source-integrity-blocked` **on evidence that does not
exist**.

**Decision.** Register `PENDING_ACCESS`, evaluated **ahead of every BLOCKED
trigger**. It arms nothing, it is a verdict on **access** rather than on H1, and
it is explicitly not a source-integrity closure.

**Alternatives rejected.** *Firing BLOCKED*: it would record a source-integrity
death this repository did not measure — the exact error the NPLExperiment
correction closed a hypothesis over, run in reverse. *Substituting a placeholder
finding*: standing rule 5.

**Consequences.** **The amendment was written while holding zero bars, zero
prices, zero volumes and zero sessions**, which is what makes it un-fittable:
there is no result. It is pinned as **not a bypass** — a test walks the
present-input space and requires the clause to be **inert** the moment both
measurements exist. GO, DEGRADED and BLOCKED are unchanged in text, threshold and
precedence.

---

## ADR-018: A manual-run guard with a named override

**Date:** 2026-08-29 · **Status:** accepted · A.3 TASK 3

**Context.** A manual pass running while a timer's unit is active gives two
processes writing one append-only ledger, and the rows interleave. Standing rule
10 says to union intervals and order by clock — **which is a repair.**

**Decision.** `require_no_active_unit` refuses while `orb-daily.service` or
`orb-actions.service` is active. The override is a **named environment
variable**, `ORB_ALLOW_MANUAL_RUN=1`, so that an override is visible in a shell
history rather than being a flag nobody remembers passing.

**Alternatives rejected.** *A lock file*: it survives a crash and then blocks
every subsequent run. *No guard, relying on the repair*: refusing is cheaper than
repairing, and the repair is lossy when two writers interleave inside one line.

**Consequences.** Both units are **inert today**: the CLI entry points refuse and
exit **78** because Section 0 fired `PENDING_ACCESS`. **A collector that runs and
stores nothing looks identical in a log to one that ran and found nothing**, so
refusing loudly is the only honest inert state.
