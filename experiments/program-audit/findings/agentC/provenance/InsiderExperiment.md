# InsiderExperiment — provenance verification (Agent C, referee)

Repository: `InsiderExperiment`
Anchored SHA: `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25) — this is also
`HEAD` of the live repository at the time of this audit, so the git history and the anchor coincide.
Document text read from `SNAP/InsiderExperiment/` (tracked, anchored).
Git objects read read-only from `/home/kiros-li/Documents/GitHub/InsiderExperiment`.
Untracked ledgers and artifact mtimes read read-only from the live working tree at
**2026-09-04 18:21–18:29 UTC** (UNANCHORED; they sit outside the anchored SHA and may have changed
after 2026-08-25, though every mtime observed falls inside the 2026-08-25 session window).
Prepared 2026-09-04.

Input: `findings/agentC/verification/InsiderExperiment.inventory.md` §4 and
`InsiderExperiment.inventory.json` `provenance_claims` (IP-01 … IP-15).

---

## 0. The commit record, in full

Seven commits, all authored 2026-08-25 by `kiros-li`, linear on `master`, author date equal to
committer date on every one. Times are the repository's own `-07:00`; the ledgers are stamped in
UTC, which is the same instant one day later.

| SHA | Author date (−07:00) | Same instant (UTC) | Subject |
|---|---|---|---|
| `fbfc74e` | 2026-08-25T18:34:56 | 2026-08-26T01:34:56Z | feat: scaffold, standing guards, and REGISTRATION Section 0 power gate |
| `398755b` | 2026-08-25T18:38:50 | 01:38:50Z | feat: REGISTRATION Sections 1 to 16, the full specification |
| `ccc9b13` | 2026-08-25T18:47:16 | 01:47:16Z | feat: Form 4 corpus from EDGAR, CORPUS-GO fired |
| `cb17046` | 2026-08-25T19:11:45 | 02:11:45Z | feat: the power gate, computed without reading alpha. BLOCKED at 49.35 bp |
| `672b343` | 2026-08-25T19:11:45 | 02:11:45Z | test: 106 tests green, and five registered mutations that fail the right guard |
| `d8b81f1` | 2026-08-25T19:11:55 | 02:11:55Z | docs: nine ADRs, the A.1 progress entry, and Section 15 results |
| `12d9fd3` | 2026-08-25T23:24:15 | 2026-08-26T06:24:15Z | Close at BLOCKED on the power gate, weight concentration not corpus, artifacts preserved |

### When data first existed

Established three ways, all agreeing.

1. **First wire request.** `ledgers/fetch.jsonl` line 1, `"recorded_at":"2026-08-26T01:35:18+00:00"`
   = 18:35:18 −07:00, for `2013q1_form345.zip`. **22 seconds after `fbfc74e`.**
2. **First measurement.** `ledgers/evidence.jsonl` record 1, `kind: market_port`,
   `"recorded_at":"2026-08-26T01:36:26+00:00"` = 18:36:26 −07:00, carrying `sessions 2615`,
   `formations 124`, `distinct_symbols 1218`, `bars_copied 2713496`. `reports/stage_a1/port.json`
   has mtime `2026-08-25 18:36:26.716 −07:00`, and `var/insider_market.db` mtime
   `2026-08-25 18:36:05.514 −07:00`.
3. **First data artifact committed.** `reports/stage_a1/port.json`, added in `398755b`
   (18:38:50) — the same commit that first added REGISTRATION Sections 1 to 16.

Full evidence-ledger timeline (14 records, all read 2026-09-04 18:21 UTC):

| # | kind | UTC | local −07:00 | payload |
|---|---|---|---|---|
| 1 | market_port | 01:36:26Z | 18:36:26 | 2,713,496 bars, both AiTrader SHA-256 equal, `unchanged: true` |
| 2 | corpus_gate | 01:42:24Z | 18:42:24 | CORPUS-GO, 4,585 |
| 3 | corpus_gate | 01:45:27Z | 18:45:27 | CORPUS-GO, 4,585 |
| 4 | corpus_validation | 01:46:56Z | 18:46:56 | 25 agree, 0 disagree |
| 5 | portfolio_build | 01:49:32Z | 18:49:32 | book_width_mean 71.909 |
| 6 | corpus_gate | 01:51:05Z | 18:51:05 | CORPUS-GO, 4,585 |
| 7 | portfolio_build | 01:51:10Z | 18:51:10 | book_width_mean 71.909 |
| 8 | **power_gate** | **01:51:14Z** | **18:51:14** | **BLOCKED, mde 49.3543** |
| 9 | portfolio_build | 01:52:33Z | 18:52:33 | + diagnostics block |
| 10 | power_gate | 01:52:49Z | 18:52:49 | BLOCKED, 49.3543 |
| 11 | corpus_gate | 02:05:33Z | 19:05:33 | CORPUS-GO, 4,585 (final) |
| 12 | portfolio_build | 02:05:40Z | 19:05:40 | final |
| 13 | power_gate | 02:05:40Z | 19:05:40 | BLOCKED, 49.3543 (final) |
| 14 | corpus_validation | 02:06:24Z | 19:06:24 | 25 agree, 0 disagree (final) |

Every artefact mtime under `reports/`, `var/` and `ledgers/` is ≤ `2026-08-25 19:10:28 −07:00`
(`mutations.json`), i.e. before the last three A.1 commits and 4 h 14 min before the Z.1 commit.

---

## 1. Registration claims table

Fifteen provenance claims (IP-01 … IP-15 in the inventory), plus one this pass found (IP-16),
each checked against git objects and, where the claim is about time, against the ledgers.
Counts: **17 SUPPORTED, 4 NOT_SUPPORTED, 2 PARTIAL, 1 UNVERIFIABLE** across the 24 rows of this
section and §2 together (16 registration claims, 8 parameter changes). Three draft findings.

| # | Claim (short) | File:line | Commit named | Commit found | Commit date (−07:00) | Data first existed | Status |
|---|---|---|---|---|---|---|---|
| IP-01 | Every parameter fixed before any measurement; Section 0 committed before Task 4 computes anything; a change needs a numbered amendment | `REGISTRATION.md:5-9` | none explicit (18:34 named in `progress.md:223`) | `fbfc74e` | 18:34:56 | 18:35:18 (first fetch) | **SUPPORTED** |
| IP-02 | Section 0 committed 18:34 before Task 4; Sections 1–16 committed 18:38; every parameter frozen first | `progress.md:223-224` | `fbfc74e`, `398755b` (by time) | both | 18:34:56 / 18:38:50 | 18:35:18 | **SUPPORTED** (with a stated nuance, below) |
| IP-03 | Section 15 empty when Section 0 was committed at 18:34 | `REGISTRATION.md:589-590` | `fbfc74e` (by time) | `fbfc74e` | 18:34:56 | 18:35:18 | **SUPPORTED** |
| IP-04 | Value-weighted named primary before any number was visible | `progress.md:47-48`; `REGISTRATION.md:761-762,856-858` | `fbfc74e`/`398755b` | both | 18:34:56 | first power_gate 18:51:14 | **SUPPORTED** |
| IP-05 | Equal-weighted registered secondary and labelled non-verdict-bearing before any number was visible; not promoted | `REGISTRATION.md:856-858` | `398755b` (by time) | `398755b` | 18:38:50 | first power_gate 18:51:14 | **SUPPORTED** |
| IP-06 | "Section 16. Amendments — None in force." read against `REGISTRATION.md:8-9` | `REGISTRATION.md:798-800` | none | — | — | corpus built 18:47:16 | **NOT_SUPPORTED** → DRAFT-P-1 |
| IP-07 | `insider.power` structurally incapable of emitting a mean; sealed store has one permitted reader | `CLAUDE.md:20-24` | none | — | — | — | **SUPPORTED** |
| IP-08 | Verdict stands on the registered primary; equal-weighted 34.29 not promoted | `progress.md:261-263` | none | — | — | — | **SUPPORTED** |
| IP-09 | No systemd unit or timer was ever installed by this repository | `progress.md:127-131` | none | — | — | — | **PARTIAL** (true today; the 2026-08-25 state is not observable) |
| IP-10 | Both AiTrader hashes re-verified unchanged at closure | `progress.md:135-138` | none | — | — | — | **PARTIAL** (`universe.py` independently confirmed; `analysis_bars.db` no longer reproducible) |
| IP-11 | The operator-prior slot is present, empty, and blocks Stage B; the assistant's 0.12 sits outside it | `REGISTRATION.md:497-513` | none | — | — | — | **SUPPORTED** |
| IP-12 | ADR-008 moved exactly one transaction; 4,585 and 49.35 unchanged | `DECISIONS.md:245-249` | ADR-008; change lands in `cb17046`/`672b343` | both | 19:11:45 | corpus built 18:47:16 | **SUPPORTED** |
| IP-13 | Z.1 records only: no statistic, no alpha, no sealed store, no request, no result changed | `progress.md:9-10` | `12d9fd3` | `12d9fd3` | 23:24:15 | — | **SUPPORTED** |
| IP-14 | The calibration ledger holds zero independently formed entries | `progress.md:305-306` | none | — | — | — | **UNVERIFIABLE** (ledger lives outside this repository) |
| IP-15 | "The commit record puts … Stage Z.1 at about 20 minutes. The Z.1 brief records five hours. The commit record cannot confirm that figure." | `progress.md:115-117` | `d8b81f1`, `12d9fd3` | both | 19:11:55 / 23:24:15 | — | **NOT_SUPPORTED** → DRAFT-P-2 |
| IP-16 | "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit timestamps where one exists." (not in the LOCATE inventory; found in this pass) | `progress.md:193-194` | none | — | — | first ledger record 2026-08-26T01:35:18Z | **NOT_SUPPORTED** → DRAFT-P-3 |

### The evidence behind each row

**IP-01, IP-03 — SUPPORTED.** `REGISTRATION.md` at `fbfc74e` is 159 lines and ends inside Section
0.5. `git diff --unified=0 fbfc74e HEAD -- REGISTRATION.md` is a single hunk,
`@@ -159,0 +160,737 @@`, 737 insertions and **0 deletions**. Independently:
`git show fbfc74e:REGISTRATION.md | head -159 | sha1sum` and
`git show HEAD:REGISTRATION.md | head -159 | sha1sum` both give
`1091db55b22df21ba45963246d92219267242434`. Section 0 is byte-identical at the anchor. Quoting the
committed version:

```
$ git show fbfc74e:REGISTRATION.md   (lines 39-46)
| Verdict | Bar | Consequence |
|---|---|---|
| **GO** | MDE at or below 20 bp per month | ... Stage B is authorized. |
| **DEGRADED** | MDE between 20 and 40 bp per month | ... |
| **BLOCKED** | MDE above 40 bp per month | ... Stage B is never written and the repo closes on the finding. |

