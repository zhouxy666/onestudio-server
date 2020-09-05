from flask import json, request
from werkzeug.exceptions import HTTPException
from app.models.base import db
from datetime import date, datetime, time
from werkzeug.http import http_date


class ApiException(HTTPException):
    code = 500
    msg = 'make a mistake'
    error_code = 999
    data = None
    count = None

    def __init__(self, code=None, msg=None, error_code=None, data=None, count=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        if error_code:
            self.error_code = error_code
        if data:
            self.data = data
        if count:
            self.count = count
        super(ApiException, self).__init__(msg, None)

    def get_body(self, environ=None):
        body = dict(
            data=[],
            error_code=self.error_code,
            msg=self.msg,
            request=request.method + ' ' + self.get_url_no_param()
        )
        if self.data:
            body['data'] = self.serialize_data(self.data)
        if self.count is not None:
            body['count'] = self.count
        text = json.dumps(body)
        return text

    def get_headers(self, environ=None):
        return [('Content-Type', 'application/json')]

    def serialize_data(self, o):
        '''
        如果返回的实例是模型类，那么通过dict来序列化
        :param o:
        :return:
        '''
        if isinstance(o, db.Model):
            return dict(o)
        if isinstance(o, date):
            return http_date(o.timetuple())
        if isinstance(o, datetime):
            return http_date(o.utctimetuple())
        if isinstance(o, time):
            return http_date(o.utctimetuple())
        return o

    @staticmethod
    def get_url_no_param():
        full_url = str(request.full_path)
        main_path = full_url.split('?')
        return main_path[0]
