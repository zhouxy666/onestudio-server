from flask import request, jsonify
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.members import Members, Grade
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess
from app.validators.forms import MemberForm, DivideGradesForm
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
        print(members)
        count = Members.query.count()
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
    name = request.args.get('name') or ''
    members = Members.query.filter(Members.name.like('%' + name + '%'), Members.status == 1).all()
    res_members = [v.to_dict() for v in members]
    if len(members) == 0:
        return Success(data=res_members, msg='member is not found')
    return Success(data=res_members)


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
        member.grades = form.grades
    return Success()


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


@api.route('/divide_grades', methods=['post'])
def bind_grades():
    form = DivideGradesForm().validate_for_api()
    members = Members.divide_grades(form.member_id.data, form.grade_ids.data)
    print(members)
    return Success()
