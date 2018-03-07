from __future__ import unicode_literals

import requests

from .errors import NotionError
from .format import Format

class NotionClient:

    def __init__(self, api_token, _api_root='https://app.usenotion.com'):
        self.api_root = _api_root

        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


    def report(self, date, value, ingredient_key=None, ingredient_id=None):
        data = {
            'value': Format.value(value),
            'date': Format.date(date)
        }

        arg_error_msg = 'one of ingredient_id or ingredient_key is required'

        if ingredient_key and ingredient_id:
            raise NotionError(arg_error_msg)
        elif ingredient_key:
            data['ingredient_key'] = ingredient_key
        elif ingredient_id:
            data['ingredient_id'] = ingredient_id
        else:
            raise NotionError(arg_error_msg)


        url = self.api_root + '/api/v1/report'

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        return response

    def batch_report(self, ingredient_id, reports):
        data = {
            'ingredient_id': ingredient_id,
            'reports': [Format.report(r) for r in reports],
        }

        url = self.api_root + '/api/v1/batch_report'

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        return response

    def create_ingredient(self, name, reports):
        data = {
            'name': name,
            'reports': [Format.report(r) for r in reports],
        }

        url = self.api_root + '/api/v1/ingredient'

        response = requests.post(url, json=data, headers=self.headers)
        response.raise_for_status()

        return response
