# LICENCES.md — Stage D: three candidates, read terms-first

Written by Stage D on 2026-08-30. **This stage enumerated nothing.** No
contract, price, order book, volume, bucket count or dispersion was produced by
any task in it, and no market-data request was sent to any venue. Sections 4
and 10 stand intact. Zero dollars spent.

Every claim below is governed by **ADR-012**: a statement about what a source
permits carries a quoted clause, the document's effective date, and the date it
was fetched — or it is recorded UNMEASURED and the stage proceeds as if
permission were absent. The check is `pmexperiment.admissibility`, written in
Task 1 and fired over this repository's own claims before it was fired at
anything external.

---

## Verdict

**No candidate returns PERMITTED.**

| # | candidate | verdict | ground |
|---|---|---|---|
| 1 | a Polymarket written-authorization request | **PROHIBITED** | the in-force Terms prohibit the tool class unconditionally; a route to *request* exists but none is addressed to this asker, and nothing has been requested or granted |
| 2 | published academic datasets of prediction-market records | **UNMEASURED** | the leading dataset states CC BY 4.0 three times, but neither the dataset card nor the CC BY 4.0 legal code prints any date, so ADR-012 element (2) fails; chain of title and AI-clause coverage are separately unestablished |
| 3 | third-party data platforms (Dune among them) | **PROHIBITED** (Dune) / **UNMEASURED** (the rest) | Dune's in-force Terms prohibit bots, crawlers and scrapers, grant no right in data, gate API keys behind a paid subscription, and bind non-registrants; no other platform's document was retrieved |

**UNMEASURED is not a synonym for PROHIBITED.** They carry the same operational
consequence — the stage proceeds as if permission were absent — and different
epistemic content: one is a measured refusal, the other is an absence. The
distinction is enforced in code (`pmexperiment.admissibility.CandidateVerdict`)
and it is the reason candidate 2 is not written down as closed.

---

## Method

### What this stage fetched, and what it refused to fetch

Licence, terms, acceptable-use, contact, pricing and dataset-documentation
pages **only**. No market data, no dataset file, no query result, no API data
endpoint — not once, and not "to check reachability". **"Reachability" in this
document means only that a licence document loaded, at a stated status.** It
never means that data is reachable. Polymarket's and Kalshi's data-reachability
positions remain where Stages A and C left them.

One disclosure made rather than left to be noticed: the Polymarket Institute's
researcher guide, fetched as a documentation page squarely inside that scope,
itself *prints* specimen API responses — a market record, a price, a
price-history array. Those values arrived inside a manual. No endpoint that
would produce them was called, and no such value is used, stored or reported
anywhere. Reading a manual that prints an example is not fetching data, and the
distinction is drawn here rather than blurred.

### Establishing that the document is the document

Stage C's near miss is the reason this section exists: `polymarket.com/tos`
returns HTTP 200 with a 217 KB body that strips to ~1,354 characters, and
reporting from it would have been reporting on an app shell. Every document
below carries its body size and extracted text length.

**The shell signature reproduced exactly.** `polymarket.com/tos` measured
**217,045 bytes → 1,405 characters, 0.65 % text**. The real instrument was
located without rendering anything: the served HTML itself contains, at byte
offset 51958, `<iframe title="tos" src="https://docs.google.com/document/d/1N4a…/preview">`
under a Next.js route segment named `(embedded-docs)`. Searching the shell for
`written consent`, `Effective` and `Notices` returned **zero hits each**.

**The real Terms were read in full and proved complete**: 14 `DOCS_modelChunk`
payloads with insert indices 1, 4080, 8395, 12724, 17396, 21516, 25728, 30289,
34437, 38848, 43982, 48054, 52612, 56807 — each beginning exactly where the
previous ended, **zero gaps**, running 1 → 58,830 and terminating on the
document's own final clause. **58,830 characters / 59,061 bytes**, against the
59,617 bytes Stage C recorded. An independent verification pass reconstructed
the identical 14 chunks with identical indices.

**A limitation of the text-ratio bar, found by using it.** The ratio depends on
the extraction method. On the same retained Dune body, the verification pass
measured **18.05 %** text and this session's own tag-stripping measured
**67.98 %**. Both clear the 5 % bar and the classification is unchanged, but the
bar is method-dependent, and `pmexperiment.admissibility` records absolute
length as deliberately *not* a bar for the separate reason that a short licence
is a whole document. Recorded as a real limitation of the procedure rather than
left for a later session to discover.

### Verification coverage, reported separately from the findings

Standing rule 7: operational health and sample composition never merge. Each
candidate report was to be checked by three adversarial lenses — quotation
fidelity, date provenance, scope and convenience.

| candidate | lenses on the first pass | lenses added by the re-run | final coverage |
|---|---|---|---|
| 1 — Polymarket authorization | quotation fidelity | date provenance, scope and convenience | **3 / 3** |
| 2 — academic datasets | all three | a second scope pass | **3 / 3** |
| 3 — third-party platforms | date provenance, scope and convenience | quotation fidelity | **3 / 3** |

Four of thirteen agents died on a session limit on the first pass; the run was
resumed and every lens now has a result. **The verification was not decoration
and it is reported as load-bearing**, because it changed the document:

- it **overturned** candidate 3's central factual claim — that Dune's in-force
  Terms were unreadable — with one HTTP header;
- it caught **two selective quotations** that had already gone into a draft of
  this file: the Polymarket Terms' only affirmative grant, and Kalshi's
  Section I PERMITTED USES;
