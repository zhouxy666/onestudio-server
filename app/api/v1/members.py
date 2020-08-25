from flask import request, jsonify
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.members import Members
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess
from app.validators.forms import MemberForm
from flask import request

api = Redprint('members')


@api.route('', methods=['get'])
def get_members():
    params = request.args.to_dict()
    limit = params.get('limit')
    page = params.get('page')
    members = []
    count = 0
    # count = len(Members.query.filter_by().all())
    # members = Members.query.filter_by().order_by(Members.create_time.desc()).limit(limit).offset((page - 1) * limit)
    if limit is None or page is None:
        members = Members.query.filter_by().order_by(Members.create_time.desc()).all()
        count = Members.query.count()
    else:
        paginate = Members.query.filter_by().order_by(Members.create_time.desc()).paginate(int(page), int(limit))
        members = paginate.items
        count = paginate.total
    res_members = [dict(item) for item in members]
    return Success(data=res_members, count=count)


@api.route('/<int:member_id>', methods=['get'])
@auth.login_required
def get_member(member_id):
    member = Members.query.get_or_404(member_id, msg='member not found')
    return Success(data=member)


@api.route('/search', methods=['get'])
@auth.login_required
def search_member():
    name = request.args.get('name') or ''
    members = Members.query.filter(Members.name.like('%' + name + '%'))
    res_members = [dict(member) for member in members]
    if len(res_members) == 0:
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
                       form.nickname.data)
    return CreateSuccess()


@api.route('', methods=['PUT'])
@auth.login_required
def update_member():
    form = MemberForm().validate_for_api()
    Members.update_member(form.id.data,
                          form.name.data,
                          form.gender.data,
                          form.age.data,
                          form.mobile.data,
                          form.nickname.data)
    return Success()


@api.route('/<int:uid>', methods=['delete'])
@auth.login_required
def delete_member(uid):
    with db.auto_commit():
        member = Members.query.filter_by(id=uid).first_or_404(msg='没有找到该会员')
        member.delete()
    return DeleteSuccess()
