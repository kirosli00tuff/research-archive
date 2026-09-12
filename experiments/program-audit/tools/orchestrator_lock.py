#!/usr/bin/env python3
"""Exactly one live Claude session orchestrates the audit.

Why: claude-auto-retry keeps an old session alive in a detached tmux session and resumes it after a
limit reset, so an operator who opens a new terminal after a "session limit" message ends up with two
orchestrators launching the same workflows onto the same output files (happened 2026-09-05 and 2026-09-12).

Lock file (outside git, survives reboots because the pid then no longer exists):
  /home/kiros-li/.cache/program-audit/scratchpad/ORCHESTRATOR.json
  {"pid": <claude pid>, "start": <process start ticks>, "tmux": <session name>, "claimed": <utc>, "session_url": <str>}
A holder is live when that pid exists, is a claude process, and has the recorded start time (so a
reused pid after a reboot is not mistaken for the holder).

CLI:  tools/orchestrator_lock.py --check    exit 1 and explain if another live session holds the lock
      tools/orchestrator_lock.py --release  delete the lock (only the holder, or if the holder is dead)
"""
import datetime, json, os, subprocess, sys

LOCK = os.environ.get('PROGRAM_AUDIT_LOCK', '/home/kiros-li/.cache/program-audit/scratchpad/ORCHESTRATOR.json')


def _cmdline(pid):
    try:
        return open(f'/proc/{pid}/cmdline', 'rb').read().replace(b'\0', b' ').decode(errors='replace')
    except OSError:
        return ''


def _stat_fields(pid):
    try:
        return open(f'/proc/{pid}/stat').read().rsplit(')', 1)[1].split()
    except (OSError, IndexError):
        return []


def _ppid(pid):
    f = _stat_fields(pid)
    return int(f[1]) if len(f) > 1 else 0


def _starttime(pid):
    f = _stat_fields(pid)
    return int(f[19]) if len(f) > 19 else None


def ancestors(pid):
    out = []
    while pid > 1 and len(out) < 40:
        out.append(pid)
        pid = _ppid(pid)
    return out


def is_claude(pid):
    c = _cmdline(pid)
    return bool(c) and ('/claude ' in c or c.rstrip().endswith('/claude') or c.startswith('claude '))


def my_claude_pid():
    for p in ancestors(os.getpid()):
        if is_claude(p):
            return p
    return None


def tmux_session_of(pid):
    r = subprocess.run(['tmux', 'list-panes', '-a', '-F', '#{session_name} #{pane_pid}'], capture_output=True, text=True)
    if r.returncode:
        return None
    anc = set(ancestors(pid))
    for line in r.stdout.splitlines():
        name, pane_pid = line.rsplit(' ', 1)
        if pane_pid.isdigit() and int(pane_pid) in anc:
            return name
    return None


def holder():
    try:
        d = json.load(open(LOCK))
    except (OSError, ValueError):
        return None
    return d if isinstance(d, dict) and isinstance(d.get('pid'), int) else None


def holder_is_live(h):
    return is_claude(h['pid']) and (h.get('start') is None or _starttime(h['pid']) == h['start'])


def live_other_holder():
    h = holder()
    if not h or not holder_is_live(h):
        return None
    me = my_claude_pid()
    return None if me is not None and h['pid'] == me else h


def claim(session_url=''):
    me = my_claude_pid() or os.getpid()
    d = {'pid': me, 'start': _starttime(me), 'tmux': tmux_session_of(me),
         'claimed': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%MZ'), 'session_url': session_url}
    os.makedirs(os.path.dirname(LOCK), exist_ok=True)
    json.dump(d, open(LOCK, 'w'), indent=1)
    return d


def explain(h):
    t = h.get('tmux') or tmux_session_of(h['pid']) or '<no tmux session found>'
    return (f"ORCHESTRATOR LOCK: another live Claude session holds the audit (claude pid {h['pid']}, tmux {t}, "
            f"claimed {h.get('claimed')}, {h.get('session_url') or 'no session url'}).\n"
            f"Stand down and let it finish. If the operator has decided this session takes over, close it with\n"
            f"    tmux kill-session -t {t}\n"
            f"after its runs have ended (or if it is only waiting on a limit with no live runs), then re-run.")


def refuse_if_other(session_url=''):
    h = live_other_holder()
    if h:
        sys.exit(explain(h))
    return claim(session_url)


def main():
    if '--release' in sys.argv:
        h = holder()
        if h and holder_is_live(h) and h['pid'] != my_claude_pid():
            sys.exit(explain(h))
        if os.path.isfile(LOCK):
            os.remove(LOCK)
        print('lock released')
        return
    h = live_other_holder()
    if h:
        sys.exit(explain(h))
    cur = holder()
    print('no other live orchestrator; ' + (f"lock held by this session (pid {cur['pid']}, tmux {cur.get('tmux')})" if cur and holder_is_live(cur) else 'lock free or stale'))


if __name__ == '__main__':
    main()