- it **refuted candidate 2 on ADR-012 element (1)** as well as element (2), a
  failure the licence read had certified as "satisfied, and generously";
- it **deleted one leg** of candidate 1's counterargument rebuttal as unsound;
- it **closed the AI/ML axis**, which no licence read had searched, on the very
  clause class that decided Kalshi.

Every one of those corrections makes the record weaker or narrower, not
stronger. None of them changed a verdict. Their findings are recorded below
beside the findings they correct, rather than filed separately where a reader
would not meet them.

---

## Candidate 1 — a Polymarket written-authorization request

**Verdict: PROHIBITED.**

### Reachability of the licence documents

11 document fetches, all HTTP 200, all single-shot, no pagination, no retries:
`polymarket.com/tos` (0.122 s), the embedded Terms document (0.258 s),
`help.polymarket.com` (0.317 s), `docs.polymarket.com` builder tiers (0.299 s),
`institutional.polymarket.com` (0.289 s), `polymarket.com/privacy` (0.240 s),
the embedded Privacy Policy (0.715 s), the Kalshi Data Terms PDF (0.345 s), and
three Polymarket Institute pages (0.137 / 0.078 / 0.279 s). Plus 2 WebSearch
queries. **No API host was contacted.**

### The governing document

**POLYMARKET.COM TERMS OF USE**, published by Adventure One QSS, Inc.
**Effective date 2026-08-11**, printed on the document's own masthead under a
genuine `Effective as of` label — not a copyright year:

> POLYMARKET.COM
> TERMS OF USE
> Effective as of August 11, 2026

**Fetched 2026-08-30.** All three ADR-012 elements present.

### The clause that closes it, quoted verbatim

> Use any data mining tools, robots, crawlers, or similar data gathering and
> extraction tools to scrape or otherwise remove data from the Site, any other
> Interface, or Features;

The chapeau governing that list reads only **"You agree that you will not:"** —
verified as carrying no global `unless`, `except`, `provided that`, or
written-consent proviso. The bullet is unconditional on entity type and carries
**no consent path at all**.

The adjacent clause that does carry one attaches to a different act:

> Use any manual process to monitor or copy any of the material on the Site, any
> other Interface, or Features or for any other unauthorized purpose without our
> prior written consent;

**The consent proviso attaches to *manual* processes.** Even a granted written
consent under that clause would not by its terms unlock automated collection.

### The instrument's one affirmative grant, disclosed because it exists

The verification pass found this omitted from the licence read, and it is
recorded here rather than left out, because a method built on quoting the
governing instrument cannot skip that instrument's only licence grant:

> Subject to the Terms, the Company hereby grants you a personal, limited,
> revocable, non-exclusive, non-sublicensable, non-transferable license to use,
> copy, and distribute in connection with such use the Site, any other
> Interface, and Features. This license is solely intended to allow you to
> access, use or otherwise interact with the Site, any other Interface, and
> Features.

It is subordinated (`Subject to the Terms`) and narrowed (`solely intended to
allow you to access, use or otherwise interact with`), so it does not defeat the
data-mining bullet. It is disclosed because it is the instrument's own answer to
the question "does this document grant anything at all?", and the answer is yes,
narrowly.

### Does a contact route exist? Yes — and none of them is addressed to this asker

| route | published where | scope on its face | bears on research data access |
|---|---|---|---|
| `hello@polymarket.com` | ToS `Contact Us`, the document's final sentence | "questions, complaints, or claims concerning the Features" | **no** — a request to compile research data is none of those three |
| `data-licensing@polymarket.com` | `institutional.polymarket.com`, live `mailto:` anchor | opens "If you or your clients are **Capital Markets Entities**" | **closest in subject matter, wrong addressee class** |
| `builder@polymarket.com` | `docs.polymarket.com` builder tiers | builder-program tier upgrades | **no** — see below |
| `institute@polymarket.com` | `institute.polymarket.com` | research initiative front door | weak evidence (3.46 % text page); zero occurrences of `licence`/`terms` |
| `legal@polymarket.com` | Privacy Policy | "comments or questions about this Policy" | no — all 11 occurrences are data-subject rights |
| `press@polymarket.com` | site footers | press | no |

**There is no notices clause.** Searched over the full 58,830 characters:
`Notices` — 0 occurrences, `Notice` — 0. **There is no postal address**: `Attn`
0, `Suite` 0, `P.O` 0, `postal` 0, `mailing` 0; all three occurrences of
`address` are "wallet address" or "e-mail address". `authorization` — **0
occurrences**; Polymarket, unlike Kalshi, never uses the word.

**The data-licensing route is scoped to a class this repository is not in:**

> All Capital Markets Entities looking to consume Polymarket data must do so in
> consultation with Polymarket and ICE. This applies to any Polymarket data or
> content, whether sourced from the API or on-chain, and whether in raw,
> derived, aggregated, or anonymized form.

> If you or your clients are Capital Markets Entities, please contact us here to
> find out more: data-licensing@polymarket.com and
> sales-icedataservices-usinsidesales@theice.com .

That page prints **no effective date** — only `© 2026`, which is not promoted.

**The builder program is gated on order flow, and therefore closed to a
repository that will never trade.** Its published upgrade path, step 2:

> Generate Volume
> Route orders through Polymarket and demonstrate consistent usage.

