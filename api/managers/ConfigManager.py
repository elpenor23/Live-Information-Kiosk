import json
import os
from managers.ErrorManager import ErrorManager

CONFIG_DIR = "/config/"
WEATHER_API_CONFIG_FILE = "weatherAPIConfig.json"
CLOTHING_CONFIG_FILE = "clothingConfig.json"
INTENSITY_CONFIG_FILE = "intensityConfig.json"
TEMP_ADJUSTMENT_CONFIG_FILE = "tempAdjustConfig.json"

class ConfigManager():
    def get_api_config_data():
        return get_config_data(CONFIG_DIR, WEATHER_API_CONFIG_FILE)
    
    def get_clothing_config_data():
        return get_config_data(CONFIG_DIR, CLOTHING_CONFIG_FILE)

    def get_intensity_config_data():
        return get_config_data(CONFIG_DIR, INTENSITY_CONFIG_FILE)

    def get_temperature_adjustment_config_data():
        return get_config_data(CONFIG_DIR, TEMP_ADJUSTMENT_CONFIG_FILE)

def get_config_data(dir, filename):
    #get path to parent directory aka root api directory
    pathname = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        
    return open_json_file(pathname + dir + filename)

def open_json_file(filename):
    """ Opens the passed in JSON config file read only and returns it as a python dictionary"""
    try:
        with open(filename, 'r') as config_file:
            config_data = json.load(config_file)
    except IOError as ex:
        error_text = "Could not read config file: " + filename
        ErrorManager.log_error("ConfigManager.open_json_file: " + error_text)
        return {"error": "Error opening config file."}
    else:
        return config_data