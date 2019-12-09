from exts import db
import datetime

# 中间表
user_grade = db.Table('user_grade',
                      db.Column('user_id', db.INTEGER, db.ForeignKey('user.id'), primary_key=True),
                      db.Column('grade_id', db.INTEGER, db.ForeignKey('grade.id'), primary_key=True))


# 用户表
class User(db.Model):
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

    # 出生年月
    birthday = db.Column(db.Date, nullable=True)
    # 电话
    phone = db.Column(db.String(20), nullable=True)
    # 住址
    address = db.Column(db.String(100), nullable=True)

    # 创建时间 报名日期
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    # 信息更新时间
    upgrade_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)


# 班级表
class Grade(db.Model):
    __tablename__ = 'grade'

    # id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 班级名称
    name = db.Column(db.String(100), nullable=False)
    # 星期
    week = db.Column(db.String(20), nullable=False)
    # 描述
    description = db.Column(db.Text, nullable=True)

    # 上课时间
    start_time = db.Column(db.Time, nullable=False)
    # 下课时间
    end_time = db.Column(db.Time, nullable=False)

    # 建立与用户的多对多关系
    users = db.relationship(User, secondary=user_grade, backref=db.backref('grades'))


# 课件
class Course(db.Model):
    __tablename__ = 'course'

    # id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # code 课件编号
    code = db.Column(db.String(100), nullable=False)
    # 课件名称
    name = db.Column(db.String(100), nullable=False)


# 上课表
class Class(db.Model):
    __tablename__ = 'class'

    # id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 用户id（外键）
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    # 课件 (外键)
    course_id = db.Column(db.INTEGER, db.ForeignKey('course.id'))
    # 打卡时间
    punch_time = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=False)

    # 课件名称
    course_name = db.relationship(Course, backref=db.backref('classes'))
    # 学生名称
    user_name = db.relationship(User, backref=db.backref('classes'))


# 产品表
class Product(db.Model):
    __tablename__ = 'product'

    # id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 产品名称name
    name = db.Column(db.String(100), nullable=False)
    # 原价
    original_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 优惠价
    special_price = db.Column(db.DECIMAL(10, 2), nullable=False)
    # 课时
    lessons = db.Column(db.INTEGER, nullable=False)


# 优惠券
class Coupon(db.Model):
    __tablename__ = 'coupon'

    # 折扣id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # 名称
    name = db.Column(db.String(100), nullable=False)
    # 代金券
    amount_ticket = db.Column(db.DECIMAL(10, 2), nullable=False, default=0.00)
    # 赠送课时
    extend_lessons = db.Column(db.INTEGER, nullable=False, default=0)
    # 折扣
    discount = db.Column(db.DECIMAL(4, 2), nullable=False, default=1.00)


# 订单表
class Order(db.Model):
    __tablename__ = 'order'

    # 订单id
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    # user_name 用户名称
    user_id = db.Column(db.INTEGER, db.ForeignKey('user.id'))
    # 关联的产品
    product_id = db.Column(db.INTEGER, db.ForeignKey('product.id'))
    # 优惠券
    coupon_id = db.Column(db.INTEGER, db.ForeignKey('coupon.id'))
    # 数量
    number = db.Column(db.INTEGER, nullable=False)
    # 订金
    deposit = db.Column(db.DECIMAL(10, 2), nullable=True, default=0.00)
    # 订单状态 ['done':'完成';'book':'订金']
    status = db.Column(db.String(20), nullable=False)

    # 订单创建时间
    create_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    # 订单完成时间
    complete_time = db.Column(db.DateTime, nullable=False)

    # 用户名称
    user_name = db.relationship(User, backref=db.backref('orders'))
    # 优惠券
    coupon_name = db.relationship(Coupon, backref=db.backref('orders'))
    # 产品名称
    product_name = db.relationship(Product, backref=db.backref('orders'))
