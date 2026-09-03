# STATE ANCHOR

Recorded (rev0): 2026-09-02T09:31:15Z (UTC), before any reading of repository content by any audit agent.

Every finding in this audit is a claim about the state below. Any finding that
could be invalidated by later commits must say so. Repositories with commits
dated 2026-09-02 (NPLExperiment, PMExperiment) were being edited minutes before
this anchor was taken and are the most likely to move during the audit.

## Anchored HEADs

| Repository | Branch | HEAD SHA | Last commit (author date) | Commits | Pre-existing porcelain entries |
|---|---|---|---|---|---|
| AiTrader | main | `705e0ed128b7e184be6c1a23dcd06750c524c525` | 2026-08-24 19:53:49 -0700 | 199 | 1 |
| ETFExperiment | master | `4d110027674e7b4cd2861cf4e0e74f975111daf1` | 2026-08-28 19:43:48 -0700 | 28 | 0 |
| HFExperiment | main | `82e77a021256d917c665ff6d4304c25b08f35451` | 2026-08-28 14:14:08 -0700 | 13 | 4 |
| InsiderExperiment | master | `12d9fd36cf055cb10ea67a3fc737e404217bc95a` | 2026-08-25 23:24:15 -0700 | 7 | 0 |
| MLCryptoEngine | main | `5359a11fc753cdcd2606aea991dae826293d0307` | 2026-08-22 18:14:46 -0700 | 91 | 0 |
| NPDExperiment | main | `2d3d0aebf977fb2821ec78c25b370c84ec055920` | 2026-08-25 13:26:58 -0700 | 11 | 0 |
| NPLExperiment | main | `8f1fef83be0f76cbd671c2ce0fbfe8b1c4a5ea2c` | 2026-09-02 02:24:43 -0700 | 32 | 0 |
| ORBExperiment | main | `f2aa675a80fc06b74979040b3028154d1add5ec0` | 2026-08-29 20:46:22 -0700 | 59 | 0 |
| PMExperiment | main | `03d16e71dbf25a86c529884662d02136f8e82334` | 2026-09-02 02:50:29 -0700 | 36 | 0 (rev1; was 3 at rev0) |
| VRPExperiment | main | `d37cf6d190dfdaef8e613daf099a507fe1a77dcf` | 2026-08-30 00:08:02 -0700 | 12 | 0 |
| retail-power-limits | main | `dda39b2f148569a6fe9be956a979471b2330611d` | 2026-08-29 00:21:28 -0700 | 3 | 0 |
| solattn | main | `b3f5062bd87ca92303fc090f129b71e1e09b434c` | 2026-08-28 23:28:41 -0700 | 20 | 0 |
| solclear | main | `d2985769229ad40a3f02f0fe5a2fe0ad4fca295f` | 2026-08-22 19:31:12 -0700 | 28 | 0 |

## Pre-existing working-tree state (NOT caused by this audit)

Recorded verbatim from `git status --porcelain` at anchor time. Nothing in this
audit had touched any audited repository when these were recorded, and this
audit never writes under an audited path.

- **AiTrader** `M COLLECTION_LOG.md`: already present in the 2026-08-29
  baseline (`provenance/git-baseline-BEFORE.txt`). A collector process appears
  to append to this file continuously.
- **HFExperiment** `?? Accept:`, `?? GET`, `?? Host:`, `?? User-Agent:`:
  already present in the 2026-08-29 baseline. They look like stray files from a
  mis-quoted `curl` invocation by the repository owner.
- **PMExperiment** `M DECISIONS.md`, `M REGISTRATION.md`, `M docs/ACCESS.md`:
  **NOT in the 2026-08-29 baseline and NOT present in the first metadata read
  taken by this session a few minutes before the anchor check.** They appeared
  between that first read and the anchor check at 09:31:15Z. PMExperiment's HEAD
  commit is dated 2026-09-02 02:23 local (09:23Z), eight minutes before the
  anchor. The operator is editing PMExperiment concurrently with this audit.
  These uncommitted edits are outside the anchored state and are not read by
  any agent.

```
AiTrader:            M COLLECTION_LOG.md
HFExperiment:       ?? Accept:   ?? GET   ?? Host:   ?? User-Agent:
PMExperiment:        M DECISIONS.md   M REGISTRATION.md   M docs/ACCESS.md
```

All other repositories: clean working tree at anchor time.

## Snapshot protocol (how agents read the anchored state)

Because at least one repository is being edited concurrently, agents do not
read repository content from the live working trees. Immediately after the
anchor was recorded, each repository was exported at its anchored SHA with
`git archive --format=tar <SHA> | tar -x -C <scratch>/snap/<repo>` into a
session scratch directory outside every audited path. `git archive` reads only
committed objects and does not touch the working tree or index. Agents read
tracked content from these snapshots; file paths and line numbers in the
snapshot are identical to `git -C <repo> show <SHA>:<path>`.

