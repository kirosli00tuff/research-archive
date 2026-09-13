# HFExperiment — provenance verification (Agent C, PROVENANCE)

Repository: HFExperiment
Anchored SHA: 82e77a021256d917c665ff6d4304c25b08f35451 (main, 2026-08-28) — this is also live `HEAD`
Document text read from SNAP/HFExperiment (line numbers identical to `git show 82e77a0:<path>`).
Git objects read from the live repository, read-only, per COMMON_RULES.
Prepared 2026-09-04 UTC. Every finding below is a claim about the anchored SHA.

## What this repository's provenance question actually is

The verdict instrument of this experiment — the forward shadow series — **never produced a single
observation**. `data/bars.db` holds 0 rows in all six tables and `data/ledger/` is empty (live,
read 2026-09-04T00:18:48Z and 00:19:03Z), the timer is `disabled`/`inactive` and absent from
`systemctl --user list-timers --all` (read 2026-09-04T00:18:43Z), and the repository closed on
2026-08-25/26. So the classic pre-registration failure — a bar moved after seeing the outcome it
judges — is **structurally impossible here** and is not what I found. The real provenance questions
are (a) was the one bar that *could* have been contaminated, the Section 0 broker outcome map,
fixed before the broker was measured, and (b) does the record's own account of itself match the
git objects and the stored ledgers. (a) verifies cleanly. (b) has six discrepancies, five of them
hygiene and one — the dating of the terminal closure — worth a line in the audit.

### The commit timeline (author dates in UTC; author and committer dates are identical on all 13)

| # | sha | UTC | what landed |
|---|---|---|---|
| 1 | `c4e9817` | 2026-08-23T22:23:16Z | **root**, no parents. REGISTRATION.md only, +49/−0. Section 0 outcome map. |
| 2 | `0a0d214` | 2026-08-23T22:42:34Z | scaffold, `docs/ACCESS.md` (broker measurement), `universe.py`, A.1 reports |
| 3 | `91a1dcb` | 2026-08-23T22:43:53Z | DECISIONS.md, progress.md, db hashes, mutation log |
| 4 | `a8f4b0d` | 2026-08-24T04:40:25Z | **`registered.py` created**, costmodel, REGISTRATION.md Sections 1–12 (+235/−0), A.2 book spreads |
| 5 | `23d9ffa` | 2026-08-24T04:40:30Z | A.2 decisions and progress |
| 6 | `6ac61d2` | 2026-08-25T00:36:21Z | bar pipeline, shadow series, verdict engine, timer; `registered.py` +22/−0 |
| 7 | `8c4c3bc` | 2026-08-25T00:36:21Z | B.1 acceptance; REGISTRATION.md +12/−1 (amendment log opened) |
| 8 | `9634157` | 2026-08-25T02:46:28Z | order intents, wired gate, spend ledger, probe |
| 9 | `b4a7a23` | 2026-08-25T02:46:28Z | C.1 refusals demonstrated |
| 10 | `669eb5c` | 2026-08-25T03:09:06Z | A.1b capability test; Section 0 verdict BLOCKED appended |
| 11 | `23b7791` | 2026-08-25T03:09:55Z | lint fix in the A.1b script (4/4) |
| 12 | `f13e1d3` | 2026-08-25T07:45:29Z | **terminal closure**, timer disarmed; REGISTRATION.md +11/−0, progress +18/−0 |
| 13 | `82e77a0` | 2026-08-28T21:14:08Z | ADR-026 correction; DECISIONS +60/−0, ACCESS.md +47/−19, progress +48/−0 |

### When data first existed (the anchor for every "before data" claim)

| data | first existed | evidence |
|---|---|---|
| Already-spent holdout (AiTrader recorded round of 2026-07-26) | **before the repository** | `HFExperiment/reports/stage_a1/db_hash_before.txt:1` records sha256 `c30d3f44…` of `AiTrader/analysis_bars.db`; AiTrader `backtest/universe.py` last changed at AiTrader `d6ad37a`, 2026-07-26T20:58:28−07:00 |
| Broker documentation measurement | 2026-08-23T22:42:34Z | `docs/ACCESS.md` first appears at `0a0d214` — **19 min 18 s after** the root commit |
| A.1 formation reproduction | 2026-08-23T22:42:34Z | `reports/stage_a1/formations.json`, `reproduce_log.txt` at `0a0d214` |
| A.2 spread measurement | **2026-08-24T04:23:29Z** | `reports/stage_a2/book_spreads.json:2` `"measured_utc": "2026-08-24T04:23:29Z"` — 16 min 56 s before its commit `a8f4b0d` |
| C.1 demonstration + read-only probe | 2026-08-25T02:40:23Z / 02:40:30Z | `reports/stage_c1/demo_ledger.jsonl` `run_utc`; `refusals.md:331` `server_time_epoch 1787625630` = 2026-08-25T02:40:30Z |
| A.1b broker behaviour measurement | 2026-08-25T03:05:15.955Z → 03:07:17.172Z | `reports/stage_a1b/evidence.jsonl`, 51 records, min/max `utc` — 1 min 49 s before its commit `669eb5c` |
| **Shadow-series observations** | **never** | `data/bars.db` 0 rows in `bars`, `sessions`, `assets`, `universe`, `formations`, `fetch_log`; `data/ledger/` empty (live, UNANCHORED, read 2026-09-04T00:18:48Z / 00:19:03Z) |

