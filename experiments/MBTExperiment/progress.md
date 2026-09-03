# progress.md — where MBTExperiment is right now

Newest entry first. Every stage states its ETAs **before** the work is armed and
re-quotes them from measurement afterward. Every stage prompt is logged here
**verbatim on receipt, before any file is touched**.

---

## Stage B closed HARNESS-BLOCKED, 2026-09-03. The known-answer test never ran.

**HARNESS-BLOCKED, 3 of 4 registered conditions held.** The harness builds, all
five guards fire under mutation, and the census is armed with its projected
completion date. **The known-answer test did not run**, because no Gateway
session exists, so the what-if reader has never reproduced an independently
checkable margin and its MBT output is not trusted. That is the binding
condition, and it is the registered one rather than a substitute.

**A blocked result was an expected outcome here and is a fully acceptable one.**
No threshold was softened, no friendlier spread source substituted, no refused
window dropped to reach twenty, no paper figure promoted into a gate, and the
premium basis was fixed before any spread existed and was not reselected.

### The numbers

| figure | value | n |
|---|---|---|
| stage verdict | **HARNESS-BLOCKED** | 3 of 4 conditions held |
| MARGIN gate | **ABSENT**, `no_live_session` | n = 0 live sessions |
| COST gate | **ABSENT**, `insufficient_sample` | n = 0 of 20 windows |
| registered COST ceiling | **34.600 bps** of notional | from 112.72 bps at n = 491 |
| ceiling not selected, kept visible | 49.610 bps | from 142.740 bps at n = 1,955 |
| MARGIN ceiling | $1,000/contract, 12.80% of $7,812.46 | quoted, not re-derived |
| IB Gateway reachability | **0 reachable** | n = 13 TCP attempts, 3 probes |
| exchange and regulatory fee | **`Absent(not_served)`** | n = 3 independent reasons |
| census windows | **0 accepted, 0 refused** | of 20 required |
| census duration once begun | **5 collection days** | fixed by the distinctness rule |
| guards demonstrated by provoked refusal | **28 refusals** | n = 5 guards |
| registered mutations behaving as registered | **5 of 5** | 0 failures |
| boundary digest, open vs close | **identical**, manifests byte-identical | 2,901 entries, 324,887,193 bytes |
| suite at close | **159 passed** | mypy strict clean, 29 files |

### What fired, and why

**Nothing fired. Both gates are ABSENT and both are recorded with their reasons
rather than omitted from the verdict table.**

**MARGIN** is `Absent(no_live_session)`. A margin is a property of the account and
needs a U-prefixed session. It was registered as unfireable in this stage in
Section 0.3, before any measurement, so this is the registered state rather than
a shortfall against a target.

**COST** is `Absent(insufficient_sample)` at 0 of 20 windows, and it carries a
second block that survives the first. The fee leg is `Absent(not_served)`, so the
all-in sum cannot be formed at all, and the gate falls back to the measured legs
as a strict lower bound. **A lower bound can FAIL and can never PASS.** So both
gates are blocked from PASS for independent reasons and the terminal state is
over-determined: **fixing the Gateway alone would not change the verdict.**

### The one defect worth carrying forward

**The mutation harness found a hole in Guard 1 that nothing else found.** The
package's only order construction went through an injected class, so the call
site read `order_cls(...)` and sat outside the scan's constructor list. Flipping
`whatIf` to `False` there changed nothing. **Review, `mypy --strict`, `ruff` and
156 passing tests had all missed it.** Both fixes were kept: the site constructs
`Order` directly, and the scan now keys on the `whatIf` argument rather than on
the callee name. ADR-009.

### ETAs, re-quoted from the log against their up-front figures

