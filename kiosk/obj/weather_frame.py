#!/usr/bin/python3
""" Frame used to display weather """

from PyQt5 import QtCore
from PyQt5.QtWidgets import QLabel, QFrame, QGridLayout
from PyQt5.QtGui import QPixmap
from obj.clock_frame import Clock
from obj.indoor_frame import Indoor
from datetime import datetime, timedelta

LABLESTYLE = "QLabel { color : white; font-size: 30px;}"
SMALL_LABELSTYLE = "QLabel {font-size: 20px;}"
WEATHER_ICON_SIZE = 200

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

        self.temperature_label = QLabel()
        self.temperature_label.setStyleSheet(SMALL_LABELSTYLE)

        self.icon_label = QLabel()
        self.icon_label.setFixedWidth(WEATHER_ICON_SIZE)
        self.icon_label.setFixedHeight(WEATHER_ICON_SIZE)
        self.icon_label.setScaledContents(True)
        
        self.currently_label = QLabel()
        self.error_label = QLabel()
        self.error_label.setStyleSheet(SMALL_LABELSTYLE)
        self.error_label.setVisible(False)
        
        self.comfort_icon_label = QLabel()
        self.forecast_label = QLabel()
        self.forecast_label.setStyleSheet(SMALL_LABELSTYLE)
        self.location_label = QLabel()

        frame_layout.addWidget(self.icon_label, 0, 0, 5, 1)

        frame_layout.addWidget(self.currently_label, 0, 1)
        frame_layout.addWidget(self.comfort_icon_label, 0, 2, QtCore.Qt.AlignLeft)
        frame_layout.addWidget(self.error_label, 1, 1, QtCore.Qt.AlignTop)
        frame_layout.addWidget(self.location_label, 2, 1)
        frame_layout.addWidget(self.temperature_label, 3, 1)
        frame_layout.addWidget(self.forecast_label, 4, 1)

        weather_area.setLayout(frame_layout)
        overall_layout.addWidget(weather_area, 0, 0, QtCore.Qt.AlignLeft)

        self.indoor_frame = Indoor()
        overall_layout.addWidget(self.indoor_frame, 0, 1, QtCore.Qt.AlignRight)

        self.clock_frame = Clock()
        overall_layout.addWidget(self.clock_frame, 0, 2, QtCore.Qt.AlignRight)

        self.setLayout(overall_layout)

        # everything is setup now update the weather!
        self.update_display(weather_controller)

    def update_display(self, weather_controller):
        """ Updates the weather and all the weather data """
        if weather_controller.weather_icon is not None:
            image = QPixmap(weather_controller.weather_icon)
            self.icon_label.setPixmap(image)

        self.currently_label.setText("Current Temp: " + weather_controller.current_temp_formatted + "( " + weather_controller.current_feels_like_formatted + ")")
        
        ten_minutes_ago = (datetime.now() - timedelta(minutes=10))

        #if our weather is over ten minutes old show an error to the user
        if weather_controller.current_weather_time < ten_minutes_ago:
            self.error_label.setVisible(True)
            self.error_label.setText(weather_controller.weather_time_formatted)
        else:
            self.error_label.setVisible(False)

        self.forecast_label.setText(weather_controller.forecast_text)
        self.temperature_label.setText(weather_controller.summary_text)

        self.location_label.setText(weather_controller.location)

        comfot_icon_size = 30
        if weather_controller.comfort_icon is not None:
            image = QPixmap(weather_controller.comfort_icon)
            small_image = image.scaled(comfot_icon_size,
                                       comfot_icon_size,
                                       QtCore.Qt.KeepAspectRatio,
                                       QtCore.Qt.FastTransformation)
            self.comfort_icon_label.setPixmap(small_image)

    def update_clock(self):
        """ Tells the clock to update itself """
        self.clock_frame.tick()

    def update_moon(self):
        """ Tells the moon to update itself """
        self.clock_frame.update_moon_phase()
        #self.indoor_frame.updateDate()

    def update_indoor_status(self, data):
        """ tells the indoor to update it's status """
        self.indoor_frame.update(data)
