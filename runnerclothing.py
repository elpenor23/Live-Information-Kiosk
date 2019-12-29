# smartmirror.py
import sys
from PyQt5.QtWidgets import QApplication
from UISetup import SmartMirrorUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = SmartMirrorUI()
    sys.exit(app.exec_())