---

## 1. Registration claims table

`—` in "commit named" means the document names no commit; the commit column then gives the commit
`git log --follow` / `git log -S` identifies as introducing the claim or the figure it concerns.

| # | claim (abridged; verbatim in the JSON) | file:line | commit named | commit found (UTC) | data first existed | status |
|---|---|---|---|---|---|---|
| P1 | "Registered 2026-08-23, before any broker measurement was taken." | REGISTRATION.md:8-10 | — | `c4e9817` 2026-08-23T22:23:16Z | broker measurement 2026-08-23T22:42:34Z | **SUPPORTED** |
| P2 | "REGISTRATION.md Section 0 committed at c4e9817 before any broker measurement." | progress.md:192-193 | **c4e9817** | `c4e9817` exists, **root**, +49/−0, REGISTRATION.md only | as P1 | **SUPPORTED** |
| P3 | "Amendments append. Nothing edits in place." | REGISTRATION.md:4 | — | — | — | **SUPPORTED** (one line deleted ever, in the amendment-log preamble) |
| P4 | "Sections 1 through 12 registered 2026-08-23." | REGISTRATION.md:58 | — | `a8f4b0d` 2026-08-24T04:40:25Z (= 2026-08-23 21:40 local) | A.2 spreads 04:23:29Z, same session | **SUPPORTED** (local-date convention) |
| P5 | "Width 5 is the PRIMARY width … chosen now, before any forward data exists, on the already-spent holdout" | REGISTRATION.md:92-95 | — | `a8f4b0d` | forward data: **never** | **SUPPORTED** |
| P6 | "The shadow series starts at the registration date and is never backfilled before it" | REGISTRATION.md:71-72 | — | `a8f4b0d`; `SHADOW_SERIES_START` at `6ac61d2` | no rows ever | **SUPPORTED** (vacuously; gate present at registered.py:97) |
| P7 | "rho … frozen at 0.071641" | REGISTRATION.md:248 | — | `a8f4b0d` (doc + `cost_table.md:40`); `RHO_FROZEN` at `6ac61d2` | never re-tuned: registered.py has zero deletions | **SUPPORTED** |
| P8 | "Amendments are dated, numbered, appended, and each records what data existed" | REGISTRATION.md:271-274 | — | log opened `8c4c3bc` | — | **PARTIAL** — all three entries state the data extant; none is *numbered*; one is misdated (P10/DRAFT-P-1) |
| P9 | "zero shadow observations, because the series has not started" (acceptance) | REGISTRATION.md:290-295 | — | `8c4c3bc` 2026-08-25T00:36:21Z | 0 rows | **SUPPORTED** |
| P10 | "zero shadow observations, because the series never started" (closure) | REGISTRATION.md:313-315 | — | `f13e1d3` 2026-08-25T07:45:29Z | 0 rows; timer disabled/inactive/unscheduled | **PARTIAL** — the substance verifies; the entry's own date (2026-08-26) does not — **DRAFT-P-1** |
| P11 | "copied verbatim from the recorded round" / "COPIED 2026-08-23 from AiTrader backtest/universe.py … Do not edit the logic" | REGISTRATION.md:78-79; universe.py:1-6 | — | `0a0d214` | AiTrader source frozen since 2026-07-26 (`d6ad37a`) | **SUPPORTED** — diff of the 330 lines after the 6-line header vs AiTrader is **one import line** (`from collections.abc import Iterable, Sequence` vs `from typing import …`); logic byte-identical |
| P12 | "the 12-1 ranking is implemented from its registered description" | DECISIONS.md:99-101 | — | `91a1dcb` | — | **SUPPORTED**, and self-disclosed at DECISIONS.md:106-110 |
| P13 | "Database hash unchanged: c30d3f4486e975a0 before and after." | progress.md:211-212 | — | `91a1dcb` | A.1 read 2026-08-23 | **SUPPORTED** — `db_hash_before.txt` and `db_hash_after.txt` are byte-identical, both `c30d3f4486e975a0ebd9c9e2f2f53c27ebe27463e44600d9a30815615abfdf51` |
| P14 | "Numbered ADRs, append-only." | DECISIONS.md:3 | — | `91a1dcb` | — | **SUPPORTED** for append-only: `91a1dcb` +114/−0, `23d9ffa` +104/−0, `8c4c3bc` +86/−0, `b4a7a23` +85/−0, `669eb5c` +30/−0, `82e77a0` +60/−0 — **zero deletions in the file's whole history**. Note ADR-022 → ADR-026; ADR-023/024/025 appear nowhere in the tree. |
| P15 | "Neither document was amended, so the repository advertised a blocker that no longer existed…" | DECISIONS.md:441-443 | **82e77a0** | `82e77a0` 2026-08-28T21:14:08Z | A.1b 2026-08-25T03:05Z | **SUPPORTED** — `docs/ACCESS.md` untouched between `0a0d214` and `82e77a0`; ADR-003 untouched between `91a1dcb` and `82e77a0` |
| P16 | "ADR-003 keeps its original text with a superseded note beneath it. Nothing is rewritten to look as though it was always right." | DECISIONS.md:452-454 | **82e77a0** | `82e77a0`, DECISIONS.md **+60/−0**, hunks `@@ -44,6 +44,16 @@` (the ADR-003 blockquote at :47-55) and `@@ -417,3 +427,53 @@` (ADR-026) | — | **PARTIAL** — true of DECISIONS.md; in the same commit `docs/ACCESS.md` **deletes** the Task 3 closing paragraph containing the repository's own falsified prediction — **DRAFT-P-4** |
| P17 | "The act of running the B.1 stage prompt was the acceptance" | DECISIONS.md:230-235 | — | `8c4c3bc` | — | **UNVERIFIABLE** — the only record is the same session's own amendment entry (REGISTRATION.md:286-295) and this commit; no operator-authored artifact exists in or beside the repository |
| P18 | "The operator holds a funded live IBKR account … (operator statement, 2026-08-28, consistent with the A.1b session log)" | docs/ACCESS.md:187-189 | **82e77a0** | `82e77a0` | A.1b ledger 2026-08-25 | **PARTIAL** — the account id verifies (`evidence.jsonl:2` `managed:["[paper account ID removed]"]`); "funded live account" is an operator statement, disclosed as such, with no artifact; the surrounding restatement is contradicted on two figures — **DRAFT-P-2, DRAFT-P-3** |
| P19 | "the structural guard test fails if any lacks an enforcement site" | REGISTRATION.md:59-61 | — | `a8f4b0d` (guard extended 22/−5 in the same commit) | — | **SUPPORTED** — `tests/test_structural_guard.py:39-46` enumerates `fields(RegisteredThresholds)`; I confirmed all 10 fields have ≥1 consumption site outside `registered.py` (min 1: `traded_width` at `scripts/cost_table_a2.py:83`, `secondary_alpha_one_sided` at `src/hfexperiment/verdict.py:115`). Scope note: the guard covers dataclass fields only, so `RHO_FROZEN`, `SHADOW_SERIES_START`, the four `PROJECTION_*` constants, `CHURN_NAMES_PER_MONTH` and the 0.15 prior are outside it. |
| P20 | "Demo constants … labelled DEMO everywhere, resolving nothing registered." | DECISIONS.md:392-394 | — | `b4a7a23` | — | **SUPPORTED** — `registered.py:110-127` still holds all three as `DeferredParameter`; Amendment 1 never landed |
| P21 | "Append-only. One dated entry per stage, newest at top." | progress.md:3 | — | `91a1dcb` | — | **NOT_SUPPORTED** for "newest at top" — the newest entry (2026-08-28T22:10Z) is the **last** in the file at progress.md:226 — **DRAFT-P-5** |
| P22 | "Installed to ~/.config/systemd/user/ by scripts/install_timer.sh." | systemd/hfexperiment-bars.timer:4 | — | `6ac61d2` | — | **NOT_SUPPORTED** — `git log --all -- 'scripts/install_timer.sh'` is empty; no `.sh` file has ever been tracked on any ref — **DRAFT-P-6** |

