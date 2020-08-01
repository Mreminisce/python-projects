from datetime import datetime

from sayhello import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    body = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    # 时间戳字段，utcnow 生成不包含时区信息的 UTC 格式时间，index=True 开启索引
