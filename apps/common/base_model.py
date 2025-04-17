from exts import db
from datetime import datetime

class BaseModel(db.Model):
    '''
    抽象基类
    '''

    __abstract__ = True

    create_time = db.Column(db.DateTime, nullable=False, default=datetime.now, comment='创建时间')
    update_time = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now, comment='更新时间')