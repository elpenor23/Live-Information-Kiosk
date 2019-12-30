#!/usr/bin/python3
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton, QFrame, QApplication,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)
from PyQt5.QtGui import QIcon, QPixmap
import os, time
from controllers.WeatherController import WeatherController
from obj.ClockFrame import Clock
lableStyle = "QLabel { color : white; font-size: 30px;}"

class Weather(QFrame):
    def __init__(self, weatherConfig):
        QFrame.__init__(self)

        overallLayout = QGridLayout()
        overallLayout.setAlignment(QtCore.Qt.AlignTop)

        weatherArea = QFrame()
        weatherArea.setStyleSheet(lableStyle)

        frameLayout = QGridLayout()
        frameLayout.setAlignment(QtCore.Qt.AlignTop)
        frameLayout.setAlignment(QtCore.Qt.AlignLeft)

        self.degreeFrm = QFrame(self)
        self.temperatureLbl = QLabel(self.degreeFrm)
        self.iconLbl = QLabel(self.degreeFrm)
        self.currentlyLbl = QLabel(self)
        self.forecastLbl = QLabel(self)
        self.locationLbl = QLabel(self)
        self.weatherConfig = weatherConfig
        self.getWeatherData()
        self.updateDisplay()
        
        frameLayout.addWidget(self.iconLbl, 0, 0, 5, 1)
        frameLayout.addWidget(self.degreeFrm, 0, 1)
        frameLayout.addWidget(self.temperatureLbl, 1, 1)
        frameLayout.addWidget(self.currentlyLbl, 2, 1)
        frameLayout.addWidget(self.locationLbl, 3, 1)
        frameLayout.addWidget(self.forecastLbl, 4, 1)
        

        weatherArea.setLayout(frameLayout)
        overallLayout.addWidget(weatherArea, 0, 0, QtCore.Qt.AlignLeft)

        self.clockFrame = Clock()
        overallLayout.addWidget(self.clockFrame, 0, 0, QtCore.Qt.AlignRight)

        self.setLayout(overallLayout)

    def getWeatherData(self):
        self.wc = WeatherController(self.weatherConfig)
        self.wc.parse_weather()
        self._weatherConfig = self.wc._weather_obj

    def updateDisplay(self):
        if self.wc.weatherIcon is not None:
            image = QPixmap(self.wc.weatherIcon)
            small_image = image.scaled(200, 200, QtCore.Qt.KeepAspectRatio, QtCore.Qt.FastTransformation)
            self.iconLbl.setPixmap(small_image)
        else:
            # remove image
            self.iconLbl.setPixmap(None)

        self.currentlyLbl.setText("Current Temp: " + self.wc.currentTempFormatted)
        self.forecastLbl.setText(self.wc.forecastText)
        self.temperatureLbl.setText(self.wc.summaryText)

        self.locationLbl.setText(self.wc.location)

    def updateClock(self):
        self.clockFrame.tick()
