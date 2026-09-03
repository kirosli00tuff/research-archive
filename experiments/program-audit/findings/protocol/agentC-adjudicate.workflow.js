export const meta = {
  name: 'agentC-adjudicate',
  description: 'Agent C job three: rule on every Agent A and Agent B finding (blind, cross-repo, seeded) per repository; adjudicate A/B contradictions explicitly',
  phases: [
    { title: 'Rule', detail: 'per repository, two adjudicators: one over the A set, one over the B set' },
    { title: 'Reconcile', detail: 'per repository: contradictions between A and B on the same entry, final rulings file' },
  ],
}

const RULES_PATH = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/COMMON_RULES.md'
const SNAP = '/tmp/claude-1000/-home-kiros-li-Documents-GitHub-program-audit/5ca157a0-1746-4eb9-a1b8-f3732ea42bf4/scratchpad/snap'
const F = '/home/kiros-li/Documents/GitHub/program-audit/findings'
const OUT = F + '/agentC/adjudication'
const REPOS = ['retail-power-limits','HFExperiment','InsiderExperiment','NPDExperiment','VRPExperiment','ETFExperiment','solclear','PMExperiment','solattn','NPLExperiment','MLCryptoEngine','ORBExperiment','AiTrader']
const BATCH = 2

const ROLE = `
YOU ARE AGENT C, the referee, in its final job: ADJUDICATION. You have no thesis. Agent A argued the
program closed too early; Agent B argued it claimed too much. Only now may Agent C read their
output. Your rulings rest on the anchored snapshots, the live git history and untracked data
(read-only), Agent C's own verification and provenance work (${F}/agentC/verification/,
${F}/agentC/provenance/, ${F}/agentC/<repo>.md, ${F}/agentC/seeded/), and recomputation in the
Python venv where needed. A ruling is never a vote; it is a statement about evidence.
Rulings: UPHELD (the finding is correct as stated); UPHELD_WITH_CORRECTION (the substance stands
but a figure, line, severity, class, label or scope must change — state the corrected values);
NOT_UPHELD (the evidence does not support the finding, or the authors' text already handles it in
a way the finding ignores, or the arithmetic is wrong — show why); UNRESOLVABLE_ON_AVAILABLE_EVIDENCE
(state exactly what evidence would settle it and where it would come from).
A finding that merely restates a limitation the authors disclosed must be ruled
UPHELD_WITH_CORRECTION (label READ, severity at most S3, note the disclosure) if the finding failed
to say so, or UPHELD if it said so. Do not soften a correct S1 because the authors are diligent
elsewhere; do not uphold an S1 because the thesis is attractive.
`

