from flask import Flask, render_template
from flask_script import Manager
from flask_bootstrap import Bootstrap


app = Flask(__name__)
# flask_script扩展包，命令行解释器
bootstrap = Bootstrap(app)
manager = Manager(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)


if __name__ == '__main__':
    app.run()
