from flask import Flask
from flask import render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/token_profile/')
def make_token_profile_widget():
    name = 'XAUR'
    return render_template("token_profile.html",
                           token_short_name=name)


if __name__ == '__main__':
    app.run()
