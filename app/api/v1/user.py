from app.libs.redprint import Redprint
from app.libs.token_auth import auth
from app.models.user import User
from app.libs.error_code import Success

api = Redprint('user')


@api.route('')
@auth.login_required
def get_users():
    users = User.query.all()
    res_users = [dict(item) for item in users]
    return Success(data=res_users)


@api.route('/<int:uid>')
@auth.login_required
def get_user(uid):
    user = User.query.get_or_404(uid, msg='user not Found')
    return Success(data=user)
