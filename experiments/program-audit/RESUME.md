# Resuming the audit after a reboot or a session-limit hit

The machine is shut down often (laptop fan). Everything the audit needs survives that:

| What | Where | Survives reboot? |
|---|---|---|
| Findings, ledgers, drafts, proposals | `findings/`, `proposals/` (git) | yes |
| Run provenance, launch args, leads, cleanliness log | `provenance/` (git) | yes |
| Repository snapshots (13, sha256 manifest in `provenance/snapshot-manifest.json`) | `/home/kiros-li/.cache/program-audit/scratchpad/snap/` | yes |
| Recomputation venv, rules copy | `/home/kiros-li/.cache/program-audit/scratchpad/{venv,COMMON_RULES.md}` | yes |
| Agents' scratch computations | `work/` (git, via the `scratchpad/work` symlink) | yes |
| Workflow journals (partial results of interrupted runs) | `~/.claude/projects/-home-kiros-li-Documents-GitHub-program-audit/*/subagents/workflows/*/journal.jsonl` | yes |
| Legacy `/tmp/claude-1000/.../scratchpad` symlinks | recreated at login by the `program-audit-tmp-links` systemd user unit | recreated |
| In-flight workflows and background waits | — | **no**: relaunch from disk state |

The workflow scripts read the persistent scratchpad directly (since 2026-09-04 18:4xZ); the `/tmp` links
exist only for older prompts and drafts that still quote the old path.

## The recipe (one command, then the launches it prints)

```
python3 tools/resume.py --runs-dead --commit --session-url <current session URL>
```

It verifies the snapshots, recreates the links, banks cross-repo leads from every journal, runs the AFTER
cleanliness check for each run in `provenance/launch-args/ACTIVE.json` (loud if anything but the
pre-existing dirt shows up), writes the next args file per unfinished blind pass, runs the BEFORE check,
appends a RUN_LOG stub, commits what is on disk, and prints one Workflow invocation per agent:

```
Workflow({ scriptPath: <printed path>, args: <printed JSON> })       # A, B, C in parallel
python3 tools/mark_launched.py <A|B|C> <run> <task-id> <workflow-id>  # records it in ACTIVE.json + RUN_LOG
git commit provenance/                                                 # task ids
```

Without `--runs-dead` the script only verifies, banks leads and reports state; use that while runs are alive.
`--phase seeded|adjudication|D` prints the later-phase state and args shapes once the blind passes are complete.

Interrupted agents often wrote their files before dying: the state report lists drafts without ledgers
and consolidated repositories awaiting verification. A missing ledger can be recovered by a follow-up
Opus agent (see RUN_LOG, 2026-09-04 18:5xZ) instead of rerunning the reader.

## Standing rules that never change

- The audited repositories are read-only. No commits, edits, file creation, branch changes or stashes
  anywhere under them. Any accidental modification is reported loudly, never reverted quietly.
- Never read `.env`, `.keystore/`, `*.session`, credentials, tokens or API keys.
- `findings/independent/` is reserved: never create, read or write anything under it.
- [personal repo, name removed], solcopy and MBTExperiment are out of scope and are never read.
- Model policy: `findings/protocol/MODEL_POLICY.md` (Opus everywhere except the three inheriting agents).

**Exactly one live session orchestrates.** `tools/resume.py` and `tools/mark_launched.py` take an orchestrator lock keyed on the live `claude` process (`~/.cache/program-audit/scratchpad/ORCHESTRATOR.json`, checked by pid, process start time and command line; stale after a reboot). If another live session holds it they refuse and print its tmux session name. Why: claude-auto-retry keeps an old session alive in a detached tmux session and resumes it after a limit reset, so a new terminal opened after a "session limit" message becomes a second orchestrator launching the same workflows onto the same files (2026-09-05, 2026-09-12). When refused: stand down and let the holder finish, or, if the operator has decided this session takes over, wait until the holder's runs have ended, run `tmux kill-session -t <name>`, then re-run the recipe. `ListAgents` shows the same thing (a busy "Program-audit four-agent neutral review" peer). `tools/orchestrator_lock.py --check` reports the state without claiming.

