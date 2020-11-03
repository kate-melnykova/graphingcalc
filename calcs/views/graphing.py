# ./calc/views/graphing
"""
graphing calculator
"""
from typing import List
from decimal import Decimal
import math
import os

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


def plot_function(s: str, xmin: str, xmax: str, npoints=1000, raw_data={}):
    xmin = float(xmin)
    xmax = float(xmax)
    assert npoints > 0
    assert xmin < xmax # TODO: add to validators
    func_val = []
    s = rpn(s, function=True)
    func = lambda var: compute_rpn([elem if elem != 'x' else Decimal(var) for elem in s])
    stepsize = (xmax - xmin) / npoints
    xvals = []
    for i in range(npoints):
        val = xmin + stepsize*i
        xvals.append(val)
        func_val.append(func(val))

    # fig = plt.figure()
    fig = SettingAxes.make_plot(raw_data)
    SettingLine.plot(fig, func_val, xmin, xmax, raw_data)
    #plt.plot(xvals, func_val, color=params['linecolor'])

    plt.savefig(os.getcwd() + filepath + 'plot.png')
    # plt.show()







