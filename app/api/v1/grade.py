from flask import request, jsonify
from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.base import db
from app.models.members import Members
from app.libs.error_code import Success, CreateSuccess, DeleteSuccess
from app.validators.forms import MemberForm
from flask import request

api = Redprint('grade')


@api.route('', methods=['get'])
def get_grade():
    return 'hello,world'
    pass


@api.route('', methods=['post'])
def add_grade():
    return 'add,grade'
    pass
