# DECISIONS

Numbered architecture decision records. Each states what was decided, what it
costs, and what would overturn it.

---

## ADR-001. The note lives in its own repository, not inside any of the four

**Status.** Accepted, 2026-08-29.

**Context.** The note's claim is about four repositories at once:
NPDExperiment, InsiderExperiment, ETFExperiment and HFExperiment. The obvious
cheaper options were to append it to one of them, or to a fifth already holding
cross-cutting material.

**Why each of those was rejected.**

*Inside one of the four.* Every one of the four is **closed**, and closed here
means something specific: the registration is binding, the verdict has fired,
the amendment log is sealed against anything that responds to an observed
outcome, and the artifacts are preserved so the result stays auditable. Adding a
document that reinterprets a fired verdict — even a document that only quotes it
— puts new prose inside a boundary those repositories drew on purpose. It would
also privilege whichever host was picked. A note filed inside InsiderExperiment
reads as InsiderExperiment's account of the other three, and its most important
claim is precisely that the four are separate.

*Inside AiTrader or MLCryptoEngine.* Both are parent programs with their own
live hypothesis registers, and MLCryptoEngine's register carries an explicit
warning against confusing closure types. Filing a note about power closures into
a register whose entries are cost-bound and signal-absent invites exactly the
merge it warns about.

*A cross-cutting document with no repository.* The note quotes about ninety
figures from seven repositories. Without a build there is nothing to stop a
figure drifting, and a secondary source whose numbers drift is worse than no
secondary source, because it launders an error into something that looks
checkable.

**Decision.** A separate repository, holding the note, the sourced figures, and
the tests that pin one to the other. It reads all seven sibling repositories and
writes to none of them.

**Cost.** Duplication. Every figure now exists twice — once where it was
measured and once here — and the copy can go stale in a way the original
cannot. That cost is paid down by ADR-002, not eliminated.

**What would overturn it.** A future document that needed to *change* one of the
four rather than quote it. That is not this note, and if such a document is ever
written it belongs in the repository it changes, as a numbered amendment, under
that repository's own rules.

---

## ADR-002. The note is a secondary source, and the build treats it as one

**Status.** Accepted, 2026-08-29.

**Context.** This repository measured nothing. Every number in it was measured
elsewhere and is being re-quoted, which is the failure mode most likely to
produce a confident error: a transcription slip here is invisible, because there
is no measurement to disagree with it.

**Decision.** Three mechanisms, in increasing strength.

1. Every figure is typed as `Figure(value, source)` in `rplimits/cases.py`, and
   `Figure.__post_init__` raises on a source key that does not resolve. A figure
   cannot be added without a citation, because the constructor refuses.
2. Every citation resolves to a repository, a file or commit marker, a short
   hash and a date in `rplimits/sources.py`, rendered into `SOURCES.md` so a
   reader can check the note without this repository's help. `SOURCES.md` names
   the two `git` commands that do it.
3. The tables and per-case records in the documents are **generated** from that
   data between markers, and `tests/test_render.py` re-renders each block and
   compares it to the file. Prose and data cannot diverge silently.

**Cost.** The documents are partly machine-owned, so an editor who reflows a
generated table by hand will fail the build until they run
`uv run python -m rplimits --write`. That friction is the point.

**What would overturn it.** Nothing available. The alternative is trusting the
prose, and the prose is what the mechanism exists to distrust.

---

## ADR-003. Four handed-over figures are corrected in the note, not silently repeated

**Status.** Accepted, 2026-08-29.

**Context.** The note was commissioned with figures already attached, and the
instruction was explicit: do not paraphrase a number that has not been read, and
correct anything the repositories do not carry.

**Decision.** Four corrections are stated in the note's own body, under a
heading, rather than in a footnote:

1. NPDExperiment's "415 days" is 415 days of *data*, not elapsed collection.
   The phrase is quoted correctly from InsiderExperiment's Section 0.1 — but the
   whole experiment ran on 2026-08-25, with collection taking 194 minutes.
