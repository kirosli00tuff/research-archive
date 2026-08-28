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

## 2026-08-28T03:25Z — Stage B.1 complete

| Task | ETA | Actual |
|---|---|---|
| 1. Amendment 3, committed + pushed pre-read | 20 min | 12 min |
| 2. Reader, CLI, AST pins, known-answer gate | 60 min | 40 min |

Amendment 3 (commit 6399d63) registered the table and seven reading rules
before the reader existed. npl/stageb/reader.py (the single allowlisted
module), npl/stageb/cli.py (its only importer, `hash`/`read`), AST pins
amended with an equality pin on the allowlist and an importer scan. Known
answers to the digit in report.md; 172 tests, mypy strict 53 files, ruff
clean. B.1 re-hash: 21 modules, exactly the sanctioned diff
(stageb/__init__.py) plus the two new modules. Session network requests
still 0.

## 2026-08-28T03:40Z — Stage B.2 complete — THE ROW FIRED: FAIL

| Task | ETA | Actual |
|---|---|---|
| 1. The read, exactly once | 10 min | latch 03:01:01Z, read complete 03:01:08Z (18 s wall) |
| 2. Fire the verdict, record everywhere | 25 min | 22 min |

Latch sha256 2d204ccb…438f67e (21 module hashes inside); artifact
reports/stage_b/read.json sha256 44554896…be840c. P1 197/312, lower
bound 0.5707 < 0.60 FAIL; P2 111/312, p = 1.000 FAIL; P3 114/175,
p = 3.767e-05 PASS; the Amendment 3 table fires FAIL mechanically.
Cost-insensitive (P1 lb 0.5740/0.5707/0.5609 across bands, n = 312 each).
Full record: REGISTRATION.md Stage B verdict record + H-NPL closure
entry; narrative in report.md; README status line updated. The 62 pending
census events recorded pending-at-closure. Zero network requests.

## 2026-08-28T03:55Z — Stage B.3 complete — Stage B closed

| Task | ETA | Actual |
|---|---|---|
| 1. Consequence execution (FAIL row) | 10 min | 4 min — both npl timers disabled+stopped, nothing npl scheduled, news-collect and solattn verified untouched; closure entry in REGISTRATION.md |
| 2. Gates and mutations | 25 min | 14 min — make all green (172 tests, mypy strict 54 files); MB1/MB2/MB3 all CAUGHT, restored byte-for-byte, 21-module surface re-verified against hashes_b1.json |
| 3. Close-out | 20 min | this entry + final commit/push |

