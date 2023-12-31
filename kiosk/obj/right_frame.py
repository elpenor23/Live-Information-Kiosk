#!/usr/bin/python3
""" Frame used to display time and date """

import time, os
from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from controllers.moon_data_controller import MoonDataController
from controllers.indoor_status_controller import IndoorStatusController

LABLESTYLE = "QLabel { color : white; font-size: 30px;}"
SPACERLABELSTYLE = "QLabel {font-size: 5px;}"
MOONPHASE_LABLESTYLE = "QLabel { color : white; font-size: 20px;}"
MOON_ICON_SIZE = 100

class RightFrame(QFrame):
    """ class that defines the date and time frame"""
    def __init__(self):
        QFrame.__init__(self)
        self.setStyleSheet(LABLESTYLE)

        main_layout = QGridLayout()
        self.main_frame = QFrame()
        #self.main_frame.setStyleSheet("border: 1px solid white;")

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
        
        frame_layout.addWidget(self.time_label, 0, 0)
        frame_layout.addWidget(self.day_of_week_label, 1, 0)
        frame_layout.addWidget(self.date_label, 2, 0)
        frame_layout.addWidget(self.day_time_label, 3, 0)
        frame_layout.addWidget(self.day_length_label, 6, 0)
        frame_layout.addWidget(self.moon_phase, 8, 0)
        frame_layout.addWidget(self.moon_icon, 9, 0)

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

    def update_date(self, moon_data):
        if IndoorStatusController.has_indoor():
            self.day_time_label.hide()
            self.date_label.show()
        else:
            self.day_time_label.show()
            self.date_label.hide()

        if "dayLength" in moon_data:
            self.day_length_label.setText(moon_data["dayLength"])
            
        if "dayTimeFormatted" in moon_data:
            self.day_time_label.setText(moon_data["dayTimeFormatted"])
