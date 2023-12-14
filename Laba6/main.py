import unittest
from calculator import Calculator  

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator('en_US')  

    def test_addition(self):
        result = self.calc.OPERATORS['+'](10, 5)
        self.assertEqual(result, 15)

    def test_subtraction(self):
        result = self.calc.OPERATORS['-'](10, 5)
        self.assertEqual(result, 5)

    def test_multiplication(self):
        result = self.calc.OPERATORS['*'](10, 5)
        self.assertEqual(result, 50)

    def test_division(self):
        result = self.calc.OPERATORS['/'](10, 5)
        self.assertEqual(result, 2)
        
        result = self.calc.OPERATORS['/'](10, 0)
        self.assertEqual(result, "Error: division on zero")

    def test_sqrt(self):
        result = self.calc.OPERATORS['√'](9, 0)
        self.assertEqual(result, 3)

    def test_power(self):
        result = self.calc.OPERATORS['^'](2, 3)
        self.assertEqual(result, 8)

    def test_modulo(self):
        result = self.calc.OPERATORS['%'](10, 3)
        self.assertEqual(result, 1)
        result = self.calc.OPERATORS['%'](10, 0)
        self.assertEqual(result, "Error: division on zero")

if __name__ == '__main__':
    unittest.main()
