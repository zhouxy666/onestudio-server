from app.libs.error_code import ServerError, AuthScopeFailed, NotFound


class AuthBase(object):
    def __init__(self, auth, endpoint):
        self.auth = auth
        self.endpoint = endpoint
        self.module, self.view_fun = self.get_module_endpoint()

    def check_auth(self, **kwargs):
        modules = kwargs.get('modules')
        endpoints = kwargs.get('endpoints')
        #
        # if endpoints and self.endpoint in endpoints:
        #     return True
        #
        # if modules and self.module in modules:
        #     return True

        if endpoints is not None:
            if self.endpoint in endpoints:
                return True
            else:
                # raise AuthScopeFailed(msg='endpoint %s is not allowed' % self.endpoint)
                return False

        if modules is not None:
            if self.module in modules:
                return True
            else:
                # raise AuthScopeFailed(msg='module %s is not allowed' % self.module)
                return False

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
        modules = ['v1.user', 'v1.members']
        return self.check_auth(modules=modules)

    def admin(self):
        modules = ['v1.user', 'v1.members']
        return self.check_auth(modules=modules)

    def user(self):
        endpoints = ['v1.user+get_user',
                     'v1.user+delete_user',
                     'v1.user+update_user',
                     'v1.user+create_user']
        return self.check_auth(endpoints=endpoints)

    def wx_user(self):
        pass

    def verify_auth(self):
        try:
            return getattr(self, self.auth)()
        except:
            raise ServerError()
