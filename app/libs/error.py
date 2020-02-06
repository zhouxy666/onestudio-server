from flask import json, request
from werkzeug.exceptions import HTTPException


class ApiException(HTTPException):
    code = 500
    msg = 'make a mistake'
    error_code = 999

    def __init__(self, code=None, msg=None, error_code=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        super(ApiException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            error_code=self.error_code,
            msg=self.msg,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    @staticmethod
    def get_url_no_param():
        full_url = str(request.full_path)
        main_path = full_url.split('?')
        return main_path[0]
