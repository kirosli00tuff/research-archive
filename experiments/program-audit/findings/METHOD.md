# METHOD — how this audit was run

Status: DRAFT written during Phase 1 (2026-09-03 04:50Z). Sections marked `[AT FREEZE]` are
completed immediately before the `findings-frozen` tag and not edited afterwards.

## 1. Object and scope

Thirteen repositories under `/home/kiros-li/Documents/GitHub/` were audited at the commits recorded
in `findings/ANCHOR.md`: AiTrader, ETFExperiment, HFExperiment, InsiderExperiment, MLCryptoEngine,
NPDExperiment, NPLExperiment, ORBExperiment, PMExperiment, VRPExperiment, retail-power-limits,
solattn, solclear. Three repositories present on disk were excluded by operator instruction and never
read: [personal repo, name removed], solcopy and MBTExperiment (the last added on 2026-09-03 06:37Z, during Agent A
run 6; the rules already excluded everything outside the thirteen, so no agent had read it).

Every finding is a claim about the anchored state. Each carries the anchored SHA and a statement of
whether later commits could invalidate it. PMExperiment was re-anchored once, before any agent read
it, because a concurrent session closed the project between the first anchor (2006ae6) and the first
read; the audited state is rev1 (03d16e7). The rationale is in ANCHOR.md.

## 2. The read-only rule and how it was enforced

The audited repositories were never modified. Enforcement had four layers:

1. **Snapshots.** Every repository was exported at its anchored SHA with `git archive` into a
   read-only tree (`chmod -R a-w`). Agents read tracked content from the snapshot, whose paths and
   line numbers equal `git show <SHA>:<path>`. The snapshots were rebuilt twice after host reboots
   cleared /tmp; each rebuild used the same SHAs and reproduced identical file counts
   (413/109/98/73/292/75/147/157/32/47/21/99/55).
2. **Live access limited to two purposes.** Git history (`log|show|diff|blame|rev-parse|ls-tree|
   cat-file`) and untracked working-tree data (opened read-only, labelled UNANCHORED with the UTC
   read time). Never `.env`, keystores, sessions, credentials.
3. **Cleanliness checks.** `tools/git_status_check.sh <label>` records HEAD, branch and
   `git status --porcelain` for all thirteen repositories before and after every run, appending to
   `provenance/git-status-checks.log`. Agents were additionally instructed to record porcelain
   output before and after any live access of their own. Pre-existing dirt that predates the audit:
   AiTrader ` M COLLECTION_LOG.md` (a collector appends to it) and four stray untracked files in
   HFExperiment (`Accept:`, `GET`, `Host:`, `User-Agent:`). Any other entry would be reported, not
   reverted.
4. **Computation in a separate environment.** Recomputations used a dedicated Python 3.12 venv
   (numpy, scipy, pandas, statsmodels, pyarrow) with scratch files only under the audit's work
   directory. Repository scripts were never executed in place.

The full text given to every agent is `findings/protocol/COMMON_RULES.md`.

## 3. Agents and theses

| Agent | Thesis / role | Output |
|---|---|---|
| A | The program closed hypotheses too early or too hard (Direction A). | `findings/agentA/` |
| B | The program claimed too much: positives, blockers, figures not supported by evidence (Direction B). | `findings/agentB/` |
| C | Referee. Independent verification of the highest-severity numeric claims per repository against code, data and git objects; provenance checks; then adjudication of every A and B finding. | `findings/agentC/` |
| D | Forward proposals only, after the findings are frozen; authored no finding. | `proposals/` |

### 3.1 Per-repository chain (A and B)

Each repository was processed by a chain of sub-agents, each with a fresh context:

1. **Readers** (Fable). One reader per document group (large repositories were split into two or
   three parts, e.g. registration / decisions / progress). Each reader writes draft findings and a
   reopen (A) or positives (B) ledger under `_drafts/<repo>/`.
2. **Consolidator** (Opus). Merges the drafts into `<repo>.md`, `<repo>.json` and the ledger,
   assigns IDs `AUDIT-<AGENT>-<REPO>-<n>`, removes duplicates, and records cross-repo leads.
3. **Two verifiers** (Opus). Verifier 1 checks citation fidelity: every quoted claim exists at the
   cited file and line in the snapshot. Verifier 2 checks disclosure and labelling: DERIVED vs READ,
   the disclosed-limitation rule, severity caps.
4. **Applier** (Opus). Applies the verifiers' verdicts to the md/json, adds a "Citation check" line
   per finding, and lists anything dropped under "Dropped after verification".
5. **Cross-repo pass** (Fable), after all thirteen chains: findings that only appear when two
   repositories are read together, with IDs continuing each target repository's sequence.

### 3.2 Agent C chain

Per repository: **locate** (Opus; inventory of numeric claims with their sources) → **verify**
(Fable; recompute at least the three highest-severity numeric claims from code, data or git
objects; status VERIFIED / CONTRADICTED / UNVERIFIABLE; CI estimator and independence; test tail,
degrees of freedom, multiplicity correction versus the registered rule) in parallel with
**provenance** (Fable; `git show` against stated commits; SUPPORTED / NOT_SUPPORTED / PARTIAL /
UNVERIFIABLE) → **consolidate** (Opus) → **check** and **apply** (Opus). Only after C's blind
output and seeded checks were committed did C read A and B: **rule-A** and **rule-B** (Fable) per
repository, then **reconcile** (Fable) into `adjudication/<repo>.md/.json` with one of UPHELD /
UPHELD_WITH_CORRECTION / NOT_UPHELD / UNRESOLVABLE_ON_AVAILABLE_EVIDENCE per A/B finding.

### 3.3 Seeded checks

