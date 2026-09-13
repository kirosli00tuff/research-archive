# ETFExperiment — VERIFY pass (Agent C, referee)

**Repository:** ETFExperiment
**Anchored SHA:** `4d110027674e7b4cd2861cf4e0e74f975111daf1` (master, 2026-08-28)
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/ETFExperiment/`
**Live repo touched read-only for:** git log (commit times) and untracked `data/` primitives
**Work dir:** `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-verify/`
**Python:** `/home/kiros-li/.cache/program-audit/scratchpad/venv/bin/python`
**Verified against:** `findings/agentC/verification/ETFExperiment.inventory.md` / `.json` (this agent's LOCATE pass)

## Headline

This repository is, on the numbers, unusually reproducible. **Every simulated power figure in
`reports/stage_a2/power.json` and `reports/stage_a2/e2_minimum_n.json` reproduces bit-for-bit**
from the anchored source with the anchored seed — all 12 E1 cells, all 12 E2 cells, all 8 E2
minimum-grid cells, and all three E1 minimum-N bisections (237 / 845 / 3776). The census, the
archive density, the retro-revision table, the substrate coverage, the rate-ceiling probe counts
and the pre-period derived quantities all reconcile exactly from stored primitives. The
end-to-end archive-density chain — raw Wayback timemaps → 451 mementos → 37 admissible days →
11 served values — was rebuilt from the untracked raw data and reproduces the artifact exactly.

Five things do not check out, and they are set out as draft findings:

1. **`DRAFT-V-1`** — the "**measured forward accrual rate of 20.8 admissible days per month**"
   was never measured. It is `21 weekdays/month × 333/336`, i.e. the rate at which the *source
   prints a value*, applied as though every future printed day were admissible. The repository's
   own measured admissible rate is **11 days in 16 months = 0.69/month**, and its forward
   collector produced **0 admissible days**. Below ~14.4 admissible days/month the registered
   BLOCKED power trigger fires, so "BLOCKED does not fire on power" holds only at the unmeasured
   figure.
2. **`DRAFT-V-2`** — "the registered five-fund aggregate differs from the all-fund total by a
   mean of **47.42M USD** (median 27.20M, range −903.20M to +1,205.20M, n = 333)" is not a
   difference at all. Those four numbers are the **mean, median, min and max of the Farside
   all-fund `Total` column itself** over the same 333 days (recomputed: 47.42M / 27.20M /
   −903.20M / +1,205.20M — exact to the printed digit). The actual difference is mean −7.44M,
   median −3.00M, range −150.40M to +363.00M, and exceeds the registered 100M threshold on
   **6 of 333 days**, not "large against" it.
3. **`DRAFT-V-3`** — a **Šidák union-type correction on an all-must-pass (intersection–union)
   decision rule**. Recomputed at the uncorrected α = 0.05: E1 power at N = 163 rises 0.6105 →
   0.7320 and E1's minimum N falls 237 → 207. The closure verdict does not move.
4. **`DRAFT-V-4`** — "The **220 charged requests** stand as the total lifetime network cost" was
   already stale when committed: the ledger held **238** charges three minutes before the
   Amendment 6 commit.
5. **`DRAFT-V-5`, `DRAFT-V-6`** — two small factual mis-counts: "572 of 572 post-boundary rows
   across **three** pages" (it is two pages), and a stated pacing equivalence that fails on one
   of six endpoints.

Two attributions of the E1 minimum-N simulation budget in the documents disagree with each other
and both disagree with the code; that is folded into `DRAFT-V-3`'s evidence and recorded in the
claims table under `ETF-C03`.

---

## 1. Claims table

Tolerance convention: "exact" means bit-identical to the stored float; "printed" means agreement
to every digit the document prints; "±x" is an absolute tolerance on the quantity named.

| # | Claim (short) | Stated | Source of truth used | Recomputed | Tol | Status |
|---|---|---|---|---|---|---|
| C01 | GO closed: archive density **11 of 333 = 0.0330** vs the 0.60 bar, "short by a factor of 18", "no subsequent measurement can restore it" — `REGISTRATION.md:863-867` | 11/333 = 0.0330; ×18 | `retro_revision.json` (comparable_days 11, archive_admissible_days 37); `archive_density.json` (union 37, n 333); rebuilt end-to-end from untracked `data/access/timemap-{recent,all_data}.txt` + `farside_all_parsed.json` through `src/etf/archive.py` | 11/333 = 0.033033; 0.60/0.0330 = **18.16**; unbounded ceiling 112/333 = 0.3364 < 0.60 | printed | **VERIFIED** |
| C02a | Projected achieved **N = 163** at 2027-03-31 — `REGISTRATION.md:984` | 163 | `power.json` (weekdays_to_deadline 153, printed_day_rate 333/336, admissible 11); `scripts/power_gate.py:29-43,69-81` | weekdays 2026-08-28→2027-03-31 = **153**; 11 + round(153×333/336) = **163**; also 152 and 88 reproduce | exact | **VERIFIED** |
| C02b | "at the **measured forward accrual rate of 20.8 admissible days per month**" — `REGISTRATION.md:981-982` | 20.8 admissible days/month, labelled *measured* | `census.json` by_month (11 admissible over 16 months); `census.json` admissible_forward_capture = 0; `scripts/power_gate.py:71` `printed_rate = 333/336`; grep across all artifacts | 21 weekdays/mo × 333/336 = **20.81** (a printed-day rate); **measured** admissible rate = 11/16 months = **0.69/month**; measured forward admissible days = **0** | n/a | **CONTRADICTED** (`DRAFT-V-1`) |
| C02c | "achieved N = 300 arrives around **2027-10-26**" — `REGISTRATION.md:985-986` | 2027-10-26 | arithmetic on the stated 20.8/month from N = 11 | (300−11)/20.8 = 13.89 months from 2026-08-28 → **2027-10-24** | "around" | **VERIFIED** (conditional on C02b's rate) |
| C03a | E2 minimum N **300**, E1 minimum N **237**, governing **300** — `REGISTRATION.md:974-978` | 300 / 237 / 300 | `e2_minimum_n.json`; `power.json:minimum_n_for_e1`; re-ran `src/etf/power.py` in the work dir | E2 grid published_0.18: 200 → 0.676667, 250 → 0.71, 300 → 0.80 (all **bit-identical**); E1 `minimum_n(0.18, 0.8)` = **237**; 845 and 3776 also exact | exact | **VERIFIED** |
| C03b | E1's 237 attributed to "**1,200 draws, 300 sims/cell**" — `REGISTRATION.md:1011` | 1,200 / 300 | `src/etf/power.py:225-234` `minimum_n(..., draws=4_000, simulations=600)` | code runs **4,000 draws / 600 simulations**; 1,200/300 is E2's budget (`scripts/e2_minimum.py:42`); `report.md:329-330` separately implies 20,000/2,000 | n/a | **CONTRADICTED** (folded into `DRAFT-V-3`) |
| C04 | "**BLOCKED does not fire on power** … Measured: **0.6105**" — `REGISTRATION.md:869-871` | E1 = 0.6105 at ρ 0.18, N = 163 | re-ran `e1_power(163, 0.18)` from anchored source, seed 20260828 | **0.6105**, bit-identical; all 12 E1 cells of `power.json` reproduce exactly | exact | **VERIFIED** (the figure; the N it rests on is C02b) |
| C05 | "**0 of 11** revised / sign flips / threshold crosses; **11 of 11** intact; below the registered minimum of 30" — `REGISTRATION.md:756-769` | 0/0/0, 11/11, min 30 | `retro_revision.json` 37 rows; `scripts/retro_revision.py:108-124` | 11 rows `state=stored`, every `delta_usd == 0.0` and `as_printed_usd == current_usd`; 0 flips, 0 crosses; `meets_registered_minimum` false. `revised = delta != 0.0` is the tightest possible definition — it cannot fail to fire | exact | **VERIFIED** |
| C06 | Census **336 rows, 11 admissible**, exclusions 53/243/25/3 + 1 operational — `report.md:260-269` | 336 = 11+53+243+25+3+1 | `census.json`; `archive_density.json` | 11 + 325 = **336**; by_month days sum **336**, by_month admissible sum **11**; 37 = 11 served + 25 served-no-value + 1 fetch-failed; 333 printed + 3 = 336 | exact | **VERIFIED** |
| C07a | Archive crawls "**0.316 times per calendar day** (n = 153 out-of-sample mementos over 484 calendar days)" — `docs/ACCESS.md:380-382` | 0.316; n 153; 484 days | untracked `data/access/timemap-*.txt` parsed with `src/etf/archive.py:parse_timemap`, read 2026-09-05T05:55Z | **153** mementos with `captured_at ≥ 2025-05-01`; 153/484 = **0.31612** | printed | **VERIFIED** |
| C07b | "**48.37 percent** of those mementos already fall inside the registered 20:00–08:00 UTC window" — `docs/ACCESS.md:382-383` | 48.37% | same timemaps | mementos in the 20:00–08:00 UTC clock band: **74 of 153 = 0.48366** | printed | **VERIFIED** (see note below on the stricter reading) |
| C07c | "an **unbounded** window … would reach only **112 of 333 (33.63 percent)**" — `docs/ACCESS.md:384-385` | 112/333 = 0.3363 | same timemaps + the 333-day universe | days with any memento dated D or D+1: **112 of 333 = 0.336336** | exact | **VERIFIED** |
| C08 | "Amendment 1 recorded … **37 of 333 (0.1111)** … measurement moved it by a factor of **3.4**" — `REGISTRATION.md:713-735` | 0.1111 → 0.0330; ×3.4 | `archive_density.json` union vs `retro_revision.json` | union admissible_share = 0.111111 (recomputed from raw timemaps: 37); 0.1111/0.03303 = **3.364** | printed | **VERIFIED** |
| C09 | "Binomial standard error on a 0.80 estimate at 300 draws is **0.0231**" — `REGISTRATION.md:1018-1019` | 0.0231 | arithmetic | √(0.8·0.2/300) = **0.023094** | printed | **VERIFIED** |
| C10 | "**5,002** hourly candle rows … 11 funding pages … **142 of 333** days covered at 0.95/0.95" — `report.md:288-290` | 5002 / 11 / 142 | `substrate_coverage.json` (333 per-day rows); untracked `data/outcomes/btc-1h-servable-window.json` (row count + timestamps only, no price read), read 2026-09-05T05:57Z | sealed store holds **5,002** unique hourly opens, 2026-02-01T11:00Z → 2026-08-28T20:00Z, **no duplicates, no gaps**; per-day rows with candle_coverage ≥ 0.95 **and** funding_coverage ≥ 0.95: **142** | exact | **VERIFIED** |
| C11a | Pre-period sd **0.027431** (n = 475), mean hourly funding **0.00002226** (n = 11,423 hours, 23 pages) — `report.md:296-299` | as stated | `preperiod_inputs.json` only | the summary matches the document to the printed digit; **the candle and funding payloads were never written to disk** (`scripts/preperiod_inputs.py` writes only the summary) | n/a | **UNVERIFIABLE at the primitive level** — inputs absent; irrecoverable without refetching the venue |
| C11b | Derived: 24-hour hold sum **0.000534**, **19.5 %/yr**, n = 475 from 476 closes, 11,423 over 23 pages | as stated | `preperiod_inputs.json` | mean_hourly × 24 = 0.00053436 **exact**; × 365 × 100 = 19.50405 **exact**; 2024-01-11→2025-04-30 inclusive = 476 closes → **475** returns; 22×500 + 423 = **11,423** across 23 pages | exact | **VERIFIED** |
| C12a | "**96 probe requests across 6 endpoints, every one HTTP 200**" — `report.md:137-139` | 96, all 200 | `rate_ceilings.json` | 16 rungs × 6 requests = **96** statuses, **all 200**, across 6 endpoints; per-endpoint n = 18/18/18/12/12/18 | exact | **VERIFIED** |
| C12b | "Paces are set at **twice the fastest verified-clean spacing** — half the highest verified-clean *rate*" — `report.md:150-151` | the two are the same rule | `rate_ceilings.json` | holds for 5 of 6 endpoints; for `archive.timemap` twice the fastest clean spacing = **2.0 s** (the operating value) but half the highest clean rate (21.28/min) = **5.64 s** — a 2.8× divergence, because that endpoint's observed rate fell at the tighter rung (21.28/min at 2.0 s vs 12.29/min at 1.0 s) | n/a | **CONTRADICTED** for one endpoint (`DRAFT-V-6`) |
| C13 | "`candleSnapshot` caps at **5,001 rows** (n = 17 bisection probes) … reaches back to **2026-02-01T11:00:00Z** … Probes at 730, 550, 400, 300, 250 and 225 days back returned **0 rows**" — `report.md:108-111` | 5001; 17; 6 zero-row probes | `depth.json`, `candle_horizon.json` (9), `candle_horizon_bisect.json` (8) | 9 + 8 = **17** probes; zero-row probes are exactly {730, 550, 400, 300, 250, 225}; `candle_cap_1h` row_count **5001**, first_open **2026-02-01T11:00:00Z**; hours in [11:00 Feb 1, 20:00 Aug 28) = **5001** exactly; 5001/24 = 208.375 | exact | **VERIFIED** |
| C14 | "**676 date rows** … **336** on or after 2025-05-01, of which **333** print a value"; "`Total` prints `0.0` … **3 of 3** such rows over n = 336" — `report.md:64, 91-92` | 676 / 336 / 333; 3 of 3 | untracked `data/access/farside_all_parsed.json`, read 2026-09-05T05:59Z | **676** rows; **336** on/after 2025-05-01; **333** with all five registered funds printed; all-dash OOS rows = **3** (26 May 2025, 19 Jun 2025, 28 Aug 2026), each with `Total = "0.0"` | exact | **VERIFIED** |
| C15a | "**315 of 333** out-of-sample days agree within 2 percent" — `docs/ACCESS.md:179-181` | 315/333 | untracked `sosovalue-btc.html` `__NEXT_DATA__` (660 rows) + `farside_all_parsed.json`, read 2026-09-05T05:56Z | **315 of 333** under a relative tolerance against either denominator (316 under a max-denominator rule); the named worst day 2026-08-11 is **7.8M vs 4.886M**, exact | printed | **VERIFIED** |
| C15b | "the registered five-fund aggregate **differs from** the all-fund total by a mean of **47.42M USD** (median 27.20M, range −903.20M to +1,205.20M, n = 333) — large against the registered 100M threshold" — `docs/ACCESS.md:172-177` | mean 47.42M, median 27.20M, range −903.20M..+1,205.20M | same two untracked files | **the actual difference** is mean **−7.44M**, median **−3.00M**, range **−150.40M..+363.00M**; \|difference\| mean 17.61M, median 9.70M; \|difference\| ≥ 100M on **6 of 333** days. The four printed numbers are instead the **mean/median/min/max of the Farside `Total` column itself** over the same 333 days: **47.42M / 27.20M / −903.20M / +1,205.20M** | exact | **CONTRADICTED** (`DRAFT-V-2`) |
| C16 | Live descriptive n = 333, 138 long / 114 short / 81 flat, **trade share 0.7568** — `report.md:284-287` | 0.7568 | `census.json` | (138 + 114)/333 = **0.7567568**, matches stored; 138 + 114 + 81 = 333 | exact | **VERIFIED** |
| C17 | "The **220 charged requests** stand as the **total lifetime** network cost" — `REGISTRATION.md:1160-1161` | 220 lifetime | untracked `data/ledgers/requests.jsonl` (476 lines), read 2026-09-05T05:58Z; `git log -1 4d11002` | charge #220 lands 2026-08-28T20:40:46Z with the split **33 flow / 79 archive / 108 venue** and settles 213×200, 5×404, 1×401, 1×403 — every stated figure correct **as of that instant**. The ledger holds **238** charges, the last at 2026-08-29T02:40:32Z, **three minutes before** the Amendment 6 commit at 2026-08-29T02:43:48Z. Lifetime split is 51/79/108 | n/a | **CONTRADICTED** as a lifetime total (`DRAFT-V-4`) |
| C18 | "The retro cohort is **8 trading days**" with eight named dates — `REGISTRATION.md:742-745` | 8 | `retro_revision.json` + `depth.json` window start | 11 served days minus the 3 before 2026-02-01 = **8**; the eight dates match the named list exactly | exact | **VERIFIED** |
| C19a | "**All six** registered mutations … each caught, source restored green" — `report.md:405-407` | 6 of 6 | `reports/stage_a4/mutations.log` | 6 lines, every one `caught=True restored_green=True` | exact | **VERIFIED** |
| C19b | "**Two of the six** required fixing the harness rather than the source" — `report.md:419` | 2 of 6 | `mutations.log` | the log records outcomes only — no diff, no failing test id, no harness/source attribution | n/a | **UNVERIFIABLE** — the artifact does not record which |
| C20a | "mypy strict clean across **76 files**" — `report.md:401-403` | 76 | `pyproject.toml:44` `files = ["src/etf","tests","scripts"]`; file counts at the anchor | 34 + 26 + 16 = **76** `.py` files | exact | **VERIFIED** (the count) |
| C20b | "`make lint`, `make typecheck` and `make test` are green" | green | — | no gate output is stored anywhere in the repository | n/a | **UNVERIFIABLE** — artifact absent (not re-run: running the repo's own gates is out of scope) |
| C21 | "A 9 bp round trip is **3.3 percent** of one daily standard deviation" — `report.md:301-303` | 3.3% | `preperiod_inputs.json` + `src/etf/costs.py` | 0.0009 / 0.0274305 = **0.032810** | printed | **VERIFIED** |
| C22 | minimum N 237 vs "near 250" **held**; 845 vs "high hundreds to low thousands" **held** — `REGISTRATION.md:834-842` | both hold | `power.json`; `REGISTRATION.md:381-382` | 237 and 845 both reproduce exactly; both fall inside the qualitative anchors registered at `REGISTRATION.md:376-388` before any data existed | n/a | **VERIFIED** (as a qualitative comparison) |
| C23 | "Newey-West **t 3.12** over **313** days … implies … **ρ ≈ 0.176**" — `REGISTRATION.md:343-345` | ρ ≈ 0.176 | arithmetic on the carried figure | inverting the stated formula t = ρ√(n−2)/√(1−ρ²) gives ρ = t/√(n−2+t²) = **0.17421**; ρ = t/√n = 0.1764 reproduces the printed 0.176 | ±0.002 | **VERIFIED** within the stated "≈" (exact inversion of the printed formula is 0.174, not 0.176) |
| C24 | "**81 of 333** days (24.3 percent)" inside the ±100M band — `DECISIONS.md:89-92` | 81/333 = 24.3% | `census.json` | 81/333 = **0.243243** | printed | **VERIFIED** |
| C25 | "E1 at 20,000 permutation draws and 2,000 simulations; E2 at 1,500 draws and 400 simulations" — `report.md:329-332` | as stated | `power.json`; `scripts/power_gate.py:95,100`; `src/etf/power.py:86-104` | exact for the power **table** (E1 defaults 20,000/2,000; E2 called with draws=1500, simulations=400). Not the budget used for the **minimums** — see C03b | exact | **VERIFIED** for the power table |
| C26 | "Forward-only accrual … reaches roughly **291** by 2027-10-31, plus the **11** … for about **302**" — `REGISTRATION.md:1129-1131` | 291 + 11 = 302 | arithmetic; `scripts/power_gate.py` method | 20.8 × 14 months = **291.2**, so 291 is the stated rate × 14 months. The repository's own weekday method gives 306 weekdays × 333/336 = **303** forward, i.e. **314** total — the two methods differ by 12 days inside one document | n/a | **VERIFIED** as arithmetic on C02b's rate; internally inconsistent with the method used for N = 163 |
| C27 | "achieved N = **237** arrives around **2027-07-26**" — `REGISTRATION.md:911-913` | 2027-07-26 | arithmetic on 20.8/month | (237−11)/20.8 = 10.87 months from 2026-08-28 → **2027-07-24** | "around" | **VERIFIED** (conditional on C02b) |
| C28 | "**Neither** selected source serves a per-row publication timestamp (n = 2 of 2)"; the words "evening" and "night" appear **zero times** across both pages — `docs/ACCESS.md:196, 123-124` | 0 of 2; 0 occurrences | untracked `farside-btc.html`, `farside-btc-all.html`, `sosovalue-btc.html`, read 2026-09-05T05:59Z | whole-word case-insensitive count of `evening` and `night` = **0** in both Farside pages (the 6 substring hits are `midnight` inside WordPress CSS/SVG identifiers); SoSoValue's row shape carries `dataDate` only | exact | **VERIFIED** |
| C29 | "measured live at **572 of 572** post-boundary rows across **three** pages" — `REGISTRATION.md:604-606` | 572; three pages | `venue_and_archive.json`; `depth.json` | 72 (funding_post_period, 72/72 gated) + 500 (funding_2025_05_page, 500/500 gated) = **572 of 572** — across **two** pages. The other three funding pages probed (funding_pre_period, funding_2024_01, funding_2023_05) are entirely pre-boundary with 0 gated rows | n/a | 572 **VERIFIED**; "three pages" **CONTRADICTED** (`DRAFT-V-5`) |
| C30 | "`verdict.py` … is imported by nothing" — `REGISTRATION.md:934-938` | 0 importers | grep across `src`, `scripts`, `tests` at the anchor | the only import site is `tests/test_verdict.py:14`, which itself asserts no Stage A module imports it (`test_no_stage_a_module_imports_the_verdict_machinery`); `data/state/` (the Stage B latch path) is absent from the live tree | exact | **VERIFIED** |

### Note on C07b

The stated 48.37 % is the share of out-of-sample mementos whose **clock time** falls in the
20:00–08:00 UTC band, and on that reading it reproduces exactly (74/153). Under the stricter
reading — mementos falling inside the qualifying window of one of the 333 *trading* days, which
is what `src/etf/archive.py:qualifying_window` actually tests — the figure is **57 of 153
(37.5 %)**, because weekend and holiday captures land in the clock band but qualify for no
trading day. The document's sentence says "fall inside the registered 20:00–08:00 UTC window",
which is the clock reading, and the inference it supports ("about what a 12-hour window should
catch") is sound on that reading. Recorded, not raised.

### Note on C01's window bound

`src/etf/archive.py:90-95` bounds the qualifying window **below** at 20:00Z on D
(`CONFIG.snapshot_peak_start_hour_utc`), while `REGISTRATION.md:190-199` §3.3 registers only
"an archive capture **strictly before the entry anchor**". Sensitivity, recomputed from the raw
timemaps: lower bound at D 20:00Z → **37** admissible; D 08:00Z → 66; D 00:00Z → **78**;
D−1 00:00Z → 114; wholly unbounded (any capture dated D or D+1) → **112**. Every one of these is
far below the 0.60 bar (200 days), and only 11 of the 37 that pass the registered window served a
value at all. **C01's "no subsequent measurement can restore it" therefore survives every window
this data admits**, and the authors themselves state and quantify the ceiling
(`docs/ACCESS.md:384-385`). No finding.

---

## 2. Derived quantities table

Every row recomputed from stored primitives with `venv/bin/python`; scripts in
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-verify/`.

