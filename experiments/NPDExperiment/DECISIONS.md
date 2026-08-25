# Decisions

Numbered architecture decision records. Newest last. A decision recorded here
is binding until a later numbered record supersedes it by number.

## ADR-001. Gate the experiment on knowledge cutoff, not on model rank

**Status.** Accepted, 2026-08-25.

**Context.** A model has read everything published before its cutoff. Only
days written after it stopped reading are exam pages. A stronger model with a
later cutoff has fewer clean days, not more.

**Decision.** The gate model is chosen for the size of the clean window its
cutoff leaves, not for its position on any leaderboard. `gpt-5-2025-08-07`
carries a verified cutoff of 2024-09-30, which leaves 432 trading days through
the bar store's last complete session. Stronger 2026-cutoff models arrive with
78 to 140 clean pages and screen for large effects only, so they form the
registered conditional phase C.1 and the scheduled replays of B.3. They are
never the gate.

**Consequence.** The gate runs on a model that is not the strongest available.
This is deliberate. A larger clean sample on a weaker model answers the
question. A tiny clean sample on a stronger model does not.

## ADR-002. Name the dated snapshot, never the bare alias

**Status.** Accepted, 2026-08-25.

**Context.** `gpt-5` is an alias. It repoints when a successor ships.

**Decision.** Every call, every config field, and every line of the
registration names `gpt-5-2025-08-07`.

**Consequence.** A registration naming a moving target cannot be replicated or
replayed. Naming the snapshot makes both possible. If OpenAI retires the
snapshot the experiment stops rather than silently substituting.

## ADR-003. Split collection from evaluation

**Status.** Accepted, 2026-08-25.

**Context.** The predecessor's findings were selected after the outcomes were
visible. A pooled confidence Spearman read plus 0.0357 while every provider was
individually negative, and that artifact was reported as a result.

**Decision.** B.1 collects and stores rankings. It computes no statistic that
relates an output to an outcome. B.2 evaluates once, later, and only after the
operator writes his prior into Amendment 0.

**Consequence.** The analyst cannot see a result while any degree of freedom
remains open. The cost is a session boundary in the middle of the work.

## ADR-004. Seal the forward returns behind a single reader

**Status.** Accepted, 2026-08-25.

**Context.** A convention that says "do not look" is not a control. The
predecessor had conventions.

**Decision.** Forward returns live in their own store, `var/npd_sealed.db`.
The only module permitted to name that path or open that store is
`npd.eval.evaluator`. `tests/test_guards.py` walks every source file, and fails
when any other module references the sealed path, the sealed table, or the
evaluator's reader function.

**Consequence.** Breaking the seal requires editing a guard test, which shows
up in a diff. The full verdict pipeline is proved end to end on synthetic data
with fake returns, so B.2's code is exercised without touching one real
outcome.

## ADR-005. The four council lessons become registration clauses

**Status.** Accepted, 2026-08-25.

**Context.** Four specific failures of the predecessor are each reproducible in
this design unless a clause forbids them.

**Decision.**

1. Per-model inference is primary. Pooled numbers are descriptive and never
   touch a verdict. Evidence: the council's pooled confidence Spearman read
   plus 0.0357 while Opus read minus 0.0996, Gemini minus 0.1156, and GPT-5.5
   minus 0.2724.
2. Power is registered before the first call. Evidence: the council's wide
   sample pre-registered 272 calls and 66 clusters against a 50 bp detectable
   effect and delivered 274 and 80, and the interval still excluded the effect
   the design was powered for.
3. No confidence field exists in version one. Evidence: the council's
   confidence was decoration, the buckets were non-monotone, the top bucket was
   worst at 25 percent, and no verdict ever reached 0.65.
4. The consolidat cell is recorded as a dormant named secondary. Evidence: the
   2026-07-27 session preserved a rationale cell, stated reasons containing
   "consolidat", at 71.7 percent on 53 calls, explicitly not a finding. This
   design emits no rationales, so the cell stays dormant, named, and applicable
   only if a rationale-emitting variant is ever registered.

**Consequence.** Each clause costs something. Clause 3 discards a field the
operator may want. Clause 1 forbids the pooled number that would look best.
Both costs are paid on purpose.

## ADR-006. The enumerated feature list governs, and it holds nine features

**Status.** Accepted, 2026-08-25.

**Context.** The brief describes the logistic baseline as fitting "the
identical eight features". The brief's own enumeration lists nine. Returns over
1, 5, 10, 20, and 60 sessions is five. Realized volatility over 20 and 60 is
two. Dollar-volume z-score over 60 is one. Volume trend 5 over 60 is one.

**Decision.** The enumerated list governs, because the brief also states that
the list is complete and that nothing else ever enters the prompt. The count is
nine. The logistic baseline fits the same nine.

**Consequence.** The discrepancy is recorded rather than silently resolved. A
reader comparing the brief to the code finds the reason here.

## ADR-007. Register the contrast power honestly, do not repair it by swapping the primary

**Status.** Accepted, 2026-08-25.

**Context.** The window clears the registered power floor of detectable IC
0.025 at 30 names, at 0.0179. The primary contrast does not sit as comfortably.
The primary horizon is five sessions, so consecutive days share four fifths of
their forward window, and the variance of the mean inflates by 3.4. The
effective day count falls from 427 to 126, and the minimum detectable contrast
lands between 0.026 and 0.047 depending on how correlated the model and the
best baseline turn out to be.

**Decision.** Register the primary as specified, at the five-session horizon,
and register the limitation beside it. The secondary one-session horizon
carries no overlap penalty and detects between 0.014 and 0.025, which is
better. It stays secondary.

**Consequence.** The primary detects effects in the upper half of the realistic
band 0.01 to 0.05 and is underpowered for the lower half. Recorded before
collection rather than discovered after. Promoting the better powered secondary
to primary after seeing a result is exactly the move this repository exists to
prevent.
