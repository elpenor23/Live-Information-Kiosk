#!/usr/bin/python3
""" base application start """
import sys, os
import logging
import logging.handlers
from PyQt5.QtWidgets import QApplication
from ui_setup import AppUI
DIRNAME = os.path.dirname(__file__)
LOG_FILENAME = os.path.join(DIRNAME, "log/kiosk_log.log")

def get_logger():
    """ Initializes the logger for the entire program """
    # Set up a specific logger with our desired output level
    kiosk_logger = logging.getLogger('kiosk_log')
    kiosk_logger.setLevel(logging.INFO)

    # Add the log message handler to the logger
    handler = logging.handlers.RotatingFileHandler(
                LOG_FILENAME, maxBytes=2000000, backupCount=5)
    log_formatter = logging.Formatter('{asctime}: {levelname:8s} - {message}', style='{')
    handler.setFormatter(log_formatter)

    kiosk_logger.addHandler(handler)
    return kiosk_logger

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    LOGGER = get_logger()
    LOGGER.debug("Starting the APP.")
    UI = AppUI()
    sys.exit(APP.exec_())
