from flask_httpauth import HTTPBasicAuth
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer \
    as Serializer, BadSignature, SignatureExpired
from app.libs.error_code import AuthFailed

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(token, password):
    # token
    verify_token(token)
    return True


def verify_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except BadSignature as e:
        raise AuthFailed(msg='token is invalid')
    except SignatureExpired:
        raise AuthFailed(msg='token is expired')
    print(data)
