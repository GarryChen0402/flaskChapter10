from flask_sqlalchemy import SQLAlchemy
from flask_ckeditor import  CKEditor
from flask_wtf import CSRFProtect
from flask_mail import Mail
from flask_cache import Cache
from celery import Celery
db=SQLAlchemy()
mail=Mail()
cache=Cache()
ckeditor= CKEditor()
csrf = CSRFProtect()
celery_app=Celery()