from datetime import datetime
from flask import render_template, session, redirect, url_for, flash, current_app

from . import main


# flash是flask的核心特性：用户提交错误的表单信息，服务器发回的响应重新渲染表单，并显示一个消息提示用户
@main.route('/')
def index():
    return render_template('index.html')
