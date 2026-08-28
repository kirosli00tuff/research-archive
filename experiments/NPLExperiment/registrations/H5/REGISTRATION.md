# registrations/H5/REGISTRATION.md — HIP-3 equity-style perpetual basis, a feasibility entry

> **STATUS: REGISTERED 2026-08-28, BEFORE ANY H5 NETWORK CALL.**
>
> At the moment this document was committed, this entry had sent **zero
> requests**. No H5 price had been read, no asset context had been fetched,
> no basis had been computed, and no funding-service answer existed. The
> ticker-to-underlying mapping (Section 2), the market calendar (Section 5),
> the outcome map (Section 6) and the spend arithmetic (Section 7) are all
> committed as tested code in this same commit, **before** the first probe.
>
> **From this point the specification is closed.** Changing anything here
> requires a dated amendment appended at the bottom, stating what data
> existed when it was made. Nothing above an amendment line is ever edited.
>
> **What this entry is.** H5 is a **feasibility entry, not a trade
> hypothesis.** It authorizes no capital, no Stage B read of a trading
> outcome, and no Stage C. Its terminal states are **VIABLE** — a successor
> hypothesis is worth registering in a fresh repo — or **CLOSED**, with
> **INDETERMINATE** as the registered middle. There is no design here that
> could be traded, and none is planned.
>
> **What it does not touch.** H2's collectors, ledgers, latches and stores
> are **read-only** to every path in this entry, enforced by
> `npl.h5.stores.h5_store`, which refuses any write outside `data/h5/`. The
> generating-sample quarantine holds (standing rule 12). All thirteen
> register rules remain in force.

---

## 0. Standing-rule compliance, stated before the sections

Three of the register's rules bind this entry in ways worth writing out,
because the obvious implementation of "measure the basis" breaks all three.

**Outcome blindness (rule 7).** No H5 path parses a candle payload — not
`o`, `h`, `l`, `c`, or `v`, under any spelling — and the repo-wide AST guard
in `tests/test_guards.py` already covers every module added here. The
consequence is registered up front rather than discovered later: **a
retrospective basis cannot be built from `candleSnapshot`.** A candle read
blind carries `t`, `T` and a row count, which is not a price; a candle read
with a price is a rule-7 violation. So Task 3's retrospective series can
come only from a venue-served field that carries a **deviation** directly,
in the same row as its timestamp — or from nothing, which is a recorded
absence and a legitimate result.

**Funding (rule 7, second half).** No H5 path reads a funding rate **value**,
anywhere, for any instrument. Funding is recorded as **service**: whether
the venue carries a funding field on the asset context, and whether
`fundingHistory` returns rows, with counts and timestamps. That is the
operator's actual first question — *is funding served on these instruments
at all* — and it is answerable without reading a single rate. Service is
read through the existing gated reader at `entry_ms=None`, where every rate
comes back `Absent(blindness_gated)` and refuses coercion to a number.

**The retrospective gate.** Where the venue serves a **historical deviation
series**, that series is a near-deterministic function of the funding rate.
Reading it across a registered event's open outcome window would be a
post-entry funding read wearing a different field name. So the retrospective
read alone is gated: a coin in the H1 generating sample, in the H2/H3/H4
fresh plan, or on either leg of an assigned H2 pair records
`excluded_quarantined` and contributes to the coverage census only. Its
**contemporaneous** snapshot is unaffected, on the precedent already
registered in H1 Section 5, where the entry-anchor `l2Book` touch state is a
descriptive cost input on both pair legs and is not an outcome field.
Enforcement: `npl.h5.gate`, refusal produced by test.

---

## 1. The question

**Do HIP-3 equity-style perps trade at a persistent, measurable deviation
from their underlying reference, and is that deviation large relative to the
18 bp round-trip cost floor?**

The 18 bp figure is measured, not assumed: HIP-3 builder markets default to
double the venue's native fees — 3 bp maker and 9 bp taker per side — so a
taker round trip is **18 bp central, with the registered band at 6 and 36**
(`CONFIG.hip3_round_trip_bp`, H1 Section 5 / ADR-003, unchanged).

This is a question about **venue-served fields**, not about a trade. Section
4 says why that distinction is the whole entry.

## 2. The universe

**Every instrument on every HIP-3 dex whose ticker resolves to an
identifiable equity, ETF, or index underlying**, enumerated mechanically
from `perpDexs` and per-dex `meta`. The main dex is out of scope: it lists
tokens, and the question is about the equity-style family the builder dexs
introduced.

