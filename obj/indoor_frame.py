#!/usr/bin/python3
""" Frame used to display time and date """

import os
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
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
        
        self.wifi_icon_label = QLabel()
        self.ble_icon_label = QLabel()
        
        frame_layout.addWidget(self.in_use_label, 0, 0)
        frame_layout.addWidget(self.wifi_icon_label, 0, 1)
        frame_layout.addWidget(self.ble_icon_label, 0, 2)

        self.setLayout(frame_layout)
        self.setup_icons()
        self.manage_icons("XX")
    def update(self):
        """ Updates the status of the indoor """
        styleSheetToUse = LABLESTYLE_INDOOR_UNKNOWN
        testToUse = LABLETEXT_INDOOR_UNKNOWN

        indoor_status = get_indoor_status()

        if indoor_status.find("B") > -1 or indoor_status.find("W") > -1:
            styleSheetToUse = LABLESTYLE_INDOOR_INUSE
            testToUse = LABLETEXT_INDOOR_INUSE
        else:
            testToUse = LABLETEXT_INDOOR_OPEN
            styleSheetToUse = LABLESTYLE_INDOOR_OPEN
        
        if indoor_status.find("old") > -1:
            testToUse += "**"

        self.manage_icons(indoor_status)
        self.setStyleSheet(styleSheetToUse)
        self.in_use_label.setText(testToUse)

    def setup_icons(self):
        DIRNAME = os.path.dirname(__file__)
        icon_size = 40
        
        wifi_icon = os.path.join(DIRNAME, "../assets/wifi.png")
        ble_icon = os.path.join(DIRNAME, "../assets/bluetooth.png")

        image = QPixmap(wifi_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.wifi_icon_label.setPixmap(small_image)

        image = QPixmap(ble_icon)
        small_image = image.scaled(icon_size,
                                icon_size,
                                QtCore.Qt.KeepAspectRatio,
                                QtCore.Qt.FastTransformation)
        self.ble_icon_label.setPixmap(small_image)

    def manage_icons(self, indoor_status):
        if indoor_status.find("W") > -1:
            self.wifi_icon_label.show()
        else:
            self.wifi_icon_label.hide()

        if indoor_status.find("B") > -1:
            self.ble_icon_label.show()
        else:
            self.ble_icon_label.hide()