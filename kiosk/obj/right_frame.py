#!/usr/bin/python3
""" Frame used to display time and date """

import time, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout, QProgressBar
from PyQt5.QtGui import QPixmap
from controllers.moon_data_controller import MoonDataController
from controllers.indoor_status_controller import IndoorStatusController

LABLESTYLE = "QLabel { color : white; font-size: 30px;}"
SPACERLABELSTYLE = "QLabel {font-size: 5px;}"
MOONPHASE_LABLESTYLE = "QLabel { color : white; font-size: 20px;}"

STATUSSTYLE_OFF = "QProgressBar {border: 4px solid red;border-radius: 5px;text-align: center;background-color: red;color: black;} QProgressBar::chunk {background-color: red;}"
STATUSSTYLE_LOW = "QProgressBar {border: 4px solid orange;border-radius: 5px;text-align: center;background-color: white;color: black;} QProgressBar::chunk {background-color: orange;}"
STATUSSTYLE_OK = "QProgressBar {border: 4px solid gold;border-radius: 5px;text-align: center;background-color: white;color: black;} QProgressBar::chunk {background-color: gold;}"
STATUSSTYLE_GOOD = "QProgressBar {border: 4px solid green;border-radius: 5px;text-align: center;background-color: white;color: black;} QProgressBar::chunk {background-color: green;}"
STATUSSTYLE_FULL_POWER = "QProgressBar {border: 4px solid purple;border-radius: 5px;text-align: center;background-color: white;color: black;} QProgressBar::chunk {background-color: purple;}"

MOON_ICON_SIZE = 100

class RightFrame(QFrame):
    """ class that defines the date and time frame"""
    def __init__(self):
        QFrame.__init__(self)
        self.setStyleSheet(LABLESTYLE)

        main_layout = QGridLayout()
        self.main_frame = QFrame()

        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)
        

        self.time_label = QLabel()
        self.day_of_week_label = QLabel()
        self.day_of_week_label.setStyleSheet(MOONPHASE_LABLESTYLE)
        self.date_label = QLabel()
        self.day_length_label = QLabel()
        self.day_length_label.setStyleSheet(MOONPHASE_LABLESTYLE)
        self.day_time_label = QLabel()
        self.day_time_label.setStyleSheet(MOONPHASE_LABLESTYLE)
        self.moon_phase = QLabel()
        self.moon_phase.setStyleSheet(MOONPHASE_LABLESTYLE)
        self.moon_icon = QLabel()

        self.status = QProgressBar()
        self.status.setStyleSheet(STATUSSTYLE_OK)
        self.status.setGeometry(0, 0, 2000, 10)
        self.status.setValue(0)
        self.status.setOrientation(QtCore.Qt.Vertical)
        
        frame_layout.addWidget(self.time_label, 0, 0)
        frame_layout.addWidget(self.day_of_week_label, 1, 0)
        frame_layout.addWidget(self.date_label, 2, 0)
        frame_layout.addWidget(self.day_time_label, 3, 0)
        frame_layout.addWidget(self.day_length_label, 4, 0)
        frame_layout.addWidget(self.moon_phase, 5, 0)
        frame_layout.addWidget(self.moon_icon, 6, 0)
        frame_layout.addWidget(self.status, 0, 1, 7, 1)

        self.main_frame.setLayout(frame_layout)
        main_layout.addWidget(self.main_frame)
        self.setLayout(main_layout)
        moon_data = MoonDataController.get_moon_phase()
        self.update_moon_data(moon_data)
        self.tick()

    def tick(self):
        """ Updates the date and time of the frame """
        self.time_label.setText(time.strftime('%-I:%M:%S %p')) #hour in 12h format
        self.day_of_week_label.setText(time.strftime('%A'))
        self.date_label.setText(time.strftime("%b %-d %Y"))

    def update_moon_data(self, moon_data):
        self.update_moon_phase(moon_data)
        self.update_date(moon_data)

    def update_solar_data(self, solar_data):
        self.update_solar_bar(solar_data["percet_power_generated"])

    def update_moon_phase(self, moon_data):                
        if "phaseName" in moon_data:
            self.moon_phase.setText(moon_data["phaseName"])

            DIRNAME = os.path.dirname(__file__)       
            moon_icon = os.path.join(DIRNAME, "../assets/" + moon_data["phaseIcon"] + ".png")
            image = QPixmap(moon_icon)
            small_image = image.scaled(MOON_ICON_SIZE,
                                        MOON_ICON_SIZE,
                                        QtCore.Qt.KeepAspectRatio,
                                        QtCore.Qt.FastTransformation)
            self.moon_icon.setPixmap(small_image)
        else:
            self.moon_phase.setText("Moon API Error!")

    def update_date(self, data):
        if IndoorStatusController.has_indoor():
            self.day_time_label.hide()
            self.date_label.show()
        else:
            self.day_time_label.show()
            self.date_label.hide()

        if "dayLength" in data:
            self.day_length_label.setText(data["dayLength"])
            
        if "dayTimeFormatted" in data:
            self.day_time_label.setText(data["dayTimeFormatted"])

    def update_solar_bar(self, percent_power):
        style_to_use = STATUSSTYLE_OFF

        if percent_power > 0 and percent_power < 33:
            style_to_use = STATUSSTYLE_LOW
        if percent_power >= 33 and percent_power < 66:
            style_to_use = STATUSSTYLE_OK
        if percent_power >= 66 and percent_power < 100:
            style_to_use = STATUSSTYLE_GOOD
        if percent_power >= 100:
            style_to_use = STATUSSTYLE_FULL_POWER

        #just to make sure we do not break the status bar
        #it would be cool if the number could go over 100 
        # but it can not.
        if percent_power > 100:
            percent_power = 100

        self.status.setStyleSheet(style_to_use)
        self.status.setValue(percent_power)