#!/usr/bin/python3
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton, QFrame, QApplication,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)
from PyQt5.QtGui import QIcon, QPixmap

from controllers.PeopleController import PeopleController
from obj.sunrise import sun
import json
from controllers.TemperatureAdjustmentController import TemperatureAdjustmentController
from controllers.ClothingController import ClothingController

lableStyle = "QLabel { color : white; }"

class RunningClothes(QFrame):
    def __init__(self, peopleConfigFileName, tempAdjustConfigFileName, weatherConfigJSON):
        QFrame.__init__(self)
        self.setFrameStyle(QFrame.Panel);
        self.setStyleSheet(lableStyle)
        frameLayout = QGridLayout()
        frameLayout.setAlignment(QtCore.Qt.AlignTop)
 
        tempAdjustConfig = self.openConfigFile(tempAdjustConfigFileName)

        peopleController = PeopleController(peopleConfigFileName)

        s = sun(lat=weatherConfigJSON["latitude"],long=weatherConfigJSON["longitude"])

        wind = self.getWind(weatherConfigJSON["currently"]["windSpeed"], tempAdjustConfig["wind_speed"])
        
        runnerRow = 1
        for runner in peopleController.people:
            runnerFrame = QFrame()
            runnerLayout = QGridLayout()
            runnerLayout.setAlignment(QtCore.Qt.AlignTop)
            runnerName = QLabel(runner["name"])
            runnerLayout.addWidget(runnerName, 0, 0)
            col = 0
            row = 0
            for intensity in peopleController.intensities:
                tempAdjuster = TemperatureAdjustmentController(s.timeOfDay(), weatherConfigJSON["currently"]["icon"], wind, runner["gender"], runner["feel"], intensity, weatherConfigJSON["currently"]["temperature"], tempAdjustConfig)
                cc = ClothingController(tempAdjuster.adjustedTemperature, "config/clothingConfig.json", runner["gender"], intensity, weatherConfigJSON["currently"]["icon"], s.timeOfDay())
                clothes = cc.calculateItems()

                intensityFrame = QGroupBox(intensity)
                intensityLayout = QGridLayout()
                intensityLayout.setAlignment(QtCore.Qt.AlignTop)
                
                #print(clothes)
                for bodyPart in clothes:
                    row += 1
                    item = QLabel(clothes[bodyPart])
                    intensityLayout.addWidget(item, row, 0)

                intensityFrame.setLayout(intensityLayout)
                runnerLayout.addWidget(intensityFrame, 1, col)
                col += 1

            runnerFrame.setLayout(runnerLayout)
            frameLayout.addWidget(runnerFrame, runnerRow, 0)
            runnerRow += 1
            if runnerRow == 2:
                runnerFrame.setVisible(False)

        self.setLayout(frameLayout)

    def getWind(self, windSpeed, windSpeedConfig):
        if windSpeedConfig["light_min"] <= windSpeed <= windSpeedConfig["light_max"]:
            return "light_wind"
        elif windSpeedConfig["wind_min"] <= windSpeed <= windSpeedConfig["wind_max"]:
            return "windy"
        elif windSpeedConfig["heavy_min"] <= windSpeed <= windSpeedConfig["heavy_max"]:
            return "heavy_wind"

    def openConfigFile(self, configFileName):
        try:
            configFile = open(configFileName, 'r')
        except IOError as ex:
            errorText = "Could not read config file: " + configFileName
            print(errorText)
            print(ex)
            sys.exit()

        #get the data
        configData = json.loads(configFile.read())
        configFile.close
        return configData       



