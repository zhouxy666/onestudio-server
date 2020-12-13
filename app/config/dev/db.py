# 配置MYSQL
MYSQL_CONFIG = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'root',
    'password': '1234',
    'host': 'localhost',
    'port': '3306',
    'database': 'onestudio_dev',
    # 'database': 'onestudio_test',
}

SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
    **MYSQL_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
