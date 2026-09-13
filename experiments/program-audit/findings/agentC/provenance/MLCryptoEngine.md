# MLCryptoEngine — PROVENANCE (Agent C, referee/verifier)

**Repository:** MLCryptoEngine
**Anchored SHA:** `5359a11fc753cdcd2606aea991dae826293d0307` (main, 2026-08-22)
**Live HEAD at read time:** `5359a11fc753cdcd2606aea991dae826293d0307` — identical to the anchor
**Snapshot read:** `/home/kiros-li/.cache/program-audit/scratchpad/snap/MLCryptoEngine/`
**Live read window (UTC):** 2026-09-12T22:32:10Z .. 2026-09-12T22:46:50Z
**Agent:** C — no thesis. Verified claims are reported as verified; unverifiable is reported as unverifiable.

## Headline

**Sixteen provenance claims from the inventory, plus six further registrations located during this pass: 31 SUPPORTED, 3 PARTIAL, 0 NOT_SUPPORTED, 0 UNVERIFIABLE.**
All 22 named commits resolve, all are ancestors of the anchored HEAD, and every registration commit
precedes its result commit. **No registered bar, threshold, horizon, universe rule, sample floor,
multiplicity level or cost figure in any of the twelve registration blocks was ever edited** — checked
by `git log -L` over each block's exact anchored line range, which returns exactly one commit (the
registration) in every case. Twelve parameter changes after data existed were located; **all twelve
carry a dated amendment** with reason, effect and — where an outcome moved (GMX) — the outcome change
itself. Three findings are raised, none of which touches the pre-registration record: two concern the
completeness of the adversarial audit's own follow-through, one a doubled provenance for the fee figure.

This repository's pre-registration discipline is the strongest of any I have verified, and the
corroborating evidence is not only documentary: vendor-archive retrieval timestamps, a recorder
session ledger and the raw capture's own instrument set all independently confirm that the bars
predate the data.

---

## 1. Registration claims table

| # | claim (abbrev.) | file:line | commit named | found | commit date (UTC) | data first existed | status |
|---|---|---|---|---|---|---|---|
| 1 | C.17 bars + binding end condition "before any data" | HYPOTHESES.md:5-6 | `370ba41` | yes | 2026-08-06T14:02:46Z | new archives 14:06:28.6Z (+3m42s); run logged 18:23:31.6Z | **SUPPORTED** |
| 2 | C.16 momentum bars "before any result" | HYPOTHESES.md:150 | `88b69d8` | yes | 2026-08-06T05:09:05Z | run logged 2026-08-06T13:04:51.6Z (+7h56m) | **SUPPORTED** |
| 3 | H6 thin-perp census bars, before the window closes | HYPOTHESES.md:201 | `6025f5c` | yes | 2026-08-06T19:18:06Z | window closed 2026-08-11T00:00Z; result deb041b 08-11T06:56Z | **SUPPORTED** |
| 4 | "ten thin instruments were not read … a raise, not a comment" | report.md:2868-2870 | `287fc10` | yes | 2026-08-06T19:28:34Z | census could not run before 2026-08-11T00:00Z | **SUPPORTED** |
| 5 | D.1b blind universe rule + seed, registered before retrieval | DECISIONS.md:2382-2386 | `4bde24c` | yes | 2026-08-12T04:43:22Z | subscription restart 2026-08-12T04:50:36.894Z (+7m14s) | **SUPPORTED** |
| 6 | C.19 rug-audit bars "before any probe" (≥5,000 tokens) | report.md:2940 | `35e3466` | yes | 2026-08-06T19:47:47Z | first probe of *every* source ≥ 19:52:57.9Z (+5m10s) | **SUPPORTED** |
| 7 | Detection baselines + first-model bar "before any model" | report.md:3130 | `902d2e6` | yes | 2026-08-07T02:05:22Z | first model file mtime 2026-08-07T10:02:24.9Z (+8h) | **SUPPORTED** |
| 8 | C.14 thresholds registered; rho sign-gate corrected | report.md:2261, 2316 | `a2d7466`, `5430eba` | yes | 06:47:14Z / 07:17:26Z | C.14 runs logged 10:26:59.8Z, 10:41:51.9Z | **SUPPORTED** |
| 9 | Adversarial audit against commit `ed786ce`, 13 findings | report.md:5017-5020 | `fb296cb`, `ed786ce` | yes | 2026-08-13T03:31:44Z / 2026-08-12T06:16:42Z | audit postdates the result by 21 h | **SUPPORTED** |
| 10 | "all findings have been actioned" | AUDIT.md:18 | none | n/a | — | — | **PARTIAL** → DRAFT-P-1 |
| 11 | "every bar predates its result and no threshold was ever edited" | AUDIT.md:586-588 | none | n/a | whole history (91 commits) | — | **SUPPORTED** |
| 12 | "Machinery known-answer tested: reproduces C.9's −3.05 / −2.75" | HYPOTHESES.md:201 | `287fc10` | yes | 2026-08-06T19:28:34Z | C.9 targets published c74257e 2026-08-04T05:50Z | **PARTIAL** → DRAFT-P-2 |
| 13 | Hyperliquid maker fee "recorded here 2026-08-12 from the … published fee schedule" | fees.py:12-14 | none | n/a | figure in venues.yaml since 2026-08-01 | — | **PARTIAL** → DRAFT-P-3 |
| 14 | kraken/coinbase retired; 12-day three-venue overlap | HYPOTHESES.md:503-506 | none (ADR-060) | n/a | — | partitions read 2026-09-12T22:43Z | **SUPPORTED** |
| 15 | Scoring window opened at session marker `1786510236894021684` | report.md:4657-4660 | `4bde24c` | yes | — | marker present in sessions.jsonl | **SUPPORTED** |
| 16 | H1 note: every figure traces to a commit, all in `main` | docs/notes/h1-…md:295-311 | 12 commits | all 12 | 2026-08-01 .. 2026-08-12 | n/a | **SUPPORTED** |
| 17 | C.24 bars | report.md:3470-3545 | `c1b469e` | yes | 2026-08-07T09:45Z | result 9294da1 +1h12m | **SUPPORTED** |
| 18 | C.25 thresholds | report.md:3683-3734 | `5504352` | yes | 2026-08-07T21:04Z | result 41e6275 +1h05m | **SUPPORTED** |
| 19 | C.26 affordability threshold | report.md:3851-3893 | `0c62d80` | yes | 2026-08-07T22:28Z | result 2403a8e +46m | **SUPPORTED** |
| 20 | D.1a GO bar | report.md:4108-4148 | `513d2c1` | yes | 2026-08-11T07:35Z | result 8b6fbc7 +22m | **SUPPORTED** |
| 21 | D.1c kill conditions, quoting policy, horizon bars | report.md:4262-4343 | `4b8bc1f` | yes | 2026-08-12T02:32Z | result 8ce2838 +23m | **SUPPORTED** |
| 22 | D.1d bounded-replay policy, fill rules, kill conditions | report.md:4715-4795 | `6a17edf` | yes | 2026-08-12T05:46Z | result ed786ce +30m | **SUPPORTED** |

