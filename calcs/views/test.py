from decimal import Decimal
import math
import unittest
from unittest import TestCase

from parameters import *
from convert_to_rpn import rpn, preprocess
from implement_rpn import compute_rpn


class Test_convertion_to_rpn(TestCase):
    def test_spaces(self):
        self.assertListEqual(preprocess('2 +3'), ['2', f'+','3'])
        self.assertListEqual(preprocess('4 - 8'), ['4',f'_f{names.index("-")}','8'])
        self.assertListEqual(preprocess('5  *   3'), ['5', f'_f{names.index("*")}', '3'])
        self.assertListEqual(preprocess(' 6/4'), ['6',f'_f{names.index("/")}','4'])
        self.assertListEqual(preprocess('  2.3  ^  3   '), ['2.3', f'_f{names.index("^")}', '3'])

    def test_simple_algebra(self):
        self.assertListEqual(rpn('2+3'), [Decimal('2'), Decimal('3'), '+'])
        self.assertListEqual(rpn('4-8'), [Decimal('4'), Decimal('8'), '-'])
        self.assertListEqual(rpn('5*3'), [Decimal('5'), Decimal('3'), '*'])
        self.assertListEqual(rpn('6/4'), [Decimal('6'), Decimal('4'), '/'])
        self.assertListEqual(rpn('2^3'), [Decimal('2'), Decimal('3'), '^'])

    def test_precedence(self):
        self.assertListEqual(rpn('2+3*4'), [Decimal('2'), Decimal('3'), Decimal('4'), '*', '+'])
        self.assertListEqual(rpn('5*6+7'), [Decimal('5'), Decimal('6'), '*', Decimal('7'), '+'])

    def test_brackets(self):
        self.assertListEqual(rpn('(2+3)-5'),[Decimal('2'), Decimal('3'), '+', Decimal('5'), '-'])
        self.assertListEqual(rpn('4*(6-7)'), [Decimal('4'), Decimal('6'), Decimal('7'), '-', '*'])
        self.assertListEqual(rpn('(2.78+3)*(7-8)'), [Decimal('2.78'), Decimal('3'), '+',
                                                 Decimal('7'), Decimal('8'), '-',
                                                 '*'])

    def test_constants(self):
        self.assertListEqual(rpn('e'), [Decimal(math.e)])
        self.assertListEqual(rpn('e+pi'), [Decimal(math.e), Decimal(math.pi), '+'])
        self.assertListEqual(rpn('e*(3 + 7 - e)'), [Decimal(math.e), Decimal('3'),
                                                    Decimal('7'), Decimal(math.e),
                                                    '-', '+', '*'])

    def test_functions(self):
        self.assertListEqual(rpn('sin(3)'), [Decimal('3'), 'sin'])
        self.assertListEqual(rpn('arcsin(0.5)'), [Decimal('0.5'), 'arcsin'])
        self.assertListEqual(rpn('cos( 8 ) + tan(7)'), [Decimal('8'), 'cos', Decimal('7'), 'tan', '+'])
        self.assertListEqual(rpn('cos(arcsin(1/e))'), [Decimal('1'), Decimal(math.e),
                                                      '/', 'arcsin', 'cos'])

    def test_precedence(self):
        self.assertListEqual(rpn('3 * 4 +  6'), [Decimal('3'), Decimal('4'), '*', Decimal('6'), '+'])
        self.assertListEqual(rpn('1-2*5'), [Decimal('1'), Decimal('2'), Decimal('5'), '*', '-'])
        self.assertListEqual(rpn('1/2*4'), [Decimal('1'), Decimal('2'), '/', Decimal('4'), '*'])

    def test_unary_minus(self):
        self.assertListEqual(rpn('-6'), [Decimal('6'), '--'])
        self.assertListEqual(rpn('-4+3'), [Decimal('4'), '--', Decimal('3'), '+'])
        self.assertListEqual(rpn('2^-2'), [Decimal('2'), Decimal('2'), '--', '^'])
        self.assertListEqual(rpn('-5^2'), [Decimal('5'), Decimal('2'), '^', '--'])


class Test_computing_rpn(TestCase):
    def test_simple_algebra(self):
        self.assertEqual(compute_rpn([Decimal('2'), Decimal('3'), '+']), Decimal('5'))
        self.assertEqual(compute_rpn([Decimal('4'), Decimal('8'), '-']), Decimal('-4'))
        self.assertEqual(compute_rpn([Decimal('5'), Decimal('3'), '*']), Decimal('15'))
        self.assertEqual(compute_rpn([Decimal('6'), Decimal('4'), '/']), Decimal('1.5'))
        self.assertEqual(compute_rpn([Decimal('2'), Decimal('3'), '^']), Decimal('8'))

    def test_brackets(self):
        self.assertEqual(compute_rpn([Decimal('2'), Decimal('3'), '+', Decimal('5'), '-']), Decimal('0'))
        self.assertEqual(compute_rpn([Decimal('4'), Decimal('6'), Decimal('7'), '-', '*']), Decimal('-4'))
        self.assertEqual(compute_rpn([Decimal('2.78'), Decimal('3'), '+',
                                      Decimal('7'), Decimal('8'), '-', '*']), Decimal('-5.78'))

    def test_constants(self):
        self.assertEqual(compute_rpn([Decimal(math.e)]), Decimal(math.e))
        self.assertEqual(compute_rpn([Decimal(math.e), Decimal(math.pi), '+']), Decimal(math.e)+Decimal(math.pi))
        self.assertEqual(compute_rpn([Decimal(math.e), Decimal('3'), Decimal('7'), Decimal(math.e),
                                      '-', '+', '*']),
                         Decimal(math.e)*(Decimal('3') + Decimal('7')-Decimal(math.e)))

    def test_functions(self):
        self.assertEqual(compute_rpn([Decimal('3'), 'sin']), Decimal(math.sin(3)))
        self.assertEqual(compute_rpn([Decimal('0.5'), 'arcsin']), Decimal(math.asin(0.5)))
        self.assertEqual(compute_rpn([Decimal('8'), 'cos', Decimal('7'), 'tan', '+']),
                         Decimal(math.cos(8)+math.tan(7)))
        self.assertEqual(compute_rpn([Decimal('1'), Decimal(math.e), '/', 'arcsin', 'cos']),
                         Decimal(math.cos(math.asin(1/math.e))))

    def test_precedence(self):
        self.assertEqual(compute_rpn([Decimal('2'), Decimal('3'), Decimal('4'), '*', '+']), Decimal('14'))
        self.assertEqual(compute_rpn([Decimal('5'), Decimal('6'), '*', Decimal('7'), '+']), Decimal('37'))

    def test_unary_minus(self):
        self.assertEqual(compute_rpn([Decimal('6'), '--']), Decimal('-6'))
        self.assertEqual(compute_rpn([Decimal('4'), '--', Decimal('3'), '+']), Decimal('-1'))
        self.assertEqual(compute_rpn([Decimal('2'), Decimal('2'), '--', '^']), Decimal('0.25'))
        self.assertEqual(compute_rpn([Decimal('5'), Decimal('2'), '^', '--']), Decimal('-25'))


class TestGraphingCalc(TestCase):
    def test_implementable_function(self):
        pass


if __name__ == '__main__':
    unittest.main()
