# ETFExperiment — provenance verification (Agent C, referee)

- **Repository:** ETFExperiment
- **Anchored SHA:** `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28 local / 2026-08-29T02:43:48Z)
- **Document text read from:** `SNAP/ETFExperiment/` (the anchored `git archive` export)
- **Git objects read from:** the live repository, read-only, `git log|show|diff|blame|rev-parse|cat-file|ls-tree|reflog|for-each-ref|grep`
- **Unanchored working-tree data read:** `data/ledgers/requests.jsonl` and `data/*/` listings (gitignored, live only) — read 2026-09-05T04:00Z to 04:12Z; may have changed after the anchor (its mtime is 2026-08-29T02:40:42Z, so it has not)
- **Recomputation:** `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-prov/` (copies of `src/etf/power.py` and `src/etf/config.py` from SNAP, driven by my own scripts; nothing executed inside the audited repository)
- **Generated:** 2026-09-05T04:20Z

The referee has no thesis here. Sixteen of the nineteen provenance claims verify, several of
them to the second, and that is reported as plainly as the five that do not.

---

## 0. The timeline everything is measured against

Every commit in this repository was authored on 2026-08-28 local (UTC-7). Converted to UTC:

| UTC | commit | what it did |
|---|---|---|
| 2026-08-28T07:57:16Z | `4b9c874` | repo init, governing prompt logged |
| **08:05:56Z** | `815f888` | scaffold, five standing guards, CLAUDE.md, **`src/etf/config.py` with every registered numeric parameter** |
| **08:07:59Z** | `44567f6` | **REGISTRATION.md Section 0** + `section0.py` + `observability.py` + their tests |
| 08:09:26Z | `e33b03c` | REGISTRATION.md Sections 1–12 |
| 08:11:17Z | `38b9397` | Section 13 priors, Section 14 carried figures, HYPOTHESES.md, `registration_check.py` |
| 08:11:50Z | `0c29049` | Stage A.0 close-out (progress.md) |
| **08:12:19Z** | — | **FIRST NETWORK REQUEST.** `data/ledgers/requests.jsonl` line 1: `meta.robots`, `kind":"charge"` |
| 20:04:41Z | `97da329` | A.1 Task 1 access verification committed (the probes themselves ran at 08:12Z) |
| 20:11:32Z | `0cd8572` | A.1 T3/T4 machinery; `config.py` gains three flow-source string fields |
| **20:16:31Z** | `294eab7` | **Amendment 1** |
| 20:19:50Z–20:34:47Z | — | substrate_coverage, preperiod_inputs, retro_revision, census artifacts written |
| 20:35:28Z | `66a0c81` | census admissibility rule changed (served value, not merely a capture) |
| **20:35:37Z** | — | **`reports/stage_a2/power.json` `computed_at`** |
| **20:36:13Z** | `41351a9` | **Amendment 2** — and, in the same commit, the `power_gate.py` E2-budget edit |
| 20:38:24Z | `46056f9` | DECISIONS.md, 18 ADRs |
| 20:39:00Z | `fe60a22` | README; `power.json` committed |
| 20:40:00Z | — | `e2_minimum_n.json` `computed_at` |
| **20:40:58Z** | `67f25f3` | **Amendment 3** |
| 20:41:54Z | `a881956` | six mutations, all caught, source restored green |
| 20:43:33Z–20:45:24Z | `856674d`…`ffac03d` | report.md, HYPOTHESES.md, ACCESS.md, progress.md |
| **20:45:53Z** | `cf6efaf` | **Amendment 4** — governing minimum N 237 → 300 |
| 20:46:53Z | `5192ba8` | Stage A close-out. **Ledger held exactly 220 charges at this instant.** |
| **23:39:33Z** | `3f5d629` | **Amendment 5** — H1 closed. Ledger held 228. |
| **2026-08-29T02:43:48Z** | `4d11002` | **Amendment 6** — `etf-snap` disarmed. **Ledger held 238.** |
| 2026-08-29T18:45:06Z | — | `refs/remotes/origin/master` updated by push (**after** the anchor; see P15) |

**Data first existed at 2026-08-28T08:12:19Z**, 29 seconds after the last Stage A.0 commit.
`data/` is gitignored, so its absence at `44567f6` cannot be read from the tree; the ledger's
own first row is the check, and `reports/stage_a1/robots_and_terms.json` carries the same
`requested_at` timestamps (08:12:19Z … 08:12:54Z) independently.

---

## 1. Registration claims table

Nineteen provenance claims from `findings/agentC/verification/ETFExperiment.inventory.md §4`.
Status: SUPPORTED / PARTIAL / NOT_SUPPORTED / UNVERIFIABLE.

| # | claim (file:line) | commit named | commit found & date (UTC) | data first existed | status | finding |
|---|---|---|---|---|---|---|
| P01 | Section 0 registered before any network call — REGISTRATION.md:3-8 | none in text; `44567f6` | yes, 2026-08-28T08:07:59Z | 08:12:19Z (ledger row 1) | **SUPPORTED** — gap 4 m 20 s; `git ls-tree -r 44567f6` lists no data artifact | — |
| P02 | scaffold, guards, CLAUDE.md, REGISTRATION Sections 0-14, HYPOTHESES all committed before the first request — report.md:17-21 | `815f888`, `44567f6`, `e33b03c`, `38b9397`, `0c29049` | all five exist: 08:05:56 / 08:07:59 / 08:09:26 / 08:11:17 / 08:11:50Z | 08:12:19Z | **SUPPORTED** — all five strictly before, margin 29 s on the last | — |
| P03 | `fire_section0` committed with the document; boundary fixtures exactly on 0.80 / 0.50 / 0.50 with "one-ULP steps" — REGISTRATION.md:65-70 | `44567f6` | yes, 08:07:59Z | 08:12:19Z | **PARTIAL** — co-commit and on-boundary fixtures verified (`GO_FLOOR`, `BLOCKED_FLOOR`, `unstable=0.5`); the steps are `1e-12`, not one ULP (~1.1e-16 at 0.8) | S4, §3 note |
| P04 | REGISTRATION.md is append-only; nothing above an amendment line is ever edited — CLAUDE.md:101-103 | none | six post-data commits touch it | 08:12:19Z | **SUPPORTED** — all six diffs are `+N / -0` and every hunk header is a pure end-append (`@@ -594,0 +595,102 @@` etc.) | — |
| P05 | "the request ledger (143 charged requests)" and no census/power at Amendment 1 — REGISTRATION.md:598-607 | `294eab7` | yes, 20:16:31Z | — | **PARTIAL** — census.json (20:34:47Z) and power.json (20:35:37Z) both postdate it, as claimed; but the ledger held **145** charges at the commit instant (#144 20:14:03Z, #145 20:14:06Z), not 143 | S4, §3 note |
| P06 | "No power number existed when this amendment was written" — REGISTRATION.md:700-709 | `41351a9` | yes, 20:36:13Z | — | **NOT_SUPPORTED** — `power.json` `computed_at` 20:35:37Z, 36 s earlier; and that file's E2 values reproduce **only** at the `draws=1500` budget introduced by the `power_gate.py` edit carried inside this very commit | **DRAFT-P-3** |
| P07 | No outcome value has been read — REGISTRATION.md:823-827 | `67f25f3` | yes, 20:40:58Z | — | **SUPPORTED (as far as checkable)** — `tests/test_guards.py:121` walks the parse tree for `{o,h,l,c,v,open,high,low,close,volume}` over `src/` and `scripts/` with `STAGE_B_OUTCOME_EXEMPT = ()`; `data/state/` absent; `verdict.py` imported only by its own test | — |
| P08 | "572 of 572 post-boundary rows across three pages" gated — REGISTRATION.md:604-606 | `294eab7` | yes, 20:16:31Z | — | **PARTIAL** — 572 of 572 verified exactly (venue_and_archive `funding_post_period` 72/72; depth `funding_2025_05_page` 500/500); post-boundary rows live on **two** pages, not three (five funding pages were probed in all) | S4, §3 note |
| P09 | The anchor has not moved and cannot until the A.1 Task 3 measurement exists — REGISTRATION.md:695-696, 790-793 | `294eab7`, `41351a9` | both exist | — | **SUPPORTED** — `entry_anchor_hour_utc=8` byte-identical from `815f888` (08:05:56Z, pre-data) to the anchor; `config.py` has exactly two commits and the second is 12 added lines, 0 deleted | — |
| P10 | No secret anywhere; `.env.example` empty on purpose — CLAUDE.md:113-114 | none | — | — | **PARTIAL** — no credential in any blob in history (scanned all reachable commits for `api_key`/`secret`/`token`/`bearer`/`sk-`/`AKIA`; only hits are Cloudflare beacon tokens inside a captured third-party HTML fixture); `.env.example` is a 200-byte comment block, not byte-empty | S4, §3 note |
| P11 | The Section 13 operator prior slot was never filled — REGISTRATION.md:1090-1094 | `3f5d629` | yes, 23:39:33Z | — | **SUPPORTED** — `registration_check._FILL` re-run against `REGISTRATION.md` at every one of the seven commits that touch it: label present, no match, all seven | — |
| P12 | `etf-snap` and `etf-daily` disarmed; no armed collector, no running process — REGISTRATION.md:1157-1159 | `4d11002` | yes, 2026-08-29T02:43:48Z | — | **SUPPORTED** — `systemctl --user` at 2026-09-05T04:06Z: both `disabled` + `inactive`, neither in `list-timers --all` | — |
| P13 | "The **220 charged requests** stand as the total lifetime network cost" — REGISTRATION.md:1160-1161 | `4d11002` | yes, 2026-08-29T02:43:48Z | — | **NOT_SUPPORTED** — the ledger held **238** charges at that commit; charge #238 is stamped 02:40:32Z, 3 m 16 s earlier | **DRAFT-P-5** |
| P14 | All six mutations applied to real source, each caught, source restored green — report.md:405-407 | `a881956` | yes, 20:41:54Z | — | **SUPPORTED** — `reports/stage_a4/mutations.log` at that commit reads `caught=True restored_green=True` on all six; all six anchor strings verified present in the anchored source; the earlier run's one SKIP and one `restored_green=False` are **disclosed by the authors** at report.md:417-421 | — |
| P15 | Nothing pushed; no remote exists; four pre-existing timers untouched — progress.md:520-524 | none | — | — | **SUPPORTED at the anchor** — `refs/remotes/origin/master` reflog shows a single entry, `update by push` at **2026-08-29T18:45:06Z**, ~16 h *after* the last commit and after the claim was written; no `FETCH_HEAD`, no `ORIG_HEAD`. `npl-watch` (60 min), `news-collect` (22:31Z), `npl-daily` (01:40Z) all present with the stated schedules; `solattn-daily` is not present now (see §4) | — |
| P16 | The DEGRADED expectation was stated before the census existed — REGISTRATION.md:72-86 | `44567f6` / `e33b03c` | yes, 08:07:59Z | 08:12:19Z | **SUPPORTED** — `git show 44567f6:REGISTRATION.md` is 86 lines and is **byte-identical** to lines 1-86 of the anchored file | — |
| P17 | No accrual, coverage, lag, retention, revision or capture-density figure is registered before it is measured — REGISTRATION.md:571-573 | `38b9397` | yes, 08:11:17Z (pre-data) | 08:12:19Z | **NOT_SUPPORTED in one instance** — Section 9's "rough anchors" are correctly labelled expectations (REGISTRATION.md:386-388); the archive-density, revision, coverage and pacing figures were all measured before use. The **20.8 admissible-days-per-month accrual figure** is not: it is labelled "measured", the census measured `admissible_forward_capture = 0`, and no stored artifact holds it | **DRAFT-P-4** |
| P18 | Stage B opens the sealed store exactly once behind a latch; `verdict.py` built dark, imported by nothing — REGISTRATION.md:400-408 | `e33b03c` | yes, 08:09:26Z | — | **SUPPORTED** — `data/state/` absent from the live tree at 2026-09-05T04:07Z; `grep` for `import verdict` across `src`, `scripts`, `tests` returns only `tests/test_verdict.py`, which itself asserts no Stage A module imports it | — |
| P19 | ADR-003 dated 2026-08-28, accepted, "registered as REGISTRATION.md §8", citing 81 of 333 days (24.3 %, n = 333) — DECISIONS.md:74-92 | `46056f9` | yes, 20:38:24Z | census 20:34:47Z | **PARTIAL** — the decision *is* registered at §8, committed 08:09:26Z pre-data, and §8 already carried the qualitative rationale ("a large fraction of them") without a figure; the quantified 24.3 % postdates that registration by 12 h 25 m and the ADR does not say so, though it does label the figure "measured" and carries its n | S4, §3 note |

Additional simulation-budget claims, checked because they are provenance claims about how a
registered figure was produced:

| # | claim (file:line) | status | finding |
|---|---|---|---|
| P20 | "Simulation budget stated: E1 at 20,000 permutation draws and 2,000 simulations; E2 at 1,500 draws and 400 simulations" — REGISTRATION.md:856-857 (and report.md:329-332) | **PARTIAL** — exactly right for the E1 *power* table (all six cells reproduce bit-for-bit at 20,000/2,000) and for E2 (reproduces only at 1,500/400); **wrong for the E1 minimum-N table printed 20 lines above it**, which reproduces exactly at `minimum_n`'s defaults of 4,000 draws / 600 simulations | **DRAFT-P-1** |
| P21 | "E1 minimum N at the published 0.18 \| **237** \| 1,200 draws, 300 sims/cell" — REGISTRATION.md:1011 | **NOT_SUPPORTED** — 1,200/300 is Amendment 4's *E2* grid budget (`scripts/e2_minimum.py:42`); E1's 237 came from 4,000/600 | **DRAFT-P-2** |
| P22 | `reports/stage_a2/power.json` records `"permutation_draws": 20000, "power_simulations": 2000` | **PARTIAL** — true of the E1 power cells only; the same file's E2 cells and `minimum_n_for_e1` were produced at other budgets, and the header does not say so | folded into DRAFT-P-1 |

---

## 2. Parameter changes after data existed

Data existed from 2026-08-28T08:12:19Z. Every change below is after that instant.

| # | what changed | where | commit / UTC | amendment recorded? | reference | verdict-relevant? |
|---|---|---|---|---|---|---|
| C01 | Three flow-source fields added to CONFIG (`flow_recent_url`, `flow_all_data_url`, `flow_source_name`) | `src/etf/config.py` | `0cd8572` 20:11:32Z | **yes** (5 min later) | Amendment 1 §1, REGISTRATION.md:609-618 | no (source selection) |
| C02 | Operating paces replaced: `flow.table` 30.0→10.0 s, `archive.timemap`/`availability` 10.0→2.0 s, `venue.candleSnapshot`/`fundingHistory` 5.0→2.0 s, `kraken.ohlc` 5.0→2.0 s; `PROVISIONAL_MIN_SPACING_S` renamed `MEASURED_MIN_SPACING_S` | `src/etf/pacing.py` | `294eab7` 20:16:31Z | **yes**, same commit | Amendment 1 §2, REGISTRATION.md:631-656 | no |
| C03 | The *rule* for setting paces changed: Section 12 registered "half the measured ceiling"; no ceiling was found, so the amendment substituted "twice the fastest verified-clean spacing" | `src/etf/pacing.py`, REGISTRATION.md:433 | `294eab7` 20:16:31Z | **yes**, with its reason and the NPLExperiment precedent named | REGISTRATION.md:633-639 | no |
| C04 | `meta.robots` / `meta.terms` added to the pacing map | `src/etf/pacing.py` | `97da329` 20:04:41Z | no explicit amendment line, but the endpoints appear in Amendment 1's "not measured" row treatment and in docs/ACCESS.md | REGISTRATION.md:649 | no — S4 at most |
| C05 | Admissibility rule tightened: a qualifying archive capture must *serve a value*, not merely exist; a failed fetch reclassified `excluded_ineligible` → `source_failed` (unknown) | `src/etf/census.py` | `66a0c81` 20:35:28Z | **yes** (45 s later) | Amendment 2 §1 and §5, REGISTRATION.md:711-738, 799-810 | **yes** — it moves the density from 0.1111 to 0.0330 |
| C06 | Archive capture density figure 37/333 = 0.1111 → 11/333 = 0.0330 | REGISTRATION.md | `41351a9` 20:36:13Z | **yes**, recorded as *falsified* rather than corrected in place; Amendment 1 left unedited above | REGISTRATION.md:713-738 | **yes** — GO is eliminated on it |
| C07 | **E2 power budget reduced from the registered `CONFIG.power_simulations=2000` / `permutation_draws=20000` to `draws=1500, simulations=400`** | `scripts/power_gate.py:100` | `41351a9` 20:36:13Z | **partial** — the commit that makes the change is Amendment 2, whose §6 says "Every registered bar, both co-primaries, alpha_adj, the effect assumptions … unchanged" and does not mention it; it is stated one amendment later | Amendment 3, REGISTRATION.md:856-859 | yes (E2 powers) — but **disclosed** at Amendment 3 |
| C08 | **E1 minimum-N budget: `minimum_n()` defaults to `draws=4_000, simulations=600` and `power_gate.py:105` calls it with no override, while the register states 20,000/2,000 for E1** | `src/etf/power.py:232-233` | `5fa460a` 20:27:29Z | **no amendment anywhere** | — | **yes** — 237 and 845 are the figures the closure and the reopen path are stated against | 
| C09 | Governing minimum N 237 → 300 | REGISTRATION.md, HYPOTHESES.md, report.md | `cf6efaf` 20:45:53Z | **yes** — Amendment 4, dated, reasoned, stating the data that existed (the E2 grid, `e2_minimum_n.json` `computed_at` 20:40:00Z, which does predate it) | REGISTRATION.md:947-991 | **yes** |
| C10 | Amendment 5 §5's "permanently forecloses reopen path (b)" corrected to path (c) | REGISTRATION.md, DECISIONS.md, progress.md, report.md | `4d11002` 02:43:48Z | **yes** — Amendment 6, appended, Amendment 5 left unedited | REGISTRATION.md:1096-1119 | yes (the collection decision) |
| C11 | `HOLD_HOURS` literal 24 → `CONFIG.horizon_primary_days * 24` | `src/etf/recorder.py` | `c9e8c9d` 20:31:09Z | not needed — numerically identical, removes a duplicated literal | — | no |
| C12 | **No registered numeric parameter changed at all.** `git diff 815f888 4d11002 -- src/etf/config.py` = **12 insertions, 0 deletions**, all three string fields plus comments | `src/etf/config.py` | — | — | — | — |

Confirmed unchanged from the pre-data commit `815f888` (08:05:56Z) to the anchor:
`entry_anchor_hour_utc=8`, `anchor_amendment_percentile=0.95`, `signal_threshold_usd=100_000_000.0`,
`horizon_primary_days=1`, `reversal_horizon_max_days=20`, `alpha_adj = 1 − 0.95^(1/2)`,
`threshold_grid_usd=(0, 50M, 100M, 200M)`, `power_go_floor=0.80`, `power_blocked_floor=0.50`,
`power_simulations=2_000`, `permutation_draws=20_000`, `rho_registered=0.09`, `rho_undecayed=0.18`,
`rho_quartered=0.045`, `pre_period_end_date="2025-05-01"`, `interim_deadline="2026-12-31"`,
`projection_deadline="2027-03-31"`, `archive_density_pass_share=0.60`,
`revision_intact_pass_share=0.90`, `min_outcome_coverage_candles/funding=0.95`,
`retro_revision_sample_min=30`, and the per-source caps 200 / 2,000 / 5,000 per day.

**C08 is the only parameter deviation after data existed that carries no dated amendment.**
C07 carries one, one amendment late.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1 — the E1 minimum-N table of Amendment 3 §1 and `reports/stage_a2/power.json` `minimum_n_for_e1`
- **Direction:** A — the closure's figures were not produced by the method the register states for them, so the provenance is looser than labelled
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED (git objects + exact reproduction from the repository's own code)
- **Claim challenged (verbatim quote):** "Simulation budget stated: E1 at 20,000 permutation draws / and 2,000 simulations; E2 at 1,500 draws and 400 simulations, whose simulation / error near a power of one half is about 0.025 — both registered floors sit far / from these values." — ETFExperiment/REGISTRATION.md:856-859 (repeated verbatim at ETFExperiment/report.md:329-332)
- **Evidence:**
  - The sentence sits directly beneath **two** tables in Amendment 3 §1: the minimum-N table at ETFExperiment/REGISTRATION.md:834-838 (237 / 845 / 3,776) and the power table at ETFExperiment/REGISTRATION.md:846-851.
  - `src/etf/power.py:225-234` — `minimum_n(rho_true, target, *, lo=20, hi=4000, alpha=CONFIG.alpha_adj, draws=4_000, simulations=600, seed=20260828)`. ETFExperiment/src/etf/power.py:232-233.
  - `scripts/power_gate.py:105` calls it with **no** budget override: `label: minimum_n(rho, TARGET) for label, rho in assumptions.items()`. ETFExperiment/scripts/power_gate.py:104-106.
  - `src/etf/power.py:91-92` — `e1_power` *does* default to `CONFIG.permutation_draws` (20,000) and `CONFIG.power_simulations` (2,000), so the statement is correct for the power table.
  - `reports/stage_a2/power.json` (tracked; read 2026-09-05T04:02Z) records `"permutation_draws": 20000, "power_simulations": 2000` for the whole file, written unconditionally from CONFIG at ETFExperiment/scripts/power_gate.py:115-116.
- **Recomputation:** inputs — `src/etf/power.py` and `src/etf/config.py` copied verbatim from SNAP into my work directory and driven by my own script (`work/agentC-etf-prov/repro_minn.py`, `repro_stated.py`, and an E1 power probe). Method — call the repository's own functions at the two budgets, same seed 20260828.
  - **As-run (4,000 draws / 600 simulations):** `minimum_n(0.18, 0.80) = 237`; `minimum_n(0.09, 0.80) = 845`. **Both reproduce the register bit-for-bit.**
  - **At the budget the register states (20,000 / 2,000):** `minimum_n(0.18, 0.80) = 237` (unchanged); **`minimum_n(0.09, 0.80) = 1016`**, against the registered **845** — a 20.2 % difference.
  - **E1 power table at 20,000 / 2,000:** all six cells reproduce exactly (0.0815, 0.0500, 0.3870, 0.1155, 0.6105, 0.2015). The stated budget is correct for that table.
  - Tolerance: exact equality; these are seeded deterministic integer-count ratios.
- **What would resolve it:** either a dated amendment recording that the minimum-N bisection ran at 4,000 draws / 600 simulations, or a rerun of `minimum_n` at the registered 20,000 / 2,000 with the 0.09 figure restated as 1,016. Note that 1,016 still sits inside Section 9's registered anchor of "high hundreds to low thousands" (REGISTRATION.md:382), so **no stated conclusion changes**; and the direction of the error understates how much data E1 would need, which if anything strengthens the closure.
- **Confidence:** HIGH — both figures were reproduced exactly from the repository's own seeded code at the as-run budget, and the stated budget was run to completion.
- **Invalidated by later commits?:** no — `4d11002` is the last commit and `power.py` has not changed since `5fa460a`.
- **Disclosed by authors?:** no — the register and the report both state a single E1 budget covering the whole section, and `power.json` repeats it. The E2 departure *is* disclosed in the same sentence; the E1 minimum-N departure is not disclosed anywhere.

### DRAFT-P-2
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1 — Amendment 5's closing figure table
- **Direction:** A — the figure the closure is deliberately rested on carries a provenance label that belongs to a different computation
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "| E1 minimum N at the published 0.18 | **237** | 1,200 draws, 300 sims/cell |" — ETFExperiment/REGISTRATION.md:1011
- **Evidence:**
  - 1,200 draws / 300 simulations is **Amendment 4's E2 grid** budget: `scripts/e2_minimum.py:42` — `power = e2_power(n, rho, inputs, draws=1200, simulations=300)` (ETFExperiment/scripts/e2_minimum.py:42), matching Amendment 4's own statement at ETFExperiment/REGISTRATION.md:958-959 and the stored `reports/stage_a2/e2_minimum_n.json` (`computed_at` 2026-08-28T20:40:00Z, grid cells 200/250/300 and 200…1200).
  - The next row of the same table, "E2 minimum N at the published 0.18 | **300** | 1,200 draws, 300 sims/cell" (ETFExperiment/REGISTRATION.md:1012), is correct — the label was carried up one row onto a figure it does not describe.
  - E1's 237 came from `minimum_n` at 4,000 draws / 600 simulations (reproduced exactly; see DRAFT-P-1).
  - The row matters: ETFExperiment/REGISTRATION.md:1015 and ETFExperiment/report.md:456-463 rest the closure on "E1's 237 … the smallest minimum on the record", explicitly to make it robust to the unpinned E2 figure.
- **Recomputation:** as DRAFT-P-1. `minimum_n(0.18, 0.80)` returns 237 at 4,000/600, at 20,000/2,000, and is stated by the register as 237; the *value* is stable, only its stated provenance is wrong.
- **What would resolve it:** an amendment correcting the n-column of that row to the budget `minimum_n` actually used.
- **Confidence:** HIGH — the two budgets are both readable in the repository's own scripts and only one of them can have produced 237.
- **Invalidated by later commits?:** no — Amendment 6 (`4d11002`) appends without editing Amendment 5.
- **Disclosed by authors?:** no.

### DRAFT-P-3
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 2's statement of what data existed when it was made
- **Direction:** A — a blindness claim that the artifacts in the amendment's own commit contradict
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED (git objects + artifact timestamp + exact reproduction)
- **Claim challenged (verbatim quote):** "No power / number existed when this amendment was written." — ETFExperiment/REGISTRATION.md:708-709
- **Evidence:**
  - Amendment 2 is commit `41351a9`, author and commit date 2026-08-28 13:36:13 −0700 = **2026-08-28T20:36:13Z**.
  - `reports/stage_a2/power.json` carries `"computed_at": "2026-08-28T20:35:37Z"` — **36 seconds earlier** (ETFExperiment/reports/stage_a2/power.json:6; the same value is in the blob committed at `fe60a22`, so it is not a later overwrite).
  - The preceding commit is `66a0c81` at 20:35:28Z, so the whole authoring window for Amendment 2 is 45 seconds wide and the power run lands 9 seconds into it.
  - **`41351a9` itself contains the edit that produced that file.** `git diff 41351a9^ 41351a9 -- scripts/power_gate.py` replaces `e2 = e2_power(n, rho, inputs)` with `e2 = e2_power(n, rho, inputs, draws=1500, simulations=400)` and adds the justifying comment "E2's inner permutation is O(draws x n) per simulation, so the gate runs it at a smaller but stated budget" — a comment that can only be written after observing the gate's cost.
  - Recomputation confirms `power.json` was produced by the **post-edit** script: `e2_power(11, 0.18, …, draws=1500, simulations=400) = 0.0600` = stored 0.0600, while `draws=2000` gives 0.0725; `e2_power(11, 0.09, …)` 1500 → 0.0375 = stored, 2000 → 0.0475; `e2_power(88, 0.18, …)` 1500 → 0.3325 = stored, 2000 → 0.3800. Three for three at 1,500, none at 2,000.
- **Recomputation:** inputs — `reports/stage_a2/power.json` `economic_inputs` block (daily_sd 0.027430504889517645, daily_funding_sum 0.0005343574667950626, round_trip_cost_bp 9.0, trade_share 0.7567567567567568) fed to `src/etf/power.py:119` `e2_power` copied from SNAP. Method — reproduce stored cells at each candidate budget. Result — exact match at 1,500/400 only. Tolerance: exact equality (seeded).
- **What would resolve it:** a shell or session record fixing the moment the amendment text was composed relative to 20:35:37Z. Nothing in the repository can settle it: `git` records only the commit instant, and the ledger has no row between 20:32:17Z and 20:40:46Z. If "written" is read as "committed", the claim is false; if it is read as "drafted before the gate was run", it is unverifiable and the amendment does not say so.
- **Confidence:** MEDIUM — the artifact ordering is certain and the co-committed `power_gate.py` edit is strong circumstantial evidence that the gate had been run and inspected; the word "written" leaves a 9-second window in which the claim could be literally true.
- **Invalidated by later commits?:** no — Amendment 2 stands unedited at the anchor, as the append-only rule requires.
- **Disclosed by authors?:** no. Amendment 3 (REGISTRATION.md:821-824) correctly lists "the completed power computation" among the data that existed by then, but Amendment 2 asserts the opposite for a moment 4 m 45 s earlier.

### DRAFT-P-4
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1 — the deadline finding, on which the `untestable-at-achievable-power` closure rests
- **Direction:** A — the closure is labelled as resting on measured, outcome-blind figures; its accrual input is a planning number
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED (stored census artifact + arithmetic on the repository's own projection code)
- **Claim challenged (verbatim quote):** "**The deadline finding, restated at the governing figure.** At the measured / forward accrual rate of 20.8 admissible days per month:" — ETFExperiment/REGISTRATION.md:981-982 (also "forward accrual 20.8 admissible days/month" REGISTRATION.md:1010; "the measured **20.8 admissible days per month**" REGISTRATION.md:1129; "At the measured forward accrual rate of 20.8 admissible days per month" report.md:360 and 447-448; HYPOTHESES.md:70, 82, 84; progress.md:493, 533; DECISIONS.md:555, 596)
- **Evidence:**
  - The registration's own governing correction, written pre-data at `38b9397` (2026-08-28T08:11:17Z): "**Therefore: no accrual, coverage, lag, retention, revision, or capture-density figure in this repository is registered before it is measured.** Every such figure is named as an A.1 or A.2 **measurement target**, never as an input" — ETFExperiment/REGISTRATION.md:571-573, with "admissible days per month and the trailing rate | **A.2 Task 1**" at ETFExperiment/REGISTRATION.md:584. Section 9 restates it: "a planning number must never become a registered one" — ETFExperiment/REGISTRATION.md:386-388.
  - **No forward accrual was measured.** `reports/stage_a2/census.json` (tracked; read 2026-09-05T04:04Z) records `"admissible_forward_capture": 0` and `"admissible_retro_archive": 11`. `reports/stage_a2/power.json` `scenarios` records `"achieved_forward_only": 0`.
  - **The figure is stored nowhere.** `grep -rn "20\.8\|accrual\|per_month" reports/` returns nothing. It exists only in prose.
  - **The stored projection uses a different rate.** `power.json` records `"weekdays_to_deadline": 153`, `"printed_day_rate": 0.9910714285714286`, `"forward_only_by_deadline": 152`, `"all_cohorts_by_deadline": 163` — i.e. 153 weekday calendar days × 333/336, produced by `scripts/power_gate.py:71-81`. Over the 215 days from 2026-08-28 to 2027-03-31 that is **21.5 admissible days per month**, not 20.8.
  - **20.8 does not reproduce the 163 it is paired with.** 7.06 months × 20.8 = 146.8 forward days, +11 retro = **158**, against the stated 163. Conversely 20.8 = (252/12) × (333/336) = 20.8125 — the conventional 252-US-trading-day year times the measured printed-day rate — or 333 printed days over a ~16.0-month out-of-sample window. Either way it is a calendar convention applied to a measured print count, not a measurement of the rate at which days become admissible.
- **Recomputation:** inputs — `reports/stage_a2/census.json` and `reports/stage_a2/power.json` (read 2026-09-05T04:04Z), and the weekday counter at ETFExperiment/scripts/power_gate.py:29-43 reimplemented in my work directory. Method — count weekdays over each stated interval, multiply by the stored `printed_day_rate`, and convert to a monthly rate. Result — 89 weekdays to 2026-12-31 → 88 (matches the register's 88); 153 weekdays to 2027-03-31 → 152 (matches 152/163); implied rate 21.4–21.5/month across every interval, against the stated 20.8. Tolerance: ±0.1 days/month.
- **What would resolve it:** either an amendment stating that 20.8 is a projection from the measured printed-day count under an assumed forward capture success and not a measured accrual, with its arithmetic shown; or a single accrual rate used consistently for both the 163 and the 2027-10-26 arrival date. The conclusion is not at stake — at 21.5/month the deadline shortfall narrows but does not close (300 is still reached around 2027-09) — but the label is.
- **Confidence:** MEDIUM-HIGH — HIGH that no forward accrual was measured (the census says 0), that the figure is in no artifact, and that it does not reproduce the 163 beside it; MEDIUM on the exact derivation of 20.8, which I can bound to two candidate constructions but not read off any file.
- **Invalidated by later commits?:** no — `4d11002` is the last commit and it repeats the figure at REGISTRATION.md:1129.
- **Disclosed by authors?:** no. `scripts/power_gate.py:69-71` discloses the weekday × printed-rate projection in a code comment, but no document states that the accrual figure is a projection, and every document calls it "measured".

### DRAFT-P-5
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 6 §4, the final network-cost record
- **Direction:** neutral — hygiene; the figure bears on no verdict
- **Class:** PROVENANCE (STALE_FIGURE)
- **Severity:** S3
- **Label:** DERIVED (append-only ledger, live working tree)
- **Claim challenged (verbatim quote):** "- The **220 charged requests** stand as the total lifetime network cost. Zero / dollars, no capital, no credential, at any point." — ETFExperiment/REGISTRATION.md:1160-1161 (also progress.md:602, "**220 charged requests** lifetime")
- **Evidence:**
  - `data/ledgers/requests.jsonl` (gitignored, live working tree only — **UNANCHORED**; read 2026-09-05T04:01Z; file mtime 2026-08-29T02:40:42Z, i.e. unmodified since the day of the anchor): 476 rows, **238 `kind":"charge"` rows**, first 2026-08-28T08:12:19Z, last 2026-08-29T02:40:32Z.
  - Amendment 6 is commit `4d11002`, 2026-08-29T02:43:48Z — **3 minutes 16 seconds after charge #238**.
  - Charge #220 is stamped 2026-08-28T20:40:46Z. The ledger held exactly 220 charges at commit `5192ba8` (2026-08-28T20:46:53Z), which is where the figure and its breakdown were first written (progress.md:514-516).
  - The breakdown proves the figure is that snapshot: at 220 charges the split is **flow 33, archive 79, venue 108** and the settles are **213 × 200, 5 × 404, 1 × 401, 1 × 403** — exactly what progress.md:564-565 states. Across all 238 the split is **flow 51**, archive 79, venue 108, and **231 × 200**.
  - The 18 extra charges are all `flow.table` at a 20-minute cadence from 21:00:36Z to 02:40:32Z — `etf-snap`, which Amendment 5 (23:39:33Z, ledger then at 228) explicitly kept armed at "roughly 33 requests per day" and which Amendment 6 disarms in the same bullet list as the 220 figure.
- **Recomputation:** inputs — `data/ledgers/requests.jsonl` rows filtered on `kind == "charge"`; method — count, and bisect the timestamp list at each amendment's commit instant. Result — 145 at Amendment 1, 219 at Amendment 2, 220 at Amendments 3 and 4, 228 at Amendment 5, **238 at Amendment 6**. Tolerance: exact counts.
- **What would resolve it:** restating the lifetime figure as 238, or dating the 220 figure to the Stage A close-out where it was true.
- **Confidence:** HIGH — the ledger is append-only, its last write predates the commit, and the 220-row breakdown matches the documents digit for digit.
- **Invalidated by later commits?:** no — `4d11002` is the last commit, and the ledger has not been written since 2026-08-29T02:40:42Z.
- **Disclosed by authors?:** no. Amendment 5 (REGISTRATION.md:1084) does state `etf-snap` "costs roughly 33 requests per day", which is the mechanism, but no document revises the total.

### Minor, recorded for completeness (S4, not pursued)

- **REGISTRATION.md:66-68** — "one-ULP steps across each". The boundary fixtures do sit exactly on 0.80, 0.50 and 0.50 (`tests/test_section0.py:40, 48, 80-81, 93-94`), but the steps are `1e-12`, roughly 9,000 ULPs at 0.8. The property being tested — strict-versus-non-strict comparison at the registered boundary — is genuinely pinned; only the description of the step size is wrong.
- **REGISTRATION.md:605-606** — "572 of 572 post-boundary rows across three pages". The 572 verifies exactly (`funding_post_period` 72/72 gated; `funding_2025_05_page` 500/500 gated). Post-boundary rows appear on **two** pages; five funding pages were probed in total, the other three carrying only pre-2025-05-01 rows (0 gated of 72, 500, 500).
- **REGISTRATION.md:601** — "the request ledger (143 charged requests)". 143 was the count at 20:12:49Z; the ledger held 145 at the 20:16:31Z commit. The two extra rows are the `archive.timemap` fetches at 20:14:03Z and 20:14:06Z whose measurement (`archive_density.json` `measured_at` 20:14:03Z) Amendment 1 itself registers.
- **CLAUDE.md:113 / REGISTRATION.md:426** — "`.env.example` is empty on purpose". The file is a 200-byte comment block whose first line reads "# Deliberately empty." No credential exists anywhere in history.
- **`src/etf/pacing.py:20-24`** — the code comment says "96 requests across 8 endpoints"; the register says "96 probe requests across 6 endpoints" (REGISTRATION.md:634) and the six per-endpoint counts in the same comment sum to exactly 96. **The register is the correct one**; the code comment is wrong.
- **DECISIONS.md:89-92 (ADR-003)** — the "81 of 333 days (24.3 percent, n = 333)" citation postdates the §8 registration it documents by 12 h 25 m (census `census_run_at` 20:34:47Z vs `e33b03c` 08:09:26Z). §8 as registered carried the same rationale qualitatively and without a figure (REGISTRATION.md:295-298), and the ADR labels the figure "measured" and carries its n, so the decision's provenance is intact; only the ADR's single date obscures that the number arrived later.

---

## 4. What could not be checked, and why

1. **Whether any network request was made before 2026-08-28T08:12:19Z.** The pre-registration ordering claim rests on the ledger's own first row plus `reports/stage_a1/robots_and_terms.json`. Both are written by the same code path (`etf.ledger.requests`). A request sent outside that path would leave no trace I can read. `data/` is gitignored, so I cannot use the tree at `44567f6` to prove the ledger did not exist — only that no data artifact was tracked. The claim is supported by everything available and cannot be closed beyond that.
2. **When Amendment 2 was "written" as opposed to committed.** See DRAFT-P-3. Git records commit instants only. No shell history, editor state or session log is in the repository.
3. **Whether `solattn-daily` existed on 2026-08-28** (progress.md:522). It is not in `systemctl --user list-timers --all` at 2026-09-05T04:06Z. `solattn` is a separate audited repository and its timer state is outside this repository's evidence. The other three named timers (`npl-watch` 60 min, `news-collect` 22:31Z, `npl-daily` 01:40Z) are all present with the stated schedules. **UNVERIFIABLE, not contradicted.**
4. **Whether the A.1 Task 1 probe code that ran at 08:12Z is the code committed at 20:04:41Z.** The probes ran twelve hours before their commit; `meta.robots` is the first ledger endpoint and was only added to the pacing map in that commit. The working tree at run time therefore held uncommitted code. This does not touch the pre-registration ordering (the registration commits all precede 08:12:19Z) but it means the *probe* code cannot be pinned to a commit that predates its own run.
5. **Whether the sealed outcome store was ever opened outside the repository's own code paths.** I verified the structural guards, the absence of `data/state/`, and that `verdict.py` is imported by nothing. An out-of-band read (a REPL, a notebook) would leave no trace. Stated as a limit, not as a doubt.
6. **The E2 minimum-N grid was not independently recomputed.** `e2_power` at n = 300 with 1,200 draws and 300 simulations is order 10^8 inner operations in pure Python; the budget claim for that grid was verified by reading `scripts/e2_minimum.py:42` and matching it against `e2_minimum_n.json`, not by re-running it.
7. **Whether the push to `origin` carried anything the anchor does not contain.** `refs/remotes/origin/master` equals `4d11002`, so the pushed tip is the anchored commit; I did not and could not inspect the remote.

---

## 5. What verified, stated plainly

A verified claim is a result. These are the ones that hold, several of them tightly:

- **The pre-registration ordering is real and is the strongest thing in this repository.** Five commits carrying the scaffold, the guards, CLAUDE.md, REGISTRATION.md Sections 0–14 and HYPOTHESES.md all land between 08:05:56Z and 08:11:50Z; the first network charge is stamped 08:12:19Z. The margin on the last commit is 29 seconds and on Section 0 is 4 minutes 20 seconds. Nothing in the tree at `44567f6` is a data artifact.
- **REGISTRATION.md is genuinely append-only.** All six post-data commits touching it are `+N / −0`, and every hunk header is an append at the end of the file (`@@ -594,0 +595,102 @@`, `@@ -696,0 +697,121 @@`, `@@ -817,0 +818,128 @@`, `@@ -945,0 +946,46 @@`, `@@ -991,0 +992,103 @@`, `@@ -1094,0 +1095,67 @@`). Not one byte above an amendment line was ever edited. Amendment 6 corrects Amendment 5 by appending a correction rather than editing it, exactly as CLAUDE.md:101-103 requires.
- **No registered numeric parameter ever moved.** `git diff 815f888 4d11002 -- src/etf/config.py` is 12 insertions and 0 deletions, all of them the three flow-source URLs and their comments. Every bar, floor, threshold, horizon, alpha, deadline, cap and coverage figure is byte-identical to the version committed 2 minutes 23 seconds before the first network request.
- **The Section 0 expectation was registered before the data.** `git show 44567f6:REGISTRATION.md` is 86 lines and is byte-identical to the anchored file's lines 1–86, including the DEGRADED expectation and its stated scope narrowing.
- **The operator prior slot never parsed.** `registration_check._FILL` was re-run against all seven committed versions of REGISTRATION.md: the label is present in all seven, the fill matches in none.
- **The two changes that did move a figure were both properly amended.** The archive-density falsification (0.1111 → 0.0330) is recorded as *falsified* in Amendment 2 with Amendment 1 left standing above it, and the census code change that caused it landed 45 seconds earlier. The governing minimum N (237 → 300) is recorded in Amendment 4, whose stated input — `e2_minimum_n.json`, `computed_at` 20:40:00Z — does predate it.
- **The pacing change is the model of a well-handled post-data amendment.** The registered rule ("half the measured ceiling") could not be applied because no ceiling was found; Amendment 1 substitutes an explicit alternative, names the precedent, records that the figures are bounded by what was probed rather than by what the server would refuse, and leaves the two unmeasured endpoints on their slower pre-measurement figures rather than letting them inherit a sibling's.
- **The mutation harness claim is true and its earlier failure is disclosed.** `reports/stage_a4/mutations.log` at `a881956` records all six caught and restored green; all six anchor strings are present in the anchored source; and report.md:417-421 discloses that two of the six first required fixing the harness.
- **The collectors are disarmed.** `etf-snap.timer` and `etf-daily.timer` are both `disabled` and `inactive` and appear in no timer listing, checked 2026-09-05T04:06Z.
- **No credential exists anywhere in history**, across every reachable commit.

If the thesis had been that this repository back-dated its registration, edited bars after seeing
data, or moved a threshold to reach a verdict, the evidence would have shown it here and it does
not. What the evidence does show is a cluster of **provenance-labelling** defects — a simulation
budget stated for figures it did not produce, an accrual figure called measured that was not
measured, a blindness claim contradicted by an artifact in the same commit, and a request count
carried past its expiry — in a repository whose substantive registration discipline holds.

---

## 6. Live-repo access log

Per COMMON_RULES, `git status --porcelain` was run on the live repository before the first access
and after the last. Both outputs are recorded verbatim.

**Before first access — 2026-09-05T03:58:55Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

(no output from `status --porcelain` — clean)

**After last access — 2026-09-05T04:15:27Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

(no output from `status --porcelain` — clean)

`HEAD` matched the anchored SHA before and after. **Nothing in the audited repository was
modified, and no entry of mine appears in either status output.**

**Note on an untracked file that does not appear in `status`.** `_CLOSED_DO_NOT_RUN_HERE`
(747 B, mtime 2026-09-02 22:38 local) sits in the live tree, hidden from `status` by
`.git/info/exclude`. It is an owner-written closure marker dated three days before this audit.
**It is not mine and predates this audit**; it is named here because COMMON_RULES requires any
working-tree entry beyond the listed pre-existing dirt to be reported. I did not open it beyond
`ls`.

**Read-only operations performed on the live repository**

| time (UTC) | operation | purpose |
|---|---|---|
| 03:58:55 | `git status --porcelain`, `git rev-parse HEAD` | pre-access record |
| 03:59–04:00 | `git log --all --date=iso-strict`, `git log --reverse --name-status`, `TZ=UTC git log --date=format-local` | build the commit timeline in true UTC |
| 04:00 | `git ls-tree -r --name-only 44567f6` | P01/P03 — what was in the tree at the Section 0 commit |
| 04:00–04:01 | `ls -la data/`, `head`/`wc` on `data/ledgers/requests.jsonl` | UNANCHORED working-tree read, P01/P05/P13 |
| 04:01 | `git diff --numstat` and `git diff -U0 … \| grep '^@@'` for six REGISTRATION.md commits | P04 — append-only |
| 04:01–04:02 | `git log --follow -p -- src/etf/config.py`, `git show <c>:src/etf/config.py` | P09, C12 — parameter immutability |
| 04:02 | `git diff 41351a9^ 41351a9 -- scripts/power_gate.py`, `git show fe60a22:reports/stage_a2/power.json` | C07, DRAFT-P-1, DRAFT-P-3 |
| 04:02–04:03 | `git show 4d11002:<reports/**>` for every tracked report | artifact timestamps |
| 04:03 | `git log -S "220 charged"`, `git log -S "20.8"` | trace figures to their first commit |
| 04:03 | `git remote -v`, `git for-each-ref`, `git reflog show refs/remotes/origin/master`, `git config --get-regexp '^remote\.'`, `git branch -r` | P15 — remote and push dating |
| 04:04 | reads of `reports/stage_a2/census.json`, `power.json`, `e2_minimum_n.json` from the working tree (tracked, tree clean) | DRAFT-P-1, DRAFT-P-4 |
| 04:04–04:05 | `git show a881956 --stat`, `git diff a881956^ a881956`, `git diff 66a0c81^ 66a0c81` | P14, C05 |
| 04:05 | `git show <c>:REGISTRATION.md` for seven commits (written to my work dir) | P11 — prior-slot regex at every version |
| 04:06 | `systemctl --user is-enabled/is-active`, `systemctl --user list-timers --all` | P12, P15 (not a repository access) |
| 04:07 | `ls data/state` (absent), `ls _CLOSED_DO_NOT_RUN_HERE` | P18 |
| 04:08 | `git grep -I -n -E '(api[_-]?key\|secret\|token\|…)' $(git rev-list --all)` | P10 — history-wide secret scan |
| 04:15:27 | `git status --porcelain`, `git rev-parse HEAD` | post-access record |

All computation ran from copies under
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-prov/`. No script belonging to
the audited repository was executed in place, and nothing was written inside
`/home/kiros-li/Documents/GitHub/ETFExperiment` or into `SNAP/`.
