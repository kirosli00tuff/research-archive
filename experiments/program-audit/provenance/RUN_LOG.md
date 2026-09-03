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
