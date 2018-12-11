from flask import Flask, render_template, session, redirect, url_for, flash
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
# manager = Manager(app)
moment = Moment(app)


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
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Look like you have changed your name!')
        # 使用请求上下文的会话功能，就会避免post表单提交，然后刷新造成的提示“提交表单”的问题
        session['name'] = form.name.data
        # 重定向==redirect('/');使用url_for的原因:使用URL映射生成URL,保证URL和定义的路由兼容，修改路由名字后依然可用
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'), current_time=datetime.utcnow())


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
