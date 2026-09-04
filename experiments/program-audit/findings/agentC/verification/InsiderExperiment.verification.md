# InsiderExperiment — verification (Agent C, VERIFY)

Repository: `InsiderExperiment`
Anchored SHA: `12d9fd36cf055cb10ea67a3fc737e404217bc95a` (master, 2026-08-25)
Snapshot read: `SNAP/InsiderExperiment/` (tracked files, anchored)
Live tree read: `/home/kiros-li/Documents/GitHub/InsiderExperiment/` (git objects and
untracked/gitignored data only, read-only)
Recomputation: `scratchpad/venv/bin/python` under `scratchpad/work/agentC/insider/`.
No repository script was copied or executed. `var/insider_sealed.db` was **not** opened.
Prepared: 2026-09-04, live reads 18:20–18:31 UTC.

**Headline.** The deciding number reproduces exactly. Every figure in
`reports/stage_a1/power.json` — all four series, the four-point Newey-West grid, the drop
counts — was recomputed from the stored centered series in `var/insider_dispersion.db` and
agrees to the last stored decimal. The corpus totals, the attrition funnel, the lag
distribution, the cost band, the Section 0.4 floor derivation, the universe port and the
fetch-ledger cost claims all reproduce. The membership series was rebuilt independently from
the corpus store and the market store and reproduces `mean_book_width` and `session_coverage`
to full double precision. **This repository's closure is supported by its own artifacts.**

Nine discrepancies were found. None of them moves the BLOCKED verdict. Seven are stale or
mis-transcribed descriptive figures; one is a process breach (a registered config field deleted
after measurement with no amendment); one is a pair of book-width figures computed on two
different books and then presented as one comparison.

---

## A. Claims table

Tolerance convention: a stated figure is VERIFIED when the recomputation agrees to the
precision at which the document states it (e.g. "49.35" against a recomputed 49.35430).

