from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.libs.error_code import Success

api = Redprint('book')


@api.route('')
@auth.login_required
def get_book():
    return Success()
