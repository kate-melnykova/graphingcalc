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
    expression1 = StringField('f(x)=',
                             validators=[validators.Length(min=1, max=100)],
                             render_kw={'style': 'width:80%;'})
    xmin1 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax1 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label1 = StringField('Label')
    linecolor1 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ])
    linewidth1 = FloatField('Line width',
                           default=2.0,
                           validators=[validators.NumberRange(min=0.0,
                                                              message='Line width must be positive')])

    linestyle1 = SelectField('Line style', default='-', choices=[
        ('-', 'Solid'),
        ('--', 'Dashed'),
        ('-.', 'Dashed-dot'),
        ('.', 'Dotted')
    ])

    expression2 = StringField('f(x)=',
                              validators=[validators.Length(min=1, max=100)],
                              render_kw={'style': 'width:80%;'})
    xmin2 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax2 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label2 = StringField('Label')
    linecolor2 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ])
    linewidth2 = FloatField('Line width',
                           default=2.0,
                           validators=[validators.NumberRange(min=0.0,
                                                              message='Line width must be positive')])

    linestyle2 = SelectField('Line style', default='-', choices=[
        ('-', 'Solid'),
        ('--', 'Dashed'),
        ('-.', 'Dashed-dot'),
        ('.', 'Dotted')
    ])

    expression3 = StringField('f(x)=',
                              validators=[validators.Length(min=1, max=100)],
                              render_kw={'style': 'width:80%;'})
    xmin3 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax3 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label3 = StringField('Label')
    linecolor3 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ])
    linewidth3 = FloatField('Line width',
                           default=2.0,
                           validators=[validators.NumberRange(min=0.0,
                                                              message='Line width must be positive')])

    linestyle3 = SelectField('Line style', default='-', choices=[
        ('-', 'Solid'),
        ('--', 'Dashed'),
        ('-.', 'Dashed-dot'),
        ('.', 'Dotted')
    ])

    title = StringField('Title')
    xlabel = StringField('x label')
    ylabel = StringField('y label')
    isgrid = BooleanField(false_values=False)
    submit = SubmitField()

    def validate(self):
        if not FlaskForm.validate(self):
            return False

        # check that xmin < xmax
        def get_attr(name):
            attr = getattr(self, name)
            return attr.data

        for i in range(1, 4):
            if get_attr(f'xmin{i}') is None and get_attr(f'xmax{i}') is None:
                continue
            elif get_attr(f'xmin{i}') is None or get_attr(f'xmax{i}') is None:
                return False
            elif get_attr(f'xmin{i}') > get_attr(f'xmax{i}'):
                return False

        return True