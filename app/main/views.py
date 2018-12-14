from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app

from . import main
from .forms import NameForm
from .. import db
from ..models import User
from ..eamil import send_email


# flash是flask的核心特性：用户提交错误的表单信息，服务器发回的响应重新渲染表单，并显示一个消息提示用户
@main.route('/', methods=['GET', 'POST'])
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
            if current_app.config['FLASK_ADMIN']:
                send_email(current_app.config['FLASK_ADMIN'], 'New User',
                          'mail/new_user', user=user)
        else:
            session['known'] = True
        # 使用请求上下文的会话功能，就会避免post表单提交，然后刷新造成的提示“提交表单”的问题
        session['name'] = form.name.data
        form.name.data = ''
        # 重定向==redirect('/');使用url_for的原因:使用URL映射生成URL,保证URL和定义的路由兼容，修改路由名字后依然可用
        # url_for的参数要使用蓝图的命名规则：.index / main.index
        return redirect(url_for('.index'))
    return render_template('index.html', form=form, name=session.get('name'), konwn=session.get('known', False),
                           current_time=datetime.utcnow())
