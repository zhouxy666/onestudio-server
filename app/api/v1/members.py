from flask import request, jsonify
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.members import Members
from app.validators.members import MembersForm, CreateMembersForm
from app.libs.token_auth import auth
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess, UpdateSuccess

api = Redprint('members')


@api.route('', methods=['get'])
@auth.login_required
def get_members():
    pagination = dict(request.args)
    page = int(pagination.get('page')) or 1
    size = int(pagination.get('size')) or 10
    members = Members.query.order_by(Members.create_time.desc())\
        .limit(size).offset((page - 1) * size).all()
    data = {
        'members': [dict(member) for member in members],
        'count': Members.query.count()
    }
    return Success(data=data)


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


@api.route('/create', methods=['post'])
@auth.login_required
def create_member():
    # 校验表单
    # form = CreateMembersForm().validate_for_api()
    # form = MembersForm().validate_for_api()
    form = CreateMembersForm().validate_for_api()

    # 通过后创建member
    Members.create_member(form.name.data,
                          form.openid.data,
                          form.gender.data,
                          form.avatarurl.data,
                          form.age.data,
                          form.mobile.data,
                          form.nickname.data)
    return CreateSuccess()


@api.route('/<int:member_id>', methods=['put'])
@auth.login_required
def update_member(member_id):
    member = Members.query.get_or_404(member_id)
    # 校验表单
    form = MembersForm().validate_for_api()
    with db.auto_commit():
        for key in form:
            if key.data:
                setattr(member, key.name, key.data)
        return UpdateSuccess()


@api.route('/<int:member_id>', methods=['delete'])
@auth.login_required
def delete_member(member_id):
    with db.auto_commit():
        member = Members.query.filter_by(id=member_id).first_or_404('member not exist')
        member.delete()
    return DeleteSuccess()
