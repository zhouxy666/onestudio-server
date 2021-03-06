from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm
from app.models.user import User
from app.models.members import Members
from app.libs.enums import ClientTypeEnum
from app.libs.error_code import Success

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify,
        ClientTypeEnum.USER_WX: Members.verify
    }
    # 验证账号
    user = promise[form.type](
        form.username.data,
        form.password.data
    )

    # 获取用户的权限
    auth_map = {
        1: 'super_admin',
        2: 'admin',
        3: 'user',
        4: 'wx_user'
    }
    user_auth = auth_map[user.auth]
    # 生成token
    return Success(data=generate_auth_token(uid=user.id, ac_type=form.type, auth=user_auth))


def generate_auth_token(uid, ac_type, auth):
    '''生成令牌'''
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=3600)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'auth': auth
    }).decode('ascii')
