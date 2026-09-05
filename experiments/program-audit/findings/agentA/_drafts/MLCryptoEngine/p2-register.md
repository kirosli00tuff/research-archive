# Agent A draft findings — MLCryptoEngine, part p2-register

**Repository:** MLCryptoEngine · **Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Assigned documents (primary evidence):** `HYPOTHESES.md`, `DECISIONS.md`, `AUDIT.md`, `docs/notes/`, `audit/`
**Direction:** A — closed too early or too hard.
**Read in full:** HYPOTHESES.md (572 lines), DECISIONS.md (2,701 lines), AUDIT.md (647 lines),
`docs/notes/h1-predictability-without-capturability.md`, `audit/census_ci.json` + `audit/*.py`.
`report.md`, `progress.md`, `CLAUDE.md`, `research/microstructure/*.py` and the live repo's untracked
`data/` were read for corroboration only; where a finding's *primary* evidence sits outside my
document set that is stated in the finding.

Eight draft findings: four S2, four S3.

---

### DRAFT-p2-register-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H3 / H6 — passive spread capture on thin Hyperliquid perpetuals; the D.1d order-lifecycle closure and the claim that it closes the whole thin tail
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A **negative bounded D.1 closes the thin tail (and H3) completely**" — MLCryptoEngine/HYPOTHESES.md:205
- **Evidence:** The census (C.27) scored ten thin perps and **five** cleared the pre-registered bars (BH q=0.10 + CI>0 + both-halves + ≥300 trades). Two of the five have by far the largest measured capture and were never carried into the order-lifecycle replay that closed H6: "NOT (+31) and TNSR (+35) survive but sub-capacity (positive_but_rare)" — MLCryptoEngine/HYPOTHESES.md:198. They were excluded on the **capacity tier alone**, not on sign or significance: NOT median daily USD $71k, TNSR $63k, against `CAPACITY_MEDIAN_DAILY_USD = 100_000.0` (MLCryptoEngine/research/microstructure/registered.py:63; the per-instrument table with the "($71k med)" / "($63k med)" annotations is MLCryptoEngine/report.md:4057-4058). Both clear the other capacity leg — `CAPACITY_TRADES_PER_DAY = 150.0` (registered.py:62) against n = 3,282 (NOT) and 5,205 (TNSR) scored prints over a 6.76-day recorded span = 485 and 770 trades/day (n and horizon from MLCryptoEngine/audit/census_ci.json, keys `NOT`/`TNSR`; the 96.4% coverage / 6.76-day span is MLCryptoEngine/HYPOTHESES.md:198 and registered.py:201-206). Their significance survives every correction the audit added: day-clustered 95% lower bounds **+29.18 (NOT)** and **+32.15 (TNSR)**, block-bootstrap **+28.91** and **+34.14** (`audit/census_ci.json`, fields `day_cluster_ci95_lower_bps` / `block_bootstrap_ci90_lower_bps`; recomputed below). H3's own registered reopening condition is "an instrument whose spread-to-cost ratio exceeds 1.0 *with* adverse selection below the excess" (MLCryptoEngine/HYPOTHESES.md:86) — a condition NOT and TNSR meet by 31 and 35 bps and which no later entry retires for them. The replay that closed H6 ran on PUMP and MERL only (MLCryptoEngine/HYPOTHESES.md:196-197; corrected headline MLCryptoEngine/report.md:5122).
- **Recomputation (if any):** Inputs: census worst-horizon nets PUMP +4.300, MERL +6.450, NOT +31.154, TNSR +35.504 bps **per round trip** (the census net is `full touch spread − adverse − ROUND_TRIP_BPS(3.0)`, MLCryptoEngine/research/microstructure/registered.py:57,107 and MLCryptoEngine/audit/census_ci.json); corrected bounded results PUMP −4.81 and MERL −4.35 bps **per leg** (MLCryptoEngine/report.md:5122), converted to round-trip by the project's own unit note "Per round trip the bounded result is **−9.62**, not −4.81" (MLCryptoEngine/report.md:5177; the same unit mismatch is audit finding A11, MLCryptoEngine/AUDIT.md:374-389). Method: express the fall from per-fill census accounting to the order-lifecycle replay in one unit and compare it against the two unreplayed survivors. Result (scratch: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p2/recompute.txt`): PUMP fall = 4.300 − (−9.620) = **13.92 bps/round trip**; MERL fall = 6.450 − (−8.700) = **15.15 bps/round trip**. Applying the *larger* of the two measured falls leaves **NOT at +16.00 and TNSR at +20.35 bps per round trip**, still positive. Driving NOT to zero needs a fall of 31.15 bps = **2.06×** the largest fall the replay actually produced; TNSR needs 35.50 = **2.34×**. The closure's own mechanism, at its own measured magnitude, does not reach them.
- **What would resolve it:** Run `research/microstructure/fill_replay.py` / `d1d.py` on the recorded NOT and TNSR fills for the census week — the raw capture is on disk and immutable (`data/raw/venue=hyperliquid/date=2026-08-04..08-11`, and NOT remained subscribed to 2026-08-13). One replay pass over 8 days took 166 s wall (MLCryptoEngine/report.md:5022). Either both go negative — and "closes the thin tail completely" is earned — or they do not, and H3's reopening condition is still live on two instruments.
- **Confidence:** MEDIUM — the arithmetic and the exclusion ground are certain, but the fall need not be constant across instruments (a thinner, wider-spread book could lose more per stale quote), so the replay is what settles it, not the extrapolation.
- **Invalidated by later commits?:** no — recording ended 2026-08-13 (MLCryptoEngine/DECISIONS.md:2583) and no later stage revisits the census population; the anchor is the project's terminal state on this question.
- **Disclosed by authors?:** partially — the sub-capacity exclusion and the "report the arithmetic and stop" routing are stated at MLCryptoEngine/report.md:4083-4085 and MLCryptoEngine/HYPOTHESES.md:198, but no document anywhere states that the thin-tail closure rests on two of five bar-clearing instruments, and HYPOTHESES.md:205 asserts the opposite ("completely").

