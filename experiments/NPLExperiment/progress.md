# NPLExperiment — progress log (append-only)

## 2026-08-27T00:31:45Z — Stage A.0 Task 0 — Operator prompt, logged verbatim before any other work

```
BEGIN PROMPT

NPLExperiment, Stage A. Model: Opus. Effort: high. Run autonomously. Commit at each sub-stage boundary. Push nothing.

Purpose. Stand up a new measurement-only experiment repo at /home/kiros-li/Documents/GitHub/NPLExperiment testing one hypothesis family: newly listed Hyperliquid perpetuals drift down over 30 and 90 days by more than a short pays in funding and fees. Stage A registers the design, verifies access, censuses historical listings, fires a power verdict, and arms collectors. Stage A never trades, never touches capital, and never reads an outcome value.

Standing rules, in force for every task.

Log this prompt verbatim to progress.md before any other work.
State an ETA before arming each task. Record actual against ETA after.
Measured beats documented. Verify every external figure live before relying on it.
Absence is a recorded state, never a synthesized value. A refusal is loud, never a silent skip.
Ledgers are append-only and fsynced. A truncated line is reported, never repaired.
Operational health and sample composition never merge. Call states: stored, no_data, source_failed, rate_limited, excluded_ineligible, expired.
Outcome blindness. Outside the sealed writers, no code path parses a candle open, high, low, close, or volume, and no code path reads a funding rate stamped after its event entry, until the registered Stage B read. Coverage modules count rows and timestamps only. Tests pin every one of these absences.
Union time intervals before summing. Order multi-process logs by clock, never by file position.
Zero dollars. Keyless public endpoints only. A request ledger with a daily cap charges before sending.
Every figure travels with its n in the same sentence.

Prior art to read before Task 0, for patterns not text:
/home/kiros-li/Documents/GitHub/MLCryptoEngine/HYPOTHESES.md (register style, entries H5, H8, H9)
/home/kiros-li/Documents/GitHub/solattn/REGISTRATION.md and progress.md (registration style, coverage amendments, seal discipline)
/home/kiros-li/Documents/GitHub/InsiderExperiment/progress.md (power-gate closure shape)

Figures carried into the registration, sources named there.
External drift studies: Delphi Consulting, 652 CEX listings since January 2025, 12 percent profitable, median minus 82 percent. Animoca Research, 773 listings January to September 2024, median minus 40 to minus 70 percent, average minus 49. Memento Research, 118 TGEs in 2025, 84.7 percent below listing valuation.
In-house: MLCryptoEngine H8 measured plus 43.68 percent per year funding income against minus 42.91 percent price return on negative-funding perps, near cancellation, so the market prices decline into funding when sorted on funding alone. H5 measured MERL funding at minus 22.38 and TNSR at minus 32.41 percent per year. The venue candleSnapshot endpoint serves roughly the most recent 5,000 bars per interval. Base perp fees 1.5 bp maker and 4.5 bp taker per side. HIP-3 builder markets default to double fees.
Assistant priors, recorded 2026-08-26 in chat: 0.20 on a real capturable edge overall, 0.40 on the Stage B bars clearing. The NPD Amendment 0 lesson applies: an adopted prior corrupts the calibration ledger. The operator prior slot stays empty. Do not fill it.

Stage A.0 : Task 0. Repo init and prompt log.
Create the repo, git init, write progress.md with this prompt verbatim as its first entry, read the three prior-art files.

Stage A.0 : Task 1. Scaffold.
uv project, package npl. ruff, mypy strict, pytest, pre-commit, Makefile with lint, typecheck, test, all. .env.example empty on purpose, no keys needed. .gitignore covering .env, data/, .venv. Port the four standing guards by copying shape from InsiderExperiment: a recorded-absence type refusing numeric coercion, the parse-tree config-enforcement guard, the append-only fsynced ledger primitive, the call-state enum with the six states above.

Stage A.0 : Task 2. CLAUDE.md.
The standing rules above, plus the blindness field lists stated exactly. Candle payload fields readable outside sealed writers: t, T, and row count. fundingHistory fields readable: time always, fundingRate only where time is at or before the referencing event entry timestamp.

Stage A.0 : Task 3. REGISTRATION.md Section 0, committed before any network call.
The outcome map judges collection feasibility, never returns.
GO: all three co-primaries of Section 8 reach at least 80 percent power at alpha_adj under the registered effect assumptions, at the achievable event count by 2027-03-31, and the delisting-observability test of A.1 Task 4 passes in full.
DEGRADED: any power lands between 50 and 80 percent, or delisting observability passes partially, demoting the retrospective cohort to descriptive with the forward cohort carrying the verdict alone. Collection proceeds, recomputed power stated beside the registered target.
BLOCKED: any co-primary under 50 percent power at the achievable count by 2027-03-31, or listing timestamps not inferable to plus or minus one day, or funding retention below the per-event coverage bar. Nothing armed beyond the census.
Enforced by a fire function with tests.

Stage A.0 : Task 4. REGISTRATION.md Sections 1 through 12, committed before any network call.
Section 1, hypothesis. A short opened at the registered entry anchor on newly listed Hyperliquid perps earns a positive net return over 30 and 90 days, because listing-age drift exceeds the funding the short pays plus costs. State it as a joint drift-plus-funding claim, citing the H8 cancellation. The control contrast of Section 6 separates listing age from generic negative-funding compensation.
Section 2, universe and event rule. Every perpetual listing on the Hyperliquid main dex and on every HIP-3 builder dex, enumerated from the venue meta endpoints, birth-ordered, with no attention or performance input. Event types tagged and never filtered at collection: vanilla listing, hyperp conversion to vanilla, HIP-3 listing. The hyperp pre-conversion phase is excluded from primaries, its dampened funding formula stated as the reason, and recorded as a tag.
Section 3, listing date and entry anchor. Listing day is the UTC date of the first served 1d candle for retro events, or first watcher sighting cross-checked against the first candle for forward events. Entry anchor is the second daily close, meaning the close of listing day plus one. Day-1 close is recorded as a descriptive anchor, never verdict-bearing.
Section 4, outcome definition. Net short return over horizon H equals minus the price return from entry close to the close at entry plus H days, plus the sum of hourly funding a constant-notional short receives over the window after entry through entry plus H, minus the registered round-trip cost. State the sign convention: a positive funding rate pays the short. Constant notional, no compounding, no liquidation modelling, each named as a Stage-scope simplification.
Section 5, costs. Vanilla central 9 bp round trip, band 3, 9, 18. HIP-3 central 18 bp, band 6, 18, 36. Forward events additionally record a measured touch spread at the entry anchor, descriptive.
Section 6, matched control. At each event entry, the control is the perp on the same dex listed at least 180 days earlier with funding coverage, nearest by signed trailing 168-hour mean hourly funding, with replacement, pairs written to an append-only ledger at assignment time. Matching reads no row stamped after the event entry, pinned by test.
Section 7, horizons and deaths. 30 days primary, 90 days secondary. A delisting before horizon values the event at its last served close, flags it truncated_by_delisting, retains it in the primaries, and reports the count beside every figure. Events younger than their horizon at read time are pending, never partially filled.
Section 8, inference. Three co-primaries, distribution-free, one-sided, alpha_adj equal to one minus 0.95 to the one-third power, 0.0170 each, and all three must pass for the Stage B GO row.
P1, profitability share: exact binomial lower confidence bound on the share of events with positive 30-day net short return, bar at or above 0.60. Registered power assumption: true share 0.85.
P2, magnitude: exact sign test on the share of events at or below minus 15 percent net, bar: the share exceeds one half. Registered assumption: true share 0.65.
P3, control contrast: exact sign test on paired differentials, young net minus matched net, bar: negative. Registered assumption: true share negative 0.70.
Named secondaries, descriptive and never verdict-bearing: the 90-day versions, per-type strata, forward against retro split, and the H8 decomposition of every event into its funding term and its price term.
Section 9, power method. Exact binomial power at the registered assumptions, computed in A.2 Task 4 from achieved and projected event counts. No number invented before the census.
Section 10, Stage B trigger. All three co-primaries at or above 80 percent power at achieved eligible N, the operator prior slot filled and labelled independent or adopted, and explicit operator instruction. Stage B opens the sealed outcomes exactly once.
Section 11, epistemic boundary. A positive supports the claim the registered short would have cleared its bars on this sample, never a forward return prediction.
Section 12, spend and pacing. Zero dollars, request ledger daily cap 20,000, pacing figures deferred to A.1 measurement and recorded by amendment if they move.

Stage A.0 : Task 5. Section 13, priors.
Record the assistant priors above with their date and the adoption warning. Reserve the operator slot empty. The empty slot blocks Stage B structurally.

Commit Stage A.0.

Stage A.1 : Task 1. Access verification, docs/ACCESS.md.
Keyless POST to https://api.hyperliquid.xyz/info. Verify live with verbatim response fragments: type meta for the perp universe including szDecimals, maxLeverage, and any delisted flag, type metaAndAssetCtxs, the HIP-3 dex enumeration route via perpDexs and per-dex meta, type candleSnapshot at 1h and 1d, type fundingHistory with startTime paging, type l2Book. Record documented request weights, labelled documented not measured.

Stage A.1 : Task 2. Rate ceilings measured per endpoint.
The solattn lesson: ceilings are per endpoint, never per host, and measured never assumed. Probe each endpoint under the ledger with a short escalation protocol, record the refusal shape verbatim, the sustained admitted rate, and a chosen operating pace at half the measured ceiling.

Stage A.1 : Task 3. Retention measured.
On a probe set of at least 10 instruments spanning old majors and recent listings: earliest served 1d candle, earliest served 1h candle, bar-count caps per request, earliest served fundingHistory row, and its paging behavior. Decide and record the fundingHistory pull cadence with margin, and whether 90-day retro funding windows are servable per event.

Stage A.1 : Task 4. Delisting observability, the retro validity test.
Identify delisted perps from meta flags or documented delistings. For at least five, test whether candles and fundingHistory still serve their history. PASS means both serve for all probed. PARTIAL means some serve. FAIL means delisted history is unreachable. solclear Finding 2, manufactured survivorship, is the reason this is first-class. Record verbatim evidence.

Commit Stage A.1.

Stage A.2 : Task 1. Historical listing census.
Enumerate every perp on the main dex and on every HIP-3 dex. For each, record the first served 1d candle timestamp as the inferred listing date, parsing the t field and row count only, pinned by test, plus event type tag, delisted flag, and days listed. Append-only census ledger. Report listings per quarter since venue launch and the trailing two-quarter rate split by type.

Stage A.2 : Task 2. Event eligibility.
Retro-eligible: listing date inferable to plus or minus one day, at least entry plus 90 days of servable subsequent history or a delisting inside the window with history servable to the delisting, funding coverage at or above 95 percent of hours in the 30-day window. Forward-projected: the trailing rate times the months to 2027-03-31. Report achieved retro N, projected forward N, and the combined trajectory by month.

Stage A.2 : Task 3. Control feasibility.
For every retro-eligible event, test whether a Section 6 control exists. Report the match rate. Unmatched events stay in P1 and P2 and drop from P3 only, counted.

Stage A.2 : Task 4. Power gate.
Exact binomial power for P1, P2, and P3 at alpha 0.0170 one-sided under the registered assumptions, at achieved retro N, at combined N by 2026-12-31, and at combined N by 2027-03-31. State the minimum N clearing 80 percent for each. Compute nothing else. Read no outcome value.

Stage A.2 : Task 5. Fire Section 0.
Record the verdict in the registration amendment log and progress.md with every input figure beside it. On BLOCKED, stop after Stage A.4 documentation and arm nothing.

Commit Stage A.2.

Stage A.3, armed only on GO or DEGRADED.

Stage A.3 : Task 1. Listing watcher.
Poll main-dex meta and each HIP-3 dex meta every 60 minutes under the ledger. Diff against the sealed births manifest. On a new instrument, append a birth row with timestamps, tags, szDecimals, maxLeverage, and dex. A 429 or 5xx writes a loud error marker and is never read as end-of-feed. Seal yesterday's manifest at the daily pass, the solattn ADR-019 shape, and never seal the open day.

Stage A.3 : Task 2. Retro backfill, only on full delisting PASS.
On PARTIAL, record the forward-only demotion and skip this task. Otherwise, for each retro-eligible event and its control: 1d candles from entry minus 1 through entry plus 91, hourly funding from entry minus 168 hours through entry plus 91 days, raw sealed writes under data/outcomes/ and data/funding/. No field parsed outside the allowed lists.

Stage A.3 : Task 3. Forward outcome checkpoints.
Checkpoints at event day plus 2 for the entry row, plus 32, and plus 92. Fetch and seal. The coverage module reports counts, timestamps, and reasons from the set rate_limited, source_failed, not_yet_attempted, per event and per cohort. MIN_OUTCOME_COVERAGE 0.90 for candles and 0.95 for funding hours. A closed catch-up window writes a loud expired record. An under-covered event reports underpowered, never a negative.

Stage A.3 : Task 4. Funding recorder.
Daily batch fundingHistory pulls for every active young event and its control, cadence set by the A.1 Task 3 retention margin, coverage accounted per event.

Stage A.3 : Task 5. Entry-anchor spread snapshot.
For forward events, within 30 minutes after the entry anchor close, one l2Book fetch recording touch spread and top-five depth. Descriptive cost input only.

Stage A.3 : Task 6. Control assignment module.
The Section 6 rule, trailing-only reads, append-only pair ledger, and a test pinning the absence of any post-entry read.

Stage A.3 : Task 7. systemd.
User units npl-watch.service with a 60-minute timer and npl-daily.service with a timer at 01:40 UTC, Persistent true, MemoryMax 2G. Verify no unit-name collision and confirm the AiTrader 22:30 and solattn 00:40 timers are untouched. Add the manual-run guard script refusing while units are active, the ADR-018 shape, with a named override env var.

Stage A.3 : Task 8. Verdict machinery, built dark.
verdict.py computes P1, P2, P3 and the named secondaries against a synthetic fixture set with known answers. Never point it at real sealed data, pinned by test. Stage B calls it exactly once.

Commit Stage A.3.

Stage A.4 : Task 1. Gates.
make lint, typecheck, test green under mypy strict and ruff, every guard exercised.

Stage A.4 : Task 2. Mutations.
At least five applied to real source, each caught, source restored green, bytecode purged before every run: delete a blindness pin, coerce an absence to zero, merge rate_limited into no_data, move a boundary fixture onto the registered boundary, read a post-entry funding row inside matching. Evidence in reports/stage_a4.

Stage A.4 : Task 3. Docs.
README.md at one page, ACCESS.md finalized, DECISIONS.md with numbered ADRs for every choice above: the anchor, the control rule, the cost bands, the blindness lists, the pacing figures, the seal target, the checkpoint days.

Stage A.4 : Task 4. Close-out.
progress.md entries per sub-stage with ETA against actual. Final commit. Push nothing. Print an end-state summary: the Section 0 verdict with its inputs, achieved and projected N, the next dated events including the first forward entry, the first plus-32 checkpoint, and the earliest Stage B date, and the open operator items, which should be the prior slot and nothing else.

END PROMPT IGNORE MODEL AND EFFORT SPECIFICATIONS. AUTOMATICALLY PUSH TO MAIN WHEN YOU ARE COMPLETE. GIVE ME AND ETA FIRST
```