| Derived quantity | Stated | Primitives used | Recomputed | Agrees |
|---|---|---|---|---|
| archive density share | 0.0330 | 11 served / 333 printed | 0.0330330 | yes |
| shortfall factor vs the 0.60 bar | "factor of 18" | 0.60 / 0.033033 | 18.164 | yes |
| falsification factor | "factor of 3.4" | 0.111111 / 0.033033 | 3.3636 | yes |
| union admissible set | 37 | recent 32 ∪ all_data 10 | 37, set-identical to stored | yes |
| density partition | 37 + 53 + 243 | `archive_density.json` union | = 333 | yes |
| 37 = served + no-value + failed | 11 + 25 + 1 | `retro_revision.json` states | 37 | yes |
| census partition | 11 + 53 + 243 + 25 + 3 + 1 | `census.json` | = 336 | yes |
| printed partition | 333 + 3 | `census.json` | = 336 | yes |
| by_month totals | 336 days, 11 admissible | `census.json:by_month` (16 months) | 336, 11 | yes |
| live trade share | 0.7567568 | (138 + 114)/333 | 0.75675676 | yes |
| admissible trade share | 0.7272727 | (5 + 3)/11 | 0.72727273 | yes |
| inside-band share | 24.3 % | 81/333 | 0.2432432 | yes |
| weekdays to interim | 89 | 2026-08-28 → 2026-12-31 | 89 | yes |
| weekdays to deadline | 153 | 2026-08-28 → 2027-03-31 | 153 | yes |
| printed-day rate | 0.99107143 | 333/336 | 0.991071428 | yes |
| N by deadline (all cohorts) | 163 | 11 + round(153 × 333/336) | 163 | yes |
| N forward-only by deadline | 152 | round(153 × 333/336) | 152 | yes |
| N forward-only by interim | 88 | round(89 × 333/336) | 88 | yes |
| accrual rate implied by the method | 20.8/month | 21 weekdays × 333/336 | 20.8125 | yes (but see C02b) |
| accrual rate implied by Amendment 6 | 20.8/month | 291 / 14 months | 20.7857 | yes |
| **measured** admissible days per month | — (never printed) | 11 admissible / 16 census months | **0.6875/month** | — |
| 24-hour funding sum | 0.000534 | mean_hourly × 24 | 0.00053435747 (exact) | yes |
| annualised funding | 19.5 %/yr | daily_sum × 365 × 100 | 19.504048 (exact) | yes |
| pre-period return count | n = 475 | 476 daily closes 2024-01-11..2025-04-30 | 475 | yes |
| pre-period funding hours | 11,423 over 23 pages | 22 × 500 + 423 | 11,423 | yes |
| cost as a share of daily σ | 3.3 % | 0.0009 / 0.0274305 | 0.0328102 | yes |
| ρ from the carried t | ≈ 0.176 | t = 3.12, n = 313 | t/√(n−2+t²) = 0.17421; t/√n = 0.17641 | printed value matches t/√n |
| Šidák α | 0.0253205655 | 1 − 0.95^(1/2) | 0.025320565519103666 | yes |
| candle-window hours | 5,001 rows = 208.4 days | 5001/24 | 208.375 | yes |
| hours in the served window | — | [2026-02-01T11:00Z, 2026-08-28T20:00Z) | 5,001 exactly | consistent with `depth.json` |
| sealed rows vs the measured cap | 5,002 vs 5,001 | sealed store timestamps | 5,002 unique opens, no gaps, last open 2026-08-28T20:00Z; the depth probe (20:0xZ) stopped at the 19:00 open, the seal (20:19:50Z) included the 20:00 bar — the extra row is the window sliding, not a duplicate | resolved, no defect |
| E2 SE at p = 0.5, m = 300 | 0.0289 | √(0.25/300) | 0.0288675 | yes |
| E2 SE at p = 0.5, m = 400 | ≈ 0.025 | √(0.25/400) | 0.025 exactly | yes |
| E1 power at N = 163 under α = 0.05 | — | re-ran `e1_power` | 0.7320 (vs 0.6105 at α_adj) | see `DRAFT-V-3` |
| E1 minimum N under α = 0.05 | — | re-ran `minimum_n` | 207 at ρ 0.18; 748 at ρ 0.09 (vs 237 / 845) | see `DRAFT-V-3` |
| E2 power at n = 300 under α = 0.05 | — | re-ran `e2_power` | 0.8967 (vs 0.8000); grid minimum still 300 because n = 250 gives 0.78 | see `DRAFT-V-3` |
| N at which E1 crosses the 0.50 BLOCKED floor | — | `e1_power(n, 0.18)` scan | 0.4475 at n = 100, 0.4755 at 110, 0.511 at 115, 0.5025 at 120, 0.5275 at 125 → crossing ≈ **n 113–120** | see `DRAFT-V-1` |
| accrual rate at which BLOCKED fires | — | N = 11 + rate × 7.06 months ≤ ~115 | **≈ 14.4 admissible days/month** | see `DRAFT-V-1` |
| lifetime request split | 33/79/108 = 220 | `requests.jsonl` charges 1..220 | exact at charge #220; lifetime is 51/79/108 = 238 | see `DRAFT-V-4` |
| difference vs level, SoSoValue cross-check | mean 47.42M etc. | `farside_all_parsed.json` + `sosovalue-btc.html` | difference: mean −7.44M / median −3.00M / range −150.40..+363.00M; **`Total` level: mean 47.42M / median 27.20M / range −903.20..+1,205.20M** | see `DRAFT-V-2` |

