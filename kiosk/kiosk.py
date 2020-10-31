#!/usr/bin/python3
""" base application start """
import sys, os
import logging
import logging.handlers
from PyQt5.QtWidgets import QApplication
from ui_setup import AppUI


# def get_logger():
#     """ Initializes the logger for the entire program """
#     # Set up a specific logger with our desired output level
#     kiosk_logger = logging.getLogger('kiosk_log')
#     kiosk_logger.setLevel(logging.INFO)

#     # Add the log message handler to the logger
#     handler = logging.handlers.RotatingFileHandler(
#                 LOG_FILENAME, maxBytes=2000000, backupCount=5)
#     log_formatter = logging.Formatter('{asctime}: {levelname:8s} - {message}', style='{')
#     handler.setFormatter(log_formatter)

#     kiosk_logger.addHandler(handler)
#     return kiosk_logger

if __name__ == '__main__':
    APP = QApplication(sys.argv)
    UI = AppUI()
    sys.exit(APP.exec_())