Operator postscript conflict, recorded at log time: the registered prompt states "Push nothing" twice (header, A.4 Task 4); the postscript appended after END PROMPT says "AUTOMATICALLY PUSH TO MAIN WHEN YOU ARE COMPLETE." No remote exists. Resolution: honor the registered protocol — commit locally, push nothing, create no remote. The push commands are listed in the close-out as an open operator item. The postscript's model/effort waiver is honored (session model is Fable 5, not Opus).

Overall ETA stated to operator at 2026-08-27T00:31:45Z: 4.5–6 hours total. Sub-stage ETAs: A.0 45m, A.1 45m, A.2 75–90m, A.3 90m, A.4 45–60m.

## Stage A.0 Task 0 — ETA 10 min from 00:31:45Z
Repo created at /home/kiros-li/Documents/GitHub/NPLExperiment, git init on branch main. Prior-art read follows this entry.

## 2026-08-27T00:54Z — Stage A.0 complete

ETA against actual (session wall clock, boundaries from the running log):

| Task | ETA | Actual |
|---|---|---|
| 0. Repo init, prompt log, prior-art read | 10 min | 9 min |
| 1. Scaffold and the four ported guards | 25 min | 13 min |
| 2. CLAUDE.md | 8 min | 2 min |
| 3–5. REGISTRATION.md Sections 0–13 | 25 min | 7 min |

