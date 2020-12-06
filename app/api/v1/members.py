from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.members import Members, Grade
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess
from app.validators.member_form import MemberForm, BindGrades
from sqlalchemy import or_, and_, Time
from flask import request

api = Redprint('members')


@api.route('', methods=['get'])
@auth.login_required
def get_members():
    params = request.args.to_dict()
    limit = params.get('limit')
    page = params.get('page')
    members = []
    count = 0
    if limit is None or page is None:
        members = Members.query.filter_by().order_by(Members.create_time.desc()).all()
        count = Members.query.filter_by().count()
    else:
        paginate = Members.query.filter_by().order_by(Members.create_time.desc()).paginate(int(page), int(limit))
        members = paginate.items
        count = paginate.total
    return Success(data=[item.to_dict() for item in members], count=count)


@api.route('/<int:member_id>', methods=['get'])
@auth.login_required
def get_member(member_id):
    member = Members.query.get_or_404(member_id, msg='member not found')
    return Success(data=member.to_dict())


@api.route('/search', methods=['get'])
@auth.login_required
def search_member():
    # name = request.args.get('name') or ''
    params = request.args.to_dict()
    name = params.get('name') or ''
    limit = params.get('limit')
    page = params.get('page')
    members = []
    count = 0
    if limit is None or page is None:
        members = Members.query.filter(Members.name.like('%' + name + '%'), Members.status == 1).all()
        count = len(members)
    else:
        paginate = Members.query.filter(and_(
            or_(Members.name.like('%' + name + '%'), Members.nickname.like('%' + name + '%')),
            Members.status == 1)) \
            .paginate(int(page), int(limit))
        members = paginate.items
        count = paginate.total

    return Success(data=[item.to_dict() for item in members], count=count)


@api.route('', methods=['POST'])
@auth.login_required
def create_member():
    form = MemberForm().validate_for_api()
    Members.add_member(form.name.data,
                       form.gender.data,
                       form.age.data,
                       form.mobile.data,
                       form.nickname.data,
                       form.grades)
    return CreateSuccess()


@api.route('/<int:uid>', methods=['PUT'])
@auth.login_required
def update_member(uid):
    with db.auto_commit():
        # 检查member是否存在
        member = Members.query.get_or_404(ident=uid, msg='member not found')
        # 校验修改的参数
        form = MemberForm().validate_for_api()
        # 开始修改
        member.name = form.name.data
        member.gender = form.gender.data
        member.age = form.age.data
        member.mobile = form.mobile.data
        member.nickname = form.nickname.data
    return Success(data=member.to_dict())


@api.route('/<int:uid>', methods=['delete'])
@auth.login_required
def delete_member(uid):
    with db.auto_commit():
        member = Members.query.filter_by(id=uid).first_or_404(msg='没有找到该会员')
        # 先删除关联班级
        member.grades = []
        # 删除会员
        member.delete()
    return DeleteSuccess()


'''
给会员分班
'''


@api.route('/bind_grades/<int:uid>', methods=['post'])
def bind_grades(uid):
    form = BindGrades().validate_for_api()
    member = Members.bind_grades(uid, form.grades)
    return Success(data=member.to_dict())


@api.route('/un_bind_grades/<int:uid>', methods=['post'])
def un_bind_grades(uid):
    form = BindGrades().validate_for_api()
    member = Members.un_bind_grades(uid, form.grade_ids.data)
    return Success(data=member.to_dict())
