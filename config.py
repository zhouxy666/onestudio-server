import os

DEBUG = True
SECRET_KEY = os.urandom(24)

SERVER_NAME = '127.0.0.1:5000'
# 配置MYSQL
MYSQL_CONFIG = {
    'dialect': 'mysql',
    'driver': 'mysqldb',
    'username': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': '3306',
    'database': 'one_studio'
}

SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(**MYSQL_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
