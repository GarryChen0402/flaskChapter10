from exts import db
from apps.common.base_model import BaseModel

class GoodsCategory(BaseModel):
    __tablename__ = 't_goods_category'
    cat_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), comment='分类名称')
    parent_id = db.Column(db.Integer, nullable=False, comment='父类ID')
    logo = db.Column(db.String(50), comment='分类logo图片')
    is_nav = db.Column(db.Boolean, default=False, comment='是否显示在导航栏中')
    sort = db.Column(db.Integer, comment='排序')
    goods = db.relationship('Goods', backref='back_cate', lazy=True)

    def __repr__(self):
        return self.name