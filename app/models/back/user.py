from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, SmallInteger
from werkzeug.security import generate_password_hash


class User(Base):
    __tablename__ = 'user'
    # id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 姓名
    name = db.Column(db.String(20), nullable=False)
    # 性别
    gender = db.Column(db.String(20), nullable=False)
    # 年龄
    age = db.Column(db.String(20), nullable=False)
    # 剩余课时
    left_lessons = db.Column(db.INTEGER, nullable=False, default=0)
    # 会员等级 1.为普通会员;
    vip_level = db.Column(db.String(50), nullable=False, default=1)

    # 昵称
    nickname = db.Column(db.String(20), unique=True, nullable=True)
    # 出生年月
    birthday = db.Column(db.Date, nullable=True)
    # 电话
    phone = db.Column(db.String(20), nullable=True)
    # 住址
    address = db.Column(db.String(100), nullable=True)
    # 电子邮件
    email = Column(String(24), unique=True, nullable=False)
    # 是否为管理员
    auth = Column(SmallInteger, default=1)
    # 密码
    _password = Column('password', String(100))

    # 创建时间 报名日期
    # created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # 信息更新时间
    # upgrade_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    @staticmethod
    def register_by_email(nickname, account, secret):
        with db.auto_commit():
            user = User()
            user.nickname = nickname
            user.email = account
            user.password = secret
            db.session.add(user)
            pass
        pass
