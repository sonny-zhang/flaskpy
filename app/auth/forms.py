from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Submit')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64),
                                                   Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                          'Usernames must have only letters, numbers, '
                                                          'dots or underscores')])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                             message='Passwords must match.')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        """Custom validation function, validate_ begins with a method followed by the field name,
        which is called with the regular validation function.
        """
        if User.query.filter_by(email=field.data).first():
            #: validate/verification/authentication failed
            raise ValidationError('Email already registered.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username already registered.')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    password = PasswordField('New Password', validators=[DataRequired(), EqualTo('password2',
                                                                                 message='Passwords must match.')])
    password2 = PasswordField('Confirm New Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Submit')


class PasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('password2',
                                                                                 message='Passwords must match!')])
    password2 = PasswordField('Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ChangeEmailForm(FlaskForm):
    email = StringField('New Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email already registered.')
