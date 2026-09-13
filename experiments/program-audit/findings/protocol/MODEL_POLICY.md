# Model policy (operator instruction, 2026-09-03 00:45Z)

Operator: "run fable for all analysis. downgrade to opus if the task is more mundane and less
logic required."

Applied as follows. Every agent that reads evidence and forms a judgement runs on Fable 5.1
(the session model, inherited when no model is given). Agents whose task is mechanical run on
Opus 5 (`model: 'opus'`).

| Workflow | Fable 5.1 (analysis) | Opus 5 (mechanical) |
|---|---|---|
| Agent A blind | readers (A-read:*), cross-repository pass | consolidators, both citation verifiers, appliers |
| Agent B blind | readers (B-read:*), cross-repository pass | consolidators, both citation verifiers, appliers |
| Agent C blind | numeric verification (C-verify), provenance (C-provenance) | inventory (C-locate), consolidators, citation checker, applier |
| Seeded checks (A, B, C) | checks 1-6 including per-repo check 3 | triage extraction, check-3 merge |
| Agent C adjudication | rule-A, rule-B, reconcile | none |
| Agent D | D1 merge, D2 proposers and ranker, D3 generators and screeners, D4-D5 | D1 per-repo extraction, candidate collection, screening-file write |

Rationale for each Opus assignment: the task is grep-and-compare (does the quote exist at the
line, does the figure match), merge-and-format (assign IDs, enforce field order, keep json in sync),
or tabulation (list every CI/correction/prior with file:line). None of them decides whether a
finding is true. Where a mechanical agent's output turns out to need judgement (a disputed
correction), the applier is instructed to re-check the source itself, and Agent C adjudicates
every A and B finding on Fable regardless.

Agent A run 3 (wf_e113872d-e9e) started before this instruction with all roles on Fable; it was
stopped after its first two readers completed and resumed under this policy, so the two completed
Fable readers were kept and every later mechanical agent ran on Opus.

## Revision 2 (operator instruction, 2026-09-03 19:30Z)

Operator: "im already at 80% fable limit weekly, and we were planning on running all 3 agents. use
fable sparingly please."

Applied from Agent A run 9 onward. Every agent carries an explicit `model: 'opus'` except three
single-shot judgement steps, which omit the model and inherit the session model (Fable 5.1 while
the session runs on Fable; whatever the operator selects with /model otherwise):

| Workflow | inherits session model (Fable if the session is Fable) | Opus 5 (explicit) |
|---|---|---|
| Agent A blind | cross-repository pass (A-cross-repo) | readers, consolidators, verifiers, appliers |
| Agent B blind | cross-repository pass (B-cross-repo) | readers, consolidators, verifiers, appliers |
| Agent C blind | none | inventory, numeric verification, provenance, consolidators, checker, applier |
| Seeded checks (A, B, C) | none | triage, checks 1-6, check-3 merge |
| Agent C adjudication | none | rule-A, rule-B, reconcile |
| Agent D | D4-D5 verdict and recommendation | D1 extraction and merge, D2 proposers and ranker, D3 generators, collection, screeners, writer |

The orchestrating session itself is Fable 5.1 and is the largest remaining Fable consumer; the
operator can move it to Opus with /model at any time, which also moves the three inheriting agents.
Fable outputs already on disk are kept: Agent A readers for retail-power-limits, HFExperiment,
InsiderExperiment and NPDExperiment (runs 3-6). Agent A run 8 (wf_c79bd45f-a47) was stopped at
19:27Z with the VRPExperiment and ETFExperiment readers about three minutes in on Fable; their partial
work was discarded and they re-run on Opus in run 9. Every finding therefore records which model
produced it only through this file and RUN_LOG.md: readers on Fable for the four repositories named
above, Opus for the other nine and for every Agent B and C reader.
