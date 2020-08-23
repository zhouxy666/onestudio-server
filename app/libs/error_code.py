from app.libs.error import ApiException


class Success(ApiException):
    code = 200
    msg = 'success'
    error_code = 0


class DeleteSuccess(Success):
    code = 202
    error_code = 0


class CreateSuccess(ApiException):
    code = 201
    msg = 'create_success'
    error_code = 0


# 参数错误
class ParameterException(ApiException):
    code = 400
    msg = 'invalid parameter'
    error_code = 40000


# 资源无法访问
class NotFound(ApiException):
    code = 400
    msg = 'the resource is not found'
    error_code = 40004


# 鉴权失败
class AuthFailed(ApiException):
    '''
    1003 password is error
    '''
    code = 401
    msg = 'authorization failed'
    error_code = 40001


class ServerError(ApiException):
    code = 500
