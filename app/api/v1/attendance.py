from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.error_code import Success

api = Redprint('attendance')


@api.route('', methods=['get'])
@auth.login_required
def get_attendance():
    return Success()


@api.route('', methods=['post'])
@auth.login_required
def create_attendance():
    return Success(data=222)
