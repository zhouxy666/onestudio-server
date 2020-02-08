from werkzeug.exceptions import HTTPException
from flask_cors import CORS
from app.app import create_app

from app.libs.error import ApiException

app = create_app()


@app.errorhandler(Exception)
def framework_error(e):
    if isinstance(e, ApiException):
        return e
    if isinstance(e, HTTPException):
        code = e.code
        msg = e.description
        error_code = 1007
        return ApiException(msg=msg, code=code, error_code=error_code)
    else:
        if not app.config['DEBUG']:
            return ApiException()


if __name__ == '__main__':
    CORS(app, supports_credentials=True)
    app.run()