### Quoted commit evidence for the named-commit claims

**P2 — `git show c4e9817 --stat`:**

```
commit c4e98177334d31758c4c3796a216de6d620f6e89
Author: kirosli00tuff <[private email removed]>
Date:   Sun Aug 23 15:23:16 2026 -0700
    docs: register broker outcome map before any measurement
 REGISTRATION.md | 49 +++++++++++++++++++++++++++++++++++++++++++++++++
 1 file changed, 49 insertions(+)
```

`git rev-list --parents -n1 c4e9817` returns the sha alone — no parents, so this is the root
commit and nothing preceded it. `git show c4e9817:REGISTRATION.md` lines 6-45 carry the whole
outcome map, including the bar that decided the experiment:

```
 6  ## Section 0: Broker outcome map
 8  Registered 2026-08-23, before any broker measurement was taken. The three outcomes
 9  below are fixed now so the broker answer cannot be read against a bar its own
10  measurement could see.
12  ### GO
14  A broker accepts a Canadian resident individual account, serves US equities,
15  exposes an API that places orders and reads fills programmatically, and accepts
16  fractional quantities through that API at 45 USD per name.
33  ### BLOCKED
35  No reachable broker clears the bars.
37  Consequence: phases C and D stop. Phase B proceeds unchanged, because the shadow
38  series needs no broker, no account, and no money.
```

`diff <(git show c4e9817:REGISTRATION.md) <(git show 82e77a0:REGISTRATION.md | head -49)` differs
only at lines 47 and 49, where the amendment-log stub was later displaced by Section 1: **lines
1-46, the entire outcome map, are byte-identical at the root commit and at the anchor.** The bar
that fired BLOCKED on 2026-08-25 is textually the bar written on 2026-08-23, 19 minutes before
`docs/ACCESS.md` existed.

**P16 — `git show 82e77a0 -- DECISIONS.md`** is `+60/−0` across two hunks, so nothing in
DECISIONS.md was replaced. The ADR-003 note is an inserted blockquote:

```
47  > **Superseded 2026-08-28, see ADR-026.** The two sentences above about
48  > the operator holding no IBKR account and every sub-test being
55  > left standing rather than rewritten so the sequence stays legible.
```

ADR-003's original lines 33-45 are unchanged from `91a1dcb`.

---

## 2. Parameter changes after data existed

**There are none.** No registered bar, parameter, outcome map, prior or decision rule in this
repository was ever edited after it was committed. The evidence is a complete deletion census over
all 13 commits — `git log --numstat` filtered to entries with a non-zero deletion count returns
exactly four rows in the entire history:

