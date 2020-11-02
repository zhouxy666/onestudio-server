from wtforms import StringField, IntegerField, TimeField
from wtforms.validators import DataRequired, length, Email, Regexp, ValidationError
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.models.members import Members
from app.models.grade import Grade
from app.validators.base import BaseForm


class GradeForm(BaseForm):
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
            ["1", "2", "3", "4", "5", "6", "7"].index(value.data)
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
    grade_name = StringField()
    week = StringField()
    start_time = TimeField()
    end_time = TimeField()
    # 需要更新的班级
    grade_id = ''
    grade = None

    def __init__(self, grade_id):
        self.grade_id = grade_id
        self.grade = Grade.query.get_or_404(ident=grade_id, msg='grade_id不存在')
        super(UpdateGradeForm, self).__init__()
        pass

    def validate_grade_name(self, value):
        # 如果grade_name不是空的
        if value.data not in [None, '']:
            # 校验班级的名称，不能重复
            valid_name = Grade.query.filter(Grade.grade_name == value.data,
                                            Grade.status == 1,
                                            Grade.id != self.grade_id).first()
            if valid_name is not None:
                raise ValidationError(msg='{} 班级名已存在'.format(value.data))
        else:
            value.data = self.grade.grade_name

    def validate_week(self, value):
        if value.data in [None, '']:
            value.data = self.grade.week

    def validate_start_time(self, value):
        if value.data in [None, '']:
            value.data = self.grade.start_time

    def validate_end_time(self, value):
        if value.data in [None, '']:
            value.data = self.grade.end_time


# 绑定会员
class BindMembers(BaseForm):
    member_ids = StringField()
    members = []

    def validate_member_ids(self, value):
        self.members = self.validate_str_ids(Members, value.data)
        value.data = [int(member.id) for member in self.members]
