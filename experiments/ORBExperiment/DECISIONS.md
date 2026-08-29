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

---

## ADR-019: Secret redaction sits at the recording boundary, not the call site

**Date:** 2026-08-29 · **Status:** accepted · A.-1 TASK 0, Guard 8

**Context.** Three vendor credentials now exist. Three individually harmless
facts compose into a leak: **a credentialed endpoint can return the key inside
its own error body**; **`docs/ACCESS.md` records refusal payloads verbatim**,
which is the whole point of the file; and **`orb.seal.SealedWriter` stores raw
vendor bytes without parsing them**, which is what makes it a sealed writer. Put
together, a key reaches a committed artifact **without any module ever printing
one on purpose.**

**Decision.** Redact where a string becomes a **record**, not where a request is
built. Three boundaries, each pinned by parse tree in
`test_every_recording_boundary_routes_through_the_redactor`:
`AppendOnlyLedger.append` → `redact_row`, `SealedWriter.store` → `redact_data`,
`Response.__post_init__` → `redact_text` and `redact_data`. **A `Response` is
redacted on birth**, so one built by any caller in any tool is already safe to
record. Recordable about a credential: **name, presence, character length**. Not
recordable: value, prefix, suffix, **and any hash** — a hash of a 32-character
key is a **confirmation oracle for a guess**.

**Alternatives rejected.** *Redact at each call site*: a call site can be
forgotten and there is no bound on how many exist; a recording boundary is three
places. *Never record refusal payloads*: the payloads are the evidence — A.1
TASK 5's reach boundary and A.1 TASK 7's ceiling are both **verbatim refusal
strings**, and a repository that cannot quote them cannot show its work. *Hash
the credential to prove absence*: that is the confirmation oracle above.

**Consequences.** **Redaction is deterministic** — the same secret always becomes
the same placeholder — because A.1 TASK 3 measures the bar revision rate by
comparing **stored bytes** across two pulls 14 days apart, and **a varying
redactor would make every pull differ from every other pull and register a
fabricated 100 percent revision rate**: a BLOCKED at `> 0.020` manufactured by
the guard meant to protect the measurement. Pinned both ways. A secret shorter
than **8 characters is refused, not redacted**, with the fixture **on** the
boundary. `Response.byte_count` counts what the vendor served and
`stored_byte_count` what would be stored, so **a vendor echoing a key back is
visible without anyone reading the body** — recorded as an indicator and
**labelled an indicator rather than a proof**.

---

## ADR-020: The operator prior is labelled INDEPENDENT and, separately, not blind

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 1, REGISTRATION.md
Amendment 5

**Context.** Section 13 reserved the operator prior slot and registered the test
for its label **before** any number existed: `independent` *"only if it was
reached without reading the line above"*, `adopted` otherwise. The operator
recorded **0.30** on 2026-08-29, against the assistant's **0.15** of 2026-08-28 —
a **factor-of-2.0** disagreement.

**Decision.** Label it **`INDEPENDENT`**, because the operator formed 0.30 rather
than taking 0.15. **And record a second, separate field:
`blindness = independent_but_not_blind`**, because the assistant's number was
recorded first and was **visible** to the operator before this one was formed.
**A later reader must not score 0.30 as an unanchored estimate.**

**Alternatives rejected.** *Label it `adopted`*: false — the operator did not
take the assistant's number, and mislabelling it would corrupt the ledger in the
opposite direction. *Label it `INDEPENDENT` and say nothing else*: technically
correct and quietly misleading, because the calibration ledger would score an
anchored prior as a blind one. *Have the assistant resolve the ambiguity in the
operator's stated reason*: that is the assistant writing the operator's reasoning
into the ledger — **the adopted-prior error run backwards**.

**Consequences.** The operator's stated reason — *prior house experiments have
carried pessimistic evaluations* — **admits two readings that push in opposite
directions**, and both are recorded, unresolved: **harsh house gates** argue for
a *lower* prior on H1 clearing them; **systematic under-forecasting of survival**
argues for a *higher* one. **The operator did not narrow between them and this
repository does not narrow on the operator's behalf. H1 resolves and scores 0.30
either way.** Section 10 clause 2 now reads **satisfied**; clauses 1 and 3 do
not, and the Stage C latch stays closed. `orb.latch.normalise_prior_label` folds
case and surrounding space **and nothing else**, because a latch refusing a
correct answer over letter case would fail exactly once, at the most expensive
moment, and its refusal would be **indistinguishable from the refusal that exists
to stop an unlabelled slot**.

---

## ADR-021: Tape identification is a branch ahead of the agreement thresholds, not a reinterpretation of them

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 4, REGISTRATION.md
Amendment 7

**Context.** Section 0's cross-vendor agreement clause — `PASS ≥ 0.95`,
`PARTIAL ≥ 0.85`, `FAIL` below, firing **BLOCKED-4** — assumes two feeds trying
to measure **the same thing**. Alpaca serves both a consolidated feed and an
IEX-only feed from the same endpoint, one parameter apart. **IEX ran about 2.8
percent of consolidated volume in the measured window.** Scoring an IEX-only feed
against the 0.95 bar would fire BLOCKED on **entitlement** while recording it as
**integrity**.

**Decision.** A branch evaluated **before** the agreement verdict, gating whether
it may fire at all. **`SAME_TAPE`** at a median first-5-minute volume ratio in
`[0.90, 1.10]` — thresholds apply as written. **`DIFFERENT_TAPE`** below `0.50` —
**thresholds do not apply and must not fire**; a high-or-low disagreement is a
**tape-coverage finding**, and it routes to an operator item. **`AMBIGUOUS`**
between — **fire nothing**, record the distribution, hand over the numbers.