---

## 3. Intervals table

**No confidence interval on any estimate is reported anywhere in this repository.** Neither
co-primary was ever run on data, so there is no estimate to put an interval around. What exists
is three binomial standard errors on *simulated powers*, two min/max ranges, and a set of
empirical quantiles. Each is set out below with the estimator actually used, whether independence
was assumed, and whether the data structure makes that assumption doubtful.

| # | Quantity | Where | Estimator actually used | Independence assumed? | Data structure | Doubtful? | Reproduces? |
|---|---|---|---|---|---|---|---|
| I1 | SE 0.0231 on a power estimate of 0.8000 | `REGISTRATION.md:1018-1019` | binomial SE of a simulated proportion, √(p(1−p)/m), m = 300 | **yes**, and correctly | 300 independent replications of `e2_power`, each with a fresh `_bivariate` draw from one `random.Random(20260828)` stream | **no** — the replications genuinely are i.i.d. draws from the simulator; the only dependence is the shared RNG stream, which does not induce correlation between replications | **yes**: √(0.8·0.2/300) = 0.023094; the 0.8000 it applies to reproduces bit-for-bit |
| I2 | SE 0.0289 at a power near 0.5 | `REGISTRATION.md:966-968` | binomial SE at p = 0.5, √(0.25/m), m = 300 | yes, correctly | same | no | **yes**: √(0.25/300) = 0.0288675. The non-monotonicity it explains (0.3567 at n = 350 vs 0.3433 at n = 400) reproduces bit-for-bit and the gap of 0.0133 is 0.46 SE — the "simulation noise" reading is correct |
| I3 | SE ≈ 0.025 at a power near 0.5, m = 400 | `REGISTRATION.md:856-859`, `report.md:329-332` | binomial SE at p = 0.5, √(0.25/400) | yes, correctly | the Amendment 3 power-table E2 cells | no | **yes**: exactly 0.025 |
| I4 | Print-window range: served (n = 11) **+04:05 to +08:00**; dashed (n = 23) **−03:38 to +04:29**; overlap +04:05 to +04:29 | `report.md:230-237` | min/max of archived capture timestamps, split by served-value vs dashed — a **range, explicitly not an interval estimate** | not applicable (no distributional claim) | archived Wayback capture times, **censored by a crawl schedule the project did not choose**, and each capture is an upper bound on the print time rather than the print time | the censoring is the reason it cannot be an interval; the document says exactly this and refuses to move the anchor on it (`report.md:239-242`, `REGISTRATION.md:786-793`) | **yes**: served offsets +04:04:37 … +07:59:42 (rounds to +04:05 … +08:00); dashed −03:37:41 … +04:29:02 (rounds to −03:38 … +04:29); overlap +04:05 to +04:29 |
| I5 | Cross-check difference: mean 47.42M, median 27.20M, **range −903.20M to +1,205.20M**, n = 333 | `REGISTRATION.md:622-623`, `docs/ACCESS.md:174-175`, `report.md:65` | stated as location + range of a per-day **difference** between two published series | not applicable | two independently published daily series over the same 333 days | — | **no.** The four numbers are the mean/median/min/max of the Farside `Total` **level**, not of any difference. See `DRAFT-V-2` |
| I6 | Signal-distribution quantiles p05/p25/median/p75/p95 for n = 11 and n = 333 | `reports/stage_a2/census.json` | nearest-rank empirical quantiles (`scripts/census.py:quantiles`) | not applicable — descriptive, no interval claimed | daily aggregate net flow, USD | at n = 11 the p05 and p95 collapse onto the min and max, which the artifact shows plainly | **yes**; no document attaches a dispersion figure or interval to them |

