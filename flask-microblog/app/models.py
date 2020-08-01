from datetime import datetime
from hashlib import md5
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


followers = db.Table(
    'followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # index 参数设置字段可索引
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    # backref 参数定义外键中代表'多'的模型反向调用'一'时使用的属性名称，比如 post.author
    # lazy='dynamic' 把查询设置为动态，即只在被调用时才会执行
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    followed = db.relationship(
        'User', 
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), 
        lazy='dynamic'
    )
    # secondary 指定用于该关系的关联表
    # primaryjoin 指明通过关系表关联到左侧实体（关注者）的条件
    # secondaryjoin 指明通过关系表关联到右侧实体（被关注者）的条件
    # followers.c.follower_id 表示引用关系表中的 follower_id 列
    # backref 定义右侧实体访问该关系的方式

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        return 'https://www.gravatar.com/avatar/?d=identicon'
    # 生成随机头像   

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)    

    def followed_posts(self):
        own = Post.query.filter_by(user_id=self.id)
        followed = Post.query.join(
            followers, 
            (followers.c.followed_id == Post.user_id)
        ).filter(followers.c.follower_id == self.id)

        return followed.union(own).order_by(Post.timestamp.desc())
    # 联合查询用户自己和已关注用户的动态


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
