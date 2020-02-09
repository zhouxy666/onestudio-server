from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException


class BaseFrom(Form):
    def __init__(self):
        data = request.get_json(silent=True) or \
               request.form.to_dict()
        super(BaseFrom, self).__init__(data=data)

    def validate_for_api(self):
        valid = super(BaseFrom, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self
