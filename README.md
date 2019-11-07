# Graphic calculator

Evaluates a formula with an arbitrary number of operations and plots the graph of a function.

## Installation
To install this app, you need to have `docker` to be installed. Then, open the terminal and run
`$ docker-compose up -d --build`
and
`$ docker-compose up`
The web interface is accessible at http://0.0.0.0:5000/

## Getting started
This app implements the reverse polish notation (RPN) to provide a computationally tractable way to evaluate the expression.
The **calculator** does:
* allows any amount of spaces
* checks if there are errors in the formula
* accepts functions:
 -- Parenthesis
 -- Exponents and logarithms: exp, ln, and log
 -- Trigonometric functions: sin, cos, tan & tg, cot, arcsin, arccos, arctan
 -- Other: factorial, greatest common divisor (gcd), modulo (mod)
* does not accept parameters
The implementation of the functions takes precedence.

To compute the value, enter the expression of the interest, and click submit. That's it!

The **graphing calculator** accepts the same functions as the calculator and also the variable x. The figure is plotted over provided range of x-values: the function is being evaluated over 1000 points in the interval. In addition, user may or may not specify the following parameters:
-- Grid on or off
-- Color of the line
-- Size of the line

## Technical information
The image is returned via the GET request, so it may be incorporated in your website.

