# COMMON RULES FOR EVERY AUDIT AGENT (read fully before doing anything)

## Absolute rule: the audited repositories are READ ONLY
You never modify an audited repository. No commits, edits, file creation, deletion,
renames, branch changes, checkouts, stashes, resets, `uv sync`, `pip install`, `make`,
test runs, or script executions with a working directory inside an audited path.
Never open any file under /home/kiros-li/Documents/GitHub/<audited-repo> for writing.
Accidental modification is reported loudly in your output, never reverted.

The audited repositories (live paths, under /home/kiros-li/Documents/GitHub/):
AiTrader, ETFExperiment, HFExperiment, InsiderExperiment, MLCryptoEngine, NPDExperiment,
NPLExperiment, ORBExperiment, PMExperiment, VRPExperiment, retail-power-limits, solattn, solclear.
Excluded and never read: [personal repo, name removed], solcopy, MBTExperiment, and everything else under GitHub/ except program-audit.

## Where to read content: the ANCHORED SNAPSHOTS
Every repository was exported at its anchored SHA with `git archive` to:
  /tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap/<repo>/
Call this SNAP/<repo>. Read tracked files from SNAP. Paths and line numbers in SNAP are
identical to `git -C <live repo> show <SHA>:<path>`. Cite files as <repo>/<path>:<line>.
The snapshots are read-only; do not write into them.

Anchored SHAs (every finding carries the SHA of the repository it concerns):
  AiTrader            705e0ed128b7e184be6c1a23dcd06750c524c525  (main,   2026-08-24)
  ETFExperiment       4d110027674e7b4cd2861cf4e0e74f975111daf1  (master, 2026-08-28)
  HFExperiment        82e77a021256d917c665ff6d4304c25b08f35451  (main,   2026-08-28)
  InsiderExperiment   12d9fd36cf055cb10ea67a3fc737e404217bc95a  (master, 2026-08-25)
  MLCryptoEngine      5359a11fc753cdcd2606aea991dae826293d0307  (main,   2026-08-22)
  NPDExperiment       2d3d0aebf977fb2821ec78c25b370c84ec055920  (main,   2026-08-25)
  NPLExperiment       8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c  (main,   2026-09-02)
  ORBExperiment       f2aa675a80fc06b74979040b3028154d1add5ec0  (main,   2026-08-29)
  PMExperiment        03d16e71dbf25a86c529884662d02136f8e82334  (main,   2026-09-02, closed project)
  VRPExperiment       d37cf6d190dfdaef8e613daf099a507fe1a77dcf  (main,   2026-08-30)
  retail-power-limits dda39b2f148569a6fe9be956a979471b2330611d  (main,   2026-08-29)
  solattn             b3f5062bd87ca92303fc090f129b71e1e09b434c  (main,   2026-08-28)
  solclear            d2985769229ad40a3f02f0fe5a2fe0ad4fca295f  (main,   2026-08-22)

## When you may touch a LIVE repository, and how
Only two read-only purposes:
 1. Git history/provenance: `git -C <live> log|show|diff <a> <b>|blame|rev-parse|ls-tree|cat-file`.
    Never checkout, stash, reset, clean, add, commit, branch, merge, rebase, worktree, gc.
 2. Untracked or gitignored data that exists only in the working tree (data/, var/, ledgers/,
    cache/, *.db, reports artifacts not in git). Open read-only. Anything read this way is
    UNANCHORED: say so, give the read time (UTC), and note it may have changed after the anchor.
Never read .env, .keystore/, *.session, credentials, tokens or API keys. If you see one, do not
copy it anywhere.
Before your first live-repo access for a given repo, and after your last one, run
`git -C <live> status --porcelain` and record BOTH outputs verbatim in your output file.
Pre-existing dirt that is NOT yours: AiTrader ' M COLLECTION_LOG.md' (a collector appends to it);
HFExperiment '?? Accept:', '?? GET', '?? Host:', '?? User-Agent:' (owner's stray files). Report
any other entry loudly.

## Computation
A Python with numpy/scipy/pandas/statsmodels/pyarrow is at
  /tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/venv/bin/python
Write scratch scripts and outputs ONLY under
  /tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/work/<your-agent-label>/
Never execute a repository's own scripts in place. If you must run one, copy it to your work dir
and run it there with inputs read from SNAP or live data paths (read-only) and outputs to your
work dir. Prefer writing your own short recomputation from stored primitives.

## Output discipline
Write ONLY under the output directory named in your task (inside
/home/kiros-li/Documents/GitHub/program-audit/findings/ or /proposals/). Never create, read or
write anything under findings/independent/ (reserved). Never read another agent's directory
unless your task explicitly permits it. Do not run git commands inside program-audit; the
orchestrator commits.

## The finding format (every finding, no exceptions)
- ID: AUDIT-<AGENT>-<REPO>-<n>   (agent letter A, B or C; repo short name exactly as listed; n from 1 per repo)
- Repository and anchored SHA
- Hypothesis or artifact concerned
- Direction: A (closed too early) or B (claimed too much)
- Class: one of OVER_CLOSED, UNDER_CLOSED, UNSUPPORTED_POSITIVE, ARITHMETIC, STATISTICAL,
  INTERNAL_INCONSISTENCY, CROSS_REPO_INCONSISTENCY, STALE_FIGURE, PROVENANCE, PROCESS
- Severity: S1 a stated conclusion is wrong or unsupported; S2 a label contradicts its own
  evidence; S3 a blocker or external figure is stale; S4 hygiene
- Label: DERIVED (obtained from data, code or a git object) or READ (obtained from a document)
- The exact claim challenged, QUOTED VERBATIM, with file and line
- The evidence, with figures and their n, each with file and line (or data path + read time)
- What would resolve it
- Confidence: HIGH / MEDIUM / LOW with one sentence why
- Could later commits invalidate this? yes/no and why
- Disclosed by the authors? If the document already discloses the limitation you are raising,
  the finding is READ, is at most S3, and must say plainly that the authors disclosed it and
  where. Presenting a disclosed limitation as a discovery is itself a process failure.

You may not invent evidence and you may not misquote. If you cannot find a file, line and
figure for a claim, you do not have a finding. Quote with enough context to be located by grep.

## Report where you found nothing
A sound repository is reported sound, with a list of what you checked and what you would have
expected to find if the thesis held. Manufacturing findings is worse than a clean result.

## Anchoring caveat
Every finding is a claim about the anchored SHA. NPLExperiment and PMExperiment had commits on
2026-09-02 and are actively developed; ORBExperiment and VRPExperiment moved in the days before
the anchor. Say explicitly when a finding could be invalidated by later commits.
