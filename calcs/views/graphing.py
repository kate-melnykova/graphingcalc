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

filepath = '/media/'

variable_name = 'x'
settings = {
    'figsize': (6, 6),
    'title': 'y=f(x)',
    'xlabel': f'Variable x',
    'ylabel': None,
    'label': None
}


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


def plot_function(s: str, xmin: str, xmax: str, npoints=1000, params={}):
    xmin = float(xmin)
    xmax = float(xmax)
    assert npoints > 0
    assert xmin < xmax
    func_val = []
    s = rpn(s, function=True)
    func = lambda var: compute_rpn([elem if elem != 'x' else Decimal(var) for elem in s])
    stepsize = (xmax - xmin) / npoints
    xvals = []
    for i in range(npoints):
        val = xmin + stepsize*i
        xvals.append(val)
        func_val.append(func(val))

    plt.figure(figsize=settings['figsize'])
    plt.plot(xvals, func_val)
    plt.title(settings['title'])
    plt.xlabel(settings['xlabel'])
    plt.savefig(os.getcwd() + filepath + 'plt2.png')
    # plt.show()






