"""auth/views.py auth system view function module
    Introduce the auth blueprint, and use the route modifier of blueprint
to define authentication-related routes.
    flask_login: Manages the authentication status in the user authentication system, operation [user session].
"""
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from ..models import User
from .. import db
from ..email import send_email
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetRequestForm, PasswordResetForm


@auth.before_app_request
def before_request():
    """拦截请求：用户已登录+用户未认证+请求不在蓝图中"""
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
        Avoid template naming conflicts with the main blueprint
    and subsequent blueprints, and save the template used by the blueprint in a separate folder
    :return:
    """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            #: login_user():Marked as login status in user session.
            login_user(user, form.remember_me.data)
            #: 你必须验证 next 参数的值。如果不验证的话，你的应用将会受到重定向的攻击。
            #: 访问[未授权的URL]时会显示登录表单，Flask-Login会把原地址保存在args[查询字符串]的next参数中
            #: 如果args中没有next参数，就重定向到首页，否则就返回到之前访问的[未授权的URl]页面
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            print(next)
            return redirect(next)
        flash('邮箱或密码错误！')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account', 'auth/email/confirm',
                   user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', form=form)


@login_required
@auth.route('/confirm/<token>')
def confirm(token):
    """Bug: if request are't logged in, response will receive an error of 500."""
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        db.session.commit()
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@login_required
@auth.route('/confirm')
def resend_confirmation():
    """Resend the authentication confirmation email."""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Confirm Your Account', 'auth/email/confirm',
               user=current_user, token=token)
    flash('A new confirmation email has been sent to you by email.')
    return redirect(url_for('main.index'))


@login_required
@auth.route('/change_password', methods=['GET', 'POST'])
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash('Your password has been updated.')
            return redirect(url_for('main.index'))
        else:
            flash('Invalid password.')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            token = user.generate_reset_token()
            send_email(user.email, 'Confirm Your Account', 'auth/email/reset_password',
                       user=user, token=token)
            flash('请到你的邮箱确认要进行重置密码操作！')
            return redirect(url_for('auth.login'))
        flash('邮箱无效！')
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    # if not current_user.is_anonymous:
    #     return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        if User.reset_password(token, form.password.data):
            db.session.commit()
            flash('您的密码已经修改完成，请登录！')
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)
