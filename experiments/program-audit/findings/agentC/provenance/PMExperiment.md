# PMExperiment — provenance verification (agent C, referee)

**Agent C has no thesis.** This document establishes what the git objects, the stored
documents and the working tree actually support about *when* each bar, parameter, outcome map,
prior and decision rule was fixed. A claim that verifies is recorded as verified, in the same
detail as one that does not. Unverifiable is recorded as unverifiable and is never guessed at.

| | |
|---|---|
| Repository | `PMExperiment` |
| Anchored SHA | `03d16e71dbf25a86c529884662d02136f8e82334` (`main`, 2026-09-02 — also live `HEAD` at read time) |
| Document text read from | `/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/` (snapshot at the anchor) |
| Git objects read from | `/home/kiros-li/Documents/GitHub/PMExperiment/` — read-only plumbing only |
| Source inventory | `findings/agentC/verification/PMExperiment.inventory.md` §4 (P1–P25) and `.json` `provenance_claims` |
| Compiled | 2026-09-11, 02:02Z–02:11Z |
| History size | **36 commits**, all authored and committed by `kirosli00tuff <[private email removed]>`, author date == committer date on every one; one branch `main`, no tags, no notes |

**All times in this document are UTC.** The repository's commits carry a `-07:00` offset; the
repository's own convention is UTC read from `date -u` (`progress.md:663-666`), and every date
comparison below is made in UTC and cross-checked in local `-07:00`. Where the two conventions
would give different answers this is stated; there is exactly one commit where they do not, and
it is the one finding.

---

## 0. The short version

**The substantive provenance of this repository verifies, and verifies unusually well.**

- **Not one registered constant was ever modified or removed.** `pmexperiment/registry.py` has
  exactly **three** commits and all three are **purely additive** (`git log --follow -p`):
  `9080186` creates it, `9b4bd4f` appends `FX_TURNOVER_REGISTERED`, `f789079` appends
  `PERMITTED_MIN_VOLUME_USD`. `Z_CRITICAL 2.0`, `EFFECT_BAND_LO 0.02`, `EFFECT_BAND_HI 0.08`,
  the ten `BUCKET_EDGES_CENTS`, `TAIL_BUCKETS_CENTS`, `SNAPSHOT_S24_HOURS`/`S30_DAYS`,
  `UNRESTRICTED_SAMPLE_SIZE 2000`, `SAMPLE_SEED 20260829`, `WILSON_Z 1.96`,
  `ACCESS_MIN_SETTLED_MARKETS 1000`, `ACCESS_OUTCOME_PRESENCE_MAX_RECORDS 5`,
  `PERMITTED_MIN_MATURITY_DAYS 30` and the whole cost model are **byte-identical from
  `9080186` (2026-08-29T07:37:33Z) to HEAD**.
- **`REGISTRATION.md` Sections 0 through 14 are byte-identical across all eleven commits that
  touched the file after registration** (SHA-256 of the region is constant; recomputed
  independently of the LOCATE pass).
- **`pmexperiment/band.py`, `pmexperiment/power.py`, `docs/BAND.md`, `tests/test_band.py` and
  `tests/test_power.py` each have exactly one commit in the entire history.** The gate that
  produced the repository's one verdict, and the document recording it, have never been touched
  since they were written.
- **`DECISIONS.md` and `report.md` have zero deletions in their entire history**; `progress.md`
  has zero deletions after `180c235`, which predates Entry 0. The three append-only claims hold
  against the objects.
- **No test pin was ever weakened.** Every deletion in a test file is a rename, a `ruff`
  re-wrap, a guard-scope *widening*, or the deliberate inverted scaffold test whose own
  docstring announces its replacement.
- **Every date stamp in the repository matches the git object that carries it — except the
  seven carried by one commit, `f686036`.** All 20 other ADR `Status:` dates, all six other
  amendment `Made` dates, and all `HYPOTHESES.md` amendment headers match their commits exactly.

**One finding.** `f686036` (2026-08-29T18:05:26Z) carries seven document date stamps, all
reading **2026-08-30** — one calendar day later than the commit, in UTC and in local `-07:00`
alike. That is **DRAFT-P-1** (S2). It is a dating error, not an ordering error: git shows the
ordering the repository claims. One further literal over-statement is recorded as **DRAFT-P-2**
(S4, disclosed by the authors).

---

## 1. Registration claims table

Every claim the inventory located that something was fixed in a named commit, or before the
thing it judges existed. `commit found` gives the short SHA and its **author == committer** date
in UTC.

### 1.1 The Section-0 registration and the amendments

