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

@app.route('/ico_profile/', methods=['GET'])
def make_ico_profile_widget():
    name = request.args.get('token_name', None)
    if name is not None:
        return render_template("ico_profile.html",
                               token_name=name)
    else:
        return jsonify({'status': 400,
                        'error_message': 'No token short name provided!'})

@app.route('/diagram/')
def make_diagram_widget():
    labels = ["Red", "Blue", "Yellow", "Green", "Purple", "Orange"];
    data = [12, 19, 3, 5, 2, 3];

    if labels is not None:
        return render_template('diagram.html', values=data, labels=labels)
    else:
        return jsonify({'status': 400,
                        'error_message': 'No token short name provided!'})

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8080')