Rows 17-22 are registrations that the inventory did not list as claims; they were checked because
AUDIT.md:586-588 makes a whole-history statement that must hold for every registration in the repo.

### What the strongest rows rest on

**Row 1 (C.17).** `git show 370ba41 --stat` is `progress.md | 82 +++` and nothing else. At that commit
`report.md` contains no mention of C.17 at all and `progress.md` contains only the registration heading
and the sentence *"Nothing in C.17 has been probed, fetched, or computed at the time of writing."* The
entire C.17 implementation (`research/medium/*`, `tests/test_medium.py`, 1,584 lines) enters four and a
half hours later at `4f1b030`. Independently, `data/vendor/archive/manifest.jsonl` records the two new
C.17 sources first retrieved at **2026-08-06T14:06:28.584Z** (Coin Metrics) and **14:06:29.776Z**
(DefiLlama) — **3 minutes 42 seconds after the registration commit**. The run itself is logged at
18:23:31.6Z carrying `git_sha 370ba414`, i.e. it executed with the tree at the registration commit.

**Row 6 (C.19).** Seven independent third-party sources, each with a machine-written `retrieved_at`:
`solrpds_github` 19:52:57.868Z, `rugcheck_api/v1/stats` 19:53:06.039Z, `rugcheck_api` token reports
19:53:08.199Z, `dexscreener_api` 19:53:15.212Z, `goplus_api` 19:53:16.889Z, `arxiv_abstracts`
19:53:17.980Z, `helius_api` 2026-08-07T03:06:47.947Z. The bars were committed at **19:47:47Z**. Every
one of the seven is after it, the earliest by five minutes, and none before. `helius_credit_ledger.jsonl`
row 1 (`ts 2026-08-07T03:04:53.631Z`, `"probe DezXAZ8z"`) is a second, independent clock agreeing.

**Row 5 / row 15 (D.1b).** `git diff 4bde24c HEAD -- research/microstructure/blind_universe.py` is
**empty**: the rule and `SEED = 20260812` are byte-identical from registration to anchor. The recorder's
own ledger carries the restart at `ts_ns 1786510236894021684` = **2026-08-12T04:50:36.894022Z**, 7m14s
after the registration commit. Decompressing the first full post-restart hour of the raw capture
(`data/raw/venue=hyperliquid/date=2026-08-12/hour=05/messages.ndjson.zst`) yields exactly **27 distinct
instruments** — `0G ANIME BERA BIGTIME BTC COMP CRV DOGE DYM ETH HYPE ICP KAITO KAS LAYER LDO LIT MERL
MOODENG NEAR NOT PENDLE PUMP SAGA TRUMP VIRTUAL ZEC` — matching report.md:4646-4652's band table cell
for cell (25 blind picks + PUMP + MERL carried over). The hour before the restart carries the twelve
old names `ARB BTC DOT ETH GMX HYPE LINK MERL NOT PUMP SOL TNSR` — exactly `THIN_COINS` + BTC/ETH — and
SOL, DOT, LINK, ARB, GMX, TNSR are absent afterwards, precisely as the report states.