| # | claim (verbatim, trimmed) | file:line | commit named in doc | commit found (UTC) | status |
|---|---|---|---|---|---|
| **RC1** (P1) | "**Section 0 registered 2026-08-29, before the first request to the measured source.** No request had been sent to any Kalshi endpoint when the commit carrying this section was made." | `REGISTRATION.md:7-9` | none | `9080186` **2026-08-29T07:37:33Z** | **PARTIAL** |
| **RC2** (P2) | Amendment 1 — "**Made 2026-08-30, before any statistic relating a price to an outcome exists.**" | `REGISTRATION.md:667` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC3** (P2) | Amendment 2 — "**Made 2026-08-30.** A new gate, ordered ahead of the power gate" | `REGISTRATION.md:707` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC4** (P2) | Amendment 3 — "**Made 2026-08-30.** A deliberate scope change" | `REGISTRATION.md:751` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC5** (P2) | ADR-006 (second) — "**Status:** accepted, 2026-08-30." | `DECISIONS.md:140` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC6** (P2) | ADR-007 (second) — "**Status:** accepted, 2026-08-30." | `DECISIONS.md:160` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC7** (P2) | ADR-008 — "**Status:** accepted, 2026-08-30." | `DECISIONS.md:180` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC8** | "## **Amended 2026-08-30** — the venue split, and what H1 now means" | `HYPOTHESES.md:87` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC9** | "## Entry 3 — amendments 1 to 3: venue, fee band, scope — **2026-08-30**" | `progress.md:202` | none | `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** (date) |
| **RC10** | "the pair dated 2026-08-29 … and the pair **dated 2026-08-30** (Polymarket; the fee band ordering) … **Cite an ambiguous number with its date.**" | `DECISIONS.md:197-204` | none | both pairs: `98ce2d4` **2026-08-29T07:53:10Z** and `f686036` **2026-08-29T18:05:26Z** | **NOT_SUPPORTED** — both pairs are 2026-08-29 in git, so the registered disambiguator does not disambiguate against the objects |
| **RC11** (P3) | Amendment 4 — "**Made 2026-08-29, before the band gate fired** and while no statistic relating a price to an outcome exists. **Registered before it is used**, as Stage B Task 3 requires." | `REGISTRATION.md:783-785` | `4d75f66` (in ADR-010) | `4d75f66` **2026-08-29T19:17:21Z**; band table `34307b6` **19:22:44Z**; verdict `32dc10a` **19:24:06Z** | **SUPPORTED** |
| **RC12** (P4) | "`registry.FX_TURNOVER_REGISTERED` was committed in **`9b4bd4f`**, one commit *before* the Amendment 4 text it cites landed in **`4d75f66`**. Both sit inside the same task and no verdict fired between them" | `DECISIONS.md:304-307`; `progress.md:515-518` | `9b4bd4f`, `4d75f66` | `9b4bd4f` **19:15:55Z** (touches `registry.py`, `band.py`, `tests/test_band.py`, `tests/test_guards.py`); `4d75f66` **19:17:21Z**, the immediately following commit, touches `REGISTRATION.md` only; no verdict between them | **SUPPORTED — exactly** |
| **RC13** (P5) | Amendment 5 — "**Made 2026-08-30, before a single contract had been enumerated from any venue.**" | `REGISTRATION.md:855-856`; ADR-011 `DECISIONS.md:313-315` | none | `f789079` **2026-08-30T03:34:00Z** | **SUPPORTED** |
| **RC14** (P6) | Amendment 6 — "**Made 2026-08-30, before any contract was enumerated from Polymarket**" | `REGISTRATION.md:914-916` | none | `1b3124e` **2026-08-30T03:40:52Z** | **SUPPORTED** |
| **RC15** (P7) | "**Made 2026-09-02**" on Amendments 7, 8, 9 and "accepted, 2026-09-02" on ADR-016…ADR-021 | `REGISTRATION.md:1011, 1073, 1122`; `DECISIONS.md:553, 635, 686, 750, 771, 787` | `905d552` at `progress.md:1569` | `17dfebd` 09:31:26Z, `fe7e6b9` 09:32:22Z, `f8128b2` 09:34:01Z, `905d552` 09:44:12Z, `03d16e7` 09:50:29Z — **all 2026-09-02** | **SUPPORTED** |

### 1.2 Fixed-once and never-edited claims

| # | claim (verbatim, trimmed) | file:line | commit named | evidence from git | status |
|---|---|---|---|---|---|
| **RC16** (P8) | "The band is computed once and registered. It is **not** recomputed after seeing a calibration result, and **no bucket may be added to it afterwards.**" | `REGISTRATION.md:744-745`; restated `REGISTRATION.md:1106-1111`, `HYPOTHESES.md:153-157`, `DECISIONS.md:729-734` | none | `docs/BAND.md`: **one commit, `34307b6` 2026-08-29T19:22:44Z**, never modified. `pmexperiment/band.py`: **one commit, `9b4bd4f`**. `tests/test_band.py`: **one commit, `9b4bd4f`**. `BUCKET_EDGES_CENTS` / `EFFECT_BAND_*` unchanged since `9080186` | **SUPPORTED** |
| **RC17** (P9) | Section 13 "**it was never filled, and it is left empty permanently.** … **This prior may not be described anywhere as pre-registered**" | `REGISTRATION.md:1015-1029`; `README.md:168-175`; `DECISIONS.md:666-674`; `report.md:434-441` | none | Section 13's region hash is constant from `180c235` to HEAD; text at HEAD is still "*To be filled by the operator before the gate fires*" (`REGISTRATION.md:351-353`). `git log -S"5 to 8"` first hits `2006ae6` **2026-09-02T09:23:41Z**, the verbatim-logged Stage E prompt — after every verdict. All 12 occurrences of "pre-registered" at HEAD are negations | **SUPPORTED** |
| **RC18** (P10) | "The paragraph below **stands unedited as it was registered on 2026-08-29**, so a reader can see what the design provided for and what actually happened." | `REGISTRATION.md:636-641` | none | Section 16 changed at exactly one commit after `9080186`: `f8128b2` (2026-09-02T09:34:01Z), whose `REGISTRATION.md` diff is **117 insertions, 0 deletions**. The prepended annotation is disclosed in place | **SUPPORTED** |
| **RC19** (P11) | "Amendments append here, numbered … **Nothing above this line is edited after Section 0 is committed.**" | `REGISTRATION.md:660-661` | none | Sections **0–14 byte-identical** at all eleven post-registration commits. But **Section 15** lost its placeholder at `98ce2d4` (`-*Written only after the gate fires. Empty until then.*`) and **Section 16** gained the annotation at `f8128b2`. Both are above Section 17 | **PARTIAL** → DRAFT-P-2 |
| **RC20** (P22) | Amendment 3 — "the fee band of Amendment 2 fires **first**. The power gate fires **second**, and only over a region the band left open." | `REGISTRATION.md:765-767`; `HYPOTHESES.md:112-115`; `DECISIONS.md:158-174` | none | Definition `f686036` 18:05:26Z → firing `32dc10a` 19:24:06Z. The power gate never fired at any commit (`power.py` has one commit and no caller outside tests) | **SUPPORTED** |
| **RC21** | "`DECISIONS.md` … **the file is append-only**"; "Each section is written for the moment it landed and **is not revised afterwards**"; "`progress.md` … **append-only**" | `DECISIONS.md:200`; `report.md:3`; `README.md:217` | none | `--numstat` over full history: `DECISIONS.md` **0 deletions ever** (12 commits); `report.md` **0 deletions ever** (6 commits); `progress.md` **0 deletions** at all 18 commits after `180c235` | **SUPPORTED** |

### 1.3 Claims that rest on something the repository does not retain

| # | claim (verbatim, trimmed) | file:line | status | why |
|---|---|---|---|---|
| **RC22** (P12) | "Stage A read **11 keyless market requests** before its terms position was established … Stage C read `robots.txt` and the terms **first**, and therefore sent **zero** market-data requests." | `REGISTRATION.md:495-500`; `docs/ACCESS.md:203-206` | **UNVERIFIABLE** | No request ledger, response body or timestamped log exists at any commit. `git log --all --diff-filter=A` adds **31 files ever**, none a data artifact |
| **RC23** (P13) | "**Zero market-data requests were sent to Polymarket. Zero requests of any kind were sent in Stage E.**" | `README.md:108-109`; `REGISTRATION.md:528-531` | **UNVERIFIABLE** | An unfalsifiable negative from inside the repository. Consistent with the total absence of stored responses |
| **RC24** (P14) | "**the raw probe responses were not retained beyond this report** and the two tickers named above" | `docs/ACCESS.md:87-89` | **SUPPORTED** (as an absence) | Verified against the object store: no data artifact was ever added at any commit. The repository states the limitation itself rather than leaving it to be found |
| **RC25** (P15) | "Raw enumeration responses … are **stored untouched in `data/raw/` (gitignored, append-only)**"; Section 14: "regenerable from **the stored raw enumeration and candlestick responses under `data/raw/`**" | `REGISTRATION.md:320-321`, `:359-363` | **PARTIAL (vacuous)** | `data/raw/` does not exist; `data/` holds one 0-byte `.gitkeep` (live tree, read **2026-09-11T02:09:31Z**). Nothing was ever enumerated, so the clause is **unexercised**, not breached — but Section 14's reproducibility guarantee is therefore empty rather than satisfied |
| **RC26** (P20) | "**the Kalshi Data Terms of Use print no date at all** — `Effective` 0 occurrences, `Last Updated` 0" | `README.md:65-74`; `DECISIONS.md:435-439` | **UNVERIFIABLE** | The PDF is not retained. The *consequence* (the Kalshi claim is UNMEASURED under the repository's own procedure) is verifiable against `pmexperiment/admissibility.py` and pinned by `tests/test_admissibility.py` |
| **RC27** (P21) | "**The received date was not in the prompt and was not synthesized.** … it was asked for and supplied: **2026-09-01**." | `progress.md:1419-1420` | **PARTIAL — the checkable half SUPPORTED** | `git show 2006ae6:progress.md \| grep -c "2026-09-01"` = **0**: the string is absent from the Stage E prompt as logged verbatim before any other work. Its first appearance anywhere is `17dfebd`/`905d552` (2026-09-02). The "asked for and supplied" half is outside the repository and unverifiable |
| **RC28** (P23) | "**A floor chosen by someone else, before this repository existed, cannot have been tuned to this sample**" | `REGISTRATION.md:862-877`; ADR-011 `DECISIONS.md:323-328` | **UNVERIFIABLE** (external) | Requires that Bürgi-Deng-Whelan really use "total staked ≥ $1,000". `tests/test_registry.py:77-87` pins both the number **and** its citation sentence, which is the strongest internal guarantee available |
| **RC29** (P25) | "**Every guard here carries a test that fails when the guard is removed, verified by mutation**" and the per-stage tallies (9, 5, 5, 6, 13, 14, 2) | `README.md:231-232`; `CLAUDE.md:45-46` | **UNVERIFIABLE** | No mutation log, harness script or CI artifact exists at any commit. The tests that would be killed are present and readable; that each mutation was run is document-only. The repository records three harness faults that produced false-green runs (`progress.md:815-833, 991-997, 1232-1246`) |

### 1.4 Self-audit claims about the git objects themselves

| # | claim (verbatim, trimmed) | file:line | status | evidence |
|---|---|---|---|---|
| **RC30** (P16) | "**32 commits, 189 reachable objects**, every blob decompressed and scanned: **zero credential-shaped strings**" | `progress.md:1537-1539` | **SUPPORTED — exactly** | At `1ba50aa`, HEAD when Stage E Task 5 ran: `git rev-list --count` = **32**, `git rev-list --objects \| wc -l` = **189**. (At the anchor: 36 and 213) |
| **RC31** (P19) | "**Entry 6 states it was logged at 2026-08-29T19:32Z. That figure is wrong.** … The measured logging time is **2026-08-30T03:31Z**" | `progress.md:652-666` | **SUPPORTED** | `84f7b92` is **2026-08-30T03:31:03Z**. The repository caught its own extrapolated timestamp and the correction is right — which is the reason DRAFT-P-1 is reported as an outlier rather than as a habit |
| **RC32** (P17) | "`.env.example` … is **294 bytes**, five comment lines, and contains no `=` at all" | `progress.md:1539-1541` | **SUPPORTED** | 294 bytes in the anchored snapshot; pinned by `tests/test_honesty.py:98-100` |
| **RC33** (P18) | "`LICENSE` is MIT, **17 lines**" | `progress.md:1541-1542` | **PARTIAL** | 21 physical lines / 17 non-blank. "17 lines" is the non-blank count. Hygiene only |
| **RC34** (P24) | "`tests/test_registry.py` **pins the figures to the document**, so code and registration cannot drift apart silently" | `pmexperiment/registry.py:1-6` | **SUPPORTED**, with one note | Nine tests, each asserting a constant against a quoted `REGISTRATION.md` substring (`tests/test_registry.py:22-99`). **Note:** `FX_TURNOVER_REGISTERED` is the one `registry.py` constant *not* pinned in that file; it is pinned by value at `tests/test_band.py:182-184` and to its document sentence at `tests/test_honesty.py:218-223`. The guarantee holds across the suite, not within the one file the sentence names |

---

## 2. Parameter changes after data existed

### 2.1 When did data exist?

Two clocks, because the repository has two kinds:

- **D1 — access measurement.** The first HTTP probe of Kalshi, placed by the document at
  "~07:44Z" on 2026-08-29 (`progress.md:58-59`, uncorroborated). The first *committed* record
  of a measurement is `docs/ACCESS.md`, added in `98ce2d4` at **2026-08-29T07:53:10Z**. That
  commit is the earliest object-anchored proof that measured data existed.
- **D2 — a statistic relating a price to an outcome.** **Never.** No contract was ever
  enumerated, no bucket built, no calibration computed; the power gate never fired on any
  venue. `git log --all --diff-filter=A --name-only` adds 31 files across the whole history and
  **not one is a data artifact**; `data/` holds a single 0-byte `.gitkeep`.

So every change below is "after data existed" in the D1 sense and "before data existed" in the
D2 sense. Both readings are given per row.

### 2.2 The table

`registry.py` was never edited destructively — the two rows marked **(additive)** append a new
constant and change nothing existing.

| # | parameter / bar / rule changed | commit (UTC) | after D1? | after D2? | dated amendment recording it | date correct against git? | finding? |
|---|---|---|---|---|---|---|---|
| **PC1** | **Measurement universe moves Kalshi → Polymarket** (Section 1's source) | `f686036` **2026-08-29T18:05:26Z** | **yes** — after `98ce2d4` 07:53:10Z | no | **yes** — Amendment 1 `REGISTRATION.md:665-703`, ADR-006(2nd) `DECISIONS.md:138-154`; reason given, and the Kalshi data that existed is named ("Kalshi's PENDING_ACCESS verdict of 2026-08-29 stands") | **NO — stamped 2026-08-30** | **DRAFT-P-1** |
| **PC2** | **A new gate inserted ahead of the power gate** (the fee-versus-edge band, with its three verdicts and the 2.0 / 4.0-point break-even) | `f686036` **2026-08-29T18:05:26Z** | **yes** | no | **yes** — Amendment 2 `REGISTRATION.md:705-747`, ADR-007(2nd) `DECISIONS.md:158-174` | **NO — stamped 2026-08-30**, which is *after* the date the document gives for the gate's own firing (`docs/BAND.md:3`, `HYPOTHESES.md:119`) | **DRAFT-P-1** |
| **PC3** | **Scope: measurement-only → a terminal question that admits a trading decision** | `f686036` **2026-08-29T18:05:26Z** | **yes** | no | **yes** — Amendment 3 `REGISTRATION.md:749-779`, ADR-008 `DECISIONS.md:178-194` | **NO — stamped 2026-08-30** | **DRAFT-P-1** |
| **PC4** | **`FX_TURNOVER_REGISTERED = 1.0`** — the FX turnover k that binds the cost floor **(additive)** | code `9b4bd4f` **19:15:55Z**; text `4d75f66` **19:17:21Z** | yes | no | **yes** — Amendment 4 `REGISTRATION.md:781-849`, ADR-010 `DECISIONS.md:274-307`, which **discloses the 86-second code-before-text lag itself** | **yes** | no |
| **PC5** | **`PERMITTED_MIN_VOLUME_USD = 1000.0`** — the permitted-subset volume floor **(additive)** | `f789079` **2026-08-30T03:34:00Z** | yes | no | **yes** — Amendment 5 `REGISTRATION.md:851-911`, ADR-011 `DECISIONS.md:311-341`. Names the data that existed and the exposure: "Stage A's Task 2 never armed, so the floor was never filled in, and Entry 5 records that this is exactly why Amendment 2's BAND-NARROW row could not be evaluated in Stage B"; ADR-011 adds "it is being set by the same session that will go on to read that count" | **yes** | no — see note (a) |
| **PC6** | **Amendment 1's premise retracted** — the ground on which the venue moved | `1b3124e` **2026-08-30T03:40:52Z** | yes | no | **yes** — Amendment 6 `REGISTRATION.md:912-1009`, ADR-012 `DECISIONS.md:344-390` | **yes** | no |
| **PC7** | **New admissibility bars: `MIN_DOCUMENT_TEXT_RATIO = 0.05` and `REQUIRED_ELEMENTS = ("clause","effective_date","fetch_date")`** | `b67fc84` **2026-08-30T04:28:05Z** | **yes — and calibrated on data** | no | **yes** — ADR-012 `DECISIONS.md:344-390` (03:45:12Z) fixes the three elements; the 5 % ratio and its derivation are recorded at `pmexperiment/admissibility.py:39-49` and `docs/LICENCES.md:56-83` | **yes** | no — see note (b) |
| **PC8** | **`GATE_MODULES` widened** — `("power.py",)` → `+ band.py` → `+ admissibility.py` | `9b4bd4f` 19:15:55Z; `b67fc84` 04:28:05Z | yes | no | in-code rationale at `tests/test_guards.py:19-27`; Stage entries in `progress.md` | n/a | no — the guard's scope only ever **widened** |
| **PC9** | **Amendment 7** — the entity path declined by operator decision | `fe7e6b9` **2026-09-02T09:32:22Z** | yes | no | **yes** — `REGISTRATION.md:1009-1071`, ADR-017 `DECISIONS.md:633` | **yes** | no |
| **PC10** | **Amendment 8** — closure, and the three reopening conditions | `f8128b2` **2026-09-02T09:34:01Z** | yes | no | **yes** — `REGISTRATION.md:1071-1120`, ADR-018 `DECISIONS.md:686` | **yes** | no |
| **PC11** | **Amendment 9** — trading access is not data permission; a fourth reopening row | `03d16e7` **2026-09-02T09:50:29Z** | yes | no | **yes** — `REGISTRATION.md:1120-1174`, ADR-019/020/021 `DECISIONS.md:750, 771, 787` | **yes** | no |
| **PC12** | **Section 16 annotated at closure** (a prepended qualifier above the registered paragraph) | `f8128b2` **2026-09-02T09:34:01Z** | yes | no | **disclosed in place**, `REGISTRATION.md:636-641`; 0 deletions in the diff | **yes** | no |
| **PC13** | **Section 15 placeholder replaced by results** (first at `98ce2d4`, then appended five times) | `98ce2d4` **07:53:10Z** onward | yes | no | design-provided: the section header itself reads "*Written only after a gate fires*" (`REGISTRATION.md:369`) | n/a | contributes to **DRAFT-P-2** |
| **PC14** | **`tests/test_honesty.py` edits with deletions** (`98ce2d4`, `baa2bf3`, `905d552`) | various | yes | no | — | n/a | no — inspected line by line: a test rename, two `ruff` re-wraps, and the scaffold's deliberately inverted `test_registration_is_not_yet_registered`, whose own docstring says "Stage A Task 0 removes the banner in the same commit that registers Section 0, and this test is replaced then". **No pin was weakened** |

**(a) On PC5.** The floor was registered **after** the band verdict fired (`32dc10a`
2026-08-29T19:24:06Z → `f789079` 2026-08-30T03:34:00Z), and the band verdict had recorded the
floor's *absence* as its reason for not firing BAND-NARROW ("the volume clause cannot be
evaluated because no floor was ever registered", `docs/BAND.md:287`, `REGISTRATION.md:417`). The
band was not recomputed afterwards, which is what Amendment 2 requires. Amendment 5 names this
sequence explicitly and ADR-011 names the conflict of interest explicitly. Recorded here so the
sequence is on the table; **it is not a finding**, because the change carries a dated amendment
with its reason and with the data that existed, exactly as the rule requires.

**(b) On PC7.** `MIN_DOCUMENT_TEXT_RATIO = 0.05` is a bar **calibrated on the single
measurement it was derived from** — Polymarket's `tos` shell at 0.65 % text, measured in Stage C
before `1b3124e` — and then applied to the Stage D licence candidates and retroactively to this
repository's own Stage A Kalshi claim. Two things make it clean: the bar was fixed at
`b67fc84` **04:28:05Z**, before the candidate documents were read and judged at `7b5a751`
**06:22:49Z**; and its derivation, its direction of error and its method-dependence are all
disclosed by the authors at `pmexperiment/admissibility.py:39-49` and `docs/LICENCES.md:76-83`
("A limitation of the text-ratio bar, found by using it"). Its retroactive application convicts
the repository's own earlier claim, which is the honest direction. **Not a finding**; recorded
because the task asks for every bar fixed after data existed.

---

## 3. Draft findings

### DRAFT-P-1
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the dating of Amendments 1–3, ADR-006(2nd)/ADR-007(2nd)/ADR-008,
  the `HYPOTHESES.md` venue-split amendment and `progress.md` Entry 3 — the registration record
  for the fee-versus-edge band gate that produced the repository's only verdict
- **Direction:** neutral — the git objects establish the ordering the repository claims; what is
  wrong is the record of *when*, not the sequence. Read from the documents alone, however, the
  error runs in direction B: Amendment 2 appears to have been made the day **after** the gate it
  defines fired
- **Class:** PROVENANCE
- **Severity:** S2 — a stated date label contradicts the git object that carries it, and that
  date is the repository's own registered disambiguator for two duplicated ADR numbers
- **Label:** DERIVED (git objects)
- **Claim challenged (verbatim quote):**
  - "**Made 2026-08-30, before any statistic relating a price to an outcome exists.**" — PMExperiment/REGISTRATION.md:667
  - "**Made 2026-08-30.** A new gate, ordered ahead of the power gate, because it is free and may be decisive on its own." — PMExperiment/REGISTRATION.md:707
  - "**Made 2026-08-30.** A deliberate scope change, recorded rather than allowed to drift." — PMExperiment/REGISTRATION.md:751
  - "**Status:** accepted, 2026-08-30." — PMExperiment/DECISIONS.md:140, :160, :180
  - "## Amended **2026-08-30** — the venue split, and what H1 now means" — PMExperiment/HYPOTHESES.md:87
  - "## Entry 3 — amendments 1 to 3: venue, fee band, scope — **2026-08-30**" — PMExperiment/progress.md:202
  - "the pair dated 2026-08-29 (PENDING_ACCESS; the withheld rate-limit measurement) and the pair **dated 2026-08-30** (Polymarket; the fee band ordering) … **Cite an ambiguous number with its date.**" — PMExperiment/DECISIONS.md:197-204
- **Evidence:**
  - All seven stamps land in **one commit**. `git show f686036 --stat` (read 2026-09-11T02:03Z):
    `DECISIONS.md | 57 +`, `HYPOTHESES.md | 32 +`, `REGISTRATION.md | 116 +-`,
    `progress.md | 44 +`, `tests/test_honesty.py | 37 +` — 5 files, 285 insertions, 1 deletion.
  - `git log -1 --format=%ad%n%cd --date=iso-strict f686036` → author **`2026-08-29T11:05:26-07:00`**,
    committer **`2026-08-29T11:05:26-07:00`** = **2026-08-29T18:05:26Z**. The stamps read
    2026-08-30. **The mismatch survives both conventions**: 2026-08-29 in UTC and 2026-08-29 in
    the repository's own `-07:00` local time.
  - **The repository's convention is UTC**, and it is applied correctly everywhere else:
    `f789079` (20:34:00 −07:00 = 2026-08-30T03:34:00Z) is stamped 2026-08-30 and matches;
    `1b3124e` (03:40:52Z) matches; `84f7b92` (03:31:03Z) matches; `4d75f66` (2026-08-29T19:17:21Z)
    is stamped 2026-08-29 and matches.
  - **It is an isolated outlier, not a habit.** Machine-mapping every `## ADR-nnn.` heading to
    the commit that introduced it (script at
    `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov/adrs.py`, run
    2026-09-11T02:05Z) gives **23 ADR entries**; **20 of 23 match their commit's UTC date
    exactly** and the three that do not are precisely ADR-006(2nd), ADR-007(2nd) and ADR-008 in
    `f686036`. Likewise **six of seven** `Made <date>` amendment stamps and **four of five**
    `HYPOTHESES.md` amendment headers match.
  - **The error is internally visible.** The next `progress.md` entry, Entry 4, records
    "**Logged 2026-08-29T19:08Z**" (PMExperiment/progress.md:248-249; commit `e2d8f10` at
    2026-08-29T19:07:37Z — correct), so Entry 3 is stamped **a day later** than the entry that
    follows it 62 minutes afterwards.
  - **Three consequences the wrong date actually has, all of which git resolves in the
    repository's favour:**
    1. Amendment 4 is stamped "Made **2026-08-29**" (PMExperiment/REGISTRATION.md:783) while the
       Amendment 2 it operates under is stamped 2026-08-30 — an amendment apparently predating
       the amendment it depends on. Git: `f686036` 18:05:26Z → `4d75f66` 19:17:21Z, correct order.
    2. Amendment 2 (stamped 2026-08-30) defines the gate the repository says fired on
       **2026-08-29** — "Written by Stage B on 2026-08-29" (PMExperiment/docs/BAND.md:3), "The
       band gate, fired 2026-08-29: BAND-OPEN" (PMExperiment/HYPOTHESES.md:125), "after the band
       gate fired on 2026-08-29" (PMExperiment/REGISTRATION.md:1011). On the documents' own
       dates the gate fired the day before its registering amendment. Git: `f686036` 18:05:26Z →
       `34307b6` 19:22:44Z → `32dc10a` 19:24:06Z — **1 h 19 min of genuine pre-registration.**
    3. `DECISIONS.md:203` registers "**Cite an ambiguous number with its date**" as the sole
       disambiguator for the duplicated ADR-006/ADR-007 pairs. Against the objects **both pairs
       are 2026-08-29** (`98ce2d4` 07:53:10Z and `f686036` 18:05:26Z), so the registered
       disambiguator does not disambiguate. (No document in the repository actually cites
       "ADR-00n, 2026-08-30"; the four date-qualified citations that exist —
       PMExperiment/docs/BAND.md:113, :287, PMExperiment/REGISTRATION.md:417,
       PMExperiment/docs/ACCESS.md:197 — all name the 2026-08-29 pair and all resolve correctly.)
  - **The repository holds itself to the opposite standard**, which is why this is reportable
    rather than trivial: "**a timestamp inferred from a previous timestamp is documented, not
    measured**" (PMExperiment/progress.md:662-663), written when it caught and corrected an
    extrapolated timestamp in Entry 6 — a correction this audit confirms is right (`84f7b92` =
    2026-08-30T03:31:03Z).
