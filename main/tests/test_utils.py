from django.test import TestCase

from main import utils


class UtilTests(TestCase):
    def test_date_from_str(self):
        string = "12/4/2011"
        date = utils.date_from_str(string)

        self.assertEqual(date.day, 4)
        self.assertEqual(date.month, 12)
        self.assertEqual(date.year, 2011)