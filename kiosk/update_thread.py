#!/usr/bin/python3
""" Controls the timing of when to update the UI
    This is a thread so that the UI stays active and happy
"""
import time, datetime
from PyQt5 import QtCore

class UpdateThread(QtCore.QThread):
    """ This class runs and determines when to update the UI """
    update_clock = QtCore.pyqtSignal()
    update_person = QtCore.pyqtSignal()
    update_weather_and_clothes = QtCore.pyqtSignal()
    update_indoor = QtCore.pyqtSignal()
    update_moon = QtCore.pyqtSignal()
        
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True

    def run(self):
        """ main function for the thread. tells the UI when to update """
        # every 1 seconds update clock
        # every 10 seconds update indoor status
        # every 30 seconds switch person to view
        # every 5 minutes update weather
        # every hour check if day has changed, if yes check moon phase
        update_person_seconds = 30
        update_clock_seconds = 1
        update_weather_seconds = 300
        update_indoor_seconds = 10
        check_date_seconds = 3600

        current_date = datetime.date.today()

        i = 1
        while self.keep_going:
            if i % update_person_seconds == 0:
                self.update_person.emit()
            
            if i % update_weather_seconds == 0:
                self.update_weather_and_clothes.emit()

            if i % update_clock_seconds == 0:
                self.update_clock.emit()

            if i % update_indoor_seconds == 0:
                self.update_indoor.emit()

            if i % check_date_seconds == 0:
                if current_date != datetime.date.today():
                    self.update_moon.emit()
                
            i += 1
            time.sleep(1)
        # return

    def stop(self):
        """stops the thread and closes nicely"""
        self.keep_going = False
        self.wait()
        self.exit()
        return