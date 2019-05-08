import io
import sys
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


class MenuInputsTests(WorklogTests, unittest.TestCase):
    def test_menu_inputs(self):
        inputs_to_pass = ['notvalid', 'b', 'notvalid', 'a',
                          'Daniel', 'q', 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.main_menu_loop()
                mock.assert_called_with('b) Search entries')


class AddEntryTests(WorklogTests, unittest.TestCase):
    def test_valid_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 60, 'This is a test', 'y']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with('\nEntry saved successfully!')

    def test_not_valid_time_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 'not integer', 60,
                          'This is a test', 'n']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with(
                    '\nValue must be a number. Please try again.')

    def test_not_valid_save_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 60, 'This is a test', 'asdf', 'n']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.add_entry()
                mock.assert_called_once_with('\nYou must enter [Yn]')


class ViewEntriesTests(WorklogTests, unittest.TestCase):
    def test_view_entry_if_entry_provided(self):
        test_entry = work_log.Entry.select()
        inputs_to_pass = ['q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.view_entries(test_entry)
                mock.assert_called_with('q) return to previous menu')

    def test_view_entry_input_next_previous_quit(self):
        inputs_to_pass = ['n', 'p', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.view_entries()
                mock.assert_called_with('q) return to previous menu')

    def test_view_entry_input_update(self):
        inputs_to_pass = ['u', 'Task1', 32, '', '2019-05-01', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.view_entries()
                mock.assert_called_with('\nEntry successfully updated!')

    def test_view_entry_input_delete(self):
        inputs_to_pass = ['d', 'n', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.view_entries()
                mock.assert_called_with('q) return to previous menu')


class UpdateEntryTests(WorklogTests, unittest.TestCase):
    def test_update_entry_invalid_time(self):
        test_entry = work_log.Entry.get_by_id(1)
        inputs_to_pass = ['Task1', 'not valid time', 32, '', '2019-05-01', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.update_entry(test_entry)
                mock.assert_called_with('\nEntry successfully updated!')

    def test_update_entry_invalid_date(self):
        test_entry = work_log.Entry.get_by_id(1)
        inputs_to_pass = ['Task1', 32, '', 'not valid date', '2019-05-01', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.update_entry(test_entry)
                mock.assert_called_with('\nEntry successfully updated!')


class DeleteEntryTests(WorklogTests, unittest.TestCase):
    def test_delete_entry_input_invalid_and_yes(self):
        work_log.Entry.create(task_title='Job2',
                              employee_name='Geoff',
                              time_spent=80,
                              optional_notes='This is a delete test'
                              )
        test_entry = work_log.Entry.get_by_id(2)
        inputs_to_pass = ['not a valid input', 'y', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.delete_entry(test_entry)
                mock.assert_called_with('\nEntry successfully deleted!')


class SearchNameTests(WorklogTests, unittest.TestCase):
    def test_not_valid_search_by_employee_name(self):
        inputs_to_pass = ['Bob']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_employee()
                mock.assert_called_once_with(
                    '\nNo employee matches found for {}'.format(
                        inputs_to_pass[0]))


class SearchDateTests(WorklogTests, unittest.TestCase):
    def test_valid_date_not_found(self):
        inputs_to_pass = ['2019-05-01', 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_date()
                mock.assert_called_once_with(
                    '\nSorry but there are no entries found for that specific date')


class SearchRangeDatesTests(WorklogTests, unittest.TestCase):
    def test_valid_dates_not_found(self):
        inputs_to_pass = ['2018-05-01', '2019-05-01', 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_range_of_dates()
                mock.assert_called_once_with(
                    '\nSorry but there are no entries found for that range of dates')


class SearchTimeTests(WorklogTests, unittest.TestCase):
    def test_valid_time_spent_not_found(self):
        inputs_to_pass = [55, 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_time_spent()
                mock.assert_called_once_with(
                    '\nNo entries found with {} minutes.'.format(
                        inputs_to_pass[0]))


class SearchWordTests(WorklogTests, unittest.TestCase):
    def test_valid_word_not_found(self):
        inputs_to_pass = ['Link', 'q', 'q']
        with patch('builtins.input', side_effect=inputs_to_pass):
            with patch('builtins.print', side_effect=print) as mock:
                result = work_log.search_by_word()
                mock.assert_called_once_with(
                    '\nNo entry found with word {} in title or notes .'.format(
                        inputs_to_pass[0]))


if __name__ == '__main__':
    unittest.main()
