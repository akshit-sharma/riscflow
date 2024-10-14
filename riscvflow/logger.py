import logging

# Set up a logger for the library
logger = logging.getLogger(__name__)  # Use the module name as the logger name

# Set a default log level (this can be overridden by the user's application)
logger.setLevel(logging.INFO)

# Create a handler to output logs to the console (this can be customized by users)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create a formatter for log messages
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Add the formatter to the console handler
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

