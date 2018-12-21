from datetime import datetime
from flask import render_template, abort, session, redirect, url_for, flash, current_app
from . import main
from ..models import User


# flash是flask的核心特性：用户提交错误的表单信息，服务器发回的响应重新渲染表单，并显示一个消息提示用户
@main.route('/')
def index():
    return render_template('index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    return render_template('user.html', user=user)
