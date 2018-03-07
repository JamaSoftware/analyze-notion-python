from __future__ import unicode_literals
import numbers

from .errors import NotionError

class Format(object):

    @staticmethod
    def date(date):
        try:
            return date.strftime('%Y-%m-%d')
        except AttributeError:
            raise NotionError('expected datetime, not {}'.format(date))

    @staticmethod
    def value(value):
        if isinstance(value, numbers.Number):
            return value
        else:
            raise NotionError('expected number, not {}'.format(value))

    @staticmethod
    def report(report):
        try:
            return {
                'date': Format.date(report['date']),
                'value': Format.value(report['value']),
            }
        except:
            raise NotionError(
                "expected a report to have a 'date' and 'value' key")