**Summary for section B:** every interval-adjacent figure in this repository is a binomial SE on
an i.i.d. simulation, and independence is the right assumption in all three cases. **No standard
error, interval or test anywhere in this repository is computed on the time series, the panel, or
any repeated-within-day structure**, because no outcome was ever read — so the usual hazard
(treating serially dependent daily returns as i.i.d.) never arises here. The one quantity with a
genuinely awkward data structure (I4) is the one the authors explicitly refuse to promote.

---

## 4. Tests table

| # | Test / statistic | Where | Tail | Matches registered direction? | dof / null distribution | Correction applied | Decision rule | Correction matches rule? | Reproduces? |
|---|---|---|---|---|---|---|---|---|---|
| T1 | α_adj = 1 − 0.95^(1/2) = 0.0253205655 per co-primary | `REGISTRATION.md:284-286`; `src/etf/config.py:25` | one-sided | yes | — | **Šidák**, 2 tests, FWER 0.05 | "**Both must pass** for the Stage B GO row" (`REGISTRATION.md:285-286`) and "**both** co-primaries at or above 80 percent power" (`REGISTRATION.md:394`) — an **intersection–union / conjunction** rule | **NO.** Šidák is a union-type correction controlling P(at least one false rejection). An IUT that requires *all* components to reject has size bounded by the **largest** component α, so each component may be tested at the full 0.05 with no inflation. See `DRAFT-V-3` | α_adj reproduces exactly (0.025320565519103666) |
| T2 | E1: Spearman ρ under a permutation null | `REGISTRATION.md:290-293`; `src/etf/power.py:70-104` | **upper**, `spearman(xs,ys) > critical` | yes — registered "one-sided positive" | distribution-free; permutation null of ranks, depends on n alone; **no dof**. Critical value is a Monte-Carlo quantile at 20,000 draws: `index = ceil((1−α)·draws) − 1`, i.e. the empirical 0.9747 quantile | α_adj per T1 | co-primary of a conjunction | see T1 | **NEVER COMPUTED ON DATA** — no test statistic and no p-value exists. The simulator reproduces exactly, and I measured its **empirical size** at the registered α: 0.0265 / 0.0270 / 0.0295 at n = 163 across three seeds, 0.0220 at n = 300 (MC SE 0.0035) — correctly calibrated |
| T3 | E2: mean net return per trade under a label permutation | `REGISTRATION.md:302-306`; `src/etf/power.py:119-166` | **upper**, `perm_edge/traded − cost ≥ observed`, p = (exceed+1)/(draws+1) | yes — registered "one-sided lower bound above zero" | permutation null over signed position labels; **no dof**; the p-value uses the standard +1 Monte-Carlo correction, which is exact-valid | α_adj per T1 | co-primary of a conjunction | see T1 | **NEVER COMPUTED ON DATA**. Simulator reproduces exactly; empirical size at ρ = 0, n = 163: **0.0225** against the nominal 0.0253 — correctly calibrated |
| T4 | Permutation critical value vs the 1/√(n−1) asymptotic | `tests/test_power.py:59-65` | one-sided upper | — | asymptotic sd of Spearman ρ under H0 | none | engine calibration | n/a | **re-ran verbatim: cut 0.11530 against the asymptotic 0.11660, \|diff\| 0.00130 < 0.02 — passes** |
| T5 | Empirical size of E1 at a zero true effect | `tests/test_power.py:75-78` | one-sided upper | — | simulated bivariate normal, ρ = 0 | none | engine calibration | n/a | **re-ran verbatim: size 0.05375 against nominal 0.05, inside the asserted (0.02, 0.09)**. The band is wide relative to the nominal — my own tighter run at the registered α (T2) closes that gap and the engine passes |
| T6 | Threshold-sensitivity secondary over the 0/50/100/200M grid, "with **Šidák correction inside the secondary** (four cells)" | `REGISTRATION.md:315-316` | one-sided | yes | — | Šidák over 4 cells | a **descriptive secondary**, never verdict-bearing (`REGISTRATION.md:308, 321`) | **yes** — a union-type correction over four exploratory cells with no conjunction rule attached is the correct use | never run |
| T7 | Carried external statistics: Newey-West **t 3.12** (next-day), t 8.99, IV first-stage **F 21.58**, Granger β 0.47 / t 9.75, conditional reversal t −2.42 to −3.99, 10-day total t 4.49 | `REGISTRATION.md:493-502` | as published | — | the source study's daily panel, n = 313 | none in-repo | none — **explicitly labelled carried**, not measured here (`REGISTRATION.md:482-485`) | n/a | **UNVERIFIABLE** — external, no data in-repo. Only t 3.12 propagates into a bar, via ρ ≈ 0.18 → the registered 0.09 (see C23) |
| T8 | Carried external **t 2.65** (IV impact 0.20 %/100M, 563 days) | `REGISTRATION.md:510-512` | as published | — | the same author's extended panel | none | carried | n/a | **UNVERIFIABLE** — external. Called "the single most important number carried into this registration" and it is the sole justification for halving the effect assumption |
| T9 | Carried external 90-day rolling coefficient 0.16, "indistinguishable from zero", down from 0.68 | `REGISTRATION.md:542-545` | — | — | rolling daily correlation | none | carried | n/a | **UNVERIFIABLE** — external, and "indistinguishable from zero" is reported with no standard error or interval on either side |

