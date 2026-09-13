# PMExperiment — provenance verification (VERIFY)

**Agent C (referee/verifier). No thesis.** This document establishes what the git objects, the
stored code and the document text actually support about the claim that bars, parameters, an
outcome map, a prior and a decision rule were fixed in a named commit or before data existed.
Where a claim verifies it is recorded as verified; where it cannot be checked it is recorded as
unverifiable and is not guessed at.

| | |
|---|---|
| Repository | `PMExperiment` |
| Anchored SHA | `03d16e71dbf25a86c529884662d02136f8e82334` (main, 2026-09-02, closed project) |
| Snapshot read (document text) | `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/` |
| Live repo (read-only git plumbing only) | `/home/kiros-li/Documents/GitHub/PMExperiment/` |
| Compiled | 2026-09-12, 02:20Z–02:45Z |
| Input | `findings/agentC/verification/PMExperiment.inventory.md` §4 and `.inventory.json` `provenance_claims` (25 claims, P1–P25) |
| History size | **36 commits**, all by `kirosli00tuff <[private email removed]>`, 2026-08-29T07:09:55Z → 2026-09-02T09:50:29Z. Author date == committer date on every commit. Committer timezone is −07:00; **every time in this document is UTC.** |

## Counts

| | SUPPORTED | PARTIAL | NOT_SUPPORTED | UNVERIFIABLE | total |
|---|---|---|---|---|---|
| registration claims (P1–P25) | 13 | 5 | 1 | 6 | **25** |
| parameter changes | 7 | 4 | 1 | 0 | **12** |
| **total** | **20** | **9** | **2** | **6** | **37** |

Three draft findings: **DRAFT-P-1 (S3)**, **DRAFT-P-2 (S4)**, **DRAFT-P-3 (S3)**. None of them
moves a verdict; all three are stated with that said plainly.

---

## What "before data existed" means in this repository, established first

This determines every date comparison below, so it is established before the tables rather than
asserted inside them.

**No data artifact was ever committed.** `git log --all --diff-filter=A --name-only` over the
entire 36-commit history adds exactly 32 files: ten Markdown documents, five Python modules,
seven test files, three `.gitkeep` markers, and seven config/toolchain files. **Zero** files with
a `.json`, `.csv`, `.parquet`, `.db`, `.ndjson`, `.jsonl`, `.txt`, `.pkl`, `.npy` or `.sqlite`
extension exist at any commit. `data/` in the live tree holds one 0-byte `.gitkeep`
(`ls -laR`, read 2026-09-12T02:41Z — **UNANCHORED**, may have changed after the anchor);
`data/raw/` and `data/vendor/` are in `.gitignore` (`PMExperiment/.gitignore:12-13`) and neither
directory exists.

So "data" here has exactly two meanings and they must not be conflated:

1. **Measurements that existed** — Stage A's 11–13 keyless Kalshi HTTP probes, first sent at
   **~2026-08-29T07:44Z** (`PMExperiment/progress.md:58-59`, the session's own log; **no probe
   response was retained**, `PMExperiment/docs/ACCESS.md:87-89`), and Stage C's Polymarket
   `robots.txt`/terms reads on **2026-08-30** (`PMExperiment/docs/ACCESS.md:115-126`). These are
   the only "data existed" boundary that matters, and it is attested by the repository's own log
   and by nothing else.
2. **A statistic relating a price to an outcome** — **never existed at any commit.** Every
   amendment that says "while no statistic relating a price to an outcome exists" is therefore
   trivially true for the whole history, and is marked as such rather than credited as a
   demonstration.

**Every registered constant was fixed at one commit and never changed.**
`pmexperiment/registry.py` has three commits — `9080186` (49 lines added), `9b4bd4f` (9 added),
`f789079` (8 added) — and **zero deleted lines across all three**. `pmexperiment/band.py` has one
commit (`9b4bd4f`). `pmexperiment/power.py` has one commit (`9080186`).
`pmexperiment/admissibility.py` has one commit (`b67fc84`). `docs/BAND.md` has one commit
(`34307b6`). No bar, threshold, horizon, universe bound, z-value, n target or cost figure in this
repository was ever edited after it was first committed. That is the single most load-bearing
result in this document and it is verified by plumbing, not by reading.

---

## 1. Registration claims table

`commit found` gives the commit the claim's content actually landed in, its UTC author date, and
`(=cd)` where author date equals committer date (true for all 36 commits).

