from unittest import TestCase
from math_operators import add, subtract, multiply, division


class MathOperatorsTest(TestCase):
    def test_add(self):
        self.assertEquals(add(4, 5), 9)
        self.assertNotEquals(add(-1, 4), 2)

    def test_subtract(self):
        self.assertEquals(subtract(5, 0), 5)

    def test_multiply(self):
        self.assertEquals(multiply(4, 5), 20)
        self.assertEquals(multiply(7, 0), 0)

    def test_division(self):
        self.assertEquals(division(30, 5), 6)
        self.assertRaises(ZeroDivisionError, division, 4, 0)


