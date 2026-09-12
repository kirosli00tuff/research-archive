#!/usr/bin/env python3
"""Unit tests for tools/orchestrator_lock.py (run: python3 tools/test_orchestrator_lock.py)."""
import json, os, sys, tempfile, unittest
from unittest import mock

TMP = tempfile.mkdtemp()
os.environ['PROGRAM_AUDIT_LOCK'] = os.path.join(TMP, 'ORCHESTRATOR.json')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import orchestrator_lock as ol  # noqa: E402


class LockTests(unittest.TestCase):
    def setUp(self):
        if os.path.isfile(ol.LOCK):
            os.remove(ol.LOCK)

    def write_holder(self, pid, start=1):
        json.dump({'pid': pid, 'start': start, 'tmux': 'claude-retry-fake', 'claimed': 'x'}, open(ol.LOCK, 'w'))

    def test_refuses_when_another_live_claude_holds_the_lock(self):
        self.write_holder(999999, start=1)
        with mock.patch.object(ol, 'is_claude', return_value=True), mock.patch.object(ol, '_starttime', return_value=1), \
             mock.patch.object(ol, 'my_claude_pid', return_value=123):
            with self.assertRaises(SystemExit) as cm:
                ol.refuse_if_other('url')
        self.assertIn('claude-retry-fake', str(cm.exception))
        self.assertIn('999999', str(cm.exception))

    def test_proceeds_and_claims_when_holder_is_dead(self):
        self.write_holder(999999)
        d = ol.refuse_if_other('url')
        self.assertEqual(d, json.load(open(ol.LOCK)))
        self.assertIsInstance(d['pid'], int)

    def test_proceeds_when_holder_is_this_session(self):
        first = ol.claim('url1')
        second = ol.refuse_if_other('url2')
        self.assertEqual(first['pid'], second['pid'])
        self.assertEqual(json.load(open(ol.LOCK))['session_url'], 'url2')

    def test_reused_pid_with_different_start_time_is_not_live(self):
        self.write_holder(999999, start=1)
        with mock.patch.object(ol, 'is_claude', return_value=True), mock.patch.object(ol, '_starttime', return_value=2):
            self.assertIsNone(ol.live_other_holder())

    def test_no_lock_file_means_free(self):
        self.assertIsNone(ol.live_other_holder())

    def test_corrupt_lock_file_means_free(self):
        open(ol.LOCK, 'w').write('{not json')
        self.assertIsNone(ol.live_other_holder())


if __name__ == '__main__':
    unittest.main()
