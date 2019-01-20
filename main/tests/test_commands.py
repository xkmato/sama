from io import StringIO

from django.core.management import call_command
from django.test import TestCase


class CommandTests(TestCase):
    def test_load_schools_from_cvs(self):
        out = StringIO()
        call_command('load_schools_from_csv', 'test_files/test_csv_data.csv', stdout=out)
        self.assertIn('Created or updated all 25 rows from test_files/test_csv_data.csv', out.getvalue())