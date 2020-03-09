from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.models.members import Members
from app.validators.base import BaseFrom


class ClientForm(BaseFrom):
    account = StringField(validators=[
        DataRequired('账号不能为空'),
    ])
    secret = StringField(validators=[
        DataRequired('密码不能为空'),
    ])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type = client


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        length(min=5, max=32),
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
        Regexp(r'^[a-zA-Z0-9_*&$#@]{6,22}$')
    ])

    # nickname = StringField(validators=[
    #     DataRequired(),
    #     length(min=2, max=22)
    # ])
    nickname = StringField()

    def validate_account(self, value):
        if User.query.filter_by(email=value.data).first():
            raise ValidationError('账号已存在')


class UserWxForm(BaseFrom):
    # 姓名
    name = StringField(validators=[
        DataRequired(),
    ])
    openid = StringField(validators=[
        DataRequired(),
        length(max=28)
    ])
    # 性别
    gender = IntegerField(validators=[
        DataRequired(),
    ])
    # 头像
    avatarurl = StringField(validators=[
        DataRequired(),
    ])
    # 年龄
    age = StringField()
    # 电话
    mobile = StringField()
    # 昵称
    nickname = StringField()

    def validate_openid(self, value):
        if Members.query.filter_by(openid=value.data).first():
            raise ValidationError('账号已存在')