---

### DRAFT-p2-register-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — short-horizon directional prediction; the C.14 four-day dispersion used to *strengthen* the closure
- **Direction:** A
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Across four full days the same measurement ranges −2.44 to +3.05 bps** — a draw from a distribution centred near zero, not a small positive edge." — MLCryptoEngine/HYPOTHESES.md:50
- **Evidence:** The same claim is repeated as the closure-strengthening argument in the outward-facing note: "That 3.31 bps came from a single day. Across four full days the same measurement ranges **−2.44 to +3.05 bps**: a draw from a distribution centred near zero, not a small positive edge." (MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:129-130), and "This did not reopen the question — it closed it harder." (same file, line 134). The four daily values are given at MLCryptoEngine/report.md:2366 (range −2.4378 to +3.0497) and MLCryptoEngine/report.md:2378 ("Phase B's headline **3.31 bps at 900 s came from 2026-07-31**, which is the +3.05 day here. On the other three full days the same measurement is +0.15, −2.44 and +0.74."). **n = 4 days.** The closure rests on a four-point sample being read as evidence of a null. Meanwhile the archive that would settle it was accumulating at zero cost: the live untracked capture holds **eleven complete 24-hour Coinbase days** (2026-07-31 and 2026-08-02 … 2026-08-11) out of 14 recorded dates, `data/raw/venue=coinbase/date=*/hour=*` in the live repository, read **2026-09-05T05:58Z** (UNANCHORED working-tree data; may have changed after the anchor — but the venue was retired on 2026-08-12 with immutable history, MLCryptoEngine/DECISIONS.md:2413-2425, so growth is not possible). C.14 ran on 2026-08-05, when four full days existed; the measurement was never re-run before recording stopped on 2026-08-13 (MLCryptoEngine/DECISIONS.md:2583), and the register still carries the n=4 figure at the anchor.
- **Recomputation (if any):** Inputs: the four daily 900 s gross-capture values +3.0497, +0.15, −2.4378, +0.74 bps (MLCryptoEngine/report.md:2366 for the two extremes, MLCryptoEngine/report.md:2378 for the middle two). Method: one-sample t on n=4. Result: mean **+0.3755 bps**, sd **2.2546**, se **1.1273**, t(0.975,3) = 3.1824 → **95% CI [−3.21, +3.97] bps**. The interval contains zero, contains the withdrawn 3.31 bps headline (H0: mean = 3.31 gives t = −2.60, two-sided p = 0.080, not rejected) and contains the 3.0 bps round trip of the cheapest reachable venue (H0: mean = 3.0 gives t = −2.33, p = 0.102, not rejected). At the measured sd, **n ≈ 5 full days** gives 80% power to separate a 3.0 bps mean from zero at α = 0.05 — one more day than was used, and seven fewer than were on disk by 2026-08-12. Working: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p2/recompute.txt` §1.
- **What would resolve it:** Re-run the C.14 900 s capture measurement on all eleven complete Coinbase days (and the eleven complete Kraken days) already on disk. The data is immutable and the replay path is the project's own; nothing is purchased and no venue is contacted. If the mean is then bounded away from 3 bps with a real interval, the "centred near zero" claim is earned; at n=4 it is not distinguishable from an edge that clears a 3 bps venue.
- **Confidence:** HIGH — the four values, the n, and the eleven complete days on disk are all directly observed; the arithmetic is a textbook one-sample t.
- **Invalidated by later commits?:** no — the register and the note both carry the n=4 claim at the anchored SHA, and recording ended nine days earlier.
- **Disclosed by authors?:** no for the arithmetic. The *sample* is disclosed ("six validated days … of which two are degraded", MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:192-197) and the project's own honesty rule says "A result on days of data is pipeline validation, not evidence of edge" (MLCryptoEngine/CLAUDE.md:130) — but no document states the interval this n produces, and the same n is used in the opposite direction, to *strengthen* a closure rather than to caveat it.

---

### DRAFT-p2-register-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H1 — the registered reopening condition, and the venue it says is unreachable
- **Direction:** A
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** READ
- **Claim challenged (verbatim quote):** "A round-trip cost below roughly **3 bps**, i.e. under 1.5 bps per side. On Coinbase that is the 0 bps maker tier requiring **$250M trailing 30-day volume**; on Kraken, the 0 bps maker tier at **$10M**. Neither is reachable at this project's capital." — MLCryptoEngine/HYPOTHESES.md:54
- **Evidence:** Three statements in the same two documents contradict the enumeration in that reopening cell. (1) The register's own venue-cost table: "| Hyperliquid perps, base tier | 1.5 bps | **3.0 bps** | 2026-08-01 |" — MLCryptoEngine/HYPOTHESES.md:307. That is the **base** tier; it requires no trailing volume. (2) The register's own summary of the cost landscape: "**The cheapest venue reachable from British Columbia is Hyperliquid at 3 bps**" — MLCryptoEngine/HYPOTHESES.md:322-323. (3) The standalone note repeats both halves 185 lines apart: the cost table at MLCryptoEngine/docs/notes/h1-predictability-without-capturability.md:76 and "Against the cheapest venue reachable from this operator's jurisdiction at all — Hyperliquid at **3 bps**" at lines 82-83, then quotes the reopening condition verbatim at line 261 asserting no reachable venue reaches it. The register's "Genuinely open" section restates the false enumeration flatly: "H1's reopening condition — sub-3 bps round trip needs $10M–$250M of trailing 30-day volume." — MLCryptoEngine/HYPOTHESES.md:516-517, filed under "**Would require a change in venue access, capital, or latency**" (line 513). No change in access is required: the project subscribed to Hyperliquid from 2026-08-01 and recorded 13 days across up to 27 instruments (MLCryptoEngine/DECISIONS.md:2390 for the 27-instrument subscription; MLCryptoEngine/progress.md:2792 for the 13 days). The directional pipeline was never run on it: H1's sample is "Coinbase and Kraken spot" (MLCryptoEngine/HYPOTHESES.md:51) and H2's is CME MBT (line 67); the note's scope section lists the venue set as "Kraken spot, Coinbase Advanced spot, CME MBT" (docs/notes/…:204-205). The feed supports the test at the deciding horizon: the capability matrix credits Hyperliquid with the BBO and trade feature classes measured at p50 123 ms bbo cadence, excluding only depth and sub-100 ms features (MLCryptoEngine/research/features/capabilities.py:11-31), while H1's deciding number is a **900 s** horizon figure (HYPOTHESES.md:50) — four orders of magnitude above the cadence limit. H2's reopening condition — "Reopens only on evidence of measurable AUC on a *different* instrument or feature class" (HYPOTHESES.md:70) — is likewise satisfiable by that untested venue and instrument set.
- **Recomputation (if any):** none needed for the inconsistency itself. Economic relevance: H1's deciding 900 s capture has a four-day 95% CI of [−3.21, +3.97] bps (DRAFT-p2-register-2), which straddles the 3.0 bps round trip this venue charges — so the question the reopening condition poses is genuinely open at that venue rather than settled by arithmetic.
- **What would resolve it:** Either correct the reopening cell to say that the threshold *is* met at Hyperliquid's base tier and state on what grounds the hypothesis nevertheless stays closed, or run the Phase B pipeline on the recorded Hyperliquid capture at the 60 s / 300 s / 900 s horizons with the BBO+trade feature set and report AUC beside gross capture per ADR-039 (DECISIONS.md:1740-1745). Both are free; the second consumes only data already on disk.
- **Confidence:** HIGH — every quoted figure is in the register itself, and the two statements are directly contradictory about the same venue.
- **Invalidated by later commits?:** no — the note carrying the contradiction was written at the anchor commit (ADR-065, MLCryptoEngine/DECISIONS.md:2579-2610) and its reopening quotation is pinned by test, so the wording is frozen rather than provisional.
- **Disclosed by authors?:** no — the register nowhere reconciles its own "cheapest reachable venue is Hyperliquid at 3 bps" with H1's "neither is reachable at this project's capital"; the note reconciles the two only for the 100 ms horizon (0.0291 bps missing 3 bps by ~100×, docs/notes/…:82-85), never for the 900 s horizon that decided H1.

---

### DRAFT-p2-register-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H10 — liquidation aftermath reversion, closed as "unidentifiable in available data"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "labeling the recorded week through per-user queries would take one polite request per fill-participant against 2.64M fills — weeks of querying to label seven days of history" — MLCryptoEngine/report.md:2668-2670 (this sentence is the sole cost ground for declining the venue's own liquidation label; the register's closure line it supports is "**Zero identifiable liquidations** in 2,639,510 recorded fills", MLCryptoEngine/HYPOTHESES.md:164) — *primary evidence for the quoted sentence lies in report.md, outside my assignment; the closure it produces, its status, its blocker and its reopening condition are all in HYPOTHESES.md:163-168, which is mine.*
- **Evidence:** The label exists and the project already used it successfully. The register's own closure line records that every recorded fill carries the counterparty addresses — "One key-set across every fill — `(coin, hash, px, side, sz, tid, time, users)`" (MLCryptoEngine/HYPOTHESES.md:164) — and that the venue's per-user endpoint was used to ground-truth an anomaly: "the one anomalous value (all-zeros hash, 18.0% of fills) ground-truths via `userFillsByTime` to **TWAP fills**" (same line). The stage states the label is there: "The venue *does* label liquidations — `userFillsByTime` fills carry a `liquidation` object when the fill was one — but only **per user**: you must already know the liquidated address to ask." (MLCryptoEngine/report.md:2664-2666). The recorded `users` field supplies exactly those addresses. The register also notes the field's existence as grounds for future reopening: "The venue's per-user `liquidation` field makes a future flag plausible" (MLCryptoEngine/HYPOTHESES.md:168). The reopening bar is not "label every fill" but "**≥ 300 labeled liquidations across the subscribed instruments**" (HYPOTHESES.md:168). The declining argument is therefore a cost estimate, and the unit in it is wrong: `userFillsByTime` is keyed by *address*, and one request returns all of that address's fills in the window — so the request count is bounded by distinct addresses, not by fills or by participant slots.
- **Recomputation (if any):** Inputs: the untracked live capture `data/raw/venue=hyperliquid/date=2026-08-0{1..6}/hour=*/messages.ndjson.zst` (the exact window the stage used, MLCryptoEngine/report.md:2645-2646), read **2026-09-05T05:55Z** (UNANCHORED working-tree data; the venue was stopped 2026-08-13 and raw capture is immutable under the project's own rule, so it cannot have grown). Method: stream every hour file, extract the `users` arrays from the `trades` channel, count occurrences and distinct 40-hex addresses (script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p2/count_users.sh`; per-day output in `fills_per_day.txt`). Result: **5,906,654 address occurrences** over the six days (= 2 per fill → 2,953,327 fills, the same order as the stage's 2,639,510 for its slightly shorter window) resolving to **62,905 distinct addresses**. The per-user labelling route therefore costs **at most 62,905 requests**, not one per fill-participant across 2.64M fills — an overstatement of **93.9×** read per participant slot, or **46.9×** read per fill. At 60 requests/minute that is **17.5 hours**; at a deliberately slow 10/minute, 104.8 hours. Neither is "weeks", and the bar is 300 labelled events, not 2.9M labelled fills. Working: `recompute.txt` §4.
- **What would resolve it:** Query `userFillsByTime` over the 62,905 recorded addresses for the recorded window and count fills carrying a `liquidation` object. If ≥300 land across the subscribed instruments, the pre-specified matched-control test at HYPOTHESES.md:168 runs as written on data already on disk; if fewer than 300 do, the closure becomes "too thin by prior declaration" on a measured count rather than "unidentifiable", which is a different and better-supported verdict.
- **Confidence:** MEDIUM-HIGH — the address count is directly measured and the endpoint's per-address semantics are stated by the project itself; what is not established is how many of those fills carry the flag, which is precisely the measurement that was declined.
- **Invalidated by later commits?:** no — no later stage revisits H10, and the recorded week is immutable.
- **Disclosed by authors?:** no — the per-user route is disclosed and explicitly declined, but on a cost figure the repository's own data contradicts by ~47–94×; nothing in HYPOTHESES.md, report.md or DECISIONS.md counts the distinct addresses.

---

### DRAFT-p2-register-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H11 class B (exchange netflow) — the +75-day publication lag that is both the applied handicap and the registered reopening constraint
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**(a)** a free exchange-flow source at **≤ 2-day** publication lag with **≥ 3 years** of history — the measured 75-day staleness is the binding data constraint on class B" — MLCryptoEngine/HYPOTHESES.md:185
- **Evidence:** The 75-day figure comes from exactly one retrieval of a file the project itself classifies as a living, whole-file-regenerating snapshot. The register: "publication lags applied per source — **A +1d, B +75d (measured: the free Coin Metrics snapshot ends 75 days before retrieval)**" (MLCryptoEngine/HYPOTHESES.md:182). ADR-042 makes the override binding — "**A measured delay overrides a documented one, in whichever direction.** The 75-day CM staleness went into the study as 75 days" (MLCryptoEngine/DECISIONS.md:1875-1877) — and in the same ADR anticipates repeated retrieval: "**Living snapshots are archived dated.** A source that regenerates its whole file (CM) … cannot land at a stable path without hiding revisions. Each retrieval is an immutable dated snapshot" (DECISIONS.md:1878-1882). Only one retrieval ever happened. The provenance manifest contains exactly two `coinmetrics_community` lines, both `"retrieved_at":"2026-08-06T14:06:2…Z"`, both `"period":"2026-08-06"`, from `https://raw.githubusercontent.com/coinmetrics/data/master/csv/btc.csv` and `…/eth.csv` (live `data/vendor/archive/manifest.jsonl`, 14,191 lines, read **2026-09-05T06:00Z**, UNANCHORED). The archived file's last row is dated **2026-05-24** (live `data/vendor/archive/coinmetrics/asset=btc/btc_2026-08-06.csv`, tail, same read time), confirming the 74–75 day gap for that one snapshot and nothing about the source's steady-state cadence. The project's own precedent for exactly this failure mode is ADR-018: "**a single-day measurement of an expiring instrument measures the expiry, not the instrument.** … any capability decision resting on one session must state which session" (MLCryptoEngine/DECISIONS.md:691-694). The consequence is load-bearing: ADR-042 records that "Without the measured override, class B would have shown the freshest signal in the study" (DECISIONS.md:1890-1892), and class B still returned 7/8 cells with positive net Sharpe under the handicap (MLCryptoEngine/report.md:2797-2798). The re-measurement is a single free HTTPS GET of a public GitHub raw file whose commit history is itself free to inspect; sixteen further project days elapsed (2026-08-06 → 2026-08-22) and no second retrieval was made.
- **Recomputation (if any):** none — the finding is that the deciding figure has n = 1. Manifest count of `coinmetrics` provenance lines: 2 (one per asset, one retrieval date). Days between the archived file's last row (2026-05-24) and its retrieval (2026-08-06): 74.
- **What would resolve it:** Re-fetch `coinmetrics/data` at any later date and compare last-row date against retrieval date, or read the upstream repository's commit history for the two CSVs. If the file is normally current to ~1–2 days, the +75d handicap applied to class B was an artefact of one stale snapshot, H11's reopening condition (a) is already satisfied by the source the stage used, and class B needs re-scoring at its true lag. If 75 days is the source's steady state, the closure and the reopening condition are both confirmed on a second sample.
- **Confidence:** MEDIUM — that the measurement is n=1 and never repeated is certain; whether it is unrepresentative is exactly what was never checked.
- **Invalidated by later commits?:** no — the anchored commit is the project's terminal state and contains no second retrieval.
- **Disclosed by authors?:** partially — the snapshot's retrieval date and the whole-file-regeneration property are disclosed (MLCryptoEngine/report.md:2734; DECISIONS.md:1878-1882), but no document states that the binding lag rests on a single observation, and the register presents it as "the measured 75-day staleness" without an n.

---

### DRAFT-p2-register-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 / C.27 census — GMX's demotion from survivor to "unresolved" on a day-clustered interval
- **Direction:** A
- **Class:** ARITHMETIC
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "PUMP and MERL survive HAC, day-clustered and block-bootstrap correction; **GMX does not** (+0.288 IID → **−0.070** day-clustered) and should be read as **unresolved, not a survivor**." — MLCryptoEngine/HYPOTHESES.md:198
- **Evidence:** The −0.070 is a **two-sided** t(0.975, 6) bound applied to a bar the same audit shows is one-sided, and it is not what the repository's own corrected code or its own committed evidence artefact produce. Audit finding A6: "The registered bar is *'95% CI lower bound > 0'* and the p-value on the next line is explicitly `p_one_sided`. But `student_t.ppf(0.5 + 0.95/2, n-1)` = 1.96 — the two-sided 95% value; a one-sided 95% bound needs 1.645." (MLCryptoEngine/AUDIT.md:264-271). The corrected implementation shipped at the anchor computes the day-clustered bound with the **one-sided** critical value: `mean - float(student_t.ppf(CONFIDENCE, clusters - 1)) * day_se` with `CONFIDENCE = 0.95` (MLCryptoEngine/research/microstructure/registered.py:181-185 and :64), and its docstring says so — "``ci95_lower_bps`` is the A6 correction: a one-sided registered bar … judged with the one-sided critical value" (registered.py:167-170). The committed audit artefact agrees with the code and not with the prose: `"GMX": { … "day_cluster_ci95_lower_bps": 0.028088199564967276, "block_bootstrap_ci90_lower_bps": 0.10088443048485143 }` (MLCryptoEngine/audit/census_ci.json). Both bounds are **above zero**. The −0.070 figure is repeated in AUDIT.md:193 and MLCryptoEngine/report.md:5150 and frozen into the permanent register at HYPOTHESES.md:198.
- **Recomputation (if any):** Inputs from MLCryptoEngine/audit/census_ci.json key `GMX`: `net_mean_bps` 0.404431, `day_cluster_se` 0.193692, `n_days` 7. Method: reproduce both critical-value conventions. Result: one-sided t(0.95,6) = 1.9432 → lower bound **+0.0281** (matches the JSON field to 4 dp); two-sided t(0.975,6) = 2.4469 → lower bound **−0.0695** (matches the published −0.070). Block-bootstrap 5th-percentile lower bound **+0.1009**. Under the convention the registered bar actually specifies and the corrected code actually implements, GMX clears zero on the IID, HAC, day-clustered **and** block-bootstrap intervals. Working: `recompute.txt` §3.
- **What would resolve it:** State GMX's day-clustered bound under the same one-sided convention the corrected code uses (+0.028), or state explicitly that the demotion uses a stricter two-sided convention and why. Either way the register should not carry a number the repository's own shipped implementation no longer produces.
- **Confidence:** HIGH — the discrepancy is exactly reproducible from the committed artefact and the committed source, and both conventions are named in the repository's own text.
- **Invalidated by later commits?:** no — `registered.py`, `audit/census_ci.json` and `HYPOTHESES.md` are all at the anchored SHA and disagree with each other there.
- **Disclosed by authors?:** no for the discrepancy. The authors do disclose an independent ground for discounting GMX — its net "flips negative at 300 s (−0.04, CI −0.25) and 900 s (−0.45, CI −0.76)" (MLCryptoEngine/report.md:4495-4497, summarised at HYPOTHESES.md:204) — which is why this is S3 and not S2: GMX's discount survives even though the quoted statistic does not.

---

### DRAFT-p2-register-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 / H3 — the three pending clocks the register says still read out, and the "screened positives" demotion they were registered to resolve
- **Direction:** A
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "Two clocks still read out for the record: the Hyperliquid latency distribution (2026-08-19, moot for the sign) and the blind-universe scoring window (2026-09-09, now a selection-bias check)." — MLCryptoEngine/HYPOTHESES.md:263-265
- **Evidence:** All three of the register's pending clocks were foreclosed by a recording stop recorded in the same repository at the same anchor. (1) HYPOTHESES.md:197: "The blind window closing 2026-09-09 still reads out — as a selection-bias check". (2) HYPOTHESES.md:205: the ≥4-week re-run "which the recorders accrue at zero cost by ~2026-09-08" (the same accrual promise is at MLCryptoEngine/DECISIONS.md:2296-2297 and :2371). (3) The latency clock at HYPOTHESES.md:264. Against these: "**Context.** Recording ended 2026-08-13 with every register entry closed." — MLCryptoEngine/DECISIONS.md:2583 (ADR-065, dated 2026-08-22, the anchor date). The blind universe was registered on 2026-08-12 with "Earliest close 2026-09-09" and a scoring rule requiring "a fresh ≥ 4-week window from subscription spanning > 1 volatility regime" (MLCryptoEngine/DECISIONS.md:2391-2393), and the subscription restart is dated 2026-08-12 — so exactly **one day** of the required ≥28 was ever captured. The consequence is the part not carried into the register: the D.1c selection audit demoted the census survivors — "the C.9 pick was a **spread-motivated screen** … survivors demote to **screened positives**; BH corrected the 10 tested, not the 177 screened; an unbiased volume-band rule blind to spread fields folds into the ≥ 4-week re-run" (MLCryptoEngine/HYPOTHESES.md:204) — and ADR-059 exists precisely so that "The screened-positive demotion becomes resolvable by measurement instead of standing forever" (MLCryptoEngine/DECISIONS.md:2395-2396). With the window abandoned, the demotion now stands forever, and neither HYPOTHESES.md nor DECISIONS.md says so.
- **Recomputation (if any):** none. Elapsed capture on the blind universe: subscription restart 2026-08-12 (DECISIONS.md:2390; session marker cited at MLCryptoEngine/report.md:4658) to recording stop 2026-08-13 = **1 day** against the registered ≥28.
- **What would resolve it:** Amend the register's three pending-clock statements to record that the windows were closed by the 2026-08-13 stop, and state plainly that the screened-positive demotion of PUMP and MERL is unresolved rather than pending. If the demotion matters to the closure — and ADR-059 was written on the premise that it does — restarting the Hyperliquid recorder for four weeks is one config flip and ~8.4 GB (DECISIONS.md:2423-2426).
- **Confidence:** HIGH — every date is stated in the repository, and the arithmetic is one subtraction.
- **Invalidated by later commits?:** no — DECISIONS.md:2583 and HYPOTHESES.md:263-265 are both at the anchored SHA and contradict each other there.
- **Disclosed by authors?:** yes (MLCryptoEngine/progress.md:2782-2784: "The 27-instrument blind universe subscribed on 2026-08-12 is therefore left with 1 day of capture and is **not** a scoreable window; it should not be treated as one."). The authors disclosed it in progress.md on 2026-08-13; the finding is that the register — the file the project itself tells a future reader to start from for "the register and every reopening condition" (MLCryptoEngine/progress.md:2800-2802) — was edited on 2026-08-22 for ADR-065 and E.1 and still says the opposite. Severity is capped at S3 for that reason.

---

### DRAFT-p2-register-8
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H2 — transfer to CME micro futures, labelled "signal-absent"
- **Direction:** A
- **Class:** OVER_CLOSED
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Closed — signal-absent** · 2026-08-03" — MLCryptoEngine/HYPOTHESES.md:65 (the register defines the label as the non-reopening one: "**Signal-absent**: there is nothing to capture. **Does not reopen on a better model, a better feature set, or lower fees.**" — MLCryptoEngine/HYPOTHESES.md:32-34)
- **Evidence:** The harshest label in the project's own taxonomy is applied to a result the project simultaneously records as resting on one walk-forward fold: "Stage C.8 reports **one clean fold**, not two and not three, and states that six months would give three. This is recorded as a limitation of the range, which is a purchasing decision (ADR-021), not a modelling one — the fix is more data, not a smaller window." (MLCryptoEngine/DECISIONS.md:1005-1008). The purchasing decision stopped at two of four months because a charge was committed for bytes never delivered: "June was priced, committed, and **OOM-killed mid-download** by a defect in our own fetch path (ADR-022) after its $35.51 had been charged to the ledger … **The stage stopped at two months rather than raise it.** July was never attempted." (MLCryptoEngine/DECISIONS.md:855-859). ADR-021 names the free recovery step and never records it being taken: "Resuming June and July requires first reconciling the June charge against the Databento invoice — the client exposes no usage endpoint, so only the portal can say whether the killed stream was billed. If it was not, reversing that entry makes all four months affordable under the unchanged cap." (MLCryptoEngine/DECISIONS.md:865-868). The live spend ledger confirms neither the reversal nor any further purchase ever happened: 29 entries totalling **$82.1179** against the $120 cap, last entry timestamped `2026-08-04T05:37:07Z`, no reversal record, no July purchase (live `data/vendor/spend_ledger.jsonl`, read **2026-09-05T05:59Z**, UNANCHORED working-tree data). The word "portal" appears in the repository only in the two places that propose the check (MLCryptoEngine/DECISIONS.md:866 and MLCryptoEngine/progress.md:1015-1017), never in a record of its result.
- **Recomputation (if any):** Inputs: ledger entries (live `data/vendor/spend_ledger.jsonl`); cap $120 (MLCryptoEngine/DECISIONS.md:846); month quotes June $36.1880, July $21.2955 (MLCryptoEngine/progress.md:975). Method: sum the ledger's `usd` field and compare with the cap. Result: spend **$82.1179**, headroom **$37.8821**. The undelivered June entry is $35.5144 of that spend; reversing it leaves $73.40 of headroom against $57.48 needed for both months. Even without any reversal, the July month alone ($21.2955) fits inside the existing $37.88 headroom, so the cap was never the binding obstacle to a second, independent out-of-sample month.
- **What would resolve it:** Either check the vendor portal and reverse the undelivered charge (free), or relabel H2 from "signal-absent" to a cost-and-sample-bounded closure that says what one clean fold over two consecutive months of one contract can and cannot establish. The register's own taxonomy makes the difference material: "signal-absent" is declared not to reopen on more data, which is exactly what this closure lacks.
- **Confidence:** MEDIUM — the label's evidential basis (AUC 0.501 at every horizon, and the +0.215 → −0.785 bps stride-1 reversal, HYPOTHESES.md:66,70) is genuinely flat and may well survive more data; the finding is that the non-reopening label was assigned while the project's own documents said the fix was more data and the budget for it was unspent.
- **Invalidated by later commits?:** no — the ledger's final entry predates the anchor by 18 days and no later ADR revisits the range.
- **Disclosed by authors?:** yes, in part — the sample limitation is disclosed at MLCryptoEngine/HYPOTHESES.md:68 ("Two months of one contract … A single instrument on a single venue") and the unfinished purchase at DECISIONS.md:855-868. What is not disclosed anywhere is that the closure label chosen is the one the register defines as not reopening on more data, while the unspent budget and the unexecuted reconciliation both remained available. Severity is capped at S3 for the disclosed half.

---

## What I checked and found sound

Where the thesis did not hold. Each of these was examined specifically because it looked like a
candidate for premature closure, and the evidence did not support the finding.

- **The D.1d closure itself (H6, PUMP and MERL).** I looked hard for an arithmetic or model defect
  behind −4.81 / −4.35 and found the opposite: an adversarial audit re-derived the whole 28,658,883-record
  replay bit-exactly from raw (MLCryptoEngine/AUDIT.md:490), both real fill-path defects bias the result
  *upward* so correcting them made the closure stronger (AUDIT.md:591-592), the decomposition identity sums
  in code and by hand (AUDIT.md:489), pre-registration is clean with no threshold ever edited
  (AUDIT.md:492), and the census ran after its window closed (AUDIT.md:493). The audit's own decisive
  follow-up — correct A4 and re-run — **was** performed, with the predicted direction confirmed
  (MLCryptoEngine/report.md:5035-5060: PUMP −4.7503 → −4.8087, MERL −4.2314 → −4.3459).
- **The latency escape route for H6.** ADR-062's zero-crossing grid is a real test and it returns no
  crossing anywhere on {+0,+50,+100,+200,+400,+800} ms (MLCryptoEngine/DECISIONS.md:2489-2497;
  report.md:5125-5126). "Lower latency reopens it" is correctly excluded.
- **The withdrawal of the D.1d mechanism claim (ADR-064).** The project perturbed its own feed ordering,
  found the edge/inventory split unstable, and *withdrew the attribution while keeping the closure*
  (MLCryptoEngine/DECISIONS.md:2542-2574). It also rewrote H6's reopening condition because the old one
  "named a test that could not settle anything" (DECISIONS.md:2565-2571). That is the opposite of closing
  early on a story.
- **The withdrawal of a control that did not cover what it claimed (ADR-063).** The known-answer gate was
  struck rather than softened, replaced by a differential gate with a coverage assertion, and the
  replacement caught a real defect on its first run (MLCryptoEngine/DECISIONS.md:2505-2538). The residual
  — "the D.1d replay has still only run once with no second pair of eyes" (DECISIONS.md:2538) — is
  disclosed by the authors in those words.
- **H6's reopening route (b), a $10-minimum live or paper test.** I considered raising "a cheaper path was
  named and not tried": the register itself says venue fill-level ground truth "measures the net directly
  and needs no attribution at all" (MLCryptoEngine/HYPOTHESES.md:197), the venue minimum is $10
  (DECISIONS.md:2322), and the credential rule forbids order-placement keys only "in every stage before D"
  (MLCryptoEngine/CLAUDE.md:118-119) — D.1 is stage D. It does not hold as a finding: the registered
  design spends capital only on a *positive* D.1 ("a positive one is the first thing worth simulating for
  real capital", HYPOTHESES.md:205), and declining to spend money to confirm a negative is a defensible
  pre-registered rule rather than an early closure.
- **H4 (cointegration).** Break-even costs of 300–550 bps against a 3 bps venue mean cost was never the
  constraint (MLCryptoEngine/HYPOTHESES.md:102); the universe is survivorship-free by construction with
  12 of 60 members dying in sample (line 99); the holdout produced fewer hits than chance (91 vs 77.0,
  line 98). The reopening condition is a genuine two-clause threshold and neither clause is met in this
  repository. The one place the thesis could bite — ticker reuse and the LUNA splice — is handled by an
  explicit blunt rule (DECISIONS.md:1294-1304).
- **H9 (momentum).** The registered grid, the deflation over 12 trials, the dominant-beta benchmark and
  the separate executable universe are all applied, and each changed the conclusion in the honest
  direction (MLCryptoEngine/DECISIONS.md:1846-1856). The three cells clearing the literal bar cluster at
  one holding period, which the registration named in advance as a fitting artefact
  (HYPOTHESES.md:147).
- **H8's arithmetic.** +43.68 − 42.91 − 0.66 = +0.11 checks; the 1.76 vs 1.5 bps break-even margin is 17%
  as stated (HYPOTHESES.md:131,135). The named-but-untested variant — a cross-sectionally beta-hedged
  version — is explicitly disclosed as "a different hypothesis, and would need its own test"
  (HYPOTHESES.md:135), so it is a scoping statement rather than an unexamined escape route.
- **H5's reopening trigger.** "Current funding above roughly 10% annualised sustained for a quarter,
  measured live" (HYPOTHESES.md:118). No later entry in this repository measures funding above that
  threshold; the only later funding measurement is D.1c's, which found funding immaterial at ≤0.33 bps
  (HYPOTHESES.md:204). Trigger not met here.
- **H7's disclosure.** Its data condition was actively destroyed by the retirement of the kraken/coinbase
  feeds, and the register says so plainly, with the remedy and its cost: "the kraken/coinbase feeds were
  retired at D.1b (2026-08-12), so that overlap stopped accruing at 12 days; reopening H7 now requires
  restarting those recorders first (one config flip, ADR-060)" (MLCryptoEngine/HYPOTHESES.md:507-508).
  Fully disclosed; not a finding.
- **D2's cost closure.** The ~124,764-weighted price against a 60,000 cap was measured, not assumed, the
  cheaper restructure was tried and failed on identification (0/8 pools resolved a creator), and the
  end condition was registered before the probe (MLCryptoEngine/DECISIONS.md:2208-2226). The register
  labels the result "concluded, not closed-absent" and states the confirmation is priced out rather than
  refuted (HYPOTHESES.md:257).
- **A3's headline conclusion.** I re-derived every instrument's day-clustered and block-bootstrap bounds
  from `audit/census_ci.json`: PUMP and MERL do survive every correction (day-clustered lower bounds
  +3.74 and +2.70 one-sided, +3.59 and +1.73 two-sided; block-bootstrap +4.16 and +5.12). Only GMX's
  reported bound is convention-dependent (DRAFT-p2-register-6).
- **A8's direction.** The capacity-tier denominator error is conservative as claimed, and the corrected
  code now divides by the recorded span and takes a true median (`registered.py:196-206`). It could not
  have promoted NOT or TNSR across the $100k floor — a 3.5% rate correction against a 29–37% shortfall.
- **The H6 register row's superseded headline.** HYPOTHESES.md:197 still narrates the closure with the
  pre-correction −4.75 / −4.23 figures; the corrected −4.81 / −4.35 appear one row above at :196 with
  "(was −4.75 / −4.23)". Untidy but disclosed and directionally harmless — S4 hygiene at most, recorded
  here rather than raised.

## Live-repo access log

Live repository touched, read-only, for git history and untracked working-tree data
(`data/raw/venue=*`, `data/vendor/spend_ledger.jsonl`, `data/vendor/archive/manifest.jsonl`,
`data/vendor/archive/coinmetrics/asset=btc/btc_2026-08-06.csv`). No file under
`/home/kiros-li/Documents/GitHub/MLCryptoEngine` was opened for writing; no git state-changing command
was run. No `.env`, keystore, session or credential file was opened.

**Before** (`git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain`, 2026-09-05T05:54:52Z):

```
```

(empty — clean working tree; `git rev-parse HEAD` = `5359a11fc753cdcd2606aea991dae826293d0307`, identical to the anchor)

**After** (same command, 2026-09-05T06:02:49Z):

```
```

(empty — clean working tree; `git rev-parse HEAD` unchanged at `5359a11fc753cdcd2606aea991dae826293d0307`)

Scratch work, scripts and recomputation outputs are under
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentA-mlcrypto-p2/`.