**The resolution rule is a registered string mapping, written before any
price was read** — `npl.h5.resolution`, committed in this commit. It is
exact-string and mechanical. A ticker resolves iff its exact string appears
in one of three tables; nothing fuzzy-matches and nothing guesses.

The registered admission criterion, stated once: an entry is `resolved` only
where the ticker string is **(a) an exact listed ticker symbol on a major
exchange**, or **(b) an unambiguous name or standard abbreviation of exactly
one listed issuer or one named public index.** Everything failing both tests
is excluded — including several tickers whose likely meaning is obvious to a
reader. **A likely meaning is a guess, and a guess is what this table exists
to refuse.**

Three recorded states, counted separately and reported both separately and
as a union (the union is the prompt's `excluded_unresolvable`):

| state | meaning | reasons recorded |
|---|---|---|
| `resolved` | an identifiable equity, ETF, or index underlying | `equity`, `etf`, `index` |
| `excluded_non_equity` | resolves confidently, but not to an equity-style underlying | `crypto`, `crypto_index`, `commodity`, `fx`, `rate` |
| `excluded_unresolvable` | does not resolve to an identifiable underlying at all | `private_no_public_underlying`, `ambiguous_ticker`, `basket_no_named_reference`, `venue_house_index`, `not_in_registered_mapping` |

**The mapping as committed**, before any H5 price read: **104** resolved
entries, **57** non-equity entries, **37** unresolvable entries — **198**
registered ticker strings, exactly the distinct bare-ticker set of the
2026-08-27/28 census (505 instruments, 11 dexs, 272 distinct HIP-3
(dex, coin) pairs on disk at precondition). Applied to that census the
mapping yields **151 resolved** (118 equity, 18 index, 15 ETF), **80
excluded_non_equity**, **41 excluded_unresolvable**, across 8 of the 10
HIP-3 dexs; `hyna` and `vntl` contribute zero. **Those figures are a
projection from the stored census, not the measurement.** Task 2
re-enumerates from the live venue and its counts govern.

## 3. The measurements

All descriptive. **None is verdict-bearing on returns**, and no return is
computed anywhere in this entry.

Per resolved instrument, at the daily cadence, from **one snapshot**:

| measurement | venue field | recorded when unserved |
|---|---|---|
| perp mark | `markPx` | `reference_unserved` path; the instrument counts in the coverage census only |
| the venue's own oracle or index price | first served of `oraclePx`, then `indexPx` | `reference_unserved` |
| funding **service** | presence of `funding` on the context; `fundingHistory` row count | `funding_unserved` |
| open interest | `openInterest` | recorded absence |
| touch spread and top-five depth | one `l2Book` fetch | recorded absence with its call state |

**Basis is defined as**

    basis_bp = (markPx - reference) / reference * 10_000

**computed only from fields the venue serves in the same snapshot.** That
half of the sentence is enforced, not documented: every served number
carries the id of the snapshot it came from, and `npl.h5.basis.basis_bp`
raises `CrossSnapshotBasis` on a mismatch. **`midPx`, `prevDayPx` and
`impactPxs` are registered non-references**: book and mark state, not a
reference. Substituting one for an unserved oracle is exactly the defect
Section 4 exists for, and the mapping from an unserved reference to a
recorded absence is pinned by test.

**If no reference is served for an instrument, that is recorded as
`reference_unserved` and the instrument contributes to the coverage census
only.** No value is imputed, carried forward, or interpolated — ever, in any
series (`npl.h5.basis.basis_series`, pinned).

**The retrospective series (Task 3).** Registered conditionally, before
measurement, because what the venue serves historically is not yet known:

- Where the venue serves a **historical series of the registered basis's own
  construction** — a mark and a reference in the same historical row — that
  is **retrospective basis** and it fires the Section 6 map.
- Where the venue serves only a **differently constructed** deviation series
  (a premium index built on impact prices rather than the mark, say), that
  series is a **named secondary**. It is reported in full with its n by
  session tag, it sizes the census window, and it **may fire CLOSED but may
  never fire VIABLE** (Section 6, the asymmetry, with its reasoning).
- Where the venue serves neither, retrospective coverage is **absent**, per
  instrument, and the entry fires on the forward census instead.

## 4. The honesty clause

**This entry reads no external equity price feed.** Zero dollars, keyless
public endpoints, one venue.

Every reference in Section 3 is **the venue's own**. A basis computed
against a stale or venue-internal reference measures **the venue's own
bookkeeping, not a tradable gap.** Stated plainly, three ways, because this
is the sentence the rest of the entry has to survive:

1. **A wide measured basis is a lead, never evidence of a trade.** It says
   the venue's mark and the venue's reference disagree. It does not say a
   counterparty exists at either price, that the underlying is open, or that
   anything could be executed against.
2. **A narrow measured basis may be an artefact of the mark's own
   construction.** Where a venue builds its mark from a blend that already
   includes its oracle, the difference between them is bounded by
   arithmetic before any market participant acts. **Registered expectation:
   a near-zero registered basis is the more likely measurement**, and it
   would be a fact about the mark-price formula, not about the market. That
   expectation is written here so a small number cannot later be presented
   as a surprise, and a large one cannot be presented as a discovery of
   something this data can establish.
3. **The successor repo would need an independent underlying feed** — a real
   quote for the real equity, on the real exchange calendar — to make any
   claim about tradability. Nothing measured here substitutes for it.

The prior context makes this sharper, not softer. The equity leg through
IBKR refuses fractional orders (error 10243) and bills whole-share round
trips at **40 to 100 bp** at this operator's sizes (HFExperiment ADR-026,
closed and carried), so **no cross-venue pair design is registrable here**
even if the deviation were real and large. A VIABLE row means only that
someone with a better feed should look.

