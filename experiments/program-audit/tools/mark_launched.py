#!/usr/bin/env python3
"""Record a workflow launch so tools/resume.py can AFTER-check it after a crash or reboot.

Usage: tools/mark_launched.py <A|B|C|seeded-A|seeded-B|seeded-C|adj|D> <run> <task-id> <workflow-id>
Appends to provenance/launch-args/ACTIVE.json and one line to provenance/RUN_LOG.md.
"""
import datetime, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ACTIVE = os.path.join(ROOT, 'provenance', 'launch-args', 'ACTIVE.json')
RUN_LOG = os.path.join(ROOT, 'provenance', 'RUN_LOG.md')
PREFIX = {'A': '01-agentA-blind', 'B': '02-agentB-blind', 'C': '03-agentC-blind',
          'seeded-A': '04-agentA-seeded', 'seeded-B': '05-agentB-seeded', 'seeded-C': '06-agentC-seeded',
          'adj': '07-agentC-adjudicate', 'D': '08-agentD-proposals'}
NAME = {'A': 'Agent A', 'B': 'Agent B', 'C': 'Agent C', 'seeded-A': 'Agent A seeded', 'seeded-B': 'Agent B seeded',
        'seeded-C': 'Agent C seeded', 'adj': 'Agent C adjudication', 'D': 'Agent D'}


def main():
    if len(sys.argv) != 5 or sys.argv[1] not in PREFIX:
        sys.exit(__doc__)
    agent, run, task, wf = sys.argv[1], int(sys.argv[2]), sys.argv[3], sys.argv[4]
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ')
    entry = {'agent': agent, 'run': run, 'label': f'{PREFIX[agent]}-run{run}', 'task': task, 'wf': wf, 'launched': now}
    active = json.load(open(ACTIVE)) if os.path.isfile(ACTIVE) else []
    active = [e for e in active if not (e['agent'] == agent and e['run'] == run)] + [entry]
    json.dump(active, open(ACTIVE, 'w'), indent=1)
    with open(RUN_LOG, 'a') as f:
        f.write(f"{NAME[agent]} run {run}: task {task} ({wf}), launched {now[11:]}.\n")
    print(json.dumps(entry))


if __name__ == '__main__':
    main()
