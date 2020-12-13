from flask import Flask


def register_blueprints(app):
    from app.api.v1 import create_blueprint_v1
    app.register_blueprint(create_blueprint_v1(), url_prefix='/v1')


def register_plugin(app):
    from app.models.base import db
    # 初始化db
    db.init_app(app)
    pass


def create_app():
    app = Flask(__name__)
    print('... ENV ...', app.config['ENV'])

    if app.config['ENV'] == 'development':
        app.config.from_object('app.config.dev.db')
        app.config.from_object('app.config.dev.setting')
        app.config.from_object('app.config.dev.secure')
    else:
        app.config.from_object('app.config.prod.db')
        app.config.from_object('app.config.prod.setting')
        app.config.from_object('app.config.prod.secure')

    # 注册蓝图
    register_blueprints(app)

    # 注册插件
    register_plugin(app)

    return app
