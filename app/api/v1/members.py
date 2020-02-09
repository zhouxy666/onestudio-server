from app.libs.redprint import Redprint
from app.models.members import Members
from app.libs.error_code import Success

api = Redprint('members')


@api.route('')
def get_members():
    members = Members.query.first()
    return Success(data=members)


@api.route('/create')
def create_member():
    return 'create'