Its tiers are denominated in `Daily Relayer Txn Limit`; its benefits are Builder
Fees, Order Attribution, Gasless Trading and volume rewards. Across 389,435
bytes: `terms of use` 0, `license` 0, `licence` 0. The Terms mention the program
exactly once, and only as a reservation of the Company's own discretion —
"the Company reserves the right to grant access to … the Company's builder
program" — which confers nothing and invites no one.

### The strongest counterargument, and why it is not taken

Polymarket's own research arm published, on 2026-07-24:

> Polymarket's exchange data is accessible to students, researchers, and
> learners. Our open APIs provide access to markets, orders, trades, and more.

Three reasons it does not move the verdict, each independently sufficient.
**First**, it says *accessible*, not *permitted* — the distinction this
repository has now recorded twice. **Second**, it fails ADR-012 on its face:
occurrences of `licen` on that page — covering license, licence, licensed,
licensing — are **zero**; occurrences of `Terms of Use` are **zero**; and its
only date is a byline on a "7 min read" article, which is not an effective date.
**Third**, the Institute advertises its independence — "The Founding Scientific
Director sets the research agenda, not Polymarket" — and an entity that stresses
it does not speak for Polymarket cannot be read as speaking for Polymarket's
permissions.

**A fourth reason was offered and is withdrawn here rather than carried.** The
licence read argued that the guide "is dated eighteen days *before* the Terms
took effect" and is therefore superseded as a prior representation. The
verification pass refuted the leg: the page was **still live when fetched on
2026-08-30**, so it is a standing published representation *after* the Terms'
effective date, not merely a prior one. The same reading also promotes a
publication byline into a date doing legal work — the exact move the report
refuses one paragraph earlier. **An argument that fails is deleted, not
softened**, and the three that remain are each sufficient without it.

### The Kalshi comparison, corrected

Kalshi names the path verbatim — "unless Kalshi … give you prior written
authorization, you are strictly prohibited from … compiling (including, without
limitation, through framing or systematic retrieval to create collections,
compilations, databases or directories)" — and **publishes no address to walk
it**. Across the full extracted PDF text: `@` **0 occurrences**, `contact`
**0**, `address` **0**.

**Two corrections to this repository's own record travel with that finding.**

**(a) The Kalshi Data Terms of Use print no date at all.** `Effective` — 0
occurrences. `Last Updated` — 0. This was found independently by the licence
read and by this session's own search of every tracked document: the only
effective date anywhere in this repository is Polymarket's 2026-08-11. **ADR-012
states that "Stage A's Kalshi finding met that bar." It met two elements of
three.** The clause is quoted and the fetch date recorded; the effective date
does not exist to be recorded. Under the procedure the Kalshi claim is
**UNMEASURED, not admissible** — and **this changes no verdict**, because
UNMEASURED and PROHIBITED both mean proceed as if permission were absent. What
it changes is the strength the record claims for itself. Pinned in
`tests/test_admissibility.py`.

**(b) Kalshi's Section I PERMITTED USES was never disclosed by this repository,
and it cuts both ways.** Found by the verification pass in the same 6,648-char
document Stage A said it read end to end:

> You may access content only for your personal use for non-commercial purposes.
> Non-commercial use does not include the use of Kalshi Data without prior
> written consent from Kalshi in connection with: (1) the development of any
> software program, including, but not limited to, training a machine learning
> or artificial intelligence system; or (2) providing archived or cached data
> sets containing Kalshi Data to another person or entity.

It is an affirmative personal, non-commercial permission — and it conditions
software development, AI/ML training, and cached data sets on prior written
consent. Quoting only the prohibitions made the Kalshi framing one-sided, and
the omission is recorded rather than quietly repaired.

### Why PROHIBITED and not UNMEASURED

The prohibition itself is fully measured: clause quoted verbatim and contiguous,
a genuine `Effective as of` label on the document, and a stated fetch date. A
candidate named "a written-authorization request" cannot license anything until
an authorization has been requested and granted. **Neither has happened. This
stage drafted nothing, sent nothing, and contacted no one.** A route to ask is
not an answer, and an unexercised route is not a permission.

**The label is stated precisely, because it is easy to misread.** PROHIBITED
here is the **baseline** — what the in-force Terms permit today, absent any
authorization. It is **not** a record that authorization was sought and refused.
**Nothing was requested, so nothing was refused.** A later reader must not
convert this row into "Polymarket declined."

### What the verification pass corrected in this candidate

The verdict is unchanged. Four findings materially qualify how far it reaches,
and are recorded because a claim that survives review unchanged in *scope* as
well as in *conclusion* is rare enough to be suspicious.

1. **The load-bearing clause was quoted without its defined terms, so its reach
   was asserted rather than measured.** "Site", "any other Interface" and
   "Features" are all defined terms in the instrument, and none of the
   definitions was quoted. The prohibition's *existence* is measured; the exact
   boundary of what it covers is not.
2. **The on-chain path is narrower than the licence read claimed.** It stated
   the bullet "prohibits the tool class this measurement would require, today,
   of anyone." That overstates the text. The bullet is scoped to "the Site, any
   other Interface, or Features", and **a public Polygon ledger is none of the
   three on its face**. Amendment 6 already records the Polygon question as a
   live reopening path "under a legal analysis this repository has not
   performed", and that remains its status — neither closed here nor opened here.
3. **The Restricted Jurisdictions list is incorporated by reference and names
   Canada by province.** The Terms cite "the list published at
   `https://docs.polymarket.com/api-reference/geoblock`", fetched HTTP 200 at
   509,725 bytes, which names Canada four times at province level. For a
   Canadian participant the Terms narrow further, as Amendment 6 recorded.