| # | claim (abridged; verbatim quotes in the findings and the JSON) | file:line | commit named in doc | commit found + UTC date | data first existed | status | notes |
|---|---|---|---|---|---|---|---|
| **P1** | "Section 0 registered 2026-08-29, before the first request to the measured source." | `REGISTRATION.md:7-9` | none | `9080186` **2026-08-29T07:37:33Z** | first probe ~07:44Z (`progress.md:58-59`, log only) | **PARTIAL** | Commit half fully verified: `git show 9080186 --stat` touches `REGISTRATION.md` (+258/−60), `pmexperiment/power.py` (+82), `pmexperiment/registry.py` (+49) and four test files. The claimed content is in that commit's version — `9080186:REGISTRATION.md:103` "**0.02 to 0.08**", `:110-112` the GO/DEGRADED/BLOCKED map with edges, `:206` `C(p) = 0.04 + 0.01 + 0.03·p`, `:208` "**0.0785**", `:301` "z = 2.0 two-sided". Ordering half rests on the session log alone; no retained probe timestamps it. |
| **P2** | "**Made 2026-08-30**" (Amendments 1, 2, 3) and "**Status:** accepted, 2026-08-30." (2nd ADR-006, 2nd ADR-007, ADR-008) | `REGISTRATION.md:667,707,751`; `DECISIONS.md:140,160,180` | none | `f686036` **2026-08-29T18:05:26Z** (11:05:26 −07:00) | Stage A probes, 2026-08-29 ~07:44Z | **NOT_SUPPORTED** | The date is wrong by one calendar day in UTC **and** in the committer's own −07:00 local time. See **DRAFT-P-1**. |
| **P3** | Amendment 4: "**Made 2026-08-29, before the band gate fired** … **Registered before it is used**" | `REGISTRATION.md:783-785` | `4d75f66` (via ADR-010) | `4d75f66` **2026-08-29T19:17:21Z** | as above | **SUPPORTED** | Band verdict `32dc10a` is **2026-08-29T19:24:06Z** — 6 min 45 s later. `4d75f66 --stat` touches `REGISTRATION.md` only (+72/−0). |
| **P4** | "`registry.FX_TURNOVER_REGISTERED` was committed in **`9b4bd4f`**, one commit *before* the Amendment 4 text it cites landed in **`4d75f66`**" | `DECISIONS.md:304-307`; `progress.md:515-518` | `9b4bd4f`, `4d75f66` | `9b4bd4f` **19:15:55Z**; `4d75f66` **19:17:21Z** | as above | **SUPPORTED** | Exact. `9b4bd4f` touches `band.py` (+135), `registry.py` (+9), `tests/test_band.py` (+184), `tests/test_guards.py` (+19/−2); `4d75f66` is the immediately next commit and touches `REGISTRATION.md` only. The added constant reads `FX_TURNOVER_REGISTERED: float = 1.0` under the comment "# --- Amendment 4 — the FX turnover". The repository disclosed its own lag correctly. |
| **P5** | Amendment 5: "**Made 2026-08-30, before a single contract had been enumerated from any venue.**" | `REGISTRATION.md:855-856`; `DECISIONS.md:313-315` | none | `f789079` **2026-08-30T03:34:00Z** | as above | **SUPPORTED** | Date correct in UTC (local date is 2026-08-29T20:34 −07:00, i.e. the repository dates by UTC here — which is what makes P2 anomalous). "Before enumeration" is trivially satisfied: nothing was enumerated at any commit. |
| **P6** | Amendment 6: "**Made 2026-08-30, before any contract was enumerated from Polymarket**" | `REGISTRATION.md:914-916` | none | `1b3124e` **2026-08-30T03:40:52Z** | as above | **SUPPORTED** | `1b3124e --stat`: `REGISTRATION.md` +151/−0, `docs/ACCESS.md` +127/−0. |
| **P7** | "**Made 2026-09-02**" on Amendments 7, 8, 9 and ADR-016 … ADR-021 | `REGISTRATION.md:1011,1073,1122`; `DECISIONS.md:553,635,686,750,771,787` | `905d552` (progress.md:1569) | Am.7 `fe7e6b9` **09:32:22Z**; Am.8 `f8128b2` **09:34:01Z**; Am.9 `03d16e7` **09:50:29Z**; ADR-016 `17dfebd` **09:31:26Z**; ADR-017 `fe7e6b9`; ADR-018 `905d552` **09:44:12Z**; ADR-019/020/021 `03d16e7` — all 2026-09-02 | as above | **SUPPORTED** | Each introducing commit located with `git log -S"### Amendment n —"` / `-S"## ADR-0nn."` `--reverse`. All six dates correct in UTC and in local time. |
| **P8** | "The band is computed once and registered. It is **not** recomputed after seeing a calibration result, and **no bucket may be added to it afterwards.**" | `REGISTRATION.md:744-745`; `:1106-1111`; `HYPOTHESES.md:153-157`; `DECISIONS.md:729-734` | none | `docs/BAND.md`: **exactly one commit**, `34307b6` **2026-08-29T19:22:44Z** | as above | **SUPPORTED** | Verified three ways: `git log --follow -- docs/BAND.md` returns one commit; `pmexperiment/band.py` returns one commit (`9b4bd4f`); `pmexperiment/registry.py` has zero deleted lines across its three commits, so `BUCKET_EDGES_CENTS`, `EFFECT_BAND_LO/HI` and every cost constant are byte-identical from `9080186` to HEAD. |
| **P9** | Section 13 "was never filled, and it is left empty permanently … **may not be described anywhere as pre-registered**" | `REGISTRATION.md:1015-1029`; `README.md:168-175`; `DECISIONS.md:666-674`; `report.md:434-441` | none | n/a — region unchanged since `9080186` | as above | **SUPPORTED** | Section 13 sits inside the Sections 0–14 region whose **SHA-256 is `00a7e9aa6b36d3d1…` at all eleven versions** of `REGISTRATION.md` from `9080186` to `03d16e7` (script: `scratchpad/work/agentC-pm-prov2/regions.py`). At HEAD it reads "*To be filled by the operator before the gate fires*" with no figure. Independently: the operator's prior "**5 to 8 percent**" first enters the repository at `2006ae6` **2026-09-02T09:23:41Z**, the Stage E operator prompt logged verbatim — i.e. at closure, after every verdict, exactly as `HYPOTHESES.md:267` states. |
| **P10** | Section 16: "The paragraph below **stands unedited as it was registered on 2026-08-29**" | `REGISTRATION.md:636-641` | none | `9080186`; annotation added `f8128b2` **2026-09-02T09:34:01Z** | as above | **SUPPORTED** | SHA-256 of the "Written before the read. **H1 closes** …" paragraph is `42173f13e69a04da…` at every version from `9080186` to HEAD. `f8128b2` touches `REGISTRATION.md` with **+117/−0** — the closure annotation is a pure insertion. |
| **P11** | "Amendments append here … **Nothing above this line is edited after Section 0 is committed.**" | `REGISTRATION.md:660-661` | none | `9080186`; one contradicting edit at `98ce2d4` **2026-08-29T07:53:10Z** | as above | **PARTIAL** | The substance verifies hard (Sections 0–14 byte-identical; Section 16's paragraph byte-identical; all other growth above Section 17 is pure insertion: `4d75f66` +72/−0, `32dc10a` +59/−0, `f789079` +59/−0, `1b3124e` +151/−0, `17dfebd` +56/−0, `fe7e6b9` +62/−0, `f8128b2` +117/−0, `03d16e7` +54/−0). The literal sentence is contradicted by exactly one line: see **DRAFT-P-2**. |
| **P12** | "Stage A read **11 keyless market requests** before its terms position was established … Stage C read `robots.txt` and the terms **first**, and therefore sent **zero** market-data requests." | `REGISTRATION.md:495-500`; `docs/ACCESS.md:203-206`; `DECISIONS.md:386-389`; `report.md:180-186` | none | — | — | **UNVERIFIABLE** | No request ledger, response body or timestamped outbound log exists at any commit (complete added-file list above). `CLAUDE.md:29` standing rule 6, "Ledgers are append-only and fsynced", has no file behind it in this repository. Recorded as unverifiable, not as contradicted. |
| **P13** | "**Zero market-data requests were sent to Polymarket. Zero requests of any kind were sent in Stage E.**" | `README.md:108-109`; `REGISTRATION.md:528-531`; `docs/ACCESS.md:214-216` | none | — | — | **UNVERIFIABLE** | An unfalsifiable negative from inside the repository. The total absence of any stored response at any commit is *consistent* with it and is not evidence for it. |
| **P14** | "**the raw probe responses were not retained beyond this report**" | `docs/ACCESS.md:87-89` | none | — | — | **SUPPORTED** | Verified as an absence over the whole history, not just at HEAD: the complete `--diff-filter=A` file list contains no data-shaped file. This is the sentence that makes every Stage A/C/D measurement irreproducible, and the repository states it plainly. |
| **P15** | "stored untouched in `data/raw/` (gitignored, append-only)" and Section 14's "regenerable from: the stored raw enumeration and candlestick responses under `data/raw/`" | `REGISTRATION.md:320-321`; `:359-363` | none | `9080186` (both sentences are pre-registration design text, inside the byte-identical Sections 0–14) | — | **PARTIAL** | `data/raw/` **does not exist** (live `ls -laR data/`, 2026-09-12T02:41Z, UNANCHORED). The clause is a forward-looking requirement written before the read, and no enumeration ever ran, so Section 14's reproducibility guarantee is **vacuous rather than violated**. Not raised as a finding: the repository states everywhere that zero contracts were enumerated. |
| **P16** | "**32 commits, 189 reachable objects** … **zero credential-shaped strings**" | `progress.md:1537-1539` | none | audit ran at `1ba50aa` **2026-09-02T09:36:29Z** | — | **SUPPORTED** | Recomputed: `git rev-list --count 1ba50aa` = **32**; `git rev-list --objects 1ba50aa | wc -l` = **189**. Exact. (At the anchored HEAD: 36 and 213.) The "zero credential-shaped strings" half is a scan result with no stored output and is not separately verified here. |
| **P17** | "`.env.example` … is **294 bytes, five comment lines, and contains no `=` at all**" | `progress.md:1539-1541` | none | `10041da` (scaffold), never modified | — | **SUPPORTED** | `wc -c` = **294**, `wc -l` = **5**, `grep -c "="` = **0**. Byte-for-byte. |
| **P18** | "`LICENSE` is MIT, **17 lines**, `Copyright (c) 2026 kirosli00tuff`" | `progress.md:1541-1542` | none | `10041da`, never modified | — | **PARTIAL** | MIT and the copyright line verified (`head -3`). The file is **21 physical lines / 17 non-blank** (`wc -l` = 21, `grep -c .` = 17), so "17 lines" is the non-blank count. Hygiene only; no finding raised. |
| **P19** | "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** … The measured logging time is **2026-08-30T03:31Z**" | `progress.md:652-666` | `84f7b92` | `84f7b92` **2026-08-30T03:31:03Z** | — | **SUPPORTED** | The correction is right to the minute. `84f7b92 --stat` touches `progress.md` only (+109/−0). The repository caught its own extrapolated timestamp and appended the correction rather than editing in place — which is what makes **DRAFT-P-1** an omission rather than a habit. |
| **P20** | "the Kalshi Data Terms of Use print no date at all — `Effective` 0 occurrences, `Last Updated` 0" | `README.md:65-74`; `DECISIONS.md:435-439`; `docs/LICENCES.md:266-276`; `progress.md:999-1010` | none | — | — | **UNVERIFIABLE** | The PDF is not retained at any commit, so the occurrence counts cannot be checked. The *consequence* — the Kalshi claim is UNMEASURED under the repository's own procedure — is verifiable against `pmexperiment/admissibility.py` and is pinned by `tests/test_admissibility.py` (which contains `test_stage_a_kalshi_claim_carries_no_effective_date_in_the_record`). |
| **P21** | "The **received date was not in the prompt and was not synthesized** … **2026-09-01**." | `progress.md:1419-1420`; `REGISTRATION.md:533-544`; `docs/ACCESS.md:220-234` | none | — | — | **UNVERIFIABLE** | The correspondence is not in the repository, and `docs/ACCESS.md:285-289` / ADR-016 say so ("the operator's summary of the reply, not its text"). The claim is recorded UNMEASURED by the repository's own procedure. |
| **P22** | "the fee band of Amendment 2 fires **first**. The power gate fires **second**" | `REGISTRATION.md:765-767`; `HYPOTHESES.md:112-115`; `DECISIONS.md:158-174` | none | chain below | Stage A probes | **SUPPORTED** | Commit order is unambiguous: gate defined `f686036` **18:05:26Z** → arithmetic `9b4bd4f` **19:15:55Z** → FX amendment `4d75f66` **19:17:21Z** → table `34307b6` **19:22:44Z** → verdict `32dc10a` **19:24:06Z**. The power gate never fired at all; `pmexperiment/power.py` has one commit, at registration, and no caller. |
| **P23** | "**A floor chosen by someone else, before this repository existed, cannot have been tuned to this sample**" ($1,000 volume floor) | `REGISTRATION.md:862-877`; `pmexperiment/registry.py:44-50`; `DECISIONS.md:323-328` | none | `f789079` **2026-08-30T03:34:00Z** | — | **UNVERIFIABLE** | External: whether Bürgi-Deng-Whelan really uses "total staked ≥ $1,000" cannot be checked from here. Internally the strongest available guarantee is real: `f789079` adds the constant, the Amendment 5 text and `tests/test_registry.py::test_volume_floor_is_pinned_to_amendment_five` **in one commit**, and that test asserts both the number *and* the citation sentence "total staked ≥ $1,000, final spread ≤ 20c" against `REGISTRATION.md`. The constant has never been edited. |
| **P24** | "`tests/test_registry.py` **pins the figures to the document**, so code and registration cannot drift apart silently" | `pmexperiment/registry.py:1-6` | none | `9080186` (docstring), tests grown at `9b4bd4f`, `f789079` | — | **PARTIAL** | Nine tests in `tests/test_registry.py` assert **17 of the 18** registered constants against quoted `REGISTRATION.md` substrings. The eighteenth, `FX_TURNOVER_REGISTERED`, is pinned elsewhere and not there: numerically at `tests/test_band.py:184` and to its document sentence ("k = 1 binds") at `tests/test_honesty.py:218-221`, with an enforcement-site guard at `tests/test_guards.py:102-114`. **The guarantee exists; only the attribution to one file is over-broad.** No finding raised — the drift the sentence promises to catch is in fact caught. |
| **P25** | "**Every guard here carries a test that fails when the guard is removed, verified by mutation**" + tallies 9, 5, 5, 6, 13, 14, 2 | `README.md:231-232`; `CLAUDE.md:45-46`; `progress.md:502-507, 806-813, 982-989, 1202-1214, 1517-1535, 1645-1648`; `DECISIONS.md:708-718` | none | — | — | **UNVERIFIABLE** | No mutation log, harness script or CI artifact exists at any commit — `scripts/` contains only `.gitkeep` in the complete added-file list. The tests that would be killed are present and readable; that each mutation was *run* and killed is document-only. The repository itself records harness faults that produced false-green runs (`progress.md:815-833, 991-997, 1232-1246, 1638-1648`), which is the strongest internal reason to treat the tallies as unverified, and it is the authors who recorded them. |

---

## 2. Parameter changes after data table

Every change to a bar, parameter, universe, gate or decision rule made after the first
measurement existed (2026-08-29 ~07:44Z), whether or not it is a finding.

| # | what changed | where | introduced by + UTC date | data that existed at the time | dated amendment? | amendment ref | status | notes |
|---|---|---|---|---|---|---|---|---|
| **C1** | **The measurement universe moves venue**: Section 1's source Kalshi → Polymarket | `REGISTRATION.md:665-703` | `f686036` **2026-08-29T18:05:26Z** | Stage A's 11–13 keyless Kalshi probes and its PENDING_ACCESS verdict (`98ce2d4`, 07:53:10Z) | **yes** | Amendment 1 + 2nd ADR-006 (`DECISIONS.md:138-156`) | **PARTIAL** | The change is amended, numbered, reasoned, and carries the data that existed (Kalshi PENDING_ACCESS, the keyless spring-2024 depth bound, MLCryptoEngine's AUC 0.501 transfer ground). **Its stated date is wrong by one day** — DRAFT-P-1. Nothing else about it fails. |
| **C2** | **A new gate is added ahead of the registered power gate**: the fee-versus-edge band, with three new verdict rows BAND-EMPTY / BAND-NARROW / BAND-OPEN | `REGISTRATION.md:705-747` | `f686036` **2026-08-29T18:05:26Z** | as C1 | **yes** | Amendment 2 + 2nd ADR-007 (`DECISIONS.md:158-176`) | **PARTIAL** | This is the most consequential change in the repository — the band gate produced its only verdict. Verified: the three verdict conditions in `f686036:REGISTRATION.md:503-505` are the same three under which `32dc10a` fired **1 h 19 m later**, and the gate reads "no contract, no price and no outcome from any venue". The quantifier it turns on (existential over the band, judged at its top) is taken from Amendment 2's own rationale sentence "no price region where a documented effect could survive" and the choice is disclosed in `pmexperiment/band.py:83-96`, with the strict alternative implemented and reported beside it at `band.py:99-105`. **Only the stated date fails** — DRAFT-P-1. |
| **C3** | **Scope change**: the terminal question now admits whether a tradeable edge exists | `REGISTRATION.md:749-780` | `f686036` **2026-08-29T18:05:26Z** | as C1 | **yes** | Amendment 3 + ADR-008 (`DECISIONS.md:178-196`) | **PARTIAL** | Amended and reasoned; the no-trading guard in `CLAUDE.md` is unaltered across the whole history. **Stated date wrong by one day** — DRAFT-P-1. |
| **C4** | **New cost parameter**: `FX_TURNOVER_REGISTERED = 1.0` (the binding k = 1 case, which sets the 0.0300 FX-free floor and the 2.15-point held-route margin) | `pmexperiment/registry.py:58-66`; `REGISTRATION.md:782-853` | constant `9b4bd4f` **19:15:55Z**; text `4d75f66` **19:17:21Z** | Stage A probes; no contract data, ever | **yes** | Amendment 4 + ADR-010 (`DECISIONS.md:300-311`) | **SUPPORTED** | Registered 6 m 45 s before the verdict it feeds. The 1 m 26 s code-before-text lag is itself disclosed and correct (P4). Value never edited. |
| **C5** | **New filter bar**: `PERMITTED_MIN_VOLUME_USD = 1000.0` added to the permitted subset | `pmexperiment/registry.py:44-50`; `REGISTRATION.md:855-912` | `f789079` **2026-08-30T03:34:00Z** | Stage A probes; zero contracts ever enumerated | **yes** | Amendment 5 + ADR-011 (`DECISIONS.md:311-341`) | **SUPPORTED** | Constant, amendment text and the pinning test land in **one commit**. Imported from an external study (external half unverifiable — P23). Never edited. It binds nothing, because no universe was ever enumerated. |
| **C6** | **A registered premise is retracted**: Amendment 1's ground for moving to Polymarket is withdrawn after Polymarket's terms were read | `REGISTRATION.md:914-1009` | `1b3124e` **2026-08-30T03:40:52Z** | Stage C's Polymarket `robots.txt` + Terms read, same session | **yes** | Amendment 6 + ADR-012 (`DECISIONS.md:344-393`) | **SUPPORTED** | A retraction recorded as an amendment rather than an edit; date correct. |
| **C7** | **New admissibility bar**: `MIN_DOCUMENT_TEXT_RATIO = 0.05` (below it, a page is classed a client-rendered shell and the claim it carries falls to UNMEASURED) | `pmexperiment/admissibility.py:39-49` | `b67fc84` **2026-08-30T04:28:05Z** | the Polymarket shell measurement it is calibrated from, made **the same day** in Stage C (`docs/ACCESS.md:125-126`) | **no numbered amendment**; dated ADR-012 records the *rule*, not the *number* | ADR-012 `DECISIONS.md:344-347` (accepted 2026-08-30, commit `52d39ec` 03:45:12Z); derivation disclosed in the module docstring | **PARTIAL** | See **DRAFT-P-3**. The derivation is disclosed with the measurement and the direction of error named; the bar appears nowhere in `REGISTRATION.md`; and it **bound no verdict** — `docs/LICENCES.md:76-82` records that both extraction methods (18.05 % and 67.98 %) "clear the 5 % bar and the classification is unchanged", and says so under the heading "**A limitation of the text-ratio bar, found by using it.**" |
| **C8** | **New decision rule**: ADR-012's three required elements (`clause`, `effective_date`, `fetch_date`), applied retroactively to claims already in the record | `pmexperiment/admissibility.py:51-54`; `DECISIONS.md:344-393` | rule `52d39ec` **2026-08-30T03:45:12Z**; code `b67fc84` **04:28:05Z** | Stage A's 2026-08-29 Kalshi permission claim and Amendment 1's premise, both already committed | **yes** | Amendment 6 / Section 15.3 record ADR-012 | **SUPPORTED** | A rule created after the claims it then judges — and the repository fired it **first over its own claims** (commit subject of `b67fc84`), convicting its own Stage A position, pinned by `tests/test_admissibility.py::test_stage_a_kalshi_claim_carries_no_effective_date_in_the_record`. Retroactive application is disclosed, dated, and self-convicting rather than self-serving. The three elements were applied to Stage D's candidates only after being committed (`7b5a751` **06:22:49Z**). |
| **C9** | **Edit above the amendment line**: `REGISTRATION.md` Section 15's placeholder "*Written only after the gate fires. Empty until then.*" → "*Written only after a gate fires.*" | `REGISTRATION.md:369` | `98ce2d4` **2026-08-29T07:53:10Z** (+32/−1) | Stage A probes, ~9 min earlier | **no** | — | **NOT_SUPPORTED** (against P11's literal sentence) | See **DRAFT-P-2**. No figure, bar or rule changed; it is a wording change to a results placeholder that the design provides for. |
| **C10** | **In-place edits to an evidence document**: `docs/LICENCES.md` corrected twice | `docs/LICENCES.md` | `3204e5a` **2026-08-30T06:25:40Z** (+131/−31); `baa2bf3` **06:35:19Z** (+52/−8) | Stage D's three licence candidates, read the same session | **yes (disclosed)** | commit bodies + `progress.md` Entry 9/9.1 | **SUPPORTED** | Both edits belong to a resumed verification pass folded back into the document. The commit body states "The corrections all narrow or weaken the record and none changes a verdict." Verified: no registered constant, bar or figure is touched by either commit, and the accompanying `tests/test_honesty.py` change (+62/−3) is a re-wrap of one assertion plus two added tests — **no assertion was weakened** (`git show baa2bf3 -- tests/test_honesty.py`). |
| **C11** | **README rewritten for a cold reader** | `README.md` | `1ba50aa` **2026-09-02T09:36:29Z** (+199/−65) | everything | n/a | commit body; `progress.md` Entry 11 | **SUPPORTED** | Numeric diff across the rewrite: the only figures present before and absent after are `2024` and `429`, both Stage-A narrative details — and both are **retained** at `REGISTRATION.md:391, 524, 539` and `docs/ACCESS.md:46, 58, 72, 320`. Every verdict figure survives (`0.0512`, `0.01 to 0.05`, `415 days`, `49.35 bp` at `README.md:183-188`; `5.85`, `8.00`, `0.0300` added). No registered figure changed. |
| **C12** | **Everything else: no change at all** | `pmexperiment/registry.py`, `band.py`, `power.py`, `admissibility.py`, `docs/BAND.md` | — | — | n/a | — | **SUPPORTED** | The exhaustive deletion sweep over all 36 commits (`git log --reverse -p --unified=0` across the whole tree, filtered to removed lines) returns **no deleted line anywhere that carries a bar, threshold, horizon, universe bound, alpha, z-value, n target or cost figure**. Every such figure's first appearance is also its only one: `0.02 to 0.08`, `z = 2.0`, `20260829`, `0.0785`, `0.0515`, `0.015` at `9080186`; `0.0585` at `9b4bd4f`; `5.85`, `8.00 points`, `0.0300` at `34307b6`; `1000.0` at `f789079`. |

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** The registration dates carried by Amendments 1, 2 and 3, by the second ADR-006, the second ADR-007 and ADR-008, by `HYPOTHESES.md`'s venue-split amendment and by `progress.md` Entry 3 — i.e. the stated date of the commit that registered the fee-versus-edge band gate, the repository's only fired verdict.
- **Direction:** neutral — the true registration is one day **earlier** than stated, so the ordering claim (registered before fired) is strengthened, not weakened; nothing in the verdict moves.
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim quote):** "**Made 2026-08-30, before any statistic relating a price to an outcome exists.**" — PMExperiment/REGISTRATION.md:667; "**Made 2026-08-30.** A new gate, ordered ahead of the power gate, because it is" — PMExperiment/REGISTRATION.md:707; "**Made 2026-08-30.** A deliberate scope change, recorded rather than allowed to" — PMExperiment/REGISTRATION.md:751; "**Status:** accepted, 2026-08-30." — PMExperiment/DECISIONS.md:140, PMExperiment/DECISIONS.md:160, PMExperiment/DECISIONS.md:180; "## Amended 2026-08-30 — the venue split, and what H1 now means" — PMExperiment/HYPOTHESES.md:87; "## Entry 3 — amendments 1 to 3: venue, fee band, scope — 2026-08-30" — PMExperiment/progress.md:202.
- **Evidence:**
  - All eight statements landed in **one commit**, `f686036ac2cab96b7c451c23a48c53d2bbb8431a`, whose **author date and committer date are both 2026-08-29T18:05:26Z** (`Sat Aug 29 11:05:26 2026 -0700`). Verified by `git show f686036 --stat --format='%H%nauthor:%ad%ncommit:%cd'` against the live repo, read 2026-09-12T02:24Z. The date is wrong by one calendar day **in UTC and in the committer's own −07:00 local time alike**; no timezone reachable from −07:00 places 18:05:26Z on 2026-08-30.
  - The amendment text itself is present in that commit's version: `git show f686036:REGISTRATION.md` line 430 "**Made 2026-08-30, before any statistic relating a price to an outcome exists.**", line 470 and line 514 likewise; `git show f686036:DECISIONS.md` lines 140, 160, 180 "**Status:** accepted, 2026-08-30." So the wrong date was written at the time, not introduced later.
  - **The repository's own record contradicts it twice more.** (i) The very next commit, `e2d8f10` at **2026-08-29T19:07:37Z**, logs `progress.md` Entry 4 as "**Logged 2026-08-29T19:08Z, per standing rule 1**" (PMExperiment/progress.md:248-249) — a later event correctly dated 08-29. (ii) ADR-009 and ADR-010, committed **1 h 17 m after** `f686036` in `34307b6` at 2026-08-29T19:22:44Z, are dated "**Status:** accepted, 2026-08-29." (PMExperiment/DECISIONS.md, ADR-009 at :210 and ADR-010 at :276). The register therefore reads, in document order, 08-30 → 08-29 → 08-29, and `REGISTRATION.md:783` has Amendment 4 "**Made 2026-08-29**" operating under the Amendment 2 it says was made on 08-30.
  - **Every other date in the repository is correct.** Amendment 4 (`4d75f66`, 19:17:21Z) says 08-29 ✓; Amendment 5 (`f789079`, 2026-08-30T03:34:00Z) says 08-30 ✓; Amendment 6 (`1b3124e`, 03:40:52Z) says 08-30 ✓; ADR-011/012/013/014/015 (03:34:00Z–06:35:19Z) say 08-30 ✓; Amendments 7/8/9 and ADR-016…021 (2026-09-02, 09:31:26Z–09:50:29Z) say 2026-09-02 ✓; `progress.md` Entry 7 and Entry 9 headers say 08-30 ✓. The `f686036` block is the sole exception in 36 commits.
  - This is the exact error class the repository names and corrects elsewhere: "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** It was extrapolated … rather than read from the clock" (PMExperiment/progress.md:652-656), with the principle "**a timestamp inferred from a previous timestamp is documented, not measured**" (PMExperiment/progress.md:660-662), and standing rule 4 "**Measured beats documented.**" (PMExperiment/CLAUDE.md:25).
