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

filepath = 'templates/'

variable_name = 'x'
settings = {
    'figsize': (6, 6),
    'title': 'y=f(x)',
    'xlabel': f'Variable x',
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

    return lambda var: [elem if elem != variable else var for elem in s], variable


def plot_function(s: str, xmin: int or float, xmax: int or float, npoints=1000, settings=settings):
    assert npoints > 0
    assert xmin < xmax
    func_val = []
    func, var_name = implementable_function(s)
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
    plt.savefig(os.path.join(filepath, 'plt.eps'))
    plt.show()