- **Recomputation (if any):** none required — this is a direct comparison of document text
  (snapshot `snap/PMExperiment/`, lines cited above) against commit metadata
  (`git log -1 --format=%ad %cd --date=iso-strict`, and `TZ=UTC … --date=iso-strict-local`),
  read 2026-09-11T02:03Z–02:06Z. Full ADR→commit map produced by
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov/adrs.py`.
- **What would resolve it:** a dated erratum in `progress.md` (the repository's established
  mechanism — Entry 6.1 is exactly this) recording that the seven stamps carried by `f686036`
  read 2026-08-30 where the commit is 2026-08-29T18:05:26Z, that the substantive ordering is
  unaffected, and that the ADR-006/ADR-007 disambiguation-by-date at `DECISIONS.md:203` must be
  read as "the second pair, commit `f686036`" rather than as a date.
- **Confidence:** HIGH — seven stamps, one commit, author date == committer date, and the
  mismatch holds in UTC and in local `-07:00` alike.
- **Invalidated by later commits?:** no at the anchored SHA, which is also live `HEAD`
  (`03d16e7`, 2026-09-02) and the project is closed. A later erratum commit would resolve it
  without changing what the anchored tree says.
- **Disclosed by authors?:** **no.** The repository audits its own timestamps elsewhere —
  Entry 6.1 (PMExperiment/progress.md:652-666) corrects an extrapolated one, and
  `progress.md:511-515` records the ADR numbering collision arising from "the 2026-08-29 and
  **2026-08-30** sessions" — but that sentence repeats the wrong date rather than catching it,
  and no entry, amendment or ADR anywhere records that `f686036`'s stamps disagree with the
  commit.

### DRAFT-P-2
- **Repository / SHA:** PMExperiment / `03d16e71dbf25a86c529884662d02136f8e82334`
- **Hypothesis or artifact:** the immutability guarantee written at the head of Section 17
- **Direction:** neutral — pure hygiene; the substantive guarantee (no registered bar,
  parameter, outcome map, prior or decision rule changed) verifies exactly
- **Class:** PROVENANCE
- **Severity:** S4 — hygiene. Both edits are provided for by the design and one is explicitly
  disclosed in place, so this is capped low by the disclosure rule
- **Label:** DERIVED (git diffs)
- **Claim challenged (verbatim quote):** "Amendments append here, numbered, each carrying its own
  evidence and the date it was made. **Nothing above this line is edited after Section 0 is
  committed.**" — PMExperiment/REGISTRATION.md:660-661
- **Evidence:**
  - **The substance verifies.** Sections 0–14 are **byte-identical at all eleven commits that
    touched `REGISTRATION.md` after `9080186`** — region SHA-256 constant across
    `98ce2d4, f686036, 4d75f66, 32dc10a, f789079, 1b3124e, 17dfebd, fe7e6b9, f8128b2, 03d16e7`
    (recomputed independently at
    `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov/sections.py`, run
    2026-09-11T02:04Z; region length 16,640 bytes at every one of them).
  - **Two regions above Section 17 did change.** `git show 98ce2d4 -- REGISTRATION.md`:
    `@@ -366,7 +366,38 @@` … `-*Written only after the gate fires. Empty until then.*` — the
    Section 15 placeholder, replaced by Stage A's result. `git show f8128b2 -- REGISTRATION.md`:
    `@@ -570,8 +570,76 @@` adds Section 15.5 and the Section 16 annotation (117 insertions,
    **0 deletions**). Section 15 and Section 16 both sit above the Section 17 header.
  - The only other deletion above Section 17 in the whole history is `f686036`'s
    `-*(empty)*` — the Section 17 body placeholder itself.
- **Recomputation (if any):** section-region hashing of `git show <c>:REGISTRATION.md` at each of
  the 13 commits that touch the file; script and output in
  `/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov/sections.py`.
- **What would resolve it:** narrowing the sentence to what the design means and what the objects
  show — e.g. "Nothing in Sections 0–14 is edited after Section 0 is committed; Section 15 is
  written as gates fire and Section 16 may be annotated at closure."
- **Confidence:** HIGH — two diff hunks, quoted above, against a sentence with no qualifier.
- **Invalidated by later commits?:** no; `03d16e7` is the anchor and live HEAD, and the project
  is closed.
- **Disclosed by authors?:** **yes, for both edits.** Section 15's header reads "*Written only
  after a gate fires*" (PMExperiment/REGISTRATION.md:369) and the Section 16 annotation announces
  itself in its own first words — "**Recorded 2026-09-02 at closure, before the paragraph it
  qualifies**" (PMExperiment/REGISTRATION.md:636-641). This is an over-broad sentence, not a
  concealed edit, and it is reported at S4 for that reason.

---

## 4. What could not be checked, and why

| what | why it cannot be settled from here |
|---|---|
| **The time of the first HTTP request (~07:44Z, `progress.md:58-59`)** | No probe response was retained at any commit (`docs/ACCESS.md:87-89`). Git fixes the Section-0 commit at 2026-08-29T07:37:33Z and the first committed measurement at 07:53:10Z, so the *recording* of measurement demonstrably follows registration — but git cannot exclude an HTTP request made before 07:37:33Z. Nothing contradicts the claim; nothing independent corroborates it |
| **Request ordering and counts in Stages A, C, E** (11 keyless reads before the terms position; zero Polymarket market-data requests; zero Stage E requests) | Standing rule 6 promises "ledgers are append-only and fsynced"; **no ledger file exists at any commit and none exists in the working tree**. These are unfalsifiable negatives from inside the repository |
| **The Kalshi Data Terms PDF occurrence counts** (`Effective` 0, `Last Updated` 0) | The instrument is not retained. Only the consequence — that the claim is UNMEASURED under `pmexperiment/admissibility.py` — is checkable, and it checks out |
| **The Kalshi desk correspondence of 2026-09-01** | Not in the repository; `docs/ACCESS.md:285-289` and ADR-016 say so ("the operator's summary of the reply, not its text"). The one checkable half — that the received date was not in the Stage E prompt — **verifies** (0 occurrences in `2006ae6:progress.md`) |
| **The mutation tallies (9, 5, 5, 6, 13, 14, 2) and "verified by mutation"** | No harness, log or CI artifact at any commit. The tests that would be killed are present and readable; that each mutation was run and killed is document-only. The repository itself records three harness faults that produced false-green runs |
| **Bürgi-Deng-Whelan's "total staked ≥ $1,000" filter** (the source of `PERMITTED_MIN_VOLUME_USD`) | External publication, outside this audit's reach. `tests/test_registry.py:77-87` pins the number *and* the citation sentence together, which is the strongest internal guarantee available |
| **Section 14's reproducibility guarantee** | Not falsifiable and not satisfiable: `data/raw/` never existed because nothing was ever enumerated. Recorded as **vacuous**, not as breached |

---

## 5. Live-repository access log

**Purpose of access:** git history and objects for provenance (§1–§3), plus one `ls -la` of the
working tree and `data/` to establish that no data artifact exists outside git.

**No repository file was opened for writing. No git state-changing command was run. No
repository script was executed.** Every document quotation is from the anchored snapshot
`/home/kiros-li/.cache/program-audit/scratchpad/snap/PMExperiment/`. Commands used against the
live repository, all read-only: `git status --porcelain`, `git rev-parse`, `git rev-list
--count`, `git rev-list --objects`, `git log` (`--all`, `--follow -p`, `-S`, `--numstat`,
`--name-status`, `--diff-filter=A`, `--format`, `--date=iso-strict` / `iso-strict-local`),
`git show` (`--stat`, `<commit>:<path>`, `-- <path>`), `git branch -a`, `git tag`, `ls -la`,
`cat .git/info/exclude`.

Scratch scripts and outputs were written **only** to
`/home/kiros-li/.cache/program-audit/scratchpad/work/agentC-pm-prov/`
(`sections.py`, `adrs.py`).

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` BEFORE first access
— 2026-09-11T02:02:14Z:**

