from flask import Flask
from flask import jsonify
from flask import render_template
from flask import request

from blockchain.git_analytics import get_git_commit_widget
from blockchain.contract_analysis import token_summary_data
from blockchain.provider import symbol
from blockchain.contract_analysis import reputation

from blockchain.contract_analysis import holders_chart_data

from blockchain.contract_analysis import ico_chart_data

app = Flask(__name__)


def pretty_numbers(value, r=2):
    return '{:,}'.format(round(value, r)).replace(',', ' ')


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/ico_info/', methods=['GET'])
def make_ico_info_widget():
    name = request.args.get('token_name', None)
    price_usd, price_btc, total_volume, market_cap, change_percent = token_summary_data(name)
    short_name = symbol(name)
    color = "red"
    if change_percent > 0:
        color = "green"
    if change_percent == 0:
        color = "yellow"
    if name is not None:
        return render_template("index.html",
                               token_name=name,
                               color = color,
                               short_name=short_name,
                               price_usd=pretty_numbers(price_usd),
                               price_btc=price_btc,
                               total_volume=pretty_numbers(total_volume),
                               market_cap=pretty_numbers(market_cap, 0),
                               change_percent=pretty_numbers(change_percent),
                               )
    else:
        return jsonify({'status': 400,
                        'error_message': 'Wrong token name provided!'})


@app.route('/ico_statistic/', methods=['GET'])
def make_ico_chart_widget():
    name = request.args.get('token_name', None)
    labels, cumulative_values = ico_chart_data(name)

    if name is not None:
        return render_template("ico_history.html",
                               token_name=name,
                               labels=labels,
                               cumulative_values=cumulative_values
                               )
    else:
        return jsonify({'status': 400,
                        'error_message': 'Wrong token name provided!'})


@app.route('/holders/', methods=['GET'])
def make_holders_widget():
    name = request.args.get('token_name', None)
    labels, data = holders_chart_data(name, 2)

    if labels is not None:
        return render_template('pie_chart.html', values=data, labels=labels)
    else:
        return jsonify({'status': 400,
                        'error_message': 'Wrong token name provided!'})


@app.route('/git_stat/', methods=['GET'])
def make_git_stat_widget():
    name = request.args.get('token_name', None)
    state, stars, forks, x, y = get_git_commit_widget(name)
    if state:
        return render_template("git_info.html",
                               token_name=name,
                               stars=stars,
                               forks=forks,
                               values=y,
                               labels=x
                               )
    else:
        return jsonify({'status': 400,
                        'error_message': 'Wrong token name provided!'})


@app.route('/reputation/', methods=['GET'])
def make_reputation_widget():
    name = request.args.get('token_name', None)
    state = reputation(name)

    if state is not None:
        color = 'black'
        if state == 'OK ':
            color = 'green'
        if state =='NEUTRAL ':
            color = 'yellow'
        if(state =='SUSPICIOUS '):
            color = 'blue'
        if (state == 'UNSAFE '):
            color = 'red'
        print(color)
        print(state)
        return render_template("reputation.html",
                               token_name=name,
                               color=color,
                               state=state
                               )
    else:
        return jsonify({'status': 400,
                        'error_message': 'Wrong token name provided!'})






# @app.route('/token_summary/', methods=['GET'])
# def make_token_profile_widget():
#     name = request.args.get('token_name', None)
#     if name is not None:
#         return render_template("index.html",
#                                token_name=name)
#     else:
#         return jsonify({'status': 400,
#                         'error_message': 'No token short name provided!'})

# @app.route('/ico_profile/', methods=['GET'])
# def make_ico_profile_widget():
#     name = request.args.get('token_name', None)
#     if name is not None:
#         return render_template("ico_profile.html",
#                                token_name=name)
#     else:
#         return jsonify({'status': 400,
#                         'error_message': 'No token short name provided!'})
#
# @app.route('/token_profile/', methods=['GET'])
# def make_token_profile_widget():
#     name = request.args.get('token_short_name', None)
#     if name is not None:
#         return render_template("token_profile.html",
#                                token_name=name)
#     else:
#         return jsonify({'status': 400,
#                         'error_message': 'No token short name provided!'})
#
#
# @app.route('/token_profile/', methods=['GET'])
# def make_token_profile_widget():
#     name = request.args.get('token_short_name', None)
#     if name is not None:
#         return render_template("token_profile.html",
#                                token_name=name)
#     else:
#         return jsonify({'status': 400,
#                         'error_message': 'No token short name provided!'})





if __name__ == '__main__':
    app.run(host='0.0.0.0', port='82')