- **Recomputation (if any):** none required — a date comparison. Inputs: `git show f686036 --format='%ad %cd' --date=iso-strict` (live repo, read 2026-09-12T02:24Z) vs the eight quoted document lines in `snap/PMExperiment/`. Method: compare stated calendar date to the commit's author date in UTC and in −07:00. Result: stated 2026-08-30, actual 2026-08-29 in both. Tolerance: exact.
- **What would resolve it:** an appended, dated correction in `progress.md` in the shape Entry 6.1 already uses, stating that Amendments 1–3, the second ADR-006/007, ADR-008, the `HYPOTHESES.md` venue-split amendment and Entry 3 were made on 2026-08-29T18:05:26Z and that the recorded 2026-08-30 was inferred rather than read. No registered value needs to change.
- **Confidence:** HIGH — the commit's author and committer dates are immutable git object fields and the eight document lines are in that same commit's tree.
- **Invalidated by later commits?:** no — `03d16e7` is the anchored HEAD and the final commit; `f686036`'s object cannot change, and nothing after it corrects the date.
- **Disclosed by authors?:** no. The repository corrects an analogous timestamp error at `PMExperiment/progress.md:650-666` (Entry 6.1) and nowhere mentions this one; `PMExperiment/progress.md:511-512` in fact repeats it, describing the two ADR-006/007 pairs as coming "from the **2026-08-29 and 2026-08-30** sessions" when git dates both sessions to 2026-08-29 (07:53:10Z and 18:05:26Z).

