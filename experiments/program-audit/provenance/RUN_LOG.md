# Run log

## 2026-09-02 09:59Z — Agent A blind pass, run 1 (FAILED, no output)
Workflow wf_f06615d7-b2f launched at 09:59:56Z with 37 sub-agents. Every sub-agent failed with
"You've hit your session limit · resets 7:10am (America/Vancouver)" (14:10Z) after 375 s,
1.77M sub-agent tokens and 207 tool uses. Zero agents completed; zero files were written under
findings/agentA (verified: directory empty at 18:36Z). Cleanliness check
"01-agentA-blind-run1-FAILED-AFTER" at 18:36:08Z shows only the pre-existing AiTrader and
HFExperiment entries. No audited repository was modified. Relaunched as run 2 after the reset.
Independence impact: none — no output existed for any later agent to see.

## 2026-09-02 18:37Z — Agent A blind pass, run 2 (FAILED, no output)
Resumed wf_f06615d7-b2f at 18:37Z after the 14:10Z reset. All 37 sub-agents failed again with
"You've hit your session limit · resets 4:30pm (America/Vancouver)" (23:30Z) after 409 s,
2.94M sub-agent tokens and 419 tool uses. Zero agents completed; zero files under findings/agentA
(verified 2026-09-03 00:31Z). Cleanliness check "01-agentA-blind-run2-FAILED-AFTER" shows only the
pre-existing AiTrader and HFExperiment entries. No audited repository was modified.
Lesson: at full parallelism every in-flight agent dies together when the limit hits and nothing is
banked. Run 3 is throttled to two repositories at a time, smallest first, so completed agents are
cached by the workflow runtime and survive later limit hits.

## 2026-09-03 00:26Z — host reboot
The workstation rebooted (uptime 6 min at 00:32Z). /tmp was cleared: the anchored snapshots, the
recomputation venv, the scratch copy of COMMON_RULES.md and the drafted B/C/seeded workflow scripts
were lost. Snapshots were rebuilt with `git archive` at the SAME anchored SHAs (all thirteen
anchored commits still present in the live repositories; file counts identical to the first
export). The rules file was restored from findings/protocol/COMMON_RULES.md. Workflow scripts are
now kept under findings/protocol/ in this repository and launched from there.

## 2026-09-03 00:33Z — Agent A blind pass, run 3 (throttled, in progress)
Launched wf_e113872d-e9e from findings/protocol/agentA-blind.workflow.js with BATCH=2 (two
repositories at a time, smallest first). At 00:45Z the operator instructed: Fable for all analysis,
Opus for mundane low-logic tasks. The scripts were patched (consolidators, verifiers, appliers,
inventory/triage, merges -> Opus; readers, cross-repo, verification, provenance, seeded checks,
adjudication, Agent D reasoning -> Fable; see findings/protocol/MODEL_POLICY.md). After the two
batch-1 readers completed (00:50:58Z; drafts on disk), the run was stopped and resumed at 00:52Z
with resumeFromRunId so the two completed Fable readers replayed from cache and every later
mechanical agent runs on Opus. Task id after resume: wdmfcod2d.

## 2026-09-03 00:52Z–01:0xZ — Agent A blind pass, run 3 outcome (PARTIAL)
The resumed run (task wdmfcod2d) ended with agents_done=2, agents_error=24. Banked in the workflow
cache (journal wf_e113872d-e9e, three `result` rows): the retail-power-limits reader (Fable), the
HFExperiment reader (Fable) and the retail-power-limits consolidator (Opus, 11 findings
AUDIT-A-retail-power-limits-1..11). Failed with "You've hit your session limit · resets 9:40pm
(America/Vancouver)" (04:40Z): both retail-power-limits verifiers and every reader from batch 2
onward. On disk: findings/agentA/_drafts/{retail-power-limits,HFExperiment}/all.md(+.reopen.md) and
findings/agentA/retail-power-limits.{md,json,reopen.md}. Cleanliness check
"01-agentA-blind-run3-partial-AFTER" (04:47Z): only the pre-existing AiTrader and HFExperiment
entries. No audited repository was modified.

