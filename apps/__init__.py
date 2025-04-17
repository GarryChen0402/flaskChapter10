from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.testing.suite.test_reflection import users

from config import DevelopmentConfig
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from exts import mail

naming_convention = {
    'ix' : 'ix_%(column_0_label)s',
    'uq' : 'uq_%(table_name)s_%(column_0_name)s',
    'ck' : 'ck_%(table_name)s_%(column_0_name)s',
    'fk' : 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s',
    'pk' : 'pk_%(table_name)s'
}

# 实例化登陆管理器对象
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.session_protection = 'strong'
login_manager.login_message = '欢迎回来'

from apps.basic import basic_bp
from apps.cates import cates_bp
from apps.goods import goods_bp
from apps.users import users_bp
from apps.members import members_bp
from apps.orders import orders_bp

ckeditor = CKEditor()
csrf = CSRFProtect()

def create_app():
    app=Flask(__name__)
    # 加载配置文件
    app.config.from_object(DevelopmentConfig)
    # 登陆管理器初始化
    login_manager.init_app(app)
    # 加载蓝图
    app.register_blueprint(basic_bp, url_prefix='/basic')
    app.register_blueprint(cates_bp, url_prefix='/cates')
    app.register_blueprint(goods_bp, url_prefix='/goods')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(members_bp, url_prefix='/members')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    # 初始化数据库
    db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))
    db.init_app(app)
    # 数据库编辑器
    ckeditor.init_app(app)
    # CSRF初始化
    csrf.init_app(app)
    # 初始化邮件
    mail.init_app(app)
    return app
