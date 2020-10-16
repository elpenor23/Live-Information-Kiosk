#!/usr/bin/python3
""" Frame used to display time and date """

import requests
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from lib.utils import get_indoor_status


LABLESTYLE_INDOOR_OPEN = "QLabel { color : white; font-size: 30px; border: 3px solid white; background: green;}"
LABLESTYLE_INDOOR_INUSE = "QLabel { color : white; font-size: 30px; border: 3px solid white; background: red;}"
LABLESTYLE_INDOOR_UNKNOWN = "QLabel { color : black; font-size: 30px; border: 3px solid white; background: yellow;}"

LABLETEXT_INDOOR_OPEN = "Indoor Free"
LABLETEXT_INDOOR_INUSE = "Indoor In Use!"
LABLETEXT_INDOOR_UNKNOWN = "Indoor Unknown?"

class Indoor(QFrame):
    """ class that defines the date and time frame"""
    def __init__(self):
        QFrame.__init__(self)
        self.setStyleSheet(LABLESTYLE_INDOOR_UNKNOWN)
        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)

        self.in_use_label = QLabel(LABLETEXT_INDOOR_UNKNOWN)
        # self.day_of_week_label = QLabel()
        # self.date_label = QLabel()

        frame_layout.addWidget(self.in_use_label, 0, 0)
        # frame_layout.addWidget(self.day_of_week_label, 1, 0)
        # frame_layout.addWidget(self.date_label, 2, 0)

        self.setLayout(frame_layout)
        # self.tick()

    def update(self):
        """ Updates the status of the indoor """
        styleSheetToUse = LABLESTYLE_INDOOR_UNKNOWN
        testToUse = LABLETEXT_INDOOR_UNKNOWN

        indoor_status = get_indoor_status()

        if indoor_status.find("inuse") > -1:
            styleSheetToUse = LABLESTYLE_INDOOR_INUSE
            testToUse = LABLETEXT_INDOOR_INUSE
        elif indoor_status.find("open") > -1:
            testToUse = LABLETEXT_INDOOR_OPEN
            styleSheetToUse = LABLESTYLE_INDOOR_OPEN
        
        if indoor_status.find("old") > -1:
            testToUse += "**"

        self.setStyleSheet(styleSheetToUse)
        self.in_use_label.setText(testToUse)