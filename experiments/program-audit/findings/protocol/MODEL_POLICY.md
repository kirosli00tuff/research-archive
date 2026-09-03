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
