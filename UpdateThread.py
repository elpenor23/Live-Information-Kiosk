#!/usr/bin/python3
import time
from PyQt5 import QtCore

class UpdateThread(QtCore.QThread):
    updateClock = QtCore.pyqtSignal()
    updatePerson = QtCore.pyqtSignal()
    updateWeatherAndClothes = QtCore.pyqtSignal()
        
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True

    def run(self):
        # every 1s update clock
        # every 30 seconds switch person to view
        # every 5 minutes update weather
        updatePersonSeconds = 30
        updateClockSeconds = 1
        updateWeatherSeconds = 300
        i = 1
        while self.keep_going:
            if i % updatePersonSeconds == 0:
                self.updatePerson.emit()
            
            if i % updateWeatherSeconds == 0:
                self.updateWeatherAndClothes.emit()

            if i % updateClockSeconds == 0:
                self.updateClock.emit()
                
            i += 1
            time.sleep(1)
        # return

    def stop(self):
        self.keep_going = False
        self.wait()
        self.exit()
        return