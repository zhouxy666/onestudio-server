from exts import db
import datetime


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    age = db.Column(db.String(20), nullable=False)
    total_less = db.Column(db.INTEGER, nullable=False)
    vip_level = db.Column(db.String(50), nullable=False)

    birthday = db.Column(db.DateTime, nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(100), nullable=True)

    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    upgrade_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


class ClassSchedule(db.Model):
    __tablename__ = 'class_schedule'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=True)

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)


class TimeSheet(db.Model):
    __tablename__ = 'time_sheet'

    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    sign_in_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    student_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    class_id = db.Column(db.INTEGER, db.ForeignKey('class_schedule.id'))

    class_name = db.relationship(ClassSchedule, backref=db.backref('timeSheets'))
    student = db.relationship(User, backref=db.backref('timeSheets'))
