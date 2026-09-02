# PMExperiment

**The question.** Are prediction-market prices mis-calibrated by enough to
survive the costs a Canadian retail participant actually pays?

**The answer, 2026-09-02, terminal.** Unknown, and not knowable here. **H1 is
unmeasurable at this house's standard. Not disproven, not unlikely,
unmeasurable.**

**The reason.** Both venues closed on their own terms, all three licence
candidates failed, and the one route that does exist is gated on an established
legal entity that the operator does not hold and has decided not to create.
**The power gate never fired, on any venue, over any region. No statistic
relating a price to an outcome was ever computed.**

**Five stages. Zero dollars. Zero contracts enumerated. No trade, ever.** This
repository **never trades, holds no account, places no order**, and has **no
stage in which one is planned**. `.env.example` is empty on purpose.

**A documented negative is a valid and expected outcome. So is BLOCKED.** The
operator's prior was 5 to 8 percent, so **a null was the modal expected
outcome** before any of this began. What follows is the method working, not a
disappointment.

---

## What is worth taking from here

**This is the contribution, and it is the reason the repository is public.**
Nothing below required data access, and each one is portable to any project that
has to decide what it is allowed to read.

### 1. ADR-012, a claim about permission written as a procedure

A statement about what a source permits carries **a quoted clause, the
document's effective date, and the date it was fetched** — or it is recorded
**UNMEASURED** and the work proceeds as if permission were absent.

It exists because this repository moved its **entire measurement venue** on a
claim that cited none of the three. `pmexperiment/admissibility.py` is that
sentence as code: it judges the *form* of a claim and never its merits, because
a procedure that scored the persuasiveness of a clause would be dressing a
judgement up as a measurement. **UNMEASURED is not a synonym for PROHIBITED** —
same operational consequence, different epistemic content, one a measured
refusal and the other an absence.

**It has a known blind spot, found by firing it on correspondence at closure:**
the check tests that a clause is non-empty and **cannot tell a quotation from a
paraphrase**. Recorded, not repaired — see ADR-016.

### 2. ADR-015, the symmetry of convenience

A venue may not be held to a **looser** reading than another because its verdict
would be more convenient — and **the rule runs both ways.**

A licence read here declared a platform's terms unreadable, quoted a superseded
archive, and published PROHIBITED anyway. Both halves were wrong: bare `curl`
returned 403, the same `curl` with nothing added but a browser `User-Agent`
returned **HTTP 200**, and **PROHIBITED on an instrument that was never read is
a synthesized value.** With a no-candidate outcome already blessed as
legitimate, the **over-strict** reading had quietly become the convenient one.
That is the same error as inferring permission from silence, with the sign
reversed.

### 3. The self-audit that convicted this repository's own finding

ADR-012 stated that "Stage A's Kalshi finding met that bar." Fired against
itself, it did not: **the Kalshi Data Terms of Use print no date at all** —
`Effective` 0 occurrences, `Last Updated` 0 — so the finding **met two of three
elements**, not three.

It changed no verdict, because UNMEASURED and PROHIBITED both mean proceed as if
permission were absent. It is recorded anyway, because **a procedure that only
ever convicts other people's documents is not a procedure.**

### 4. Stage B's direction correction: the effect is charged FX where FX is worst

The published favourite-longshot magnitudes are quoted at **longshot** prices,
where the documented miscalibration is *over*pricing — so a buyer there holds a
**negative** edge. The exploitable expression on a binary venue is the
complement, and restated in the underpriced direction **every registered
magnitude sits at a high entry price**:

| source figure | exploitable side | entry price | underpricing |
|---|---|---|---|
| Bürgi, 5c winning 3 % | NO | **0.95** | 0.02 |
| Bürgi, 95c winning 98 % | YES | **0.95** | 0.03 |
| Krause, sub-30c settling 4.0 % | NO | **0.883** | 0.077 |

**The registered FX is proportional to entry price, so every exploitable
expression of the band is charged FX at 88–95c rather than at 5–12c** — near the
maximum rather than near the minimum. A cost model applied to the *quoted* price
instead of the *exploitable* one would have understated the charge by an order
of magnitude. The unit determination and the FX treatment are coupled, and the
coupling is what makes the turnover question material rather than academic.

---

## What was actually read, stated exactly

**No price series was ever collected, and no statistic relating a price to an
outcome was ever computed.** Stage A's 11 keyless probe requests did receive two
settled records carrying `last_price_dollars` and `result` — that is recorded
here rather than rounded to "no market price was ever read", because rounding it
is precisely the kind of claim this repository exists to refuse. Nothing was
retained, no price bucket was ever built, and no dispersion was ever computed.

**Zero market-data requests were sent to Polymarket. Zero requests of any kind
were sent in Stage E.**

## The route ledger

| route | verdict | on what | date |
|---|---|---|---|
| Kalshi, keyless | **PENDING_ACCESS** | terms do not sanction keyless systematic retrieval or AI-mediated use without written authorization | 2026-08-29 |
| Polymarket | **PENDING_ACCESS** | Terms effective 2026-08-11 prohibit the data-gathering tool class, expressly including on-chain | 2026-08-30 |
| a Polymarket authorization request | **PROHIBITED** (baseline) | six published addresses, none addressed to this asker | 2026-08-30 |
| published academic datasets | **UNMEASURED** | ADR-012 elements (1) and (2) both unmet on the leading candidate | 2026-08-30 |
| third-party platforms | **PROHIBITED** / **UNMEASURED** | Dune's in-force terms; four others never retrieved | 2026-08-30 |
| **Kalshi Internal Use** | **EXISTS-AND-UNTRAVELLED** | **not declined on the merits**; gated on an established legal entity | received 2026-09-01 |
| the entity | **declined by the operator** | a cost decision, not evidence about H1 | 2026-09-02 |