4. **The AI/ML axis is now measured, and it is a null.** Across the
   58,830-character Polymarket Terms: `artificial intelligence` **0**,
   `machine learning` **0**, `large language` **0**, `llm` **0**, `neural`
   **0**. **Polymarket has no AI-use clause where Kalshi has one**, and this is
   a measured absence rather than an unchecked one. It was unchecked until the
   verification ran it — on the very axis that decided Kalshi.

---

## Candidate 2 — published academic datasets of prediction-market records

**Verdict: UNMEASURED**, and it rests on the candidate that came *closest*, not
on the weakest.

### The leading dataset

**`TimeSeventeen/Polymarket-v1`** (Boka Qin, Rui Yang; paper arXiv:2606.04217),
a corpus of on-chain event logs from Polymarket v1 on Polygon. Read as
`/raw/main/README.md` (24,460 bytes) **deliberately, to avoid the Data Studio
viewer on the landing page, which can surface preview rows** — no record was
read.

**Licence stated three times**, and the prose grant speaks to both things this
repository would need:

> license: cc-by-4.0

> | License | CC-BY-4.0 |

> ## License
>
> Released under **CC-BY-4.0**. You may share and adapt the material for any
> purpose, including commercially, provided you give appropriate credit.

**The four fields the power gate needs are all documented**, transcribed from
the card's published schema table and not from any record:

| gate input | field in `daily_aligned/` | documented as |
|---|---|---|
| entry price | `price` (double) | "Raw execution price of the traded outcome token in this row, in USDC.e per share", timestamped by `block_timestamp`; plus `p_event`, an event-normalised probability axis |
| category | `category`, `category_refined` | "Original market category" / "Refined/cleaned market category used in analysis" |
| maturity | `opens_at`, `close_at`, `resolved_at` | "Market open time" / "Market close time" / "Market resolution time, if resolved" |
| resolution **presence** | `resolution_status` | establishes presence **without** reading the value; `winning_outcome_label` also exists and the repository must not read it |

That last row matters: presence is separable from value in this schema, which is
exactly what standing rule 8 requires.

**Depth and coverage, from the documentation only:** `OrderFilled/`
**1,201,580,990 rows** (~49.1 GB compressed Parquet), coverage **2022-11-21 to
2026-04-28**. A documented limitation bears directly on the registered cost
model: "On-chain settlement only: No off-chain central limit order book (CLOB)
quote-level data, cancellations, or resting-order depth is provided" — so the
registered 1-cent half-spread could not be checked against this corpus.

### Why it is UNMEASURED — on two elements, not one

**Element (1) fails as well**, and this correction came from the verification
pass rather than from the licence read, which had certified element (1)
"satisfied, and generously." **The two CC BY 4.0 clauses that grant were quoted
and the two clauses in the same document that limit were passed over** — Section
1's cap on Licensed Rights and Section 5(a)'s disclaimer of title, both set out
below. Quoting a licence's grants while omitting its limits is not a verbatim
reading of the clause bearing on the use; it is a verbatim reading of the half
that helps. **Element (1) is measured as *text present*, not as *an effective
grant*.**

**Element (2) fails.** The dataset card prints no effective, last-updated or
revision label; its only years are data-coverage bounds and a BibTeX citation
year, neither of which may be promoted. **The CC BY 4.0 legal code prints no
date whatsoever** — every four-digit year in the document was enumerated, and
the only dated references are to the WIPO Copyright Treaty of 1996. The grant is
undated and the terms it incorporates are undated too.

**A correction to that finding, made here rather than left standing.** The
licence read concluded "there is no second document to fall back to." **There
is one, it is named on the face of the legal code, and it was not read** — the
footer points to an errata page carrying "the date of change". So element (2)
is recorded as **failing on the documents actually read**, and the one document
that might bear on it was not fetched. That is a gap in this stage's evidence,
not a property of the licence, and it is written down as a gap.

