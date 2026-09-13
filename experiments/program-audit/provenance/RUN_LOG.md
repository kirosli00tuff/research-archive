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

## 2026-09-03 19:08Z–19:27Z — Agent A blind pass, run 8 outcome (STOPPED by operator model-budget instruction)
Task w5e6202dj (wf_c79bd45f-a47). Batch 1 completed and is banked: InsiderExperiment verifiers 1 and 2
and applier (kept 3, corrected 4, dropped 0; IDs -1..-7 unchanged) and NPDExperiment verifiers 1 and 2
and applier (kept 0, corrected 4, dropped 0; IDs -1..-4 unchanged), all Opus. Batch 2 had started the
VRPExperiment and ETFExperiment readers on Fable at ~19:23Z when the operator wrote "im already at 80%
fable limit weekly ... use fable sparingly please"; the run was stopped at 19:27Z with those two readers
about three minutes in and nothing written to disk by them (no draft files). MODEL_POLICY.md revision 2
records the new allocation: explicit Opus on every agent except A-cross-repo, B-cross-repo and D4-D5.
All five workflow scripts patched and syntax-checked. Cleanliness check
"01-agentA-blind-run8-stopped-AFTER": only the pre-existing entries.

## 2026-09-03 19:36Z — Agent A blind pass, run 9 (fresh run wf_60282a09-268, Opus readers)
First run under MODEL_POLICY.md revision 2: readers, consolidators, verifiers and appliers all on Opus;
only A-cross-repo inherits the session model. Args from tools/agent_state.py: done_repos =
[HFExperiment, InsiderExperiment, NPDExperiment, retail-power-limits]; done_parts = {}; consolidated = {};
the same 36 cross-repo leads as run 8 (provenance/launch-args/agentA-run9.args.json). Cleanliness check
"01-agentA-blind-run8-stopped-AFTER" serves as the BEFORE check for this run (nothing touched an audited
repository in between). Task id w4jh48cgb. Nine repositories to read, BATCH = 2, smallest first.

## 2026-09-03 19:36Z–~20:27Z — Agent A blind pass, run 9 outcome (account session limit)
Task w4jh48cgb (wf_60282a09-268). Result: agents_done = 8, agents_error = 19; every failure carried
"You've hit your session limit · resets 4:50pm (America/Vancouver)" (23:50Z). Completed and banked
(all Opus): the VRPExperiment and ETFExperiment readers (single "all" part each, drafts and reopen
ledgers under _drafts/), both consolidators (VRPExperiment 7 findings AUDIT-A-VRPExperiment-1..7 with one
S1 OVER_CLOSED DERIVED; ETFExperiment as recorded in its json) and all four verifiers, whose verdicts are
saved verbatim to provenance/partial-outputs/agentA-VRP-ETF.verifier-verdicts.run9-limit.json. Both
appliers failed on the limit, so run 10 re-runs verifiers and appliers for these two repositories
(tools/agent_state.py reports them consolidated-but-unverified); the run-9 verdicts stay in provenance
for comparison only. Failed before writing anything: all seventeen reader parts for solclear,
PMExperiment, solattn, NPLExperiment, MLCryptoEngine, ORBExperiment and AiTrader.
The consolidators' structured cross-repository leads were added to the run-10 args. The orchestrating
session was itself rate-limited (a /compact attempt failed with the same message) and restarted.
Cleanliness check "01-agentA-blind-run9-AFTER": only the pre-existing entries.

## 2026-09-03 ~23:44Z — fourth reboot; scratchpad symlinks re-created
The operator reported another reboot; at 23:54Z uptime read 10 minutes. /tmp was cleared again. The
scratchpad symlink was re-created for the original session id (5ca157a0…, the path every prompt uses)
and for the two later harness session ids; the persistent directory, its 13 snapshots and COMMON_RULES.md
were untouched.

## 2026-09-03 23:5xZ — VRPExperiment: applier completed the md but not the json (run 9)
Re-inspection of run 9 shows the VRPExperiment applier (Opus) finished editing VRPExperiment.md at
20:20Z — all seven findings carry a "Citation check" line, three verifier splits resolved against the
snapshot, AUDIT-A-VRPExperiment-7 raised S4→S2 — and then hit the limit before syncing VRPExperiment.json
(mtime 20:03Z, pre-correction) and before returning its counts. Decision, as for InsiderExperiment on
run 7: the md is the consolidation of record; a single mechanical Opus agent syncs the json to it
(severity, label, corrected lines and quotes, plus the citation_check key the appliers add), forbidden
to touch the md. tools/agent_state.py already reports VRPExperiment complete (json present, md carries
"Citation check"), so run 10 skips it.

