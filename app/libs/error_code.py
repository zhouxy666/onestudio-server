from app.libs.error import ApiException


class ClientTypeError(ApiException):
    code = 400
    msg = 'client is invalid'
    error_code = 1006


class ParameterException(ApiException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class Success(ApiException):
    code = 200
    msg = 'success'
    error_code = 200