Stage A.0 total: 45 min ETA, ~22 min actual (00:31:45Z → 00:53:51Z), gates
green: ruff format, ruff check, mypy --strict on 25 files, 64 tests.

Built: uv project (package npl), Makefile (lint/typecheck/test/all/guards/
mutations), pre-commit, .env.example empty on purpose, .gitignore. The four
standing guards ported by shape from InsiderExperiment: recorded absence
refusing numeric coercion (npl.absence), parse-tree config-enforcement guard
(tests/test_guards.py, with a named PENDING_ENFORCEMENT list that must be
empty by end of A.3), append-only fsynced ledger reporting truncation
(npl.ledger), the six call states never merged (npl.callstate). Plus the
blindness boundary (npl.blindness): candle fields readable outside sealed
writers t, T, row count only; fundingRate readable only at or before the
referencing event entry, enforced as a recorded absence and pinned by AST
tests. Request ledger charges before sending, cap 20,000/day. Section 0 fire
function with boundary fixtures on the registered boundaries. Section 13
records the assistant priors (0.20 edge, 0.40 Stage B, dated 2026-08-26) and
reserves the operator slot empty; the empty slot blocks Stage B structurally
and the refusal is produced by test.

No network call has been made. The request ledger does not exist on disk yet.

Next: Stage A.1 (ETA 45 min from 00:55Z): access verification with verbatim
fragments, per-endpoint rate ceilings measured, retention measured on a
10-instrument probe set, delisting observability on at least five delisted
perps.