**Alternatives rejected.** *Read the vendors' documentation and trust it*: that is
a documented figure standing in for a measured one, which standing rule 4
forbids by name — and the whole reason this branch exists is that a tape claim is
cheap to publish. *Widen the agreement thresholds to absorb a single-venue feed*:
that makes the gate unable to detect the failure it exists for. *Compare bar
counts instead of volume*: IEX serves a bar for most minutes; **it is the volume
inside the bar that is 2.8 percent**, so bar counts would have missed it.

**Consequences.** **Measured `SAME_TAPE` on Massive against Alpaca-SIP: median
1.005197, IQR [1.003096, 1.007726], n = 100 session-ticker pairs, 0 below the
0.20 single-venue threshold.** Two controls were run because **a discriminator
pointed at one pair is an assertion about nothing**: Massive vs Alpaca-IEX
separated at **0.027856**, and the within-vendor control Alpaca-SIP vs Alpaca-IEX
separated at **0.027761** — same vendor, same host, same request, one parameter
changed, which removes every explanation for a separation that is not the tape,
**including this repository's own window arithmetic**. The measurement window is
**not** the registered pre-period carve-out, because **neither credential serves
it** (Massive `403`, Alpaca `200` with 0 bars); the five sessions used sit
**strictly after `holdout_end`**, outside both registered windows. **The carve-out
boundary is unmoved and was not widened** — the sealed comparator is already the
registered exception and is not window-limited.

---

## ADR-022: The two feeds share an upstream, and the agreement gate is scoped accordingly

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 4, REGISTRATION.md
Amendments 7 and 8

**Context.** The agreement gate exists because of Concretum: **identical
opening-range code, four vendors, identical dates, parameters and starting
capital, final portfolio values from 226,000 to 726,000 USD** — a threefold
spread from vendor choice alone (**carried**, C-13). **That spread is a spread
across upstreams.**

**Decision.** Record, **before the agreement figure exists**, that this pair does
not run that test. The evidence is the **tightness, not the level**: the IQR of
the Massive-against-Alpaca-SIP first-5-minute volume ratio is **[1.003096,
1.007726] — 0.46 percentage points wide over n = 100 pairs**. Two independently
constructed consolidations would not agree that closely that consistently; **one
SIP-derived upstream redistributed twice** would. So: **a `PASS` establishes that
two redistributors of one upstream agree. It does not establish that the
first-5-minute high and low are vendor-independent.**

**Alternatives rejected.** *Report the agreement figure without the caveat*: it
would read as the Concretum test and it is not. *Drop the gate as uninformative*:
it still detects a redistribution-pipeline fault, which is a real hazard.
*Acquire a third feed now*: that is an operator action and a possible spend, and
**this repository spends nothing without an explicit instruction**.

**Consequences.** Two scope limits compose and both are registered before the
number exists. **From Amendment 8:** the two feeds overlap only from
**2024-08-29**, giving **459 of 875 holdout sessions and 0 of 1,762 in-sample
sessions**. **From this ADR:** within that overlap the pair scores a
redistribution pipeline. **Together: the gate as it can actually be run
establishes that two redistributors of one upstream agree, on 459 of 2,637
registered sessions.** A third feed on a genuinely different upstream is an
**open operator item**; it does not block the ladder, and Section 11's epistemic
boundary gains a line.

---

## ADR-023: Alpaca is the primary bar vendor and Massive is the reference vendor

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 8 · **supersedes the
provisional recommendation in `docs/ACCESS.md`**, which is left visible

**Context.** `docs/ACCESS.md` recommended **Massive as primary** on **documented**
grounds: the only probed vendor publishing a delisted-ticker reference endpoint
*and* minute aggregates on one host. **Standing rule 4 says the measurement
wins**, and the measurements are now in. The choice is made on the **two
integrity questions and not on price** — both tiers cost zero.

**The measurements the decision rests on.**

| question | Alpaca | Massive |
|---|---|---|
| **serves delisted names with intraday history** | **`PASS` — 203 names measured, n = 229 in-window names checked, share 0.8865** | only inside a 24-month window; **1,171 of 4,731 in-window delisted names, 24.8 percent, is the entire pool it could ever answer for**; 16 of 18 in-window sampled served |
| **retroactively rewrites already-served bars** | **`Absent(not_yet_measured)`** — TASK 9 arms it; the answer needs a ≥ 14-day wait | **`Absent(not_yet_measured)`** |
| measured historical reach | **2016-01-04**, n = 16 probes — **1,762/1,762 in-sample, 875/875 holdout** | **2024-08-29**, n = 16 probes — **0/1,762 in-sample, 459/875 holdout** |
| enumerates delisted names **with a delisting date** | **no** — `/v2/assets?status=inactive` serves 19,189 US equity rows and **carries no delisting date at all** | **yes** — 6,421 rows, 4,731 in-window |
| measured rate ceiling | **not reached**; 25/25 admitted at 134.05/min | **5.00/min**, first refusal at request 6 of 8 on **both** endpoints |
| tape | **`SAME_TAPE`** with Massive, median **1.005197**, n = 100 | same measurement, same n |

**Decision.** **Alpaca is the primary bar vendor. Massive is the reference
vendor.** Neither can do the other's job on the tiers this repository holds, and
the division is a **measured fact rather than a preference**: Massive is the only
vendor that can **enumerate** delisted names with dates, and it can serve the
bars for barely a quarter of them; Alpaca serves the bars across the full
registered window and cannot enumerate delistings at all.

**Alternatives rejected.** *Keep Massive as primary per `docs/ACCESS.md`*: it
serves **0 of 1,762 in-sample sessions**. *Keep Massive as primary and shrink the
registered windows to fit its reach*: **that is the work-around the ladder
forbids** — the windows are pinned in Section 7 and do not move to accommodate a
tier. *Drop Massive entirely*: it is the **only** source of delisting dates, and
without it the universe is survivor-only by construction — the exact failure
BLOCKED-3 exists to prevent. *Buy the Massive Starter tier*: **spend requires an
explicit operator instruction and its own ADR**, and it would buy only the
agreement gate's scope back, not primary collection.

