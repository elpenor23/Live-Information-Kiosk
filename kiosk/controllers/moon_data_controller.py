from lib.utils import open_config_file, get_api_data, API_CONFIG_FILE_NAME, LOCATION_CONFIG_FILENAME
from datetime import datetime

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT_LONG = "%Y-%m-%dT%H:%M:%S%z"
TIME_FORMAT = "%-I:%M %p"
class MoonDataController():
    def get_moon_phase():
        api_config = open_config_file(API_CONFIG_FILE_NAME)
        location_config = open_config_file(LOCATION_CONFIG_FILENAME)

        moon_data = get_api_data(api_config["local_moon_phase_endpoint"], {"lat": location_config["latitude"], "lon": location_config["longitude"]})

        return moon_data
