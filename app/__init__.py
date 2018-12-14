'app/__init.py 放置app的工厂函数'

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import config

# 没有migrate和manager
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()


# app工厂函数：延迟创建app实例、注册蓝图
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    # 注册蓝图
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