**Consequences, stated in the decision text rather than a footnote.**

1. **The pair carries the same tape and shares an upstream** (ADR-021, ADR-022),
   so the cross-vendor agreement measurement **scores a redistribution pipeline
   rather than two independent feeds**, and **it is not the Concretum test**.
2. **The pair overlaps only from 2024-08-29** (Amendment 8), so the agreement
   gate covers **459 of 875 holdout sessions and none of the in-sample window**.
3. **Alpaca covers the in-sample window with zero margin** — its earliest served
   session is **2016-01-04**, the exact first session of the registered window.
   **One trimmed month of vendor history and the coverage is gone.** This is not
   a comfortable pass and the ADR refuses to record it as one.
4. **The second integrity question is unanswered and this decision does not
   pretend otherwise.** Whether either vendor **retroactively rewrites**
   already-served bars is `Absent(not_yet_measured)`. **A.1 TASK 9 arms the
   clock; the answer arrives no earlier than 14 calendar days later**, and until
   it does **nothing is armed**.
5. **Alpaca refuses at HTTP 200.** It served `200` on **all 260** delisted checks,
   including every name it served nothing for, and `200` with `bars: null` for
   out-of-reach sessions. **On the primary vendor, health cannot be read from the
   status line** — `served` is **status code and bar count**, never either alone.
   This is the third vendor-specific instance of ADR-008 and it is now the
   primary's defining operational hazard.

---

## ADR-024: A vendor filter parameter that is silently ignored is a measurement hazard, not an inconvenience

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 6

**Context.** The delisted enumeration asked Massive for
`delisted_utc.gte=2016-01-04` and `delisted_utc.lte=2026-06-30`. **The filters
were not honoured.** The response carried **1,690 rows outside the window** —
names delisted from 2004 through 2015, and names delisted after 2026-06-30 —
out of **6,421** returned. A caller trusting the filter would have recorded
**6,421 as the in-window count: a 36 percent overstatement**, with no error, no
warning and no status code to notice.

**Decision.** **Apply every window filter client-side**, from fields this
repository holds — here `delisted_utc`, a readable field present on every row.
A vendor filter is a **request for a convenience, never a guarantee about the
response**.

**Alternatives rejected.** *Trust the filter and record 6,421*: the overstatement
is invisible in the response. *Trust it and spot-check*: a spot check that passes
proves nothing about the rows it did not sample. *Report both figures without
choosing*: the registered threshold needs one number, and the correct one is the
one this repository computed.

**Consequences.** **It invalidated the first sample rather than merely annoying
it.** The 120-name draw came from the whole list, so **31 of 120 sat outside the
registered window and outside Alpaca's measured reach** — those names miss on
**reach**, not on **coverage**. In-window: **81 of 89 served, 0.910**.
Out-of-window: **0 of 31, 0.000**. **The 0 of 31 is the confirmation** — coverage
failures scatter, and these align exactly with the reach boundary measured
independently at TASK 5. The sample was re-drawn in-window and **enlarged to
n = 229** rather than scaled up, because **the registered threshold is a count
and a rate multiplied by 4,731 is a synthesized value** that standing rule 5
forbids.

---

## ADR-025: A response body is recorded verbatim only when it is a refusal

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 3, recorded as a deviation
at `progress.md` Entry 11

**Context.** The first credentialed probe round recorded `body_redacted` for
**every** response and printed it to the console. For three probes those
fragments contained **OHLCV values**. Under the blindness field lists,
`open`, `high`, `low`, `close` and `volume` are **never readable outside a sealed
writer**, and a report file is not a sealed writer. **Guard 5 cannot catch this
class**: it walks parse trees for **field names in source**, and a value that
only ever appears inside a runtime string is invisible to it.

**Decision.** An asymmetric recording policy, in code rather than in care, at
`tools/_a1r.py::record_body`: **a refusal is recorded verbatim; a served payload
is not recorded at all.** The asymmetry runs on **status code**, which is itself
a readable field. A served payload records **byte count, SHA-256 and bar count**
instead — all three readable — and the bar count is computed by
`orb.comparator.count_bars` **inside the sealed comparator**, so exactly one
module in this repository turns vendor bytes into anything at all.

**Alternatives rejected.** *Truncate the fragment shorter*: a shorter fragment
still carries bars. *Filter priced keys out of the recorded body*: that requires
naming priced fields outside a sealed module, which Guard 5 correctly forbids.
*Record nothing at all*: `docs/ACCESS.md` exists to carry refusal payloads
verbatim, and **A.1 TASK 5's reach boundary and A.1 TASK 7's ceiling are both
verbatim refusal strings** — deleting them would delete the evidence.

**Consequences.** The sessions touched before the fix were **2015-06-01**, inside
the pre-period carve-out and **served nothing by either vendor**, and
**2026-07-15**, **after `holdout_end` = 2026-06-30** and therefore outside both
registered windows. **No bar from either registered window was read or
recorded**, and the reports were rewritten under the new policy **before the
commit**, so **no bar value is committed**. `count_bars` returns `0` for a
refusal, an unparseable body **and** a served empty set, and **the caller
separates those three by status code, never by the count** — standing rule 7,
enforced by the shape of the function rather than by its documentation.

---

## ADR-026: An unreached ceiling is recorded as absent, never as a large number

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 7, REGISTRATION.md
Amendment 9

**Context.** A.1 TASK 7 measured Massive's ceiling at **5.00 requests per
minute** — first refusal at request **6 of 8** on both endpoints, `n = 16` — and
ran Alpaca to **25 of 25 admitted at 134.05 per minute with zero refusals**.
Alpaca's limiter was **never reached**.

