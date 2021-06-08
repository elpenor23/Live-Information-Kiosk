from PyQt5 import QtCore
from datetime import datetime
from lib.utils import get_api_data, open_config_file, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME

class APIThread(QtCore.QThread):
    get_data = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True
        self.run_weather = False
        self.run_indoor_status = False
        self.config_data = open_config_file(API_CONFIG_FILE_NAME)
        self.location_config = open_config_file(LOCATION_CONFIG_FILENAME)

    def run(self):
        while self.keep_going:
            if self.run_indoor_status or self.run_weather:
                self.run_api()

    def run_api(self):
        data = {}
        if self.run_indoor_status:
            # print("Hitting INDOOR API")
            self.run_indoor_status = False
            data["api"] = "indoor_status"
            data["return"] = get_api_data(self.config_data["local_indoor_status_endpoint"], {})
        elif self.run_weather:
            # print("Hitting WEATHER API")
            self.run_weather = False
            data["api"] = "weather"
            data["return"] = get_weather_from_local_api(self.config_data["local_weather_endpoint"], self.location_config["latitude"], self.location_config["longitude"])

        self.get_data.emit(data)

    def run_this(self, api):
        if api == "indoor_status":
            self.run_indoor_status = True
        elif api == "weather":
            self.run_weather = True

        self.api_ready = True

    def stop(self):
        self.keep_going = False
        self.wait()
        self.exit()
        return

def get_weather_from_local_api(local_api_weather_endpoint, lat, lon):
    params = {
        'lat': lat,
        'lon': lon,
    }

    json_results = get_api_data(local_api_weather_endpoint, params)

    return json_results