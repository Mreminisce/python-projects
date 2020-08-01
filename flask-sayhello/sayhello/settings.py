import os
import sys

from sayhello import app


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


dev_db = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
# app.root_path 把数据库文件保存到项目根路径，可以改成 app.instance_path 保存到 instance 文件夹

SECRET_KEY = os.getenv('SECRET_KEY', 'secret string')
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', dev_db)

# Flask 的配置除了通过 config 对象直接写入外，还可以从单独的 settings.py 或 config.py 文件中读取  
# 在单独的文件中定义配置不再使用 config 对象，而是直接以键值对的方式写出
