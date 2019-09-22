from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_required,\
    login_user, logout_user, current_user
import json
from redis import Redis

from factory_app import factory_app
from views.convert_to_rpn import rpn, preprocess
from views.implement_rpn import compute_rpn
from views.graphing import plot_function
from redispy import get_connection
from views.auth import User
from views.auth.login_form import auth

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
    expression = request.form['expression']
    print(expression)
    rpn_list = rpn(expression)
    val = compute_rpn(rpn_list)
    flash(f'{expression}')
    flash(f'{val}')
    #return redirect(url_for('index'))
    #return render_template('index.html')
    return jsonify({'val': str(val), 'expression': expression}), 200


@app.route('/graph_request', methods=['POST'])
def graph_request():
    expression = request.form['expression']
    print(expression)
    plot_function(expression, 0, 1)
    return redirect(url_for('graph'))

@app.route('/graph')
def graph():
    return render_template('graph.html')