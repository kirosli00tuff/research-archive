# Agent B draft findings — MLCryptoEngine, part p1-report

Repository: MLCryptoEngine @ `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22).
Primary documents read in full: `report.md` (5,190 lines), `README.md` (83 lines).
Supporting reads (context only, other readers' primaries): `progress.md`, `HYPOTHESES.md`,
`AUDIT.md`, `data/validate/replay.py`, `research/detection/scorer.py`, and untracked artifacts
under `data/processed/` and `logs/` in the live working tree.

Standing note on this repository: it is unusually disciplined. Pre-registration commits precede
every result commit I checked (see §"What I checked and found sound"); the negatives are
corrected for multiplicity, survivorship and cost with a rigour most of the positives are not.
The findings below concentrate, per my assignment, on the places where a positive, a shipped
artifact or a PASS label is held to a weaker standard than the same repository applied to its
negatives.

---

### DRAFT-p1-report-1
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** Phase A acceptance — the venue-day **PASS** verdicts appended to `report.md`
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Phase A is accepted when **all** of the following hold, measured by the validation\nharness over recorded data:" … "4. Reconstructed top-of-book agrees with venue-provided snapshots wherever the venue\n   supplies them within tick-size tolerance." — MLCryptoEngine/report.md:10 and MLCryptoEngine/report.md:21-22
- **Evidence:**
  - The harness that emits PASS/FAIL never tests criterion 4. `data/validate/replay.py:690-732` builds `failure_reasons` from: no book data, uncertified integrity mechanism, `crossed_unexplained`, `seq_gaps_unexplained`, `checksum_failures_unexplained`, `checksums_verified == 0`, `valid_coverage_excl_gaps_pct < FULL_DAY_THRESHOLD*100`, and snapshot-silence. `snapshot_mismatches` is computed (`data/validate/replay.py:592`, `:673`) and printed (`data/validate/report_writer.py:73`) but appears in no failure branch — MLCryptoEngine/data/validate/replay.py:690-732.
  - On the very first accepted day, criterion 4 fails on its face and the day is still PASS: coinbase 2026-07-31 BTC-USD **7 mismatches of 12 snapshot compares**, ETH-USD **9 of 15**; kraken ETH/USD **2 of 6** — MLCryptoEngine/report.md:457 (heading "coinbase — 2026-07-31 — **PASS**"), :469, :470, :491 (kraken PASS), :504.
  - Hyperliquid 2026-08-03 is marked **PASS** with **6,616 of 16,099** (BTC) and **6,884 of 16,099** (ETH) mismatches, i.e. 41% — MLCryptoEngine/report.md:1289, :1301, :1302.
  - Criterion 4 was written 2026-07-30 08:04 in the repository's first commit `bde3082`, before any data (`git blame -L 8,23 5359a11 -- report.md`), and never amended (`git log -- report.md` shows no commit touching that block).
  - It was demoted **after** the mismatches existed, in `progress.md` and not in `report.md`: "TOB-vs-snapshot compares mismatch at some reconnect snapshots (coinbase 7 of 12 and 9 of 15, kraken 0 of 6 and 2 of 6): expected staleness across a disconnect, informational, not a pass/fail criterion." — MLCryptoEngine/progress.md:227-230, commit `301ea12` (2026-07-31), the same commit that records the PASS. The same bullet then asserts "both venue-days meet the stated criteria" — MLCryptoEngine/progress.md:231-232.
- **Recomputation (if any):** none needed; the counts are printed in the report's own tables and the code path is read directly.
- **What would resolve it:** either implement criterion 4 as a gate (with the stated tick-size tolerance and an explicit carve-out for post-reconnect staleness and for snapshot-stream venues), or amend `report.md`'s criterion list to say criterion 4 is diagnostic. As it stands a reader of `report.md` alone is told four criteria must all hold and shown a PASS where one demonstrably does not.
- **Confidence:** HIGH — the criterion text, the mismatch counts and the code path are all in the snapshot and mutually contradictory.
- **Invalidated by later commits?:** no — the criteria block and `replay.py` are unchanged at the anchor, and recording ended 2026-08-13 so no further validation runs exist.
- **Disclosed by authors?:** partially (MLCryptoEngine/progress.md:227-230) — progress.md records the mismatch counts and re-labels the criterion "informational, not a pass/fail criterion", but `report.md`, which states the criterion and prints the PASS, carries neither the demotion nor the counts' interpretation, and progress.md in the same bullet claims the venue-days "meet the stated criteria".

### DRAFT-p1-report-2
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 / detection track — the registered "lift noise floor" of 0.02 used to certify the C.24, C.25 and C.26 positives
- **Direction:** B
- **Class:** STATISTICAL
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "A decontaminated precision exceeding 0.570 by **≤ 0.02**\n   is **within-noise**, not signal (≈ 1 SE at the expected fold sizes)." — MLCryptoEngine/report.md:3514-3516
- **Evidence:**
  - The deciding C.24 cell: 6h behavioural decon precision **0.654** at recall **0.53** against base **0.557**, lift **+0.097** — MLCryptoEngine/report.md:3610.
  - The report's own sample size for it: "the lift is **marginal** (~+0.10 at n_test honest 97 → roughly 1.8 SE above base)" — MLCryptoEngine/report.md:3636-3637. Recomputing from those figures gives SE(precision) = 0.0537, so the registered 0.02 floor is **0.37 SE**, not ≈ 1 SE.
  - C.26 measures the standard error directly and confirms the same order: "+0.032, with SE ≈ 0.039, a 95% interval of **[−0.045, +0.109] that still includes zero**" — MLCryptoEngine/report.md:3947-3949. At SE 0.039 the 0.02 floor is **0.51 SE**.
  - Every verdict that leans on the floor is therefore a sub-one-standard-error result certified against a threshold advertised as one standard error: C.24 "lift +0.097 > 0.02" (report.md:3661-3662), C.25 "lift +0.047 > 0.02" and "mid-stratum lift +0.051 > 0.02" (report.md:3836-3838), C.26's mid-stratum "+0.032" settling "just above the 0.02 noise floor" (report.md:3952-3955).
- **Recomputation (if any):** inputs report.md:3610 (precision 0.654, recall 0.53, base 0.557) and report.md:3637 (n_test honest decon = 97; confirmed independently as 97 from the persisted matrix `data/processed/detection/behavior_c24.csv`, 2024 rows with `decon == honest_candidate`, read 2026-09-12 ~20:05 UTC, UNANCHORED). Method: TP = 0.53 × 97 = 51.4; predicted-positive n = TP / 0.654 = 78.6; SE = sqrt(0.654 × 0.346 / 78.6) = **0.0537**; lift/SE = 0.097 / 0.0537 = **1.81** (reproduces the report's "roughly 1.8 SE"); 0.02 / 0.0537 = **0.37 SE**. For SE to equal 0.02 the operating point would need **566** predicted-positive pools; the largest test fold anywhere in the track is 310 rows (`behavior_c25.csv`).
- **What would resolve it:** restate the floor as what it is — roughly 0.4–0.5 SE at the realised fold sizes — and re-read C.25's "survives" and C.26's "just above the noise floor" against a 1-SE (or CI-based) criterion, under which none of +0.047, +0.051 or +0.032 clears.
- **Confidence:** HIGH — the report supplies both the lift-to-SE ratio and the SE itself, and they are mutually inconsistent with "≈ 1 SE".
- **Invalidated by later commits?:** no — the detection track concluded at C.26 (2026-08-07) and nothing after the anchor revisits it.
- **Disclosed by authors?:** partially — C.26 discloses that the interval includes zero (report.md:3948-3949) and calls the finding "small and unconfirmed", but the "≈ 1 SE at the expected fold sizes" parenthetical is never corrected and the C.25 verdict (report.md:3835-3838) still reads the floor as a passed test.

### DRAFT-p1-report-3
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 — the C.24 "qualified positive at 6h+"
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**A cutoff cleared the honest bar above the noise floor (6h: 0.654 ≥ 0.60, lift\n+0.097 > 0.02), so the registered negative branch does not fire.**" — MLCryptoEngine/report.md:3661-3662
- **Evidence:**
  - The positive is one cell of a grid the report itself counts: "18 cells were scored\n(3 cutoffs × 3 sets × 2 labels)" — MLCryptoEngine/report.md:3639-3640. No multiplicity correction is applied to any of them; the C.24 pre-registration (report.md:3485-3526) registers a cutoff list, an unanswerable floor and a noise floor, but **no** multiplicity rule.
  - The same repository corrects its **negatives** for exactly this: Benjamini–Hochberg at q = 0.05 across 1,653 screened pairs and a deflated Sharpe over 1,653 trials in C.10 (report.md:1457-1470, :1590-1600); deflated Sharpe with n_trials = 12 in C.16 (report.md:2515-2517); n_trials = 40 in C.17 (report.md:2722-2723); and **BH q = 0.10 across the ten census instruments**, registered in advance, in C.18/C.27 (report.md:2882-2884, :4063-4064).
  - Under that same BH q = 0.10 standard applied to the 18 cells, the 6h decon cell does not survive: its one-sided p is 0.035 against a BH threshold of 0.0056 for the most significant of 18 (0.0167 even at k = 3).
  - The report's own hedge is a coherence argument, not a correction: "though the positive is coherent across 6h, 24h,\nboth label versions, and the behaviour-beats-launch comparison rather than one\nlone cell" (report.md:3640-3642) — but the 24h cell is the one the same page flags as base-rate-inflated ("At\n24h the honest base rate (0.630) **exceeds the 0.60 bar**, so a classifier that\ndoes nothing clears it", report.md:3594-3596), and the v0 label version is the one C.23 established measures the easy hard-rug boundary (report.md:3355-3360).
- **Recomputation (if any):** inputs report.md:3610 and :3637 as in DRAFT-2. Method: z = (0.654 − 0.557)/0.0537 = 1.81; one-sided p = 1 − Φ(1.81) = **0.0353**. BH q = 0.10 over m = 18: thresholds k·q/m = 0.0056 (k=1), 0.0111 (k=2), 0.0167 (k=3), 0.0333 (k=6). 0.0353 exceeds all of them, so no BH configuration over the scored grid declares this cell a discovery. Python: `scipy.stats.norm`, script under scratchpad work dir.
- **What would resolve it:** apply the project's own registered multiplicity standard (BH q = 0.10 across the 18 scored cells, or a deflated statistic with n_trials = 18) to the C.24 grid and restate the verdict, or state explicitly that the positive branch fired on an uncorrected bar while every negative in the project was corrected.
- **Confidence:** MEDIUM-HIGH — the arithmetic is straightforward and the asymmetry with the repository's own practice is documented, but the choice of which 18 cells constitute the family is mine, not the authors' (they neither registered a family nor corrected one).
- **Invalidated by later commits?:** no — C.25 and C.26 re-test the same positive and move it down (+0.047, then +0.032 with a CI including zero), which strengthens rather than weakens this finding.
- **Disclosed by authors?:** partially — the cell count and the marginality ("roughly 1.8 SE above base") are disclosed at report.md:3636-3642; the absence of any multiplicity correction, and the contrast with the project's own BH/DSR practice on its negatives, is not.

### DRAFT-p1-report-4
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D1 — the shipped hard-rug **clearance scorer** (`research/detection/scorer.py`, `data/processed/detection/hard_rug_scorer.txt`)
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "a *low* score **clears** a pool as not-a-hard-rug at **0.984 precision, covering 0.538 of honest pools**" — MLCryptoEngine/report.md:3652-3653 (restated at report.md:3968-3970 and in the artifact's own scope string, MLCryptoEngine/research/detection/scorer.py:105-118)
- **Evidence:**
  - The shipped model's metadata gives the exact fold: `test_n` 194, `test_hard_rug` 77 (so 117 honest), clearance point precision 0.9844 at recall 0.5385 — `data/processed/detection/hard_rug_scorer.meta.json` (live working tree, read 2026-09-12 ~20:00 UTC; UNANCHORED, untracked). Those numbers imply **TP = 63, predicted-clear = 64, FP = 1**: the headline 0.984 is 63/64 and rests on a **single** false clearance.
  - The false-clearance rate on the non-honest class is therefore 1/77 = 0.0130, with a Wilson 95% interval of **[0.0023, 0.070]**.
  - The repository sets itself the standard of scoring this track at the external base rate and applies it to its baselines: "**Any scorer on this track is judged on minority-class (honest-token) precision, never accuracy**" (report.md:3008-3009) and "At the external 98.7% launch-population base rate the honest precision of the\ntrivial classifiers is **0.013**" (report.md:3135-3136). The shipped scorer's headline is never re-expressed at that base rate anywhere in `report.md`, in `scorer.py`, or in the register entry.
  - Transferred to the base rates the project itself names, the same operating point gives: 0.984 at the test fold's honest base rate 0.603; **0.947** at the SolRPDS pool population's 0.299 (report.md:3086-3089); **0.354** at the external 0.013 the repo uses for its baselines — and **0.09 to 0.76** across the 95% interval of the one-error false-clearance rate.
- **Recomputation (if any):** inputs `hard_rug_scorer.meta.json` (test_n 194, test_hard_rug 77, precision 0.9844, recall 0.5385), report.md:3086-3089 (labels_v0 shares: hard_rug 65.3%, honest_candidate 29.9%), report.md:3135-3136 (external honest base rate 0.013). Method: TP = 0.5385 × 117 = 63.0; predicted-clear = TP/0.9844 = 64.0; FP = 1.0; FPR = 1/77 = 0.01297; precision(base) = base·0.5385 / (base·0.5385 + (1−base)·0.01297) → 0.984 at base 0.603, **0.947** at 0.299, **0.354** at 0.013. Wilson 95% CI for 1/77 = [0.0023, 0.0700] → precision at base 0.013 of **0.755** and **0.092** at the interval ends. Wilson 95% CI for 63/64 itself = [0.917, 0.997].
- **What would resolve it:** publish the clearance precision at the base rate of the population the tool would be pointed at, with the interval implied by a single observed false clearance; or state that the 0.984 figure is conditional on a fold constructed at a 0.603 honest base rate by the C.21 balanced stratified design (report.md:3176-3179) and is not the number a user of the artifact gets.
- **Confidence:** HIGH — the deciding counts are exact integers from the shipped artifact's own metadata, and the base-rate transfer is arithmetic the repository performs itself for its trivial baselines.
- **Invalidated by later commits?:** no — the scorer and its metadata are unchanged after 2026-08-07 and the detection track concluded.
- **Disclosed by authors?:** partially — the base-rate hazard is stated qualitatively in three places ("in the wild ~99% of launches are scam-adjacent, so this filters a small honest minority, not a calibrated general classifier", research/detection/scorer.py:117-118; report.md:3970-3972; HYPOTHESES.md:241), but it is never quantified, the one-false-positive basis of 0.984 is never stated, and the register still reads "Nothing reopens the *result* — it works" (MLCryptoEngine/HYPOTHESES.md:243, primary evidence outside my assignment).

### DRAFT-p1-report-5
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 — "the positive survives unbiasing" (C.25), carried into C.26's summary of what the detection track delivered
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "- **The behavioural finding.** Post-launch activity (6h) separates honest from\n  soft/slow rugs where launch-window state (C.23) could not — a real signal that\n  **survived depth-unbiasing at half its C.24 magnitude**" — MLCryptoEngine/report.md:3973-3975
- **Evidence:**
  - The two halves of that sentence rest on two disjoint measurements. The honest-versus-soft/slow separation is a **decontaminated-label** result measured only on the **biased** C.24 overlap ("decon, overlap (C.24 replay) | 0.654 | 0.557 | +0.096" — report.md:3798). The depth-unbiased result is a **v0-label** result ("v0, corrected | 0.822 | 0.775 | **+0.047**" — report.md:3797), and v0 cannot address the honest-versus-soft/slow question at all.
  - The repository established that itself: "**v0's \"honest\" class still contains the soft and slow rugs** (v0 only\nsplits off hard rugs), so 0.984 is *hard-rug detection* — the easy case" — MLCryptoEngine/report.md:3355-3357.
  - The substitution is confirmed in the persisted artifact: of the 310 rows in the 2024 test fold of `data/processed/detection/behavior_c25.csv`, **136 carry an empty `decon` field** — every one of the 166 depth-corrected pools (`source == c25_deep`) is unlabelled for decontamination. Read from the live working tree 2026-09-12 ~20:05 UTC (UNANCHORED, untracked). So no decon figure on the unbiased sample can exist, by construction.
  - The registered survival criterion was written on decon and the verdict was rendered on v0: "The C.24 positive is recorded as **surviving** the unbiased sample iff, at the 6h cutoff on the depth-corrected sample, **behavioural decon** lift over base is **> 0.02** *and* precision clears **0.60 at recall ≥ 0.50**" (report.md:3700-3706) versus "**The C.24 positive survives the unbiased sample by the registered criterion** (6h **v0** clears 0.60 at recall ≥ 0.5, lift +0.047 > 0.02)" (report.md:3835-3837).
  - The "clears 0.60" half of that criterion is vacuous on the corrected sample: the measured base rate is **0.775** (report.md:3797), above the 0.60 bar, so the all-honest classifier clears it at recall 1.0 — the identical defect the report flagged and asterisked for the 24h cell of C.24 (report.md:3594-3596) but not here. On the persisted (firmed) matrix the test-fold honest share is higher still, **253/310 = 0.816**.
- **Recomputation (if any):** inputs `data/processed/detection/behavior_c25.csv` (live tree, read 2026-09-12 ~20:05 UTC). Method: `csv.DictReader`; rows with `year == 2024` = 310, of which `cls == honest_candidate` = 253 → base 0.8161; `decon` empty on 136 of those 310; `source == c25_deep` = 166 rows, all `cls == honest_candidate`, all with empty `decon`.
- **What would resolve it:** state the composite claim as two separate, non-overlapping results — "decon separation measured on the biased sample; depth-unbiased survival measured on v0, which does not test the soft/slow boundary" — or drop the "separates honest from soft/slow rugs … survived depth-unbiasing" conjunction from the track's summary of deliverables.
- **Confidence:** HIGH — the label substitution is stated in the report and independently verified in the persisted matrix.
- **Invalidated by later commits?:** no — C.26 is the track's final stage and the matrix is unchanged after 2026-08-07.
- **Disclosed by authors?:** partially — C.25 §3 discloses the substitution plainly ("the corrected-sample bar runs on **v0 labels** … decon is reported only on the C.24 overlap for continuity", report.md:3782-3786) and warns that the base rate rose; the C.26 deliverables summary (report.md:3973-3978) and the register's D2 "Deciding number" row state the composite claim without it.

### DRAFT-p1-report-6
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** D2 — reproducibility of the C.24 6h headline
- **Direction:** B
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "Behavioural matrix persisted to `behavior_c24.csv` and the scorer to\n`hard_rug_scorer.txt`, both regenerable" — MLCryptoEngine/report.md:3679-3680
- **Evidence:**
  - The stage's deciding cell is the **6h** cutoff, whose retained population is **256** pools (report.md:3591); the report says so explicitly: "**The clean evidence is 6h**, where the base rate (0.557) is still below the bar" (report.md:3615-3617).
  - The persisted matrix is the **24h** population: `data/processed/detection/behavior_c24.csv` holds **231** data rows, matching the 24h row of the population table (report.md:3592), with a 2024 test fold of 154 rows and 97 decon-honest → base 97/154 = **0.630**, the 24h base rate, not the 6h 0.557. Its feature columns are un-prefixed (`n_tx`, `max_gap_s`, `time_since_last_at_cutoff_s`, `err_fraction`) — one cutoff only. Read from the live working tree 2026-09-12 ~20:05 UTC (UNANCHORED, untracked).
  - The one cutoff the report asterisks as untrustworthy ("*24h clears are base-rate-inflated (base > bar)", report.md:3615) is the one preserved; the one it calls the clean evidence is not.
  - Regeneration is not free at the anchor: the C.24 sweep cost 2,157 credits (report.md:3578) against "**1,199 of 60,000 remaining**" after C.26 (report.md:3998), and the project's own cap rule forbids a further raise.
- **Recomputation (if any):** inputs `data/processed/detection/behavior_c24.csv`. Method: row count 231; `Counter(year)` = {2024: 154, 2021: 26, 2022: 26, 2023: 25}; among 2024 rows `Counter(decon)` = {honest_candidate: 97, hard_rug: 37, soft_rug: 20} → honest base 97/154 = 0.6299, matching report.md:3592's 0.630 (24h) and not report.md:3591's 0.557 (6h).
- **What would resolve it:** persist the 6h feature matrix (or all three cutoffs), or state in the report that the persisted artifact backs the 24h cell only and that the headline 6h cell is not reproducible from anything on disk within the remaining budget.
- **Confidence:** HIGH — the row count and the recovered base rate identify the cutoff unambiguously.
- **Invalidated by later commits?:** no — the file is unchanged since 2026-08-07 and the track concluded.
- **Disclosed by authors?:** no — the report states the matrix is persisted and regenerable without saying which cutoff it holds.

### DRAFT-p1-report-7
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — D.1d's verdict caveats
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**deleting every\n  crossing fill still leaves both instruments negative** (−3.98 / −2.57)." — MLCryptoEngine/report.md:5002-5003
- **Evidence:**
  - The same document withdraws exactly those two numbers 70 lines earlier: "The figures originally given here\n> (PUMP **−3.98**, MERL **−2.57**, MERL improved **−3.43**) were obtained by\n> subtracting the crossing rows from the totals. That is invalid twice over" — MLCryptoEngine/report.md:4925-4928 — and replaces them: "Re-run properly (`_crossing_fills` disabled, all 8 days replayed) the answer is\n> **PUMP −4.35, MERL −2.13**" — MLCryptoEngine/report.md:4931-4933.
  - The register carries the corrected pair (**−4.35 / −2.13**) — MLCryptoEngine/HYPOTHESES.md:197 (primary evidence outside my assignment) — so the stale pair survives only in `report.md`'s own conclusion paragraph.
  - Direction of the error: the withdrawn figures are more favourable to PUMP's closure being marginal (−3.98 vs −4.35) and less favourable on MERL (−2.57 vs −2.13); the verdict (both negative) is unaffected either way.
- **Recomputation (if any):** none — the report supplies both the withdrawn and the corrected figures.
- **What would resolve it:** replace the pair in §5's caveat bullet with −4.35 / −2.13, or mark it as the `as_published` variant.
- **Confidence:** HIGH — both figures are in the same file and one is explicitly labelled invalid.
- **Invalidated by later commits?:** no — `report.md` was last touched by `d2a0f05` (2026-08-12), the very commit that added the withdrawal, and has not been edited since.
- **Disclosed by authors?:** yes for the arithmetic error itself (report.md:4925-4933); no for the fact that the superseded pair still stands in the verdict.

### DRAFT-p1-report-8
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 / C.27 — the "screened-positive demotion" and the blind-universe window registered to lift it
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**PUMP was a screened positive** (\"first above cost\") and **MERL sat\n  inside a 10-instrument multiplicity correction of a 177-perp screen**; the\n  blind window closing **2026-09-09** remains the first unbiased test" — MLCryptoEngine/report.md:4990-4993
- **Evidence:**
  - Recording stopped 2026-08-13T05:02:49Z, and the project's own final entry states the window will never be scoreable: "The 27-instrument blind\nuniverse subscribed on 2026-08-12 is therefore left with 1 day of capture and is\n**not** a scoreable window; it should not be treated as one." — MLCryptoEngine/progress.md:2782-2784 (commit `aeabff6`, 2026-08-12 22:05, i.e. 16 minutes after the last edit to `report.md` in `d2a0f05` at 21:49; `git log --date=iso -- report.md` and `git show --stat aeabff6`, which touches `progress.md` only).
  - `report.md` therefore still asserts a pending unbiased test in three places — report.md:4706 ("**Blind four-week scoring window earliest close: 2026-09-09**"), report.md:4790 ("the 2026-09-09 blind window reads out — the screened-positive demotion\n   stands until an unbiased selection is scored"), report.md:4993 — and the register agrees with the report rather than with progress.md: "The blind window closing 2026-09-09 still reads out — as a selection-bias check" (MLCryptoEngine/HYPOTHESES.md:197) and "Two clocks still read out for the record … the\nblind-universe scoring window (2026-09-09, now a selection-bias check)" (MLCryptoEngine/HYPOTHESES.md:263-265) — both primary evidence outside my assignment.
  - Consequence for the project's only bar-clearing positive: the D.1c selection audit measured that the C.9 pick was spread-motivated and that "BH q=0.10 was corrected across the 10 tested, not the 177 screened, so \"expected false positives 0.5\" understates the search that surfaced PUMP" (report.md:4522-4525), and registered that the demotion stands until an unbiased selection is scored (report.md:4789-4791). That correction now has no scheduled resolution, and `report.md` does not say so.
- **Recomputation (if any):** none — dating only, from `git log` / `git show` on the live repository (read-only).
- **What would resolve it:** a one-line amendment to report.md §D.1d.5 and to the register stating that the blind window was abandoned at the 2026-08-13 recording stop and that the screened-positive demotion on PUMP (and the 10-of-177 multiplicity gap) is permanently unresolved rather than pending.
- **Confidence:** HIGH — the cancellation is recorded in the repository's own progress log and the contradicting sentences are verbatim in report.md.
- **Invalidated by later commits?:** no — the anchor is 2026-08-22, nine days after the recording stop, and neither report.md nor HYPOTHESES.md was touched in between.
- **Disclosed by authors?:** partially — progress.md:2762-2784 discloses the stop and its reasoning fully; report.md and HYPOTHESES.md, the two documents the project tells a future reader to start from, do not carry it.

### DRAFT-p1-report-9
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** README.md — the project's framing to an outside reader
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "- **Phase A** — data pipeline, storage, order book reconstruction validated *(current)*" — MLCryptoEngine/README.md:79
- **Evidence:**
  - At the anchor the project has run Phase B (report.md:677+), the whole of Phase C (C.8–C.27), and Phase D.1a–D.1d; ended its alpha search by pre-registered decision on 2026-08-06 ("the alpha search of this project ends by decision, dated 2026-08-06", report.md:2847-2848); closed its last open hypothesis on 2026-08-12 ("H6 closes and D.2 does not follow", report.md:4973-4975); and stopped recording on 2026-08-13 (progress.md:2762-2768). README.md still presents Phase A as current and Phases B–E as forward plan.
  - The venue table lists Kraken spot, Coinbase Advanced Trade and CME micro futures (README.md:14-18) and **omits Hyperliquid entirely** — the venue that carries C.9, C.11, C.13, the H6 census, and every D.1 result, and the only venue still recording after 2026-08-12. Kraken and Coinbase were formally **retired** on 2026-08-12 with a new venue kind `retired` (report.md:4662-4700), while README.md:48 still instructs "Record public market data from Kraken and Coinbase" and README.md:61 "The recorder is meant to run continuously".
  - README.md:81 promises "**Phase C** — hftbacktest simulation with measured latency and true fee tiers"; D.1a measured that "`hftbacktest` and `numba` are not installed, and more fundamentally its queue models need observable L2/L3 book evolution the feed does not provide" (report.md:4229-4231).
  - README.md:82-83 present "**Phase D** — paper trading against live feeds on a placed VPS" and "**Phase E** — minimum viable live capital" with no indication that the register reached zero open alpha items.
  - README.md was last substantively edited on 2026-07-30 (`10c7579`); the only later change is the one-line Findings link added 2026-08-22 in `ae03bf6` (`git log -- README.md`).
- **Recomputation (if any):** none.
- **What would resolve it:** a status line on README.md recording that the research concluded, which venues are retired, and that Phases C–E as described were not reached; the single word "*(current)*" beside Phase A is the load-bearing error.
- **Confidence:** HIGH — the README text and the report's conclusions are both in the snapshot.
- **Invalidated by later commits?:** no — README.md is unchanged at the anchor and the project is complete.
- **Disclosed by authors?:** partially — README.md:66-68 points the reader to "`progress.md` for current status", which is accurate and current; the README's own Phase table, venue table and quick-start are not, and a reader who does not follow the pointer is left with a live-project picture.

### DRAFT-p1-report-10
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** C.20 — the viability gate that justified continuing the detection track ("avoidance is viable")
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**The mass does not sit in the first minutes. ~96% of the hard-rug class\noutlives any plausible score-and-act latency**, so avoidance tooling is viable\nfor this class" — MLCryptoEngine/report.md:3067-3069
- **Evidence:**
  - The ~96% is the complement of the 5-minute row: "within 5 minutes | **3.93%**" — MLCryptoEngine/report.md:3061. The same table gives the figures for the latencies the project's own deliverables actually operate at: "within 1 hour | 18.8%" (report.md:3062) and "within 24 hours | 41.5%" (report.md:3063).
  - No later stage of the project can act within 5 minutes. The shipped scorer scores at T0+30min: "The launch window is **1,800 s from first pool activity**" (report.md:3187-3188), and the register's extension path is "live deployment (score at T0+30min)" (HYPOTHESES.md:244, outside my assignment). The behavioural signal C.24/C.25/C.26 rest on does not exist before 6h: "1h fails, 6h and 24h clear" (report.md:3633-3634).
  - At those cutoffs the project measured the already-rugged fraction directly and it matches the C.20 table rather than the 96% headline: of 281 pools, 5 excluded at 1h, **25 at 6h**, **50 at 24h** for a prior label event (report.md:3590-3592), against 119 hard rugs in that sample — i.e. **21.0%** of hard rugs are already realised at the 6h cutoff and **42.0%** at 24h, reproducing C.20's 18.8%/41.5%.
  - So the avoidable fraction at the cutoff the track's positive lives at is ~79%, and ~58% at 24h — not ~96%. The viability figure is never restated after the cutoffs moved.
- **Recomputation (if any):** inputs report.md:3590-3592 (retained/excluded per cutoff) and the C.25 statement that the C.23 reached set is 281 pools of which 119 are hard rugs (report.md:3773-3775, "joined C.24's 281 → 258 honest + 119 hard-rug"). Method: 25/119 = 0.210 at 6h; 50/119 = 0.420 at 24h; compare report.md:3062-3063 (0.188 at 1h, 0.415 at 24h). Independent check on the persisted 24h matrix `behavior_c24.csv`: 231 retained = 281 − 50 ✓.
- **What would resolve it:** restate the viability figure at the cutoff the deliverables use (T0+30min, 6h, 24h) rather than at 5 minutes, or scope the ~96% claim explicitly to a hypothetical T0+5min scorer that the project never built.
- **Confidence:** MEDIUM-HIGH — the inputs are the authors' own tables and the 6h/24h exclusion counts corroborate them; what is contestable is only whether "any plausible score-and-act latency" was a fair characterisation when written, before the 30-minute window and the 6h cutoff existed.
- **Invalidated by later commits?:** no — C.20 was never revised and the track concluded at C.26.
- **Disclosed by authors?:** partially — the 1-hour and 24-hour rows sit in the same table (report.md:3062-3063) and C.24 discloses the per-cutoff exclusions; the conclusion sentence, and the "There is time to act on ~96% of hard rugs" restatement at report.md:3077, are not revisited.

### DRAFT-p1-report-11
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** H6 — D.1a's GO and D.1c's restated positive, after D.1d
- **Direction:** B
- **Class:** INTERNAL_INCONSISTENCY
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "PUMP and MERL stay\nnet-positive assumed always-last, so the capture's *sign* is settled independent\nof the unestimable term." — MLCryptoEngine/report.md:4236-4239
- **Evidence:**
  - D.1d measured the same two instruments at **−4.81 (PUMP)** and **−4.35 (MERL)** bps under an order-lifecycle fill model at the same always-last queue assumption — MLCryptoEngine/report.md:5122. The sign was not settled; it reversed.
  - The same over-claim is restated in D.1c and also stands unmarked: "Under the always-last bound\nthe queue-lengthening is already priced; the +2.15 lower end is **robust to\nentry**, not merely to queue position" (report.md:4391-4393) and "**PUMP**: estimate **+2.15 bps per round trip**" (report.md:4535-4536).
  - D.1c also treats two figures produced under the *same* every-print fill credit as mutual corroboration: "two independent routes to the same number, one per-fill and one\nthrough the position" (report.md:4473-4474). D.1d's own framing contradicts the independence: "D.1c's sim was generous on\nfills — every print credited min(print, quote) as though the quote sat at the\ntouch" (report.md:4717-4719), and the "routes" diverge by ~6 bps once fills are modelled.
  - The asymmetry is the point: `report.md` applies an explicit supersession banner to the **D.1d results** section, where an external audit challenged the *closure's* control and mechanism ("> **Partly superseded, 2026-08-12, by the adversarial audit …**", report.md:4799-4808), but no banner to the two earlier sections whose *positive* central claims the project's own subsequent measurement overturned.
- **Recomputation (if any):** none — all figures are printed in report.md.
- **What would resolve it:** a one-line supersession banner on §D.1a.5 and §D.1c.5 of the same kind D.1d received, and withdrawal of the "two independent routes" characterisation.
- **Confidence:** MEDIUM — the document is a dated chronological log in which later sections plainly supersede earlier ones, and D.1d does explain the fall (report.md:4976-4979); the finding is about which claims were marked and which were left standing, not about a hidden error.
- **Invalidated by later commits?:** no — report.md is unchanged after 2026-08-12.
- **Disclosed by authors?:** partially — D.1d states the fall from the per-fill accounting (report.md:4976-4979) and the register records the closure; the D.1a and D.1c sentences themselves carry no marking.

### DRAFT-p1-report-12
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** C.19 — the GO verdict that opened the detection track
- **Direction:** B
- **Class:** UNSUPPORTED_POSITIVE
- **Severity:** S3
- **Label:** READ
- **Claim challenged (verbatim quote):** "**Hit 1, indeterminate 3, missed 0.** The plain reading: no documented rug\nshows pre-event signals *provably absent* — the scheme as designed misses\nnothing" — MLCryptoEngine/report.md:2983-2985
- **Evidence:**
  - The registered failure condition was: "a heuristic\nscheme that misses documented rugs fails the audit" — MLCryptoEngine/report.md:2939-2942 (commit `35e3466`, before any probe). At evaluation it was operationalised as *provably absent*, so a scheme that produced a verified pre-event signal on **1 of 4** documented rugs — the other three "indeterminate without historical state" (report.md:2978-2981) — passed a bar written to fail schemes that miss documented rugs.
  - The GO's other deciding figure counts labels, not the coverage the bar required: "**GO requires ≥ 5,000\nlabeled tokens obtainable free with pre-event feature coverage**" (report.md:2939-2941) versus "the hard-rug class alone provides\n~76,000 labeled pools free, 15× the floor** — the audit is a **GO**" (report.md:3026-3027). The pre-event feature coverage the track then needed was measured, in the same section, as absent keylessly for three of the four mechanisms (report.md:2986-2992), and the realised feature-covered sample never exceeded **281** pools (C.23, report.md:3398-3400) — 5.6% of the registered floor.
  - The track's eventual conclusion is consistent with the bar's unmet clause rather than with its headline: the honest bar was never cleared on launch-window state (C.22 0.411/0.294, C.23 0.574), and C.26 ends with the confirming test "measured-unaffordable" (report.md:3987-3992).
- **Recomputation (if any):** none — 75,996/5,000 = 15.2 reproduces "15×" exactly; the point is which quantity is being counted.
- **What would resolve it:** state the GO as conditional — "≥ 5,000 labels obtainable free; pre-event feature coverage verified for one of four mechanisms and unavailable keylessly for three" — which is what the section's own §2 and §5 measure.
- **Confidence:** MEDIUM — on a literal reading the ≥5,000 clause is met (nine keyless pre-event fields are listed at report.md:3098-3108 and are obtainable for the whole SolRPDS set), so the finding is about the framing of "15× the floor" and the "misses nothing" reading of a 1-of-4 known-answer result, not about a fabricated number.
- **Invalidated by later commits?:** no — C.19 was never revised.
- **Disclosed by authors?:** yes for the inputs — the 1-hit/3-indeterminate table (report.md:2972-2981), the indexer requirement (report.md:2986-2992) and the "binding constraint" framing (report.md:3026-3040) are all in the same section; the finding is that the verdict sentence does not carry them.

### DRAFT-p1-report-13
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** C.22 — the "genuine information" claim for `top5_concentration_wend`
- **Direction:** B
- **Class:** ARITHMETIC
- **Severity:** S4
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "top5 concentration carries genuine\ninformation (precision 3–4× the 0.013 external base rate, ~1.3× the 0.30 SolRPDS\nbase rate)" — MLCryptoEngine/report.md:3329-3331
- **Evidence:**
  - The measured precisions in the row above are **0.411** (v0) and **0.294** (decontaminated) — MLCryptoEngine/report.md:3307-3308.
  - 0.411 / 0.013 = **31.6×** and 0.294 / 0.013 = **22.6×**, not "3–4×". The companion figure is right: 0.411/0.30 = 1.37 ≈ "~1.3×"; 0.294/0.30 = 0.98.
  - Separately, the 0.013 comparator is a different population from the one the precisions were measured on: 0.013 is the external launch-population honest base rate (report.md:3135-3136) while the fold's base rate is ~0.30 (report.md:3307-3308), so the ratio is not a like-for-like lift in either version.
- **Recomputation (if any):** inputs report.md:3307-3308 (0.411, 0.294) and report.md:3135-3136 (0.013). Method: direct division. 0.411/0.013 = 31.6; 0.294/0.013 = 22.6.
- **What would resolve it:** correct the multiple (or delete the cross-population comparison and keep only the ~1.3× against the fold's own base rate, which is the meaningful one).
- **Confidence:** HIGH — two-number division from figures on the same page.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no — the sentence stands uncorrected. Noting honestly that the error runs *against* the authors' interest (it understates their own result by an order of magnitude), so it is hygiene rather than over-claim; the cross-population framing is the part that flatters.

### DRAFT-p1-report-14
- **Repository / SHA:** MLCryptoEngine / 5359a11fc753cdcd2606aea991dae826293d0307
- **Hypothesis or artifact:** report.md's "Measured results" section, and the Kraken cost figure carried through C.8/C.10/C.14
- **Direction:** B
- **Class:** STALE_FIGURE
- **Severity:** S4
- **Label:** READ
- **Claim challenged (verbatim quote):** "### Data volume by venue and symbol\n\n(no data recorded yet)" — MLCryptoEngine/report.md:29-31 (identically at :35, :39, :43)
- **Evidence:**
  - All four "Measured results" tables still read "(no data recorded yet)" at a SHA where the project has recorded and closed a 14 GB archive across three venues (progress.md:2786-2792) and analysed 28.7M records in a single D.1d pass (report.md:4810). The section's own preamble says "The sections below are empty until data has been recorded and validated" (report.md:26).
  - Second instance: the Kraken base tier was corrected twice. The 2026-08-01 17:45 Phase B run records "kraken: maker 25.0 bps, taker 40.0 bps per leg (tier 0)" (report.md:681); the 2026-08-02 run records "kraken: maker 40.0 bps, taker 80.0 bps per leg (tier 0)" (report.md:773, commit `2299c7f`); and the tier was reconciled back to 25 bps maker / 50 bps round trip on 2026-08-08 (ADR-055, folded in at commit `81e456e`; stated in the shipped note, docs/notes/h1-predictability-without-capturability.md, cost table). C.8 (report.md:978, "Kraken ETH/USD (Phase B) | 80.00 bps"), C.10 ("80.0 bps at Kraken base-tier spot maker", report.md:1490-1491) and C.14 ("**5.00 bps against an 80 bps round trip**", report.md:2329) were never restated against the corrected tier.
- **Recomputation (if any):** none.
- **What would resolve it:** delete or fill the placeholder tables; and annotate the Kraken-cost rows with the ADR-055 correction.
- **Confidence:** HIGH — placeholders and superseded figures are verbatim in the file.
- **Invalidated by later commits?:** no.
- **Disclosed by authors?:** no for the placeholders. For the Kraken tier, the correction is disclosed in ADR-055/HYPOTHESES.md and in the shipped H1 note, but not in the report sections that use the old figure. Noting honestly that this staleness runs *against* the authors' interest — the corrected 50 bps round trip makes every affected result look better, not worse, and changes no verdict.

---

## What I checked and found sound

Where I expected the thesis to hold and it did not:

- **Pre-registration is real, and the commit order proves it.** Every registered-bar stage has a `docs: pre-register …` commit strictly preceding its results commit: C.14 `a2d7466` (2026-08-04 23:47) → `17df5ad`/`ddf525d`; C.16 `88b69d8` → `022a059`; C.17 `370ba41` → `4f1b030`; C.18 `6025f5c` → `287fc10`; C.19 `35e3466` → `f7a0bee`; C.20 `902d2e6` → `d1a7a7e`; C.24 `c1b469e` → `9294da1`; C.25 `5504352` → `41e6275`; C.26 `0c62d80` → `2403a8e`; D.1a `513d2c1` → `8b6fbc7`; D.1c `4b8bc1f` → `8ce2838`; D.1b `4bde24c` → `e544aa5`; D.1d `6a17edf` → `ed786ce`. The C.24 artifact `data/processed/detection/behavior_c24.csv` has mtime 2026-08-07 03:43, after its pre-registration commit at 02:45 and before its results commit at 03:57 — consistent with the claim that no C.24 data existed at registration. I found **no** case of a bar moved, widened or re-specified after its own result was known except the two noted above (Phase A criterion 4, and the decon→v0 substitution, both of which the authors record).
- **C.14 §1 is a bar reported against the project, not for it.** The registered rho branch was mis-specified for the world that occurred, the code was fixed *to* the registered text rather than the reverse (`5430eba`), and the outcome is reported as INCONCLUSIVE under the bar as written (report.md:2312-2318). That is the opposite of the amendment-rescues-verdict pattern.
- **C.10's deflated Sharpe arithmetic reproduces exactly.** With per-bar SR 0.0514, SR0 0.1058, T 1,095, skew 3.78, kurtosis 79.50 (report.md:1586-1592), the Bailey–López de Prado DSR is Φ(−1.943) = **0.0260**, matching the published 0.026 to three decimals. Annualisation also checks: 0.0514 × √365 = 0.982 ≈ the stated 0.98.
- **C.8's gross-capture identity is exact.** `gross = mean(EV) + mean(cost)` at 5.325 bps maker reproduces every row of report.md:1002-1009 (+0.005/+0.005/+0.005/+0.015/+0.045/+0.035/+0.085/+0.215) and the taker column at 7.255 bps.
- **C.9's decisive subtraction reproduces.** 0.164 − 0.215 − 3.000 = −3.051; 0.545 − 0.298 − 3.000 = −2.753; 2.640 − 0.678 − 6.211 = −4.249 (report.md:1210-1216). The CME ratio column also reproduces (M6A 3.099/3.178 = 0.98; MET 8.981/101.762 = 0.09; MBT 2.640/6.211 = 0.43).
- **C.13's break-even is right and its verdict is against itself.** 1.5 × (0.66 + 0.11)/0.66 = **1.75** bps a side, matching the published 1.76 and the "margin of 17%" (report.md:2185-2187); price/funding volatility ratio 1.81/0.166 = **10.9×** (report.md:2142-2145); fixed-cohort decile-spread decay (241.50 → 53.45) = **77.8%** (report.md:2050-2053).
- **C.11's own honest benchmark holds.** 5 of 10 instruments clear 4% cash, with margins 1.57–4.07 points (report.md:1831-1836), and the stage's headline is the decay, not the 8%.
- **C.16 and C.17 are negatives corrected harder than they needed to be** — DSR with n_trials 12 and 40, registered artifact patterns named in advance, executable-subset collapse reported (0.302 → 0.013), and C.17's FAIL triggering a pre-registered end of the alpha search.
- **The C.27 census bars were registered before the scored window closed** (`6025f5c`, 2026-08-06, window closing 2026-08-11) with BH q = 0.10, a ≥300-trade floor, both-halves robustness, a capacity tier and an explicit upper-bound statement, and the outcome-to-action map was followed verbatim rather than reasoned fresh (report.md:4089-4106). The known-answer gate reproduces C.9's closed BTC/ETH nets to −0.001/−0.003 bps.
- **The D.1d closure survives its own adversarial audit, and the corrections move it the unfavourable way for the authors' earlier claims but the favourable way for the closure** (PUMP −4.75 → −4.81, MERL −4.23 → −4.35; report.md:5029-5032). A1, A2 and A13 are recorded as withdrawals rather than as reinterpretations, including the sentence "the D.1d replay ran once, and no second pair of eyes has checked it" (report.md:4846-4847).
- **The C.27 statistical corrections were applied against the authors' interest**: A3 inflates the intervals 2–17×, demoting GMX from survivor to unresolved, and A6 records that the one-sided/two-sided error made the bar ~19% *harder* than registered (report.md:5139-5160).
- **The shipped H1 note (`docs/notes/h1-predictability-without-capturability.md`, linked from README.md:75) is scrupulous** — it carries the single-day origin of the 3.31 bps headline, the −2.44/+3.05 four-day range, the one-regime scope, the not-run ETH pair, and the external audit's "unaudited, not clean" label for its own closure. Its arithmetic checks: 50/0.0291 = 1,718 ≈ "1,700×"; 3/0.0291 = 103 ≈ "100×"; 80/5.00 = 16×.
- **The coverage-metric artifact (100.01–100.02%) is disclosed, bounded and verdict-neutral** (progress.md:221-227): the excess is ≤ 12.9 s ≈ 0.015% against a 99.9% threshold. I checked every PASS in report.md and found none whose verdict turns on it, and none where excluded recorder downtime materially rescued a day (the largest downtime exclusion on any PASS day is 574 ms, report.md:1942, :1978).
- **One rhetorical "first" I checked and am not filing as a finding:** C.27 calls itself "the project's first pre-registered-bar-clearing positive" (report.md:4005-4006) although C.24's honest bar (`902d2e6`) was pre-registered and cleared four days earlier (report.md:3661-3662). The register resolves it by placing the detection track "off the alpha register — ADR-044" (HYPOTHESES.md:225), so the two statements can be read consistently.

## Live-repo access log

Live repository touched read-only (`git log`, `git show`, `git blame`, `git rev-parse`, `git status`) plus read-only reads of untracked working-tree data under `data/processed/detection/`, `data/processed/reports/` and `logs/` (directory listings and CSV/JSON reads only; no `.env`, keystore, session or credential file was opened). All reads on 2026-09-12 between approximately 19:50 and 20:15 UTC; untracked data is UNANCHORED and may have changed after the 2026-08-22 anchor.

Before first access:
```
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
(no output — clean)
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine rev-parse HEAD
5359a11fc753cdcd2606aea991dae826293d0307
```

After last access:
```
$ git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain
(no output — clean)
```

No modification was made to the audited repository.