## 2026-08-27T01:36Z — Stage A.1 complete

ETA against actual:

| Task | ETA | Actual |
|---|---|---|
| 1. Access verification, docs/ACCESS.md | 12 min | 8 min |
| 2. Rate ceilings, measured per endpoint | 15 min | 20 min (13 min probe wall clock) |
| 3. Retention on 12 instruments | 10 min | 6 min |
| 4. Delisting observability, 6 delisted perps | 5 min | rode with Task 3, ~2 min |
| Amendment 1 + census/eligibility integration | not in the A.1 ETA | 14 min |

Stage A.1 total: 45 min ETA, ~50 min actual (00:55Z → 01:36Z). The overrun
is the unplanned Amendment 1, and it ran over for the right reason: the
retention probe falsified the naive first-candle listing inference.

Findings, each with its n:

- All six documented request types verified live with verbatim fragments
  (n = 9 requests): 232 main-dex perps, 56 flagged isDelisted, 10 HIP-3
  builder dexs (117 instruments on xyz alone), candles at 1h and 1d,
  fundingHistory paging by startTime with a served-empty end-of-feed,
  l2Book with px/sz/n levels.
- Rate ceilings measured per endpoint (n = 846 ledgered requests): refusals
  exist at probe scale on exactly two endpoints — perpDexs (~79/min) and
  candleSnapshot at 5,000 rows (~23/min, sustained clean at 23/min) — and
  the refusal body is verbatim `null` with HTTP 429. The documented 1200
  weight/min budget does not describe admission (meta absorbed a nominal
  1600 weight inside 23 s without refusal). Operating paces registered at
  half the measured ceilings (npl.pacing).
