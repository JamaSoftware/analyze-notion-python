import datetime
import unittest

import notion

Format = notion._Format # pylint: disable=protected-access

class FormatTestCase(unittest.TestCase):

    def test_date(self):
        date = datetime.datetime.now()

        self.assertEqual(
            date.strftime('%Y-%m-%d'),
            Format.date(date))

    def test_date_raises(self):
        with self.assertRaises(notion.NotionError):
            Format.date('10-11-12')

    def test_value(self):
        self.assertEqual(1, Format.value(1))

    def test_value_raises(self):
        with self.assertRaises(notion.NotionError):
            Format.value('1')

    def test_report(self):
        date = datetime.datetime.now()

        self.assertEqual(
            {
                'date': date.strftime('%Y-%m-%d'),
                'value': 1,
            },
            Format.report({
                'date': date,
                'value': 1,
            })
        )
