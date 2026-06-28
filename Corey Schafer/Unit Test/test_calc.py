import unittest
import calc

# Documentation for the unittest.TestCase class:
# https://docs.python.org/3/library/unittest.html#unittest.TestCase.debug


# Test cases for the calculator functions
class TestCalc(unittest.TestCase):

    # Test the addition function
    def test_add(self):
        self.assertEqual(calc.add(10, 5), 15)
        self.assertEqual(calc.add(-1, 1), 0)
        self.assertEqual(calc.add(-1, -1), -2)

    # Test the subtraction function
    def test_subtract(self):
        self.assertEqual(calc.subtract(10, 5), 5)
        self.assertEqual(calc.subtract(-1, 1), -2)
        self.assertEqual(calc.subtract(-1, -1), 0)

    # Test the multiplication function
    def test_multiply(self):
        self.assertEqual(calc.multiply(10, 5), 50)
        self.assertEqual(calc.multiply(-1, 1), -1)
        self.assertEqual(calc.multiply(-1, -1), 1)

    # Test the division function
    def test_divide(self):
        self.assertEqual(calc.divide(10, 5), 2)
        self.assertEqual(calc.divide(-1, 1), -1)
        self.assertEqual(calc.divide(-1, -1), 1)
        self.assertEqual(calc.divide(5, 2), 2.5)

        # Check that division by zero raises a ValueError
        self.assertRaises(ValueError, calc.divide, 10, 0)

        # Alternative syntax for checking exceptions
        with self.assertRaises(ValueError):
            calc.divide(10, 0)


if __name__ == "__main__":
    unittest.main()

# Run the tests from the command line:
# python3 -m unittest test_calc.py