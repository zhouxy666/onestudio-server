from app.libs.redprint import Redprint
from flask_restful import Resource, Api

api = Redprint('user')


@api.route('/get')
def get_user():
    return 'i am user'