## 2026-09-03 ~02:14Z — second host reboot (detected 04:44Z)
`uptime` at 04:44Z showed 2h30m, i.e. a boot near 02:14Z, two hours after the first reboot. /tmp
was cleared again: snapshots, venv and the batch-1 scratch scripts
(scratchpad/work/agentA-rpl-consolidate/verify.py, scratchpad/work/agentA-HFExperiment/recompute.py)
were lost. The figures those scripts produced are recorded verbatim in the finding text, but the
scripts themselves cannot be re-inspected; Agent C's verification is independent and does not rely
on them. Remedy: the harness scratchpad path is now a symlink to
/home/kiros-li/.cache/program-audit/scratchpad (persistent across reboots). Snapshots were rebuilt
there at the same anchored SHAs (all thirteen file counts identical: 413/109/98/73/292/75/147/157/
32/47/21/99/55, chmod a-w), the venv was rebuilt (numpy 2.5.2, scipy 1.18.1, pandas 3.0.5,
statsmodels 0.15.0), and scratchpad/work now resolves to program-audit/work/ so agent scratch
scripts are committed with each phase. Every path quoted in prompts and COMMON_RULES.md is
byte-identical, so the three cached agents remain valid for resume. If /tmp is cleared again the
only repair is to re-create the one symlink.

## 2026-09-03 04:48Z — Agent A blind pass, run 4 (resume of wf_e113872d-e9e)
Resumed after the 04:40Z reset with the same scriptPath and resumeFromRunId. Cleanliness check
"01-agentA-blind-run4-BEFORE" recorded immediately before launch.

## 2026-09-03 04:48Z–05:43Z — Agent A blind pass, run 4 outcome (PARTIAL)
Task wsse8izdx: agents_done=10, agents_error=21, 1.56M sub-agent tokens, 55 min. Completed and
cached: the full retail-power-limits chain (verify1, verify2, apply: kept 4, corrected 7, dropped 0)
and the full HFExperiment chain (reader, consolidate: 7 findings AUDIT-A-HFExperiment-1..7,
verify1, verify2, apply: kept 3, corrected 4, dropped 0). Every batch-2+ reader failed with
"You've hit your session limit · resets 2:40am (America/Vancouver)" (09:40Z). Cleanliness check
"01-agentA-blind-run4-AFTER" (06:17Z): only the pre-existing entries.
Provenance note: the HFExperiment reader executed TWICE. Its run-3 result (8 draft findings, the
version committed at 8c8e789) was in the journal, yet the resume re-ran it under a different cache
key (the reader prompt is unchanged in the script diff feb292c..e1dbcd5; cause not identified).
The run-4 draft (7 findings) overwrote the run-3 draft on disk and is what the consolidator used.
Both executions were blind Fable runs of the same prompt; the run-3 draft remains in git history.
The operator reset the session limit manually at ~06:15Z ("/limit-reset"), which also started a
new harness session (transcripts now under .../2c6a58bc-.../).

## 2026-09-03 06:19Z — run 5a ABORTED after 2 minutes (journal not carried across sessions)
The resume launched in the new session directory with an empty journal, so the runtime began
re-executing the two cached readers (retail-power-limits, HFExperiment). Stopped at 06:21Z before
either wrote a file (draft mtimes unchanged, see below). The old journal (114 rows, 11 results)
was copied into the new session's workflow directory and the run resumed as 5b. The aborted
journal is kept as journal.aborted-run5a.jsonl.bak. No finding was affected.

