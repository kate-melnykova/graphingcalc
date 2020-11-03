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
from wtforms import StringField, DecimalField, BooleanField, FloatField
from wtforms import PasswordField, SubmitField, SelectField
from wtforms import validators

# from views.auth import User
from model import db, User
# from redispy import get_connection


class ComputeForm(FlaskForm):
    expression = StringField('Enter the formula',
                             validators=[validators.Length(min=1, max=100)],
                             render_kw={'style': 'width:80%;'})
    submit = SubmitField()


class GraphingForm(FlaskForm):
    expression = StringField('f(x)=',
                             validators=[validators.Length(min=1, max=100)],
                             render_kw={'style': 'width:80%;'})
    xmin = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax = FloatField('To x=', [validators.Length(min=6, max=35)])
    title = StringField('Title')
    xlabel = StringField('x label')
    ylabel = StringField('y label')
    isgrid = BooleanField(false_values=False)
    linecolor = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ])
    linewidth = FloatField('Line width',
                           default=2.0,
                           validators=[validators.NumberRange(min=0.0,
                                                              message='Line width must be positive')])

    linestyle = SelectField('Line style', default='-', choices=[
        ('-', 'Solid'),
        ('--', 'Dashed'),
        ('-.', 'Dashed-dot'),
        ('.', 'Dotted')
    ])
    submit = SubmitField()