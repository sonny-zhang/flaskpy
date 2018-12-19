from . import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app


# 定义模型：一对多
class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    # 关系的面向对象视角，返回与role相关联用户组的列表，参数1:模型. 参数backref:向User模型添加role属性
    users = db.relationship('User', backref='role')

    def __repr__(self):
        return '<Role {}>'.format(self.name)


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    # 建立外键的值，映射到roles表id
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    # password变成属性调用，可修改，不可查看
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        """ When setting the value of the password attribute, the assignment method
        calls the generate_password_hash() function provided by Werkzeug,
        It's result is assigned to the password_hash field.
        :param password: user's password
        :return: password_hash
        """
        self.password_hash = generate_password_hash(password)

    #: check password
    def verify_password(self, password):
        """
        Compares the user's password with the password_hash value stored in the User model.
        :param password: user's password
        :return: True or False
        """
        return check_password_hash(self.password_hash, password)

    #: Generates an authentication token
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    #: Confirm an authentication token. if pass, the confirmed property value is set to True
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True


# Flask-Login requires callback function to load the user with specified identifier.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
