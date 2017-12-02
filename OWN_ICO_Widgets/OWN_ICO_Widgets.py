from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/token_profile/', methods=['GET'])
def make_token_profile_widget():
    name = request.args.get('token_short_name', None)
    if name is not None:
        return render_template("token_profile.html",
                               token_short_name=name)
    else:
        return jsonify({'status': 400,
                        'error_message': 'No token short name provided!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='80')
