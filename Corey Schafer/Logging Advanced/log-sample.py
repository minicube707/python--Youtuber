import logging
import employee

# Create a logger for this module
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Define the format for log messages
formatter = logging.Formatter('%(asctime)s:%(name)s:%(message)s')

# Create a file handler that only logs ERROR messages
file_handler = logging.FileHandler('sample.log')
file_handler.setLevel(logging.ERROR)
file_handler.setFormatter(formatter)

# Create a stream handler for displaying log messages in the console
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

# Add both handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)


def add(x, y):
    """Add Function"""
    # Return the sum of two numbers
    return x + y


def subtract(x, y):
    """Subtract Function"""
    # Return the difference between two numbers
    return x - y


def multiply(x, y):
    """Multiply Function"""
    # Return the product of two numbers
    return x * y


def divide(x, y):
    """Divide Function"""
    try:
        # Try to divide the first number by the second number
        result = x / y
    except ZeroDivisionError:
        # Log the exception if the second number is zero
        logger.exception('Tried to divide by zero')
    else:
        # Return the result if no exception occurred
        return result


# Define the two numbers used for the calculations
num_1 = 10
num_2 = 0

# Perform the addition and log the result
add_result = add(num_1, num_2)
logger.debug('Add: {} + {} = {}'.format(num_1, num_2, add_result))

# Perform the subtraction and log the result
sub_result = subtract(num_1, num_2)
logger.debug('Sub: {} - {} = {}'.format(num_1, num_2, sub_result))

# Perform the multiplication and log the result
mul_result = multiply(num_1, num_2)
logger.debug('Mul: {} * {} = {}'.format(num_1, num_2, mul_result))

# Perform the division and log the result
div_result = divide(num_1, num_2)
logger.debug('Div: {} / {} = {}'.format(num_1, num_2, div_result))