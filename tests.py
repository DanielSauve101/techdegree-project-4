import unittest
from unittest.mock import patch

from peewee import SqliteDatabase

import work_log


test_db = SqliteDatabase(':memory:')
MODELS = [work_log.Entry]


class WorklogTests(unittest.TestCase):
    def setUp(self):
        test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)
        test_db.connect(reuse_if_open=True)
        test_db.create_tables(MODELS, safe=True)

    def test_add_entry(self):
        inputs_to_pass = ['Job1', 'Daniel', 60, 'This is a test', 'y']
        with patch('builtins.input', side_effect=inputs_to_pass):
            result = work_log.add_entry()
            self.assertEqual(result, inputs_to_pass)


if __name__ == '__main__':
    unittest.main()
