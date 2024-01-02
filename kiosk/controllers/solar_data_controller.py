from lib.utils import open_config_file, get_api_data, API_CONFIG_FILE_NAME
from datetime import datetime

class SolarDataController():
    def get_solar_data():
        api_config = open_config_file(API_CONFIG_FILE_NAME)

        solar_data = get_api_data(api_config["local_solar_endpoint"], {})

        processed_solar_data = SolarDataController.process_solar_data(solar_data)
        return solar_data
    
    def process_solar_data(solar_data):
        solar_data["percet_power_generated"] = round((solar_data["currentPower"]/solar_data["maxPower"]) * 100)
