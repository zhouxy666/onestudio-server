from wtforms import StringField, IntegerField, TimeField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.models.members import Members
from app.models.grade import Grade
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
    grade_ids = StringField()
    grades = []

    def validate_gender(self, value):
        try:
            [1, 2].index(value.data)
        except ValueError as e:
            raise e

    def validate_grade_ids(self, value):
        if value.data is None or value.data == '':
            return
        grade_id_list = value.data.split(',')
        grades = []
        # 检查需要绑定的grade是否存在
        if len(grade_id_list) > 0:
            for grade_id in grade_id_list:
                grade = Grade.query.get_or_404(ident=grade_id, msg='{grade_id}不存在'.format(grade_id=grade_id))
                grades.append(grade)
        self.grades = grades


class GradeForm(BaseForm):
    id = StringField()
    grade_name = StringField(validators=[
        DataRequired(),
    ])
    week = StringField(validators=[
        DataRequired(),
    ])
    start_time = TimeField(validators=[
        DataRequired(),
    ])
    end_time = TimeField(validators=[
        DataRequired(),
    ])
    member_ids = StringField()
    members = []

    def validate_week(self, value):
        try:
            ["0", "1", "2", "3", "4", "5", "6"].index(value.data)
        except ValueError as e:
            raise e

    def validate_grade_name(self, value):
        grade = Grade.query.filter_by(grade_name=value.data).first()
        if grade is not None:
            raise ValidationError('班级名已存在')

    def validate_member_ids(self, value):
        if value.data is None or value.data == '':
            return
        member_id_list = value.data.split(',')
        members = []
        for member_id in member_id_list:
            member = Members.query.get_or_404(ident=member_id, msg="%s 会员不存在" % member_id)
            members.append(member)
        self.members = members


'''
member_id = '1'
grade_ids = '1,2,3,4,5,'
'''


class UpdateGradeForm(GradeForm):
    def validate_grade_name(self, value):
        pass


class DivideGradesForm(BaseForm):
    member_id = StringField()
    grade_ids = StringField()
