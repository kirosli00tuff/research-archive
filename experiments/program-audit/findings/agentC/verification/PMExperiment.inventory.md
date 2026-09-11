# PMExperiment — verification inventory (LOCATE)

**Agent C (referee/verifier). No thesis. This document locates what can be verified; it
adjudicates nothing.** Where a check has already been run to establish *which artifact backs
which figure*, its result is stated plainly — a verified figure is recorded as verified.

| | |
|---|---|
| Repository | `PMExperiment` |
| Anchored SHA | `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project) |
| Snapshot read | `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/` |
| Live repo touched | `/home/kiros-li/Documents/GitHub/PMExperiment/` — git objects and `ls -la` of the working tree only, read-only |
| Compiled | 2026-09-05, 23:26Z–23:35Z |
| Documents read | `README.md`, `CLAUDE.md`, `REGISTRATION.md` (all 1,170 lines), `HYPOTHESES.md`, `DECISIONS.md`, `progress.md`, `report.md`, `docs/BAND.md`, `docs/ACCESS.md`, `docs/LICENCES.md` |
| Not present | There is no `FINDINGS.md`, no `registrations/` directory, no `reports/` directory, and **no `data/`, `audit/` or artifact directory containing a single stored figure**. Registration is the single `REGISTRATION.md`; `docs/BAND.md` is the only evidence document carrying computed numbers. |

Counts: **31 artifact entries** (29 tracked and anchored, plus the git object store and one
untracked working-tree marker),
**26 numeric claims** ranked with **8 marked MUST-VERIFY**, **0 confidence intervals and
0 p-values or test statistics reported anywhere** against **11 registered-but-never-fired
statistical entries**, **25 provenance claims**.

**The single fact that shapes this whole inventory.** This repository contains **no stored
data artifact of any kind, and never has**. `git log --all --diff-filter=A --name-only` over
the entire history returns **zero** files with a `.json`, `.csv`, `.parquet`, `.db`, `.ndjson`
or `.txt` extension; `data/` in the live tree holds only a zero-byte `.gitkeep`
(read 2026-09-05T23:28Z). Every number in this repository is therefore one of exactly three
kinds: **(a)** arithmetic over constants that are themselves in the registration and in
`pmexperiment/registry.py` — fully recomputable and fully anchored; **(b)** a figure a session
reported having measured over HTTP, with **no retained response** — unanchored and
irreproducible by construction, and the repository says so
(`docs/ACCESS.md:87-89`, "the raw probe responses were not retained beyond this report");
**(c)** a figure imported from an outside publication or another repository in this program.
The verifiable surface is therefore (a) plus the git objects, and it is unusually clean;
(b) is unverifiable and must never be guessed at.

---

## 1. Artifacts — every place a number could be verified

### 1.1 Analysis and measurement code (tracked, anchored at `03d16e7`)

| path | what it holds | which document figures it backs | anchored? |
|---|---|---|---|
| `pmexperiment/registry.py` (66 lines) | **Every registered constant, in one place.** `Z_CRITICAL 2.0`; `EFFECT_BAND_LO 0.02` / `EFFECT_BAND_HI 0.08`; the ten `BUCKET_EDGES_CENTS` and `TAIL_BUCKETS_CENTS ((1,10),(91,99))`; `SNAPSHOT_S24_HOURS 24` / `SNAPSHOT_S30_DAYS 30`; `UNRESTRICTED_SAMPLE_SIZE 2000`; `SAMPLE_SEED 20260829`; `WILSON_Z 1.96`; `ACCESS_MIN_SETTLED_MARKETS 1000`; `ACCESS_OUTCOME_PRESENCE_MAX_RECORDS 5`; `PERMITTED_MIN_MATURITY_DAYS 30`; `PERMITTED_MIN_VOLUME_USD 1000.0`; `FEE_PER_SIDE_USD 0.02`, `FEE_SIDES 2`, `HALF_SPREAD_USD 0.01`, `FX_PER_DIRECTION 0.015`, `FX_DIRECTIONS 2`; `FX_TURNOVER_REGISTERED 1.0` | **every figure in `docs/BAND.md`**, `REGISTRATION.md` Sections 0.2–0.4, 2, 3, 9, 11 and Amendments 2, 4, 5 | YES |
| `pmexperiment/band.py` (135 lines) | **The gate that produced the repository's one number.** `ExitRoute` (fee sides 1 vs 2); `fee_borne`; `fx_cost(p,k) = 0.03·p/k`; `required_underpricing = fee + 0.01 + fx`; `band_top_exceeds_requirement` (strict `<` against 0.08 — the *existential* reading); `band_bottom_exceeds_requirement` (the strict reading, reported and not used); `bucket_midpoint = (lo+hi)/200`; `surviving_buckets`; `is_band_empty`. BAND-NARROW and BAND-OPEN are deliberately **not** derived in code (`band.py:128-134`) | **the entire `docs/BAND.md` Pass-1 table**, the 5.85 / 8.00 verdict, the 0.0300 floor, the 2.15-point margin, the crossings | YES |
| `pmexperiment/power.py` (82 lines) | `minimum_detectable_effect = Z_CRITICAL·sqrt(v̄/n)`, `None` on an empty cell; `fire_power_gate` mapping MDE → GO / DEGRADED / BLOCKED, lower edge inclusive; `cost_floor(p) = 0.02·2 + 0.01 + 0.03·p` — Section 11's C(p) | Section 0.3's outcome map, Section 0.4's planning bars, Section 11's C(0.95)=0.0785 and C(0.05)=0.0515. **Never fired on real data** | YES |
| `pmexperiment/admissibility.py` (190 lines) | **ADR-012 as a procedure.** `MIN_DOCUMENT_TEXT_RATIO 0.05`; `REQUIRED_ELEMENTS ("clause","effective_date","fetch_date")`; `DocumentReading.text_ratio` / `looks_client_rendered` / `is_established`; `missing_elements` (`clause.split()` non-empty; `date.fromisoformat` on both dates); `admit`; `permits` (only PERMITTED permits) | every ADMISSIBLE / UNMEASURED verdict in `docs/LICENCES.md`, `REGISTRATION.md` 15.4, ADR-012/014/015/016; the 5 % text-ratio bar quoted in its own docstring from the Polymarket shell measurement | YES |
| `pmexperiment/__init__.py` (3 lines) | Docstring only; `__all__` empty | — | YES |

### 1.2 Tests — the pinning layer (tracked, anchored)

| path | test fns | what it pins | anchored? |
|---|---|---|---|
| `tests/test_honesty.py` (602 lines) | **59** | Named sentences in `README.md`, `CLAUDE.md`, `REGISTRATION.md`, `HYPOTHESES.md`, `DECISIONS.md`, `report.md`, `progress.md`, `docs/*`. Pins the figures `0.0512`, `0.01 to 0.05`, `415 days`, `49.35 bp`, `AUC 0.501`, `5.85 points`, `8.00 points`, `0.0785`, `0.0585`, `0.0300`, `0.0200`, `313,972`; pins that Section 13 stays empty, that the prior is never called pre-registered, that BAND-OPEN is never written as an edge | YES |
| `tests/test_band.py` (184 lines) | **14** | `required_underpricing(0.95, X, k=1) == 0.0785`, `(0.05, X) == 0.0515`, `(0.95, H) == 0.0585`; the two routes differ by exactly one `FEE_PER_SIDE_USD`; `fx_cost(0.95,1) == 0.0285` and `→0` at `k=inf`; FX-free held floor `== 0.03`; band bottom survives at **0/10** buckets on both routes at every k; band top survives at **10/10**; route-X margin `0.0015` vs slack `0.00195`; route-H margin `0.0215` vs slack `0.00135`, `margin > 10×slack` | YES |
| `tests/test_admissibility.py` (229 lines) | **14** | The three real permission claims reconstructed as fixtures; includes `test_stage_a_kalshi_claim_carries_no_effective_date_in_the_record` — the self-conviction | YES |
| `tests/test_registry.py` (99 lines) | **9** | **Each registered constant against a quoted string in `REGISTRATION.md`** — a mechanised code↔document provenance guard | YES |
| `tests/test_power.py` (85 lines) | **9** | MDE at n=100 `== 0.043589`; GO inclusive at n=475; DEGRADED at 474 and at 30; BLOCKED at 29 and at 0; `cost_floor(0.95)==0.0785`, `(0.05)==0.0515` | YES |
| `tests/test_guards.py` (166 lines) | **6** | AST scan of `power.py`, `band.py`, `admissibility.py` for outcome tokens; the scanner is itself fed a violation; every registered bar has a `registry.` enforcement site; each ADR-012 element blanked singly must collapse the claim | YES |
| `tests/__init__.py` | 0 | empty | YES |
| **suite total** | **111** | matches `progress.md:1648`'s closing "**111 pass**" **exactly** (counted by `grep -c '^def test_'` over `tests/*.py`) | — |

### 1.3 Binding documents (tracked, anchored) — where the claims live

| path | lines | what it holds | anchored? |
|---|---|---|---|
| `REGISTRATION.md` | 1,170 | Sections 0–17. §0 the two gates and the outcome map; §0.4 the planning bars; §2 and §11 the cost model; §3 the effect band and its three sources; §9 the power method; §13 the empty prior; §14 reproducibility; §15.1–15.5 the five fired verdicts; §16 closure conditions annotated at closure; §17 Amendments 1–9 | YES |
| `progress.md` | 1,651 | Entries 0–12 with sub-entries. ETA-vs-actual tables per task with commit hashes and Z-timestamps; the mutation-harness fault record; the closing git/credential audit | YES |
| `docs/LICENCES.md` | 846 | Stage D's three candidates; byte counts, text ratios, occurrence counts, dataset row counts; the Stage E addendum | YES |
| `DECISIONS.md` | 796 | ADR-001 … ADR-021, including the recorded duplicate ADR-006/ADR-007 numbering collision | YES |
| `report.md` | 487 | One never-revised section per stage: Scaffold, A, B, C, D, E | YES |
| `HYPOTHESES.md` | 358 | H1 / H1t / H2 / H3 register, five dated amendments, the carry-forward figure table at :138-145 | YES |
| `docs/BAND.md` | 341 | **The only evidence document with computed numbers.** Task 1 quoted inputs; Task 2 unit determination; Task 3 FX; Task 4 Pass 1 the 10×6 band table, crossings, margins; Pass 2 the Canadian filter; Task 5 the verdict | YES |
| `docs/ACCESS.md` | 333 | Kalshi (Stage A), Polymarket (Stage C), the Kalshi desk reply (Stage E): latencies, byte counts, request logs, verbatim clauses | YES |
| `README.md` | 233 | The cold-reader front door; the route ledger; the one number and what it is not | YES |
| `CLAUDE.md` | 78 | The sixteen standing rules later entries cite by number | YES |

### 1.4 Configuration and toolchain (tracked, anchored)

| path | what it holds | backs | anchored? |
|---|---|---|---|
| `pyproject.toml` (43) | deps `httpx`, `pydantic`, `pydantic-settings`; dev `pytest`, `ruff`, `mypy`, `pre-commit`; `mypy strict = true`, `warn_unreachable`; ruff `line-length 88`, `select E,F,I,N,UP,B,SIM,RUF` | the "lint, typecheck clean" claims; note **no numpy/scipy** — nothing statistical could have been computed with the declared dependency set | YES |
| `.env.example` (5 lines, **294 bytes, zero `=`**) | five comment lines, empty on purpose | `progress.md:1539-1541`'s audit line — **verified byte-for-byte** | YES |
| `.gitignore` (13) | `.env`, `.env.*` with `!.env.example`, `*.session`, `data/raw/`, `data/vendor/` | `progress.md:1542-1543` — verified | YES |
| `LICENSE` (21 physical lines, **17 non-blank**) | MIT, `Copyright (c) 2026 kirosli00tuff` | `progress.md:1541`'s "`LICENSE` is MIT, 17 lines" — matches the **non-blank** count, not the physical one | YES |
| `Makefile` (27) | `lint`, `typecheck`, `test`, and a `verify` target that only **echoes** the recorded access state and refuses to re-probe | the "make targets green" claims | YES |
| `.pre-commit-config.yaml` (14) | ruff-format, ruff --fix, check-added-large-files, **detect-private-key**, end-of-file-fixer, trailing-whitespace | the credential-hygiene claims | YES |
| `uv.lock` (717) | pinned toolchain | reproducibility | YES |
| `data/.gitkeep`, `scripts/.gitkeep`, `docs/.gitkeep` | zero bytes each | **the absence of every data artifact** | YES |

### 1.5 Stored result artifacts — **there are none, and there never were**

| what a reader might expect | state |
|---|---|
| `reports/*.json`, ledgers, manifests, parquet, CSV, sqlite | **none, at any commit.** `git log --all --diff-filter=A --name-only` over 36 commits adds no file with a data extension |
| `data/raw/` — the directory Section 14 names as the reproducibility record ("regenerable from the stored raw enumeration and candlestick responses under `data/raw/`", `REGISTRATION.md:359-363`) and Section 10 calls "gitignored, append-only" (`REGISTRATION.md:320-321`) | **does not exist** in the live tree. `data/` holds one zero-byte `.gitkeep`. Read 2026-09-05T23:28Z |
| an append-only fsynced ledger (standing rule 6, `CLAUDE.md:29-30`) | **no ledger file exists** anywhere in the repository or its history |
| the Kalshi probe responses (11 API reads), the Polymarket robots/ToS bodies, the Dune/HuggingFace bodies, the Kalshi Data Terms PDF, the correspondence | **none retained.** `docs/ACCESS.md:87-89` states the probe responses "were not retained beyond this report"; `docs/LICENCES.md` reports byte counts and occurrence counts from bodies that are not in the repository |
| **consequence** | **every access, latency, byte-count, occurrence-count and text-ratio figure in `docs/ACCESS.md` and `docs/LICENCES.md` is READ-only evidence and cannot be re-derived from anything this repository stores.** The band arithmetic is the opposite case and is fully DERIVED-verifiable. |

### 1.6 Git objects as the verification substrate (live, read-only)

The git history is the *only* non-document artifact in this repository, and it carries real
evidence. Read 2026-09-05T23:27Z–23:33Z.

| object | figure it can settle |
|---|---|
| 36 commits, 2026-08-29T07:09:55Z → 2026-09-02T09:50:29Z; **213 reachable objects at HEAD** | the closing audit's "**32 commits, 189 reachable objects**" — **verified exactly at `1ba50aa`**, which was HEAD when Stage E Task 5's audit ran (`git rev-list --count 1ba50aa` = 32; `git rev-list --objects 1ba50aa \| wc -l` = 189) |
| per-commit author/committer dates | every "Made <date>" amendment header and every Z-timestamp in `progress.md`'s ETA tables |
| `git log -- docs/BAND.md` → **one commit only** (`34307b6`, 2026-08-29T19:22:44Z) | Amendment 2's "the band is computed once and registered … **not** recomputed" — **verified: the band document has never been touched again** |
| `REGISTRATION.md` Sections 0–14 across all 13 commits that touched the file | **verified byte-identical from `9080186` (the Section-0 commit) to HEAD** — SHA-256 of the pre-§15 region is `a33f7768…` at every one of the 11 post-registration commits |
| `git ls-tree -r HEAD` → 32 files; branches `main` only; **no tags**; remote `github.com/kirosli00tuff/PMExperiment` | scope of the anchored tree |

### 1.7 Untracked / gitignored in the live working tree — **UNANCHORED**

Read by `ls -la` on 2026-09-05 at 23:28Z. Nothing here is repository evidence.

| path | size / date | what it is | anchored? |
|---|---|---|---|
| `_CLOSED_DO_NOT_RUN_HERE` | 747 B, 2026-09-02 22:38 local | Operator marker written **after** the anchor, excluded locally via `.git/info/exclude` (verified). Says the repository is closed and no session may run in it. Recorded so it is not mistaken for repository evidence | **NO** |
| `.venv/`, `.mypy_cache/`, `.pytest_cache/`, `.ruff_cache/` | dirs, 2026-08-29 | Toolchain caches, gitignored. Not opened | **NO** |
| `data/` | one 0-byte `.gitkeep`, 2026-08-29 00:07 | **empty** — the absence is itself the finding | n/a |

`git status --porcelain` on the live tree was **empty before and after** every access
(§5 below). No `.env`, no `*.session`, no credential-shaped file exists; none was opened.

---

## 2. Numeric claims, ranked — MUST-VERIFY marked

Ranked by how much rests on them. Ranks 1–8 are marked **MUST-VERIFY**; the brief requires at
least three, and the whole of this repository's positive output is one arithmetic chain that
needs eight checks to be walked end to end.

### ★ MUST-VERIFY 1 — the number the repository's only verdict rests on

> "**BAND-OPEN — a surviving region exists that the permitted subset admits, at entry prices
> 91–99c held to resolution, requiring 5.85 points of underpricing at the registered FX
> turnover against a registered band whose top is 8.00 points.**"
> — `REGISTRATION.md:409-412`; identically `README.md:139-141`, `docs/BAND.md:15-18`,
> `HYPOTHESES.md:130-133`, `report.md:61-68`, `docs/LICENCES.md:718`

Figures: **0.0585** required vs **0.0800** band top. **n = none** — this is arithmetic over
registered constants and no sample stands behind it, which the documents say repeatedly.
Produced by `pmexperiment/band.py:68-80` `required_underpricing(0.95, HELD_TO_RESOLUTION,
turnover=1.0)` over `registry.py:53-66`; pinned by `tests/test_band.py:56-59`.
**Independently recomputed: 0.02 + 0.01 + 0.03×0.95 = 0.0585 exactly.** This is the single
figure every closure document carries forward, and the one a reader is most likely to
mis-read as evidence of an edge — which the repository itself forbids in five places.

### ★ MUST-VERIFY 2 — the decisive figure, "for a reader who reads one number"

> "**fee and half-spread alone total 0.0300 on the held route before any FX at all, against a
> registered band bottom of 0.0200. No FX treatment, no venue price and no exit route reaches
> the bottom of the band.**"
> — `REGISTRATION.md:456-459`; `report.md:105-108`; `HYPOTHESES.md:140`;
> `docs/BAND.md:241-243`; `progress.md:449-451`

Figures: 0.02 + 0.01 = **0.0300** against `EFFECT_BAND_LO` **0.0200**. n = none.
Produced by `band.py:46-48` + `registry.HALF_SPREAD_USD`; pinned by
`tests/test_band.py:84-96` and `tests/test_band.py:99-107` (band bottom survives at
**0 of 10** buckets on both routes at k = 1, 12 and ∞). **Independently recomputed: holds.**

### ★ MUST-VERIFY 3 — "the cost floor runs entirely inside the effect band at every price"

> "**There are no crossings inside the tradeable price range.** … R_H(p) = 0.03 + 0.03p …
> p = **−0.3333** … p = **+1.6667** … R_X(p) = 0.05 + 0.03p … p = **−1.0000** … p =
> **+1.0000** — the curve meets the band top exactly at $1.00, a price that cannot be traded"
> — `docs/BAND.md:212-227`; the conclusion at `REGISTRATION.md:448-454` ("the arithmetic
> confirms it to **0.0015**"); `report.md:97-103`; `progress.md:442-447`

n = none. **Independently recomputed: (0.02−0.03)/0.03 = −0.3333, (0.08−0.03)/0.03 = 1.6667,
(0.02−0.05)/0.03 = −1.0000, (0.08−0.05)/0.03 = +1.0000 exactly, and 0.08 − 0.0785 = 0.0015.**
This is the claim Section 2 registered in advance as "the central economic fact this
repository exists to test", so it is the one place where a pre-registered prediction is
declared confirmed.

### ★ MUST-VERIFY 4 — the whole Pass-1 band table, 10 buckets × 6 columns

> the table at `docs/BAND.md:199-210` (R_H and R_X at k = 1, k = 12, k → ∞ for all ten
> registered deciles), reproduced in four rows at `progress.md:435-440`

60 cells at 4 decimal places, n = none. Produced by `band.py:68-80` over
`registry.BUCKET_EDGES_CENTS`. **Independently recomputed from the registered constants
alone: all 60 cells match at `%.4f` with zero mismatches**, including the cells whose
apparently inconsistent rounding (0.0316 vs 0.0517 at the 1–10c row; 0.0347 vs 0.0376 at
11–20 and 21–30) is the honest consequence of binary float representation, not an error.

### ★ MUST-VERIFY 5 — the margins, and the reason route X was excluded

> "route H clears by 4.84 points at 1–10c falling to **2.15 points** at 91–99c; route X clears
> by 2.83 points falling to **0.15 points** at 91–99c. **Route X's margin at the favourite
> tail (0.0015) is smaller than the 0.00195 by which Section 2's FX base understates cost at
> the same price** … Route H's margin at that bucket is 0.0215 against a comparable 0.00135 —
> larger by a factor of 16"
> — `docs/BAND.md:255-265`; the exclusion at `REGISTRATION.md:426-429` and
> `docs/BAND.md:322-327`; "5.73 points at 91c rising to 5.97 at 99c" at
> `REGISTRATION.md:423-424` and `docs/BAND.md:317-318`

n = none. Pinned by `tests/test_band.py:149-172`. **Independently recomputed: 0.08−0.0585 =
0.0215; 0.08−0.0785 = 0.0015; 0.03×0.05 = 0.0015 plus 0.015×0.03 = 0.00045 summing to
0.00195; held-route slack 0.03×0.03 + 0.00045 = 0.00135; ratio 15.93 ("a factor of 16");
R_H(0.91) = 0.0573, R_H(0.99) = 0.0597.** One cosmetic asymmetry worth a look in VERIFY:
0.04835 is written "4.84" while 0.02835 in the same sentence is written "2.83".

### ★ MUST-VERIFY 6 — the unit determination and the direction correction

> "| Bürgi's 5c contract winning 3 % | 0.03 − 0.05 = **−0.02** … | −0.02/0.05 = **−40.0 %** …
> | Bürgi's 95c contract winning 98 % | **+0.03** | **+3.16 %** | Krause's **−0.077** …
> implies a mean bucket price of **0.117** … implies a mean price of **0.043**"
> — `docs/BAND.md:128-137`, `DECISIONS.md:221-231`; the exploitable-side table with entry
> prices 0.950 / 0.950 / **0.883** at `docs/BAND.md:151-155`, `DECISIONS.md:246-250`,
> `README.md:84-88`; "the 3.0 exactly ties the fee-plus-spread floor of 0.0300 even with FX
> driven to zero" at `REGISTRATION.md:433-436`, `HYPOTHESES.md:143`, `README.md:147-149`

n: Bürgi 313,972 prices / 46,282 contracts / 12,403 events; **Krause n absent everywhere**.
**Independently recomputed: −0.02 and −40.0 %; +0.03 and +3.158 % (printed "+3.16"/"+3.1");
0.040 + 0.077 = 0.117 and 0.040/0.923 = 0.0433; 1 − 0.117 = 0.883; 0.6×0.05 = 0.030 and
0.6×0.095 = 0.057.** The underlying published magnitudes are external and unverifiable here.

### ★ MUST-VERIFY 7 — the power bars derived before any request

> "| GO, MDE ≤ 0.02 | ≥ **475** | | stay out of BLOCKED, MDE ≤ 0.08 | ≥ **30** |" at
> `v̄ = 0.0475`, "so sqrt(v̄) ≈ **0.218**"; and "GO needs about **703** markets (475 / 0.676)"
> — `REGISTRATION.md:120-137` and `REGISTRATION.md:148-150`

n = none realized; these are planning figures and the registration labels them so.
Produced by `pmexperiment/power.py:37-45`; pinned at the boundary by
`tests/test_power.py:37-62`. **Independently recomputed: 4×0.0475/0.02² = 475.0 exactly;
4×0.0475/0.08² = 29.6875 → ≥ 30; sqrt(0.0475) = 0.2179; 475/0.676 = 702.66.**
These bars are the design's whole power argument and **were never tested against a count**.

### ★ MUST-VERIFY 8 — the registered cost floor C(p) in its two written forms

> "C(p) = 0.04 + 0.01 + 0.03·p … the floor is **0.0785**" (`REGISTRATION.md:203-212`) and
> "C(p) = 0.05 + 0.03·p … C(0.95) = 0.0785. C(0.05) = 0.0515." (`REGISTRATION.md:335-338`)

n = none. Produced by `pmexperiment/power.py:74-82`; cross-pinned to `band.py` by
`tests/test_band.py:30-41` and to prose by `tests/test_power.py:76-79`.
**Independently recomputed: both forms agree and give 0.0785 and 0.0515.** Worth carrying
into VERIFY that `power.cost_floor` charges **both** fee sides while
`band.required_underpricing(HELD_TO_RESOLUTION)` charges one — the two are reconciled by
route, not in conflict, and `band.py:77-78` says so.

---

### Ranks 9–26 — not marked MUST-VERIFY

**9. The five access-gate readings and the keyless depth bracket.** "earliest retrievable
settled close sits **between 2024-01-01 (empty page) and 2024-05-31 (present)**, bracketed by
`max_close_ts` probes … **n = 6** probes" — `docs/ACCESS.md:72`, `REGISTRATION.md:389-393`,
`DECISIONS.md:100-105`. Backing artifact: **none retained**. READ-only.

**10. Stage A's request budget and latencies.** "HTTP 200, latencies **99.9–213.8 ms** across
**11** requests"; "**13 outbound requests total** … 2 robots.txt (429, 404) and 11 API reads
— 2 settled-listing reads, 6 depth brackets, 3 candlestick reads"; "HTTP 200 in **127.6 ms**,
**2 records** returned" — `docs/ACCESS.md:18,71,80-89`, `progress.md:41`. **No artifact.**

**11. Stage C's Polymarket request log.** "`robots.txt` polymarket.com **HTTP 200 in 35.7 ms,
73 bytes**, no `Disallow`"; "404 in **280.1 / 201.4 / 220.9 ms**"; "**7 requests** … plus 1
fetch of the embedded terms from `docs.google.com`"; "**zero** market-data requests" —
`docs/ACCESS.md:106-111,210-216`, `REGISTRATION.md:477-478,502-506`. **No artifact.**

**12. The Polymarket ToS size figures, which do not agree with each other.** `59,617 bytes`
(`docs/ACCESS.md:122`, `REGISTRATION.md:479`, `progress.md:726`, and quoted inside
`pmexperiment/admissibility.py:42`) against "**58,830 characters / 59,061 bytes**, against the
59,617 bytes Stage C recorded" (`docs/LICENCES.md:72-73`); and the shell at "217 KB body …
**1,354 characters**" (`docs/ACCESS.md:126-127`) against "**217,045 bytes → 1,405 characters,
0.65 % text**" (`docs/LICENCES.md:61-62`). **The disagreement is disclosed in
`docs/LICENCES.md` itself**; 1405/217045 = 0.647 % and 1354/217045 = 0.624 %, so both text
shares are internally coherent with their own numerator.

**13. The occurrence-count nulls that carry licence verdicts.** `Notices` 0, `Notice` 0,
`authorization` 0, `Attn`/`Suite`/`P.O`/`postal`/`mailing` 0 across **58,830 characters**
(`docs/LICENCES.md:195-199`); `artificial intelligence` 0, `machine learning` 0,
`large language` 0, `llm` 0, `neural` 0 (`docs/LICENCES.md:332-337`); Kalshi PDF `Effective`
0, `Last Updated` 0, `@` 0, `contact` 0, `address` 0 in a **6,648-char** document
(`docs/LICENCES.md:261-267,280`); `docs.polymarket.com` "terms of use" 0 / "license" 0 /
"acceptable use" 0 / "public data" 0 across **389,435 bytes** (`docs/ACCESS.md:188-193`,
`docs/LICENCES.md:222-223`); Dune `aggregate`/`derived`/`redistribute`/`republish`/`resell`/
`commercial use`/`creative commons`/`open source`/`public domain` 0 each
(`docs/LICENCES.md:582-586`). **No artifact for any of them.**

**14. Dataset depth figures.** `TimeSeventeen/Polymarket-v1`: **1,201,580,990 rows**,
~49.1 GB, 2022-11-21 → 2026-04-28, card read as 24,460 bytes — `docs/LICENCES.md:348-384`,
`HYPOTHESES.md:218`, `report.md:241`. Others at `docs/LICENCES.md:465-473` (1.9 B / 538,587
vs 1.1 B / 268 K contradiction; ~727 M rows; ~10,016 markets / ~5.08 M trades; 770 k+
markets / 943 M+ fills). All external, none retained.

**15. Third-party platform document measurements.** Dune ToS **172,750 bytes**, pricing shell
56,756 → 81 chars (**0.14 %**) and 67,316 → 269 (**0.40 %**), text ratio measured **18.05 %**
by one pass and **67.98 %** by another on the same body; Token Terminal 86,702 bytes /
**25.06 %**; geoblock page **509,725 bytes** — `docs/LICENCES.md:78-82,328-331,528-532,
590-597,601-609`. **The "$390/month Plus, $1,990/month Premium" figures are expressly
recorded as NOT adopted** (`docs/LICENCES.md:594-597`).

**16. Verification-effort figures.** "**13 agents, ~2.1 M subagent tokens and 454 tool uses**
across two passes, four of which died on a session limit" (`progress.md:959-960`); "**Four of
thirteen agents died**" (`docs/LICENCES.md:97`); "All **17** quoted or attributed strings …
**14 match byte-for-byte; 3 differ only in typographic apostrophes**"
(`docs/LICENCES.md:614-618`); "3 / 3" lens coverage per candidate (`docs/LICENCES.md:91-95`).

**17. Suite and mutation counts, stage by stage.** 34 (`progress.md:12`) → 39
(`progress.md:235`) → **63** with "nine new honesty tests, five verified by mutation"
(`progress.md:502-507`) → **72** with "six mutations, all six load-bearing"
(`progress.md:806-813`) → 89 with "five source-level mutations" (`progress.md:982-986`) →
**95** with "thirteen mutations, all thirteen load-bearing" (`progress.md:1202-1214`) →
**108** with "fourteen mutations, all fourteen load-bearing" (`progress.md:1517-1527`,
`DECISIONS.md:708-718`) → **111** (`progress.md:1648`). **The 111 is verified by counting
`def test_` in the anchored tree; the mutation counts are unverifiable — no mutation log,
harness or CI artifact is stored.**

**18. The closing git and credential audit.** "**32 commits, 189 reachable objects**, every
blob decompressed and scanned: **zero credential-shaped strings** … `.env.example` is **294
bytes, five comment lines, and contains no `=` at all** … `LICENSE` is MIT, **17 lines**" —
`progress.md:1537-1543`. **Verified against git: 32/189 at `1ba50aa`, 294 bytes, zero `=`,
MIT, 17 non-blank lines.**

**19. ETA-versus-actual figures for all five stages.** Stage B "**22.9 min against a 75-min
stated ETA**, overrun by a factor of 3.3 in the safe direction" (`progress.md:534-535`);
Stage C "**~17 min against 50**" (`progress.md:836`); Stage D "**~2 h 15 min against 55 min**
… overrunning by a factor of 2.5", Task 2 "**~111 min** against 20", "exceeded it by a factor
of **5.5**" (`progress.md:942,948,1255-1261`); Stage E "**~21.4 min against 50 min stated**,
**43 %** of estimate", Task 1 "landed within **3 %** — 7.8 min against 8", Task 4 "missed by a
factor of **3.2**" (`progress.md:1385-1400,1573-1574`). **Partly checkable against commit
timestamps**, which match the quoted Z-times to the second where a commit hash is given.

**20. Every registered constant, pinned to its sentence.** `0.02 to 0.08`, `z = 2.0
two-sided`, the ten deciles and the tail cell, `m = 2,000`, `seed 20260829`, `Wilson 95%
lower bound` (`WILSON_Z 1.96`), `≥ 1,000 settled markets`, `at most five records`,
30-day maturity, `$1,000` volume floor, `$0.02` per side × 2, `1 cent` half-spread, `1.5 %`
per direction × 2, `k = 1` — `REGISTRATION.md` §0.2–0.5, §2, §3, §9, Amendments 4 and 5;
`pmexperiment/registry.py:8-66`; **mechanically pinned by `tests/test_registry.py`.**

**21. Imported figures from other repositories in this program.** NPD "**0.0512** against an
effect band of **0.01 to 0.05** … after **415 days** of collection and **6.9378 USD** of
spend" (`REGISTRATION.md:31-38`, `README.md:182-186`, `CLAUDE.md:54-58`); Insider "**BLOCKED
at 49.35 bp**" (`REGISTRATION.md:47`, `README.md:187-188`); MLCryptoEngine "H2 … cross-venue
transfer at **AUC 0.501**" (12 occurrences across 6 files); "**Eleven** MLCryptoEngine
hypotheses closed on cost rather than on signal" (`REGISTRATION.md:710-712`,
`DECISIONS.md:162`). **Cross-repo checkable; not checkable inside PMExperiment.**

**22. Figures imported from the published literature.** Bürgi-Deng-Whelan: **313,972**
Yes-and-No prices on **46,282** contracts across **12,403** events, Kalshi 2021 → April 2025,
staked ≥ $1,000, spread ≤ 20c, open ≥ 24 h; "lose over **60 %**"; "**−40 %**"; "**+3.1 %**";
"average pre-fee return **−20 %**"; "**two-thirds** of all recorded prices sit in the 1–10c
and 90–99c bands". Krause: sub-30c settled YES **4.0 %**, bias **−0.077**, **n never
recorded**. CPI companion: SSRN **7087538**, **95 contracts over 12 months**, no classic
bias. Page-Clemen: EJ **123(568):491–513, 2013**; "MAE roughly triples between the closing day
and ten days out" — `REGISTRATION.md:225-251`, `docs/BAND.md:37-63`. **External.**

**23. The zero-totals that carry the closure.** "**Five stages. Zero dollars. Zero contracts
enumerated. Zero market-data requests to Polymarket. Zero requests of any kind in Stage E. No
price bucket, no dispersion, and no statistic relating a price to an outcome, anywhere,
ever.**" — `report.md:476-478`, `README.md:16`, `REGISTRATION.md:628-630`,
`progress.md:1547-1549`. **Negative claims; the git tree corroborates the absence of any
artifact, but no request log exists to corroborate the request counts.**

**24. The operator prior, "5 to 8 percent".** `README.md:170`, `REGISTRATION.md:1021-1022`,
`HYPOTHESES.md:267`, `DECISIONS.md:642`, `report.md:352,416-417`. **Explicitly labelled
stated-not-registered everywhere it appears** (see Provenance P9).

**25. Kalshi's documented rate limit, "Basic tier 200 reads/s".** `docs/ACCESS.md:75`,
`DECISIONS.md:132-133`, `progress.md:45`. **Labelled "claim, not a measurement"** in the same
row, with ADR-007 (2026-08-29) as the named deviation.

**26. The candlestick probe.** "1 candle" on a fresh traded market; "**0 daily candles**" on
`NASDAQ100-24OCT25-T21499.99`, closed 2024-10-25, over T−40d..T — `docs/ACCESS.md:21`,
`progress.md:44`. **Counted ambiguous and attributed to nothing**, per standing rule 15.
No artifact.

---

## 3. Intervals and tests

**There is no confidence interval, no p-value, no test statistic, no standard error and no
estimate of any effect reported anywhere in this repository.** That is not an omission; it is
the repository's central claim about itself, asserted in `README.md:13-14`,
`REGISTRATION.md:384-387`, `HYPOTHESES.md:16-17`, `report.md:357-358`, and in every stage
entry. A grep across all ten documents and all eleven Python files for `confidence`,
`interval`, `p-value`, `significan`, `standard error`, `bootstrap`, `t-stat` returns only
standing rule 10's "union time **intervals** before summing", `REGISTRATION.md:293`'s
unfilled Section 8, and one test-function name.

What exists instead is **registered statistical machinery that never fired**, plus imported
test-shaped figures. Eleven entries:

| # | entry | file:line | stated estimator / test | n | data structure |
|---|---|---|---|---|---|
| I1 | `MDE = z · sqrt(v̄ / n_T)`, z = **2.0 two-sided** | `REGISTRATION.md:99-106`, `REGISTRATION.md:301-308`, `pmexperiment/power.py:37-45` | minimum detectable effect on a proportion, normal approximation | **none — never computed on any cell** | a tail-cell count `n_T` and a mean Bernoulli dispersion `v̄` |
| I2 | the verdict map GO ≤ 0.02 < DEGRADED ≤ 0.08 < BLOCKED, lower edge inclusive | `REGISTRATION.md:105-112`, `pmexperiment/power.py:48-71` | threshold rule against the registered effect band | none | one `GateReading` per cell |
| I3 | `v̄` = mean of `p_i(1−p_i)` over the cell's snapshot prices, "computed from prices alone. No outcome enters it" | `REGISTRATION.md:74-77` | null Bernoulli dispersion | none | integer-cent prices 1–99 |
| I4 | planning dispersion **0.0475** at 5c/95c, `sqrt(v̄) ≈ 0.218` | `REGISTRATION.md:120-129`, `tests/test_power.py:21` | planning value, labelled as such | none | — |
| I5 | planning bars **n_T ≥ 475** (GO) and **n_T ≥ 30** (out of BLOCKED) | `REGISTRATION.md:126-129` | inversion of I1 | none | — |
| I6 | **Wilson 95 % lower bound** on the sampled tail share, `WILSON_Z = 1.96` | `REGISTRATION.md:88-95`, `REGISTRATION.md:303-304`, `pmexperiment/registry.py:33` | Wilson score interval, lower bound; `n_T = N × bound` | none — no universe was ever enumerated, so no sample was ever drawn | a uniform sample of m = 2,000 without replacement, seed 20260829 |
| I7 | Section 8, **Inference** — "the estimator, the interval construction, the clustering unit, and the trial grid with its multiplicity correction" | `REGISTRATION.md:291-295` | **`*To be registered after the gate fires.*` — never registered** | — | — |
| I8 | boundary assertions n = 475 → MDE 0.02 (GO), 474 → DEGRADED, 30 → DEGRADED, 29 → BLOCKED, 0 → BLOCKED with `mde is None` | `tests/test_power.py:24-73` | unit tests of I1/I2 | synthetic | — |
| I9 | imported: MLCryptoEngine H2 cross-venue transfer at **AUC 0.501** | `HYPOTHESES.md:103,191,241,300,347`, `REGISTRATION.md:625,693,1150`, `DECISIONS.md:153`, `report.md:222,456`, `docs/LICENCES.md:656`, `progress.md:215,777,1139,1554` | ROC AUC from another repository | not stated here | — |
| I10 | imported: NPD realized minimum detectable contrast **0.0512** vs band **0.01 to 0.05**, after **415 days** and **6.9378 USD** | `REGISTRATION.md:31-44`, `CLAUDE.md:54-58`, `README.md:182-186`, `DECISIONS.md:41-42` | MDE from another repository, quoted verbatim as a block quote | not stated here | — |
| I11 | imported: Insider fired **BLOCKED at 49.35 bp** | `REGISTRATION.md:46-47`, `CLAUDE.md:60-61`, `README.md:187-188`, `DECISIONS.md:43-44` | a cost/power gate figure from another repository | not stated here | — |

**Two things a verifier should look at, both of which are registered-and-unfired and
therefore affect no reported result.** First, I1 uses `z` alone with **no power term `z_β`**,
so "minimum detectable effect" here is a one-standard-error-style detectability threshold at
roughly 50 % power rather than the conventional `(z_{α/2}+z_β)·SE`; the registration inherits
the form from InsiderExperiment (`REGISTRATION.md:46-49`, `pmexperiment/power.py:51-55`) and
does not claim otherwise. Second, I6's constant is **1.96**, the two-sided 95 % z, while the
text names a **one-sided** "95 % **lower** bound" — for which 1.645 is the conventional value;
`tests/test_registry.py:59-66` pins the constant to the phrase without reconciling them.
Neither was ever exercised, because no cell was ever built.

---

## 4. Provenance claims

Twenty-five claims that something was fixed before, or independently of, the thing it judges.
Where git settles one, the result is stated.

| # | claim, verbatim | file:line | commit named | what would have to be true |
|---|---|---|---|---|
| **P1** | "**Section 0 registered 2026-08-29, before the first request to the measured source.** No request had been sent to any Kalshi endpoint when the commit carrying this section was made." | `REGISTRATION.md:7-9`; restated `HYPOTHESES.md:22`, `report.md:37`, `progress.md:57-59` | none named; the commit is `9080186` | The commit exists at **2026-08-29T07:37:33Z** (verified). `progress.md:58-59` puts the first request at "~07:44Z". **No retained probe response timestamps that request**, so the ordering rests on the commit plus the session's own log. |
| **P2** | "**Made 2026-08-30**" on Amendments **1, 2 and 3**, and "**Status: accepted, 2026-08-30**" on the second ADR-006 and second ADR-007 | `REGISTRATION.md:667, 707, 751`; `DECISIONS.md:140, 160` | all five landed in one commit, `f686036` | The commit's author and committer date is **2026-08-29T18:05:26Z (11:05:26 −07:00)** — **one calendar day earlier than the stated date, in UTC and in local time alike**. The *ordering* claim survives intact (`f686036` 18:05Z precedes the band verdict `32dc10a` at 19:24:06Z), but the *dates* do not match the objects. |
| **P3** | "**Made 2026-08-29, before the band gate fired** and while no statistic relating a price to an outcome exists. **Registered before it is used**, as Stage B Task 3 requires." (Amendment 4, the FX turnover) | `REGISTRATION.md:783-785` | `4d75f66` | Verified: `4d75f66` at **2026-08-29T19:17:21Z**, band verdict `32dc10a` at **19:24:06Z**. Note the internal oddity this creates with P2: Amendment 4 is dated a day **before** the Amendment 2 it operates under. |
| **P4** | "**Recorded rather than tidied:** `registry.FX_TURNOVER_REGISTERED` was committed in **`9b4bd4f`**, one commit *before* the Amendment 4 text it cites landed in **`4d75f66`**." | `DECISIONS.md:304-307`; also `progress.md:515-518` | `9b4bd4f`, `4d75f66` | **Verified exactly.** `9b4bd4f` (19:15:55Z) touches `registry.py`, `band.py`, `tests/test_band.py`, `tests/test_guards.py`; `4d75f66` (19:17:21Z) is the immediately following commit and touches `REGISTRATION.md` only. The repository disclosed its own lag correctly. |
| **P5** | "**Made 2026-08-30, before a single contract had been enumerated from any venue.**" (Amendment 5, the volume floor) | `REGISTRATION.md:855-856`; ADR-011 `DECISIONS.md:313-315` | `f789079` | Verified: **2026-08-30T03:34:00Z**. "Before enumeration" is trivially satisfied — nothing was ever enumerated, anywhere. |
| **P6** | "**Made 2026-08-30, before any contract was enumerated from Polymarket** and while no statistic relating a price to an outcome exists." (Amendment 6) | `REGISTRATION.md:914-916` | `1b3124e` | Verified: **2026-08-30T03:40:52Z**. |
| **P7** | "**Made 2026-09-02**" on Amendments 7, 8 and 9, and on ADR-016 through ADR-021 | `REGISTRATION.md:1011, 1073, 1122`; `DECISIONS.md:553, 635, 686, 750, 771, 787` | `fe7e6b9`, `f8128b2`, `905d552`, `03d16e7` | Verified: all four commits are dated **2026-09-02**, 09:32Z–09:50Z. |
| **P8** | "The band is computed once and registered. It is **not** recomputed after seeing a calibration result, and **no bucket may be added to it afterwards.**" | `REGISTRATION.md:744-745`; enforced again at `REGISTRATION.md:1106-1111`, `HYPOTHESES.md:153-157`, `DECISIONS.md:729-734` | none named | **Verified by git: `docs/BAND.md` has exactly one commit in its entire history — `34307b6`, 2026-08-29T19:22:44Z — and has never been modified since.** |
| **P9** | "Section 13, `The operator prior` … **it was never filled, and it is left empty permanently.** … **This prior may not be described anywhere as pre-registered**" | `REGISTRATION.md:1015-1029`; `README.md:168-175`; `DECISIONS.md:666-674`; `report.md:434-441` | none named | Verified at HEAD: Section 13 still reads *"To be filled by the operator before the gate fires"* with no figure. Pinned by `tests/test_honesty.py:508-527`. A full-history diff would settle "never filled"; the Sections 0–14 hash below already does. |
| **P10** | "The paragraph below **stands unedited as it was registered on 2026-08-29**, so a reader can see what the design provided for and what actually happened." (Section 16) | `REGISTRATION.md:636-641` | none named | The section carries an **explicitly disclosed** closure annotation prepended above the original paragraph. Whether the original paragraph itself is byte-identical is a `git diff` on Section 16 alone. |
| **P11** | "Amendments append here, numbered … **Nothing above this line is edited after Section 0 is committed.**" | `REGISTRATION.md:660-661` | none named | **Partly verified, and the interesting part verifies.** Sections **0 through 14 are byte-identical from `9080186` to HEAD** — SHA-256 of that region is `a33f7768…` at all eleven commits that touched the file after registration. What *did* change above Section 17 is Section 15 (`*Written only after a gate fires*`, `REGISTRATION.md:369`) and the Section 16 annotation, both of which the design provides for. |
| **P12** | "Rule 12 requires the terms be recorded *before any repeated fetch*. Stage A read **11 keyless market requests** before its terms position was established … Stage C read `robots.txt` and the terms **first**, and therefore sent **zero** market-data requests." | `REGISTRATION.md:495-500`; `docs/ACCESS.md:203-206`; `DECISIONS.md:386-389`; `report.md:180-186` | none | Only the session's own narrative attests the ordering. **No request ledger, no response body and no timestamped log is stored**, and standing rule 6's "ledgers are append-only and fsynced" has no file behind it here. |
| **P13** | "**Zero market-data requests were sent to Polymarket. Zero requests of any kind were sent in Stage E.**" | `README.md:108-109`; `REGISTRATION.md:528-531`; `docs/ACCESS.md:214-216` | none | Same as P12: an unfalsifiable negative from inside the repository. The absence of any stored response is consistent with it, and `.gitignore`'s `data/raw/` line plus an empty `data/` is the only corroboration available. |
| **P14** | "**the raw probe responses were not retained beyond this report** and the two tickers named above" | `docs/ACCESS.md:87-89` | none | **Verified as an absence**: no probe artifact exists at any commit. This is the sentence that makes every Stage A/C/D measurement irreproducible, and the repository states it plainly. |
| **P15** | "Raw enumeration responses contain result fields and are **stored untouched in `data/raw/` (gitignored, append-only)**"; and Section 14: "The gate verdict must be **regenerable from: the stored raw enumeration and candlestick responses under `data/raw/`** … A rerun may depend on no other state." | `REGISTRATION.md:320-321`; `REGISTRATION.md:359-363` | none | **`data/raw/` does not exist** in the live tree (read 2026-09-05T23:28Z; `data/` holds one 0-byte `.gitkeep`). Consistent with no enumeration ever having run, but it means Section 14's reproducibility clause is **vacuous** rather than satisfied. |
| **P16** | "**32 commits, 189 reachable objects**, every blob decompressed and scanned: **zero credential-shaped strings**" | `progress.md:1537-1539` | none named | **Verified exactly at `1ba50aa`**, which was HEAD when Stage E Task 5 ran: `git rev-list --count` = **32**, `git rev-list --objects \| wc -l` = **189**. (At the anchored HEAD the same commands give 36 and 213.) |
| **P17** | "`.env.example` … is **294 bytes, five comment lines, and contains no `=` at all** — pinned by a test since the scaffold" | `progress.md:1539-1541` | none | **Verified byte-for-byte**: 294 bytes, 5 lines, 0 occurrences of `=`. Pinned by `tests/test_honesty.py:98-100`. |
| **P18** | "`LICENSE` is MIT, **17 lines**, `Copyright (c) 2026 kirosli00tuff`" | `progress.md:1541-1542` | none | MIT and the copyright line verified. The file is **21 physical lines / 17 non-blank**, so "17 lines" is the non-blank count. |
| **P19** | "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** … The measured logging time is **2026-08-30T03:31Z**" | `progress.md:652-658` | `84f7b92` | **Verified: `84f7b92` is dated 2026-08-30T03:31:03Z.** The repository caught and corrected its own extrapolated timestamp, and the correction is right. |
| **P20** | ADR-012's own self-conviction: "**the Kalshi Data Terms of Use print no date at all** — `Effective` 0 occurrences, `Last Updated` 0 — so the finding **met two of three** elements" | `README.md:65-74`; `DECISIONS.md:435-439`; `docs/LICENCES.md:266-276`; `progress.md:999-1010` | none | The PDF is **not retained**, so the occurrence counts are unverifiable here. The *consequence* — that the Kalshi claim is UNMEASURED under the repository's own procedure — is verifiable against `pmexperiment/admissibility.py` and is pinned by `tests/test_admissibility.py`. |
| **P21** | "The **received date was not in the prompt and was not synthesized**. Standing rule 5 forbids exactly that, so it was asked for and supplied: **2026-09-01**." | `progress.md:1419-1420`; `REGISTRATION.md:533-544`; `docs/ACCESS.md:220-234` | none | **The correspondence itself is not in the repository** — `docs/ACCESS.md:285-289` and ADR-016 say so ("what this repository holds is **the operator's summary of the reply, not its text**"). The claim is recorded UNMEASURED by the repository's own procedure. |
| **P22** | "the fee band of Amendment 2 fires **first**. The power gate fires **second**, and only over a region the band left open." (Amendment 3, the registered gate order) | `REGISTRATION.md:765-767`; `HYPOTHESES.md:112-115`; `DECISIONS.md:158-174` | none | Trivially satisfied: the power gate never fired. Commit order confirms the band gate's definition (`f686036`) precedes its firing (`32dc10a`). |
| **P23** | "**A floor chosen by someone else, before this repository existed, cannot have been tuned to this sample**" — the $1,000 volume floor imported verbatim from Bürgi-Deng-Whelan | `REGISTRATION.md:862-877`; `pmexperiment/registry.py:44-50`; ADR-011 `DECISIONS.md:323-328` | none | Requires that the benchmark study really uses "total staked ≥ $1,000" — **external, unverifiable here**. `tests/test_registry.py:77-87` pins **both** the number and its citation sentence, which is the strongest internal guarantee available. |
| **P24** | "`tests/test_registry.py` **pins the figures to the document**, so code and registration cannot drift apart silently" | `pmexperiment/registry.py:1-6` | none | **Verified by reading the test**: nine tests assert each constant against a quoted substring of `REGISTRATION.md`. This is a real, mechanised provenance guard and it covers every constant the band gate consumes. |
| **P25** | "**Every guard here carries a test that fails when the guard is removed, verified by mutation**" — and the per-stage mutation tallies (9, 5, 5, 6, 13, 14, 2) | `README.md:231-232`; `CLAUDE.md:45-46`; `progress.md:502-507, 806-813, 982-989, 1202-1214, 1517-1535, 1645-1648`; `DECISIONS.md:708-718` | none | **No mutation log, harness script or CI artifact is stored anywhere.** The tests that would be killed are present and readable; the claim that each mutation was run and killed is READ-only. The repository does record three separate harness faults that produced false-green mutation runs (`progress.md:815-833, 991-997, 1232-1246, 1638-1648`), which is itself the reason to treat the tallies as unverified. |

---

## 5. Live-repository access log

Purpose of access: (1) git history and objects for provenance; (2) `ls -la` of the working
tree to establish what untracked data exists. **No repository file was opened for writing, no
git state-changing command was run, and no repository script was executed.** All content was
read from the anchored snapshot; the live tree was inspected only by `ls -la`, `wc -c`,
`grep -c` on two already-tracked files (`LICENSE`, `.env.example`), and read-only git
plumbing (`rev-parse`, `rev-list`, `log`, `show`, `ls-tree`, `branch`, `tag`, `remote`,
`notes list`, `status --porcelain`).

Commands used against the live repository, all read-only:
`git rev-parse HEAD`, `git rev-parse --abbrev-ref HEAD`, `git log --format=… --date=iso-strict`,
`git rev-list --count`, `git rev-list --objects`, `git show --stat`, `git show <c>:<path>`,
`git log -- <path>`, `git ls-tree -r --name-only HEAD`, `git branch -a`, `git tag`,
`git remote -v`, `git notes list`, `ls -la`, `ls -laR data/`, `cat .git/info/exclude`,
`cat _CLOSED_DO_NOT_RUN_HERE`, `wc -c .env.example`, `wc -l LICENSE`, `head -3 LICENSE`,
`grep -c`. Extracted blobs were written **only** to the session scratchpad and to
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-locate/`.

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` BEFORE first
access — 2026-09-05T23:26:57Z:**

```
```

(empty — the command produced no output; exit status 0)

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` AFTER last
access — 2026-09-05T23:30:32Z:**

```
```

(empty — the command produced no output; exit status 0)

**Both outputs are empty and identical. Nothing was modified.** The working tree carries one
untracked file, `_CLOSED_DO_NOT_RUN_HERE`, which does not appear in `status` because it is
listed in `.git/info/exclude` (verified by reading that file). This is **pre-existing operator
dirt, not mine**: it is dated 2026-09-02 22:38 local, three days before this access, and its
own text says it was "written 2026-09-02 after a session was opened here by mistake." It is
reported here rather than passed over, per the common rules' instruction to report any
working-tree entry beyond the listed pre-existing exceptions.

**Recomputation scratch** (outside every audited path):
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-locate/band_recompute.py` and
`round_check.py`, run with the audit venv. They read no repository file — every constant is
typed in from the registration — and write nothing outside the work directory.
