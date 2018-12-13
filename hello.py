from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import MigrateCommand, Migrate
from flask_mail import Mail, Message
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime
from threading import Thread
import os

basedir = os.path.abspath(os.path.dirname(__file__))

# 初始化flask应用
app = Flask(__name__)
# 设置秘钥，生成令牌
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
# 如果设置成 True (默认情况)，Flask-SQLAlchemy 将会追踪对象的修改并且发送信号。这需要额外的内存， 如果不必要的可以禁用它。
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Email配置
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['FLASK_MAIL_SUBJECT_PREFIX'] = '[Flaskpy]'
app.config['FLASK_MAIL_SENDER'] = 'Flasky Admin <758896823@qq.com>'
app.config['FLASK_ADMIN'] = os.environ.get('FLASK_ADMIN')

# 初始化bootstrap,然后就可以使用一个包含所有bootstrap文件的基模板
bootstrap = Bootstrap(app)
# Moment本地化时间
moment = Moment(app)
db = SQLAlchemy(app)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['FLASK_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr


# 定义模型：一对多
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 关系的面向对象视角，返回与role相关联用户组的列表，参数1:模型. 参数backref:向User模型添加role属性
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # 建立外键的值，映射到roles表id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)


# 表单类
class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')


# flash是flask的核心特性：用户提交错误的表单信息，服务器发回的响应重新渲染表单，并显示一个消息提示用户
@app.route('/', methods=['GET', 'POST'])
def index():
    # NameForm()实例表示表单
    form = NameForm()
    # validate_on_submit对表单数据进行验证(验证函数验证)
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.name.data).first()
        if user is None:
            user = User(username=form.name.data)
            db.session.add(user)
            db.session.commit()
            session['known'] = False
            flash('Looks like you have changed your name!')
            if app.config['FLASK_ADMIN']:
                send_email(app.config['FLASK_ADMIN'], 'New User',
                          'mail/new_user', user=user)
        else:
            session['known'] = True
        # 使用请求上下文的会话功能，就会避免post表单提交，然后刷新造成的提示“提交表单”的问题
        session['name'] = form.name.data
        form.name.data = ''
        # 重定向==redirect('/');使用url_for的原因:使用URL映射生成URL,保证URL和定义的路由兼容，修改路由名字后依然可用
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), konwn=session.get('known', False),
                           current_time=datetime.utcnow())


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.run(debug=True)