```
a8f4b0d  22   5  tests/test_structural_guard.py     (guard extended to RegisteredThresholds)
8c4c3bc  12   1  REGISTRATION.md                    ("Append-only. No entries yet." -> "Append-only.")
23b7791   4   4  scripts/a1b_capability_test.py     (lint: variable names)
82e77a0  47  19  docs/ACCESS.md                     (ADR-026 correction; see DRAFT-P-4)
```

`src/hfexperiment/registered.py`, which is where every registered number lives, appears in exactly
two commits, `a8f4b0d` (+111/−0, created) and `6ac61d2` (+22/−0, appended), **both pure
additions**. `REGISTRATION.md` Sections 0-12 have never had a line removed or altered.

| parameter / bar / rule | value at anchor | first committed | changed after? | data extant at introduction | amendment | status |
|---|---|---|---|---|---|---|
| Section 0 outcome map (GO / DEGRADED / BLOCKED) | REGISTRATION.md:12-39 | `c4e9817` 2026-08-23T22:23:16Z | **no** — lines 1-46 byte-identical at HEAD | none of the broker measurement (started 19 min later) | n/a | SUPPORTED |
| `restart_floor_usd` | 500.0 | `a8f4b0d` registered.py:56 | no | holdout only, disclosed | n/a | SUPPORTED |
| `spend_cap_usd_per_year` | 100.0 | `a8f4b0d` registered.py:59 | no | holdout + A.2 costs, disclosed | n/a | SUPPORTED |
| `primary_width` / `traded_width` / `secondary_widths` | 5 / 20 / (20,50) | `a8f4b0d` registered.py:62-64 | no | already-spent holdout — **explicitly disclosed** at REGISTRATION.md:92-95 | n/a | SUPPORTED |
| `alpha_one_sided` / `secondary_alpha_one_sided` | 0.05 / 0.025 | `a8f4b0d` registered.py:67-68 | no | none forward | n/a | SUPPORTED |
| `crossing_target_days` | 1600 | `a8f4b0d` registered.py:69 | no | none forward | n/a | SUPPORTED |
| `futility_bp_per_day` | 10.0 | `a8f4b0d` registered.py:70 | no | none forward | n/a | SUPPORTED |
| `cost_hurdle_bp_per_day` | 4.07 | `a8f4b0d` registered.py:78 | no | **A.2 spreads, measured 04:23:29Z, 16 m 56 s earlier, in the same commit** — disclosed at registered.py:71-78 and REGISTRATION.md:249 as "the measured cost hurdle" | n/a | SUPPORTED (a cost bar derived from a cost measurement, labelled as such) |
| `CHURN_NAMES_PER_MONTH` | {5: 2.0, 20: 5.2} | `a8f4b0d` registered.py:85 | no | A.1 Task 4, `0a0d214`, disclosed at registered.py:83 | n/a | SUPPORTED |
| `RHO_FROZEN` | 0.071641 | doc `a8f4b0d` REGISTRATION.md:248; code `6ac61d2` registered.py:91 | no | no forward data | n/a | SUPPORTED |
| `SHADOW_SERIES_START` | "2026-09-01" | `6ac61d2` registered.py:97, and the acceptance amendment `8c4c3bc` REGISTRATION.md:288-289 | no | 0 shadow rows then and now | acceptance entry, 2026-08-24 | SUPPORTED |
| `PROJECTION_MEAN_BP` / `_SIGMA_BP` / `_CLEAR_ZERO_DAY` / `_CLEAR_HURDLE_DAY` | 27.99 / 418.0 / 2061 / 2852 | doc `a8f4b0d` REGISTRATION.md:256-262 + `reports/stage_a2/cost_table.md:40`; code `6ac61d2` registered.py:104-107 | no | holdout figures, sourced from the stage prompt (`scripts/cost_table_a2.py:32`: "prompt: excess 27.99 bp/day, tracking error 66.4 pct/yr = 418 bp/day") | n/a | SUPPORTED as to fixity; source is external — see §4 |
| Registered prior | 0.15 | `a8f4b0d` REGISTRATION.md:277 | no; reaffirmed at acceptance, REGISTRATION.md:288-289 | none forward | acceptance entry, 2026-08-24 | SUPPORTED |
| Deferred parameters (per-name notional, broker min notional, mixed-order billing) | still `DeferredParameter` | `a8f4b0d` registered.py:110-127 | no | — | **Amendment 1 never landed** — correctly, since no live order was ever placed | SUPPORTED |
| Inherited cost band / UNMEASURED carry | (15.8, 50.0), carry 50.0 | `a8f4b0d` `costmodel.py` | no | A.2 | n/a | SUPPORTED |

