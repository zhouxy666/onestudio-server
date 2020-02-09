from app.libs.error_code import CreateSuccess
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm, UserEmailForm, UserWxForm
from app.libs.enums import ClientTypeEnum
from app.models.user import User
from app.models.members import Members

api = Redprint('client')


@api.route('/register', methods=['POST', 'GET'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email,
        ClientTypeEnum.USER_WX: __register_by_wx
    }
    promise[form.type]()
    return CreateSuccess()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data,
                           form.account.data,
                           form.secret.data)


def __register_by_wx():
    form = UserWxForm().validate_for_api()
    Members.register_by_wx(form.name.data,
                           form.openid.data,
                           form.gender.data,
                           form.avatarurl.data,
                           form.age.data,
                           form.mobile.data,
                           form.nickname.data)