### DRAFT-P-2
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `REGISTRATION.md`'s immutability guarantee for everything above the Section 17 amendment line.
- **Direction:** neutral — pure hygiene; the edited line is a results placeholder and carries no figure, bar or rule.
- **Class:** PROVENANCE
- **Severity:** S4
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim quote):** "Amendments append here, numbered, each carrying its own evidence and the date it was made. Nothing above this line is edited after Section 0 is committed." — PMExperiment/REGISTRATION.md:660-661
- **Evidence:**
  - Section 0 was committed in `9080186` at 2026-08-29T07:37:33Z. Sixteen minutes later, `98ce2d4` (2026-08-29T07:53:10Z) edits `REGISTRATION.md` with **+32/−1**, and the one deleted line is above the amendment line: `git show 98ce2d4 -- REGISTRATION.md` shows `-*Written only after the gate fires. Empty until then.*` replaced by `+*Written only after a gate fires.*` at what is now PMExperiment/REGISTRATION.md:369.
  - That is the **only** contradicting edit in the history. Every other change above Section 17 is a pure insertion — `git log --numstat -- REGISTRATION.md` gives `4d75f66` +72/−0, `32dc10a` +59/−0, `f789079` +59/−0, `1b3124e` +151/−0, `17dfebd` +56/−0, `fe7e6b9` +62/−0, `f8128b2` +117/−0, `03d16e7` +54/−0 — and `f686036`'s single deletion is the `*(empty)*` placeholder *below* the line, inside Section 17 itself.
  - **The substance of the guarantee verifies hard, and that is the more important result.** SHA-256 of the whole Sections 0–14 region is `00a7e9aa6b36d3d1…` at **all eleven versions** of `REGISTRATION.md` from `9080186` to HEAD; SHA-256 of Section 16's original paragraph is `42173f13e69a04da…` at all eleven (script: `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov2/regions.py`, run 2026-09-12T02:31Z). No registered value, bar, map, prior or rule was ever edited in place.
