#!/usr/bin/python3
""" base application start """
import sys
from PyQt5.QtWidgets import QApplication
from ui_setup import AppUI


if __name__ == '__main__':
    APP = QApplication(sys.argv)
    UI = AppUI()
    sys.exit(APP.exec_())
