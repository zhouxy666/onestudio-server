from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired
from app.models.members import Members
from app.models.grade import Grade
from app.validators.base import BaseForm


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


# 绑定会员
class BindGrades(BaseForm):
    grade_ids = StringField()
    grades = []

    def validate_grade_ids(self, value):
        self.grades = self.validate_str_ids(Grade, value.data)
        value.data = [int(grade.id) for grade in self.grades]
