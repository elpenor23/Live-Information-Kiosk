#!/usr/bin/python3
""" Controls the timing of when to update the UI
    This is a thread so that the UI stays active and happy
"""
import time
import logging
from PyQt5 import QtCore

class UpdateThread(QtCore.QThread):
    """ This class runs and determines when to update the UI """
    update_clock = QtCore.pyqtSignal()
    update_person = QtCore.pyqtSignal()
    update_weather_and_clothes = QtCore.pyqtSignal()
        
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True

    def run(self):
        """ main function for the thread. tells the UI when to update """
        self.logger = logging.getLogger('kioskLog')
        
        # every 1s update clock
        # every 30 seconds switch person to view
        # every 5 minutes update weather
        update_person_seconds = 30
        update_clock_seconds = 1
        update_weather_seconds = 300
        i = 1
        while self.keep_going:
            if i % update_person_seconds == 0:
                self.update_person.emit()
                self.logger.debug("emitting to update person.")
            
            if i % update_weather_seconds == 0:
                self.update_weather_and_clothes.emit()
                self.logger.debug("Emmitting to update weather and clothes.")

            if i % update_clock_seconds == 0:
                self.update_clock.emit()
                self.logger.debug("Emitting to update clock.")
                
            i += 1
            time.sleep(1)
        # return

    def stop(self):
        """stops the thread and closes nicely"""
        self.keep_going = False
        self.wait()
        self.exit()
        return