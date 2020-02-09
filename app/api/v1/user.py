from flask import g
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.models.base import db
from app.libs.error_code import Success, DeleteSuccess, AuthFailed

api = Redprint('user')

'''
超级管理员
'''


@api.route('/all')
@auth.login_required
def get_users():
    users = User.query.all()
    res_users = [dict(item) for item in users]
    return Success(data=res_users)


@api.route('/<int:uid>', methods=['GET'])
@auth.login_required
def super_get_user(uid):
    user = User.query.get_or_404(uid, msg='user not found')
    return Success(data=user)


@api.route('/<int:uid>', methods=['delete'])
@auth.login_required
def super_delete_user(uid):
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404(msg='user not found')
        user.delete()
    return DeleteSuccess()


'''
普通用户
'''


@api.route('', methods=['GET'])
@auth.login_required
def get_user():
    uid = g.user.uid
    user = User.query.get_or_404(uid, msg='user not found')
    return Success(data=user)


@api.route('', methods=['delete'])
@auth.login_required
def delete_user():
    '''
    为了防止删除用户出现越权的问题,uid必须要重token中获取，不能让用户自己去制定
    '''
    uid = g.user.uid
    with db.auto_commit():
        user = User.query.filter_by(id=uid).first_or_404(msg='user not found')
        user.delete()
    return DeleteSuccess()


@api.route('/<int:uid>', methods=['put'])
def update_user(uid):
    pass


@api.route('/<int:uid>', methods=['post'])
def create_user(uid):
    pass