| # | Claim (short) | file:line | Stated | Source of truth | Recomputed | Tol | Status |
|---|---|---|---|---|---|---|---|
| C1 | MDE primary | `REGISTRATION.md:812-816`, `:719`, `:712`; `progress.md:14-18`, `:187`, `:241`; `DECISIONS.md:288-292` | 49.35 bp/month | `var/insider_dispersion.db` centered series (n=2,581), formula `power/mde.py:38-66` | **49.3543** | 1e-4 | **VERIFIED** |
| C2 | BLOCKED fires at 49.35 against a 40 bp bar | `REGISTRATION.md:43,708`; `section0.py:77-87` | BLOCKED | `section0.py:62,77` branch, `config.py:142` `mde_degraded_ceiling_bp=40.0` | 49.3543 > 40.0 → BLOCKED; rationale string in `power.json` is byte-identical to the f-string at `section0.py:80-85` | exact | **VERIFIED** |
| C3 | 4,585 events; 99.5 % coverage; mean book width 71.9 | `REGISTRATION.md:594-596` | 4,585 / 99.5 % / 71.9 | `var/insider_corpus.db` `event` (4,585 rows), membership rebuilt from `event.symbol,entry_session` × `insider_market.db.session` | 4,585; **0.9954110898661568**; **71.90895121014215** | exact | **VERIFIED** |
| C4 | The by-year table under that headline | `REGISTRATION.md:601-608` | 262/406/524/457/717/297/502/505/410/363/99, implicitly 4,585 | `corpus.json` `events_per_year`; independently rebuilt from `event.entry_session` | 263/409/531/462/728/298/504/508/418/365/99; printed table sums to **4,542** | exact | **CONTRADICTED** (DRAFT-V-1) |
| C5 | TE 9.993 %, N_eff 2,869.9 from 2,581 sessions, VIF 0.899, sd 62.95 bp | `REGISTRATION.md:712,717-719,844-848`; `progress.md:35-38`; `DECISIONS.md:158-160` | as stated | same centered series | TE **9.9933 %**, N_eff **2,869.9**, N **2,581**, VIF **0.8993**, sd **62.9519 bp** | 1e-4 | **VERIFIED** |
| C6 | "that tracking error is the whole of the 49.35" | `REGISTRATION.md:845-846` | identity | `mde.py:50,66` | MDE = 2·21·(TE/√252)/√N_eff; 2·21·(0.099933/15.8745)/√2869.9 = 49.354 bp | 1e-3 | **VERIFIED** |
| C7 | VW book "holds a mean of 71.9 names and behaves like 29.7 effective names" | `REGISTRATION.md:839-840`, `:749`; `progress.md:31-32`, `:249-250` | 71.9 → 29.7 | `portfolio.json[0]`, `power.json` series[0] `book_width_mean 66.93`, dispersion store `book_width` | 71.909 is `membership.mean_width()` **before** the 13,750 `not_priced` drop; the book that produced 29.731282 and the 49.35 averages **66.92522278** names | — | **CONTRADICTED** (DRAFT-V-3) |
| C8 | Top-1 14.9 %, top-5 33.8 %, corr 0.904 | `REGISTRATION.md:749`, `:840-841` | 14.9 / 33.8 / 0.904 | `portfolio.json[0].diagnostics` | 0.149323 / 0.337911 / 0.903981 | 5e-4 | **VERIFIED** |
| C9 | 214 wire requests, 2.78 GB, zero non-200 | `REGISTRATION.md:827-830`; `progress.md:23-27` | 214 / 2.78 GB / 0 | `ledgers/fetch.jsonl` (684 records, UNANCHORED, read 18:24 UTC) | 214 `wire` + 470 `cache`; wire bytes **2,783,280,665**; status 200 on all 684; max 7 wire requests in any one second against the registered 8/s | exact | **VERIFIED** |
| C10 | "The cache on disk is 2,783,280,665 bytes, which equals the wire total exactly" | `REGISTRATION.md:832-833` | equal | `du -sb cache/edgar` + `find -type f` (UNANCHORED, read 18:28 UTC) | **2,783,280,665** bytes across exactly **214** files | exact | **VERIFIED** |
| C11 | "Stage A.1 at about 51 minutes of session wall clock" | `progress.md:115-116` | ~51 min | git commit record; the ETA table at `progress.md:196-205` | 18:20 → 19:11:55 = 51.9 min, but the table's own eight Actuals sum to **111 min**; tasks 5/6/7 claim 20+32+22 min across commits 10 s apart | — | **CONTRADICTED** (DRAFT-V-5) |
| C12a | EW secondary: TE 6.86 %, MDE 34.29, "would have fired DEGRADED" | `REGISTRATION.md:852-854`, `:715`; `progress.md:42-44`; `DECISIONS.md:318-321` | 6.86 % / 34.29 / DEGRADED | dispersion store, 126-session equal-weighted series | TE **6.8556 %**, MDE **34.2897**; 20 < 34.2897 ≤ 40 → DEGRADED at `section0.py:62` | 1e-4 | **VERIFIED** |
| C12b | "the equal-weighted book holds 71.9 and behaves like 66.9" / "Both books hold 71.9 names" | `REGISTRATION.md:852-853`, `:863`, `:750`; `progress.md:42`, `:252-253` | 71.9 → 66.9 | `power.json` series[3], dispersion store `book_width` for (126, equal_weighted) | The EW book's `book_effective_names` **66.925223** is *exactly* the mean priced width **66.92522278**. The EW book holds 66.93 and behaves like 66.93 | 1e-6 | **CONTRADICTED** (DRAFT-V-4) |
| C13 | Net band 13.3 to 34.7 bp/month; drags 5.33 / 16.67 | `REGISTRATION.md:417-418,420-422,736`; closure rounds to "13 to 35" at `:815` | as stated | `cost.py:30-57`, `config.py:136-137` (32/100 bp), hold 126/21 = 6.0 months | 32/6 = **5.3333**; 100/6 = **16.6667**; net (30−16.6667, 40−5.3333) = **13.3333, 34.6667** | 1e-4 | **VERIFIED** |
| C14 | Attrition funnel, eight rows and eleven sub-reasons | `REGISTRATION.md:620-628,632-644` | 2,876,095 intake … 4,585 qualifying | `corpus.json` `attrition` (30 keys) | Every group sum matches the printed row; the eight rows sum to **exactly 2,876,095**; the share column reproduces to 2 dp (0.30/89.64/4.56/5.18/0.08/0.08/0.00/0.16) | 0.005 pp | **VERIFIED** |
| C15 | "Only 5.8 percent … happen at a liquid-500 name" / "94.2 percent" outside | `REGISTRATION.md:656-660`, `:778-779`, `:893-894`; `DECISIONS.md:120-125` | 5.8 % / 94.2 % / 16 of 17 | `corpus.json` attrition | 9,160/(148,883+9,160) = **5.7959 %**; 94.2041 %; 148,883/9,160 = 16.25 | 0.05 pp | **VERIFIED** |
| C16 | "absent for 3,350 of the 4,585 … 73.1 percent" | `REGISTRATION.md:662-663` | 3,350 / 73.1 % | `corpus.json` `flag_absent_events`; `event.flag_reported` splits 3,350/1,235 | 3,350; **73.064 %** | 0.05 pp | **VERIFIED** |
| C17 | Lag table: p25 1, p50 1, p75 3, p90 4, p95 4, p99 230, max 1,988, mean 9.52; "73.0 percent within two … 95.9 within four"; "a tail of 91 events" | `REGISTRATION.md:672-684` | as stated | `corpus.json` `lag_distribution` (88 bins, sums to 4,585) | 1/1/3/4/4/**230**/**1988**/**9.5154**; ≤2 days **72.999 %**; ≤4 days **95.856 %**; >10 days **91** | 0.05 pp | **VERIFIED** |
| C18 | ADR-003: "51.3 percent … within one calendar day and 95.9 percent within four" | `DECISIONS.md:97-99` | 51.3 / 95.9 | same | **51.3195 %** / **95.8561 %** | 0.05 pp | **VERIFIED** |
| C19 | Section 0.4 floor derivation (19.52/39.04 bp, 3.10/6.20 %, 23.4/93.7 names, 468/1,000/1,875 events, 4.24 % and ~27 bp at 1,000, +11.8 %) | `REGISTRATION.md:97-100,110-113,119-123,137-138,143-144` | as stated | hand arithmetic on the registered planning values at `:90-93`; same identity as `mde.py:38-50` | 19.519 / 39.038 bp; 3.098 / 6.197 %; 23.44 / 93.77 names; 468.0 / 1,000.0 / 1,874.5; TE 4.2426 %, MDE **27.38 bp**; √(2520/2016) = **1.1180** → +11.8 % | 0.01 | **VERIFIED** |
| C20 | "The Johnsen filter rejected 209 of 773 clusters"; the DRI refusal | `REGISTRATION.md:693-697`; `reports/stage_a1/refusals.md:13-22` | 209 / 773; DRI 2020-04-23/27, 12 filers, modal fraction 1.00 vs 0.80 | `corpus.json` `clusters_found/rejected`; `insider_corpus.db.cluster` (773 rows, 209 with `rejected=1`) | 773 / 209 confirmed in both the JSON and the store; the serialized refusal block matches the prose | exact | **VERIFIED** |
| C21 | "449 unclassifiable in 2016, 257 in 2017, **257 in 2018**, falling to 84 by 2023" | `REGISTRATION.md:702-704` | 257 in 2018; monotone fall to 84 | `corpus.json` `unclassifiable_by_year` (sums to 2,057) | 2018 = **256**; 2022 = **296**, so the series does not fall monotonically (2021 = 110 → 2022 = 296 → 2023 = 84) | exact | **CONTRADICTED** (DRAFT-V-2) |
| C22 | "2,057 transactions carry that state" | `REGISTRATION.md:701` | 2,057 | `corpus.json` `attrition.filtered_routine/insufficient_history`; `unclassifiable_by_year` | 2,057 in both | exact | **VERIFIED** |
| C23 | "removed 13,750 name-sessions … about 7.4 percent of held name-sessions" | `DECISIONS.md:262-265` | 13,750 / 7.4 % | `power.json.dropped_primary`, `portfolio.json[0].dropped`, dispersion `dropped` table | 13,750 in all three; 13,750/(71.909 × 2,581) = **7.41 %** | 0.05 pp | **VERIFIED** |
| C24 | Five registered mutations, every guard failed when mutated and green when restored | `progress.md:228-229`, `:265-290`; `DECISIONS.md:352-396` | 5 / all true | `reports/stage_a1/mutations.json` | 5 records, all `guard_failed_when_mutated: true` and `guard_green_when_restored: true`, each naming a real `tests/test_guards.py` node | exact | **VERIFIED** (see note in §E on `final_suite`) |
| C25 | "106 tests" | `progress.md:217-218`; commit subject `672b343` | 106 | AST enumeration of `tests/` (10 `test_*.py` files, no test classes, no collection hooks in `conftest.py`, `testpaths=["tests"]`, `addopts="-q --strict-markers"`) | 96 test functions + 7 extra from the 8-way parametrize at `test_section0.py:16` + 2 from the 3-way at `test_universe_port.py:87` = **105** | exact | **CONTRADICTED** (DRAFT-V-9) |
| C26 | "56 source files" / "mypy strict on 56 files" | `progress.md:216-217` | 56 | `pyproject.toml:56` `files = ["src/insider","tests","scripts"]` | 43 + 11 + 3 = **57** `.py` files under those roots (56 if `tests/conftest.py` is excluded); mypy was not run | — | **UNVERIFIABLE** — mypy's own file count cannot be reproduced without running it, and running it is out of scope |
| C27 | "`/home` sits on a 466 GB filesystem with 328 GB available, 26 percent used" | `progress.md:147-149` | 466 / 328 / 26 % | `df -h /home` at 18:30 UTC 2026-09-04 | 466G / **324G** / **27 %** | ±1 % over 10 days | **VERIFIED** (consistent with drift) |
| C28a | `backtest/universe.py` hash `8188eea0…5529` unchanged | `progress.md:135,138`; `port.json` | 8188eea0…5529 | `sha256sum` of the live AiTrader file, 18:26 UTC | **8188eea0aef8a4d737e220095b9081071e26e4b4d30cceafb5082d7bfe525529**, mtime 2026-07-26 | exact | **VERIFIED** |
| C28b | `analysis_bars.db` hash `d599ccf0…f924` unchanged | `progress.md:135,137`; `port.json` | d599ccf0…f924 | live file today | Size is now **7,323,656,192** against `port.json`'s recorded 7,320,629,248, mtime 2026-09-03 | — | **UNVERIFIABLE** — the AiTrader collector has written to the file since 2026-08-25; the digest cannot be reproduced today and its failure to reproduce is **not** evidence against this repository |
| C29 | `port.json`: 2,615 sessions, 124 formations, 1,218 symbols, 2,713,496 bars | `reports/stage_a1/port.json` | as stated | `var/insider_market.db` (UNANCHORED, read 18:27 UTC) | `session` **2,615**; `COUNT(DISTINCT formation_date)` **124**; `COUNT(DISTINCT symbol)` **1,218**; `bar` **2,713,496** | exact | **VERIFIED** |
| C30 | ADR-004: "500 of 500 members reproduced exactly at each" of three formation dates | `DECISIONS.md:109-112` | 500/500 | `insider_market.db.membership` | 62,000 rows; **every one of the 124 formation dates carries exactly 500 members** (single distinct group count). The three-date port check itself is `tests/test_universe_port.py:87`, which was not executed | exact for the stored side | **VERIFIED** for the stored membership; the *comparison against AiTrader's own store* was not re-run |
| C31 | Validation routes: ratio 2.04–2.14 across 53 quarters; 25 XML agree, 0 disagree; 21 of 25 tickers present | `DECISIONS.md:60-66`, `:209-210` | as stated | `reports/stage_a1/validation.json` | 53 quarters, min **2.043**, max **2.140**; 25 agrees / 0 disagrees; **21** of 25 `symbol_present` | exact | **VERIFIED** |
| C32 | ADR-002: "53 files totalling about 750 MB" | `DECISIONS.md:58` | ~750 MB | `ledgers/fetch.jsonl`, the 53 `form345.zip` wire records | **570,492,991 bytes = 570.5 MB (544 MiB)** | — | **CONTRADICTED** (DRAFT-V-8) |
| C33 | ADR-002: "on the order of two million Form 4 documents … above 69 hours of wall clock" | `DECISIONS.md:50-54`; `REGISTRATION.md:558-560` | 2 M / >69 h | `validation.json` totals; arithmetic | 2,000,000/8/3600 = **69.44 h** — the arithmetic is right. But `validation.json` gives **2,440,873** Form 4 documents across **all** issuers, not universe issuers, and no stored artifact counts universe-issuer documents | — | arithmetic **VERIFIED**; the 2 M premise **UNVERIFIABLE** — no artifact counts Form 4 documents restricted to universe issuers |
| C34 | "That is 51 percent of all role rejections" | `REGISTRATION.md:652-654` | 51 % | `corpus.json` attrition | 46,706/131,222 (all role rejections) = **35.59 %**; the most favourable denominator, ten-percent-owner rejections only, gives 46,706/93,664 = **49.87 %** | 0.5 pp | **CONTRADICTED** (DRAFT-V-7) |
| C35 | "roughly ten times the surviving corpus" | `REGISTRATION.md:653-654` | ~10× | same | 46,706/4,585 = **10.19** | 0.5 | **VERIFIED** |
| C36 | P1: "Section 0 is committed before Task 4 computes anything" | `REGISTRATION.md:5-9`; `progress.md:223-224` | Section 0 frozen at `fbfc74e` | `git diff --unified=0 fbfc74e 12d9fd3 -- REGISTRATION.md` | A single purely additive hunk `@@ -159,0 +160,737 @@`. **Lines 1–159 are byte-identical** from the first commit to the anchor. First SEC wire request 18:35:18, 22 s after `fbfc74e` (18:34:56); first `corpus_gate` evidence record 18:42:24; first `power_gate` 18:51:14 | exact | **VERIFIED** |
| C37 | P3: "Section 15 … Empty at the time Section 0 was committed at 18:34" | `REGISTRATION.md:589-590` | absent at `fbfc74e` | git | Section 15 first appears in `d8b81f1` (19:11:55); the additive hunk confirms it was absent earlier | exact | **VERIFIED** |
| C38 | P4/P5: value-weighted named primary and equal-weighted secondary "before any number was visible" | `REGISTRATION.md:761-762`, `:856-858`; `progress.md:47-48` | labels predate the numbers | `git show fbfc74e:src/insider/config.py`; evidence ledger | `primary_weighting="value_weighted"` and `secondary_weighting="equal_weighted"` are present at `fbfc74e` (18:34:56); the first `power_gate` evidence record is 18:51:14 | exact | **VERIFIED** |
| C39 | P6: "## Section 16. Amendments — None in force" | `REGISTRATION.md:798-800`, read against `:8-9` | no registered value changed after `fbfc74e` | `git diff fbfc74e 672b343 -- src/insider/config.py` | The registered field `benchmark_id: str` / `benchmark_id="U-LIQ-500-VW"` was **deleted at `672b343`, 19:11:45**, i.e. after the corpus build (18:47) and after the power gate fired (18:51), with no numbered amendment | exact | **CONTRADICTED** (DRAFT-V-6) |
| C40 | P7: the power path cannot reach a first moment | `CLAUDE.md:20-24`; `REGISTRATION.md:155-159`; `DECISIONS.md:165-193` | series sums to zero; no first-moment field | dispersion store; `dispersion.py:123-148`, `mde.py:18-35` | The four stored series sum to **−1.37e-16, +1.70e-16, −2.92e-16, −7.52e-17** — genuinely centered. `DispersionStats` and `MdeResult` carry no first-moment field. `insider_sealed.db` was not opened by this audit | 1e-15 | **VERIFIED** |
| C41 | P11: Section 12 closes unfilled; the assistant's 0.12 sits outside the slot | `REGISTRATION.md:497-513`, `:876-885` | empty; 0.12 outside | `REGISTRATION.md:506`; `registration_check.py:17,43-49` | The `[ EMPTY.` marker is present at `:506`, so `operator_prior()` short-circuits to `None`. The 0.12 at `:513` does not match `_PRIOR_RE` (which requires a `>`-prefixed line), so it cannot be read as the operator's number | exact | **VERIFIED** |
| C42 | P13: Z.1 "computes no statistic, reads no alpha, … changes no result" | `progress.md:9-10`; `REGISTRATION.md:806-808` | records only | `git show --stat 12d9fd3`; artifact mtimes | `12d9fd3` touches exactly `DECISIONS.md`, `REGISTRATION.md`, `progress.md`: **408 insertions, 0 deletions**. Every file under `reports/stage_a1/` has mtime ≤ **2026-08-25 19:10:28 −0700**, before the Z.1 commit at 23:24:15 | exact | **VERIFIED** |
| C43 | P9: "No systemd unit was ever installed … Nothing remains scheduled" | `progress.md:127-131`; `DECISIONS.md:303-306` | none | `~/.config/systemd/user`, `/etc/systemd/system`, `systemctl --user list-units/list-timers --all`, `crontab -l` at 18:30 UTC | No unit, timer or cron entry matches `insider` | exact | **VERIFIED as of today**; the state on 2026-08-25 cannot be reconstructed |
| C44 | Cross-repository figures (NPD 0.0512 / 415 days / 6.9378 USD / 427→125.6; H-F z 1.668 vs 2.50 and 42–66 % TE; P26 19,648 trades at −1.97 bp; "eight families, zero positives") | `REGISTRATION.md:21-25,345-347,389-391,424-425`; `progress.md:103-112`; `DECISIONS.md:12-16` | as stated | — | Not produced here and not derivable from any artifact in this repository | — | **UNVERIFIABLE inside this repository** — each needs its source repository |
| C45 | Literature figures (CMP 82 bp/month 1989–2007, "roughly 30 to 40 bp on 2008–2024, a 60 to 70 percent decay"; Ozlen–Batumoglu 70–80 %; sigma 30 % annualized) | `REGISTRATION.md:48-55,107-108,181-186` | as stated | — | External to this repository; the 30–40 bp decayed band is the bar the BLOCKED floor was placed against (`:57-59`) and is **load-bearing but not derivable from any artifact here** | — | **UNVERIFIABLE** — no primary source is stored in the repository |

**Counts for this table (47 rows).** VERIFIED **33**, CONTRADICTED **9** (C4, C7, C11, C12b, C21, C25, C32, C34, C39), UNVERIFIABLE **5** (C26, C28b, C33, C44, C45 — C33's arithmetic verifies, its premise does not).

---

## B. Derived quantities table

Every derived figure recomputed from stored primitives. All agree unless marked.

| Derived quantity | From primitives | Stated | Recomputed | Status |
|---|---|---|---|---|
| Sample SD, primary (ddof 1 on the centered series) | 2,581 stored `centered` values | 62.9519 bp | 62.95190 bp | agrees |
| Bartlett VIF at lag 21, primary | same, `1+2Σ(1−k/22)ρ_k` | 0.8993 | 0.89932 | agrees |
| Effective periods = N/VIF | 2,581 / 0.89932 | 2,869.9 | 2,869.90 | agrees |
| Annualized TE = sd·√252 | sd | 9.9933 % | 9.99330 % | agrees |
| Monthly SE = 21·sd/√N_eff | sd, N_eff | 24.6771 bp | 24.67715 bp | agrees |
| MDE = 2.0·SE | SE | 49.3543 bp | 49.35430 bp | agrees |
| Autocorrelations ρ1/ρ5/ρ21, primary | centered series | 0.00645 / −0.03824 / 0.01029 | identical | agrees |
| NW grid MDE at lags 5/21/63/126 | centered series | 50.19 / 49.35 / 49.11 / 49.53 | 50.1903 / 49.3543 / 49.1057 / 49.5319 | agrees |
| 21-session VW series (N, VIF, TE, MDE) | dispersion store | 2,513 / 0.9667 / 15.7032 % / 81.4849 | identical | agrees |
| 63-session VW series | dispersion store | 2,563 / 0.8606 / 11.8273 % / 57.3398 | identical | agrees |
| 126-session EW series | dispersion store | 2,581 / 0.9224 / 6.8556 % / 34.2897 | identical | agrees |
| Drop counts, primary | dispersion `dropped` table | 12 / 0 / 22 / 13,750 | identical | agrees |
| Session accounting | 2,615 sessions − 12 empty_book − 22 no_finite_member_return | 2,581 | 2,581 | agrees |
| `mean_book_width` (membership, pre-drop) | rebuilt from `event` × `session`, hold 126 | 71.90895121014215 | **71.90895121014215** | agrees exactly |
| `session_coverage` | 2,603 non-empty of 2,615 | 0.9954110898661568 | **0.9954110898661568** | agrees exactly |
| Mean **priced** book width, both 126-session series | dispersion `book_width` | (power.json 66.93) | **66.92522278186749** | agrees; **≠ 71.909** (see C7/C12b) |
| EW `book_effective_names` | `portfolio.json[3]` | 66.925223 | equals the mean priced width to 1e-6 — by construction for equal weights | agrees; exposes C12b |
| Events by entry year | `event.entry_session` | (JSON) 263/409/531/462/728/298/504/508/418/365/99 | identical, sums to 4,585 | agrees with the JSON, **not** with the printed table |
| Attrition group sums | 30 sub-reason keys | 8,613 / 2,578,217 / 131,222 / 148,883 / 2,362 / 2,213 / 0 / 4,585 | identical; total exactly 2,876,095 | agrees |
| Attrition share column | group / 2,876,095 | 0.30 / 89.64 / 4.56 / 5.18 / 0.08 / 0.08 / 0.00 / 0.16 % | identical to 2 dp | agrees |
| Universe pass rate | 9,160 = 4,585+2,362+2,213 | 5.8 % / 94.2 % | 5.7959 % / 94.2041 % | agrees |
| 46,706 as a share of role rejections | attrition | 51 % | 35.59 % (or 49.87 % on the narrowest denominator) | **disagrees** |
| 10b5-1 absent share | 3,350 / 4,585 | 73.1 % | 73.064 % | agrees |
| Lag distribution, all statistics | 88 bins summing to 4,585 | p99 230, max 1,988, mean 9.52, ≤2 d 73.0 %, ≤4 d 95.9 %, ≤1 d 51.3 %, >10 d 91 | 230 / 1,988 / 9.5154 / 72.999 % / 95.856 % / 51.320 % / 91 | agrees |
| Cost drags and net band | 32 and 100 bp over 6.0 months | 5.33 / 16.67; 13.3 to 34.7 | 5.3333 / 16.6667; 13.3333 / 34.6667 | agrees |
| Net band under the **primary** (pessimistic) bar alone | `cost.py:50-54` discloses the pairing | (not stated as such) | 13.3 to **23.3** bp/month | consistent with the disclosed asymmetric pairing; disclosed at `REGISTRATION.md:409-411` and `cost.py:50-54` |
| Section 0.4 inversions | t=2.0, M=21, √N_eff=40.99, sigma=30 % | 19.52/39.04 bp; 3.10/6.20 %; 23.4/93.7; 468/1,000/1,875; 4.24 %; ~27 bp; +11.8 % | 19.519/39.038; 3.098/6.197; 23.44/93.77; 468.0/1,000.0/1,874.5; 4.2426 %; 27.38; 1.1180 | agrees |
| Wire-request cost | 684 ledger records | 214 wire, 2,783,280,665 B, 0 non-200 | identical; cache on disk equals it byte for byte across 214 files | agrees |
| Wire breakdown | ledger URLs | (not stated) | 53 DERA `form345.zip` = 570,492,991 B; 53 full-index = 2,207,515,405 B; 82 per-filing XML = 458,435 B; 25 submissions = 4,018,868 B; 1 `company_tickers.json` | the 2.78 GB is dominated by the full-index route, not the data sets |
| Throttle compliance | ledger timestamps | 8 req/s registered | max **7** wire requests in any one wall-clock second | agrees |
| Sum of the ETA table's Actual column | `progress.md:198-205` | (implied ≤ 51 min) | **111 min** | **disagrees** |
| Market store against `port.json` | `insider_market.db` | 2,615 / 124 / 1,218 / 2,713,496 | identical; 62,000 membership rows, exactly 500 per formation at all 124 | agrees |
| Corpus store against `corpus.json` | `insider_corpus.db` | 4,585 / 3,350 / 773 / 209 / 2,057 | `event` 4,585; `flag_reported` 3,350:1,235; `cluster` 773 with 209 rejected; `meta` agrees | agrees |
| Collected pytest cases | AST of `tests/` | 106 | **105** | **disagrees** |

---

## C. Intervals table

**There is no confidence interval anywhere in this repository.** A grep of `REGISTRATION.md`,
`DECISIONS.md`, `progress.md`, `CLAUDE.md` and `reports/stage_a1/refusals.md` for "confidence
interval", "95 %", "CI", "±" and "interval" returns no estimate. This is a designed property,
not an omission: Stage A.1 computes second moments only and Stage B — which is where the
interval would have lived — was never written (`REGISTRATION.md:483-488`, `:769-774`,
`:889-891`).

| Interval | Estimator actually used | Independence assumed? | Data structure | Reproduces? | Status |
|---|---|---|---|---|---|
| *(none exists)* | — | — | — | — | **UNVERIFIABLE — no interval is stated anywhere in the repository, so there is nothing to check.** |
| Nearest analogue: the **registered** Stage B interval, never computed | Day-clustered SEs on the calendar-time series, Newey-West Bartlett at lag 21, grid 5/21/63/126 (`REGISTRATION.md:452-465`) | **No.** The registration explicitly rejects independence across days and handles serial correlation with a Bartlett kernel; clustering is on the day, and the calendar-time construction is chosen precisely so that same-day events are counted once (`REGISTRATION.md:340-349`, `membership.py:1-8`) | Daily time series of a calendar-time portfolio; overlapping 126-session holds mean membership persists, which the registered lag of 21 is explicitly chosen to accommodate (`:461-465`) | Not applicable — never computed | **N/A (registered, unfired)** |
| The interval-shaped object that *was* computed: the Bartlett variance inflation feeding N_eff | `1 + 2Σ_{k=1..L}(1−k/(L+1))ρ_k` at `dispersion.py:104-120` | **No** — the whole point of the estimator is to relax it | Same daily series, 2,581 obs, overlapping holds | **Yes** — 0.8993 at lag 21 and the full 5/21/63/126 grid reproduce to 1e-4 | **VERIFIED** |

Note on the direction of the serial-correlation adjustment. VIF < 1 at every lag on the grid,
so the adjustment *raises* N_eff above the raw session count and therefore *lowers* the MDE.
The document states this plainly (`REGISTRATION.md:725-729`) and it means the serial-correlation
treatment moves the verdict toward GO, not toward BLOCKED — the BLOCKED finding is not an
artifact of the variance adjustment. Recomputing at every registered lag confirms the verdict
survives the whole grid (49.11 to 50.19 bp, all above 40).

---

## D. Tests table

**There is no p-value and no realized test statistic anywhere in this repository.** No
hypothesis test was run: Stage A.1 fires two threshold gates on counts and second moments, and
Stage B, which is where the test would have lived, was never written. The test-statistic-shaped
quantities are these.

| Quantity | Value | file:line | Estimator / distribution | Tail | dof / distribution | Multiplicity correction | Decision rule | Correction matches rule? | Reproduces? | Status |
|---|---|---|---|---|---|---|---|---|---|---|
| Registered critical value | t = 2.0 | `REGISTRATION.md:478-480`; `config.py:147` | **Registered constant, not estimated.** Applied identically to A.1 power and (had it run) B inference | **Two-sided**, stated explicitly | Not a t distribution in use — 2.0 is a fixed constant, used as a normal-approximation critical value; no dof is claimed | **None** | Single pre-registered primary contrast (`REGISTRATION.md:467-472`) | **Yes.** One contrast is not a family; a Šidák or Bonferroni here would be a correction with nothing to correct | n/a (constant) | **VERIFIED — no mismatch** |
| Registered direction vs the tail used | V1: "Net alpha **positive** and significant at t 2.0" (`:437`) | `REGISTRATION.md:437,478` | — | Registered direction is **one-sided (positive)**; the critical value applied is **two-sided 2.0** | — | none | single | **Yes, and conservatively.** A two-sided 2.0 against a directional alternative is the *harder* bar (≈ one-sided 2.5 %), so the tail choice cannot flatter a positive | n/a | **VERIFIED** |
| Power-gate MDE | 49.3543 bp/month | `power.json`; `mde.py:53-67`; `REGISTRATION.md:82-88` | `MDE = t_crit · SE`, SE = 21·sd/√N_eff | two-sided at t 2.0 | normal approximation, N_eff 2,869.9 | none | Single threshold, three-branch (GO / DEGRADED / BLOCKED), boundaries inclusive at the lower edge (`REGISTRATION.md:45-46`, `section0.py:51,62`) | Yes — a single gate needs no correction | **Yes**, to 1e-4 | **VERIFIED** |
| *Convention note on the MDE* | — | `mde.py:54`, `REGISTRATION.md:82-88` | The quantity is `t_crit·SE`, i.e. **the smallest alpha that would be called significant if observed exactly — 50 % power**, not the conventional 80 %-power MDE `(z_{α/2}+z_β)·SE = 2.80·SE` | — | — | — | — | — | Recomputed at the 80 % convention the primary MDE would be **69.1 bp/month** | **Registered before measurement and applied consistently across every series and every bar in Section 0.4, so it is not a post-hoc choice. It cannot flatter the BLOCKED verdict — the conventional MDE is larger, i.e. more strongly BLOCKED. It is the one place where the secondary's "would have fired DEGRADED" (34.29) depends on the convention: at the 80 % convention the secondary would be 48.0 bp, i.e. BLOCKED. The secondary is labelled non-verdict-bearing, so nothing turns on it. Recorded, not raised as a finding.** |
| Corpus gate | 4,585 events and 99.5 % coverage | `section0.py:90-140`; `power.json`/`corpus.json` verdicts | Deterministic threshold on counts; no sampling distribution | n/a | n/a | **None** | **Conjunction** — CORPUS-GO requires *both* the 1,000-event floor **and** the 80 % coverage floor (`REGISTRATION.md:68-73`; `section0.py:106,117` chained early returns) | **Yes.** A conjunction / all-must-pass rule needs no union-type correction per component, and none is applied. Had a Šidák or Bonferroni been applied here it would have been the classic mismatch; it was not | **Yes** — 4,585 ≥ 1,000 and 0.99541 ≥ 0.80 both hold; the JSON rationale string is byte-identical to `section0.py:136-138` | **VERIFIED — correction and rule agree** |
| Newey-West lag grid | 4 MDEs, 49.11–50.19 | `power.json` `newey_west_grid`; `REGISTRATION.md:721-723` | Same estimator at four bandwidths | — | — | **None, and none is needed**: the grid is a **sensitivity report**, explicitly non-verdict-bearing (`REGISTRATION.md:474-476`), not four tests whose minimum is taken | Single (lag 21 fires; the other three are reported beside it) | **Yes.** The verdict is read off the registered lag, not off the best of four, so there is no selection to correct | **Yes**, all four to 1e-4 | **VERIFIED** |
| Secondaries (21- and 63-session holds, EW weighting, 32 bp cost bar) | 81.48 / 57.34 / 34.29 | `REGISTRATION.md:713-715`, `:852-854` | Same estimator | — | — | **None** | All four are labelled non-verdict-bearing **before** any of them was computed (`REGISTRATION.md:474-476`; `config.py` at `fbfc74e`), and none is promoted | **Yes.** With no promotion path there is no multiple-comparisons family; the labelling is verifiable in the first commit, so it is not a post-hoc claim | **Yes** | **VERIFIED** |
| Portfolio–benchmark correlation | 0.904 VW, 0.953 EW | `REGISTRATION.md:749-750`; `returns.py:224-226` | `np.corrcoef` on the two daily series, n=2,581 | — | no interval or test attached | none | descriptive | n/a | **Yes** (0.903981 / 0.952946) | **VERIFIED** |
| Cross-repository statistic (READ only) | "H-F at z 1.668 against a 2.50 bar" | `progress.md:107-108` | Not produced here | — | — | — | — | — | not computable here | **UNVERIFIABLE inside this repository** |

One structural observation, recorded rather than raised. The equal-weighted series is
benchmarked against an **equal-weighted** universe, not the value-weighted one: `returns.py:202`
passes the series' own `weighting` into `_weights` for the benchmark, and `portfolio.json[3]`
confirms it (`bench_weight_top1_share` 0.002 = 1/500 for the EW row against 0.0702 for the VW
rows). So the VW-vs-EW comparison at `REGISTRATION.md:749-750` changes the benchmark as well as
the book. This is **registered**, not hidden — `REGISTRATION.md:351-352` says "at the same
weighting basis as the portfolio" — so it is not a finding, but a reader who takes the two rows
as a clean single-factor contrast would be reading more into them than the design supports.

---

## E. Draft findings

Nine. Temporary IDs; the consolidator assigns final ones.

### DRAFT-V-1
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.1, the qualifying-events-by-year table
- **Direction:** neutral (hygiene — no verdict number depends on it)
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** the by-year table at InsiderExperiment/REGISTRATION.md:601-608, read against the "4,585 qualifying events" headline at InsiderExperiment/REGISTRATION.md:594 —

  > `| 2016 | 262 | 2022 | 502 |`
  > `| 2017 | 406 | 2023 | 505 |`
  > `| 2018 | 524 | 2024 | 410 |`
  > `| 2019 | 457 | 2025 | 363 |`
  > `| 2020 | 717 | 2026 | 99 |`
  > `| 2021 | 297 | | |`
- **Evidence:**
  - The printed table sums to **4,542**, against the "**4,585** qualifying events" stated three lines above it at InsiderExperiment/REGISTRATION.md:594. n = 11 year cells.
  - `reports/stage_a1/corpus.json` `events_per_year` at the anchor reads 263 / 409 / 531 / 462 / 728 / 298 / 504 / 508 / 418 / 365 / 99 and sums to **4,585**. Nine of the eleven cells differ from the printed table; none matches downward.
  - `git show ccc9b13:reports/stage_a1/corpus.json` carries exactly the printed cells (262 / 406 / 524 / …, sum 4,542). The correction landed in `cb17046` (2026-08-25 19:11:45 −07:00); Section 15 was first written in `d8b81f1` (19:11:55), ten seconds later, and the corrected `corpus.json` had been on disk since **19:05:33** (mtime, read 2026-09-04 18:29 UTC). The document therefore transcribes a console output that the run had already superseded.
  - Independent rebuild: expanding the 4,585 rows of `var/insider_corpus.db.event` by `entry_session` reproduces the JSON cells exactly (263 / 409 / 531 / 462 / 728 / 298 / 504 / 508 / 418 / 365 / 99), so the JSON is right and the printed table is wrong. (`var/insider_corpus.db` is untracked and UNANCHORED; read 2026-09-04 18:27 UTC.)
  - The same stale cells propagate to `DECISIONS.md:148-149`: "the corpus shows **717** qualifying events in 2020 against **297** in 2021" — the artifact says 728 and 298.
- **Recomputation (if any):** inputs `var/insider_corpus.db.event.entry_session` (4,585 rows) and `var/insider_market.db.session` (2,615 rows); method: group by year of `entry_session`; result 4,585 across the eleven JSON cells; tolerance exact. Printed-table sum: 4,542, a shortfall of exactly 43 — the count ADR-013 attributes to the composite-natural-key merge.
- **What would resolve it:** replacing the eleven cells at REGISTRATION.md:601-608 and the two figures at DECISIONS.md:148-149 with the post-fix values, or a one-line note beside the table stating that it is the pre-fix composition and pointing at ADR-013.
- **Confidence:** HIGH — the superseded values are recoverable byte for byte from `ccc9b13` and the corrected values are reproduced independently from the event store.
- **Invalidated by later commits?:** no — this repository is closed and `12d9fd3` is the last commit; nothing after the anchor touches these files.
- **Disclosed by authors?:** partly. ADR-013 (DECISIONS.md:400-416) discloses the merge defect and names the 4,542 figure: "The build reported 4,585 qualifying events while the table held 4,542." What is **not** disclosed anywhere is that the published Section 15.1 table still carries the pre-fix cells; ADR-013 presents the defect as corrected, and in the store it was.

### DRAFT-V-2
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.4, the `insufficient_history` by-year series
- **Direction:** neutral (hygiene)
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The front truncation it causes is visible in the by-year counts: 449 unclassifiable in 2016, 257 in 2017, 257 in 2018, falling to 84 by 2023 as the look-back window fills." — InsiderExperiment/REGISTRATION.md:701-704
- **Evidence:**
  - `reports/stage_a1/corpus.json` `unclassifiable_by_year` at the anchor: 2008 1, 2012 1, 2014 1, 2015 11, 2016 **449**, 2017 **257**, 2018 **256**, 2019 188, 2020 174, 2021 110, 2022 **296**, 2023 **84**, 2024 95, 2025 96, 2026 38. Sum 2,057, matching the prose's own "2,057 transactions carry that state" at REGISTRATION.md:701. n = 15 year cells.
  - 2018 is **256**, not 257. `git show ccc9b13:reports/stage_a1/corpus.json` has 2018 = 257; `cb17046` moved one transaction from `insufficient_history` to `routine` (attrition 2058 → 2057, 155 → 156), which is exactly the ADR-008 correction, and it is the 2018 cell that lost the transaction.
  - The prose is internally mixed: the total (2,057) is post-fix while the 2018 cell (257) is pre-fix.
  - "falling to 84 by 2023" is not what the series does: 2021 is 110 and **2022 is 296**, so the count nearly triples before it falls to 84. The 2022 = 296 value is identical in the pre- and post-fix artifacts, so this half of the claim is not a staleness artifact but a mischaracterization of the stored series.
- **Recomputation (if any):** inputs `reports/stage_a1/corpus.json` `unclassifiable_by_year` (15 cells) at InsiderExperiment/reports/stage_a1/corpus.json; method: read cells and sum; result sum 2,057, 2018 = 256, 2022 = 296; tolerance exact.
- **What would resolve it:** correcting 257 → 256 for 2018, and either dropping "falling to 84 by 2023" or restating it as "falling to 84 by 2023 apart from a 2022 rebound to 296".
- **Confidence:** HIGH — read directly from the tracked artifact and confirmed against the superseded version in git.
- **Invalidated by later commits?:** no — closed repository, anchor is the tip.
- **Disclosed by authors?:** no. ADR-008 (DECISIONS.md:245-249) discloses that one transaction moved label and asserts the qualifying set and the MDE are unchanged — both of which verify — but it does not say which year cell moved, and nothing anywhere discloses the 2022 rebound.

### DRAFT-V-3
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 17.3 / 15.6, the "what did fail" explanation of the BLOCKED verdict
- **Direction:** neutral — it does not weaken the closure; it slightly *overstates* the concentration collapse that the closure is attributed to
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The value-weighted book holds a mean of **71.9 names and behaves like 29.7 effective names**, because the heaviest name carries **14.9 percent** of the book and the heaviest five carry **33.8 percent**." — InsiderExperiment/REGISTRATION.md:839-841
- **Evidence:**
  - The two numbers are computed on **two different books**. 71.909 is `MembershipSeries.mean_width()` (InsiderExperiment/src/insider/portfolio/membership.py:46-54), written to `portfolio.json` at InsiderExperiment/src/insider/portfolio/build.py:59. It averages `len(book)` over non-empty sessions **before** the `not_priced` drop.
  - 29.731282, 0.149323 and 0.337911 are computed at InsiderExperiment/src/insider/portfolio/returns.py:213-217 on `priced`, the book after the drop (`priced = [n for n in book if n in members]`, returns.py:189-190). The same drop is what removes **13,750** name-sessions (`power.json` `dropped_primary.not_priced`).
  - The book that actually produced the 29.7, the weight shares and the 49.35 has a mean width of **66.925** names, not 71.9: `power.json` series[0] `book_width_mean: 66.93` (InsiderExperiment/reports/stage_a1/power.json), whose source is `widths.append(len(priced))` at returns.py:210.
  - Recomputed from the dispersion store's own `book_width` column: mean = **66.92522278186749** over n = 2,581 sessions (`var/insider_dispersion.db`, UNANCHORED, read 2026-09-04 18:22 UTC).
  - Effect on the stated collapse: the document's ratio is 71.909/29.731 = **2.42×**; the like-for-like ratio on the book that produced both numbers is 66.925/29.731 = **2.25×**. The direction of the error therefore makes the concentration look worse than it is, i.e. it favours the BLOCKED explanation. The verdict itself is untouched — the MDE reproduces exactly.
  - The same pairing appears in the table at InsiderExperiment/REGISTRATION.md:749 ("| 126, value-weighted | 71.9 | **29.7** |", column headed "Names held") and at InsiderExperiment/progress.md:31-32 and :249-250.
- **Recomputation (if any):** inputs `var/insider_dispersion.db` `centered_excess.book_width` for (hold_sessions 126, weighting value_weighted), n = 2,581, and the rebuilt membership series from `var/insider_corpus.db.event` × `var/insider_market.db.session`; method: arithmetic mean of each width series; results 66.92522278186749 (priced) and 71.90895121014215 (pre-drop, which reproduces `corpus.json` `mean_book_width` exactly); tolerance 1e-9.
- **What would resolve it:** stating the priced width beside the membership width — "holds a mean of 71.9 names of which 66.9 are priced on an average session, and behaves like 29.7 effective names" — or labelling the 15.6 column "Names in the book before the mid-hold universe drop".
- **Confidence:** HIGH — both figures are recomputed from stored primitives and the two code paths that produce them are three lines apart in the same function.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no. ADR-009 (DECISIONS.md:258-280) discloses the mid-hold drop and its 13,750 name-sessions, and Section 15.1 correctly labels 71.9 as the corpus-side mean book width. Nothing states that the width and the effective-names figure are computed on different books, and Section 17.3 presents them as one sentence about one book.

### DRAFT-V-4
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 17.4 / ADR-011, the equal-weighted secondary
- **Direction:** neutral — the true figures make the secondary's book *less* collapsed, not more
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "On the identical names, the equal-weighted book holds **71.9 and behaves like 66.9**, with tracking error of **6.86 percent** and an MDE of **34.29 bp per month, which would have fired DEGRADED**." — InsiderExperiment/REGISTRATION.md:852-854
- **Evidence:**
  - The 6.86 %, the 34.29 and the DEGRADED branch all verify exactly (recomputed 6.8556 % and 34.2897; 20 < 34.2897 ≤ 40 at InsiderExperiment/src/insider/section0.py:62). This finding concerns only the "**71.9 and behaves like 66.9**" pair.
  - For an equal-weighted book, inverse Herfindahl **is** the name count by construction (`_effective_names` at InsiderExperiment/src/insider/portfolio/returns.py:118-124 with `raw = np.ones(len(names))` at returns.py:101). So the effective-names figure for the EW series can only equal the mean **priced** width.
  - It does, to six decimals: `portfolio.json[3].diagnostics.book_effective_names` = **66.925223** (InsiderExperiment/reports/stage_a1/portfolio.json), and the mean of `book_width` for (126, equal_weighted) in `var/insider_dispersion.db` is **66.92522278186749** over n = 2,581. The agreement is exact, not coincidental.
  - Therefore the equal-weighted book **holds 66.93 names and behaves like 66.93 names**. The stated "71.9 → 66.9" implies a ~7 % concentration effect inside an equal-weighted book, which cannot exist.
  - The same claim is asserted more strongly at InsiderExperiment/REGISTRATION.md:863 ("Both books hold 71.9 names.") and InsiderExperiment/progress.md:42 ("holds the identical 71.9 names") and :252-253 ("holds the same 71.9 names").
  - Both 126-session rows of `portfolio.json` do carry `book_width_mean 71.909` and identical `dropped` maps, so the *membership* claim that the two books hold the same names is true; it is the pairing of that width with the effective-names figure that is not.
- **Recomputation (if any):** inputs `var/insider_dispersion.db` `centered_excess.book_width` for (126, equal_weighted), n = 2,581 (UNANCHORED, read 2026-09-04 18:22 and 18:26 UTC), against `reports/stage_a1/portfolio.json[3].diagnostics.book_effective_names`; method: arithmetic mean vs the stored diagnostic; result 66.92522278186749 vs 66.925223; tolerance 1e-6 — they agree.
- **What would resolve it:** restating as "the equal-weighted book prices 66.9 names on an average session and behaves like all 66.9 of them, against the value-weighted book's 29.7", which is a sharper statement of the same point.
- **Confidence:** HIGH — the identity is forced by the code and confirmed numerically to six decimals.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no.

### DRAFT-V-5
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the "cost, measured rather than asserted" record and the ETA-against-actual table
- **Direction:** neutral (process record; no hypothesis figure depends on it)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Cost, measured rather than asserted.** The commit record puts Stage A.1 at about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about 20 minutes." — InsiderExperiment/progress.md:115-117
- **Evidence:**
  - The eight "Actual" entries in the table at InsiderExperiment/progress.md:198-205 read 5, 10, 4, 4, 14, 20, 32 and 22 minutes. They sum to **111 minutes**, against the 51 minutes claimed at progress.md:116 for the same stage. n = 8 task rows.
  - The table header at InsiderExperiment/progress.md:192-194 states "Timings are wall clock, session start 18:20 UTC, boundaries taken from commit timestamps where one exists", so the actuals are asserted to partition the same interval.
  - The commit record (`git log --date=iso-strict`, live repo, read 2026-09-04 18:21 UTC): `fbfc74e` 2026-08-25T18:34:56−07:00, `398755b` 18:38:50, `ccc9b13` 18:47:16, `cb17046` 19:11:45, `672b343` 19:11:45, `d8b81f1` 19:11:55, `12d9fd3` 23:24:15. Wall clock 18:20 → 19:11:55 is **51.9 min**.
  - Three of the eight actuals cannot come from commit boundaries: tasks 5, 6 and 7 claim 20 + 32 + 22 = **74 minutes** but sit across `cb17046`/`672b343` (identical timestamp, Δ = 0 s) and `d8b81f1` (Δ = 10 s). The interval `ccc9b13` → `d8b81f1` is 24 min 39 s in total.
  - Task 4's actual (14 min) also exceeds its commit interval `398755b` → `ccc9b13` (8 min 26 s).
  - The Z.1 figure is separately unsupported: the gap from the last A.1 commit (19:11:55) to the Z.1 commit (23:24:15) is **4 h 12 min**, not the "about 20 minutes" stated at progress.md:116-117.
- **Recomputation (if any):** inputs the eight Actual cells at InsiderExperiment/progress.md:198-205 and the seven commit timestamps from `git -C /home/kiros-li/Documents/GitHub/InsiderExperiment log --format='%h %ad' --date=iso-strict`; method: sum the column, difference consecutive commit times; results 111 min against 51.9 min of wall clock, and 74 min of claimed task time across 24 min 39 s of commit interval; tolerance ±1 min.
- **What would resolve it:** either marking the per-task actuals as estimates rather than commit-derived, or reconciling the column to the 51.9-minute interval it says it partitions.
- **Confidence:** HIGH — both sides are read directly, one from the document and one from git objects.
- **Invalidated by later commits?:** no — closed repository; `12d9fd3` is the tip.
- **Disclosed by authors?:** partly. progress.md:117-119 discloses that the Z.1 brief's five-hour figure "cannot be confirmed" by the commit record, which is a disclosure about the *brief's* number. It does not disclose that the document's own ETA table contradicts the document's own 51-minute figure by a factor of more than two, nor that the "about 20 minutes" for Z.1 sits against a 4 h 12 min commit gap.

### DRAFT-V-6
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the registration-freeze rule and Section 16
- **Direction:** neutral (process; no measured number changed)
- **Class:** PROCESS
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "None in force. Section 0 fired BLOCKED, so no amendment can authorize Stage B." — InsiderExperiment/REGISTRATION.md:800 (read against "Changing a registered value after that commit requires a numbered amendment in Section 17 carrying its own evidence." — InsiderExperiment/REGISTRATION.md:8-9)
- **Evidence:**
  - `git diff fbfc74e 12d9fd3 -- src/insider/config.py` (live repo, read 2026-09-04 18:25 UTC) is exactly two deletions: the field declaration `benchmark_id: str` and its registered value `benchmark_id="U-LIQ-500-VW"`. Nothing else in the frozen configuration moved between the first commit and the anchor.
  - `git log -S 'benchmark_id' -- src/insider/config.py` places the removal in **`672b343`, 2026-08-25T19:11:45−07:00** ("test: 106 tests green, and five registered mutations…").
  - That is **after** the corpus was built (`ccc9b13`, 18:47:16; corpus_gate evidence records 18:42:24 and 18:45:27) and **after** the power gate fired (first `power_gate` evidence record 18:51:14 local, `ledgers/evidence.jsonl`, read 2026-09-04 18:24 UTC). A registered value was therefore removed with the verdict already visible.
  - No numbered amendment exists: Section 16 is the quoted "None in force", and Section 17 contains no amendment, only the closure.
  - The likely mechanism is visible in the same commit: `benchmark_id` had **no enforcement site anywhere** at `fbfc74e` (`git grep -n benchmark_id fbfc74e -- src tests scripts` returns only the declaration and the value in `config.py`), and `672b343` is the commit that introduced `tests/test_guards.py::test_every_config_field_has_an_enforcement_site` (mutation 5 in `reports/stage_a1/mutations.json` targets exactly that guard). The registered field was deleted to satisfy the new guard rather than amended.
  - Consequence for the record: Section 5's benchmark is prose only after that commit (InsiderExperiment/REGISTRATION.md:351-357), and that prose is itself ambiguous — "The value-weighted return of the full universe at the same weighting basis as the portfolio" — where the code implements the second clause (`returns.py:202` passes the series' own weighting into the benchmark), so the equal-weighted series is benchmarked against an equal-weighted universe (`portfolio.json[3].diagnostics.bench_weight_top1_share` = 0.002 = 1/500 against 0.070165 for the value-weighted rows).
- **Recomputation (if any):** none needed — this is a git-object claim. Inputs: `git diff fbfc74e 672b343 -- src/insider/config.py`, `git log -S`, `ledgers/evidence.jsonl` timestamps.
- **What would resolve it:** a numbered amendment in Section 17 recording the removal, its time, and the guard that forced it — which is the procedure REGISTRATION.md:8-9 prescribes and which the repository followed for every other correction (ADR-008, ADR-012, ADR-013).
- **Confidence:** HIGH — the diff, the commit time and the absence of an enforcement site are all directly observable in git objects.
- **Invalidated by later commits?:** no — closed repository.
- **Disclosed by authors?:** no. ADR-012 (DECISIONS.md:356-374) discloses that the config-enforcement guard was strengthened in the mutation exercise, which is the mechanism, but nothing anywhere records that a registered field was deleted from the frozen configuration as a consequence, and Section 16 asserts the opposite.

### DRAFT-V-7
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** Section 15.2, "three facts this table settles"
- **Direction:** neutral (hygiene)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The strict ten-percent-owner reading, registered in Section 3.3, cost **46,706** officer-or-director purchases. That is 51 percent of all role rejections and roughly ten times the surviving corpus." — InsiderExperiment/REGISTRATION.md:652-654
- **Evidence:**
  - `reports/stage_a1/corpus.json` `attrition` gives the four role-rejection sub-reasons: `filtered_role/tenpercentowner` 46,958; `filtered_role/tenpercentowner_also_titled` **46,706**; `filtered_role/roles_other` 32,536; `filtered_role/roles_none` 5,022. Total **131,222**, matching the printed funnel row at InsiderExperiment/REGISTRATION.md:623.
  - 46,706 / 131,222 = **35.59 %**, not 51 %.
  - The narrowest defensible denominator — ten-percent-owner rejections only, 46,958 + 46,706 = 93,664 — gives 46,706 / 93,664 = **49.87 %**, which rounds to 50, not 51.
  - No denominator in the artifact yields 51 %: it would require a base of 91,580.
  - The companion figure in the same sentence verifies: 46,706 / 4,585 = **10.19**, "roughly ten times the surviving corpus".
- **Recomputation (if any):** inputs the four `filtered_role/*` keys of `reports/stage_a1/corpus.json`; method: ratio against each candidate denominator; results 35.59 % and 49.87 %; tolerance 0.5 pp.
- **What would resolve it:** replacing "51 percent of all role rejections" with "36 percent of all role rejections" or "half of all ten-percent-owner rejections", whichever was meant.
- **Confidence:** HIGH — the arithmetic is unambiguous and the artifact is tracked at the anchor.
- **Invalidated by later commits?:** no — closed repository; the `filtered_role/*` counts are identical in the pre-fix `ccc9b13` artifact, so this is not a staleness artifact.
- **Disclosed by authors?:** no.

### DRAFT-V-8
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** ADR-002, the route decision
- **Direction:** neutral (hygiene)
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "They are the SEC's parse of the same XML documents, published free, in 53 files totalling about 750 MB." — InsiderExperiment/DECISIONS.md:57-58
- **Evidence:**
  - `ledgers/fetch.jsonl` (684 records, untracked and UNANCHORED, read 2026-09-04 18:24 UTC) holds 53 `wire` records whose URL contains `form345`, i.e. the 53 quarterly DERA zips. Their `bytes_read` sum to **570,492,991 bytes = 570.5 MB (544 MiB)**, not ~750 MB. n = 53.
  - The 2.78 GB total the repository reports elsewhere is dominated by a different route: the 53 full-index responses account for **2,207,515,405 bytes**, the 82 per-filing XML documents 458,435 bytes, the 25 submissions responses 4,018,868 bytes, and one `company_tickers.json`. The four groups plus the DERA zips sum to the verified 2,783,280,665 bytes.
  - Every one of the 684 records carries status 200 and the on-disk cache is exactly 2,783,280,665 bytes across exactly 214 files (`du -sb cache/edgar`, read 2026-09-04 18:28 UTC), so `bytes_read` is the delivered body size and not an estimate.
- **Recomputation (if any):** inputs `ledgers/fetch.jsonl`, records with `served_from == "wire"` and `"form345" in url`; method: sum `bytes_read`; result 570,492,991; tolerance exact.
- **What would resolve it:** correcting "about 750 MB" to "about 570 MB", or stating explicitly if the 750 MB refers to the uncompressed content of the zips rather than the download, which the ledger cannot measure.
- **Confidence:** MEDIUM — the download figure is exact, but "750 MB" could plausibly have been intended as an uncompressed or a published-catalogue figure, neither of which any stored artifact records.
- **Invalidated by later commits?:** no — closed repository. The ledger is untracked, so the figure is UNANCHORED; its mtime (2026-08-25 19:06:24) falls inside the A.1 session window.
- **Disclosed by authors?:** no.

### DRAFT-V-9
- **Repository / SHA:** InsiderExperiment / `12d9fd36cf055cb10ea67a3fc737e404217bc95a`
- **Hypothesis or artifact:** the scaffold record
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "`make all` runs clean: ruff, ruff format, mypy strict on 56 files, 106 tests." — InsiderExperiment/progress.md:217-218 (the same count is the commit subject of `672b343`, "test: 106 tests green, and five registered mutations that fail the right guard")
- **Evidence:**
  - AST enumeration of the tracked test tree at the anchor gives **96** functions named `test_*` across the ten `test_*.py` files (`test_absence` 7, `test_cluster` 10, `test_cost` 6, `test_edgar` 7, `test_guards` 23, `test_ledger` 5, `test_membership` 9, `test_power` 12, `test_section0` 7, `test_universe_port` 10).
  - Two parametrize decorators expand the collection: `@pytest.mark.parametrize(("mde","expected"), [...8 cases...])` at InsiderExperiment/tests/test_section0.py:16 adds 7, and `@pytest.mark.parametrize("formation", ["2016-04-01","2021-04-01","2026-07-01"])` at InsiderExperiment/tests/test_universe_port.py:87 adds 2. Total collected = 96 + 7 + 2 = **105**.
  - Nothing else can add to the collection: there are no test classes (`grep -n '^class' tests/*.py` returns nothing), `tests/conftest.py` contains only a `sys.path` insertion and no collection hook, and `pyproject.toml:62-64` sets `testpaths = ["tests"]` with `addopts = "-q --strict-markers"` — no `--doctest-modules`.
  - Corroboration from the run's own artifact: `reports/stage_a1/mutations.json` `final_suite` is a pytest progress line of **33 dots** padded to 79 columns before `[100%]`. On an 80-column terminal the preceding full line holds 72 dots, giving 72 + 33 = **105**.
  - The tracked test tree is byte-identical from `672b343` to the anchor (`git diff --stat 672b343 12d9fd3 -- tests/ src/ scripts/` is empty), so the claim and the count refer to the same code.
- **Recomputation (if any):** inputs `SNAP/InsiderExperiment/tests/*.py`; method: `ast.parse`, count `FunctionDef` nodes whose name starts with `test_`, add `len(elts) - 1` for each `parametrize` decorator's literal case list; result 105; tolerance exact. pytest itself was **not** run — the audit venv has no pytest and installing into or running inside the audited repository is out of scope.
- **What would resolve it:** a `pytest --collect-only -q` count run by the author, or correcting 106 → 105.
- **Confidence:** MEDIUM — the AST enumeration is complete for every collection mechanism this suite uses and is independently corroborated by the stored progress line, but pytest was not executed, so a collection subtlety cannot be ruled out entirely.
- **Invalidated by later commits?:** no — closed repository, and the test tree is unchanged from the commit that made the claim.
- **Disclosed by authors?:** no. `reports/stage_a1/mutations.json` `final_suite` does not evidence a pass count either way — it captured a progress line rather than pytest's summary because `summary_line()` (InsiderExperiment/scripts/mutations.py:118-122) fell through to its last-line fallback; the harness's own exit-code check (scripts/mutations.py:178-179) is what actually established that the suite was green.

---

## F. What could not be checked and why

1. **`var/insider_sealed.db` was not opened**, by design. The raw daily excess-return series and
   therefore the realized alpha remain unread by this audit, as they were by the experiment.
   Consequence: the audit can confirm that the dispersion store is centered (the four series sum
   to ≤ 3e-16) and that no first-moment field exists on the power path, but it cannot confirm
   that the centered series is the centering of *that particular* sealed series. That would
   require opening the seal, which would destroy the property being audited.
2. **`AiTrader/analysis_bars.db` SHA-256** cannot be re-verified. The file is 7,323,656,192 bytes
   with mtime 2026-09-03 against `port.json`'s recorded 7,320,629,248; the AiTrader collector has
   written to it since 2026-08-25. Its failure to reproduce today is **not** evidence against
   InsiderExperiment. `backtest/universe.py` does still hash to the recorded value.
3. **The three-formation universe port check** (`tests/test_universe_port.py:87`, ADR-004's "500
   of 500 members reproduced exactly at each") was not re-executed. What was verified is the
   stored side: all 124 formations in `var/insider_market.db` carry exactly 500 members. The
   comparison against AiTrader's own store would require running repository code against the
   audited AiTrader tree.
4. **mypy's own file count** ("56 files") cannot be reproduced without running mypy. The three
   configured roots hold 57 `.py` files (43 + 11 + 3); 56 if `tests/conftest.py` is excluded.
5. **The "on the order of two million Form 4 documents" premise** in ADR-002 is not derivable
   from any stored artifact. `validation.json` gives 2,440,873 Form 4 documents across **all**
   issuers over the 53 quarters; nothing counts documents restricted to universe issuers, and
   the universe holds 1,218 distinct symbols across 124 formations. The *arithmetic* on the
   stated premise (2 M / 8 per second = 69.4 h) is correct.
6. **Every cross-repository figure** — NPDExperiment's 0.0512, 415 days, 6.9378 USD and
   427 → 125.6 effective days; HFExperiment's z 1.668 against a 2.50 bar and 42–66 % tracking
   error; P26's 19,648 trades at −1.97 bp; and "eight price-based and signal-based hypothesis
   families … zero positives" — is READ-only here and needs its source repository.
7. **Every literature figure** — Cohen–Malloy–Pomorski's 82 bp per month and its "roughly 30 to
   40 bp on 2008 to 2024" decayed replication, Ozlen–Batumoglu's 70–80 % dissipation, the 30 %
   annualized sigma used in Section 0.4 — is external. The decayed 30–40 bp band is the number
   the BLOCKED floor of 40 was placed against (`REGISTRATION.md:57-59`), so it is load-bearing
   and unverifiable inside this repository. The whole closure is conditional on it.
8. **P9's systemd claim** is verifiable only as of today (no unit, timer or cron entry matches
   `insider` at 2026-09-04 18:30 UTC). The host state on 2026-08-25 cannot be reconstructed.
9. **All figures drawn from `var/`, `ledgers/` and `cache/` are UNANCHORED.** Those paths are
   gitignored and sit outside the anchored SHA. Every one was read on 2026-09-04 between 18:20
   and 18:31 UTC; every observed mtime falls inside the 2026-08-25 18:35–19:10 session window,
   which is consistent with them being the artifacts the anchored reports were written from, but
   that is corroboration and not proof.

---

## G. Live-repository access log

Purpose of access, both permitted kinds only: (1) git history and provenance — `log`, `show`,
`diff`, `grep <rev>`, `rev-parse`; (2) untracked or gitignored data that exists only in the
working tree — `var/insider_corpus.db`, `var/insider_dispersion.db`, `var/insider_market.db`
(all opened read-only via `file:…?mode=ro` URIs), `ledgers/fetch.jsonl`,
`ledgers/evidence.jsonl`, `cache/edgar` sizes and file counts only, and `reports/` mtimes.
`var/insider_sealed.db` was **not** opened. `.env` was **not** opened. No file in an audited
repository was opened for writing. No repository script was copied or executed. All computation
ran under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/agentC/insider`
with the audit venv.

Outside this repository, read-only and for the boundary claim only:
`ls -la` and `sha256sum` on `~/Documents/GitHub/AiTrader/backtest/universe.py`, and `ls -la` on
`~/Documents/GitHub/AiTrader/analysis_bars.db`. No other AiTrader path was touched and
`news_experiment.db` was not opened.

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` before first
access — 2026-09-04T18:20:55Z:**

```
```
(empty output, exit 0 — clean working tree)

**`git -C /home/kiros-li/Documents/GitHub/InsiderExperiment status --porcelain` after last
access — 2026-09-04T18:30:48Z:**

```
```
(empty output, exit 0 — clean working tree, unchanged. Nothing was modified.)

Untracked-but-ignored entries present at both reads (`git status --ignored --porcelain`):
`.env`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/`, `.venv/`, `_CLOSED_DO_NOT_RUN_HERE`,
`cache/`, `ledgers/`, `var/`, and eight `__pycache__/` directories. Identical to the set recorded
in the LOCATE inventory. `_CLOSED_DO_NOT_RUN_HERE` is excluded via `.git/info/exclude`, is dated
2026-09-02 — **after** the anchor — and records that a session was opened in this closed
repository by mistake. It is not an experiment artifact and it is not on COMMON_RULES' list of
pre-existing dirt; it is reported here again for the record. No other unexpected entry appeared.
