from flask import request
from wtforms import Form
from app.libs.error_code import ParameterException


class BaseForm(Form):
    def __init__(self):
        data = request.get_json(silent=True) or \
               request.form.to_dict()
        super(BaseForm, self).__init__(data=data)

    def validate_for_api(self):
        valid = super(BaseForm, self).validate()
        if not valid:
            raise ParameterException(msg=self.errors)
        return self

    '''
    '1,2,3,4' ==> ['1','2','3','4']
    '''

    @staticmethod
    def validate_str_ids(model, ids):
        if ids in [None, '']:
            return []
        split_ids = str(ids).split(',')
        instance_list = []
        for ins_id in split_ids:
            model_ins = model.query.get_or_404(ident=ins_id, msg='{}不存在'.format(ins_id))
            instance_list.append(model_ins)
        return instance_list