- **Recomputation (if any):** inputs `git show <c>:REGISTRATION.md` for the eleven versions from `9080186` to `03d16e7`; method: extract the line range from the `## 0.` header to the `## 15. ` header and from `Written before the read.` to the following `---`, SHA-256 each; result: one distinct digest per region across all eleven versions. Tolerance: exact byte equality.
- **What would resolve it:** either narrowing the sentence to what is true and already provided for ("Sections 0–14 are never edited; Section 15 is written as gates fire and Section 16 may carry a dated closure annotation"), or an appended note recording the `98ce2d4` wording change.
- **Confidence:** HIGH — a single-line diff in a git object, with the surrounding history exhaustively checked for others.
- **Invalidated by later commits?:** no — `03d16e7` is the anchored HEAD and the final commit.
- **Disclosed by authors?:** partly. The registration itself designates Section 15 as "*Written only after a gate fires.*" (PMExperiment/REGISTRATION.md:369) and Section 16's annotation is explicitly flagged as "**Recorded 2026-09-02 at closure, before the paragraph it qualifies**" (PMExperiment/REGISTRATION.md:636-638), so the *practice* of writing above the line is disclosed; the specific in-place edit of the placeholder sentence is not recorded anywhere.

### DRAFT-P-3
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** `MIN_DOCUMENT_TEXT_RATIO = 0.05`, the bar that separates a readable document from a client-rendered shell and so decides whether a permission claim is ADMISSIBLE or falls to UNMEASURED under ADR-012.
- **Direction:** neutral — the bar fails closed (toward UNMEASURED), and it was in fact non-binding on every recorded verdict, so no closure or positive in the repository rests on it.
- **Class:** PROVENANCE
- **Severity:** S3
- **Label:** DERIVED (git objects + code)
- **Claim challenged (verbatim quote):** "**Do not tune a filter to increase a sample.** Register it, then report what it yields." — PMExperiment/CLAUDE.md:36; read against "Changing a registered value now requires a numbered amendment appended to Section 17, carrying its own evidence." — PMExperiment/REGISTRATION.md:9-10
- **Evidence:**
  - The bar is set from a measurement rather than registered ahead of one, and the code says so: "The one client-rendered page this repository has measured sets this bar. `docs/ACCESS.md` records `polymarket.com/tos` returning HTTP 200 with a 217 KB body that stripped to 1,354 characters of text — a text share near 0.6 % … A plain or lightly marked-up document sits far above 5 %; an app shell sits far below it." — PMExperiment/pmexperiment/admissibility.py:39-48, with `MIN_DOCUMENT_TEXT_RATIO: float = 0.05` at PMExperiment/pmexperiment/admissibility.py:49.
  - **Ordering, from git:** the measurement it is calibrated from was recorded in Stage C on 2026-08-30 (PMExperiment/docs/ACCESS.md:125-126, committed `1b3124e` 2026-08-30T03:40:52Z). The bar was committed **48 minutes later**, in `b67fc84` at **2026-08-30T04:28:05Z** — `pmexperiment/admissibility.py` has exactly one commit in the whole history. It was then applied to the three Stage D licence candidates in `7b5a751` at **2026-08-30T06:22:49Z**.
  - **The figure 0.05 appears nowhere in `REGISTRATION.md`.** `grep -n "text ratio\|text share\|5 %\|client-rendered" REGISTRATION.md` returns only unrelated hits (the Wilson bound at :92, the 1.5 % FX schedule at :201, :787, :836). The dated ADR that records the rule — ADR-012, "**Status:** accepted, 2026-08-30" at PMExperiment/DECISIONS.md:346 — names the three required elements and no numeric bar. So the bar exists in code with a dated commit and a disclosed rationale, but in no numbered amendment.
  - **It bound nothing.** The repository measured the same document two ways and recorded both: "On the same retained Dune body, the verification pass measured **18.05 %** text and this session's own tag-stripping measured **67.98 %**. Both clear the 5 % bar and the classification is unchanged" — PMExperiment/docs/LICENCES.md:76-79. No Stage D verdict turned on the ratio.
