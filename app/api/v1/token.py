from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm
from app.models.user import User
from app.libs.enums import ClientTypeEnum

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: User.verify
    }
    # 验证账号
    user = promise[form.type](
        form.account.data,
        form.secret.data
    )
    # 生成token
    return generate_auth_token(uid=user.id, ac_type=form.type, auth=user.auth)


def generate_auth_token(uid, ac_type, auth):
    '''生成令牌'''
    s = Serializer(current_app.config['SECRET_KEY'],
                   expires_in=3600)
    return s.dumps({
        'uid': uid,
        'type': ac_type.value,
        'auth': auth
    }).decode('ascii')
