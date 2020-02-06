import os

DEBUG = True
SERVER_NAME = '127.0.0.1:5000'
SECRET_KEY = os.urandom(24)

# 配置MYSQL
MYSQL_CONFIG = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': '3306',
    'database': 'onestudio_study'
}

SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
    **MYSQL_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