**Amendment log completeness.** Three entries exist, all appended, each stating the data extant:
acceptance (REGISTRATION.md:286-295, `8c4c3bc`), Section 0 verdict (`:297-304`, `669eb5c`), closure
(`:306-315`, `f13e1d3`). Each is dated; none is numbered, though REGISTRATION.md:271 says
amendments are "dated, numbered, appended". The verdict entry states "**No parameter changes**"
(`:304`) and the git objects confirm it exactly.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the terminal closure record — REGISTRATION.md amendment log and progress.md
- **Direction:** A
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Experiment closed by operator decision, instruction dated 2026-08-26." — HFExperiment/REGISTRATION.md:308 (identically at HFExperiment/progress.md:7-8: "Closed. Experiment closed by operator decision, instruction dated / 2026-08-26.")
- **Evidence:** Both sentences, and both headings "### 2026-08-26: Closure" (REGISTRATION.md:306) and "## 2026-08-26: Closure" (progress.md:5), were introduced by exactly one commit, `f13e1d3` (`git log -S"2026-08-26: Closure" -- progress.md` and `git show f13e1d3 -- REGISTRATION.md`, both returning only `f13e1d3`). `f13e1d3`'s author date **and** committer date are both **2026-08-25T07:45:29Z** (`TZ=UTC git log --date=iso-strict-local`), i.e. 2026-08-25T00:45:29−07:00 local. The record of an instruction dated 2026-08-26 therefore exists in the object store roughly 16 hours before the earliest instant of 2026-08-26 UTC, and no timezone on earth (max UTC+14) places that commit on 2026-08-26. The repository's other amendment entries are dated consistently with their commits under one convention or the other — acceptance "2026-08-24" / `8c4c3bc` 2026-08-25T00:36:21Z (local date), verdict "2026-08-25" / `669eb5c` 2026-08-25T03:09:06Z (UTC date) — so the closure entry is the only one matching neither. `git grep -n "2026-08-26" 82e77a0` returns only these four closure lines plus an unrelated fixture at tests/test_spendledger.py:42; no operator artifact bearing that date exists in the tree. The later commit `82e77a0` (2026-08-28T21:14:08Z), a record-hygiene commit made with the operator present (DECISIONS.md:445-448), did not correct it, so the discrepancy stands at the anchor.
- **Recomputation (if any):** none required; date arithmetic only. `f13e1d3` = 2026-08-25T07:45:29Z; stated instruction date 2026-08-26; difference ≥ 16 h 14 m in the wrong direction.
- **What would resolve it:** an operator-authored artifact dated 2026-08-26 (a message, a note, a signed instruction) that the closure entry records, or a corrected amendment stating the true instruction date and why the entry was written a day early. Note that the substance of the closure verifies independently — the timer is disabled and inactive, and no shadow row ever existed — so only the *dating* is in question.
- **Confidence:** HIGH — the commit's author and committer dates agree and the introducing commit is unambiguous.
- **Invalidated by later commits?:** no — `82e77a0` is the anchor and the live HEAD, and it left the text unchanged. A future commit could add a correcting amendment.
- **Disclosed by authors?:** no — nothing in REGISTRATION.md, progress.md or DECISIONS.md mentions the gap between the entry's date and the commit that carries it.

### DRAFT-P-2
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the A.1b broker-capability measurement record (Section 0 verdict evidence)
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A.1b resolved it by behaviour on 2026-08-25, paper / account [paper account ID removed], Gateway server version 187." — HFExperiment/DECISIONS.md:407-408 (ADR-022); repeated at HFExperiment/reports/stage_a1b/a1b_report.md:4, HFExperiment/DECISIONS.md:439, HFExperiment/progress.md:235 and HFExperiment/docs/ACCESS.md:178
- **Evidence:** The only machine-written record of the A.1b session is `reports/stage_a1b/evidence.jsonl` (51 records, n=1 `connected` record). Its line 2 reads verbatim: `{"kind":"connected","managed":["[paper account ID removed]"],"server_version":178,"utc":"2026-08-25T03:05:16.497779Z"}` — **178, not 187**. ADR-022 introduces the 187 figure in the sentence immediately before it says "Observed, verbatim in reports/stage_a1b/evidence.jsonl" (DECISIONS.md:410). The value in the ledger is machine-captured: `scripts/a1b_capability_test.py:158` writes `server_version=self.ib.client.serverVersion()`, and that script writes only the `.jsonl`; the `.md` report is hand-written prose. The figure 187 does exist in this repository, but in a *different* session — `reports/stage_c1/refusals.md:332` `"server_version": 187` from the C.1 read-only probe whose `server_time_epoch` 1787625630 decodes to 2026-08-25T02:40:30Z, 25 minutes earlier and committed in `b4a7a23`, one commit before A.1b. So the prose figure matches the earlier probe, not the session it is attributed to. The `82e77a0` correction commit propagated 187 into two further documents without checking it against the ledger it cites.
- **Recomputation (if any):** `reports/stage_a1b/evidence.jsonl`, all 51 records parsed 2026-09-04T00:1xZ from SNAP: exactly one `connected` record; `server_version` = 178; no record anywhere in the file contains 187.
- **What would resolve it:** the raw session log showing the Gateway's reported API server version at 03:05:16Z, or an amendment correcting the four documents to 178 (or explaining a second connection at a different version). Note the substantive A.1b verdict is fully corroborated by the same ledger — 3 × error 10243 on decimal quantities (MU MKT, MU LMT, TE MKT), 1 × error 10244 on cashQty, whole-share control `PreSubmitted` — so nothing about BLOCKED depends on this figure.
- **Confidence:** HIGH — a single machine-written field contradicts the prose in four places; the alternative source of 187 is identified.
- **Invalidated by later commits?:** no — `82e77a0` re-propagated the figure rather than correcting it, and it is the anchor.
- **Disclosed by authors?:** no. Overlaps inventory claim C6 ("Gateway server version, prose vs ledger"), which is flagged MUST-VERIFY in HFExperiment.inventory.md:136-141; the parent should deduplicate.