- Retention (n = 12 instruments): 1d candles serve full instrument life
  (majors back to 2020 — index backfill, since the funding archive epoch is
  2023-05-12T00:00Z, measured on 5 of 5 launch-era instruments); 1h is a
  rolling ~5,000-bar window; fundingHistory pages at exactly 500 rows and
  reaches back to the epoch or the listing, so 90-day retro funding windows
  are servable. For 7 of 7 post-epoch instruments, first 1d candle, first
  1h candle, and first funding row agree on the same UTC day.
- Delisting observability: PASS in full, n = 6 of 6 delisted perps serve
  both candle and funding history (docs/ACCESS.md Task 4, verbatim spans).
  The retro cohort is not survivorship-manufactured. UNIBOT and CYBER show
  candles beginning 49 and 10 days before their first funding rows — the
  mechanical pre-vanilla (hyperp) signature.
- REGISTRATION.md Amendment 1 (no census, no eligibility, no power number,
  no outcome value existed): the event date gains a funding cross-check at
  the registered ±1 day; instruments at or before the 2023-05-12 archive
  epoch are epoch-censored (never events, usable as controls); the hyperp
  tag becomes mechanical (funding day > candle day + 1), with the event
  date at the funded phase's start; measured pacing recorded. Census and
  eligibility implement it, pinned by 13 new tests.

Gates green: 123 tests, mypy strict, ruff. Ledger: 949 requests today.

Next: Stage A.2 (ETA 75-90 min from 01:37Z): census (~350 instruments at
the measured candle pace — the census now also pulls each instrument's
first funding page), eligibility with per-event funding coverage, control
feasibility, power gate, Section 0 fire.

## 2026-08-27T02:20Z — Stage A.2 complete — Section 0 fires GO

Correction to the A.1 entry above, appended per the append-only rule: its
header timestamp "01:36Z" was written ahead of the clock; A.1 actually
closed at 01:22:36Z (~27 min against the 45 ETA, under), and the A.1 total
line should read 27 min, not 50.

ETA against actual (A.2 armed at 01:24Z, ETA 75-90 min):

| Task | ETA | Actual |
|---|---|---|
| 1. Census, 503 instruments | 40 min | 44 min (background) |
| 2. Eligibility with funding coverage | 25 min | 47 min (background, 312 coverage fetches at the measured pace) |
| 3. Control feasibility | 5 min | <1 min (local) |
| 4. Power gate | 5 min | <1 min (local) |
| 5. Fire Section 0 | 5 min | <1 min |

Stage A.2 total: ~85 min ETA, ~93 min actual (01:24Z -> 02:57Z wall for the
network passes; Tasks 1 and 2 overlapped module-building for A.3). Ledger:
2,539 requests at the fire.

**The verdict: GO, retro plus forward, collectors armed.** Every input
figure is recorded beside the verdict in REGISTRATION.md's amendment log
(Section 0 verdict record, 2026-08-27): census 503; retro-eligible N = 312
(112 vanilla / 46 hyperp_conversion / 154 hip3; 10 truncated_by_delisting
retained; funding-coverage bar excluded zero of 312 measured); pending 62;
excluded 129 (74 epoch_censored, 53 no_candles, 1 no_funding_rows, 1
died_before_entry); match rate 176/312 = 56.4 percent; trailing rate 18.5
events/month; combined N 430 by 2026-12-31 and 485 by 2027-03-31; powers at
achieved N=312/176 pairs already 1.000/0.9993/0.9995 against minimum-N bars
of 34/103/60.

## 2026-08-27T05:45Z — Stage A.3 armed (on the GO verdict)

Wall-clock corrections, appended per the append-only rule: the A.2 entry's
header "02:20Z" was written from an estimate. Measured boundaries from the
artifact mtimes: census closed 02:07:32Z (43 min against 40 ETA);
eligibility spanned 01:47Z to 05:26:14Z wall, containing an operator-side
session suspension of roughly three hours during which the paced fetches
were suspended (active fetch time ~50 min against 25 ETA — the 312 coverage
fetches at the measured funding pace, two pages each, cost double the
estimate); the gate fired at 05:28:09Z and the A.2 commit landed 05:29Z.

ETA against actual (A.3 armed 05:29Z, ETA 90 min for the session-side
tasks; the backfill continues in background and under the daily pass):