## 2026-09-03 06:21Z — run 5b STOPPED after 3 minutes (positional resume cache re-ran completed agents)
With the journal carried across, the resume still started the HFExperiment consolidator and both
retail-power-limits verifiers, all three of which had cached results. Cause (workflow reference,
"Resume"): the cache replays the longest UNCHANGED PREFIX of agent() calls; with two repository
chains interleaving and partial failures, the call order shifts and everything after the first
mismatch runs live. The same mechanism explains the HFExperiment reader's second execution in run
4. Stopped at 06:24Z before any output file was touched (mtimes unchanged; git status clean).
Remedy: tools/agent_state.py scans the agent's output directory (a repository is complete when
its <repo>.json exists and <repo>.md carries "Citation check" lines, or the json is empty; a reader
part is complete when its draft and ledger exist) and the result is passed as workflow `args`;
the script skips completed chains and parts, and every launch is fresh (no resumeFromRunId).
Disk state, not the runtime cache, is the ground truth from run 6 onward.

## 2026-09-03 06:27Z — Agent A blind pass, run 6 (fresh run wf_d4536152-b3a, disk-state args)
Launched fresh (no resumeFromRunId) with args from tools/agent_state.py: done_repos =
[HFExperiment, retail-power-limits], done_parts = {}, plus the 20 cross-repo leads those two
consolidators returned (recovered from the journals, recorded in
provenance/launch-args/agentA-run6.args.json). Cleanliness check "01-agentA-blind-run6-BEFORE"
(06:24Z): only the pre-existing entries. Task id w1c402gcy.

## 2026-09-03 06:37Z — operator: exclude MBTExperiment
"if you see MBTExperiment ignore it as well". MBTExperiment exists on disk (HEAD 548a4e8, read with
`git rev-parse` only). Added to the excluded list in ANCHOR.md, COMMON_RULES.md (repository copy and
the live scratchpad copy that agents read at start) and METHOD.md. Agent A run 6 was in progress;
its rules already excluded everything outside the thirteen audited repositories, so no reader could
have opened it. Agents launched from now on see the explicit name.

