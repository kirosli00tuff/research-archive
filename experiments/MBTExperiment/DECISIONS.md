# DECISIONS.md — append-only ADR log

One record per architectural decision. Append only. A superseded decision gets a
new record naming the one it supersedes; the old record stays as written.

```
### ADR-NNN — <title> (<date>)
**Context.** What forced the decision, with its measurement and n.
**Decision.** What was chosen.
**Consequence.** What this costs and what it forecloses.
**Alternatives rejected.** Named, with the reason each lost.
```

---

### ADR-001 — The COST ceiling rests on the most recent quarter, not the full sample (2026-09-03)

**Context.** VRPExperiment's handover derives a 49.610 bps ceiling from half the
BTC premium's full-sample one-sided 95% lower bound of 142.740 bps (n = 1,955)
less the measured p90 commission of 21.760 bps. The same repository measured that
premium **decaying monotonically across all four quarters, 284.53, 250.59,
145.13, 112.72 bps, a 60.4% fall, at n = 488, 488, 488 and 491**, and states
plainly *"Do not read the BTC premium as stationary."* The most recent quarter
does not support the number the bar rests on. This had to be settled **before any
spread was measured**, because choosing after seeing one is the move a
registration exists to foreclose.

**Decision.** **The most recent quarter, giving a ceiling of 34.600 bps.** Both
ceilings are registered in REGISTRATION.md Section 0.6 so the choice stays
visible, and `REGISTERED_PREMIUM_BASIS` names the chosen one in code.

The reasoning is stated in **mechanism terms, not expected-result terms**: a
short variance seller collects the premium **in force over the tenor they hold**,
not the average of the sample's history, and the registered hedging rule holds a
30-day tenor. A monotone decline across every partition is a trend rather than
noise around a stable mean, and **the mean of a trending series describes its
history rather than estimating its next value**. The argument does not rest on
any belief about how wide the MBT spread will prove to be, and would be identical
if the spread were known to be one basis point.

**Consequence.** The bar is 15.010 bps stricter, and the gate is correspondingly
harder to pass. **The two bases are not like for like, and the asymmetry runs
against the choice made**: 142.740 is a one-sided lower bound carrying a
confidence haircut, and 112.72 is a point estimate carrying none, so the swap
changes level and confidence together. The quarterly lower bound is
`Absent(not_recorded)` in the closed repository and is not computed here, because
that would re-read a spent sample.

**The direction of the gap is known and is the safe one.** A one-sided lower
bound never exceeds its point estimate, so a like-for-like quarterly basis would
give a ceiling **at or below** 34.600 bps. The registered ceiling is an **upper
bound on the like-for-like ceiling**: too generous if anything, never too strict.
A FAIL against it would be a FAIL against the stricter figure too.

**Alternatives rejected.** *The full-sample basis (49.610 bps)* lost because it
assumes a stationarity its own sample refutes. *Computing the quarterly lower
bound* lost because it requires re-reading VRPExperiment's spent 1,955-day sample,
which the boundary forbids. *Deferring the choice until a spread existed* lost
because that is precisely the post-hoc selection the registration forecloses, and
the 15.010 bps gap is wide enough to decide the gate on its own.

---

### ADR-002 — Guard one is shaped by a measurement of the broker API, not by the registered wording (2026-09-03)

**Context.** `CLAUDE.md` rule 1 requires that *"every `placeOrder` call site must
carry `whatIf=True`"*. Measured against the locked `ib_async 2.1.0`:
`IB.placeOrder(contract, order)` **transmits and accepts no `whatIf` keyword at
all**. The flag is a field on the `Order` object, and `IB.whatIfOrder` copies the
order, sets `whatIf = True`, and previews.

**Decision.** Implement the rule where the flag genuinely lives, in three parts.
**No transmitting call site exists in the package at all.** The set is empty
rather than guarded. **Every order construction carries `whatIf=True` as a
literal.** **Every call of the package's own preview wrapper carries it as a
literal.** All three fail on a missing flag, a `False` literal, and a
non-literal.

**Consequence.** The guard is stronger than the wording it implements: a call
that cannot be written cannot be misconfigured. It also diverges from the literal
text of the rule, which is recorded here so a later reader does not read the
divergence as drift. **Writing `whatIf=True` onto `placeOrder` would have been
theatre**: the method does not read one and would transmit anyway, and a guard
that checks a flag the callee ignores is worse than no guard, because it reads as
protection.

