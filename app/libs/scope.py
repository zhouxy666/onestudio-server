from app.libs.error_code import ServerError


class AuthBase(object):
    def __init__(self, auth, endpoint):
        self.auth = auth
        self.endpoint = endpoint
        self.module, self.view_fun = self.get_module_endpoint()

    def check_auth(self, **kwargs):
        modules = kwargs.get('modules')
        endpoints = kwargs.get('endpoints')

        if endpoints and self.endpoint in endpoints:
            return True

        if modules and self.module in modules:
            return True

        return False

    def get_module_endpoint(self):
        split_endpoint = self.endpoint.split('+')
        return split_endpoint[0], split_endpoint[1]


class AuthScope(AuthBase):
    # endpoint ==> v1.user+super_get_user
    # auth ==> super_get_user
    def __init__(self, auth, endpoint):
        super(AuthScope, self).__init__(auth, endpoint)

    def super_admin(self):
        modules = ['v1.user', 'v1.members', 'v1.grade', 'v1.attendance']
        return self.check_auth(modules=modules)

    def admin(self):
        modules = ['v1.members', 'v1.grade', 'v1.attendance']
        return self.check_auth(modules=modules)

    def user(self):
        endpoints = []
        return self.check_auth(endpoints=endpoints)

    def wx_user(self):
        pass

    def verify_auth(self):
        try:
            return getattr(self, self.auth)()
        except:
            raise ServerError()