---

## 5. Draft findings

Temporary IDs; the consolidator assigns final IDs.

### DRAFT-V-1
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** H1's closure at `untestable-at-achievable-power`; the projected achieved N of 163 and the Section 0 finding that BLOCKED does not fire on power
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The deadline finding, restated at the governing figure.** At the measured forward accrual rate of 20.8 admissible days per month:" — ETFExperiment/REGISTRATION.md:981-982; and the table row "| projected achieved N at the registered deadline | **163** | forward accrual 20.8 admissible days/month |" under a column headed "measured" — ETFExperiment/REGISTRATION.md:1008-1010
- **Evidence:**
  - The figure 20.8 appears in **no artifact and in no line of code**. Grep across `reports/`, `src/`, `scripts/` at the anchor returns nothing; the only occurrences are the twelve prose citations (REGISTRATION.md:982, :1010, :1129; report.md:360, :447, :506; HYPOTHESES.md:70, :82, :84; progress.md:493, :533, :581; DECISIONS.md:555, :596).
  - The code that produces N = 163 is `ETFExperiment/scripts/power_gate.py:71`, `printed_rate = 333 / 336`, applied to a **calendar weekday count** (`trading_days_between`, ETFExperiment/scripts/power_gate.py:29-43). 21 weekdays/month × 333/336 = 20.8125. The quantity actually measured is the rate at which **the source prints a value**, not the rate at which a day is **admissible**.
  - The repository measured the admissible rate and it is not 20.8. `ETFExperiment/reports/stage_a2/census.json` `by_month` records **11 admissible days across 16 months = 0.69 per month** (n = 336 date rows, 333 printed). The comment at ETFExperiment/scripts/power_gate.py:69-70 states the substitution in the open: "The forward cohort accrues at the measured **printed-day** rate".
  - Forward accrual was measured and it was zero. `census.json` `admissible_forward_capture` = **0** (n = 336); ETFExperiment/report.md:264 prints "**admissible** (all retro-archive; forward-capture 0) | **11**". The live untracked snapshot ledger `data/snapshots/flow_snapshots.jsonl` (read 2026-09-05T05:52Z, UNANCHORED) holds 20 captures over one trade date, every one showing 2026-08-28 as `signal_usd: null` — 0 admissible days from 0 completed forward days.
  - Section 14.7 of the registration forbids exactly this: "**Therefore: no accrual, coverage, lag, retention, revision, or capture-density figure in this repository is registered before it is measured.** Every such figure is named as an A.1 or A.2 **measurement target**, never as an input" — ETFExperiment/REGISTRATION.md:571-573 — and ETFExperiment/REGISTRATION.md:584 names "admissible days per month and the trailing rate" as an A.2 Task 1 measurement target.
  - What turns on it: "**BLOCKED does not fire on power.** Its power trigger is E1 under 0.50 at the published-magnitude assumption at the achievable count by 2027-03-31. Measured: **0.6105**. The trigger is not met." — ETFExperiment/REGISTRATION.md:869-871, enforced at ETFExperiment/src/etf/section0.py:125-136.
- **Recomputation (if any):**
  - Inputs: `reports/stage_a2/power.json` (weekdays_to_deadline 153, printed_day_rate 333/336, scenarios), `reports/stage_a2/census.json` (admissible 11, admissible_forward_capture 0, by_month), `src/etf/power.py:86-104` (e1_power, seed 20260828), `src/etf/config.py:25` (α_adj).
  - Method: re-ran the anchored `e1_power` in the work dir over a grid of N at ρ = 0.18 to locate the 0.50 BLOCKED floor, and converted N back to a required accrual rate through the repository's own projection identity N = 11 + rate × (2026-08-28 → 2027-03-31 in months).
  - Result: N = 163 reproduces exactly (11 + round(153 × 333/336)). E1 power = 0.4475 at n = 100, 0.4755 at 110, **0.5110 at 115**, 0.5025 at 120, 0.5275 at 125, 0.5870 at 140, 0.6105 at 163 — the 0.50 floor is crossed at **n ≈ 113–120**. Solving 11 + rate × 7.06 months ≤ 115 gives **rate ≤ ≈ 14.4 admissible days per month**. At the repository's only *measured* admissible rate (0.69/month) the achievable N is ≈ 16 and E1 power ≈ 0.08, far under the floor.
  - Tolerance: exact on the reproduced power figures (bit-identical); the crossing point is located to ±5 in n by the 0.0112 Monte-Carlo SE at 2,000 simulations.
