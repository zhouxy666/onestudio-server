from flask import request
from app.libs.redprint import Redprint
from app.models.base import db
from app.models.members import Members
from app.validators.members import MembersForm
from app.libs.token_auth import auth
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess, NotFound

api = Redprint('members')


@api.route('', methods=['get'])
@auth.login_required
def get_members():
    members = Members.query.all()
    res_members = [dict(member) for member in members]
    return Success(data=res_members)


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
    form = MembersForm().validate_for_api()

    # 通过后创建member
    Members.create_member(form.name.data,
                          form.openid.data,
                          form.gender.data,
                          form.avatarurl.data,
                          form.age.data,
                          form.mobile.data,
                          form.nickname.data)
    return CreateSuccess()


@api.route('/<int:member_id>', methods=['delete'])
@auth.login_required
def delete_member(member_id):
    with db.auto_commit():
        member = Members.query.filter_by(id=member_id).first_or_404('member not exist')
        member.delete()
    return DeleteSuccess()