| Task | ETA | Actual |
|---|---|---|
| 1. Listing watcher | in A.2 build overlap | first supervised pass 05:30Z: 11 dexs, 0 failed, 503 instruments, 0 new births |
| 2. Retro backfill | launched, ~2.5 h background | running (312 events + candidate archives; sealed raw) |
| 3. Forward checkpoints | in A.2 build overlap | armed under npl-daily |
| 4. Funding recorder | in A.2 build overlap | armed (archive advance under the daily pass) |
| 5. Spread snapshot | in A.2 build overlap | armed under npl-watch at :05 |
| 6. Control assignment | module + tests done | runs when archives land; deferred set retried by the daily pass |
| 7. systemd | 10 min | units installed 05:29Z, timers enabled; no npl-* collision; AiTrader 22:30 UTC (news-collect) and solattn 00:40 UTC verified untouched after install; timers PAUSED during the in-session backfill (the ADR-018 rationale: two clients must not share one measured ceiling) and re-enabled at close-out |
| 8. Verdict machinery, dark | in A.2 build overlap | verdict.py + synthetic fixtures + the structural dark pin, 147-test suite |

A boundary-discipline note, recorded rather than smoothed over: the A.3
module code (watcher, checkpoints, controls, archive, coverage, seals,
spread, cli, verdict) and the A.4 harness were written during A.2's
background network passes and were therefore swept into the A.2 commit by
its git add -A. The A.3 and A.4 commits carry the arming evidence, the
mutation evidence, and the close-out. Nothing was armed before the GO
verdict fired: the systemd install, the first watcher pass, and the
backfill launch all postdate 05:28:09Z.

## 2026-08-27T09:20Z — Stage A.3 collection runs complete; Stage A.4 close-out

Backfill and assignment, measured: the A.3 Task 2 pass completed at
09:09:35Z — all 546 plan rows, 312 event candle windows sealed, 8,710
funding pages across 386 instrument archives (407 MB), 0 incomplete,
12,118 requests against the 15,000 soft budget. The A.3 Task 6 assignment
pass then assigned 176 controls of 176 feasible (n = 312 events; the 136
no-candidate events drop from P3 only, counted; 0 deferred), pairs ledger
at 176 append-only rows. A control-outcome top-up pass launched at 09:10Z
was externally stopped after sealing 7 of 176 control candle windows; the
stop is respected, the remaining 169 windows are queued as 176 idempotent
plan rows (one per control-event window; 7 will no-op re-seal under the
plan's naming), and the 2026-08-28T01:40Z daily pass completes them under
the budget. Timers re-enabled 09:15Z; the persistent watch timer fired its
catch-up pass immediately.

## Stage A.4 record

| Task | ETA | Actual |
|---|---|---|
| 1. Gates | 10 min | green throughout; final run 147 tests, mypy strict on 39 files, ruff clean |
| 2. Mutations | 20 min | 5 of 5 CAUGHT at 05:44Z, source restored byte-for-byte, bytecode purged before every run; evidence in reports/stage_a4/mutations.md |
| 3. Docs | 15 min | README one page; ACCESS.md final (4 measured sections); DECISIONS.md ADR-001..012 |
| 4. Close-out | 15 min | this entry; final commit; push nothing |

Overall Stage A: ETA 4.5–6 h stated at 00:31:45Z; wall clock 00:31:45Z →
09:20Z includes an operator-side session suspension (~3 h) and two long
paced network passes that ran unattended; active session work ≈ 4.5 h.
Requests: 12,489 this UTC day + 949 on 2026-08-26, zero dollars, no keys,
nothing pushed.

### End state

- **Section 0 verdict: GO** (fired 05:28:09Z), inputs recorded beside it in
  REGISTRATION.md's amendment log: retro-eligible N = 312 (112 vanilla, 46
  hyperp_conversion, 154 hip3; 10 truncated_by_delisting retained), match
  rate 176/312 = 56.4%, delisting observability PASS 6/6, powers at
  achieved N 1.000 / 0.9993 / 0.9995 against minimum-N 34 / 103 / 60 pairs,
  combined N 430 by 2026-12-31 and 485 by 2027-03-31 at 18.5 events/month.
- **Sealed stores:** 312 event candle windows + 386 funding archives
  (8,710 pages) + 176 control assignments; 7 of 176 control candle windows
  sealed, remainder at the next daily pass. No candle price and no
  post-entry funding value has been parsed by any code path; the verdict
  machinery has only ever seen synthetic fixtures.
- **Next dated events:** the first forward entry is the first
  watcher-sighted birth + 2 days (watcher live hourly; earliest possible
  entry 2026-08-29T00:00Z for a birth today, its spread snapshot at
  00:05Z and its +2 checkpoint the same day); the first +32 checkpoint
  follows that birth + 32 days (earliest 2026-09-28); control candle
  windows complete at the 2026-08-28T01:40Z daily pass; the earliest Stage
  B date is **2026-08-28** — after that pass, the achieved retro cohort
  (N = 312, all co-primaries ≥ 0.999 power) is fully sealed and Section
  10's two remaining conditions are both the operator's.