- **What would resolve it:** either (a) an artifact or code path that measures a forward admissible-day rate — which requires the forward collector to run past at least one completed print, and it was disarmed 2026-08-29T02:43:48Z before that happened; or (b) relabelling 20.8 as a **projection under the assumption that the repository's own capture makes every printed day admissible**, stating the assumption, and reporting the Section 0 power row's sensitivity to it. The substantive question — whether a 20-minute snapshotter across 20:00–14:00 UTC would in fact catch the print before the 08:00Z anchor — is not settled by this record: the served-capture range the repository itself measured runs up to **+07:59:42**, i.e. eighteen seconds inside the anchor (`reports/stage_a1/retro_revision.json`, recomputed).
- **Confidence:** HIGH — that the figure is a printed-day rate and not a measured admissible rate is readable directly from `scripts/power_gate.py:69-71` and from the census's own `by_month` block; the power sensitivity is a bit-exact rerun of the repository's own function. MEDIUM only on the counterfactual accrual rate a working snapshotter would have achieved, which no data settles.
- **Invalidated by later commits?:** no — the repository is closed and disarmed at the anchor, the census and power artifacts are anchored, and no commit after 4d11002 exists on master.
- **Disclosed by authors?:** **Partly, and only in code.** The substitution is stated plainly in a source comment (`ETFExperiment/scripts/power_gate.py:69-70`) and the forward-capture count of 0 is printed in the census table (`ETFExperiment/report.md:264`, `README.md:37`). **No document anywhere describes 20.8 as anything other than "measured"**, and the word "measured" is attached to it in all twelve prose citations and in a table column literally headed `measured` (REGISTRATION.md:1008). The disclosure does not cover the label.

### DRAFT-V-2
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** A.1 Task 1 source selection; the SoSoValue cross-check and the justification for the registered five-fund universe
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Measured over the 333 overlapping out-of-sample days, **the registered five-fund aggregate differs from the all-fund total by a mean of 47.42M USD (median 27.20M, range −903.20M to +1,205.20M, n = 333)** — large against the registered 100M USD threshold. The two are **not interchangeable**" — ETFExperiment/docs/ACCESS.md:172-177. Repeated at ETFExperiment/REGISTRATION.md:620-623 ("the two differ by **a mean of 47.42M USD (median 27.20M, range −903.20M to +1,205.20M, n = 333)** — large against the registered 100M threshold") and ETFExperiment/report.md:65 ("differing by a mean of **47.42M USD** (median 27.20M, range −903.20M to +1,205.20M, n = 333) — large against the registered 100M threshold, so the two are **not interchangeable**").
- **Evidence:**
  - Data: untracked `ETFExperiment/data/access/farside_all_parsed.json` (676 rows, 14-column header) and `ETFExperiment/data/access/sosovalue-btc.html` (1,086,812 B, `__NEXT_DATA__` payload of 756,748 B carrying 660 daily rows). Both read read-only at **2026-09-05T05:56Z**. UNANCHORED (`.gitignore` line 2 excludes `data/`), but they are the only route to the figure — no script in `scripts/` computes the cross-check and no module names sosovalue.
  - Registered universe: `ETFExperiment/src/etf/config.py:141`, `flow_universe_tickers=("IBIT","FBTC","GBTC","ARKB","BITB")`.
  - The actual per-day difference between the five-fund aggregate and the all-fund total, over the same n = 333 printed out-of-sample days: **mean −7.44M, median −3.00M, range −150.40M to +363.00M** against Farside's own `Total`; **mean −7.15M, median −2.89M, range −150.43M to +366.16M** against SoSoValue's `totalNetInflow`. Absolute difference: **mean 17.61M, median 9.70M**.
  - `|five-fund − all-fund| ≥ 100M` on **6 of 333 days (1.8 %)**, which is the opposite of "large against the registered 100M USD threshold".
  - What the four printed numbers actually are: the **mean, median, minimum and maximum of the Farside all-fund `Total` column itself**, over the same 333 days — recomputed **47.42M / 27.20M / −903.20M / +1,205.20M**, matching every printed digit. (SoSoValue's own series over the same days: 47.13M / 27.29M / −903.11M / +1,205.18M; the five-fund series: 39.98M / 27.40M / −860.90M / +1,142.40M, which are exactly `census.json`'s stored `signal_distribution_live_descriptive` mean/median/min/max.)
  - The companion claim in the same paragraph **does** verify: "**315 of 333** out-of-sample days agree within 2 percent" (ETFExperiment/docs/ACCESS.md:179-181) reproduces as 315 of 333, and the named worst day, "2026-08-11, 7.8M against 4.89M", reproduces as Farside `Total` 7.8M vs SoSoValue 4.886M.
