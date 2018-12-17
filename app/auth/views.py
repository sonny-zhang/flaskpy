from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required
from . import auth
from ..models import User
from .forms import LoginForm


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            nextd = request.args.get('next')
            print(nextd)
            if nextd is None or not nextd.startswith('/'):
                nextd = url_for('main.index')
            print(nextd)
            return redirect(nextd)
        flash('Invalid username or password.')
    return render_template('auth/login.html', form=form)


@login_required
@auth.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))

