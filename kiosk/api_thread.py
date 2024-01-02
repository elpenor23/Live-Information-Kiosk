from PyQt5 import QtCore
from controllers.moon_data_controller import MoonDataController
from controllers.weather_controller import WeatherController
from controllers.indoor_status_controller import IndoorStatusController
from controllers.solar_data_controller import SolarDataController

class APIThread(QtCore.QThread):
    get_data = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True
        self.things_to_run = []

    def run(self):
        while self.keep_going:
            if len(self.things_to_run) > 0:
                self.run_api(self.things_to_run[0])
                self.things_to_run.pop(0)

    def run_api(self, item_to_run):
        data = {}
        data["api"] = item_to_run
        if item_to_run == "indoor_status":
            # print("Hitting INDOOR API")
            data["return"] = IndoorStatusController.get_indoor_status()
        elif item_to_run == "weather":
            # print("Hitting WEATHER API")
            data["return"] = WeatherController.get_weather_data()
        elif item_to_run == "moon":
            # print("Hitting MOON API")
            data["return"] = MoonDataController.get_moon_phase()
        elif item_to_run == "solar":
            # print("Hitting SOLAR API")
            data["return"] = SolarDataController.get_solar_data()

        self.get_data.emit(data)

    def run_this(self, api):
        self.things_to_run.append(api)

    def stop(self):
        self.keep_going = False
        self.wait()
        self.exit()
        return


