import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy # flask-sqlalchemy 库, 依赖于 SQLAlchemy
from flask_login import LoginManager    # flask-login 库


WIN = sys.platform.startswith('win')    # SQLite URI compatible
if WIN:
    prefix = 'sqlite:///'               # 数据库文件的绝对地址
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# os.getenv 读取系统环境变量 SECRET_KEY 的值，如果没有获取到则使用 dev
# app.config 告诉 SQLAlchemy 数据库连接地址，注意配置变量的最后一个单词是 URI 不是 URL
# app.root_path 返回程序实例所在模块的路径，也就是项目根目录
# 数据库文件一般用 .db、.sqlite 和 .sqlite3 作为后缀
# 最后关闭对模型修改的监控，在扩展类实例化前加载配置

db = SQLAlchemy(app)                    # 初始化 sqlalchemy 扩展，传入程序实例 app
login_manager = LoginManager(app)       # 实例化 flask-login 扩展类


@login_manager.user_loader
def load_user(user_id): 
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user
# 用户加载回调函数，接受用户 ID 作为参数
# Flask-Login 提供了一个 current_user 变量在用户登录后保存模型记录


login_manager.login_view = 'login'
# 让 login_required 重定向操作正确执行
# 如果需要还可以设置 login_manager.login_message 来自定义错误提示消息


@app.context_processor
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user) 
# 可以使用 app.context_processor 装饰器来注册多个模板内都需要使用的变量
# 在这里注册一个模板上下文处理函数，函数返回一个字典注入到模板的上下文环境中
# 让后面创建的任意一个模板都可以直接使用 user 变量


from watchlist import views, errors, commands
