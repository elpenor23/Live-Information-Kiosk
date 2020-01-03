""" Utils for getting data from api and opening config files """
from datetime import datetime
import json
import traceback
import os
import requests

DIRNAME = os.path.dirname(__file__)
API_CONFIG_FILE_NAME = os.path.join(DIRNAME, "../config/apiConfig.json")

def get_weather(lat, lon):
    """Gets the weather from the api in the apiConfig File"""

    config_data = open_config_file(API_CONFIG_FILE_NAME)
    weather_req_url = config_data["weather_req_url"]
    weather_api_token = config_data["weather_api_token"]
    weather_lang = config_data["weather_lang"]
    weather_unit = config_data["weather_unit"]
    weather_exclude_list = config_data["weather_exclude_list"]
    try:
        # get weather
        debug = False
        if debug:
            # this is here to make it easy to be sure
            # that we are hitting the api as little as possible
            # for free we only get 1000 calls a day (1 every 1.5 minutes)
            # so we do not want an error that uses them all up on us
            now = datetime.now()
            dt_string = now.strftime("%m/%d/%Y %H:%M:%S")
            print(dt_string + " - Getting Weather From API!")

        weather_req_url = weather_req_url % (weather_api_token,
                                             lat,
                                             lon,
                                             weather_lang,
                                             weather_unit,
                                             weather_exclude_list)
        request = requests.get(weather_req_url)
        return json.loads(request.text)
    except Exception:
        traceback.print_exc()
        error_text = "Error Could not get weather."
        print(error_text)

def open_config_file(config_filename):
    """ Opens the passed in JSON config file read only and returns it as a python dictionary"""

    try:
        with open(config_filename, 'r') as config_file:
            config_data = json.load(config_file)
    except IOError:
        error_text = "Could not read config file: " + config_filename
        print(error_text)
    else:
        return config_data
