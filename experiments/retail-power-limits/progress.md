# Progress

Append-only. Newest at top. Each stage states its ETA before it starts and its
actual after it finishes.

---

## S.1. The note, written and shipped. 2026-08-29

**ETAs stated before work began**, per task, in the order the prompt fixes:
reading pass 12 minutes; evidence extraction 8; progression 5; contrast cases 5;
the note 12; the artifact, gates and git 18. Stated total 50 to 60 minutes of
tool time.

**Actual.** The scaffold was created at 00:07:32 and the gates ran green at 00:18,
so the build half came in a little over its 30-minute estimate. The reading pass
that preceded it is **not timestamped in this repository** and its actual is
therefore not claimed — recorded as unmeasured rather than estimated after the
fact, which is the same rule the sibling repositories apply to a figure nobody
wrote down at the time.

**Prompt logged before work began, as instructed.** The governing instruction
named seven repositories to read in full and read-only, five tasks, and a
standing rule: *do not paraphrase a number you have not read; if a figure named
here is not in the repo, say so and correct it.* That rule produced the four
corrections in ADR-003 and is the reason the note carries a correction section
at all.

### What was read

Read-only, nothing modified in any sibling repository. No sibling repository was
written to, and this repository imports nothing from them at runtime — the
figures are transcribed, not loaded, so a stale sibling checkout cannot change
what this note says.

| repository | read | role |
|---|---|---|
| NPDExperiment | REGISTRATION.md, progress.md, DECISIONS.md, closing commit | power case |
| InsiderExperiment | REGISTRATION.md Sections 0 and 17, DECISIONS.md, closing commit | power case |
| ETFExperiment | REGISTRATION.md, README.md, both closing commits | power case |
| HFExperiment | REGISTRATION.md, closure entry, progress.md, README.md | power case, inherited |
| AiTrader | RETURN.md, PROGRESS.md, round commit `a0a9ef6` | HFExperiment's inherited resolution |
| MLCryptoEngine | HYPOTHESES.md, the H1 capturability note | contrast case |
| solattn | REGISTRATION.md and its Stage B entry, FINDINGS.md | contrast case |
| solclear | FINDINGS.md | contrast case |

AiTrader was not on the reading list. It was opened because HFExperiment's
README attributes its own power resolution to the AiTrader round of 2026-07-26,
and a case carried on an attribution needs the attributed record read rather
than trusted. That is the only addition to the list.

### What was built

- `docs/the-power-limit.md`, the note, for a reader outside this program.
- `SOURCES.md`, every figure mapped to repository, file and commit, plus the two
  `git` commands that check one.
- `rplimits/`, the sourced figures as frozen data and the renderers for the
  generated blocks. No data, no statistic, no network.
- `tests/`, 111 tests: source-registry integrity, case integrity, drift between
  prose and data, the honesty pins, and a credential scan. Every detector has a
  canary asserting it fires.
- `DECISIONS.md`, six ADRs, of which ADR-001 is the required record of why this
  lives in its own repository.

### The gates

`make lint`, `make typecheck` and `make test` all green. Ruff format and check
clean, mypy strict clean over 11 source files, 111 tests passing.

### Two defects found while building, both fixed

**The block-sync tool reported work it had not done.** `write_blocks` used
`re.sub`, which returns the input unchanged when nothing matches, so the first
run announced that it had rewritten four blocks while writing none of them. The
markers were empty at that point and the pattern required a newline the empty
form did not have. The drift test caught it, which is the only reason it was
seen. `write_blocks` now uses `subn` and raises unless a block matches exactly
once. **A sync tool that can report on work it did not do is worse than no sync
tool**, because everything downstream then compares against a document nobody
wrote — the InsiderExperiment ADR-012 shape, one layer over.

**`blocks_in` matched nothing, silently.** It built its pattern by escaping a
null byte and substituting on the escaped form, and `re.escape` does not escape
null bytes, so the substitution never fired and the finder returned an empty
list. An empty list made the parametrized drift test collect zero cases and
report a **skip**, not a failure. Two tests were added first — one asserting the
case list is non-empty, one asserting every renderer is used by some document —
and both then failed honestly. The pattern is now a plain literal.

Both defects have the same shape and it is worth naming: **a check that cannot
fail passes, and reads exactly like a check that passed.**

### One finding about the artifact itself

Checked at push time rather than assumed: **four of the seven source
repositories have no remote.** NPDExperiment, InsiderExperiment, ETFExperiment
and HFExperiment are local-only. The three contrast cases and AiTrader are
public on GitHub.

That is the awkward direction. The evidence bounding the claim is independently
checkable; the evidence the claim rests on is not. It is disclosed in
`SOURCES.md` with a per-repository table and in the note's own scope section,
rather than left for a reader to discover by trying a clone that fails. The
recorded commit hashes still bind: if those four are ever published, every
citation resolves against them without amendment.

**This does not block the note and it is not repaired by anything in this
repository.** Publishing the four is an operator decision, and it is outside
this repository's boundary in exactly the way ADR-001 describes.

### Scope, restated at the close

This repository holds no market data, opens no data source, computes no
statistic, and makes no claim about any market. Its claim is about
detectability at retail scale, on four cases, and the scope-limit sentence is
pinned in two documents so it cannot be trimmed later. Three contrast cases are
carried for the same reason: the four power closures must not be read as though
every negative in this program were a power negative.

### Outstanding

None inside the repository. The four sibling experiments remain closed and were
not touched.
