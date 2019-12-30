#!/usr/bin/python3
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton, QFrame, QApplication,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)
from PyQt5.QtGui import QIcon, QPixmap

from controllers.PeopleController import PeopleController
from obj.sunrise import sun
import json, os
from controllers.TemperatureAdjustmentController import TemperatureAdjustmentController
from controllers.ClothingController import ClothingController
from lib.utils import openConfigFile

lableStyle = "QLabel { color : white; font-size: 30px;} QGroupBox { color : white; font-size: 30px; font-weight: bold; margin-top: 1.5ex; border: 2px solid gray; border-radius: 3px; } QGroupBox::title { subcontrol-origin: margin;subcontrol-position: top left; /* position at the top center */ padding: 0 8px; font-weight: bold;}"
dirname = os.path.dirname(__file__)
clothingConfigFileName = os.path.join(dirname,"../config/clothingConfig.json")

class RunningClothes(QFrame):
    def __init__(self, peopleConfigFileName, tempAdjustConfigFileName, weatherConfigJSON):
        QFrame.__init__(self)
        self.setStyleSheet(lableStyle)
        self.runnerWidgetList = []
        frameLayout = QGridLayout()
        frameLayout.setAlignment(QtCore.Qt.AlignTop)

        tempAdjustConfig = openConfigFile(tempAdjustConfigFileName)

        peopleController = PeopleController(peopleConfigFileName)

        s = sun(lat=weatherConfigJSON["latitude"],long=weatherConfigJSON["longitude"])

        wind = self.getWind(weatherConfigJSON["currently"]["windSpeed"], tempAdjustConfig["wind_speed"])

        runnerRow = 1
        for runner in peopleController.people:
            runnerFrame = QFrame()
            runnerLayout = QGridLayout()
            runnerLayout.setAlignment(QtCore.Qt.AlignTop)
            runnerName = QLabel(runner["name"])
            runnerName.setStyleSheet("QLabel { color: green; font-size: 35px; font-weight: bold; text-decoration: underline;}")
            runnerLayout.addWidget(runnerName, 0, 0)
            col = 0
            row = 0
            # print("*********" + runner["name"] + "*************")
            for intensity in peopleController.intensities:
                tempAdjuster = TemperatureAdjustmentController(s.timeOfDay(), weatherConfigJSON["currently"]["icon"], wind, runner["gender"], runner["feel"], intensity["type"], weatherConfigJSON["currently"]["temperature"], tempAdjustConfig)
                cc = ClothingController(tempAdjuster.adjustedTemperature, clothingConfigFileName, runner["gender"], intensity["type"], weatherConfigJSON["currently"]["icon"], s.timeOfDay())
                clothes = cc.calculateItems()

                degree_sign= u'\N{DEGREE SIGN}'
                intensityFrame = QGroupBox(intensity["name"]) # + " - " + str(round(tempAdjuster.adjustedTemperature)) + degree_sign)
                intensityLayout = QGridLayout()
                intensityLayout.setAlignment(QtCore.Qt.AlignTop)

                # print(clothes)
                for bodyPart in clothes:
                    row += 1
                    item = QLabel(clothes[bodyPart])
                    intensityLayout.addWidget(item, row, 0)

                intensityFrame.setLayout(intensityLayout)
                runnerLayout.addWidget(intensityFrame, 1, col)
                col += 1

            runnerFrame.setLayout(runnerLayout)
            frameLayout.addWidget(runnerFrame, runnerRow, 0)
            self.runnerWidgetList.append(runnerFrame)
            runnerRow += 1
            if runnerRow != 2:
                runnerFrame.setVisible(False)

        self.setLayout(frameLayout)

    def getWind(self, windSpeed, windSpeedConfig):
        if windSpeedConfig["light_min"] <= windSpeed <= windSpeedConfig["light_max"]:
            return "light_wind"
        elif windSpeedConfig["wind_min"] <= windSpeed <= windSpeedConfig["wind_max"]:
            return "windy"
        elif windSpeedConfig["heavy_min"] <= windSpeed <= windSpeedConfig["heavy_max"]:
            return "heavy_wind"