After each agent's blind pass was committed, the same agent ran six seeded checks in its own
`seeded/` subdirectory, never backfilled into the blind output: (1) multiplicity as conjunction
versus union with corrected power; (2) co-primary endpoint coupling across at least six cells at
the 1e-3 threshold; (3) CI half-width · √n / σ ≈ 1.96 as a flat-normal signature, with clustered or
block recomputation; (4) carried versus measured figures; (5) calibration priors, ledger and
scoring; (6) cross-repo propagation and figure concordance. IDs use n = 100·k + i for check k.

### 3.4 Finding format

ID; repository and SHA; hypothesis or artifact; direction; class ∈ {OVER_CLOSED, UNDER_CLOSED,
UNSUPPORTED_POSITIVE, ARITHMETIC, STATISTICAL, INTERNAL_INCONSISTENCY, CROSS_REPO_INCONSISTENCY,
STALE_FIGURE, PROVENANCE, PROCESS}; severity S1–S4; the challenged claim quoted verbatim with file
and line; evidence with figures and n; what would resolve it; confidence; DERIVED or READ; whether
later commits could invalidate it; whether the authors disclosed the limitation. A limitation the
authors disclosed is READ, capped at S3, and must say so. Agents report where they found nothing.
`tools/build_index.py` validates every `<repo>.json` against these fields and builds a
severity-ranked INDEX.md.

## 4. Model policy

Operator instruction (2026-09-03 00:45Z): Fable for all analysis; Opus where the task is
mechanical and needs little reasoning. Readers, the cross-repo pass, C's verification and
provenance, seeded checks, adjudication and D's reasoning ran on Fable. Consolidators, verifiers,
appliers, C's locate/consolidate/check/apply, seeded triage, the check-3 merge and D's per-repo
constraint extraction ran on Opus. The full mapping is `findings/protocol/MODEL_POLICY.md`. The
two batch-1 Agent A readers had already completed on Fable before the instruction; every
mechanical agent after it ran on Opus.

## 5. Independence protocol

- Each sub-agent starts with a fresh context and receives only COMMON_RULES.md, its task, the
  snapshot paths and (where the chain requires it) files under its own agent's output directory.
- Agents are forbidden to read any other agent's directory, `findings/independent/` (reserved for a
  later audit by a different model; nothing was created, read or written there), and any excluded
  repository.
- Order and commits: A blind → commit → A seeded → commit → B blind → commit → B seeded → commit →
  C blind → commit → C seeded → commit → C adjudication (first time C reads A and B) → commit →
  SUMMARY.md + METHOD.md → commit + tag `findings-frozen` → D. D reads only frozen findings.
- The orchestrator (this session) wrote no finding. It authored prompts, ran cleanliness checks,
  committed outputs and wrote SUMMARY.md and METHOD.md from the agents' files.
- Leak audit `[AT FREEZE]`: every sub-agent transcript under the workflow directories is grepped
  for reads of other agents' directories (`findings/agentA`, `findings/agentB`, `findings/agentC`,
  `work/agent<X>-`) by agents not entitled to them. Results are listed in §8.

Known, unavoidable dependencies: agents B and C ran after A's files existed on disk. The
prohibition was by instruction plus the transcript grep, not by filesystem isolation.

## 6. Infrastructure and run history

The dominant operational constraint was the account usage limit, which kills every in-flight
sub-agent at once. Detailed timeline in `provenance/RUN_LOG.md`; summary:

- Agent A runs 1 and 2 (2026-09-02, 37 sub-agents at full parallelism) died on the limit with
  nothing banked.
- From run 3 the workflows were throttled to two repositories at a time, smallest first, so
  completed sub-agents are cached by the workflow runtime and a resume re-runs only failures.
- The host rebooted twice on 2026-09-03 (≈00:26Z and ≈02:14Z), clearing /tmp and the snapshots,
  venv and batch-1 scratch scripts. From 04:47Z the scratchpad path is a symlink to a persistent
  directory. The two lost scratch scripts (`agentA-rpl-consolidate/verify.py`,
  `agentA-HFExperiment/recompute.py`) are named in the retail-power-limits and HFExperiment
  findings; their outputs are quoted in the finding text, but the scripts themselves cannot be
  re-inspected. Later scratch work is committed under `work/`.
- Run 3 was stopped and resumed once to apply the model policy; the cached Fable readers were
  kept.
- The workflow runtime's resume cache turned out to be positional (it replays the longest
  unchanged prefix of agent calls). With two repository chains interleaving and partial failures,
  the call order shifted between runs and completed agents re-ran: the HFExperiment reader
  executed twice (run 3 and run 4; the second draft, 7 findings, is the one consolidated; the
  first, 8 findings, is in git history at 8c8e789), and run 5b started re-running the
  HFExperiment consolidator and both retail-power-limits verifiers before it was stopped with no
  file touched. From run 6 the cache is not relied upon: `tools/agent_state.py` scans the agent's
  output directory and the workflow skips, via `args`, every repository or stage whose output is
  complete on disk. Each launch's args are kept under `provenance/launch-args/`.
- A manual limit reset by the operator at ~06:15Z started a new harness session; workflow
  journals do not carry across sessions, which is why run 5a re-ran readers and was aborted
  within two minutes (no file touched).

`[AT FREEZE]` Complete list of runs, resumes and limit hits per agent.

## 7. What the orchestrator did not do

It did not read the audited repositories itself beyond `git rev-parse`, `git status --porcelain`,
`git archive`, and file counts. It did not edit any agent's finding after that agent's chain
finished. It did not re-run an agent to change an outcome.

## 8. Leaks and caveats `[AT FREEZE]`

To be completed from the transcript grep and the run log before tagging.
