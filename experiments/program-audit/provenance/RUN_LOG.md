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