- **Recomputation (if any):** none — an ordering and presence check. Inputs: `git log --follow -- pmexperiment/admissibility.py` and `git log --follow -- docs/ACCESS.md` (live repo, read 2026-09-12T02:33Z); `grep` over `snap/PMExperiment/REGISTRATION.md`. Result: bar committed 2026-08-30T04:28:05Z, after the 2026-08-30T03:40:52Z measurement that sets it, and absent from the registration. Tolerance: exact.
- **What would resolve it:** a numbered amendment in Section 17 recording the 5 % bar, the measurement it was read off, the date, and the direction of error — the same treatment Amendments 4 and 5 give the FX turnover and the volume floor; or an explicit statement that ADR-012's numeric threshold is deliberately held in code and outside the registration, with the reason.
- **Confidence:** MEDIUM — the commit ordering and the absence from the registration are certain; whether a bar that decides ADMISSIBLE vs UNMEASURED counts as a "filter" under standing rule 9, as opposed to a procedural admissibility test, is a reading of the rule rather than a measurement.
- **Invalidated by later commits?:** no — `admissibility.py` has one commit and `03d16e7` is the anchored HEAD.
- **Disclosed by authors?:** **yes, substantially.** The derivation from the Polymarket shell measurement, and the direction of error it introduces, are stated in full at PMExperiment/pmexperiment/admissibility.py:39-48; the bar's method-dependence is recorded by the authors themselves under the heading "**A limitation of the text-ratio bar, found by using it.**" at PMExperiment/docs/LICENCES.md:76-82, which also records that the classification is unchanged. What is *not* disclosed is only that the number sits in no numbered amendment. This finding is therefore capped at S3 and is a process gap, not a discovery about the verdicts.

