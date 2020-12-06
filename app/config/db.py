# 配置MYSQL
MYSQL_CONFIG = {
    'dialect': 'mysql',
    'driver': 'pymysql',
    'username': 'root',
    'password': '123456',
    # 'host': 'localhost',
    'host': '106.53.240.98',
    'port': '3306',
    # 'database': 'onestudio_dev',
    # 'database': 'onestudio_test',
    'database': 'onestudio'
}

SQLALCHEMY_DATABASE_URI = '{dialect}+{driver}://{username}:{password}@{host}:{port}/{database}?charset=utf8'.format(
    **MYSQL_CONFIG)
SQLALCHEMY_TRACK_MODIFICATIONS = False
