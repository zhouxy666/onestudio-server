from flask import Flask
from exts import db
import config

app = Flask(__name__)
app.config.from_object(config)

# 初始化数据库
db.init_app(app)


@app.route('/')
def hello():
    return 'hello,world'


if __name__ == '__main__':
    app.run()
