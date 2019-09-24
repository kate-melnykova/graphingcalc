class BaseApp(Exception):
    pass


class ParenthesisMismatch(BaseApp):
    """
    If the input has imbalanced parentheses
    """
    message = 'Imbalanced parentheses'


class UnknownFunction(BaseApp):
    """
    If the function entered is not known to the system
    """
    def __init__(self, func_name):
        self.message = f'Unknown function: {func_name}'


class ImplementRPNError(BaseApp):
    """
    During implementing RPN, we met unknown symbol
    """
    message = 'Unknown error while implementing the RPN'


class NotEnoughArgsError(BaseApp):
    """
    If there are not enough arguments for the function
    """
    def __init__(self, func_name):
        self.message = f'Insufficient amount of arguments, supposedly for {func_name}'


class TooManyArgsError(BaseApp):
    """
    If the stack has some leftover elements after implementation
    """
    message = 'Too many arguments in the expression'
    

class UnknownVarNameError(BaseApp):
    """
    Unknown variable name
    """
    message = 'Unknown variable name'
    
    
class TooManyVarError(BaseApp):
    """
    Both variables x and t are present in formulas
    """
    message = 'Both variables x and t are found in formula'