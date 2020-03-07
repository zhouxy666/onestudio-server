from app.models.base import Base, db
from sqlalchemy import Column, SmallInteger, Integer, String, Date
from sqlalchemy import orm


class Members(Base):
    __tablename__ = 'members'
    # id
    id = Column(Integer, primary_key=True, autoincrement=True)
    # 小程序的openid
    openid = Column(String(28), nullable=False)
    # 姓名
    name = Column(String(24), nullable=False)
    # 性别 1-男 2-女 3-??
    gender = Column(SmallInteger, nullable=False, default=1)
    # 头像url
    avatarurl = Column(String(100), nullable=True)
    # 电话
    mobile = Column(String(24), nullable=True)
    # 昵称
    nickname = Column(String(100), nullable=True)
    # 小程序和公众号等路的会员都是普通用户 4
    auth = Column(SmallInteger, default=4)
    # 年龄
    age = Column(String(24), nullable=True, default=1)

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'status', 'openid', 'name', 'gender', 'avatarurl', 'mobile', 'nickname', 'auth', 'age']
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
    def create_member(name, openid, gender, avatarurl, age, mobile, nickname):
        with db.auto_commit():
            member = Members()
            member.name = name
            member.openid = openid
            member.gender = gender
            member.avatarurl = avatarurl
            member.age = age
            member.mobile = mobile
            member.nickname = nickname
            db.session.add(member)
