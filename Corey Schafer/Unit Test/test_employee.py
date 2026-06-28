import unittest
from unittest.mock import patch
from employee import Employee


# Test cases for the Employee class
class TestEmployee(unittest.TestCase):

    # Run once before all test methods
    @classmethod
    def setUpClass(cls):
        print("SetUpClass")

    # Run once after all test methods
    @classmethod
    def tearDownClass(cls):
        print("tearDownClass")

    # Run before each test method
    def setUp(self):
        print("SetUp")
        self.emp_1 = Employee("Corey", "Schafer", 50000)
        self.emp_2 = Employee("Sue", "Smith", 60000)

    # Run after each test method
    def tearDown(self):
        print("TearDown\n")

    # Test the email property
    def test_email(self):

        print("test_email")
        self.assertEqual(self.emp_1.email, "Corey.Schafer@email.com")
        self.assertEqual(self.emp_2.email, "Sue.Smith@email.com")

        # Update first names and verify that the email property changes
        self.emp_1.first = "John"
        self.emp_2.first = "Jane"

        self.assertEqual(self.emp_1.email, "John.Schafer@email.com")
        self.assertEqual(self.emp_2.email, "Jane.Smith@email.com")

    # Test the fullname property
    def test_fullname(self):

        print("test_fullname")
        self.assertEqual(self.emp_1.fullname, "Corey Schafer")
        self.assertEqual(self.emp_2.fullname, "Sue Smith")

        # Update first names and verify that the fullname property changes
        self.emp_1.first = "John"
        self.emp_2.first = "Jane"

        self.assertEqual(self.emp_1.fullname, "John Schafer")
        self.assertEqual(self.emp_2.fullname, "Jane Smith")

    # Test the salary raise method
    def test_apply_raise(self):

        print("test_apply_raise")
        self.emp_1.apply_raise()
        self.emp_2.apply_raise()

        self.assertEqual(self.emp_1.pay, 52500)
        self.assertEqual(self.emp_2.pay, 63000)

    # Test the monthly_schedule method using a mocked HTTP request
    def test_monthly_schedule(self):
        with patch('employee.requests.get') as mocked_get:

            # Simulate a successful HTTP response
            mocked_get.return_value.ok = True
            mocked_get.return_value.text = "Success"

            schedule = self.emp_1.monthly_schedule("May")
            mocked_get.assert_called_with("http://company.com/Schafer/May")
            self.assertEqual(schedule, "Success")

            # Simulate a failed HTTP response
            mocked_get.return_value.ok = False

            schedule = self.emp_2.monthly_schedule("June")
            mocked_get.assert_called_with("http://company.com/Smith/June")
            self.assertEqual(schedule, "Bad Response!")


if __name__ == "__main__":
    unittest.main()