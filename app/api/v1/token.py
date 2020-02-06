from app.libs.redprint import Redprint
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import jsonify, current_app

api = Redprint('token')


@api.route('', methods=['POST'])
def get_token():
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
    token = s.dumps({'id': 'zhouxy'}).decode('ascii')
    return token
