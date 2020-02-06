from app.api.v2 import v2_blueprint


@v2_blueprint.route('/user')
def get_user():
    return 'user'
