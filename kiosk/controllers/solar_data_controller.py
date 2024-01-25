from lib.utils import open_config_file, get_api_data, API_CONFIG_FILE_NAME
from datetime import datetime

class SolarDataController():
    def get_solar_data():
        api_config = open_config_file(API_CONFIG_FILE_NAME)

        solar_data = get_api_data(api_config["local_solar_endpoint"], {})
        if "error" not in solar_data:
            processed_solar_data = SolarDataController.process_solar_data(solar_data)
        else:
            processed_solar_data = solar_data

        return processed_solar_data
    
    def process_solar_data(solar_data):
        if "maxPower" in solar_data:
            if solar_data["maxPower"] > 0:
                solar_data["percet_power_generated"] = round((solar_data["currentPower"]/solar_data["maxPower"]) * 100)
            else:
                solar_data["percet_power_generated"] = 0
        else:
            solar_data["maxPower"] = 10000
            solar_data["currentPower"] = 0
            solar_data["percet_power_generated"] = 0

        return solar_data