Overall Stage B: ETA 3.5–4.5 h stated at 02:31:22Z; actual 02:31Z →
03:55Z ≈ 1 h 24 min. Requests this stage: 0 (the ledger's last rows are
the collectors' own final passes). Zero dollars, no keys.

### End state

- **Row fired: FAIL** (read 03:01:08Z, latch 03:01:01Z). Inputs: P1
  197/312, CP lower bound 0.5707 vs bar 0.60; P2 111/312, p = 1.000; P3
  114/175, p = 3.767e-05; effective N 312/312/175 vs minimums 34/103/60;
  pending 0/0; 224,633 funding rows inside the 30d windows;
  cost-insensitive across bands (P1 lb 0.5740/0.5707/0.5609).
- **Hashes:** latch data/state/stage_b_read.json sha256
  2d204ccb23c4961597d2e4a3263b2abffeb1f8f2e32230ee3c4b97857438f67e (21
  module hashes inside); artifact reports/stage_b/read.json sha256
  4455489675c3774f05c977cb7edb9d8b26928f851400077b31263f5826be840c;
  read-surface hashes reports/stage_b/hashes_b0.json and hashes_b1.json.
- **Collectors: disarmed** (npl-watch.timer, npl-daily.timer disabled and
  stopped 03:44Z; nothing npl scheduled; AiTrader and solattn untouched).
  62 pending events recorded pending-at-closure; sealed stores, census,
  pairs, and ledgers retained; nothing deleted.
- **Remote:** git@github.com:kirosli00tuff/NPLExperiment.git (PRIVATE);
  origin/main confirmed equal to local HEAD at the final push.
- **Open operator items: none.** The hypothesis is closed; any redesign
  (funding-conditioned, magnitude-recalibrated) is a new hypothesis
  requiring its own registration.

## 2026-08-28T03:27:30Z — Stage A (register entries H2, H3, H4) Task 0 — Operator prompt, logged verbatim before any other work

```
BEGIN PROMPT

NPLExperiment, Stage A for register entries H2, H3, H4. Model: Opus. Effort: high. Run autonomously. Commit at each sub-stage boundary and push every commit to origin main, the Amendment 2 protocol stands. State an overall ETA and per-sub-stage ETAs before any work.

Purpose. Same repo, new architecture. Convert NPLExperiment from a single-hypothesis experiment into a multi-hypothesis register in the MLCryptoEngine style. Three co-registered successor hypotheses test on fresh, unread data only, share one collection substrate, and sit under one familywise error budget with an outcome-blind power cull. H1, the closed H-NPL, migrates into the register as the founding entry. Stage A restructures, registers all three designs, quarantines the spent Stage B read, recovers the collector gap, re-censuses, computes per-hypothesis power, fixes k and alpha, fires per-hypothesis Section 0 verdicts, re-arms collectors for survivors, hardens, and documents. Stage A never trades, never touches capital, and reads no outcome value: counts, timestamps, coverage, and pre-entry features only.

Standing rules. The ten Stage A rules remain in force verbatim, plus:
11. Push every commit. 12. The Stage B read is spent. reports/stage_b/read.json, every value inside it, and every outcome window read on 2026-08-28 are quarantined from all H2, H3, H4 code paths, enforced by AST pin and by test. The 312 retro events and their 176 control windows are the generating sample: usable for power assumptions, never for verdicts. 13. Pre-entry features are readable where registered: a trailing funding rate stamped at or before its event entry is a feature, never an outcome. The pin lists say exactly this.

Figures carried in as assumptions, generating-sample-derived and labelled so in every registration: P3 pair share 114/175 = 0.651, paired price differential +6.43 points and funding differential +0.88 over 30 days, strata share-positive vanilla 0.670 (n 112), hyperp_conversion 0.696 (n 46), hip3 0.584 (n 154), event-level decomposition +1.33 funding and +1.00 price, forward accrual 18.5 events/month, match rate 0.564, pending-at-closure cohort 62 events, venue minimum notional near 10 dollars, costs per leg 9 bp round trip vanilla and 18 bp HIP-3 central with the registered bands. Assistant priors, recorded 2026-08-28 in chat: H2 0.25 overall and 0.35 on bars clearing, H3 0.10, H4 0.05. The Section 13 adoption warning carries over verbatim. Three operator prior slots, reserved and empty, one per hypothesis, each blocking its own Stage B structurally. Do not fill any of them.

Stage A.0 : Task 0. Prompt log and ETAs.
Log this prompt verbatim to progress.md. State the ETA table.

Stage A.0 : Task 1. Register restructure.
Create HYPOTHESES.md at repo root in the MLCryptoEngine register style: status header, one entry per hypothesis with claim, design pointer, verdict, and dated closure where closed. Entry H1 migrates the H-NPL record: the FAIL row, its three co-primary figures, the spent-read hashes, and a pointer to the root REGISTRATION.md as the archived registration. Entries H2, H3, H4 open with claims and pointers to registrations/H2/REGISTRATION.md, registrations/H3/REGISTRATION.md, registrations/H4/REGISTRATION.md. Append a pointer amendment to the root REGISTRATION.md recording the architecture change. Rewrite docs/STAGES.md for the register architecture. Nothing in the old registration is edited beyond the appended amendment.

Stage A.0 : Task 2. Quarantine, built and tested before any registration.
Extend the AST pins: no module opens reports/stage_b/read.json or any file under reports/stage_b/ except the existing stageb CLI surface, no module imports npl.stageb.reader, and the read-surface allowlist stays at length one until a successor Stage B amends it. Add the generating-sample pin: event IDs of the 312 retro events are recorded in data/state/generating_sample.json and no verdict-bearing statistic in any successor hypothesis admits them. Both refusals produced by test, never asserted.

Stage A.0 : Task 3. Substrate specification.
One census, one watcher, one funding recorder, one checkpoint scheduler, per-hypothesis eligibility views on top. The config guard extends to the new keys. Per-hypothesis latches and readers come later and dark.

Stage A.0 : Task 4. registrations/H2/REGISTRATION.md, committed before any new network call.
H2, the age-contrast pair. Sections mirror the H1 architecture with these contents.
Hypothesis: a pair opened at the second daily close, short the young listing and long its funding-matched elder on the same dex at equal constant notional, held 30 days, earns a positive net return, because listing-age drift exceeds what funding matching already prices. Universe: every fresh event, meaning the 62 pending-at-closure events where windows are servable plus all forward births on every dex, no attention or performance input, hyperp pre-conversion phase excluded as before. Control rule: the H1 Section 6 rule verbatim, same dex, listed at least 180 days earlier, nearest signed trailing 168-hour mean hourly funding, with replacement, assigned at entry, trailing-only reads pinned. Outcome: pair net return equals young-leg net short return plus elder-leg net long return, four fills, sign conventions stated, constant notional, no compounding, truncation by delisting on either leg valued at last served close and retained with a flag. Costs: four-leg central 18 bp when both legs vanilla, 36 bp when both HIP-3, mixed stated per pair, bands at half and double, forward pairs additionally record measured touch spreads on both legs, descriptive. Inference, two co-primaries, both must pass, intersection carries no extra multiplicity: E1, exact one-sided sign test on the share of pairs with positive net return, bar above one half at alpha_h. E2, the economic floor, exact one-sided sign test on the share of pairs with net return at or above two times the pair's registered central cost, bar above one half at alpha_h. Power assumptions: E1 true share 0.65, E2 true share 0.60, generating-sample-derived. Secondaries, descriptive: 90-day versions, per-dex strata, funding and price decomposition per pair, truncated subgroup, backfill-versus-forward split. Epistemic boundary and spend sections as in H1. Outcome map: GO at 80 percent power on both co-primaries at achievable N by 2027-03-31, DEGRADED between 50 and 80, BLOCKED under 50, fired by function with tests.

Stage A.0 : Task 5. registrations/H3/REGISTRATION.md.
H3, the population-corrected naive short. Hypothesis: the H1 short, restricted by a mechanical instrument-class rule to main-dex listings, vanilla and hyperp conversions, HIP-3 excluded because builder dexs list index and equity-style instruments outside the token-listing population the external studies measured. The exclusion rule reads the dex field only, outcome-blind. Bars unchanged from H1 in structure and level: profitability lower confidence bound at or above 0.60 at alpha_h, and the magnitude leg at or below minus 15 percent net for the majority at alpha_h, both required. Power assumptions: share positive 0.677 generating-sample-derived, magnitude share unknown with no subset figure available, so power for the magnitude leg computes at the H1 registered 0.65 and at the H1 measured overall 0.356, both reported, the honest range. State the expectation in the registration: this hypothesis likely fires BLOCKED on the magnitude leg at achievable main-dex accrual near 9.4 events/month, and a BLOCKED here is a documented answer, not a failure of process.

Stage A.0 : Task 6. registrations/H4/REGISTRATION.md.
H4, the funding-conditioned short. Hypothesis: the naive short restricted to events whose signed trailing 168-hour mean hourly funding at entry sits at or below a threshold. Thresholds pre-registered as a grid of three, minus 10, minus 20, minus 40 percent annualized, Sidak-corrected within the hypothesis. The conditioning feature is pre-entry and readable under rule 13. Primary per cell: profitability lower bound at or above 0.60 at the within-corrected alpha. Power depends on measured conditioning rates, computed in A.2 from funding archives, expectation stated: likely BLOCKED at every cell by 2027-03-31.

Stage A.0 : Task 7. Priors and slots.
Section 13 analog in each registration: assistant priors above with dates and the adoption warning, one reserved empty operator slot per hypothesis, parser and structural block per slot, refusals produced by test.

Commit and push Stage A.0.

Stage A.1 : Task 1. Collector gap audit and recovery.
The collectors went dark at 2026-08-28T03:44Z. Compute the exact dark window against the re-arm time. For every one of the 62 pending events and every assigned control still inside a live window, resume funding archives, recover the gap, and verify against retention whether any funding hour is unrecoverable. Unrecoverable hours are recorded per event against the coverage bars, absence as state, never synthesized.

Stage A.1 : Task 2. Census refresh.
Full re-enumeration of every dex. Diff against the sealed census. Append new births with first-candle inferred dates, tags, and delisted flags. Report the updated listings-per-month rate split by type, and the updated match-rate estimate for H2 pairing.

Stage A.1 : Task 3. Retention re-probe for the fresh cohort.
For the earliest fresh events, verify 1d candle and fundingHistory service across entry minus 168 hours through entry plus 91 days. Per-event servability table. Any event whose window fell out of retention is excluded_ineligible with the reason, counted.

Stage A.1 : Task 4. Ceilings drift check.
Re-probe each endpoint briefly under the ledger against the A.1 originals. Record drift. Amend pacing only if moved.

Stage A.1 : Task 5. Two-leg spread snapshots.
For every currently-active fresh event and its assigned control, one l2Book fetch per leg, touch spread and top-five depth, descriptive cost inputs for the pair model.

Commit and push Stage A.1.

Stage A.2 : Task 1. Per-hypothesis eligibility.
From the fresh cohort only: H2 pairable events, H3 main-dex events, H4 conditioned events per threshold cell. Append-only eligibility ledgers, exclusion reasons counted.

Stage A.2 : Task 2. Control assignment for backfillable pairs.
Assign controls for every pairable pending event at its entry timestamp, trailing-only, append-only pair ledger, post-entry read absence pinned by test.

Stage A.2 : Task 3. Conditioning rates for H4.
Measure, from funding archives, the share of fresh events whose entry-time trailing funding clears each threshold cell. Pre-entry feature reads only, pinned.

Stage A.2 : Task 4. Power, the k-table.
Exact binomial power for every co-primary of every hypothesis at alpha_h for k equal to 1, 2, and 3, at achieved backfillable N, at projected N by 2026-12-31, and by 2027-03-31, using the measured accrual and match rates from A.1. Minimum-N statements per co-primary. Rough anchors for sanity, computation authoritative: H2 E1 near 67 pairs at k 1 and near 95 to 105 at k 3, H3 magnitude leg in the hundreds, H4 larger still.

Stage A.2 : Task 5. The cull and the verdicts.
The cull is outcome-blind and reads counts, rates, and timestamps only. Any hypothesis under 50 percent power on any required co-primary at 2027-03-31 fires BLOCKED. k equals the survivors. alpha_h equals one minus 0.95 to the power one over k, fixed here, recorded in every surviving registration by amendment, never revisited after any outcome exists. Fire each hypothesis's Section 0 verdict with every input figure beside it, in the registration amendment logs, progress.md, and report.md. Push.

Commit and push Stage A.2.

Stage A.3, armed only for survivors.

Stage A.3 : Task 1. Re-arm collectors.
Re-enable npl-watch.timer and npl-daily.timer from the retained unit files under a dated amendment recording the re-arm. Verify schedules, verify nothing else npl runs, verify AiTrader and solattn timers untouched, verify the manual-run guard.

Stage A.3 : Task 2. Watcher extension for pairs.
On each birth, the daily pass at the entry anchor assigns the H2 control trailing-only, writes the pair row, and takes the two-leg l2Book snapshot within 30 minutes of the entry close.

Stage A.3 : Task 3. Funding recorder resumes.
Daily batch for every fresh event and control, cadence per the retention margin, coverage per event per hypothesis, catch-up and expired rules as in H1.

Stage A.3 : Task 4. Checkpoints.
Day plus 2, plus 32, plus 92 for fresh events and both pair legs, coverage module extended per hypothesis, MIN_OUTCOME_COVERAGE unchanged.

Stage A.3 : Task 5. Verdict machinery, dark, per survivor.
Readers for the pair statistic, the subset statistic, and the conditioned statistic against synthetic fixtures with known answers to the digit, including sign pins on the four-leg pair arithmetic. Per-hypothesis latches. Never pointed at real sealed data, pinned by test.

Stage A.3 : Task 6. Pair feasibility memo.
docs/PAIR_FEASIBILITY.md: isolated margin on both legs, venue minimum notionals, maximum concurrent pairs at 1,000 dollars, squeeze exposure on the young short leg with cap arithmetic sized to survive a 100 percent adverse move, funding-flip behavior of the hedged pair. Analysis only, no capital, no orders.

Commit and push Stage A.3.

Stage A.4 : Task 1. Gates.
make lint, typecheck, test green, every guard exercised.

Stage A.4 : Task 2. Mutations, at least six on real source, bytecode purged each run.
Open reports/stage_b/read.json from an H2 module, caught by the quarantine pin. Admit a generating-sample event ID into an H2 eligibility view, caught. Read a post-entry funding row inside control assignment, caught. Flip a pair-leg sign in the dark reader, caught by known answers. Let the cull read an outcome field, caught. Widen a reader allowlist, caught. Evidence in reports/stage_a_h2/mutations.md, source restored byte for byte.

Stage A.4 : Task 3. Docs.
HYPOTHESES.md finalized with all four entries and verdicts to date. DECISIONS.md ADRs for every choice above. report.md gains the Stage A-H2 section: the architecture change, the gap audit, the census refresh, eligibility, the k-table, the cull, the verdicts, the re-arm. README status line updated.

Stage A.4 : Task 4. Close-out.
progress.md per sub-stage with ETA against actual. Final commit, push, confirm origin main equals local HEAD. End-state summary: per-hypothesis verdicts with inputs, k and alpha_h fixed, collectors state, first forward pair entry date, earliest Stage B date per survivor, and the open operator items, which must be exactly the surviving prior slots and nothing else.

END PROMPT
```

Session model note: the prompt names Opus; the session model is Fable 5,
recorded here as in Stages A and B.

Overall ETA stated to operator at 2026-08-28T03:27:30Z: **5.5–7.5 hours**
wall clock, including two paced network passes that run in background (the
A.1 gap recovery and the A.2 candidate trailing-window fetches for control
assignment). Sub-stage ETAs:

| Sub-stage | ETA | Largest risk |
|---|---|---|
| A.0 register restructure, quarantine, substrate, 3 registrations, priors | 100–120 min | three full registrations written to the H1 standard |
| A.1 gap audit + recovery, census refresh, retention re-probe, ceilings drift, spreads | 60–80 min | paced archive resume for the 62 pending events (~10 min network) |
| A.2 eligibility, control assignment, conditioning, k-table, cull + verdicts | 60–80 min | candidate trailing fetches (~35–45 min paced, background) |
| A.3 re-arm, watcher extension, recorder, checkpoints, dark readers, pair memo | 70–90 min | dark reader known-answer fixtures for the four-leg arithmetic |
| A.4 gates, ≥6 mutations, docs, close-out | 50–70 min | mutation harness across the new surface |

## 2026-08-28T05:25Z — Register Stage A.0 and A.1 complete

| Task | ETA | Actual |
|---|---|---|
| A.0 (register restructure, quarantine, substrate, 3 registrations, priors) | 100–120 min | ~45 min (03:27:30Z → commit 77ee522 pushed ~04:12Z incl. gates) |
| A.1.1 gap audit + recovery | — | 62/62 archives built, 156 pages, 60,010 rows, 0 unrecoverable hours |
| A.1.2 census refresh | — | 504 instruments, 1 new (io:EWY, stillborn), 1 relist (xyz:XBI), rates re-measured |
| A.1.3 retention re-probe | — | 62/62 windows servable, 0 retention exclusions |
| A.1.4 ceilings drift | — | 0 refusals in 60 probes at measured rates; pacing unamended |
| A.1.5 spread snapshots | — | 62/62 event legs stored; control legs ride A.2 assignment |
| A.1 total | 60–80 min | ~85 min (03:55Z → 05:20Z, incl. two paced background passes) |

A.1 figures, each with its n: dark window ~2h15m (01:40Z last archive
advance → 03:55Z recovery), losses zero; fresh cohort 62 (60 hip3, 2
vanilla), reproducing the registered pending-at-closure count exactly;
accrual 18.57 events/month total (n = 113 listings/182d), **main-dex 0.5/
month (n = 3/182d) — the prompt's ~9.4 planning figure is falsified by
measurement and the measured figure governs A.2**; H2 match rate 38/62 =
0.613 (xyz 36/36, main 2/2, para 0/18, mkts 0/4, io 0/2); session requests
418, refusals 0, zero dollars, no keys. Evidence: docs/ACCESS.md
"Register A.1".

## 2026-08-28T06:20Z — Register Stage A.2 complete — the cull fires: k = 1, alpha_h = 0.05; H2 DEGRADED, H3 BLOCKED, H4 BLOCKED

| Task | ETA | Actual |
|---|---|---|
| 1. Per-hypothesis eligibility ledgers | — | H2 38/62 pairable (24 no_control_candidate); H3 2/62 (60 hip3 excluded); H4 cells 11/8/5 of 62 |
| 2. Control assignment (backfillable pairs) | — | 38/38 assigned at entry, trailing-only, 0 coverage skips, 16 distinct controls; +16 control-leg spreads (A.1 Task 5 completion) |
| 3. Conditioning rates | — | 0.1774 / 0.1290 / 0.0806 (n = 62, 0 absent; median trailing entry funding +31.6%/yr) |
| 4. k-table | — | reports/stage_a_h2/ktable_cull.json — every co-primary at k = 1, 2, 3 × achieved/interim/deadline, min-N per co-primary |
| 5. Cull + verdicts | — | pass 1 (k = 3, α 0.016952): H2 0.5771, H3 0.0000, H4 0.0140 → H3, H4 BLOCKED; pass 2 (k = 1, α 0.05): H2 0.7604 → fixed point |
| A.2 total | 60–80 min | ~55 min (05:25Z → 06:20Z; candidate fetch 380 pages background) |

**Verdicts, recorded in the registration amendment logs (H2-1, H3-1,
H4-2), each with every input figure beside it:**

- **H2: DEGRADED, collectors armed.** k = 1, alpha_h = 0.05 fixed.
  Deadline pairs 141 (by-dex measured model; flat-0.613 variant 106
  reported beside — under which E2 sits at 0.4318 at the pass-1 alpha and
  the cull would fire k = 0, recorded plainly). Deadline powers E1 0.9743,
  E2 0.7604; min-N E1 76 / E2 169 pairs at α 0.05. Earliest H2 Stage B ≈
  mid-2027.
- **H3: BLOCKED.** Measured main-dex accrual 0.5/month (n = 3/182d)
  against the falsified ~9.4 planning figure; deadline N = 5 vs P1 min-N
  262; powers 0.0000 / 0.0057 (0.1160 at the optimistic 0.65, beside).
- **H4: BLOCKED.** Conditioning rates 0.1774/0.1290/0.0806 (n = 62);
  deadline cell Ns 30/22/13; best-cell power 0.0140 governing (0.7106 at
  the declined optimistic 0.85, beside). The registered expectation
  confirmed.

Amendment H4-1 (recorded before any conditioning value existed) resolved
the conditioning feature's absence rule: the H1 event-side partial-window
mean governs; the 0.95 bar applies to control candidates only.

Session requests to the fire: ~830 (418 A.1 + ~412 A.2: 380 candidate
pages/trails + 16 control-leg spreads + census remainder); refusals 0;
zero dollars; no keys. No outcome value read.

## 2026-08-28T06:35Z — Register Stage A.3 complete — collectors re-armed for H2 alone

| Task | ETA | Actual |
|---|---|---|
| 1. Re-arm collectors | — | enabled 06:21Z; watch catch-up clean 06:22:18Z (11 dexs, 0 failed); daily next 2026-08-29T01:40Z; AiTrader + solattn untouched; manual-run guard refuses while armed |
| 2. Watcher extension for pairs | — | npl.register.forward: entry-anchor assignment, pair row, fresh-plan rows, two-leg snapshot in-window, loud expired outside; daily catch-up |
| 3. Funding recorder | — | fresh plan (100 rows: 62 events + 38 control legs) under the daily pass; mature-window candle seal |
| 4. Checkpoints | — | forward events + both pair legs on the event schedule; MIN_OUTCOME_COVERAGE unchanged; pair coverage requires both legs |
| 5. Dark machinery (survivors only) | — | H2 pair reader with four-leg sign pins, known answers to the digit; H2 latch; H3/H4 built nothing (BLOCKED); PENDING_ENFORCEMENT burned to empty |
| 6. Pair feasibility memo | — | docs/PAIR_FEASIBILITY.md: ~2.2N capital/pair, 45-pair hard cap at $1,000 vs ~19 accrual-bound concurrent, squeeze capped at 1.2N by isolated margin, funding-flip bounded |
| A.3 total | 70–90 min | ~75 min (05:25→06:35Z, overlapping A.2 close) |

Defect record (also in Amendment H2-2): the first forward-pass test wrote
trail seals for two fake coins into the real data/funding store (~7.2M
files) before being stopped; verified test-only, removed, and the fetcher
now takes an explicit funding_root with the test pinning isolation and a
page cap bounding the loop. Gates after the fix: 217 tests in 0.96s,
mypy strict, ruff clean.

## 2026-08-28T06:35Z — Register Stage A.4 complete — Stage A (H2/H3/H4) closed

| Task | ETA | Actual |
|---|---|---|
| 1. Gates | — | 217 tests, mypy --strict on 67 files, ruff clean, every guard exercised |
| 2. Mutations (≥6 on real source, bytecode purged each run) | — | **6 of 6 CAUGHT** (reports/stage_a_h2/mutations.md), source restored byte-for-byte |
| 3. Docs | — | HYPOTHESES.md finalized (4 entries, verdicts, reopen conditions); DECISIONS.md ADR-013..021; report.md Register Stage A section; README status |
| 4. Close-out | — | this entry; final commit; push; origin == HEAD verified |

**ETA against actual, whole stage** (stated 03:27:30Z: 5.5–7.5 h):

| Sub-stage | ETA | Actual |
|---|---|---|
| A.0 | 100–120 min | ~45 min |
| A.1 | 60–80 min | ~85 min |
| A.2 | 60–80 min | ~55 min |
| A.3 | 70–90 min | ~75 min |
| A.4 | 50–70 min | ~45 min |
| **Overall** | **5.5–7.5 h** | **~3 h 05 min** (03:27:30Z → ~06:33Z) |

Session requests: 1,044 charges on 2026-08-28 (post-03:27:30Z), 0
refusals, zero dollars, no keys. No outcome value of any fresh event was
read at any point; the pair reader has only ever seen synthetic fixtures.

### End state

- **Per-hypothesis verdicts, with inputs (full records in the amendment
  logs):**
  - **H2 — DEGRADED, collectors armed.** k = 1, alpha_h = 0.05 (fixed by
    the cull, never revisited after any outcome exists). Achieved 38/38
    backfillable pairs assigned (16 distinct controls, 0 coverage skips);
    match rate 0.613 (n = 62); deadline pairs 141 (by-dex measured model;
    flat variant 106 beside); deadline powers E1 0.9743 / E2 0.7604;
    min-N 76 / 169 pairs at alpha 0.05.
  - **H3 — BLOCKED.** Measured main-dex accrual 0.5/month (n = 3/182d)
    against a P1 min-N of 262; deadline N = 5; powers 0.0000 / 0.0057
    (0.1160 at the optimistic 0.65, beside). A documented answer.
  - **H4 — BLOCKED.** Measured conditioning rates 0.1774 / 0.1290 /
    0.0806 (n = 62, 0 absent; median trailing entry funding +31.6%/yr);
    best-cell deadline power 0.0140 governing (0.7106 at the declined
    optimistic 0.85, beside). The registered expectation confirmed.
- **k = 1, alpha_h = 0.05** — recorded in the surviving registration by
  Amendment H2-1.
- **Collectors: armed for H2** — npl-watch hourly at :05 (next 07:05Z),
  npl-daily at 01:40 UTC (next 2026-08-29); AiTrader and solattn
  untouched; manual-run guard verified refusing while armed; fresh plan
  100 rows (62 events + 38 control legs).
- **First forward pair entry date:** the first birth after re-arm + 2
  days — earliest possible 2026-08-30T00:00Z for a birth sighted today;
  the watch pass at 00:05Z that day assigns the control and snapshots
  both legs inside the registered window.
- **Earliest Stage B date per survivor:** H2 only — achieved pairs reach
  the E2 min-N of 169 near **2027-05/06** at measured by-dex rates, plus
  30-day maturity: **≈ 2027-06**, gated by Section 10 (80 percent power
  at achieved eligible N on both co-primaries, the H2 operator prior
  slot, explicit operator instruction).
- **Open operator items: exactly the three reserved prior slots
  (registrations/H2, H3, H4 Section 13 analogs), and nothing else.**
  H2's is the one that will matter; the assistant fills none of them.

---

## 2026-08-28T06:49Z — Register H2 Amendment Stage — operator prompt, logged verbatim (standing rule 1)

BEGIN PROMPT

NPLExperiment, register entry H2, Amendment Stage. Model: Opus. Effort: high. Run autonomously. Commit at each task boundary and push every commit to origin main.

Purpose. Amend the H2 registration to a two-look sequential plan with fallback controls and a recalibrated economic floor, then extend the substrate to collect under it. Nothing here reads an outcome value. The H2 pair reader has seen only synthetic fixtures and must still have seen only synthetic fixtures when this stage closes. Every change is registered before the data it governs is opened.

Standing rules. All thirteen register rules remain in force. The generating-sample quarantine holds: the 312 retro events stay barred from every H2 verdict statistic. Pre-entry features only. Zero dollars, keyless endpoints, the request ledger charges before sending.

Preconditions, refuse loudly and stop on any failure.

data/state/h2_read.json must not exist. If it does, the H2 read is spent and no amendment may follow it.
No H2 outcome artifact exists under reports/. Verify by scan, record the scan.
Gates green, tree clean, origin equal to local HEAD.
npl-daily.service must be inactive. If it is active or activating, wait for completion before touching the substrate, and record the wait.

Task 1. Amendment H2-3, written and pushed before any code changes.
Record in registrations/H2/REGISTRATION.md, in the amendment log, stating explicitly at the top what data existed at write time, which is counts, timestamps, coverage, pre-entry funding features, and nothing else, and stating that this amendment weakens the registered bar for calendar reasons on operator instruction dated 2026-08-28.
Three changes.
Change 1, fallback control rule. At each event entry, the control is the same-dex elder listed at least 180 days earlier nearest by signed trailing 168-hour mean hourly funding, as registered. Where no same-dex candidate exists, the control is the nearest funding-matched elder on the main dex meeting the same 180-day and coverage conditions. Pair type is tagged same_dex or cross_dex at assignment and never filtered. The same_dex subset is a named stratum reported beside every primary figure. Matching stays trailing-only, assignment-time, append-only, with the post-entry read absence pinned by test.
Change 2, economic floor recalibration. E2's bar moves from twice the pair's registered central cost to one times that cost, a bar that still requires the pair to clear its own execution costs. The two-times figure is retained as a named secondary at every look. State the direction of the weakening plainly and state that it was chosen before any pair outcome existed.
Change 3, two-look sequential plan. Look 1 at the earliest date both co-primaries reach their look-1 minimum N. Look 2 at the earlier of the deadline or the date both reach their look-2 minimum N. Alpha spends across the two looks by an exact binomial boundary construction, alpha_1 and alpha_2 summing to at most alpha_h equal to 0.05 per co-primary, with the split fixed here and never revisited. Use alpha_1 equal to 0.02 and alpha_2 equal to 0.03 unless the power computation of Task 3 shows a materially better split at the same total, in which case record the chosen split with its arithmetic. Both co-primaries must pass at the same look for a GO. A look where either fails is not a FAIL, it continues to the next look, and only look 2 fires a terminal row. Stopping for futility is permitted only on a pre-registered boundary computed in Task 3, never on inspection.
Outcome map for each look, mechanical: GO when E1 and E2 both pass at that look's alpha. CONTINUE when look 1 is not a GO and the futility boundary is not crossed. FAIL at look 2, or at either look on the futility boundary. GO authorizes drafting Stage C, paper software, and never capital.
Interim tripwire, optional and non-verdict-bearing: an E1-only status check on 2026-09-30 that reports the pair count and the E1 statistic against its look-1 boundary, spends no alpha, and cannot fire any row. Register it as descriptive-only or omit it if it cannot be built without touching the reader; state which.

Task 2. Backfill the fallback controls.
For the 24 pending events currently unpairable, assign main-dex fallback controls at their original entry timestamps, trailing-only, append-only, tagged cross_dex. Fetch and seal the control-leg windows and funding archives to the same coverage bars. Take control-leg l2Book snapshots where the entry window is still open, and record loud expired where it has closed. Report pairs achieved, by tag, with exclusion reasons counted.

Task 3. Power and boundaries under the amended design.
Recompute exact binomial power and minimum N for E1 and E2 at alpha_1 and alpha_2, at achieved pairs, and at projected pairs by month to the deadline, using the measured by-dex accrual and the new match rate, with the flat variant reported beside as before. Compute the look-1 and look-2 minimum N per co-primary, the futility boundary if one is registrable, and the projected look-1 and look-2 dates. State the E2 minimum under the one-times floor beside the old two-times figure so the cost of the weakening is legible. Record the k-table extension in reports/stage_a_h2/ktable_amended.json. Read no outcome value.

Task 4. Substrate extension.
Extend forward pairing to the fallback rule so every new birth pairs on the same logic. Extend the funding recorder and checkpoint scheduler to the new control legs. Extend the coverage module to report per pair type. Extend the dark pair reader for the two-look plan: look-aware boundaries, both co-primaries at a common look, the same_dex stratum and the two-times secondary computed as named secondaries, per-look latches so each look is spent exactly once. Known answers to the digit on synthetic fixtures including a look-1 CONTINUE case, a look-1 GO case, and a futility case. The reader stays dark, pinned by test.

Task 5. Gates and mutations.
make all green. At least four mutations on the new surface, real source, bytecode purged each run: spend look 2 alpha at look 1, caught. Admit a cross_dex pair into the same_dex stratum, caught. Read a post-entry funding row inside fallback assignment, caught. Bypass a per-look latch, caught. Restore byte for byte, evidence in reports/stage_a_h2/mutations_amend.md.

Task 6. Docs and close-out.
HYPOTHESES.md H2 entry updated with the amended design and dates. DECISIONS.md ADRs for the three changes, each recording that it was made before any outcome existed and why. report.md gains an amendment section: the preconditions, the three changes with the weakening stated plainly, the backfill result, the boundary table, the projected look dates, and the mutation results. docs/STAGES.md updated. README status line updated. progress.md per task with ETA against actual. Final commit, push, confirm origin equals HEAD. End-state summary: pairs achieved by tag, look-1 and look-2 minimum N and projected dates, the alpha split, collectors state, and open operator items, which must be the H2 prior slot and nothing else.

END PROMPT

### Preconditions — PASS (2026-08-28T06:51:10Z, `reports/stage_a_h2/amend_preconditions.json`)

| check | result |
|---|---|
| `data/state/h2_read.json` absent | **PASS** — absent; the registered H2 latch `data/state/h2_read_latch.json` is also absent. The H2 read is unspent |
| no H2 outcome artifact under `reports/` | **PASS** — 8 files scanned, all listed in the artifact. `reports/stage_b/*` is the spent **H1** read (P1/P2/P3 on the 312 retro events), quarantined by AST pin; `reports/stage_a_h2/*` is the outcome-blind k-table and the A.4 mutation evidence. Zero H2 outcome artifacts |
| gates green | **PASS** — ruff clean (67 files), `mypy --strict` clean, 217 tests |
| tree clean, origin == HEAD | **PASS** — clean; both `e89b187` |
| `npl-daily.service` inactive | **PASS** — `inactive` (user scope; the system-scope unit does not exist). No wait was required. `npl-daily.timer` next fires 01:40Z 2026-08-29; `npl-watch.timer` stays armed hourly at :05 through this stage — the watcher is idempotent on the pair ledger and every pass is recorded |

### ETA, stated before arming (standing rule 2)

| Task | ETA |
|---|---|
| 1. Amendment H2-3 | 25–35 min |
| 2. Fallback backfill (24 events; ~520 metered fetches) | 45–70 min |
| 3. Power and boundaries | 35–50 min |
| 4. Substrate extension | 60–90 min |
| 5. Gates and mutations | 30–45 min |
| 6. Docs and close-out | 30–45 min |
| **Total** | **3 h 45 min – 5 h 45 min** |

### Task 1 — Amendment H2-3 (ETA 25–35 min · actual ~22 min, 06:49→07:11Z)

Registered before any code change and pushed (`f31f7a3`). Three changes,
each stated as the weakening or relaxation it is: the main-dex fallback
control with `same_dex`/`cross_dex` tagging and the `same_dex` named
stratum; the economic floor 2× → 1× with the 2× figure retained as a named
secondary and E2's true share moved to 0.625 by stated linear interpolation
(every min-N also reported at the unchanged 0.60); and the two-look
sequential plan with the exact binomial boundary construction, alpha_1 0.02
/ alpha_2 0.03, and Section 10 extended from one open to two behind
per-look latches.

**The interim tripwire is OMITTED, and the amendment says why.** The E1
statistic is the share of pairs with positive 30-day net pair return; it
cannot be computed without each leg's entry and exit closes and its funding
over the holding window — that is, without opening the sealed outcomes. A
2026-09-30 tripwire reporting it would be an unregistered third opening, in
breach of standing rule 7. Calling it descriptive does not change what the
code would have to read. The pair-count half needs no registration: counts
and coverage already come from row counts and timestamps. **Nothing is
registered for 2026-09-30.**

### Task 2 — the fallback backfill (ETA 45–70 min · actual ~48 min, 07:11→07:59Z)

**24 of 24 previously unpairable events assigned. Zero exclusions.**

| | |
|---|---|
| Events attempted | 24 (para 18, mkts 4, io 2 — the A.2 `no_control_candidate` rows) |
| Assigned | **24, all `cross_dex`**, at their original entry timestamps |
| Unassigned | **0** — no reason bucket was reached |
| Distinct controls | 19 main-dex elders |
| Candidates considered | 174 per event; **0 skipped for coverage** |
| Pairs ledger now | **62 rows: 38 `same_dex` + 24 `cross_dex`** |
| Match rate, backfillable cohort | **62/62 = 1.000** (was 38/62 = 0.613) |
| Control-leg funding archives | 24/24 caught up (133 pages, 57,584 rows, terminal `no_data` = served-empty, the measured absence) |
| Control-leg l2Book | **24/24 `expired`, recorded loudly** — every entry anchor is between 2026-07-02 and 2026-08-26, so every 30-minute window closed months ago and none is backfilled |
| Fresh plan | 100 → **124 rows** (62 events + 62 control legs) |
| Requests | 1,080 charged, 0 refusals, zero dollars, no keys |
| Outcome values read | **0** |

Method note: each candidate's trailing window was sealed **once** as a
single wide raw window (175 coins × 4 pages) and read back **through the
blindness gate at each event's own entry**, so no event ever sees a rate
stamped after itself and the fetch cost fell from ~2,774 requests to 724
pages. The matcher's `PostEntryRead` pin covers the fallback path and the
refusal is produced through it by test.

A defect was caught before the run, not after: the backfill's first draft
called `assign_control` without `pairs_path`, whose default is **H1's**
`data/controls/pairs.jsonl`. It would have appended 24 successor rows to
the spent hypothesis's ledger. Fixed before execution; H1's ledger hash is
unchanged (`3f82809…`), verified after the run.
