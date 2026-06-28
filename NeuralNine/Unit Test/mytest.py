import myfunction
import unittest

# Test cases for the imperfect multiplication function
class TestMultiplyImperfect(unittest.TestCase):
    
    # Test multiplication with two positive integers
    def test_with_two_positives(self):
        self.assertEqual(myfunction.multiply_with_loop_imperfect(17, 19), 17 * 19)
        self.assertEqual(myfunction.multiply_with_loop_imperfect(1787912, 1231241), 1787912 * 1231241)
        self.assertEqual(myfunction.multiply_with_loop_imperfect(1, 2), 1 * 2)
    
    # Test multiplication when one operand is zero
    def test_with_one_zero(self):
        self.assertEqual(myfunction.multiply_with_loop_imperfect(17, 0), 0)
        self.assertEqual(myfunction.multiply_with_loop_imperfect(0, 17), 0)
    
    # Test multiplication when both operands are zero
    def test_with_two_zero(self):
        self.assertEqual(myfunction.multiply_with_loop_imperfect(0, 0), 0)
    
    # Test multiplication with one negative operand
    def test_with_one_negative(self):
        self.assertEqual(myfunction.multiply_with_loop_imperfect(17, -19), 17 * (-19))
        self.assertEqual(myfunction.multiply_with_loop_imperfect(-19, 17), (-19) * 17)
    
    # Test multiplication with two negative operands
    def test_with_two_negatives(self):
        self.assertEqual(myfunction.multiply_with_loop_imperfect(-17, -19), 17 * 19)

# Test cases for the improved multiplication function     
class TestMultiplyBetter(unittest.TestCase):
    
    # Test multiplication with two positive integers
    def test_with_two_positives(self):
        self.assertEqual(myfunction.multiply_with_loop_better(17, 19), 17 * 19)
        self.assertEqual(myfunction.multiply_with_loop_better(1787912, 1231241), 1787912 * 1231241)
        self.assertEqual(myfunction.multiply_with_loop_better(1, 2), 1 * 2)
    
    # Test multiplication when one operand is zero
    def test_with_one_zero(self):
        self.assertEqual(myfunction.multiply_with_loop_better(17, 0), 0)
        self.assertEqual(myfunction.multiply_with_loop_better(0, 17), 0)
    
    # Test multiplication when both operands are zero
    def test_with_two_zero(self):
        self.assertEqual(myfunction.multiply_with_loop_better(0, 0), 0)
    
    # Test multiplication with one negative operand
    def test_with_one_negative(self):
        self.assertEqual(myfunction.multiply_with_loop_better(17, -19), 17 * (-19))
        self.assertEqual(myfunction.multiply_with_loop_better(-19, 17), (-19) * 17)
    
    # Test multiplication with two negative operands
    def test_with_two_negatives(self):
        self.assertEqual(myfunction.multiply_with_loop_better(-17, -19), 17 * 19)
        
# Test cases for the integer length function
class TestIntegerLength(unittest.TestCase):
    
    # Test the length of positive integers
    def test_with_positive_integer(self):
        self.assertEqual(myfunction.length_of_integer(123456), 6)
        self.assertEqual(myfunction.length_of_integer(1), 1)
        self.assertEqual(myfunction.length_of_integer(10), 2)
    
    # Test the length of negative integers (including the minus sign)
    def test_with_negative_integer(self):
        self.assertEqual(myfunction.length_of_integer(-123), 4)
        self.assertEqual(myfunction.length_of_integer(-1), 2)
        self.assertEqual(myfunction.length_of_integer(-123456), 7)
    
    # Test the length of zero
    def test_with_zeros(self):
        self.assertEqual(myfunction.length_of_integer(0), 1)
       
    # Test invalid input types 
    def test_with_invalid_type(self):
        self.assertRaises(TypeError, myfunction.length_of_integer, "12315")
        self.assertRaises(TypeError, myfunction.length_of_integer, "Hello")
        self.assertRaises(TypeError, myfunction.length_of_integer, True)
        self.assertRaises(TypeError, myfunction.length_of_integer, 123.3124)
        self.assertRaises(TypeError, myfunction.length_of_integer, [1, 2, 3, 4])
        
if __name__ == '__main__':
    unittest.main()

# Run the tests from the command line:
# python3 -m unittest mytest.py