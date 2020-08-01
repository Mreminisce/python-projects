from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from watchlist import db


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.String(4))
# 模型类必须继承 db.Model，创建的表名会自动小写处理
# 每一个类属性字段要实例化 db.Column 类并且传入类型参数

class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)    # 将生成的密码保持到对应字段

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password) # 验证密码后返回布尔值
# Werkzeug 内置了用于生成和验证密码散列值的函数
# 继承 Flask-Login 提供的 UserMixin 类
# 让 User 类继承 current_user，is_authenticated() 等几个用于判断认证状态的属性和方法
