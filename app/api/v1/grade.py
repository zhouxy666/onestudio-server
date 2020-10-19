from wtforms.validators import ValidationError
from app.libs.redprint import Redprint
from app.models.grade import Grade
from app.libs.error_code import Success, DeleteSuccess, ParameterException, UpdateSuccess
from app.validators.grade_form import GradeForm, UpdateGradeForm, BindMembers
from sqlalchemy import or_, and_, Time
from flask import request, jsonify
from app.models.base import db

api = Redprint('grade')


@api.route('', methods=['get'])
def get_grades():
    params = request.args.to_dict()
    limit = params.get('limit')
    page = params.get('page')
    map_grades = []
    count = 0

    if limit is None or page is None:
        grades = Grade.query.filter_by().order_by(Grade.create_time.desc()).all()
        count = Grade.query.count()
    else:
        paginate = Grade.query.filter_by().order_by(Grade.create_time.desc()).paginate(int(page), int(limit))
        grades = paginate.items
        count = paginate.total

    return Success(data=[v.to_dict() for v in grades], count=count)


@api.route('/<int:uid>', methods=['get'])
def get_grade(uid):
    grade = Grade.query.get_or_404(ident=uid, msg="没有找到这个班级")
    return Success(data=grade.to_dict())


@api.route('', methods=['post'])
def add_grade():
    form = GradeForm().validate_for_api()
    '''
    查询设置的时间段是否已经有课程
    '''
    res_grade = Grade.query.filter(
        and_(Grade.week == form.week.data,
             or_(
                 and_(form.start_time.data >= Grade.start_time, form.start_time.data <= Grade.end_time),
                 and_(form.end_time.data >= Grade.start_time, form.end_time.data <= Grade.end_time)
             ),
             Grade.status == 1
             )) \
        .first()

    if res_grade is not None:
        return ParameterException(msg='{grade_name} 星期{week} {start_time}-{end_time} 已安排课程'
                                  .format(week=res_grade.week,
                                          start_time=res_grade.start_time,
                                          end_time=res_grade.end_time,
                                          grade_name=res_grade.grade_name))

    Grade.add_grade(form.grade_name.data,
                    form.week.data,
                    form.start_time.data,
                    form.end_time.data)
    return Success()


@api.route('/<int:grade_id>', methods=['put'])
def update_grade(grade_id):
    # 使用校验器校验剩余的参数
    form = UpdateGradeForm(grade_id).validate_for_api()
    grade = form.grade
    '''
    查询设置的时间段是否已经有课程
    '''
    res_grade = Grade.query.filter(
        and_(Grade.week == form.week.data,
             or_(
                 and_(form.start_time.data >= Grade.start_time, form.start_time.data <= Grade.end_time),
                 and_(form.end_time.data >= Grade.start_time, form.end_time.data <= Grade.end_time)
             ),
             Grade.id != grade_id,
             Grade.status == 1
             )) \
        .first()

    if res_grade is not None:
        return ParameterException(msg='{grade_name} 星期{week} {start_time}-{end_time} 已安排课程'
                                  .format(week=res_grade.week,
                                          start_time=res_grade.start_time,
                                          end_time=res_grade.end_time,
                                          grade_name=res_grade.grade_name))
    with db.auto_commit():
        grade.grade_name = form.grade_name.data
        grade.week = form.week.data
        grade.start_time = form.start_time.data
        grade.end_time = form.end_time.data
        grade.members = form.members

    return UpdateSuccess()


@api.route('/<int:uid>', methods=['delete'])
def delete_grade(uid):
    with db.auto_commit():
        grade = Grade.query.get_or_404(ident=uid, msg='没有找到该会员')
        # 先删除关联班级
        grade.members = []
        # 删除会员
        grade.delete()
    return DeleteSuccess()


@api.route('/bind_members/<int:gid>', methods=['post'])
def bind_members(gid):
    form = BindMembers().validate_for_api()
    grad = Grade.bind_members(gid, form.members)
    return Success(data=grad.to_dict())


@api.route('/un_bind_members/<int:gid>', methods=['post'])
def un_bind_members(gid):
    form = BindMembers().validate_for_api()
    grad = Grade.un_bind_members(gid, form.members)
    return Success(data=grad.to_dict())
