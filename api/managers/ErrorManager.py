import logging, os
from logging.handlers import RotatingFileHandler
DIRNAME = os.path.dirname(__file__)
LOG_FILENAME = os.path.join(DIRNAME, "../log/api_error.log")

class ErrorManager():
    def log_error(message):
        logger = get_logger()
        logger.critical(message)
        
def get_logger():
    """ Initializes the logger for the entire program """
    # Set up a specific logger with our desired output level
    logger = logging.getLogger("kiosk_error_log")
    logger.setLevel(logging.DEBUG)
    handler = RotatingFileHandler(LOG_FILENAME, maxBytes=100000, backupCount=10)
    logger.addHandler(handler)
    log_formatter = logging.Formatter('{asctime}: {levelname:8s} - {message}', style='{')
    handler.setFormatter(log_formatter)

    return logger