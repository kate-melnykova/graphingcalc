from views.parameters import *


def compute_rpn(s: List[Decimal or str]) -> Decimal:
    temp_stack = []
    while s:
        elem = s.pop(0)
        if isinstance(elem, Decimal):
            temp_stack.append(elem)
        else:
            if elem in ['+', '-', '*', '/', '^']:
                operator = convert_alg_to_func[elem]
                # implement action on last two elements of temp_stack
                if len(temp_stack) < 2:
                    raise NotEnoughArgsError(elem)
                term2 = temp_stack.pop()
                term1 = temp_stack.pop()
                temp_stack.append(Decimal(operator(term1, term2)))
            elif elem == '--':
                term = temp_stack.pop()
                temp_stack.append(-term)
            elif elem in functions:
                [operator, nargs] = functions[elem]
                try:
                    terms = temp_stack[-nargs:]
                except:
                    raise NotEnoughArgsError(operator.__name__)
                terms = [term for term in terms]
                temp_stack = temp_stack[:-nargs]
                temp_stack.append(Decimal(operator(*terms)))
            else:
                raise ImplementRPNError

    if len(temp_stack) != 1:
        raise TooManyArgsError
    return temp_stack[0]