**Alternatives rejected.** *Literal compliance* lost for the reason above.
*Guarding only construction* lost because an order can be mutated after
construction, which the AST cannot see, so `what_if_order` checks the object
again at the moment of use.

---

### ADR-003 — The three provenance kinds are separated, and admissibility branches on the kind (2026-09-03)

**Context.** The paper-only clause blocks the two gates unequally. A margin is a
property of the **account**, a commission report of the **fill**, and a quote of
the **market data feed**. Treating "paper" as one blanket state would either
block the census that is genuinely collectible or admit a margin that is not.

**Decision.** `ProvenanceKind` carries MARGIN, QUOTE and COMMISSION_REPORT, and
`gates.require_admissible` branches on the kind. MARGIN and COMMISSION_REPORT are
live-only. QUOTE is admissible from paper **when the tick is real-time**, and
every such result carries a `DOCUMENTED, NOT MEASURED` note in its
`admissibility_note` field.

**Consequence.** The label travels **with the number** rather than living only in
a document, so a downstream reader meets it. The paper-quote admissibility is a
**claim** resting on IBKR routing market data by subscription rather than by
account type, with its falsifiers registered in Section 0.5, and it is
re-verified against a live session whenever one appears.

**Alternatives rejected.** *One blanket paper flag* lost because it cannot express
the asymmetry the clause actually has. *Treating the paper-quote claim as
measured* lost because nothing here measured it, and measured beats documented.

---

### ADR-004 — Window distinctness is fixed in clock terms, which makes the census clock-bound (2026-09-03)

**Context.** VRPExperiment 4.1 requires *"at least 20 distinct observation
windows"* and does not define distinct. A count-based reading permits 20 samples
in one afternoon, which measures one book state twenty times.

**Decision.** **At least 60 minutes between windows, and at most 4 windows from
any one UTC calendar day.**

**Consequence.** 20 windows need **5 collection days minimum**, so the census is
clock-bound and cannot be compressed by any amount of effort. The rule fixes the
**duration** and not the **start**, so the projection runs from the first day a
session exists; `tools/census_projection.py` computes it from a start date rather
than hard-coding one that would go stale.

**Alternatives rejected.** *A count-only rule* lost because it permits an inflated
`n` over one book state, making a 90th percentile look better determined than it
is. *Tighter spacing with no per-day cap* lost because the p90 would then describe
the tail of a single session rather than the tail across sessions.

---

### ADR-005 — Both chain tie rules are fixed as arbitrary, and the registration says so (2026-09-03)

**Context.** Two implementer choices decide which straddle is measured, and each
produces a valid-looking straddle either way: the at-the-money strike when two
are equidistant, and the 30-day expiry when two are equidistant.

**Decision.** The at-the-money reference is the **hedge future's touch midpoint**.
The strike tie goes to the **lower** strike. The tenor is measured to the
**settlement instant**, not to midnight, and its tie goes to the **longer**
expiry.

**Consequence.** The reference rule has a mechanism: a strike chosen against
anything other than the instrument that hedges it is not delta-neutral against
that instrument, so the registered rebalance counts would no longer apply. The
tenor tie has one: the registered hedging path is 30 days and the shorter side
truncates it. **The strike tie has none, and the registration says so plainly.**
Two equidistant strikes are equally at-the-money, the choice is arbitrary by
construction, and fixing it beforehand so it cannot be made after seeing which
quotes tighter **is the entire function of registering it**.

**Alternatives rejected.** *Measuring the tenor in calendar days* lost because CME
crypto options settle at a contract-specific time, so two expiries on one date
have different tenors; `tests/test_chain.py` contains a case where the two rules
disagree at 29.75 against 30.458 days, so a silent reversion fails the build.
*Inventing a mechanism for the strike tie* lost because there is not one, and a
manufactured justification would be worse than an admitted arbitrary choice.

---

### ADR-006 — A gate with an absent leg fires on a lower bound, which can FAIL and never PASS (2026-09-03)

**Context.** The COST gate compares option spread plus future spread plus
exchange and regulatory fees against a ceiling. The fee leg is
`Absent(not_served)` for three independent reasons, so the sum cannot be formed:
`Absent` refuses addition, by design.

**Decision.** `gates.fire_lower_bound` fires on the measured legs as a **strict
lower bound**. Above the ceiling it returns **FAIL**, soundly, because every
absent leg is non-negative. At or below it returns **ABSENT**, never PASS.

