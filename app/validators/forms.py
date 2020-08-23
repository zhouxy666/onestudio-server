from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.models.members import Members
from app.validators.base import BaseForm


class ClientForm(BaseForm):
    username = StringField(validators=[DataRequired('账号不能为空'), length(
        min=5, max=32
    )])
    password = StringField(validators=[
        DataRequired()
    ])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type = client


class UserEmailForm(ClientForm):
    username = StringField(validators=[
        DataRequired('账号不能为空'),
        length(min=5, max=32),
        Email(message='invalidate email')
    ])
    password = StringField(validators=[
        DataRequired(),
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


class UserWxForm(BaseForm):
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


class MemberForm(BaseForm):
    id = StringField()
    # 姓名
    name = StringField(validators=[
        DataRequired(),
    ])
    gender = IntegerField(validators=[
        DataRequired(),
    ])
    mobile = StringField()
    nickname = StringField()
    age = StringField()

    def validate_gender(self, value):
        try:
            [1, 2].index(value.data)
        except ValueError as e:
            raise e
