from __future__ import unicode_literals

import requests

from .format import Format
from .errors import NotionClientError, NotionError

class NotionClient(object):

    def __init__(self, api_token, _api_root='https://app.usenotion.com'):
        self.api_root = _api_root

        self.headers = {
            'Authorization': api_token,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
        }


    def _request(self, path, json):
        url = self.api_root + path
        request = requests.Request('POST', url, json=json, headers=self.headers)
        response = None
        try:
            with requests.Session() as session:
                response = session.send(request.prepare())
        except requests.exceptions.RequestException as error:
            raise NotionClientError(request, response, error)

        try:
            response.raise_for_status()
        except requests.exceptions.RequestException as error:
            raise NotionClientError(request, response, error)

        return response

    def report(self, date, value, ingredient_key=None, ingredient_id=None):
        """Submit a value at at date for an ingredient

        Args:
            date (datetime): the date of the report
            value (number): the value of the report
            ingredient_key (string, optional): a new or existing ingredient key to report for
            ingredient_id (string, optional): an existing ingredient id to report for

        Raises:
            ArgumentError: raised if one of `ingredient_id` or `ingredient_key`
                is not supplied

            NotionClientError: raised if the report could not be made

        Note:
            Exactly one of `ingredient_id` or `ingredient_key` is required.

            If `ingredient_key` is supplied and a corresponding ingredient does
            not exist, a new ingredient will be created.
        """
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

        return self._request('/api/v1/report', data)

    def batch_report(self, ingredient_id, reports):
        """Submit multiple values at multiple dates for an ingredient

        Args:
            ingredient_id (string): the id of the ingredient to report for
            reports (list): a list of dicts with keys:
                'date' (datetime): the date of a report
                'value' (number): the value of a report

        Raises:
            NotionClientError: raised if the reports could not be made
        """
        data = {
            'ingredient_id': ingredient_id,
            'reports': [Format.report(r) for r in reports],
        }

        return self._request('/api/v1/batch_report', data)

    def create_ingredient(self, name, reports):
        """Creates a new ingredient with a schedule determined by the reports

        Args:
            name (string): the desired name of the new ingredient
            reports (list): a list of dicts with keys:
                'date' (datetime): the date of a report
                'value' (number): the value of a report

        Note:
            The reports must have a regular amount of time difference from
            each other (days, weeks, etc) so that a schedule can be setup for
            the newly created ingredient

        Raises:
            NotionClientError: raised if the ingredient could not be created
        """
        data = {
            'name': name,
            'reports': [Format.report(r) for r in reports],
        }

        return self._request('/api/v1/ingredient', data)
