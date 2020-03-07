from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.validators.base import BaseFrom
from app.models.members import Members


class MembersForm(BaseFrom):
    # 姓名
    name = StringField(validators=[
        DataRequired(),
    ])
    # openid
    openid = StringField(validators=[
        DataRequired(),
        length(max=28)
    ])
    # 性别
    gender = IntegerField(validators=[
        DataRequired(),
    ])
    # 头像
    # validators=[
    #         DataRequired(),
    #     ]
    avatarurl = StringField()
    # 年龄
    age = StringField()
    # 电话
    mobile = StringField()
    # 昵称
    nickname = StringField()

    def validate_openid(self, value):
        if Members.query.filter_by(openid=value.data).first():
            raise ValidationError('账号已存在')
