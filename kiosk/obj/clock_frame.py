#!/usr/bin/python3
""" Frame used to display time and date """

import time, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from controllers.moon_phase_controller import MoonPhaseController

LABLESTYLE = "QLabel { color : white; font-size: 30px;}"
MOONPHASE_LABLESTYLE = "QLabel { color : white; font-size: 20px;}"
MOON_ICON_SIZE = 100

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
        self.moon_phase = QLabel()
        self.moon_phase.setStyleSheet(MOONPHASE_LABLESTYLE)
        self.moon_icon = QLabel()

        frame_layout.addWidget(self.time_label, 0, 0)
        frame_layout.addWidget(self.day_of_week_label, 1, 0)
        frame_layout.addWidget(self.date_label, 2, 0)
        frame_layout.addWidget(self.moon_phase, 3, 0)
        frame_layout.addWidget(self.moon_icon, 4, 0)

        self.setLayout(frame_layout)
        self.update_moon_phase()
        self.tick()

    def tick(self):
        """ Updates the date and time of the frame """
        self.time_label.setText(time.strftime('%I:%M:%S %p')) #hour in 12h format
        self.day_of_week_label.setText(time.strftime('%A'))
        self.date_label.setText(time.strftime("%b %-d %Y"))

    def update_moon_phase(self):
        moon_data = MoonPhaseController.get_moon_phase()
        if "phase_name" in moon_data:
            phase_text = moon_data["phase_name"]
            self.moon_phase.setText(phase_text)

            DIRNAME = os.path.dirname(__file__)       
            moon_icon = os.path.join(DIRNAME, "../assets/" + moon_data["phase_icon"] + ".png")
            image = QPixmap(moon_icon)
            small_image = image.scaled(MOON_ICON_SIZE,
                                        MOON_ICON_SIZE,
                                        QtCore.Qt.KeepAspectRatio,
                                        QtCore.Qt.FastTransformation)
            self.moon_icon.setPixmap(small_image)
        else:
            self.moon_phase.setText("Moon API Error!")