Boundaries are inclusive at the lower edge. An MDE of exactly 20.00 bp is GO. An
MDE of exactly 40.00 bp is DEGRADED.
```
```
$ git show fbfc74e:REGISTRATION.md   (lines 68-73)
Registered floor, both conditions required:
- **1,000 qualifying events** over the bar span, counted after every ex-ante filter in Section 3.
- **80 percent of in-span sessions carrying a non-empty book** at the primary six-month hold.
```
```
$ git show fbfc74e:REGISTRATION.md   (lines 84-88)
    MDE_month = t * M * s_d / sqrt(N_eff)
with t the critical value 2.0, M the registered 21 sessions per month, s_d the
daily excess-return standard deviation, and N_eff the effective independent
period count after the serial-correlation penalty.
```
Section 15 does not exist in `fbfc74e` (the file stops at line 159); it is first added by `d8b81f1`
at 19:11:55, and `git diff -U2 d8b81f1^ d8b81f1 -- REGISTRATION.md` shows the stub it replaced was
`-Filled by Task 4 and Task 5. Empty at the time Section 0 was committed.`

**IP-02 — SUPPORTED, with the sequence stated.** `git show fbfc74e:src/insider/config.py` already
carries **every** registered value later cited anywhere in the document: `mde_go_ceiling_bp=20.0`,
`mde_degraded_ceiling_bp=40.0`, `corpus_event_floor=1_000`, `corpus_coverage_floor=0.80`,
`t_critical=2.0`, `newey_west_lags=21`, `newey_west_lag_grid=(5, 21, 63, 126)`,
`primary_hold_sessions=126`, `secondary_hold_sessions=(21, 63)`, `entry_lag_sessions=1`,
`primary_weighting="value_weighted"`, `secondary_weighting="equal_weighted"`, `spread_bp_low=15.8`,
`spread_bp_high=50.0`, `round_trip_bp_low=32.0`, `round_trip_bp_high=100.0`,
`decayed_gross_band_bp=(30.0, 40.0)`, `sessions_per_month=21`, `routine_consecutive_years=3`,
`min_history_years=3`, `cluster_min_filers=3`, `cluster_window_days=5`,
`johnsen_same_date_price_fraction=0.80`, `min_transaction_usd=10_000.0`, `exclude_10b5_1=True`,
`allowed_transaction_codes=("P",)`, `assistant_prior=0.12`, `sec_requests_per_second=8.0`.
A pickaxe on each of those eighteen literal assignments
(`git log -S '<literal>' -- src/insider/config.py`) returns **exactly one commit, `fbfc74e`**, for
every one: none was ever edited. `src/insider/section0.py` (the gate that fires the verdict) and
`src/insider/cost.py` (the drag and net band) each have a `git log --follow` of exactly one commit,
`fbfc74e`. So the enforced bars were frozen 22 seconds before the first wire request.

Nuance, stated because it is a real ordering and the authors themselves publish the times: the
market port ran at 18:36:26 and wrote `port.json`, and Sections 1 to 16 were committed 2 min 24 s
later, at 18:38:50, in the same commit that added `port.json`. The claim survives because the
market port used only `universe_id`, `bars_start`, `bars_end` — all frozen at 18:34:56 — and
because Sections 1 to 16 introduce no numeric parameter that was not already in `config.py`
(checked line by line: Sections 6 to 10 name 126, 21, 63, 15.8, 50, 32, 100, 2.0, lag 21 with grid
5/21/63/126, and the 30–40 band; 5.33/16.67 and 13.3/34.7 are computed by `insider.cost`, itself
frozen at `fbfc74e`). "Every parameter … fixed before any measurement runs" is true of every
parameter; the *prose* of Sections 1–16 postdates the first measurement by 2 min 24 s, and
`progress.md:223-224` discloses that timing itself.

**IP-04, IP-05 — SUPPORTED.** `primary_weighting="value_weighted"` and
`secondary_weighting="equal_weighted"` are in `config.py` at `fbfc74e` (18:34:56).
`git diff --unified=0 398755b HEAD -- REGISTRATION.md` touches only lines ≥ 589; Sections 7
(lines 385-398) and 10 (lines 452-482) are unchanged from `398755b` (18:38:50) to the anchor. The
two deletions in `d8b81f1` that the inventory flagged as needing location are both prose stubs in
Sections 15 and 16, not Sections 7 or 10:
`-Filled by Task 4 and Task 5. Empty at the time Section 0 was committed.` and `-None in force.`
The first equal-weighted MDE (`34.2897`, in `reports/stage_a1/power.json`) was computed at the
first `power_gate` record, 18:51:14 — 12 min 24 s after Sections 7 and 10 were committed.
`power.json` records `verdict: BLOCKED` with top-level `mde_bp_per_month: 49.3543`, which is the
`value_weighted`/126 row; the `equal_weighted`/126 row at 34.2897 is present and fires nothing.

**IP-07 — SUPPORTED.** `DispersionStats` (`src/insider/power/dispersion.py:124-150`) and
`MdeResult` (`src/insider/power/mde.py:19-36`) carry no first-moment field: the tuples are holds,
weighting, counts, `sd_daily_excess`, tracking error, NW lags, VIF, effective periods,
autocorrelations, book-width order statistics. `grep -rn "SEALED_DB\|insider_sealed" src/` returns
only `paths.py` (defines it), `eval/evaluator.py` (the sole reader; opens
`f"file:{SEALED_DB}?mode=ro"`) and `portfolio/returns.py` (writes only — `_sealed()` at lines
245-254 opens, `executescript`, `INSERT`, `commit`, `close`; no `SELECT`). `tests/test_guards.py:32-38`
declares exactly that allow-set with the comment `# writes, never reads`.

