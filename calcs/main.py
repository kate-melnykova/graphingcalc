import os

from flask import Flask, render_template, request, redirect,\
    url_for, flash, jsonify, send_from_directory, send_file
from flask_login import LoginManager, UserMixin, login_required,\
    login_user, logout_user, current_user
# import flask_bootstrap
from flask_wtf import FlaskForm
import json
from redis import Redis

from factory_app import factory_app
from views.convert_to_rpn import rpn, preprocess
from views.implement_rpn import compute_rpn
from views.graphing import plot_function
from redispy import get_connection
from views.auth import User
from views.auth.login_form import auth
from views.exceptions import *

app, celery = factory_app()

######
# LoginManager setup
######
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def user_loader(username):
    user_db = get_connection(db=app.config['USER_DB']).get(username)
    if user_db is not None:
        return User.deserialize(user_db)
    else:
        return None


app.register_blueprint(auth)


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/schedule_calculation', methods=['POST'])
def schedule_calculation():
    try:
        expression = request.form['expression']
        print(expression)
        rpn_list = rpn(expression)
        val = compute_rpn(rpn_list)
        flash(f'{expression}')
        flash(f'{val}')
    except BaseApp as e:
        return jsonify({'error': e.message}), 500
    return jsonify({'val': str(val), 'expression': expression}), 200


default_plot_parameters = {'title': None,
                           'xlabel': None,
                           'ylabel': None,
                           'linecolor': 'b',
                           'isgrid': False,
                           'filename': 'plot.png'
                           }


@app.route('/graph_request', methods=['GET', 'POST'])
def graph_request():
    expression = request.args.get('expression')
    # add try-except
    xmin = float(request.args.get('xmin'))
    xmax = float(request.args.get('xmax'))

    # read all plot properties
    params = dict(default_plot_parameters)
    for p in default_plot_parameters:
        if request.args.get(p, None):
            params[p] = request.args[p]

    filename = params['filename']
    plot_function(expression, xmin, xmax, params=params)
    print(os.getcwd() + '/media/' + filename)
    return send_file(os.getcwd() + '/media/' + filename, as_attachment=False)


@app.route('/graph')
def graph():
    return render_template('graph.html')
