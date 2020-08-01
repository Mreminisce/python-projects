import os
from flask import Flask
# __init__.py 文件有两个作用：一是包含应用工厂；二是告诉 Python flaskr 文件夹应当视作一个包。


def create_app(test_config=None): # create_app 是一个应用工厂函数
    app = Flask(__name__, instance_relative_config=True)
    # 创建 Flask 实例
    # __name__ 是当前 Python 模块的名称， 使用 __name__ 可以方便地告诉应用在哪里设置路径。
    # instance_relative_config=True 告诉应用配置文件使用相对于 instance folder 的相对路径。
    # instance 文件夹在 flaskr 包的外面，用于存放配置密钥和数据库等本地数据，不应当提交到版本控制系统。

    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    # create and configure the app, 设置一个应用的缺省配置
    # SECRET_KEY 是给应用保证数据安全的密钥。在开发过程中可以简单设置为 'dev'，
    # 但是在发布的时候必须使用一个随机值来重载它。
    # DATABASE 是 SQLite 数据库文件的存放路径，它位于 Flask 存放实例的 app.instance_path 之内。

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
        # load the instance config, if it exists, when not testing
        # 如果 config.py 存在的话就使用其中的值来重载缺省配置，例如在部署的时候设置正式的 SECRET_KEY。
    else:
        app.config.from_mapping(test_config)
        # load the test config if passed in
        # 把 test_config 传递给应用工厂并且替代实例配置，实现测试和开发的配置分离和相互独立。
    try:
        os.makedirs(app.instance_path)
        # ensure the instance folder exists，创建保存 SQLite 数据库文件的 app.instance_path 文件夹。
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World !'
    # a simple page that says hello，创建一个简单的路由

    from . import db
    db.init_app(app)                # 导入并注册数据库文件

    from . import auth
    app.register_blueprint(auth.bp) # 导入并注册 auth 蓝图

    from . import blog
    app.register_blueprint(blog.bp) # 导入并注册 blog 蓝图
    app.add_url_rule('/', endpoint='index')
    # 用 app.add_url_rule() 关联 'index' 和 '/' URL 可以使 url_for('index')
    # 和 url_for('blog.index') 都有效，生成同样的 '/' URL。

    return app