**Decision.** `MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` is **`None`**.
*"The ceiling was not reached"* is a **different claim** from *"there is no
ceiling"* and from *"the ceiling is 134"*, and it is recorded as its own value.
The operating pace for such an endpoint comes from **half the highest observed
admitted rate**, and `orb.vendors.PACE_BASIS` states, per endpoint, whether the
figure rests on a **measured ceiling** or an **observed admitted rate**.

**Alternatives rejected.** *Record 134 as the ceiling*: it is a rate that was
admitted, not a rate that was refused, and recording it as a ceiling would make
an unmeasured figure look measured. *Escalate until Alpaca refuses*: the
measurement's purpose is a safe operating pace, and 60 per minute is already far
more than any registered task needs — **escalating further would buy a number
this repository has no use for at the cost of hammering a vendor**. *Use the
documented 200*: documented, never measured.

**Consequences.** `test_the_operating_pace_is_at_most_half_the_measured_ceiling`
walks every endpoint **with** a measured ceiling and fails if one is paced above
half of it; endpoints with `None` are skipped by construction and are covered
instead by `test_an_unmeasured_endpoint_is_never_paced_faster_than_a_measured_sibling`.
**Amendment 2's prediction held and is recorded as having held**: the 88.4 per
minute measured against a 401 overstated the authenticated ceiling by **17.7×**,
and an operator pacing from it would have been **refused on 3 of every 8
requests**.

---

## ADR-027: The pre-period carve-out is amended two-sided, and the direction of the compromise is recorded

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 1, REGISTRATION.md
Amendment 11 · **supersedes ADR-012 in scope, not in method**

**Context.** ADR-012 registered a one-sided carve-out: power inputs may read bars
stamped **strictly before** 2016-01-04T14:30:00.000Z, enforced at one site with
the boundary in one place. **Measurement falsified the assumption it rested on.**
A.1 TASK 5, `n = 16` reach probes per credential: **Alpaca serves from
2016-01-04** — *exactly* `CONFIG.in_sample_start` — and **Massive from
2024-08-29**. `n = 2` credentials, **0 serving** any session before the boundary.
**The carve-out was never reachable**, and E2 power was recorded
`Absent(not_served)` rather than computed.

**Decision.** The carve-out becomes **two-sided**: strictly before
`CONFIG.pre_period_end_ms`, **or** at or after `CONFIG.post_holdout_start_ms` =
**2026-07-01T04:00:00.000Z**, which is 2026-07-01T00:00:00.000 US Eastern (EDT,
UTC−04:00). **The pre-period half is retained unweakened**, not deleted, even
though measurement shows it empty. **Both halves are enforced at the same single
site** — `orb.preperiod` — under the **same names**, which are already pushed and
are not renamed: `require_pre_period` and `gate_pre_period` delegate to a
two-sided `require_carve_out`, and `is_pre_period` keeps its exact original
meaning for the `PRE_PERIOD` provenance check.

**The cost is registered rather than argued away.** The post-holdout region sits
outside both registered windows, so reading it leaks no observation any verdict
is computed on — **and it is not equivalent to the original boundary.**
Dispersion estimated after 2026-06-30 reflects a **later** regime than the sample
it is applied to; a pre-2016 estimate would have reflected an **earlier** one.
**Neither is neutral. The compromise now runs forward rather than backward**, and
the figure **may misstate in-sample dispersion in either direction by an amount
this repository has not measured and does not claim to bound.** Every E2 figure
derived from it carries that sentence attached.

**Alternatives rejected.** *Leave the carve-out one-sided and keep E2 `Absent`
forever*: the only vendor that could serve it would have to reach before
2016-01-04, no such credential exists, none is planned, and the co-primary would
be permanently unpowered on an accident of vendor entitlement rather than on the
world. *Read a slice of the in-sample window instead*: that is reading the
outcome to plan the test of the outcome, which is the exact thing the carve-out
exists to prevent. *Invent a dispersion figure or carry one*: it would register a
number this repository did not measure — the NPLExperiment failure. *Set the
second boundary at UTC midnight*: UTC midnight on 2026-07-01 is **20:00 Eastern
on 2026-06-30**, inside the last holdout session date, and would admit that
session's after-hours bars.

**Consequences.** `CONFIG.post_holdout_start_ms` joins `pre_period_end_ms` under
**three** structural guards: neither literal is typed outside `config.py`,
neither is read from config outside `preperiod.py`, and **`preperiod.py` must
read both**. **Four boundary fixtures sit exactly on the four edges** and all four
are exercised; the sealed interior is swept separately at the first and last
session of each registered window. **Mutation 13** moves the post-holdout fixture
off its edge and the suite goes green, recording a fixture that stopped binding.
`orb.bars.Provenance` gains `POST_HOLDOUT`, validated at construction — it widens
nothing, it names a region the amended carve-out already permits. **The
post-holdout region grows as real time advances and never intersects a registered
window**, and the sessions used in any computation are recorded in the
append-only ledger at the time of that computation.

---

## ADR-028: The in-sample window is single-sourced, and that is a registered scope limitation rather than a verdict input

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 2, REGISTRATION.md §11.1
SL-3 and Amendment 12

**Context.** A.1 TASK 5 measured historical reach on both credentials, `n = 16`
probes each. The reference vendor's tier serves nothing before **2024-08-29**, so
**cross-vendor agreement covers 459 holdout sessions and 0 in-sample sessions**.
**All 1,762 in-sample sessions rest on a single unverified feed.** Until this
ADR, that fact lived only as an input field on a verdict record —
`cross_vendor_overlap_in_sample_sessions: 0` — and as one clause of a table row.

