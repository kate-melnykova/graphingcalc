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
from views.graphing_setting import create_plot

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
    return create_plot(raw_data, filepath)







