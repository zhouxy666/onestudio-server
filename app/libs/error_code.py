from app.libs.error import ApiException


class Success(ApiException):
    code = 200
    msg = 'success'
    error_code = 200


# 参数错误
class ParameterException(ApiException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


# 资源无法访问
class NotFound(ApiException):
    code = 400
    msg = 'the resource is not found'
    error_code = 1001


# 鉴权失败
class AuthFailed(ApiException):
    '''
    1003 password is error
    '''
    code = 401
    msg = 'authorization failed'
    error_code = 1005