## 5. Session structure

**Every snapshot is tagged by underlying-market session**, computed from the
snapshot timestamp against a **registered US market calendar written before
collection** (`npl.h5.calendar`, committed in this commit), in
`America/New_York`:

| tag | definition |
|---|---|
| `regular` | a trading day, 09:30 up to the day's close (16:00, or 13:00 on a registered early-close day) |
| `extended` | a trading day, 04:00–09:30 and close→20:00 (close→17:00 on an early-close day) |
| `closed_weekday` | Monday–Friday outside those windows, and the whole of a registered full holiday |
| `weekend` | Saturday or Sunday in New York |

The NYSE full-closure and 13:00-close tables are written out by date for
**2024 through 2027** rather than derived, so a rule change in a later year
is an amendment and not a silent recomputation. **A timestamp in an
uncovered year is a loud refusal**, never a default to "open".

**Deviation is characterized within each tag separately.** The tags are not
cosmetic: a perp on a closed underlying has no reference market at all, and
pooling it with regular hours is the fastest way to manufacture a basis that
is really just a stale reference. Every figure in this entry carries its tag
and its n.

## 6. The outcome map

Fired at the end of the census window by `npl.h5.outcome.fire`, from counts
and medians only. The thresholds are **arithmetic on the registered cost
band, not free numbers**: the floor is `CONFIG.hip3_round_trip_bp[1]` =
**18 bp**, and the bar is `h5_viable_basis_multiple` × floor = **3 × 18 =
54 bp**.

**VIABLE.** At least **20 instruments** carry a served reference **and at
least 30 days of coverage each**; the **median absolute basis in at least
one session tag exceeds 54 bp**; and **funding is served on at least half**
those instruments.
*Consequence:* draft a successor hypothesis for a fresh repo, with an
independent underlying feed and its own registration. **No capital.** The
draft is blocked while the Section 9 operator slot is empty
(`npl.h5.priors.require_operator_prior_for_successor`).

**INDETERMINATE.** The coverage bars are met but the basis sits **between 18
and 54 bp** median absolute.
*Consequence:* recorded as a lead requiring the independent feed to resolve.
**No successor authorized on this evidence alone.**

**CLOSED.** The median absolute basis is **under 18 bp in every session
tag**, **or** fewer than **20 instruments** carry a served reference, **or**
funding is served on **fewer than half**.
*Consequence:* the family closes, the entry is written in the register
style, collection stops.

**PENDING** is a fourth, **non-terminal** state and is not a verdict: it
records that at least 20 instruments carry a served reference and funding
clears, but fewer than 20 have reached the 30-day coverage bar, so the
census window is still open. A PENDING row carries the days needed and the
projected fire date. The three terminal states remain exactly the operator's
three.