## 2026-09-03 06:27Z–06:54Z — Agent A blind pass, run 6 outcome (KILLED with the harness session)
Task w1c402gcy (wf_d4536152-b3a). The operator had to relaunch the session and CLI; the workflow
died with the process at ~06:54Z. Journal: 6 started, 4 results — NPDExperiment reader (Fable),
InsiderExperiment reader (Fable), NPDExperiment consolidator (Opus, 4 findings
AUDIT-A-NPDExperiment-1..4, S1 ARITHMETIC DERIVED among them) and NPDExperiment verifier 1 (Opus).
In flight when killed: NPDExperiment verifier 2 and the InsiderExperiment consolidator, which had
written InsiderExperiment.md (7 IDs) and .reopen.md but not the .json. Those two partial files are
copied to provenance/partial-outputs/ and will be overwritten by the re-run consolidator; the
reader drafts (the consolidator's inputs) are intact. Cleanliness check
"01-agentA-blind-run6-killed-AFTER" (06:58Z): only the pre-existing entries.
Remedy: tools/agent_state.py now also reports "consolidated but unverified" repositories so the
A/B scripts skip the consolidator and run only verify/apply (NPDExperiment: 4 findings).

## 2026-09-03 06:59Z — Agent A blind pass, run 7 (fresh run, disk-state args)
done_repos = [HFExperiment, retail-power-limits]; done_parts = {InsiderExperiment: [all],
NPDExperiment: [all]}; consolidated = {NPDExperiment: 4}; 29 cross-repo leads taken from the three consolidators'
structured results in the journals (the ledger parser in the scanner returns line-wrapped fragments,
so it is not used for the prompt hints). Args recorded in provenance/launch-args/agentA-run7.args.json.
Task id wux6sep9q (wf_e8863b9a-427), launched 07:01Z.

## 2026-09-03 07:01Z–~07:10Z — Agent A blind pass, run 7 outcome (account session limit)
Task wux6sep9q (wf_e8863b9a-427). Result: agents_done = 2, agents_error = 21; every failure carried
"You've hit your session limit · resets 4:10am (America/Vancouver)" (11:10Z). The journal holds no
labels or timestamps, so completion is reconstructed from results and file mtimes.
Completed: NPDExperiment verifier 1 and verifier 2 (Opus); both verdicts saved verbatim to
provenance/partial-outputs/agentA-NPDExperiment.verifier-verdicts.run7-limit.json (verifier 1: KEEP all;
verifier 2: CORRECT on -1 with a disclosure_ref). The applier that would have consumed them failed on the
limit, so run 8 re-runs both verifiers and the applier for NPDExperiment; the run-7 verdicts stay in
provenance for comparison only and are not fed to run 8.
Partial: the InsiderExperiment consolidator (Opus, second attempt) wrote InsiderExperiment.md (07:05:39Z,
7 findings AUDIT-A-InsiderExperiment-1..7: one S2, three S3, three S4, with the "Dropped at consolidation"
and "Live-repo access log" sections) and InsiderExperiment.reopen.md (07:07:38Z, with the 7-item
"Leads for the cross-repository pass" section), then hit the limit before writing InsiderExperiment.json
and before returning its structured result. Both files copied to
provenance/partial-outputs/agentA-InsiderExperiment.{md,reopen.md}.run7-limit-consolidator.
Failed before doing anything: the readers for VRPExperiment, ETFExperiment, solclear, PMExperiment,
solattn, NPLExperiment, MLCryptoEngine, ORBExperiment and AiTrader (no draft files written; draft
directories empty).
Cleanliness check "01-agentA-blind-run7-AFTER" (18:56Z, first opportunity after the reboot below): only
the pre-existing entries (AiTrader ` M COLLECTION_LOG.md`; HFExperiment four untracked curl-artifact
names). Every audited HEAD equals its anchored SHA.

## 2026-09-03 ~18:52Z — third reboot; scratchpad symlink re-created
The operator reports the machine rebooted during the night; at 18:56Z uptime read 4 minutes, so the last
boot was at about 18:52Z. /tmp was cleared again, which removed the harness scratchpad directory for the
original session id (5ca157a0…) that every prompt path points at. Repaired at 18:56Z exactly as before:
`ln -s /home/kiros-li/.cache/program-audit/scratchpad <session-dir>/scratchpad` for both harness session
ids (5ca157a0… and the current 2c6a58bc…). The persistent directory was untouched: snapshot file counts
413/109/98/73/292/75/147/157/32/47/21/99/55 for the thirteen repositories, unchanged since the anchor.
No prompt path changed.

## 2026-09-03 18:58Z — InsiderExperiment: json produced by mechanical transcription of the run-7 md
Decision: rather than run the consolidator a third time (two partials already on disk), the run-7
consolidator's completed InsiderExperiment.md is treated as the consolidation and the missing
InsiderExperiment.json is produced by a single mechanical Opus agent (model policy: mechanical work goes
to Opus) that transcribes the seven finding blocks into the 22-key contract from consolidatorPrompt(),
with NPDExperiment.json and HFExperiment.json as the shape reference, and is forbidden to edit the md.
The verifiers and applier then run in run 8 exactly as for any consolidated-but-unverified repository
(tools/agent_state.py reports consolidated = {NPDExperiment: 4, InsiderExperiment: 7}), and verifier 1
checks the json against the md as part of its citation lens. The seven cross-repository leads for
InsiderExperiment are taken from the reopen ledger's "Leads for the cross-repository pass" section
(the consolidator never returned its structured result) and added to the run-8 launch args.

## 2026-09-03 19:08Z — Agent A blind pass, run 8 (fresh run wf_c79bd45f-a47, disk-state args)
Launched fresh (no resumeFromRunId) after the 11:10Z limit reset, with args from tools/agent_state.py:
done_repos = [HFExperiment, retail-power-limits]; done_parts = {InsiderExperiment: [all],
NPDExperiment: [all]}; consolidated = {InsiderExperiment: 7, NPDExperiment: 4}; 36 cross-repo leads
(the 29 from run 7 plus the 7 InsiderExperiment leads from its reopen ledger). Args recorded in
provenance/launch-args/agentA-run8.args.json. Cleanliness check "01-agentA-blind-run8-BEFORE" (19:06Z):
only the pre-existing entries. Task id w5e6202dj. Batches (BATCH = 2, smallest first): Insider/NPD
verify+apply, then the nine unread repositories in ORDER.