## 2026-09-03 23:56Z — Agent A run 10, Agent B run 1 and Agent C run 1 launched IN PARALLEL (operator instruction)
Operator: "try to run agents B and C and D in parallel please". The blind passes of A, B and C are
independent by construction (each reads only the snapshots, the live repositories read-only, and its
own output directory; the rules forbid reading another agent's directory), so the brief's
"each agent commits before the next starts" sequencing is relaxed for the blind passes on the
operator's instruction; the dependent stages keep their order: seeded checks after each blind pass
commits, C adjudication after A and B are complete and C's own blind and seeded output is committed,
D after the findings-frozen tag (every D prompt reads SUMMARY.md and the adjudication, so D cannot
start now). Trade-off recorded: three concurrent workflows put more agents in flight when the account
session limit trips, so more in-flight work is lost per hit, but the window's budget is used without
idle gaps and with fewer orchestrator turns (the orchestrator is Fable and is being spared).
- Agent A run 10: task w8drvu029 (wf_c46820bd-e14). Args in provenance/launch-args/agentA-run10.args.json:
  done_repos = [HFExperiment, InsiderExperiment, NPDExperiment, VRPExperiment, retail-power-limits];
  ETFExperiment consolidated (8 findings) awaiting verify/apply; seven repositories to read. Cross-repo
  leads are no longer passed as args; the cross-repo agent reads provenance/launch-args/agentA-leads.json
  (56 leads from six consolidators). BEFORE check: "01-agentA-blind-run9-AFTER" (nothing touched since).
- Agent B run 1: task wf2sax6x7 (wf_58f35560-86a). Empty state (provenance/launch-args/agentB-run1.args.json);
  readers on Opus per MODEL_POLICY.md revision 2. BEFORE check "02-agentB-blind-run1-BEFORE" (23:54Z):
  only the pre-existing entries.
- Agent C run 1: task wv1y3i6h0 (wf_17777430-12f). Empty state (provenance/launch-args/agentC-run1.args.json);
  every stage on Opus. BEFORE check "03-agentC-blind-run1-BEFORE" (23:54Z): only the pre-existing entries.

## 2026-09-04 00:0xZ — VRPExperiment.json synced to the corrected md (mechanical Opus agent)
Result: kept 2 (findings 1, 4), corrected 5 (2, 3, 5, 6, 7), dropped 0; AUDIT-A-VRPExperiment-7 S4→S2;
23 keys with citation_check on every finding; claim quotes verified character-for-character against the md;
md untouched. VRPExperiment is complete for Agent A.

## 2026-09-03 23:56Z–2026-09-04 ~00:40Z — outcomes of the three parallel runs (account session limit, resets 04:50Z)
All three workflows ended with "You've hit your session limit · resets 9:50pm (America/Vancouver)".
Several agents wrote their output files before the limit killed them and are banked from disk (the
harness reports them as failed because their structured return never arrived); each was checked for
its closing sections before being counted.
- Agent A run 10 (w8drvu029, wf_c46820bd-e14): agents_done 4, error 16. ETFExperiment verified and
  applied (kept 2, corrected 6, dropped 0; IDs -1..-8) — ETFExperiment complete, six of thirteen done.
  PMExperiment p2-progress reader returned; PMExperiment p1-register and solclear p1-findings readers
  wrote complete drafts and reopen ledgers before failing. Fourteen reader parts never started.
- Agent B run 1 (wf2sax6x7, wf_58f35560-86a): agents_done 3, error 24. retail-power-limits reader and
  consolidator (8 findings AUDIT-B-retail-power-limits-1..8: three S2, five S3; 14 cross-repo leads →
  provenance/launch-args/agentB-leads.json) and the HFExperiment reader returned. The HFExperiment
  consolidator wrote HFExperiment.md (18 findings, all closing sections) and HFExperiment.positives.md
  (with its leads section) before failing, without the json. Verifiers for retail-power-limits and
  all other readers failed.
- Agent C run 1 (wv1y3i6h0, wf_17777430-12f): agents_done 6, error 13. retail-power-limits and
  HFExperiment: inventory (C-locate), numeric verification (C-verify) and provenance (C-provenance)
  returned. The HFExperiment consolidator wrote HFExperiment.md (9 findings, closing sections) before
  failing, without HFExperiment.json and HFExperiment.scoreboard.json; the retail-power-limits
  consolidator wrote nothing. Eleven inventories never started.
Cleanliness checks "01-agentA-blind-run10-AFTER", "02-agentB-blind-run1-AFTER",
"03-agentC-blind-run1-AFTER" (04:51Z): only the pre-existing entries.

## 2026-09-04 04:5xZ — HFExperiment json files for B and C by mechanical transcription; A run 11 launched
As for InsiderExperiment (A, run 7): the complete consolidator mds are the consolidations of record;
one mechanical Opus agent each transcribes findings/agentB/HFExperiment.json (18 findings, contract
from consolidatorPrompt in agentB-blind.workflow.js) and findings/agentC/HFExperiment.json plus
HFExperiment.scoreboard.json (9 findings, contract items 5-6 in agentC-blind.workflow.js, counts from
the on-disk claims and provenance json), forbidden to touch the mds. B and C relaunch after those files
exist so their scanners report HFExperiment as consolidated-but-unverified; A relaunches now.
Agent A run 11: args done_repos = [ETFExperiment, HFExperiment, InsiderExperiment, NPDExperiment,
VRPExperiment, retail-power-limits]; done_parts = {PMExperiment: [p1-register, p2-progress],
solclear: [p1-findings]}; leads via file. BEFORE check: "01-agentA-blind-run10-AFTER".
Agent A run 11: task wy7aw6e69 (wf_d768adf5-f74), launched 04:55Z.

## 2026-09-04 05:0xZ — Agent B run 2 launched (HFExperiment json transcribed)
findings/agentB/HFExperiment.json written by the mechanical Opus agent: 18 findings (1 S1, 6 S2, 9 S3,
2 S4), 22 contract keys, claim quotes verified verbatim against the md, md and positives ledger
untouched. Args (provenance/launch-args/agentB-run2.args.json): consolidated = {retail-power-limits: 8,
HFExperiment: 18} awaiting verify/apply; eleven repositories to read; leads via
provenance/launch-args/agentB-leads.json. BEFORE check: "02-agentB-blind-run1-AFTER" (04:51Z; nothing
touched an audited repository since).
Agent B run 2: task wll806z2p (wf_0a1e70b2-b89), launched 05:02Z.

## 2026-09-04 05:1xZ — Agent C run 2 launched (HFExperiment json and scoreboard transcribed)
findings/agentC/HFExperiment.json (9 findings: 1 S2, 2 S3, 6 S4; directions neutral ×6, A ×1, B ×2;
22 contract keys, claim quotes verified verbatim) and HFExperiment.scoreboard.json (claims 20 verified /
7 contradicted / 3 unverifiable on the 30 granular rows; intervals 14 audited, 2 independence doubtful,
8 recomputed, 0 conclusion moved; tests 6 audited, 0 issues; provenance 30 supported / 2 not supported /
4 partial / 1 unverifiable) written by the mechanical Opus agent from the consolidator md and the on-disk
claims and provenance json; md untouched. Args (provenance/launch-args/agentC-run2.args.json):
HFExperiment consolidated awaiting check/apply; retail-power-limits inventory, verification and
provenance done, consolidator to run; eleven repositories from inventory. BEFORE check:
"03-agentC-blind-run1-AFTER" (04:51Z; nothing touched an audited repository since).
Agent C run 2: task wsyhgs1dy (wf_5c7ad8a5-a74), launched 05:12Z.

## 2026-09-04 18:2xZ — Runs A11 / B2 / C2 ended on the session limit (reset 09:50Z); reboot 11:06Z; bookkeeping
Agent A run 11 (wy7aw6e69, wf_d768adf5-f74): 6 agents done, 15 failed. PMExperiment consolidated (12
findings: S2×5 S3×6 S4×1), verified by two verifiers and applied (kept 7, corrected 5) → DONE. solclear p2
reader and consolidator done (10 findings: S1×2 S2×3 S3×4 S4×1); the solclear verifiers failed before
returning; readers for solattn, NPLExperiment, MLCryptoEngine, ORBExperiment and AiTrader failed before
writing. 13 PMExperiment + 9 solclear cross-repo leads appended to agentA-leads.json (56 → 78). AFTER
check "01-agentA-blind-run11-AFTER" (18:18Z): only the pre-existing dirt (AiTrader COLLECTION_LOG.md,
HFExperiment four stray untracked names).
Agent B run 2 (wll806z2p, wf_0a1e70b2-b89): 6 done, 21 failed. retail-power-limits verified and applied
(kept 4, corrected 4) and HFExperiment verified and applied (kept 10, corrected 8) → both DONE. The
InsiderExperiment reader (14 draft findings: S2×2 S3×10 S4×2) and the NPDExperiment reader (20 draft
findings: S1×3 S2×5 S3×9 S4×3) wrote complete all.md drafts (closing "found sound" and live-access-log
sections present; both logs show a clean tree before and after) but were killed before writing their
all.positives.md ledgers; the other nine readers failed before writing anything. Recovery: two follow-up
Opus agents write the two ledgers from the drafts plus the snapshots, with no live-repo access; the drafts
are not modified. Each ledger ends with a note saying so. AFTER check "02-agentB-blind-run2-AFTER" (18:18Z):
pre-existing dirt only.
Agent C run 2 (wsyhgs1dy, wf_5c7ad8a5-a74): 7 done, 11 failed. retail-power-limits consolidated (8
findings) and applied (kept 7, corrected 1) → DONE; HFExperiment applied (kept 6, corrected 3) → DONE.
InsiderExperiment and NPDExperiment inventories written; their verification and provenance stages failed
before writing; the nine other locates failed. AFTER check "03-agentC-blind-run2-AFTER" (18:18Z):
pre-existing dirt only.
Reboot: /tmp cleared again; scratchpad symlinks re-created (four session ids); snapshots intact (13 dirs,
file counts unchanged: 413/109/98/73/292/75/147/157/32/47/21/99/55).

## 2026-09-04 18:21Z — A run 12 and C run 3 launched in parallel; B run 3 waits for the two ledgers
Agent A run 12 args (agentA-run12.args.json): done_repos = [ETFExperiment, HFExperiment, InsiderExperiment,
NPDExperiment, PMExperiment, VRPExperiment, retail-power-limits]; done_parts = {solclear: [p1-findings,
p2-progress]}; consolidated = {solclear: 10}; leads via file (78 entries). BEFORE check
"01-agentA-blind-run12-BEFORE" (18:20Z). Task wp3z70q72 (wf_f3fc900f-431).
Agent C run 3 args (agentC-run3.args.json): done_repos = [HFExperiment, retail-power-limits];
InsiderExperiment and NPDExperiment inventory done, verification/provenance/consolidate to run; nine
repositories from inventory. BEFORE check "03-agentC-blind-run3-BEFORE" (18:20Z). Task w9ku6yk69
(wf_ac411b13-975).

## 2026-09-04 18:5xZ — B positives ledgers recovered; B run 3 launched
findings/agentB/_drafts/InsiderExperiment/all.positives.md (57,990 bytes) and
findings/agentB/_drafts/NPDExperiment/all.positives.md (51,197 bytes; 35 numbered entries: 14 positive,
4 qualified positive, 9 shipped, 4 open, 4 thresholded negative, plus open-items and thresholded-negatives
tables) written by two follow-up Opus agents from the drafts and the snapshots. Neither draft changed
(git diff empty). Neither agent touched the live repositories; the NPDExperiment agent reported one
read-only `git status --porcelain` inside program-audit itself (not an audited repository), nothing
staged or changed. Both ledgers carry the recovery note at the end.
Agent B run 3 args (agentB-run3.args.json): done_repos = [HFExperiment, retail-power-limits]; done_parts =
{InsiderExperiment: [all], NPDExperiment: [all]}; consolidated = {}; leads via file (14 entries). BEFORE
check "02-agentB-blind-run3-BEFORE".
Agent B run 3: task w6njcsz94 (wf_bb83861e-ebb), launched 18:31Z. All three blind passes (A run 12, B run 3, C run 3) now run concurrently.

## 2026-09-04 18:4xZ — Reboot-safety (operator: "make everything reboot-safe")
The six workflow scripts and both copies of COMMON_RULES.md now point at the persistent scratchpad
/home/kiros-li/.cache/program-audit/scratchpad (snap/, venv/, COMMON_RULES.md, work/) instead of the
/tmp/claude-1000/.../5ca157a0.../scratchpad path that every reboot erased. Snapshot content is unchanged
(13 repositories, 1,618 files; sha256 manifest written to provenance/snapshot-manifest.json and verified).
The old /tmp path is still recreated as a symlink at login by the systemd user unit
program-audit-tmp-links.service (tools/tmp_links.sh, session ids in provenance/launch-args/SESSIONS.txt) for
prompts and drafts that quote it. tools/resume.py is the one-command resume (RESUME.md); it AFTER-checks the
runs recorded in provenance/launch-args/ACTIVE.json by tools/mark_launched.py against
DIRT_BASELINE.json, banks journal leads, writes next args and BEFORE checks, and prints the launches.
work/ (agents' recomputation scripts and intermediate outputs, 2.2 MB, cited by DERIVED findings) is now
committed as provenance; a secrets scan found nothing. Runs in flight (A 12, B 3, C 3) were launched with
the old paths, which remain valid through the symlinks; the new paths apply from the next launch.

## 2026-09-04T23:02Z — tools/resume.py
agent A: 8/13 done
agent B: 2/13 done
agent C: 2/13 done
AFTER checks: pre-existing dirt only
prepared A run 13 (provenance/launch-args/agentA-run13.args.json)
prepared B run 4 (provenance/launch-args/agentB-run4.args.json)
prepared C run 4 (provenance/launch-args/agentC-run4.args.json)
Outcomes of the runs closed above (all cut by the 5-hour session limit at ~19:00Z, reset 23:00Z):
- A run 12 (wf_f3fc900f-431): solclear verified and applied (12 → kept 3, corrected 7); readers for
  solattn, NPLExperiment, MLCryptoEngine, ORBExperiment and AiTrader never started. A now 8/13.
- B run 3 (wf_bb83861e-ebb): InsiderExperiment consolidated (14 findings: S2×2 S3×10 S4×2) and
  NPDExperiment consolidated (19 findings); both verify/apply stages and all remaining readers failed.
  12 cross-repo leads banked from the two consolidators (B leads now 26). B stays 2/13.
- C run 3 (wf_ac411b13-975): InsiderExperiment verification, provenance and consolidation (10 findings)
  done; NPDExperiment verification and provenance done, consolidation pending; nine locates failed.
  C stays 2/13. Snapshot manifest re-verified on resume (13 repos, 1618 files).
Next: A run 13, B run 4, C run 4 launched in parallel from the prepared args.
Agent A run 13: task wftt3hir9 (wf_7d192f1f-1c2), launched 23:02Z.
Agent B run 4: task wvgkzos5s (wf_971efc5d-8a6), launched 23:02Z.
Agent C run 4: task w4n9tddim (wf_3c3f08c2-582), launched 23:02Z.

## 2026-09-05T03:41Z — tools/resume.py
agent A: 8/13 done
agent B: 4/13 done
agent C: 4/13 done
AFTER checks: pre-existing dirt only
prepared A run 14 (provenance/launch-args/agentA-run14.args.json)
prepared B run 5 (provenance/launch-args/agentB-run5.args.json)
prepared C run 5 (provenance/launch-args/agentC-run5.args.json)
Agent A run 14: task wvffhfqmx (wf_990e6ca4-939), launched 03:42Z.
Agent B run 5: task wc77dsx68 (wf_77c4a710-2b4), launched 03:42Z.
Agent C run 5: task w9pltaes5 (wf_5eccab36-37a), launched 03:42Z.
Outcomes of A run 13 / B run 4 / C run 4 (launched 23:02Z, cut by the session limit; reset 03:40Z 2026-09-05):
- A run 13 (wf_7d192f1f-1c2): solattn and NPLExperiment readers done; both consolidators wrote their
  outputs (solattn 11 findings, NPLExperiment 12) before dying, so their cross-repo leads never returned
  (recovered below if present in the reopen notes). MLCryptoEngine, ORBExperiment, AiTrader readers failed.
- B run 4 (wf_971efc5d-8a6): InsiderExperiment verified and applied (14: kept 8, corrected 6);
  NPDExperiment verified and applied (19: kept 8, corrected 11). All nine remaining readers failed. B now 4/13.
- C run 4 (wf_3c3f08c2-582): InsiderExperiment applied (10: kept 9, corrected 1); NPDExperiment
  consolidated (9 findings; 20 claims verified, 6 contradicted, 4 unverifiable) and applied (kept 4,
  corrected 5). All nine locates failed (VRPExperiment inventory file written, treated as not started). C now 4/13.
Next: A run 14, B run 5, C run 5 launched in parallel at 03:41Z.

## 2026-09-05T05:47Z — tools/resume.py
agent A: 10/13 done
agent B: 4/13 done
agent C: 4/13 done
AFTER checks: pre-existing dirt only
prepared A run 15 (provenance/launch-args/agentA-run15.args.json)
prepared B run 6 (provenance/launch-args/agentB-run6.args.json)
prepared C run 6 (provenance/launch-args/agentC-run6.args.json)
Outcomes of A run 14 / B run 5 / C run 5 (launched 03:42Z, cut by the session limit; reset 08:40Z 2026-09-05; laptop rebooted in between, scratchpad snapshots re-verified 13 repos / 1618 files):
- A run 14 (wf_990e6ca4-939): solattn verified and applied (11: kept 4, corrected 7); NPLExperiment verified
  and applied (12: kept 4, corrected 8). Readers for MLCryptoEngine, ORBExperiment, AiTrader failed. A now 10/13.
  Cross-repo leads for solattn (L1-L8) and NPLExperiment (L1-L11) banked from the reopen notes (A leads 97).
- B run 5 (wf_77c4a710-2b4): VRPExperiment and ETFExperiment readers done (one draft + positives ledger each);
  both consolidators failed; all other readers failed. B stays 4/13; run 6 consolidates from the drafts.
- C run 5 (wf_5eccab36-37a): VRPExperiment verification and provenance done, consolidation failed;
  ETFExperiment inventory done, verification failed; seven locates failed. C stays 4/13; run 6 resumes both by stage.
Next: A run 15, B run 6, C run 6 launched in parallel from the prepared args.
Agent A run 15: task ws4kof4qk (wf_2e43f915-89e), launched 05:48Z.
Agent B run 6: task wm5vvibkp (wf_c8c88fdf-277), launched 05:48Z.
Agent C run 6: task wo23ohmlr (wf_f3402ad6-0a6), launched 05:48Z.

## 2026-09-05T18:02Z — tools/resume.py
agent A: 10/13 done
agent B: 4/13 done
agent C: 4/13 done
AFTER checks: pre-existing dirt only
prepared A run 16 (provenance/launch-args/agentA-run16.args.json)
prepared B run 7 (provenance/launch-args/agentB-run7.args.json)
prepared C run 7 (provenance/launch-args/agentC-run7.args.json)
Outcomes of A run 15 / B run 6 / C run 6 (launched 05:48Z, cut by the session limit; reset 10:40Z 2026-09-05):
- A run 15 (wf_2e43f915-89e): MLCryptoEngine readers p1-report, p2-register, p3-progress and ORBExperiment
  readers p1-registration, p2-decisions, p3-progress all wrote their drafts (some died after writing, before
  returning); no consolidation ran. AiTrader readers failed. A stays 10/13; run 16 consolidates both from drafts.
- B run 6 (wf_c8c88fdf-277): VRPExperiment consolidated (13 findings) and ETFExperiment consolidated
  (9 findings), with positives ledgers; both verify stages and the ETFExperiment apply failed; all nine remaining
  readers failed. 28 cross-repo leads banked from the two consolidators (B leads now 54). B stays 4/13.
- C run 6 (wf_f3402ad6-0a6): VRPExperiment consolidated (6 findings; 25 claims verified, 3 contradicted,
  4 unverifiable; provenance 26 supported, 1 not supported, 5 partial), apply failed; ETFExperiment verification
  and provenance done, consolidation pending; seven locates failed. C stays 4/13.
Next: A run 16, B run 7, C run 7 launched in parallel from the prepared args.
Agent A run 16: task w3qlkf1yb (wf_29ed3211-19d), launched 18:02Z.
Agent B run 7: task wuwdh1h0k (wf_1aaac622-79e), launched 18:02Z.
Agent C run 7: task w250dtisj (wf_fbabed09-3b3), launched 18:02Z.

## 2026-09-05T23:01Z — tools/resume.py
agent A: 11/13 done
agent B: 6/13 done
agent C: 5/13 done
AFTER checks: pre-existing dirt only
prepared A run 17 (provenance/launch-args/agentA-run17.args.json)
prepared B run 8 (provenance/launch-args/agentB-run8.args.json)
prepared C run 8 (provenance/launch-args/agentC-run8.args.json)

## 2026-09-05T23:01Z — tools/resume.py
agent A: 11/13 done
agent B: 6/13 done
agent C: 5/13 done
AFTER checks: pre-existing dirt only
prepared A run 18 (provenance/launch-args/agentA-run18.args.json)
prepared B run 9 (provenance/launch-args/agentB-run9.args.json)
prepared C run 9 (provenance/launch-args/agentC-run9.args.json)
Agent A run 17: task wivgbczsc (wf_6001ea88-d6d), launched 23:01Z.
Agent C run 8: task ww760g9m3 (wf_72e77c78-e86), launched 23:01Z.
Outcomes of A run 16 / B run 7 / C run 7 (launched 18:02Z, cut by the session limit; reset 23:00Z 2026-09-05):
- A run 16 (wf_29ed3211-19d): ORBExperiment consolidated, verified and applied (17 findings; the applier wrote
  its outputs before dying). MLCryptoEngine consolidated (17 findings); verify and apply failed. AiTrader readers
  failed again. 26 cross-repo leads banked (A leads 123). A now 11/13.
- B run 7 (wf_1aaac622-79e): VRPExperiment verified and applied (13: kept 5, corrected 8); ETFExperiment verified
  and applied (9: kept 6, corrected 3). PMExperiment readers p1-register and p2-progress wrote drafts and ledgers;
  solclear p1-findings wrote its draft (54,822 bytes, closing sections present) but no positives ledger; all other
  readers failed. B now 6/13.
- C run 7 (wf_fbabed09-3b3): VRPExperiment applied (6: kept 4, corrected 2). ETFExperiment consolidated
  (8 findings; 30 claims verified, 6 contradicted, 2 unverifiable; provenance 20 supported, 5 not supported,
  9 partial); apply failed. Seven locates failed. C now 5/13.
Next: A run 17 and C run 8 launched at 23:01Z. B run 8 waits for a recovery agent (Opus, snapshot only, no
live-repo access, draft not modified) to write the solclear p1-findings positives ledger, then launches with
solclear/p1-findings marked done so the reader is not re-run.
Agent A run 18: task wphdud8k7 (wf_be393c81-acf), launched 23:02Z.
Agent C run 9: task wp3qbdri6 (wf_7d7a8dc6-ffe), launched 23:02Z.

## 2026-09-05T23:07Z — second session stood down (duplicate launches aborted)
A second orchestrator session was opened by the operator after the limit message while the first session
(auto-retrying in tmux) was still alive and had already launched A run 17 (wf_6001ea88-d6d), C run 8
(wf_72e77c78-e86) and a solclear p1-findings ledger recovery agent at 23:01Z. Before noticing this, the
second session ran resume.py a second time (prepared run 18/9/9 args, commit f3b2138; superseded, never
used), launched A run 18 (task wphdud8k7, wf_be393c81-acf) and C run 9 (task wp3qbdri6, wf_7d7a8dc6-ffe)
at 23:02Z, and a second ledger recovery agent at 23:03Z. All three were stopped with TaskStop at ~23:05Z,
about two to three minutes in. Their agents wrote only scratch files under work/agentC-etf-citecheck3/ and
work/agentB-solclear-p1-ledger/ (nothing under findings/); the A run 18 verifier and applier for
MLCryptoEngine wrote nothing. Runs 18 and 9 moved from ACTIVE.json to HISTORY.json marked aborted-duplicate;
AFTER checks "01-agentA-blind-run18-AFTER-aborted" and "03-agentC-blind-run9-AFTER-aborted": only the
pre-existing dirt. The first session was told by cross-session message and remains the sole orchestrator;
A run 17 and C run 8 stay in ACTIVE.json. Rule added to RESUME.md: check ListAgents for a busy peer
program-audit session before running resume.py --runs-dead or launching anything.
Agent B run 8: task wy3jvvj7i (wf_5e8f4f9a-b30), launched 23:12Z.
solclear p1-findings positives ledger recovered (Opus recovery agent, snapshot only, no live-repo access; 47 entries:
shipped 7, positive 11, qualified positive 7, thresholded negative 13, open 9; draft byte-for-byte unchanged).
B run 8 args amended to mark solclear/p1-findings done (provenance/launch-args/agentB-run8.args.json), then launched.
A peer session (5fb0ac) briefly duplicated A run 17 and C run 8 at 23:02-23:05Z before stopping them (see its
entry above, commit 606440e); it reported only scratch writes under work/, nothing under findings/.

## 2026-09-11T02:01Z — tools/resume.py
agent A: 12/13 done
agent B: 6/13 done
agent C: 6/13 done
AFTER checks: pre-existing dirt only
prepared A run 19 (provenance/launch-args/agentA-run19.args.json)
prepared B run 10 (provenance/launch-args/agentB-run10.args.json)
prepared C run 10 (provenance/launch-args/agentC-run10.args.json)
Outcomes of A run 17 / C run 8 / B run 8 (launched 23:01Z and 23:12Z 2026-09-05 by the first session, cut by the
session limit at ~23:49Z; that session was then closed by the operator's decision and this session took over;
laptop off until 2026-09-11, snapshots re-verified 13 repos / 1618 files):
- A run 17 (wf_6001ea88-d6d): MLCryptoEngine verified and applied (17: kept 4, corrected 13). AiTrader readers p1-experiment, p2-return, p3-progress all wrote their drafts; the
  consolidator did not run. A now 12/13; run 19 consolidates AiTrader from the drafts.
- C run 8 (wf_72e77c78-e86): ETFExperiment applied (8: kept 5, corrected 3). PMExperiment and solclear inventories written;
  their verification stages and the five remaining locates failed. C now 6/13.
- B run 8 (wf_5e8f4f9a-b30): PMExperiment consolidated (15 findings) with positives ledger; solclear p2-progress
  reader wrote its draft and ledger (p1-findings ledger recovered earlier); solclear consolidator and PMExperiment
  verify/apply failed; the other readers failed. 10 cross-repo leads banked (B leads now 64). B stays 6/13.
Next: A run 19, B run 10, C run 10 launched in parallel from the prepared args (runs 18/9/9 were the aborted
duplicates; their args files are unused).
Agent A run 19: task wnw8ieasi (wf_a0ca737c-8b6), launched 02:02Z.
Agent B run 10: task wymv8bac7 (wf_184ea9a1-55a), launched 02:02Z.
Agent C run 10: task wtnii7w5y (wf_be87ffc6-5e5), launched 02:02Z.

## 2026-09-12T02:34Z — tools/resume.py
agent A: 12/13 done
agent B: 6/13 done
agent C: 6/13 done
AFTER checks: pre-existing dirt only
prepared A run 20 (provenance/launch-args/agentA-run20.args.json)
prepared B run 11 (provenance/launch-args/agentB-run11.args.json)
prepared C run 11 (provenance/launch-args/agentC-run11.args.json)
Outcomes of A run 19 / B run 10 / C run 10 (launched 02:02Z 2026-09-11; A cut by the session limit at ~02:18Z,
reset 05:40Z; B and C killed when the Claude Code process exited, laptop rebooted 2026-09-12T02:32Z):
- A run 19 (wf_a0ca737c-8b6): AiTrader consolidator failed on the limit after writing a partial AiTrader.md and
  AiTrader.reopen.md (no .json); treated as not consolidated, rerun in run 20. A stays 12/13.
- B run 10 (wf_184ea9a1-55a): solclear consolidator wrote a partial solclear.md (no .json, no positives ledger);
  treated as not consolidated, rerun in run 11. PMExperiment verify/apply did not complete. B stays 6/13.
- C run 10 (wf_be87ffc6-5e5): PMExperiment and solclear verification/provenance agents wrote partial files
  (PMExperiment.claims.json, provenance/*.md) but no verification.md; both stages rerun in run 11. C stays 6/13.
Next: A run 20, B run 11, C run 11 launched in parallel from the prepared args.
Agent A run 20: task w4q52keg5 (wf_6a93ce12-f98), launched 02:35Z.
Agent B run 11: task wfdztn6yy (wf_2eda5146-765), launched 02:35Z.
Agent C run 11: task wftis2chm (wf_501f50e3-299), launched 02:35Z.

## 2026-09-12T07:31Z — tools/resume.py
agent A: 13/13 done
agent B: 7/13 done
agent C: 6/13 done
AFTER checks: pre-existing dirt only
prepared A run 21 (provenance/launch-args/agentA-run21.args.json)
prepared B run 12 (provenance/launch-args/agentB-run12.args.json)
prepared C run 12 (provenance/launch-args/agentC-run12.args.json)
Outcomes of A run 20 / B run 11 / C run 11 (launched 02:35Z 2026-09-12, cut by the session limit at ~03:20Z; reset 07:30Z):
- A run 20 (wf_6a93ce12-f98): AiTrader consolidated, verified and applied (18: kept 6, corrected 12). A now 13/13,
  blind per-repo pass COMPLETE. The cross-repo pass started and failed on the limit; 13 AiTrader leads banked
  (A leads 136). Run 21 runs the cross-repo pass only.
- B run 11 (wf_2eda5146-765): PMExperiment verified and applied (15: kept 7, corrected 8); solclear consolidated (22 findings) and verified, apply failed. Ten readers failed. 11 leads banked
  (B leads 75). B now 7/13.
- C run 11 (wf_501f50e3-299): solclear verified, provenance and consolidated (6 findings; 24 claims verified,
  3 contradicted, 8 unverifiable); PMExperiment verified, provenance and consolidated (8 findings; 34 verified,
  7 contradicted, 14 unverifiable); both applies failed; five locates failed. C stays 6/13 with two repos at apply.
Next: A run 21 (cross-repo), B run 12, C run 12 launched in parallel from the prepared args.
Agent A run 21: task wxc3j9631 (wf_70480361-cfd), launched 07:31Z.
Agent B run 12: task wlokk3xyl (wf_809a265b-e46), launched 07:31Z.
Agent C run 12: task wkuee2l6v (wf_88280fd9-57b), launched 07:31Z.

## 2026-09-12T12:31Z — tools/resume.py
agent A: 13/13 done
agent B: 8/13 done
agent C: 8/13 done
AFTER checks: pre-existing dirt only
prepared B run 13 (provenance/launch-args/agentB-run13.args.json)
prepared C run 13 (provenance/launch-args/agentC-run13.args.json)
Outcomes of A run 21 / B run 12 / C run 12 (launched 07:31Z 2026-09-12 by the auto-resumed earlier session, which was
then closed at 08:12Z by the operator's standing decision; this session holds the orchestrator lock from here on):
- A run 21 (wf_70480361-cfd): cross-repo pass completed and committed by that session as 085ed15 (CROSS_REPO.md/.json,
  7 findings: 3 S3, 4 S4; all 136 leads dispositioned; live-repo status unchanged before/after). Agent A's blind phase
  is complete: 13/13 repositories plus the cross-repo pass.
- B run 12 (wf_809a265b-e46): solclear verified and applied (22 findings); the five remaining readers failed on the limit. B now 8/13.
- C run 12 (wf_88280fd9-57b): PMExperiment applied (8: kept 7, corrected 1) and solclear applied (6: kept 4, corrected 2); NPLExperiment and
  solattn inventories written; their verification stages and the other locates failed on the limit. C now 8/13.
Next: B run 13, C run 13 launched in parallel from the prepared args; nothing to launch for A.
Agent B run 13: task w6w1wi8rd (wf_ea0a475c-55a), launched 12:31Z.
Agent C run 13: task wx3xrwqmj (wf_c31a635b-6c1), launched 12:31Z.

## 2026-09-12T17:31Z — tools/resume.py
agent A: 13/13 done
agent B: 8/13 done
agent C: 8/13 done
AFTER checks: pre-existing dirt only
prepared B run 14 (provenance/launch-args/agentB-run14.args.json)
prepared C run 14 (provenance/launch-args/agentC-run14.args.json)
Outcomes of B run 13 / C run 13 (launched 12:31Z 2026-09-12, cut by the session limit at ~13:20Z; reset 17:30Z):
- B run 13 (wf_ea0a475c-55a): solattn readers done and consolidated (13 findings) with positives ledger, verify failed;
  NPLExperiment readers done and consolidated (17 findings; the consolidator wrote its outputs before dying). Readers
  for MLCryptoEngine, ORBExperiment, AiTrader failed. 7 cross-repo leads banked (B leads now 82). B stays 8/13.
- C run 13 (wf_c31a635b-6c1): solattn verified, provenance done and consolidated (6 findings; 26 claims verified,
  2 contradicted, 5 unverifiable); NPLExperiment verified, provenance done and consolidated (11 findings; 56 verified,
  17 contradicted, 4 unverifiable); both applies failed. Locates for MLCryptoEngine, ORBExperiment, AiTrader failed.
  C stays 8/13.
Next: B run 14, C run 14 launched in parallel from the prepared args.
Agent B run 14: task w86tzg1v4 (wf_03aec5c0-372), launched 17:31Z.
Agent C run 14: task wnne7gngh (wf_80d0a649-3b8), launched 17:31Z.

## 2026-09-12T22:31Z — tools/resume.py
agent A: 13/13 done
agent B: 10/13 done
agent C: 10/13 done
AFTER checks: pre-existing dirt only
prepared B run 15 (provenance/launch-args/agentB-run15.args.json)
prepared C run 15 (provenance/launch-args/agentC-run15.args.json)
Outcomes of B run 14 / C run 14 (launched 17:31Z 2026-09-12, cut by the session limit at ~18:25Z; reset 22:30Z):
- B run 14 (wf_03aec5c0-372): solattn verified and applied (13: kept 10, corrected 3); NPLExperiment verified and
  applied (17: kept 6, corrected 11). MLCryptoEngine p1-report reader wrote draft and ledger; MLCryptoEngine
  p2-register and p3-progress and ORBExperiment p1-registration, p2-decisions, p3-progress readers wrote complete
  drafts (closing sections present) but died before their positives ledgers; AiTrader readers failed. B now 10/13.
  Recovery: five follow-up Opus agents write the five ledgers from the drafts plus the snapshots, no live-repo
  access, drafts not modified, each ledger ending with a recovery note; B run 15 then launches with all six
  MLCryptoEngine/ORBExperiment parts marked done so the consolidators run directly.
- C run 14 (wf_80d0a649-3b8): solattn applied (6: kept 5, corrected 1); NPLExperiment applied (11: kept 5,
  corrected 6). MLCryptoEngine and ORBExperiment inventories written, verification/provenance failed; AiTrader
  locate failed. C now 10/13.
Next: C run 15 launched now; B run 15 after the ledger recovery.
Agent C run 15: task w1g0lu1f9 (wf_5fc34499-d67), launched 22:32Z.
Ledger recovery (22:33Z-22:50Z 2026-09-12): five follow-up Opus agents wrote MLCryptoEngine p2-register (37 entries)
and p3-progress (38) and ORBExperiment p1-registration (40), p2-decisions (49) and p3-progress (29) positives ledgers
from the drafts and the snapshots; drafts unchanged (git diff empty); no live-repository access; each ledger carries
the recovery note; committed as 14e0f7a. AFTER check "02-agentB-ledger-recovery-AFTER": only the pre-existing dirt.
B run 15 args: MLCryptoEngine and ORBExperiment all three parts done, consolidators run directly; AiTrader readers.
Agent B run 15: task wka7otvpo (wf_ce3f1fe3-fb8), launched 22:48Z.

## 2026-09-13T08:55Z — tools/resume.py
agent A: 13/13 done
agent B: 10/13 done
agent C: 10/13 done
AFTER checks: pre-existing dirt only
prepared B run 16 (provenance/launch-args/agentB-run16.args.json)
prepared C run 16 (provenance/launch-args/agentC-run16.args.json)
Outcomes of B run 15 / C run 15 (launched 22:48Z and 22:32Z 2026-09-12, cut by the session limit at ~23:05Z; reset
03:30Z 2026-09-13; laptop then off until ~08:55Z, snapshots re-verified):
- B run 15 (wf_ce3f1fe3-fb8): MLCryptoEngine and ORBExperiment consolidators (from the six drafts and recovered
  ledgers) and the three AiTrader readers all failed on the limit before writing anything. B stays 10/13.
- C run 15 (wf_5fc34499-d67): MLCryptoEngine provenance done, verification failed; ORBExperiment verification and
  provenance done, consolidation failed; AiTrader locate failed. C stays 10/13.
Next: B run 16 (same args as run 15), C run 16 launched in parallel.
