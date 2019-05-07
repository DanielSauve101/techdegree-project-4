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
        work_log.Entry.create(task_title='Job1',
                              employee_name='Daniel',
                              time_spent=60,
                              optional_notes='This is a test'
                              )


class AddEntryTests(WorklogTests, unittest.TestCase):
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


class SearchNameTests(WorklogTests, unittest.TestCase):
    def test_not_valid_search_by_employee_name(self):
        inputs_to_pass = ['Bob']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_employee()
                mock.assert_called_once_with(
                    '\nNo employee matches found for {}'.format(inputs_to_pass[0]))

    def test_valid_search_by_employee_name(self):
        inputs_to_pass = ['Daniel', 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = work_log.search_by_employee()
            self.assertIn(inputs_to_pass[0], work_log.Entry.select().where(
                work_log.Entry.employee_name.contains(inputs_to_pass[0])))


if __name__ == '__main__':
    unittest.main()