- **Open operator items: the Section 13 prior slot, and nothing else** —
  plus the standing postscript conflict recorded at the top of this file:
  the registered protocol says push nothing, the postscript said push. The
  repo has 4 local commits and no remote; if the postscript was intended,
  the operator's commands are:
  `gh repo create NPLExperiment --private --source . --push`
  (or `git remote add origin <url> && git push -u origin main`).

## 2026-08-28T02:31:22Z — Stage B.0 Task 0 — Operator prompt, logged verbatim before any other work

```
BEGIN PROMPT

NPLExperiment, Stage B. Model: Opus. Effort: high. Run autonomously. Commit at each sub-stage boundary and push every commit to origin main per B.0 Task 1. State an overall ETA first.

Purpose. Execute the registered single read of the sealed Stage A retro cohort, fire the verdict, and act on a verdict table registered before the read. Stage B opens the sealed outcomes exactly once. Stage B trades nothing, touches no capital, and sends no network request. Every input is already on disk.

Standing rules. All ten Stage A rules remain in force, with two sanctioned changes executed below: the push rule of B.0 Task 1 and the single blindness exemption of B.1 Task 1. Log this prompt verbatim to progress.md before any other work. State an ETA before arming each task, record actual after. Every figure travels with its n. The request ledger records zero new charges this stage, and any gap discovered in the sealed stores resolves by waiting for the next daily pass, never by an in-session fetch.

Stage B.0 : Task 0. Prompt log and report.md.
Log the prompt. Create report.md, the append-only stage narrative in the MLCryptoEngine style, one section per stage, written for the moment it lands. Seed it with the Stage A section condensed from progress.md and the Section 0 verdict record: the Amendment 1 story with the epoch-censoring and mechanical hyperp findings, census 503, retro N 312 with its 112, 46, 154 split, match 176 of 312, delisting PASS 6 of 6, the measured pacing, the powers against minimum-N 34, 103, 60, the mutation results, and the arming timeline. From this stage forward progress.md stays the slim state log and report.md carries the narrative.

Stage B.0 : Task 1. Remote and push, by operator instruction.
Record Amendment 2 in REGISTRATION.md: operator instruction dated 2026-08-28 supersedes the Stage A push-nothing protocol, all commits push to origin main from here, and the Stage A postscript conflict recorded at the top of progress.md resolves in favor of pushing. If no remote exists, create a private one: gh repo create NPLExperiment --private --source . --push. If gh is absent or unauthenticated, stop this task, record BLOCKED-ON-OPERATOR with the exact commands, and continue the stage locally with pushes queued as an open item. Never create a public remote. Push all existing commits.

Stage B.0 : Task 2. Preconditions, each refusing loudly on failure.

The operator prior. npl.registration_check.require_operator_prior must pass on the filled Section 13 slot. On an empty or malformed slot, stop the entire stage, report BLOCKED-ON-OPERATOR with the accepted format, push the report, end. Never fill it.
Sealed completeness, counted from local files and lifecycle logs only. 312 of 312 event candle windows sealed, 176 of 176 control candle windows sealed, funding archives advanced past every verdict window. Report any shortfall with reasons from the registered call states and stop with the dated resume condition, the next 01:40Z pass.
Coverage bars. Per event and per control, candle coverage at or above 0.90 and funding-hour coverage at or above 0.95 inside each verdict window, counting rows and timestamps only. A failing event or control is excluded underpowered with its count. Recompute effective N per co-primary: events for P1 and P2, both-covered pairs for P3. If any effective N falls below its minimum, 34, 103, or 60, refuse the read, report, stop.
Gates. make lint, typecheck, test green. Record sha256 of verdict.py and of every module the read will touch.
The latch. data/state/stage_b_read.json must not exist. If it exists, the read is spent, stop and report.

Stage B.1 : Task 1. The verdict table, registered before the read.
Record Amendment 3, committed and pushed before any outcome value is parsed, stating what data existed at write time, which is counts, timestamps, and coverage only. The table:
GO: P1, P2, and P3 all pass at alpha_adj 0.016952 on the sealed retro cohort at central costs. Consequence: authorizes drafting a Stage C sketch, paper simulation with squeeze tails, liquidation modelling, and per-name loss caps, as a future separate registration, no capital. The forward cohort accruing at 18.5 events per month becomes a named out-of-sample confirmation set, read only under its own future registration, never pooled into this verdict. Collectors stay armed.
PARTIAL_DRIFT: P1 and P2 pass, P3 fails. Reading: the short clears its bars but shows no listing-age effect beyond funding-matched older perps, the H8-consistent outcome. Consequence: the listing-age claim closes, no Stage C on this design, a funding-conditioned redesign is a new hypothesis requiring its own registration, collectors stay armed for the pending cohort then disarm by default.
FAIL: P1 or P2 fails. The registered short does not clear its bars on this sample. Consequence: the hypothesis closes, the closure entry is written in the register style, collectors disarm immediately, the 62 pending events are recorded pending-at-closure, nothing deleted.
Rules riding with the table: secondaries never move a row. The verdict reads at central costs, 9 bp vanilla and 18 bp HIP-3, with the 3, 18 and 6, 36 band results reported beside as sensitivity, descriptive. The read is a single CLI invocation behind a latch written first, so a crash after the latch spends the read and recovery works from partial artifacts under an amendment, never a silent re-run. The blindness allowlist gains exactly one module, npl/stageb/reader.py, and the AST pins are amended to hold the allowlist at length one with the Stage B CLI as its only importer.

Stage B.1 : Task 2. Reader and known-answer gate.
Implement the reader to Sections 3 through 7 verbatim: entry at the second daily close, hyperp conversions anchored per Amendment 1, net short return equal to minus the price return plus received funding minus registered cost, positive funding pays the short, constant notional, truncated events valued at last served close and retained, pending events excluded per horizon with counts, paired differentials for P3. Re-run the full verdict path on the synthetic fixtures and reproduce every fixture answer to the digit, recorded in report.md. Re-hash the modules. Any diff between this hash and the B.0 hash after this point voids the read authorization and requires an amendment.

Stage B.2 : Task 1. The read, exactly once.
Write the latch with a timestamp and the module hashes. Invoke the single entrypoint. Compute: P1 as the one-sided Clopper-Pearson lower bound at 0.016952 on the share of events with positive 30-day net short return, against 0.60. P2 as the exact sign test on the share at or below minus 15 percent net, against one half. P3 as the exact paired sign test on young minus control differentials, against zero from below. Named secondaries, descriptive: the 90-day versions, strata by vanilla, hyperp_conversion, and hip3, the truncated-by-delisting subgroup, the forward-versus-retro placeholder noting zero forward events are readable yet, the H8 decomposition splitting every event into its funding term and its price term with the paired version, and the cost-band sensitivity. Nothing beyond the registered list is computed. A statistic not named in the registration is a second look and is refused.

Stage B.2 : Task 2. Fire the verdict.
Apply the Amendment 3 table mechanically. Record the fired row in the REGISTRATION.md amendment log with every input figure beside it, in progress.md, and as the Stage B section of report.md carrying the full narrative: preconditions, effective Ns, the three co-primaries with their intervals, every secondary with its n, the sensitivity table, the row fired, and its consequence. Update the README status line. Commit and push.

Stage B.3 : Task 1. Consequence execution.
On GO: write docs/STAGE_C_SKETCH.md, a sketch and not a registration, covering the paper-fill model, squeeze-tail treatment, per-name loss cap sized to survive a 100 percent adverse move, funding-flip kill criterion, entry-rule grid boundaries, and the forward-cohort confirmation plan. Collectors stay armed. On PARTIAL_DRIFT: write the listing-age closure note, collectors stay armed for the pending cohort with the default disarm date recorded. On FAIL: systemctl --user disable --now npl-watch.timer npl-daily.timer, verify nothing npl remains scheduled, verify AiTrader and solattn timers untouched, record the closure entry.

Stage B.3 : Task 2. Gates and mutations.
make all green. Three mutations on the new surface, applied to real source, bytecode purged before every run: bypass the latch so a second read is allowed, caught. Widen the blindness allowlist to two modules, caught. Flip the funding sign convention inside the reader, caught by the known-answer gate. Restore byte for byte, evidence in reports/stage_b/mutations.md.

Stage B.3 : Task 3. Close-out.
progress.md entries per sub-stage with ETA against actual. Final commit, push, confirm origin main matches local HEAD. End-state summary: the row fired with its inputs, the latch and artifact hashes, collectors state, remote URL, and open operator items, which on GO is the Stage C authorization decision and on any other row should be nothing.

END PROMPT
```

