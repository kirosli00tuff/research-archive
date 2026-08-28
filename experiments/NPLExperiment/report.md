# NPLExperiment — the stage narrative

Append-only, one section per stage, written for the moment it lands. From
Stage B forward, progress.md is the slim state log (ETA against actual,
newest last) and this file carries the narrative. Nothing here is ever
revised to fit a result; a correction is appended, dated, and says what it
corrects.

The project in one sentence: a measurement-only test of whether newly
listed Hyperliquid perpetuals drift down over 30 and 90 days by more than a
short pays in funding and fees — no trading, no capital, no keys, and a
documented negative is a valid and expected outcome.

---

## Stage A — registration, census, power, arming (2026-08-27)

Stage A opened at 00:31:45Z with an empty directory and closed at 09:20Z
with a registered design, a censused venue, a GO verdict, and armed
collectors. Nothing in between read an outcome value: outside the sealed
raw writers, no code path in this repository has ever parsed a candle
open, high, low, close, or volume, or a funding rate stamped after its
event entry. The verdict machinery exists, is tested, and has only ever
seen synthetic fixtures.

**The registration came first.** Sections 0–13 of REGISTRATION.md — the
hypothesis, the universe rule, the entry anchor at the second daily close,
the net-short outcome with its sign convention, the cost bands, the
funding-matched control, the truncation rule for delistings, three
co-primaries at alpha_adj = 0.016952, the exact-binomial power method, the
Stage B trigger, and the priors — were committed before the first network
request. The request ledger was empty at that commit; that ordering is the
whole point.

**Access measurement falsified the naive design, before any census
(Amendment 1).** The retention probe (n = 12 instruments) found the venue
serves index-backfilled 1d candles predating its own funding archive epoch
of 2023-05-12T00:00Z — majors' candles begin in 2020, so a first served
candle is not a listing date for anything old enough to reach the epoch.
For every probed instrument listed after the epoch (7 of 7), first 1d
candle, first 1h candle, and first funding row agree on the same UTC day.
And two instruments (UNIBOT, CYBER) show candles beginning 49 and 10 days
before their first archived funding row — the mechanical signature of a
hyperp pre-vanilla phase, visible in timestamps alone. Amendment 1
therefore added the funding cross-check at the registered ±1 day, censored
the pre-epoch era (74 instruments, never events, usable as controls), and
made the hyperp tag mechanical, with the event date at the funded phase's
start. The bias direction was stated at amendment time: every one of these
moves pushes the measured effect toward the null, not away from it.
Delisting observability — the survivorship test that decides whether a
retro cohort is even legitimate — passed in full: 6 of 6 probed delisted
perps still serve both candle and funding history. Rate ceilings were
measured per endpoint (n = 846 ledgered probe requests; refusals on
exactly two endpoints, verbatim `null` at HTTP 429) and operating paces
registered at half the measured ceilings.

**The census and the gate.** 503 instruments enumerated (232 main dex, 271
across 10 HIP-3 builder dexs). Retro-eligible events: **N = 312** — 112
vanilla, 46 hyperp_conversion by the mechanical tag, 154 hip3 — of which
10 are truncated_by_delisting and retained per Section 7. Pending
(younger than horizon): 62. Excluded: 129 (74 epoch_censored, 53
no_candles, 1 no_funding_rows, 1 died_before_entry). The funding-coverage
bar excluded zero of 312 measured windows. Control feasibility: **176 of
312 events (56.4 percent)** have a Section 6 candidate; the 136 unmatched
stay in P1 and P2 and drop from P3 only. Exact binomial power at the
registered assumptions (0.85 / 0.65 / 0.70), at achieved N = 312 events
and 176 pairs: **P1 1.000, P2 0.9993, P3 0.9995**, against minimum-N bars
of **34, 103, and 60**. Section 0 fired **GO** at 05:28:09Z with every
input figure recorded beside it in the amendment log.

