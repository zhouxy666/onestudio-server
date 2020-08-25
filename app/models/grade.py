from app.models.base import Base, db
from sqlalchemy import Column, SmallInteger, Integer, String, Date, DateTime, orm


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
    start_time = Column(DateTime, nullable=False)
    # 下课
    end_time = Column(DateTime, nullable=False)
