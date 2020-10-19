from app.models.base import Base, db
from sqlalchemy import Column, SmallInteger, Integer, String, Date, DateTime, orm, Time


def grade_fun(grade):
    grade.start_time = str(grade.start_time)
    grade.end_time = str(grade.end_time)
    return grade


# 序号	名称	星期	上课时间	下课时间	描述
class Grade(Base):
    __tablename__ = 'grade'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 班级名称
    grade_name = Column(String(24), nullable=False)
    # 星期
    week = Column(String(24), nullable=False, default=1)
    # 上课
    start_time = Column(Time, nullable=False)
    # 下课
    end_time = Column(Time, nullable=False)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'grade_name', 'week', 'start_time', 'end_time', 'create_time']
        super(Grade, self).__init__()

    @staticmethod
    def add_grade(grade_name, week, start_time, end_time):
        with db.auto_commit():
            grade = Grade()
            grade.grade_name = grade_name
            grade.week = week
            grade.start_time = start_time
            grade.end_time = end_time
            db.session.add(grade)

    @staticmethod
    def serialize_grade(grade):
        grade.start_time = str(grade.start_time)
        grade.end_time = str(grade.end_time)
        return grade

    @staticmethod
    def serialize_grades(grades):
        # 把start_time和end_time处理一下
        res_grades = list(map(grade_fun, grades))
        return [dict(item) for item in res_grades]

    @staticmethod
    def bind_members(grade_id, add_members):
        with db.auto_commit():
            grade = Grade.query.get_or_404(ident=grade_id, msg='grade_id is not found')
            members = grade.members
            member_ids = [member.id for member in members]
            for m in add_members:
                if m.id not in member_ids:
                    grade.members.append(m)
            return grade

    @staticmethod
    def un_bind_members(grade_id, remove_members):
        with db.auto_commit():
            grade = Grade.query.get_or_404(ident=grade_id, msg='grade_id is not found')
            remove_member_ids = [member.id for member in remove_members]
            grade.members = [m for m in grade.members if m.id not in remove_member_ids]
            return grade

    def to_dict(self):
        result_dict = {}
        for column_name in self.fields:
            value = getattr(self, column_name, None)
            if column_name in ['start_time', 'end_time']:
                form_time = value.strftime('%H:%M:%S')
                result_dict[column_name] = form_time
            else:
                result_dict[column_name] = value

        # members
        result_dict['members'] = [{
            'id': member.id,
            'name': member.name
        } for member in self.members]
        return result_dict
