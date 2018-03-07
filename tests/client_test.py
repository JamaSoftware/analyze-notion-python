from datetime import datetime, timedelta
import os
import unittest

import notion

TOKEN = os.environ.get('NOTION_TOKEN')
API_ROOT = os.environ.get('NOTION_API_ROOT')

class RequestTestCase(unittest.TestCase):

    def setUp(self):
        if TOKEN and API_ROOT:
            self.api = notion.NotionClient(TOKEN, _api_root=API_ROOT)
        else:
            raise RuntimeError('set NOTION_TOKEN and NOTION_API_ROOT to run this test')

        result = self.api.report(datetime.now(), 1, 'python_test_report')
        self.ingredient_id = result.json()['id']


class ReportTestCase(RequestTestCase):

    def test_report_by_key(self):
        self.api.report(datetime.now(), 1, ingredient_key='test_report_by_key')

    def test_report_by_id(self):
        self.api.report(datetime.now(), 1, ingredient_id=self.ingredient_id)

    def test_report_invalid_date(self):
        with self.assertRaises(notion.NotionError):
            self.api.report('today', 1, ingredient_key='test_report_invalid_date')

    def test_report_invlaid_value(self):
        with self.assertRaises(notion.NotionError):
            self.api.report(datetime.now(), '1', ingredient_id=self.ingredient_id)


class BatchReportTestCase(RequestTestCase):

    def test_batch_report(self):
        self.api.batch_report(self.ingredient_id, [
            {'date': datetime.now(), 'value': 1},
        ])

    def test_batch_report_single_report(self):
        with self.assertRaises(notion.NotionError):
            self.api.batch_report(
                self.ingredient_id, {'date': datetime.now(), 'value': 10})


class CreateIngredient(RequestTestCase):

    def test_create_ingredient(self):
        self.api.create_ingredient('test_create_ingredient', [
            {'date': datetime.now(), 'value': 1},
            {'date': datetime.now() + timedelta(days=1), 'value': 2},
            {'date': datetime.now() + timedelta(days=2), 'value': 3},
            {'date': datetime.now() + timedelta(days=3), 'value': 0},
        ])

    def test_create_ingredient_bad_data(self):
        try:
            self.api.create_ingredient('test_create_ingredient', [
                {'date': datetime.now(), 'value': 1},
                {'date': datetime.now() + timedelta(days=1), 'value': 2},
                {'date': datetime.now() + timedelta(days=4), 'value': 3},
            ])
            self.fail()
        except notion.NotionClientError as error:
            self.assertFalse(error.response.ok)
