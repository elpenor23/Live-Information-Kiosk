from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton, QFrame, QApplication,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)
import time

lableStyle = "QLabel { color : white; font-size: 30px;}"

class Clock(QFrame):
    def __init__(self):
        QFrame.__init__(self)
        self.setStyleSheet(lableStyle)
        frameLayout = QGridLayout()
        frameLayout.setAlignment(QtCore.Qt.AlignTop)

        self.timeLbl = QLabel()
        self.dayOWLbl = QLabel()
        self.dateLbl = QLabel()

        frameLayout.addWidget(self.timeLbl, 0,0)
        frameLayout.addWidget(self.dayOWLbl, 1,0)
        frameLayout.addWidget(self.dateLbl, 2,0)

        self.setLayout(frameLayout)
        self.tick()

    def tick(self):
        self.timeLbl.setText(time.strftime('%I:%M:%S %p')) #hour in 12h format
        self.dayOWLbl.setText(time.strftime('%A'))
        self.dateLbl.setText(time.strftime("%b %-d %Y"))