**Arming and the seal.** systemd user units installed at 05:29Z
(npl-watch hourly at :05, npl-daily at 01:40 UTC; AiTrader's 22:30 and
solattn's 00:40 timers verified untouched). The retro backfill sealed 312
event candle windows and 8,710 funding pages across 386 instrument
archives (407 MB) by 09:09:35Z, 12,118 requests against the 15,000 soft
budget, zero dollars, no keys. Control assignment wrote 176 pairs (of 176
feasible) to the append-only ledger; the control candle windows completed
under the 2026-08-28T01:40Z daily pass. The mutation exercise ran five
registered mutations against real source — a deleted blindness pin, an
absence coerced to zero, rate_limited merged into no_data, a boundary
moved off 0.80, a post-entry funding read inside matching — and the suite
caught **5 of 5**, with source restored byte-for-byte and bytecode purged
before every run.

**The operator's conditions closed after close-out.** The Section 13 prior
slot was filled 0.40 (adopted) on operator instruction dated 2026-08-27,
and the stage ladder (docs/STAGES.md) recorded rows A and B as registered
fact with C and D as operator-revised sketch. Stage A ended with exactly
one Stage B condition outstanding: the explicit operator instruction.

---

## Stage B — the sealed read (2026-08-28)

The operator instruction arrived 2026-08-28: execute the registered single
read of the sealed Stage A retro cohort, fire the verdict against a table
registered before the read, and act on the row that fires. Stage B trades
nothing, touches no capital, and sends no network request of its own —
every input is already on disk, and any gap resolves by waiting for the
next daily pass, never by an in-session fetch.

This section is appended task by task as the stage runs.

### B.0 Task 0 — prompt log and this file

The operator prompt is logged verbatim in progress.md
(2026-08-28T02:31:22Z entry). This report seeds with the Stage A narrative
above, condensed from progress.md and the Section 0 verdict record. From
here forward progress.md stays the slim state log.

### B.0 Task 1 — the push protocol (Amendment 2)

Amendment 2 records the operator instruction dated 2026-08-28 superseding
the Stage A push-nothing protocol, and resolves the postscript conflict at
the top of progress.md in favor of pushing. The remote was found already in
place — `origin = git@github.com:kirosli00tuff/NPLExperiment.git`,
visibility PRIVATE, origin/main already at the Stage A close commit — so
no remote was created; every Stage B commit pushes to it.

### B.0 Task 2 — preconditions: PASS (2026-08-28T02:47:28Z)

Every check ran from local files and lifecycle logs only, through the
blindness readers (t, T, time, row counts), and the session sent zero
network requests. The results, each figure with its n:

- **Operator prior:** the Section 13 slot is filled — 0.40 (adopted),
  written by the assistant on operator instruction 2026-08-27.
  `require_operator_prior` passes.
- **Sealed completeness:** 312 of 312 event candle windows sealed and
  hash-verified; 176 of 176 control candle windows sealed and
  hash-verified (the 2026-08-28T01:40Z daily pass completed the 169
  outstanding); every live window's funding archive reaches the last
  hourly stamp inside its 90-day verdict window, and every truncated
  window's archive exists to its instrument's death. Zero shortfalls.
- **Cohort reconstruction:** the plan, census, and pairs ledgers reproduce
  the registered cohort exactly — 312 events (10 truncated_by_delisting)
  and 176 control windows; every plan row is either a resolved event or a
  queued control window, none unaccounted.
- **Coverage bars** (candles ≥ 0.90, funding hours ≥ 0.95, inside each
  verdict window): 312 of 312 events pass at 30 days and 312 of 312 at 90;
  175 of 176 controls pass at both horizons. The one failure is
  NEIROETH, the assigned control for the APEX event at entry day 20360:
  NEIROETH was delisted at that event's entry, so its verdict window has
  zero expected days and it is excluded **underpowered** (n = 1 pair
  dropped from P3, counted; the event stays in P1 and P2).
- **Effective N:** P1 312, P2 312, P3 175 — against the registered
  minimums 34, 103, 60. All clear.
- **Gates:** ruff clean, mypy --strict on 50 files, 159 tests green.
- **Hashes:** sha256 of all 19 modules on the read surface recorded in
  reports/stage_b/hashes_b0.json (verdict.py:
  see file — any post-B.1 diff voids the read authorization).
- **The latch:** data/state/stage_b_read.json does not exist. The read is
  unspent.

### B.1 Task 1 — Amendment 3: the verdict table, registered before the read

Amendment 3 was committed and pushed (commit 6399d63) while the only data
in existence were counts, timestamps, and coverage — before the reader
existed. It registers the three-row table (GO / PARTIAL_DRIFT / FAIL) with
consequences, the riding rules (secondaries never move a row; central
costs decide with the 3, 18 / 6, 36 bands descriptive; a latch written
first so a crash spends the read), and seven reading rules fixing every
discretion point — entry close, exit close and its last-served-close
fallback, the funding sum's window and sign, symmetric control
truncation, cost classes, pending exclusion, and the closed secondaries
list. The blindness allowlist gains exactly one module,
npl/stageb/reader.py, with npl/stageb/cli.py as its only importer, both
held by new AST pins in tests/test_guards.py (an equality pin on the
allowlist tuple and an importer scan).

### B.1 Task 2 — the reader and the known-answer gate

npl/stageb/reader.py implements Sections 3–7 and the reading rules;
npl/stageb/cli.py is the single entrypoint (`hash` and `read`), applying
the Amendment 3 table mechanically. The full verdict path re-ran on the
synthetic fixtures — 172 tests green (ruff clean, mypy --strict on 53
files) — and the known answers reproduce to the digit:

- Price 1.0 → 0.7 over 30 days with 720 hourly rates at +1e-5:
  price term **0.3**, funding term **+0.0072** (n = 720 rows), net at
  central 9 bp **0.3063**.
- Flat price with 720 hourly rates at −1e-4: funding term **−0.072**,
  net **−0.0729** — the Stage A.3 fixture answer reproduced through the
  sealed path (the funding-sign pin).
- Delisting after day 9 (close 0.5): valued at the last served close,
  price term **0.5**, funding stops at truncation (n = 240 of 720 rows,
  +0.0024).
- Missing exact horizon candle: exit falls back to the last served close
  at or before entry + H (day-28 close 0.8 → price term 0.2).
- Missing entry candle: a recorded absence (no_candles), underpowered,
  never a number.
- End-to-end paired fixture (event 1.0 → 0.7 at +1e-5 funding against
  control 2.0 → 1.9 at −1e-5): event net30 **0.3063** (low 0.3069, high
  0.3054), net90 **0.4207**, control net30 **0.0419**, paired H8 funding
  differential **+0.0144**, price differential **+0.25**, P3 1 of 1.
- The latch: a read spends it; a second read refuses (ReadAlreadySpent);
  a pre-existing latch refuses before any work; a tampered or missing
  hash record voids the authorization (ReadAuthorizationVoided).

**The B.1 re-hash** (reports/stage_b/hashes_b1.json, 21 modules): exactly
one diff against B.0 — stageb/__init__.py, gaining the registered
allowlist constant, the diff Amendment 3 itself sanctions — plus the two
new modules (reader.py, cli.py). Every other read-surface module is
byte-identical to its B.0 hash. From this point any diff voids the read
authorization; the CLI verifies the full 21-module surface before writing
the latch.

### B.2 — the read, and the row that fired: FAIL

The latch was written at 2026-08-28T03:01:01Z with the 21 module hashes
inside (latch sha256 2d204ccb…438f67e), and the single CLI invocation
completed at 03:01:08Z, writing reports/stage_b/read.json (sha256
44554896…be840c). The preconditions re-verified inside the same
invocation: 312 events, 176 controls, effective N 312 / 312 / 175,
pending 0 at both horizons, 224,633 funding rows summed inside the
30-day windows, zero network requests.

**The three co-primaries at alpha_adj = 0.016952, central costs:**

| test | figure | n | statistic | bar | verdict |
|---|---|---|---|---|---|
| P1 profitability | 197 positive (63.14%) | 312 | lower bound 0.5707 | ≥ 0.60 | **FAIL** |
| P2 magnitude | 111 at ≤ −15% (35.58%) | 312 | p = 1.000 | > ½ at alpha | **FAIL** |
| P3 listing-age contrast | 114 young < control (65.14%) | 175 | p = 3.767e-05 | negative | **PASS** |

The Amendment 3 table is mechanical: P1 or P2 failing fires **FAIL**.

**The secondaries, descriptive, each with its n:**

- Cost bands: P1 lower bound 0.5740 / 0.5707 / 0.5609 at low / central /
  high (198 / 197 / 194 successes of 312); P2 and P3 identical at every
  band. The verdict is cost-insensitive.
- 90 days: share positive 208/312 = 66.7%, lower bound 0.6069 (would sit
  above 0.60 — descriptive only); P2-90d 159/312, p = 0.389; P3-90d
  111/175, p = 2.36e-04.
- Strata, share positive at 30d: vanilla 67.0% (n = 112),
  hyperp_conversion 69.6% (n = 46), hip3 58.4% (n = 154) — the HIP-3
  stratum, 154 of the 312, is the weakest.
- Truncated by delisting: 5 of 10 positive.
- H8 decomposition (n = 312): mean funding term +1.33%, mean price term
  +1.00% per event over 30 days — the average short earned about +2.2%
  net, dominated by funding, not price. Paired (n = 175): funding
  differential +0.88 points, price differential +6.43 points against
  funding-matched controls.
- Forward-versus-retro: zero forward events readable; the forward cohort
  was never pooled and now closes unread (pending-at-closure).

**What the sample actually said.** The listing-age effect is real — P3
passed at 3.8e-05 and young perps underperformed their funding-matched
controls by 6.4 price points on average — but it is thin per event: most
young listings do not fall 15 net points in 30 days (35.6% do, against
the registered assumption of 65%), and the profitability share's exact
lower bound misses its 0.60 bar. The H8 lesson repeats under a
listing-age sort: the market prices most of the decline into funding, and
the drift left over is too small for the registered trade. Amendment 3's
PARTIAL_DRIFT row anticipated the mirror image of this outcome (bars
clear, no age effect); the sample delivered the opposite (age effect, no
bars) — and both map to closure of this design, by the registered table.
The registered assumption that failed hardest was P2's true share of
0.65; the measured share was 0.356 (n = 312).

**Consequence executed (the FAIL row):** the hypothesis closes with the
H-NPL closure entry in REGISTRATION.md; collectors disarm immediately;
the 62 pending census events are recorded pending-at-closure; nothing is
deleted. The operator's Section 13 prior of 0.40 (adopted) on the bars
clearing resolves against the prior; the assistant's 0.40 likewise. A
documented negative was a registered, expected outcome; this is one.

### B.3 — consequence, mutations, close-out

**The disarm, executed and verified** (2026-08-28T03:44Z):
`systemctl --user disable --now npl-watch.timer npl-daily.timer` removed
both unit links; `list-timers --all` and `list-units --all` show nothing
npl scheduled or active (n = 0 of each); the AiTrader news-collect timer
(next 15:31 PDT) and the solattn-daily timer are untouched, verified in
the same listing. The unit files remain in ops/systemd/ as history;
nothing was deleted. The request ledger recorded **zero charges by this
stage** — the last ledger rows are the collectors' own final passes.

**Mutations on the new surface, 3 of 3 CAUGHT**
(reports/stage_b/mutations.md; bytecode purged before every run, source
restored byte-for-byte, suite green after each restore; the latch already
existed, so no mutation could touch a live verdict):

1. Bypass the latch so a second read is allowed — caught by the
   ReadAlreadySpent tests (the refusal is produced, not asserted).
2. Widen the blindness allowlist to two modules — caught by the equality
   pin holding the allowlist at length one.
3. Flip the funding sign convention inside the reader — caught by the
   known-answer gate (the −0.0729 sign pin).

After restore: `make all` green (172 tests, mypy --strict on 54 files,
ruff clean) and all 21 read-surface modules verify byte-identical against
reports/stage_b/hashes_b1.json; the latch and read artifact hashes are
unchanged (2d204ccb…438f67e, 44554896…be840c).

**End state.** The row fired was FAIL, on effective N 312 / 312 / 175
with P1 197/312 (lower bound 0.5707 < 0.60), P2 111/312 (p = 1.000), P3
114/175 (p = 3.767e-05), cost-insensitive across the registered bands.
The hypothesis register carries the H-NPL closure entry; the collectors
are disarmed; the 62 pending events are pending-at-closure; the sealed
stores (312 event windows, 176 control windows, 386 funding archives),
the census, the pairs ledger, and all request ledgers remain on disk,
unread beyond the single registered read. The remote is
git@github.com:kirosli00tuff/NPLExperiment.git (private), origin/main at
the close-out commit. Open operator items: none.

---

## Register Stage A — the multi-hypothesis conversion (2026-08-28)

The operator instruction arrived hours after the H1 closure: same repo,
new architecture. NPLExperiment converts into a multi-hypothesis register
in the MLCryptoEngine style — HYPOTHESES.md at the root, H1 migrated in as
the founding closed entry, and three co-registered successors (H2 the
age-contrast pair, H3 the population-corrected naive short, H4 the
funding-conditioned short) that test on fresh, unread data only, share the
one collection substrate, and sit under one familywise budget with an
outcome-blind power cull. The spent Stage B read was quarantined from
every successor code path before any successor registration existed: an
AST string pin holds the reachable stage_b surface at exactly the two H1
modules, import isolation seals the stageb package, the 312 retro event
IDs are recorded in data/state/generating_sample.json, and every successor
view refuses them — the refusals produced by test on synthetic offenders,
never asserted. The register substrate (views, conditioning, cull, priors,
fresh-cohort reconstruction) landed with the suite green before the first
new network call, and all three registrations — each with its Section 0
outcome map, its generating-sample-labelled assumptions, its epistemic
boundary, and its own reserved empty operator prior slot — were committed
and pushed before any successor measurement.

**A.1 measured, and one carried figure died.** The collector gap
(01:40Z last archive advance → 03:55Z recovery, disarm 03:44Z between)
lost nothing: the venue retains full 1d and funding history, the 62
pending-at-closure events reconstructed exactly from the sealed census
(60 hip3, 2 vanilla), and their archives were built from scratch — 156
pages, 60,010 funding hours, **0 unrecoverable hours** (every leading gap
is pre-launch structural absence). The census refresh found 504
instruments (one new: io:EWY, delisted at birth, never an event; one
relist: xyz:XBI). Accrual re-measured at **18.57 events/month** (n = 113
listings/182d) — the carried 18.5 confirmed — but **main-dex accrual
measured 0.5/month (n = 3), falsifying the prompt's ~9.4/month planning
figure for H3**. The H2 match rate on the fresh cohort measured 0.613
(38/62): xyz 36/36 pairable, main 2/2, and the young dexs (para, mkts,
io) zero until their instruments cross the 180-day candidate age at
deterministic dates. Retention: 62/62 fresh windows fully servable.
Ceilings: 0 refusals in 60 probes at the A.1-measured rates — no drift,
pacing unamended.

**A.2 assigned, measured, and culled.** Control assignment ran the H1
Section 6 rule verbatim at each backfillable entry, trailing-only through
the pinned matcher: **38 of 38 pairable events assigned, 0 candidates
skipped for coverage, 16 distinct controls**, both legs' touch spreads
snapshotted (descriptive). The H4 conditioning rates measured **0.1774 /
0.1290 / 0.0806** (n = 62, 0 absent) — the fresh cohort's median trailing
entry funding is **+31.6 percent/yr**, so deeply negative entry funding
is rare, exactly the failure mode H4's registered expectation named. The
k-table (reports/stage_a_h2/ktable_cull.json) computed every co-primary
at k = 1, 2, 3 across achieved / interim / deadline sample sizes, and the
cull ran to its registered fixed point:

- **Pass 1 (k = 3, alpha_h = 0.016952):** H2 required 0.5771; H3 0.0000;
  H4 best cell 0.0140 → **H3 and H4 fire BLOCKED.**
- **Pass 2 (k = 1, alpha_h = 0.05):** H2 required 0.7604 → fixed point.
- **k = 1. alpha_h = 0.05. H2 fires DEGRADED** (E1 0.9743 / E2 0.7604 at
  141 projected deadline pairs; min-N 76 / 169). Collectors arm for H2
  alone.

The pair projection that fed the cull is the by-dex measured model —
per-dex accrual times deterministic 180-day pairability onsets, all
A.1-measured — with the flat 0.613 summary reported beside as
sensitivity. The sensitivity is not cosmetic and is recorded plainly:
under the flat variant H2's E2 leg sits at 0.4318 at the pass-1 alpha and
the register would have culled everything (k = 0). The by-dex model
governs because pairability on this venue is a deterministic function of
measured dex age (xyz measured 36/36), not a stationary share.

Three amendments carry the record: H2-1 (DEGRADED; k and alpha_h fixed,
never revisited after any outcome exists), H3-1 (BLOCKED — the measured
0.5/month main-dex rate against a 262-event min-N is the documented
answer), H4-2 (BLOCKED — the registered expectation confirmed by the
measured rates). H4-1, recorded before any conditioning value existed,
resolved a drafting contradiction in the conditioning feature's absence
rule in favor of the governing H1 event-side definition.

**A.3 armed the survivor alone.** The collectors re-enabled at 06:21Z
under Amendment H2-2 — watch hourly at :05 (Persistent catch-up clean:
11 dexs, 0 failed), daily at 01:40 UTC (no double-fire; today's pass
predated the H1 disarm), AiTrader and solattn verified untouched, the
manual-run guard verified refusing while armed. The watcher now runs the
H2 pair pass at each birth's entry anchor: trailing-only assignment
through the pinned matcher, the pair row, both legs onto the fresh plan
(100 rows seeded: 62 events + 38 control legs), and the two-leg l2Book
snapshot inside the registered 30-minute window — a late pass writes the
loud expired row and the daily pass catches up the assignment. The fresh
cohort's candle windows seal once at maturity (entry+92d) under the
fresh plan; forward births checkpoint at +2/+32/+92 with the pair's
elder leg on its event's schedule; H2 coverage requires both legs. The
dark machinery exists for the survivor only: the pair reader reproduces
known answers to the digit with sign pins on all four legs, and the H2
latch refuses a second read — H3 and H4, BLOCKED, got no readers and no
latches, and asking for theirs refuses loudly by test. The pair
feasibility memo (docs/PAIR_FEASIBILITY.md) sizes the design: ~2.2N
capital per pair with the young short's isolated margin at 1.2N
surviving a +100 percent squeeze by construction, a 45-pair hard cap at
$1,000 against ~19 accrual-bound concurrent pairs — capital is not the
binding constraint, accrual is.

One defect surfaced during hardening and is recorded, not smoothed over
(Amendment H2-2, ADR-021): the first forward-pass test drove the trail
fetcher into the real data/funding store through a default-parameter
root — 7.2M fake-coin seal files, verified test-only and removed; the
fetcher now takes its root explicitly, the test pins the isolation, and
a page cap bounds the loop.

**A.4 hardened and closed.** Gates green throughout (217 tests, mypy
--strict, ruff). The register mutation exercise ran six mutations on
real source, bytecode purged before every run, **6 of 6 CAUGHT**
(reports/stage_a_h2/mutations.md): the spent read opened from an H2
module (string quarantine pin), a generating-sample ID admitted to a
view (the produced refusal), a post-entry funding read inside assignment
(PostEntryRead), a flipped pair-leg sign (the known-answer gate), the
cull reading an outcome field (the repo-wide OHLCV pin), and a widened
reader allowlist (the equality pin). Source restored byte-for-byte after
each. ADR-013 through ADR-021 record every choice; HYPOTHESES.md carries
all four entries with verdicts; the register's end state — per-hypothesis
verdicts, k = 1, alpha_h = 0.05, collectors armed for H2, earliest H2
Stage B near mid-2027 — is in the A.4 close-out of progress.md. Open
operator items: **the three reserved prior slots, and nothing else** —
H2's slot is the one that will matter, and the assistant fills none of
them.

## Register H2 — the amendment stage (2026-08-28)

Amendment H2-1 had left H2 in an awkward place. The design survived the
cull at DEGRADED, its collectors were armed, and its arithmetic said the
governing co-primary needed **169 achieved pairs** before its single
registered read could fire — reached near 2027-05/06 at the measured
accrual, plus 30 days of maturity, which is **past its own 2027-03-31
projection deadline**. A registered experiment that cannot report inside
its own horizon is not a strict experiment; it is an experiment that never
answers. The operator's instruction of 2026-08-28 was to amend it, and this
section records what was weakened, by how much, and what it bought.

**The preconditions, checked and recorded before anything else**
(`reports/stage_a_h2/amend_preconditions.json`, PASS at 07:51:10Z on the
project clock): `data/state/h2_read.json` absent and the registered latch
`data/state/h2_read_latch.json` absent — the H2 read is unspent; a scan of
all eight files under `reports/` finding **zero H2 outcome artifacts**
(`reports/stage_b/*` is the spent **H1** read, quarantined by AST pin;
`reports/stage_a_h2/*` is the outcome-blind k-table and the A.4 mutation
evidence); gates green; tree clean; origin equal to HEAD;
`npl-daily.service` inactive, so no wait was required.

**Amendment H2-3 registered three changes before a line of code moved,
and was committed and pushed before any of them was implemented.**

**Change 1, the fallback control — a relaxation.** Where the event's own
dex has no instrument meeting both the 180-day age condition and the
coverage condition, the control is the nearest funding-matched elder **on
the main dex**, under identical distance, tie-break, and replacement rules.
A same-dex candidate always wins. Every pair carries `pair_type`, and the
tag **never filters a primary statistic** — the `same_dex` subset is a
named stratum reported beside every primary figure at every look, because a
cross-dex pair matches funding but not venue microstructure and the reader
must be able to see whether the primary rests on it.

**Change 2, the economic floor — a weakening, stated as one.** E2's bar
moves from **twice** the pair's registered central cost to **once** it. A
pair returning between one and two times its own execution cost now counts
as a success where it did not. The bar still requires each pair to clear
its own round trip (18, 27, or 36 bp by class), so E2 remains an economic
test; what it no longer requires is a doubling. **The 2× figure is retained
as a named secondary computed at every look**, so the cost of the weakening
sits in the same artifact as its benefit. The registered power assumption
had to move with the floor — E2's 0.60 was itself a judgment discount from
E1's 0.651, never a measurement — and the new figure, **0.625**, comes from
linear interpolation in the floor multiple between multiple 0 (E1's 0.65)
and multiple 2 (0.60). Linear is the neutral choice, not a claim about a
distribution nobody has measured, and because it is a choice **every
minimum N below is reported twice**, at 0.625 and at the unchanged 0.60.

**Change 3, the two-look plan — a relaxation of Sections 8, 9, and 10.**
Two registered looks replace one, on an exact binomial boundary: k₁ from
alpha_1 = 0.02 alone, k₂ from the spend **conditional on not having
rejected at look 1**, over the independent increment, with alpha_2 = 0.03.
Total type-I is at most 0.05 by construction, with no asymptotic
approximation anywhere. Both co-primaries must clear the same look for a
GO; look 1 can only GO, CONTINUE, or fire a pre-registered futility
boundary; only look 2 and that boundary fire a terminal row. Section 10's
"exactly once" becomes **exactly twice**, one open per look, each behind a
write-once fsynced latch, with look 2 structurally unable to run before
look 1's latch exists.

**The interim tripwire was omitted, and the amendment says why.** The
prompt offered an optional E1-only status check on 2026-09-30, descriptive,
spending no alpha. The E1 statistic is the share of pairs with positive
30-day net pair return; computing it requires each leg's entry and exit
closes and its funding over the holding window — that is, opening the
sealed outcomes. There is no construction of it that does not read an
outcome value, so a 2026-09-30 tripwire would have been an unregistered
third opening, in direct breach of standing rule 7. Calling it descriptive
does not change what the code would have to read. **Nothing is registered
for 2026-09-30.**

**The backfill answered better than the projection.** All 24 previously
unpairable events (para 18, mkts 4, io 2) were assigned main-dex fallback
controls at their **original** entry timestamps, trailing-only,
append-only, tagged `cross_dex`: **24 of 24, zero exclusions**, 19 distinct
controls, 174 candidates considered per event and **none skipped for
coverage**. The pairs ledger stands at **62 rows — 38 `same_dex` plus 24
`cross_dex`** — and the backfillable cohort's match rate went from 0.613 to
**1.000**. The 24 control legs joined the fresh plan (124 rows), their
funding archives caught up in 133 pages and 57,584 rows, and all 24
control-leg l2Book windows were recorded **`expired`, loudly** — every
entry anchor lies between 2026-05-30 and 2026-08-28, so every 30-minute
window closed long ago and none is backfilled. 1,080 requests, zero
refusals, zero dollars, no keys, and **no outcome value read**. Each
candidate's trailing window was sealed once as a single wide raw window and
read back **through the blindness gate at each event's own entry**, so no
event ever sees a rate stamped after itself; that cut the fetch from ~2,774
requests to 724 pages without touching the rule.

One defect was caught **before** the run rather than after: the backfill's
first draft called `assign_control` without a path, and its default is
**H1's** ledger. It would have appended 24 successor rows to the spent
hypothesis's record. Fixed before execution; H1's ledger hash verified
unchanged afterwards.

**The boundary table (Amendment H2-4, `ktable_amended.json`).**

| co-primary | look-1 min N | look-2 min N | single-look min N |
|---|---|---|---|
| E1 (share 0.65) | 42 | 84 | 76 |
| **E2, 1× floor (0.625) — governing** | **59** | **117** | 111 |
| E2, 1× floor at the unchanged 0.600 | 92 | 184 | 169 |
| E2, pre-amendment 2× floor, one look | — | — | **169** |

The pre-amendment 169 recomputes exactly from the same registered inputs
and reproduces Amendment H2-1 — the arithmetic checking itself. **The cost
of the weakening in one line: 169 pairs at a single look becomes 117 at
look 2 with a stop available at 59; a reader who rejects the interpolated
share and holds E2 at 0.60 should read 184/92, and the design then does not
reach 0.80 by the deadline.** Both figures travel at every look.

At the look-2 minimum (n₂ = 117): n₁ = 59, **k₁ = 38, k₂ = 69**, exact
spend 0.0182 + 0.0240 = **0.0422**, powers 0.9322 / 0.8237. At the deadline
(n₂ = 135): k₁ = 43, k₂ = 79, spend 0.0403, powers 0.9552 / **0.8629**.
Every total spend sits **inside** alpha_h = 0.05 and the generator refuses
loudly if one ever does not. **The alpha split 0.02 / 0.03 stands**: six
splits were evaluated against a two-clause materiality test written before
it was applied, and the only two that gain power — (0.01, 0.04) and
(0.005, 0.045), at +0.027 and +0.026 — buy it by cutting the interim's
firing probability by 0.193 and 0.277, which clause (b) refuses. Futility
is registrable and registered: at n₁ = 59, **E1 f₁ = 31 and E2 f₁ = 27** at
the 0.10 conditional-power floor.

**The dates, which are the point of the whole exercise.** A pair becomes
readable when its window seals at entry + 92 days. At the measured accrual
of 18.57 events/month and the amended match rate of 1.000: 62 pairs by
2026-11-30, 80 by year end, 117 by 2027-03-01, 135 by the deadline.
**Look 1 projects to 2026-11-26 and look 2 to 2027-03-01 — one month
inside the registered 2027-03-31 deadline**, against an unamended earliest
read near 2027-06. Recomputed power beside the registered 0.80 target, as
the DEGRADED rule requires: **0.8886 single-look, 0.8629 two-look**, both
above it. Section 0's DEGRADED record is not edited and is not re-fired.

**A defect in the amendment's own wording, found while writing the reader
and corrected before any data existed.** H2-3's look-2 GO condition, read
literally, would have fired **FAIL** whenever one co-primary's look-1 count
had already crossed k₁ while the other had not — punishing strong early
evidence. Amendment H2-4 §7 corrects it: a co-primary passes at look 2 when
the procedure has rejected its null **by** look 2. That is the union of the
two registered rejection regions, so the exact spend and every number in
the table above are unchanged. The lesson, now recorded for the third time
in this project: a registration written in prose and a reader written in
code disagree in the corners, and only writing the code reveals it — so
write the reader in the same session as the amendment, while the correction
is still free.

**Gates and mutations.** `make all` green throughout: ruff, `mypy --strict`
on 71 files, **249 tests**. The amendment mutation exercise ran on real
source with bytecode purged before every run, **6 of 6 CAUGHT**
(`reports/stage_a_h2/mutations_amend.md`): spending look 2's alpha at look 1
(k₁ is 38 at alpha_1 and 37 at the whole budget — a one-success gap, which
is the size a boundary fixture must have), admitting a `cross_dex` pair into
the `same_dex` stratum, reading a post-entry funding row inside fallback
assignment, bypassing a per-look latch, dropping the pair-type tag, and
letting the look-2 read run without look 1's counts. Source restored
byte-for-byte, verified by sha256 against a pre-run snapshot and by an empty
`git diff`; the register A.4 harness still catches **6 of 6** against the
amended source, so the older pins did not rot under the new code.

**The reader is still dark.** `data/state/h2_look1_latch.json` and
`h2_look2_latch.json` do not exist. The structural pin still holds
`register/pairs.py` to pure imports, no file API, and no string naming a
sealed location. **The H2 pair reader had seen only synthetic fixtures when
this stage opened, and has seen only synthetic fixtures at its close.** The
one open operator item is unchanged and unchangeable by the assistant: the
**H2 operator prior slot**, which now blocks both looks.

---

## Register entry H5 — HIP-3 equity-style perpetual basis (2026-08-28)

**A feasibility entry, not a hypothesis.** H5 asks whether the perp mark on
HIP-3 equity-style instruments sits far enough from its underlying reference
to be worth investigating, whether funding is served on these instruments at
all, and whether a daily-latency expression is conceivable for this operator.
It authorizes no capital, no Stage B read of a trading outcome, and no
Stage C. Its terminal states are **VIABLE** — meaning a successor is worth
registering **in a fresh repository, with an independent underlying feed** —
or **CLOSED**, with INDETERMINATE as the registered middle.

### What was registered before anything was read

`registrations/H5/REGISTRATION.md` was committed and pushed with **zero H5
requests sent**, and it carries its machinery as tested code rather than
prose: the exact-string ticker mapping (198 entries), the US market calendar
for 2024–2027 with its four session tags, the basis definition with the
same-snapshot rule enforced by snapshot id, the outcome map built dark with
fixtures sitting exactly on 18.00 bp, 54.00 bp, 20 instruments and a 10-of-20
funding share, the request-budget arithmetic, the write containment gate, and
the empty operator prior slot.

Three consequences were registered **before** measurement, because the
obvious implementation breaks all three: no retrospective basis can come from
`candleSnapshot` under standing rule 7; H5 reads no funding rate value
anywhere and records funding as *service*; and the retrospective read is
gated away from every registered cohort because the venue's historical
deviation field is a funding-rate proxy.

### What the venue actually serves

Two full census passes, 323 requests each, returning **identical** counts,
plus a 6-request reconnaissance probe. `docs/H5_ACCESS.md` carries the
verbatim fragments.

| question | answer |
|---|---|
| Is a reference served? | **Yes — `oraclePx` on 151 of 151** resolved instruments. `reference_unserved`: **zero**. |
| Is funding served? | **Yes.** The `funding` field on 151 of 151 contexts; `fundingHistory` rows on **94 of 94 live** instruments, every one stamped inside the last two hours. The 2026-08-27 `no_data`/`caught_up=true` records carried into this entry were **an archive cursor at its end, not an absent field**. |
| Is there a book? | Two-sided on 94 of 94 live; empty on all 57 delisted. Live median touch spread **4.18 bp** (IQR 1.31–10.78). |
| Historical mark-vs-oracle? | **No.** The venue serves neither historically. **A retrospective basis of the registered construction does not exist.** |
| Historical deviation of any kind? | **Yes, differently built**: `premium`, hourly. Verified arithmetically against the contemporaneous BTC context — served premium −0.0003482613 equals (77501.0 − 77528.0)/77528.0 exactly, where 77501.0 is the served impact ask. An **impact-price** deviation, therefore a named secondary that may fire CLOSED and never VIABLE. |

### The universe, and the exclusion that mattered

273 HIP-3 instruments over 10 dexs → **151 resolved** (118 equity, 15 ETF,
18 index), 80 `excluded_non_equity`, 42 `excluded_unresolvable` → **94 live**.

**57 of the 151 resolved instruments are delisted, and they are where every
large basis lives.** All three fields agree on all 57 — `isDelisted`,
`openInterest` exactly 0, `dayNtlVlm` exactly 0 — with zero conflicting cases
and zero of the 94 live instruments matching any of them.

| stratum | n | median abs basis | IQR | max | > 18 bp | **> 54 bp** |
|---|---:|---:|---:|---:|---:|---:|
| **live** | **94** | **3.72 bp** | 0.73 – 7.31 | 51.4 bp | 8.5 % | **0.0 %** |
| delisted | 57 | 30.52 bp | 0.00 – 210.79 | 2,481 bp | 54.4 % | **45.6 %** |

Amendment H5-2 excludes them, on a conjunctive three-field rule. **The
amendment deleted this entry's only route to VIABLE**, which is the direction
that makes it credible: it was made with the census in hand, disclosed in
full in its own text, and it costs rather than buys.

### The row, fired 2026-08-28T22:20Z

> ### **PENDING — the census window is open. Projected fire date 2026-09-26.**

| clause | measured | bar | result |
|---|---|---|---|
| instruments carrying a served reference | **94** | ≥ 20 | **clears** |
| funding served on those instruments | **94 of 94, share 1.000** | ≥ 0.500 | **clears** |
| instruments at 30 days of coverage | **0** | ≥ 20 | **window open** |
| median absolute basis, `extended` (n = 188) | **4.14 bp** | floor 18 / bar 54 | — |
| `regular`, `closed_weekday`, `weekend` | **no observations yet** | — | recorded absent, not zero |

Neither CLOSED clause fires. What is missing is time — and per **Amendment
H5-1**, the floor clause of CLOSED is a statement about *every* session tag
and cannot be made from two snapshots in one tag. That amendment was made
before any firing and makes CLOSED **strictly harder**; it cost this entry a
same-day close.

**29 daily passes remain.** The collector is armed and runs last in the
01:40Z daily pass, at 209 requests — **1.05 percent of the daily cap** —
behind an H2 yield that postpones H5 rather than competing with H2 work.

### The retrospective answer, and why it is a shortfall

The cohort gate leaves **27 of 151** instruments eligible; **124 are
`excluded_quarantined`**. Of the 27, **25 return no funding rows at all** over
the registered 180-day window and **2 are days-old listings** — `io:NBIS`
(n = 8, 1 covered day) and `xyz:XBI` (n = 31, 2 days). **39 observations, 2
instruments, 0 meeting the 30-day bar.**

The secondary is fired on the venue's field service rather than on the gate's
residue — feeding it 2 instruments would have fired CLOSED on an artefact of
this entry's own quarantine — and it lands **PENDING and not projectable**:
its coverage cannot be reached. Its pooled figures are recorded so the
shortfall is legible, not so they can be read.

### The honesty clause, demonstrated rather than argued

**32 of the 57 delisted instruments are still being served an unbroken hourly
funding series** — 168 rows each, the most recent stamped 2026-08-28T21:00Z —
on markets with zero open interest, zero volume and no book. The venue
accrues funding where nothing trades.

That is Section 4's whole point in one measurement: these fields are the
venue's bookkeeping, and bookkeeping continues after the market stops. A wide
measured basis is a **lead, never evidence of a trade**, and the successor
repository would need an independent underlying feed before it could claim
anything about tradability. The closed-and-carried IBKR economics — 40 to
100 bp whole-share round trips at this operator's sizes, fractional orders
refused at error 10243 — mean no cross-venue pair is registrable here in any
case.