| task | ETA stated up front | actual | outcome |
|---|---|---|---|
| 0 orientation and probes | 20 min | **1.2 min** | 17× fast |
| 1 scaffold and five guards | 70 min | **16.2 min** | 4× fast |
| 2 registration Section 0 | 30 min | **3.5 min** | 9× fast |
| 3 registration Sections 1+ | 40 min | **0.8 min** | 50× fast |
| 4 paper harness | **SKIPPED, declared blocked up front** | 3.3 min to record the block | **skipped, named as skipped** |
| 5 bid-ask census | **clock-bound, not effort-bound** | 1.2 min to arm | 5 collection days once begun |
| 6 fee leg | 15 min | **1.0 min** | 15× fast |
| 7 fire the gates | 20 min | **1.0 min** | 20× fast |
| 8 five mutations | 35 min | **2.7 min** | 13× fast |
| 9 documents and closing checks | 40 min | in this entry | n/a |

**Every effort-bound ETA was wrong in the same direction by roughly an order of
magnitude, and the reason is locatable because the assumption was named.** The
ETAs rested on "the authoring rate measured writing `tools/boundary_hash.py` and
`tools/probe_gateway.py`, two modules of about 130 lines, both correct on the
first run with no rework."

**The named assumption held. An unnamed one did not.** What was actually measured
about those two modules is that they needed **no rework**, a correctness
property. The conversion from that into **minutes** was never measured and was
substituted from a human-scale estimate of typing and reviewing time. So the
error sits entirely in the unmeasured step, which is exactly where naming the
assumption was supposed to leave it.

**Task 3's 50× miss is the clearest case.** Its ETA assumed "fixing a rule costs
about twice transcribing one", which is an *effort* claim. Effort and wall clock
did not map onto each other at all, because both transcription and rule-fixing
resolved to a single document write.

**Task 4's ETA was declared SKIPPED up front**, not estimated and missed. It is
named as skipped here rather than smoothed over. Recording the block still cost
3.3 minutes, which was itself unestimated.

**The one ETA that held is the clock-bound one.** Task 5 was stated as 5
collection days minimum, derived from the registered rule rather than from an
authoring rate, and that figure is unchanged: it is a property of the rule and no
effort compresses it.

### Boundary and neighbours

**The VRPExperiment boundary is unchanged.** Hashed before any work and again at
closure: 2,901 entries, 324,887,193 bytes, 0 unreadable paths, **both digests
identical and the two manifests byte-identical**. Its working tree is clean and
its HEAD is unchanged at `d37cf6d`. It was read as text and never written.

**No systemd unit was installed by this stage and no timer was touched.** No unit
file anywhere references MBTExperiment. The three protected timers keep their
enablement symlinks in `timers.target.wants/`, dated 2026-07-29 and 2026-08-27
and **unchanged by this stage**. `Linger=yes` is confirmed via `loginctl`.

**One honest gap in that check.** `systemctl --user` could not reach the user
scope bus from this session, so the **enabled and active runtime state of the
three timers is `Absent(no_user_bus)`** rather than verified. The on-disk
enablement is verified; the running state is not, and it is recorded as unchecked
rather than claimed.

**One timer did appear inside the session window and it is not this stage's.**
`claude-auto-retry-reconcile.timer`, created 2026-09-02 23:51 PDT against a
session that began 23:26 PDT, belongs to the third-party `claude-auto-retry` npm
tool, executes `node .../claude-auto-retry/bin/cli.js reconcile`, and carries
**zero references to MBTExperiment**. This stage ran no `systemctl` command that
mutates anything and wrote nothing under `~/.config/systemd`.

**NPLExperiment was not disturbed**: no file modified on 2026-09-03, and its H2
collection continues toward its 2026-11-26 look. **`news_experiment.db` was never
opened**: last access 2026-09-02 17:18, before this session began.

**No `.env` was written anywhere outside this repository.** No `.env` under
`~/Documents/GitHub` has an mtime inside the session window, and VRPExperiment has
no `.env` at all, only an empty `.env.example` dated 2026-08-29.

### Open operator items

