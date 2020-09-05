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
                       'create_time', 'grades']
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
    def divide_grades(member_id, grade_ids=''):
        grades = []
        if grade_ids is not None and grade_ids != '':
            grade_id_list = grade_ids.split(',')
            # 检查需要绑定的grade是否存在
            for grade_id in grade_id_list:
                grade = Grade.query.get_or_404(ident=grade_id, msg='{grade_id}不存在'.format(grade_id=grade_id))
                grades.append(grade)
        with db.auto_commit():
            member = Members.query.get_or_404(member_id)
            member.grades = grades
            db.session.add(member)
            return member

    @staticmethod
    def update_member(uid, name, gender, age, mobile='', nickname='', grades=[]):
        with db.auto_commit():
            member = Members.query.get_or_404(uid, msg='member not found')
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
            value = getattr(self, column_name, None)
            if column_name == 'grades':
                result_dict['grades'] = [v.to_dict() for v in value]
            else:
                result_dict[column_name] = value
        return result_dict
