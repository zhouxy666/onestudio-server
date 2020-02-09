from flask import current_app, g, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed
from collections import namedtuple
from app.libs.scope import AuthScope

UserTuple = namedtuple('User', ['uid', 'type', 'auth'])

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    # 验证token
    user_info = verify_token(token)
    # 用户获取token成功后，把用户的信息存入g变量中
    g.user = user_info
    # 权限控制，根据auth和endpoint，控制用户的访问权限
    return AuthScope(user_info.auth, request.url_rule.endpoint).verify_auth()


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature as e:
        raise AuthFailed(msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(msg='token is expired')

    return UserTuple(data['uid'], data['type'], data['auth'])
