from PyQt5 import QtCore
from datetime import time
from lib.utils import get_api_data, open_config_file, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME

class APIThread(QtCore.QThread):
    get_data = QtCore.pyqtSignal(dict)

    def __init__(self):
        QtCore.QThread.__init__(self)
        self.keep_going = True
        self.api_ready = False
        self.api_to_run = ""
        self.config_data = open_config_file(API_CONFIG_FILE_NAME)
        self.location_config = open_config_file(LOCATION_CONFIG_FILENAME)

    def run(self):
        while self.keep_going:
            if self.api_ready:
                self.run_api(self.api_to_run)

    def run_api(self, api_to_run):
        data = {"api": api_to_run}
        #reset things immediately so we do not end up here twice
        self.api_ready = False
        self.api_to_run = ""

        if api_to_run == "indoor_status":
            data["return"] = get_api_data(self.config_data["local_indoor_status_endpoint"], {})
        elif api_to_run == "weather":
            data["return"] = get_weather_from_local_api(self.config_data["local_weather_endpoint"], self.location_config["latitude"], self.location_config["longitude"])

        self.get_data.emit(data)

    def run_this(self, api):
        self.api_to_run = api
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