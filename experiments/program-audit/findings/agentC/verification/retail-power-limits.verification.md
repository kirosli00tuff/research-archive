# retail-power-limits — verification (Agent C, VERIFY)

Repository: `retail-power-limits`
Anchored SHA: `dda39b2f148569a6fe9be956a979471b2330611d` (main, 2026-08-29)
Read from: `SNAP/retail-power-limits/` plus the sibling snapshots and read-only sibling git history.
Work dir: `/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC-verify/`

## What this repository is, and what "verify" therefore means

`retail-power-limits` computes nothing. `rplimits/` is a frozen registry of quoted strings
(`cases.py`), a citation registry (`sources.py`), four markdown builders (`render.py`) and a
marker-block writer (`docsync.py`). There is no data, no estimator, no analysis code. **Every
numeric claim is a transcription claim**, so verification means going to the sibling repository at
the commit `rplimits/sources.py` names and comparing.

That is what was done. All 24 citations were resolved in the live sibling repositories, every
MUST-VERIFY figure was recomputed from the sibling's own stored primitives where they exist, and
the repository's own arithmetic (the 411-minute sum, the census, the shortfalls, the ratios) was
recomputed independently.

**Headline result: the transcription is overwhelmingly accurate.** All four deciding numbers
(0.0512, 49.35 bp/month, 163-vs-300, z 1.668) reproduce exactly from the primary records; all 24
citations resolve; every cited file is byte-identical between the cited commit and the sibling's
anchored SHA (zero drift); all four "Closure language, exact." quotations and all eight quoted
commit subjects are verbatim; the one figure the repository declares derived (411 minutes) is
correct and its exclusion note is correct. Seven discrepancies were found. One is substantive
(the NPDExperiment achieved-sample figure); the rest are hygiene- or characterisation-grade.

---

## A. Claims table

Tolerance convention: "±1 ulp of the stated rounding" means the recomputed value rounds to the
stated value at the stated number of significant figures.