**Consequence.** **The COST gate can close the question negatively and can never
close it positively while the fee leg is absent.** Combined with the MARGIN gate's
need for a U-prefixed session, **both gates are blocked from PASS for independent
reasons and the stage verdict is over-determined**: fixing the Gateway alone
would not change it. This follows VRPExperiment's own use of its commission-only
bound, which it used as a constraint and never reported as the cost.

**Alternatives rejected.** *Returning PASS when the bound clears the ceiling* lost
because the absent legs are unbounded above by any evidence held here.
*Estimating the fee* lost because it is the estimate the stage forbids, and
because a fee inferred from a rule of thumb would enter a verdict as though
measured.

---

### ADR-007 — The credential exemption is line-scoped behind a marker, not file-scoped (2026-09-03)

**Context.** The honesty scan fired on `tests/test_guards.py` the moment the
suite was tracked, matching the synthetic account shapes its own fixtures use. A
file-wide allowlist was the obvious fix and the wrong one.

**Decision.** A line carrying an explicit synthetic-fixture marker is exempt.
The marker token itself is deliberately **not written in this document**: the
scanner skips any line containing it, so naming it here would create an exemption
in a file that should have none. A second test asserts the marker appears **only**
in the two test files, and a third asserts the exemption does not reach the line
below it. Writing this ADR tripped that first test, which is the guard behaving
as designed.

**Consequence.** **A real account number pasted anywhere in an exempt file still
fails the build**, and claiming an exemption is a deliberate act visible at the
exact line. The cost is that a fixture line must carry a comment, and that ruff's
reflow can move a marker off its line, which happened twice and was caught by the
scan itself.

**Alternatives rejected.** *A file-wide allowlist* lost because it blinds the
scanner to the file most likely to hold a realistic-looking account. *Building
fixture strings from concatenated parts* lost because it evades the repository's
own scanner, which is the pattern the scanner exists to catch.

---

### ADR-008 — The stage verdict is computed from artifacts rather than written by hand (2026-09-03)

**Context.** REGISTRATION.md Section 0.1 registers HARNESS-READY as four
conditions holding at once. A verdict typed into a document can drift from the
evidence beneath it, and drift in that direction always favours the author.

**Decision.** `mbt.verdict.decide` reads each condition from the artifact that
demonstrates it and returns the verdict, exposed as `mbt.cli verdict`.

**Consequence.** The verdict is re-runnable, so the operator sees it change the
moment a condition is met rather than waiting for a document edit. HARNESS-READY
requires all four; three held at the close and **the binding condition is the
known-answer test**, which did not run.
`HARVESTABLE-CONFIRMED` and `VENUE_BLOCKED` are **not representable** in the
enum, because a registered-but-unreachable outcome is an invitation to reach for
it.

**Alternatives rejected.** *A hand-written verdict* lost for the drift reason.
*Treating "census armed" as "census collected"* lost because armed is not
collected, and the condition asks only that the projection exists; the artifact
states the distinction and reports 0 of 20 alongside.

---

### ADR-009 — The mutation harness found a hole nothing else found, and both fixes were kept (2026-09-03)

**Context.** Mutations 1 and 2 flipped and de-literalised the `whatIf` flag on the
package's **only** order construction, and the no-transmit scan **stayed green**.
`build_short_option_order` took the order class as a parameter, so the call site
read `order_cls(...)`, and the scan matched call sites against a list of known
constructor names that did not contain it. Review, `mypy --strict`, `ruff` and
**156 passing tests** had all missed it.

**Decision.** Both fixes, because they close different shapes of the hole.
`broker.py` constructs `Order` **directly**, so the site is covered by name. The
scan additionally holds **any** call carrying a `whatIf` keyword to the literal
requirement, **keyed on the argument rather than on the callee**.

**Consequence.** A constructor reached through a parameter, a factory or an alias
is now covered regardless of its name. The class was injected for testability,
and removing the injection made the test **stronger**: it now exercises the real
`ib_async` `Order` rather than a stub.

**This is the argument for having a mutation harness at all**, recorded because
the lesson is easy to lose: the refusal artifacts showed Guard 1 refusing on
synthetic sources the entire time, while the one real call site sat unchecked. **A
guard can refuse correctly while its test asserts nothing about the code that
matters**, and only mutating real source finds that.

**Alternatives rejected.** *Adding `order_cls` to the constructor list* lost
because it fixes one spelling of a general hole. *Keeping the injection and
guarding by name only* lost for the same reason.

---

### ADR-010 — The venue requires `transmit=True` on a what-if, and the flag was NOT flipped (2026-09-03)

