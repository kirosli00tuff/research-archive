#!/usr/bin/env python3
"""Scan an agent's output directory and print, as JSON, what is already complete on disk.

Usage: tools/agent_state.py <outdir> --ledger reopen|positives

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


def main():
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