**IP-09 — PARTIAL.** Checked on the host at 2026-09-04 18:26 UTC: `~/.config/systemd/user` holds
18 entries, none naming this repository (`claude-auto-retry-reconcile`, `etf-daily`, `etf-snap`,
`hfexperiment-bars`, `news-collect`, `npl-daily`, `npl-watch`, `solattn-*`);
`grep -ril insider ~/.config/systemd/user /etc/systemd/system` returns nothing;
`systemctl --user list-timers --all` lists 8 timers, none matching; `systemctl --user list-units
--all | grep -i insider` returns nothing; `crontab -l` says `no crontab for kiros-li`. The claim
holds as of today. It cannot be established for 2026-08-25 from any artefact in this repository, so
the status is PARTIAL rather than SUPPORTED — the negative is confirmed, its date is not.

**IP-10 — PARTIAL, and the checkable half is confirmed.** `sha256sum` of
`SNAP/AiTrader/backtest/universe.py` (AiTrader anchored at `705e0ed`, 2026-08-24, i.e. the day
before the port) returns
`8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529`, **exactly** the
`universe_sha256_before` and `universe_sha256_after` in `reports/stage_a1/port.json` and the digest
printed at `progress.md:138`. That is independent confirmation of one of the two hashes.
`analysis_bars.db` is not reproducible: `port.json` records `bars_size_bytes: 7320629248` and the
live file is 7,323,656,192 bytes with mtime 2026-09-03 — the AiTrader collector has written to it
since, so a mismatch today is not evidence against this repository.
`src/insider/paths.py:36-40` names exactly two AiTrader paths and no other, with the comment
`# Read-only source paths in the neighbouring repository. Two paths, no others.` /
`# Nothing here is ever written and news_experiment.db is never named.`

