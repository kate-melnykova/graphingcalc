"""
convert infix notation to rpn
"""
from typing import List
from decimal import Decimal
import math

from views.parameters import *
from views.exceptions import *


def preprocess(s: str) -> List[str]:
    s.replace(',', ' ')
    for idx, name in enumerate(names):
        s = s.replace(name, f' _f{idx} ')
    return s.split()


def rpn(string: str or List[str], function=False):
    if isinstance(string, str):
        string = preprocess(string)
    output = []
    op_queue = []
    token = None
    
    print(string)
    variable = 'x'
    if function:
        if 't' in string:
            variable = 't'
    
    while string:
        prev_token = token
        token = string.pop(0) # read token
        # if the token is a number, then:
        #    push it to the output queue.
        if not token.startswith('_f'):
            if function and token == variable:
                output.append(variable)
            else:
                try:
                    output.append(Decimal(token))
                except:
                    raise UnknownFunction(token)

        else:
            token = names[int(token[2:])]
            if token in constants.keys():
                output.append(Decimal(constants[token]))

            # if the token is a function then:
            #    push it onto the operator stack
            elif token in functions.keys():
                op_queue = [token] + op_queue
            elif token in ['+', '-', '*', '/', '^']:
                # check if it is unary minus or plus
                if token in ['+', '-'] and (prev_token is None
                                            or prev_token in functions
                                            or prev_token in ['+', '-', '*', '/', '^']
                                            or prev_token == '('):
                    if token == '-':
                        op_queue = ['--'] + op_queue
                else:
                    # consider precedence
                    token_prec = precedence[token]
                    while op_queue:
                        if op_queue[0] in ['+', '-', '*', '/', '^', '--']:
                            if precedence[op_queue[0]] > token_prec:
                                token_temp = op_queue.pop(0)
                                output.append(token_temp)
                            else:
                                break
                        else:
                            break
                    op_queue = [token] + op_queue

            # if the token is a left paren (i.e."("), then:
            #    push it onto the operator stack.
            elif token == '(':
                op_queue = [token] + op_queue
            # if the token is a right paren (i.e.")"), then:
            #    while the operator at the top of the operator stack is not a left paren:
            #        pop the operator from the operator stack onto the output queue.
            elif token == ')':
                token = op_queue.pop(0)
                while token != '(':
                    output.append(token)
                    if op_queue:
                        token = op_queue.pop(0)
                    else:
                        raise ParenthesisMismatch

                    #  / * if the stack runs out without
                    # finding a left paren, then there are mismatched parentheses. * /

                # if there is a left paren at the top of the operator stack, then:
                # pop the operator from the operator stack and discard it
                if op_queue:
                    if op_queue[0] in functions:
                        token = op_queue.pop(0)
                        output.append(token)
                token = ')'

    # after while loop, if operator stack not null, pop everything to output queue
    if op_queue:
        if op_queue == '(':
            raise ParenthesisMismatch

    output += op_queue
    op_queue = []
    return output