**Context.** Measured on a live paper session: IBKR refuses every what-if this
package can construct, with error 321, *"Error validating request.-'bD' : cause -
What-If order should have transmit flag set to TRUE."* Raised on **4 of 4
products** tried: SPY, the ES front future, the MBT front future and an MBT
option. The request is then never resolved, so the call **hangs** rather than
failing.

`build_short_option_order` sets `transmit=False`, and `what_if_order` **refuses**
an order carrying `transmit=True`. So the package cannot obtain a margin from the
venue on any product, in any environment. **This is the binding half of the
condition that blocked Stage B**, and it moved from the environment into this
harness.

Stage B's own reasoning, recorded in `broker.py`, was that *"a preview never
needs it"*. The venue's validation says a preview is **required** to carry it.
**The standing rule worked exactly as intended: measured behaviour beat
documentation, and the documentation here was this repository's own.**

A second defect sits behind it and would bind next. With `transmit=True` but no
explicit TIF, IBKR warns 10349, *"Order TIF was set to DAY based on order
preset"*, and ends the request with **no `OrderState` at all**. Isolated at
**n = 4 combinations**: TIF unset returns nothing whether or not the account
field is set, and `tif="DAY"` returns an `OrderState` whether or not it is.
**TIF is load-bearing and the account field is not.**

**Decision.** **Record both defects and change neither.** The package keeps
`transmit=False` and keeps refusing `transmit=True`. Permission was measured by a
diagnostic run **outside** the package, so the package's no-transmit property is
exactly as Stage B left it, and the diagnostic script is preserved verbatim under
`reports/task2/` so the measurement is reproducible without becoming package code.

**Consequence.** The known-answer test cannot pass, so the stage closes
**HARNESS-BLOCKED** a second time. That is the intended outcome and not a
shortfall.

**Why this is not a judgement call to make autonomously.** Flipping the flag
would clear the binding blocker, and with an operator margin supplied the stage
would reach HARNESS-READY. **That is precisely why it was not done here.** The
change would weaken the single flag whose purpose is preventing order
transmission, in reaction to what the venue turned out to demand, and the
resulting HARNESS-READY would rest on a safety property rewritten after the fact.
This stage's governing rule names that move exactly: *a second HARNESS-BLOCKED
with a sharper reason is a better outcome than a HARNESS-READY that rests on a
rule rewritten after the fact.*

**The risk the flag actually carries, stated so the operator can weigh it.** With
`transmit=False`, a `whatIf` that somehow became `False` would leave the order
unsent: **two independent failures are needed to transmit**. With
`transmit=True`, one is. The counterweight is that Guard 1 verifies the `whatIf`
literal at build time at every construction site and every wrapper call,
`what_if_order` asserts it again on the object at the moment of use, and
registered mutation 1 breaks the suite when it is flipped. **The decision is
whether one verified barrier is enough where there were two**, and it belongs to
the operator.

**Alternatives rejected.** *Flipping `transmit` to `True`* lost for the reason
above. *Setting `transmit=True` only inside `what_if_order`, after the `whatIf`
assertion* lost because it localises the change without altering the risk
profile, and dressing a safety reduction as an encapsulation improvement is
worse than making it plainly. *Leaving the defect unrecorded until a live
session* lost because the measurement is cheap now and the evidence is complete.

---

### ADR-011 — The census projection runs from a window actually collected, so it is absent (2026-09-03)

**Context.** Stage B recorded the condition *"the census is armed with its
projected completion date"* as **held**, on a projection computed from a
**hypothetical** start, because no session existed and no window could be
attempted. A session now exists, **3 windows have been attempted and all 3 were
refused**, and the stage prompt requires the projection to run from *the first
window actually collected rather than from a hypothetical start*.

**Decision.** `condition_census_armed` reads
`reports/task5/projection_from_first_window.json` and holds **only when a
projected completion date actually exists**. With 0 of 20 windows accepted there
is no first window, so the date is `Absent(insufficient_sample)` and **the
condition no longer holds**.

**Consequence.** The verdict moves from 3 of 4 conditions held to **2 of 4**. The
stage was already HARNESS-BLOCKED on the known-answer test, so this **sharpens
the block rather than changing the outcome**, and it moves *away* from
HARNESS-READY, which is the direction that needs no operator permission.

**Why the stale artifact had to stop being read.** It would keep reporting a
completion date of 2026-09-09 for a census that **cannot begin on any day**,
because the blocker is a missing market-data subscription rather than elapsed
time. **That is exactly the drift a computed verdict exists to prevent**, and a
verdict reading a superseded artifact is a hand-written verdict with extra steps.

