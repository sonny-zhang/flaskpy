'main/__init__.py 创建蓝图'

from flask import Blueprint
# 创建蓝图
main = Blueprint('main', __name__)

# 为了避免循环导入依赖，因为在views,errors也会导入main
from . import views, errors
from ..models import Permission


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
