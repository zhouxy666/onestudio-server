from flask import Blueprint

v2_blueprint = Blueprint('v2', __name__)

from app.api.v2 import user
