import logging

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Define the format used for log messages
formatter = logging.Formatter('%(levelname)s:%(name)s:%(message)s')

# Create a file handler to write logs to employee.log
file_handler = logging.FileHandler('employee.log')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)


class Employee:
    """A sample Employee class"""

    # Initialize an Employee with a first and last name
    def __init__(self, first, last):
        self.first = first
        self.last = last

        # Log information when a new Employee is created
        logger.info('Created Employee: {} - {}'.format(self.fullname, self.email))

    # Return the employee's email address
    @property
    def email(self):
        return '{}.{}@email.com'.format(self.first, self.last)

    # Return the employee's full name
    @property
    def fullname(self):
        return '{} {}'.format(self.first, self.last)


# Create three Employee objects
emp_1 = Employee('John', 'Smith')
emp_2 = Employee('Corey', 'Schafer')
emp_3 = Employee('Jane', 'Doe')
