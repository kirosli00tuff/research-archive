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
