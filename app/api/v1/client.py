from app.libs.error_code import Success
from app.libs.redprint import Redprint
from app.validators.forms import ClientForm, UserEmailForm
from app.models.user import User
from app.libs.enums import ClientTypeEnum

api = Redprint('client')


@api.route('/register', methods=['POST', 'GET'])
def create_client():
    form = ClientForm().validate_for_api()
    promise = {
        ClientTypeEnum.USER_EMAIL: __register_user_by_email
    }
    promise[form.type]()
    return Success()


def __register_user_by_email():
    form = UserEmailForm().validate_for_api()
    User.register_by_email(form.nickname.data, form.account.data, form.secret.data)
