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
from wtforms import StringField, DecimalField, BooleanField, FloatField, IntegerField
from wtforms import PasswordField, SubmitField, SelectField
from wtforms import validators
from wtforms.widgets.html5 import RangeInput, NumberInput

# from views.auth import User
from model import db, User
# from redispy import get_connection


class ComputeForm(FlaskForm):
    expression = StringField('Enter the formula',
                             validators=[validators.Length(min=1, max=100)],
                             render_kw={'style': 'width:80%;'})
    submit = SubmitField()


class GraphingForm(FlaskForm):
    """
    expression1 = StringField('f(x)=',
                             validators=[validators.Length(min=1, max=100)],
                             render_kw={'style': 'width:80%;'})
    xmin1 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax1 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label1 = StringField('Label')
    include_in_legend1 = BooleanField('Include in legend', default=True)
    linecolor1 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ], default=['b'])
    linewidth1 = FloatField('Line width',
                           default=2.0,
                           validators=[validators.NumberRange(min=0.0,
                                                              message='Line width must be positive')])
    markersize1 = FloatField('MarkerSize', default=2.0)
    scatterplot1 = BooleanField('Scatterplot?')
    n_points1 = IntegerField('Number of points', default=1000)

    linestyle1 = SelectField('Line style', default='-', choices=[
        ('-', 'Solid'),
        ('--', 'Dashed'),
        ('-.', 'Dashed-dot'),
        ('.', 'Dotted')
    ])
    noise1 = IntegerField('Noise level in %',
                          default=0,
                          widget=RangeInput(step=5),
                          render_kw={'style': 'width:40%; display:inline-block'})

    expression2 = StringField('f(x)=',
                              validators=[validators.Length(min=1, max=100)],
                              render_kw={'style': 'width:80%;'})
    xmin2 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax2 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label2 = StringField('Label')
    include_in_legend2 = BooleanField('Include in legend', default=True)
    linecolor2 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ], default='r')
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
    scatterplot2 = BooleanField('Scatterplot?')
    markersize2 = FloatField('MarkerSize', default=2.0)
    n_points2 = IntegerField('Number of points', default=1000)
    noise2 = IntegerField('Noise level in %',
                          default=0,
                          widget=RangeInput(step=5))

    expression3 = StringField('f(x)=',
                              validators=[validators.Length(min=1, max=100)],
                              render_kw={'style': 'width:80%;'})
    xmin3 = FloatField('From x=', [validators.Length(min=6, max=35)])
    xmax3 = FloatField('To x=', [validators.Length(min=6, max=35)])
    label3 = StringField('Label')
    include_in_legend3 = BooleanField('Include in legend', default=True)
    linecolor3 = SelectField('Line color', choices=[
        ('b', 'Blue'),
        ('g', 'Green'),
        ('r', 'Red'),
        ('c', 'Cyan'),
        ('m', 'Magenta'),
        ('y', 'Yellow'),
        ('k', 'Black'),
        ('w', 'White')
    ], default='c')
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
    scatterplot3 = BooleanField('Scatterplot?')
    n_points3 = IntegerField('Number of points', default=1000)
    markersize3 = FloatField('MarkerSize', default=2.0)
    noise3 = IntegerField('Noise level in %',
                          default=0,
                          widget=RangeInput(step=5))
    """
    title = StringField('Title', render_kw={'style': 'width:90%;'})
    xlabel = StringField('x label', render_kw={'style': 'width:90%;'})
    ylabel = StringField('y label', render_kw={'style': 'width:90%;'})
    isgrid = BooleanField('Grid?', false_values=False)
    legend = BooleanField('Legend?')
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
