#!/usr/bin/python3
""" Controls the timing of when to update the UI
    This is a thread so that the UI stays active and happy
"""
import time, datetime
from PyQt5 import QtCore
from api_thread import APIThread
from lib.utils import THREAD_CONFIG_FILENAME, open_config_file

class UpdateThread(QtCore.QThread):
    """ This class runs and determines when to update the UI """

    update_data = QtCore.pyqtSignal(dict)
    update_signal = QtCore.pyqtSignal(str)
        
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True
        self.api_thread = APIThread()
        self.api_thread.get_data.connect(self.thread_callback_return)
        self.api_thread.start()

    def run(self):
        """ main function for the thread. tells the UI when to update """       
        config = open_config_file(THREAD_CONFIG_FILENAME)
        update_person_seconds = config["update_person_seconds"]
        update_clock_seconds = config["update_clock_seconds"]
        update_weather_seconds = config["update_weather_seconds"]
        update_indoor_seconds = config["update_indoor_seconds"]
        check_date_seconds = config["check_date_seconds"]
        check_solar_seconds = config["check_solar_in_seconds"]

        seconds = 1

        #TODO: ON API ERROR PAUSE AND WAIT INSTEAD OF CONSTANTLY HITTING THE API
        while self.keep_going:
            # print("i = " + str(i) + " @ " + str(datetime.datetime.now()))
            
            #just emit things
            if seconds % update_clock_seconds == 0:
                self.update_signal.emit("clock")
            
            if seconds % update_person_seconds == 0:
                self.update_signal.emit("person")
            
            #hit API to get data
            if seconds % check_date_seconds == 0:
                # print("Calling api thread for: moon @ " + str(datetime.datetime.now()))
                self.api_thread.run_this("moon")  

            if (seconds % update_weather_seconds == 0) or seconds == 1:
                # print("Calling api thread for: weather @ " + str(datetime.datetime.now()))
                self.api_thread.run_this("weather")          

            if seconds % update_indoor_seconds == 0:
                # print("Calling api thread for: indoor_status @ " + str(datetime.datetime.now()))
                self.api_thread.run_this("indoor_status")

            if seconds % check_solar_seconds == 0:
                #print("Calling api thread for: solar @ " + str(datetime.datetime.now()))
                self.api_thread.run_this("solar")  

            #make sure we do not overflow int
            if seconds < 10800:
                seconds += 1
            else:
                seconds = 1
            
            #sleep 1 second and then do it all over again
            time.sleep(1) 

        return

    def stop(self):
        """stops the thread and closes nicely"""
        self.keep_going = False
        self.wait()
        self.exit()
        return

    def thread_callback_return(self, data):
        # print("results returned for: " + data["api"] + " @ " + str(datetime.datetime.now()))
        self.update_data.emit(data)

        return