from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

app = Flask('sayhello')               # 硬编码程序路径获取包名称，等同于 __name__.split('.')[0]
app.config.from_pyfile('settings.py') # from_pyfile() 加载配置文件
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

db = SQLAlchemy(app)
moment = Moment(app)                  # 使用 flask-moment 库集成 Moment.js，国际化处理日期和时间
bootstrap = Bootstrap(app)
# 实例化 Bootstrap-flask 库，可以提供在模板中使用的 load_css() 和 load_js() 等方法
# Bootstrap-flask 默认从 CDN 加载 bootstrap 资源
# 可以配置 BOOTSTRAP_SERVE_LOCAL = True 选项换成使用本地资源，调试模式下则自动使用本地资源 


from sayhello import views, errors, commands
# 导入模块，让其他文件和程序实例关联起来
# 模块需要从构造文件中导入程序实例，为了避免循环依赖，因此导入语句在文件末尾定义