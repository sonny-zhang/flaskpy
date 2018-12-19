"""app/__init.py factory function run app:
    After the process of creating the program has moved into the factory function,
the blueprint can be used to de define the route in the global scope.

We use different blueprint for different program functions.
"""

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_login import LoginManager
from config import config


#: 没有migrate和manager
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
#: To initialize Flask-Login, you need these three sentences.
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'


# app工厂函数：延迟创建app实例、注册蓝图
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)

    # main blueprint
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    """" The Route associated with the user authentication systems can be defined in the auth blueprint.
        url_prefix:optional parameters  
        With this parameter,all routes defined in the registered blueprint are prefixed with
    the specified prefix.
    """
    from .auth import auth as auth_bluprint
    app.register_blueprint(auth_bluprint, url_prefix='/auth')

    return app
