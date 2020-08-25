from app.models.base import Base, db
from sqlalchemy import Column, SmallInteger, Integer, String, Date, DateTime, orm, ForeignKey


class MembersGrade():
    __tablename__ = 'members_grade'

    id = Column(Integer, primary_key=True)
    member_id = Column(Integer, ForeignKey("members.id"))
    grade_id = Column(Integer, ForeignKey("grade.id"))
