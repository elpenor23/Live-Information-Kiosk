# smartmirror.py
import sys
from PyQt5.QtWidgets import QApplication
from UISetup import AppUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = AppUI()
    sys.exit(app.exec_())