1. **The live margin read.** Needs a U-prefixed session. Blocked by the
   non-functioning internal fans and by the absence of a live profile for this
   project. Lifting the paper-only clause is an operator edit to `CLAUDE.md`,
   never a flag. **The harness needs no change to accept it.**
2. **`MBT_IB_PAPER_CLIENT_ID` is unset in `.env`.** The config guard refuses
   before opening a socket and names the variable.
3. **IB Gateway is not running.** Release 10.45 is installed and configured for
   paper. No IBC exists, so it starts only through an interactive IBKR login.
4. **The known-answer expected margin** is an operator input, read by a person,
   because CME's Data Terms of Use refusal binds automated access.

Items 2 and 3 unblock the census and the known-answer test. **Item 1 is the only
one that unblocks the MARGIN gate.**

---


## Stage B prompt, logged verbatim on receipt, 2026-09-02

Logged before any other file was touched, per `CLAUDE.md`. Working directory was
confirmed first: `/home/kiros-li/Documents/GitHub/MBTExperiment`, no `/closed/`
in the path, no `_CLOSED_DO_NOT_RUN_HERE` marker at the root.

```text
BEGIN PROMPT - SUMMARY OF PROMPT: MBTExperiment Stage B. Scaffold, five structural guards including a no-transmit AST scan, a pre-registration with two gates and a premium-basis decision, a paper-only IB Gateway harness that transmits no order, and a clock-bound bid-ask census. Terminal states are HARNESS-READY or HARNESS-BLOCKED. No live session, no capital, no premium recomputed.

Stage B: Scaffold, registration, the no-transmit paper harness, and the bid-ask census. Model: Opus 5. Effort: xhigh.

Why this repository's numbering opens at B. Stage A was issued and was accidentally opened inside VRPExperiment, a closed repository, on 2026-09-02. It overwrote that repository's empty .env and stopped. No measurement was touched, no latch was spent, no commit was made. The label is not reused, and this note exists so a future reader does not look for a missing Stage A.

Before anything else, confirm your working directory. Print it. If the path contains /closed/, or if a file named _CLOSED_DO_NOT_RUN_HERE sits at its root, stop, report the path, and take no further action: do not write, do not commit, do not create a .env, do not run make. You should be in ~/Documents/GitHub/MBTExperiment. Proceed only from there.

Read CLAUDE.md and README.md in full. Then read, across the read-only boundary and without writing a byte to it, VRPExperiment's docs/HANDOVER.md, docs/COSTS.md, docs/ARTIFACT.md, HYPOTHESES.md, DECISIONS.md ADR-008 and ADR-009, and REGISTRATION.md Sections 4.1, 4.2 and 4.3 in full. VRPExperiment sits at ~/Documents/GitHub/VRPExperiment today and relocates to ~/Documents/GitHub/closed/VRPExperiment when stage_move_closed.sh runs, so resolve it by locating the marker rather than by assuming either path.

Log this prompt to progress.md verbatim before any file is touched.

Run autonomously. Commit at every task boundary. Push nothing.

This stage transmits no order, opens no live session, authorizes no capital, sizes no position, and recomputes no premium. VRPExperiment measured the premium, closed on 2026-08-30, and its 1,955-day sample is spent. No figure in it is recomputed, extended, or re-read.

State a measured ETA for every task before arming it. Measured means derived from a probe that reads actual pace, with the assumption it rests on named in the same sentence, so a wrong ETA is debuggable rather than mysterious. Task 5 is clock-bound rather than effort-bound and states the calendar date it completes and that it cannot be compressed. Re-quote every ETA from the log at the end against its up-front figure, and name any skipped ETA as skipped rather than smoothing over it.

Task 0. Orientation, the read-only boundary, and feasibility probes.

Hash the VRPExperiment boundary before any work begins and again at closure, per path, as a sha256 over the sorted sequence of relative path, size, and file sha256. Record both snapshots as artifacts and compare them at the end.

Probe on paper only, and derive every ETA below from what you measure: IB Gateway reachability on the configured host and port, connection and handshake latency, the account list the session returns, futures options permission on CME crypto products, MBT option chain enumeration and its size, and the market data subscription state on both an MBT option and the MBT front future. Record explicitly whether ticks arrive real-time, delayed, or frozen, since a delayed tick is inadmissible later and you need to know now rather than after twenty windows.

If futures options permission on CME crypto products is absent on the account, that is a terminal finding for this stage. Record it, write HARNESS-BLOCKED with that reason, and stop rather than building a harness that has nothing to point at.

Task 1. Scaffold and the five standing guards, ported by copying and never by importing.

uv, ruff, ruff format, mypy strict, pytest, pre-commit, Makefile. Copy the patterns from solcopy, InsiderExperiment and VRPExperiment. An import would make a closed repository a live dependency of an open one, and the next refactor here would edit a sealed artifact.

Guard one, no transmit. Walk the parse tree of the entire package and assert that every call site of a broker order-placing method carries whatIf=True as a literal keyword argument. Fail the build on a missing flag, on a False literal, and on a flag supplied from a variable, an attribute, or a call, because a value that is not a literal cannot be verified at build time. Do not implement this as a text search. A previous project's config guard scanned raw text, matched the key inside a trailing comment, and called that enforcement.

Guard two, environment provenance. The environment tag on every recorded figure derives from the account number the session actually connected to, read back from the broker, never from the variable that was supposed to select it. A D prefix is paper and a U prefix is live. A session declaring live that connects to a D-prefixed account refuses and writes nothing. Configuration states an intent and the connection states a fact, and the fact wins.

Guard three, paper inadmissibility. Any attempt to fire a gate from a figure tagged paper raises. Pinned by test.

Guard four, the deciding-read latch, ported from VRPExperiment TASK 6. Fsynced before returning, one spend per registered figure, second attempt raising LatchAlreadySpentError. Build it and test it now even though no live read happens in this stage, because retrofitting a latch into a session that already has a live connection open is the wrong order.

Guard five, recorded absence. A missing quote, an unquoted leg, a crossed book, a zero bid, a missing fee line, and an unavailable live session are each a typed absence carrying its reason and refusing coercion to a number.

Every guard is demonstrated by producing its refusal as an artifact under reports/, never by asserting it in prose. make all green before proceeding.

Task 2. REGISTRATION.md Section 0, committed before any figure is measured.

Register three terminal states, not two. HARNESS-READY when the harness builds, all five guards fire under mutation, the known-answer test reproduces an independently checkable margin, and the census is armed with its projected completion date. HARNESS-BLOCKED when any of those fails, or when account permission is absent. This stage never reaches HARVESTABLE-CONFIRMED or VENUE_BLOCKED, because the MARGIN gate cannot fire without a U-prefixed session.

Register both gates with their thresholds quoted from VRPExperiment's handover. MARGIN passes when initial margin on a short MBT option sits at or below 12.80 percent of the 7,812.46 dollar notional, being 1,000 dollars per contract. COST passes when the absent legs at the p90 end, being option and future bid-ask plus CME exchange and regulatory fees, sit at or below the registered ceiling.

Register the MARGIN gate as Absent(no_live_session) for this stage, naming the two operator constraints: the machine's internal fans are not functioning, so concurrent live and paper sessions are not run, and no separate live profile exists for this project. An absent gate is a recorded state carrying its reason. It is never an unfired gate quietly omitted from a verdict table, and never a paper figure promoted to stand in for a live one.

Register the three provenance kinds separately, because they are not equally blocked. A margin figure is a property of the account and carries the account prefix read back from the session, so it needs a U-prefixed session and is unavailable here. A quote is a property of the market data feed and carries the subscription state and tick delay status, so it is collectible on paper when real-time. A commission report is a property of the fill and is synthetic under paper, so it is unavailable here in either direction.

Register the admissibility of a paper-sourced quote as an assumption rather than a measurement. It rests on IBKR routing market data by subscription rather than by account type. State the claim, state what would falsify it, and register that it is re-verified against a live session whenever one becomes available. The standing rule is that measured beats documented, this one is currently documented, and every census figure is labelled accordingly wherever it is reported.

Settle the premium basis now, before any spread is measured. This is the load-bearing decision of the stage. The 49.610 bps ceiling derives from half the full-sample one-sided 95 percent lower bound of 142.740 bps, less the measured p90 commission of 21.760 bps. That sample decays monotonically across its four quarters at 284.53, 250.59, 145.13 and 112.72 bps, a 60.4 percent fall, so the most recent quarter does not support the figure the ceiling rests on. Against the decayed figure the room is 56.360 less 21.760, leaving 34.600 bps. Fix one basis with reasoning stated in mechanism terms rather than in expected-result terms, register both resulting ceilings so the choice stays visible to any reader, and record that selecting a basis after seeing a spread measurement voids this registration.

Task 3. REGISTRATION.md Sections 1 onward, committed before any quote is stored.

Transcribe VRPExperiment 4.1, 4.2 and 4.3 verbatim rather than paraphrasing them: at least 20 distinct observation windows on the at-the-money 30-day series with median and 90th percentile reported alongside their n, central assigned to the median and pessimistic to the 90th percentile with the assignment already fixed upstream and not reopened here, and the plus or minus 0.10 delta band evaluated daily with registered sweeps at plus or minus 0.05 and plus or minus 0.20. Carry the measured rebalance counts of median 11 and p90 16, with the BTC maximum of 20 recorded.

Then fix what those sections leave to an implementer, because each is a place where a quiet wrong answer produces a valid-looking straddle either way. Fix the at-the-money strike selection rule. Fix the 30-day tenor resolution rule for the case where no expiry lands exactly on 30 days, including which direction to round and what to do at a tie. Fix what makes two observation windows distinct, in clock terms rather than in count terms. Fix the refusal conditions covering an unquoted leg, a crossed book, a zero bid, a stale timestamp, and a delayed or frozen tick.

Port the commission figures as measured rather than recomputed: 0.85 dollars per MBT contract at the lowest volume tier, 4.352 bps for the four-fill straddle round trip, 1.088 bps per rebalance fill on the micro future, 16.320 bps central and 21.760 bps pessimistic all in on commission alone.

Register that Deribit's 22.50 bps BTC round-trip spread is REFERENCE ONLY and may never be substituted for a CME spread, citing ADR-008 and the ORBExperiment precedent it rests on, where a carried band understated five of six legs and produced a shift 11.27 times too small while overstating a sixth.

Count the trial grid and register its deflation. Reserve a numbered section for the operator prior and leave it empty.

Task 4. The paper harness, development only, with a known-answer test.

Connect on the paper port. Resolve the at-the-money 30-day MBT straddle from the live chain under the rules registered in Task 3. Run a what-if preview against the short straddle and parse the initial margin change, the maintenance margin change, and the commission estimate.

Before any MBT output is believed, reproduce an independently checkable margin on a liquid product through the same code path, and record the comparison. A new path reproduces a previously measured answer before its output is trusted.

Record explicitly whether the what-if commission estimate includes exchange and regulatory fees or excludes them. The IBKR schedule states that non-member exchange and regulatory fees are applied on top, so this is a question to answer by measurement rather than by assumption, and the answer is a fact about the paper environment rather than about the venue.

No figure produced in this task is admissible to any gate, and a test pins that feeding a paper-tagged figure to a gate raises.

Task 5. The bid-ask census, armed and begun.

This task is clock-bound and cannot be compressed. State the projected completion date up front from the registered window-distinctness rule and the count of at least 20.

Before appending any window, verify and record the real-time subscription state on all three instruments: both option legs and the MBT future used for hedging. Sample all three. A spread measured on options alone understates the hedge leg across a median of 11 rebalances and a p90 of 16, and the hedge leg is where most of the rebalance cost lives.

Record per window: both option bids and asks, the future bid and ask, the venue timestamp, the local timestamp, the subscription state, and the tick delay status. Refuse a window carrying any unquoted, crossed, zero-bid, stale or delayed leg, record the refusal with its reason, and never fill the gap by widening a figure from another venue.

Because the machine's internal fans are not functioning, run the census as discrete sampling with the session closed between windows, never as a resident collector. A missed window is a gap in a discrete sample and is recorded as one, never backfilled.

Task 6. The exchange and regulatory fee leg.

Determine it or record it absent, and do not estimate it. Paper fills are simulated and their commission reports synthetic, so a fee read from a paper execution measures the simulator rather than CME. If the paper what-if response carries a fee breakdown, record what it contains and label it as a paper-environment fact. Otherwise record the leg Absent(not_served) with its reason, and state in the same sentence which direction the resulting bound errs and by how much the registered ceiling therefore overstates the room. Do not estimate a fee from a rule of thumb, infer one from a third party, or carry one from another repository.

Task 7. Fire what can be fired, record what cannot.

The MARGIN gate does not fire and is recorded absent with its reason. The COST gate's spread legs are computed from the census as it stands, reported with their n and their window count against the registered minimum of 20, and the gate itself fires only when that minimum is met. If the census is short at the time of writing, report the interim figures clearly labelled as interim and fire nothing.

Write the stage verdict as HARNESS-READY or HARNESS-BLOCKED. Name the live margin read as an open operator item with the two constraints that block it, so it is a named gap rather than a missing number.

Task 8. Tests and the five registered mutations, with Python bytecode purged before every run.

Purge bytecode first, every time. A same-byte-length restore once left mutated bytecode valid under CPython's mtime-and-size cache check, and the harness reported a restore as still red. A mutation harness that reports results from source no longer on disk is worse than no harness.

The five mutations. Flip a whatIf literal to False and confirm the no-transmit AST guard fails the build. Supply the whatIf flag from a variable rather than a literal and confirm the same guard fires. Make a session declaring live connect to a D-prefixed account and confirm the provenance guard refuses and writes nothing. Feed a paper-tagged figure to a gate and confirm it raises. Spend the deciding latch twice and confirm LatchAlreadySpentError.

Every mutation is demonstrated by the artifact it produces under reports/, and the whole suite goes green on restore.

Task 9. Document and commit.

Write a progress.md entry, newest first, with the outcome in its first line, the numbers table, what fired and why, and every ETA re-quoted from the log against its up-front figure with any skipped ETA named as skipped. Write ADR-001 onward in DECISIONS.md. Write FINDINGS.md with every claim carrying its sample size in the same sentence as its number.

Re-hash the VRPExperiment boundary and record it unchanged. Confirm no systemd unit was installed and no timer touched, that AiTrader's news-collect.timer, npl-watch.timer and npl-daily.timer remain enabled and active with Linger=yes still enabled, and that NPLExperiment's H2 collection running toward its 2026-11-26 look was not disturbed. Confirm no .env was written anywhere outside this repository.

The governing rule for this stage. A blocked or absent result is an expected outcome and a fully acceptable one. Do not soften a threshold, substitute a friendlier spread source, drop a refused window to reach twenty, promote a paper figure into a gate, or reselect the premium basis after seeing a number. VRPExperiment reached a qualified block by refusing to open an account rather than by estimating what an account would have shown, and this stage holds the same line everywhere the account it does have cannot answer.

END PROMPT
```

---

## Repository shell created, 2026-09-02

Scaffold only. No registration, no measurement, no claim. Created by the
management session, not by a coding session. No Python module exists yet and no
test exists yet.

The two thresholds in `CLAUDE.md` and `README.md` are quoted from
VRPExperiment's `docs/HANDOVER.md` and are cited, not re-derived.

Stage A.1 is next and is the first coding session.