**IP-11 — SUPPORTED.** `REGISTRATION.md:507` still reads
`> [ EMPTY. The operator writes a number here himself, before Stage B runs. ]` at the anchor.
`src/insider/registration_check.py:59-66` raises `OperatorPriorMissing` rather than warning, and
`operator_prior()` returns `None` whenever `EMPTY_MARKER` is present, so absence of the marker is
not treated as presence of a prior. `assistant_prior=0.12` lives in `config.py`, outside the
Section 12 slot, and `REGISTRATION.md:513` records it beside the slot.

**IP-12 — SUPPORTED.** `git diff -U1 ccc9b13 cb17046 -- reports/stage_a1/corpus.json` moves
`filtered_routine/insufficient_history` 2058 → 2057 and `filtered_routine/routine` 155 → 156, and
`routine_labels.insufficient_history` 2472 → 2471, `routine_labels.routine` 159 → 160. Exactly one
transaction, as ADR-008 claims. `qualifying_events` does not appear in the diff, so 4,585 is
unchanged; all three `power_gate` evidence records (18:51:14, 18:52:49, 19:05:40) carry
`mde_bp_per_month: 49.3543`, so the MDE is unchanged across the corpus rebuild. The same commit
also rewrites all eleven `events_per_year` cells and `unclassifiable_by_year["2018"]` 257 → 256;
that is the surrogate-key fix, covered separately by ADR-013, and it is the numeric lane's IC-02,
not a defect in ADR-008's own arithmetic.

**IP-13 — SUPPORTED.** `git show --stat 12d9fd3` lists exactly `DECISIONS.md`, `REGISTRATION.md`,
`progress.md`; `--name-status` shows three `M` entries, 408 insertions and **0 deletions**. No file
under `src/`, `reports/`, `var/`, `ledgers/` or `cache/` is touched. Every mtime under those
directories is ≤ 2026-08-25 19:10:28 −07:00, four hours before the Z.1 commit. The last ledger
append is 19:06:24, so no request was sent and no evidence record was written during Z.1.