**Decision.** It is registered as **SL-3**, a numbered scope limitation in
Section 11, the epistemic boundary, and mirrored in the `HYPOTHESES.md` H1 entry.
**The consequence for the verdict is stated before any read exists: a PASS
computed on the in-sample window is conditional on a single vendor's rendering of
that window being faithful, and this repository holds no measurement supporting
that condition.** Any in-sample figure is reported with the limitation attached
**in the same sentence**, on the same terms standing rule 13 attaches an n.

**The exposure has a measured size in the literature and none here.** Concretum
Research: **226,000 to 726,000 USD** final equity across **four vendors** on
identical opening-range code, dates, parameters and starting capital (carried,
C-13). **That is the risk a cross-vendor measurement exists to bound, and it
cannot currently be bounded for the in-sample window.**

**Alternatives rejected.** *Add a Section 0 branch that fires on it*: a scope
limitation says what a verdict **means**; it does not change **when** one fires,
and adding a branch would have made an epistemic fact into an operational one.
*Weaken or requalify the existing branches*: the registration forbids it and the
diff shows `src/orb/section0.py` untouched. *Leave it in a verdict input field*:
a fact that changes what a PASS means belongs in the section about what a verdict
supports, not in a field a later reader has to notice. *Choose between the two
retirement routes*: both cost something the assistant cannot spend — money, or
the operator's acceptance.

**Consequences.** Two routes are recorded without choosing between them and
without spending: **(a)** a reference credential whose tier reaches **2016-01-04**,
which retires SL-3 **on measurement**; **(b)** **explicit operator acceptance**
that the in-sample window is single-sourced, which retires nothing by measurement
and is **a decision, not a finding**. Both are carried to the open operator items
of `docs/HANDOVER.md`, which go from two to three. **Neither blocks the ladder
and neither is a precondition for the 2026-09-12 re-pull.**

---

## ADR-029: The consolidated tape is a guarded config field, and a non-consolidated feed needs a stated reason

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 3, REGISTRATION.md
Amendment 13

**Context.** The feed was a **function default** — `feed: str = "sip"` at
`src/orb/vendors.py` line 259. **The default was correct**; every call site
passed or inherited it. The defect was structural: **nothing made a call site say
which tape it wanted**, so nothing would have noticed one that said the wrong
thing. A.1 TASK 4 measured what the wrong branch costs: the single-venue feed
carries a **median 0.027761 of consolidated first-5-minute volume over `n = 100`
pairs**, IQR [0.021200, 0.037068], **100 percent of pairs below the registered
0.20 threshold**.

**Decision.** `CONFIG.consolidated_feed = "sip"`, under the existing parse-tree
config guard. `alpaca_minute_bars` takes `feed` **with no default** and validates
it against the configured value. **`alpaca_minute_bars_on_feed` is the only
builder that may request a non-consolidated feed, and it requires a non-empty
`tape_control_reason`** — an exception with no reason recorded at its call site
is a default wearing a different name. `VendorRequest` carries the feed, manifests
record it, and `require_manifest_feed` refuses a manifest that omits it **before
the first re-pull request is sent**.

**Alternatives rejected.** *Keep the default and add a comment*: a comment does
not fail a build. *Refuse every non-consolidated request outright*: the Amendment
7 tape control **must** request the single-venue feed to measure how far it sits
from the consolidated one, and a rule that forbids the measurement that justifies
the rule is not a rule. *Guard only `src/orb`*: a default is overridable **at a
call site**, and the call sites live in `tools/`, so the guard walks both.

**Consequences.** Five parse-tree guards and three runtime tests. **Mutation 14**
flips the configured value to the single-venue feed and is **caught by
`test_the_configured_feed_is_the_consolidated_tape`** — a guard, not a number
that merely moved. **The sealed probe slice's feed is confirmed by measurement
rather than assumed**: `n = 8` chunks re-requested on **both** feeds, 7
discriminating, **all 7 sealed bar counts equal to the consolidated count and
none to the single-venue count**, 480 bar files on disk against 480 in the
manifest, 737,507 bars. One chunk served **0 bars on both feeds** and is recorded
as **uninformative and excluded rather than counted** — the first run counted the
`0 == 0` tie as a match to the single-venue feed and returned `NOT_CONFIRMED`,
and **the classifier was fixed rather than the verdict**.

---

## ADR-030: The Alpaca ceiling is re-measured, and a burst allowance is not a sustained rate

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 4 of the amendment pass,
REGISTRATION.md Amendment 14 · **supersedes one rejected alternative of ADR-026**

**Context.** ADR-026 recorded Alpaca's ceiling as `None` and **rejected**
escalating further, on the grounds that *"escalating further would buy a number
this repository has no use for at the cost of hammering a vendor."* **Two things
changed.** ADR-023 made **Alpaca the primary bar vendor**, so its ceiling is now
the one that governs collection rather than a spare vendor's; and an operator
instruction asked for the measurement. **ADR-026 is not edited. This ADR
supersedes that single rejected alternative and nothing else in it.**

**The registered protocol could not have reached the ceiling, and the reason is
structural.** The A.1 TASK 7 cell **requested** 0.2 s spacing — 300 per minute —
and **achieved 134.05**. A sequential client sends at most `60 / latency` per
minute whatever spacing it asks for, and the documented figure is **200 per
minute**, so **a single-threaded escalation cannot attempt the documented limit,
let alone exceed it.** Escalating spacing further measures latency.

**Decision.** The escalation gains **bounded concurrency cells** — 2, 4 and 8
workers — after the sequential ones, each stopping at its **first** refusal, with
the request ledger charged **before every send, under a lock**, so the registered
daily cap holds across workers exactly as it holds sequentially. **And the result
is recorded as two different quantities, because it is two different
quantities:**

