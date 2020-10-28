import datetime

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user, login_required, logout_user #, current_user
# from redis import Redis
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField, SubmitField
from wtforms import validators

# from views.auth import User
from model import db, User
# from redispy import get_connection


class RegistrationForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
        validators.Length(min=6, max=35),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField()


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    password = PasswordField('Password', [validators.Length(min=6, max=35)])
    submit = SubmitField()


def generate_error_message(form_errors):
    error_message = f''
    for k, v in form_errors.items():
        error_message += f""" -- {k}: {v[0]} \n"""
    return error_message


auth = Blueprint('auth', __name__)


@auth.route('/login')
@auth.route('/register')
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    return render_template('login.html', regform=regform, loginform=loginform)


@auth.route('/registration/process', methods=['POST'])
def registration_process():
    regform = RegistrationForm(request.form)
    if not regform.validate():
        error_message = f"""Incorrect credentials: \n""" + generate_error_message(regform.errors)
        flash(error_message)
        return redirect(url_for('auth.register'))

    username = regform.username.data
    # validate that there is no such user
    user = User.query.filter_by(username=username).first()
    if user is None:
        user = User(username=username, email=regform.email.data)
        user.set_password(regform.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash('Username already exists')
        return redirect(url_for('auth.register'))


@auth.route('/login/process', methods=['POST'])
def login_process():
    loginform = LoginForm(request.form)
    if not loginform.validate():
        flash(f"""Incorrect credentials: \n""" + generate_error_message(loginform.errors))
        return redirect(url_for('auth.register'))

    username = loginform.username.data
    # validate that there is such user
    user = User.query.filter_by(username=username)
    if user is None:
        flash(f"""The username does not exist: \n""" + generate_error_message(loginform.errors))
        return redirect(url_for('auth.register'))

    if user.verify_password(loginform.password.data):
        user.last_login = datetime.datetime.now()
        db.session.commit()
        login_user(user, remember=True)
        return redirect(url_for('index'))
    else:
        flash(f"""Incorrect password \n""" + generate_error_message(loginform.errors))
        return redirect(url_for('auth.register'))


@auth.route("/logout")
@login_required
def logout():
    return render_template('logout.html')


@auth.route('/logout/process', methods=['POST'])
def logout_process():
    if request.form['response'] == 'yes':
        logout_user()
        flash('Successfully logged out')
        return redirect(url_for('auth.register'))
    else:
        return redirect(url_for('index'))