```
```

(empty — the command produced no output; exit status 0)

**`git -C /home/kiros-li/Documents/GitHub/PMExperiment status --porcelain` AFTER last access
— 2026-09-11T02:10:54Z:**

```
```

(empty — the command produced no output; exit status 0)

**Both outputs are empty and identical. Nothing was modified.**

The working tree carries one untracked file, `_CLOSED_DO_NOT_RUN_HERE` (747 bytes, dated
2026-09-02 22:38 local), which does not appear in `status` because `.git/info/exclude` lists it
(verified by reading that file). **This is pre-existing operator dirt, not mine** — it predates
this access by nine days and was already reported in the LOCATE pass on 2026-09-05. It is
reported again here per the common rules' instruction to report any working-tree entry beyond
the listed pre-existing exceptions. The tree also carries `.venv/`, `.mypy_cache/`,
`.pytest_cache/` and `.ruff_cache/`, all gitignored and all dated 2026-08-29 — untouched by this
audit.

**Unanchored reads.** One: `ls -la` of `/home/kiros-li/Documents/GitHub/PMExperiment/data/` and
of the repository root, read **2026-09-11T02:09:31Z**. `data/` holds exactly one entry, a 0-byte
`.gitkeep` dated 2026-08-29 00:07 local. There is no `data/raw/`. This is a working-tree
observation and could in principle have changed after the anchor; the git history independently
shows no data artifact was ever tracked.
