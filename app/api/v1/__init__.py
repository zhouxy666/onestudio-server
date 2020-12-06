from flask import Blueprint
from app.api.v1 import user, book, client, token, members, grade, attendance


def create_blueprint_v1():
    bp_v1 = Blueprint('v1', __name__)

    user.api.register(bp_v1, url_prefix='/user')
    book.api.register(bp_v1, url_prefix='/book')
    client.api.register(bp_v1, url_prefix='/client')
    token.api.register(bp_v1, url_prefix='/token')
    members.api.register(bp_v1, url_prefix='/members')
    grade.api.register(bp_v1, url_prefix='/grade')
    attendance.api.register(bp_v1, url_prefix='/attendance')
    return bp_v1