### DRAFT-P-3
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the ADR-026 correction note in docs/ACCESS.md Task 3
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Stage A.1b connected on **2026-08-25, 02:57 to / 03:07 UTC, to Gateway 127.0.0.1:4002, server version 187, account / [paper account ID removed], declared mode paper**, and settled four of the six sub-tests by / behaviour (`reports/stage_a1b/a1b_report.md`)." — HFExperiment/docs/ACCESS.md:177-180
- **Evidence:** Two components of this sentence are contradicted by the artifacts it cites. (i) **Window.** `reports/stage_a1b/evidence.jsonl` spans `2026-08-25T03:05:15.955248Z` (`stage_start`) to `2026-08-25T03:07:17.172526Z` (`final_positions`), n=51 records; the sole `connected` record is at `03:05:16.497779Z`. The claimed connection window 02:57–03:07 UTC is ten minutes; the ledger's is two minutes and one second, and no record precedes 03:05:15.955Z. (ii) **Count.** `git show 82e77a0 -- docs/ACCESS.md` shows the original table's six rows deleted and a **seven**-row table added; the added seventh row is `| whole-share control order | **RESOLVED — ACCEPTED** | …`, which was not among the six sub-tests the same paragraph refers to and which ADR-026 itself lists separately as part of "four RESOLVED, two MOOT, one RUNNABLE" (DECISIONS.md:451-452 — 4+2+1 = 7). Of the *original six* rows, three are RESOLVED (decimal totalQuantity, cashQty, MinSize/SizeIncrement), two MOOT and one RUNNABLE. "Four of the six" counts a row created by the correction itself among the six it corrects.
- **Recomputation (if any):** min/max of the 51 `utc` fields in `reports/stage_a1b/evidence.jsonl`, parsed 2026-09-04 from SNAP: 03:05:15.955248Z / 03:07:17.172526Z, span 121.2 s. Row census from the `82e77a0` diff: 6 removed, 7 added, statuses 4 RESOLVED / 2 MOOT / 1 RUNNABLE.
- **What would resolve it:** the session wall-clock log covering 02:57–03:05:15Z (setup or a first connection attempt would explain the window), and either a re-count to "three of the six, plus a control the correction adds" or a note that the table gained a row.
- **Confidence:** HIGH for the count (arithmetic on the commit's own diff); MEDIUM for the window (a stage may have begun before its ledger's first write, though "connected on … 02:57 to 03:07 UTC" is specifically a connection claim).
- **Invalidated by later commits?:** no — `82e77a0` is the anchor.
- **Disclosed by authors?:** partly — ADR-026's own status breakdown sums to seven, which discloses that the table grew, but no document reconciles that with "four of the six".

### DRAFT-P-4
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the ADR-026 record-hygiene correction, commit 82e77a0
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Decided. ACCESS.md Task 3 is re-headed SUPERSEDED, the false sentence is / struck rather than deleted, and the sub-test table is re-statused against / the A.1b evidence: four RESOLVED, two MOOT, one RUNNABLE. ADR-003 keeps / its original text with a superseded note beneath it. Nothing is rewritten / to look as though it was always right." — HFExperiment/DECISIONS.md:450-454
- **Evidence:** `git show 82e77a0 -- docs/ACCESS.md` is `+47/−19`. The struck sentence is genuinely struck (docs/ACCESS.md:184-187, `~~…~~`), and ADR-003 is genuinely additive (DECISIONS.md +60/−0). But the same diff **deletes without trace** the paragraph that closed Task 3, which contained the repository's own prediction — the one A.1b falsified:

  ```
  -The documentation conflict stands unresolved on purpose: IBKR staff wrote
  -in June 2026 that the API does not support cash-quantity orders outside
  -crypto, a third-party guide from March 2026 claims the opposite, and an
  -Elite Trader thread reports cashQty rounding down to whole shares through
  -the Web API. The likely resolution is that cashQty is unsupported while
  -decimal share quantities work, which the quote-first-divide-then-submit
  -path handles. Likely is not measured. The verdict waits for the test.
  ```

  It was replaced by a rewritten paragraph in resolved-past tense ("The documentation conflict, for the record, is now resolved rather than open …"). `grep -rn "quote-first-divide-then-submit\|Likely is not measured\|verdict waits for the test\|stands unresolved on purpose"` over the whole anchored tree returns **nothing**: the falsified prediction survives only in the git object store. The asymmetry is the point — the merely *stale* sentence about account access is preserved struck, while the *wrong* forecast ("decimal share quantities work", refuted by three error-10243 refusals) is removed. ADR-026's own enumeration of what it changed does not mention this deletion.
- **Recomputation (if any):** n/a — diff and grep only.
- **What would resolve it:** restoring the deleted paragraph struck through, as the adjacent sentence was, or an amendment noting that Task 3's closing paragraph was replaced and why.
- **Confidence:** MEDIUM — the deletion is certain; whether it amounts to "rewritten to look as though it was always right" is a judgement, and the replacement text does date the resolution honestly to 2026-08-25.
- **Invalidated by later commits?:** no — `82e77a0` is the anchor and the live HEAD.
- **Disclosed by authors?:** partly — ADR-026 discloses that the table was "re-statused", but no document records that a paragraph containing a falsified prediction was deleted rather than struck.

