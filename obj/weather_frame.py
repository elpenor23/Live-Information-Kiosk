#!/usr/bin/python3
""" Frame used to display weather """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from obj.clock_frame import Clock

LABLESTYLE = "QLabel { color : white; font-size: 30px;}"

class Weather(QFrame):
    """ This is the frame that holds the weather and clock information """
    def __init__(self, weather_controller):
        """ initializing the frame """
        QFrame.__init__(self)

        overall_layout = QGridLayout()
        overall_layout.setAlignment(QtCore.Qt.AlignTop)

        weather_area = QFrame()
        weather_area.setStyleSheet(LABLESTYLE)

        frame_layout = QGridLayout()
        frame_layout.setAlignment(QtCore.Qt.AlignTop)
        frame_layout.setAlignment(QtCore.Qt.AlignLeft)

        self.degree_frame = QFrame(self)
        self.temperature_label = QLabel(self.degree_frame)
        self.icon_label = QLabel(self.degree_frame)
        self.currently_label = QLabel()
        self.forecast_label = QLabel()
        self.location_label = QLabel()

        frame_layout.addWidget(self.icon_label, 0, 0, 5, 1)
        frame_layout.addWidget(self.degree_frame, 0, 1)
        frame_layout.addWidget(self.temperature_label, 1, 1)
        frame_layout.addWidget(self.currently_label, 2, 1)
        frame_layout.addWidget(self.location_label, 3, 1)
        frame_layout.addWidget(self.forecast_label, 4, 1)

        weather_area.setLayout(frame_layout)
        overall_layout.addWidget(weather_area, 0, 0, QtCore.Qt.AlignLeft)

        self.clock_frame = Clock()
        overall_layout.addWidget(self.clock_frame, 0, 0, QtCore.Qt.AlignRight)

        self.setLayout(overall_layout)

        # everything is setup now update the weather!
        self.update_display(weather_controller)

    def update_display(self, weather_controller):
        """ Updates the weather Ifon and all the weather data """
        if weather_controller.weather_icon is not None:
            image = QPixmap(weather_controller.weather_icon)
            small_image = image.scaled(200,
                                       200,
                                       QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.FastTransformation)
            self.icon_label.setPixmap(small_image)
        else:
            # remove image
            self.icon_label.setPixmap(None)

        self.currently_label.setText("Current Temp: " + weather_controller.current_temp_formatted)
        self.forecast_label.setText(weather_controller.forecast_text)
        self.temperature_label.setText(weather_controller.summary_text)

        self.location_label.setText(weather_controller.location)

    def update_clock(self):
        """ Tells the clock to update itself """
        self.clock_frame.tick()