- **Recomputation (if any):** inputs `data/access/farside_all_parsed.json` (parsed with the repository's own cell conventions: dash → absent, parentheses → negative, values in millions) and `data/access/sosovalue-btc.html` → `props.pageProps.historyData.list[*].{dataDate,totalNetInflow}`; universe filter `d >= CONFIG.oos_start_date` (`src/etf/config.py`), five-fund aggregate absent when any registered fund cell is a dash (`src/etf/flow.py:aggregate` convention). Script: `work/agentC-etf-verify/c15b.py`, `c15c.py`. Result as above; tolerance exact to the printed 0.01M.
- **What would resolve it:** replacing the sentence's four numbers with the difference statistics actually measured (mean −7.44M, median −3.00M, range −150.40M..+363.00M, |diff| ≥ 100M on 6 of 333 days), and restating the inference that follows from them. If the intent was to report the *scale of the flow series* rather than the *difference between universes*, the sentence needs a different verb, and the "not interchangeable" conclusion then has no measured support in the record.
- **Confidence:** HIGH on the recomputation — the four stated numbers reproduce exactly as the level statistics of a different series, which is not a coincidence a rounding difference could produce. MEDIUM on the consequence: a near-interchangeable second publisher matters to reopen threshold (b) (`ETFExperiment/HYPOTHESES.md:84`), because SoSoValue's archive-capture density over the test window was never measured and this figure is what closed the question of using it. It does **not** reopen the closure: SoSoValue serves no per-row publication timestamp either (`docs/ACCESS.md:169`), so reopen threshold (a) is untouched.
- **Invalidated by later commits?:** no — the repository is closed at the anchor and the two data files carry mtimes of 2026-08-28, before the anchor's documents were finalised. The figure could in principle move if the sources revised their history after 2026-08-28; that would change the difference statistics but could not convert a difference into a level.
- **Disclosed by authors?:** no. The figure is presented as measured, with its n, in three documents and the README summary line (`ETFExperiment/README.md:29` carries the companion 315-of-333 row), and nothing anywhere flags it as a level rather than a difference.

### DRAFT-V-3
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Section 8 inference; every power figure, every minimum N, and the stated shortfall that carries the closure
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Two co-primaries, distribution-free, one-sided, at `alpha_adj = 1 − 0.95^(1/2) = 0.0253205655` each. Both must pass for the Stage B GO row.**" — ETFExperiment/REGISTRATION.md:284-286; with the comment "alpha_adj = 1 - 0.95 ** (1/2): two co-primaries, family-wise 0.05, Sidak." — ETFExperiment/src/etf/config.py:25; and Section 10's "**both co-primaries at or above 80 percent power at achieved admissible N**" — ETFExperiment/REGISTRATION.md:394.
- **Evidence:**
  - Šidák is a **union-type** correction: it controls P(at least one false rejection) when a family of tests is read disjunctively. The decision rule it is attached to here is a **conjunction** — both co-primaries must reject before the Stage B GO row fires. That is an intersection–union test, whose size is bounded by the **largest** component level, so each component may be tested at the full nominal 0.05 with the overall type-I error still at 0.05. Applying Šidák costs power and buys nothing.
  - The mismatch is load-bearing on magnitudes: the whole closure is stated as a shortfall between an achievable N of 163 and a governing minimum N of 300, at ETFExperiment/REGISTRATION.md:1008-1015, including "| shortfall at the deadline, governing figure | **137 days** |" and "| shortfall at the deadline, **most favourable figure on the record** | **74 days** |".
  - Both engines are correctly *sized* at whatever α they are given — I verified this independently rather than assuming it: empirical size of E1 at the registered α is 0.0265 / 0.0270 / 0.0295 at n = 163 across three seeds and 0.0220 at n = 300 (MC SE 0.0035); E2's empirical size at ρ = 0, n = 163 is 0.0225. The defect is the choice of α, not the implementation.
  - **A second, separate defect in the same claim family:** the simulation budget attributed to E1's minimum N is wrong in two documents, in two different ways. ETFExperiment/REGISTRATION.md:1011 attributes E1's 237 to "1,200 draws, 300 sims/cell", which is E2's budget (`ETFExperiment/scripts/e2_minimum.py:42`). ETFExperiment/report.md:329-330 states "E1 at 20,000 permutation draws and 2,000 simulations", which is the power-**table** budget. The code that produced 237 runs at **4,000 draws and 600 simulations** (`ETFExperiment/src/etf/power.py:225-234`). The figure itself is correct — `minimum_n(0.18, 0.8)` reproduces 237 exactly — but neither stated n is the n that produced it.
  - Also recorded: `minimum_n` bisects a **noisy simulated** power curve (`ETFExperiment/src/etf/power.py:242-252`), so its output is a random variable, not a well-defined minimum; the repository acknowledges the analogous point for E2's grid at REGISTRATION.md:966-972 but not for E1's bisection.
- **Recomputation (if any):**
  - Inputs: anchored `src/etf/power.py`, `src/etf/config.py`, `reports/stage_a2/census.json`, `reports/stage_a2/preperiod_inputs.json`; costs from `src/etf/costs.py` (9 bp central).
  - Method: re-ran the repository's own `e1_power`, `e2_power` and `minimum_n` unmodified, first at the registered α_adj (to establish bit-exact reproduction) and then at α = 0.05, the level an intersection–union rule permits per component. Script: `work/agentC-etf-verify/iut.py`.
  - Result: **E1 power at N = 163, ρ = 0.18: 0.6105 → 0.7320.** **E1 minimum N at ρ = 0.18: 237 → 207**; at ρ = 0.09: 845 → 748. **E2 power at n = 300, ρ = 0.18: 0.8000 → 0.8967**; at n = 250: 0.7100 → 0.7800; at n = 200: 0.6767 → 0.7767 — so E2's reported minimum stays 300 at the registered grid resolution of 50, while the true minimum moves into (250, 300).
  - **Consequence, stated plainly: the closure does not move.** 163 still falls short of 207 and of 300; E1's power at achievable N is still under the 0.80 GO floor and still over the 0.50 BLOCKED floor; the Section 0 verdict is unchanged. What moves is the stated magnitude: the "most favourable figure on the record" shortfall of 74 days becomes 44, and the reported power at achievable N rises by 0.12.
  - Tolerance: bit-exact on every figure reproduced at α_adj; the α = 0.05 figures carry the same 0.0112 (E1, 2,000 sims) and 0.023–0.029 (E2, 300–400 sims) Monte-Carlo SE as the originals.
- **What would resolve it:** either (a) an amendment recording that Section 8's rule is an intersection–union test and that each co-primary is therefore tested at 0.05, with the power table and both minimums recomputed; or (b) a stated reason for keeping the conservative level — for example a decision rule elsewhere in the map that reads the co-primaries disjunctively. I found none: Section 8 (REGISTRATION.md:285-286), Section 10 (REGISTRATION.md:392-395) and `src/etf/section0.py:139` are all conjunctions, and the only disjunctive use of Šidák in the registration is the four-cell threshold-sensitivity **secondary** (REGISTRATION.md:315-316), where it is used correctly.
- **Confidence:** HIGH on the mismatch — the decision rule is quoted verbatim in the same sentence as the correction, and the IUT result is standard. HIGH on the recomputed magnitudes, which are reruns of the repository's own functions. HIGH that the closure survives.
- **Invalidated by later commits?:** no — Section 8 is above every amendment line and unedited, and `ALPHA_ADJ` is a frozen A.0 constant.
- **Disclosed by authors?:** no. The registration states the Šidák rationale ("two co-primaries, family-wise 0.05, Sidak", `src/etf/config.py:25`) and the conjunction rule in the same breath without noticing they pull against each other. The budget mis-attributions at REGISTRATION.md:1011 and report.md:329-330 are likewise undisclosed.

### DRAFT-V-4
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 6's closing cost statement
- **Direction:** neutral (hygiene)
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The **220 charged requests** stand as the total lifetime network cost. Zero dollars, no capital, no credential, at any point." — ETFExperiment/REGISTRATION.md:1160-1161. Same figure at ETFExperiment/progress.md:514-516 ("**220 charged requests** across the whole stage — 33 flow, 79 archive, 108 venue — settling 213 × 200, 5 × 404, 1 × 401, 1 × 403") and ETFExperiment/progress.md:564, :602.
- **Evidence:**
  - `ETFExperiment/data/ledgers/requests.jsonl` (untracked, 61,572 B, 476 lines), read read-only **2026-09-05T05:58Z**. UNANCHORED. It holds **238 charge rows and 238 settle rows**, first charge 2026-08-28T08:12:19Z, last charge **2026-08-29T02:40:32Z**.
  - Charge **#220** lands at 2026-08-28T20:40:46Z, and at that instant the split is exactly **flow 33 / archive 79 / venue 108** and the settles are **213×200, 5×404, 1×401, 1×403** — every figure the documents print is correct *as of 20:40:46Z*.
  - Amendment 6 (the anchored commit `4d11002`) is stamped 2026-08-28T19:43:48−07:00 = **2026-08-29T02:43:48Z**, three minutes and sixteen seconds after the ledger's last charge. Lifetime totals at that moment: **238 charges**, split **flow 51 / archive 79 / venue 108**, settling 231×200, 5×404, 1×401, 1×403.
  - The 18 extra charges are all `flow`, taken between 20:40Z and 02:40Z by the `etf-snap` collector that **Amendment 6 itself disarms** two lines earlier (ETFExperiment/REGISTRATION.md:1157).
- **Recomputation (if any):** inputs `data/ledgers/requests.jsonl` (read time above) and `git -C <live> log -1 --date=iso-strict 4d11002`; method: count `kind == "charge"` rows, take the prefix of length 220, tabulate `source` and the settle `http_status`; compare against the commit timestamp. Result as above; tolerance exact (integer counts).
- **What would resolve it:** an amendment line recording 238 as the lifetime figure, or restating 220 as "at the time Amendment 5 was written". Nothing scientific turns on it — no measurement, bar or verdict uses the request count.
- **Confidence:** HIGH — integer counts from an append-only ledger against a git commit timestamp.
- **Invalidated by later commits?:** no. The ledger has not grown since 2026-08-29T02:40:32Z and both timers are disabled and inactive (checked in the LOCATE pass).
- **Disclosed by authors?:** no — the sentence says "total lifetime", not "at the time of writing".

### DRAFT-V-5
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Amendment 1's pre-period blindness statement
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "every funding rate stamped at or after 2025-05-01 that has passed through a reader has been gated — measured live at **572 of 572 post-boundary rows across three pages**." — ETFExperiment/REGISTRATION.md:604-606
- **Evidence:**
  - `ETFExperiment/reports/stage_a1/venue_and_archive.json`: `funding_post_period`, `row_count` 72, `gated_rows` **72**, `readable_rows` 0.
  - `ETFExperiment/reports/stage_a1/depth.json`: `funding_2025_05_page`, `row_count` 500, `gated_rows` **500**, first_time 2025-05-01T00:00:00.104Z.
  - 72 + 500 = **572 of 572** — the count is right, and it comes from **two** pages, not three.
  - The other three funding pages that passed a reader are entirely **pre**-boundary and have `gated_rows` 0: `funding_pre_period` (72 rows, first_time 2025-04-01), `funding_2024_01` (500 rows, 2024-01-01…2024-01-21), `funding_2023_05` (500 rows, 2023-05-13…2023-06-25). Five pages total, three of them pre-boundary.
- **Recomputation (if any):** inputs `reports/stage_a1/venue_and_archive.json` and `reports/stage_a1/depth.json` at the anchor; method: sum `gated_rows` and `row_count` over every funding probe whose stamps fall at or after `CONFIG.pre_period_end_ms`. Result 572 of 572 over 2 pages; tolerance exact.
- **What would resolve it:** "across two pages", or a third post-boundary funding probe if one exists outside these two artifacts. I found none.
- **Confidence:** HIGH — the page count is a direct read of two anchored artifacts.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no.

### DRAFT-V-6
- **Repository / SHA:** ETFExperiment / `4d110027674e7b4cd2861cf4e0e74f975111daf1`
- **Hypothesis or artifact:** Stage A.1 Task 2 pacing rule
- **Direction:** neutral (hygiene)
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Paces are set at **twice the fastest verified-clean spacing** — half the highest verified-clean *rate*, because there is no ceiling to halve." — ETFExperiment/report.md:150-151
- **Evidence:**
  - The sentence asserts that the two formulations are the same rule. For `archive.timemap` they are not. `ETFExperiment/reports/stage_a1/rate_ceilings.json` records rungs at 5.0 s (5.78/min), 2.0 s (**21.28/min**) and 1.0 s (12.29/min), all HTTP 200, with `highest_verified_clean_rate_per_min` 21.28 and `operating_min_spacing_s` **2.0**.
  - Twice the fastest verified-clean spacing = 2 × 1.0 s = **2.0 s** — the operating value.
  - Half the highest verified-clean rate = 21.28 / 2 = 10.64/min = **5.64 s** — 2.8× slower than the operating value.
  - The divergence exists because this endpoint's observed rate **fell** at the tighter rung (12.29/min at 1.0 s spacing against 21.28/min at 2.0 s), so rate and spacing are not monotone for it. The two formulations agree, to rounding, on the other five endpoints (flow.table 10.0 s vs 9.86 s; the four 2.0 s endpoints vs 2.00–2.04 s).
  - The table this sentence sits under (ETFExperiment/report.md:141-148) prints `archive.timemap | 21.28/min (n = 18) | 2.0 s`, so both halves of the contradiction are on the same page.
- **Recomputation (if any):** inputs `reports/stage_a1/rate_ceilings.json` (all 6 endpoints, 16 rungs, 96 requests); method: for each endpoint compute 2 × (fastest all-200 spacing) and 60 / (highest_verified_clean_rate / 2) and compare to `operating_min_spacing_s`. Result as above; tolerance exact to 0.01 s.
- **What would resolve it:** naming one of the two formulations as the rule and deriving the other, or recording that they diverge for `archive.timemap` and which one the operating pace follows. Nothing scientific turns on it; this is a courtesy-pacing statement, and the operating pace is at 2.0 s against a floor of 1.0 s either way.
- **Confidence:** HIGH — arithmetic on one anchored artifact.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — though the neighbouring sentence does disclose the related limitation that "The figures are bounded by what was probed, not by what the server would" (ETFExperiment/report.md:155).

---

## 6. What could not be checked, and why

| Item | Why not | What is missing |
|---|---|---|
| **Pre-period daily sd 0.027431 (n = 475) and mean hourly funding 0.00002226 (n = 11,423 over 23 pages)** at the primitive level | `ETFExperiment/scripts/preperiod_inputs.py` writes only the summary; the 1d candle payload and the 23 funding pages were **never written to disk** and are absent from `data/`. Every derived quantity that can be checked against the summary does check (24-hour sum, annualisation, 476 closes → 475 returns, 22×500+423 = 11,423) | the raw payloads; irrecoverable without refetching the venue, which is out of scope and would also be a new network call the repository's own closure forbids |
| **"Two of the six [mutations] required fixing the harness rather than the source"** (`report.md:419`) | `reports/stage_a4/mutations.log` records outcome flags only — no diff, no failing test id, no harness-vs-source attribution | a per-mutation record naming the failure site |
| **"`make lint`, `make typecheck` and `make test` are green: ruff clean, mypy strict clean"** (`report.md:401-403`) | no gate output is stored in the repository. The **76** file count verifies exactly (34 src + 26 tests + 16 scripts against `pyproject.toml:44`); "green" does not, and re-running the repository's gates is outside a read-only audit | a stored lint/typecheck/test report, or a CI log |
| **Every carried external statistic** — Newey-West t 3.12 (n = 313), t 8.99, IV F 21.58, Granger β 0.47 / t 9.75, reversal t −2.42..−3.99, 10-day t 4.49, IV t 2.65 (n = 563), the 90-day rolling 0.16 vs 0.68 | measured by other authors on data this repository does not hold, and **explicitly labelled carried** at `REGISTRATION.md:482-485` | the source studies' data. Only t 3.12 propagates into a bar (via ρ ≈ 0.18 → registered 0.09); the arithmetic of that propagation **is** checked, at C23 |
| **The Section 0 verdict object and the as-printed observability verdict** as computed objects | `src/etf/section0.py:fire_section0` and `src/etf/observability.py:fire_observability` are called by nothing outside their own tests; no verdict artifact exists under `reports/`. I verified instead that the *inputs* the prose verdict cites reproduce, and that the prose verdict is what the functions would return on those inputs (density 0.0330 < 0.60 → `density_ok` False; `fire_observability` **raises** on `revision_days = 0`, so the forward leg genuinely cannot be evaluated, which is what the documents say) | a stored verdict object, or a script that fires the gate and writes its output |
| **Whether a working forward snapshotter would have made every printed day admissible** — the assumption behind `DRAFT-V-1` | the collector ran for ~6 h over a single trade date, was disarmed at 2026-08-29T02:43:48Z, and produced 0 admissible days from 0 completed forward days | at least one completed forward print inside the qualifying window. The retro evidence is suggestive on both sides: served captures run +04:05 to **+07:59:42**, i.e. up against the 08:00Z anchor |
| **Everything under `data/`** as an anchored fact | `.gitignore` line 2 excludes `data/` in full, so no raw primitive is in the snapshot. Six claims (C07a-c, C14, C15a-b, C17, C28) could only be checked against untracked files | nothing missing for the check itself — the files exist and reproduce — but every figure derived from them is **UNANCHORED**, carries its read time (2026-09-05T05:52Z–05:59Z), and may have changed after the anchor. Two files demonstrably did: the request ledger grew 220 → 238 and the snapshot ledger 2 → 20 captures, both before the collectors were disarmed |

---

## 7. Live-repo access log

Per COMMON_RULES, `git status --porcelain` was run on the live repository before the first access
and after the last. Both outputs are recorded verbatim.

**Before first access — 2026-09-05T05:48:34Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

**After last access — 2026-09-05T06:04:15Z**

```
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment status --porcelain
(no output — clean, exit 0)
$ git -C /home/kiros-li/Documents/GitHub/ETFExperiment rev-parse HEAD
4d110027674e7b4cd2861cf4e0e74f975111daf1
```

`HEAD` matched the anchored SHA before and after. **Nothing in the audited repository was
modified, and no repository script was executed in place.** The one untracked working-tree entry
that does not appear in `status` — `_CLOSED_DO_NOT_RUN_HERE`, excluded via `.git/info/exclude`
line 7, owner-written 2026-09-02 — was recorded in the LOCATE pass and is not mine.

**Read-only operations performed on the live repository**

| time (UTC) | operation | purpose |
|---|---|---|
| 05:48:34 | `git status --porcelain`, `git rev-parse HEAD` | pre-access record |
| 05:52 | `ls -la data/access/`; read `data/access/timemap-recent.txt`, `timemap-all_data.txt`, `farside_all_parsed.json` | C07a-c, C14 — memento counts, the 333-day universe, the all-dash rows |
| 05:52 | read `data/snapshots/flow_snapshots.jsonl` row count and open-day state | `DRAFT-V-1` — forward-capture admissibility |
| 05:56 | read `data/access/sosovalue-btc.html` (`__NEXT_DATA__` payload only) | C15a-b — the cross-check |
| 05:57 | read `data/outcomes/btc-1h-servable-window.json` — **`t` timestamps only, for row count, duplicate and gap checks; no price field was extracted or retained** | C10, C13 — the 5,002 / 5,001 reconciliation |
| 05:58 | read `data/ledgers/requests.jsonl` (476 lines) | C17 / `DRAFT-V-4` |
| 05:59 | `grep -cwiE 'evening|night'` over `data/access/farside-btc.html`, `farside-btc-all.html`, `sosovalue-btc.html` | C28 |
| 06:00 | `git log --date=iso-strict -12`, `git log -1 4d11002` | commit time of Amendment 6 for `DRAFT-V-4` |
| 06:04:15 | `git status --porcelain`, `git rev-parse HEAD` | post-access record |

No `.env`, keystore, session or credential file was opened. No file in the audited repository was
written. All computation ran under
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-etf-verify/` against a **copy** of
`src/etf` taken from the anchored snapshot; the audited tree was never used as a working
directory.

**Anchoring caveat.** Every figure derived from `data/` is UNANCHORED and carries its read time
above. The live tree stands clean at the anchored SHA, but `data/` moved after the anchor's
documents were written — the request ledger from 220 to 238 charges and the snapshot ledger from
2 to 20 captures, both between 2026-08-28T20:40Z and 2026-08-29T02:40Z. `DRAFT-V-4` turns on
exactly that movement. Nothing has been added since.
