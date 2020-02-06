from flask import Flask
from app.api.v2 import v2_blueprint


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')
    # app.register_blueprint(v2_blueprint, url_prefix='/v2')


def register_plugin(app):
    from app.models.base import db
    # 初始化db
    db.init_app(app)
    pass


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.db')
    # app.config.from_object('app.config.setting')
    # app.config.from_object('app.config.secure')

    # 注册插件
    register_plugin(app)

    # 注册蓝图
    register_blueprints(app)

    return app