Exactly **one document in the whole sweep carried a properly labelled effective
date** — Hugging Face's own Terms of Service, "Effective Date: September 15,
2022" — and it is the platform's, not any dataset's. Its Open Source clause
expressly declines to override content licences ("The Open Source license terms
are not intended to be replaced or overridden by the license and other terms of
these Terms"), so it hands governance straight back to the undated documents and
cannot cure them.

### Three further gaps, so the date is not read as the only one

The verification pass established that curing the date would **not** make this
candidate usable, and that must be recorded or the escalation below will be
misread as a one-step fix:

1. **CC BY 4.0 self-limits to rights the licensor actually held, and disclaims
   title.** Section 1: "*Licensed Rights* means the rights granted to You … which
   are limited to all Copyright and Similar Rights that apply to Your use of the
   Licensed Material **and that the Licensor has authority to license**."
   Section 5(a) disclaims "warranties of title … non-infringement". The card
   itself states the corpus "is derived from public on-chain activity and is not
   affiliated with or endorsed by Polymarket." **A third-party republisher's CC
   BY tag over a corpus derived from someone else's venue is not a measurement
   that the republisher held the rights to grant it.**
2. **The AI and machine-learning axis was never searched by the licence read** —
   the very clause class that closed Kalshi, on a use that is expressly
   AI-assisted. The verification pass closed it **partially and reports the
   remainder as open**: `artificial intelligence`, `machine learning`, `text and
   data mining` and `automated` are **zero** in the CC BY 4.0 legal code, and
   `artificial`, `machine learning` and `llm` are **zero** on the Polymarket-v1
   card; Hugging Face's Terms mention machine learning only as the platform's
   subject matter, never as a restriction. It remains **unchecked** in the four
   dataset `LICENSE` bodies, in `SII-WANGZJ`'s `DATA_DESCRIPTION.md`, and — most
   sharply — in **Manifold's Terms of Service, which was not read and which is a
   prediction-market venue's ToS, the same document class where the Kalshi
   prohibition lived.**
3. **Whether a venue's terms reach a downstream on-chain-derived corpus at all
   is a question this repository has registered as open**, not settled. Amendment
   6 records the Polygon-read question as a live reopening path "under a legal
   analysis this repository has not performed." The licence read wrote "Neither
   venue's terms govern this candidate" — **a positive assertion about the reach
   of a document, which is exactly the class of claim ADR-012 governs**, and it
   carries no clause and no date. The correct record is: **the venue terms'
   reach over this corpus is UNRESOLVED**, and the repository proceeds as if
   permission were absent. The card's own provenance section also narrows its
   blanket "derived from public on-chain activity" disclaimer — it enumerates
   `OrderFilled` events from Polymarket's first-generation exchange contract —
   so whether the *market metadata* fields the gate needs (`category`,
   `opens_at`, `close_at`) are on-chain in origin is **not established by the
   documentation**.

### The other datasets, each recorded

| dataset | licence as documented | why not | depth |
|---|---|---|---|
| `SII-WANGZJ/Polymarket_data` | "MIT License - Free for commercial and research use" | no effective date; its one date label sits under `## Dataset Statistics` and dates the **data**; maturity/resolution/category not established from the card | card and GitHub README **contradict each other**: 1.9 B records / 538,587 markets vs 1.1 B / 268 K |
| `gregyoung14/openmarket-btc-polymarket` | frontmatter `license: apache-2.0` only | no prose grant; **conflicts** with the source repo, which GitHub reports as `NOASSERTION`; **no category field at all** — BTC up/down binaries only, so no cross-category axis for a gate | ~727 M rows, 2026-03-14 → 2026-07-01, with a documented collection gap 22 Apr – 12 May |
| `thomaswmitch/kalshi-*` | bare frontmatter `license: mit`, no prose grant | undated; the markets card documents no snapshot timestamp, so a price *at a point in time* is not established | ~10,016 markets / ~5.08 M trades, Aug 2023 – Aug 2025 |
| `jon-becker/prediction-market-analysis` | **NONE STATED** for the data | no License section at any heading level; the repo-level MIT does not on its face reach a 36 GiB corpus served from a different origin. **Public downloadability is not a licence.** | self-described largest public Polymarket + Kalshi corpus |
| Manifold data dumps | **no licence identifier**; "provided for personal and non-commercial use only", restrictions incorporated by reference into a ToS **not read** | an inherited venue restriction, recorded as the case this task asked to be flagged separately | — |
| arXiv:2604.20421 lifecycle suite | no landing page or licence located | recorded absent, not permissive | on paper the deepest: 770 k+ markets, 943 M+ fills, Oct 2020 – Mar 2026 |
| IEM / PredictIt / Metaculus / Betfair | no published dataset licence located | IEM access appears to run through direct contact; **nobody was contacted** | — |

### The tension this candidate raises, escalated and not resolved

ADR-012's effective-date requirement was written against a mutable
Terms-of-Service page that a venue can silently rewrite, where knowing *which
version* you read is the whole game. **CC BY 4.0 looks like a different kind of
object**: `4.0` *is* its version identity, and its grant is by its own words
"irrevocable". Applied literally, ADR-012 makes it impossible for **any**
CC-licensed dataset, anywhere, ever, to be recorded PERMITTED — because no
Creative Commons legal code prints a date.

**The strongest form of that argument does not survive its own document.** The
legal code's footer reads: `Version 4.0 • See the errata page for any
corrections and the date of change.` **The instrument carries an external,
dated corrections register**, so "the text does not drift" is contradicted by
the text. That cuts *toward* requiring a date, not away from it — which is the
opposite of what the argument needed, and it was found by the verification pass
rather than by the read that made the argument.

**That tension is recorded, and this stage does not resolve it.** The operator
prompt forbids softening ADR-012 to admit a candidate, and softening a standard
at precisely the moment it excludes the one attractive candidate — having
applied it without complaint to Kalshi and to Polymarket when it excluded them —
is what standing rule 9 exists to prevent. **The gate stays closed.**

If a later session judges that immutable named public licences should satisfy
element (2) by version identity in place of a printed date, that is a defensible
**numbered amendment, registered before the measurement it governs** — and it
would still leave the three gaps above untouched. **Curing the date is not the
whole distance to usable, and no reader should take it as such.**

---

## Candidate 3 — third-party data platforms carrying prediction-market tables

**Verdict: PROHIBITED for Dune, the one in-scope platform measured. UNMEASURED
for the rest.**

### The correction the verification pass forced, recorded first

The licence read reported that Dune's current Terms were **unreadable** —
"Cloudflare blocks every non-browser client", "Cloudflare is fingerprinting the
TLS/client, not the headers" — and quoted every Dune clause from archived
snapshots labelled `Last updated on: May 20th, 2025`, while publishing a verdict
of PROHIBITED.

**That was wrong twice over, and both errors matter more than the verdict.**

**First, the unreadability claim is false.** Bare `curl` returns 403; the same
`curl` with nothing added but a browser `User-Agent` returns **HTTP 200**. The
in-force instruments were one header away. Independently re-extracted in this
session from the retained 172,750-byte body: **`Last updated on: June 3rd,
2026`** is printed in the document, and every load-bearing clause is present —
`bots, crawlers, scrapers`, `a mean other than Dune`, `copy or mirror any
material`, the `non-exclusive, non-transferrable, non-sublicensable, revocable,
and limited right to use the Services` grant, and `Dune retains all rights to
all elements of the Service`. The zero-counts hold in the current text too:
`aggregat` 0, `derived` 0, `redistribut` 0, `republish` 0, `resell` 0. The SQL
API Addendum in force is labelled `Last updated: May 13, 2026`.

**Second, PROHIBITED on an unread instrument is a synthesized value.** This is
**Amendment 1's error with the sign reversed**: Amendment 1 inferred *permission*
from a document it never read; the licence read inferred *prohibition* from a
document it never read. ADR-012 has no direction-of-travel exemption, and
standing rule 5 — "absence is a recorded state, never a synthesized value" —
forbids it in both directions. ADR-012 prescribes two distinct outputs and they
must not be collapsed: **record UNMEASURED** (a recorded state) and **proceed as
if permission were absent** (an operating posture).

The verdict below is PROHIBITED because the in-force instrument has now actually
been read, not because the archived one was.

### The governing documents

**Dune Terms of Service**, label **`Last updated on: June 3rd, 2026`** — a
*last-updated* label, and the substitution for an *effective* label is disclosed
here rather than silently made. **Fetched 2026-08-30**, 172,750 bytes
decompressed. The **Dune SQL API Service Addendum** (`Last updated: May 13,
2026`) is expressly incorporated and "applies in addition to the General Terms
and Conditions", so both govern jointly.

### The clauses

> By accessing or using any Service, you signify that you have read, understand,
> and agree to be bound by these Terms of Service, REGARDLESS OF WHETHER YOU
> HAVE REGISTERED WITH DUNE AS A USER.

A non-account holder is bound by the prohibitions and receives no grant.

> bots, crawlers, scrapers, or other automated means

> use a mean other than Dune's provided interface

> copy or mirror any material contained on the Site or the Services

> Dune retains all rights to all elements of the Service

The single user-facing grant is a "non-exclusive, non-transferrable,
**non-sublicensable**, revocable, and limited right to use the **Services**" —
a right to use a service, not a right in data, and non-sublicensable, so it could
not extend to a reader of a published result.

**Programmatic query is account-gated with no keyless path.** The Addendum:
"After the User's subscription to a Subscription Plan, Dune will provide User
with applicable API Keys". This repository holds no account, and creating one,
accepting terms, or subscribing are all outside what it may do without an
explicit operator instruction (standing rule 11).

**Permission was searched for affirmatively, not inferred from silence.** In the
Dune Terms: `aggregate`, `derived`, `redistribute`, `republish`, `resell`,
`resale`, `commercial use`, `creative commons`, `open source`, `public domain`,
`free to use` — **zero occurrences each**. `grants you`, `we grant`, `you may
use`, `permitted to` — zero each.

### What tier that requires — UNMEASURED, and deliberately so

`dune.com/pricing` is a client-rendered shell in both the archived copy (56,756
bytes → 81 characters, **0.14 %**, text ending in "Loading") and live (67,316
bytes → 269 characters, **0.40 %**). The docs page that does carry a credit rate
prints no effective date; a schema.org `dateModified` exists in its metadata and
**a modification timestamp is not an effective date**. A search summary offered
"$390/month Plus, $1,990/month Premium" as tilde-prefixed approximations from no
document that was read; **those figures are not adopted**. The tier price is
recorded UNMEASURED rather than filled in.

### The other platforms

**Token Terminal** — Terms "last updated on: February 22, 2024", read live and
fully measured (86,702 bytes, 25.06 % text). It prohibits aggregation for
onward supply: "Copy, manipulate or aggregate any Content (including data) **for
the purpose of making it available to any third party**". **Two corrections the
verification forced:** its licence grant is "solely for your personal or
non-commercial use", which **covers** a retail individual's non-trading research
rather than prohibiting it — citing it as a prohibition inverts it; and Token
Terminal was **never established to carry prediction-market tables at all**, so
it is not properly a platform of this candidate and cannot carry the verdict.

**Flipside Crypto, Allium, Nansen, Sim** — **no governing document retrieved.**
Unavailable, never permissive. `sim.dune.com/terms` answers 301.

**One quotation finding, recorded because the standard is verbatim.** All 17
quoted or attributed strings for this candidate are present and contiguous in
the documents named. **14 match byte-for-byte; 3 differ only in typographic
apostrophes and quotation marks** — a silent normalisation, immaterial to
meaning, and disclosed rather than left for a reader to discover on their own
re-fetch.

### The finding that survives regardless of any of the above

**Dune's terms nowhere establish that Dune holds redistributable rights in the
third-party prediction-market data it surfaces.** Routing through a third-party
platform cannot cure the upstream position that already fired PENDING_ACCESS on
Polymarket. **A third party's convenience is not permission.**

---

## What each candidate would and would not license

No candidate returns PERMITTED, so the registered questions — which universe
becomes measurable, whether the Stage B region of 91–99c is reachable inside it,
and whether the Canadian-permitted filter can be applied to its records — are
**not reached for any candidate**. They are recorded as not reached, not as
answered in the negative.

The one candidate that came closest is recorded with what it *would* have
offered, so a later session does not have to rediscover it: `Polymarket-v1`
documents all four gate inputs and 1,201,580,990 rows over 2022-11-21 to
2026-04-28, which on its documentation would make the unrestricted Polymarket
universe measurable, and it carries the `category`, `opens_at` and `close_at`
fields the Canadian-permitted filter of economic indicators, financial markets
and climate at a 30-day minimum maturity would need. **It documents no
order-book depth, so Amendment 5's volume floor could be applied but the
registered 1-cent half-spread could not be checked.** None of that is licensed,
and none of it is measured.

## The transfer statement, which holds whatever the outcome

**Any measurement on Polymarket records — from the venue, from a dataset, or
from a third-party platform — licenses a statement about Polymarket and nothing
whatever about Kalshi.** H1t remains **UNTESTED** on three grounds: a documented
Kalshi bias reported not to replicate on Polymarket, the largest Polymarket study
reporting no general longshot bias where other work finds one on Kalshi, and this
program's own MLCryptoEngine H2 measuring cross-venue transfer at **AUC 0.501**.

**A dataset licence changes the permission, never the venue.** A CC BY 4.0 grant
over Polymarket-derived records would license reading those records; it would not
make them evidence about a Canadian-tradeable venue. No Polymarket figure exists
today, and none may ever be written anywhere as evidence about Kalshi.

---

## What this stage did not read, recorded so it is not mistaken for absence

A completeness pass over all three candidate reports found that **the candidate
space was sampled, not enumerated**, and the gaps are listed here rather than
left for a later session to rediscover. None of them is a document that was read
and found permissive; all are documents that were **not read at all**.

| not read | why it matters |
|---|---|
| **Versioned repository deposits — Zenodo, Dataverse, OSF, figshare** | **the sharpest gap.** A DOI landing page prints a licence, a publication date and a version *by construction* — the one document class that routinely satisfies all three ADR-012 elements. Candidate 2 reached UNMEASURED on element (2) **without fetching a single deposit landing page**, recording only a search-result absence. |
| the **CC BY 4.0 errata page**, named in the legal code's own footer | bears directly on element (2), the element candidate 2 fails |
| **Manifold's Terms of Service** | its data page incorporates the restrictions by reference; the governing instrument was left at the door, and it is a prediction-market venue's ToS — the document class where the Kalshi prohibition lived |
| **six Dune addenda incorporated by reference**, including the Data Hub Service Addendum | the Data Hub is the product closest to a data study; only the SQL API Addendum was read |
| **Token Terminal's Subscription Agreement** | its ToS was called fully measured while naming an agreement that was not read |
| **Kalshi's non-PDF surface** — main Terms of Use, help centre, API documentation licensing | one 3-page Data Terms PDF was the whole of the Kalshi reading in this stage |
| **ICE documents** | Polymarket institutional data is distributed through ICE, whose address is quoted and whose terms are unread |
| **IEM, PredictIt, Metaculus, Betfair**; Kaggle, BigQuery public datasets, Snowflake Marketplace, subgraph hosts | dismissed in a line each, or never considered |
| **regulatory disclosure routes** | Kalshi is a CFTC-designated contract market with public reporting obligations; whether settlement history is obtainable from a **regulator** rather than a venue was never asked |

**The direction of bias is named: an under-sampled candidate space biases toward
UNMEASURED**, which is the fail-closed direction and therefore the safe one —
but it is still a bias, and a verdict of "there is none" is a verdict over what
was read. **It is not a proof that no permitted route exists.** The honest
position below is stated with that limit attached, not without it.

**One further observation from the completeness pass, recorded because it is
uncomfortable and correct.** Three reports on permission produced **zero
coverage figures** — no bucket count, no per-category resolved-contract count,
no dispersion, from any route. That is this stage's registered scope working as
designed: it enumerates nothing. But the precedent this repository was built
against, NPDExperiment, failed on **power**, not on permission. **Even if an
authorization were granted tomorrow, the power question would still be
unanswered**, and nothing in Stages A through D has moved it.

---

## The honest position

**No candidate returns PERMITTED. There is none among the routes this stage
read.**

**The consequence, stated plainly: the calibration question is unmeasurable at
this house's standard until an authorization is granted.** Not unmeasurable in
principle, and not unmeasured because the arithmetic came out badly — the power
gate has still never fired, on any venue, over any region. Unmeasurable because
every route to the records either prohibits the reading or cannot show it is
permitted, and this repository does not proceed on the second any more than on
the first.

**What the register now carries, in full:**

| finding | status | what stands behind it |
|---|---|---|
| **BAND-OPEN**, entry prices 91–99c held to resolution, requiring 5.85 points at k = 1 against a band top of 8.00 | **fired 2026-08-29** | arithmetic over registered constants. **No calibration measurement whatsoever.** |
| Kalshi access | **PENDING_ACCESS**, 2026-08-29 | terms; and now, under Stage D's own procedure, **UNMEASURED on the effective-date element** |
| Polymarket access | **PENDING_ACCESS**, 2026-08-30 | terms, effective 2026-08-11, quoted and dated |
| three licence candidates | **PROHIBITED / UNMEASURED / PROHIBITED**, 2026-08-30 | this document |
| H1 | **OPEN**, unmeasured on every route examined | nothing |
| H1t, transfer | **UNTESTED** | nothing, and there is nothing to transfer |

**BAND-OPEN is a cost finding with no calibration measurement behind it, and
that sentence is the whole of what this repository has established about
prices.** It records that cost alone does not close the question. It is not
evidence that an edge exists. Every magnitude any cited source places inside its
surviving bucket — Bürgi's 2.0 and 3.0 points — **fails** the cost floor, and
the band survives on its registered top, set by the one source whose n the
registration never recorded.

### Why this is a terminal state and not a setback

**It is the outcome the design was built to produce cheaply, and it produced it
cheaply.** Four stages: **zero dollars, zero contracts enumerated, zero
market-data requests to Polymarket, and no statistic relating a price to an
outcome anywhere in this repository.** The precedent this repository was built
against — NPDExperiment — discovered its answer after 415 days of collection, in
the same session that read the result. This one has discovered, before
collecting anything, that the collection is not permitted.

**A negative on access is a real finding about the world, not a failure to
find one.** The finding is: *the public prediction-market record is technically
reachable and, at every route this stage could read, not licensed for the
systematic reading a calibration measurement requires.* Two venues and three
third-party routes now say the same thing, in five different documents, for four
different reasons. That is a result. It is the result.

**And the register is honest about what it cost.** The permitted-subset filter
has still never been applied to a real enumeration. Amendment 5's volume floor
of $1,000 is registered and **never exercised** — its cost in sample is
unmeasured, reported absent rather than as zero. Those are not oversights; they
are the registered casualties of an access verdict, exactly as Section 0.3
prescribes.

### What is deliberately not done here

**No fourth venue is proposed.** The prompt forbids it and the reasoning is the
repository's own: proposing a new venue after three routes close is how a
measurement-only project turns into a search for a venue that will say yes, and
the sequence Kalshi → Polymarket → datasets → platforms has already produced one
retracted amendment for exactly that reason.

**ADR-012 is not softened to admit a candidate.** The one candidate it excludes
on a technicality it arguably was not written for — a CC-licensed dataset, which
no Creative Commons legal code dates — is recorded with that tension stated in
full, escalated to the operator, and **left closed**. Curing the date would not
open it anyway: element (1), chain of title, and the AI-clause gap all remain.

### What would change it

Only these, and each is an operator decision rather than a measurement:

1. **Written authorization** from Adventure One QSS, Inc., or from Kalshi. This
   remains the only path that reopens measurement on a **Canadian-tradeable**
   venue, and Stage D establishes that Polymarket publishes addresses but none
   addressed to this asker, while Kalshi names the ask and publishes no address
   at all.
2. **A numbered amendment** on whether an immutable named public licence
   satisfies ADR-012's element (2) by version identity — registered *before* the
   measurement it governs, and only alongside closing element (1), the chain of
   title, and the AI-clause search.
3. **A paid tier** at a third-party platform, which requires an account, an
   acceptance of terms and a payment — all outside standing rule 11 absent an
   explicit operator instruction — and which would still not establish that the
   platform holds redistributable rights in the underlying records.

None of these is a second look, because no outcome has ever been read.

---

# Addendum — Stage E, 2026-09-02: one of these routes was answered

**This section is appended, not an edit.** Everything above it stands as Stage D
wrote it on 2026-08-30, including the verdicts, so a reader can see what was
believed then and what is known now.

**Row 1 of "What would change it" was travelled, and it answered.** Kalshi's
institutional desk replied on **2026-09-01** that the use as described **fits
their Internal Use data licence** — **it was not declined on the merits** — and
that applying requires **an established legal entity** with formation documents
and beneficial-owner verification. It further reports that the **2021 historical
depth is available through historical endpoints** on that licence, not subject
to the live-data cutoff Stage A measured at roughly spring 2024. Full record in
`docs/ACCESS.md`, REGISTRATION.md Section 15.4 and DECISIONS.md ADR-016.

**What that does to this document's central sentence.** "There is none among the
routes this stage read" was true and remains true of what Stage D read. **"There
is none" was never true of the world**, and this document said so in its own
limits section: *the candidate space was sampled, not enumerated*, and *"there is
none" is a verdict over what was read, and it is not a proof that no permitted
route exists.* **The caveat was vindicated in two days.** It is the strongest
argument this repository can offer for writing completeness limits at all.

**One row above is now known to be incomplete as written.** Row 1 says Kalshi
"names the ask and publishes no address at all". A reachable institutional desk
exists; **how it was reached is not recorded here**, because this repository did
not reach it and will not synthesize the route. What is recorded is that Stage
D's search for a Kalshi contact route was not exhaustive, in a document that
already said its search was not exhaustive.

**What has not changed, and must not be read as having changed:**

- **No licence was granted.** Nothing was applied for, so nothing was granted and
  nothing was refused. The route exists; it was not travelled.
- **The claim is UNMEASURED under ADR-012**, on element (2) — correspondence
  carries a received date, not an effective date — and in substance on element
  (1), because what is held is the operator's summary, not the reply's text.
- **Three questions survive the entity requirement, all unread:** the fee,
  whether Internal Use permits **publishing** a calibration result, and whether
  it carries the **AI/ML written consent** that Kalshi's Section I conditions
  separately. **An established legal entity is a necessary step, not a
  sufficient one.**
- **BAND-OPEN is still a cost finding with no calibration measurement behind
  it.** Nothing in the reply is a price, and no statistic relating a price to an
  outcome exists in this repository.
- **The transfer statement is untouched.** A dataset licence changes the
  permission, never the venue — and neither does a venue licence change the
  absence of a measurement.
- **No fourth venue is proposed.** A route answering is not a licence to resume
  the search.

**And one thing this addendum does not do: it does not reopen Stage D's other
two verdicts.** Polymarket and the three licence candidates are where Stage D
left them. One route answered; the rest were not re-asked.