2. ETFExperiment's 845 / above-1,200 / about-302 triple belongs to Amendment 6's
   assessment of what further collection would buy, not to the closure. The
   closure fired on 163 projected against 300 governing at the 2027-03-31
   deadline.
3. HFExperiment fired BLOCKED on the *broker*, not on power. Its power
   resolution is inherited from the AiTrader round of 2026-07-26 and from its own
   Section 11 arithmetic.
4. MLCryptoEngine's 0.03 bps of capture was measured against Kraken's 50 bps
   round trip, a miss of about 1,700x. The 3 bps figure is the cheapest reachable
   venue, against which the same edge misses by about 100x.

**Cost.** The note is longer and its opening is less clean. A correction section
placed before the argument slows a reader down at exactly the point they are
deciding whether to trust the document.

**What would overturn it.** Evidence that any of the four corrections is itself
wrong, which is checkable: each cites the file and commit it was read from.

---

## ADR-004. HFExperiment is carried as a power case, and labelled as inherited

**Status.** Accepted, 2026-08-29.

**Context.** Three of the four cases fired a power-shaped verdict inside their
own registration. HFExperiment did not. Its Section 0 fired BLOCKED on IBKR's
refusal of fractional quantities through the API, and it then closed by operator
decision on 2026-08-26 with its shadow series never started.

**The case for including it anyway.** Its README's first sentence states that
H-F was "tested once in the AiTrader cross-sectional round of 2026-07-26 and
resolved on statistical power rather than absent signal", and that round is
unambiguous: z 1.668 against a corrected bar of 2.50, needing 104.0 percent per
year of excess against 70.5 delivered, with the largest raw outperformance the
parent project ever measured. Its own Section 11 then priced the forward version
at 2,061 trading days to clear zero and 2,852 to clear the cost hurdle.

**Decision.** Include it, and label the inheritance in the case record, in the
note's correction section, and in the caveat field the tests require every case
to carry. A reader must not come away thinking four power gates fired.

**Cost.** The claim is weaker than "four independent power gates". It is stated
at the strength the evidence supports instead.

**What would overturn it.** A reading of the AiTrader round that makes it a
signal closure rather than a power closure. The round's own headline argues
against that in terms: *not absent signal ... the binding constraint on this
family is the position limit.*

---

## ADR-005. The scope limit is pinned as hard as the figures

**Status.** Accepted, 2026-08-29.

**Context.** A note like this decays in one direction. Nobody strengthens a
caveat later; they trim it for length, and each trim is individually reasonable.
Four cases become "consistently"; a detectability result becomes "the effect
isn't there"; and the document ends up claiming what it spent its first page
refusing to claim.

**Decision.** `tests/test_honesty.py` pins the scope-limit sentence in both
`README.md` and the note, pins the headline figures in both, and asserts the
note never contains any of four overclaiming phrasings. Every detector carries a
canary that proves it fires — the InsiderExperiment ADR-012 lesson, that a guard
which has never been shown to fail is not a guard, applied here.

**Cost.** The pinned sentence cannot be reworded without editing the test, which
makes a genuine improvement to the phrasing slightly annoying. That is the
intended asymmetry: rewording is possible, deleting is not silent.

**What would overturn it.** Nothing. The mechanism costs one file and it defends
the only thing this note has.

---

## ADR-006. The one derived figure is flagged as derived

**Status.** Accepted, 2026-08-29.

**Context.** The cost asymmetry needs NPDExperiment's total stage time. The
repository records per-stage actuals and never sums them.

**Decision.** The 411 minutes is stated as this note's arithmetic over six
quoted addends — A.1 22, A.2 34, B.0 68, B.0b 52, B.1 194, B.2 41 — and
`SOURCES.md` carries a dedicated section saying so, including what the total
excludes. Every other number in the repository is quoted rather than computed.

**Cost.** One number in the note is weaker than the rest, and the note says
which one.

**What would overturn it.** NPDExperiment recording its own total, which it does
not.
