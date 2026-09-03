#!/usr/bin/env python3
"""Scan an agent's output directory and print, as JSON, what is already complete on disk.

Usage: tools/agent_state.py <outdir> --ledger reopen|positives   (agents A and B)
       tools/agent_state.py <outdir> --agent C                  (agent C blind chain)
       tools/agent_state.py <outdir> --seeded                   (seeded checks, any agent)
       tools/agent_state.py <adjdir> --adjudication             (agent C adjudication)

Output: {"done_repos": [...], "done_parts": {repo: [part, ...]}, "leads": ["repo: lead", ...]}
Passed verbatim as `args` to the agent's workflow script, which then skips completed work.
Rationale: the workflow runtime's resume cache is positional (longest unchanged prefix of agent
calls); with concurrent chains and partial failures the call order shifts and completed agents
re-run, overwriting verified output. Disk state is the ground truth instead.
"""
import json, os, re, sys

MIN_DRAFT_BYTES = 400
LEADS_HEADING = '## Leads for the cross-repository pass'


def repo_is_done(outdir, repo):
    jp = os.path.join(outdir, f'{repo}.json')
    mp = os.path.join(outdir, f'{repo}.md')
    if not (os.path.isfile(jp) and os.path.isfile(mp)):
        return False
    try:
        data = json.load(open(jp))
    except Exception:
        return False
    if isinstance(data, list) and len(data) == 0:
        return True  # consolidator found nothing; no verification stage exists
    return 'Citation check' in open(mp, encoding='utf-8', errors='replace').read()


def parts_done(outdir, repo, ledger):
    d = os.path.join(outdir, '_drafts', repo)
    if not os.path.isdir(d):
        return []
    done = []
    for f in sorted(os.listdir(d)):
        if not f.endswith('.md') or f.endswith(f'.{ledger}.md'):
            continue
        part = f[:-3]
        draft = os.path.join(d, f)
        led = os.path.join(d, f'{part}.{ledger}.md')
        if os.path.getsize(draft) >= MIN_DRAFT_BYTES and os.path.isfile(led):
            done.append(part)
    return done


def leads_from_md(outdir, repo):
    mp = os.path.join(outdir, f'{repo}.md')
    if not os.path.isfile(mp):
        return []
    text = open(mp, encoding='utf-8', errors='replace').read()
    i = text.find(LEADS_HEADING)
    if i < 0:
        return []
    body = text[i + len(LEADS_HEADING):]
    m = re.search(r'\n## ', body)
    body = body[:m.start()] if m else body
    return [f'{repo}: ' + ln.lstrip('-* ').strip() for ln in body.splitlines() if ln.strip().startswith(('-', '*'))]


def c_state(outdir):
    """Agent C: per-repository stage completion for the locate -> verify|provenance -> consolidate -> check/apply chain."""
    vd, pd = os.path.join(outdir, 'verification'), os.path.join(outdir, 'provenance')
    repos = set()
    for d, suf in ((vd, '.inventory.json'), (pd, '.json')):
        if os.path.isdir(d):
            repos |= {f[:-len(suf)] for f in os.listdir(d) if f.endswith(suf)}
    repos |= {f[:-5] for f in os.listdir(outdir) if f.endswith('.json') and not f.startswith('INDEX')}
    state = {'done_repos': [], 'stages': {}}
    for r in sorted(repos):
        st = {
            'inventory': os.path.isfile(os.path.join(vd, f'{r}.inventory.md')) and os.path.isfile(os.path.join(vd, f'{r}.inventory.json')),
            'verification': os.path.isfile(os.path.join(vd, f'{r}.verification.md')) and os.path.isfile(os.path.join(vd, f'{r}.claims.json')),
            'provenance': os.path.isfile(os.path.join(pd, f'{r}.md')) and os.path.isfile(os.path.join(pd, f'{r}.json')),
            'consolidated': os.path.isfile(os.path.join(outdir, f'{r}.json')) and os.path.isfile(os.path.join(outdir, f'{r}.md')),
            'n_findings': None,
        }
        if st['consolidated']:
            try:
                data = json.load(open(os.path.join(outdir, f'{r}.json')))
                st['n_findings'] = len(data) if isinstance(data, list) else None
            except Exception:
                st['consolidated'] = False
        if st['consolidated'] and (st['n_findings'] == 0 or 'Citation check' in open(os.path.join(outdir, f'{r}.md'), encoding='utf-8', errors='replace').read()):
            state['done_repos'].append(r)
        elif any(st.values()):
            state['stages'][r] = st
    return state