**IP-14 — UNVERIFIABLE.** The calibration ledger is a program-level artefact outside this
repository. Nothing in `InsiderExperiment` can confirm or contradict "zero independently formed
entries". Recorded as unverifiable rather than guessed at.

---

## 2. Parameter changes after data existed

Data first existed at **2026-08-25 18:35:18 −07:00** (first wire request) / **18:36:26** (first
measurement). Everything below is a change committed after that instant. Nothing else in the
repository changed after it: the pickaxe over all eighteen registered literals returns one commit
each, `fbfc74e`, and `section0.py`, `cost.py`, `classify.py` and `cluster.py` each have a one-commit
`--follow` history at `fbfc74e`.

| # | What changed | File | Commit | Date (−07:00) | Verdict-relevant? | Dated amendment? | Amendment ref | Status |
|---|---|---|---|---|---|---|---|---|
| C-1 | `benchmark_id: str` declaration and `benchmark_id="U-LIQ-500-VW"` value **deleted** from the frozen `Config` | `src/insider/config.py` | `672b343` | 19:11:45 | no — the field was read by no module at any commit | **no** | none anywhere | **NOT_SUPPORTED** → DRAFT-P-1 |
| C-2 | Routine classification **order reversed**: pattern tested first, three-year history gate second | `src/insider/corpus/routine.py` | `672b343` | 19:11:45 | no — one label moved; 4,585 and 49.3543 unchanged | yes | ADR-008, `DECISIONS.md:226-256`, "Accepted, Stage A.1, 2026-08-25", with the defect, the reason, and the corpus impact | SUPPORTED (see note) |
| C-3 | `event` table primary key changed from the composite natural key `(accession, filer_cik, transaction_date, value_usd)` to a surrogate `event_id INTEGER PRIMARY KEY AUTOINCREMENT`; `INSERT OR REPLACE` → `INSERT` | `src/insider/corpus/store.py` | `cb17046` | 19:11:45 | yes — it restored 43 previously merged events | yes | ADR-013, `DECISIONS.md:400-416`, "Accepted, Stage Z.1, 2026-08-25. Records a defect corrected in A.1." | SUPPORTED |
| C-4 | Build now raises when the offered event count and the stored count diverge | `src/insider/corpus/build.py:412-420` | `cb17046` | 19:11:45 | no — a guard, not a parameter | yes | ADR-013 | SUPPORTED |
| C-5 | `events_per_year` all eleven cells rewritten (262→263, 406→409, 524→531, 457→462, 717→728, 297→298, 502→504, 505→508, 410→418, 363→365, 99 unchanged); `filtered_routine/*` and `routine_labels` as in C-2; `unclassifiable_by_year["2018"]` 257→256 | `reports/stage_a1/corpus.json` | `cb17046` | 19:11:45 | yes — these are the printed corpus figures | yes | ADR-013 (+ ADR-008 for the one-label move) | SUPPORTED as a change; the *document* transcription is the numeric lane's IC-02 |
| C-6 | The 25-document and 25-issuer validation samples changed (30 rows replaced, e.g. `0000895126-16-000555`/CHK → `0001127602-16-063277`/RRC) | `reports/stage_a1/validation.json` | `cb17046` | 19:11:45 | no — both runs report 25 agree, 0 disagree | yes (consequential) | ADR-013 | SUPPORTED |
| C-7 | Sealed and dispersion store schemas gained a `weighting` column, primary keys extended to `(hold_sessions, weighting, date)`; concentration diagnostics added | `src/insider/portfolio/returns.py` | `cb17046` | 19:11:45 | no — it lets the secondary series coexist with the primary rather than overwrite it | not recorded as an amendment (it is not a registered value) | — | SUPPORTED |
| C-8 | Lint/format only, no parameter: `pyproject.toml` (two per-file `T20` ignores), `scripts/refuse_env_commit.py` (parenthesised a precedence bug in the `.env` matcher), `edgar/bulk.py`, `edgar/client.py`, `market/source.py`, `market/store.py`, `corpus/validate.py`, `registration_check.py` | various | `cb17046` | 19:11:45 | no | n/a | — | SUPPORTED |

The C-6 sample change is fully explained and needs no amendment of its own: `validate.py:118-123`
draws a deterministic systematic sample, `rows[::step][:25]` over
`FROM event ORDER BY entry_session, accession`. Restoring 43 merged rows shifted the stride
positions, so different documents were drawn. No seed, no randomness, and the verdict of the route
(25 agree, 0 disagree) is identical in both runs (evidence records 4 and 14).

**Note on C-2, recorded rather than raised as a finding.** ADR-008 discloses this change fully —
dated, with the defect, the literature argument, the corpus impact and how it was found. Two
residues are worth stating without inflating them into a finding. First, the change lives in
`DECISIONS.md`, not in the numbered-amendment slot that `REGISTRATION.md:8-9` names, and
`REGISTRATION.md:798-800` still reads "None in force." Second, the registered sentence the change
supersedes was never amended: `REGISTRATION.md:258` still reads "**Three years of trading history
is required to classify at all.**", which the shipped `routine.py` no longer does — a
pattern-routine insider with under three years of history is now labelled `routine`. Both residues
are folded into DRAFT-P-1's evidence, which is about the "None in force" statement.

