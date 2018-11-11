from flask import Flask

app = Flask(__name__)


@app.route("/")
def index():
    return "<hl>Hello Word!<hl/>"


@app.route("/user/<name>")
def user(name):
    return "<h1>Hello, {}!<h1/>".format(name)


if __name__ == "__main__":
    app.run(debug=True)
