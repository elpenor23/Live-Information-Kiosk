from PyQt5 import QtCore
from lib.utils import get_api_data, open_config_file, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME
from controllers.moon_data_controller import MoonDataController
from controllers.weather_controller import WeatherController
from controllers.indoor_status_controller import IndoorStatusController

class APIThread(QtCore.QThread):
    get_data = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True
        self.run_weather = False
        self.run_indoor_status = False
        self.run_moon = False
        self.config_data = open_config_file(API_CONFIG_FILE_NAME)
        self.location_config = open_config_file(LOCATION_CONFIG_FILENAME)

    def run(self):
        while self.keep_going:
            if self.run_indoor_status or self.run_weather or self.run_moon:
                self.run_api()

    def run_api(self):
        data = {}
        if self.run_indoor_status:
            # print("Hitting INDOOR API")
            self.run_indoor_status = False
            data["api"] = "indoor_status"
            data["return"] = IndoorStatusController.get_indoor_status()
        elif self.run_weather:
            # print("Hitting WEATHER API")
            self.run_weather = False
            data["api"] = "weather"
            data["return"] = WeatherController.get_weather_data()
        elif self.run_moon:
            # print("Hitting MOON API")
            self.run_moon = False
            data["api"] = "moon"
            data["return"] = MoonDataController.get_moon_phase()

        self.get_data.emit(data)

    def run_this(self, api):
        if api == "indoor_status":
            self.run_indoor_status = True
        elif api == "weather":
            self.run_weather = True
        elif api == "moon":
            self.run_moon = True

        self.api_ready = True

    def stop(self):
        self.keep_going = False
        self.wait()
        self.exit()
        return