### DRAFT-P-5
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** progress.md's stated ordering and dating discipline
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Append-only. One dated entry per stage, newest at top." — HFExperiment/progress.md:3
- **Evidence:** Two defects, both in the single entry added by `82e77a0`. (i) **Ordering.** The file's headings run 2026-08-26 (`:5`), 2026-08-25 (`:23`), 2026-08-25 (`:56`), 2026-08-24 (`:102`), 2026-08-23 (`:152`), 2026-08-23 (`:187`) — correctly descending — and then "## 2026-08-28T22:10Z — ADR-026: the stale no-account blocker, corrected" at `:226`, the newest entry, at the **bottom**. (ii) **Timestamp.** That heading's stated time, 2026-08-28T22:10Z, is **56 minutes after** the author and committer date of the only commit that contains it, `82e77a0` = 2026-08-28T21:14:08Z, so the entry claims to have been written after the commit that carries it.
- **Recomputation (if any):** `git log -S"ADR-026" -- progress.md` returns `82e77a0` alone; 22:10Z − 21:14:08Z = +55 m 52 s.
- **What would resolve it:** moving the entry to the top, or a note that ADR-026 is not a stage and is appended deliberately; and a corrected timestamp.
- **Confidence:** HIGH — both are direct reads of the file and the commit object.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — progress.md:228 calls the entry "Not a stage", which explains why it is not a stage entry but not why it sits below older entries under a "newest at top" rule, and says nothing about the timestamp.

### DRAFT-P-6
- **Repository / SHA:** HFExperiment / 82e77a021256d917c665ff6d4304c25b08f35451
- **Hypothesis or artifact:** the shadow-series systemd timer unit
- **Direction:** neutral
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "# Installed to ~/.config/systemd/user/ by scripts/install_timer.sh." — HFExperiment/systemd/hfexperiment-bars.timer:4
- **Evidence:** `git ls-tree -r --name-only 82e77a0 -- scripts/` returns eight files, all `.py`: `a1b_capability_test.py`, `cost_table.py`, `cost_table_a2.py`, `daily_run.py`, `demo_c1.py`, `fetch_c1_formation.py`, `measure_book_spreads.py`, `reproduce_formation.py`. `git log --all --oneline -- 'scripts/install_timer.sh' '*install_timer*'` returns nothing, and a scan of every added file across all refs (`git log --all --diff-filter=A --name-only`) finds **no `.sh` file has ever been tracked in this repository**. The named installer therefore never existed at any commit, so the units were installed by some untracked means; the installation itself is real (the inventory records the installed units byte-identical to the tracked copies) and the timer is now disabled, inactive and unscheduled (live `systemctl --user`, read 2026-09-04T00:18:43Z).
- **Recomputation (if any):** n/a.
- **What would resolve it:** committing the installer, or amending the comment to describe how the units were actually installed.
- **Confidence:** HIGH — exhaustive over all refs.
- **Invalidated by later commits?:** no — `82e77a0` is HEAD; a later commit could add the script, which would not change its absence at the anchor.
- **Disclosed by authors?:** no.

---

## 4. What could not be checked and why

1. **Whether the broker measurement was *performed* before 2026-08-23T22:23:16Z.** Git proves only
   that the *artifact* (`docs/ACCESS.md`) was committed 19 min 18 s after the outcome map. ACCESS.md
   is documentation research with no capture timestamps; a reading done earlier and written up later
   is not excluded by any object in the repository. What *is* excluded is the contaminating case
   that matters — the deciding bar was fractional-through-the-API at 45 USD, which was measured only
   on 2026-08-25 by A.1b, two days and eleven commits after the bar was fixed, and the bar's text is
   byte-identical across that span. Status for P1/P2: SUPPORTED, with this scope stated.

2. **The provenance of 27.99 bp/day, 418 bp/day and IR 1.062.** These drive Section 1's hypothesis,
   the primary-width choice and the whole projection (day 2061, day 2852), and **no artifact in this
   repository stores them**. REGISTRATION.md:115 labels the row "recorded"; the only in-repo pointer
   to their origin is a code comment, `scripts/cost_table_a2.py:32`: "prompt: excess 27.99 bp/day,
   tracking error 66.4 pct/yr = 418 bp/day" — i.e. they were handed to the session in the stage
   prompt. Verifying them requires the AiTrader recorded round and is inventory claim C3's job, not
   a provenance question. Recorded here as an external-figure dependency, not as a finding.

3. **P17, acceptance by delegation.** UNVERIFIABLE by construction: the acceptance is an act
   ("running the B.1 stage prompt"), and the only records are the same session's own amendment entry
   and commit `8c4c3bc`. There is no operator-authored artifact anywhere in or beside the repository.
   The authors state this plainly (DECISIONS.md:230-235), so it is disclosed, not concealed.

4. **P18's "funded live IBKR account".** The paper account id `[paper account ID removed]` verifies against
   `evidence.jsonl`. "Funded" and "live" rest on an operator statement of 2026-08-28, labelled as
   such in the document. No artifact could confirm it and none should — reading a broker statement
   is out of scope and would touch credentials.

