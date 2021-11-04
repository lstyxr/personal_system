from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_whooshee import Whooshee
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension, toolbar

app = Flask('mysystem')
app.secret_key = 'mysystem'
app.debug = True
toolbar = DebugToolbarExtension(app)

# 初始化 whooshee
whooshee = Whooshee(app)

# 使用配置
app.config.from_pyfile('config.py')

# 实例化数据库对象
db = SQLAlchemy(app)

# 自己创建的 commands.py 文件
from mysystem import commands

# 数据库同步相关
migrate = Migrate()
migrate.init_app(app, db=db)

# 初始化登录
login_manager = LoginManager(app)
login_manager.init_app(app)

from mysystem import views, commands, models