SEEDED_FILES = {1: 'CHECK1_multiplicity', 2: 'CHECK2_endpoint_independence', 4: 'CHECK4_carried_vs_measured',
                5: 'CHECK5_calibration', 6: 'CHECK6_cross_repository_propagation'}


def seeded_state(outdir):
    """Seeded checks: triage per repo, check3 per repo, checks 1/2/4/5/6 and the check3 merge."""
    def js(*parts):
        return os.path.isfile(os.path.join(outdir, *parts))
    tri = os.path.join(outdir, '_triage')
    c3 = os.path.join(outdir, 'CHECK3_intervals')
    return {
        'triage_done': sorted(f[:-5] for f in os.listdir(tri) if f.endswith('.json') and js('_triage', f[:-5] + '.md')) if os.path.isdir(tri) else [],
        'check3_done': sorted(f[:-5] for f in os.listdir(c3) if f.endswith('.json') and js('CHECK3_intervals', f[:-5] + '.md')) if os.path.isdir(c3) else [],
        'checks_done': [k for k, name in SEEDED_FILES.items() if js(name + '.json') and js(name + '.md')],
        'c3merge_done': js('CHECK3_intervals.json') and js('CHECK3_intervals.md'),
    }


def adjudication_state(adjdir):
    """Agent C adjudication: rule-A / rule-B partials and the reconciled per-repository output."""
    part = os.path.join(adjdir, '_partial')
    done = sorted(f[:-5] for f in os.listdir(adjdir) if f.endswith('.json') and os.path.isfile(os.path.join(adjdir, f[:-5] + '.md'))) if os.path.isdir(adjdir) else []
    partial = {}
    if os.path.isdir(part):
        for f in os.listdir(part):
            m = re.match(r'^(.+)\.([AB])\.json$', f)
            if m and os.path.isfile(os.path.join(part, f'{m.group(1)}.{m.group(2)}.md')) and m.group(1) not in done:
                partial.setdefault(m.group(1), []).append(m.group(2))
    return {'done_repos': done, 'rules_done': {k: sorted(v) for k, v in partial.items()}}


def main():
    if len(sys.argv) >= 3 and sys.argv[2] == '--adjudication':
        print(json.dumps(adjudication_state(sys.argv[1]), indent=1)); return
    if len(sys.argv) >= 3 and sys.argv[2] == '--seeded':
        print(json.dumps(seeded_state(sys.argv[1]), indent=1)); return
    if len(sys.argv) >= 4 and sys.argv[2] == '--agent' and sys.argv[3] == 'C':
        print(json.dumps(c_state(sys.argv[1]), indent=1)); return
    if len(sys.argv) < 4 or sys.argv[2] != '--ledger' or sys.argv[3] not in ('reopen', 'positives'):
        sys.exit(__doc__)
    outdir, ledger = sys.argv[1], sys.argv[3]
    repos = sorted({f[:-5] for f in os.listdir(outdir) if f.endswith('.json') and not f.startswith(('CROSS_REPO', 'INDEX'))} |
                   set(os.listdir(os.path.join(outdir, '_drafts'))) if os.path.isdir(os.path.join(outdir, '_drafts')) else set())
    state = {'done_repos': [], 'done_parts': {}, 'leads': []}
    for r in repos:
        if repo_is_done(outdir, r):
            state['done_repos'].append(r)
            state['leads'].extend(leads_from_md(outdir, r))
        else:
            p = parts_done(outdir, r, ledger)
            if p:
                state['done_parts'][r] = p
    print(json.dumps(state, indent=1))


if __name__ == '__main__':
    main()