**Boundary conventions, fixed here:** the VIABLE comparison is **strictly
greater** than 54 (a median of exactly 54.00 is INDETERMINATE); the CLOSED
floor comparison is **strictly less** than 18 in *every* tag (exactly 18.00
in any tag is not CLOSED); the funding bar is **at least** one half (10 of
20 passes, 9 of 20 closes); the instrument bar is **at least** 20. Every one
of those boundaries has a fixture sitting exactly on it.

**The asymmetry for a named secondary series, with its reasoning.** A
deviation series the venue serves under a construction *different* from the
registered basis may fire CLOSED but never VIABLE.
*Why CLOSED is allowed:* if the venue's own deviation bookkeeping never
clears the cost floor anywhere, there is nothing for a better feed to
rescue — the venue is telling us its two internal prices agree.
*Why VIABLE is not:* a large number under a different construction could be
an artefact of that construction — a clamp, an impact-price effect, a
different denominator — rather than a deviation of the registered kind.
Enforced in `npl.h5.outcome.fire` and pinned by test.

## 7. Spend and pacing

**Zero dollars. Keyless public endpoints only.** The H5 census rides the
existing daily pass under `npl.pacing.OPERATING_PACING_S`, charging the one
shared request ledger before sending, like every other collector (standing
rule 9).

**Request budget per pass, stated as arithmetic** (`npl.h5.spend`):

    1 perpDexs
  + 1 meta per HIP-3 dex               (10 at the census)
  + 1 metaAndAssetCtxs per HIP-3 dex   (10)
  + 1 l2Book per resolved instrument   (151 at the census projection)
  ------------------------------------------------------------------
  = 172 requests per pass

**172 of the registered 20,000 daily cap is 0.86 percent**, and 1.15 percent
of the 15,000 daily soft budget the H1/H2 collectors work under. The
registered **H5 pass cap is 1,000 requests, 5 percent of the daily cap**;
a planned pass over it is refused as arithmetic, before anything is sent.

**H5 must not delay or displace H2 work**, and two mechanisms hold that,
neither of them a promise:

1. **Order.** The H5 block runs **last** in the daily pass, after the seal,
   the checkpoints, the retro plan and the fresh plan.
2. **Yield.** H5 refuses to start when the day's ledger spend has already
   reached the H2 soft budget, so a long H2 catch-up postpones H5 to
   tomorrow rather than the reverse.

The retrospective read (Task 3) is a one-off, budgeted separately at
`h5_retro_page_budget` = **12 `fundingHistory` pages per instrument** over
`h5_retro_lookback_days` = **180 days** (12 × 500 hourly rows = 250 days of
headroom). At 151 instruments that is a **1,812-request ceiling**, 9.1
percent of the daily cap, spent once.

## 8. The epistemic boundary

**A VIABLE row states that a deviation exists on venue-served fields, at a
size worth investigating with better data.**

It states **nothing** about returns. Nothing about tradability. Nothing
about capital. It does not imply a counterparty, a fill, a borrow, a hedge,
or an execution path, and it authorizes none of those. The one action a
VIABLE row authorizes is **writing a registration in a different repository**
— and that registration would have to earn its own power verdict against an
independent underlying feed before it measured anything.

A CLOSED row states that the venue's own fields do not show a deviation of
the registered size, or that the instruments do not carry the fields the
question needs. **A documented negative is a valid and expected outcome** —
the assistant's prior below says it is the likely one.

## 9. Priors

**Assistant prior, recorded 2026-08-28 in chat, before any H5 measurement:**

- **0.05** that a real capturable edge exists in this family.

**The adoption warning, standing (carried verbatim):** the NPD Amendment 0
lesson applies — an adopted prior corrupts the calibration ledger. The
assistant's number above is context, **not the operator's number**, and it
must not be copied into the slot below. The assistant never fills the slot.

**The operator prior slot, reserved and empty:**

> Operator prior on the H5 family carrying a real capturable edge: _reserved,
> empty — only the operator fills this, as a probability in [0, 1] followed
> by `(independent)` or `(adopted)`. Nothing else parses._

**What the empty slot blocks.** H5 has no Stage B and no capital, so an
empty slot cannot block a read. It blocks the **consequence** of a VIABLE
row: **drafting the successor hypothesis** (`npl.h5.priors`, exercised by
`tests/test_h5_registration.py`). The map still fires and the row is still
recorded — a verdict is never withheld for want of a prior. Only the action
it would authorize waits.

---

## Amendments
