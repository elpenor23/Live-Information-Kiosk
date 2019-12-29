#!/usr/bin/python3
#Creates and sets up the GUI
#This is what controls all the GUI 
from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import (QWidget, QProgressBar, QLabel, QLineEdit, QRadioButton,
            QPlainTextEdit, QGridLayout, QGroupBox, QCheckBox, QPushButton, QSizePolicy, QDial)

from obj.WeatherFrame import Weather
from obj.RunningClothesFrame import RunningClothes

class SmartMirrorUI(QWidget):
    def __init__(self):
        super(SmartMirrorUI, self).__init__()
        self.initUI()
          
    #####################################
    #Start - Build All section of the UI
    #####################################
    #Add all the sections to the main window 
    def initUI(self):
        # self.tk.bind("<Return>", self.toggle_fullscreen)
        # self.tk.bind("<Escape>", self.end_fullscreen)
        windowLayout = QGridLayout()
        windowLayout.setAlignment(QtCore.Qt.AlignTop)
        weatherFrame = Weather("config/weatherConfig.json")
        windowLayout.addWidget(weatherFrame, 0, 0)

        runningClothesFrame = RunningClothes("config/peopleConfig.json", "config/tempAdjustConfig.json", weatherFrame._weatherConfig)
        windowLayout.addWidget(runningClothesFrame, 1, 0)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.black)
        self.setPalette(p)

        #Set the layout and window
        self.setLayout(windowLayout)
        self.move(300, 150)
        # self.setFixedSize(500, 500) #should be fullscreen
        self.setWindowTitle("This should eventuallt be invisible!")    
        self.show()

    def keyPressEvent(self, e):
        if str(e.key()) == str(QtCore.Qt.Key_Escape):
            self.showNormal()
            self.setGeometry(300, 150, 500, 500)  
            # self.move(300, 150)
        elif str(e.key()) == str(QtCore.Qt.Key_Return):
            self.showFullScreen()