- **A measured burst allowance**: `n = 391` sent, **384 admitted**, first `429`
  at cumulative request **385**, elapsed **55.96 s**,
  `{"message": "too many requests."}`. **The whole escalation fit inside one
  rolling minute**, so a token bucket of capacity near 400 refilling at the
  documented 200 per minute produces exactly this observation — and so does a
  hard 411-per-minute limiter. **The measurement does not distinguish them.**
- **A measured sustained lower bound**: after a 75 s cooldown, **250 of 250
  admitted over 75.10 s** at a scheduled 200 per minute, **0 refusals**,
  **199.73 per minute**. **The sustained ceiling is at or above that and is not
  known exactly.**

`MEASURED_CEILING_PER_MINUTE["alpaca:bars"]` therefore **stays `None`**.

**Alternatives rejected.** *Record 411.72 per minute as the ceiling*: it is the
rate over a window shorter than the limiter's own period, and recording it would
be **ADR-026's error running in reverse** — turning an unmeasured quantity into a
large number. The tool's first analysis pass did exactly that, proposing an
operating pace of **689.37 per minute**, and it was corrected before anything was
registered. *Write 199.73 into the ceiling dict*: a lower bound is not a ceiling,
and the test now refuses it explicitly. *Pace from the documented 200*:
documented, never measured. *Leave the pace at 60 per minute*: the pace is
derived from the measurement, and the rule is half the maximum rate **actually
attempted**, which is now 199.73 rather than 134.05.

**Consequences.** `CONSERVATIVE_SPACING_S["alpaca:bars"]` moves to **0.61 s =
98.36 per minute** — half of 199.73 with the spacing rounded **up** so the pace
lands below the half figure. **The three unmeasured Alpaca endpoints keep 1.0 s**:
pacing is per endpoint, never per host (solattn ADR-021), and a measurement on
one licenses no change to a sibling.
`test_an_unmeasured_endpoint_is_never_paced_faster_than_a_measured_sibling` was
**rewritten from a proxy to the rule** — it asserted *every endpoint of a vendor
shares one spacing*, which held only while no endpoint had been measured on a
rate. **One further figure was falsified in passing**: the A.1 TASK 7 **134.05
per minute** was that moment's latency and not a limiter, since the **identical**
request shape achieved **223.16 per minute** today, `n = 25`. **The Alpaca daily
cap moves 2,000 → 3,000 as a circuit breaker**, not from any measured daily
allowance, and the operational trigger — this pass's own spend — is recorded
plainly rather than dressed up.

---

## ADR-031: The carve-out dispersion writer returns two scalars, and a refusing cost model is bracketed rather than weakened

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 5, REGISTRATION.md
Amendment 15

**Context.** Amendment 11 made a region readable that had never been readable
before, and Section 9 needs a per-trade dispersion figure from it. **Two problems
arrived together.** First, computing that figure means running the registered
Section 2 selection, the Section 3 entry, stop and exit and the Section 6 cost
model over **real bars**, before the Stage C latch, in a repository whose whole
discipline is that this does not happen. Second, **the frozen Section 6 cost
model refuses every trade**: A.2 TASK 2 measured the SEC Section 31 rate at
0.0000206 per dollar and **did not measure its effective date**, so the schedule
is empty and the model refuses rather than take a fee from the wrong year.
`sec.gov` returned **403 Request Rate Threshold Exceeded** on two further
attempts here, `n = 4` across two sessions, and the stored IBKR schedule carries
the rate with **no effective date anywhere on the page**.

**Decision, part one — the contract.** `orb.dispersion` is a **latched module and
a sealed writer at once**. It reads priced fields, because an opening-range rule
is a statement about highs and lows, and it **returns exactly two `float` scalars
and integer counts**: the standard deviation of net PnL **per share**, and the
realized trigger rate. **The mean is deliberately absent.** A mean net PnL *is*
the outcome this repository is blind to; a dispersion is not — so the two-scalar
contract does not merely limit an interface, it **keeps the outcome sealed even
inside a region the carve-out permits reading**. Per share rather than per trade
in dollars, because Section 4 registers a risk fraction and **no equity level**,
so a dollar figure is defined only up to an arbitrary scale.

**Decision, part two — the bracket.** The registered figure under the frozen
model is reported as **`Absent`**, `n = 550` trades refused. Beside it, the
**one** unmeasured component is varied across **both ends of a bracket** with
everything else held frozen: **zero**, because a fee cannot be negative — a fact
about arithmetic, not an assumption about the world — and **0.0000206**, the one
rate measured. **The bracket came out 0.0084 percent wide**, so the unmeasured
effective date **does not matter for this figure, and that is measured rather
than hoped.**

**Alternatives rejected.** *Report only `Absent` and leave E2 unpowered*: the
absence is real and is reported, but a bracket whose two ends agree to one part
in ten thousand is **evidence**, and withholding it would be as much a choice as
inventing a number. *Invent or carry an effective date*: the NPLExperiment
failure, and precisely what `costs_registered.py` was written to refuse. *Drop
the SEC fee from the model*: that is inventing an effective date with extra
steps. *Return the trade series and let a caller compute the dispersion*: the
series is the outcome. *Make the writer a sealed module rather than a latched
one*: `test_every_latched_module_exists_and_is_named` requires the two sets to be
**disjoint**, and this module must import `orb.universe` and `orb.signal`, which
only a latched module may do.