**Row 11 (the whole-history claim).** See §2's last row. Twelve `git log -L` runs, one commit each.

---

## 2. Parameter changes after data existed

Every change below post-dates the data it could have touched. **All twelve carry a dated amendment.**

| # | what changed | file | commit | date | direction | amendment | status |
|---|---|---|---|---|---|---|---|
| 1 | `ROUND_TRIP_BPS = 3.0` → `HYPERLIQUID_MAKER_ROUND_TRIP_BPS` (A10) | registered.py:58-59 | `d2a0f05` | 2026-08-12 | **value unchanged (3.0)** | progress.md:2742-2746; report.md §8; fees.py | SUPPORTED |
| 2 | CI critical value two-sided 1.96 → one-sided 1.645 (A6) | registered.py:180-186 | `d2a0f05` | 2026-08-12 | **loosens ~19%** | progress.md:2737-2741; report.md:5155-5161; AUDIT.md:264-281 | SUPPORTED |
| 3 | Day-clustered SE added; **GMX survivor → unresolved** (A3) | registered.py:146-164 | `d2a0f05` | 2026-08-12 | tightens 2-28× | progress.md:2737-2741; report.md:5137-5153; HYPOTHESES.md:196 | SUPPORTED |
| 4 | Capacity denominator 7 days → recorded span; true median (A8) | registered.py:212, 249-259 | `d2a0f05` | 2026-08-12 | loosens ~3.5% | progress.md:2737-2741; report.md:5163-5170 | SUPPORTED |
| 5 | Queue model `touch` → `own_level`; **PUMP −4.7503→−4.8087, MERL −4.2314→−4.3459** (A4) | fill_replay.py | `d2a0f05` | 2026-08-12 | strengthens closure | progress.md:2709-2719; report.md:5037-5063 | SUPPORTED |
| 6 | ALO-rejection suppression scope (A5) | fill_replay.py | `d2a0f05` | 2026-08-12 | no numeric effect (measured) | report.md:5065-5081 | SUPPORTED |
| 7 | D.1d known-answer gate withdrawn, replaced by differential test (A1) | d1d.py, reference_replay.py, test_fill_replay_gate.py | `d2a0f05` | 2026-08-12 | withdrawal of a warrant | **ADR-063** (2026-08-12); report.md:5083-5101 | SUPPORTED |
| 8 | **H6 reopening condition rewritten**; fill-instant attribution withdrawn (A13) | HYPOTHESES.md:194-195 | `d2a0f05` | 2026-08-12 | reopening rule changed | **ADR-064** (2026-08-12); report.md:5103-5113 | SUPPORTED |
| 9 | Counterfactual −3.98 / −2.57 → **−4.35 / −2.13** (A2) | report.md:4925 | `d2a0f05` | 2026-08-12 | conclusion unchanged | report.md:4925 (inline, dated) | SUPPORTED |
| 10 | Kraken base tier 25/40 → 40/80, then 40/80 → **25/40** | config/venues.yaml | `2299c7f`, `81e456e` | 2026-08-01, 2026-08-08 | **cost down after results existed** | **ADR-012** (2026-08-01), **ADR-055** (2026-08-08) | SUPPORTED |
| 11 | Label horizons extended to 60/300/**900 s**; `MAX_LABEL_HORIZON_NS` derived | fixed_horizon.py, pipeline.py | `03c99f9` | 2026-08-02 | **horizon extended after a result** | **ADR-015** (2026-08-01); progress.md Stage C.2 (2026-08-02) | SUPPORTED |
| 12 | CME fee 4.5 bps → $2.02/contract/side | config/venues.yaml | `16b3fa4` | 2026-08-03 | units correction | ships with the C.8 write-up | SUPPORTED |
| — | **Twelve registration blocks: no change of any kind** | progress.md, report.md | — | — | — | — | **SUPPORTED** |

### Notes on the three that deserve scrutiny

**#2 (A6) is the only post-data change that loosens a bar.** The registered text (progress.md:2085-2092)
says only *"95% confidence interval lower bound above zero at the worst of the three horizons"* and does
not say one- or two-sided; C.27 was scored with the two-sided 1.96 and the correction moves to 1.645.
The amendment states the direction against itself — *"making the bar ~19% harder than registered"* — keeps
`ci95_lower_bps_as_scored` so the published figure stays regenerable, and asserts no instrument's
category moves. Whether that assertion holds numerically is a verification-task question; the
amendment discipline is what is verified here, and it is complete.

**#10 is the only cost figure ever revised downward after results existed** (Kraken 40 → 25 bps maker on
2026-08-08, after C.16 and C.17 had closed using the 40 bps figure). ADR-055 records the new source, the
retrieval date, the diagnosis (*"the 0.40 / 0.80 recorded earlier captured the non-Pro retail/instant
fees"*), the magnitude and the effect on each affected closure. The discretion this would otherwise
create had already been removed in advance: C.17's registration (progress.md:2020-2028) registered
**both** a 40 bps and a 25 bps spot column before any C.17 data existed.

**#11 is the one horizon extension after a result existed** — and the 900 s horizon it added is the one
H1's headline (−76.69 bps net EV) is stated at. Two Phase B runs were already in the ledger
(2026-08-01T17:45:30Z and 2026-08-02T01:05:18Z) when `03c99f9` extended the set. It predates every
pre-registration in the repository (HYPOTHESES.md itself arrives two days later at `fd18ba2`), so it is
an exploratory-phase change rather than an edit to a registered bar, and ADR-015 plus the dated
progress.md entry warn against exactly the reading the change could invite: *"The uptick at 900 s rests
on one day … it must not be read as edge returning at longer horizons."*

### How the "no threshold was ever edited" claim was tested

`git log -p` over `research/`, `config/` and `engine/` across all 91 commits, filtered to lines that
add or remove an `UPPER_SNAKE` constant, returns **exactly two commits that ever changed one**:
`03c99f9` (row 11) and `d2a0f05` (rows 1-6). Every other constant in the repository was written once.
Separately, for each of the twelve registration blocks the anchored line range was located and
`git log -L <a>,<b>:<file>` run over it:

```
C.14   a2d7466  progress.md:1579-1680   → 1 commit
C.16   88b69d8  progress.md:1819-1877   → 1 commit
C.17   370ba41  progress.md:1948-2028   → 1 commit
C.18   6025f5c  progress.md:2071-2132   → 1 commit
C.19   35e3466  progress.md:2152-2194   → 1 commit
C.20   902d2e6  progress.md:2233-2259   → 1 commit
C.24   c1b469e  report.md:3470-3545     → 1 commit
C.25   5504352  report.md:3683-3734     → 1 commit
C.26   0c62d80  report.md:3851-3893     → 1 commit
D.1a   513d2c1  report.md:4108-4148     → 1 commit
D.1c   4b8bc1f  report.md:4262-4343     → 1 commit
D.1d   6a17edf  report.md:4715-4795     → 1 commit
```

In each case the single commit is the registration itself. All twelve are pure insertions (`+N/-0`) and
0 of their 738 added lines is missing verbatim from the anchor. **AUDIT.md:586-588's claim holds, and
holds more broadly than the audit claimed it** — the audit scoped its verdict to the H6 chain
(AUDIT.md:642-647); this check covers every registration in the repository.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** AUDIT.md's post-audit status banner; the H6 closure chain's remediation record
- **Direction:** B — it presents the remediation of the census/D.1c/D.1d chain as complete when two findings, one of which biases a census *net* upward, were not acted on
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Status, 2026-08-12: all findings have been actioned.** This file is the frozen audit record as delivered against commit `ed786ce`; it is not updated as fixes land." — MLCryptoEngine/AUDIT.md:18-20
- **Evidence:**
  - 11 of the 13 findings have a verifiable action in the anchored tree: A1 → `tests/test_fill_replay_gate.py` (present, with the coverage assertion at :179-184, *"gate does not execute: {unexecuted} — this is finding A1 again"*) and `research/microstructure/reference_replay.py` (present); A2 → MLCryptoEngine/report.md:4925; A3 → `registered.py:146-164`; A4 → `fill_replay.py` (`own_level`); A5 → `fill_replay.py`; A6 → `registered.py:180-186`; A8 → `registered.py:212, 249-259`; A10 → `research/microstructure/fees.py`; A11 → report.md §D.1d.5; A12 → `d1d.py:275-280` (`raise ValueError`); A13 → DECISIONS.md ADR-064.
  - **A7 and A9 have no action anywhere.** `grep -oE '\bA7\b|\bA9\b'` over `report.md`, `progress.md`, `DECISIONS.md`, `HYPOTHESES.md`, `research/` and `tests/` returns **0 hits for each**, while every other finding id returns 2-13 hits (A1 docs=7/code=5, A3 5/2, A4 2/5, A10 4/5, A13 8/0, …). The dated amendment at progress.md:2704-2748 enumerates A4, A5, A1, A13, A2, A3/A6/A8, A10/A11/A12 — eleven ids, not thirteen — and report.md:5015-5188 (§Stage D.1d corrections) covers the same eleven.
  - **A9's defect is still live at the anchor.** AUDIT.md:325-349 states that `_ReplayFeed.run_day` skips out-of-window records so trades armed within one horizon of the close never resolve, and that `d1c.py` handles the same case correctly. At the anchor, `research/microstructure/registered.py` has no resolution tail — grep for `TAIL|drain|flush` over the file finds nothing, `_queues` is drained only inside `on_quote` (registered.py:105-120), and `_ReplayFeed.run_day` still `continue`s on out-of-window records (registered.py:353-355) — whereas `research/microstructure/d1c.py:18-20,73` carries `RESOLUTION_TAIL_NS = 900_000 * 1_000_000` for exactly that case.
  - A9's second instance is also unfixed: a deadline falling inside a quote gap resolves against `self._last_mid` from before the gap (`registered.py:113-116`), which AUDIT.md:345-349 says biases `adverse` toward zero and **`net` upward** — the direction that flatters the census positives.
- **Recomputation (if any):** none — this is a presence/absence check over the anchored tree plus `git diff 287fc10 HEAD -- research/microstructure/registered.py` (154 lines; no tail-drain hunk).
- **What would resolve it:** either a dated entry recording A7 and A9 as considered-and-no-action-needed with the reason (the audit's own materiality assessments — A7 "matches disclosure", A9 "~0.01% of trades" — would suffice), or narrowing the banner to "all findings that require a change have been actioned".
- **Confidence:** HIGH — the absence is a mechanical grep over the anchored tree and the A9 code defect is directly readable at `registered.py:105-120, 353-355`.
- **Invalidated by later commits?:** no — the anchor is the repository's second-to-last commit and a gitignored operator marker `_CLOSED_DO_NOT_RUN_HERE` dated 2026-09-02 indicates the project is closed.
- **Disclosed by authors?:** partly — AUDIT.md:282-298 (A7) and AUDIT.md:325-349 (A9) disclose both findings in full, including their materiality, so a reader of AUDIT.md sees them. What is not disclosed is that they were not actioned; the banner asserts the opposite. The severity is held at S3 for that reason.

### DRAFT-P-2
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** H6 / Stage C.27 registered thin-perp census; the known-answer gate offered as its machinery warrant
- **Direction:** B — the C.27 census positives (PUMP +4.30, MERL +6.45 bps) rest on a validation warrant the code does not provide
- **Class:** PROVENANCE
- **Severity:** S2
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "The real known-answer gates are `registered.known_answer` (reproduces C.9's BTC/ETH nets — genuine and useful, and it does exercise the same accumulators the scored run uses) and D.1d's generous-mode gate (A1 — covers nothing that matters)." — MLCryptoEngine/AUDIT.md:568-571. Restated as "Machinery validated on BTC and ETH only — C.9's own window (2026-08-01 → 08-03), C.9's own measure, **through the same reader and accumulators**" — MLCryptoEngine/report.md:2901-2902, and as the registered machinery rule "The census pipeline is validated exclusively on BTC and ETH … A pipeline that cannot reproduce the closed answer does not get to produce the open one." — MLCryptoEngine/progress.md:2126-2130.
- **Evidence:**
  - `known_answer()` — MLCryptoEngine/research/microstructure/registered.py:394-403 — calls `run_census(raw_dir, date, coins=set(LIQUID_COINS), result=result)`.
  - `run_census` — MLCryptoEngine/research/microstructure/census.py:79-101 — builds `InstrumentCensus(spread=SpreadCensus(symbol=symbol), adverse=AdverseSelection(symbol=symbol, horizons_ms=horizons_ms))` (census.py:33-45), i.e. the accumulators in `spread.py` and `adverse.py`.
  - The scored C.27 run — `run_registered_census`, MLCryptoEngine/research/microstructure/registered.py:381-390 — instead constructs `RegisteredInstrument(symbol=coin)` (registered.py:87-145) and drives it through `_ReplayFeed` (registered.py:346-379). `RegisteredInstrument.on_quote` computes `spread = (ask - bid) / mid * 1e4` inline (registered.py:107-108) and `_resolve` computes adverse inline (registered.py:122-124); it is an independent implementation.
  - MLCryptoEngine/research/microstructure/registered.py:44-46 imports `iter_day_records`, `AGGRESSOR_SIGN, CensusResult, _quote, run_census` and `HYPERLIQUID_MAKER_ROUND_TRIP_BPS` — **neither `SpreadCensus` nor `AdverseSelection`**. `grep -n 'SpreadCensus|AdverseSelection'` over the file returns two hits only, both prose: a docstring at :19 and a comment at :110 ("Resolve deadlines with AdverseSelection's **exact semantics**"), i.e. the code itself describes a re-implementation of the semantics, not a reuse of the accumulator.
  - The two paths share `iter_day_records` (so "the same **reader**" is correct), `_quote` and `AGGRESSOR_SIGN`, and nothing else.
  - The audit's own coverage table two pages earlier is consistent with this and not with its verdict: MLCryptoEngine/AUDIT.md:561 records "`spread.py`, `adverse.py` | **no test file imports them**" and AUDIT.md:564-566 "reached only transitively through `run_census`" — which is precisely the path `known_answer` takes and the scored census does not.
  - `tests/test_registered_census.py` does exercise `RegisteredInstrument` with **synthetic** inputs (adverse canary at :130, prefix invariance at :160, sample floor at :203, outcome map at :217), but its only real-data call is `run_census(tmp_path, "2026-08-04", coins={"BTC","ETH"})` at :100 — again the other path. No test reproduces a closed answer through `RegisteredInstrument`.
- **Recomputation (if any):** none — a static call-graph and import check over the anchored snapshot.
- **What would resolve it:** either a known-answer run of C.9's window through `run_registered_census`/`RegisteredInstrument` restricted to BTC/ETH, reported against C.9's published −3.05 / −2.75; or a correction of AUDIT.md:568-571 and report.md:2901-2902 to say the gate validates `census.run_census` and that the registered census is a separate implementation covered only by synthetic tests.
- **Confidence:** HIGH — the two code paths are disjoint by import, and the claim is a specific assertion about which accumulators execute.
- **Invalidated by later commits?:** no — `registered.py`'s last touch is `d2a0f05` (2026-08-12), before the anchor, and the project is closed.
- **Disclosed by authors?:** no for the claim challenged. The report does disclose that the *measure* differs (report.md:2917-2921: "the registered spread measure credits the fill with the spread standing at the trade, where C.9's time-weighted mean blends in quiet periods"), which makes the situation more pointed rather than less: a gate running a different measure through a different implementation cannot satisfy the registered rule that a pipeline must reproduce the closed answer to be allowed to produce the open one. The code comment at registered.py:110 is the only place that hints the accumulator is a re-implementation.

### DRAFT-P-3
- **Repository / SHA:** MLCryptoEngine / `5359a11fc753cdcd2606aea991dae826293d0307`
- **Hypothesis or artifact:** the Hyperliquid base-tier maker fee — the single input every C.27, D.1c and D.1d net scales with
- **Direction:** neutral — no figure in the repository moves; the defect is in the provenance record attached to the figure
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED
- **Claim challenged (verbatim quote):** "**Source.** Hyperliquid perpetuals, base tier (< $5M 14-day volume, no staking discount): **0.015% maker / 0.045% taker** -- 1.5 bps / 4.5 bps. Recorded here 2026-08-12 from the Hyperliquid published fee schedule." — MLCryptoEngine/research/microstructure/fees.py:12-14, in a module that opens "The one place the Hyperliquid fee schedule is stated (audit finding A10)." — MLCryptoEngine/research/microstructure/fees.py:1 and states "Before this module the maker fee lived as three unsourced, undated literals … while `config/venues.yaml` carried fully sourced, dated ladders for **Kraken and Coinbase**." — MLCryptoEngine/research/microstructure/fees.py:3-6
- **Evidence:**
  - MLCryptoEngine/config/venues.yaml:182-190 carries a **fourth** statement of the same figure, sourced and dated differently: "`# Perp schedule verified 2026-08-01 (hiperwire.io/explainers/hyperliquid-trading-fees-explained, supa.is/article/hyperliquid-trading-fees-2026): base tier 0.015% maker / 0.045% taker`" with "`- { volume_usd_30d: 0, maker_bps: 1.5, taker_bps: 4.5 }`" — two third-party explainer sites, dated 2026-08-01, not the venue and not 2026-08-12.
  - `git log -S "maker_bps: 1.5" -- config/venues.yaml` returns exactly one commit, `70842ae` (2026-08-01 11:31 -0700), and `git log -S "hiperwire" -- config/venues.yaml` the same, so that statement has been in the repository since 2026-08-01 and has never been edited.
  - The venues.yaml statement is the one the registrations cite, not fees.py: MLCryptoEngine/progress.md:2021 "Hyperliquid legs 1.5 bps/side (venues.yaml, verified 2026-08-01)" (C.17 registration, commit `370ba41`); MLCryptoEngine/progress.md:2089-2090 "3.0 bps round trip (Hyperliquid base-tier maker, `config/venues.yaml`, verified 2026-08-01)" (C.18/H6 registration, commit `6025f5c`); MLCryptoEngine/report.md:1114 the same for C.9.
  - Both files remain present and un-reconciled at the anchor, so the repository states two different origins and two different dates for one number.
- **Recomputation (if any):** none — the numeric value is identical (1.5 bps maker; `HYPERLIQUID_MAKER_ROUND_TRIP_BPS = 2.0 * 1.5 = 3.0`, fees.py:37-43) and no published figure changes.
- **What would resolve it:** a line in `fees.py` reconciling the two — either "the 2026-08-01 venues.yaml entry, sourced to explainers, is superseded by this venue-sourced 2026-08-12 reading" or a note that venues.yaml's entry is the registered citation and fees.py merely re-verified it — and a cross-reference in `venues.yaml:182-190` pointing at `fees.py`.
- **Confidence:** HIGH for the inconsistency (both texts are anchored and quoted); MEDIUM for its importance, since the value is identical and the repository's exposure is documentary, not numeric.
- **Invalidated by later commits?:** no — both files are at their final state at the anchor.
- **Disclosed by authors?:** partly. `fees.py:12-20` is unusually candid that the figure is *documented, not measured* and "the weakest input in the chain", and ADR-055 establishes the project's own rule that fee schedules are dated measurements to be re-verified. What is not disclosed is that a differently-sourced, differently-dated statement of the same figure remains in `venues.yaml` and is the one the registrations cite; fees.py:3-6 in fact implies venues.yaml had no Hyperliquid entry.

---

## 4. What could not be checked, and why

1. **The D.1b seeded draw is not reproducible.** The rule and seed are anchored and byte-identical since
   registration, and the resulting 27-instrument subscription is confirmed in the raw capture — but the
   retrieved `metaAndAssetCtxs` ranking payload the rule was applied to **is not stored anywhere**. Searched
   `logs/` and `data/processed/` (live, 2026-09-12T22:37Z); the only stored universe artifact is
   `data/processed/pairs/universe_2021-08_2026-07.json`, which is C.10's. report.md:4646 records band member
   *counts* (B0 4 / B1 7 / B2 36 / B3 107 / B4 23 of 177) but not the member *names*, so the seeded sample
   cannot be redrawn. What is verified is the rule, the seed, the timing, and the 27 names that actually
   came out; what cannot be verified is that those 25 are what the seed would have produced from that
   ranking. **UNVERIFIABLE by construction**, recorded as such rather than guessed at.
2. **Whether the A6 correction really moves no instrument's category** is a numeric question requiring the
   per-instrument census rows; it belongs to the verification task, not here. This report verifies only
   that the change is dated, reasoned and disclosed.
3. **The 2026-09-09 blind-window readout** postdates the 2026-08-22 anchor entirely and recording in fact
   stopped 2026-08-13 (`aeabff6`). No anchored evidence can settle it, and the report itself says the window
   "still reads out … as a selection-bias check".
4. **Three of the nine rows** in the H1 note's provenance table were not individually spot-checked (the
   deep-LOB citation row, the H1 reopening-condition row, and the "Unaudited, not clean" row); six were, all
   clean, and all twelve named commits resolve in `main`.
5. **Whether the author saw C.11 funding/basis data before choosing C.17's bars** is unfalsifiable from git.
   The registration states plainly that classes C and D come "from the C.11 archive on disk", so the reader
   is told; the two *new* archives and every C.17 computation postdate the bars.
6. **UNANCHORED reads.** `data/vendor/archive/manifest.jsonl`, `helius_credit_ledger.jsonl`, `data/raw/venue=*`
   partitions and `sessions.jsonl`, and `data/processed/detection/*` mtimes are working-tree artifacts, not
   tracked at the anchor. All were read read-only at the times stated and may in principle have changed after
   the 2026-08-22 anchor; each carries its read time above.

### Two observations recorded but not raised as findings

- **The outcome-to-action map registers four outcomes but no precedence for a mixed one.** C.27 landed mixed
  (PUMP/MERL/GMX survivors *and* NOT/TNSR `positive_but_rare`), and `registered.py:313-319` resolves it in the
  direction that continued the project ("input to a D.1 fill-simulation decision") rather than the direction
  that stopped it ("report the fill-frequency arithmetic and stop"). This is **not** a post-hoc choice: the
  precedence was fixed at `287fc10` on 2026-08-06, five days before the window closed and the thin instruments
  were read, and `git diff 287fc10 HEAD` shows `assemble()`'s precedence block unchanged since. Recorded
  because the registration's own text does not contain it.
- **The H6 register's D.1d row still leads with the superseded figures** ("PUMP −4.75 bps, MERL −4.23 bps",
  HYPOTHESES.md:194) while the Status row immediately above gives the corrected −4.81 / −4.35 and says
  "(was −4.75 / −4.23)". Disclosed in the same table, so not a finding here; noted for the verification pass.

## 5. Where this repository is sound

Reported plainly, because a sound result is a result. Checked and found clean:

- Every one of 22 named commit hashes resolves, and every one is an ancestor of the anchored HEAD.
- Every registration commit precedes its result commit; where a run ledger exists, the run's `logged_at`
  falls between the two.
- Every registration commit is a pure insertion (`+N/-0`), and the six documentation-only ones touch nothing
  but `progress.md` or `report.md`.
- No registration commit's tree contains the result it registers (checked directly for C.14, C.16, C.17,
  C.18, C.19, C.20).
- No line of any registration block was ever edited (twelve `git log -L` runs, one commit each).
- Only two commits in 91 ever changed a named constant anywhere in `research/`, `config/` or `engine/`, and
  both are documented with a dated ADR.
- Every parameter change after data existed carries a dated amendment naming the reason, the effect on the
  numbers, and — for GMX — the outcome that moved.
- The single external audit was demonstrably run against the tree it names: five of its line references
  resolve character-for-character in `ed786ce`.
- The audit record has been edited once since delivery, and only to add a dated status banner and fix a code
  fence; no finding text was altered.

If the thesis were that this program closed early or claimed too much on the strength of a
pre-registration story, the place it would show is the registration record — and the registration record
verifies, on git objects, three independent data clocks, and the raw capture itself.

---

## 6. Live-repo access log

Every access below was read-only. No `checkout`, `stash`, `reset`, `clean`, `add`, `commit`, `branch`,
`merge`, `rebase`, `worktree` or `gc` was run against the audited repository; no file in it was opened for
writing; no repository script was executed in place; `.env` was not opened. Scratch scripts and outputs were
written only to `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-prov-MLCE/`.

| time (UTC) | action | result |
|---|---|---|
| 2026-09-12T22:32:10Z | `git -C <live> status --porcelain` (PRE-ACCESS); `rev-parse HEAD`; `rev-parse --abbrev-ref HEAD` | EMPTY. HEAD `5359a11f…0307`, branch `main` — identical to the anchor. |
| 2026-09-12T22:32Z | `git log -1 --format=… --date=iso-strict` on 22 commit ids; `git merge-base --is-ancestor <c> HEAD` on all 22; `git rev-list --count HEAD` | All 22 resolve, all ancestors of HEAD; 91 commits total. |
| 2026-09-12T22:32Z | `git log --format=… --reverse HEAD`; `git log --follow -- progress.md` | Full ordered history recorded above. |
| 2026-09-12T22:33Z | `git show <c> --stat` and `git show <c> -- <file>` for 370ba41, 88b69d8, 6025f5c, a2d7466, 5430eba, 4bde24c, 35e3466, 902d2e6, 287fc10, 17df5ad, 022a059, 4f1b030, d2a0f05, fb296cb, 2299c7f, 03c99f9, 16b3fa4, 513d2c1, 4b8bc1f, 6a17edf, c1b469e, 5504352, 0c62d80 | Registration contents and diffs recorded. |
| 2026-09-12T22:33Z | `git show <c>:<path>` for progress.md / report.md / registered.py / fill_replay.py / d1d.py / blind_universe.py at 370ba41, 88b69d8, 287fc10, ed786ce, 4bde24c, c74257e, ddf525d, fd18ba2, 81e456e | Tree contents at named commits verified; A1/A7/A8 line references confirmed at `ed786ce`. |
| 2026-09-12T22:33Z | `git log -L <a>,<b>:<file>` over twelve registration blocks; `git log -p` filtered for constant changes over `research config engine`; `git log -S` on `maker_bps: 1.5`, `Perp schedule verified`, `hiperwire`, `MAKER_FEE_BPS`, `3.05` | One commit per block; two constant-changing commits in 91; fee-figure history as recorded. |
| 2026-09-12T22:34Z | `git diff 287fc10 HEAD -- research/microstructure/registered.py`; `git diff 4bde24c HEAD -- research/microstructure/blind_universe.py` | 154 lines / 0 lines. |
| 2026-09-12T22:34Z | `ls -la --time-style=full-iso` on `data/vendor/archive/`, `data/vendor/archive/{coinmetrics,defillama}`, `data/processed/detection/`, `logs/` | mtimes recorded; no binary opened; `.env` not opened. |
| 2026-09-12T22:36Z | read `data/vendor/archive/manifest.jsonl` (14,191 rows) — `source`, `dataset`, `retrieved_at` fields only, aggregated; `head -1 data/vendor/helius_credit_ledger.jsonl`; `wc -l` on it | Per-source first/last retrieval windows recorded. `url` values were not printed or copied. File is mode 0600 but is a vendor download manifest, not a credential. |
| 2026-09-12T22:37Z | `ls data/raw/venue=*/`; `tail -5 data/raw/venue=hyperliquid/sessions.jsonl`; `grep -c 1786510236894021684 sessions.jsonl` | Partition ranges and the session marker recorded. |
| 2026-09-12T22:38Z | `zstd -dc data/raw/venue=hyperliquid/date=2026-08-{11,12}/hour=05/messages.ndjson.zst \| grep -o coin \| sort -u` (decompressed to stdout, three sample lines written to the agent work dir only) | 12 instruments before the restart, 27 after. Nothing written to the repository. |
| 2026-09-12T22:46:50Z | `git -C <live> status --porcelain` (POST-ACCESS); `rev-parse HEAD` | EMPTY. HEAD `5359a11f…0307`, unchanged. |

**Pre-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T22:32:10Z), verbatim:**

```
(no output — working tree clean; exit status 0)
```

**Post-access `git -C /home/kiros-li/Documents/GitHub/MLCryptoEngine status --porcelain` (2026-09-12T22:46:50Z), verbatim:**

```
(no output — working tree clean; exit status 0)
```

`git rev-parse HEAD` = `5359a11fc753cdcd2606aea991dae826293d0307`, identical before and after and identical
to the anchored SHA. No dirt was present and none was introduced. Nothing was written to, created in, or
deleted from the audited repository.