function rulePrompt(repo, agentLetter) {
  const dir = F + '/agent' + agentLetter
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
TASK: rule on EVERY finding by Agent ${agentLetter} that concerns repository ${repo}. Collect them
with a small script (python3, read-only) from: ${dir}/${repo}.json (blind), ${dir}/CROSS_REPO.json
(entries whose "repo" is ${repo}), and every ${dir}/seeded/*.json and ${dir}/seeded/CHECK3_intervals/*.json
(entries whose "repo" is ${repo}). Then read the corresponding markdown blocks in ${dir}/${repo}.md,
${dir}/CROSS_REPO.md and ${dir}/seeded/*.md for the full text. Also read Agent ${agentLetter}'s
"found sound" and "dropped" sections for ${repo}: a dropped finding is not ruled on, but note if
the same claim reappears.
For EACH finding: re-open the cited source in ${SNAP}/${repo}/ (and the other repository's snapshot
for cross-repo findings), check the quote, the figures and n, and the reasoning; consult Agent C's
own verification/provenance/seeded results for ${repo}; recompute where the finding rests on
arithmetic; then rule. Write the reasoning so a reader can follow it without the finding in front
of them: quote the key line, give the figure with n, cite file:line, and state the ruling.
OUTPUT: ${OUT}/_partial/${repo}.${agentLetter}.md (one section per finding: ID, one-line claim,
ruling, corrected fields if any, reasoning, evidence refs, what would settle it if unresolvable)
and ${OUT}/_partial/${repo}.${agentLetter}.json: array of {finding_id, agent, repo, source
(blind|cross_repo|seeded), original_severity, original_class, original_label, ruling,
corrected_severity, corrected_class, corrected_label, reasoning, evidence_refs (array),
would_settle (string or null), relies_on_agentC_ref (string or null)}. If Agent ${agentLetter}
raised no finding for ${repo}, write both files saying so and listing what Agent ${agentLetter}
reported as sound. Return counts by ruling.`
}

const RECONCILE_SCHEMA = { type: 'object', properties: {
  repo: { type: 'string' }, ruled: { type: 'integer' },
  upheld: { type: 'integer' }, upheld_with_correction: { type: 'integer' }, not_upheld: { type: 'integer' }, unresolvable: { type: 'integer' },
  contradictions: { type: 'integer' }, agreements: { type: 'integer' } },
  required: ['repo','ruled','upheld','upheld_with_correction','not_upheld','unresolvable','contradictions','agreements'] }

function reconcilePrompt(repo) {
  return `First run: cat ${RULES_PATH}   and follow every rule in it.
${ROLE}
RECONCILE task for repository ${repo}. Inputs: ${OUT}/_partial/${repo}.A.md/.json and
${OUT}/_partial/${repo}.B.md/.json (Agent C's own partial rulings), plus the original findings in
${F}/agentA and ${F}/agentB for ${repo} where you need the text.
 1. CONTRADICTIONS: identify every entry (hypothesis, artifact, closure, figure) on which Agent A
    and Agent B raised findings that cannot both be right (A says closed too early, B says the same
    closure was too generous; A says a blocker expired, B says the blocker was never the real
    reason; A and B cite different figures for the same quantity). For each: name both IDs, state
    the contradiction in one sentence, adjudicate EXPLICITLY (which side the evidence supports, or
    neither, or both partially), and state what evidence would settle it. Re-open the sources.
 2. AGREEMENTS: identify every entry where A and B independently raised the same underlying point
    (possibly with opposite framing). List the ID pairs. These feed the agreement matrix.
 3. FINAL RULINGS: merge the partial rulings into ${OUT}/${repo}.md (sections: Summary counts,
    Contradictions adjudicated, Independent agreements, Rulings on Agent A findings, Rulings on
    Agent B findings) and ${OUT}/${repo}.json: array of the ruling objects from both partials,
    each augmented with "contradicts" (array of IDs) and "agrees_with" (array of IDs). Do not change
    a partial ruling unless the contradiction analysis requires it; if you do, record the change and
    the reason in the reasoning field.
Return the counts.`
}

// Disk-state driven skipping (see agentA-blind.workflow.js): tools/agent_state.py <adjdir>
// --adjudication passes {done_repos, rules_done:{repo:['A','B']}} as args; every launch is fresh.
const STATE = args || {}
const DONE_REPOS = new Set(STATE.done_repos || [])
const RULES_DONE = STATE.rules_done || {}
async function repoChain(repo) {
  if (DONE_REPOS.has(repo)) { log(`${repo}: adjudication on disk, skipped`); return { repo, stage: 'done', rec: { repo, on_disk: true } } }
  const rd = new Set(RULES_DONE[repo] || [])
  if (rd.size) log(`${repo}: rule ${[...rd].join('/')} partial(s) on disk, skipped`)
  const [a, b] = await parallel([
    () => rd.has('A') ? Promise.resolve('on-disk') : agent(rulePrompt(repo, 'A'), { label: `C-rule-A:${repo}`, phase: 'Rule' }),
    () => rd.has('B') ? Promise.resolve('on-disk') : agent(rulePrompt(repo, 'B'), { label: `C-rule-B:${repo}`, phase: 'Rule' }),
  ])
  if (!a || !b) return { repo, stage: 'rule-failed', a: !!a, b: !!b }
  const rec = await agent(reconcilePrompt(repo), { label: `C-reconcile:${repo}`, phase: 'Reconcile', schema: RECONCILE_SCHEMA })
  return { repo, stage: rec ? 'done' : 'reconcile-failed', rec }
}

phase('Rule')
const out = []
for (let i = 0; i < REPOS.length; i += BATCH) {
  const batch = REPOS.slice(i, i + BATCH)
  log(`batch ${i / BATCH + 1}: ${batch.join(', ')}`)
  const res = await parallel(batch.map(r => () => repoChain(r)))
  out.push(...res.filter(Boolean))
}
const incomplete = out.filter(r => r.stage !== 'done').map(r => `${r.repo}:${r.stage}`)
if (incomplete.length) log(`incomplete: ${incomplete.join(', ')}; resume after the limit resets`)
return out.map(r => r.rec || { repo: r.repo, stage: r.stage })