**Consequences.** `dispersion.py` joins `LATCHED_MODULES`, so **no module in
`src/orb` may import it** and its only entry point is a tool.
`test_the_dispersion_writer_returns_two_scalars` checks **both** the return
annotations and the record's field types — exactly two `float` fields, every
other field an `int`, and no field named `mean`. **Mutation 15** adds a
trade-list return and is caught by it. The boundary is enforced **per bar**
through the two-sided `require_pre_period`, and every bar carries
`Provenance.POST_HOLDOUT`, validated at construction. **That fixture caught
mutation 13 on its next run** — the post-holdout edge is now pinned twice, and
mutation 13 is `expect_green=False` as a result. **One test fixture was caught by
a registered filter rather than by an assertion**: the first draft built sessions
with a 0.20 USD range and evaluated nothing, because the registered 14-session
ATR filter requires **above 0.50 USD**. The fixture was wrong and the filter was
right.

---

## ADR-032: Section 8 is a conjunction, so each co-primary runs at the full nominal level

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 1 of the inference-repair
pass, REGISTRATION.md Amendment 18 · **supersedes ADR-005 on the arithmetic, not
on the judgement**

**Context.** Section 8 registers *"Two co-primaries, one-sided, and **both must
pass**"*, and then applies `alpha_adj = 1 − 0.95^(1/2) = 0.02532057` to **each**.
Those two sentences do not agree. `1 − 0.95^(1/k)` is the **Šidák** correction for
a family-wise error rate under a **union** rule, where the family succeeds if
**any** component rejects. **Section 8's rule is a conjunction.**

**Decision.** **Each co-primary runs one-sided at `alpha = 0.05`.** Section 8's
rule is an **intersection-union test**, and **Berger (1982)** — *Multiparameter
hypothesis testing and acceptance sampling*, `Technometrics` **24(4), 295–300** —
establishes that an IUT whose components each run at level `a` has **overall size
at most `a`**, with no correction owed. The argument is one line and is written
into the registration rather than cited: under the global null, the event that
**all** components reject is a **subset** of the event that **any single one**
does, so `P(all reject) <= P(component 1 rejects) = a`.

Registered as `CONFIG.per_test_alpha = 0.05`, read through
`orb.verdict.per_test_alpha()`.

**Alternatives rejected.** *Keep 0.02532057 as a conservative choice*: it is not
a choice, it is a correction for a different rule, and a registration that pays
an unowed penalty is misdescribing its own severity — a later reader would take
0.7435 as what the design can detect when the design could detect 0.8325.
*Remove `alpha_adj`*: it is already pushed, it is **correct for the rule it
describes**, and deleting it would remove the evidence that the error was an
error rather than a preference — its test now names which question it answers.
*Also loosen the deflated-Sharpe deflation*: **rejected outright.** The DSR's
correction is for the **8 registered parameterization trials**, four range
lengths crossed with two entry rules. **That is a different multiplicity** — the
number of ways the rule could have been *specified* — and it is untouched.
*Treat the correction as licence to move a threshold*: no bar, gate or
assumption moved.

**Consequences.** **E1 at the registered 1.40 Sharpe assumption on the achievable
holdout moves 0.743521 → 0.832450, and the minimum n for 80 percent power falls
1,006 → 795 against 875 achievable — a shortfall of 131 becomes a surplus of
80.** **No datum changed**; a power shortfall reported in every document since
the first commit was an artefact of the wrong correction. **ADR-005 registered
that shortfall openly rather than meeting it at the read, and that judgement was
right on the facts as they stood** — this ADR supersedes its arithmetic and
leaves ADR-005 unedited, per the rule that a reversal is a new ADR. **E1 is one
of two co-primaries under a conjunction, so 0.832450 is not the design's power**;
ADR-034 and Section 10.1 make joint power the operative figure.

---

## ADR-033: E2 is replaced with a pessimistic-cost economic null, because the old one could not fail on cost

**Date:** 2026-08-29 · **Status:** accepted · A.0 TASK 2 of the inference-repair
pass, REGISTRATION.md Amendment 19

**Context.** Amendment 15 measured that **E2 power equalled E1 power to between
1e-05 and 1e-12** at every assumption and horizon. The cause is arithmetic:
E2's implied per-trade mean was derived from the same Sharpe assumption E1 uses,
so `implied_mean / annual_sharpe` was a **constant 0.02884727** and E2's effect
size was a **linear rescale of E1's**. **Under a conjunction, a co-primary that
is a rescale of the other is not a second hurdle** — whichever rejects first,
both do.

**Decision.** **E2 tests whether mean net PnL per trade remains above zero when
every slippage leg is set to the pessimistic end of the band Section 6 registered
before any data existed** — 0.040 entry, 0.080 stop exit, 0.020 close exit,
against the central 0.020, 0.040, 0.010. **Null: the pessimistic-cost mean is at
or below zero.** One-sided at 0.05, permutation on session labels clustered by
session date, the same clustering as E1.

**Alternatives rejected.** *Repair E2's parameterization*: any null of the form
*"the mean is positive at central costs"* sits **inside E1's alternative**,
because it is the same claim in different units. **The null has to change, not
its parameterization.** *Drop E2 and run a single co-primary*: that would remove
the only place cost can independently fail the design, which is the failure mode
Section 1's structural doubt 2 names as the most likely one. *Use the optimistic
end as a second null*: it tests nothing the central case does not.

**Consequences.** **The per-trade dispersion stops cancelling.** The pessimistic
shift is an **absolute dollar quantity per share**, so E2's effect size is
`(central_mean − shift) / dispersion` and a constant subtraction does not divide
out. **The A.1 TASK 5 dispersion measurement of 2.029585 USD per share becomes
load-bearing, having been inert under the old E2.** The shift itself depends on
the realized **stop-versus-close mix**, which was an assumption until ADR-035
measured it. **The amendment was written and committed before the shift was
measured**, and it pre-registers what a collapse would mean — so the collapse
ADR-034 records cannot read as a rationalisation. **The rationale, in the
registration's own words: the dominant failure mode across this program is cost
absorbing a real directional edge, the independent replication found a 0.070
USD/share gross edge dying at 0.022 USD/share of entry slippage (carried, C-6),
and an inference design that cannot fail on cost is not testing the thing most
likely to be true.**