Agents access the live repositories only for two read-only purposes:

1. **Git history and provenance** (`git log`, `git show`, `git diff <a> <b>`,
   `git blame`, `git rev-parse`), which the snapshot cannot provide.
2. **Untracked or gitignored data artifacts** (ledgers, caches, `data/`,
   `var/`, SQLite databases) that exist only in the working tree. Data read
   this way is **unanchored**: it is labelled with the read time and the
   caveat that it may have changed after the anchor. Sizes at anchor time:
   ETFExperiment/data 19M, HFExperiment/data 101M, InsiderExperiment/ledgers
   188K + cache 2.6G + var 227M, NPDExperiment/ledgers 1000K + var 901M,
   NPLExperiment/data 489M, ORBExperiment/data 340M, VRPExperiment/data 207M,
   solattn/data 756M, solclear/data/vendor 1.6M, MLCryptoEngine/data ~31G,
   AiTrader `*.db` ~7G.

Agents are prohibited from reading `.env`, `.keystore/`, `*.session`, or any
credential-bearing file in any audited repository.

## Anchor revision 1 (recorded before any agent read repository content)

At rev0 (09:31:15Z) PMExperiment was anchored at `2006ae6914cfd8a74da44ce57c74df9f4382ead3` with three
uncommitted modifications (`DECISIONS.md`, `REGISTRATION.md`,
`docs/ACCESS.md`). The operator confirmed that a separate CLI session was
closing PMExperiment at that moment over Kalshi and Polymarket terms-of-service
and jurisdiction (UBC) issues. That session committed three closure commits
(905d552 09:44:12Z, a7517c5 09:44:40Z, 03d16e7 09:50:29Z) and left the working
tree clean. Because no audit agent had yet read any repository content, and
because auditing a mid-closure state would be less useful than auditing the
closed state, PMExperiment was re-anchored to `03d16e71dbf25a86c529884662d02136f8e82334` and re-snapshotted.
No other repository's anchor changed. The rev0 snapshot of PMExperiment was
set aside unread.

The audit reads PMExperiment as a **closed** project at `03d16e71dbf2`. Any
PMExperiment finding that depends on the closure commits is a claim about
those commits and must say so.

## Excluded repositories

- `[personal repo, name removed]`: excluded as unrelated (per the audit brief).
- `MBTExperiment`: present on disk (HEAD 548a4e8 at 2026-09-03 06:37Z, read with `git rev-parse` only). Excluded by
  operator instruction on 2026-09-03 ("if you see MBTExperiment ignore it as well"). Never read, never
  snapshotted, not in the cleanliness checks.
- `solcopy`: a new repository the operator created during this session. The
  operator instructed the audit to ignore it. It is not anchored, not
  snapshotted, and not read.

## Movement since the 2026-08-29 baseline

`provenance/git-baseline-BEFORE.txt` (captured 2026-08-29 23:23 local) recorded
HEADs for the same thirteen repositories. Comparing to the anchor above:

- AiTrader: unchanged (`705e0ed128b7`)
- ETFExperiment: unchanged (`4d110027674e`)
- HFExperiment: unchanged (`82e77a021256`)
- InsiderExperiment: unchanged (`12d9fd36cf05`)
- MLCryptoEngine: unchanged (`5359a11fc753`)
- NPDExperiment: unchanged (`2d3d0aebf977`)
- **NPLExperiment: MOVED** `c2aaa279292e` -> `8f1fef83be0f`
- ORBExperiment: unchanged (`f2aa675a80fc`)
- **PMExperiment: MOVED** `7b5a75104057` -> `2006ae6914cf` (rev0) -> `03d16e71dbf2` (rev1)
- **VRPExperiment: MOVED** `3ad609827324` -> `d37cf6d190df`
- retail-power-limits: unchanged (`dda39b2f1485`)
- solattn: unchanged (`b3f5062bd87c`)
- solclear: unchanged (`d2985769229a`)

## Cleanliness protocol

`tools/git_status_check.sh <label>` is run before and after every agent phase.
Each run appends a labelled block to `provenance/git-status-checks.log` with
HEAD, branch and the full `git status --porcelain` output for all thirteen
repositories. Any entry that appears in an AFTER block and not in the matching
BEFORE block is an audit-caused modification and is reported loudly in
`findings/METHOD.md`, never reverted.

The only git commands this audit runs against an audited repository are
read-only: `rev-parse`, `log`, `show`, `status --porcelain`, `ls-files`,
`diff` between committed objects, and `blame`. No `checkout`, `stash`, `reset`,
`commit`, `add`, `branch`, `merge`, `rebase` or `clean`.

## Reserved path

`findings/independent/` is reserved for a possible later audit by a different
model. Nothing in this run creates, reads or writes under it.
