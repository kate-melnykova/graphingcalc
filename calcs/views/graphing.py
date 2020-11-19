# ./calc/views/graphing
"""
graphing calculator
"""
from typing import List
from decimal import Decimal
import math
import os

import numpy as np
import matplotlib.pyplot as plt

from views.parameters import *
from views.exceptions import *
from views.convert_to_rpn import rpn
from views.implement_rpn import compute_rpn
from views.graphing_setting import SettingAxes, SettingLine

filepath = '/media/'

variable_name = 'x'


def implementable_function(s: str):
    s = rpn(s, function=True)
    if 'x' in s:
        variable = 'x'
        if 't' in s:
            raise TooManyVarError
    elif 't' in s:
        variable = 't'
    else:
        raise UnknownVarNameError
    print(f'Variable is {variable}')

    def func(var):
        plug_var = [elem if elem != variable else var for elem in s]
        print(plug_var)
        return compute_rpn(plug_var)

    return func


def plot_function(raw_data={}):
    # fig = plt.figure()
    # create initial plot figure
    figsize_x = raw_data.get('figsize_x', 6)
    figsize_y = raw_data.get('figsize_y', 6)
    figsize = (6, 6)
    try:
        figsize_x = float(figsize_x)
    except (ValueError, OverflowError):
        pass
    else:
        figsize[0] = figsize_x

    try:
        figsize_y = float(figsize_y)
    except (TypeError, ValueError, OverflowError):
        pass
    else:
        figsize[1] = figsize_y

    fig, ax = plt.subplots(figsize=figsize)
    SettingAxes(fig, ax, raw_data)
    SettingLine.plot(fig, ax, raw_data)
    #plt.plot(xvals, func_val, color=params['linecolor'])

    plt.savefig(os.getcwd() + filepath + 'plot.png')
    # plt.show()







