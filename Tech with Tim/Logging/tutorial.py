import logging

# Configure the root logger.
# This configuration writes INFO-level messages and above to log.log.
logging.basicConfig(
    level=logging.INFO,
    filename="log.log",
    filemode="w",
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Create a logger specific to this module.
logger = logging.getLogger(__name__)


# Log messages with different severity levels.
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")


# Store a value and include it in the log message.
x = 2
logger.info("The value of x is %s", x)


# Handle a division by zero error.
try:
    result = 1 / 0
except ZeroDivisionError:
    # Log the complete exception traceback.
    logger.exception("An error occurred while dividing by zero")


# Create a separate custom logger.
custom_logger = logging.getLogger(__name__)
custom_logger.setLevel(logging.INFO)

# Create a file handler for the custom logger.
file_handler = logging.FileHandler("test.log")

# Define the format for the custom logger.
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

# Apply the formatter to the file handler.
file_handler.setFormatter(formatter)

# Add the handler to the custom logger.
custom_logger.addHandler(file_handler)

# Test the custom logger.
custom_logger.info("Testing the custom logger")