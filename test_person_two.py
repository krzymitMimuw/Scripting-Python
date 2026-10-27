import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from file_manager import generate_paths, manage_files, parser
from json_data import read_json, write_json


class PersonTwoTests(unittest.TestCase):
    def test_defaults(self):
        paths = generate_paths('data')
        self.assertEqual(len(paths), 84)
        self.assertEqual(paths[0], Path('data/January/Monday/Morning'))
        self.assertEqual(paths[-1], Path('data/December/Sunday/Morning'))

    def test_intervals_and_periods(self):
        self.assertEqual(generate_paths('data', ['May'], ['Monday-Wednesday'], ['Evening']), [
            Path('data/May/Monday/Evening'), Path('data/May/Tuesday/Morning'),
            Path('data/May/Wednesday/Morning')])
        self.assertEqual(len(generate_paths('data', ['May'])), 7)

    def test_invalid_arguments(self):
        for months, days in [(['May', 'June'], ['Monday']), (['May'], ['Sunday-Monday']), (['../x'], ['Monday'])]:
            with self.assertRaises(ValueError):
                generate_paths('data', months, days)

    def test_duplicates(self):
        self.assertEqual(len(generate_paths('.', ['May', 'May'], ['Monday', 'Monday'])), 1)

    def test_json_round_trip(self):
        with tempfile.TemporaryDirectory() as root:
            with patch('json_data.random.choice', return_value='A'), patch('json_data.random.randint', side_effect=[17, 465]):
                write_json(Path(root))
            record = json.loads((Path(root) / 'Dane.json').read_text())
            self.assertEqual(record, {'Model': 'A', 'Wynik': 17, 'Czas': 465})
            self.assertEqual(read_json(Path(root)), 465)

    def test_other_models_and_invalid_files(self):
        with tempfile.TemporaryDirectory() as root, contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(read_json(Path(root)), 0)
            for record in [{'Model': 'B', 'Wynik': 1, 'Czas': 999}, {'Model': 'C', 'Wynik': 0, 'Czas': 1000}, [], {}, {'Model': 'A', 'Wynik': 1, 'Czas': '5s'}, {'Model': 'A', 'Wynik': 1, 'Czas': True}, {'Model': 'A', 'Wynik': 1, 'Czas': 1001}]:
                (Path(root) / 'Dane.json').write_text(json.dumps(record))
                self.assertEqual(read_json(Path(root)), 0)
            (Path(root) / 'Dane.json').write_text('{broken')
            self.assertEqual(read_json(Path(root)), 0)

    def test_integration(self):
        with tempfile.TemporaryDirectory() as root, contextlib.redirect_stdout(io.StringIO()):
            flags = ['-r', root, '-m', 'May', '-d', 'Monday-Wednesday', '-j']
            with patch('json_data.random.choice', side_effect=['A', 'B', 'A']), patch('json_data.random.randint', side_effect=[1, 100, 2, 200, 3, 300]):
                manage_files(parser.parse_args(flags + ['-t']))
            self.assertEqual(len(list(Path(root).rglob('Dane.json'))), 3)
            self.assertEqual(manage_files(parser.parse_args(flags + ['-o'])), 400)
            result = subprocess.run([sys.executable, str(Path(__file__).with_name('file_manager.py')), *flags, '-o'], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn('400s', result.stdout)

    def test_read_does_not_create_directories(self):
        with tempfile.TemporaryDirectory() as root, contextlib.redirect_stdout(io.StringIO()):
            missing = Path(root) / 'missing'
            args = parser.parse_args(['-o', '-j', '-r', str(missing)])
            self.assertEqual(manage_files(args), 0)
            self.assertFalse(missing.exists())


if __name__ == '__main__':
    unittest.main()