---

## ADR-034: The latch condition is joint power, and it collapsed

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 4 of the inference-repair
pass, REGISTRATION.md Section 10.1 and Amendment 21

**Context.** Section 10 clause 1 read *"Both co-primaries at or above 80 percent
power at achievable N"* — a **per-component** condition. Section 8 asserts the
claim only if **both** reject, so the quantity the latch needs is **the
probability that both reject**, and that is **not implied by either component
power**: two components at 0.80 each can be jointly anywhere from **0.60** to
**0.80** depending on their dependence.

**Decision, part one.** **Clause 1 is restated as a JOINT condition** in Section
10.1, appended with clause 1 left standing. **Joint power is bounded above by the
smaller component power, unconditionally** — `P(A and B) <= P(A)` and
`P(A and B) <= P(B)`, needing no dependence assumption and admitting no escape
from one. `orb.power.joint_power` returns the bound, the Fréchet lower bound and
the **binding component by name**, so no caller can report the larger component
as the design's power.

**Decision, part two — the finding, recorded rather than routed around.** **The
measured pessimistic shift of 0.041455 USD per share exceeds the implied central
mean of 0.040386 at the registered 1.40 Sharpe assumption.** The
**pessimistic-cost mean is −0.001068 USD per share — negative**. E2's alternative
lies **inside its own null**, **E2 power is 0.043277 on the achievable holdout —
below the 0.05 size of the test — and joint power collapses to 0.043277 with no
session count reaching 80 percent at any sample size.**

**Alternatives rejected, each because it would have rescued a figure rather than
reported one.** *Adjust the cost band*: Section 6's pessimistic figures were
registered before any data existed and using them is the point. *Adjust the
effect assumption*: 1.40 is half the published 2.81 for the decay reasons ADR-005
registered, and moving it to clear a bar would be choosing the answer.
*Adjust the alpha*: 0.05 was fixed by ADR-032 **before this table existed**, for
a reason unrelated to it. *Substitute a weaker E2*: the null was fixed by ADR-033
before the shift was measured. *Clamp a negative power to the size of the test*:
`e2_power_pessimistic` returns the figure below `alpha` because that is the true
answer, and clamping would hide exactly what the amendment exists to surface.

**Consequences.** **Two questions now have different answers and the verdict
record keeps them in separate fields**: the corrected alpha **does** move E1
across its 80 percent bar (0.743521 → 0.832450, min n 1,006 → 795), and **joint
power does not** (0.043277, min n unreachable). **Correcting the multiplicity
error made E1 powered and left the design unpowered.** The margin is measured
because the operator's decision turns on it: **the break-even Sharpe is 1.437035
and the registered 1.40 sits 2.577 percent below it**; the break-even stop share
is **0.346206** against a measured **0.381818**. **Three routes are handed to the
operator and none is chosen here** — a narrower verdict scope with E2 demoted to
a named secondary, a cost band narrowed on execution evidence this repository
does not hold, or closure as **`untestable-at-achievable-power`**, the fourth
closure kind already in the house record. **None of the three depends on the
2026-09-12 bar-integrity calendar.**

---

## ADR-035: The ambiguous rate is measured at zero, and a zero is reported with its bound

**Date:** 2026-08-29 · **Status:** accepted · A.1 TASK 3 of the inference-repair
pass, REGISTRATION.md Amendment 20

**Context.** Section 2 **excludes** name-sessions where both the opening-range
high and low are crossed inside the same one-minute bar, because the minute
cannot say which came first and this repository refuses to guess. **The size of
that exclusion had never been measured.** At a trigger rate of 0.982143 it could
have been material, and an exclusion that removes a large share of the sample is
a scope limitation whether or not anyone notices.

**Decision.** Measure it inside the sealed writer alongside the stop-versus-close
mix, on the same post-holdout carve-out, and **report a zero count with its
uncertainty rather than as a certainty**. **Measured: 0.000000, `n = 560`
selected name-sessions, 0 events.** By the **rule of three**, a one-sided 95
percent upper bound on a rate observed zero times in 560 is **3/560 ≈ 0.0054**.
**The registered exclusion removes at most about half a percent of the sample on
this slice, and removed none of it.** The operator's 10 percent threshold was not
crossed, **so no scope limitation is raised and the exclusion rule is
unchanged.**

**Alternatives rejected.** *Report 0.000000 without a bound*: a zero count at
`n = 560` is not evidence that the rate is zero, and reporting it bare would
invite exactly that reading. *Widen the ambiguity definition to produce a
non-zero rate*: that would change a registered rule to make a measurement more
interesting. *Read the exit mix off priced trades, as A.1 TASK 5 did*:
**rejected, and this is the substantive part.** The frozen Section 6 model prices
**nothing** — its SEC Section 31 effective date is unmeasured — so that route
would have returned a stop share of **0.0** and a pessimistic shift of **0.030**,
**understating the shift by 0.011455 USD per share on every trade, silently**.
The mix is read off the Section 3 stop and close rules directly, and
`test_the_mix_is_read_off_the_bars_and_not_off_priced_trades` pins it.

**Consequences.** The measured **stop-exit share of 0.381818, `n = 550`**, gives
the **pessimistic shift of 0.041455 USD per share** that ADR-034's collapse turns
on, between hard arithmetic bounds of **0.030** all-close and **0.060** all-stop.
The writer's contract grows a second record, `CarveOutExecutionMix`, carrying
**three `float` measurements and integer denominators** — the four the operator
named plus the n's standing rule 13 requires, **a deviation named in Amendment 20
rather than taken quietly**. **Mutation 16** adds a trade-list return to the new
entry point and is caught by the extended pin.
