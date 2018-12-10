from flask import Flask
from flask_script import Manager


app = Flask(__name__)
# flask_script扩展包，命令行解释器
manager = Manager(app)


@app.route('/')
def index():
    return '<h1>Hello World!</h1>'


@app.route('/user/<name>')
def user(name):
    return '<h1>Hello %s!</h1>' % name


if __name__ == '__main__':
    manager.run()