**The registered duration is unchanged and is not a completion date.** 20 windows
at the registered cap of 4 per UTC day is **5 collection days**. That figure is a
property of the rule, it is the one ETA in Stage B that held, and it stays
correct. It is not a completion date because there is no start to add it to.

**Alternatives rejected.** *Keeping the hypothetical projection* lost for the
drift reason. *Reporting the condition held because the duration exists* lost
because the registered condition names a completion **date**, and a duration is
not one. *Amending the registered condition text* lost outright: the registration
is closed.

---

### ADR-012 — The client id held the account number, and the loader echoed it (2026-09-03)

**Context.** Found before any measurement was taken. `.env` carried the **paper
account number** in the `MBT_IB_PAPER_CLIENT_ID` slot. The TWS API `clientId` is
an int32, so a 9-character D-prefixed string cannot be one: this was a paste,
not a choice. The stage prompt records the variable as *now set*, and it was set,
to a value that is not a client id.

Two failures followed, and the second is worse. `GatewayConfig.load` passed the
value to a bare `int()`, which raises `ValueError` rather than a `ConfigError`,
so the CLI's absence recording did not catch it and the command died on an
uncaught traceback. **And `ValueError` embeds the string it failed on**, so the
account number reached stderr and would have reached any artifact that captured
the traceback.

**Decision.** Validate the shape in `_require_int`, raise `MalformedConfigError`
(a `ConfigError`), and report **the variable and the observed shape, never the
value**. Set the `.env` client id to `4202`, an integer distinct from AiTrader's
`_DEFAULT_CLIENT_ID = 17`, since CLAUDE.md requires a distinct client id per
environment and TradingView and TWS competing for one Gateway session starve each
other.

**Consequence.** A malformed client id now fails closed with a message that names
the variable and describes the shape, and no credential-shaped value can reach a
log through this path.

**Why this is the same family as ADR-009.** `tests/test_honesty.py` scans
**tracked files** for account shapes and was **clean the entire time the hole was
open**, because it cannot see a runtime exception path. **A guard can refuse
correctly while the path that actually matters goes unchecked** — which is the
lesson ADR-009 recorded, arriving from a different direction.

**Alternatives rejected.** *Supplying the client id through the process
environment* lost because it works around the defect rather than recording and
fixing it. *Leaving `.env` for the operator and stopping* lost because the value
cannot be what was intended, the fix is not a registered rule, and stopping would
have blocked every measurement in the stage on a paste error. *Guessing which
integer the operator meant* was not attempted; `4202` is recorded as a choice
made here, and the operator may change it freely.

### ADR-011 — close on capital rather than continue to the census (2026-09-03)

**Context.** CME's published outright rates put maintenance on one MBT future at
$1,704.00 for front month 09/2026, being 20.837% of the $8,177.75 measured
notional, against a registered MARGIN ceiling of 12.80%. Exceedance 1.628x on the
hedge leg alone, at the exchange minimum, in maintenance terms. 18 paper previews
put a single short option at 2.0x to 2.7x that figure, zero of 18 below the
ceiling.

**Decision.** Fire the MARGIN gate FAIL on a notional-normalized basis and close
the repository VENUE_BLOCKED, unqualified. Do not fix the transmit invariant, do
not buy the CME crypto market data subscription, do not run the census.

**Consequence.** The COST gate never fires, so no CME spread is ever measured by
this repository and the 34.600 bps ceiling is never tested. That is accepted: a
cost band prices a position the margin figures say cannot be held, and measuring
it would answer a question that no longer has a decision attached. The transmit
defect is documented in ADR-010 and in `CLOSURE.md` and travels to whatever
touches a broker API next, unrepaired here.

**Why normalized to notional.** A dollar ceiling moves with the bitcoin price and
a fraction of notional does not. Bitcoin fell roughly 42% between registration
and measurement. Leaving the verdict in dollars would have made it hostage to a
price move rather than robust to one.

**Alternatives rejected.** *Fixing transmit first and taking a paper margin read
across a hedged cycle* lost on ordering: the published exchange minimum already
breaks the gate on the cheapest leg, so the paper read would refine a number
whose verdict is settled. *Raising the ceiling to fit a larger sleeve* lost
because the ceiling was registered before the measurement and a threshold revised
after seeing the number is not a threshold. *Leaving the repository open pending a
capital decision* lost because an open repository with a failed gate and no next
action is the drift the closure discipline exists to prevent; `REINTRODUCTION.md`
carries the reopening conditions instead.