---

## 4. What could not be checked, and why

Recorded as unverifiable, not converted into findings. Six of the twenty-five provenance claims
(P12, P13, P20, P21, P23, P25) cannot be settled from inside this repository, and one further
claim (P1) is half-settled.

| item | why it cannot be checked | what would settle it |
|---|---|---|
| **The first-request time, ~07:44Z on 2026-08-29** (P1's second half) | `docs/ACCESS.md:87-89` states "the raw probe responses were not retained beyond this report". No response body, header, or outbound log exists at any commit. The ordering claim therefore rests on `progress.md:58-59` plus the commit time. | A retained response with a `Date` header, or a request ledger with fsynced timestamps. |
| **Request ordering within Stage A and Stage C** (P12) | Same absence. `CLAUDE.md:29` standing rule 6 promises append-only fsynced ledgers; no ledger file was ever committed. | An append-only request ledger in git or in `data/`. |
| **"Zero requests" to Polymarket and in Stage E** (P13) | An unfalsifiable negative. Absence of stored responses is consistent with it and is not evidence for it. | An outbound-request log, or a network capture. |
| **The Kalshi PDF occurrence counts, `Effective` 0 / `Last Updated` 0** (P20) | The PDF is not retained at any commit. | The retained PDF, or a hash of it recorded at fetch time. |
| **The Kalshi desk reply and its received date 2026-09-01** (P21) | The correspondence is not in the repository, and `docs/ACCESS.md:285-289` and ADR-016 say so. | The message itself, or a hash committed at receipt. |
| **That Bürgi-Deng-Whelan uses "total staked ≥ $1,000"** (P23) | External to this repository and to this audit's read scope. | The cited publication. |
| **The mutation tallies 9, 5, 5, 6, 13, 14, 2** (P25) | No mutation log, harness script or CI artifact exists at any commit; `scripts/` holds only `.gitkeep`. The repository records three harness faults that produced false-green runs. | A committed mutation-run log or CI output. |
| **"zero credential-shaped strings" over 189 objects** (P16's second half) | The scan's output was not retained; only its two counts were, and those verify exactly. | The scan output, or a re-run — out of scope here, since it would require decompressing every blob. |

**What I would have expected to find if a provenance thesis held, and did not find.** A
post-hoc-registration audit looks for: a bar edited after a result was seen; a threshold that
first appears in the same commit as the verdict it clears; a band recomputed after a calibration
reading; an amendment back-dated to precede the data it responds to; a prior filled in after the
fact and then described as pre-registered. **None of these is present.** `registry.py` has zero
deleted lines across its three commits; `band.py`, `power.py`, `admissibility.py` and
`docs/BAND.md` have one commit each; Sections 0–14 of the registration are byte-identical across
eleven versions; the band gate's definition precedes its firing by 79 minutes and its arithmetic
by 8 minutes; the operator's prior enters the repository at closure, in the operator's own logged
prompt, and every document that mentions it says it was not registered in advance. The one dating
error found (DRAFT-P-1) runs in the direction that makes the registration look **later** than it
was — the opposite of the direction a back-dating thesis would predict.

---

## 5. Live-repository access log

**Purpose of access:** git objects for provenance (history, dates, per-commit file contents,
diffs, object counts), plus one `ls -laR` of `data/` to establish whether `data/raw/` exists.
**No repository file was opened for writing, no git state-changing command was run, and no
repository script was executed.** All document text was read from the anchored snapshot at
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`.

Commands used against the live repository, all read-only: `git rev-parse HEAD`,
`git log --format=… --date=iso-strict [--reverse] [--follow] [--numstat] [-p] [-S…] [-- <path>]`,
`git show <commit> --stat`, `git show <commit>:<path>`, `git show <commit> -- <path>`,
`git rev-list --count`, `git rev-list --objects`, `git log --all --diff-filter=A --name-only`,
`git status --porcelain`, and `ls -laR data/`. One scratch script
(`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov2/regions.py`) shelled out to
`git show <c>:REGISTRATION.md` only and wrote nothing outside the work directory.

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` BEFORE first access —
2026-09-12T02:20:41Z:**

```
```

(empty — the command produced no output; exit status 0)

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` AFTER last access —
2026-09-12T02:44:52Z:**

```
```

(empty — the command produced no output; exit status 0)

**Both outputs are empty and identical; `git rev-parse HEAD` returns
`03d16e71dbf25a86c529884662d02136f8e82334` before and after. Nothing was modified.** The working
tree carries one untracked file, `_CLOSED_DO_NOT_RUN_HERE`, which does not appear in `status`
because it is listed in `.git/info/exclude`. This is **pre-existing operator dirt, not mine** —
it was already recorded by the LOCATE pass on 2026-09-05 and is dated 2026-09-02, before either
access. It is reported here rather than passed over, per the common rules.

**Unanchored reads** (working tree, not the snapshot): `ls -laR
/home/kiros-li/Documents/GitHub/PMExperiment/data/` at **2026-09-12T02:41Z** — one 0-byte
`.gitkeep`, no `data/raw/`, no `data/vendor/`. This may have changed after the 2026-09-02 anchor.

**Recomputation scratch** (outside every audited path):
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov2/` — `regions.py` (region
hashing across eleven `REGISTRATION.md` versions) and `claims.txt` (the inventory's 25 claims,
dumped for working reference).