**Note on commit ordering, recorded rather than raised.** `cb17046` commits the corrected
`corpus.json` (the one-label move of C-2) while its tree still holds the *uncorrected*
`routine.py`; the fix arrives one commit later in `672b343`. Re-running the corpus builder at
`cb17046` would not reproduce `cb17046`'s own `corpus.json`. The two commits carry the same author
timestamp to the second (19:11:45), so this is one commit operation split in two, and the anchor
`12d9fd3` is internally consistent. Recorded for the record; not a finding.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the registration's amendment discipline — `Config`, the frozen
  parameter set, and `REGISTRATION.md` Section 16
- **Direction:** neutral (pure hygiene: no figure in the repository moves either way)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "None in force. Section 0 fired BLOCKED, so no amendment
  can authorize Stage B." — InsiderExperiment/REGISTRATION.md:800. Read against "Changing a
  registered value after that commit requires a numbered amendment in Section 17 carrying its own
  evidence." — InsiderExperiment/REGISTRATION.md:8-9, and against the config file's own rule,
  "Values here are registered in REGISTRATION.md and frozen before Task 4 computes anything.
  Changing one after the corpus is built requires a numbered amendment." —
  InsiderExperiment/src/insider/config.py:8-9.
- **Evidence:**
  - A registered field was deleted after the corpus was built.
    `git -C <live> diff fbfc74e 672b343 -- src/insider/config.py` (read 2026-09-04 18:23 UTC):
    ```
    @@ -18,13 +18,12 @@ class Config:
         # --- span ---------------------------------------------------------
         universe_id: str
    -    benchmark_id: str
         bars_start: str
    @@ -84,13 +83,12 @@ CONFIG: Final = Config(
         universe_id="U-LIQ-500-stk-w60-m40-p5",
    -    benchmark_id="U-LIQ-500-VW",
    ```
    `672b343` author date **2026-08-25T19:11:45−07:00**. The corpus was built at `ccc9b13`
    18:47:16 and CORPUS-GO had already fired four times in the evidence ledger (18:42:24, 18:45:27,
    18:51:05, 19:05:33); the power gate had already fired BLOCKED three times (18:51:14, 18:52:49,
    19:05:40). n/a — this is a code object, not a sample.
  - No amendment records it. `REGISTRATION.md:798-800` (Section 16, the amendments section) reads
    "None in force." `git grep benchmark_id HEAD` and `git grep "U-LIQ-500-VW" HEAD` both return
    nothing; the string appears in no ADR, no progress entry and no section of the registration.
    `DECISIONS.md` has thirteen ADRs and none mentions the benchmark identifier.
  - It touches no figure. `git grep -n benchmark_id fbfc74e` and `git grep -n benchmark_id cb17046`
    each return exactly two hits, both inside `src/insider/config.py` (lines 24 and 90). No module
    outside `config.py` ever read the field at any commit, so its removal cannot have moved
    49.3543, 4,585, 71.9 or any other number. `reports/stage_a1/portfolio.json` and the
    `portfolio_build` evidence records still carry a `no_benchmark: 0` drop key, so the benchmark
    itself is computed (in `portfolio/returns.py`); only its registered *identifier* is gone.
    Section 5's benchmark, `REGISTRATION.md:351-357`, survives as prose with nothing enforcing it.
  - Second instance of the same statement failing, disclosed elsewhere by the authors: the
    registered classification order at `REGISTRATION.md:258` ("**Three years of trading history is
    required to classify at all.**", committed `398755b` 18:38:50 and never amended) is superseded
    by `git diff 672b343^ 672b343 -- src/insider/corpus/routine.py`, which tests the routine pattern
    before the history gate. That change **is** disclosed, dated and reasoned in ADR-008
    (`DECISIONS.md:226-256`) — it is cited here only because Section 16 reports it as nothing in
    force and Section 3.4's own sentence was left standing.
- **Recomputation (if any):** none required. The mechanism of the deletion is visible:
  `src/insider/config.py:3-6` states "Every field declared here must be referenced by at least one
  module under src/insider outside this file. tests/test_guards.py fails when a field has no
  enforcement site", and `tests/test_guards.py:119-130`
  (`test_every_config_field_has_an_enforcement_site`) asserts exactly that over the AST of every
  source file. `benchmark_id` had no enforcement site, so the guard added in `672b343` would have
  failed on it; the field was deleted rather than enforced or amended. The guard did its job; the
  amendment discipline did not record the consequence.
- **What would resolve it:** a numbered amendment in `REGISTRATION.md` Section 16 (or Section 17,
  whichever the authors intend — see the pointer note below) recording that `benchmark_id` was
  removed on 2026-08-25 at 19:11:45, why, what data existed at the time, and that no computed figure
  depends on it; and a matching correction to "None in force." Alternatively a statement that
  deleting an unenforced decorative field is not "changing a registered value" under the Section 0
  rule, which would make the claim true by definition.
- **Confidence:** HIGH — the diff, the commit date, the absence of the identifier anywhere at HEAD
  and the "None in force." line are all direct reads of git objects and the anchored tree.
- **Invalidated by later commits?:** no. `12d9fd3` is both the anchor and the live `HEAD`; there is
  no commit after it, and the repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker dated
  2026-09-02.
- **Disclosed by authors?:** no. No ADR, no progress entry and no registration section mentions
  `benchmark_id` or its removal. (The *routine-order* instance cited as a second example **is**
  disclosed, at `DECISIONS.md:226-256`; the finding does not rest on it.)

### DRAFT-P-2
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the session-cost record — what the commit record is said to establish
  about Stage Z.1's duration
- **Direction:** B (a cost/effort figure is presented as record-backed when the record does not
  carry it)
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Cost, measured rather than asserted.** The commit record
  puts Stage A.1 at about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about
  20 minutes. The Z.1 brief records five hours. The commit record cannot confirm that figure, which
  presumably counts operator time between stages that this repository does not observe." —
  InsiderExperiment/progress.md:115-119
- **Evidence:**
  - `git -C <live> log --all --date=iso-strict` (read 2026-09-04 18:22 UTC) returns **seven**
    commits, n = 7. Six belong to Stage A.1 (18:34:56 to 19:11:55) and **exactly one** belongs to
    Stage Z.1: `12d9fd3`, 2026-08-25T23:24:15−07:00, author date equal to committer date. A single
    commit has no interior interval, so the commit record supplies **no** Z.1 duration at all — it
    cannot put Z.1 "at about 20 minutes" any more than it can confirm five hours.
  - The only interval the commit record does carry across the boundary is
    `d8b81f1` 19:11:55 → `12d9fd3` 23:24:15 = **4 h 12 min 20 s**, which is far from 20 minutes and
    is not inconsistent with the brief's five hours.
  - No artefact narrows it either: every mtime under `reports/`, `var/` and `ledgers/` is
    ≤ 2026-08-25 19:10:28 −07:00 (`mutations.json` 19:10:28; `evidence.jsonl` and `fetch.jsonl`
    19:06:24), so nothing was written during the Z.1 window. That is exactly what makes IP-13
    ("no result changed") SUPPORTED, and it is the same fact that leaves the 20-minute figure
    unsourced.
  - The 51-minute A.1 figure is also only partly from the commit record: its start, 18:20, is
    earlier than the first commit (`fbfc74e` 18:34:56) and earlier than the first ledger record
    (18:35:18). 18:20 comes from `progress.md:193`, not from any git object.
- **Recomputation (if any):** inputs — `git log` author dates for `d8b81f1` and `12d9fd3`
  (InsiderExperiment, read 2026-09-04 18:22 UTC); method — subtract; result 4:12:20; tolerance ±1 s.
  Commit count for Stage Z.1: 1.
- **What would resolve it:** attributing the 20 minutes to its actual source (a session clock or the
  Z.1 brief) rather than to "the commit record", or stating plainly that the commit record bounds
  neither figure and that the only observable is the 4 h 12 min gap.
- **Confidence:** HIGH — the commit count and the two timestamps are direct reads; the inference
  that one commit yields no interval is arithmetic.
- **Invalidated by later commits?:** no. There is no commit after `12d9fd3`, and a later commit
  could only add Z.1 boundaries that did not exist when the sentence was written.
- **Disclosed by authors?:** partly, and the disclosed half is the other one. The same passage says
  "The commit record cannot confirm that figure" of the **five-hour** brief figure
  (`progress.md:117-118`) and closes "Both are recorded rather than one being picked"
  (`progress.md:119`). What is not disclosed is that the 20-minute figure is equally unsupported by
  the record it is attributed to. This overlaps the numeric lane's Rank 6 (the stated session cost)
  and is reported here because the claim is specifically about what the git record shows.

### DRAFT-P-3
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the ETA-against-actual table and the session timeline
- **Direction:** neutral (hygiene)
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Timings are wall clock, session start 18:20 UTC,
  boundaries taken from commit timestamps where one exists." — InsiderExperiment/progress.md:193-194
- **Evidence:**
  - Every commit in the repository is stamped `−07:00`: `fbfc74e` `2026-08-25T18:34:56-07:00`,
    `12d9fd3` `2026-08-25T23:24:15-07:00` (n = 7 commits, `git log --date=iso-strict`, read
    2026-09-04 18:22 UTC).
  - The ledgers are stamped in true UTC and are one calendar day later: `ledgers/fetch.jsonl` line 1
    `"recorded_at":"2026-08-26T01:35:18+00:00"`, `ledgers/evidence.jsonl` record 1
    `"recorded_at":"2026-08-26T01:36:26+00:00"` (read 2026-09-04 18:21 UTC, n = 684 fetch records
    and 14 evidence records).
  - 18:35:18 −07:00 = 2026-08-26T01:35:18Z. The stated "session start 18:20 UTC" is therefore a
    local (PDT) clock time mislabelled as UTC; in UTC the session began 2026-08-26T01:20Z. The same
    mislabelling carries into the "18:20 to 19:11" span at `progress.md:116` and into every row of
    the task table at `progress.md:196-205`.
  - The internal arithmetic is unaffected: 18:20 → 19:11 is 51 minutes in either zone.
- **Recomputation (if any):** inputs — commit author date `fbfc74e` (−07:00) and `fetch.jsonl` line
  1 (`+00:00`); method — convert; result: the two differ by exactly 7 h, confirming the commit clock
  is UTC−07:00 and the "UTC" label on 18:20 is wrong; tolerance ±1 s.
- **What would resolve it:** relabelling the session start as local time (or restating it as
  2026-08-26T01:20Z), so a later reader comparing the task table against the UTC-stamped ledgers
  does not find a seven-hour discrepancy.
- **Confidence:** HIGH — both clocks are read directly and their offset is exact.
- **Invalidated by later commits?:** no; there is no commit after the anchor.
- **Disclosed by authors?:** no. The sentence asserts the zone rather than qualifying it.

---

## 4. What could not be checked, and why

| Item | Why not |
|---|---|
| `analysis_bars.db` SHA-256 `d599ccf0…e924` (IP-10) | The live file is 7,323,656,192 bytes with mtime 2026-09-03 against `port.json`'s recorded `bars_size_bytes: 7320629248`. The AiTrader collector has written to it since 2026-08-25, so the digest cannot be recomputed and a mismatch today would say nothing about this repository. The companion hash (`backtest/universe.py`) **was** confirmed from the AiTrader snapshot; see IP-10 above. |
| Whether a systemd unit existed on 2026-08-25 (IP-09) | Only the present state of the host is observable. Today's check is clean; the historical negative rests on the authors' word plus the absence of any unit file, timer or installer script in the repository at any commit. |
| The program calibration ledger, "zero independently formed entries" (IP-14) | The ledger is outside this repository. Nothing here can confirm or contradict it. Recorded as unverifiable rather than guessed. |
| Whether the working tree at 18:36:26 (the market port) matched `fbfc74e` exactly | Git records commits, not working trees. The port used only `universe_id`, `bars_start` and `bars_end`, all present at `fbfc74e`, and `market/universe.py`, `build.py`, `source.py`, `store.py` all have a one-commit `--follow` history at `fbfc74e` — so the code that ran is the code that was committed at 18:34:56 unless it was edited and reverted, which git cannot exclude. |
| Whether the working tree at 19:05:33 (the final corpus build) matched any single commit | It did not match `cb17046` (see the commit-ordering note in §2): the corrected `corpus.json` was produced by a `routine.py` that only lands in `672b343`. The anchor is consistent; the intermediate commit is not. |
| The stored realized alpha | `var/insider_sealed.db` was **not** opened by this audit, by design. Its existence (884,736 bytes, mtime 2026-08-25 19:05:40) and its single permitted reader were checked statically only. |
| Whether Stage Z.1 took 20 minutes or five hours | Neither is observable. See DRAFT-P-2: the record carries one Z.1 commit and a 4 h 12 min gap, and nothing finer. |

A pointer note, below the level of a finding: `REGISTRATION.md:8-9` requires "a numbered amendment
in **Section 17**", but the anchored document places Amendments at Section 16
(`REGISTRATION.md:798`) and Closure at Section 17 (`REGISTRATION.md:804`). Lines 1-159 were written
at `fbfc74e` before Sections 1-16 existed, so the section numbers had not yet been fixed. Recorded
so that a reader chasing the amendment rule is not sent to the wrong section.

---

## 5. Live-repository access log

Purpose of access: git history and provenance only (`log`, `show`, `diff`, `rev-parse`, `grep`,
`branch`), and read-only reads of untracked/gitignored working-tree data (`ledgers/*.jsonl`,
mtimes under `reports/` and `var/`). No repository script was executed, nothing was written, `.env`
was not opened, and `var/insider_sealed.db` was not opened. Host checks for IP-09 (`systemctl`,
`crontab -l`, `ls ~/.config/systemd/user`) ran outside every audited repository. The AiTrader hash
was computed from the anchored snapshot, not from the live AiTrader tree.

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` before first
access — 2026-09-04T18:21:00Z:**

```
```
(empty output, exit 0 — clean working tree)

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` after last
access — 2026-09-04T18:29:24Z:**

```
```
(empty output, exit 0 — clean working tree, unchanged)

Ignored entries present at the closing read (`git status --ignored --porcelain`): `.env`,
`.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.venv/`, `_CLOSED_DO_NOT_RUN_HERE`, `cache/`,
`ledgers/`, `var/`, and eight `__pycache__/` directories — identical to the set the LOCATE pass
recorded at 05:29–05:33 UTC. `_CLOSED_DO_NOT_RUN_HERE` is excluded via `.git/info/exclude`, is
dated 2026-09-02 (after the anchor), and is an operator marker rather than an experiment artefact.
It is not on the COMMON_RULES list of pre-existing dirt and is reported here for the record; it was
already reported in the LOCATE inventory. No other unexpected entry was seen, and this pass created
none.

Scratch work ran under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC`;
no repository script was copied or executed.