5. **The ADR numbering gap.** ADR-022 is followed by ADR-026; `grep -rn "ADR-023\|ADR-024\|ADR-025"`
   over the whole anchored tree returns nothing, and DECISIONS.md has zero deletions in its history,
   so nothing was removed. Whether three ADRs were drafted and never committed, or the numbering
   simply skipped, is not determinable from the git objects. Not raised as a finding: no claim in
   the repository asserts contiguous numbering.

6. **Live untracked data is UNANCHORED.** `data/bars.db`, `data/c1_formation.db` and `data/ledger/`
   were read from the live working tree at 2026-09-04T00:18:48Z and 00:19:03Z with
   `file:…?immutable=1` (no `-wal`/`-shm` sidecar can be created). They may change after that read,
   though the repository carries a `_CLOSED_DO_NOT_RUN_HERE` marker and the timer is disarmed.

7. **Cross-repository check performed and passed.** P11 required reading AiTrader, which
   COMMON_RULES permits read-only. `AiTrader/backtest/universe.py` (330 lines) versus
   `HFExperiment/src/hfexperiment/universe.py` minus its 6-line COPIED header differs by exactly one
   line — `from collections.abc import Iterable, Sequence` where AiTrader has
   `from typing import Iterable, Sequence` — a typing-import modernisation, no logic change.
   AiTrader's file has not changed since `d6ad37a`, 2026-07-26T20:58:28−07:00, i.e. the version that
   ran the recorded round is the version that was copied. AiTrader was touched with `git -C … log`,
   `git show` and `git status --porcelain` only; its status showed the pre-existing ` M COLLECTION_LOG.md`
   that COMMON_RULES records as owner dirt, before and after.

---

## 5. Live-repo access log

No file under `/home/kiros-li/Documents/GitHub/HFExperiment/` was opened for writing. No repository
script was executed. `.env` was not read. SQLite reads used `file:…?immutable=1`. All scratch output
went to `/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC-prov-HF/`.

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — BEFORE first access, 2026-09-04T00:11:16Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

**`git -C /home/kiros-li/Documents/GitHub/HFExperiment status --porcelain` — AFTER last access, 2026-09-04T00:26:52Z:**

```
?? Accept:
?? GET
?? Host:
?? User-Agent:
```

Identical, and exactly the four stray files COMMON_RULES records as pre-existing owner dirt.
Nothing else appeared. No accidental modification occurred.

Secondary repository (P11 only): `git -C /home/kiros-li/Documents/GitHub/AiTrader status --porcelain`
returned ` M COLLECTION_LOG.md` — the pre-existing collector dirt COMMON_RULES names — both before
the P11 reads and again at 2026-09-04T00:26:52Z, unchanged by them.

| time (UTC) | command | purpose |
|---|---|---|
| 00:11:16 | `git status --porcelain` | pre-access baseline |
| 00:11:2x | `git log --format=… --date=iso-strict --reverse`, `git log --numstat --reverse` | timeline, deletion census |
| 00:12:xx | `git rev-list --parents -n1 c4e9817`, `git show --stat c4e9817`, `git show c4e9817:REGISTRATION.md` | P1, P2 |
| 00:12:xx | `git log --follow -p -- REGISTRATION.md`, `git show 8c4c3bc/669eb5c/f13e1d3 -- REGISTRATION.md` | P3, P4, P8, P9, P10, DRAFT-P-1 |
| 00:13:xx | `diff <(git show c4e9817:REGISTRATION.md) <(git show 82e77a0:REGISTRATION.md \| head -49)` | Section 0 fixity |
| 00:13:xx | `git show 6ac61d2 -- src/hfexperiment/registered.py`, `git show 82e77a0 -- DECISIONS.md`, `git show 82e77a0 -- docs/ACCESS.md` | parameter table, P14, P16, DRAFT-P-4 |
| 00:14:xx | `git log -S"<figure>"` for 4.07, 27.99, 1.062, 0.071641, 0.15, 418.0, 2061, 2852, 1600, 0.025, 500.0, 100.0, 5.2, 15.8, 28.76, 56.84, 1.41, 1.75 | first-introduction dates |
| 00:15:xx | `git log --all -- 'scripts/install_timer.sh'`, `git log --all --diff-filter=A --name-only`, `git ls-tree -r --name-only 82e77a0 -- scripts/` | DRAFT-P-6 |
| 00:15:xx | `git grep -n` at c4e9817 / a8f4b0d / 0a0d214 / 82e77a0 | figure locations at each commit |
| 00:16:xx | `git -C AiTrader log -- backtest/universe.py`, `git show d6ad37a:backtest/universe.py`, `git -C AiTrader status --porcelain` | P11 |
| 00:18:43 | `systemctl --user is-enabled/is-active hfexperiment-bars.timer`, `list-timers --all` | P10 (system state, outside the repo, read-only) |
| 00:18:48 | sqlite `file:data/bars.db?immutable=1`, `file:data/c1_formation.db?immutable=1` — table list + `count(*)` | P5, P6, P9, P10 |
| 00:19:03 | `ls -la data/`, `ls -la data/ledger/` | shadow-series emptiness |
| 00:2x:xx | `git rev-parse HEAD`, `git branch -a`, `TZ=UTC git log --date=iso-strict-local` | anchor confirmation, UTC dates |
| 00:26:52 | `git status --porcelain` (HFExperiment and AiTrader) | post-access baseline |
