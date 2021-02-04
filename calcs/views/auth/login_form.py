import datetime

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask_login import login_user, login_required,\
    logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField, SubmitField
from wtforms import validators, ValidationError

from model import db, User

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


class Edit_profile(FlaskForm):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    prev_password = PasswordField('Old Password', [
        validators.InputRequired(),
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('New Password')
    confirm = PasswordField('Repeat Password',
                            [validators.EqualTo('password', message='Passwords must match')])
    # accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
    submit = SubmitField()

    def validate_password(_, field):
        if field.data and (len(field.data) < 6 or len(field.data) > 35):
            raise ValidationError('The password length must be between 6 and 35 digits')


def generate_error_message(form_errors):
    error_message = f''
    for k, v in form_errors.items():
        error_message += f""" -- {k}: {v[0]} \n"""
    return error_message


auth = Blueprint('auth', __name__)

"""
@auth.route('/login')
@auth.route('/register')
def register():
    regform = RegistrationForm(request.form)
    loginform = LoginForm(request.form)
    return render_template('login.html',
                           regform=regform,
                           loginform=loginform)
"""


@auth.route('/login')
def login():
    loginform = LoginForm(request.form)
    return render_template('login2.html',
                           loginform=loginform)


@auth.route('/register')
def register():
    regform = RegistrationForm(request.form)
    return render_template('register2.html',
                           regform=regform)



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
    users = User.query.filter_by(username=username).limit(1).all()
    if not users:
        flash(f"""The username does not exist: \n""" + generate_error_message(loginform.errors))
        return redirect(url_for('auth.register'))

    for user in users:
        if user.verify_password(loginform.password.data):
            user.last_login = datetime.datetime.now()
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            return redirect(url_for('index'))

    flash(f"""Incorrect password \n""" + generate_error_message(loginform.errors))
    return redirect(url_for('auth.register'))


@auth.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if request.method == 'GET':
        form = Edit_profile(obj=current_user)
        form.password.data = ''
        form.confirm.data = ''
        return render_template('edit_profile.html',
                               form=form)

    elif Edit_profile(request.form).validate():
        user = User.query.filter_by(username=current_user.username).first()
        form = Edit_profile(request.form)
        # verify the original password
        prev_password = form.prev_password.data
        if not user.verify_password(prev_password):
            flash('Password is incorrect. Please try again')
            return render_template('edit_profile.html',
                               form=form)
        # check if username is available
        user_username = User.query.filter_by(username=user.username).first()
        user_email = User.query.filter_by(email=user.email).first()
        is_username_taken = user_username and user_username.id != user.id
        is_email_taken = user_email and user_email.id != user.id
        if is_username_taken and is_email_taken:
            flash('Given username and email are both taken. Please try again')
            form.username.data = user.username
            form.email.data = user.email
            return render_template('edit_profile.html',
                                   form=form)
        elif is_username_taken:
            flash('Given username is taken. Please try again')
            form.username.data = user.username
            return render_template('edit_profile.html',
                                   form=form)
        elif is_email_taken:
            flash('Given email is taken. Please try again')
            form.email.data = user.email
            return render_template('edit_profile.html',
                                   form=form)

        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        print(f'Type user is {type(user)}, user.username is {user.username}')
        login_user(user, remember=True)
        db.session.add(user)
        db.session.commit()
        flash('The profile change was successtul!')
        return redirect(url_for('index'))
    else:
        flash('Validation error')
        return render_template('edit_profile.html',
                               form=request.form)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    flash('Successfully logged out')
    return redirect(url_for('auth.login'))







