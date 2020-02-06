from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.validators.base import BaseFrom


class ClientForm(BaseFrom):
    account = StringField(validators=[DataRequired('账号不能为空'), length(
        min=5, max=32
    )])
    secret = StringField(validators=[
        DataRequired()
    ])
    type = IntegerField(validators=[DataRequired()])

    def validate_type(self, value):
        try:
            client = ClientTypeEnum(value.data)
        except ValueError as e:
            raise e
        self.type = client.name


class UserEmailForm(ClientForm):
    account = StringField(validators=[
        Email(message='invalidate email')
    ])
    secret = StringField(validators=[
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
