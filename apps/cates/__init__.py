from flask import Blueprint

cates_bp = Blueprint('cates', __name__, url_prefix='/cates')

from apps.cates import views