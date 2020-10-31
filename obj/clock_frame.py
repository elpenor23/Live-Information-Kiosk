#!/usr/bin/python3
""" Frame used to display time and date """

import time
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout


LABLESTYLE = "QLabel { color : white; font-size: 30px;}"

class Clock(QFrame):
    """ class that defines the date and time frame"""
    def __init__(self):
        QFrame.__init__(self)
        self.setStyleSheet(LABLESTYLE)
        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self.time_label = QLabel()
        self.day_of_week_label = QLabel()
        self.date_label = QLabel()

        frame_layout.addWidget(self.time_label, 0, 0)
        frame_layout.addWidget(self.day_of_week_label, 1, 0)
        frame_layout.addWidget(self.date_label, 2, 0)

        self.setLayout(frame_layout)
        self.tick()

    def tick(self):
        """ Updates the date and time of the frame """
        self.time_label.setText(time.strftime('%I:%M:%S %p')) #hour in 12h format
        self.day_of_week_label.setText(time.strftime('%A'))
        self.date_label.setText(time.strftime("%b %-d %Y"))
