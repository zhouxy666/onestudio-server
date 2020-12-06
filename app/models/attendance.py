from app.models.base import Base, db
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime, orm
from sqlalchemy.orm import relationship


class SignIn(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    sign_in_time = Column(DateTime, nullable=True)
    member = relationship('Members', backref='sign_in_record')

    @orm.reconstructor
    def __init__(self):
        self.fields = ['id', 'sign_in_time', 'create_time', 'member_id']
        super(SignIn, self).__init__()