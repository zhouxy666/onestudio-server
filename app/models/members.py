from app.models.base import Base, db
from sqlalchemy import Column, SmallInteger, Integer, String, Date
from sqlalchemy import orm
from app.models.grade import Grade

members_grade = db.Table('members_grade',
                         db.Column('id', db.Integer, primary_key=True, autoincrement=True),
                         db.Column('member_id', db.Integer, db.ForeignKey('members.id')),
                         db.Column('grade_id', db.Integer, db.ForeignKey('grade.id')))


class Members(Base):
    __tablename__ = 'members'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 姓名
    name = Column(String(24), nullable=False)
    # 性别 1-男 2-女 3-??
    gender = Column(SmallInteger, nullable=False, default=1)
    # 头像url
    avatarurl = Column(String(100), nullable=True,
                       default='//apic.douyucdn.cn/upload/avatar_v3/201909/533af0de15b14cb0996bc4b9645a73fa_middle.jpg')
    # 小程序的openid
    openid = Column(String(28), nullable=True)
    # 电话
    mobile = Column(String(24), nullable=True)
    # 昵称
    nickname = Column(String(100), nullable=True)
    # 小程序和公众号等路的会员都是普通用户 4
    auth = Column(SmallInteger, default=4)
    # 年龄
    age = Column(String(24), nullable=True, default=1)

    # 定义多对多的关系
    grades = db.relationship("Grade", secondary=members_grade, backref=db.backref('members'))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'openid', 'name', 'gender', 'avatarurl', 'mobile', 'nickname', 'auth', 'age',
                       'create_time']
        super(Members, self).__init__()

    # # 出生年月
    # birthday = Column(Date, nullable=True)
    # # 住址
    # address = Column(String(100), nullable=True)
    # 电子邮件
    # email = Column(String(24), unique=True, nullable=False)
    # 是否为管理员
    # auth = Column(SmallInteger, default=1)
    # 密码
    # _password = Column('password', String(100))
    # 剩余课时
    # left_lessons = Column(INTEGER, nullable=True, default=0)

    # 创建时间 报名日期
    # created_date = Column(DateTime, default=datetime.datetime.utcnow)
    # 信息更新时间
    # upgrade_date = Column(DateTime, default=datetime.datetime.utcnow)

    @staticmethod
    def add_member(name, gender, age, mobile, nickname, grades=[]):
        with db.auto_commit():
            member = Members()
            member.name = name
            member.gender = gender
            member.age = age
            member.mobile = mobile
            member.nickname = nickname
            member.grades = grades
            db.session.add(member)

    '''
    分班
    '''

    @staticmethod
    def bind_grades(member_id, bind_grades):
        with db.auto_commit():
            member = Members.query.get_or_404(ident=member_id)
            grades = member.grades
            grade_ids = [g.id for g in grades]
            # 检查需要绑定的grade是否存在
            for bind_grade in bind_grades:
                if bind_grade not in grade_ids:
                    member.grades.append(bind_grade)
            return member

    @staticmethod
    def un_bind_grades(member_id, remove_grade_ids):
        with db.auto_commit():
            member = Members.query.get_or_404(ident=member_id)
            result_grades = []
            member.grades = [grade for grade in member.grades if grade.id not in remove_grade_ids]
            member.grades = result_grades
            return member

    @staticmethod
    def update_member(uid, name, gender, age, mobile='', nickname='', grades=[]):
        with db.auto_commit():
            member = Members.query.get_or_404(ident=uid, msg='member not found')
            member.name = name
            member.gender = gender
            member.age = age
            member.mobile = mobile
            member.nickname = nickname
            member.grades = grades

    def verify(self, openid):
        pass

    def to_dict(self):
        result_dict = {}
        for column_name in self.fields:
            result_dict[column_name] = getattr(self, column_name, None)

        result_dict['grades'] = [{
            'id': grade.id,
            'week': grade.week,
            'start_time': grade.start_time.strftime('%H:%M:%S'),
            'end_time': grade.end_time.strftime('%H:%M:%S'),
            'grade_name': grade.grade_name
        } for grade in self.grades]

        return result_dict
