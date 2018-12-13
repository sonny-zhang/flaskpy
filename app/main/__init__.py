from flask import Blueprint
main = Blueprint('main', __name__)

# 为了避免循环导入依赖，因为在views,errors也会导入main
from . import views, errors