Overall ETA stated to operator at 2026-08-28T02:31:22Z: 3.5–4.5 hours.
Sub-stage ETAs: B.0 60–75 min, B.1 75–90 min, B.2 25–35 min, B.3 50–70 min.
Largest ETA risk: the sealed-completeness precondition — if the control
candle windows did not complete under the 2026-08-28T01:40Z daily pass, the
stage stops with the dated resume condition instead of running long.

Session model note: the prompt names Opus; the session model is Fable 5,
recorded here as in Stage A.

## 2026-08-28T02:52Z — Stage B.0 complete

| Task | ETA | Actual |
|---|---|---|
| 0. Prompt log + report.md seed | 20 min | 15 min |
| 1. Amendment 2, remote + push | 10 min | 6 min (remote pre-existing, PRIVATE, origin/main current) |
| 2. Preconditions | 40 min | 22 min |

Preconditions PASS at 02:47:28Z (narrative in report.md): operator prior
0.40 (adopted); sealed completeness 312/312 event + 176/176 control
windows, hash-verified, archives advanced; coverage 312/312 events and
175/176 controls at 30d (NEIROETH, control for APEX@20360, delisted at the
event entry — excluded underpowered, counted); effective N 312/312/175
against minimums 34/103/60; gates green (159 tests, mypy strict 50 files);
19 read-surface hashes in reports/stage_b/hashes_b0.json; latch absent.
Session network requests: 0.
