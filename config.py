import os
base_dir=os.path.abspath(os.path.dirname(__file__))
SECRET_KEY="12345678!@#$%^&*"
import datetime
import os

class BaseConfig(object):
    SECRET_KEY="12345678!@#$%^&*"

class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gyc:051342gyc@localhost:3306/flaskChapter10?charset=utf8mb4"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=90)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 90,
        'pool_recycle': 7200,
        'max_overflow': 1024
    }
    SQLALCHEMY_ECHO = False  # 打印SQL

    #SERVER_NAME="/"
    #APPLICATION_ROOT="/"
    PREFERRED_URL_SCHEME="/"
    #编辑器配置
    CKEDITOR_SERVE_LOCAL=True
    CKEDITOR_HEIGHT=400
    CKEDITOR_FILE_UPLOADER="goods.uploads"
    UPLOADED_PATH=os.path.join(base_dir,r"media\uploads")
    CKEDITOR_WIDTH=500
    #邮件配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USERNAME = 'gychen0402@foxmail.com'
    MAIL_PASSWORD = 'mptoiqkloszqgbhc'
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEFAULT_SENDER = ('admin', '579344125@qq.com')

    #缓存配置
    CACHE_TYPE="redis"
    CACHE_REDIS_HOST="localhost"
    CACHE_REDIS_PORT=6379
    CACHE_REDIS_PASSWORD="051342gyc"
    CACHE_REDIS_DB= 5

    #分布式任务队列
    CELERY_BROKER_URL = "redis://default:051342gyc@localhost:6379/10"
    CELERY_RESULT_BACKEND = "redis://default:051342gyc@localhost:6379/11"
    CELERYBEAT_SCHEDULE = {
                        'run_build_index': {
                        'task': 'tasks.build_index',
                        'schedule': datetime.timedelta(seconds=30)  # 定时任务间隔，这里设置为30秒
                        },
                        }

class Test(BaseConfig):
    pass


class ProductionConfig(BaseConfig):
    #正式数据库
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://gyc:051342gyc@localhost:3306/flaskChapter10Production?charset=utf8mb4"
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(days=90)
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 5,
        'pool_timeout': 90,
        'pool_recycle': 7200,
        'max_overflow': 1024
    }
    SQLALCHEMY_ECHO = True  # 取消打印SQL
    CKEDITOR_SERVE_LOCAL = True
    CKEDITOR_HEIGHT = 400
    CKEDITOR_FILE_UPLOADER = "goods.uploads"
    UPLOADED_PATH = os.path.join(base_dir, "ch10/myshop-admin/migrations/uploads")
    CKEDITOR_WIDTH = 500


config = {
    # "dev": DevelopmentConfig,
    "development": DevelopmentConfig,
    "test": Test,
    # "prod": ProductionConfig,
    "production": ProductionConfig
}