| # | claim (short) | file:line | stated | source of truth | recomputed | tol | status |
|---|---|---|---|---|---|---|---|
| C-01 | NPD realized MDE | `retail-power-limits/docs/the-power-limit.md:72`; `README.md:20`; `SOURCES.md:38`; `rplimits/cases.py:95,405` | 0.0512 | `NPDExperiment/reports/stage_b2/evaluation.md:81,93` (bootstrap SE 0.02562) + `NPDExperiment/src/npd/eval/evaluator.py:544` (`realized_mde = t_critical * se`) + `src/npd/config.py:119` (`t_critical=2.0`) | 2.0 × 0.02562 = **0.05124 → 0.0512** | 4 dp | **VERIFIED** |
| C-01b | NPD effect band | `SOURCES.md:34`; `cases.py:89-92` | 0.01 to 0.05, registered in Section 9.2 | `NPDExperiment/REGISTRATION.md:247` ("Realistic effect band from the literature: 0.01 to 0.05", inside §9) | identical | exact | **VERIFIED** |
| C-01c | NPD pre-registered projection | `SOURCES.md:38`; `cases.py:96` | 0.026 to 0.047 | `NPDExperiment/REGISTRATION.md:233-236` grid, detect column 0.0469 … 0.0257 | 0.0257→0.026, 0.0469→0.047 | 2 sf | **VERIFIED** |
| C-01d | NPD realized sd vs registered assumption | `SOURCES.md:38`; `cases.py:96-97` | 0.36339 against "at most 0.2626" | `NPDExperiment/progress.md:42`; `REGISTRATION.md:233` (corr 0.00 cell = max of grid) | identical; 0.2626 is the grid maximum | exact | **VERIFIED** |
| C-02 | Insider realized MDE | `SOURCES.md:86`; `docs/the-power-limit.md:73,92,208`; `README.md:21`; `cases.py:146,172,412` | 49.35 bp/month vs BLOCKED floor 40 | `InsiderExperiment/REGISTRATION.md:712,718-719`; §0.4 identity `MDE_month = t*M*s_d/sqrt(N_eff)` at `REGISTRATION.md:84-88` | TE 9.993 %/√12 = 288.47 bp monthly; N_eff months = 2869.9/21 = 136.662; SE = **24.676 bp**; ×2.0 = **49.353 → 49.35** | 4 sf | **VERIFIED** |
| C-02b | Insider BLOCKED floor 40 / GO 20 | `cases.py:147`; `SOURCES.md:70` | 40 BLOCKED, 20 GO, committed before the measurement | `InsiderExperiment/REGISTRATION.md:41-46` at `fbfc74e` and unchanged at `cb17046` (`git diff fbfc74e cb17046 -- REGISTRATION.md` touches nothing before line 157) | identical at both commits | exact | **VERIFIED** |
| C-03 | ETF closure comparison | `SOURCES.md:122`; `docs/the-power-limit.md:138-139`; `DECISIONS.md:102-104`; `cases.py:235-236` | 163 projected vs 300 governing at 2027-03-31 | `ETFExperiment/REGISTRATION.md:984-986,1010-1015` (Amendment 5); `DECISIONS.md:528`; `HYPOTHESES.md:70`; `progress.md:486-487` | identical | exact | **VERIFIED** |
| C-03b | ETF census | `SOURCES.md:106`; `cases.py:206-210` | 336 rows = 11 + 53 + 243 + 25 + 3 + 1 | `ETFExperiment/report.md:260-269` | 11+53+243+25+3+1 = **336** | exact | **VERIFIED** |
| C-04 | HF inherited resolution | `docs/the-power-limit.md:75`; `README.md:23`; `SOURCES.md:134`; `cases.py:257-259,426` | z 1.668, bar 2.50, needed 104.0 %/yr, delivered 70.5, shortfall 1.5× | `AiTrader/RETURN.md@f819b68:2857` (`+27.99 [-4.9, +60.9] (1.668)`, TE 66.4%), `:2899` (`66.4 / 104.0 / 70.5 / 1.5x`), `:2844` | delivered = 27.99 bp × 252 = **70.53 %/yr**; needed = 66.4 × 2.50 / √2.55 = **103.95 → 104.0**; shortfall 104.0/70.5 = **1.475 → 1.5×** | 1 dp | **VERIFIED** |
| C-05 | The progression clock | `docs/the-power-limit.md:211-214` | 13:26:58 → 18:34:56 (5 h 08 m) → 23:24:15, "under ten hours" | `git -C NPDExperiment log -1 2d3d0ae` and `git -C InsiderExperiment log -1 fbfc74e/12d9fd3`; `rev-list --max-parents=0` confirms `fbfc74e` is the first commit | gap1 = **5 h 07 m 58 s**; total = **9 h 57 m 17 s** | round-up of 2 s | **VERIFIED** |
| C-06 | The one derived figure | `DECISIONS.md:184-186`; `SOURCES.md:292-300`; `cases.py:112` | 411 min = 22+34+68+52+194+41, excludes Z.1 | `NPDExperiment/progress.md:110,186,234,267,298,331` (the six "Actual: N minutes" lines) and the absence of any timing line in §Z.1 | sum = **411**; six stages are the complete timed set; Z.1 is untimed | exact | **VERIFIED** |
| C-07 | NPD effective-sample base | `SOURCES.md:42`; `cases.py:100-104` | "404 evaluable days; 125.6 independent-equivalent days after the 3.4 variance inflation" as *sample achieved* | `NPDExperiment/reports/stage_b2/evaluation.md:92` (**achieved effective sample size 201.2**); `REGISTRATION.md:227` (125.6 is the pre-collection projection off **427**) | 427/3.4 = 125.59 (projection); **404/3.4 = 118.8 ≠ 125.6**; achieved N_eff = (0.36339/0.02562)² = **201.2** | 1 dp | **CONTRADICTED** — see DRAFT-V-1 |
| C-08 | HF width-widening | `SOURCES.md:134`; `cases.py:259-261` | TE 66.4→31.7, excess 27.99→10.04, z 1.668→1.455 | `AiTrader/RETURN.md@f819b68:2872,2880` | all four figures identical; AiTrader's own wording is "adds return AND noise in roughly equal proportion, so the z barely moves (1.668 against 1.455)" | exact | **VERIFIED** (transcription). The z pair is Newey-West at 21 lags (`:2852`), not the iid TE ratio, which would give 1.696 / 1.274 — a methodological note, not a discrepancy |
| C-09 | ETF Amendment 6 triple | `docs/the-power-limit.md:132-139`; `SOURCES.md:122`; `cases.py:230-236` | 845 / above 1,200 / about 302 by 2027-10-31, clears 300 by two days | `ETFExperiment/REGISTRATION.md:978-979,1129-1133` | 291 forward + 11 = 302; 302 − 300 = 2 | exact | **VERIFIED** |
| C-10 | NPD money and calls | `docs/the-power-limit.md:239-240`; `SOURCES.md:50`; `cases.py:112` | 6.9378 USD of a 10.00 cap, 920 billed calls, +2 calibration | `NPDExperiment/progress.md:201-202,104`; `REGISTRATION.md:789` | identical | exact | **VERIFIED** |
| C-11 | Insider corpus and periods | `SOURCES.md:74`; `cases.py:152-154` | 4,585 events / floor 1,000; 2,581 sessions at 99.5 % vs floor 80 %; 2,869.9 effective; VIF 0.899 | `InsiderExperiment/REGISTRATION.md:594-595,712,824-825`; `progress.md:235-240` | 2,581/0.899 = 2,870.97; implied VIF = 2581/2869.9 = **0.89933** → "0.899" | 3 dp | **VERIFIED** |
| C-12 | Insider weight concentration | `docs/the-power-limit.md:96-97`; `SOURCES.md:78`; `cases.py:158-161` | 71.9 names behaving like 29.7; top 14.9 %, top-5 33.8 %; ~23 effective names required; 9.993 % TE is the whole of the 49.35 | `InsiderExperiment/REGISTRATION.md:749,755-756,112` (23.4 names at the BLOCKED floor), `:844-846` | identical; "about 23" is 23.4 | 2 sf | **VERIFIED** |
| C-13 | Insider Newey-West robustness | `SOURCES.md:70`; `cases.py:148` | 50.19 @ lag 5, 49.11 @ lag 63, 49.53 @ lag 126 | `InsiderExperiment/REGISTRATION.md:721-722` | identical (the registered lag 21 value, 49.35, is the headline and is correctly not re-listed) | exact | **VERIFIED** |
| C-14 | Insider equal-weighted secondary | `docs/the-power-limit.md:227-229,388-390`; `cases.py` (via `DECISIONS.md`) | would have landed at 34.29 bp and fired DEGRADED | `InsiderExperiment/REGISTRATION.md:715,764,852-853`; `progress.md:242` | identical | exact | **VERIFIED** |
| C-15 | Insider universe scope | `SOURCES.md:90`; `cases.py:179-180` | 94.2 % of qualifying-shaped purchases outside the liquid-500 band | `InsiderExperiment/REGISTRATION.md:778,893` | identical | exact | **VERIFIED** |
| C-16 | NPD coverage | `SOURCES.md:42`; `cases.py:100-102`; `docs/the-power-limit.md:130` | 415 of 432, 96.1 % vs a 90 % bar | `NPDExperiment/progress.md:190-191,195`; `REGISTRATION.md:83` | 415/432 = **96.065 % → 96.1** | 1 dp | **VERIFIED** |
| C-17 | NPD mechanism | `docs/the-power-limit.md:169-176` | grid 0.026–0.047 over corr 0.0–0.7; realized 0.0512 outside it; sd at 98 % of the corr −1 maximum | `NPDExperiment/REGISTRATION.md:231-236,732-735` | max sd = √(2·(1−(−1)))·(1/√29) = **0.37139**; 0.36339/0.37139 = **97.85 % → 98** | 2 sf | **VERIFIED** |
| C-18 | NPD sample required | `SOURCES.md:46`; `cases.py:106-108` | ~4× the evaluable days, near 1,700; window accrues ~21 trading days/month | `NPDExperiment/progress.md:51-55`; `REGISTRATION.md` §Closure | 4×427 = 1,708; 4×415 = 1,660; 4×404 = 1,616 — "near 1,700" fits the 427 base | 2 sf | **VERIFIED** |
| C-19 | ETF capture density | `docs/the-power-limit.md:103-104`; `SOURCES.md:106` | 11 of 333 = 3.30 % vs a registered 60 % bar | `ETFExperiment/report.md:187,438`; `REGISTRATION.md:728,865,1062`; `progress.md:150` (the 60 % PASS rule) | 11/333 = **3.3033 % → 3.30** | 2 dp | **VERIFIED** |
| C-20 | ETF required N and shortfalls | `SOURCES.md:102,110`; `cases.py:200-203,215-217` | E1 237 / 845; E2 300 / >1,200; governing 300; shortfalls 137 and 74 | `ETFExperiment/REGISTRATION.md:978-979,1014-1015`; `HYPOTHESES.md:70` | 300−163 = **137**; 237−163 = **74** | exact | **VERIFIED** |
| C-21 | ETF cost | `SOURCES.md:114`; `cases.py:220-222` | zero dollars, no credential, 220 charged requests, no outcome value read | `ETFExperiment/progress.md:514,564,602`; `REGISTRATION.md:1160`; `README.md@fe60a22:7-10` | identical | exact | **VERIFIED** |
| C-22 | AiTrader raw outperformance | `docs/the-power-limit.md:110-114` | 90.3 %/yr vs benchmark 19.7, "the largest that project ever measured" | `AiTrader/RETURN.md@f819b68:2844,2857` | 90.3 / 19.7 identical; the superlative is AiTrader's own sentence ("the largest raw outperformance this project has ever measured") | exact | **VERIFIED** (as a quotation; the superlative itself is AiTrader's claim, not independently checked over AiTrader's whole register) |
| C-23 | HF forward schedule | `SOURCES.md:142`; `cases.py:269-273`; `docs/the-power-limit.md:114-116` | lower bound clears zero at day 2,061, the 4.07 bp/day hurdle at day 2,852, "eight to eleven years" | `HFExperiment/REGISTRATION.md@f13e1d3:249,261` (§11) | 2061/252 = **8.18 yr**; 2852/252 = **11.32 yr**; the phrase "Eight to eleven years" is HF's own | exact | **VERIFIED** |
| C-24 | solattn primary | `SOURCES.md:184`; `cases.py:337-339`; `docs/the-power-limit.md:297-301` | lift −1.0779, 95 % day-clustered bootstrap [−3.3354, +0.0204], n = 12,798 / 2,107 / Q5 412 | `solattn/FINDINGS.md:98-102` | identical | exact | **VERIFIED** |
| C-25 | MLCryptoEngine cost margins | `SOURCES.md:172`; `cases.py:311-317` | AUC 0.9432, 0.0291 bps, 50 bps → ~1,700×; 3 bps → ~100×; H4 300–550 bps → 100–180× | `MLCryptoEngine/docs/notes/h1-…md@ae03bf6:39,54,77,80-84`; `HYPOTHESES.md@d2a0f05:102,282-283` | 50/0.0291 = **1,718**; 3/0.0291 = **103.1**; 300/3 = 100, 550/3 = **183.3** → "100 to 180×" (MLC's own phrase) | 2 sf | **VERIFIED** |
| C-26 | solclear figures | `SOURCES.md:192,196`; `cases.py:353-367` | 18 cleared vs floor 20 at 30 d, 4 at 90 d; 4,695,489 vs 124,764 = 37.6×; survivorship "60 points at 30 days and 79 at 90"; 97.5 % vs 18.75 % | `solclear/FINDINGS.md@c692032:73,297-299,109,122-123` | 4,695,489/124,764 = **37.635 → 37.6×** ✔; **30 d gap = 97.5 − 18.75 = 78.75**; **90 d gap = 100 − 40 = 60.0** — the two horizon labels are swapped | 1 dp | **CONTRADICTED** on the survivorship gap labels — see DRAFT-V-2; the rest VERIFIED |
| C-27 | Insider cost, time and wire | `SOURCES.md:82`; `cases.py:165-167`; `docs/the-power-limit.md:241` | zero dollars; 214 wire requests, 2.78 GB, zero non-200; ~51 min A.1 and 20 for Z.1 "by the commit record"; alpha sealed | `InsiderExperiment/REGISTRATION.md:828`; `progress.md:24-25,115-120` | every figure identical; **but the sibling records a competing Z.1 figure of five hours in the same paragraph and says "Both are recorded rather than one being picked"** | exact | **VERIFIED as transcribed**, but selective — see DRAFT-V-4 |
| C-28a | Self-report: source files | `progress.md:59,68` | "11 source files" | `find` over the anchored tree, mypy scope `files = ["rplimits","tests"]` | **11** `.py` files (6 in `rplimits/`, 5 in `tests/`) | exact | **VERIFIED** |
| C-28b | Self-report: tests | `progress.md:59,68` | "111 tests passing" | pytest collection on a scratch copy of the anchored tree, run with the repository's own pinned pytest | **112 tests collected** (test_sources 74, test_cases 19, test_honesty 10, test_render 9) | exact | **CONTRADICTED** by one — see DRAFT-V-6 |
| C-29 | "about ninety figures from seven repositories" | `DECISIONS.md:35-36` | ~90 figures, 7 repositories | no counting convention is stated anywhere | the note carries **115 distinct numeric tokens**; `cases.py` Figures carry 133 distinct numeric tokens; `sources.py` cites **8** distinct repositories | n/a | **UNVERIFIABLE** on "ninety" (no stated counting rule; it is an undercount, not an overstatement). **CONTRADICTED** on "seven" — see DRAFT-V-5 |
| C-30 | "four of the seven … are local-only" | `progress.md:113-116`; `SOURCES.md:262-271`; `docs/the-power-limit.md:44-52` | NPD, Insider, ETF, HF have no remote | `git remote -v` in each, read 2026-09-04T00:18:21Z | **all four now carry `https://github.com/kirosli00tuff/<repo>.git`**; `.git/config` mtimes are 2026-08-29 11:45 local, ~11½ h after this repository's last commit (00:21) | n/a | **CONTRADICTED as of the read date; TRUE at the anchor** — see DRAFT-V-3 |
| P-02 | Gate committed in the first commit | `docs/the-power-limit.md:218-224`; `sources.py:86` | `fbfc74e` is the first commit, subject as quoted, bars 20/40 with the boundary convention, before any corpus | `git rev-list --max-parents=0` = `fbfc74e`; `git show fbfc74e:REGISTRATION.md:41-46`; `git ls-tree -r fbfc74e` (source only, no `var/`, no corpus) | all four conditions hold | exact | **VERIFIED** |
| P-06 | Floor precedes the measurement, unchanged | `cases.py:147`; `SOURCES.md:70` | `fbfc74e` precedes `cb17046`, 40 bp unchanged between them | commit times 18:34:56 → 19:11:45 (−07:00); `git diff fbfc74e cb17046 -- REGISTRATION.md` adds only text after line 157 | holds | exact | **VERIFIED** |
| P-08 | Structural separation by import guard | `docs/the-power-limit.md:200-206` | the power package is forbidden by import guard from portfolio/market/evaluation | `InsiderExperiment/tests/test_guards.py:170-187` — AST walk, `forbidden = ("insider.portfolio","insider.market","insider.eval")` | present exactly as described, enforced by a test | exact | **VERIFIED** |
| P-10 | HF §11 registered 2026-08-23 | `docs/the-power-limit.md:266-269` | §11 priced the forward verdict before the operator proceeded | earliest commit whose `REGISTRATION.md` contains "2,061" is `a8f4b0d`, 2026-08-23T21:40:25−07:00; `REGISTRATION.md@f13e1d3:58` "Sections 1 through 12 registered 2026-08-23" | holds | exact | **VERIFIED** |
| P-11 | All 24 hashes resolve; no drift | `SOURCES.md:8-9,279-282`; `sources.py:11-13` | closed repositories, stable short hashes | scripted `rev-parse` + `cat-file -e` over all 24 entries; plus `git diff <cited> <anchor> -- <path>` for every cited file whose commit differs from the sibling anchor | **24/24 resolve; every named path exists; all 8 quoted commit subjects are verbatim; every cited file is byte-identical between the cited commit and the sibling's anchored SHA** | exact | **VERIFIED** |
| P-13 | HF closed by operator decision | `DECISIONS.md:125-129`; `cases.py:286-294` | Section 0 BLOCKED on IBKR errors 10243/10244; closed 2026-08-26; shadow never started | `HFExperiment/progress.md:5-9,32-33,248` | holds. (Sibling quirk, not this repository's: the closing commit `f13e1d3` is stamped 2026-08-25T00:45 yet records an instruction dated 2026-08-26.) | exact | **VERIFIED** |
| P-16 | Exactly one derived figure | `DECISIONS.md:184-187`; `SOURCES.md:294-300` | only the 411 minutes is this note's arithmetic | tested against every ratio and difference a verifier could suspect: 137/74 (`ETFExperiment/HYPOTHESES.md:70`), 37.6× (`solclear/FINDINGS.md:299`), 1,700×/100×/100–180× (`MLCryptoEngine`), 1.5× (`AiTrader/RETURN.md:2899`), "eight to eleven years" (`HFExperiment/REGISTRATION.md:261`), 418 bp (`HFExperiment/REGISTRATION.md:256-257`), 96.1 % (`NPDExperiment/progress.md:191`), 302 (`ETFExperiment/REGISTRATION.md:1131`) | **every one is stated by the sibling**, not formed here | exact | **VERIFIED** |
| P-18 | The drift guarantee | `DECISIONS.md:67-76` | `Figure.__post_init__` refuses an unresolvable source; the four generated blocks are re-rendered and compared | `rplimits/cases.py:29-33`; `tests/test_render.py`; suite run on a scratch copy of the anchored tree | mechanism present; **all render/drift tests pass**; the only failure in the copy is `test_the_credential_scan_has_something_to_scan`, which calls `git ls-files` and cannot work outside a work tree — an artefact of my copy, not a repository defect | n/a | **VERIFIED** |
| P-20 | Holdout touched once | `SOURCES.md:138`; `sources.py:170` | commit `a0a9ef6` subject as quoted | `git -C AiTrader log -1 a0a9ef6` | subject verbatim | exact | **VERIFIED** (the "no later commit re-scores it" half was not exhaustively checked — see §F) |

---

## B. Derived quantities table

Every derived quantity recomputable from stored primitives, recomputed independently in
`work/agentC-verify/recompute.py`.

| # | quantity | inputs (file:line) | method | recomputed | stated | agrees |
|---|---|---|---|---|---|---|
| D-01 | NPD stage total | 22, 34, 68, 52, 194, 41 — `NPDExperiment/progress.md:331,298,267,234,186,110` | sum | **411** | 411 (`retail-power-limits/DECISIONS.md:184`) | yes |
| D-02 | ETF census total | 11, 53, 243, 25, 3, 1 — `ETFExperiment/report.md:264-269` | sum | **336** | 336 (`SOURCES.md:106`) | yes |
| D-03 | ETF shortfalls | 300, 237, 163 — `ETFExperiment/REGISTRATION.md:978,984` | subtraction | **137, 74** | 137, 74 (`SOURCES.md:110`) | yes |
| D-04 | NPD coverage | 415, 432 — `NPDExperiment/progress.md:190-195` | ratio | **96.065 %** | 96.1 % | yes |
| D-05 | ETF capture density | 11, 333 — `ETFExperiment/report.md:438` | ratio | **3.3033 %** | 3.30 % | yes |
| D-06 | solclear repricing multiple | 4,695,489, 124,764 — `solclear/FINDINGS.md@c692032:297-299` | ratio | **37.635×** | 37.6× | yes |
| D-07 | MLC Kraken miss | 50, 0.0291 — `MLCryptoEngine/docs/notes/h1-…md@ae03bf6:54,77` | ratio | **1,718×** | "roughly 1,700×" | yes |
| D-08 | MLC Hyperliquid miss | 3, 0.0291 | ratio | **103.1×** | "roughly 100×" | yes |
| D-09 | MLC H4 margin | 300, 550, 3 — `HYPOTHESES.md@d2a0f05:102` | ratio | **100× and 183.3×** | "100 to 180×" | yes (round-down of 183) |
| D-10 | HF daily noise | TE 66.4 %/yr — `AiTrader/RETURN.md:2857` | /√252 | **418.3 bp/day** | "near 418" | yes |
| D-11 | HF excess delivered | 27.99 bp/day | ×252 | **70.535 %/yr** | 70.5 | yes |
| D-12 | HF excess needed at the bar | TE 66.4, bar 2.50, 2.55 yr | TE × bar / √yrs | **103.95 → 104.0 %/yr** | 104.0 (`AiTrader/RETURN.md:2899`) | yes — this resolves the apparent 104.0-vs-105.7 tension: "needed" uses the iid TE identity, while z 1.668 uses Newey-West at 21 lags (`RETURN.md:2852`) |
| D-12b | HF 50-name excess needed | TE 31.7, bar 2.50, 2.55 yr | same | **49.63 %/yr** | "about 49" (`RETURN.md:2880`) | yes |
| D-13 | HF verdict years | 2,061 and 2,852 days | /252 | **8.18 and 11.32 yr** | "eight to eleven years" | yes |
| D-14 | Insider N_eff from VIF | 2,581 sessions, VIF 0.899 — `InsiderExperiment/REGISTRATION.md:712` | division | 2,581/0.899 = **2,870.97**; implied VIF = 2581/2869.9 = **0.89933** | 2,869.9 | yes, within the stated rounding of 0.899 |
| D-15 | Insider MDE from primitives | TE 9.993 %, N_eff 2,869.9, M 21, t 2.0 | `t·(TE/√12)/√(N_eff/M)` | SE = **24.676 bp**, MDE = **49.353 bp** | 24.68, 49.35 | yes |
| D-16 | NPD achieved N_eff | sd 0.36339, bootstrap SE 0.02562 — `NPDExperiment/reports/stage_b2/evaluation.md:81-82` | `(sd/se)²` (`evaluator.py:529`) | **201.18 → 201.2** | 201.2 in the sibling; **125.6 in `retail-power-limits/SOURCES.md:42`** | **no** — DRAFT-V-1 |
| D-17 | NPD MDE if N_eff were 125.6 | sd 0.36339, N_eff 125.6, t 2.0 | `t·sd/√N_eff` | **0.0648** | 0.0512 | **no** — the two Figures in the same `PowerCase` record are mutually inconsistent by a factor of 1.27 |
| D-18 | NPD VIF bases | 3.4, 427, 404 | division | 427/3.4 = **125.59** ✔; 404/3.4 = **118.82** ✘ | 125.6 paired with 404 | 125.6 belongs to the 427 base only |
| D-19 | NPD sample loss to overlap | 125.6/427 (registered) vs 201.2/404 (realized) | 1 − ratio | registered **70.6 %**; realized **50.2 %** | "lost 70 percent" (`docs/the-power-limit.md:379`) | matches the registered projection, not the realized loss — DRAFT-V-8 |
| D-20 | NPD registered floor MDE | 0.185695, 432, t 2.0 — `REGISTRATION.md:212` | `t·sd/√N` | **0.017868** | 0.01787 | yes |
| D-21 | NPD grid cell, corr 0 | 0.2626, 125.6, t 2.0, z.80 0.8416 | detect and 80 %-power MDE | **0.0469 and 0.0666** | 0.0469, 0.0666 (`REGISTRATION.md:233`) | yes |
| D-22 | NPD sd vs theoretical max | 1/√29, corr −1 | `√(2(1−ρ))·sd₁` | max **0.37139**; ratio **97.85 %** | "98 percent of the theoretical maximum of 0.3714" | yes |
| D-23 | Progression gaps | three commit timestamps | subtraction | **5 h 07 m 58 s** and **9 h 57 m 17 s** | "five hours and eight minutes", "under ten hours" | yes (2-second round-up) |
| D-24 | solclear vs NPD gap | 2026-08-14, 2026-08-25 | date difference | **11 days** | "eleven days" | yes |
| D-25 | AiTrader corrected bar | family 4, α 0.05, two-sided | `z(1 − 0.0125/2)` | **2.4977** | 2.50 | yes |
| D-26 | solattn Šidák level | grid 160 cells, α 0.05 | `1 − 0.95^(1/160)` | **0.000321** | 0.000321 (`solattn/REGISTRATION.md:707`) | yes — the level is on the **registered 160-cell grid**, not on the 120 computable cells (which would give 0.000427) |
| D-27 | solclear survivorship gaps | 97.5, 18.75, 100, 40 — `solclear/FINDINGS.md@c692032:122-123` | subtraction | 30 d **78.75**; 90 d **60.0** | "60 points at 30 days and 79 at 90" | **no** — labels swapped, DRAFT-V-2 |
| D-28 | NPD per-call price | 6.9378, 920, 0.007508 — `NPDExperiment/progress.md:201-202` | multiplication | 920 × 0.007508 = **6.907**; 6.9378/920 = **0.0075411** | 6.9378 "at a measured 0.007508 USD each" | ~0.4 % off; a rounding artefact **in the sibling**, faithfully transcribed here |
| D-29 | ETF forward projection from the note's own date | 20.8/month, 2026-08-29 → 2027-03-31, +11 | linear accrual | **157.2** | 163 | the 163 is ETF's "all cohorts" projection (`progress.md:486`), a different base from the "forward-only" 291 that yields 302; not reconcilable from `retail-power-limits` alone, and not a discrepancy in it |
| D-30 | Repository self-count | `git ls-files`, pytest collection | count | **11 `.py` files; 112 tests** | "11 source files, 111 tests" | files yes; tests **no** — DRAFT-V-6 |

---

## C. Intervals table

| # | interval | file:line | estimator actually used (and where established) | level / tail | independence assumed | data structure | reproduces from stored data | status |
|---|---|---|---|---|---|---|---|---|
| I-01 | `[−3.3354, +0.0204]` around −1.0779 | `SOURCES.md:184`; `cases.py:337-339`; `docs/the-power-limit.md:298-300` | 95 % **day-clustered bootstrap**, resampling **3 day-clusters** (birth days 2026-08-16..18); `solattn/FINDINGS.md:98-99,213-215` | 95 %, two-sided | **No** — clustering on day is applied. But there are only **3 clusters**, so the resampling admits **ten distinct day-multisets** and the p-value's resolution floor is ~0.1; solattn states this itself at `FINDINGS.md:213-215` | 12,798 pools, cross-sectional, grouped by 3 birth days; 2,107 measurable; Q5 cell 412 | Point, bounds and n's reproduce verbatim from `solattn/FINDINGS.md:98-102`; the resample distribution itself is not stored in a form I can re-draw | **VERIFIED as transcribed.** The *characterisation* built on it ("a powered null", "detectability is not the binding term") is not supported by a 3-cluster interval that spans zero — DRAFT-V-7 |
| I-02 | `interval -4.9 to +60.9` around +27.99 bp/day | `SOURCES.md:134`; `cases.py:257-258` | Day-clustered bootstrap, 10,000 resamples, 60-cluster floor, Newey-West SE at 21 lags, bar 2.50 — established at `AiTrader/RETURN.md@f819b68:2852,2857`, **not stated anywhere in `retail-power-limits`** | Not stated here; AiTrader's family bar is |z| ≥ 2.50 two-sided | No — day-clustered, and Newey-West at 21 lags for the SE | daily excess return of a 5-position book vs an equal-weighted universe, 2.55-year holdout (~643 sessions) | Bounds reproduce verbatim from `RETURN.md:2857`; consistent with z 1.668 (a 95 % interval on a point of +27.99 with z 1.668 has a lower bound near zero, as observed) | **VERIFIED as transcribed.** `retail-power-limits` states no level, no units and no method for it — a completeness gap, recorded, not a contradiction |
| I-03 | lower bound clears zero at day 2,061; clears 4.07 bp/day at day 2,852 | `SOURCES.md:142`; `cases.py:269-273` | **Studentized asymptotic confidence sequence**, α 0.05 **one-sided**, tuning ρ minimising the boundary at a crossing time of 1,600 trading days, frozen at 0.071641 — `HFExperiment/REGISTRATION.md@f13e1d3:246-252` | α 0.05, one-sided | Not applicable — anytime-valid, peeking permitted by construction (`REGISTRATION.md:252-253`) | a hypothetical forward daily series; **n = 0 realized** — the series was disarmed before its first accrual | Day numbers reproduce verbatim; the boundary itself cannot be re-derived without the frozen ρ implementation | **VERIFIED as transcribed.** `retail-power-limits` omits the level, the tail, the boundary family and ρ; all four are stated in the sibling |
| I-04 | "0.026 to 0.047 across a grid of assumed correlations 0.0 to 0.7" | `docs/the-power-limit.md:169-171`; `SOURCES.md:38` | **Not an interval** — a pre-registered sensitivity grid; `NPDExperiment/REGISTRATION.md:231-236` | n/a | n/a — the grid *is* the sensitivity to the unknown correlation | four correlation cells | Reproduced exactly: 2.0·0.2626/√125.6 = 0.0469 and 2.0·0.1438/√125.6 = 0.0257 | **VERIFIED** — correctly labelled as a projection, not an interval, everywhere it appears |
| I-05 | effect bands (30–40 gross, 13.3–34.7 net; 0.01–0.05 rank IC; 0.09/0.18/0.045) | `SOURCES.md:34,66,98` | **Not intervals** — literature-derived effect bands and registered magnitudes | n/a | n/a | n/a | Each reproduces at its sibling (`InsiderExperiment/REGISTRATION.md:48-55,421`; `NPDExperiment/REGISTRATION.md:247`; `ETFExperiment/REGISTRATION.md:978`) | **VERIFIED** |

**No interval in this repository has its independence assumption violated in a way that moves a
stated comparison.** I-01 is the only one where the clustering is thin enough to matter, and the
consequence there is a characterisation problem (DRAFT-V-7), not a changed comparison: the kill
criterion K1 is "the interval includes zero", and it does.

---

## D. Tests table

**There is no p-value anywhere in `retail-power-limits`, and no alpha, no target power and no
critical value is stated for any figure it carries.** Every entry below therefore names the test as
it is defined in the sibling.

| # | statistic | file:line (here) | test / estimator, established at | tail | dof / distribution | correction applied | decision rule it feeds | correction matches the rule? | reproduces | status |
|---|---|---|---|---|---|---|---|---|---|---|
| T-01 | `z 1.668` vs "a corrected bar of 2.50" | `docs/the-power-limit.md:75,109`; `README.md:23`; `SOURCES.md:134`; `cases.py:257` | Day-clustered bootstrap z on paired daily excess over SPY, Newey-West SE at 21 lags — `AiTrader/RETURN.md@f819b68:2852` | **Two-sided** (`|z| ≥ 2.50`, `RETURN.md:2832`) | Normal (bootstrap z), 60-cluster floor | **Bonferroni** across a closed list of 4 primary tests, family α 0.05, per-test 0.0125 two-sided | **Union / disjunction**: four separate hypotheses (H-F, H-G, H-H, H-I), any one of which could be declared a discovery. The per-hypothesis verdict is itself a conjunction (z ≥ 2.50 AND sign AND capacity ≥ 2,500 USD/yr, `RETURN.md:2836`), but the α is not split across that conjunction | **Yes.** A union-type correction on a disjunction over four hypotheses is the right shape; the within-hypothesis conjunction correctly takes no further correction | `z(1 − 0.0125/2) = 2.4977 → 2.50` ✔; z 1.668 is AiTrader's Newey-West figure and is not re-derivable from the stored summary alone | **VERIFIED** — with the note that `retail-power-limits` calls the bar "corrected" without ever stating the family size, the α or the tail |
| T-02 | MDE `49.35 bp/month`; NW lags 5/63/126 → 50.19/49.11/49.53 | `SOURCES.md:70,86`; `cases.py:146-148` | `MDE_month = t · M · s_d / √N_eff`, Newey-West at the registered lag 21 — `InsiderExperiment/REGISTRATION.md:84-88,718-722` | **Not stated as one- or two-sided.** t = 2.0 is a "registered critical value"; the registered direction is one-sided ("predict **positive** abnormal returns", `REGISTRATION.md:3,175`). t = 2.0 corresponds to two-sided α ≈ 0.046 or one-sided α ≈ 0.023 | Normal; Newey-West lag 21 | **None, and none is needed** | **Single** pre-registered primary contrast at a single registered hold and weighting; the equal-weighted book is explicitly non-verdict-bearing (`REGISTRATION.md:764`) | **Yes** — a single registered primary needs no multiplicity correction, and none is applied | **Reproduces exactly** from stored primitives: 9.993 %/√12 = 288.47 bp; 2,869.9/21 = 136.66 months; SE 24.676 bp; ×2.0 = **49.353** | **VERIFIED**. Tail: **UNVERIFIABLE** — neither repository states whether the 2.0 is one- or two-sided, so the implied α is ambiguous between 0.023 and 0.046. It does not move the verdict (49.35 exceeds 40 by 23 %; even t = 1.645 would give 40.6, still above the floor) |
| T-03 | MDE `0.0512` (minimum detectable contrast) | `docs/the-power-limit.md:72,84`; `SOURCES.md:38`; `cases.py:95` | `realized_mde = t_critical × bootstrap SE`, where the SE comes from a **day-clustered moving-block bootstrap**, 10,000 resamples, **block length 10** (= 2 × the 5-session horizon) — `NPDExperiment/src/npd/eval/evaluator.py:508-524,544`; `reports/stage_b2/evaluation.md:73-74` | **Two-sided at t 2.0** (`evaluation.md:74`) | Bootstrap; effective N implied by the block bootstrap, not by the theoretical VIF | **None, and the registration says why**: "No family correction applies. This is one pre-registered contrast on one pre-registered model … It was written before any output existed." (`evaluation.md:84-86`) | **Single** pre-registered primary contrast | **Yes** | **Reproduces exactly**: 2.0 × 0.02562 = **0.05124**; implied N_eff = (0.36339/0.02562)² = **201.18** | **VERIFIED** for the MDE. The N_eff that produces it is **201.2**, not the 125.6 this repository records as its sample achieved — DRAFT-V-1 |
| T-04 | required N: 237 / 845 / 300 / >1,200 | `SOURCES.md:102`; `cases.py:200-203` | Simulation-based power: 1,200 draws, 300 sims per cell — `ETFExperiment/REGISTRATION.md:1011-1012` | Not stated in either repository | Simulated, not analytic | **None applied across the two co-primaries** | **Conjunction / intersection-union**: "Section 10 requires **both** co-primaries", so the governing minimum is the larger (300) — `REGISTRATION.md:1013` | **Yes.** An all-must-pass conjunction needs **no** per-component multiplicity correction, and none is applied. This is the correct shape; a Bonferroni or Šidák split here would have been the mismatch | Governing figure and shortfalls reproduce (300−163 = 137; 237−163 = 74). The simulation itself is not reproducible from stored summaries | **VERIFIED**. Target power **0.80** and the E2 pinning caveat (E2 reads exactly 0.8000 from 300 sims, binomial SE 0.0231) are stated in `ETFExperiment/REGISTRATION.md:1017-1021` but **nowhere in `retail-power-limits`** — the alpha is stated in neither |
| T-05 | K1 at 100.0 % coverage; 120 cells all negative | `SOURCES.md:180`; `cases.py:330-333` | Registered kill criterion on a single designated primary trial cell, plus a sign sweep over the computable grid — `solattn/FINDINGS.md:96-116` | Two-sided (the interval is 95 % two-sided) | Bootstrap over 3 day-clusters | **Šidák** at α_adj = 0.000321 on the **registered 160-cell grid** (4 horizons × 5 statistics × 2 match sets × 4 series) — `solattn/REGISTRATION.md:707`; `DECISIONS.md:342` | For the *primary*: **single** (K1 on one designated cell — no correction needed, and none applied). For the *grid sweep*: **union** over 160 cells | **Yes on both.** `1 − 0.95^(1/160) = 0.000321` recomputes exactly. Applying it to the 120 computable cells rather than the 160 registered ones would have given 0.000427 — the registered denominator is the correct, more conservative one, and it is what was used | Coverage (1,863/1,863; 5,907/5,907; 5,028/5,028), the 120-cell count and the negative-lift sweep all reproduce from `FINDINGS.md:104-116` | **VERIFIED**. `retail-power-limits` transcribes the sweep faithfully but calls the result "a powered null", a word solattn never uses and which no detectability figure supports — DRAFT-V-7 |
| T-06 | registered underpowered rule, 18 vs a floor of 20 | `SOURCES.md:192`; `cases.py:354-357` | A pre-registered **minimum-n rule that suppresses inference**, not a test statistic — `solclear/FINDINGS.md@c692032:73` | n/a | n/a | n/a — no significance is claimed in either direction | **Single**, and it is a suppression rule | n/a | 18 cleared / 4 at 90 d and the floor of 20 reproduce verbatim | **VERIFIED** |
| T-07 | `AUC 0.9432` at 100 ms | `SOURCES.md:172`; `cases.py:312` | A discrimination statistic over 165,075 Kraken samples across six validated days — `MLCryptoEngine/docs/notes/h1-…md@ae03bf6:39-57,301` | n/a — no test is run on the AUC | n/a | Not applicable to the AUC. (The related "H9 insignificant after deflation" is a deflated-Sharpe closure, `HYPOTHESES.md@d2a0f05:146`) | Offered as evidence the closure was **not** power-bound: the quantity is well measured and simply is not the quantity that pays | n/a | AUC and the per-horizon capture table reproduce verbatim | **VERIFIED**. `retail-power-limits` states no interval and no n for it; the n's are in the sibling |
| T-08 | the MDE identity `MDE = t · scale · sd / √N_eff` | `docs/the-power-limit.md:324`; the quoted sibling form at `:196` | `InsiderExperiment/DECISIONS.md:24-26` (ADR-001) uses `t * M * sd / sqrt(N_eff)`; `REGISTRATION.md:84` uses `MDE_month = t * M * s_d / sqrt(N_eff)` | n/a | n/a | n/a | The load-bearing methodological claim: the right-hand side needs no first moment | n/a | The block quote at `docs/the-power-limit.md:195-198` is **verbatim** from `InsiderExperiment/DECISIONS.md:24-26`; the block quote at `:185-191` is **verbatim** from `InsiderExperiment/REGISTRATION.md:21-27` | **VERIFIED**. The note renames `M` to `scale` in its own §The practice and gives neither a value; in the two cases where the identity is actually instantiated, `M` = 21 sessions/month (Insider) and the term is absent (NPD, whose SE comes from a bootstrap) |

---

## E. Draft findings

Only the seven items below survived verification as discrepancies. Everything else checked out.

### DRAFT-V-1
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The NPDExperiment `PowerCase`'s `sample_achieved` figure — the "Sample achieved" line of the generated `power-records` block.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "415 stored daily rankings of 432 eligible window days, 96.1 percent coverage against a 90 percent bar; 404 evaluable days; 125.6 independent-equivalent days after the 3.4 variance inflation the five-session horizon induces." — retail-power-limits/SOURCES.md:42 (generated from retail-power-limits/rplimits/cases.py:100-104), sourced to `NPDExperiment/progress.md @ 2d3d0ae`
- **Evidence:**
  - The cited source never pairs 404 with 125.6. `NPDExperiment/progress.md:319-320` states "the five-session horizon inflates variance by 3.4, cutting **427** evaluable days to 125.6 effective" — inside the **Stage A.2 registration** record, i.e. a projection made before collection. The same pairing appears in the registration itself at `NPDExperiment/REGISTRATION.md:227` ("which takes 427 evaluable days to **125.6** independent-equivalent days") and at `:229` ("D = 427, effective D = 125.6").
  - The **achieved** figure is 201.2. `NPDExperiment/reports/stage_b2/evaluation.md:92`: "| achieved effective sample size | **201.2** independent-equivalent days |", n = 404 evaluable days (`evaluation.md:51`).
  - `NPDExperiment/src/npd/eval/evaluator.py:529` defines it: `effective_n = (sd_daily / se) ** 2`, from the day-clustered moving-block bootstrap SE, not from the theoretical VIF of 3.4.
  - The two Figures inside the same `PowerCase` are mutually inconsistent. `realized_mde` (retail-power-limits/rplimits/cases.py:95) carries 0.0512; at N_eff = 125.6 and sd 0.36339 the MDE would be 0.0648, not 0.0512.
  - 125.6 is not reachable from 404 by any stated route: 404/3.4 = 118.8.
- **Recomputation:** inputs sd 0.36339 and bootstrap SE 0.02562 (`NPDExperiment/reports/stage_b2/evaluation.md:81-82`); method `(sd/se)²` per `evaluator.py:529` and `t·se` per `evaluator.py:544` with `t_critical=2.0` (`src/npd/config.py:119`). Results: N_eff = **201.18 → 201.2**; MDE = 2.0 × 0.02562 = **0.05124 → 0.0512**. Cross-check at the stated 125.6: 2.0 × 0.36339/√125.6 = **0.0648**. Tolerance: 4 dp on the MDE, 1 dp on N_eff. Script: `work/agentC-verify/recompute.py` (D-16, D-17, D-18).
- **What would resolve it:** replacing "125.6 independent-equivalent days" with the achieved 201.2, or re-labelling the 125.6 as the pre-registration projection over the 427-day base — which is what `docs/the-power-limit.md:164-165` already does correctly in prose ("the effective day count fell from 427 to 125.6", attributed to ADR-007 before collection).
- **Confidence:** HIGH — the sibling states the achieved figure explicitly, the code that computes it is present and unambiguous, and the stated pairing is arithmetically impossible under the note's own VIF.
- **Invalidated by later commits?:** no — `NPDExperiment` is closed at `2d3d0ae`, which is both the cited commit and the audit anchor, and `retail-power-limits` has had no commit since `dda39b2`.
- **Disclosed by authors?:** no. `DECISIONS.md` ADR-003 lists four corrections the note makes against the record it was handed; this is not among them, and `SOURCES.md:42` presents the figure as sample **achieved**.
- **Effect on the verdict:** none. The MDE 0.0512 is correct and still sits above the whole 0.01–0.05 band. The error makes NPDExperiment look 38 % more underpowered than it was.

### DRAFT-V-8
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The "cheaper independent observation" bullet in §What would change the conclusion. Same root cause as DRAFT-V-1, different locus and a separate quote.
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "NPDExperiment lost 70 percent of its sample to overlapping five-session horizons." — retail-power-limits/docs/the-power-limit.md:379
- **Evidence:** The realized loss was 50.2 %, not 70 %: 404 evaluable days (`NPDExperiment/reports/stage_b2/evaluation.md:51`) against an achieved effective sample of 201.2 (`evaluation.md:92`). The 70 % figure is the *registered projection*: 1 − 125.6/427 = 70.6 %, from `NPDExperiment/REGISTRATION.md:227`. The sentence is written in the past tense about what happened, in a paragraph arguing that the count of independent periods was the binding constraint.
- **Recomputation:** 1 − 201.2/404 = **0.502**; 1 − 125.6/427 = **0.7059**. Tolerance: 1 pp. Script: `work/agentC-verify/recompute.py` (D-19).
- **What would resolve it:** "NPDExperiment's registration projected a 70 percent loss to overlapping five-session horizons; the realized loss was 50 percent", or simply the realized figure.
- **Confidence:** HIGH — both numbers are stated in the sibling and the arithmetic is one division.
- **Invalidated by later commits?:** no — same reasoning as DRAFT-V-1.
- **Disclosed by authors?:** no. This line sits outside the generated blocks and is therefore not covered by the drift test either (`tests/test_render.py` re-renders only the four marker-delimited blocks).

### DRAFT-V-2
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The solclear `ContrastCase` deciding number — the survivorship result the note calls solclear's most transferable finding.
- **Direction:** neutral
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "archived-page sampling manufactures survivorship by 60 points at 30 days and 79 at 90, 97.5 percent death on 40 birth-ordered pools against 18.75 percent on 16 attention-crawled ones" — retail-power-limits/SOURCES.md:196 (generated from retail-power-limits/rplimits/cases.py:363-366); restated at retail-power-limits/docs/the-power-limit.md:310-312
- **Evidence:** `solclear/FINDINGS.md @ c692032:122-123` gives the table: birth-ordered n = 40 (20 at 90 d), **dead at 30 d 97.5 %**, **dead at 90 d 100 %**; attention-crawled n = 16 (15 at 90 d), **dead at 30 d 18.75 %**, **dead at 90 d 40 %**. So the 30-day gap is 78.75 points and the 90-day gap is 60.0 points — the reverse of the labels. The same sentence in `retail-power-limits` supplies the 30-day pair (97.5 vs 18.75) as support for a "60 points at 30 days" claim that pair contradicts.
- **Recomputation:** 97.5 − 18.75 = **78.75** (30 d); 100 − 40 = **60.0** (90 d). Tolerance: exact. Script: `work/agentC-verify/recompute.py` (D-27).
- **What would resolve it:** swapping the two horizon labels: "79 points at 30 days and 60 at 90".
- **Confidence:** HIGH — the source table is explicit and the subtraction is exact.
- **Invalidated by later commits?:** no. `solclear/FINDINGS.md` is byte-identical between the cited `c692032` and solclear's anchored `d298576`, so no later commit repairs it.
- **Disclosed by authors?:** no — but the error **originates in solclear**, whose own prose at `solclear/FINDINGS.md@c692032:125-126` reads "A 60-point gap at 30 days and a 79-point gap at 90 days" against its own table two lines above. `retail-power-limits` transcribed solclear's prose faithfully; the finding is that it repeated an error it also carries the data to catch. This is a contrast-case figure and nothing in the note's argument rests on which horizon carries which gap.

### DRAFT-V-4
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The time row of the cost-asymmetry table, and the InsiderExperiment `cost` Figure it renders from.
- **Direction:** B
- **Class:** CROSS_REPO_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "| time | **411 minutes** of recorded stage time across six stages, of which collection alone was 194 | about **51 minutes** for Stage A.1 and 20 for the closure |" — retail-power-limits/docs/the-power-limit.md:241
- **Evidence:**
  - `InsiderExperiment/progress.md:115-119` records **two** figures and refuses to choose: "The commit record puts Stage A.1 at about 51 minutes of session wall clock, 18:20 to 19:11, and Stage Z.1 at about 20 minutes. **The Z.1 brief records five hours.** The commit record cannot confirm that figure, which presumably counts operator time between stages that this repository does not observe. **Both are recorded rather than one being picked.**"
  - `retail-power-limits` carries only the smaller pair. The table cell at `docs/the-power-limit.md:241` drops even the provenance qualifier; the `cost` Figure at `rplimits/cases.py:166` keeps "by the commit record" but still names no alternative.
  - The magnitude matters to the row's own point: 51 + 20 = 71 minutes against NPDExperiment's 411 is a 5.8× asymmetry; 51 + 300 = 351 minutes against 411 is 1.2×.
- **Recomputation:** none required beyond the two sums above; both figures are quoted, not derived.
- **What would resolve it:** carrying both figures, as the sibling does — "about 51 minutes for Stage A.1 and either 20 minutes or five hours for the closure, depending on which of the two records the sibling itself declines to choose between".
- **Confidence:** HIGH — the competing figure and the instruction not to pick one are in the same paragraph of the cited file.
- **Invalidated by later commits?:** no. `InsiderExperiment` is closed at `12d9fd3`, the cited and anchored commit.
- **Disclosed by authors?:** partially — `rplimits/cases.py:166` says "by the commit record", which signals the provenance without naming the alternative; the note's own table drops that qualifier entirely. Per the disclosure rule this caps the finding at S3, which is where it sits.

### DRAFT-V-5
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The repository's count of its own evidence base, in four places.
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "The note quotes about ninety figures from seven repositories." — retail-power-limits/DECISIONS.md:35-36. Repeated as "Four of the **seven** source repositories are not published" (retail-power-limits/docs/the-power-limit.md:44-45), "four of the **seven** source repositories have no remote" (retail-power-limits/progress.md:113), and "for four of the **seven** that promise is currently **conditional**" (retail-power-limits/SOURCES.md:260).
- **Evidence:**
  - `rplimits/sources.py` cites **eight** distinct repositories: NPDExperiment, InsiderExperiment, ETFExperiment, HFExperiment, **AiTrader**, MLCryptoEngine, solattn, solclear (parsed from all 24 `Source` entries).
  - The repository's own table immediately under the "four of the seven" sentence has **eight rows**, AiTrader among them: retail-power-limits/SOURCES.md:262-271.
  - AiTrader is not incidental. It is the sole source for the fourth power case's deciding number: the `aitrader-return` key backs `realized_mde` for HFExperiment (retail-power-limits/rplimits/cases.py:262) and the fourth row of the headline table (retail-power-limits/rplimits/cases.py:428) — z 1.668, the 2.50 bar, 104.0 needed, 70.5 delivered, and the whole width table.
  - The test that would catch it cannot: `tests/test_sources.py:41-52` asserts `expected <= {source.repo …}` over a seven-element set that omits AiTrader — a subset assertion, so an eighth repository passes silently.
- **Recomputation:** distinct `Source.repo` values = 8 (script `work/agentC-verify/quotecheck.py`); rows in the SOURCES.md publication table = 8.
- **What would resolve it:** "eight repositories", and "four of the eight are not published". Note the correction moves against the note's own interest: 4/8 = 50 % unpublished rather than the 57 % the text implies.
- **Confidence:** HIGH — the eighth repository is listed in the repository's own table.
- **Invalidated by later commits?:** no — `retail-power-limits` has had no commit since `dda39b2`.
- **Disclosed by authors?:** partially — AiTrader is named and its publication status given at retail-power-limits/SOURCES.md:267, so a reader can see the eighth. The count sentence is what is wrong, in four places.

### DRAFT-V-3
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The publication disclosure — the repository's statement of how checkable its own citations are.
- **Direction:** neutral
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The four power cases — NPDExperiment, InsiderExperiment, ETFExperiment and HFExperiment — exist only on the operator's machine and have no remote." — retail-power-limits/docs/the-power-limit.md:45-47; tabulated as "**no — local only, no remote**" four times at retail-power-limits/SOURCES.md:268-271; recorded as a discovery at retail-power-limits/progress.md:113-116.
- **Evidence:** `git -C <repo> remote -v`, read 2026-09-04T00:18:21Z, returns `origin https://github.com/kirosli00tuff/<repo>.git` for all four. Read time and command logged in §G below.
- **Recomputation:** none. Timing evidence: `.git/config` mtimes are NPDExperiment 2026-08-29 11:45:18 −0700, InsiderExperiment 11:45:14, ETFExperiment 11:45:06, HFExperiment 11:45:10, and each has `refs/remotes/origin/` created at the same minute. This repository's three commits are 2026-08-29 00:19:47, 00:20:34 and 00:21:28 −0700 (recorded in the inventory from `git log`). **The claim was true when it was written and became false about 11½ hours later, the same day.**
- **What would resolve it:** the note is not repairable in place — it is a dated statement about the world. The correction is that the four are now published, so every citation in `SOURCES.md` is independently checkable by a stranger, which is strictly better for the note than what it claims.
- **Confidence:** HIGH — `git remote -v` is unambiguous and the mtimes bracket the change.
- **Invalidated by later commits?:** not applicable in the usual sense; the change is to the repositories' remotes, not to any commit. It cannot be invalidated by a later `retail-power-limits` commit because there has been none.
- **Disclosed by authors?:** the time-sensitivity is disclosed in spirit — retail-power-limits/SOURCES.md:279-282 says the hashes "are still doing work … so if any of the four is published later, every citation in this file resolves against it without amendment", which is exactly what has happened. That anticipation is why this is S4 rather than higher.

### DRAFT-V-6
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The repository's own gate self-report.
- **Direction:** neutral
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "mypy strict clean over 11 source files, 111 tests passing" — retail-power-limits/progress.md:68 (restated at retail-power-limits/progress.md:59)
- **Evidence:** The anchored tree collects **112** tests, not 111: `tests/test_sources.py` 74, `tests/test_cases.py` 19, `tests/test_honesty.py` 10, `tests/test_render.py` 9. The "11 source files" half is **correct** — 6 `.py` files under `rplimits/` and 5 under `tests/`, which is exactly mypy's configured scope (`retail-power-limits/pyproject.toml:41-45` with `files = ["rplimits","tests"]`).
- **Recomputation:** the anchored tree was copied to `work/agentC-verify/rpl2/` and collected with the repository's own pinned pytest; `112 tests collected in 0.04s`. Nothing was executed inside the audited repository. The one test that fails in the copy, `test_the_credential_scan_has_something_to_scan`, calls `git ls-files` and cannot pass outside a work tree — an artefact of the copy, not a defect.
- **What would resolve it:** "112 tests passing".
- **Confidence:** MEDIUM — collection counts can move with a pytest version, and I used the repository's own interpreter to minimise that risk, but I cannot rule out that the author counted at a moment when the suite held one test fewer.
- **Invalidated by later commits?:** no — there has been no commit since `dda39b2`.
- **Disclosed by authors?:** no. Nothing in the note rests on it; this is hygiene only.

### DRAFT-V-7
- **Repository / SHA:** retail-power-limits / `dda39b2f148569a6fe9be956a979471b2330611d`
- **Hypothesis or artifact:** The solattn contrast case — the note's own scope limit, offered as proof that not every closure in the program was a power closure.
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**solattn** returned a powered null. … That is what a closure looks like when detectability is not the binding term: the design measured what it set out to measure, at full coverage, and the answer was no." — retail-power-limits/docs/the-power-limit.md:295,300-302; the same characterisation at retail-power-limits/rplimits/cases.py:331 ("A powered null.") and retail-power-limits/rplimits/cases.py:343-346.
- **Evidence:**
  - **No detectability figure exists for solattn anywhere.** The note's own practice rule #1 (retail-power-limits/docs/the-power-limit.md:322-324) is that an MDE must be computed from dispersion and sample size; for the one case it labels "powered" it supplies none, and neither does solattn.
  - The interval it does supply spans zero at the upper end and is wide relative to the point estimate: lift −1.0779 with a 95 % interval **[−3.3354, +0.0204]** (`solattn/FINDINGS.md:98-99`), i.e. a width of 3.36 on a point of −1.08.
  - The clustering is on **three** clusters. The primary trial's day-clustered bootstrap resamples the three birth days 2026-08-16..18 (`solattn/FINDINGS.md:101-102`). solattn states the consequence itself: "With 3 day-clusters, `p_raw = 0.0000` carries almost no information. It means only that all **ten distinct day-multisets** share a sign — the resolution floor of the registered day-clustered bootstrap" (`solattn/FINDINGS.md:213-215`). None of this reaches `retail-power-limits`.
  - The word "powered" is `retail-power-limits`'s own. `solattn/FINDINGS.md` never uses it; its only use of the root is the **`underpowered` floor** at `:108`, and what clears that floor is the Q5 cell's 412 pools, a cell-size rule, not a statement about the primary contrast's detectability.
  - solattn's registered justification for the kill is **outcome coverage** (100.0 % on every analysed cohort, `FINDINGS.md:104-105`) plus the Q5 floor — both real and both correctly transcribed. Neither is a detectability figure.
- **Recomputation:** interval width 3.3354 + 0.0204 = **3.3558** against |point| 1.0779, a ratio of 3.11. Number of distinct multisets from resampling 3 clusters with replacement = C(5,3) = **10**, matching solattn's own statement. No further recomputation is possible: solattn's resample draws are not stored.
- **What would resolve it:** either a detectability figure for solattn's primary contrast — an MDE on the same 450 bps-net scale as the −1.0779 — or dropping "powered" for what the record supports: a fully covered null whose registered kill criterion fired, on three day-clusters.
- **Confidence:** MEDIUM — the label is a characterisation rather than a number, so it is not falsified the way a figure is; what is established is that no detectability evidence exists for it and that the cited interval's structure argues the other way.
- **Invalidated by later commits?:** no. `solattn/FINDINGS.md` is byte-identical between the cited `b3f5062` and solattn's anchored SHA, which are the same commit.
- **Disclosed by authors?:** no. The note gives the interval, so a careful reader can see it spans zero, but the three-cluster structure and solattn's own resolution-floor caveat are not carried across.
- **Note on direction:** this cuts against the note's own scope limit rather than for it. If solattn is not securely a non-power closure, the note's disclaimer that "not every closure in this program was a power closure" rests on two contrast cases rather than three — which makes the note's headline *more* universal, not less. It is recorded as B because the note claims more about solattn than its record supports.

---

## F. What could not be checked, and why

1. **The four power-case repositories' internal correctness.** This audit verified that
   `retail-power-limits` transcribes them accurately. Whether NPDExperiment's bootstrap, or
   InsiderExperiment's tracking-error estimate, or ETFExperiment's simulation is itself right is a
   question about those repositories, not this one.
2. **The tail of InsiderExperiment's t = 2.0.** Neither repository states whether the registered
   critical value is one- or two-sided, so the implied α is ambiguous between ≈0.023 and ≈0.046.
   **UNVERIFIABLE.** It does not move the verdict: at t = 1.645 the MDE would be 40.6 bp, still
   above the 40 bp BLOCKED floor.
3. **ETFExperiment's α and target power.** The 0.80 target is stated in
   `ETFExperiment/REGISTRATION.md:1017-1021`; the significance level is stated in **neither**
   repository. **UNVERIFIABLE.**
4. **AiTrader's z 1.668 and 1.455 as numbers.** They are Newey-West-at-21-lags bootstrap figures
   and the daily series is not stored in a form I can re-draw. The iid TE-ratio approximation gives
   1.696 and 1.274, which brackets the first and not the second; that is a difference between two
   standard-error conventions, not a discrepancy I can adjudicate without AiTrader's holdout series.
   **UNVERIFIABLE** at the level of re-derivation; **VERIFIED** as transcription.
5. **"the largest raw outperformance this project has ever measured"** (C-22) is a superlative over
   AiTrader's entire hypothesis register. I verified it is AiTrader's own sentence at
   `RETURN.md@f819b68:2844`; I did not enumerate AiTrader's register to test the superlative.
   **UNVERIFIABLE** as a fact, **VERIFIED** as a quotation.
6. **P-20's second half** — "no later AiTrader commit re-scores that holdout for H-F". I verified
   the `a0a9ef6` subject and that `RETURN.md` is unchanged between `f819b68` and AiTrader's anchor
   `705e0ed`. I did not walk AiTrader's full subsequent history for a re-scoring elsewhere.
   **UNVERIFIABLE** without a full-history sweep of a repository outside this task's scope.
7. **"about ninety figures"** (C-29) has no stated counting convention. The note carries 115
   distinct numeric tokens, so the claim is an undercount rather than an overstatement, but there
   is no rule against which to call it right or wrong. **UNVERIFIABLE.**
8. **ETFExperiment's 163 as a forward projection.** Projecting 20.8 admissible days/month from this
   note's own date to the deadline and adding the 11 held gives 157.2, not 163. The gap is
   explained inside ETFExperiment — the 163 is its "all cohorts" projection
   (`ETFExperiment/progress.md:486`) while the 291-plus-11 that yields 302 is "forward-only"
   (`REGISTRATION.md:1129-1130`) — but the accrual start date for the all-cohorts series is stated
   nowhere, so the 163 cannot be re-derived. **UNVERIFIABLE** as a derivation; **VERIFIED** as a
   transcription, which is all `retail-power-limits` claims for it.
9. **NPDExperiment's per-call price.** 920 × 0.007508 = 6.907, not the stated 6.9378 (a 0.4 % gap);
   922 calls gives 6.922. This is a rounding artefact **inside NPDExperiment/progress.md:201-202**,
   faithfully transcribed. Not a `retail-power-limits` finding.
10. **HFExperiment's closure date.** Its closing commit `f13e1d3` is stamped 2026-08-25T00:45:29
    −0700 yet records "instruction dated 2026-08-26" (`HFExperiment/progress.md:7-8`). A sibling
    quirk; `retail-power-limits` transcribes HFExperiment's own stated date correctly.

## What I would have expected to find if the thesis held, and did not

- **Figures that do not exist at their cited commit.** None. All 24 citations resolve, every named
  path exists, and every cited file is byte-identical between the cited commit and its sibling's
  anchored SHA. The drift ADR-001 warns about has not occurred anywhere.
- **A deciding number that does not reproduce.** None. All four reproduce from primitives, three of
  them exactly from stored counts and standard errors.
- **A quoted commit subject that is paraphrased.** None. All eight are verbatim.
- **A "Closure language, exact." block that is not exact.** None. All four are verbatim.
- **A derived figure smuggled in as a quotation.** None. Every ratio and difference a verifier would
  suspect — 137, 74, 37.6×, 1,700×, 100×, 100–180×, 1.5×, "eight to eleven years", 418 bp, 96.1 %,
  302 — is stated by the sibling. The one figure the repository declares derived (411 minutes) sums
  correctly and its exclusion note about the untimed Z.1 stage is also correct.
- **A gate back-dated after its measurement.** None. `fbfc74e` is genuinely InsiderExperiment's
  first commit, its Section 0 carries the 20/40 bars and the boundary convention, its tree contains
  no corpus, and Section 0 is untouched between `fbfc74e` and the gate commit `cb17046` 37 minutes
  later.

---

## G. Live-repo access log

All access read-only, for the two permitted purposes: git history/provenance, and confirming the
working tree matched the anchor. **No file in any audited repository was opened for writing.** No
`.env`, keystore, session or credential file was read.

**`git status --porcelain` BEFORE first access — 2026-09-04T00:13:58Z — verbatim:**

```
--- retail-power-limits ---
(end retail-power-limits)
--- NPDExperiment ---
(end NPDExperiment)
--- InsiderExperiment ---
(end InsiderExperiment)
--- ETFExperiment ---
(end ETFExperiment)
--- HFExperiment ---
?? Accept:
?? GET
?? Host:
?? User-Agent:
(end HFExperiment)
--- AiTrader ---
 M COLLECTION_LOG.md
(end AiTrader)
--- MLCryptoEngine ---
(end MLCryptoEngine)
--- solclear ---
(end solclear)
--- solattn ---
(end solattn)
```

**`git status --porcelain` AFTER last access — 2026-09-04T00:25:30Z — verbatim:**

```
--- retail-power-limits ---
(end retail-power-limits)
--- NPDExperiment ---
(end NPDExperiment)
--- InsiderExperiment ---
(end InsiderExperiment)
--- ETFExperiment ---
(end ETFExperiment)
--- HFExperiment ---
?? Accept:
?? GET
?? Host:
?? User-Agent:
(end HFExperiment)
--- AiTrader ---
 M COLLECTION_LOG.md
(end AiTrader)
--- MLCryptoEngine ---
(end MLCryptoEngine)
--- solclear ---
(end solclear)
--- solattn ---
(end solattn)
```

Identical at both ends. The only entries are the two pre-existing conditions the common rules name:
HFExperiment's four stray files and AiTrader's collector-appended `COLLECTION_LOG.md`. **Nothing
was modified by this audit.**

| command | repositories | time (UTC) | purpose |
|---|---|---|---|
| `git status --porcelain` | all 9 | 2026-09-04T00:13:58Z | mandatory before-log |
| `git log -1 --format=…` on `2d3d0ae`, `fbfc74e`, `cb17046`, `12d9fd3`; `git rev-list --max-parents=0` | NPDExperiment, InsiderExperiment | 00:14:05Z | the progression clock (C-05) and the first-commit claim (P-02) |
| `git show fbfc74e:REGISTRATION.md`; `git diff fbfc74e cb17046 -- REGISTRATION.md`; `git ls-tree -r fbfc74e` | InsiderExperiment | 00:14:4xZ | the 20/40 bars before the measurement (P-02, P-06, P-19) |
| `git log --format=…`; `git log -1` on `3f5d629`, `fe60a22`; `git show fe60a22:README.md`; `git diff fe60a22 4d11002 -- README.md` | ETFExperiment | 00:15:22Z–00:15:4xZ | closure and README citations (C-03, C-21, P-11) |
| `git log -1` on `f819b68`, `a0a9ef6`; `git show f819b68:RETURN.md` (grep only) | AiTrader | 00:15:35Z | the HF inherited figures (C-04, C-08, C-22) |
| `git log -1` on `f13e1d3`, `0a0d214`; `git show f13e1d3:REGISTRATION.md`; `git show 0a0d214:README.md`; `git log -- REGISTRATION.md` and a per-commit grep for "2,061" | HFExperiment | 00:16:11Z–00:16:5xZ | Section 11 and its registration date (C-23, P-10, P-13) |
| `git log -1` on `d2a0f05`, `ae03bf6`; `git show` both cited files | MLCryptoEngine | 00:18:00Z | the contrast-case margins (C-25) |
| `git log -1 c692032`; `git show c692032:FINDINGS.md` | solclear | 00:17:32Z | the survivorship table and Stage E (C-26, P-09, DRAFT-V-2) |
| `git remote -v` | all 8 siblings | 00:18:21Z | the publication disclosure (C-30, P-14, DRAFT-V-3) |
| `stat .git/config`; `ls .git/refs/remotes/` | the four power cases | 00:18:32Z | dating when the remotes were added |
| `git rev-parse`, `cat-file -e`, `ls-tree`, `show` over all 24 citations | all 8 siblings | 00:19:0xZ | citation resolution (P-11) |
| `git diff <cited> <anchor> -- <path>` for the 7 cited files whose commit differs from the sibling anchor | HFExperiment, AiTrader, MLCryptoEngine, solclear, ETFExperiment | 00:19:13Z | drift check (P-11, ADR-001) |
| `git status --porcelain` | all 9 | 2026-09-04T00:25:30Z | mandatory after-log |

**Unanchored reads:** the only unanchored facts in this report are the `git remote -v` results and
the `.git/config` mtimes used in DRAFT-V-3, read at 2026-09-04T00:18:21Z and 00:18:32Z. Remotes and
mtimes are not versioned and may change again. Everything else was read either from
`SNAP/<repo>/` at the audit anchors or from git objects, which cannot change.

**Scratch work,** all under
`/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/2c6a58bc-6f69-48c9-a930-b20684f1e1e4/scratchpad/work/agentC-verify/`:
`recompute.py` (every arithmetic check in §B), `quotecheck.py` (transcription fidelity of all 34
`Figure` values against their siblings), `check_sources.sh` + `sources.txt` (the 24-citation
resolution sweep), and `rpl2/` (a copy of the anchored `retail-power-limits` tree used only to
collect and run its own test suite). No repository script was executed in place; the only binary
used from an audited tree was `retail-power-limits/.venv/bin/python`, invoked with its working
directory inside the scratch copy.
