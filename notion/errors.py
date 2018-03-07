from __future__ import unicode_literals

class NotionError(Exception):
    pass

class NotionClientError(NotionError):
    def __init__(self, request, response, error):
        super().__init__(error)
        self.request = request
        self.response = response
