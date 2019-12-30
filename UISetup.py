#!/usr/bin/python3
#Creates and sets up the GUI
#This is what controls all the GUI 
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)

from obj.WeatherFrame import Weather
from obj.RunningClothesFrame import RunningClothes
from obj.ClockFrame import Clock
from UpdateThread import UpdateThread
import time

class AppUI(QWidget):
    def __init__(self):
        super(AppUI, self).__init__()
        self.initUI()
          
    #####################################
    #Start - Build All section of the UI
    #####################################
    #Add all the sections to the main window 
    def initUI(self):
        windowLayout = QGridLayout()
        windowLayout.setAlignment(QtCore.Qt.AlignTop)
        self.weatherFrame = Weather("config/locationConfig.json")
        windowLayout.addWidget(self.weatherFrame, 0, 0)

        self.runningClothesFrame = RunningClothes("config/peopleConfig.json", "config/tempAdjustConfig.json", self.weatherFrame._weatherConfig)
        windowLayout.addWidget(self.runningClothesFrame, 1, 0)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        #Set the layout and window
        self.setLayout(windowLayout)
        self.move(300, 150)
        self.show()
        #start Fullscreen
        self.showFullScreen()

        # kick off the thread
        self.updateThread = UpdateThread()
        self.updateThread.updateClock.connect(self.callbackUpdateClock)
        self.updateThread.updateWeatherAndClothes.connect(self.callbackUpdateWeatherAndClothes)
        self.updateThread.updatePerson.connect(self.callbackUpdatePerson)
        self.updateThread.start()
    
    def callbackUpdateClock(self):
        self.weatherFrame.updateClock()
        return

    def callbackUpdatePerson(self):
        people = self.runningClothesFrame.runnerWidgetList
        numberOfpeople = len(people)
        j = 0
        indexToSetVisible = 0
        while j < numberOfpeople:
            if people[j].isVisible():
                people[j].setVisible(False)
                indexToSetVisible = j + 1
            j += 1

        if indexToSetVisible > numberOfpeople-1: indexToSetVisible = 0
        people[indexToSetVisible].setVisible(True)
        return

    def callbackUpdateWeatherAndClothes(self):
        self.weatherFrame.getWeatherData()
        self.weatherFrame.updateDisplay()
        return

    def keyPressEvent(self, e):
        if str(e.key()) == str(QtCore.Qt.Key_Escape):
            self.close()
        elif str(e.key()) == str(QtCore.Qt.Key_Return):
            if self.isFullScreen():
                self.showNormal()
                self.setGeometry(300, 150, 500, 500) 
            else:
                self.showFullScreen()