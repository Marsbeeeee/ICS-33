import unittest
from pathlib import Path
import sys
import project1


class DummyIO:
    def __init__(self):
        self.data = []
    def write(self, s):
        self.data.append(s)
    def flush(self):
        pass
    def getvalue(self):
        return ''.join(self.data)

class TestProject1(unittest.TestCase):
    def capture_stdout(self, func, *args, **kwargs):
        buf = DummyIO()
        real = sys.stdout
        sys.stdout = buf
        try:
            try:
                func(*args, **kwargs)
            except SystemExit:
                pass
        finally:
            sys.stdout = real
        return buf.getvalue()

    def _write_file(self, name: str, text: str) -> Path:
        p = Path(name)
        p.write_text(text, encoding = 'utf-8')
        return p

    def test_read_input_file_path_plain(self):
        project1.input = lambda: 'fake\path.txt'
        p = project1._read_input_file_path()
        self.assertIsInstance(p, Path)
        self.assertEqual(str(p), 'fake\path.txt')

    def test_main_file_not_found(self):
        project1.input = lambda: 'this_file_does_not_exist_12345.txt'
        out = self.capture_stdout(project1.main)
        self.assertIn('FILE NOT FOUND', out)

    def test_sample_sanity_exact(self):
        content = (
            'LENGTH 900\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 100\n'
            'PROPAGATE 2 1 100\n'
            'ALERT 1 Badness 200\n'
            'CANCEL 1 Badness 450\n'
        )
        p = self._write_file('sample_input.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        expected = [
            '@200: #1 SENT ALERT TO #2: Badness',
            '@300: #2 RECEIVED ALERT FROM #1: Badness',
            '@300: #2 SENT ALERT TO #1: Badness',
            '@400: #1 RECEIVED ALERT FROM #2: Badness',
            '@400: #1 SENT ALERT TO #2: Badness',
            '@450: #1 SENT CANCELLATION TO #2: Badness',
            '@500: #2 RECEIVED ALERT FROM #1: Badness',
            '@500: #2 SENT ALERT TO #1: Badness',
            '@550: #2 RECEIVED CANCELLATION FROM #1: Badness',
            '@550: #2 SENT CANCELLATION TO #1: Badness',
            '@600: #1 RECEIVED ALERT FROM #2: Badness',
            '@650: #1 RECEIVED CANCELLATION FROM #2: Badness',
            '@900: END',
        ]
        lines = [ln for ln in out.splitlines() if ln.strip()]
        self.assertEqual(lines, expected)

    def test_recv_before_send_same_time(self):
        content = (
            'LENGTH 30\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 10\n'
            'PROPAGATE 2 1 10\n'
            'ALERT 1 X 0\n'
        )
        p = self._write_file('same_tick.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        tick10 = [ln for ln in out.splitlines() if ln.startswith('@10:')]
        self.assertEqual(tick10[0], '@10: #2 RECEIVED ALERT FROM #1: X')
        self.assertEqual(tick10[1], '@10: #2 SENT ALERT TO #1: X')

    def test_cancellation_chain_and_pruning(self):
        content = (
            'LENGTH 100\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'DEVICE 3\n'
            'PROPAGATE 1 2 10\n'
            'PROPAGATE 2 3 10\n'
            'PROPAGATE 3 1 10\n'
            'ALERT 1 A 0\n'
            'CANCEL 1 A 5\n'
        )
        p = self._write_file('cancel_chain.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        lines = out.splitlines()
        self.assertIn('@5: #1 SENT CANCELLATION TO #2: A', lines)
        self.assertIn('@15: #2 RECEIVED CANCELLATION FROM #1: A', lines)
        self.assertIn('@15: #2 SENT CANCELLATION TO #3: A', lines)
        self.assertIn('@25: #3 RECEIVED CANCELLATION FROM #2: A', lines)
        self.assertTrue(lines[-1].endswith('END'))

    def test_arrival_after_length_dropped(self):
        content = (
            'LENGTH 20\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 50\n'
            'ALERT 1 B 0\n'
        )
        p = self._write_file('late_arrival.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        lines = out.splitlines()
        # only send happens; no receive lines because arrival >= LENGTH
        self.assertIn('@0: #1 SENT ALERT TO #2: B', lines)
        self.assertNotIn('@50: #2 RECEIVED ALERT FROM #1: B', lines)
        self.assertTrue(lines[-1].endswith('END'))

    def test_comments_and_blank_lines(self):
        content = (
            '# comment line\n\n'
            'LENGTH 10\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 5\n'
            'ALERT 1 C 0\n'
        )
        p = self._write_file('comments.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        self.assertIn('@0: #1 SENT ALERT TO #2: C', out.splitlines())

    def test_unknown_command_is_ignored(self):
        content = (
            'UNKNOWN whatever\n'
            'LENGTH 20\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 5\n'
            'ALERT 1 Z 0\n'
        )
        p = self._write_file('unknown_cmd.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        lines = out.splitlines()
        self.assertIn('@0: #1 SENT ALERT TO #2: Z', lines)
        self.assertTrue(lines[-1].endswith('END'))

    def test_cancel_preempts_alert(self):
        content = (
            'LENGTH 40\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 10\n'
            'CANCEL 1 M 0\n'
            'ALERT 1 M 20\n'
        )
        p = self._write_file('preempt.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)

        lines = out.splitlines()
        self.assertIn('@10: #2 RECEIVED CANCELLATION FROM #1: M', lines)
        self.assertIn('@20: #1 SENT ALERT TO #2: M', lines)
        self.assertIn('@30: #2 RECEIVED ALERT FROM #1: M', lines)
        self.assertNotIn('@30: #2 SENT ALERT TO #1: M', lines)
        self.assertTrue(lines[-1].endswith('END'))

    def test_duplicate_cancel_same_time_dedup(self):
        content = (
            'LENGTH 20\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 5\n'
            'PROPAGATE 1 2 5\n'
            'CANCEL 1 X 0\n'
        )
        p = self._write_file('dup_cancel.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)
        at5 = [ln for ln in out.splitlines() if ln.startswith('@5:') and 'CANCELLATION' in ln]
        self.assertEqual(at5.count('@5: #2 RECEIVED CANCELLATION FROM #1: X'), 1)

    def test_duplicate_cancel_commands(self):
        content = (
            'LENGTH 20\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 5\n'
            'CANCEL 1 Z 0\n'
            'CANCEL 1 Z 0\n'
        )
        p = self._write_file('dup_cancel_cmds.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)
        self.assertIn('@5: #2 RECEIVED CANCELLATION FROM #1: Z', out.splitlines())

    def test_arrival_equal_length_dropped(self):
        content = (
            'LENGTH 10\n'
            'DEVICE 1\n'
            'DEVICE 2\n'
            'PROPAGATE 1 2 10\n'
            'ALERT 1 Q 0\n'
        )
        p = self._write_file('eq_length.txt', content)
        try:
            project1.input = lambda: str(p)
            out = self.capture_stdout(project1.main)
        finally:
            p.unlink(missing_ok = True)
        lines = out.splitlines()
        self.assertIn('@0: #1 SENT ALERT TO #2: Q', lines)
        self.assertNotIn('@10: #2 RECEIVED ALERT FROM #1: Q', lines)


if __name__ == '__main__':
    unittest.main()
