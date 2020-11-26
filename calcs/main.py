import os

from flask import Flask, render_template, request, redirect,\
    url_for, flash, jsonify, send_from_directory, send_file
from flask_login import LoginManager, UserMixin, login_required,\
    login_user, logout_user, current_user
# import flask_bootstrap
from flask_wtf import FlaskForm
import json
from redis import Redis

from views.forms import GraphingForm, ComputeForm
from factory_app import factory_app
from model import db, User
from views.convert_to_rpn import rpn, preprocess
from views.implement_rpn import compute_rpn
from views.graphing import plot_function
# from redispy import get_connection
# from views.graphing_setting import default_plot_parameters
# from views.auth import User
from views.auth.login_form import auth
from views.exceptions import *

app, celery = factory_app()

######
# LoginManager setup
######
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    """Check if user is logged-in on every page load."""
    return None if user_id is None else User.query.get(user_id)


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.register'))


app.register_blueprint(auth)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html',
                               form=ComputeForm())

    return render_template('index.html',
                           form=ComputeForm())



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


@app.route('/graph', methods=['GET', 'POST'])
def graph():
    if request.method == 'GET':
        return render_template('graph.html', form=GraphingForm())

    return render_template('graph.html', form=GraphingForm())


@app.route('/graph_request', methods=['GET', 'POST'])
def graph_request():
    filename = plot_function(raw_data=request.args)
    return send_file(filename, as_attachment=False)


@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


@app.route('/settings')
@login_required
def settings():
    return render_template('edit_profile.html')
