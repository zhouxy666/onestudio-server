from app.models.base import Base, db
from sqlalchemy import Column, Integer, String, SmallInteger, orm
from werkzeug.security import generate_password_hash, check_password_hash
from app.libs.error_code import AuthFailed


class User(Base):
    id = Column(Integer, primary_key=True)
    email = Column(String(24), unique=True, nullable=False)
    nickname = Column(String(24))
    # 默认注册的都是普通用户
    auth = Column(SmallInteger, default=3)
    _password = Column('password', String(100))

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'email', 'nickname', 'auth', 'create_time', 'status']
        super(User, self).__init__()

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

    @staticmethod
    def verify(email, password):
        user = User.query.filter_by(email=email).first_or_404(msg='user not Found')
        if not user.check_password(password):
            raise AuthFailed()
        return user

    def check_password(self, password):
        if not self._password:
            return False
        return check_password_hash(self._password, password)
