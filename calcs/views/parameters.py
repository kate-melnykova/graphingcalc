import math
from typing import List
from decimal import Decimal
from operator import add, sub, mul, truediv, pow

precedence = {
    '+': 0,
    '-': 0,
    '*': 1,
    '/': 2,
    '--': 3,
    '^': 4
}

constants = {
    'pi': math.pi,
    'e': math.e
}

functions = {
    'sin': (math.sin, 1),
    'cos': (math.cos, 1),
    'tan': (math.tan, 1),
    'tg': (math.tan, 1),
    'cot': (lambda x: 1/math.tan(x), 1),

    'arcsin': (math.asin, 1),
    'arccos': (math.acos, 1),
    'arctan': (math.atan, 1),

    'exp': (math.exp, 1),
    'ln': (math.log, 1),
    'log': (math.log, 2),

    '!': (math.factorial, 1),

    'gcd': (math.gcd, 2),
    'mod': (math.remainder, 2)
}

convert_alg_to_func = {
    '+': add,
    '-': sub,
    '*': mul,
    '/': truediv,
    '^': pow,
    '--': lambda x: -x
}


names = list(functions.keys()) + list(constants.keys()) \
            + list(precedence.keys()) + [',', '(', ')']
names = sorted(names, key=lambda x: len(x), reverse=True)