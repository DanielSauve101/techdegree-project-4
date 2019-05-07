import unittest
from unittest.mock import patch

from peewee import SqliteDatabase

import work_log


test_db = SqliteDatabase(':memory:')
MODELS = [work_log.Entry]


class WorklogTests(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS)
        test_db.connect(reuse_if_open=True)
        test_db.create_tables(MODELS, safe=True)

    def test_valid_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 60, 'This is a test', 'y']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with('\nEntry saved successfully!')

    def test_not_valid_time_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 'not integer', 60, 'This is a test', 'n']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with('\nValue must be a number. Please try again.')

    def test_not_valid_save_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 60, 'This is a test', 'asdf', 'n']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with('\nYou must enter [Yn]')


if __name__ == '__main__':
    unittest.main()