**The last two rows are the ones a reader should not blur.** Kalshi's
institutional desk raised **no merits objection**. Nothing was applied for, so
**nothing was granted and nothing was refused** — *this repository* declined the
cost of standing up an entity. A project that closes on access and a project
whose operator stopped paying look identical from outside, and only one of them
is a finding.

**Stage D was wrong in the exact way Stage D said it might be.** It published
"there is none" as terminal on 2026-08-30 while recording in the same document
that its candidate space was **sampled, not enumerated**, and that *"there is
none" is a verdict over what was read.* A route surfaced two days later. **The
caveat was load-bearing within the week**, and that is the best argument this
repository can offer for writing completeness limits at all.

## The one number this repository produced, and what it is not

**BAND-OPEN**, fired 2026-08-29: over entry prices **91–99c held to
resolution**, an edge above **5.85 points** at FX turnover k = 1 is required,
against a registered band top of **8.00 points**.

**It is a cost finding computed from registered constants with no calibration
measurement behind it. It must not be written anywhere as evidence that an edge
exists.** It records only that cost alone does not close the question. Every
magnitude any cited source places inside the surviving bucket — Bürgi's **2.0**
and **3.0** points — **fails** the **0.0300** cost floor, which the 3.0 exactly
ties even with FX driven to zero. The band survives on its top alone, and that
top is set by the one source whose **n the registration never recorded**.

## What would reopen this

Each is an operator action, not a measurement:

1. **an established legal entity applying for Internal Use** — necessary, not
   sufficient: the fee is UNMEASURED, whether Internal Use permits **publishing**
   a calibration result is UNRESOLVED, and the AI/ML written consent Kalshi
   conditions separately is UNRESOLVED;
2. **an academic tier offered by Kalshi, if one is** — a question is pending and
   unanswered; its existence is UNMEASURED, not absent;
3. **a licensed dataset whose licensor held authority to license** — the
   chain-of-title element the leading candidate could not show.

**A reply to the pending academic-tier question is a one-line register update,
not a reopening.** No fourth venue is proposed: a route finally answering is not
a licence to resume searching for one that says yes.

## The prior, and why it is not called registered

The operator's prior is **5 to 8 percent**, given **2026-09-02 at closure**.
Section 13 of `REGISTRATION.md`, `The operator prior`, reads *"to be filled by
the operator before the gate fires"* — **it was never filled, and it is left
empty permanently.** The figure is therefore **stated, not pre-registered**, and
no verdict here may be read against it as though it had been. An empty slot is a
truer record than a plausible-looking backfill.

## The measurement that was supposed to decide this repository

**Not the calibration error. The power to detect one inside the Canadian
filter.** It was never reached.

The direct precedent is NPDExperiment, which closed at *unresolved at achievable
power* with a realized minimum detectable contrast of **0.0512** against an
effect band of **0.01 to 0.05** — a design that could not have detected an
effect anywhere in the range it was testing — discovered after **415 days** of
collection, in the same session that read the result. InsiderExperiment then
registered its gate in advance and fired **BLOCKED at 49.35 bp** before
spending.

**This repository followed Insider, not NPD**, and stopped before collecting
anything. **Even if an authorization were granted tomorrow, the power question
would still be unanswered** — nothing in five stages has moved it.

**The Canadian doubt, registered before any measurement and never tested:** the
permitted categories are economic indicators, financial markets and climate —
the well-calibrated ones — and a **30-day minimum maturity** removes the
fast-resolving contracts. A split verdict was registered in advance as a
legitimate finding, reading "the mispricing may be real and **not reachable from
Canada**." It was never reached either.

## Scope

- Reads **public** market data and settlement history only. No account, on
  either side of the border, in any stage.
- Canadians cannot trade on Kalshi directly. The permitted-subset filter is a
  **registered analysis step**, never a trading plan — and it was never applied
  to a real enumeration.
- **Nothing here is trading advice, and nothing here is a suggestion to trade.**

## Layout

| path | holds |
|---|---|
| `REGISTRATION.md` | the binding pre-registration; Section 0 first, amendments append; Sections 15.1–15.5 are the fired verdicts |
| `DECISIONS.md` | ADRs; deliberate departures recorded with evidence |
| `HYPOTHESES.md` | the hypothesis register, so a settled question is not re-asked |
| `progress.md` | dated stage entries, append-only; Entry 0 of each stage is the operator prompt verbatim |
| `report.md` | one section per stage, each written for the moment it landed |
| `docs/ACCESS.md` | measured access per source, with dates |
| `docs/BAND.md` | the fee-versus-edge band arithmetic |
| `docs/LICENCES.md` | the three licence candidates, read terms-first |
| `pmexperiment/` | the package: registered constants, the band, the power arithmetic, ADR-012 as code |
| `tests/` | the suite, including the honesty and registration tests |

## Standing practices, inherited and now closed over

Pre-register before results. Measured behaviour beats documentation. Refusals
fail closed. Absence is a recorded state, never a synthesized value. Union time
intervals before summing, and never trust append order across processes. Every
figure travels with its n in the same sentence. **A gate that has never failed
is not a gate** — every guard here carries a test that fails when the guard is
removed, verified by mutation. Every prompt states a measured ETA per task and
records the actual against it.
