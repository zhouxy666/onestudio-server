from app.models.base import Base, db
from sqlalchemy import Integer, Column, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship


class SignIn(Base):
    __tablename__ = 'attendance'
    id = Column(Integer, primary_key=True, autoincrement=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    begin_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    member = relationship('Members', backref='sign_in_record')
